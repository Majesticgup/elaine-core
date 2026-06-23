# Elaine Docker Proof Runtime

Status: SOURCE PREPARED / EXECUTION RECEIPTS EXTERNAL / NEW RUNS REQUIRE A3.

This package includes Docker source files for the default controlled-alpha
reviewer proof runtime. Docker is now the preferred first reviewer environment
because it can test the clean package and proof lab without depending on the
private Elaine OS workspace or Hyper-V VM bootstrap.

## What This Proves

After an approved A3 Docker run, this lane should prove:

- the clean package builds from source in a bounded container context;
- the proof lab runs from the packaged files;
- the proof lab can generate a fresh receipt;
- the container uses synthetic/public-safe package data only;
- stronger OS, host-inspection, security-benefit, or production claims remain
  blocked.

## What This Does Not Prove

Docker proof does not prove:

- native Windows behavior;
- native Linux host behavior;
- clean VM bootstrap;
- kernel-level separation beyond Docker's own runtime boundary;
- host inspection safety;
- workstation orchestration;
- compliance, STIG, SOC, MDR, or production readiness;
- that Elaine secures people or systems.

## Hardened Runtime Contract

The Docker run must use these controls unless a later proof explicitly replaces
them:

- verified base image digest supplied through `ELAINE_BASE_IMAGE`;
- non-root container user `elaine`;
- no Docker socket mount;
- no `--privileged`;
- no host networking;
- `--network none` for proof-lab verification;
- `--read-only` root filesystem;
- writable tmpfs only at `/opt/elaine-core/runtime-receipts`;
- `--cap-drop ALL`;
- `--security-opt no-new-privileges:true`;
- no private workspace mount;
- no API keys, provider calls, hosted retrieval, or raw-secret handling.

## Intended A3 Commands

These commands are not approved for execution by this file. They are the planned
shape for a later exact A3 Docker gate after the base digest is verified.

```bash
docker build \
  --build-arg ELAINE_BASE_IMAGE=python:3.12-slim@sha256:<verified_digest> \
  -f Dockerfile \
  -t elaine-core-prooflab:local .

docker run --rm \
  --network none \
  --read-only \
  --tmpfs /opt/elaine-core/runtime-receipts:rw,noexec,nosuid,size=16m,mode=1777 \
  --cap-drop ALL \
  --security-opt no-new-privileges:true \
  elaine-core-prooflab:local \
  export-manifest --out runtime-receipts/docker-proof-lab-receipt.json
```

## Package Boundary / External Receipt Boundary

The Dockerfile intentionally fails closed unless the A3 gate provides a verified
base image digest. This package includes Docker source, runtime instructions,
and an A3 execution gate packet, but the package file itself does not authorize,
pull, build, or run Docker.

This package file does not itself authorize or prove execution unless paired
with the external A3 receipt set from the local Tuesday readiness lane:

- `outputs/elaine-tuesday-readiness-2026-06-20/docker-proof-runtime/docker-build-receipt.json`
- `outputs/elaine-tuesday-readiness-2026-06-20/docker-proof-runtime/docker-run-receipt.json`
- `outputs/elaine-tuesday-readiness-2026-06-20/docker-proof-runtime/docker-proof-lab-receipt.json`
- `outputs/elaine-tuesday-readiness-2026-06-20/docker-proof-runtime/docker-proof-runtime-execution-check-current.json`

## Receipt Promotion Rule

Docker proof may not be promoted from "source prepared" to "executed" until the
post-run receipt validator passes:

```powershell
python outputs\elaine-tuesday-readiness-2026-06-20\Run-ElaineDockerProofRuntimeExecutionReceiptCheck.py `
  --root . `
  --receipt-dir outputs\elaine-tuesday-readiness-2026-06-20\docker-proof-runtime `
  --out outputs\elaine-tuesday-readiness-2026-06-20\docker-proof-runtime\docker-proof-runtime-execution-check-current.json
```

That validator is an A2 receipt check. It does not itself pull, build, or run
Docker; it only validates the external A3 receipt set after an approved Docker
execution gate has produced one.
