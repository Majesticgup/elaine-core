# A3 Docker Proof Runtime Execution Gate

Status: PREPARED / EXECUTED IN LOCAL TUESDAY LANE / NEW RUNS REQUIRE A3.

## Purpose

Prove that Elaine Core v0.1 can run its proof lab from a clean Docker runtime
using only the package files and synthetic/public-safe proof fixtures.

Local Tuesday readiness receipts may show that this gate has already been run
once. This package file still does not authorize another image pull, build, or
container execution without a fresh exact A3 lease.

## Proposed Approval Wording

```text
Approved: A3 Docker proof runtime execution for Elaine Core v0.1.

Target:
outputs/elaine-tuesday-readiness-2026-06-20/fresh-copy-sim/elaine-core-v0.1

Allowed:
- verify one official Python 3.12 slim base image digest
- pull only that pinned base image if not already present
- build one local image named elaine-core-prooflab:local
- run one no-network proof-lab container
- use --read-only, --network none, --cap-drop ALL, no-new-privileges, and tmpfs runtime receipts
- write a redacted Docker proof receipt under the Tuesday readiness lane
- update the public export manifest and readiness board

Blocked:
- Docker socket mounts
- --privileged
- host networking
- private Elaine OS workspace mounts
- provider/API calls
- hosted retrieval over Elaine data
- raw secrets
- Git staging, commit, push, or GitHub creation
- public sharing, deployment, Anthropic sharing, counsel sharing, patent filing
- destructive cleanup outside the named image/container artifacts
```

## Required Outputs

- Docker build receipt:
  `outputs/elaine-tuesday-readiness-2026-06-20/docker-proof-runtime/docker-build-receipt.json`.
- Docker run receipt:
  `outputs/elaine-tuesday-readiness-2026-06-20/docker-proof-runtime/docker-run-receipt.json`.
- Fresh proof-lab receipt copied from the container tmpfs:
  `outputs/elaine-tuesday-readiness-2026-06-20/docker-proof-runtime/docker-proof-lab-receipt.json`.
- Post-run validator receipt:
  `outputs/elaine-tuesday-readiness-2026-06-20/docker-proof-runtime/docker-proof-runtime-execution-check-current.json`.
- Manifest update showing Docker files are included and Docker execution boundary
  flags reflect only the approved run.
- Claim ledger update confirming Docker proof does not promote production,
  security-benefit, native host, Windows, VM, compliance, SOC/MDR, or external
  validation claims.

## Required Post-Run Validator

After the A3 run, execute the local receipt validator:

```powershell
python outputs\elaine-tuesday-readiness-2026-06-20\Run-ElaineDockerProofRuntimeExecutionReceiptCheck.py `
  --root . `
  --receipt-dir outputs\elaine-tuesday-readiness-2026-06-20\docker-proof-runtime `
  --out outputs\elaine-tuesday-readiness-2026-06-20\docker-proof-runtime\docker-proof-runtime-execution-check-current.json
```

The validator must pass before any Docker proof is promoted in the readiness
board, public export manifest, GitHub packet, Anthropic packet, or release
decision packet.

## Pass Criteria

All of these must be true:

- base image is pinned by digest and recorded;
- Docker build exits `0`;
- Docker run exits `0`;
- container command uses `--network none`;
- container command uses `--read-only`;
- container command uses `--cap-drop ALL`;
- container command uses `--security-opt no-new-privileges:true`;
- no Docker socket mount is used;
- no `--privileged` mode is used;
- no private Elaine OS workspace path is mounted;
- no provider/API call, hosted retrieval, raw-secret handling, Git action, or
  public sharing occurs;
- proof-lab receipt exists and reports deterministic local proof support;
- tmpfs output does not hide packaged `receipts/README.md`;
- boundary flags remain false for production, security-benefit, compliance,
  SOC/MDR, external validation, public release, and deployment claims.

## Rollback / Cleanup Boundary

Allowed cleanup after the run is limited to:

- remove the local image `elaine-core-prooflab:local` if the owner requests it;
- remove only containers created by this exact gate if any remain.

Blocked cleanup:

- no `docker system prune`;
- no broad image, volume, container, or network deletion;
- no cleanup outside the named Docker image/container artifacts;
- no host filesystem deletion.

## Stop Conditions

Stop immediately if:

- the base digest cannot be verified;
- Docker tries to use a private workspace path;
- the container needs network access;
- the proof lab attempts provider/API calls;
- a receipt contains private paths, secrets, employer/customer material, business
  plan detail, patent-sensitive detail, raw logs, or account data;
- any command needs a broader A4/A5 gate.
