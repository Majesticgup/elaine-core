# Elaine Core v0.1 Guided Setup And Secret Entry

Status: USER-GUIDED SETUP PATTERN / V0.1 NEEDS NO SECRETS / NOT PRODUCTION READY.

Elaine Core v0.1 does not require passwords, API keys, provider accounts, Git
credentials, hosted retrieval, or private data. You can run the proof lab and
Runtime Core checks without giving Elaine or an assistant any secret.

Elaine Core v0.1 does not require passwords, API keys, provider accounts, Git credentials, hosted retrieval, or private data.

This file defines the safe pattern for future controlled setup lanes where a
reviewer or operator does need to enter a passphrase, SSH key passphrase, API
key, token, or password on their own machine.

## First Question

Before any secret-entry step, the guide or assistant should ask:

```text
Do you use a password manager, or would you rather enter everything manually?
```

Allowed answers:

- `password_manager`: you will open your password manager locally and paste
  the value only into the local terminal prompt.
- `manual`: you will type or paste the value yourself into the local terminal
  prompt.
- `skip`: no secret will be entered; continue only with no-secret checks.

## Four Setup Questions

Answer these before a credential prompt appears:

1. What are you setting up: GitHub SSH, GitHub token, provider API key, local
   password, or other?
2. Should the value be session-only, stored by your password manager, or stored
   in a local file you control?
3. What redacted receipt path should prove the prompt happened?
4. What stop condition should pause the setup: failed auth, unexpected network,
   account setting change, missing permission, or unclear scope?

For Elaine Core v0.1, the default answer is `skip`: no secret is needed.

## Hands-Off Local Prompt Pattern

When a future controlled lane needs a sensitive value, the assistant should
guide the user through a local terminal flow:

1. The assistant opens or points to a local terminal command.
2. The user chooses `password_manager`, `manual`, or `skip`.
3. The user pastes the sensitive value only into the local hidden prompt.
4. The helper validates only that a value was provided.
5. The helper writes a redacted receipt.
6. The raw value is never printed, logged, pasted into chat, committed, or put
   in a reviewer return.

Never paste secrets into chat, docs, GitHub issues, pull requests, screenshots,
receipts, model prompts, or support messages.

## Local Helper

The package includes a PowerShell helper for the prompt-and-receipt pattern:

```powershell
powershell -ExecutionPolicy Bypass -File tools\Start-ElaineGuidedSecretPrompt.ps1
```

The helper is a local prompt rehearsal. It does not configure GitHub, call a
provider, install software, change account settings, persist the secret, or
push to Git. It writes only a redacted receipt unless the user skips receipt
creation.

Expected receipt:

```text
receipts/guided-secret-entry-receipt.json
```

## Reviewer Boundary

For this public proof package, a reviewer should report a defect if any normal
v0.1 command asks for:

- a password;
- an API key;
- a GitHub token;
- an SSH private key;
- a provider account;
- a private Elaine OS workspace path;
- customer, employer, business-plan, patent-sensitive, or raw-log material.

If a future controlled reviewer packet includes a credential setup lane, it
must name the owner gate, target system, allowed action, stop conditions,
redacted receipt path, and rollback or revocation path.
