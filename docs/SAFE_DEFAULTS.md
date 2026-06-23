# Elaine Core Safe Defaults

Elaine Core v0.1 defaults to local, bounded, review-only behavior.

## Defaults

- No provider calls.
- No hosted retrieval.
- No raw-secret handling.
- No public sharing.
- No Git action.
- No deployment.
- No persistent service.
- No MCP tool execution.
- No model invocation.
- No workstation mutation.
- No private-corpus RAG.

## Package Defaults

- Proof lab runs from local files.
- Receipts write under the local `receipts/` folder.
- Runtime Core is a CLI proof helper, not a background service.
- Docker proof-runtime requires an explicit verified base-image digest.
- Strong claims remain blocked unless `CLAIM_LEDGER.md` maps them to evidence.

## Failure Default

When evidence is missing, Elaine holds the claim or action. It does not fill the gap with confident language.

