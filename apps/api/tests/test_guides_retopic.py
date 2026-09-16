"""``retopic``: the rule table that files lifestyle packs under the two-level vocabulary.

The rules are data; what the tests hold is the contract around them: a proposal is
deterministic, only ever names lifestyle topics, never removes ``finance``, leaves travel
packs alone, and ``apply`` rewrites one array and nothing else.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.guides import retopic
from app.guides.pack_cli import main
from app.guides.taxonomy import LIFE_SEED_SUBTOPICS, LIFE_SEED_TOPICS, SEED_TOPICS


def pack(slug: str, kind: str = "life", topics: list[str] | None = None) -> dict:
    return {
        "slug": slug,
        "kind": kind,
        "destination_id": "tokyo" if kind != "life" else None,
        "topics": topics if topics is not None else ["ai", "tutorial"],
        "valid_until": None,
        "featured": False,
        "display_order": 100,
        "locales": {
            "zh-TW": {
                "title": f"{slug} 標題",
                "description": "一句描述，說明這篇文章在講什麼與為什麼值得讀。",
                "blocks": [
                    {"type": "heading", "text": "第一節", "level": 2},
                    {"type": "paragraph", "text": "內文。"},
                ],
                "sources": [
                    {
                        "title": "來源",
                        "url": "https://example.com/source",
                        "checked_on": "2026-09-01",
                    }
                ],
            }
        },
    }


@pytest.fixture
def content(tmp_path: Path) -> Path:
    rows = [
        pack("ai-term-quantization"),
        pack("claude-code-getting-started"),
        pack("gemini-cli-getting-started"),
        pack("ai-image-copyright-taiwan", topics=["ai", "misc"]),
        pack("wordpress-first-site", topics=["tutorial", "software"]),
        pack("personal-finance-first-steps", topics=["finance", "tutorial"]),
        pack("weekly-review-reset-routine", topics=["productivity", "daily"]),
        pack("narita-to-tokyo", kind="howto", topics=["transport"]),
        pack("tech-news-usb-c-mandate-20260401", topics=["gadgets"]),
        pack("crypto-news-fsc-vasp-rules-20260501", topics=["finance"]),
    ]
    for row in rows:
        (tmp_path / f"{row['slug']}.json").write_text(
            json.dumps(row, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    return tmp_path


def by_slug(rows: list[retopic.Proposal]) -> dict[str, retopic.Proposal]:
    return {row.slug: row for row in rows}


def test_the_rule_table_only_names_lifestyle_sub_topics_under_their_seeded_parents() -> None:
    subtopics = {slug for slug, _, _ in LIFE_SEED_SUBTOPICS}
    assert {rule.subtopic for rule in retopic.RULES} <= subtopics
    assert set(retopic.SUBTOPIC_PARENT.values()) <= {slug for slug, _ in LIFE_SEED_TOPICS}
    assert retopic.LIFE_VOCABULARY.isdisjoint({slug for slug, _ in SEED_TOPICS})
    # Every series the registry of members knows maps to a seeded sub-topic too.
    assert set(retopic.series_members().values()) <= subtopics


def test_a_slug_earns_its_sub_topic_and_keeps_what_it_had(content: Path) -> None:
    rows = by_slug(retopic.proposals(content))
    assert rows["ai-term-quantization"].proposed == ["ai", "tutorial", "ai-terms"]
    assert rows["ai-term-quantization"].rules == ["prefix:ai-terms"]
    assert rows["claude-code-getting-started"].proposed == ["ai", "tutorial", "claude-code"]
    assert rows["gemini-cli-getting-started"].proposed == ["ai", "tutorial", "gemini-dev"]
    # ``misc`` gives way to a real subject; the original parents are never added by a rule.
    assert rows["ai-image-copyright-taiwan"].proposed == ["ai", "ai-safety"]
    # A child of one of the two new parents brings the parent with it.
    assert rows["wordpress-first-site"].proposed == ["tutorial", "software", "website", "wordpress"]
    assert rows["personal-finance-first-steps"].proposed == [
        "finance",
        "tutorial",
        "finance-basics",
    ]
    # ``tech`` is a new parent, so a tech-news article is given it. ``crypto``'s parent
    # ``finance`` is one of the original eight the rule leaves alone, so it arrives only
    # because the pack already carried it -- the gap ``pack_ingest.FINANCE_TOPICS`` covers
    # by naming ``crypto`` itself.
    assert rows["tech-news-usb-c-mandate-20260401"].proposed == ["gadgets", "tech", "tech-news"]
    assert rows["crypto-news-fsc-vasp-rules-20260501"].proposed == ["finance", "crypto"]


def test_an_article_without_a_rule_and_a_travel_article_are_left_alone(content: Path) -> None:
    rows = by_slug(retopic.proposals(content, kind=None))
    assert not rows["weekly-review-reset-routine"].changed
    assert rows["weekly-review-reset-routine"].rules == []
    assert not rows["narita-to-tokyo"].changed
    assert rows["narita-to-tokyo"].proposed == ["transport"]
    assert "narita-to-tokyo" not in by_slug(retopic.proposals(content))


def test_the_prefix_and_slug_filters_narrow_the_batch(content: Path) -> None:
    assert [
        row.slug for row in retopic.proposals(content, prefixes=("claude-code-", "gemini-"))
    ] == [
        "claude-code-getting-started",
        "gemini-cli-getting-started",
    ]
    assert [row.slug for row in retopic.proposals(content, slugs={"ai-term-quantization"})] == [
        "ai-term-quantization"
    ]


def test_every_shipped_lifestyle_proposal_is_deterministic_and_stays_in_the_vocabulary() -> None:
    first = retopic.proposals()
    second = retopic.proposals()
    assert [(row.slug, row.proposed) for row in first] == [
        (row.slug, row.proposed) for row in second
    ]
    for row in first:
        assert set(row.proposed) <= retopic.LIFE_VOCABULARY, row.slug
        assert ("finance" in row.current) <= ("finance" in row.proposed), row.slug
        assert len(row.proposed) == len(set(row.proposed)), row.slug


def test_a_dry_run_writes_nothing_and_apply_changes_only_the_topics(content: Path, capsys) -> None:
    before = {path.name: path.read_text(encoding="utf-8") for path in content.glob("*.json")}
    assert main(["--content-dir", str(content), "retopic"]) == 0
    printed = capsys.readouterr().out
    assert "| `ai-term-quantization` | ai, tutorial | ai, tutorial, ai-terms |" in printed
    assert "dry run: nothing written" in printed
    assert {
        path.name: path.read_text(encoding="utf-8") for path in content.glob("*.json")
    } == before

    assert main(["--content-dir", str(content), "retopic", "--prefix", "ai-term-", "--apply"]) == 0
    after = {path.name: path.read_text(encoding="utf-8") for path in content.glob("*.json")}
    changed = {name for name in after if after[name] != before[name]}
    assert changed == {"ai-term-quantization.json"}
    old, new = (
        json.loads(before["ai-term-quantization.json"]),
        json.loads(after["ai-term-quantization.json"]),
    )
    assert new.pop("topics") == ["ai", "tutorial", "ai-terms"] and old.pop("topics") == [
        "ai",
        "tutorial",
    ]
    assert old == new
    # Line-oriented: the diff is the one array that moved, so a reviewer can read it.
    assert (
        after["ai-term-quantization.json"].count("\n")
        == before["ai-term-quantization.json"].count("\n") + 1
    )

    # Running it again is a no-op.
    assert main(["--content-dir", str(content), "retopic", "--prefix", "ai-term-", "--apply"]) == 0
    assert "0 of 1 packs would change" in capsys.readouterr().out
    assert {path.name: path.read_text(encoding="utf-8") for path in content.glob("*.json")} == after
