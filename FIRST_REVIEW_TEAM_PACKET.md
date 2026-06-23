# Elaine Core v0.1 First Review Team Packet

Status: FIRST CONTROLLED REVIEW PACKET / PUBLIC-SAFE / NOT PRODUCTION READY.

This packet is tailored for the first three expected reviewers:

- engineer;
- creative director;
- production manager.

The goal is to test whether Elaine Core v0.1 can be understood, run, challenged,
and returned through a structured feedback path without private workspace
access or creator explanation.

## Shared Rules

- Use only the clean public package and any explicitly shared reviewer material.
- Do not ask for private Elaine OS workspace access.
- Do not use secrets, API keys, private accounts, provider calls, or hosted
  retrieval.
- Do not treat the package as production-ready or security-validated.
- Do not reshare a controlled reviewer bundle unless the owner separately
  authorizes it.
- Return specific findings with file names, headings, commands, or claim IDs
  whenever possible.

## Coverage Plan For Three Reviewers

The production-readiness gate needs these perspectives:

- `developer`
- `cybersecurity`
- `nontechnical`
- `skeptical`

With only three people, one person must credibly cover two perspectives.

Recommended first-wave assignment:

| Reviewer | Primary coverage | Secondary coverage | Gate note |
| --- | --- | --- | --- |
| Engineer | `developer` | `cybersecurity` if qualified | If the engineer cannot credibly cover cybersecurity, add a fourth cybersecurity reviewer. |
| Creative director | `nontechnical` | `skeptical` language/claim review | Focus on whether the purpose, trust posture, and first-run story are clear. |
| Production manager | `skeptical` | process/operations review | Focus on whether the handoff, stop conditions, and return workflow are complete. |

## Engineer Card

Primary question: can a capable technical reviewer run and inspect this without
undocumented help?

Do:

1. Read `README.md`, `QUICKSTART.md`, `INSTALL.md`, `CLAIM_LEDGER.md`, and
   `DO_NOT_CLAIM.md`.
2. Run the proof lab and Runtime Core commands in `DOWNLOAD_AND_REVIEW_GUIDE.md`.
3. Inspect `receipts/elaine-proof-lab-receipt.json`.
4. Note any missing dependency, unclear command, platform assumption, or
   surprising side effect.
5. If you are covering `cybersecurity`, pressure-test every security-adjacent
   phrase against `DO_NOT_CLAIM.md`, `docs/THREAT_MODEL.md`, and
   `docs/LIMITATIONS.md`.

Return:

- proof-lab result;
- command that failed, if any;
- missing step or dependency;
- strongest unsupported technical claim;
- whether the package needed private workspace access or creator explanation.

## Creative Director Card

Primary question: can a smart external reader understand what Elaine is without
being pulled into inflated or confusing language?

Do:

1. Read `README.md`, `DOWNLOAD_AND_REVIEW_GUIDE.md`, `PAPER.md`,
   `CLAIM_LEDGER.md`, and `DO_NOT_CLAIM.md`.
2. Write one sentence explaining Elaine Core v0.1 in your own words.
3. Mark phrases that sound too abstract, too promotional, too technical, or too
   strong for the evidence shown.
4. Check whether the first-run path tells a new person what to do without
   insider context.
5. Check whether the limitations are visible before trust-building claims.

Return:

- one-sentence explanation;
- top three confusing terms or sections;
- top three trust/voice issues;
- any language that sounds like a production, security, compliance, endorsement,
  or patent claim;
- whether a nontechnical stakeholder would know what to do next.

## Production Manager Card

Primary question: can this review process be executed and tracked cleanly?

Do:

1. Read `DOWNLOAD_AND_REVIEW_GUIDE.md`, `REVIEWER_GUIDE.md`,
   `REVIEWER_FEEDBACK_FORM.md`, and `REVIEWER_RETURN_TEMPLATE.json`.
2. Check whether the review sequence, stop conditions, return format, and
   closure categories are clear.
3. Identify anything that would block scheduling, assigning, tracking, or closing
   reviewer feedback.
4. Check whether a reviewer can complete the work without owner explanation.
5. Confirm whether the role coverage is enough for the current gate.

Return:

- whether the packet is executable as written;
- missing owner decision, role, deadline, or artifact;
- unclear stop condition;
- finding-closure risks;
- recommendation for the next controlled review round.

## Required Return Artifacts

Each reviewer should return:

1. Completed `REVIEWER_FEEDBACK_FORM.md`.
2. Completed copy of `REVIEWER_RETURN_TEMPLATE.json`.

Use these `covered_perspectives` values:

```json
["developer"]
["developer", "cybersecurity"]
["nontechnical"]
["nontechnical", "skeptical"]
["skeptical"]
```

Do not include raw logs, secrets, private paths, customer/employer detail,
business-plan detail, account information, or patent-sensitive material.

## Gate Outcome

This first wave can help unblock external review readiness. It does not make
Elaine production-ready.

The current production goal remains blocked until:

- enough real reviewer returns exist;
- all required perspectives are covered;
- every finding is fixed, accepted as risk, or rejected as out of scope;
- local intake and closure checks pass.
