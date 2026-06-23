# Elaine Core Versioning Policy

Elaine Core uses semantic versioning for public-review packages.

## Version Shape

`MAJOR.MINOR.PATCH[-label]`

- `MAJOR`: incompatible package, command, receipt, or claim-ledger changes.
- `MINOR`: new proof-lab behavior, documentation surface, receipt schema support, or reviewer workflow that remains backward compatible.
- `PATCH`: wording fixes, scan repairs, receipt refreshes, or non-breaking validator updates.
- `label`: prerelease state such as `alpha`, `review`, or `rc`.

## Current Version

`0.1.0-alpha`

This version is a controlled-alpha proof package. It does not claim production readiness, security outcomes, external validation, Windows support, low-resource support, or public-release approval.

## Release Rule

Every release candidate must include:

- package manifest and tree hash;
- updated changelog entry;
- release notes;
- claim ledger review;
- safety scans;
- proof-lab receipt;
- known blockers.

