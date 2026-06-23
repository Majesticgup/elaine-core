#!/usr/bin/env python3
"""Local-only, reversible context compaction for Elaine tool outputs.

This independent Elaine utility adopts low-risk context-engineering tactics
without importing, installing, or invoking Headroom.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA = "elaine.context-guard.v1"
CODE_SUFFIXES = {
    ".py",
    ".pyi",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".rs",
    ".go",
    ".java",
    ".c",
    ".cc",
    ".cpp",
    ".h",
    ".hpp",
    ".cs",
    ".sh",
    ".ps1",
    ".sql",
}
IMPORTANT_RE = re.compile(
    r"\b(error|exception|fatal|failed|failure|critical|warning|warn|timeout|abort|denied|rejected|traceback)\b",
    re.IGNORECASE,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def approx_tokens(text: str) -> int:
    return max(1, (len(text) + 3) // 4) if text else 0


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def detect_kind(path: Path, text: str) -> tuple[str, Any | None]:
    if path.suffix.lower() in CODE_SUFFIXES:
        return "code", None
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        value = None
    if isinstance(value, (list, dict)):
        return "json", value
    lines = text.splitlines()
    has_important = any(IMPORTANT_RE.search(line) for line in lines)
    has_repetition = bool(lines) and len(set(lines)) < len(lines) * 0.8
    if len(lines) >= 20 and (has_important or has_repetition):
        return "log", None
    return "text", None


def uniform_indices(total: int, count: int) -> list[int]:
    if count <= 0 or total <= 0:
        return []
    if count >= total:
        return list(range(total))
    if count == 1:
        return [total // 2]
    return sorted({round(i * (total - 1) / (count - 1)) for i in range(count)})


def compact_array(items: list[Any], max_items: int) -> tuple[dict[str, Any], dict[str, Any]]:
    unique: list[Any] = []
    seen: set[str] = set()
    for item in items:
        key = canonical(item)
        if key not in seen:
            seen.add(key)
            unique.append(item)

    important = [i for i, item in enumerate(unique) if IMPORTANT_RE.search(canonical(item))]
    keep = set(important)
    keep.update(range(min(2, len(unique))))
    keep.update(range(max(0, len(unique) - 2), len(unique)))
    remaining = max(0, max_items - len(keep))
    candidates = [i for i in range(len(unique)) if i not in keep]
    for pos in uniform_indices(len(candidates), remaining):
        if pos < len(candidates):
            keep.add(candidates[pos])

    constants: dict[str, Any] = {}
    if unique and all(isinstance(item, dict) for item in unique):
        common = set.intersection(*(set(item.keys()) for item in unique))
        for key in sorted(common):
            values = [canonical(item[key]) for item in unique]
            if len(set(values)) == 1:
                constants[key] = unique[0][key]

    retained = [unique[i] for i in sorted(keep)]
    meta = {
        "schema_version": SCHEMA,
        "strategy": "json-dedup-sample-preserve-important",
        "original_items": len(items),
        "unique_items": len(unique),
        "retained_items": len(retained),
        "dropped_items": max(0, len(items) - len(retained)),
        "important_items_preserved": len(important),
        "constant_fields": constants,
    }
    return {"_elaine_compacted_array": meta, "items": retained}, meta


def compact_json_value(value: Any, max_items: int, depth: int = 0) -> tuple[Any, dict[str, int]]:
    if depth > 5:
        return value, {"arrays_compacted": 0, "items_dropped": 0}
    if isinstance(value, list):
        if len(value) > max_items:
            compacted, meta = compact_array(value, max_items)
            return compacted, {"arrays_compacted": 1, "items_dropped": meta["dropped_items"]}
        out = []
        totals = {"arrays_compacted": 0, "items_dropped": 0}
        for item in value:
            child, stats = compact_json_value(item, max_items, depth + 1)
            out.append(child)
            totals["arrays_compacted"] += stats["arrays_compacted"]
            totals["items_dropped"] += stats["items_dropped"]
        return out, totals
    if isinstance(value, dict):
        out = {}
        totals = {"arrays_compacted": 0, "items_dropped": 0}
        for key, item in value.items():
            child, stats = compact_json_value(item, max_items, depth + 1)
            out[key] = child
            totals["arrays_compacted"] += stats["arrays_compacted"]
            totals["items_dropped"] += stats["items_dropped"]
        return out, totals
    return value, {"arrays_compacted": 0, "items_dropped": 0}


def compress_json_document(value: Any, max_items: int) -> tuple[str, dict[str, Any]]:
    compacted, stats = compact_json_value(value, max_items)
    payload = {
        "_elaine_context_guard": {
            "schema_version": SCHEMA,
            "strategy": "json-recursive-array-compaction",
            **stats,
        },
        "document": compacted,
    }
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")), payload["_elaine_context_guard"]


def compress_log(text: str, max_lines: int) -> tuple[str, dict[str, Any]]:
    lines = text.splitlines()
    counts = Counter(lines)
    keep: set[int] = set(range(min(8, len(lines))))
    keep.update(range(max(0, len(lines) - 8), len(lines)))
    keep.update(i for i, line in enumerate(lines) if IMPORTANT_RE.search(line))
    remaining = max(0, max_lines - len(keep))
    candidates = [i for i in range(len(lines)) if i not in keep]
    for pos in uniform_indices(len(candidates), remaining):
        if pos < len(candidates):
            keep.add(candidates[pos])

    out = [f"[ELAINE_CONTEXT_GUARD lines={len(lines)} retained={len(keep)}]"]
    emitted: set[str] = set()
    for i in sorted(keep):
        line = lines[i]
        if line in emitted and counts[line] > 1:
            continue
        emitted.add(line)
        suffix = f" [repeated {counts[line]}x]" if counts[line] > 1 else ""
        out.append(line + suffix)
    meta = {
        "schema_version": SCHEMA,
        "strategy": "log-dedup-sample-preserve-important",
        "original_lines": len(lines),
        "retained_lines": len(keep),
        "important_lines": sum(bool(IMPORTANT_RE.search(line)) for line in lines),
    }
    return "\n".join(out) + "\n", meta


def compress_text_lossless(text: str) -> tuple[str, dict[str, Any]]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    counts = Counter(paragraphs)
    seen: set[str] = set()
    out: list[str] = []
    for paragraph in paragraphs:
        if paragraph in seen:
            continue
        seen.add(paragraph)
        suffix = f"\n[repeated paragraph {counts[paragraph]}x]" if counts[paragraph] > 1 else ""
        out.append(paragraph + suffix)
    return "\n\n".join(out) + ("\n" if out else ""), {
        "schema_version": SCHEMA,
        "strategy": "lossless-paragraph-dedup",
        "original_paragraphs": len(paragraphs),
        "unique_paragraphs": len(out),
    }


def process(path: Path, mode: str, cache_dir: Path, max_items: int, max_lines: int, min_chars: int) -> tuple[str, dict[str, Any]]:
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    digest = sha256_bytes(raw)
    kind, parsed = detect_kind(path, text)
    receipt: dict[str, Any] = {
        "schema_version": SCHEMA,
        "generated_utc": utc_now(),
        "mode": mode,
        "input_path": str(path),
        "input_sha256": digest,
        "content_type": kind,
        "bytes_before": len(raw),
        "estimated_tokens_before": approx_tokens(text),
        "network_used": False,
        "model_call_used": False,
        "package_install_used": False,
        "status": "pass",
    }

    if kind == "code" or len(text) < min_chars:
        output = text
        strategy = "passthrough-code" if kind == "code" else "passthrough-short"
        details: dict[str, Any] = {"strategy": strategy}
    else:
        try:
            if kind == "json" and isinstance(parsed, (list, dict)):
                output, details = compress_json_document(parsed, max_items=max_items)
            elif kind == "log":
                output, details = compress_log(text, max_lines=max_lines)
            else:
                output, details = compress_text_lossless(text)
            if len(output.encode("utf-8")) >= len(raw):
                output = text
                details = {"strategy": "passthrough-no-savings"}
        except Exception as exc:  # fail open by design
            output = text
            details = {"strategy": "fail-open-original", "error_type": type(exc).__name__}
            receipt["status"] = "fail_open"

    out_bytes = output.encode("utf-8")
    receipt.update(details)
    receipt["bytes_after"] = len(out_bytes)
    receipt["estimated_tokens_after"] = approx_tokens(output)
    receipt["estimated_tokens_saved"] = max(0, receipt["estimated_tokens_before"] - receipt["estimated_tokens_after"])
    receipt["savings_percent"] = round(100 * (1 - len(out_bytes) / len(raw)), 1) if raw else 0.0

    if output != text:
        cache_dir.mkdir(parents=True, exist_ok=True)
        original_path = cache_dir / f"{digest}.original"
        original_path.write_bytes(raw)
        receipt["retrieval_ref"] = str(original_path)
    else:
        receipt["retrieval_ref"] = None

    return output, receipt


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit or compact local tool output without a model call.")
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("audit", "compress"):
        command_parser = sub.add_parser(name)
        command_parser.add_argument("input")
        command_parser.add_argument("--output")
        command_parser.add_argument("--receipt")
        command_parser.add_argument("--cache-dir", default=".elaine-context-cache")
        command_parser.add_argument("--max-items", type=int, default=15)
        command_parser.add_argument("--max-lines", type=int, default=40)
        command_parser.add_argument("--min-chars", type=int, default=1200)

    retrieve = sub.add_parser("retrieve")
    retrieve.add_argument("hash")
    retrieve.add_argument("--cache-dir", default=".elaine-context-cache")
    retrieve.add_argument("--output")

    args = parser.parse_args()
    if args.command == "retrieve":
        src = Path(args.cache_dir) / f"{args.hash}.original"
        if not src.is_file():
            print("retrieval_not_found", file=sys.stderr)
            return 2
        data = src.read_bytes()
        if args.output:
            Path(args.output).write_bytes(data)
        else:
            sys.stdout.buffer.write(data)
        return 0

    path = Path(args.input).resolve()
    output, receipt = process(
        path,
        args.command,
        Path(args.cache_dir).resolve(),
        args.max_items,
        args.max_lines,
        args.min_chars,
    )
    if args.command == "compress":
        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
        else:
            sys.stdout.write(output)
    else:
        print(json.dumps(receipt, separators=(",", ":"), sort_keys=True))
    if args.receipt:
        Path(args.receipt).write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
