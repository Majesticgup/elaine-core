# Runtime Core v0

Status: LOCAL PACKAGE CLI / NOT A SERVICE / NOT AN API / NOT AN MCP SERVER.

Runtime Core v0 is a small standard-library CLI included in this clean review package. Its job is to make Elaine easier to inspect from one local command surface.

It can:

- report package status;
- report proof-lab and receipt status;
- show blocked public/runtime claims;
- show that LLM, API, MCP, private-corpus RAG, and autonomous workstation control are held out of this package.

It does not:

- start a service;
- expose a localhost API;
- expose an MCP server;
- call a model;
- use hosted retrieval;
- install dependencies;
- read private corpus data;
- modify Git;
- publish or share anything.

Run from the package root:

```bash
python RUNTIME_CORE/elaine_runtime_core.py status --json
python RUNTIME_CORE/elaine_runtime_core.py doctor --json
python RUNTIME_CORE/elaine_runtime_core.py proof-lab --json
python RUNTIME_CORE/elaine_runtime_core.py receipts --json
python RUNTIME_CORE/elaine_runtime_core.py llm-status --json
python RUNTIME_CORE/elaine_runtime_core.py mcp-status --json
python RUNTIME_CORE/elaine_runtime_core.py gates --json
```

The CLI is proof support only. It does not prove production readiness or security outcomes.
