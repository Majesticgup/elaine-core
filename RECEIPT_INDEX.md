# Elaine Core v0.1 Receipt Index

Status: PUBLIC PACKAGE RECEIPT INDEX / NOT PRODUCTION EVIDENCE.

This index explains which proof records are bundled with the clean package and
which proof records must be attached separately by the controlled-alpha owner
packet. A receipt is evidence of a bounded local check only. It is not legal,
compliance, production, external-audit, or security-outcome evidence.

## Bundled Receipts

| Receipt | What it proves | What it does not prove |
| --- | --- | --- |
| `receipts/elaine-proof-lab-receipt.json` | The proof lab can index the clean package, hash included files, and run the synthetic DocProof cases. | Real-world security benefit, production readiness, external validation, or OS compatibility. |
| `receipts/runtime-core-proof-lab-receipt.json` | Runtime Core can invoke the proof-lab path and record a package-local receipt. | A persistent service, live API, live MCP tools, model calls, private RAG, or workstation control. |
| `receipts/tuesday-fresh-copy-proof-lab-receipt.json` | A fresh-copy proof-lab run was recorded for this package shape. | Docker, Ubuntu, Windows, low-resource, or public-release readiness. |

## Optional Local Prompt Receipt

`tools/Start-ElaineGuidedSecretPrompt.ps1` can write
`receipts/guided-secret-entry-receipt.json` during a future controlled setup
lane. That receipt proves only that a local hidden prompt flow was rehearsed or
used and that the receipt stayed redacted. It does not prove authentication,
GitHub access, provider access, account security, production readiness, or a
security outcome.

## External Track A Receipts

These receipts are not required to run the clean package, but they should be
attached by the owner if the reviewer is asked to evaluate the broader
controlled-alpha proof state.

| Evidence class | Current state | Reviewer wording ceiling |
| --- | --- | --- |
| Docker proof runtime | Passed in the owner readiness lane. | Docker proof runtime passed for the clean package under a bounded local receipt. |
| Ubuntu baseline | Passed in the owner readiness lane. | Ubuntu clean-VM baseline passed. |
| Runtime Core loopback/API/MCP preview | Passed in the owner readiness lane. | Localhost-only status/API and MCP manifest preview passed; no MCP tool execution. |
| Windows runability | Blocked. | Windows compatibility remains unproven. |
| Low-resource runability | Blocked. | Low-resource compatibility remains unproven. |
| Local LLM support | Bounded support evidence only. | Candidate reasoning support only; not daily-use readiness and not required for Track A. |

## Reviewer Check

After running the quickstart, reviewers should be able to answer:

1. Which receipt did I generate or inspect?
2. Which claim does that receipt support?
3. Which claims remain blocked or unproven?
4. Did any command require private workspace access, credentials, network access, or owner explanation?
