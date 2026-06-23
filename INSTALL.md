# Elaine Core v0.1 Install Guide

Elaine Core v0.1 is a controlled-alpha proof package. It is meant to be verified from a clean folder without access to the private Elaine OS workspace.

## Requirements

- Python 3.11 or newer.
- A terminal in the package root.
- No API keys, provider accounts, hosted retrieval, Git credentials, or private data.

## Quick Install Check

From the package root:

```powershell
python verify_install.py
```

On Linux/macOS:

```bash
python3 verify_install.py
```

Expected output is five lines or fewer and includes:

```text
ELAINE_INSTALL_CHECK=PASS
receipt=receipts/install-summary.json
```

For machine-readable output:

```powershell
python verify_install.py --json
```

## What The Verifier Does

- Confirms Python 3.11 or newer.
- Confirms the proof lab and Runtime Core scripts exist.
- Runs the six synthetic proof cases.
- Runs Runtime Core doctor.
- Writes `receipts/install-summary.json`.
- Writes `receipts/install-proof-lab-receipt.json`.
- Writes `receipts/install-runtime-doctor-receipt.json`.

No AI agent is required for normal install verification.

For minimal terminal output:

```powershell
python verify_install.py --quiet
```

The JSON output uses `elaine.install-summary.v2` and includes the SHA-256
hashes of the local executable scripts invoked by the verifier.

## Controlled Installation Preflight

Elaine Core v0.1 does not install or configure a live runtime. If a future
setup lane asks Elaine to take control of installation steps, read
`docs/CONTROLLED_INSTALLATION_GOVERNANCE.md` and run the read-only baseline:

```powershell
python tools\elaine_security_baseline_check.py
```

That baseline is SCAP/STIG-inspired, not a formal SCAP scan, STIG result,
compliance result, security validation, or production-readiness proof.
Host-changing installation work remains blocked unless an exact A3 owner gate
names the target, action, allowed commands or script, rollback path, checks,
proof path, expiry, blocked actions, and stop conditions.

## Direct Checks

These are the underlying checks that `verify_install.py` runs:

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
- Install receipts are written under `receipts/`.
- No network, provider, hosted retrieval, Git, deployment, or public sharing is required.

## Agent Verification

If a user chooses to involve Codex or another coding agent, give the agent
`INSTALL_AGENT.md` or `CODEX_FREE_PROMPT.txt`. The agent should run only
`python --version` and `python verify_install.py --json`, then stop if the
status is `pass`.

## What This Does Not Install

This package does not install a persistent service, MCP server, model runtime, endpoint monitor, SIEM connector, private RAG index, or autonomous workstation controller.

## Guided Setup Note

Elaine Core v0.1 does not need passwords, API keys, GitHub tokens, SSH private
keys, or provider credentials. If a future controlled setup path asks for a
sensitive value, read `GUIDED_SETUP_AND_SECRET_ENTRY.md` first. The expected
pattern is user-led: choose password-manager or manual entry, paste the value
only into a local hidden terminal prompt, and keep the receipt redacted.
