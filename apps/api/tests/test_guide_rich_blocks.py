"""Linked prose and literal examples survive the actual editorial/publication path."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.guides.admin_service import _ordinary_urls
from app.guides.pack_ingest import _body_length, _document_text, missing_diagram_numbers
from app.guides.schemas import CodeBlock, GuideDocument, ImageBlock, RichParagraphBlock
from tests import test_guides as guides

database = guides.database
actor = guides.actor


def rich(url: str = "https://mokaair.com/zh-TW/life/gemini-cli-gemini-md") -> dict:
    return {
        "type": "rich_paragraph",
        "inlines": [
            {"type": "text", "text": "Read "},
            {"type": "link", "text": "GEMINI.md", "url": url},
            {"type": "text", "text": " before editing."},
        ],
    }


def test_rich_paragraph_preserves_spaces_and_is_counted() -> None:
    doc = GuideDocument(title="教學", description="設定", blocks=[rich()])
    assert _document_text(doc).endswith("Read GEMINI.md before editing.")
    assert _body_length(doc) == len("ReadGEMINI.mdbeforeediting.")
    assert list(_ordinary_urls(doc)) == [rich()["inlines"][1]["url"]]


def test_document_text_carries_the_summary_and_the_faq() -> None:
    """The summary and the FAQ are sections a reader reads, so the two rules built on
    ``_document_text`` -- the diagram-number rule and the simplified-character scan the news
    batches run -- have to see them. They were added to ``_body_parts`` when the blocks landed
    but not here, which made a figure stated only in the summary read as one the article never
    carried, and a simplified character in an answer read as clean."""
    doc = GuideDocument.model_validate(
        {
            "title": "標題",
            "description": "描述",
            "blocks": [
                {"type": "summary", "items": ["頻寬最高 170GB/s。", "官方未說明售價。"]},
                {"type": "paragraph", "text": "內文。"},
                {"type": "heading", "text": "小節", "level": 2},
                {
                    "type": "faq",
                    "items": [
                        {"question": "台灣買得到嗎？", "answer": "官方未列出地區。"},
                        {"question": "記憶體上限多少？", "answer": "最高 512GB。"},
                    ],
                },
            ],
        }
    )
    text = _document_text(doc)
    for part in ("170GB/s", "官方未說明售價。", "台灣買得到嗎？", "最高 512GB。"):
        assert part in text, part
    # The diagram rule compares against this text, so a figure only the summary states counts,
    # and so does one only an answer states.
    def diagram(label: str) -> str:
        return (
            "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1600 900'>"
            f"<text x='40' y='80' font-size='48'>{label}</text></svg>"
        )

    assert missing_diagram_numbers(diagram("170GB/s"), doc) == []
    assert missing_diagram_numbers(diagram("512GB"), doc) == []
    assert missing_diagram_numbers(diagram("999GB"), doc) == ["999"]


def test_document_text_never_fuses_a_question_into_its_answer() -> None:
    """The FAQ's question and answer go in as separate parts. Joining them would splice the
    digits either side of the seam into a number the article never states, and this rule's whole
    job is to catch a figure the article never states."""
    doc = GuideDocument.model_validate(
        {
            "title": "標題",
            "description": "描述",
            "blocks": [
                {"type": "paragraph", "text": "內文。"},
                {"type": "heading", "text": "小節", "level": 2},
                {
                    "type": "faq",
                    "items": [
                        {"question": "記憶體上限是 5", "answer": "12GB 起跳。"},
                        {"question": "還有別的嗎？", "answer": "官方未說明。"},
                    ],
                },
            ],
        }
    )
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1600 900'>"
        "<text x='40' y='80' font-size='48'>512</text></svg>"
    )
    # Fused, the seam reads "…上限是 512GB 起跳。" and 512 would count as stated.
    assert missing_diagram_numbers(svg, doc) == ["512"]


@pytest.mark.parametrize(
    "url", ["javascript:alert(1)", "//evil.test", "https://a:b@evil.test", "data:text/html,x"]
)
def test_inline_links_reject_unsafe_urls(url: str) -> None:
    with pytest.raises(ValidationError):
        RichParagraphBlock.model_validate(rich(url))


def test_code_preserves_tabs_and_displays_html_as_literal_text() -> None:
    code = 'if ok:\r\n\tprint("<script>not executable</script>")\r\n'
    assert CodeBlock(type="code", label="example", code=code).code == code.replace("\r\n", "\n")
    for invalid in [" ", "hello\x1b[0m", "x" * 24001]:
        with pytest.raises(ValidationError):
            CodeBlock(type="code", label="example", code=invalid)


async def test_editor_save_publish_read_new_blocks(database, actor) -> None:
    blocks = [
        rich(),
        {
            "type": "code",
            "language": "python",
            "label": "demo.py",
            "code": "if True:\n\tprint('ok')\n",
        },
    ]
    async with guides.client(guides.make_app(database, actor)) as api:
        created = await api.post(
            "/admin/guides",
            json={
                "slug": "linked-tutorial",
                "kind": "life",
                "locale": "zh-TW",
                "topics": ["ai"],
                "document": {**guides.document(), "blocks": blocks},
            },
        )
        assert created.status_code == 201, created.text
        row = created.json()
        published = await guides.publish(api, row["id"], "zh-TW", row["locales"][0]["version"])
        assert published.status_code == 200, published.text
        public = await api.get("/guides/life/linked-tutorial", params={"locale": "zh-TW"})
        assert public.status_code == 200
        assert public.json()["document"]["blocks"] == blocks
        detail = await api.get(f"/admin/guides/{row['id']}", params={"locale": "zh-TW"})
        assert detail.status_code == 200
        locale_version = next(
            item["version"] for item in detail.json()["locales"] if item["locale"] == "zh-TW"
        )
        saved = await api.put(
            f"/admin/guides/{row['id']}/zh-TW/draft",
            json={"expected_version": locale_version, "document": detail.json()["draft"]},
        )
        assert saved.status_code == 200, saved.text
        assert saved.json()["draft"]["blocks"] == blocks


async def test_inline_link_cannot_bypass_affiliate_validation(database, actor) -> None:
    async with guides.client(guides.make_app(database, actor)) as api:
        response = await api.post(
            "/admin/guides",
            json={
                "slug": "tracked-inline",
                "kind": "life",
                "locale": "zh-TW",
                "topics": ["ai"],
                "document": {
                    **guides.document(),
                    "blocks": [rich("https://example.com/?aff_id=123")],
                },
            },
        )
        assert response.status_code == 422, response.text
        assert response.json()["code"] == "content_link_affiliate"


def test_image_description_is_optional_plain_text() -> None:
    """A diagram's ``<desc>`` lifted into the block: absent for a photograph, stripped and kept
    free of HTML and control bytes like every other text field, and capped at a paragraph's
    length. Every pack written before the field existed validates unchanged."""
    base = {
        "type": "image",
        "src": "/guides/korea-ktx-srt-ticket-guide/diagram-1.svg",
        "alt": "路線圖",
        "width": 1600,
        "height": 900,
    }
    assert ImageBlock.model_validate(base).description == ""
    lifted = ImageBlock.model_validate(
        {**base, "description": " 一般室 52,200 韓元，最快 2 小時 11 分。\r\n"}
    )
    assert lifted.description == "一般室 52,200 韓元，最快 2 小時 11 分。"
    for refused in ("<b>52,200</b>", "x" * 4001, "a\x07b"):
        with pytest.raises(ValidationError):
            ImageBlock.model_validate({**base, "description": refused})
