#!/usr/bin/env python3
"""Self-contained proof lab for the Elaine AOS public-review package."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


PACKET_ID = "elaine-core-v0.1-local-export-v0"
CASE_FILE = "PROOF_LAB/docproof_cases.json"
DEFAULT_RECEIPT = "receipts/elaine-proof-lab-receipt.json"
DOCS = [
    "PACKAGE_MANIFEST.json",
    "README.md",
    "QUICKSTART.md",
    "REVIEWER_GUIDE.md",
    "REVIEWER_FEEDBACK_FORM.md",
    "RECEIPT_INDEX.md",
    "LICENSE",
    "PAPER.md",
    "CLAIM_LEDGER.md",
    "DO_NOT_CLAIM.md",
    "SECURITY.md",
    "NOTICE.md",
    "RELEASE_REVIEW.md",
    "LICENSE_DECISION_REQUIRED.md",
    "CONTRIBUTING.md",
    "SOURCE_CARDS_CANDIDATE.md",
    "docs/ARCHITECTURE.md",
    "docs/THREAT_MODEL.md",
    "docs/GOVERNANCE_MODEL.md",
    "docs/LIMITATIONS.md",
    "docs/PRODUCT_PROOF_BACKBONE.md",
    "PROOF_LAB/README.md",
    CASE_FILE,
    "PROOF_LAB/elaine_research_proof_lab.py",
    "receipts/README.md",
]

EXPECTED_DECISIONS = {
    "claim_downgrade": "downgrade",
    "missing_proof_hold": "hold",
    "gate_block": "block",
    "receipt_proof_record": "record_receipt",
    "public_language_block": "block",
    "recall_proof_linkage": "return_proof_link",
}

BOUNDARY_FLAGS = {
    "public_release_authorized": False,
    "repository_publication_authorized": False,
    "license_selected": True,
    "counsel_disclosure_cleared": False,
    "patent_filing_authorized": False,
    "provider_call_used": False,
    "hosted_retrieval_used": False,
    "git_publication_authorized": False,
    "public_sharing_authorized": False,
    "raw_secret_handling_used": False,
    "external_review_authorized": False,
    "production_ready_claimed": False,
    "customer_validation_claimed": False,
    "peer_review_claimed": False,
    "citation_complete_claimed": False,
}

CLAIMS = [
    {
        "claim_id": "LAB-CLAIM-001",
        "claim": "The package can be indexed and hashed deterministically.",
        "state": "tested_locally",
        "proof_refs": ["receipts/elaine-proof-lab-receipt.json"],
        "limit": "This proves local package hashing only.",
    },
    {
        "claim_id": "LAB-CLAIM-002",
        "claim": "Six synthetic DocProof cases can execute as a proof-before-action slice.",
        "state": "tested_locally",
        "proof_refs": [CASE_FILE, "receipts/elaine-proof-lab-receipt.json"],
        "limit": "This proves selected synthetic cases only.",
    },
    {
        "claim_id": "LAB-CLAIM-003",
        "claim": "Public claims can map to proof, limitation, or blocked state.",
        "state": "review_candidate",
        "proof_refs": ["CLAIM_LEDGER.md", "DO_NOT_CLAIM.md"],
        "limit": "Final public release still requires owner approval.",
    },
    {
        "claim_id": "LAB-CLAIM-004",
        "claim": "A public-safe product-proof backbone summary is included in the local Core export.",
        "state": "tested_locally",
        "proof_refs": ["docs/PRODUCT_PROOF_BACKBONE.md", "receipts/elaine-proof-lab-receipt.json"],
        "limit": "This proves a local summary exists and is indexed; it does not prove field security outcomes.",
    },
]


def fail(message: str) -> None:
    print(json.dumps({"status": "fail", "error": message}, indent=2))
    sys.exit(1)


def package_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_text(root: Path, rel: str) -> str:
    path = root / rel
    if not path.exists():
        fail(f"Missing required file: {rel}")
    return path.read_text(encoding="utf-8", errors="replace")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(root: Path, rel: str) -> str:
    path = root / rel
    if not path.exists():
        fail(f"Missing file for hash: {rel}")
    return sha256_bytes(path.read_bytes())


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def build_index(root: Path) -> dict:
    docs = []
    for rel in DOCS:
        text = read_text(root, rel)
        tokens = tokenize(text)
        docs.append({
            "path": rel,
            "sha256": sha256_file(root, rel),
            "bytes": len((root / rel).read_bytes()),
            "line_count": len(text.splitlines()),
            "token_count": len(tokens),
            "unique_token_count": len(set(tokens)),
        })
    package_hash = sha256_text(json.dumps(
        [{"path": row["path"], "sha256": row["sha256"]} for row in docs],
        sort_keys=True,
        separators=(",", ":"),
    ))
    return {
        "packet_id": PACKET_ID,
        "status": "index_built",
        "indexed_document_count": len(docs),
        "source_package_hash": package_hash,
        "documents": docs,
    }


def search_index(root: Path, query: str) -> dict:
    index = build_index(root)
    tokens = tokenize(query)
    if not tokens:
        fail("Search query must include at least one token")
    results = []
    for doc in index["documents"]:
        text = read_text(root, doc["path"]).lower()
        score = sum(text.count(token) for token in tokens)
        if score:
            results.append({"path": doc["path"], "score": score, "sha256": doc["sha256"]})
    results.sort(key=lambda row: (-row["score"], row["path"]))
    return {
        "packet_id": PACKET_ID,
        "status": "search_complete",
        "query": query,
        "result_count": len(results),
        "results": results[:10],
    }


def show_claim(claim_id: str) -> dict:
    for claim in CLAIMS:
        if claim["claim_id"] == claim_id:
            return {"packet_id": PACKET_ID, "status": "claim_found", "claim": claim, "boundary_flags": BOUNDARY_FLAGS}
    fail(f"Unknown claim id: {claim_id}")


def load_cases(root: Path) -> list[dict]:
    data = json.loads(read_text(root, CASE_FILE))
    cases = data.get("cases")
    if not isinstance(cases, list):
        fail("docproof cases must contain a cases list")
    return [case for case in cases if isinstance(case, dict)]


def evaluate_case(case: dict) -> dict:
    behavior = str(case.get("behavior", ""))
    expected = EXPECTED_DECISIONS.get(behavior)
    if expected is None:
        fail(f"Unsupported behavior: {behavior}")
    passed = case.get("decision") == expected and case.get("synthetic_only") is True
    return {
        "case_id": str(case.get("id", "")),
        "behavior": behavior,
        "expected_decision": expected,
        "observed_decision": case.get("decision"),
        "result": "pass" if passed else "fail",
        "synthetic_only": case.get("synthetic_only") is True,
        "safe_output_sha256": sha256_text(str(case.get("safe_output", ""))),
        "proof_or_receipt_ref": str(case.get("receipt_ref", "")),
        "blocked_claim_allowed": False,
    }


def run_cases(root: Path) -> dict:
    results = [evaluate_case(case) for case in load_cases(root)]
    passed = sum(1 for row in results if row["result"] == "pass")
    return {
        "packet_id": PACKET_ID,
        "status": "cases_executed",
        "proof_case_count": len(results),
        "pass_count": passed,
        "fail_count": len(results) - passed,
        "case_results": results,
    }


def build_receipt(root: Path) -> dict:
    index = build_index(root)
    cases = run_cases(root)
    receipt = {
        "schema_version": 1,
        "packet_id": PACKET_ID,
        "status": "deterministic_public_review_receipt",
        "source_scope": "sanitized_public_review_package_and_synthetic_docproof_examples_only",
        "source_package_hash": index["source_package_hash"],
        "indexed_document_count": index["indexed_document_count"],
        "proof_case_count": cases["proof_case_count"],
        "pass_count": cases["pass_count"],
        "fail_count": cases["fail_count"],
        "documents": index["documents"],
        "claims": CLAIMS,
        "case_results": cases["case_results"],
        "queries": [
            search_index(root, "proof before action"),
            search_index(root, "claim downgrade"),
            search_index(root, "public release blocked"),
        ],
        "command_contract": {
            "entrypoint": "PROOF_LAB/elaine_research_proof_lab.py",
            "commands": ["index", "search", "show-claim", "run-cases", "export-manifest"],
            "stdlib_only": True,
            "external_actions": "none",
        },
        "boundary_flags": BOUNDARY_FLAGS,
        "limitations": [
            "Synthetic examples only.",
            "No public release, repository publication, provider call, hosted retrieval, deployment, counsel sharing, patent filing, or raw-secret handling is authorized.",
            "No launch-maturity, adoption, certification, managed-security, endorsement, formal-review, citation-finality, or IP-status claim is made.",
            "Final public use requires exact owner approval.",
        ],
    }
    return receipt


def export_manifest(root: Path, out: str) -> dict:
    receipt = build_receipt(root)
    out_path = (root / out).resolve()
    try:
        out_path.relative_to(root)
    except ValueError:
        fail("Refusing to write outside package root")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return receipt


def emit(value: dict) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["index", "search", "show-claim", "run-cases", "export-manifest"])
    parser.add_argument("--query", default="proof before action")
    parser.add_argument("--claim", default="LAB-CLAIM-001")
    parser.add_argument("--out", default=DEFAULT_RECEIPT)
    args = parser.parse_args()

    root = package_root()
    if args.command == "index":
        emit(build_index(root))
    elif args.command == "search":
        emit(search_index(root, args.query))
    elif args.command == "show-claim":
        emit(show_claim(args.claim))
    elif args.command == "run-cases":
        emit(run_cases(root))
    elif args.command == "export-manifest":
        emit(export_manifest(root, args.out))


if __name__ == "__main__":
    main()
