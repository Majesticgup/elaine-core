# Elaine Core v0.1 Quickstart

Status: LOCAL REVIEW PACKAGE / NOT PRODUCTION READY / NOT A SECURITY PRODUCT.

This is the shortest path for a first-time reviewer. It should work from the
package root without private Elaine OS workspace access, API keys, provider
accounts, or network access.

## Install Verification First

If you only need to verify the package, run:

```bash
python verify_install.py
```

Then stop if it reports `ELAINE_INSTALL_CHECK=PASS`. No AI agent, security
review, Docker run, Git action, provider call, or source audit is required.

## 0. Pick Your Review Path

If you downloaded this from GitHub, start with:

```text
START_HERE.md
DOWNLOAD_AND_REVIEW_GUIDE.md
GUIDED_SETUP_AND_SECRET_ENTRY.md
```

If you are one of the first three reviewers, also read:

```text
FIRST_REVIEW_TEAM_PACKET.md
```

Use `REVIEWER_FEEDBACK_FORM.md` for human-readable feedback. If you are part
of a controlled review round, also complete `REVIEWER_RETURN_TEMPLATE.json` so
the internal intake path can classify perspective coverage and findings.

## 1. Read The Boundary First

Before running commands, read:

```text
README.md
REVIEWER_GUIDE.md
docs/LIMITATIONS.md
CLAIM_LEDGER.md
DO_NOT_CLAIM.md
RECEIPT_INDEX.md
```

You should understand that Elaine Core v0.1 currently demonstrates local
proof-before-action and claim-boundary behavior on synthetic examples. It does
not prove real-world protection, deployment readiness, compliance, or external
validation.

Elaine Core v0.1 does not require secrets. If a future controlled setup lane
does require a credential, `GUIDED_SETUP_AND_SECRET_ENTRY.md` is the required
user-led pattern: password manager or manual entry, local hidden prompt,
redacted receipt, and no secret in chat or reviewer returns.

## 2. Run The Proof Lab

```bash
python PROOF_LAB/elaine_research_proof_lab.py export-manifest
python PROOF_LAB/elaine_research_proof_lab.py run-cases
python PROOF_LAB/elaine_research_proof_lab.py search --query "proof before action"
python PROOF_LAB/elaine_research_proof_lab.py show-claim --claim LAB-CLAIM-002
```

Expected receipt:

```text
receipts/elaine-proof-lab-receipt.json
```

## 3. Inspect Runtime Core

Runtime Core is a local CLI only. It is not a service, API, MCP server, model
runtime, installer, or workstation controller.

```bash
python RUNTIME_CORE/elaine_runtime_core.py status --json
python RUNTIME_CORE/elaine_runtime_core.py doctor --json
python RUNTIME_CORE/elaine_runtime_core.py proof-lab --json
python RUNTIME_CORE/elaine_runtime_core.py proof-lab --run --json
python RUNTIME_CORE/elaine_runtime_core.py receipts --json
python RUNTIME_CORE/elaine_runtime_core.py gates --json
```

## 4. Docker Proof Runtime Status

The Docker proof runtime is the preferred next reviewer path. This package is
Docker-source-prepared. The private Tuesday readiness lane has separate
Docker build/run/proof-lab receipts outside this clean package; if those
receipts are not included with a reviewer bundle, do not treat Docker proof as
self-contained package evidence.

Read:

```text
DOCKER_PROOF_RUNTIME.md
DOCKER_A3_EXECUTION_GATE.md
```

Do not pull images or run containers unless the gate is explicitly approved.

## 5. Expected Reviewer Result

A reviewer should be able to answer:

- What does Elaine Core v0.1 demonstrate today?
- What evidence supports that claim?
- Which claims are blocked?
- Which next proof would make the package stronger?

Record feedback in `REVIEWER_FEEDBACK_FORM.md`.

## 6. Stop Conditions

Stop review and report a defect if:

- any command needs private workspace files;
- any command needs an API key or network provider;
- any command modifies system settings;
- any receipt claims production readiness or security benefit;
- any private, employer, business-plan, patent-sensitive, raw-log, or secret
  material appears.
