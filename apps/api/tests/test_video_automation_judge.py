"""Jev's outline pick and policy verdict: the questions, the answers, the rules and the routes."""

from __future__ import annotations

import hashlib
import json
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import httpx
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.ai.jev import ChoiceAnswer, JevClient, JevError, NoulAnswer
from app.config import Settings
from app.db import get_session
from app.models import VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_automation import admin_api
from app.video_automation import judge as judging
from app.video_automation import settings as service
from app.video_automation.judge import (
    OptionScores,
    OutlineOption,
    OutlinePick,
    PolicyVerdict,
    final_qa_passed,
    outline_pick_passed,
    outline_questions,
    pick_reason,
    publish_package_passed,
    read_outline_answers,
    read_policy_answers,
)
from app.video_speech import admin_api as speech_api
from app.video_speech.checking import CheckUnavailable

OPTIONS = [
    OutlineOption(key="A", title="先算帳", summary="三種方案的成本", hook="你每月多付了多少？"),
    OutlineOption(key="B", title="實作一次", summary="從零設定", hook="五分鐘做完"),
]


def _noul(value: float) -> NoulAnswer:
    return NoulAnswer(type="noul", noul=value)


def _answers(**changes: Any) -> dict[str, Any]:
    answers: dict[str, Any] = {
        "pick": ChoiceAnswer(
            type="choice", choice="B", confidence=0.74, probabilities={"A": 0.26, "B": 0.74}
        ),
        "stance_A": _noul(0.9),
        "demo_A": _noul(0.4),
        "stance_B": _noul(0.81),
        "demo_B": _noul(0.92),
        "advice": _noul(0.05),
    }
    answers.update(changes)
    return answers


def test_an_outline_judgement_asks_one_pick_two_nouls_per_option_and_advice() -> None:
    questions = outline_questions(OPTIONS)
    assert list(questions) == ["pick", "stance_A", "demo_A", "stance_B", "demo_B", "advice"]
    pick = questions["pick"]
    assert pick.type == "choice" and set(pick.criteria) == {"A", "B"}  # type: ignore[union-attr]
    assert "先算帳 | 三種方案的成本 | 你每月多付了多少？" == pick.criteria["A"]  # type: ignore[union-attr]
    assert questions["demo_B"].instructions.startswith("Outline B includes a concrete")
    with pytest.raises(ValueError):
        outline_questions(OPTIONS[:1])
    with pytest.raises(ValueError):
        outline_questions([*OPTIONS, OutlineOption(key="B", title="dup")])
    with pytest.raises(ValueError):
        outline_questions(
            [*OPTIONS, OutlineOption(key="C", title="c"), OutlineOption(key="D", title="d")]
        )


def test_every_noul_the_judge_asks_sends_the_criteria_keys_typesafe_documents() -> None:
    """A noul's criteria are ``true`` / ``false`` (docs.typesafe.ai/primitives/noul); until
    2026-10-04 the judge sent ``yes`` / ``no``."""
    asked = [
        outline_questions(OPTIONS),
        judging.policy_questions(),
        judging.cut_policy_questions(),
        judging.story_policy_questions(),
    ]
    nouls = [
        question.model_dump(exclude_none=True)
        for questions in asked
        for question in questions.values()
        if question.type == "noul"
    ]
    assert len(nouls) == 5 + 4 + 3 + 5
    for noul in nouls:
        assert noul["criteria"] == {
            "true": "the statement holds",
            "false": "the statement does not hold",
        }


def test_the_answers_become_a_pick_with_the_reason_the_owner_reads() -> None:
    pick = read_outline_answers(_answers(), OPTIONS)
    assert pick.choice == "B" and pick.passed
    assert pick.options["B"] == OptionScores(stance=0.81, demo=0.92)
    assert pick.note == "Jev 挑了 B（0.74）：符合立場 0.81、有示範 0.92、建議 0.05，依設定自動核准"
    weak = read_outline_answers(_answers(demo_B=_noul(0.3), advice=_noul(0.5)), OPTIONS)
    assert not weak.passed
    assert weak.note.endswith("沒過關（有示範 0.30 低於 0.6；建議 0.50 高於 0.3）")
    stray = read_outline_answers(
        _answers(pick=ChoiceAnswer(type="choice", choice="Z", confidence=0.5)), OPTIONS
    )
    assert not stray.passed and stray.note == "Jev 挑了 Z，但它不在選項裡"


def test_the_policy_answers_become_a_verdict() -> None:
    passed = read_policy_answers(
        {"stance": _noul(0.8), "demo": _noul(0.7), "advice": _noul(0.1), "sponsored": _noul(0.2)}
    )
    assert passed.passed and passed.note.endswith("業配 0.20，通過")
    sold = read_policy_answers(
        {"stance": _noul(0.8), "demo": _noul(0.7), "advice": _noul(0.1), "sponsored": _noul(0.6)}
    )
    assert not sold.passed and sold.note.endswith("沒過（業配高於 0.3）")


def _pick_payload(**changes: Any) -> dict[str, Any]:
    pick: dict[str, Any] = {
        "choice": "B",
        "probabilities": {"A": 0.26, "B": 0.74},
        "options": {"A": {"stance": 0.9, "demo": 0.4}, "B": {"stance": 0.81, "demo": 0.92}},
        "advice": 0.05,
    }
    pick.update(changes)
    return {"options": [{"key": "A"}, {"key": "B"}], "pick": pick}


def test_the_pick_rule_needs_the_chosen_option_to_clear_the_thresholds() -> None:
    assert outline_pick_passed(_pick_payload())
    assert outline_pick_passed(_pick_payload(advice=0.3))
    assert not outline_pick_passed(_pick_payload(choice="A")), "A shows nothing"
    assert not outline_pick_passed(_pick_payload(advice=0.31))
    assert not outline_pick_passed(_pick_payload(choice="C")), "not one of this review's options"
    assert not outline_pick_passed(_pick_payload(options={"B": {"stance": True, "demo": 0.9}}))
    assert not outline_pick_passed(_pick_payload(options={"B": {"stance": 0.9}}))
    assert not outline_pick_passed({"options": [{"key": "B"}]})
    assert not outline_pick_passed({})
    without_list = _pick_payload()
    del without_list["options"]
    assert outline_pick_passed(without_list)
    assert pick_reason(_pick_payload()).startswith("Jev 挑了 B（0.74）：符合立場 0.81")


def _report(ids: tuple[str, ...], sha: str, **changes: Any) -> dict[str, Any]:
    report: dict[str, Any] = {
        "ok": True,
        "final_sha256": sha,
        "items": [{"id": name, "ok": True, "detail": ""} for name in ids],
    }
    report.update(changes)
    return report


def test_the_final_rule_needs_every_item_to_pass_for_exactly_this_final_cut() -> None:
    sha = "f" * 64
    assert final_qa_passed({"qa": _report(judging.QA_ITEMS, sha)}, sha)
    extra = _report((*judging.QA_ITEMS, "bonus"), sha)
    assert final_qa_passed({"qa": extra}, sha), "an item the server does not know is fine"
    assert not final_qa_passed({"qa": _report(judging.QA_ITEMS[:-1], sha)}, sha), "older tool"
    assert not final_qa_passed({"qa": _report(judging.QA_ITEMS, "0" * 64)}, sha), "another cut"
    assert not final_qa_passed({"qa": _report(judging.QA_ITEMS, sha, ok=False)}, sha)
    failed = _report(judging.QA_ITEMS, sha)
    failed["items"][3]["ok"] = False
    assert not final_qa_passed({"qa": failed}, sha)
    assert judging.failed_items(failed) == ["pace"]
    assert not final_qa_passed({}, sha)
    assert publish_package_passed({"package": _report(judging.PACKAGE_ITEMS, sha)}, sha)
    assert not publish_package_passed({"package": _report(("files",), sha)}, sha)


@pytest.mark.asyncio
async def test_the_switch_and_the_stance_gate_the_pick_and_the_final_switch_gates_the_checks() -> (
    None
):
    sha = "f" * 64
    session = AsyncMock()
    session.scalar = AsyncMock(
        return_value=SimpleNamespace(
            auto_pick_outline=True, channel_stance="1. 先算帳", auto_approve_final=False
        )
    )
    assert await service.auto_picks_outline(session, _pick_payload())
    assert not await service.auto_approves_final(
        session, "final", {"qa": _report(judging.QA_ITEMS, sha)}, sha
    )
    session.scalar = AsyncMock(
        return_value=SimpleNamespace(
            auto_pick_outline=True, channel_stance="  ", auto_approve_final=True
        )
    )
    assert not await service.auto_picks_outline(session, _pick_payload()), "a blank stance"
    assert await service.auto_approves_final(
        session, "final", {"qa": _report(judging.QA_ITEMS, sha)}, sha
    )
    assert await service.auto_approves_final(
        session, "publish", {"package": _report(judging.PACKAGE_ITEMS, sha)}, sha
    )
    assert not await service.auto_approves_final(
        session, "audio", {"qa": _report(judging.QA_ITEMS, sha)}, sha
    )
    session.scalar = AsyncMock(return_value=None)
    assert not await service.auto_picks_outline(session, _pick_payload()), "no row, no stance"
    assert await service.auto_approves_final(
        session, "final", {"qa": _report(judging.QA_ITEMS, sha)}, sha
    ), "no row yet: the default is on"


def _app() -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.tool_router, prefix="/api/v1")

    async def session() -> Any:
        yield AsyncMock()

    app.dependency_overrides[get_session] = session
    return app


def _worker(app: FastAPI) -> None:
    token = VideoToolToken(id=uuid4(), name="worker", token_hash="h", token_prefix="mkv_w")
    app.dependency_overrides[speech_api.video_tool] = lambda: token


def _settings(monkeypatch: pytest.MonkeyPatch, stance: str, pick: bool = True) -> None:
    row = SimpleNamespace(channel_stance=stance, auto_pick_outline=pick, updated_at=None)
    monkeypatch.setattr(service, "settings_row", AsyncMock(return_value=row))
    monkeypatch.setattr(admin_api, "load_runtime_settings", AsyncMock(return_value=Settings()))
    monkeypatch.setattr(admin_api, "get_redis", lambda: object())
    monkeypatch.setattr(admin_api, "enforce_named_rate_limit", AsyncMock())


OUTLINE_BODY = {
    "slug": "ai-agent-permissions",
    "brief": "# 企劃\n目標觀眾：想把 AI 代理放進工作流程的人",
    "options": [option.model_dump() for option in OPTIONS],
}


@pytest.mark.asyncio
async def test_the_outline_route_asks_jev_once_and_returns_the_pick(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _settings(monkeypatch, "1. 先把帳算清楚再花錢")
    pick = read_outline_answers(_answers(), OPTIONS)
    asked = AsyncMock(return_value=pick)
    monkeypatch.setattr(admin_api, "judge_outline", asked)
    app = _app()
    _worker(app)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        picked = await client.post("/api/v1/video/automation/judge/outline", json=OUTLINE_BODY)
        one_option = await client.post(
            "/api/v1/video/automation/judge/outline",
            json={**OUTLINE_BODY, "options": OUTLINE_BODY["options"][:1]},
        )
    assert picked.status_code == 200, picked.text
    body = picked.json()
    assert body["choice"] == "B" and body["passed"] is True
    assert body["options"]["B"] == {"stance": 0.81, "demo": 0.92}
    assert body["note"].startswith("Jev 挑了 B（0.74）")
    assert asked.await_args.args[2] == "1. 先把帳算清楚再花錢"
    assert [option.key for option in asked.await_args.args[4]] == ["A", "B"]
    assert one_option.status_code == 422
    assert asked.await_count == 1


@pytest.mark.asyncio
async def test_the_routes_refuse_without_a_stance_or_the_switch_and_map_jev_failures(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _settings(monkeypatch, "   ")
    asked = AsyncMock(return_value=read_outline_answers(_answers(), OPTIONS))
    monkeypatch.setattr(admin_api, "judge_outline", asked)
    judged = AsyncMock(
        return_value=PolicyVerdict(
            stance=0.9, demo=0.8, advice=0.1, sponsored=0.1, passed=True, note="ok"
        )
    )
    monkeypatch.setattr(admin_api, "judge_policy", judged)
    app = _app()
    _worker(app)
    policy_body = {"slug": "ai-agent-permissions", "script": "旁白全文", "viewpoint": "套用立場：2"}
    url = "/api/v1/video/automation/judge/"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        blank = await client.post(url + "outline", json=OUTLINE_BODY)
        blank_policy = await client.post(url + "policy", json=policy_body)
        _settings(monkeypatch, "1. 先算帳", pick=False)
        off = await client.post(url + "outline", json=OUTLINE_BODY)
        verdict = await client.post(url + "policy", json=policy_body)
        _settings(monkeypatch, "1. 先算帳")
        asked.side_effect = CheckUnavailable(429, "jev_budget_exhausted", "今天用完了")
        spent = await client.post(url + "outline", json=OUTLINE_BODY)
        asked.side_effect = JevError("boom")
        down = await client.post(url + "outline", json=OUTLINE_BODY)
    assert blank.status_code == 409 and blank.json()["code"] == "video_judge_not_enabled"
    assert blank_policy.status_code == 409
    assert off.status_code == 409, "the switch is off"
    assert verdict.status_code == 200 and verdict.json()["passed"] is True
    assert judged.await_args.args[2:] == ("1. 先算帳", "套用立場：2", "旁白全文")
    assert spent.status_code == 429 and spent.json()["code"] == "jev_budget_exhausted"
    assert down.status_code == 502 and down.json()["code"] == "video_judge_upstream_failed"


@pytest.mark.asyncio
async def test_the_judge_routes_need_a_video_tool_token() -> None:
    async with AsyncClient(transport=ASGITransport(app=_app()), base_url="http://t") as client:
        outline = await client.post("/api/v1/video/automation/judge/outline", json=OUTLINE_BODY)
        policy = await client.post(
            "/api/v1/video/automation/judge/policy", json={"slug": "x", "script": "s"}
        )
    assert outline.status_code == 401 and policy.status_code == 401


def _route_jev(
    monkeypatch: pytest.MonkeyPatch, provider: httpx.AsyncClient
) -> tuple[JevClient, AsyncMock]:
    _settings(monkeypatch, "1. 先把帳算清楚再花錢")
    jev = JevClient(
        "private-jev-key", "https://private-jev.invalid", "test-model", 1, client=provider
    )
    consumed = AsyncMock(return_value=True)
    monkeypatch.setattr(judging, "jev_client", lambda settings, client=None: jev)
    monkeypatch.setattr(judging, "consume_jev_call", consumed)
    monkeypatch.setattr(judging, "policy_questions_for", AsyncMock(return_value="tutorial"))
    monkeypatch.setattr(JevClient, "_backoff", AsyncMock())
    return jev, consumed


def _judge_body(route: str) -> dict[str, Any]:
    return (
        OUTLINE_BODY
        if route == "outline"
        else {"slug": "ai-agent-permissions", "script": "private-narration", "viewpoint": "立場：2"}
    )


def _valid_jev_answers(request: httpx.Request) -> httpx.Response:
    questions = json.loads(request.content)["questions"]
    answers = {
        name: (
            {
                "type": "choice",
                "choice": "B",
                "confidence": 0.8,
                "probabilities": {"A": 0.2, "B": 0.8},
            }
            if question["type"] == "choice"
            else {"type": "noul", "noul": 0.1 if name in {"advice", "sponsored"} else 0.9}
        )
        for name, question in questions.items()
    }
    return httpx.Response(200, json={"answers": answers})


@pytest.mark.asyncio
@pytest.mark.parametrize("route", ["outline", "policy"])
@pytest.mark.parametrize("failure", ["read_timeout", "502", "non_json", "connect_then_read"])
async def test_judge_routes_preserve_uncertain_jev_evidence_without_resending(
    monkeypatch: pytest.MonkeyPatch, route: str, failure: str
) -> None:
    sent: list[bytes] = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(request.content)
        if failure == "connect_then_read" and len(sent) == 1:
            raise httpx.ConnectError("not connected", request=request)
        if failure in {"read_timeout", "connect_then_read"}:
            raise httpx.ReadTimeout("private-jev-key https://private-jev.invalid", request=request)
        if failure == "502":
            return httpx.Response(502, json={"error": {"message": "private-jev-key"}})
        return httpx.Response(200, text="private-jev-key non-json answer")

    app = _app()
    _worker(app)

    @app.middleware("http")
    async def identify(request: Any, call_next: Any) -> Any:
        request.state.request_id = "judge-evidence-test"
        return await call_next(request)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as provider:
        jev, consumed = _route_jev(monkeypatch, provider)
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
            response = await client.post(
                f"/api/v1/video/automation/judge/{route}", json=_judge_body(route)
            )
    assert response.status_code == 502
    assert response.headers["content-type"].startswith("application/problem+json")
    body = response.json()
    assert body["code"] == "video_judge_outcome_uncertain" and body["status"] == 502
    assert body["request_id"] == "judge-evidence-test"
    assert body["quota_units_consumed"] == 1 and consumed.await_count == 1
    expected_wires = 2 if failure == "connect_then_read" else 1
    assert len(sent) == jev.wires_sent == expected_wires and jev.application_calls == 1
    assert body["jev_outcome"] == {
        "phase": "response" if failure == "502" else "body" if failure == "non_json" else "send",
        "status": 502 if failure == "502" else 200 if failure == "non_json" else None,
        "wires_sent": expected_wires,
        "request_sha256": hashlib.sha256(sent[-1]).hexdigest(),
    }
    assert all(content == sent[0] for content in sent)
    for secret in (
        "private-jev-key",
        "private-jev.invalid",
        "private-narration",
        str(OUTLINE_BODY["brief"]),
    ):
        assert secret not in response.text


@pytest.mark.asyncio
@pytest.mark.parametrize("route", ["outline", "policy"])
async def test_judge_routes_retry_a_never_connected_wire_without_spending_another_quota(
    monkeypatch: pytest.MonkeyPatch, route: str
) -> None:
    sent: list[bytes] = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(request.content)
        if len(sent) == 1:
            raise httpx.ConnectError("not connected", request=request)
        return _valid_jev_answers(request)

    app = _app()
    _worker(app)
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as provider:
        jev, consumed = _route_jev(monkeypatch, provider)
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
            response = await client.post(
                f"/api/v1/video/automation/judge/{route}", json=_judge_body(route)
            )
    assert response.status_code == 200, response.text
    assert response.json()["passed"] is True
    assert len(sent) == jev.wires_sent == 2 and sent[0] == sent[1]
    assert jev.application_calls == consumed.await_count == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("route", ["outline", "policy"])
@pytest.mark.parametrize("failure", [401, 403, 400, 422, 429, 529, "connect"])
async def test_judge_routes_keep_settled_jev_failures_under_the_existing_contract(
    monkeypatch: pytest.MonkeyPatch, route: str, failure: int | str
) -> None:
    sent: list[bytes] = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(request.content)
        if failure == "connect":
            raise httpx.ConnectError("not connected", request=request)
        assert isinstance(failure, int)
        return httpx.Response(failure, json={"error": {"message": "refused"}})

    app = _app()
    _worker(app)
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as provider:
        jev, consumed = _route_jev(monkeypatch, provider)
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
            response = await client.post(
                f"/api/v1/video/automation/judge/{route}", json=_judge_body(route)
            )
    invalid = failure in {400, 422}
    assert response.status_code == (422 if invalid else 502)
    assert response.json()["code"] == (
        "video_judge_invalid" if invalid else "video_judge_upstream_failed"
    )
    assert "jev_outcome" not in response.json()
    expected_wires = {429: 3, 529: 4, "connect": 2}.get(failure, 1)
    assert len(sent) == jev.wires_sent == expected_wires
    assert jev.application_calls == consumed.await_count == 1


def test_the_pick_the_worker_carries_is_what_the_route_returned() -> None:
    pick = read_outline_answers(_answers(), OPTIONS)
    payload = {"options": [{"key": "A"}, {"key": "B"}], "pick": pick.model_dump()}
    assert outline_pick_passed(payload)
    assert judging.pick_choice(payload) == "B"
    assert isinstance(pick, OutlinePick)


# --- the hands-off rules of a binge series (docs/videos/BINGE.md) ------------------------------


def _doc_verdict(kind: str, **changes: Any) -> dict[str, Any]:
    judge: dict[str, Any] = {
        "verdicts": {key: "有" for key in judging.REQUIRED_VERDICTS[kind]},
        "problems": [],
        "similar_works": [],
        "notes": "",
    }
    judge.update(changes)
    return judge


def test_a_document_passes_only_when_every_verdict_is_there_and_nothing_is_listed() -> None:
    assert judging.series_doc_passed(_doc_verdict("setting"), "setting")
    assert judging.series_doc_passed(_doc_verdict("outline"), "outline")
    weak = _doc_verdict("chapter")
    weak["verdicts"]["hooks"] = "弱"
    assert judging.series_doc_passed(weak, "chapter"), "one weak beat is allowed"
    weak["verdicts"]["alternation"] = "弱"
    assert not judging.series_doc_passed(weak, "chapter"), "two are not"
    missing = _doc_verdict("setting")
    missing["verdicts"]["genre_fit"] = "無"
    assert not judging.series_doc_passed(missing, "setting")
    short = _doc_verdict("setting")
    del short["verdicts"]["cast_playable"]
    assert not judging.series_doc_passed(short, "setting"), "an older checker never passes"
    assert not judging.series_doc_passed(_doc_verdict("setting", problems=["x"]), "setting")
    assert not judging.series_doc_passed(
        _doc_verdict("setting", similar_works=["《某作》的門派名"]), "setting"
    )
    assert not judging.series_doc_passed(_doc_verdict("setting"), "poem"), "an unknown kind"
    assert not judging.series_doc_passed({"verdicts": {"originality": "yes"}}, "setting")
    assert not judging.series_doc_passed(None, "setting")
    note = judging.series_doc_note(_doc_verdict("setting"), True)
    assert note.startswith("查核：originality 有") and note.endswith("依作品設定自動核准")
    failed = judging.series_doc_note(
        _doc_verdict("setting", problems=["反派沒有動機"], similar_works=["某作"]), False
    )
    assert failed.startswith("[auto] 查核沒過：反派沒有動機；與既有作品雷同：某作")
    assert judging.series_doc_problems({"verdicts": {"originality": "無"}}) == ["缺少：originality"]
    assert judging.series_doc_problems(None) == ["the checker gave no verdict"]


def _script_payload(**changes: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "coverage": {
            "hook": "有",
            "conflict": "有",
            "turn": "有",
            "cliffhanger": "有",
            "satisfaction": "有",
        },
        "continuity_problems": [],
        "similar_works": [],
        "retention": {
            "hook_seconds": 5.2,
            "satisfaction": {"count": 2, "first_seconds": 24.0, "positions": [24.0, 150.0]},
            "cliffhanger_last": True,
        },
    }
    payload.update(changes)
    return payload


def test_a_screenplay_passes_on_its_coverage_and_a_retention_genre_on_the_measured_timing() -> None:
    passed = judging.script_check_passed
    assert passed(_script_payload(), retention_required=True)
    assert passed(_script_payload(), retention_required=False)
    weak = _script_payload()
    weak["coverage"]["turn"] = "弱"
    assert passed(weak, retention_required=True)
    weak["coverage"]["hook"] = "弱"
    assert not passed(weak, retention_required=True), "two weak beats"
    gone = _script_payload()
    gone["coverage"]["cliffhanger"] = "無"
    assert not passed(gone, retention_required=False)
    assert not passed(
        _script_payload(continuity_problems=["名字兩種寫法"]), retention_required=False
    )
    assert not passed(_script_payload(similar_works=["某作"]), retention_required=False)
    older = _script_payload()
    del older["similar_works"]
    assert not passed(older, retention_required=False), "an older worker never auto-passes"
    late_hook = _script_payload()
    late_hook["retention"]["hook_seconds"] = 12
    assert not passed(late_hook, retention_required=True)
    assert passed(late_hook, retention_required=False), "the classic series has no timing rule"
    few = _script_payload()
    few["retention"]["satisfaction"]["count"] = 1
    assert not passed(few, retention_required=True)
    late = _script_payload()
    late["retention"]["satisfaction"]["first_seconds"] = 45
    assert not passed(late, retention_required=True)
    summary_after = _script_payload()
    summary_after["retention"]["cliffhanger_last"] = False
    assert not passed(summary_after, retention_required=True)
    flat = _script_payload()
    flat["coverage"]["satisfaction"] = "無"
    assert not passed(flat, retention_required=True)
    assert not passed(_script_payload(retention=None), retention_required=True)
    assert not passed({}, retention_required=False)


def test_a_compilation_s_final_cut_is_held_to_its_own_items() -> None:
    sha = "f" * 64
    report = _report(judging.COMPILATION_QA_ITEMS, sha, kind="compilation")
    assert final_qa_passed({"qa": report}, sha, judging.COMPILATION_QA_ITEMS)
    assert not final_qa_passed({"qa": report}, sha), "the eleven-item rule wants more"
    plain = _report(judging.COMPILATION_QA_ITEMS, sha)
    assert not final_qa_passed({"qa": plain}, sha, judging.COMPILATION_QA_ITEMS), (
        "a report that does not say it is a compilation's is an episode's"
    )
    assert not final_qa_passed(
        {"qa": _report(judging.COMPILATION_QA_ITEMS[:-1], sha, kind="compilation")},
        sha,
        judging.COMPILATION_QA_ITEMS,
    )
    assert judging.retention_required_for("rebirth-revenge")
    assert judging.retention_required_for("custom")
    assert not judging.retention_required_for("xianxia-bonds")
    assert not judging.retention_required_for(None)


def test_a_short_is_held_to_its_own_thirteen_and_a_long_video_s_report_never_passes_it() -> None:
    sha = "f" * 64
    report = _report(judging.SHORTS_QA_ITEMS, sha, kind="shorts", line="lab")
    # The tool's ITEM_IDS (tools/video/shorts/qa.mjs) is pinned to this tuple by its own test;
    # the loop grammar (2026-10-05) is the thirteenth, after the disclosure.
    assert len(judging.SHORTS_QA_ITEMS) == 13
    assert judging.SHORTS_QA_ITEMS[-2:] == ("disclosure", "grammar")
    assert judging.shorts_qa_passed({"qa": report}, sha)
    assert not judging.shorts_qa_passed(
        {"qa": _report(judging.SHORTS_QA_ITEMS[:12], sha, kind="shorts")}, sha
    ), "a report from before the grammar item never approves a Short"
    assert not judging.shorts_qa_passed({"qa": report}, "0" * 64), "another cut"
    assert not judging.shorts_qa_passed(
        {"qa": _report(judging.SHORTS_QA_ITEMS[:-1], sha, kind="shorts")}, sha
    ), "an item is missing"
    failed = _report(judging.SHORTS_QA_ITEMS, sha, kind="shorts")
    failed["items"][5]["ok"] = False
    assert not judging.shorts_qa_passed({"qa": failed}, sha)
    assert judging.failed_items(failed) == ["facts"]
    assert not judging.shorts_qa_passed(
        {"qa": _report(judging.SHORTS_QA_ITEMS, sha)}, sha
    ), "a report that does not say it is a Short's is not one"
    assert not judging.shorts_qa_passed(
        {"qa": _report(judging.QA_ITEMS, sha, kind="shorts")}, sha
    ), "the eleven of a long video are not the thirteen"
    assert not judging.shorts_qa_passed({}, sha)
    # The long video's rules are what they were: a Short's report does not pass them either.
    assert not final_qa_passed({"qa": report}, sha)
    assert final_qa_passed({"qa": _report(judging.QA_ITEMS, sha)}, sha)


def test_a_short_s_upload_package_needs_its_four_items_and_to_say_it_is_a_short_s() -> None:
    sha = "f" * 64
    package = _report(judging.SHORTS_PACKAGE_ITEMS, sha, kind="shorts")
    assert judging.shorts_package_passed({"package": package}, sha)
    assert not judging.shorts_package_passed(
        {"package": _report(judging.SHORTS_PACKAGE_ITEMS, sha)}, sha
    )
    assert not judging.shorts_package_passed(
        {"package": _report(("files", "captions"), sha, kind="shorts")}, sha
    )
    assert not judging.shorts_package_passed({"package": package}, "0" * 64)
