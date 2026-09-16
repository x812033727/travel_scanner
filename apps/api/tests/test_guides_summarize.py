"""``summarize``: the summary and FAQ blocks a pack gets from its own text or from a
reviewed batch, proven on packs in a temporary directory like ``test_guides_autolink``.
The shipped corpus is only checked for determinism and validity, never for counts."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.guides import summarize
from app.guides.pack_cli import main
from app.guides.schemas import GuideDocument
from app.guides.summarize import (
    SummarizeError,
    faq_from_section,
    lead_summary,
    load_batch,
    numbers_missing,
    proposals,
    render_digest,
    render_table,
    summarize_document,
)
from tests.test_guides_autolink import pack, write


def heading(text: str, level: int = 2) -> dict:
    return {"type": "heading", "text": text, "level": level}


def paragraph(text: str) -> dict:
    return {"type": "paragraph", "text": text}


LEAD = "先講結論：住上野走京成。住新宿走 JR。預算優先搭巴士。"
BODY = [
    paragraph("落地之後第一個決定就是怎麼進市區。"),
    paragraph(LEAD),
    heading("三種選擇"),
    paragraph("Skyliner 最快，票價 2,570 日圓。"),
    heading("怎麼買票"),
    paragraph("IC 卡在車站就買得到。"),
    heading("住哪裡搭什麼"),
    paragraph("依區域選線。"),
]
FAQ_LIST = [
    heading("常見問題"),
    {
        "type": "list",
        "ordered": False,
        "items": [
            "行李很多怎麼辦：搭巴士或定額計程車。",
            "深夜抵達還有車嗎？京急末班車過後只剩計程車。",
        ],
    },
]
FAQ_PAIRS = [
    heading("常見問題"),
    heading("行李很多怎麼辦", 3),
    paragraph("搭巴士或定額計程車。"),
    heading("深夜抵達還有車嗎", 3),
    paragraph("京急末班車過後只剩計程車。"),
]


def document(blocks: list[dict]) -> dict:
    return pack("x", blocks)["locales"]["zh-TW"]


# --- the article's own lead -----------------------------------------------------------


def test_a_lead_paragraph_becomes_the_summary_at_the_top_with_its_marker_stripped() -> None:
    doc = document(BODY)
    rewritten, report = summarize_document(doc)
    assert report.summary == "lead (3)"
    assert rewritten["blocks"][0] == {
        "type": "summary",
        "items": ["住上野走京成。", "住新宿走 JR。", "預算優先搭巴士。"],
    }
    assert rewritten["blocks"][1:] == BODY
    GuideDocument.model_validate(rewritten)


def test_a_lead_is_cut_to_five_sentences_and_a_short_or_long_one_is_no_candidate() -> None:
    seven = "一句話：一。二。三。四。五。六。七。"
    assert lead_summary(document([paragraph(seven)])) == ["一。", "二。", "三。", "四。", "五。"]
    assert lead_summary(document([paragraph("先講結論：只有一句。")])) is None
    assert lead_summary(document([paragraph("結論：" + "長" * 301 + "。第二句。")])) is None
    _, report = summarize_document(document([paragraph("沒有結論段。"), heading("一")]))
    assert report.summary == "no candidate"


# --- the FAQ section ------------------------------------------------------------------


def test_a_faq_list_of_question_answer_pairs_becomes_the_faq_block_and_leaves_the_body() -> None:
    doc = document(BODY + FAQ_LIST)
    rewritten, report = summarize_document(doc)
    assert report.faq == "list→faq (2)"
    assert rewritten["blocks"][-1] == {
        "type": "faq",
        "items": [
            {"question": "行李很多怎麼辦", "answer": "搭巴士或定額計程車。"},
            {"question": "深夜抵達還有車嗎？", "answer": "京急末班車過後只剩計程車。"},
        ],
    }
    assert not any(block == heading("常見問題") for block in rewritten["blocks"])
    GuideDocument.model_validate(rewritten)


def test_question_headings_each_answered_by_one_paragraph_become_the_faq_block() -> None:
    rewritten, report = summarize_document(document(BODY + FAQ_PAIRS))
    assert report.faq == "pairs→faq (2)"
    assert rewritten["blocks"][-1]["items"][0] == {
        "question": "行李很多怎麼辦",
        "answer": "搭巴士或定額計程車。",
    }
    assert sum(1 for block in rewritten["blocks"] if block.get("type") == "heading") == 3


@pytest.mark.parametrize(
    "section",
    [
        [heading("常見問題"), {"type": "list", "ordered": False, "items": ["沒有分隔的一句"]}],
        FAQ_LIST + [paragraph("延伸閱讀請看下一篇。")],
        [heading("常見問題"), {"type": "list", "ordered": False, "items": ["只有一題：答"]}],
        [
            heading("常見問題"),
            heading("問", 3),
            {"type": "rich_paragraph", "inlines": [{"type": "text", "text": "答"}]},
            heading("問二", 3),
            paragraph("答二"),
        ],
        [heading("常見問題"), paragraph("散文式的說明，沒有問答形狀。")],
    ],
)
def test_a_faq_section_the_rules_cannot_read_is_kept_as_it_is(section: list[dict]) -> None:
    doc = document(BODY + section)
    rewritten, report = summarize_document(doc)
    assert report.faq == "kept as section"
    assert rewritten["blocks"][1:] == BODY + section


def test_a_faq_section_is_kept_when_removing_it_would_leave_too_few_sections() -> None:
    doc = document([paragraph(LEAD), heading("一"), heading("二")] + FAQ_LIST)
    assert faq_from_section(doc) is None
    _, report = summarize_document(doc)
    assert report.faq == "kept as section"


def test_an_existing_summary_or_faq_is_kept_unless_replaced() -> None:
    doc = document([{"type": "summary", "items": ["舊一。", "舊二。"]}] + BODY)
    rewritten, report = summarize_document(doc)
    assert report.summary == "has summary" and rewritten["blocks"] == doc["blocks"]
    rewritten, report = summarize_document(doc, replace=True)
    assert report.summary == "lead (3)" and rewritten["blocks"][0]["items"][0] == "住上野走京成。"
    faq = document(BODY + [{"type": "faq", "items": [{"question": "問", "answer": "答"}] * 2}])
    _, report = summarize_document(faq)
    assert report.faq == "has faq"


# --- the reviewed batch ---------------------------------------------------------------


def test_a_batch_applies_per_locale_and_refuses_what_it_cannot_place(tmp_path: Path) -> None:
    item = pack("narita", BODY, kind="howto")
    item["locales"]["en"] = {
        **item["locales"]["zh-TW"],
        "blocks": [paragraph("Take the Skyliner, 2,570 yen.")],
    }
    directory = write(tmp_path / "content", item, pack("other", [paragraph("無。"), heading("一")]))
    batch_file = tmp_path / "batch.json"
    batch_file.write_text(
        json.dumps(
            {
                "narita": {
                    "zh-TW": {
                        "summary": ["京成 Skyliner 最快，票價 2,570 日圓。", "住新宿走 JR。"],
                        "faq": [
                            {"question": "問一", "answer": "答一"},
                            {"question": "問二", "answer": "答二"},
                        ],
                    },
                    "en": {"summary": ["Take the Skyliner.", "It costs 2,570 yen."]},
                }
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    rows = proposals(directory, batch=load_batch(batch_file))
    assert [row.slug for row in rows] == ["narita"]
    assert rows[0].reports["zh-TW"].summary == "batch (2)"
    assert rows[0].reports["zh-TW"].faq == "batch (2)"
    assert rows[0].reports["en"].summary == "batch (2)"
    assert (
        rows[0].documents["zh-TW"]["blocks"][0]["items"][0]
        == "京成 Skyliner 最快，票價 2,570 日圓。"
    )
    assert rows[0].documents["zh-TW"]["blocks"][-1]["type"] == "faq"
    # A number the article does not carry as written refuses the whole batch.
    with pytest.raises(SummarizeError, match="numbers_not_in_text: narita zh-TW: 2570"):
        proposals(directory, batch={"narita": {"zh-TW": {"summary": ["票價 2570 日圓。", "二。"]}}})
    with pytest.raises(SummarizeError, match="no pack named nope"):
        proposals(directory, batch={"nope": {"zh-TW": {"summary": ["一。", "二。"]}}})
    with pytest.raises(SummarizeError, match="narita has no locale ja"):
        proposals(directory, batch={"narita": {"ja": {"summary": ["一。", "二。"]}}})
    # An entry over a summary already there is refused without --replace.
    summarize.apply(rows, directory)
    with pytest.raises(SummarizeError, match="already has a summary"):
        proposals(directory, batch={"narita": {"zh-TW": {"summary": ["一。", "二。"]}}})
    replaced = proposals(
        directory, batch={"narita": {"zh-TW": {"summary": ["新一。", "新二。"]}}}, replace=True
    )
    assert replaced[0].documents["zh-TW"]["blocks"][0]["items"] == ["新一。", "新二。"]


def test_a_batch_entry_is_validated_as_the_block_it_becomes(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"x": {"zh-TW": {"summary": ["只有一句。"]}}}), encoding="utf-8")
    with pytest.raises(SummarizeError, match="x zh-TW"):
        load_batch(bad)
    bad.write_text(
        json.dumps({"x": {"zh-TW": {"summary": ["一。", "長" * 301]}}}), encoding="utf-8"
    )
    with pytest.raises(SummarizeError, match="x zh-TW"):
        load_batch(bad)
    bad.write_text(
        json.dumps({"x": {"zh-TW": {"summary": ["一。", "二。"], "faq": [{"question": "q"}]}}}),
        encoding="utf-8",
    )
    with pytest.raises(SummarizeError, match="x zh-TW"):
        load_batch(bad)
    bad.write_text(json.dumps(["not", "an", "object"]), encoding="utf-8")
    with pytest.raises(SummarizeError, match="expected an object"):
        load_batch(bad)
    assert numbers_missing(document(BODY), ["票價 2,570 日圓", "2570"]) == ["2570"]


# --- the command ----------------------------------------------------------------------


def test_the_command_prints_a_table_writes_only_on_apply_and_is_idempotent(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    directory = write(
        tmp_path / "content",
        pack("lead", BODY + FAQ_LIST, kind="howto"),
        pack("plain", [paragraph("沒有結論段。"), heading("一"), heading("二"), heading("三")]),
    )
    before = {path.name: path.read_text(encoding="utf-8") for path in directory.glob("*.json")}
    assert main(["--content-dir", str(directory), "summarize", "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert "| `lead` | zh-TW | lead (3) | list→faq (2) |" in out
    assert "1 of 2 packs would change: 1 summaries (1 lead, 0 batch), 1 FAQs;" in out
    assert "1 documents without a candidate" in out
    assert "dry run: nothing written" in out
    assert {
        path.name: path.read_text(encoding="utf-8") for path in directory.glob("*.json")
    } == before

    assert main(["--content-dir", str(directory), "summarize", "--kind", "howto", "--apply"]) == 0
    out = capsys.readouterr().out
    assert "wrote" in out and "lead.json" in out
    after = json.loads((directory / "lead.json").read_text(encoding="utf-8"))
    assert after["locales"]["zh-TW"]["blocks"][0]["type"] == "summary"
    assert after["locales"]["zh-TW"]["blocks"][-1]["type"] == "faq"
    assert {key: value for key, value in after.items() if key != "locales"} == {
        key: value for key, value in json.loads(before["lead.json"]).items() if key != "locales"
    }
    assert (directory / "plain.json").read_text(encoding="utf-8") == before["plain.json"]

    assert main(["--content-dir", str(directory), "summarize", "--kind", "howto", "--apply"]) == 0
    assert "0 of 1 packs would change" in capsys.readouterr().out
    assert (
        main(
            ["--content-dir", str(directory), "summarize", "--from", str(tmp_path / "missing.json")]
        )
        == 1
    )


def test_the_digest_says_what_a_summary_is_written_from(tmp_path: Path) -> None:
    blocks = (
        BODY
        + [
            {
                "type": "table",
                "header": ["路線", "時間"],
                "rows": [["Skyliner", "41 分"]],
                "caption": "比較",
            },
        ]
        + FAQ_PAIRS
    )
    directory = write(tmp_path / "content", pack("narita", blocks, kind="howto"))
    digest = render_digest(directory, kind="howto")
    assert "## narita (zh-TW, howto)" in digest
    assert "description: 一句描述。" in digest
    assert "- 三種選擇" in digest and "  - 行李很多怎麼辦" in digest
    assert "- 落地之後第一個決定就是怎麼進市區。" in digest
    assert "- 比較: 路線 | 時間" in digest
    assert "lead: 住上野走京成。 住新宿走 JR。 預算優先搭巴士。" in digest
    assert "faq shape: pairs×2" in digest
    assert (
        main(
            [
                "--content-dir",
                str(directory),
                "summarize",
                "--digest",
                str(tmp_path / "d.md"),
                "--dry-run",
            ]
        )
        == 0
    )
    assert (tmp_path / "d.md").read_text(encoding="utf-8") == digest


def test_the_shipped_corpus_proposes_the_same_thing_twice_and_only_valid_documents() -> None:
    first = proposals()
    second = proposals()
    assert [(row.slug, row.documents) for row in first] == [
        (row.slug, row.documents) for row in second
    ]
    for row in first:
        for rewritten in row.documents.values():
            GuideDocument.model_validate(rewritten)
    table = render_table(first)
    assert "packs would change" in table
