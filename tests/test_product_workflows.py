import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HAN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")


class ProductWorkflowTests(unittest.TestCase):
    PAIRS = {
        "Product specification elicitor": (
            "claude-code/skills/product-spec-elicitor/SKILL.md",
            "ai-agnostic-prompts/product-spec-elicitor.prompt.md",
        ),
        "Product UI sketcher": (
            "claude-code/skills/product-ui-sketcher/SKILL.md",
            "ai-agnostic-prompts/product-ui-sketcher.prompt.md",
        ),
        "Product audio sketcher": (
            "claude-code/skills/product-audio-sketcher/SKILL.md",
            "ai-agnostic-prompts/product-audio-sketcher.prompt.md",
        ),
    }

    def read(self, relative_path):
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def split_wrapper_and_body(self, text, title):
        match = re.search(rf"(?m)^# {re.escape(title)}$", text)
        self.assertIsNotNone(match, f"missing canonical heading: {title}")
        return text[: match.start()], text[match.start() :]

    def canonical_bodies(self):
        bodies = {}
        for title, paths in self.PAIRS.items():
            native = self.read(paths[0])
            portable = self.read(paths[1])
            native_wrapper, native_body = self.split_wrapper_and_body(native, title)
            portable_wrapper, portable_body = self.split_wrapper_and_body(portable, title)
            with self.subTest(title=title):
                self.assertEqual(native_body, portable_body)
                self.assertIsNone(HAN_RE.search(native_body))
                self.assertIsNotNone(HAN_RE.search(native_wrapper))
                self.assertIsNotNone(HAN_RE.search(portable_wrapper))
            bodies[title] = native_body
        return bodies

    def test_f017_pairs_are_exact_english_bodies_with_bilingual_discovery(self):
        bodies = self.canonical_bodies()
        for title, body in bodies.items():
            with self.subTest(title=title):
                self.assertIn("docs/methodology-config.json", body)
                self.assertIn("document_language", body)
                self.assertIn("missing, invalid, or migration-sensitive", body)
                self.assertIn("methodology/05-document-language.md", body)
                self.assertIn("current", body.lower())
                self.assertIn("document_language: en", body)
                self.assertIn("document_language: zh-CN", body)

    def test_specification_elicitor_preserves_modes_risks_and_patch_contract(self):
        body = self.canonical_bodies()["Product specification elicitor"]
        for value in ("new_module", "modify", "bug_fix", "cross_module"):
            with self.subTest(mode=value):
                self.assertIn(value, body)
        for invariant in (
            "Existing behavior is deleted",
            "second confirmation",
            "AI-default",
            "completed Feature",
            "trigger_ui_sketcher",
            "trigger_audio_sketcher",
            "questions_unresolved",
            "side_effects",
            "needs_review",
            "source_explanation",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, body)
        for stable_key in (
            "mode:",
            "patches:",
            "module_id:",
            "module_name:",
            "section:",
            "operation:",
            "content:",
            "source:",
        ):
            with self.subTest(stable_key=stable_key):
                self.assertIn(stable_key, body)

    def test_ui_sketcher_preserves_ascii_html_and_return_contracts(self):
        body = self.canonical_bodies()["Product UI sketcher"]
        for convention in (
            "┌─┐ │ │ └─┘",
            "┏━┓ ┃ ┃ ┗━┛",
            "[label]",
            "[[label]]",
            "< placeholder >",
            "[option ▾]",
            "Only one `[[primary CTA]]`",
        ):
            with self.subTest(convention=convention):
                self.assertIn(convention, body)
        for invariant in (
            "want_html_mockup: true",
            "docs/ui-mockups/{module-name}.html",
            "Put all primary states in one file",
            'lang="<document_language>"',
            'charset="UTF-8"',
            "<!DOCTYPE html>",
            "<head>",
            "<body>",
            "localized `<title>`",
            '<script src="https://cdn.tailwindcss.com"></script>',
            "ascii_wireframe:",
            "html_mockup:",
            "generated:",
            "notes_for_standardizer:",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, body)

    def test_audio_sketcher_preserves_elicitation_placeholders_and_schema(self):
        body = self.canonical_bodies()["Product audio sketcher"]
        self.assertIn("does **not** generate audio files", body)
        self.assertIn("two to four key questions", body)
        self.assertIn("one question at a time", body)
        for question in (
            "Q1: intent — required",
            "Q2: duration — required",
            "Q3: style — conditional",
            "Q4: reference — optional",
            "Q5: boundary behavior — conditional",
            "Countdown",
            "Completion",
            "Interruption",
        ):
            with self.subTest(question=question):
                self.assertIn(question, body)
        for band in ("<0.3s", "0.3–1s", "1–3s", ">3s"):
            with self.subTest(duration_band=band):
                self.assertIn(band, body)
        for filename in (
            "_placeholder_sfx_timer_start.wav",
            "_placeholder_sfx_timer_pause.wav",
            "_placeholder_sfx_timer_resume.wav",
            "_placeholder_sfx_countdown_tick.wav",
            "_placeholder_sfx_pomodoro_complete.wav",
            "_placeholder_sfx_session_interrupted.wav",
            "_placeholder_sfx_button_click.wav",
            "_placeholder_sfx_error.wav",
            "_placeholder_bgm_<name>.ogg",
        ):
            with self.subTest(filename=filename):
                self.assertIn(filename, body)
        for stable_key in (
            "audio_entries:",
            "id:",
            "markdown:",
            "placeholder_file:",
            "type:",
            "notes_for_standardizer:",
            "feature_notes_register:",
            "feature_module:",
            "placeholder_files:",
        ):
            with self.subTest(stable_key=stable_key):
                self.assertIn(stable_key, body)
        for bgm_dimension in (
            "use scenario",
            "intent",
            "style",
            "rhythm",
            "duration and loop behavior",
            "volume baseline",
            "optional reference",
        ):
            with self.subTest(bgm_dimension=bgm_dimension):
                self.assertIn(bgm_dimension, body)


if __name__ == "__main__":
    unittest.main()
