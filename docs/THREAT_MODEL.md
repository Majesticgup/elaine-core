# Threat Model

## Assets

- User control over local security decisions.
- User control over what data an LLM may see.
- Truthfulness of public claims.
- Owner authority over higher-risk actions.
- Evidence and limitation records.
- Private source truth excluded from public release.
- Public reader trust.

## Risks

- Unsupported claims promoted into public language.
- Missing evidence hidden by fluent AI output.
- Approval fatigue around broad or vague prompts.
- Private material leaked through release artifacts.
- Repository publication before license or counsel review.
- Synthetic examples misread as production evidence.
- AI-generated commands treated as trusted without review.
- Personal cyber-hygiene guidance overstated as proven protection.
- LLM integration examples used without data-boundary checks.

## Current Controls

- Claim ledger.
- Do-not-claim list.
- Synthetic proof lab.
- Release review checklist.
- Apache-2.0 license posture for the v0.1.0 public proof package, with future release expansion still gated.
- Public/private disclosure notice.
- Vibe-coding safety rules.

## Source-Backed Risk Pressure

External public guidance pressures the threat model but does not validate Elaine:

- NIST CSF and CIS Controls reinforce that cyber-hygiene framing should stay tied to governance, visibility, prioritization, and limitation, not broad protection claims.
- OWASP LLM/GenAI risks reinforce that AI-assisted workflows need prompt-injection, insecure-output, sensitive-data, supply-chain, excessive-agency, and overreliance boundaries.
- GitHub, OpenSSF, and SLSA guidance reinforce that a public repository needs release hygiene, dependency/security settings, provenance expectations, and disclosure instructions.

## Out Of Scope

This package does not prove runtime enforcement, bypass resistance, production security, compliance, independent auditability, or legal sufficiency.
