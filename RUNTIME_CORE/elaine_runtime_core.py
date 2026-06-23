#!/usr/bin/env python3
"""Elaine Runtime Core v0 package CLI.

This clean-package CLI aggregates local package evidence only. It deliberately
does not start services, expose APIs, run MCP tools, invoke models, use hosted
retrieval, install dependencies, mutate Git, publish, or read private data.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


RUNTIME_ID = "elaine-runtime-core-v0-package-cli"

SECRET_PATTERNS = [
    re.compile(r"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,}(?![A-Za-z0-9_-])"),
    re.compile(r"(?<![A-Za-z0-9_])github_pat_[A-Za-z0-9_]{20,}(?![A-Za-z0-9_])"),
    re.compile(r"(?<![A-Za-z0-9])ghp_[A-Za-z0-9]{20,}(?![A-Za-z0-9])"),
    re.compile(r"Bearer\s+[A-Za-z0-9._~+/-]+=*", re.I),
    re.compile(r"-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def package_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return "[outside-package]"


def boundary_flags() -> dict[str, bool]:
    return {
        "service_started": False,
        "localhost_api_started": False,
        "mcp_server_started": False,
        "model_call_used": False,
        "provider_call_used": False,
        "hosted_retrieval_used": False,
        "private_corpus_used": False,
        "install_used": False,
        "git_action_used": False,
        "deployment_used": False,
        "public_sharing_used": False,
        "raw_secret_handling_used": False,
        "destructive_action_used": False,
    }


def manifest_status(root: Path) -> dict[str, Any]:
    manifest_path = root / "PACKAGE_MANIFEST.json"
    manifest = read_json(manifest_path)
    required = manifest.get("required_files", []) if manifest else []
    missing = [item for item in required if not (root / item).is_file()]
    return {
        "path": rel(manifest_path, root),
        "present": manifest_path.is_file(),
        "json_valid": manifest is not None,
        "package_id": manifest.get("package_id") if manifest else None,
        "runtime_core_included": manifest.get("runtime_core_included") if manifest else None,
        "missing_required_files": missing,
        "public_release_authorized": manifest.get("public_release_authorized") if manifest else False,
        "production_ready_claimed": manifest.get("production_ready_claimed") if manifest else False,
    }


def proof_lab_status(root: Path) -> dict[str, Any]:
    lab = root / "PROOF_LAB/elaine_research_proof_lab.py"
    receipts = [
        root / "receipts/runtime-core-proof-lab-receipt.json",
        root / "receipts/tuesday-fresh-copy-proof-lab-receipt.json",
        root / "receipts/elaine-proof-lab-receipt.json",
    ]
    present_receipts = []
    for receipt in receipts:
        data = read_json(receipt)
        present_receipts.append(
            {
                "path": rel(receipt, root),
                "present": receipt.is_file(),
                "json_valid": data is not None,
                "status": data.get("status") if data else "missing",
            }
        )
    return {
        "proof_lab_present": lab.is_file(),
        "proof_lab_path": rel(lab, root),
        "receipts": present_receipts,
    }


def run_proof_lab(root: Path, out: Path | None) -> dict[str, Any]:
    lab = root / "PROOF_LAB/elaine_research_proof_lab.py"
    out_path = out or (root / "receipts/runtime-core-proof-lab-receipt.json")
    if not lab.is_file():
        return {"status": "fail", "error": "proof_lab_missing", "out": rel(out_path, root)}
    proc = subprocess.run(
        [sys.executable, str(lab), "export-manifest", "--out", str(out_path)],
        cwd=str(root),
        text=True,
        capture_output=True,
    )
    data = read_json(out_path)
    return {
        "status": "pass" if proc.returncode == 0 and data is not None else "fail",
        "exit_code": proc.returncode,
        "out": rel(out_path, root),
        "receipt_status": data.get("status") if data else "missing",
    }


def receipts_status(root: Path) -> dict[str, Any]:
    receipt_dir = root / "receipts"
    items = []
    for path in sorted(receipt_dir.glob("*.json")) if receipt_dir.is_dir() else []:
        data = read_json(path)
        items.append(
            {
                "path": rel(path, root),
                "json_valid": data is not None,
                "status": data.get("status") if data else "missing",
            }
        )
    return {"receipt_count": len(items), "receipts": items}


def held_status(surface: str) -> dict[str, Any]:
    return {
        "surface": surface,
        "status": "held_not_in_public_package",
        "included": False,
        "claim_ceiling": f"{surface} is documented as future/held work and is not active in this clean review package.",
    }


def gates_status(root: Path) -> dict[str, Any]:
    manifest = read_json(root / "PACKAGE_MANIFEST.json") or {}
    return {
        "blocked_public_actions": [
            "GitHub proof release without A5 approval",
            "public sharing without A5 approval",
            "deployment",
            "Anthropic sharing without A5 approval",
            "production/security-benefit claims",
        ],
        "runtime_blockers": manifest.get(
            "runtime_release_blockers",
            [
                "loopback API not implemented in clean package",
                "local MCP server not implemented in clean package",
                "model integration not active in clean package",
            ],
        ),
    }


def status_payload(root: Path) -> dict[str, Any]:
    manifest = manifest_status(root)
    proof = proof_lab_status(root)
    gates = gates_status(root)
    status = "pass"
    if not manifest["present"] or not manifest["json_valid"] or manifest["missing_required_files"]:
        status = "fail"
    if not proof["proof_lab_present"]:
        status = "fail"
    return {
        "runtime_id": RUNTIME_ID,
        "generated_utc": utc_now(),
        "status": status,
        "manifest": manifest,
        "proof_lab": proof,
        "llm": held_status("local LLM"),
        "api": held_status("loopback API"),
        "mcp": held_status("local MCP server"),
        "gates": gates,
        "claim_ceiling": "clean-package Runtime Core CLI only; no service, API, MCP server, model invocation, private RAG, production readiness, or security outcome claim",
        "boundary_flags": boundary_flags(),
    }


def assert_no_secret_shapes(payload: dict[str, Any]) -> None:
    text = json.dumps(payload, sort_keys=True, ensure_ascii=True)
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            raise RuntimeError(f"secret-shaped output detected: {pattern.pattern}")


def write_or_print(payload: dict[str, Any], out: str | None) -> None:
    assert_no_secret_shapes(payload)
    if out:
        out_path = Path(out)
        if not out_path.is_absolute():
            out_path = package_root() / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description="Elaine Runtime Core v0 package CLI")
    parser.add_argument("command", choices=["status", "doctor", "proof-lab", "receipts", "llm-status", "mcp-status", "gates"])
    parser.add_argument("--run", action="store_true", help="Run the proof lab for the proof-lab command.")
    parser.add_argument("--out", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = package_root()
    if args.command == "status":
        payload = status_payload(root)
    elif args.command == "doctor":
        payload = status_payload(root)
        payload["doctor"] = {
            "runtime_core_cli_present": True,
            "central_cli_commands": ["status", "doctor", "proof-lab", "receipts", "llm-status", "mcp-status", "gates"],
            "api_server_present": False,
            "mcp_server_present": False,
            "service_mode_present": False,
            "model_invocation_present": False,
        }
    elif args.command == "proof-lab":
        proof = proof_lab_status(root)
        payload = {
            "runtime_id": RUNTIME_ID,
            "generated_utc": utc_now(),
            "status": "pass" if proof["proof_lab_present"] else "fail",
            "proof_lab": proof,
            "boundary_flags": boundary_flags(),
        }
        if args.run:
            payload["proof_lab_run"] = run_proof_lab(root, Path(args.out) if args.out else None)
            payload["status"] = payload["proof_lab_run"]["status"]
            args.out = ""
    elif args.command == "receipts":
        payload = {
            "runtime_id": RUNTIME_ID,
            "generated_utc": utc_now(),
            "status": "pass",
            **receipts_status(root),
            "boundary_flags": boundary_flags(),
        }
    elif args.command == "llm-status":
        payload = {
            "runtime_id": RUNTIME_ID,
            "generated_utc": utc_now(),
            "status": "pass",
            "llm": held_status("local LLM"),
            "boundary_flags": boundary_flags(),
        }
    elif args.command == "mcp-status":
        payload = {
            "runtime_id": RUNTIME_ID,
            "generated_utc": utc_now(),
            "status": "pass",
            "mcp": held_status("local MCP server"),
            "boundary_flags": boundary_flags(),
        }
    else:
        payload = {
            "runtime_id": RUNTIME_ID,
            "generated_utc": utc_now(),
            "status": "pass",
            "gates": gates_status(root),
            "boundary_flags": boundary_flags(),
        }
    write_or_print(payload, args.out or None)
    return 0 if payload.get("status") == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
