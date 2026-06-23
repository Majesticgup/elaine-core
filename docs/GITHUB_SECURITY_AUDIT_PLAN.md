# Elaine Core GitHub Security Audit Plan

Status: READ-ONLY AUDIT PLAN / NO ACCOUNT SETTING CHANGES / NO SECURITY CLAIM.

This plan defines how Elaine should audit the GitHub account and repository
posture after the v0.1 public proof package is released. It does not perform a
live GitHub account audit by itself, does not change settings, and does not
claim that the repository is secure.

The read-only audit plan includes no account setting changes.

## Current Target

- Account or owner: `Majesticgup`
- Repository: `Majesticgup/elaine-core`
- Branch: `main`
- Current package release: `v0.1.0`
- Current claim ceiling: public proof package only; not production-ready, not
  security-validated, not compliance evidence.

## Automation Plan

1. Keep local package checks automated through proof-lab and Runtime Core
   receipts.
2. Keep first-reviewer returns structured through `REVIEWER_RETURN_TEMPLATE.json`.
3. Keep secret-entry work user-led through `GUIDED_SETUP_AND_SECRET_ENTRY.md`
   and a redacted local receipt.
4. Run GitHub posture audits as read-only checks first.
5. Convert every live GitHub setting change into a separate write gate with
   target, action, rollback, proof path, and stop conditions.

## Read-Only Audit Scope

The first GitHub audit should inspect, without changing:

- repository visibility and default branch;
- branch protection or rulesets for `main`;
- collaborators, teams, outside collaborators, invitations, deploy keys, and
  GitHub Apps with repository access;
- SSH keys, personal access tokens, OAuth apps, and GitHub Apps visible to the
  account owner where allowed;
- security log and audit log entries available to the account or organization;
- secret scanning, push protection, non-provider pattern scanning, and alert
  state;
- Dependabot alerts and Dependabot security update settings;
- dependency graph and dependency review posture;
- CodeQL/code scanning setup and alert state;
- GitHub Actions workflow permissions, secrets, variables, environments,
  runners, caches, and artifact retention;
- releases, tags, packages, webhooks, Pages settings, environments, and
  repository settings that could expose data or permit unsafe automation;
- issue, project, and discussion surfaces that could contain secrets or private
  material.

## Security Features To Consider

The audit should check whether these GitHub features are available and enabled
where appropriate:

- secret scanning;
- push protection;
- Dependabot alerts;
- Dependabot security updates;
- dependency graph;
- CodeQL or code scanning;
- branch protection or repository rulesets;
- required reviews and required status checks before merge;
- restricted GitHub Actions permissions;
- private vulnerability reporting or a clear `SECURITY.md` path;
- 2FA, passkeys, SSH key review, token review, OAuth app review, and GitHub App
  review for the owning account or organization;
- GitHub Projects or issues for tracking `PG-051`, `PG-052`, `PG-053`, and
  security findings.

AI-assisted GitHub features can help triage findings, but they are not evidence
by themselves. Do not paste secrets into AI features. Treat Copilot Autofix,
code scanning suggestions, and AI summaries as candidate output that needs
human review and a receipt before merge.

## Official Reference Set

- GitHub security features:
  `https://docs.github.com/en/code-security/getting-started/github-security-features`
- Quickstart for securing a repository:
  `https://docs.github.com/en/code-security/getting-started/quickstart-for-securing-your-repository`
- Push protection:
  `https://docs.github.com/en/code-security/concepts/secret-security/push-protection`
- GitHub credential types:
  `https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/github-credential-types`
- Security log events:
  `https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/security-log-events`
- Organization security:
  `https://docs.github.com/en/organizations/keeping-your-organization-secure`

## Required A4 Read-Only Gate

Use this gate text before live account or repository inspection:

```text
Approve A4 read-only GitHub audit: provider GitHub, target account Majesticgup
and repo Majesticgup/elaine-core, read-only settings/security/branch/
collaborator/releases/actions/projects/alerts metadata, no writes, no secrets,
no token display, no setting changes, proof path
outputs/elaine-tuesday-readiness-2026-06-20/github-audit/, stop if auth prompt,
permission error, private repo/corpus beyond target, or write action required.
```

Any remediation needs a separate write gate. Examples include enabling push
protection, enabling CodeQL, changing branch protection, revoking credentials,
editing collaborators, changing Actions permissions, or creating GitHub
Projects/issues.

## Audit Output

The audit should produce:

- a redacted SITREP;
- a machine-readable finding ledger;
- a settings coverage table;
- a leakage scan summary;
- a credential/access review summary with no raw tokens or key material;
- remediation recommendations split into `local_docs`, `github_setting_write`,
  `credential_owner_action`, and `blocked_without_owner_gate`;
- a claim boundary that says the audit is posture review, not proof of security
  outcomes, compliance, SOC/MDR capability, or production readiness.
