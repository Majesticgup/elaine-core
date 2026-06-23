# Elaine Core Logging And Redaction Policy

Elaine Core v0.1 uses receipts for local review. Receipts should explain what happened without exposing secrets, private workspace paths, raw logs, account data, customer data, business-plan material, or patent-sensitive implementation details.

## Receipt Rules

- Record command intent, data class, status, checks, boundary flags, and claim ceiling.
- Prefer relative package paths over private absolute paths.
- Store failure class and remediation notes without raw secret values.
- Treat screenshots, terminal logs, and model output as review material that must be scanned before sharing.

## Redaction Rules

Remove or block:

- API keys, tokens, private keys, session cookies, recovery codes, and authorization header values.
- Private home paths, private network addresses, and raw hostnames.
- Employer, customer, or account-specific data.
- Raw security logs that could contain identifiers or secrets.
- Patent-sensitive implementation details and private business plans.

## Sharing Rule

No receipt, log, screenshot, or generated output is public-safe until it passes the package safety scan and claim-boundary review.
