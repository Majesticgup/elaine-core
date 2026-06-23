# Elaine Core v0.1 Admin / Operator Guide

Elaine Core v0.1 is operated as a local proof package. The operator should treat every output as review evidence, not as production authority.

## Operator Duties

- Keep the package separate from the private Elaine OS workspace.
- Run proof commands from the package root.
- Preserve generated receipts for review.
- Compare every public claim against `CLAIM_LEDGER.md`, `DO_NOT_CLAIM.md`, and `docs/LIMITATIONS.md`.
- Stop before any action that would require external sharing, provider calls, account changes, Git actions, deployment, or raw-secret handling.

## Safe Commands

```powershell
python PROOF_LAB\elaine_research_proof_lab.py run-cases --out receipts\operator-proof-lab-receipt.json
python PROOF_LAB\elaine_research_proof_lab.py export-manifest --out receipts\operator-manifest-receipt.json
python RUNTIME_CORE\elaine_runtime_core.py status --out receipts\operator-runtime-status-receipt.json
python RUNTIME_CORE\elaine_runtime_core.py doctor --out receipts\operator-runtime-doctor-receipt.json
```

## Operating Boundary

Allowed: local proof-lab execution, package inspection, receipt review, and claim-pressure review.

Blocked: provider calls, hosted retrieval, private-corpus RAG, MCP tool execution, autonomous workstation changes, public sharing, deployment, production claims, and security-benefit claims.

## Promotion Rule

A statement can move into reviewer-facing wording only when it maps to a receipt, a limitation, or a blocked state. Missing proof is a stop condition, not a wording problem.

