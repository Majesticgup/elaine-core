# Security Policy

Status: PUBLIC PROOF PACKAGE SECURITY POLICY / NO BOUNTY / NOT SECURITY VALIDATION.

This package is a public proof package. It does not operate a managed security
response program, hosted product, or vulnerability bounty.

Elaine is designed around local cyber-governance and AI action boundaries. That means security reports should focus on whether the package leaks private material, overstates its protection, weakens the proof-before-action model, or creates unsafe automation expectations.

## Safe Report Types For Future Public Use

- Secret or private-path leakage in public files.
- Unsupported production, compliance, customer, patent, or endorsement claims.
- Proof-lab behavior that contradicts the documented case expectations.
- Documentation that implies external validation not present in the package.
- Unsafe vibe-coding guidance, including unchecked AI-generated code, unreviewed automation, hidden data movement, or missing human approval for higher-risk actions.
- LLM boundary failures in public examples, including prompt injection, excessive agency, sensitive-data disclosure, or unsupported security claims.

## Not In Scope

- Excluded: private Elaine OS workspace internals.
- Excluded: business-plan material.
- Excluded: patent-sensitive implementation detail.
- Excluded: employer or customer material.
- Excluded: requests for managed security operations.

## Vibe-Coding Security Rules

- Treat AI-generated code, scripts, reports, and security advice as candidate output until reviewed.
- Do not run generated commands against a real system unless the action, data class, rollback path, and expected proof are clear.
- Do not paste secrets, employer/customer data, private logs, private topology, or patent-sensitive implementation detail into model prompts.
- Require source references for security claims.
- Keep public claims lower than the evidence.
- Record receipts for material security decisions.
- Prefer local proof checks before hosted tools or provider calls.
- For future credential setup lanes, use `GUIDED_SETUP_AND_SECRET_ENTRY.md` so
  passwords, API keys, GitHub tokens, SSH private keys, and passphrases stay in
  a local hidden prompt and out of chat, docs, screenshots, issues, receipts, and
  reviewer returns.

## Source-Backed Release Pressure

The local release review uses public guidance as pressure, not as validation:

- OWASP LLM/GenAI risk categories pressure the package to treat prompt injection, insecure output handling, sensitive-data exposure, supply-chain risk, excessive agency, overreliance, and unbounded consumption as design hazards.
- GitHub security guidance pressures any future public repository to enable dependency, secret-scanning, and code-security review features where available.
- OpenSSF Scorecard and SLSA pressure the project to document supply-chain expectations, branch/review discipline, dependency policy, and provenance goals before broader release.
- NIST SSDF AI companion guidance pressures AI-assisted development to keep model-generated material reviewable and bounded.

These sources do not validate Elaine. They only define risks and release hygiene expectations that the package must not overclaim past.

## GitHub Posture Audit

`docs/GITHUB_SECURITY_AUDIT_PLAN.md` defines the read-only GitHub audit plan
for repository visibility, branch protection or rulesets, collaborators, deploy
keys, GitHub Apps, security logs, secret scanning, push protection, Dependabot,
CodeQL/code scanning, GitHub Actions permissions, releases, tags, packages,
webhooks, and project/issue surfaces. The plan does not authorize live account
inspection or setting changes by itself.
