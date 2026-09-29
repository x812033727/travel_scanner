"""Exercise strict content intake with local fixture packs, without publishing or fetching."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

import pytest

from app.guides import content_pack, pack_cli

ROOT = Path(content_pack.__file__).resolve().parents[4]
TOOL = ROOT / ".agents/skills/content-pipeline/scripts/intake_check.py"
SLUG = "intake-fixture"
LOCALES = ("zh-TW", "zh-CN", "en", "ja", "ko")


def load_tool() -> ModuleType:
    spec = importlib.util.spec_from_file_location("content_pipeline_intake", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def pack():
    # A self-contained valid pack: tests do not depend on authored articles or their hashes.
    document = {
        "title": "記事タイトルと内容の確認",
        "description": "対象と範囲を確認し、根拠に沿ってタイトルを整えます。" * 3,
        "hero": {
            "src": f"/guides/{SLUG}/hero.jpg",
            "alt": "内容と見出しの確認図",
            "width": 1600,
            "height": 900,
            "credit": {"author": "Mokaair", "license": "© Mokaair"},
        },
        "blocks": [
            {
                "type": "summary",
                "items": ["タイトルの対象と範囲を確認します。", "内容に合う表現を選びます。"],
            },
            {"type": "heading", "level": 2, "text": "対象を確認する"},
            {
                "type": "paragraph",
                "text": "対象と範囲を確認し、根拠に沿ってタイトルを整えます。" * 70,
            },
            {"type": "heading", "level": 2, "text": "表現を選ぶ"},
            {"type": "paragraph", "text": "内容に合う表現を選びます。"},
            {"type": "heading", "level": 2, "text": "根拠を確かめる"},
            {
                "type": "table",
                "header": ["確認項目", "手順"],
                "rows": [["対象", "内容と比較する"]],
            },
            {"type": "callout", "tone": "tip", "text": "根拠に沿う表現を選びます。"},
            {
                "type": "image",
                "src": f"/guides/{SLUG}/diagram-1.svg",
                "alt": "確認手順の図",
                "width": 1600,
                "height": 900,
            },
            {
                "type": "rich_paragraph",
                "inlines": [
                    {"type": "article", "slug": "fixture-target", "kind": "life", "text": "関連"}
                ],
            },
        ],
        "sources": [
            {
                "title": "Editorial fixture",
                "url": "https://example.org/editorial",
                "checked_on": "2026-09-29",
            }
        ],
    }
    return {
        "slug": SLUG,
        "kind": "life",
        "destination_id": None,
        "locales": {locale: copy.deepcopy(document) for locale in LOCALES},
    }


@pytest.fixture
def run_intake(tmp_path, monkeypatch, capsys):
    module = load_tool()
    content = tmp_path / "content"
    content.mkdir()
    public = tmp_path / "public"
    diagrams = public / "guides" / SLUG
    diagrams.mkdir(parents=True)
    (diagrams / "diagram-1.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900">'
        '<title>確認手順</title><desc>対象と範囲を確認する図</desc>'
        '<text font-size="24">対象と範囲</text></svg>',
        encoding="utf-8",
    )
    (content / "fixture-target.json").write_text(
        json.dumps({"kind": "life", "locales": {locale: {} for locale in LOCALES}}),
        encoding="utf-8",
    )
    monkeypatch.setattr(content_pack, "default_directory", lambda: content)
    monkeypatch.setattr(pack_cli, "default_public_dir", lambda: public)
    # main() changes cwd; pytest's monkeypatch restores the caller's cwd after this test.
    monkeypatch.chdir(tmp_path)

    def run(raw, locale="ja", *, reader_first=None):
        module.FAILS.clear()
        (content / f"{SLUG}.json").write_text(
            json.dumps(raw, ensure_ascii=False), encoding="utf-8"
        )
        argv = [
            str(TOOL),
            "--slug",
            SLUG,
            "--from-content",
            "--locale",
            locale,
            "--api-dir",
            str(ROOT / "apps/api"),
        ]
        if reader_first is not None:
            manifest = tmp_path / "manifest.json"
            manifest.write_text(json.dumps({"reader_first": reader_first}), encoding="utf-8")
            argv.extend(["--manifest", str(manifest)])
        monkeypatch.setattr(sys, "argv", argv)
        exit_code = module.main()
        return exit_code, capsys.readouterr().out

    return run


def test_japanese_body_text_is_not_article_self_reference(pack, run_intake):
    document = pack["locales"]["ja"]
    document["title"] += "と本文"
    document["description"] += "本文で根拠を確認します。"
    document["blocks"][4]["text"] = "タイトルと本文をそろえます。本文で根拠を示します。" * 7

    code, output = run_intake(pack)

    assert code == 0, output
    assert "self-reference count (本記事/この記事/本稿) = 0 (limit 1)" in output
    assert "RESULT PASS (0 failures)" in output


@pytest.mark.parametrize("term", ["本記事", "この記事", "本稿"])
@pytest.mark.parametrize("count", [1, 2])
def test_japanese_explicit_self_reference_limit(pack, run_intake, term, count):
    pack["locales"]["ja"]["blocks"][4]["text"] = f"{term}では説明します。" * count

    code, output = run_intake(pack)

    assert code == (0 if count == 1 else 1), output
    assert f"self-reference count (本記事/この記事/本稿) = {count} (limit 1)" in output


@pytest.mark.parametrize("limit, expected_code", [(2, 1), (3, 0)])
def test_japanese_limit_override_counts_title_description_and_body(
    pack, run_intake, limit, expected_code
):
    document = pack["locales"]["ja"]
    document["title"] = "この記事の確認手順"
    document["description"] += "本稿では説明します。"
    document["blocks"][4]["text"] = "本記事の手順を示します。"

    code, output = run_intake(pack, reader_first={"self_ref_limit": limit})

    assert code == expected_code, output
    assert f"self-reference count (本記事/この記事/本稿) = 3 (limit {limit})" in output


@pytest.mark.parametrize("locale", ["zh-TW", "zh-CN", "en", "ko"])
@pytest.mark.parametrize("count", [1, 2])
def test_other_locales_keep_existing_chinese_matcher(pack, run_intake, locale, count):
    # Deliberately preserve the current rule even outside Chinese; this patch changes ja only.
    text = "本文說明方法。" if count == 1 else "本文說明方法。這篇介紹規則。"
    pack["locales"][locale]["blocks"][4]["text"] = text + "本記事・この記事・本稿"

    code, output = run_intake(pack, locale)

    assert code == (0 if count == 1 else 1), output
    assert f"self-reference count (本文/這篇) = {count} (limit 1)" in output


def test_japanese_still_enforces_attribution_limit(pack, run_intake):
    # Keep the independent existing reader-first rule active, including its manifest override.
    pack["locales"]["ja"]["blocks"][4]["text"] = "官方頁寫需要確認。官方頁說需要比較。"

    code, output = run_intake(pack)
    assert code == 1, output
    assert "has 2 attribution phrases" in output

    code, output = run_intake(pack, reader_first={"attrib_para_limit": 2})
    assert code == 0, output


@pytest.mark.parametrize("problem", ["missing-summary", "summary-number", "inline-target"])
def test_japanese_structural_and_evidence_checks_remain_active(pack, run_intake, problem):
    blocks = pack["locales"]["ja"]["blocks"]
    if problem == "missing-summary":
        blocks[0] = {"type": "paragraph", "text": "タイトルの対象と範囲を確認します。"}
        expected = "first block is not summary"
    elif problem == "summary-number":
        blocks[0]["items"][0] = "確認する項目は98765です。"
        expected = "summary number '98765' not found verbatim in the body"
    else:
        blocks[-1]["inlines"][0]["slug"] = "missing-fixture-target"
        expected = "inline target missing-fixture-target does not exist"

    code, output = run_intake(pack)

    assert code == 1, output
    assert expected in output
