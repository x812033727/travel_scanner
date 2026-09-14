"""Linked prose and literal examples survive the actual editorial/publication path."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.guides.admin_service import _ordinary_urls
from app.guides.pack_ingest import _body_length, _document_text
from app.guides.schemas import CodeBlock, GuideDocument, RichParagraphBlock
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
