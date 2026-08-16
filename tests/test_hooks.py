import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from importlib.machinery import SourceFileLoader
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative_path):
    path = REPO_ROOT / relative_path
    loader = SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


gate = load_module("gate_feature_done", "claude-code/hooks/gate-feature-done.py")
commit_hook = load_module("commit_msg_hook", "git-hooks/commit-msg")


def feature_index(status_f001="pending", status_f002="pending"):
    return json.dumps(
        {
            "features": [
                {"id": "F001", "status": status_f001},
                {"id": "F002", "status": status_f002},
            ]
        }
    )


def transcript_event(event_type, role, text):
    return json.dumps(
        {
            "type": event_type,
            "message": {"role": role, "content": [{"type": "text", "text": text}]},
        }
    )


class GateFeatureDoneTests(unittest.TestCase):
    def test_edit_detects_only_newly_done_feature(self):
        with tempfile.TemporaryDirectory() as tmp:
            index = Path(tmp) / "docs" / "feature-list.json"
            index.parent.mkdir()
            index.write_text(feature_index(), encoding="utf-8")
            changed = gate._newly_done_ids(
                index,
                "Edit",
                {"old_string": '"status": "pending"', "new_string": '"status": "done"'},
            )
        self.assertEqual(changed, {"F001"})

    def test_write_compares_existing_and_proposed_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            index = Path(tmp) / "docs" / "feature-list.json"
            index.parent.mkdir()
            index.write_text(feature_index(status_f001="done"), encoding="utf-8")
            changed = gate._newly_done_ids(
                index,
                "Write",
                {"content": feature_index(status_f001="done", status_f002="done")},
            )
        self.assertEqual(changed, {"F002"})

    def test_instruction_or_user_text_is_not_evidence(self):
        evidence = "Code smell scan: pass (feature: F001, must_fix: 0, suggest: 0, acceptable: 0)"
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8") as transcript:
            transcript.write(transcript_event("user", "user", evidence) + "\n")
            transcript.flush()
            found = gate._assistant_evidence_features(transcript.name)
        self.assertEqual(found, set())

    def test_assistant_evidence_is_feature_specific(self):
        evidence = "Code smell scan: pass (feature: F002, must_fix: 0, suggest: 1, acceptable: 2)"
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8") as transcript:
            transcript.write(transcript_event("assistant", "assistant", evidence) + "\n")
            transcript.flush()
            found = gate._assistant_evidence_features(transcript.name)
        self.assertEqual(found, {"F002"})

    def test_main_blocks_when_matching_evidence_is_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            index = Path(tmp) / "docs" / "feature-list.json"
            index.parent.mkdir()
            index.write_text(feature_index(), encoding="utf-8")
            transcript = Path(tmp) / "transcript.jsonl"
            transcript.write_text(
                transcript_event(
                    "assistant",
                    "assistant",
                    "Code smell scan: pass (feature: F002, must_fix: 0, suggest: 0, acceptable: 0)",
                ),
                encoding="utf-8",
            )
            payload = {
                "tool_name": "Edit",
                "tool_input": {
                    "file_path": str(index),
                    "old_string": '"status": "pending"',
                    "new_string": '"status": "done"',
                },
                "transcript_path": str(transcript),
            }
            with patch.object(sys, "stdin", io.StringIO(json.dumps(payload))):
                with redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as raised:
                        gate.main()
        self.assertEqual(raised.exception.code, 2)

    def test_main_allows_matching_assistant_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            index = Path(tmp) / "docs" / "feature-list.json"
            index.parent.mkdir()
            index.write_text(feature_index(), encoding="utf-8")
            transcript = Path(tmp) / "transcript.jsonl"
            transcript.write_text(
                transcript_event(
                    "assistant",
                    "assistant",
                    "Code smell scan: pass (feature: F001, must_fix: 0, suggest: 0, acceptable: 0)",
                ),
                encoding="utf-8",
            )
            payload = {
                "tool_name": "Edit",
                "tool_input": {
                    "file_path": str(index),
                    "old_string": '"status": "pending"',
                    "new_string": '"status": "done"',
                },
                "transcript_path": str(transcript),
            }
            with patch.object(sys, "stdin", io.StringIO(json.dumps(payload))):
                with self.assertRaises(SystemExit) as raised:
                    gate.main()
        self.assertEqual(raised.exception.code, 0)


class CommitMessageHookTests(unittest.TestCase):
    def test_evidence_requires_feature_id_and_zero_must_fix(self):
        message = """chore(F001): done

Code smell scan: pass (feature: F001, must_fix: 0, suggest: 2, acceptable: 1)
Code smell scan: pass (feature: F002, must_fix: 1, suggest: 0, acceptable: 0)
"""
        self.assertEqual(set(commit_hook.EVIDENCE_PATTERN.findall(message)), {"F001"})

    def test_find_newly_done_ignores_already_done_features(self):
        before = json.loads(feature_index(status_f001="done"))
        after = json.loads(feature_index(status_f001="done", status_f002="done"))
        self.assertEqual(commit_hook.find_newly_done(before, after), ["F002"])


if __name__ == "__main__":
    unittest.main()
