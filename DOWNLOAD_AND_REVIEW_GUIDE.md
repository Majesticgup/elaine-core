# Elaine Core v0.1 Download And Review Guide

Status: PUBLIC PROOF PACKAGE GUIDE / NOT PRODUCTION READY / NOT A SECURITY PRODUCT.

Use this file if you downloaded Elaine Core v0.1 from GitHub and want to know
what to do next. The goal is not to install a production product. The goal is
to inspect a public proof package, run the local proof lab, and return feedback
that helps decide what claims are supported, unclear, or blocked.

## What You Have

Elaine Core v0.1 is a public proof package for a proposed local governance
framework around AI-assisted engineering, vibe coding, evidence records,
claim boundaries, owner gates, and proof receipts.

The package is designed to run without:

- private Elaine OS workspace access;
- API keys;
- provider accounts;
- hosted retrieval;
- secrets;
- system-setting changes;
- deployment;
- production data.

## What You Are Not Being Asked To Prove

Do not treat this package as proof of:

- production readiness;
- real-world protection or security outcomes;
- compliance, SOC, MDR, EDR, SIEM, or managed-security capability;
- deployment readiness;
- customer validation;
- independent endorsement;
- patent protection or legal sufficiency.

## First 20-Minute Path

1. Read `README.md`, `DO_NOT_CLAIM.md`, and `CLAIM_LEDGER.md`.
2. Read `QUICKSTART.md`.
3. Run the proof lab commands from the package root.
4. Inspect `receipts/elaine-proof-lab-receipt.json`.
5. Fill out `REVIEWER_FEEDBACK_FORM.md`.
6. If you are part of controlled review, also copy and fill
   `REVIEWER_RETURN_TEMPLATE.json`.

## Commands

Run from the package root:

```bash
python PROOF_LAB/elaine_research_proof_lab.py export-manifest
python PROOF_LAB/elaine_research_proof_lab.py run-cases
python PROOF_LAB/elaine_research_proof_lab.py search --query "proof before action"
python PROOF_LAB/elaine_research_proof_lab.py show-claim --claim LAB-CLAIM-002
python RUNTIME_CORE/elaine_runtime_core.py status --json
python RUNTIME_CORE/elaine_runtime_core.py doctor --json
python RUNTIME_CORE/elaine_runtime_core.py gates --json
```

Expected local receipt:

```text
receipts/elaine-proof-lab-receipt.json
```

## Five Questions To Answer

Answer these in plain language before you worry about technical details:

1. What do you think Elaine Core v0.1 is?
2. What does the package prove today?
3. What does the package clearly not prove yet?
4. What part was confusing, overstated, or too hard to follow?
5. What is the next proof you would need before trusting a stronger claim?

## Role-Based Review Options

Use the role closest to your perspective. One reviewer may cover more than one
perspective, but only if they can credibly answer for both.

| Role | Main job | Strong return includes |
| --- | --- | --- |
| Developer / engineer | Runability and reproducibility | Commands run, receipt inspected, missing step or dependency reported |
| Cybersecurity reviewer | Claim pressure and risk boundary | Unsupported security claims, leakage risks, and blocked actions identified |
| Nontechnical reviewer | Plain-language understanding | One-sentence explanation, confusing terms, and user-facing gaps |
| Skeptical reviewer | Overclaim pressure | Inflated wording, weak proof, and hidden assumptions called out |
| Creative / communications reviewer | Trust, voice, and onboarding clarity | Places where the story, language, or first-run path fails |
| Production / operations reviewer | Process completeness | Handoff gaps, stop conditions, role clarity, and return workflow issues |

## Controlled Review Return Path

If you are part of a controlled reviewer round, return two things:

1. `REVIEWER_FEEDBACK_FORM.md` completed in plain language.
2. A completed copy of `REVIEWER_RETURN_TEMPLATE.json`.

The JSON is intentionally fail-closed. Leave no required yes/no field blank.
Do not include secrets, private paths, account details, raw logs, business-plan
details, customer/employer information, patent-sensitive material, or screenshots
with private data.

Required perspective coverage for the current production-readiness gate:

- `nontechnical`
- `cybersecurity`
- `developer`
- `skeptical`

If only three people review, at least one return must include more than one
covered perspective. Otherwise the perspective-coverage gate remains blocked.

## Stop Conditions

Stop and report a defect if:

- a command requires private workspace files;
- a command requires an API key or hosted provider;
- a command requires network access unexpectedly;
- a command changes system or account settings;
- a document claims production readiness, security outcomes, compliance,
  deployment, endorsement, or patent protection;
- private or secret-shaped material appears in the package or generated output.

## Good Feedback Looks Like

Useful feedback is specific. Point to the file, heading, command, receipt, or
claim that caused the issue. If something sounds wrong but you are not sure why,
say that directly and explain what made you hesitate.

Good reviewer findings can be closed later as:

- `fixed`;
- `accepted_risk`;
- `rejected_out_of_scope`.

Any missing return, missing perspective, or open finding keeps the stronger
production-readiness goal blocked.
