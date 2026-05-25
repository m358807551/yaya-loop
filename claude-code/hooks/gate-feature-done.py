#!/usr/bin/env python3
"""Pre-tool-use hook: gate feature -> done transitions on code smell scan evidence.

Triggered on Edit/Write of docs/feature-list.json. If the operation would change a
feature's status from in_progress to done, scan the recent transcript for the line
"Code smell scan: pass". If absent, block with exit code 2 so Claude must run stage 6
of execute-next-feature first.

This is the last-line backstop for the three soft gates (stage 0 出关报告, stage 6
sub-agent smell scan, CLAUDE.md hardline note). Should fire rarely in practice.
"""
import json
import os
import re
import sys
from typing import Tuple


PASS_PATTERN = re.compile(r"Code smell scan:\s*pass", re.IGNORECASE)


def main():
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

    feature_id, marking_done = _detect_status_change(payload.get("tool_name"), tool_input)
    if not marking_done:
        sys.exit(0)

    transcript_path = payload.get("transcript_path", "")
    if not transcript_path or not os.path.exists(transcript_path):
        ## 找不到 transcript 时放行，避免误伤；这只是兜底，不是唯一防线。
        print("[gate-feature-done] WARNING: transcript not available, cannot verify.", file=sys.stderr)
        sys.exit(0)

    if _transcript_has_pass(transcript_path):
        sys.exit(0)

    print(
        f"⛔ 阻断：尝试把 feature {feature_id} 标记为 done，"
        f"但本会话 transcript 中找不到「Code smell scan: pass」证据。\n"
        f"请先执行 execute-next-feature 阶段 6 代码气味扫描（Task 子 agent 委派），"
        f"主 agent 输出包含 `Code smell scan: pass (must_fix: 0, suggest: N, acceptable: M)` "
        f"那一行后，再次尝试标记 done。",
        file=sys.stderr,
    )
    sys.exit(2)


def _detect_status_change(tool_name, tool_input):
    # type: (str, dict) -> Tuple[str, bool]
    """Return (feature_id, is_marking_done)."""
    if tool_name == "Edit":
        old = tool_input.get("old_string", "")
        new = tool_input.get("new_string", "")
        if '"status": "in_progress"' in old and '"status": "done"' in new:
            m = re.search(r'"id":\s*"(F\d+)"', old + new)
            return (m.group(1) if m else "?", True)
        return ("?", False)

    if tool_name == "Write":
        ## 整篇覆盖时缺少 old 上下文，但若 content 同时含 done 状态和 completed_at 时间戳，倾向认为是新近标记 done。
        content = tool_input.get("content", "")
        if '"status": "done"' in content and '"completed_at": "20' in content:
            return ("?", True)
        return ("?", False)

    return ("?", False)


def _transcript_has_pass(transcript_path):
    # type: (str) -> bool
    """Scan last ~200 lines of transcript JSONL for the pass marker."""
    try:
        with open(transcript_path, encoding="utf-8") as f:
            lines = f.readlines()
    except OSError:
        return False
    for line in lines[-200:]:
        if PASS_PATTERN.search(line):
            return True
    return False


if __name__ == "__main__":
    main()
