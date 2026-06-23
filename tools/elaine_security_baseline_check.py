#!/usr/bin/env python3
"""Read-only Elaine controlled-installation security baseline check."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA = "elaine.security-baseline-readiness.v1"
MIN_PYTHON = (3, 11)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def read_json(path: Path) -> tuple[dict[str, Any], str | None]:
    try:
        value = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        return {}, str(exc)
    return value if isinstance(value, dict) else {}, None


def add(checks: list[dict[str, Any]], control_id: str, title: str, ok: bool, detail: Any = None) -> None:
    checks.append(
        {
            "control_id": control_id,
            "title": title,
            "status": "pass" if ok else "fail",
            "detail": detail,
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a read-only SCAP/STIG-inspired Elaine readiness baseline."
    )
    parser.add_argument("--json", action="store_true", help="Print compact JSON only.")
    parser.add_argument("--root", default="", help="Package root; defaults to this script's parent package.")
    parser.add_argument(
        "--out",
        default="receipts/security-baseline-readiness.json",
        help="Receipt path relative to package root. Use empty string to skip writing.",
    )
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve() if args.root else Path(__file__).resolve().parents[1]
    checks: list[dict[str, Any]] = []

    manifest, manifest_error = read_json(root / "PACKAGE_MANIFEST.json")
    credit_policy, credit_error = read_json(root / "config" / "credit-policy.json")
    install_policy, install_error = read_json(root / "config" / "install-control-policy.json")

    gitignore = read_text(root / ".gitignore")
    install_agent = read_text(root / "INSTALL_AGENT.md")
    verifier = read_text(root / "verify_install.py")
    controlled_doc = read_text(root / "docs" / "CONTROLLED_INSTALLATION_GOVERNANCE.md")
    context_guard = read_text(root / "tools" / "elaine_context_guard.py")

    add(checks, "ELN-BASE-000", "Python version is supported", sys.version_info >= MIN_PYTHON, platform.python_version())
    add(checks, "ELN-BASE-001", "Package manifest is valid JSON", manifest_error is None, manifest_error)
    add(checks, "ELN-BASE-002", "Credit policy is valid JSON", credit_error is None, credit_error)
    add(checks, "ELN-BASE-003", "Install-control policy is valid JSON", install_error is None, install_error)
    add(
        checks,
        "ELN-BASE-004",
        "Normal verification requires no model call",
        manifest.get("install_verifier", {}).get("normal_install_requires_model") is False
        and credit_policy.get("normal_verification", {}).get("model_calls_allowed") == 0,
        {
            "manifest": manifest.get("install_verifier", {}).get("normal_install_requires_model"),
            "policy": credit_policy.get("normal_verification", {}).get("model_calls_allowed"),
        },
    )
    add(
        checks,
        "ELN-BASE-005",
        "Normal verification blocks network, provider calls, installs, Git, Docker, and host changes",
        install_policy.get("normal_verification", {}).get("network_allowed") is False
        and install_policy.get("normal_verification", {}).get("provider_calls_allowed") is False
        and install_policy.get("normal_verification", {}).get("package_installs_allowed") is False
        and install_policy.get("normal_verification", {}).get("git_actions_allowed") is False
        and install_policy.get("normal_verification", {}).get("docker_allowed") is False
        and install_policy.get("normal_verification", {}).get("host_changes_allowed") is False,
        install_policy.get("normal_verification", {}),
    )
    add(
        checks,
        "ELN-BASE-006",
        "Controlled host-changing execution is unavailable in v0.1 and requires A3",
        install_policy.get("controlled_install_execution", {}).get("available_in_v0_1") is False
        and install_policy.get("controlled_install_execution", {}).get("requires_exact_owner_gate") == "A3",
        install_policy.get("controlled_install_execution", {}),
    )
    required_gate_fields = install_policy.get("controlled_install_execution", {}).get("required_gate_fields", [])
    for field in [
        "target",
        "action",
        "allowed_commands_or_script",
        "rollback_path",
        "checks",
        "proof_path",
        "expiry",
        "blocked_actions",
        "stop_conditions",
    ]:
        add(checks, f"ELN-GATE-{field}", f"Required A3 gate field present: {field}", field in required_gate_fields, field)
    add(
        checks,
        "ELN-BASE-007",
        "Agent-assisted failure diagnosis is capped",
        credit_policy.get("agent_assisted_failure_diagnosis", {}).get("max_tool_calls") == 3
        and credit_policy.get("agent_assisted_failure_diagnosis", {}).get("max_source_files_read") == 3
        and "Maximum three tool calls" in install_agent,
        credit_policy.get("agent_assisted_failure_diagnosis", {}),
    )
    add(
        checks,
        "ELN-BASE-008",
        "Verifier emits executable-surface hashes in v2 summary",
        "schema_version" in verifier
        and "elaine.install-summary.v2" in verifier
        and "executable_surface" in verifier
        and "sha256_file" in verifier,
        "verify_install.py",
    )
    add(
        checks,
        "ELN-BASE-009",
        "Generated receipts and context cache are ignored by Git",
        "receipts/security-baseline-readiness.json" in gitignore
        and "receipts/context-guard*.json" in gitignore
        and "receipts/transcript-credit-audit*.json" in gitignore
        and ".elaine-context-cache/" in gitignore,
        ".gitignore",
    )
    add(
        checks,
        "ELN-BASE-010",
        "Secrets are not required for v0.1 and raw secret persistence is blocked by manifest",
        manifest.get("guided_setup_and_secret_entry", {}).get("v0_1_secrets_required") is False
        and manifest.get("guided_setup_and_secret_entry", {}).get("raw_secret_persisted_by_helper") is False,
        manifest.get("guided_setup_and_secret_entry", {}),
    )
    add(
        checks,
        "ELN-BASE-011",
        "Context guard passes source code and short output through unchanged",
        "passthrough-code" in context_guard and "passthrough-short" in context_guard and "fail-open-original" in context_guard,
        "tools/elaine_context_guard.py",
    )
    add(
        checks,
        "ELN-BASE-012",
        "SCAP/STIG wording is bounded and does not claim formal compliance",
        "not formal SCAP content" in controlled_doc
        and "not a DISA STIG scan" in controlled_doc
        and "not a compliance result" in controlled_doc
        and "not a security certification" in controlled_doc,
        "docs/CONTROLLED_INSTALLATION_GOVERNANCE.md",
    )

    failed = [check for check in checks if check["status"] != "pass"]
    status = "pass" if not failed else "fail"
    receipt: dict[str, Any] = {
        "schema_version": SCHEMA,
        "generated_utc": utc_now(),
        "status": status,
        "package_root_name": root.name,
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "python": platform.python_version(),
        },
        "controlled_install_execution_status": "gated_not_authorized",
        "formal_scap_content": False,
        "formal_stig_result": False,
        "compliance_claimed": False,
        "security_benefit_claimed": False,
        "network_used": False,
        "provider_call_used": False,
        "package_install_used": False,
        "host_change_used": False,
        "checks_count": len(checks),
        "failed_count": len(failed),
        "checks": checks,
        "claim_boundary": "SCAP/STIG-inspired readiness checklist only; not compliance, certification, production readiness, deployment proof, or security validation.",
    }

    if args.out:
        out_path = root / args.out
        out_path.parent.mkdir(parents=True, exist_ok=True)
        receipt["summary_receipt"] = out_path.relative_to(root).as_posix()
        out_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(receipt, separators=(",", ":"), sort_keys=True))
    else:
        print(f"ELAINE_SECURITY_BASELINE={status.upper()}")
        print(f"checks={len(checks)} failed={len(failed)}")
        print("controlled_install_execution=gated_not_authorized")
        if args.out:
            print(f"receipt={receipt['summary_receipt']}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
