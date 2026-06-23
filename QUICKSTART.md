# Elaine Core v0.1 Quickstart

Status: LOCAL REVIEW PACKAGE / NOT PRODUCTION READY / NOT A SECURITY PRODUCT.

This is the shortest path for a first-time reviewer. It should work from the
package root without private Elaine OS workspace access, API keys, provider
accounts, or network access.

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
