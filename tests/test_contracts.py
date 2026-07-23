from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SkillContractTests(unittest.TestCase):
    def test_frontmatter_dependencies(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn('version: "4.5.0"', skill)
        self.assertIn("name: trans-doc-to-md", skill)
        self.assertIn('version: ">=3.0.0,<4.0.0"', skill)
        self.assertIn("name: upload-markdown-to-lexiang", skill)
        self.assertIn('version: ">=1.1.0,<2.0.0"', skill)

    def test_no_private_translation_script_or_openai_translation(self):
        self.assertFalse((SCRIPTS / "translate_gemini.py").exists())
        youtube = (SCRIPTS / "yt_download_transcribe.py").read_text(encoding="utf-8")
        self.assertNotIn("def translate_paragraphs", youtube)
        self.assertNotIn("from openai import", youtube)
        self.assertNotIn("OPENAI_API_KEY", youtube)
        self.assertNotIn("🇨🇳", youtube)

    def test_podcast_has_no_markdown_upload_stage(self):
        podcast = (SCRIPTS / "podcast_to_lexiang.py").read_text(encoding="utf-8")
        self.assertNotIn("def _find_markdown_uploader", podcast)
        self.assertNotIn("def upload_to_lexiang", podcast)
        self.assertNotIn("--space-id", podcast)
        self.assertNotIn("--parent-entry-id", podcast)
        self.assertNotIn("--no-upload", podcast)

    def test_youtube_markdown_is_source_only(self):
        module = load_module("youtube_contract", SCRIPTS / "yt_download_transcribe.py")
        content = module.generate_markdown(
            {
                "title": "Original Title",
                "channel": "Channel",
                "webpage_url": "https://example.com/video",
                "description": "Show notes",
            },
            [{"start": 0, "text": "Original transcript."}],
            "en",
        )
        self.assertIn("## 视频介绍", content)
        self.assertIn("## 逐字稿", content)
        self.assertIn("Original transcript.", content)
        self.assertNotIn("\n---\n", content)

    def test_youtube_maps_diarization_and_merges_continuous_speaker(self):
        module = load_module("youtube_speaker_contract", SCRIPTS / "yt_download_transcribe.py")
        whisper_segments = [
            {"start": 0, "end": 20, "text": "Welcome to the show."},
            {"start": 28, "end": 45, "text": "Today we discuss evals."},
            {"start": 50, "end": 90, "text": "At our company we review traces."},
            {"start": 98, "end": 130, "text": "We then build narrow judges."},
        ]
        diarized = [
            {"start": 0, "end": 45, "spk": 0, "text": "host"},
            {"start": 50, "end": 130, "spk": 1, "text": "guest"},
        ]
        assigned = module.assign_speakers_to_whisper_segments(
            whisper_segments, diarized
        )
        module.assign_host_guest_roles(assigned)
        merged = module.merge_by_speaker(assigned)
        self.assertEqual(len(merged), 2)
        self.assertEqual([item["role"] for item in merged], ["host", "guest"])
        self.assertIn("Today we discuss evals", merged[0]["text"])
        self.assertIn("narrow judges", merged[1]["text"])

    def test_youtube_does_not_merge_different_guest_speakers(self):
        module = load_module("youtube_multi_guest_contract", SCRIPTS / "yt_download_transcribe.py")
        merged = module.merge_by_speaker([
            {"start": 0, "end": 20, "text": "First answer.", "spk": 1, "role": "guest"},
            {"start": 22, "end": 40, "text": "Second guest.", "spk": 2, "role": "guest"},
        ])
        self.assertEqual(len(merged), 2)

    def test_youtube_anonymous_roles_still_have_labels(self):
        module = load_module("youtube_labels_contract", SCRIPTS / "yt_download_transcribe.py")
        content = module.generate_markdown(
            {
                "title": "Original Title",
                "channel": "Channel",
                "webpage_url": "https://example.com/video",
                "description": "",
            },
            [
                {"start": 0, "text": "Welcome.", "role": "host"},
                {"start": 20, "text": "Thank you.", "role": "guest"},
            ],
            "en",
        )
        self.assertIn("**[00:00] 主持人：**", content)
        self.assertIn("**[00:20] 嘉宾：**", content)

    def test_podcast_markdown_is_source_only(self):
        module = load_module("podcast_contract", SCRIPTS / "podcast_to_lexiang.py")
        content = module.generate_markdown(
            [{"start": 0, "text": "原始逐字稿。"}],
            "原文标题",
            {"url": "https://example.com/podcast", "shownotes": "节目介绍"},
            language="zh",
        )
        self.assertLess(content.index("## 节目介绍"), content.index("## 逐字稿"))

    def test_podcast_merges_continuous_speaker_across_short_pauses(self):
        module = load_module("podcast_merge_contract", SCRIPTS / "podcast_to_lexiang.py")
        segments = [
            {"start": 0, "end": 20, "text": "欢迎收听。", "role": "host", "_intro_end": 45},
            {"start": 30, "end": 45, "text": "今天我们聊评估系统。", "role": "host"},
            {"start": 50, "end": 100, "text": "我们公司是这样做的。", "role": "guest"},
            {"start": 108, "end": 150, "text": "这里还有第二点。", "role": "guest"},
        ]
        merged = module.merge_by_speaker(segments)
        self.assertEqual(len(merged), 2)
        self.assertEqual([item["role"] for item in merged], ["host", "guest"])
        self.assertIn("今天我们聊评估系统", merged[0]["text"])
        self.assertIn("这里还有第二点", merged[1]["text"])

    def test_podcast_does_not_merge_different_guest_speakers(self):
        module = load_module("podcast_multi_guest_contract", SCRIPTS / "podcast_to_lexiang.py")
        segments = [
            {"start": 0, "end": 20, "text": "第一位嘉宾。", "role": "guest", "spk": 1},
            {"start": 22, "end": 40, "text": "第二位嘉宾。", "role": "guest", "spk": 2},
        ]
        self.assertEqual(len(module.merge_by_speaker(segments)), 2)

    def test_podcast_intro_does_not_force_early_guest_to_host(self):
        module = load_module("podcast_roles_contract", SCRIPTS / "podcast_to_lexiang.py")
        segments = [
            {"start": 0, "end": 25, "text": "欢迎收听，今天我们请到一位嘉宾。", "spk": 0},
            {"start": 30, "end": 40, "text": "谢谢邀请。", "spk": 1},
            {"start": 45, "end": 100, "text": "我们公司内部是这样推进评估的。", "spk": 1},
            {"start": 105, "end": 115, "text": "你们为什么这样设计？", "spk": 0},
        ]
        module.remap_speaker_roles(segments, intro_end=120)
        self.assertEqual(segments[0]["role"], "host")
        self.assertEqual(segments[1]["role"], "guest")
        self.assertEqual(segments[2]["role"], "guest")
        self.assertEqual(segments[3]["role"], "host")

    def test_podcast_anonymous_roles_still_have_labels(self):
        module = load_module("podcast_labels_contract", SCRIPTS / "podcast_to_lexiang.py")
        content = module.generate_markdown(
            [
                {"start": 0, "text": "欢迎收听。", "role": "host"},
                {"start": 20, "text": "谢谢邀请。", "role": "guest"},
            ],
            "原文标题",
            {"url": "https://example.com/podcast"},
            language="zh",
        )
        self.assertIn("**[00:00] 主持人：**", content)
        self.assertIn("**[00:20] 嘉宾：**", content)

    def test_article_standard_paths_and_metadata(self):
        article = (SCRIPTS / "fetch_article.py").read_text(encoding="utf-8")
        self.assertIn('output_path / "source.md"', article)
        self.assertIn('output_path / "meta.json"', article)
        for field in ("source_url", "source_title", "source_type", "language"):
            self.assertIn(f'"{field}"', article)

    def test_wechat_uses_native_lexiang_import_without_fetch_fallback(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        platform = (ROOT / "references" / "platform-specific.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("file_create_hyperlink", skill)
        self.assertIn("禁止浏览器/WebFetch/脚本抓取", skill)
        self.assertIn("不得静默回退抓取", skill)
        self.assertIn("禁止静默回退到 `fetch_article.py`", platform)
        self.assertIn("不生成 `source.md`、`images/`、`meta.json`", platform)

    def test_article_defaults_to_cdp_and_recognizes_custom_substack_domain(self):
        module = load_module("article_contract", SCRIPTS / "fetch_article.py")
        self.assertTrue(module._is_substack_site("https://www.a16z.news/p/example"))
        self.assertTrue(module._is_substack_site("https://example.substack.com/p/post"))
        self.assertIn("use_cdp: bool = True", (SCRIPTS / "fetch_article.py").read_text())

    def test_substack_noise_is_filtered_before_markdown_output(self):
        article = (SCRIPTS / "fetch_article.py").read_text(encoding="utf-8")
        for marker in (
            "discover more from ",
            "subscribe for more from ",
            "this newsletter is provided for informational purposes only",
        ):
            self.assertIn(marker, article)

    def test_substack_postprocessor_cuts_recommendations_and_byline(self):
        module = load_module("article_noise_contract", SCRIPTS / "fetch_article.py")
        markdown = (
            "[George](https://substack.com/@george)Jul 15, 2026\n\n"
            "Article body.\n\n"
            "![](images/subscribe.png)\n\n"
            "[Institutional AI vs Individual AI](https://example.com/related)\n"
        )
        cleaned = module._strip_substack_archive_noise(markdown, "George")
        self.assertEqual(cleaned, "Article body.")

    def test_scenarios_are_valid_json(self):
        with (ROOT / "tests" / "test-cases.json").open(encoding="utf-8") as handle:
            cases = json.load(handle)
        self.assertGreaterEqual(len(cases), 3)


if __name__ == "__main__":
    unittest.main()
