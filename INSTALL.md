# Elaine Core v0.1 Install Guide

Elaine Core v0.1 is a controlled-alpha proof package. It is meant to be run from a clean folder so a reviewer can inspect the proof lab, Runtime Core CLI, receipts, and limitations without access to the private Elaine OS workspace.

## Requirements

- Python 3.11 or newer.
- A terminal in the package root.
- No API keys, provider accounts, hosted retrieval, Git credentials, or private data.

## Quick Install Check

From the package root:

```powershell
python PROOF_LAB\elaine_research_proof_lab.py run-cases --out receipts\install-proof-lab-receipt.json
python RUNTIME_CORE\elaine_runtime_core.py doctor --out receipts\install-runtime-doctor-receipt.json
```

On Linux/macOS:

```bash
python3 PROOF_LAB/elaine_research_proof_lab.py run-cases --out receipts/install-proof-lab-receipt.json
python3 RUNTIME_CORE/elaine_runtime_core.py doctor --out receipts/install-runtime-doctor-receipt.json
```

## Expected Result

- Proof lab exits `0`.
- Runtime Core CLI exits `0`.
- Receipts are written under `receipts/`.
- No network, provider, hosted retrieval, Git, deployment, or public sharing is required.

## What This Does Not Install

This package does not install a persistent service, MCP server, model runtime, endpoint monitor, SIEM connector, private RAG index, or autonomous workstation controller.

## Guided Setup Note

Elaine Core v0.1 does not need passwords, API keys, GitHub tokens, SSH private
keys, or provider credentials. If a future controlled setup path asks for a
sensitive value, read `GUIDED_SETUP_AND_SECRET_ENTRY.md` first. The expected
pattern is user-led: choose password-manager or manual entry, paste the value
only into a local hidden terminal prompt, and keep the receipt redacted.
