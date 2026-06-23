# syntax=docker/dockerfile:1.7

# Fail closed by default. The A3 Docker execution gate must pass a verified
# Python base image digest explicitly:
#   --build-arg ELAINE_BASE_IMAGE=python:3.12-slim@sha256:<verified_digest>
ARG ELAINE_BASE_IMAGE=__ELAINE_REQUIRES_VERIFIED_PYTHON_BASE_DIGEST__
FROM ${ELAINE_BASE_IMAGE}

LABEL org.opencontainers.image.title="Elaine Core proof lab"
LABEL org.opencontainers.image.description="Local controlled-alpha proof lab for synthetic Elaine Core claim discipline checks."
LABEL org.opencontainers.image.licenses="Apache-2.0"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/elaine-core

RUN addgroup --system elaine \
    && adduser --system --ingroup elaine --home /home/elaine elaine

COPY --chown=elaine:elaine . /opt/elaine-core

RUN mkdir -p /opt/elaine-core/receipts /opt/elaine-core/runtime-receipts /tmp/elaine \
    && chown -R elaine:elaine /opt/elaine-core /tmp/elaine \
    && chmod -R go-w /opt/elaine-core /tmp/elaine

USER elaine

ENTRYPOINT ["python", "PROOF_LAB/elaine_research_proof_lab.py"]
CMD ["run-cases"]
