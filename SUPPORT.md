# Elaine Core v0.1 Support

Elaine Core v0.1 is a controlled-alpha proof package. Support is limited to reviewer installation, proof-lab execution, receipt interpretation, and claim-boundary review.

## Supported Questions

- What does the package claim today?
- How do I run the proof lab?
- Where are the receipts?
- Which claims are blocked?
- What failed during a fresh install?
- How should a future controlled setup collect a sensitive value without
  exposing it?

## Not Supported In This Package

- Production deployment.
- Endpoint protection or monitoring.
- Blocked SOC/MDR replacement claim; Elaine Core v0.1 does not replace SOC or MDR services.
- Compliance certification.
- Live model/provider integration.
- Private-corpus RAG.
- Autonomous workstation control.
- Password-manager replacement; users may use their own password manager, but
  Elaine Core v0.1 does not store or manage passwords.

## Reporting Issues

For each issue, record:

- Operating system and Python version.
- Exact command run.
- Receipt path.
- Error text with secrets removed.
- Whether the issue affects understanding, installability, proof correctness, or claim wording.

Security-sensitive issues should follow `SECURITY.md`.
Credential-entry questions should start with
`GUIDED_SETUP_AND_SECRET_ENTRY.md`.

## Severity And Escalation

| Severity | Use when | Required action |
| --- | --- | --- |
| S1 security boundary | Secret, private data, unsafe public claim, or unexpected external action appears. | Stop review, preserve the receipt, follow `SECURITY.md`, and do not redistribute the package. |
| S2 runability blocker | A clean reviewer cannot run the proof lab or Runtime Core CLI using the docs. | Record OS, command, receipt, and failure; hold reviewer expansion until fixed or waived. |
| S3 documentation defect | A reviewer can run the package but misunderstands what Elaine does or does not claim. | Update README, QUICKSTART, CLAIM_LEDGER, LIMITATIONS, or this support guide. |
| S4 polish issue | Wording, formatting, or workflow clarity can improve without changing claims or proof. | Queue for the next package refresh. |

Escalation is evidence-first: every report needs a command, receipt, screenshot, or exact file/line reference where possible.
