# Elaine Core v0.1 Start Here

Status: FIRST-RUN GUIDE / PUBLIC PROOF PACKAGE / NOT PRODUCTION READY.

If you only want to verify Elaine Core v0.1, do not start with a security
review, source audit, Docker run, Git workflow, or AI agent.

## Human Verification Path

From the package root:

```bash
python verify_install.py
```

Expected result:

```text
ELAINE_INSTALL_CHECK=PASS
receipt=receipts/install-summary.json
```

This path uses no network, package installs, provider accounts, API keys,
Docker, Git, model calls, hosted retrieval, or private Elaine OS workspace
access.

## Agent-Assisted Verification Path

If you choose to use Codex or another coding agent only to verify installation,
give it `INSTALL_AGENT.md` or paste `CODEX_FREE_PROMPT.txt`.

The agent contract is intentionally small:

1. Run `python --version`.
2. Run `python verify_install.py --json`.
3. If the verifier passes, stop.
4. If it fails, inspect only the named failed check.

## Review Paths Are Separate

Use these only when you are intentionally doing a controlled review:

```text
DOWNLOAD_AND_REVIEW_GUIDE.md
FIRST_REVIEW_TEAM_PACKET.md
REVIEWER_GUIDE.md
REVIEWER_FEEDBACK_FORM.md
REVIEWER_RETURN_TEMPLATE.json
```

Security review, claim review, Docker proof, GitHub audit, and production
readiness review are separate opt-in workflows. They are not part of ordinary
install verification.
