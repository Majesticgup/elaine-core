#!/usr/bin/env python3
"""Zero-credit Elaine Core v0.1 install verifier.

Run from the package root:
    python verify_install.py
    python verify_install.py --json
    python verify_install.py --quiet

This script uses only the Python standard library. It makes no network calls,
installs no packages, uses no provider account, and writes concise receipts
under receipts/.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MIN_PYTHON = (3, 11)
TIMEOUT_SECONDS = 60
MAX_CAPTURE_CHARS = 4000


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def safe_json(text: str) -> dict[str, Any] | None:
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def run_json(command: list[str], cwd: Path) -> tuple[int, dict[str, Any] | None, str, float]:
    start = time.perf_counter()
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return 124, None, f"Timed out after {TIMEOUT_SECONDS} seconds.", round(time.perf_counter() - start, 3)
    elapsed = round(time.perf_counter() - start, 3)
    payload = safe_json(completed.stdout.strip())
    error = completed.stderr.strip()
    if not error and payload is None and completed.stdout.strip():
        error = "Command returned non-JSON output."
    return completed.returncode, payload, error[:MAX_CAPTURE_CHARS], elapsed


def rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Elaine Core v0.1 without an AI agent.")
    parser.add_argument("--json", action="store_true", help="Print only the compact JSON summary.")
    parser.add_argument("--quiet", action="store_true", help="Write receipts and print only PASS or FAIL.")
    parser.add_argument("--root", default="", help="Package root; defaults to this script's directory.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve() if args.root else Path(__file__).resolve().parent
    receipts = root / "receipts"
    receipts.mkdir(parents=True, exist_ok=True)

    proof_script = root / "PROOF_LAB" / "elaine_research_proof_lab.py"
    runtime_script = root / "RUNTIME_CORE" / "elaine_runtime_core.py"
    required_scripts = (proof_script, runtime_script)
    missing = [rel(path, root) for path in required_scripts if not path.is_file()]

    proof_receipt_path = receipts / "install-proof-lab-receipt.json"
    doctor_receipt_path = receipts / "install-runtime-doctor-receipt.json"
    summary_path = receipts / "install-summary.json"

    summary: dict[str, Any] = {
        "schema_version": "elaine.install-summary.v2",
        "generated_utc": utc_now(),
        "package_root_name": root.name,
        "python": platform.python_version(),
        "python_supported": sys.version_info >= MIN_PYTHON,
        "network_used": False,
        "packages_installed": False,
        "provider_call_used": False,
        "model_call_used": False,
        "git_action_used": False,
        "docker_used": False,
        "missing_files": missing,
        "executable_surface": {
            rel(path, root): sha256_file(path) for path in required_scripts if path.is_file()
        },
        "checks": {},
        "status": "fail",
    }

    if sys.version_info < MIN_PYTHON:
        summary["reason"] = "Python 3.11+ is required."
    elif missing:
        summary["reason"] = "Required package files are missing."
    else:
        proof_code, proof, proof_error, proof_seconds = run_json(
            [
                sys.executable,
                str(proof_script),
                "run-cases",
                "--out",
                rel(proof_receipt_path, root),
            ],
            root,
        )
        doctor_code, doctor, doctor_error, doctor_seconds = run_json(
            [
                sys.executable,
                str(runtime_script),
                "doctor",
                "--out",
                rel(doctor_receipt_path, root),
            ],
            root,
        )

        proof_ok = bool(
            proof_code == 0
            and proof
            and proof.get("fail_count") == 0
            and proof.get("pass_count") == proof.get("proof_case_count")
            and proof_receipt_path.is_file()
        )
        doctor_ok = bool(
            doctor_code == 0
            and doctor
            and doctor.get("status") == "pass"
            and doctor_receipt_path.is_file()
        )

        summary["checks"] = {
            "proof_lab": {
                "status": "pass" if proof_ok else "fail",
                "exit_code": proof_code,
                "elapsed_seconds": proof_seconds,
                "case_count": proof.get("proof_case_count") if proof else None,
                "pass_count": proof.get("pass_count") if proof else None,
                "receipt": rel(proof_receipt_path, root) if proof_receipt_path.is_file() else None,
                "error": proof_error or None,
            },
            "runtime_doctor": {
                "status": "pass" if doctor_ok else "fail",
                "exit_code": doctor_code,
                "elapsed_seconds": doctor_seconds,
                "receipt": rel(doctor_receipt_path, root) if doctor_receipt_path.is_file() else None,
                "error": doctor_error or None,
            },
        }
        summary["status"] = "pass" if proof_ok and doctor_ok else "fail"

    summary["summary_receipt"] = rel(summary_path, root)
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.quiet:
        print(summary["status"].upper())
    elif args.json:
        print(json.dumps(summary, separators=(",", ":"), sort_keys=True))
    else:
        print(f"ELAINE_INSTALL_CHECK={summary['status'].upper()}")
        print(f"python={summary['python']} supported={str(summary['python_supported']).lower()}")
        for name, result in summary.get("checks", {}).items():
            print(f"{name}={result['status']} elapsed_seconds={result['elapsed_seconds']}")
        print(f"receipt={summary['summary_receipt']}")

    return 0 if summary["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
