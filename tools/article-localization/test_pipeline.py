"""Focused invariant tests; no paid services, CLI calls, or production writes."""

from __future__ import annotations

import copy
import importlib.util
import tempfile
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "localization_pipeline", Path(__file__).with_name("pipeline.py")
)
pipeline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline)


def sample():
    return {
        "title": "旅行說明",
        "description": "適用台灣護照的旅行說明。",
        "hero": None,
        "blocks": [
            {
                "type": "paragraph",
                "text": "入境前 3 天使用 `command`，查閱 https://example.com/rules",
            },
            {
                "type": "rich_paragraph",
                "inlines": [
                    {"type": "text", "text": "執行 "},
                    {"type": "code", "text": "echo $HOME"},
                    {
                        "type": "article",
                        "text": "下一篇",
                        "kind": "life",
                        "slug": "next",
                    },
                ],
            },
            {
                "type": "code",
                "language": "bash",
                "label": "命令範例",
                "code": "echo '保留原文 123'",
            },
            {
                "type": "table",
                "header": ["事項"],
                "rows": [["費用 100"]],
                "caption": "比較",
            },
            {
                "type": "image",
                "src": "/guides/test/diagram.svg",
                "alt": "示意圖",
                "caption": "步驟",
                "description": "旅行 3 說明",
                "width": 300,
                "height": 200,
                "credit": {
                    "author": "Mokaair",
                    "license": "© Mokaair",
                    "source_url": "https://example.com",
                },
            },
        ],
        "sources": [
            {
                "title": "官方說明",
                "url": "https://example.com",
                "checked_on": "2026-09-14",
            }
        ],
    }


class PipelineTests(unittest.TestCase):
    def test_pipeline_text_writer_normalizes_line_endings(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "portable.txt"
            pipeline.write_text_lf(path, "first\r\nsecond\rthird\n")
            self.assertEqual(path.read_bytes(), b"first\nsecond\nthird\n")
            self.assertEqual(
                pipeline.canonical_svg_text("<svg>\r\n  <text>x</text>  \r\n</svg>"),
                "<svg>\n  <text>x</text>\n</svg>\n",
            )

    def test_child_overrides_cover_effective_config_layers_and_preflight(self):
        config = {"mcp_servers": {"node_repl": {}, "unityMCP": {}}}
        effective_servers = [
            {
                "name": "node_repl",
                "enabled": True,
                "transport": {
                    "type": "stdio",
                    "command": r"C:\Program Files\Codex\node.exe",
                    "args": ["server.js"],
                    "env": {"MCP_TOKEN": "never-forward-this"},
                },
            },
            {
                "name": "unityMCP",
                "enabled": True,
                "transport": {
                    "type": "streamable_http",
                    "url": "http://127.0.0.1:8080/mcp",
                    "http_headers": {"Authorization": "never-forward-this"},
                },
            },
            {
                "name": "managed_server",
                "enabled": True,
                "transport": {"type": "stdio", "command": "managed-mcp"},
            },
        ]
        args = pipeline.child_config_args(config, effective_servers)
        self.assertEqual(
            args,
            [
                "-c",
                'mcp_servers.managed_server.command="managed-mcp"',
                "-c",
                "mcp_servers.managed_server.enabled=false",
                "-c",
                'mcp_servers.node_repl.command="C:\\\\Program Files\\\\Codex\\\\node.exe"',
                "-c",
                "mcp_servers.node_repl.enabled=false",
                "-c",
                'mcp_servers.unityMCP.url="http://127.0.0.1:8080/mcp"',
                "-c",
                "mcp_servers.unityMCP.enabled=false",
            ],
        )
        self.assertNotIn("never-forward-this", " ".join(args))
        with patch.object(
            pipeline.subprocess,
            "run",
            return_value=SimpleNamespace(
                returncode=0,
                stdout='[{"name":"node_repl","enabled":false},'
                '{"name":"managed_server","enabled":false}]',
            ),
        ) as run:
            child_env = {"PATH": "bin", "CODEX_HOME": "home"}
            pipeline.preflight_child_config("codex", args, child_env)
            self.assertEqual(run.call_args.args[0][-3:], ["mcp", "list", "--json"])
            self.assertIs(run.call_args.kwargs["env"], child_env)
        with (
            patch.object(
                pipeline.subprocess,
                "run",
                return_value=SimpleNamespace(
                    returncode=0,
                    stdout='[{"name":"project_only","enabled":true}]',
                ),
            ),
            self.assertRaisesRegex(ValueError, "remain enabled"),
        ):
            pipeline.preflight_child_config("codex", [])
        with (
            patch.object(
                pipeline.subprocess, "run", return_value=SimpleNamespace(returncode=1)
            ),
            self.assertRaisesRegex(ValueError, "no translation started"),
        ):
            pipeline.preflight_child_config("codex", args)
        with (
            patch.object(
                pipeline.subprocess,
                "run",
                return_value=SimpleNamespace(returncode=0, stdout="{}"),
            ),
            self.assertRaisesRegex(ValueError, "inventory was invalid"),
        ):
            pipeline.mcp_servers("codex", [])
        with self.assertRaisesRegex(ValueError, "override review"):
            pipeline.child_config_args({"mcp_servers": {"ambiguous.name": {}}})

    def test_child_overrides_reject_invalid_effective_transports(self):
        invalid_servers = [
            ({"name": "unknown", "transport": {"type": "sse"}}, "review"),
            ({"name": "stdio", "transport": {"type": "stdio"}}, "missing command"),
            (
                {
                    "name": "http",
                    "transport": {"type": "streamable_http", "url": ""},
                },
                "missing url",
            ),
        ]
        for server, message in invalid_servers:
            with (
                self.subTest(server=server),
                self.assertRaisesRegex(ValueError, message),
            ):
                pipeline.child_config_args({}, [server])

    def test_chatgpt_provider_config_and_child_environment_fail_closed(self):
        for config, error, message in [
            ({"model_provider": "custom"}, ValueError, "custom/API-key"),
            (
                {"model_providers": {"openai": {}}},
                ValueError,
                "must not be redefined",
            ),
            (
                {
                    "model_providers": {
                        "custom": {"base_url": "https://example.invalid"}
                    }
                },
                ValueError,
                "custom model endpoints",
            ),
            (
                {"chatgpt_base_url": "https://example.invalid"},
                ValueError,
                "custom ChatGPT",
            ),
            ({"model_providers": []}, TypeError, "explicit review"),
            ({"model_providers": {"unused": []}}, TypeError, "explicit review"),
        ]:
            with self.subTest(config=config), self.assertRaisesRegex(error, message):
                pipeline.validate_chatgpt_config(config)
        pipeline.validate_chatgpt_config(
            {"model_providers": {"unused": {"name": "Unused provider"}}}
        )

        environment = {
            "PATH": "bin",
            "Path": "windows-bin",
            "CODEX_HOME": "profile",
            "NORMAL_SETTING": "kept",
            "OPENAI_API_KEY": "secret",
            "OPENAI_CUSTOM_HEADERS": "secret",
            "openai_base_url": "https://example.invalid",
            "CODEX_API_KEY": "secret",
            "CHATGPT_BASE_URL": "https://example.invalid",
            "AZURE_OPENAI_ENDPOINT": "https://example.invalid",
        }
        sanitized = pipeline.chatgpt_child_env(environment)
        self.assertEqual(
            sanitized,
            {
                "PATH": "bin",
                "Path": "windows-bin",
                "CODEX_HOME": "profile",
                "NORMAL_SETTING": "kept",
            },
        )
        with patch.object(
            pipeline.subprocess,
            "run",
            return_value=SimpleNamespace(
                returncode=0, stdout="Logged in using ChatGPT", stderr=""
            ),
        ) as login:
            pipeline.validate_chatgpt_login("codex", sanitized)
            self.assertEqual(login.call_args.args[0], ["codex", "login", "status"])
            self.assertIs(login.call_args.kwargs["env"], sanitized)
        with (
            patch.object(
                pipeline.subprocess,
                "run",
                return_value=SimpleNamespace(
                    returncode=0, stdout="Logged in using an API key", stderr=""
                ),
            ),
            self.assertRaisesRegex(
                ValueError, "requires Codex signed in using ChatGPT"
            ),
        ):
            pipeline.validate_chatgpt_login("codex", sanitized)

    def prepared_job(self, directory):
        source = sample()
        job = {
            "slug": "test",
            "locale": "en",
            "source_locale": "zh-TW",
            "mode": "full",
            "source_document": source,
            "source_sha256": pipeline.digest(source),
            "pack_path": None,
            "assets": [],
            "fields": pipeline.document_fields(source),
        }
        job["job_sha256"] = pipeline.digest(job)
        pipeline.write_json(directory / "source.json", job)
        pipeline.write_json(directory / "fields.json", job["fields"])
        pipeline.write_json(
            directory / "receipt.json",
            {
                "status": "prepared",
                "job_sha256": job["job_sha256"],
                **pipeline.bind_artifacts(directory, job, "prepared"),
            },
        )
        return job

    def completed_job(self, directory, stage="rendered"):
        job = self.prepared_job(directory)
        pipeline.write_json(
            directory / "translated-fields.json",
            {
                "translations": {
                    key: field["source"] for key, field in job["fields"].items()
                }
            },
        )
        pipeline.write_json(directory / "document.json", job["source_document"])
        pipeline.write_json(directory / "assets.json", [])
        for name in [
            "prompt.txt",
            "output-schema.json",
            "attempt-01.jsonl",
            "attempt-01.output.json",
        ]:
            (directory / name).write_text("{}", encoding="utf-8")
        asset_dir = directory / "assets/guides/test"
        asset_dir.mkdir(parents=True)
        for name in ["diagram-en.svg", "diagram-en-preview.png", "hero-en.jpg"]:
            (asset_dir / name).write_bytes(b"test bytes")
        if stage == "rendered":
            pipeline.write_json(
                directory / "render-receipt.json", {"automatedLayoutPassed": True}
            )
        receipt = {
            "status": stage,
            "job_sha256": job["job_sha256"],
            "document_sha256": pipeline.digest(job["source_document"]),
            **pipeline.bind_artifacts(directory, job, stage, True),
        }
        pipeline.write_json(directory / "receipt.json", receipt)
        return job, receipt

    def test_resume_rejects_each_bound_input_and_render_artifact_drift(self):
        for name in [
            "translated-fields.json",
            "assets.json",
            "render-receipt.json",
            "prompt.txt",
            "output-schema.json",
            "attempt-01.output.json",
            "assets/guides/test/diagram-en.svg",
            "assets/guides/test/hero-en.jpg",
            "assets/guides/test/diagram-en-preview.png",
        ]:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                directory = Path(tmp)
                self.completed_job(directory)
                self.assertEqual(
                    pipeline.run_job(directory, "codex", 0, threading.Event())[
                        "status"
                    ],
                    "unchanged",
                )
                with (directory / name).open("ab") as handle:
                    handle.write(b"\n")
                with self.assertRaisesRegex(ValueError, "artifact changed"):
                    pipeline.run_job(directory, "codex", 0, threading.Event())

    def test_resume_rejects_added_asset_and_forged_receipt_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            job, receipt = self.completed_job(directory, "translated")
            receipt["status"] = "rendered"
            with self.assertRaisesRegex(ValueError, "stage"):
                pipeline.verify_artifacts(directory, job, receipt)
            receipt["status"] = "translated"
            (directory / "assets/unlisted.png").write_bytes(b"added")
            with self.assertRaisesRegex(ValueError, "set changed"):
                pipeline.verify_artifacts(directory, job, receipt)

    def test_existing_raster_without_svg_remains_explicit_pending_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            public = root / "apps/web/public"
            (public / "guides/test").mkdir(parents=True)
            (public / "guides/test/hero.jpg").write_bytes(
                b"raster content requiring review"
            )
            source = {
                "title": "Travel",
                "description": "Travel guide.",
                "hero": {
                    "src": "/guides/test/hero.jpg",
                    "alt": "Cover",
                    "width": 300,
                    "height": 200,
                },
                "blocks": [
                    {
                        "type": "paragraph",
                        "text": "Existing body must not be translated.",
                    }
                ],
            }
            article = {
                "slug": "test",
                "source_locale": "zh-TW",
                "source_document": source,
                "source_sha256": pipeline.digest(source),
                "missing_locales": [],
                "locale_documents": {"en": source},
                "pack_path": None,
                "pack_sha256": None,
                "status": "published",
            }
            directory = pipeline.prepare(article, "en", root / "work", public, True)
            self.assertIsNotNone(directory)
            job = pipeline.read_json(directory / "source.json")
            self.assertEqual(job["mode"], "review-only")
            self.assertEqual(job["fields"], {})
            self.assertEqual(
                pipeline.read_json(directory / "receipt.json")["status"],
                "pending_review",
            )
            drift_guard = pipeline.assert_no_drift
            with (
                patch.object(
                    pipeline,
                    "assert_no_drift",
                    side_effect=lambda current: drift_guard(current, root),
                ),
                patch.object(pipeline.subprocess, "run") as invoked,
            ):
                result = pipeline.run_job(directory, "codex", 0, threading.Event())
            invoked.assert_not_called()
            self.assertEqual(result["status"], "pending_review")
            self.assertEqual(
                result["raster_review_required"], ["/guides/test/hero.jpg"]
            )
            pipeline.assert_no_drift(job, root)
            (public / "guides/test/hero.jpg").write_bytes(b"changed")
            with self.assertRaisesRegex(ValueError, "source raster changed"):
                pipeline.assert_no_drift(job, root)

    def test_existing_publication_target_is_staged_for_review_without_model_call(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            public = root / "apps/web/public"
            source = {
                "title": "Reviewed English title",
                "description": "Reviewed English description.",
                "hero": None,
                "blocks": [{"type": "paragraph", "text": "Complete existing prose."}],
                "sources": [],
            }
            source_original = copy.deepcopy(source)
            article = {
                "slug": "test",
                "source_locale": "zh-TW",
                "source_document": source_original,
                "source_sha256": pipeline.digest(source_original),
                "missing_locales": [],
                "target_locales": ["en"],
                "publication_locales": ["en"],
                "locale_documents": {"en": source},
                "pack_path": None,
                "pack_sha256": None,
                "status": "published",
                "assets": [],
            }
            directory = pipeline.prepare(
                article, "en", root / "work", public, include_existing=False
            )
            job = pipeline.read_json(directory / "source.json")
            receipt = pipeline.read_json(directory / "receipt.json")
            self.assertEqual(job["mode"], "review-only")
            self.assertEqual(receipt["status"], "pending_review")
            self.assertTrue(receipt["schema_validated"])
            self.assertEqual(pipeline.read_json(directory / "document.json"), source)
            self.assertEqual(pipeline.read_json(directory / "assets.json"), [])
            with patch.object(pipeline.subprocess, "run") as invoked:
                result = pipeline.run_job(
                    directory, "codex", 0, threading.Event(), child_env={}
                )
            invoked.assert_not_called()
            self.assertEqual(result["status"], "pending_review")

    def test_chinese_variant_cannot_copy_body_while_only_changing_title(self):
        for source_locale, target_locale, title, translated_title, body in [
            (
                "zh-TW",
                "zh-CN",
                "台灣入境規則與完整文件說明",
                "台湾入境规则与完整文件说明",
                "這是一段繁體中文說明，規則與相關資訊需要完整保留。這是另一句詳細說明，不得省略。",
            ),
            (
                "zh-CN",
                "zh-TW",
                "台湾入境规则与完整文件说明",
                "台灣入境規則與完整文件說明",
                "这是一段简体中文说明，规则与相关资讯需要完整保留。这是另一句详细说明，不得省略。",
            ),
        ]:
            fields = {
                "/document/title": {
                    "source": title,
                    "kind": "document",
                    "max_length": 200,
                },
                "/document/blocks/0/text": {
                    "source": body,
                    "kind": "document",
                    "max_length": 4000,
                },
            }
            errors = pipeline.validate_fields(
                fields,
                {"/document/title": translated_title, "/document/blocks/0/text": body},
                source_locale,
                target_locale,
            )
            self.assertTrue(
                any(
                    "/document/blocks/0/text" in error and "copied" in error
                    for error in errors
                ),
                errors,
            )

    def test_valid_chinese_variant_may_keep_script_neutral_prose(self):
        fields = {
            "/document/title": {
                "source": "入口出口",
                "kind": "document",
                "max_length": 200,
            }
        }
        self.assertEqual(
            pipeline.validate_fields(
                fields, {"/document/title": "入口出口"}, "zh-TW", "zh-CN"
            ),
            [],
        )

    def test_stop_file_created_by_failed_attempt_prevents_transport_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.prepared_job(directory)
            stop_file = directory / "STOP"

            def transient(command, **kwargs):
                kwargs["stderr"].write(b"connection reset")
                stop_file.touch()
                return SimpleNamespace(returncode=1)

            stop = threading.Event()
            with (
                patch.object(
                    pipeline.subprocess, "run", side_effect=transient
                ) as invoked,
                patch.object(stop, "wait", return_value=False),
            ):
                result = pipeline.run_job(directory, "codex", 1, stop, stop_file)
            self.assertEqual(invoked.call_count, 1)
            self.assertEqual(result["status"], "prepared")

    def test_quota_failure_is_not_retried_and_stops_other_workers(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.prepared_job(directory)
            stop = threading.Event()

            def quota(command, **kwargs):
                kwargs["stdout"].write(
                    b'{"type":"turn.failed","error":{"message":"usage limit reached"}}\n'
                )
                return SimpleNamespace(returncode=1)

            child_env = {"PATH": "bin", "CODEX_HOME": "home"}
            with patch.object(pipeline.subprocess, "run", side_effect=quota) as invoked:
                result = pipeline.run_job(
                    directory, "codex", 2, stop, child_env=child_env
                )
            self.assertEqual(result["status"], "blocked")
            self.assertEqual(invoked.call_count, 1)
            self.assertIs(invoked.call_args.kwargs["env"], child_env)
            self.assertTrue(stop.is_set())
            self.assertFalse((directory / "running.lock").exists())
            self.assertEqual(
                pipeline.read_json(directory / "attempt-01.receipt.json")["returncode"],
                1,
            )

    def test_stop_file_prevents_new_cli_calls(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.prepared_job(directory)
            stop_file = directory / "STOP"
            stop_file.touch()
            with patch.object(pipeline.subprocess, "run") as invoked:
                result = pipeline.run_job(
                    directory, "codex", 0, threading.Event(), stop_file
                )
            self.assertEqual(result["status"], "not_started")
            invoked.assert_not_called()

    def test_existing_lock_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.prepared_job(directory)
            (directory / "running.lock").write_text('{"pid":123}', encoding="utf-8")
            result = pipeline.run_job(directory, "codex", 0, threading.Event())
            self.assertEqual(result["status"], "locked")
            self.assertTrue((directory / "running.lock").exists())

    def test_modified_staged_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            job = self.prepared_job(Path(tmp))
            job["source_document"]["title"] = "changed"
            with self.assertRaisesRegex(ValueError, "manifest changed"):
                pipeline.assert_no_drift(job)

    def test_allowlist_preserves_code_credit_urls_and_article_identity(self):
        source = sample()
        fields = pipeline.document_fields(source)
        pointers = " ".join(fields)
        self.assertNotIn("/code", pointers)
        self.assertNotIn("/credit", pointers)
        self.assertNotIn("/url", pointers)
        self.assertNotIn("/slug", pointers)
        self.assertNotIn("/inlines/1/text", pointers)
        result = copy.deepcopy(source)
        for pointer in fields:
            pipeline.set_pointer(
                result, pointer.removeprefix("/document"), "translated"
            )
        self.assertEqual(result["blocks"][2]["code"], source["blocks"][2]["code"])
        self.assertEqual(
            result["blocks"][1]["inlines"][1], source["blocks"][1]["inlines"][1]
        )
        self.assertEqual(result["blocks"][4]["credit"], source["blocks"][4]["credit"])
        self.assertEqual(result["sources"][0]["checked_on"], "2026-09-14")

    def test_prepared_migration_never_resets_a_quota_block_or_prior_attempt(self):
        for status, attempted in [("blocked", False), ("prepared", True)]:
            with tempfile.TemporaryDirectory() as tmp:
                directory = Path(tmp)
                job = self.prepared_job(directory)
                pipeline.write_json(
                    directory / "receipt.json",
                    {"status": status, "job_sha256": job["job_sha256"]},
                )
                if attempted:
                    (directory / "attempt-01.jsonl").write_text("{}", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "never reset"):
                    pipeline.migrate_prepared(directory, {}, "test")

    def test_unknown_block_fails_closed(self):
        source = sample()
        source["blocks"].append({"type": "new_unsupported", "text": "重要內容"})
        with self.assertRaisesRegex(ValueError, "unsupported block"):
            pipeline.document_fields(source)

    def test_svg_extracts_nested_tspans_and_accessibility_without_geometry(self):
        raw = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200"><title>標題</title><desc>說明</desc><text x="15">前文<tspan x="40">重點</tspan>後文</text><path d="M 0 2 L 3 4"/></svg>'
        root, slots = pipeline.svg_slots(raw)
        self.assertEqual(
            [getattr(node, key) for node, key in slots],
            ["標題", "說明", "前文", "重點", "後文"],
        )
        for node, key in slots:
            setattr(node, key, "Text")
        self.assertEqual(root[-1].attrib["d"], "M 0 2 L 3 4")
        self.assertEqual(root[2].attrib["x"], "15")

    def test_external_entity_svg_rejected(self):
        with self.assertRaisesRegex(ValueError, "entities"):
            pipeline.svg_slots(
                '<!DOCTYPE svg [<!ENTITY x SYSTEM "file:///secret">]><svg xmlns="http://www.w3.org/2000/svg"/>'
            )

    def test_field_missing_extra_numbers_and_source_copy_rejected(self):
        fields = {
            "/document/title": {
                "source": "台灣護照持有人必須在出發前確認入境要求並保留相關申請文件 3",
                "max_length": 200,
                "kind": "document",
            }
        }
        self.assertTrue(
            any(
                "field set" in message
                for message in pipeline.validate_fields(
                    fields, {"bad": "x"}, "zh-TW", "en"
                )
            )
        )
        self.assertTrue(
            any(
                "numeric" in message
                for message in pipeline.validate_fields(
                    fields, {"/document/title": "Check rules 4"}, "zh-TW", "en"
                )
            )
        )
        self.assertTrue(
            any(
                "copied" in message
                for message in pipeline.validate_fields(
                    fields,
                    {"/document/title": fields["/document/title"]["source"]},
                    "zh-TW",
                    "en",
                )
            )
        )
        self.assertEqual(
            pipeline.validate_fields(
                fields,
                {
                    "/document/title": "Taiwan passport holders must check entry requirements before departure and retain application documents 3"
                },
                "zh-TW",
                "en",
            ),
            [],
        )

    def test_simplified_conversion_can_preserve_identical_short_terms(self):
        fields = {
            "/document/title": {
                "source": "台灣旅行",
                "max_length": 200,
                "kind": "document",
            },
            "/document/blocks/0/text": {
                "source": "API",
                "max_length": 200,
                "kind": "document",
            },
        }
        result = {"/document/title": "台湾旅行", "/document/blocks/0/text": "API"}
        self.assertEqual(pipeline.validate_fields(fields, result, "zh-TW", "zh-CN"), [])

    def test_batch_requires_explicit_known_max20_sources(self):
        baseline = {
            "articles": [{"slug": f"article-{i}"} for i in range(21)],
            "batches": [{"id": "large", "slugs": [f"article-{i}" for i in range(21)]}],
        }
        with self.assertRaisesRegex(ValueError, "1–20"):
            pipeline.selected_articles(baseline, "large", None)
        with self.assertRaisesRegex(ValueError, "unknown"):
            pipeline.selected_articles(baseline, None, "missing")
        self.assertEqual(
            len(pipeline.selected_articles(baseline, None, "article-0,article-1")), 2
        )

    def test_bilingual_svg_metadata_can_collapse_duplicate_numbers(self):
        field = {
            "source": "日期 2026/9/1。Checked on 2026/9/1.",
            "max_length": 200,
            "kind": "svg",
            "svg_tag": "desc",
        }
        translation = "日期為 2026/9/1。"
        self.assertEqual(
            pipeline.validate_fields(
                {"/assets/0/text/1": field},
                {"/assets/0/text/1": translation},
                "en",
                "zh-TW",
            ),
            [],
        )
        visible_field = {**field, "svg_tag": "text"}
        errors = pipeline.validate_fields(
            {"/assets/0/text/0": visible_field},
            {"/assets/0/text/0": translation},
            "en",
            "zh-TW",
        )
        self.assertIn("changed numeric, URL, or inline-code tokens", errors[0])

    def test_nested_or_multiple_svg_descriptions_fail_closed(self):
        for source in [
            '<svg xmlns="http://www.w3.org/2000/svg"><g><desc>nested</desc></g></svg>',
            '<svg xmlns="http://www.w3.org/2000/svg"><desc>one</desc><desc>two</desc></svg>',
        ]:
            root, _ = pipeline.svg_slots(source)
            with self.assertRaisesRegex(ValueError, "one root-level desc"):
                pipeline.root_description(root)

    def test_image_only_does_not_retranslate_body_and_detects_svg_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            public = root / "apps/web/public"
            image_dir = public / "guides/test"
            image_dir.mkdir(parents=True)
            svg = image_dir / "diagram.svg"
            svg.write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200"><title>旅行 3 圖</title><desc>旅行 3 說明</desc><text x="10">旅行 3</text></svg>',
                encoding="utf-8",
            )
            source = sample()
            article = {
                "slug": "test",
                "source_locale": "zh-TW",
                "source_document": source,
                "source_sha256": pipeline.digest(source),
                "missing_locales": [],
                "locale_documents": {"en": source},
                "pack_path": None,
                "pack_sha256": None,
                "status": "published",
            }
            directory = pipeline.prepare(article, "en", root / "work", public, True)
            job = pipeline.read_json(directory / "source.json")
            self.assertEqual(job["mode"], "images-only")
            self.assertTrue(
                all(pointer.startswith("/assets/") for pointer in job["fields"])
            )
            translations = {pointer: "Travel 3" for pointer in job["fields"]}
            pipeline.materialize(job, translations, directory, validate_schema=False)
            actual = pipeline.read_json(directory / "document.json")
            self.assertEqual(actual["title"], source["title"])
            self.assertEqual(actual["blocks"][4]["src"], "/guides/test/diagram-en.svg")
            self.assertEqual(actual["blocks"][4]["description"], "Travel 3")
            pipeline.assert_no_drift(job, root)
            svg.write_text(
                '<svg xmlns="http://www.w3.org/2000/svg"/>', encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "SVG changed"):
                pipeline.assert_no_drift(job, root)

    def test_work_path_cannot_escape(self):
        with (
            tempfile.TemporaryDirectory() as tmp,
            self.assertRaisesRegex(ValueError, "outside"),
        ):
            pipeline.contained(Path(tmp), "../outside")


if __name__ == "__main__":
    unittest.main()
