"""The review judge: a model that answers a held news story in the owner's place.

The owner decided on 2026-10-06 that a story waiting in the review queue or the redraft list
is decided by a model they pick: publish it, reject it, send it back to the writer with
directions, or hand it back with reasons. The judge reads what the admin detail page shows
and nothing else, and it answers each hold once.

What keeps it from doing harm is here rather than in its instructions. It acts only while
the scanner, automatic mode, the vertical's auto-publish and its own switch are all on, read
again after the model has answered. A verdict is applied only if the row is still exactly as
the judge found it, so a person who acted meanwhile wins. It never writes a person's decision
(``human_decision``, ``human_reason``, ``human_major_error``) and never closes a story a
person confirmed. A publication goes through the same checks as the publish button, and a
rewrite meets every check of the pipeline again.

``jobs`` runs this and acts on the outcome; this module imports neither it nor the worker.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, Literal, cast
from uuid import UUID, uuid4

from redis.asyncio import Redis
from sqlalchemy import ColumnElement, func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.guides.models import GuideArticleLocale
from app.guides.schemas import GuideDocument
from app.news_automation import ai, duplicates, pipeline, policy
from app.news_automation import service as news_service
from app.news_automation.models import (
    LOCALES,
    NewsAssessment,
    NewsAutomationSettings,
    NewsCandidate,
    NewsEvidence,
    NewsPipelineRun,
    NewsSource,
)
from app.news_automation.schemas import DuplicateJudgement, RedraftJudgement, ReviewJudgement
from app.problems import AppError

logger = logging.getLogger(__name__)

Stage = Literal["zh_draft", "duplicate", "final", "redraft"]
# Review-queue holds (status manual_review) the judge answers, and what each one asks. The
# holds that need work stay with the owner: failed hard checks, changed evidence, and a
# failed check on a story that already has its article.
REVIEW_HOLDS: Mapping[str, Stage] = {
    policy.ZH_DRAFT_READY: "zh_draft",
    duplicates.DUPLICATE_UNCERTAIN: "duplicate",
    policy.JEV_FINAL_HOLD: "final",
    policy.FINAL_EDIT_HOLD: "final",
    policy.READY_TO_PUBLISH: "final",
}
# Stops of the redraft list (status needs_redraft) the judge answers. news_not_eligible is
# left out on purpose: there the writer declined a rewrite the judge itself had ordered.
REDRAFT_HOLDS = frozenset(
    {
        "news_verification_failed",
        "news_claim_source_invalid",
        "news_event_date_invalid",
        "news_locale_review_failed",
    }
)
# Rewrites the judge may order for one story, over its whole life.
MAX_JUDGE_REWRITES = 2
RUN_PREFIX = "judge-"
RUN_STAGES: Mapping[Stage, str] = {
    "zh_draft": "judge-zh-draft",
    "duplicate": "judge-duplicate",
    "final": "judge-final",
    "redraft": "judge-redraft",
}
# Failed calls after which a hold goes back to the owner instead of being tried again.
MAX_JUDGE_FAILURES = 3
# RQ's limit for one judge job; jobs.py takes it from here. On a subscription account the
# one question is the reply and at most its repair round, each bounded by the agent
# client's read timeout of 480 s (run 300 s, queue 120 s, 60 s of margin), and a finished
# article then has its evidence pages fetched again before it is published. A job RQ cuts
# leaves its run marked running and its hold unanswered, so the limit clears all of that.
JOB_TIMEOUT_SECONDS = 1_800
# A judge run still marked running and younger than this may belong to a job that is still
# asking: the job's limit, and a minute for RQ to end a job that overran it.
LIVE_RUN = timedelta(seconds=JOB_TIMEOUT_SECONDS + 60)
MAX_REASONS = 8
MAX_REASON_CHARACTERS = 400
STALE = "news_processing_stale"
# What jobs.cleanup_retention leaves in place of an evidence excerpt after 90 days.
EXPIRED_EXCERPT = "[retention-expired]"
# Why the judge leaves a candidate alone; the backfill CLI reports its pool by these.
Exclusion = Literal[
    "not_held", "has_article", "person_decided", "evidence_expired", "answered", "gate_off"
]
# The stored verdict as judge_decision. "pass" and "revise" send the story back to the
# pipeline, whose claim clears the column anyway, and the column's CHECK has no word for them.
DECISIONS: Mapping[str, str] = {
    "publish": "publish",
    "reject": "reject",
    "manual": "manual",
    "duplicate": "duplicate",
}

# Reasons the code writes for the owner. The model's own reasons follow them on the row.
DECISION_NAMES: Mapping[str, str] = {
    "publish": "發布",
    "reject": "退件",
    "duplicate": "重複新聞",
    "distinct": "不是重複",
    "rewrite": "重寫",
}
NO_VERIFIED_DRAFT = "找不到與查核紀錄相符的繁中草稿，AI 沒有可以判斷的內容，交回給你。"
NO_SAVED_ARTICLE = "這一筆沒有已儲存的五語文章，AI 沒有可以判斷的內容，交回給你。"
REWRITES_SPENT = (
    "AI 已經指示重寫 {used} 次，達到上限 {limit} 次，不再自動重寫。請自己決定重新執行或退件。"
)
CALL_UNUSABLE = "AI 代審沒有完成（{code}）：這類錯誤重試也不會成功，交回給你。"
CALL_KEEPS_FAILING = "AI 代審連續失敗 {count} 次（{code}），交回給你。"
PERSON_CONFIRMED = (
    "AI 的判斷是「{decision}」，但這一筆你已經確認要發布，AI 不會把它結案，交回給你。"
)
FINAL_EDITOR_HELD = (
    "AI 的判斷是發布，但最後編輯擋下這一篇的原因是來源不支持的說法、來源互相矛盾或"
    "內容不適合一般讀者，AI 不能直接發布，交回給你。"
)
NO_DIRECTIONS = "AI 要求重寫，但沒有寫出修改指示，交回給你。"
DIRECTIONS_TOO_LONG = "AI 要求重寫，但加上修改指示後撰稿的輸入會超過上限，交回給你。"
LEGACY_BUNDLE = (
    "AI 判斷這不是重複新聞，但這一筆只存著舊流程的五語稿、還沒有文章，"
    "重新起稿會蓋掉它，交回給你。"
)
LEGACY_REWRITE = (
    "AI 要求重寫，但這一筆只存著舊流程的五語稿、還沒有文章，重新起稿會蓋掉它，交回給你。"
)
CONFIRMED_DRAFT = (
    "AI 判斷這不是重複新聞，但這一筆是你確認過的草稿、還沒有文章，"
    "重新起稿會換掉你確認的內容，交回給你。"
)
EVIDENCE_MOVED = "AI 的判斷是發布，但來源內容在查核之後變動了，請先重新查核來源。"
REFUSED = "AI 的判斷是「{decision}」，但套用前的檢查沒有通過（{code}）：{detail}"


@dataclass(frozen=True)
class JudgeOutcome:
    """What the job does once the judge has looked at a candidate.

    ``nothing``: the story rests where the verdict left it, or the judge did not act.
    ``requeue``: the verdict sent the story back to the pipeline; run the candidate again
    with ``retry_count``. ``retry_later``: there is no verdict yet (every subscription
    account is busy, or the call failed and may work next time); judge this hold again in
    a while. ``hold`` is the error_code that was looked at and ``verdict`` what was recorded,
    each None when it does not apply.
    """

    action: Literal["nothing", "requeue", "retry_later"]
    hold: str | None = None
    retry_count: int | None = None
    verdict: str | None = None


def stage_of(candidate: NewsCandidate) -> Stage | None:
    """Which of the judge's questions this candidate's hold asks, if any."""

    if candidate.status == "manual_review":
        return REVIEW_HOLDS.get(candidate.error_code or "")
    if candidate.status == "needs_redraft" and candidate.error_code in REDRAFT_HOLDS:
        return "redraft"
    return None


def allowed_decisions(stage: Stage, hold: str, *, confirmed: bool) -> list[str]:
    """The decisions the judge may choose from; sent to it and enforced on its reply."""

    options: list[str]
    if stage == "duplicate":
        options = ["distinct", "duplicate", "manual"]
    elif stage == "redraft":
        options = ["rewrite", "reject", "manual"]
    elif hold == policy.FINAL_EDIT_HOLD:
        # The final editor holds only for a claim the evidence does not support, conflicting
        # sources or unsafe content. The judge cannot edit, so it cannot wave that through.
        options = ["reject", "manual"]
    else:
        options = ["publish", "reject", "manual"]
    if confirmed:
        # A person said publish. The judge may agree or hand back, never close the story.
        options = [option for option in options if option not in {"reject", "duplicate"}]
    return options


def legacy_bundle(candidate: NewsCandidate) -> bool:
    """Five stored locales and no article: text from before articles were saved on a failed
    check (#1136), which a new draft would overwrite."""

    return candidate.guide_article_id is None and set(LOCALES) <= set(
        candidate.draft_bundle_json or {}
    )


async def rewrites_used(session: AsyncSession, candidate: NewsCandidate) -> int:
    """Rewrites the judge has ordered for this story, on any evidence."""

    return int(
        await session.scalar(
            select(func.count())
            .select_from(NewsAssessment)
            .where(
                NewsAssessment.candidate_id == candidate.id,
                NewsAssessment.assessment_type == "judge",
                NewsAssessment.verdict == "revise",
            )
        )
        or 0
    )


async def exclusion(session: AsyncSession, candidate: NewsCandidate) -> Exclusion | None:
    """Why the judge leaves this candidate alone, or None when it would judge it."""

    stage = stage_of(candidate)
    if stage is None:
        return "not_held"
    if stage == "redraft":
        # A redraft is for a story that has nothing but its evidence: with an article there
        # is text to fix instead, and a person's decision is theirs.
        if candidate.guide_article_id is not None:
            return "has_article"
        if candidate.human_decision is not None:
            return "person_decided"
    confirmed = candidate.human_decision == "publish"
    if allowed_decisions(stage, candidate.error_code or "", confirmed=confirmed) == ["manual"]:
        # Nothing to decide: the judge cannot publish what the final editor held, and it
        # cannot close a story a person confirmed. A call could only hand it back.
        return "person_decided"
    # Expired excerpts leave nothing to write a redraft from, nothing to read a draft or an
    # article against, and nothing to draft or check from after "not a duplicate".
    expired = await session.scalar(
        select(NewsEvidence.id)
        .where(
            NewsEvidence.candidate_id == candidate.id,
            NewsEvidence.role == "evidence",
            NewsEvidence.excerpt == EXPIRED_EXCERPT,
        )
        .limit(1)
    )
    if expired is not None:
        return "evidence_expired"
    if candidate.judge_hold is not None and candidate.judge_hold == candidate.error_code:
        return "answered"
    if not (await pipeline.current_switches(session, candidate.vertical)).judge:
        return "gate_off"
    return None


async def wanted(session: AsyncSession, candidate: NewsCandidate) -> bool:
    """Whether the judge would act on this candidate now: a hold it answers, not yet
    answered, with all four switches on."""

    return await exclusion(session, candidate) is None


async def fail_interrupted_runs(
    session: AsyncSession, candidate_id: UUID | None = None
) -> list[UUID]:
    """Mark judge runs still ``running`` as stale and return their candidates; no commit.

    The worker calls this for every candidate when it starts, when no judge job can be
    running. A job calls it for its own candidate once ``_being_judged`` has found no other
    job asking about the hold: what is left running then was cut off by the job timeout, or
    belongs to a job that read the story before it last ran and whose answer will be
    dropped. Stale runs do not count toward ``MAX_JUDGE_FAILURES``: nothing says the call
    itself failed. A job whose run is failed here while it is still asking finishes that run
    when it returns (``_Case.close_run``).
    """

    criteria: list[ColumnElement[bool]] = [
        NewsPipelineRun.status == "running",
        NewsPipelineRun.stage.startswith(RUN_PREFIX),
    ]
    if candidate_id is not None:
        criteria.append(NewsPipelineRun.candidate_id == candidate_id)
    now = datetime.now(UTC)
    interrupted: list[UUID] = []
    for run in await session.scalars(select(NewsPipelineRun).where(*criteria)):
        run.status = "failed"
        run.error_code = STALE
        run.error_detail = "The worker stopped before this stage finished."
        run.finished_at = now
        if run.candidate_id not in interrupted:
            interrupted.append(run.candidate_id)
    return interrupted


async def _being_judged(session: AsyncSession, candidate: NewsCandidate) -> bool:
    """Whether another job is asking about this candidate's hold right now.

    A backlog batch, or a retry queued for an earlier hold, can start a second job while the
    first is in its call; asking again would pay for an answer that is then dropped. A run
    counts as that first job's only when it is young and began after the candidate last ran.
    One from before that read a hold the story has since left, so the hold it rests in now
    still has to be asked about.
    """

    criteria: list[ColumnElement[bool]] = [
        NewsPipelineRun.candidate_id == candidate.id,
        NewsPipelineRun.status == "running",
        NewsPipelineRun.stage.startswith(RUN_PREFIX),
        NewsPipelineRun.started_at > datetime.now(UTC) - LIVE_RUN,
    ]
    if candidate.processing_started_at is not None:
        criteria.append(NewsPipelineRun.started_at >= candidate.processing_started_at)
    return (
        await session.scalar(select(NewsPipelineRun.id).where(*criteria).limit(1))
    ) is not None


def _cut(reasons: Iterable[str]) -> list[str]:
    """Reasons as they are stored, and as a rewrite hands them to the writer."""

    kept = [reason.strip()[:MAX_REASON_CHARACTERS] for reason in reasons if reason.strip()]
    return kept[:MAX_REASONS]


@dataclass(frozen=True)
class _Seen:
    """What a verdict is formed on. A person's action or a rerun changes at least one."""

    status: str
    error_code: str | None
    evidence_hash: str | None
    retry_count: int
    human_decision: str | None
    judge_hold: str | None

    @classmethod
    def of(cls, candidate: NewsCandidate) -> _Seen:
        return cls(
            status=candidate.status,
            error_code=candidate.error_code,
            evidence_hash=candidate.evidence_hash,
            retry_count=candidate.retry_count,
            human_decision=candidate.human_decision,
            judge_hold=candidate.judge_hold,
        )


class _Case:
    """One hold in front of the judge: what it looked like, the run, and how it ends.

    Everything read off the candidate that is needed after a rollback is kept here: a
    rollback expires the loaded rows, and an expired attribute cannot be read without a
    query.
    """

    def __init__(
        self,
        session: AsyncSession,
        candidate: NewsCandidate,
        settings: NewsAutomationSettings,
        stage: Stage,
    ) -> None:
        self.session = session
        self.candidate = candidate
        self.candidate_id = candidate.id
        self.vertical = candidate.vertical
        self.stage = stage
        self.hold = cast(str, candidate.error_code)
        self.seen = _Seen.of(candidate)
        self.since = candidate.processing_started_at
        self.allowed = allowed_decisions(
            stage, self.hold, confirmed=candidate.human_decision == "publish"
        )
        self.provider = settings.judge_provider
        self.run_id: UUID | None = None
        self.usage: dict[str, int] = {}
        self.model: str | None = None

    async def standing(self) -> bool:
        """Lock the row and check that the hold is as the judge found it and the judge may
        still act.

        ``refresh`` and not ``get``: on a row this session already holds, ``get`` hands back
        the values it loaded before the model call.
        """

        await self.session.refresh(self.candidate, with_for_update=True)
        if _Seen.of(self.candidate) != self.seen:
            return False
        return (await pipeline.current_switches(self.session, self.vertical)).judge

    def record(self, verdict: str, reasons: list[str], **details: Any) -> NewsAssessment:
        """Add the judge's assessment and mark the hold answered; the caller commits."""

        candidate = self.candidate
        row = NewsAssessment(
            id=uuid4(),
            candidate_id=candidate.id,
            assessment_type="judge",
            verdict=verdict,
            provider=self.provider,
            model=self.model,
            reasons_json=reasons,
            details_json={"stage": self.stage, "hold": self.hold, **details},
            evidence_hash=candidate.evidence_hash,
            prompt_version=candidate.prompt_version,
        )
        self.session.add(row)
        candidate.judge_decision = DECISIONS.get(verdict)
        candidate.judge_hold = self.hold
        news_service.audit(
            self.session,
            None,
            "news_candidate_judged",
            f"news-candidate:{candidate.id}",
            stage=self.stage,
            hold=self.hold,
            verdict=verdict,
            provider=self.provider,
            model=self.model,
        )
        return row

    async def _run(self) -> NewsPipelineRun | None:
        if self.run_id is None:
            return None
        return await self.session.get(NewsPipelineRun, self.run_id)

    async def close_run(self, **metadata: Any) -> None:
        """Finish the run with what the call cost; the caller commits.

        A run this job failed stays failed. One that a later job took for stale while this
        one was still asking (the story ran again meanwhile, or this job outlived its limit)
        is finished like any other.
        """

        run = await self._run()
        if run is None or (run.status != "running" and run.error_code != STALE):
            return
        run.status = "succeeded"
        run.error_code = None
        run.error_detail = None
        run.finished_at = datetime.now(UTC)
        run.model = self.model or run.model
        run.input_tokens = int(self.usage.get("input_tokens", 0))
        run.output_tokens = int(self.usage.get("output_tokens", 0))
        run.metadata_json = metadata

    async def answer(
        self, verdict: str, reasons: Iterable[str], *, requeue: bool = False, **details: Any
    ) -> JudgeOutcome:
        """Record the verdict together with whatever it changed on the row, in one commit."""

        self.record(verdict, _cut(reasons), **details)
        await self.close_run(verdict=verdict, **details)
        await self.session.commit()
        return JudgeOutcome(
            "requeue" if requeue else "nothing",
            hold=self.hold,
            retry_count=self.candidate.retry_count if requeue else None,
            verdict=verdict,
        )

    async def hand_back(self, reasons: Iterable[str], **details: Any) -> JudgeOutcome:
        """Leave the hold with the owner and say why, unless the row moved meanwhile."""

        if not await self.standing():
            return await self.drop()
        return await self.answer("manual", reasons, **details)

    async def drop(self) -> JudgeOutcome:
        """The row is no longer what the judge read, or the judge may no longer act:
        nothing is recorded but that the call ran."""

        await self.session.rollback()
        await self.close_run(dropped=True)
        await self.session.commit()
        return JudgeOutcome("nothing", hold=self.hold)

    async def refused(self, decision: str, reasons: list[str], problem: AppError) -> JudgeOutcome:
        """A check refused what the judge decided: the hold goes back to the owner, answered,
        so the same call is not paid for again."""

        # publish_bundle rolls the session back on most refusals and not on all of them.
        # Either way nothing of the refused verdict may stay, and the lock is taken anew.
        await self.session.rollback()
        if not await self.standing():
            return await self.drop()
        if problem.code == "news_evidence_changed":
            # The pages moved after the article was checked. Hold it for changed evidence, as
            # the publish button does, so the owner is offered the re-check.
            self.candidate.status = "manual_review"
            self.candidate.error_code = "news_evidence_changed"
            self.candidate.error_detail = problem.detail[:4000]
            reason = EVIDENCE_MOVED
        else:
            reason = REFUSED.format(
                decision=DECISION_NAMES.get(decision, decision),
                code=problem.code,
                detail=problem.detail,
            )
        return await self.answer(
            "manual", [reason, *reasons], downgraded_from=decision, failure=problem.code
        )

    async def failed(
        self, error: Exception, decision: str | None = None, reasons: Iterable[str] = ()
    ) -> JudgeOutcome:
        """Record a failure on the run, then try again later or hand the hold back."""

        await self.session.rollback()
        waiting = isinstance(error, AppError) and error.code in pipeline.SUBSCRIPTION_WAITS
        code = (error.code if isinstance(error, AppError) else type(error).__name__)[:64]
        run = await self._run()
        if run is not None:
            run.status = "failed"
            run.error_code = code
            run.error_detail = (error.detail if isinstance(error, AppError) else str(error))[:4000]
            run.finished_at = datetime.now(UTC)
            run.model = self.model or run.model
            run.input_tokens = int(self.usage.get("input_tokens", 0))
            run.output_tokens = int(self.usage.get("output_tokens", 0))
        await self.session.commit()
        logger.warning("news judge for candidate %s failed: %s", self.candidate_id, code)
        later = JudgeOutcome("retry_later", hold=self.hold, retry_count=self.seen.retry_count)
        if waiting:
            # Every subscription account is full or signed out: nothing ran, nothing counts.
            return later
        if isinstance(error, ValueError):
            # A reply that failed validation after its repair round, or an input too large to
            # send, fails the same way next time.
            reason = CALL_UNUSABLE.format(code=code)
        else:
            failures = await self._failures()
            if failures < MAX_JUDGE_FAILURES:
                return later
            reason = CALL_KEEPS_FAILING.format(count=failures, code=code)
        details: dict[str, Any] = {"failure": code}
        if decision is not None:
            details["downgraded_from"] = decision
        return await self.hand_back([reason, *reasons], **details)

    async def _failures(self) -> int:
        """Failed calls for this hold: runs of this stage since the candidate last ran."""

        criteria: list[ColumnElement[bool]] = [
            NewsPipelineRun.candidate_id == self.candidate_id,
            NewsPipelineRun.stage == RUN_STAGES[self.stage],
            NewsPipelineRun.status == "failed",
            or_(
                NewsPipelineRun.error_code.is_(None),
                NewsPipelineRun.error_code.not_in({STALE, *pipeline.SUBSCRIPTION_WAITS}),
            ),
        ]
        if self.since is not None:
            criteria.append(NewsPipelineRun.started_at >= self.since)
        return int(
            await self.session.scalar(
                select(func.count()).select_from(NewsPipelineRun).where(*criteria)
            )
            or 0
        )


async def judge_candidate(
    session: AsyncSession, redis: Redis, environment: Settings, candidate_id: UUID
) -> JudgeOutcome:
    """Put one candidate's hold to the judge and apply what it answers.

    The model is asked without a lock or an open transaction, since a call takes minutes.
    Afterwards the row is locked and compared with what the judge was shown; if anything a
    person or a rerun touches has changed, or a switch is off, the answer is dropped.
    Whatever is recorded is committed together with what it changes on the row.
    """

    # populate_existing: a session that already holds the row would hand it back as loaded.
    candidate = await session.get(NewsCandidate, candidate_id, populate_existing=True)
    if candidate is None:
        raise AppError(404, "news_candidate_not_found", "找不到新聞候選")
    if not await wanted(session, candidate):
        return JudgeOutcome("nothing")
    stage = stage_of(candidate)
    assert stage is not None
    settings = await news_service.settings_row(session)
    case = _Case(session, candidate, settings, stage)
    if await _being_judged(session, candidate):
        # That job has this hold. Its answer, or its retry, is the one that counts.
        return JudgeOutcome("nothing", hold=case.hold)
    await fail_interrupted_runs(session, candidate.id)

    # What can be answered without paying for a call.
    draft: GuideDocument | None = None
    if stage == "zh_draft":
        draft = await news_service.verified_zh_draft(session, candidate)
        if draft is None:
            return await case.hand_back([NO_VERIFIED_DRAFT])
    elif stage == "final" and candidate.guide_article_id is None:
        return await case.hand_back([NO_SAVED_ARTICLE])
    elif stage == "redraft":
        used = await rewrites_used(session, candidate)
        if used >= MAX_JUDGE_REWRITES:
            return await case.hand_back(
                [REWRITES_SPENT.format(used=used, limit=MAX_JUDGE_REWRITES)], capped=True
            )

    try:
        run = await pipeline._start_run(
            session,
            candidate,
            RUN_STAGES[stage],
            provider=settings.judge_provider,
            model=settings.judge_model,
        )
    except IntegrityError:
        # Another judge job started the same attempt at the same moment; it has this hold.
        await session.rollback()
        return JudgeOutcome("nothing", hold=case.hold)
    case.run_id = run.id

    reply: ReviewJudgement | DuplicateJudgement | RedraftJudgement
    try:
        payload, judged = await _payload(case, draft)
        # Building the payload read from the database; the call must not hold that
        # transaction open for minutes.
        await session.commit()
        if stage == "duplicate":
            reply, case.usage, case.model = await ai.judge_duplicate(
                environment, settings, payload
            )
        elif stage == "redraft":
            reply, case.usage, case.model = await ai.judge_redraft(environment, settings, payload)
        else:
            reply, case.usage, case.model = await ai.judge_review(environment, settings, payload)
    except Exception as error:
        return await case.failed(error)

    # The call took minutes. With expire_on_commit off, the session would go on answering
    # from the rows it loaded before it: the evidence, the check records and the saved
    # article would all read as they were. From here on everything is read anew.
    session.expire_all()
    decision: str = reply.decision
    reasons = _cut(reply.reasons)
    try:
        return await _conclude(case, redis, decision, reasons, judged)
    except AppError as refusal:
        return await case.refused(decision, reasons, refusal)
    except Exception as error:
        return await case.failed(error, decision, reasons)


async def _conclude(
    case: _Case, redis: Redis, decision: str, reasons: list[str], judged: dict[str, str]
) -> JudgeOutcome:
    """Under the row lock: hold the reply to the rules, record it and apply it."""

    session, candidate = case.session, case.candidate
    if not await case.standing():
        return await case.drop()
    downgrade = await _downgrade(case, decision, reasons)
    if downgrade is not None:
        return await case.answer("manual", [downgrade, *reasons], downgraded_from=decision)
    if decision == "manual":
        return await case.answer("manual", reasons)
    if decision == "reject":
        # error_code and error_detail stay: they say which hold the story was closed in, and
        # the owner's reopen returns it there.
        candidate.status = "rejected"
        return await case.answer("reject", reasons)
    if decision == "duplicate":
        candidate.status = "duplicate"
        return await case.answer("duplicate", reasons)
    if decision == "distinct":
        # As the "not a duplicate" button: from the article when there is one, otherwise a
        # new draft. The pipeline honours this row instead of asking Jev again.
        if candidate.guide_article_id is not None:
            await news_service._queue_reverify(session, candidate, None)
        else:
            news_service._queue_new_draft(candidate, None)
            if await _rewrite_still_owed(session, candidate):
                # This hold stopped a rewrite before it was drafted. The draft that follows
                # is that rewrite, with its directions.
                candidate.error_code = pipeline.JUDGE_REDRAFT_MARKER
        return await case.answer("pass", reasons, requeue=True)
    if decision == "rewrite":
        _send_back(candidate, pipeline.JUDGE_REDRAFT_MARKER)
        return await case.answer("revise", reasons, requeue=True)
    if decision != "publish":
        # Nothing but an explicit "publish" may reach the two branches below.
        raise ValueError(f"The judge returned a decision this code does not know: {decision}")
    if case.stage == "zh_draft":
        verified = await news_service.verified_zh_draft(session, candidate)
        if verified is None or {"zh-TW": policy.document_fingerprint(verified)} != judged:
            # Not the draft the judge read, or no longer a verified one.
            return await case.drop()
        # The pipeline translates, runs the final editor and Jev's last call, and publishes
        # only if this row is still the judge's newest word when it gets there.
        _send_back(candidate, pipeline.JUDGE_APPROVED_MARKER)
        return await case.answer("publish", reasons, requeue=True)
    return await _publish(case, redis, reasons, judged)


async def _downgrade(case: _Case, decision: str, reasons: list[str]) -> str | None:
    """The code's reason when a rule turns the judge's decision into a hand-back."""

    candidate = case.candidate
    if decision not in case.allowed:
        if decision == "publish":
            return FINAL_EDITOR_HELD
        return PERSON_CONFIRMED.format(decision=DECISION_NAMES.get(decision, decision))
    if decision == "distinct" and candidate.guide_article_id is None:
        # Without an article "not a duplicate" means a new draft, and a new draft writes
        # over whatever text the candidate holds.
        if legacy_bundle(candidate):
            return LEGACY_BUNDLE
        if candidate.human_decision == "publish":
            return CONFIRMED_DRAFT
    if decision == "rewrite":
        if legacy_bundle(candidate):
            return LEGACY_REWRITE
        if not reasons:
            return NO_DIRECTIONS
        # Directions that push the writer's input over its limit would only fail the next
        # run, after the rewrite had been counted.
        evidence = await _evidence(case.session, candidate)
        if ai.draft_input_tokens(candidate, evidence, reasons) > ai.STAGE_MAX_INPUT_TOKENS:
            return DIRECTIONS_TOO_LONG
    return None


async def _rewrite_still_owed(session: AsyncSession, candidate: NewsCandidate) -> bool:
    """Whether this duplicate hold stopped a rewrite the judge had ordered.

    The rewrite's run asks Jev about duplicates before it drafts, and an uncertain answer
    replaces the marker with the duplicate hold. The pipeline writes on that answer that the
    marker was still on the row, which it is until the rewrite reaches an outcome: a draft
    call that never returned, or a draft lost to a pause in a later stage, has not used the
    directions. An outcome, or a rerun the owner asked for, clears the marker first, and
    the answer then says nothing.
    """

    directions = await pipeline.redraft_directions(session, candidate)
    if directions is None:
        return False
    answer = await session.scalar(
        select(NewsAssessment)
        .where(
            NewsAssessment.candidate_id == candidate.id,
            NewsAssessment.assessment_type == "duplicate",
            NewsAssessment.evidence_hash == candidate.evidence_hash,
        )
        .order_by(NewsAssessment.created_at.desc())
        .limit(1)
    )
    return (
        answer is not None
        and answer.verdict == "manual"
        and (answer.details_json or {}).get("interrupted") == pipeline.JUDGE_REDRAFT_MARKER
        and answer.created_at >= directions.created_at
    )


def _send_back(candidate: NewsCandidate, marker: str) -> None:
    """Queue the candidate for the pipeline under a marker that says what the judge asked."""

    candidate.status = "discovered"
    candidate.error_code = marker
    candidate.error_detail = None
    candidate.retry_count += 1


async def _publish(
    case: _Case, redis: Redis, reasons: list[str], judged: dict[str, str]
) -> JudgeOutcome:
    """Publish a finished article the judge approved, through the publish button's checks."""

    session, candidate = case.session, case.candidate
    documents, versions = await news_service.publication_bundle(session, candidate, redis)
    current = {locale: policy.document_fingerprint(item) for locale, item in documents.items()}
    if current != judged:
        # Not the text the judge read: someone edited the article during the call.
        return await case.drop()
    # Fetching the evidence pages again took seconds to minutes. As in the pipeline's judged
    # publication, an owner who turned a switch off meanwhile publishes this article themselves.
    if not (await pipeline.current_switches(session, case.vertical)).judge:
        return await case.drop()
    verdict = case.record("publish", reasons)
    news_service.audit(
        session,
        None,
        "news_candidate_judge_published",
        f"news-candidate:{candidate.id}",
        candidate_id=str(candidate.id),
        article_id=str(candidate.guide_article_id),
        judged_stage="final",
        judge_provider=case.provider,
        judge_model=case.model,
        assessment_id=str(verdict.id),
        prompt_version=candidate.prompt_version,
        evidence_sha256=candidate.evidence_hash,
    )
    await case.close_run(verdict="publish")
    # publish_bundle commits the verdict, the run and the publication together, or rolls all
    # of it back and raises.
    await news_service.publish_news_bundle(
        session,
        candidate,
        None,
        documents,
        versions,
        reason=pipeline.judge_publish_reason(reasons),
        metadata={
            "judge": True,
            "judge_provider": case.provider,
            "judge_model": case.model,
            "judged_stage": "final",
        },
    )
    return JudgeOutcome("nothing", hold=case.hold, verdict="publish")


async def _evidence(session: AsyncSession, candidate: NewsCandidate) -> list[NewsEvidence]:
    """Every evidence row in the order the admin page and the writer see them."""

    return list(
        await session.scalars(
            select(NewsEvidence)
            .where(NewsEvidence.candidate_id == candidate.id)
            .order_by(NewsEvidence.is_first_party.desc(), NewsEvidence.retrieved_at)
        )
    )


async def _records(
    session: AsyncSession,
    candidate: NewsCandidate,
    assessment_type: str,
    *,
    this_attempt: bool = False,
) -> list[NewsAssessment]:
    """A check's records on the current evidence, newest first.

    ``this_attempt`` leaves out what earlier runs of the candidate recorded. The filtering
    on ``details_json`` is done by the callers in Python: the column is ``json``, which has
    no containment operators on PostgreSQL.
    """

    criteria: list[ColumnElement[bool]] = [
        NewsAssessment.candidate_id == candidate.id,
        NewsAssessment.assessment_type == assessment_type,
        NewsAssessment.evidence_hash == candidate.evidence_hash,
    ]
    if this_attempt and candidate.processing_started_at is not None:
        criteria.append(NewsAssessment.created_at >= candidate.processing_started_at)
    return list(
        await session.scalars(
            select(NewsAssessment).where(*criteria).order_by(NewsAssessment.created_at.desc())
        )
    )


def _latest_by_locale(rows: list[NewsAssessment], stage: str) -> dict[str, NewsAssessment]:
    latest: dict[str, NewsAssessment] = {}
    for row in rows:
        if row.locale is not None and (row.details_json or {}).get("stage") == stage:
            latest.setdefault(row.locale, row)
    return latest


def _jev_answer(row: NewsAssessment | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return {
        "tier": (row.details_json or {}).get("tier"),
        "confidence": row.confidence,
        "reasons": row.reasons_json,
    }


async def _payload(
    case: _Case, draft: GuideDocument | None
) -> tuple[dict[str, Any], dict[str, str]]:
    """What the owner would see on the detail page, and the fingerprint of each text the
    judge is asked to approve, by locale: a publish verdict is for exactly that text."""

    session, candidate = case.session, case.candidate
    evidence = await _evidence(session, candidate)
    usable = [row for row in evidence if row.role == "evidence"]
    trusted = policy.trusted_alone_sites(
        await session.scalars(select(NewsSource).where(NewsSource.enabled.is_(True)))
    )
    payload: dict[str, Any] = {
        "today": datetime.now(UTC).date().isoformat(),
        "hold": {"code": case.hold, "detail": candidate.error_detail},
        "candidate": {
            "title": candidate.source_title,
            "url": candidate.canonical_url,
            "vertical": candidate.vertical,
            "event_date": candidate.event_date.isoformat() if candidate.event_date else None,
            "published_at": (
                candidate.source_published_at.isoformat()
                if candidate.source_published_at
                else None
            ),
        },
        "evidence": ai.evidence_payload(evidence),
        "sources": {
            "websites": policy.evidence_site_count(usable),
            "first_party": any(row.is_first_party for row in usable),
            "trusted_alone": any(policy.evidence_site(row.url) in trusted for row in usable),
        },
        "allowed_decisions": case.allowed,
    }
    judged: dict[str, str] = {}
    if case.stage == "zh_draft":
        assert draft is not None
        payload.update(await _draft_review(session, candidate, draft))
        judged = {"zh-TW": policy.document_fingerprint(draft)}
    elif case.stage == "final":
        review, judged = await _article_review(session, candidate, case.hold)
        payload.update(review)
    elif case.stage == "duplicate":
        payload["title"] = candidate.source_title
        payload["known_stories"] = duplicates.closest_titles(
            candidate.source_title, await duplicates.known_titles(session, candidate), limit=10
        )
    else:
        payload.update(await _redraft_review(session, candidate, case.hold, usable))
    return payload, judged


async def _draft_review(
    session: AsyncSession, candidate: NewsCandidate, draft: GuideDocument
) -> dict[str, Any]:
    """The verified Traditional Chinese draft with its claims and its two checks."""

    verifications = await _records(session, candidate, "verification")
    verification = next((row for row in verifications if row.verdict == "pass"), None)
    # Stage one asks Jev about zh-TW alone; a last call on five locales says "final".
    jev = next(
        (
            row
            for row in await _records(session, candidate, "jev")
            if row.locale == "zh-TW" and (row.details_json or {}).get("stage") != "final"
        ),
        None,
    )
    return {
        "claims": candidate.claim_ledger_json,
        "article": policy.for_review(draft),
        "checks": {
            "verification": (
                {"verdict": verification.verdict, "issues": verification.reasons_json}
                if verification is not None
                else None
            ),
            "jev": _jev_answer(jev),
        },
    }


async def _article_review(
    session: AsyncSession, candidate: NewsCandidate, hold: str
) -> tuple[dict[str, Any], dict[str, str]]:
    """The saved five-locale article as it would be published: the Traditional Chinese
    text, the locales a check held, and every locale's check records.

    A record is shown only while it describes the saved text. An article edited and checked
    again keeps the final editor's and Jev's earlier answers on the same evidence, and they
    are about text that is gone. The final editor's record names the text it read. Jev's
    last call does not, so it counts until a later review of that locale is on record: every
    re-check writes one, and the last call is the last thing a run records.
    """

    documents = {
        row.locale: GuideDocument.model_validate(row.draft_json)
        for row in await session.scalars(
            select(GuideArticleLocale).where(
                GuideArticleLocale.article_id == candidate.guide_article_id
            )
        )
    }
    if "zh-TW" not in documents:
        raise ValueError("The saved article has no Traditional Chinese text to judge.")
    # Of all five, not only the ones sent: the judge approves the article, and a locale it
    # was not shown was left out because an earlier check had passed that exact text.
    fingerprints = {
        locale: policy.document_fingerprint(item) for locale, item in documents.items()
    }
    reviews = await _records(session, candidate, "locale_review")
    reviewed: dict[str, datetime] = {}
    for row in reviews:
        if row.locale is not None:
            reviewed.setdefault(row.locale, row.created_at)
    last_call = {
        locale: row
        for locale, row in _latest_by_locale(
            await _records(session, candidate, "jev"), "final"
        ).items()
        if locale not in reviewed or reviewed[locale] <= row.created_at
    }
    edits = {
        locale: row
        for locale, row in _latest_by_locale(reviews, "final_edit").items()
        if (row.details_json or {}).get("document_sha256") == fingerprints.get(locale)
    }
    saved = [locale for locale in LOCALES if locale in documents]
    held: list[str] = []
    if hold == policy.JEV_FINAL_HOLD:
        held = [
            locale
            for locale in saved
            if locale not in last_call
            or (last_call[locale].details_json or {}).get("tier") != "act"
        ]
    elif hold == policy.FINAL_EDIT_HOLD:
        held = [
            locale for locale in saved if locale not in edits or edits[locale].verdict != "pass"
        ]
    lint = candidate.lint_json or {}
    review = {
        "verified_zh_tw": policy.for_review(documents["zh-TW"]),
        "held": {locale: policy.for_review(documents[locale]) for locale in held},
        "checks": {
            locale: {
                "jev": _jev_answer(last_call.get(locale)),
                "final_edit": (
                    {"verdict": edits[locale].verdict, "issues": edits[locale].reasons_json}
                    if locale in edits
                    else None
                ),
                "lint": lint.get(locale, []),
            }
            for locale in saved
        },
    }
    return review, fingerprints


async def _redraft_review(
    session: AsyncSession, candidate: NewsCandidate, hold: str, usable: list[NewsEvidence]
) -> dict[str, Any]:
    """Why the draft was stopped: its claims, this attempt's check records, the facts the
    code can state, and the directions that already failed."""

    revisions = list(
        await session.scalars(
            select(NewsAssessment)
            .where(
                NewsAssessment.candidate_id == candidate.id,
                NewsAssessment.assessment_type == "judge",
                NewsAssessment.verdict == "revise",
            )
            .order_by(NewsAssessment.created_at)
        )
    )
    verifications = await _records(session, candidate, "verification", this_attempt=True)
    checks: dict[str, Any] = {
        "verification": [
            {
                "round": (row.details_json or {}).get("round"),
                "verdict": row.verdict,
                "issues": row.reasons_json,
            }
            for row in reversed(verifications)
        ]
    }
    review: dict[str, Any] = {
        "stop": {"code": hold, "detail": candidate.error_detail},
        "rewrites_used": len(revisions),
        "rewrites_limit": MAX_JUDGE_REWRITES,
        "earlier_directions": [reason for row in revisions for reason in row.reasons_json],
        "claims": candidate.claim_ledger_json,
        "checks": checks,
    }
    if hold == "news_locale_review_failed":
        review.update(await _failed_translation(session, candidate, checks))
    elif hold == "news_claim_source_invalid":
        allowed = [row.url for row in usable]
        cited = {
            str(url)
            for claim in candidate.claim_ledger_json or []
            for url in claim.get("source_urls") or []
        }
        review["facts"] = {
            "cited_urls_not_evidence": sorted(cited - set(allowed)),
            "allowed_urls": allowed,
        }
    elif hold == "news_event_date_invalid":
        dates = [row.source_date or row.retrieved_at.date() for row in usable]
        review["facts"] = {
            "event_date": candidate.event_date.isoformat() if candidate.event_date else None,
            "slug": await _drafted_slug(session, candidate),
            "today": datetime.now(UTC).date().isoformat(),
            "newest_evidence_date": max(dates).isoformat() if dates else None,
        }
    return review


async def _failed_translation(
    session: AsyncSession, candidate: NewsCandidate, checks: dict[str, Any]
) -> dict[str, Any]:
    """The translation a reviewer held, with the source it was checked against.

    Only this stop reads ``draft_bundle_json``: stage two put both texts there in this
    attempt. After one of the three stage-one stops it can still hold an older draft.
    """

    failed = next(
        (
            row
            for row in await _records(session, candidate, "locale_review", this_attempt=True)
            if row.verdict == "manual" and (row.details_json or {}).get("stage") != "final_edit"
        ),
        None,
    )
    if failed is None or failed.locale is None:
        return {}
    discarded = (failed.details_json or {}).get("discarded_correction") or {}
    checks["locale_review"] = {
        "locale": failed.locale,
        "verdict": failed.verdict,
        "issues": failed.reasons_json,
        # The reviewer's own correction did not pass either; what it said about that one.
        "discarded_correction_issues": discarded.get("issues") or [],
    }
    texts: dict[str, Any] = {}
    source = await news_service.verified_zh_draft(session, candidate)
    if source is not None:
        texts["verified_zh_tw"] = policy.for_review(source)
    stored = (candidate.draft_bundle_json or {}).get(failed.locale)
    if stored:
        texts["held"] = {failed.locale: policy.for_review(GuideDocument.model_validate(stored))}
    return texts


async def _drafted_slug(session: AsyncSession, candidate: NewsCandidate) -> str | None:
    """The address the writer gave the stopped draft, from its run, when it is on record."""

    metadata = await session.scalar(
        select(NewsPipelineRun.metadata_json)
        .where(
            NewsPipelineRun.candidate_id == candidate.id,
            NewsPipelineRun.stage == "draft",
            NewsPipelineRun.status == "succeeded",
        )
        .order_by(NewsPipelineRun.started_at.desc())
        .limit(1)
    )
    slug = metadata.get("slug") if isinstance(metadata, dict) else None
    return slug if isinstance(slug, str) and slug else None
