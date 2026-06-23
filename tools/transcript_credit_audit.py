#!/usr/bin/env python3
"""Audit exported agent transcripts for credit-waste patterns using stdlib only."""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET


PATTERNS = {
    "tool_or_script_markers": r"\b(Script|Ran command|Ran \d+ commands|Shell)\b",
    "full_file_reads": r"\b(Get-Content|cat\s+|Read .* in full|read through .* in full)\b",
    "recursive_searches": r"\b(rg -n|rg --files|find \.|Get-ChildItem -Recurse)\b",
    "archive_operations": r"\b(Expand-Archive|ZipFile|extracting the zip|Listing contents of the zip)\b",
    "sandbox_or_tool_failures": r"\b(execution error|Exit code -1|timed out|CreateProcessAsUserW failed)\b",
    "approval_loops": r"\b(Auto-review approved|approval|escalation)\b",
    "broad_audit_language": r"\b(audit|security review|inspect.*whole|read.*whole executable surface|source review)\b",
    "quota_failure": r"\b(usage limit|credit limit|quota)\b",
}


def read_docx(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        xml = archive.read("word/document.xml")
    root = ET.fromstring(xml)
    texts = [node.text or "" for node in root.iter() if node.tag.endswith("}t")]
    return "\n".join(texts)


def read_text(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        return read_docx(path)
    return path.read_text(encoding="utf-8", errors="replace")


def audit(path: Path) -> dict[str, object]:
    text = read_text(path)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    long_blocks = [line for line in lines if len(line) > 1500]
    duplicate_long = sum(
        count - 1 for line, count in Counter(lines).items() if len(line) > 120 and count > 1
    )
    counts = {
        name: len(re.findall(pattern, text, flags=re.IGNORECASE)) for name, pattern in PATTERNS.items()
    }
    return {
        "path": str(path),
        "characters": len(text),
        "words": len(text.split()),
        "estimated_tokens": max(1, (len(text) + 3) // 4),
        "nonempty_lines": len(lines),
        "long_blocks_over_1500_chars": len(long_blocks),
        "duplicate_long_lines": duplicate_long,
        "signals": counts,
        "risk_flags": [
            name
            for name, value in counts.items()
            if value
            and name
            in {
                "full_file_reads",
                "recursive_searches",
                "sandbox_or_tool_failures",
                "broad_audit_language",
                "quota_failure",
            }
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit transcript size and credit-waste patterns.")
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("--output")
    args = parser.parse_args()

    report = {
        "schema_version": "elaine.transcript-credit-audit.v1",
        "files": [audit(Path(path).resolve()) for path in args.inputs],
    }
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
