"""The content-pack production tool: the editorial rules a machine can check, the Commons
licence gate, the byte caps, and an ingest that writes everything or nothing.

No network and no browser: the Commons client is an ``httpx.MockTransport`` and the renderer a
function that paints a PNG with Pillow.
"""

from __future__ import annotations

import copy
import io
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread
from typing import Any

import httpx
import pytest
from PIL import Image

from app.guides import pack_ingest
from app.guides.pack_ingest import (
    FINANCE_DISCLAIMER_MARKERS,
    HERO_MAX_BYTES,
    PHOTO_MAX_BYTES,
    USER_AGENT,
    PackIngestError,
    UrllibTransport,
    catalogue_slugs,
    check_svg,
    commons_client,
    commons_file_info,
    diagram_numbers,
    errors,
    fetch_image,
    fit_bytes,
    ingest,
    license_allowed,
    lint_all,
    lint_document,
    missing_diagram_numbers,
)
from app.guides.schemas import GuideDocument

GOOD_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900"
  width="1600" height="900" font-family="'Noto Sans TC',system-ui,sans-serif">
  <title>三種方式 / Three ways</title>
  <desc>一張比較圖。</desc>
  <defs><marker id="arrow"><path d="M0,0 L8,4 L0,8z"/></marker></defs>
  <rect width="1600" height="900" fill="#F7F1E8"/>
  <line x1="0" y1="0" x2="10" y2="10" marker-end="url(#arrow)"/>
  <text x="100" y="100" font-size="24">免費版 Free · 每月 1,000 次</text>
  <text x="100" y="200" font-size="18"><tspan>06:30</tspan> 開始</text>
</svg>
"""


def body_svg(height: int = 1980) -> str:
    return GOOD_SVG.replace('viewBox="0 0 1600 900"', f'viewBox="0 0 1600 {height}"').replace(
        'height="900"', f'height="{height}"', 1
    )


def good_document(**overrides: object) -> dict[str, Any]:
    document: dict[str, Any] = {
        "title": "ChatGPT 新手入門",
        "description": "註冊、免費與付費差別、第一個對話。",
        "hero": {
            "src": "/guides/chatgpt-beginner-guide/hero.jpg",
            "alt": "插圖",
            "width": 1,
            "height": 1,
        },
        "blocks": [
            {
                "type": "summary",
                "items": ["先註冊，用 Google 帳號最快。", "免費版夠日常用，付費版多額度與新模型。"],
            },
            {
                "type": "paragraph",
                "text": "先說結論：免費版每月 1000 次夠一般人用，早上 6:30 也能用。",
            },
            {"type": "heading", "level": 2, "text": "註冊"},
            {"type": "paragraph", "text": "用 Google 帳號登入最快。" * 150},
            {"type": "heading", "level": 2, "text": "免費與付費"},
            {
                "type": "table",
                "header": ["方案", "價格"],
                "rows": [["免費", "0"], ["Plus", "以官網為準"]],
                "caption": "2026 年 9 月查證",
            },
            {"type": "heading", "level": 2, "text": "第一個對話"},
            {"type": "callout", "tone": "tip", "title": "小提醒", "text": "不要貼個資。"},
            {
                "type": "image",
                "src": "/guides/chatgpt-beginner-guide/diagram-1.svg",
                "alt": "三種方式的比較圖",
                "width": 1,
                "height": 1,
                "caption": "三種方式",
            },
            # A site link that is not an article: an article link would be flagged as a
            # raw URL (``raw_internal_url``), which the relink command turns into an inline.
            {
                "type": "link",
                "text": "生活分享",
                "url": "https://mokaair.com/zh-TW/life",
            },
        ],
        "sources": [
            {
                "title": "OpenAI Help Center",
                "url": "https://help.openai.com/",
                "checked_on": "2026-09-13",
            }
        ],
    }
    document.update(overrides)
    return document


def test_lint_document_accepts_a_complete_article_and_names_what_is_missing() -> None:
    assert lint_document(GuideDocument.model_validate(good_document()), "life") == []

    blocks = [
        b
        for b in good_document()["blocks"]
        if b["type"] not in {"table", "callout", "image", "link"}
    ]
    stripped = GuideDocument.model_validate(
        good_document(
            blocks=blocks[:2],
            hero=None,
            sources=[{"title": "x", "url": "https://example.com/"}],
        )
    )
    codes = {problem.code: problem.level for problem in lint_document(stripped, "life")}
    assert codes["too_few_headings"] == "error"
    # The fixture keeps its summary, so the missing one is only reported without it -- and
    # never for intel, whose notices are too short to summarise.
    without = GuideDocument.model_validate(
        good_document(blocks=[b for b in good_document()["blocks"] if b["type"] != "summary"])
    )
    assert {p.code for p in lint_document(without, "life")} >= {"no_summary"}
    assert "no_summary" not in {p.code for p in lint_document(without, "intel")}
    assert codes["no_table"] == "error"
    assert codes["no_callout"] == "error"
    assert codes["no_hero"] == "error"
    assert codes["source_not_checked"] == "error"
    assert codes["no_diagram"] == "warning"
    assert codes["no_internal_link"] == "warning"
    assert codes["text_length"] == "warning"


def test_finance_rules_only_apply_to_finance_articles() -> None:
    """The disclaimer is a template check and the wording one a prompt for the reviewer, so
    one is an error and the other a warning. Both stay silent on every other subject."""
    plain = GuideDocument.model_validate(good_document())
    missing = {p.code: p.level for p in lint_document(plain, "life", topics=("finance",))}
    assert missing["finance_no_disclaimer"] == "error"

    with_disclaimer = GuideDocument.model_validate(
        good_document(
            blocks=[
                *good_document()["blocks"],  # type: ignore[misc]
                {
                    "type": "callout",
                    "tone": "warning",
                    "title": "\u672c\u6587\u4e0d\u662f\u6295\u8cc7\u5efa\u8b70",
                    "text": (
                        "\u672c\u6587\u6574\u7406\u7684\u662f\u5236\u5ea6\u8207\u65b9\u6cd5\uff0c"
                        "\u4e0d\u662f\u6295\u8cc7\u5efa\u8b70\uff0c\u4e5f\u4e0d\u63a8\u85a6\u4efb\u4f55\u5546\u54c1\u3002"
                    ),
                },
            ]
        )
    )
    codes = {p.code for p in lint_document(with_disclaimer, "life", topics=("finance",))}
    assert "finance_no_disclaimer" not in codes

    # lint_all lints one locale document at a time and is never told which locale it holds,
    # so each language's own marker has to satisfy the rule on its own. A Chinese-only marker
    # would have failed four of the five documents of every translated finance article.
    for marker in FINANCE_DISCLAIMER_MARKERS:
        translated = GuideDocument.model_validate(
            good_document(
                blocks=[
                    *good_document()["blocks"],  # type: ignore[misc]
                    {
                        "type": "callout",
                        "tone": "warning",
                        "title": "Disclaimer",
                        "text": f"This is {marker}.",
                    },
                ]
            )
        )
        found = {p.code for p in lint_document(translated, "life", topics=("finance",))}
        assert "finance_no_disclaimer" not in found, marker

    # retopic never adds ``finance`` to a crypto-* article, because ``finance`` is one of the
    # original eight parents it leaves alone. The rule keys on the whole money vertical so
    # that gap cannot silently switch the disclaimer off.
    assert "finance_no_disclaimer" in {
        p.code for p in lint_document(plain, "life", topics=("crypto",))
    }

    # The scan reads the running text, so a claim buried in a table cell counts too.
    shouting = good_document()["blocks"]
    shouting[3] = {  # type: ignore[index]
        "type": "paragraph",
        "text": "\u9019\u500b\u65b9\u6cd5\u7a69\u8cfa\uff0c\u5b8c\u5168\u7121\u98a8\u96aa\u3002"
        * 60,
    }
    loud = GuideDocument.model_validate(good_document(blocks=shouting))
    claims = {p.code: p.level for p in lint_document(loud, "life", topics=("finance",))}
    assert claims["finance_claim_language"] == "warning"

    # Money that is not investing -- a Wise transfer checklist, registering a company -- is
    # outside the rule on purpose: a disclaimer pasted where it does not belong is how one
    # stops being read. Four shipped articles are in exactly that position.
    for topics in (("banking",), ("tax-insurance",), ("finance-basics",), ("credit",)):
        assert "finance_no_disclaimer" not in {
            p.code for p in lint_document(plain, "life", topics=topics)
        }

    # Same words, a different subject: neither rule has anything to say, and neither does a
    # caller that passes no topics at all.
    for topics in (("ai",), ()):
        quiet = {p.code for p in lint_document(loud, "life", topics=topics)}
        assert "finance_claim_language" not in quiet
        assert "finance_no_disclaimer" not in quiet


def test_check_svg_holds_the_diagram_rules() -> None:
    assert check_svg(GOOD_SVG) == []
    bad = (
        GOOD_SVG.replace('viewBox="0 0 1600 900"', 'viewBox="0 0 800 450"')
        .replace("<title>三種方式 / Three ways</title>", "")
        .replace('font-size="18"', 'font-size="12"')
        .replace("<rect", '<image href="https://example.com/x.png"/><rect')
    )
    codes = {problem.code for problem in check_svg(bad)}
    assert codes == {
        "svg_viewbox",
        "svg_no_title",
        "svg_small_label",
        "svg_forbidden_element",
        "svg_external_reference",
    }
    assert check_svg("<svg")[0].code == "svg_invalid"
    # A fragment reference is how markers and gradients work; only a fetch is refused.
    assert not errors(check_svg(GOOD_SVG.replace("url(#arrow)", "url(#gradient)")))
    assert errors(check_svg(GOOD_SVG.replace("<rect", "<style>@import 'x.css';</style><rect")))


def test_body_svg_accepts_a_validated_variable_height_without_changing_the_default() -> None:
    tall = body_svg()
    assert check_svg(tall, body=True) == []
    assert {problem.code for problem in errors(check_svg(tall))} == {"svg_viewbox"}


@pytest.mark.parametrize(
    ("mutated", "code"),
    [
        (body_svg().replace('viewBox="0 0 1600 1980"', 'viewBox="0 0 1600"'), "svg_viewbox"),
        (body_svg().replace('viewBox="0 0 1600 1980"', 'viewBox="0 0 1600 NaN"'), "svg_viewbox"),
        (
            body_svg().replace('viewBox="0 0 1600 1980"', 'viewBox="0 0 1_600 1980"'),
            "svg_viewbox",
        ),
        (
            body_svg().replace('viewBox="0 0 1600 1980"', 'viewBox="0 0 １６００ 1980"'),
            "svg_viewbox",
        ),
        (body_svg().replace('viewBox="0 0 1600 1980"', 'viewBox="1 0 1600 1980"'), "svg_viewbox"),
        (body_svg().replace('viewBox="0 0 1600 1980"', 'viewBox="0 0 800 990"'), "svg_viewbox"),
        (body_svg().replace('viewBox="0 0 1600 1980"', 'viewBox="0 0 1600 0"'), "svg_viewbox"),
        (body_svg().replace('viewBox="0 0 1600 1980"', 'viewBox="0 0 1600 -1"'), "svg_viewbox"),
        (body_svg().replace('viewBox="0 0 1600 1980"', 'viewBox="0 0 1600 1980.5"'), "svg_viewbox"),
        (body_svg(4001), "svg_viewbox"),
        (
            body_svg().replace(' width="1600" height="1980"', "", 1),
            "svg_dimensions",
        ),
        (body_svg().replace('width="1600"', 'width="1600px"', 1), "svg_dimensions"),
        (body_svg().replace('width="1600"', 'width="1_600"', 1), "svg_dimensions"),
        (body_svg().replace('width="1600"', 'width="１６００"', 1), "svg_dimensions"),
        (body_svg().replace('height="1980"', 'height="1980px"', 1), "svg_dimensions"),
        (
            body_svg().replace(
                'width="1600" height="1980"', 'width="800" height="990"', 1
            ),
            "svg_dimensions",
        ),
    ],
)
def test_body_svg_rejects_invalid_or_mismatched_dimensions(mutated: str, code: str) -> None:
    assert code in {problem.code for problem in errors(check_svg(mutated, body=True))}


def test_body_svg_keeps_the_legacy_fixed_viewbox_without_root_dimensions() -> None:
    legacy = GOOD_SVG.replace(' width="1600" height="900"', "", 1)
    assert check_svg(legacy, body=True) == []


def test_body_svg_accepts_ascii_decimal_and_exponent_forms() -> None:
    numeric = body_svg().replace(
        'viewBox="0 0 1600 1980"', 'viewBox="+0.0 -0 1.6e3 1.980E+3"'
    )
    numeric = numeric.replace(
        'width="1600" height="1980"', 'width="1600.0" height="198e1"', 1
    )
    assert check_svg(numeric, body=True) == []


def test_tall_body_svg_keeps_the_existing_security_and_legibility_rules() -> None:
    tall = body_svg()
    broken = (
        tall.replace('font-size="18"', 'font-size="14"')
        .replace("<rect", '<foreignObject/><script/><image href="https://example.com/x"/><rect')
        .replace("<defs>", "<style>@import 'x.css';</style><defs>")
    )
    codes = {problem.code for problem in errors(check_svg(broken, body=True))}
    assert codes == {"svg_small_label", "svg_forbidden_element", "svg_external_reference"}
    assert not errors(check_svg(tall.replace("url(#arrow)", "url(#gradient)"), body=True))


def test_diagram_numbers_are_the_visible_labels_and_match_the_text_loosely() -> None:
    assert diagram_numbers(GOOD_SVG) == {"1,000", "06:30"}
    document = GuideDocument.model_validate(good_document())
    # The text says 1000 and 6:30; the diagram 1,000 and 06:30. Same figures.
    assert missing_diagram_numbers(GOOD_SVG, document) == []
    drawn = GOOD_SVG.replace("06:30", "07:45")
    assert missing_diagram_numbers(drawn, document) == ["07:45"]


@pytest.mark.parametrize(
    ("short_name", "allowed"),
    [
        ("CC BY-SA 4.0", True),
        ("CC BY 2.0", True),
        ("CC0", True),
        ("Public domain", True),
        ("CC-BY-SA-3.0", True),
        ("CC BY-NC 2.0", False),
        ("CC BY-ND 4.0", False),
        ("CC BY-NC-SA 2.0", False),
        ("KOGL Type 1", False),
        ("", False),
    ],
)
def test_license_allowlist(short_name: str, allowed: bool) -> None:
    assert license_allowed(short_name) is allowed


def _commons_payload(
    license_name: str,
    artist: str = '<a href="x">Someone</a>',
    *,
    url: str = "https://upload.wikimedia.org/original.jpg",
    thumburl: str = "https://upload.wikimedia.org/thumb.jpg",
    descriptionurl: str = "https://commons.wikimedia.org/wiki/File:Desk.jpg",
) -> dict[str, object]:
    return {
        "query": {
            "pages": {
                "1": {
                    "imageinfo": [
                        {
                            "url": url,
                            "thumburl": thumburl,
                            "thumbwidth": 1600,
                            "thumbheight": 1067,
                            "width": 4000,
                            "height": 2667,
                            "descriptionurl": descriptionurl,
                            "extmetadata": {
                                "LicenseShortName": {"value": license_name},
                                "Artist": {"value": artist},
                            },
                        }
                    ]
                }
            }
        }
    }


def _jpeg_bytes(size: tuple[int, int] = (2400, 1600)) -> bytes:
    image = Image.effect_noise(size, 80).convert("RGB")
    buffer = io.BytesIO()
    image.save(buffer, "JPEG", quality=95)
    return buffer.getvalue()


def _commons_client(license_name: str = "CC BY-SA 4.0") -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.host == "commons.wikimedia.org":
            assert request.url.params["titles"].startswith("File:")
            return httpx.Response(200, json=_commons_payload(license_name))
        return httpx.Response(200, content=_jpeg_bytes(), headers={"content-type": "image/jpeg"})

    return httpx.Client(transport=httpx.MockTransport(handler))


def test_commons_file_info_reads_the_licence_and_refuses_the_wrong_one() -> None:
    with _commons_client() as client:
        info = commons_file_info(client, "Desk.jpg")
    assert info.license == "CC BY-SA 4.0"
    assert info.author == "Someone"
    assert info.image_url.endswith("thumb.jpg") and info.width == 1600
    with (
        _commons_client("CC BY-NC 2.0") as client,
        pytest.raises(PackIngestError, match="not allowed"),
    ):
        commons_file_info(client, "File:Desk.jpg")


def test_fit_bytes_gets_a_noisy_picture_under_the_cap(tmp_path: Path) -> None:
    noisy = Image.effect_noise((1600, 900), 120).convert("RGB")
    target = tmp_path / "hero.jpg"
    width, height = fit_bytes(noisy, target, HERO_MAX_BYTES, "JPEG")
    assert target.stat().st_size <= HERO_MAX_BYTES
    assert (width, height) < (1600, 900)
    # With a hard cap the picture keeps its size when the quality floor lands under the cap.
    calm = Image.effect_noise((1600, 900), 12).convert("RGB")
    width, height = fit_bytes(calm, target, 50_000, "JPEG", hard_cap=10_000_000)
    assert (width, height) == (1600, 900)


def _write_workspace(
    root: Path, slug: str = "chatgpt-beginner-guide", *, with_hero_svg: bool = True
) -> Path:
    workspace = root / slug
    workspace.mkdir(parents=True)
    pack = {
        "slug": slug,
        "kind": "life",
        "destination_id": None,
        "topics": ["ai", "tutorial"],
        "featured": False,
        "display_order": 100,
        "locales": {"zh-TW": good_document()},
    }
    (workspace / "pack.json").write_text(json.dumps(pack, ensure_ascii=False), encoding="utf-8")
    (workspace / "diagram-1.svg").write_text(GOOD_SVG, encoding="utf-8")
    if with_hero_svg:
        (workspace / "hero.svg").write_text(GOOD_SVG, encoding="utf-8")
    else:
        (workspace / "images.json").write_text(
            json.dumps({"hero": {"title": "File:Desk.jpg"}}), encoding="utf-8"
        )
    return workspace


def fake_renderer(svg: Path, png: Path) -> None:
    """An illustration compresses like an illustration: flat colour and a gradient."""
    Image.linear_gradient("L").resize((1600, 900)).convert("RGB").save(png, "PNG")


def test_ingest_builds_the_pack_and_its_pictures(tmp_path: Path) -> None:
    workdir, content, public = tmp_path / "work", tmp_path / "content", tmp_path / "public"
    _write_workspace(workdir)
    report = ingest(
        workdir,
        "chatgpt-beginner-guide",
        content_dir=content,
        public_dir=public,
        renderer=fake_renderer,
    )
    assert report.ok, report.problems
    folder = public / "guides" / "chatgpt-beginner-guide"
    assert {p.name for p in folder.iterdir()} == {"hero.jpg", "hero.svg", "diagram-1.svg"}
    assert folder.joinpath("hero.jpg").stat().st_size <= HERO_MAX_BYTES
    written = json.loads((content / "chatgpt-beginner-guide.json").read_text(encoding="utf-8"))
    document = written["locales"]["zh-TW"]
    assert document["hero"]["credit"] == {
        "author": "Mokaair",
        "license": "© Mokaair",
        "source_url": None,
    }
    assert (document["hero"]["width"], document["hero"]["height"]) == (1600, 900)
    diagram = next(block for block in document["blocks"] if block["type"] == "image")
    assert diagram["src"] == "/guides/chatgpt-beginner-guide/diagram-1.svg"
    assert diagram["credit"]["author"] == "Mokaair" and diagram["width"] == 1600
    # The written pack passes the same lint the repository's own test applies.
    findings = lint_all(content, public, kind="life")
    assert findings == {"chatgpt-beginner-guide": []}


def test_ingest_preserves_tall_body_dimensions_for_every_shared_reference(
    tmp_path: Path,
) -> None:
    workdir, content, public = tmp_path / "work", tmp_path / "content", tmp_path / "public"
    workspace = _write_workspace(workdir)
    pack = json.loads((workspace / "pack.json").read_text(encoding="utf-8"))
    pack["locales"]["en"] = copy.deepcopy(pack["locales"]["zh-TW"])
    (workspace / "pack.json").write_text(json.dumps(pack, ensure_ascii=False), encoding="utf-8")
    (workspace / "diagram-1.svg").write_text(body_svg(), encoding="utf-8")

    report = ingest(
        workdir,
        "chatgpt-beginner-guide",
        content_dir=content,
        public_dir=public,
        renderer=fake_renderer,
    )
    assert report.ok, report.problems
    written = json.loads((content / "chatgpt-beginner-guide.json").read_text(encoding="utf-8"))
    for document in written["locales"].values():
        diagram = next(block for block in document["blocks"] if block["type"] == "image")
        assert (diagram["width"], diagram["height"]) == (1600, 1980)
    with Image.open(public / "guides" / "chatgpt-beginner-guide" / "hero.jpg") as hero:
        assert hero.size == (1600, 900)
    assert not errors(lint_all(content, public)["chatgpt-beginner-guide"])


@pytest.mark.parametrize(("width", "height"), [(1600, 900), (800, 990)])
def test_lint_rejects_wrong_metadata_on_the_second_reference_to_a_shared_svg(
    tmp_path: Path, width: int, height: int
) -> None:
    workdir, content, public = tmp_path / "work", tmp_path / "content", tmp_path / "public"
    workspace = _write_workspace(workdir)
    pack = json.loads((workspace / "pack.json").read_text(encoding="utf-8"))
    pack["locales"]["en"] = copy.deepcopy(pack["locales"]["zh-TW"])
    (workspace / "pack.json").write_text(json.dumps(pack, ensure_ascii=False), encoding="utf-8")
    (workspace / "diagram-1.svg").write_text(body_svg(), encoding="utf-8")
    report = ingest(
        workdir,
        "chatgpt-beginner-guide",
        content_dir=content,
        public_dir=public,
        renderer=fake_renderer,
    )
    assert report.ok, report.problems
    final_pack_path = content / "chatgpt-beginner-guide.json"
    final_pack = json.loads(final_pack_path.read_text(encoding="utf-8"))
    second = next(
        block for block in final_pack["locales"]["en"]["blocks"] if block["type"] == "image"
    )
    second.update({"width": width, "height": height})
    final_pack_path.write_text(json.dumps(final_pack, ensure_ascii=False), encoding="utf-8")

    mismatches = [
        problem
        for problem in lint_all(content, public)["chatgpt-beginner-guide"]
        if problem.code == "svg_dimensions_mismatch"
    ]
    assert len(mismatches) == 1
    assert mismatches[0].message == (
        f"en: diagram-1.svg declares {width}x{height}; the SVG is 1600x1980"
    )


def test_a_tall_body_dry_run_writes_nothing_and_a_tall_hero_is_still_rejected(
    tmp_path: Path,
) -> None:
    workdir, content, public = tmp_path / "work", tmp_path / "content", tmp_path / "public"
    workspace = _write_workspace(workdir)
    (workspace / "diagram-1.svg").write_text(body_svg(), encoding="utf-8")
    report = ingest(
        workdir,
        "chatgpt-beginner-guide",
        content_dir=content,
        public_dir=public,
        renderer=fake_renderer,
        dry_run=True,
    )
    assert report.ok and report.written == []
    assert not content.exists() and not public.exists()

    (workspace / "hero.svg").write_text(body_svg(), encoding="utf-8")
    with pytest.raises(PackIngestError, match="must be '0 0 1600 900'"):
        ingest(
            workdir,
            "chatgpt-beginner-guide",
            content_dir=content,
            public_dir=public,
            renderer=fake_renderer,
        )
    assert not content.exists() and not public.exists()


def test_ingest_fetches_a_commons_hero_and_photo_with_credit(tmp_path: Path) -> None:
    workdir, content, public = tmp_path / "work", tmp_path / "content", tmp_path / "public"
    workspace = _write_workspace(workdir, with_hero_svg=False)
    pack = json.loads((workspace / "pack.json").read_text(encoding="utf-8"))
    pack["locales"]["zh-TW"]["blocks"].append(
        {
            "type": "image",
            "src": "/guides/chatgpt-beginner-guide/photo-1.webp",
            "alt": "一張書桌",
            "width": 1,
            "height": 1,
            "caption": "書桌",
        }
    )
    (workspace / "pack.json").write_text(json.dumps(pack, ensure_ascii=False), encoding="utf-8")
    (workspace / "images.json").write_text(
        json.dumps(
            {"hero": {"title": "File:Desk.jpg"}, "photos": {"photo-1": {"title": "File:Desk.jpg"}}}
        ),
        encoding="utf-8",
    )
    with _commons_client() as client:
        report = ingest(
            workdir, "chatgpt-beginner-guide", content_dir=content, public_dir=public, client=client
        )
    assert report.ok, report.problems
    folder = public / "guides" / "chatgpt-beginner-guide"
    assert folder.joinpath("hero.jpg").stat().st_size <= HERO_MAX_BYTES
    assert folder.joinpath("photo-1.webp").stat().st_size <= PHOTO_MAX_BYTES
    document = json.loads((content / "chatgpt-beginner-guide.json").read_text(encoding="utf-8"))[
        "locales"
    ]["zh-TW"]
    assert document["hero"]["credit"] == {
        "author": "Someone",
        "license": "CC BY-SA 4.0",
        "source_url": "https://commons.wikimedia.org/wiki/File:Desk.jpg",
    }
    photo = next(b for b in document["blocks"] if b.get("src", "").endswith(".webp"))
    assert photo["width"] <= 1200 and photo["credit"]["license"] == "CC BY-SA 4.0"


def test_ingest_writes_nothing_on_a_dry_run_or_a_broken_diagram(tmp_path: Path) -> None:
    workdir, content, public = tmp_path / "work", tmp_path / "content", tmp_path / "public"
    workspace = _write_workspace(workdir)
    report = ingest(
        workdir,
        "chatgpt-beginner-guide",
        content_dir=content,
        public_dir=public,
        renderer=fake_renderer,
        dry_run=True,
    )
    assert report.ok and report.written == []
    assert not content.exists() and not public.exists()

    (workspace / "diagram-1.svg").write_text(GOOD_SVG.replace("06:30", "23:59"), encoding="utf-8")
    report = ingest(
        workdir,
        "chatgpt-beginner-guide",
        content_dir=content,
        public_dir=public,
        renderer=fake_renderer,
    )
    assert [p.code for p in errors(report.problems)] == ["diagram_number_not_in_text"]
    assert not content.exists() and not public.exists()

    (workspace / "diagram-1.svg").write_text(
        GOOD_SVG.replace('font-size="18"', 'font-size="11"'), encoding="utf-8"
    )
    with pytest.raises(PackIngestError, match="below 15 px"):
        ingest(
            workdir,
            "chatgpt-beginner-guide",
            content_dir=content,
            public_dir=public,
            renderer=fake_renderer,
        )


def test_ingest_refuses_a_topic_from_the_other_section(tmp_path: Path) -> None:
    workdir, content, public = tmp_path / "work", tmp_path / "content", tmp_path / "public"
    workspace = _write_workspace(workdir)
    pack = json.loads((workspace / "pack.json").read_text(encoding="utf-8"))
    pack["topics"] = ["ai", "transport"]
    (workspace / "pack.json").write_text(json.dumps(pack, ensure_ascii=False), encoding="utf-8")
    report = ingest(
        workdir,
        "chatgpt-beginner-guide",
        content_dir=content,
        public_dir=public,
        renderer=fake_renderer,
    )
    assert [p.code for p in errors(report.problems)] == ["topic_unknown"]


def test_lint_all_compares_the_packs_with_the_catalogue(tmp_path: Path) -> None:
    workdir, content, public = tmp_path / "work", tmp_path / "content", tmp_path / "public"
    _write_workspace(workdir)
    ingest(
        workdir,
        "chatgpt-beginner-guide",
        content_dir=content,
        public_dir=public,
        renderer=fake_renderer,
    )
    catalogue = tmp_path / "series.md"
    catalogue.write_text(
        "| # | slug | 標題 |\n|---|---|---|\n"
        "| 1 | `ai-tools-2026-overview` | 總覽 |\n"
        "| 2 | `chatgpt-beginner-guide` | 入門 |\n",
        encoding="utf-8",
    )
    assert catalogue_slugs(catalogue.read_text(encoding="utf-8")) == {
        "ai-tools-2026-overview",
        "chatgpt-beginner-guide",
    }
    findings = lint_all(content, public, kind="life", catalogue=catalogue)
    assert not errors(findings["chatgpt-beginner-guide"])
    assert [p.message for p in findings["catalogue"]] == ["ai-tools-2026-overview: not written yet"]

    # A section holds articles outside any one series. Those are not gaps: one line for the
    # record, never a warning per slug, so the real gaps stay visible and ``--warnings`` holds.
    catalogue.write_text(
        "| # | slug | 標題 |\n|---|---|---|\n| 1 | `ai-tools-2026-overview` | 總覽 |\n",
        encoding="utf-8",
    )
    findings = lint_all(content, public, kind="life", catalogue=catalogue)
    assert [(p.level, p.code) for p in findings["catalogue"]] == [
        ("warning", "catalogue_missing_pack"),
        ("info", "packs_outside_catalogue"),
    ]
    assert findings["catalogue"][1].message.startswith(
        "1 life pack(s) are not in this list, which is fine: chatgpt-beginner-guide"
    )


def test_lint_all_counts_sitemap_rows_but_has_no_ceiling_to_warn_about(tmp_path: Path) -> None:
    """The web slices each section and locale into as many numbered child sitemaps as its
    rows need, so the lint reports the count per section and locale for the curious and
    never a budget warning: there is no row a batch could push out of the sitemap."""
    from app.guides import pack_ingest
    from app.guides.content_pack import load_packs

    workdir, content, public = tmp_path / "work", tmp_path / "content", tmp_path / "public"
    _write_workspace(workdir)
    ingest(
        workdir,
        "chatgpt-beginner-guide",
        content_dir=content,
        public_dir=public,
        renderer=fake_renderer,
    )
    assert pack_ingest.sitemap_children(load_packs(content)) == {"life-zh-TW": 1}
    assert "sitemap" not in lint_all(content, public, kind="life")
    assert "sitemap" not in lint_all(content, public, kind="howto")
    assert not hasattr(pack_ingest, "SITEMAP_WARN_ROWS")


# --- the Commons transport ------------------------------------------------------------------


def _redirecting_server(location: str) -> tuple[HTTPServer, str]:
    """A one-shot HTTP server that answers `/start` with a 302 to `location`."""

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802 -- BaseHTTPRequestHandler's own spelling
            if self.path == "/start":
                self.send_response(302)
                self.send_header("Location", location)
                self.end_headers()
                return
            self.send_response(200)
            self.send_header("Content-Length", "2")
            self.end_headers()
            self.wfile.write(b"ok")

        def log_message(self, *_: object) -> None:
            return

    return _serve(Handler)


def _serve(handler: type[BaseHTTPRequestHandler]) -> tuple[HTTPServer, str]:
    server = HTTPServer(("127.0.0.1", 0), handler)
    Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_port}"


def _on_the_wire(value: str) -> str:
    """What `send_header` needs in order to put `value`'s UTF-8 bytes on the wire: it encodes
    its argument as ISO-8859-1, one character per byte."""
    return value.encode("utf-8").decode("latin-1")


@pytest.mark.parametrize("scheme", ["file", "ftp", "data"])
def test_the_commons_transport_refuses_a_url_that_is_not_http(scheme: str) -> None:
    """`urlopen` is not an HTTP client — it opens `file:`, `ftp:` and `data:` too.

    The URL is not always a constant of the module: `fetch_image` passes whatever Commons
    returned as `thumburl`, so the scheme is the vendor's choice unless something refuses it.
    """
    with httpx.Client(transport=UrllibTransport()) as client:
        with pytest.raises(PackIngestError, match="refusing"):
            client.get(f"{scheme}://example.invalid/whatever")


@pytest.mark.parametrize("location", ["file:///etc/hostname", "ftp://example.invalid/x"])
def test_a_redirect_cannot_leave_http(location: str) -> None:
    """The half that is easy to get wrong, and was.

    Left to itself `urlopen` follows redirects internally, so the hop never comes back
    through the transport and the scheme check only ever sees the first URL. urllib's own
    redirect rule allows `ftp:` as well as http and https, so that hop was reachable.
    The transport now hands the 3xx to httpx, which re-enters it for every hop.
    """
    server, base = _redirecting_server(location)
    try:
        with httpx.Client(transport=UrllibTransport(), follow_redirects=True) as client:
            with pytest.raises(PackIngestError, match="refusing"):
                client.get(f"{base}/start")
    finally:
        server.shutdown()


def test_an_ordinary_redirect_is_still_followed() -> None:
    # A guard that breaks the Commons fetch path is not an improvement: thumbnail URLs
    # redirect, and that has to keep working.
    server, base = _redirecting_server("/elsewhere")
    try:
        with httpx.Client(transport=UrllibTransport(), follow_redirects=True) as client:
            assert client.get(f"{base}/start").text == "ok"
    finally:
        server.shutdown()


# 瑞鳳殿 -- the Sendai mausoleum whose best photograph batch 7 could not ingest.
JAPANESE_NAME = "瑞鳳殿.jpg"
JAPANESE_NAME_ENCODED = "%E7%91%9E%E9%B3%B3%E6%AE%BF.jpg"
# The shape the API gave for such a file on 2026-09-19: the name percent-encoded in the path,
# a tracking query string appended, and the rendition wider than the 1600 px asked for.
UTM = "?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content="
THUMB_PATH = (
    f"/wikipedia/commons/thumb/7/72/{JAPANESE_NAME_ENCODED}/1920px-{JAPANESE_NAME_ENCODED}"
    f"{UTM}thumbnail"
)


def _commons_like_server(jpeg: bytes) -> tuple[HTTPServer, str, list[str]]:
    """A server that answers the way Commons does for a Japanese-named file, plus the one
    thing that broke the ingest: a response header carrying the name as raw UTF-8 bytes.

    Today's `thumb.wikimedia.org` names the file percent-encoded (RFC 5987) in
    `Content-Disposition`, which is plain ASCII; which header carried the bytes on the day
    batch 7 hit it is not on record. The quoted-name form of `Content-Disposition` is the
    common way a server puts a file name on the wire unencoded, and any header with a byte
    over 0x7F fails the same way, so that is the one this server sends. `seen` records
    every request path.
    """
    seen: list[str] = []
    picture_headers = {
        "Content-Type": "image/jpeg",
        "Content-Disposition": _on_the_wire(f'inline;filename="{JAPANESE_NAME}"'),
    }

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802 -- BaseHTTPRequestHandler's own spelling
            seen.append(self.path)
            base = f"http://{self.headers['Host']}"
            if self.path.startswith("/w/api.php?"):
                payload = _commons_payload(
                    "CC BY-SA 4.0",
                    url=f"{base}/wikipedia/commons/7/72/{JAPANESE_NAME_ENCODED}{UTM}original",
                    thumburl=f"{base}{THUMB_PATH}",
                    descriptionurl=f"https://commons.wikimedia.org/wiki/File:{JAPANESE_NAME_ENCODED}",
                )
                self._answer(json.dumps(payload).encode(), {"Content-Type": "application/json"})
            elif self.path == THUMB_PATH:
                self._answer(jpeg, picture_headers)
            else:
                self._answer(b"not here", {"Content-Type": "text/plain"}, status=404)

        def _answer(self, body: bytes, headers: dict[str, str], *, status: int = 200) -> None:
            self.send_response(status)
            for name, value in headers.items():
                self.send_header(name, value)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_: object) -> None:
            return

    server, base = _serve(Handler)
    return server, base, seen


def test_a_japanese_file_name_survives_the_metadata_call_and_the_download(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Batch 7's 瑞鳳殿 photograph. The request side was never the problem -- httpx
    percent-encodes the title in the API query and the name in the thumbnail path before
    urllib sees them -- but `http.client` decodes response headers as ISO-8859-1, and handing
    those strings to `httpx.Response` re-encoded them as ASCII: the first header byte over
    0x7F was `UnicodeEncodeError`, and the ingest was over."""
    server, base, seen = _commons_like_server(_jpeg_bytes((64, 48)))
    monkeypatch.setattr(pack_ingest, "COMMONS_API", f"{base}/w/api.php")
    try:
        with commons_client() as client:
            info = commons_file_info(client, f"File:{JAPANESE_NAME}")
            picture = fetch_image(client, info.image_url)
            answer = client.get(info.image_url, headers={"User-Agent": USER_AGENT})
    finally:
        server.shutdown()
    assert info.title == f"File:{JAPANESE_NAME}"
    assert info.image_url == f"{base}{THUMB_PATH}"
    assert info.file_page == f"https://commons.wikimedia.org/wiki/File:{JAPANESE_NAME_ENCODED}"
    assert picture.size == (64, 48)
    # Both hops went out percent-encoded, and the header reads back as the UTF-8 it was.
    assert f"titles=File%3A{JAPANESE_NAME_ENCODED}" in seen[0]
    assert seen[1] == THUMB_PATH
    assert answer.headers["content-disposition"] == f'inline;filename="{JAPANESE_NAME}"'


def test_a_redirect_to_a_non_ascii_location_is_followed() -> None:
    # The 3xx branch builds its Response the same way, so a `Location` carrying raw UTF-8
    # used to fail identically; httpx now reads the bytes as UTF-8 and encodes the next hop.
    server, base = _redirecting_server(_on_the_wire(f"/{JAPANESE_NAME}"))
    try:
        with httpx.Client(transport=UrllibTransport(), follow_redirects=True) as client:
            answer = client.get(f"{base}/start")
    finally:
        server.shutdown()
    assert answer.text == "ok"
    assert answer.url.raw_path == f"/{JAPANESE_NAME_ENCODED}".encode()


def test_ingest_knows_every_topic_the_write_path_accepts() -> None:
    """``ingest`` used to read the parent topics only and refused 805 published packs."""
    from app.guides.pack_ingest import _known_topics
    from app.guides.taxonomy import (
        LIFE_SEED_SUBTOPICS,
        LIFE_SEED_TOPICS,
        SEED_TOPICS,
        TRAVEL_SEED_SUBTOPICS,
    )

    life = _known_topics("life")
    assert life == {slug for slug, _ in LIFE_SEED_TOPICS} | {
        slug for slug, _parent, _labels in LIFE_SEED_SUBTOPICS
    }
    # The pair that exposed it: a sister pack carries ai-plans, a subtopic of ai.
    assert {"ai", "software", "ai-plans", "claude-code", "ai-terms"} <= life
    # Travel gained sub-topics with 0082: the dishes and ``cafe`` under ``food``. A food
    # special carries its dish alone, so a vocabulary of parents only would refuse every one.
    travel = {slug for slug, _ in SEED_TOPICS} | {
        slug for slug, _parent, _labels in TRAVEL_SEED_SUBTOPICS
    }
    for kind in ("howto", "intel"):
        assert _known_topics(kind) == travel  # type: ignore[arg-type]
    assert {"food", "cafe", "kr-dwaeji-gukbap"} <= travel
    # Each section's sub-topics stay its own, as the write path keeps them.
    assert travel.isdisjoint(life)
