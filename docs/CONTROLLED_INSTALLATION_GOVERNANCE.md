# Controlled Installation Governance

Status: FUTURE CONTROLLED EXECUTION PLAN / READ-ONLY PREFLIGHT INCLUDED /
NOT A PRODUCTION INSTALLER / NOT A FORMAL SCAP OR STIG RESULT.

Elaine Core v0.1 currently verifies a public proof package. It does not install
a service, MCP server, model runtime, endpoint monitor, private RAG index, or
workstation controller. If a future user becomes comfortable letting Elaine
take a more active role in setup, that path must be governed by this workflow.

## Control Objective

Elaine should not merely describe governance. It should enforce the workflow
with mode separation, gate checks, receipts, rollback planning, and stop
conditions before any host-changing installation step is allowed.

## Modes

### 1. Verify Only

Command:

```bash
python verify_install.py
```

This mode uses no model call, network, package install, provider account, Git,
Docker, hosted retrieval, raw secret, or host configuration change. If it
passes, ordinary installation verification stops.

### 2. Agent-Assisted Failure Diagnosis

Use only after `verify_install.py` fails. The agent may inspect only the named
failed check or missing file, with the limits in `INSTALL_AGENT.md` and
`config/credit-policy.json`.

### 3. Controlled Installation Execution

This mode is not active in v0.1. Any future host-changing installation action
requires an exact A3 owner gate that names:

- target;
- action;
- allowed command or script;
- data class;
- rollback path;
- checks;
- proof path;
- expiry;
- blocked actions;
- stop conditions.

Without that gate, Elaine must not install packages, change settings, start
services, alter credentials, call providers, deploy, publish, or claim
production/security/compliance readiness.

## SCAP/STIG-Inspired Baseline

Run the read-only baseline before any controlled execution gate:

```bash
python tools/elaine_security_baseline_check.py --json
```

This is a SCAP/STIG-inspired readiness checklist, not formal SCAP content, not a DISA STIG scan,
not a compliance result, and not a security certification.
Its purpose is to confirm that Elaine has the local controls needed to govern a
future installation lane:

- verification and security review are separate;
- host-changing work is gated;
- generated receipts and context caches are not committed;
- secrets are not required for v0.1 verification;
- raw secrets are not persisted by helper flows;
- rollback and proof paths are mandatory before changes;
- blocked claims remain blocked.

## Required Execution Shape For Future Installer Work

1. Run `python verify_install.py`.
2. Run `python tools/elaine_security_baseline_check.py --json`.
3. Ask whether the user prefers password-manager-assisted entry or manual
   hidden terminal entry if a future setup lane needs a secret.
4. Prepare a dry-run plan with exact commands, expected files, proof path, and
   rollback path.
5. Stop for the exact A3 owner gate before changing the host.
6. Execute only the approved commands.
7. Write receipts.
8. Re-run verification and baseline checks.
9. Classify findings before claiming any stronger state.

## Blocked Claims

Passing this baseline does not prove production readiness, security benefit,
SOC/MDR replacement, compliance, formal SCAP/STIG conformance, deployment,
external validation, endorsement, or patent protection.
