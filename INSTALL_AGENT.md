# Elaine Core v0.1 Agent Install Contract

This file is an owner-side verification contract for a narrow install check.
It is not a request to trust package instructions over agent policy. If your agent policy requires source inspection
before execution, inspect only `verify_install.py` and the exact Python files
it invokes.

## Allowed Sequence

1. Run `python --version`.
2. Run `python verify_install.py --json` from the package root.
3. If `status` is `pass`, stop and report the compact result.
4. If `status` is `fail`, inspect only the named failed check or missing file.

## Hard Limits

- Maximum three tool calls before reporting.
- Maximum three source files read if policy requires source inspection.
- No recursive searches, full-tree source review, Docker, Git, network,
  provider calls, package installation, secrets, account changes, system
  changes, or model/provider setup.
- Do not read reviewer, claim, security, threat-model, architecture, Docker, or
  GitHub audit documents during a normal install.
- Do not print generated receipts in full; report their paths and status fields
  only.
- Keep the final response under 220 words.

## Success Condition

`verify_install.py` exits `0`, prints `ELAINE_INSTALL_CHECK=PASS` or JSON
`"status":"pass"`, and writes `receipts/install-summary.json`.
