# Elaine Core v0.1 Troubleshooting

This guide keeps failures reviewable. Do not work around failures by adding private files, API keys, hosted services, or unpublished Elaine OS workspace paths.

## Python Is Not Found

Install Python from the operating system's normal trusted channel, then rerun the command. Do not add provider SDKs or API keys for this package.

## Proof Lab Fails

Check:

- You are in the package root.
- `PROOF_LAB/docproof_cases.json` exists.
- The output path under `receipts/` is writable.
- The failure is recorded in the receipt.

If the proof lab fails, the package is not ready for that reviewer environment.

## Runtime Core CLI Fails

Check:

- You are using the package-local `RUNTIME_CORE/elaine_runtime_core.py`.
- You are not expecting a service, API, MCP server, or model runtime.
- The command output and receipt identify the blocked or missing condition.

## Claims Sound Too Strong

Use `DO_NOT_CLAIM.md` and `CLAIM_LEDGER.md`. Downgrade the sentence unless current proof directly supports it.

## Private Data Appears

Stop review immediately. Remove the package copy from circulation, record the path and file name, and rebuild the package from source truth after remediation.

