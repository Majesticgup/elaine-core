# Headroom Tactics Adoption for Elaine

## Decision

Do not install Headroom as part of Elaine onboarding. Adopt the low-risk
architectural tactics first and evaluate any third-party proxy separately.

## Adopt Now

1. Measure tool calls, bytes or estimated tokens, retries, files read, and
   output size before changing behavior.
2. Keep normal verification deterministic. Security review is a separate lane.
3. Compress repetitive JSON and log output only when a reviewer or maintainer
   explicitly asks for compact context.
4. Pass through source code, short outputs, and exact symbolic data unchanged.
5. Preserve errors, warnings, failures, first and last records, and change
   boundaries.
6. Keep full originals in a local hash-addressed cache when compacting content.
7. Fail open to the original content if compaction fails.
8. Keep durable prompt prefixes stable and put volatile details at the tail.
9. Avoid ceremony, repeated tool output, and long narration in install results.
10. Use scripts or low-reasoning agent routes for mechanical success paths.
11. Pass compact handoff capsules between agents instead of replaying full
    transcripts.
12. Label savings as measured only when measured; otherwise call them estimates.

## Evaluate Later In An Isolated Lane

- local proxy interception;
- MCP retrieval tool injection;
- persistent cross-agent memory;
- learned per-user verbosity;
- provider-specific prompt-cache control;
- third-party compression models.

## Do Not Use For Normal Installation

- proxy or MCP server;
- model download;
- telemetry;
- automatic edits to `AGENTS.md` or other authority files;
- compression of source code or proof-critical exact records;
- full receipts printed into model context.
