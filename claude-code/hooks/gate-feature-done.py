#!/usr/bin/env python3
"""Block feature -> done transitions without feature-specific scan evidence.

This PreToolUse hook compares the current feature index with the content proposed
by Claude's Edit/Write call. Every feature newly marked ``done`` must have a
matching evidence line in an assistant text message in the recent transcript:

    Code smell scan: pass (feature: F001, must_fix: 0, suggest: 2, acceptable: 1)

Restricting evidence to assistant text prevents the literal examples contained
in skill instructions or user prompts from satisfying the gate automatically.
"""
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Set


EVIDENCE_PATTERN = re.compile(
    r"^Code smell scan:\s*pass\s*\(\s*"
    r"feature:\s*(F\d+)\s*,\s*"
    r"must_fix:\s*0\s*,\s*"
    r"suggest:\s*\d+\s*,\s*"
    r"acceptable:\s*\d+\s*\)\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    if payload.get("tool_name") not in ("Edit", "Write"):
        sys.exit(0)

    tool_input = payload.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    if not file_path.endswith("docs/feature-list.json"):
        sys.exit(0)

    newly_done = _newly_done_ids(Path(file_path), payload["tool_name"], tool_input)
    if not newly_done:
        sys.exit(0)

    transcript_path = payload.get("transcript_path", "")
    evidence = _assistant_evidence_features(transcript_path)
    missing = newly_done - evidence
    if not missing:
        sys.exit(0)

    missing_list = ", ".join(sorted(missing))
    print(
        f"BLOCKED: The following Features would be marked done: {missing_list}. "
        "This session has no matching code-smell scan evidence.\n"
        "Complete execute-next-feature Stage 6 and have the main agent output this line:\n"
        "Code smell scan: pass (feature: F0XX, must_fix: 0, suggest: N, acceptable: M)",
        file=sys.stderr,
    )
    sys.exit(2)


def _status_map(content: str) -> Dict[str, str]:
    try:
        data = json.loads(content)
    except (json.JSONDecodeError, TypeError):
        return {}
    if not isinstance(data, dict):
        return {}
    return {
        entry["id"]: entry.get("status")
        for entry in data.get("features", [])
        if isinstance(entry, dict) and entry.get("id")
    }


def _proposed_content(current: str, tool_name: str, tool_input: dict) -> str:
    if tool_name == "Write":
        return tool_input.get("content", "")

    old = tool_input.get("old_string", "")
    new = tool_input.get("new_string", "")
    if not old or old not in current:
        return current
    count = -1 if tool_input.get("replace_all") else 1
    return current.replace(old, new, count)


def _newly_done_ids(file_path: Path, tool_name: str, tool_input: dict) -> Set[str]:
    try:
        current = file_path.read_text(encoding="utf-8")
    except OSError:
        current = '{"features": []}'

    before = _status_map(current)
    after = _status_map(_proposed_content(current, tool_name, tool_input))
    return {
        feature_id
        for feature_id, status in after.items()
        if status == "done" and before.get(feature_id) != "done"
    }


def _assistant_texts(event: dict) -> Iterable[str]:
    if event.get("type") != "assistant":
        return []

    message = event.get("message", event)
    if not isinstance(message, dict) or message.get("role") != "assistant":
        return []

    content = message.get("content", [])
    if isinstance(content, str):
        return [content]
    if not isinstance(content, list):
        return []
    return [
        block.get("text", "")
        for block in content
        if isinstance(block, dict) and block.get("type") == "text"
    ]


def _assistant_evidence_features(transcript_path: str) -> Set[str]:
    if not transcript_path or not os.path.exists(transcript_path):
        return set()
    try:
        with open(transcript_path, encoding="utf-8") as transcript:
            lines: List[str] = transcript.readlines()[-200:]
    except OSError:
        return set()

    feature_ids: Set[str] = set()
    for line in lines:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        for text in _assistant_texts(event):
            feature_ids.update(EVIDENCE_PATTERN.findall(text))
    return feature_ids


if __name__ == "__main__":
    main()
