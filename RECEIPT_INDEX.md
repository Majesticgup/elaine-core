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

## Generated Install Receipts

`verify_install.py` writes these local install receipts when a user verifies the
package:

| Receipt | What it proves | What it does not prove |
| --- | --- | --- |
| `receipts/install-summary.json` | The zero-credit verifier ran the proof lab and Runtime Core doctor in that local folder. | Production readiness, security validation, external review, Docker, hosted/provider behavior, or deployment. |
| `receipts/install-proof-lab-receipt.json` | `run-cases --out` wrote the synthetic proof-case result. | Field security outcomes or full proof-lab manifest export. |
| `receipts/install-runtime-doctor-receipt.json` | Runtime Core doctor passed for the clean package. | Runtime service, API, MCP server, model call, private RAG, or workstation control readiness. |

## Generated Baseline And Credit Receipts

These optional local tools are not part of ordinary installation verification:

| Receipt | What it proves | What it does not prove |
| --- | --- | --- |
| `receipts/security-baseline-readiness.json` | The read-only controlled-installation baseline checked gates, rollback requirements, secret boundaries, ignored generated evidence, and blocked claims. | Formal SCAP/STIG compliance, certification, security validation, production readiness, host hardening, or deployment. |
| `receipts/context-guard*.json` | A local context compaction or audit run recorded byte counts, strategy, and retrieval reference when applicable. | Billed-token savings, model behavior, source-security review, or proof that all future transcripts are optimized. |
| `receipts/transcript-credit-audit*.json` | A local transcript audit counted approximate size and credit-waste signals. | Actual provider billing, comprehensive usage accounting, or correctness of an agent's work. |

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
