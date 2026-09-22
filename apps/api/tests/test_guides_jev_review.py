"""``pack_cli jev-review``: the advisory checks, proven on packs in a temporary directory.

Nothing here reaches the network. Every call goes through ``httpx.MockTransport``, and the
tests that matter most are the ones about what does *not* happen: no client without a key,
no request over ``--max-calls``, no key in a report, no pack rewritten.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import httpx
import pytest

from app.ai.jev import ChoiceQuestion, JevAuthError, NoulQuestion, estimate_tokens
from app.config import Settings
from app.guides import jev_review
from app.guides.content_pack import ArticlePack, default_directory
from app.guides.jev_review import (
    JevReviewError,
    Proposal,
    editorial_report,
    extract_units,
    overlap_report,
    plan_chunks,
    plan_editorial,
    signals_for,
)
from app.guides.pack_cli import main

SECRET = "jev-secret-key-do-not-print"  # noqa: S105 -- the value the tests hunt for


# --- fixtures -------------------------------------------------------------------------------


def pack(slug: str, blocks: list[dict[str, Any]], *, kind: str = "howto", **extra: Any) -> dict:
    return {
        "slug": slug,
        "kind": kind,
        "destination_id": None if kind == "life" else "seoul",
        "topics": ["ai"] if kind == "life" else ["transport"],
        "valid_until": None,
        "featured": False,
        "display_order": 100,
        **extra,
        "locales": {
            "zh-TW": {
                "title": f"{slug} 標題",
                "description": "一句描述。",
                "blocks": blocks,
                "sources": [
                    {"title": "來源", "url": "https://example.com/", "checked_on": "2026-09-01"}
                ],
            }
        },
    }


def write(directory: Path, *packs: dict) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    for item in packs:
        (directory / f"{item['slug']}.json").write_text(
            json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    return directory


def paragraphs(*texts: str) -> list[dict[str, Any]]:
    return [{"type": "paragraph", "text": text} for text in texts]


def settings(**overrides: Any) -> Settings:
    return Settings(**{"jev_api_key": SECRET, **overrides})


def _choice_answer(question: dict[str, Any]) -> dict[str, Any]:
    options = [key for key in question["criteria"] if key != "none"]
    probabilities = {
        option: round(0.9 / (index + 1), 4) for index, option in enumerate(options)
    }
    probabilities["none"] = 0.05
    return {
        "type": "choice",
        "choice": options[0] if options else "none",
        "confidence": 0.8,
        "probabilities": probabilities,
    }


def transport(
    *,
    noul: float | list[float] = 0.9,
    status: int = 200,
    seen: list[httpx.Request] | None = None,
) -> httpx.AsyncClient:
    """A client that answers every question in the request it is handed.

    A list of nouls is handed out one per noul question, in the order the questions
    arrive, so a test can say what each unit -- or each chunk -- came back with.
    """
    queue = list(noul) if isinstance(noul, list) else []
    default = 0.9 if isinstance(noul, list) else float(noul)

    def handler(request: httpx.Request) -> httpx.Response:
        if seen is not None:
            seen.append(request)
        if status != 200:
            return httpx.Response(status, json={"message": "no"})
        body = json.loads(request.read().decode())
        answers: dict[str, Any] = {}
        for name, question in body["questions"].items():
            if question["type"] == "noul":
                answers[name] = {
                    "type": "noul",
                    "noul": float(queue.pop(0)) if queue else default,
                }
            else:
                answers[name] = _choice_answer(question)
        return httpx.Response(200, json={"answers": answers, "usage": {"input_tokens": 120}})

    return httpx.AsyncClient(transport=httpx.MockTransport(handler))


def document_of(raw: dict) -> Any:
    return ArticlePack.model_validate(raw).locales["zh-TW"]


# --- 1. what a unit is ------------------------------------------------------------------------


def test_units_follow_the_document_and_leave_out_what_cannot_be_judged() -> None:
    raw = pack(
        "units",
        [
            {"type": "summary", "items": ["結論一。", "結論二。"]},
            {"type": "heading", "text": "怎麼去", "level": 2},
            {"type": "paragraph", "text": "從機場搭快線。"},
            {
                "type": "rich_paragraph",
                "inlines": [
                    {"type": "text", "text": "先看"},
                    {"type": "link", "text": "官網", "url": "https://example.com/"},
                ],
            },
            {"type": "list", "items": ["第一項", "第二項"], "ordered": False},
            {"type": "callout", "tone": "tip", "title": "提醒", "text": "帶零錢。"},
            {"type": "code", "language": "bash", "label": "指令", "code": "echo hi"},
            {"type": "link", "text": "外部連結", "url": "https://example.com/"},
            {
                "type": "table",
                "header": ["票種", "價格"],
                "rows": [["單程", "4,150 韓元"]],
                "caption": "票價表",
            },
            {
                "type": "image",
                "src": "/guides/units/map.svg",
                "alt": "路線圖",
                "width": 800,
                "height": 600,
                "caption": "路線示意",
                "description": "교통 정보 4,150원, 43分",
            },
            {
                "type": "faq",
                "items": [
                    {"question": "要多久？", "answer": "約四十三分鐘。"},
                    {"question": "有行李空間嗎？", "answer": "直達車每節有。"},
                ],
            },
        ],
    )
    units = extract_units(document_of(raw))
    kinds = [unit.kind for unit in units]

    assert kinds == [
        "title",
        "description",
        "summary",
        "summary",
        "heading",
        "paragraph",
        "rich_paragraph",
        "list",
        "callout",
        "table.caption",
        "image.caption",
        "faq",
        "faq",
    ]
    assert [unit.unit_id for unit in units[:3]] == ["u001", "u002", "u003"]
    assert [unit.block_index for unit in units[:3]] == [-1, -1, 0]
    texts = "\n".join(unit.text for unit in units)
    assert "echo hi" not in texts, "code is a command, not editorial voice"
    assert "外部連結" not in texts, "a link label is a button"
    assert "4,150 韓元" not in texts, "table cells are fragments; the caption is the unit"
    assert "교통 정보" not in texts, "an image description transcribes a drawing; always flagged"
    assert next(unit for unit in units if unit.kind == "rich_paragraph").text == "先看官網"
    assert next(unit for unit in units if unit.kind == "list").text == "第一項\n第二項"
    assert next(unit for unit in units if unit.kind == "callout").text == "提醒\n帶零錢。"


def test_a_sha_is_the_text_so_a_rewrite_is_visible_and_a_copy_is_not() -> None:
    first = extract_units(document_of(pack("aa", paragraphs("從機場搭快線。"))))
    second = extract_units(document_of(pack("aa", paragraphs("從機場搭快線。"))))
    third = extract_units(document_of(pack("aa", paragraphs("從機場搭巴士。"))))

    assert first[-1].sha == second[-1].sha
    assert first[-1].sha != third[-1].sha
    assert len(first[-1].sha) == 12


# --- 2-3. the question and the answers --------------------------------------------------------


async def test_every_unit_gets_its_own_noul_question_naming_it(tmp_path: Path) -> None:
    directory = write(tmp_path / "content", pack("aa", paragraphs("從機場搭快線。", "票價四千。")))
    seen: list[httpx.Request] = []

    report = await editorial_report(
        settings=settings(), content_dir=directory, client=transport(seen=seen)
    )

    assert len(seen) == 1, "one document is one round trip"
    body = json.loads(seen[0].read().decode())
    questions = body["questions"]
    assert list(questions) == ["u001", "u002", "u003", "u004"]
    assert all(question["type"] == "noul" for question in questions.values())
    assert "u003" in questions["u003"]["instructions"]
    assert set(questions["u003"]["criteria"]) == {"true", "false"}
    assert "null" not in seen[0].read().decode(), "exclude_none keeps an absent field absent"
    assert [unit["id"] for unit in body["state"]["units"]] == ["u001", "u002", "u003", "u004"]
    assert body["state"]["locale"] == "zh-TW"
    assert report["totals"]["answered"] == 4


async def test_a_confident_chinese_answer_is_confirm_until_autopilot_is_on(
    tmp_path: Path,
) -> None:
    directory = write(tmp_path / "content", pack("aa", paragraphs("本文查證的結果。")))

    held = await editorial_report(
        settings=settings(), content_dir=directory, client=transport(noul=[0.97, 0.30, 0.30])
    )
    rows = held["documents"][0]["rows"]
    assert [row["noul"] for row in rows] == [0.97, 0.3, 0.3]
    assert [row["tier"] for row in rows] == ["confirm", "hold", "hold"]
    assert [row["flagged"] for row in rows] == [True, False, False]
    assert held["documents"][0]["flag_rate"] == 0.3333, "one unit of three"
    assert held["documents"][0]["mean_noul"] == round((0.97 + 0.6) / 3, 4)

    acted = await editorial_report(
        settings=settings(jev_cjk_autopilot_enabled=True),
        content_dir=directory,
        client=transport(noul=0.97),
    )
    assert acted["documents"][0]["rows"][0]["tier"] == "act"


# --- 4-7. the things that must not happen -----------------------------------------------------


async def test_a_document_too_big_for_one_call_is_halved_never_dropped(tmp_path: Path) -> None:
    body = "。".join("首爾地鐵的轉乘動線與票價說明在這裡" * 9 for _ in range(1))
    directory = write(tmp_path / "content", pack("big", paragraphs(*([body] * 6))))
    seen: list[httpx.Request] = []

    report = await editorial_report(
        settings=settings(jev_max_state_tokens=1000),
        content_dir=directory,
        client=transport(seen=seen),
    )

    assert len(seen) > 1, "the first ask is refused by size and the batch is split"
    entry = report["documents"][0]
    assert entry["answered"] == entry["units"], "halving must not lose a unit"
    assert report["usage"]["calls"] == len(seen)
    assert not report["errors"]


async def test_a_plan_over_max_calls_is_refused_before_the_first_request(tmp_path: Path) -> None:
    directory = write(
        tmp_path / "content",
        pack("aa", paragraphs("一段。")),
        pack("bb", paragraphs("兩段。")),
        pack("cc", paragraphs("三段。")),
    )
    seen: list[httpx.Request] = []

    with pytest.raises(JevReviewError) as error:
        await editorial_report(
            settings=settings(), content_dir=directory, max_calls=2, client=transport(seen=seen)
        )

    assert seen == [], "the budget is checked before anything is sent"
    assert "--max-calls" in str(error.value)
    assert "narrow" in str(error.value)


async def test_without_a_key_no_client_is_built_and_a_dry_run_still_plans(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    directory = write(tmp_path / "content", pack("aa", paragraphs("一段。", "兩段。")))

    def explode(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("a Jev client must not be built without a key")

    monkeypatch.setattr(jev_review, "jev_client", explode)

    with pytest.raises(JevReviewError) as error:
        await editorial_report(settings=settings(jev_api_key=None), content_dir=directory)
    assert "JEV_API_KEY is not set" in str(error.value)
    assert "nothing was sent" in str(error.value)

    planned = await editorial_report(
        settings=settings(jev_api_key=None), content_dir=directory, dry_run=True
    )
    assert planned["usage"]["calls"] == 0
    assert planned["usage"]["planned_calls"] == 1
    assert planned["usage"]["planned_input_tokens"] > 0
    assert planned["totals"]["units"] == 4, "title, description and two paragraphs"
    assert planned["documents"][0]["rows"][0]["noul"] is None


async def test_the_key_never_reaches_the_report_or_the_console(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    directory = write(tmp_path / "content", pack("aa", paragraphs("一段。")))

    report = await editorial_report(
        settings=settings(), content_dir=directory, client=transport(status=401)
    )
    print(jev_review.render_editorial(report))

    assert report["errors"] == [f"aa: {JevAuthError.__name__}: Jev rejected the API key"]
    assert SECRET not in json.dumps(report, ensure_ascii=False)
    assert SECRET not in capsys.readouterr().out


# --- 8-9. chunking --------------------------------------------------------------------------


def synthetic(count: int, *, width: int = 1) -> list[jev_review.Candidate]:
    return [
        jev_review.Candidate(
            f"a{index:04d}",
            "life",
            "zh-TW",
            "題" * width,
            "敘" * width,
        )
        for index in range(count)
    ]


def test_chunks_stay_under_the_option_cap_and_the_token_cap() -> None:
    proposal = Proposal("p.json", None, "提案標題", "提案描述")
    candidates = synthetic(600)
    candidates[17].title = "提案標題"
    candidates[17].description = "提案描述"
    ranked = jev_review.rank_candidates(proposal, candidates)

    tight = plan_chunks(proposal, ranked, chunk_size=300, max_state_tokens=6_000)
    ceiling = jev_review.STATE_HEADROOM * 6_000

    assert ranked[0].slug == "a0017", "the lexically closest candidate is ranked first"
    assert ranked[0] in tight[0], "and it is in the chunk a spent budget reaches first"
    assert all(len(chunk) <= jev_review.MAX_CHUNK_CANDIDATES for chunk in tight)
    assert all(
        jev_review.chunk_tokens(proposal, chunk) <= ceiling or len(chunk) == 1 for chunk in tight
    )
    assert len(tight) > 1, "6k tokens cannot hold 600 articles"

    seen = [candidate.slug for chunk in tight for candidate in chunk]
    assert len(seen) == len(set(seen)) == 600, "every article is asked about exactly once"

    for chunk in tight:
        question = jev_review.overlap_questions(chunk)["same_article"]
        assert isinstance(question, ChoiceQuestion)
        assert "none" in question.criteria, "a chunk can always answer 'no article matches'"
        assert len(question.criteria) <= 255, "the vendor takes at most 255 options"

    roomy = plan_chunks(proposal, ranked, chunk_size=300, max_state_tokens=32_000)
    assert len(roomy[0]) == jev_review.MAX_CHUNK_CANDIDATES, "254 articles plus none"


def test_the_shipped_catalogue_costs_what_the_plan_measured() -> None:
    """The plan's per-option figures, and the chunk counts they really produce.

    186 and 158 tokens are the option side only -- the criteria entry. The state repeats
    every article as ``{id, title, description}``, so a candidate costs roughly twice that
    per request, and the token ceiling binds before ``--chunk-size 80`` does: the travel
    catalogue plans 4 chunks rather than the 3 the plan's arithmetic predicted, and the
    lifestyle one 17 rather than 12. Nothing is dropped either way; the run costs a cent
    more.
    """
    proposal = Proposal("p.json", None, "首爾機場快線搭乘攻略", "票價、班次與轉乘一次說清楚。")
    production = Settings()
    for kinds, per_option, chunk_size_only, real in (
        (("howto", "intel"), 186, 3, 4),
        (("life",), 158, 12, 17),
    ):
        candidates, _ = jev_review.load_candidates(default_directory(), kinds=kinds)
        options = [estimate_tokens({item.slug: item.option()}) for item in candidates]
        mean_option = sum(options) / len(options)
        assert abs(mean_option - per_option) <= 6, "the corpus still costs what was measured"

        count = len(candidates)
        assert -(-count // 80) == chunk_size_only, "what --chunk-size 80 alone would give"
        chunks = plan_chunks(
            proposal,
            jev_review.rank_candidates(proposal, candidates),
            chunk_size=80,
            max_state_tokens=production.jev_max_state_tokens,
        )
        assert len(chunks) == real, "what the request really costs, both sides counted"
        assert sum(len(chunk) for chunk in chunks) == count


# --- 10-11. overlap ---------------------------------------------------------------------------


def catalogue(tmp_path: Path) -> Path:
    return write(
        tmp_path / "content",
        pack("seoul-arex", paragraphs("機場快線。"), kind="howto"),
        pack("seoul-subway", paragraphs("地鐵。"), kind="howto"),
        pack("busan-bus", paragraphs("釜山巴士。"), kind="intel"),
        pack("taipei-mrt", paragraphs("台北捷運。"), kind="howto"),
    )


async def test_overlap_takes_the_highest_noul_and_re_asks_the_union(tmp_path: Path) -> None:
    directory = catalogue(tmp_path)
    proposal = Proposal("p.json", None, "機場快線攻略", "票價與轉乘。")
    seen: list[httpx.Request] = []

    report = await overlap_report(
        settings=settings(),
        proposal=proposal,
        content_dir=directory,
        chunk_size=2,
        client=transport(noul=[0.4, 0.8, 0.6], seen=seen),
    )

    assert len(seen) == 3, "two chunks and the round that makes them comparable"
    assert [block["noul"] for block in report["chunks"]] == [0.4, 0.8]
    assert report["final_round"]["asked"] is True
    assert report["verdict"]["overlap_noul"] == 0.8, "the maximum over every round"
    assert report["verdict"]["tier"] == "confirm"
    assert report["verdict"]["flagged"] is True
    assert report["verdict"]["comparable"] is True
    assert report["catalogue"]["candidates"] == 4


async def test_without_the_final_round_the_ranking_says_it_is_not_comparable(
    tmp_path: Path,
) -> None:
    directory = catalogue(tmp_path)
    seen: list[httpx.Request] = []

    report = await overlap_report(
        settings=settings(),
        proposal=Proposal("p.json", None, "機場快線攻略", "票價與轉乘。"),
        content_dir=directory,
        chunk_size=2,
        final_round=False,
        client=transport(noul=[0.4, 0.8], seen=seen),
    )

    assert len(seen) == 2
    assert report["final_round"]["asked"] is False
    assert report["verdict"]["overlap_noul"] == 0.8
    assert report["verdict"]["comparable"] is False
    assert report["verdict"]["top"], "a ranking is still offered, with the warning"


async def test_a_draft_is_read_like_a_proposal_and_never_compared_with_itself(
    tmp_path: Path,
) -> None:
    directory = catalogue(tmp_path)
    draft = tmp_path / "draft.json"
    draft.write_text(
        json.dumps(pack("seoul-arex", paragraphs("機場快線。")), ensure_ascii=False),
        encoding="utf-8",
    )
    file_proposal = tmp_path / "p.json"
    file_proposal.write_text(
        json.dumps(
            {"title": "seoul-arex 標題", "description": "一句描述。"}, ensure_ascii=False
        ),
        encoding="utf-8",
    )

    from_draft, kind = jev_review.load_draft(draft)
    from_file = jev_review.load_proposal(file_proposal)

    assert (from_draft.title, from_draft.description) == (from_file.title, from_file.description)
    assert from_draft.slug == "seoul-arex" and from_file.slug is None
    assert jev_review.kinds_for_draft(kind) == ("intel", "howto"), "a how-to sits in travel"

    plan = jev_review.plan_overlap(
        from_draft,
        settings(),
        content_dir=directory,
        kinds=jev_review.kinds_for_draft(kind),
    )
    slugs = {candidate.slug for chunk in plan.chunks for candidate in chunk}
    assert "seoul-arex" not in slugs, "a draft never competes with the pack it came from"
    assert slugs == {"seoul-subway", "busan-bus", "taipei-mrt"}
    assert plan.excluded == ["seoul-arex"]


# --- 12-13. the report and the command --------------------------------------------------------


def digest(directory: Path) -> dict[str, str]:
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(directory.glob("*.json"))
    }


async def test_a_run_carries_the_advisory_header_and_rewrites_nothing(tmp_path: Path) -> None:
    directory = write(tmp_path / "content", pack("aa", paragraphs("一段。")))
    before = digest(directory)

    report = await editorial_report(
        settings=settings(), content_dir=directory, client=transport()
    )

    assert report["advisory"] is True
    assert "Advisory only" in report["notice"]
    assert "JEV_CJK_AUTOPILOT_ENABLED" in report["notice"]
    assert report["thresholds"] == {"act": 0.9, "flag": 0.5, "cjk_autopilot": False}
    assert report["model"] == "jev-1.13.0"
    assert jev_review.render_editorial(report).startswith(jev_review.NOTICE)
    assert jev_review.render_editorial(report).endswith(jev_review.NOTICE)
    assert digest(directory) == before, "an advisory check never writes a pack"


def test_the_command_routes_the_three_checks(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    directory = write(tmp_path / "content", pack("aa", paragraphs("一段。")))
    monkeypatch.setattr("app.guides.pack_cli.get_settings", lambda: settings(jev_api_key=None))
    report = tmp_path / "out.json"

    plan = ["jev-review", "editorial", "--dir", str(directory), "--dry-run"]
    assert main([*plan, "--report", str(report)]) == 0
    written = json.loads(report.read_text(encoding="utf-8"))
    assert written["tool"] == "jev-review editorial"
    assert written["usage"]["calls"] == 0

    proposal = tmp_path / "p.json"
    proposal.write_text(
        json.dumps({"title": "提案", "description": "描述。"}, ensure_ascii=False),
        encoding="utf-8",
    )
    assert (
        main(
            [
                "jev-review",
                "overlap",
                "--dir",
                str(directory),
                "--proposal",
                str(proposal),
                "--dry-run",
            ]
        )
        == 0
    )

    before = tmp_path / "before.json"
    after = tmp_path / "after.json"
    for path in (before, after):
        path.write_text(json.dumps(minimal_report()), encoding="utf-8")
    assert main(["jev-review", "compare", "--before", str(before), "--after", str(after)]) == 0

    with pytest.raises(SystemExit) as exit_code:
        main(["jev-review", "nonsense"])
    assert exit_code.value.code == 2

    assert main(["jev-review", "editorial", "--dir", str(directory)]) == 1
    assert "JEV_API_KEY is not set" in capsys.readouterr().err


# --- 14-15. the baseline and the measurement ---------------------------------------------------


def test_the_regex_signals_are_the_rules_the_readme_states() -> None:
    assert signals_for("本文的做法是這樣。") == ["self_reference"]
    assert signals_for("這篇整理了三條路線。") == ["self_reference"]
    assert signals_for("官方頁沒寫，我們就不標。") == ["sourcing"]
    assert signals_for("這個分類不是我們加的。") == ["sourcing"]
    assert signals_for("官網的 교통 정보 欄寫著地鐵二號線市廳站三號出口步行五分鐘") == (
        ["field_name_ko"]
    )
    assert signals_for("대표메뉴 是招牌菜，這裡指店家自己掛出來的那一道，點了不會錯") == (
        ["field_name_ko"]
    )
    assert signals_for("영업시간 매일 09:00~21:00 연중무휴") == ["hangul_heavy"]
    assert signals_for("從機場搭快線到首爾站約四十三分鐘，單程 4,150 韓元。") == []


def minimal_report(**overrides: Any) -> dict[str, Any]:
    document = {
        "slug": "a",
        "kind": "howto",
        "units": 2,
        "answered": 2,
        "flagged": 1,
        "flag_rate": 0.5,
        "mean_noul": 0.6,
        "regex_hits": 1,
        "calls": 1,
        "errors": [],
        "rows": [
            {
                "unit_id": "u001",
                "block_index": -1,
                "kind": "title",
                "chars": 4,
                "sha": "0" * 12,
                "excerpt": "本文說明",
                "signals": ["self_reference"],
                "noul": 0.9,
                "tier": "confirm",
                "flagged": True,
            },
            {
                "unit_id": "u002",
                "block_index": 0,
                "kind": "paragraph",
                "chars": 5,
                "sha": "1" * 12,
                "excerpt": "從機場搭快線",
                "signals": [],
                "noul": 0.2,
                "tier": "hold",
                "flagged": False,
            },
        ],
    }
    return {"documents": [document], **overrides}


def test_compare_pairs_the_two_runs_and_draws_a_sample(tmp_path: Path) -> None:
    before = tmp_path / "before.json"
    after = tmp_path / "after.json"
    improved = minimal_report()
    improved["documents"][0] = {
        **improved["documents"][0],
        "flagged": 0,
        "flag_rate": 0.0,
        "rows": [
            {**row, "flagged": False, "noul": 0.1}
            for row in improved["documents"][0]["rows"]
        ],
    }
    control = {
        **minimal_report()["documents"][0],
        "slug": "taipei",
        "flagged": 0,
        "flag_rate": 0.0,
    }
    first = minimal_report()
    first["documents"].append(control)
    second = improved
    second["documents"].append(control)
    before.write_text(json.dumps(first, ensure_ascii=False), encoding="utf-8")
    after.write_text(json.dumps(second, ensure_ascii=False), encoding="utf-8")
    sample = tmp_path / "sample.tsv"

    result = jev_review.compare_reports(
        before, after, sample=4, seed=1, out=sample, control=("taipei",)
    )

    subject = result["subject"]
    assert subject["slugs"] == ["a"]
    assert subject["rows"][0]["rate_before"] == 0.5
    assert subject["rows"][0]["rate_after"] == 0.0
    assert subject["rows"][0]["delta"] == -0.5
    assert subject["paired"] == {"wins": 1, "losses": 0, "ties": 0}
    assert subject["residual"] == {"before": 0, "after": 0}
    assert result["control"]["slugs"] == ["taipei"], "the control group is reported apart"

    lines = sample.read_text(encoding="utf-8").splitlines()
    assert lines[0].split("\t") == list(jev_review.SAMPLE_COLUMNS)
    assert len(lines) == 5, "a header and the four rows asked for"
    assert all(line.endswith("\t") for line in lines[1:]), "label is left for a person"

    jev_review.compare_reports(before, after, sample=4, seed=1, out=sample)
    assert sample.read_text(encoding="utf-8").splitlines() == lines, "one seed, one sample"


def test_compare_refuses_something_that_is_not_a_report(tmp_path: Path) -> None:
    junk = tmp_path / "junk.json"
    junk.write_text("{}", encoding="utf-8")
    with pytest.raises(JevReviewError):
        jev_review.compare_reports(junk, junk)


def test_a_missing_locale_is_skipped_rather_than_guessed(tmp_path: Path) -> None:
    raw = pack("aa", paragraphs("一段。"))
    raw["locales"] = {"en": raw["locales"]["zh-TW"]}
    directory = write(tmp_path / "content", raw)

    plan = plan_editorial(directory, locale="zh-TW")

    assert plan.documents == []
    assert plan.skipped == [{"slug": "aa", "reason": "no zh-TW document"}]


def test_an_unreadable_pack_does_not_take_the_directory_with_it(tmp_path: Path) -> None:
    directory = write(tmp_path / "content", pack("good", paragraphs("一段。")))
    (directory / "broken.json").write_text("{not json", encoding="utf-8")

    plan = plan_editorial(directory)
    candidates, skipped = jev_review.load_candidates(directory)

    assert [document.slug for document in plan.documents] == ["good"]
    assert plan.skipped == [{"slug": "broken", "reason": "not readable as a content pack"}]
    assert [candidate.slug for candidate in candidates] == ["good"]
    assert skipped == [{"slug": "broken", "reason": "not readable as a content pack"}]


def test_the_editorial_question_is_the_defect_so_a_high_noul_means_look() -> None:
    question = NoulQuestion(
        instructions=jev_review.EDITORIAL_QUESTION.format(unit_id="u001"),
        criteria=jev_review.EDITORIAL_CRITERIA,
    )
    dumped = question.model_dump(exclude_none=True)

    assert "instead of telling the traveller" in dumped["instructions"]
    assert "本文" in dumped["criteria"]["true"]
    assert "romanisation" in dumped["criteria"]["false"]
    assert set(dumped) == {"type", "instructions", "criteria"}, "no null is serialised"
