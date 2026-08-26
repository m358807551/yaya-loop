#!/usr/bin/env python3
"""Post-tool-use hook: validate the split feature-list files after any Edit/Write.

Validates:
  - docs/feature-list.json            (index, JSON syntax)
  - docs/feature-list-revisions.json  (revision log, JSON syntax)
  - docs/features/F*.json             (per-feature details, JSON syntax)
  - cross-check: index feature ids match the set of detail files (warning only)

Cross-check mismatches are warnings, not errors — they emit to stderr but do not
block. This is so a single Edit that touches the index can complete even before
the matching detail file is written (the next Edit will rebalance things).

JSON syntax errors are reported back to Claude with the blocking hook exit code 2.
"""
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
INDEX_FILE = REPO_ROOT / "docs" / "feature-list.json"
REVISIONS_FILE = REPO_ROOT / "docs" / "feature-list-revisions.json"
DETAILS_DIR = REPO_ROOT / "docs" / "features"


def _validate_json(path: Path) -> bool:
    if not path.exists():
        return True
    try:
        with path.open(encoding="utf-8") as f:
            json.load(f)
    except json.JSONDecodeError as e:
        print(f"[HOOK] {path.relative_to(REPO_ROOT)} is invalid JSON: {e}", file=sys.stderr)
        print(
            "[HOOK] Common cause: an unescaped ASCII double quote (\") inside a JSON "
            "string. Escape it as \\\" or use language-appropriate typographic quotation marks.",
            file=sys.stderr,
        )
        return False
    return True


def _check_id_consistency() -> None:
    if not INDEX_FILE.exists() or not DETAILS_DIR.exists():
        return
    try:
        with INDEX_FILE.open(encoding="utf-8") as f:
            index = json.load(f)
    except json.JSONDecodeError:
        return
    index_ids = {entry.get("id") for entry in index.get("features", []) if entry.get("id")}
    detail_ids = {p.stem for p in DETAILS_DIR.glob("F*.json")}

    only_in_index = index_ids - detail_ids
    only_in_details = detail_ids - index_ids
    if only_in_index:
        print(
            f"[HOOK] WARNING: index references ids without detail files: {sorted(only_in_index)}",
            file=sys.stderr,
        )
    if only_in_details:
        print(
            f"[HOOK] WARNING: detail files have no matching index entry: {sorted(only_in_details)}",
            file=sys.stderr,
        )


def main() -> int:
    ok = True
    if not _validate_json(INDEX_FILE):
        ok = False
    if not _validate_json(REVISIONS_FILE):
        ok = False
    if DETAILS_DIR.exists():
        for detail in sorted(DETAILS_DIR.glob("F*.json")):
            if not _validate_json(detail):
                ok = False
    if not ok:
        return 2
    _check_id_consistency()
    return 0


if __name__ == "__main__":
    sys.exit(main())
