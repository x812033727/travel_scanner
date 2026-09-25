from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from typing import Any, Literal, cast
from uuid import UUID, uuid4

from redis.asyncio import Redis
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.guides.models import (
    GuideArticle,
    GuideArticleLocale,
    GuideArticleRevision,
    GuideArticleTopic,
    GuideTopic,
)
from app.guides.schemas import GuideDocument, SourceRef
from app.i18n import Locale
from app.models import User
from app.news_automation import ai
from app.news_automation import service as news_service
from app.news_automation.assets import ensure_assets
from app.news_automation.duplicates import (
    DUPLICATE_UNCERTAIN,
    cleared_by_editor,
    known_titles,
)
from app.news_automation.models import (
    LOCALES,
    NewsAssessment,
    NewsAutomationSettings,
    NewsCandidate,
    NewsEvidence,
    NewsPipelineRun,
)
from app.news_automation.policy import (
    READY_TO_PUBLISH,
    ZH_DRAFT_READY,
    document_fingerprint,
    event_date_problems,
    evidence_fingerprint,
    evidence_present,
    evidence_site_count,
    evidence_sufficient,
    hard_policy_problems,
)
from app.news_automation.schemas import Vertical
from app.news_automation.service import audit, gate_for, settings_row
from app.problems import AppError
from app.site_pages.schemas import LinkBlock

ACTIVE_STATUSES = ("drafting", "verifying", "locale_review", "jev_review")
# Set by an administrator's re-verify. It stays on the candidate until the run reaches an
# outcome, so a rerun after a crash or a stalled worker re-verifies the edited drafts
# instead of drafting new ones over them.
REVERIFY_MARKER = "news_reverify_requested"
ClaimOutcome = Literal["claimed", "disabled", "skipped", "deferred"]
# RQ kills a candidate job after 60 minutes; nothing legitimate is still in flight after 70.
STALE_AFTER = timedelta(minutes=70)
STALE_RECOVERY_STAGE = "stale-recovery"
MAX_AUTOMATIC_RECOVERIES = 2
# A discovered candidate this old with the switch on was never picked up: the switch was
# off when its job ran, or the enqueue after the scan failed.
ORPHAN_AFTER = timedelta(hours=2)
TOPIC_BY_VERTICAL = {"ai": "ai-news", "tech": "tech-news", "crypto": "crypto"}
TARGET_LOCALES: tuple[Locale, ...] = ("zh-CN", "en", "ja", "ko")
TOPIC_LINK_TEXT: dict[Locale, str] = {
    "zh-TW": "查看同分類最新消息",
    "zh-CN": "查看同分类最新消息",
    "en": "Browse the latest news in this topic",
    "ja": "このトピックの最新ニュースを見る",
    "ko": "이 주제의 최신 뉴스 보기",
}


async def _start_run(
    session: AsyncSession,
    candidate: NewsCandidate,
    stage: str,
    *,
    provider: str | None = None,
    model: str | None = None,
) -> NewsPipelineRun:
    attempt = (
        int(
            await session.scalar(
                select(func.count())
                .select_from(NewsPipelineRun)
                .where(
                    NewsPipelineRun.candidate_id == candidate.id,
                    NewsPipelineRun.stage == stage,
                )
            )
            or 0
        )
        + 1
    )
    run = NewsPipelineRun(
        candidate_id=candidate.id,
        stage=stage,
        attempt=attempt,
        idempotency_key=f"{candidate.id}:{stage}:{attempt}",
        provider=provider,
        model=model,
    )
    session.add(run)
    await session.commit()
    return run


async def _finish_run(
    session: AsyncSession,
    run: NewsPipelineRun,
    *,
    usage: dict[str, int] | None = None,
    model: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> None:
    run.status = "succeeded"
    run.finished_at = datetime.now(UTC)
    run.model = model or run.model
    run.input_tokens = int((usage or {}).get("input_tokens", 0))
    run.output_tokens = int((usage or {}).get("output_tokens", 0))
    run.metadata_json = metadata or {}
    await session.commit()


async def _manual(session: AsyncSession, candidate: NewsCandidate, code: str, detail: str) -> None:
    await _hold(session, candidate, "manual_review", code, detail)


async def _needs_redraft(
    session: AsyncSession, candidate: NewsCandidate, code: str, detail: str
) -> None:
    """Stop before the five-locale article exists: an editor has nothing to publish or
    fix here, only a new draft or a rejection, so it stays out of manual review.

    A re-verified candidate already has its article, which the editor can fix in the
    guide editor and verify again, so that one still goes to manual review."""

    # A confirmed draft stopped in stage two keeps the owner's confirmation: the same
    # action runs the translations again instead of drafting anew.
    kept = candidate.guide_article_id is not None or candidate.human_decision == "publish"
    status = "manual_review" if kept else "needs_redraft"
    await _hold(session, candidate, status, code, detail)


async def _hold(
    session: AsyncSession, candidate: NewsCandidate, status: str, code: str, detail: str
) -> None:
    candidate.status = status
    candidate.error_code = code
    candidate.error_detail = detail[:4000]
    await session.commit()


async def _claim_capacity(
    session: AsyncSession, candidate: NewsCandidate
) -> tuple[ClaimOutcome, NewsAutomationSettings | None]:
    # Re-read the candidate under a row lock: a retry, a sweep or a deferral for the same
    # candidate must see the status the first job committed, not the one it loaded.
    # Candidate before settings is the order report_major_error takes the same locks in.
    await session.refresh(candidate, with_for_update=True)
    settings = await settings_row(session, lock=True)
    if not settings.enabled:
        await session.rollback()
        return "disabled", None
    if candidate.status not in {"discovered", "failed"}:
        await session.rollback()
        return "skipped", None
    global_active = int(
        await session.scalar(
            select(func.count())
            .select_from(NewsCandidate)
            .where(NewsCandidate.status.in_(ACTIVE_STATUSES), NewsCandidate.id != candidate.id)
        )
        or 0
    )
    vertical_active = int(
        await session.scalar(
            select(func.count())
            .select_from(NewsCandidate)
            .where(
                NewsCandidate.status.in_(ACTIVE_STATUSES),
                NewsCandidate.vertical == candidate.vertical,
                NewsCandidate.id != candidate.id,
            )
        )
        or 0
    )
    if (
        global_active >= settings.global_concurrency
        or vertical_active >= settings.per_vertical_concurrency
    ):
        await session.rollback()
        return "deferred", None
    candidate.status = "drafting"
    candidate.processing_started_at = datetime.now(UTC)
    if candidate.error_code != REVERIFY_MARKER:
        candidate.error_code = None
    candidate.error_detail = None
    candidate.prompt_version = settings.prompt_version
    candidate.policy_version = settings.policy_version
    await session.commit()
    return "claimed", settings


def _clear_reverify_marker(candidate: NewsCandidate) -> None:
    if candidate.error_code == REVERIFY_MARKER:
        candidate.error_code = None


def _source_locked(document: GuideDocument, evidence: list[NewsEvidence]) -> GuideDocument:
    encoded = document.model_dump(mode="json")
    encoded["sources"] = [
        SourceRef(title=row.title, url=row.url, checked_on=row.retrieved_at.date()).model_dump(
            mode="json"
        )
        for row in evidence
        if row.role == "evidence"
    ]
    return GuideDocument.model_validate(encoded)


def _topic_linked(document: GuideDocument, vertical: str, locale: Locale) -> GuideDocument:
    encoded = document.model_dump(mode="json")
    topic = TOPIC_BY_VERTICAL[vertical]
    target = f"https://mokaair.com/{locale}/life/topics/{topic}"
    if not any(
        isinstance(block, dict) and block.get("type") == "link" and block.get("url") == target
        for block in encoded["blocks"]
    ):
        encoded["blocks"].append(
            LinkBlock(type="link", text=TOPIC_LINK_TEXT[locale], url=target).model_dump(mode="json")
        )
    return GuideDocument.model_validate(encoded)


async def _save_guide_bundle(
    session: AsyncSession,
    candidate: NewsCandidate,
    slug: str,
    event_date: Any,
    documents: dict[Locale, GuideDocument],
) -> tuple[GuideArticle, dict[Locale, int]]:
    now = datetime.now(UTC)
    topic = await session.scalar(
        select(GuideTopic).where(
            GuideTopic.slug == TOPIC_BY_VERTICAL[candidate.vertical],
            GuideTopic.section == "life",
            GuideTopic.is_active.is_(True),
        )
    )
    if topic is None:
        raise AppError(503, "news_topic_unavailable", "新聞主題尚未建立")

    article = (
        await session.get(GuideArticle, candidate.guide_article_id)
        if candidate.guide_article_id
        else None
    )
    if article is None:
        collision = await session.scalar(select(GuideArticle).where(GuideArticle.slug == slug))
        if collision is not None:
            raise AppError(409, "news_slug_conflict", "新聞網址代稱已被使用")
        article = GuideArticle(
            id=uuid4(),
            slug=slug,
            kind="life",
            news_date=event_date,
            is_active=True,
            created_at=now,
            updated_at=now,
        )
        session.add(article)
        session.add(GuideArticleTopic(article_id=article.id, topic_id=topic.id))
        candidate.guide_article_id = article.id

    versions: dict[Locale, int] = {}
    existing = {
        cast(Locale, row.locale): row
        for row in await session.scalars(
            select(GuideArticleLocale).where(GuideArticleLocale.article_id == article.id)
        )
    }
    for locale in LOCALES:
        typed_locale = cast(Locale, locale)
        encoded = documents[typed_locale].model_dump(mode="json")
        row = existing.get(typed_locale)
        if row is None:
            row = GuideArticleLocale(
                id=uuid4(),
                article_id=article.id,
                locale=locale,
                version=1,
                draft_json=encoded,
                created_at=now,
                updated_at=now,
            )
            session.add(row)
            version = 1
            action = "created"
        else:
            if row.published_version is not None:
                raise AppError(409, "news_article_already_published", "文章已有公開版本")
            version = row.version + 1
            row.version = version
            row.draft_json = encoded
            row.updated_at = now
            action = "draft_saved"
        session.add(
            GuideArticleRevision(
                article_locale_id=row.id,
                version=version,
                action=action,
                document_json=encoded,
                created_by_user_id=None,
                created_at=now,
            )
        )
        versions[typed_locale] = version
    audit(
        session,
        None,
        "news_draft_bundle_saved",
        f"news-candidate:{candidate.id}",
        candidate_id=str(candidate.id),
        article_id=str(article.id),
        prompt_version=candidate.prompt_version,
        policy_version=candidate.policy_version,
        evidence_sha256=candidate.evidence_hash,
    )
    await session.commit()
    return article, versions


class _Runs:
    """The pipeline run in progress, so a failure can be recorded against it."""

    def __init__(self, session: AsyncSession, candidate: NewsCandidate) -> None:
        self.session = session
        self.candidate = candidate
        self.active: NewsPipelineRun | None = None

    async def start(self, stage: str, *, provider: str | None, model: str | None) -> None:
        self.active = await _start_run(
            self.session, self.candidate, stage, provider=provider, model=model
        )

    async def finish(
        self,
        *,
        usage: dict[str, int] | None = None,
        model: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        assert self.active is not None
        await _finish_run(self.session, self.active, usage=usage, model=model, metadata=metadata)
        self.active = None


async def process_candidate(
    session: AsyncSession,
    redis: Redis,
    environment: Settings,
    candidate_id: UUID,
) -> str:
    """Run one candidate as far as it can go without a person.

    Stage one (owner decision, 2026-09-25): any source's article that is not a duplicate is
    drafted in Traditional Chinese, fact-checked against its evidence and assessed by Jev,
    then waits for the owner as ``news_zh_draft_ready``. Stage two runs once the owner has
    confirmed publication: the other four locales are translated and reviewed, the article
    is checked, saved and published. A re-verification of edited drafts runs the checks of
    both stages on the editor's text.
    """

    candidate = await session.get(NewsCandidate, candidate_id)
    if candidate is None:
        raise AppError(404, "news_candidate_not_found", "找不到新聞候選")
    outcome, settings = await _claim_capacity(session, candidate)
    if settings is None:
        return outcome

    runs = _Runs(session, candidate)
    try:
        evidence = list(
            await session.scalars(
                select(NewsEvidence)
                .where(NewsEvidence.candidate_id == candidate.id)
                .order_by(NewsEvidence.is_first_party.desc(), NewsEvidence.retrieved_at)
            )
        )
        usable = [row for row in evidence if row.role == "evidence"]
        candidate.evidence_hash = evidence_fingerprint(
            [{"url": row.url, "content_hash": row.content_hash} for row in evidence]
        )
        if not evidence_present(usable):
            # Only lead-only pages: nothing a draft could cite.
            candidate.status = "needs_evidence"
            candidate.error_code = "news_evidence_insufficient"
            candidate.error_detail = "No evidence page from an evidence source was found."
            await session.commit()
            return "needs_evidence"

        reverify_requested = candidate.error_code == REVERIFY_MARKER
        if (
            not reverify_requested
            and candidate.human_decision == "publish"
            and "zh-TW" in candidate.draft_bundle_json
        ):
            # Stage two: the owner confirmed this verified Traditional Chinese draft.
            confirmed = GuideDocument.model_validate(candidate.draft_bundle_json["zh-TW"])
            if candidate.event_date is None:
                raise AppError(409, "news_draft_unavailable", "候選草稿資料不完整")
            return await _second_stage(
                session,
                redis,
                environment,
                settings,
                candidate,
                evidence,
                usable,
                runs,
                document=confirmed,
                slug=await _drafted_slug(session, candidate),
                event_date=candidate.event_date,
                localized=None,
                automatic=False,
            )

        if await cleared_by_editor(session, candidate):
            # An editor already answered an uncertain check for this evidence.
            duplicate = "distinct"
        else:
            duplicate, confidence, duplicate_reasons = await ai.jev_duplicate_check(
                redis,
                environment,
                candidate.source_title,
                "\n".join(row.excerpt for row in evidence),
                await known_titles(session, candidate),
            )
            session.add(
                NewsAssessment(
                    candidate_id=candidate.id,
                    assessment_type="duplicate",
                    verdict="duplicate"
                    if duplicate == "duplicate"
                    else "manual"
                    if duplicate == "manual"
                    else "pass",
                    confidence=confidence,
                    provider="jev",
                    model=environment.jev_model,
                    reasons_json=duplicate_reasons,
                    details_json={},
                    evidence_hash=candidate.evidence_hash,
                    prompt_version=candidate.prompt_version,
                )
            )
        if duplicate == "duplicate":
            candidate.status = "duplicate"
            _clear_reverify_marker(candidate)
            await session.commit()
            return "duplicate"
        if duplicate == "manual":
            await _manual(
                session,
                candidate,
                DUPLICATE_UNCERTAIN,
                "Semantic duplicate check was uncertain.",
            )
            return "manual_review"
        await session.commit()

        reverify_documents: dict[Locale, GuideDocument] | None = None
        if reverify_requested:
            reverify_documents = {
                cast(Locale, locale): GuideDocument.model_validate(encoded)
                for locale, encoded in candidate.draft_bundle_json.items()
            }
            if set(reverify_documents) != set(LOCALES):
                raise AppError(422, "news_locale_bundle_incomplete", "五個語言版本必須完整")
            document = _source_locked(reverify_documents["zh-TW"], evidence)
            if candidate.guide_article_id is None:
                raise AppError(409, "news_draft_unavailable", "候選尚未建立可編輯草稿")
            article_for_slug = await session.get(GuideArticle, candidate.guide_article_id)
            if article_for_slug is None or candidate.event_date is None:
                raise AppError(409, "news_draft_unavailable", "候選草稿資料不完整")
            draft_slug = article_for_slug.slug
            draft_event_date = candidate.event_date
        else:
            await runs.start(
                "draft", provider=settings.writer_provider, model=settings.writer_model
            )
            draft, usage, model = await ai.draft_article(environment, settings, candidate, evidence)
            # Stage two builds the article under this address after the owner confirms.
            await runs.finish(usage=usage, model=model, metadata={"slug": draft.slug})
            if not draft.eligible:
                candidate.status = "rejected"
                candidate.error_code = "news_not_eligible"
                candidate.error_detail = draft.exclusion_reason
                await session.commit()
                return "rejected"
            candidate.event_date = draft.event_date
            candidate.claim_ledger_json = [claim.model_dump(mode="json") for claim in draft.claims]
            evidence_urls = {row.url for row in usable}
            unsupported_claim_urls = sorted(
                {
                    source_url
                    for claim in draft.claims
                    for source_url in claim.source_urls
                    if source_url not in evidence_urls
                }
            )
            if unsupported_claim_urls:
                await _needs_redraft(
                    session,
                    candidate,
                    "news_claim_source_invalid",
                    "Claim ledger cited non-evidence URLs: "
                    + "; ".join(unsupported_claim_urls[:5]),
                )
                return candidate.status
            document = _source_locked(draft.document, evidence)
            draft_slug = draft.slug
            draft_event_date = draft.event_date
        date_problems = event_date_problems(
            draft_event_date,
            draft_slug,
            [row.source_date or row.retrieved_at.date() for row in usable],
        )
        if date_problems:
            await _needs_redraft(
                session,
                candidate,
                "news_event_date_invalid",
                "; ".join(date_problems),
            )
            return candidate.status
        candidate.status = "verifying"
        await session.commit()

        verification_passed = False
        for verification_round in range(2):
            await runs.start(
                f"verification-{verification_round + 1}",
                provider=settings.verifier_provider,
                model=settings.verifier_model,
            )
            result, usage, model = await ai.verify_article(
                environment, settings, document, evidence
            )
            await runs.finish(usage=usage, model=model)
            session.add(
                NewsAssessment(
                    candidate_id=candidate.id,
                    assessment_type="verification",
                    verdict=result.verdict,
                    provider=settings.verifier_provider,
                    model=model,
                    reasons_json=result.issues,
                    details_json={
                        "round": verification_round + 1,
                        "document_sha256": document_fingerprint(document),
                    },
                    evidence_hash=candidate.evidence_hash,
                    prompt_version=candidate.prompt_version,
                )
            )
            if result.verdict == "pass":
                verification_passed = True
                break
            if result.verdict == "revise" and verification_round == 0 and result.corrected_document:
                document = _source_locked(result.corrected_document, evidence)
                await session.commit()
                continue
            await session.commit()
            break
        if not verification_passed:
            await _needs_redraft(
                session,
                candidate,
                "news_verification_failed",
                "Independent verification did not pass.",
            )
            return candidate.status

        if reverify_documents is not None:
            return await _second_stage(
                session,
                redis,
                environment,
                settings,
                candidate,
                evidence,
                usable,
                runs,
                document=document,
                slug=draft_slug,
                event_date=draft_event_date,
                localized=reverify_documents,
                automatic=False,
            )

        # End of stage one: keep the verified draft for the owner and ask Jev about it.
        candidate.draft_bundle_json = {"zh-TW": document.model_dump(mode="json")}
        candidate.lint_json = {}
        candidate.status = "jev_review"
        await session.commit()
        await runs.start("jev-zh-TW", provider="jev", model=environment.jev_model)
        decisions = await ai.jev_assessments(
            redis, environment, settings, candidate, {"zh-TW": document}, locales=("zh-TW",)
        )
        await runs.finish(
            usage={
                "input_tokens": sum(item.usage.get("input_tokens", 0) for item in decisions),
                "output_tokens": sum(item.usage.get("output_tokens", 0) for item in decisions),
            },
            metadata={"tiers": {item.locale: item.tier for item in decisions}},
        )
        for decision in decisions:
            session.add(
                NewsAssessment(
                    candidate_id=candidate.id,
                    assessment_type="jev",
                    locale=decision.locale,
                    verdict="pass" if decision.tier == "act" else "manual",
                    confidence=decision.confidence,
                    provider="jev",
                    model=environment.jev_model,
                    reasons_json=decision.reasons,
                    details_json={"tier": decision.tier},
                    evidence_hash=candidate.evidence_hash,
                    prompt_version=candidate.prompt_version,
                )
            )
        candidate.would_publish = bool(decisions) and all(
            item.tier == "act" for item in decisions
        )

        fresh_settings = await settings_row(session)
        gate = await gate_for(session, fresh_settings, cast(Vertical, candidate.vertical))
        if (
            fresh_settings.enabled
            and fresh_settings.mode == "automatic"
            and bool(getattr(fresh_settings, f"auto_publish_{candidate.vertical}"))
            and gate.eligible
            and candidate.would_publish
            # A single-source article always waits for a person.
            and evidence_sufficient(usable)
        ):
            return await _second_stage(
                session,
                redis,
                environment,
                settings,
                candidate,
                evidence,
                usable,
                runs,
                document=document,
                slug=draft_slug,
                event_date=draft_event_date,
                localized=None,
                automatic=True,
            )
        await _manual(
            session,
            candidate,
            ZH_DRAFT_READY,
            "A verified Traditional Chinese draft is waiting for the owner's decision.",
        )
        return "manual_review"
    except Exception as error:
        await session.rollback()
        candidate = await session.get(NewsCandidate, candidate_id)
        if candidate is not None and candidate.status not in {
            "published",
            "manual_review",
            "shadow_review",
            "needs_evidence",
            "needs_redraft",
            "duplicate",
            "rejected",
        }:
            candidate.status = "failed"
            if candidate.error_code != REVERIFY_MARKER:
                candidate.error_code = type(error).__name__[:64]
            candidate.error_detail = f"{type(error).__name__}: {error}"[:4000]
        if runs.active is not None:
            run = await session.get(NewsPipelineRun, runs.active.id)
            if run is not None:
                run.status = "failed"
                run.error_code = type(error).__name__[:64]
                run.error_detail = str(error)[:4000]
                run.finished_at = datetime.now(UTC)
        await session.commit()
        raise


async def _drafted_slug(session: AsyncSession, candidate: NewsCandidate) -> str:
    """The article address the writer chose in stage one, kept on its draft run."""

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
    if not isinstance(slug, str) or not slug:
        raise AppError(409, "news_draft_unavailable", "候選草稿資料不完整")
    return slug


async def _approver(session: AsyncSession, candidate: NewsCandidate) -> User | None:
    """The administrator who confirmed publication, for the audit rows and revisions."""

    user_id = await session.scalar(
        select(NewsAssessment.created_by_user_id)
        .where(
            NewsAssessment.candidate_id == candidate.id,
            NewsAssessment.assessment_type == "human",
            NewsAssessment.verdict == "publish",
        )
        .order_by(NewsAssessment.created_at.desc())
        .limit(1)
    )
    return await session.get(User, user_id) if user_id is not None else None


async def _second_stage(
    session: AsyncSession,
    redis: Redis,
    environment: Settings,
    settings: NewsAutomationSettings,
    candidate: NewsCandidate,
    evidence: list[NewsEvidence],
    usable: list[NewsEvidence],
    runs: _Runs,
    *,
    document: GuideDocument,
    slug: str,
    event_date: date,
    localized: dict[Locale, GuideDocument] | None,
    automatic: bool,
) -> str:
    """Translate (or take the editor's translations), review, check, save and publish."""

    candidate.status = "locale_review"
    await session.commit()
    if localized is None:
        documents: dict[Locale, GuideDocument] = {"zh-TW": document}
        for target in TARGET_LOCALES:
            await runs.start(
                f"translation-{target}",
                provider=settings.writer_provider,
                model=settings.writer_model,
            )
            translated, usage, model = await ai.translate_article(
                environment, settings, document, target
            )
            await runs.finish(usage=usage, model=model)
            documents[target] = translated.document
    else:
        documents = {**localized, "zh-TW": document}
    documents = {
        locale: _topic_linked(item, candidate.vertical, locale)
        for locale, item in documents.items()
    }
    document = documents["zh-TW"]
    session.add(
        NewsAssessment(
            candidate_id=candidate.id,
            assessment_type="locale_review",
            locale="zh-TW",
            verdict="pass",
            provider=settings.verifier_provider,
            model=settings.verifier_model,
            reasons_json=[],
            details_json={
                "basis": "verified_source_locale",
                "document_sha256": document_fingerprint(document),
            },
            evidence_hash=candidate.evidence_hash,
            prompt_version=candidate.prompt_version,
        )
    )
    for locale in TARGET_LOCALES:
        translated_document = _source_locked(documents[locale], evidence)
        locale_passed = False
        for review_round in range(2):
            await runs.start(
                f"locale-{locale}-{review_round + 1}",
                provider=settings.verifier_provider,
                model=settings.verifier_model,
            )
            locale_result, usage, model = await ai.review_locale(
                environment, settings, document, locale, translated_document
            )
            await runs.finish(usage=usage, model=model)
            if locale_result.verdict == "pass":
                locale_passed = True
                session.add(
                    NewsAssessment(
                        candidate_id=candidate.id,
                        assessment_type="locale_review",
                        locale=locale,
                        verdict="pass",
                        provider=settings.verifier_provider,
                        model=model,
                        reasons_json=[],
                        details_json={
                            "round": review_round + 1,
                            "document_sha256": document_fingerprint(translated_document),
                        },
                        evidence_hash=candidate.evidence_hash,
                        prompt_version=candidate.prompt_version,
                    )
                )
                break
            if (
                locale_result.verdict == "revise"
                and review_round == 0
                and locale_result.corrected_document
            ):
                translated_document = _source_locked(locale_result.corrected_document, evidence)
                continue
            session.add(
                NewsAssessment(
                    candidate_id=candidate.id,
                    assessment_type="locale_review",
                    locale=locale,
                    verdict="manual",
                    provider=settings.verifier_provider,
                    model=model,
                    reasons_json=locale_result.issues,
                    details_json={"round": review_round + 1},
                    evidence_hash=candidate.evidence_hash,
                    prompt_version=candidate.prompt_version,
                )
            )
            break
        documents[locale] = translated_document
        if not locale_passed:
            await _needs_redraft(
                session,
                candidate,
                "news_locale_review_failed",
                f"{locale} review did not pass.",
            )
            return candidate.status

    documents = await ensure_assets(session, candidate, documents)
    problems: dict[str, list[str]] = {
        locale: hard_policy_problems(
            item,
            cast(Vertical, candidate.vertical),
            locale,
            source_count=evidence_site_count(usable),
        )
        for locale, item in documents.items()
    }
    candidate.lint_json = problems
    candidate.draft_bundle_json = {
        locale: item.model_dump(mode="json") for locale, item in documents.items()
    }
    if any(problems.values()):
        await _needs_redraft(
            session,
            candidate,
            "news_hard_checks_failed",
            "One or more locales failed hard checks.",
        )
        return candidate.status

    await _save_guide_bundle(session, candidate, slug, event_date, documents)
    confirmed = candidate.human_decision == "publish"
    if not confirmed and not automatic:
        # An edited article nobody has confirmed yet waits for the publish button.
        _clear_reverify_marker(candidate)
        await _manual(
            session,
            candidate,
            READY_TO_PUBLISH,
            "The checked five-locale article is waiting for the publish button.",
        )
        return "manual_review"
    try:
        checked, versions = await news_service.publication_bundle(session, candidate, redis)
    except AppError as problem:
        if problem.code != "news_evidence_changed":
            raise
        await _manual(session, candidate, "news_evidence_changed", problem.detail)
        return "manual_review"
    _clear_reverify_marker(candidate)
    if confirmed:
        actor = await _approver(session, candidate)
        reason = candidate.human_reason or "The owner confirmed publication."
        metadata: dict[str, Any] = {"human_override": True, "confirmed_stage": "zh_draft"}
    else:
        actor = None
        reason = "Jev approved the Traditional Chinese draft and the vertical gate was enabled."
        metadata = {"model": environment.jev_model}
        audit(
            session,
            None,
            "news_candidate_auto_published",
            f"news-candidate:{candidate.id}",
            candidate_id=str(candidate.id),
            article_id=str(candidate.guide_article_id),
            model=environment.jev_model,
            prompt_version=candidate.prompt_version,
            evidence_sha256=candidate.evidence_hash,
        )
    await news_service.publish_news_bundle(
        session, candidate, actor, checked, versions, reason=reason, metadata=metadata
    )
    return "published"


async def recover_stalled_candidates(
    session: AsyncSession,
    *,
    now: datetime | None = None,
    limit: int = 20,
    older_than: timedelta = STALE_AFTER,
) -> list[UUID]:
    """Fail candidates whose job died mid-pipeline and return the ones to run again.

    A worker stopped by a deploy or by the job timeout leaves its candidate in an
    in-flight status that nothing moves on. It keeps holding a concurrency slot, so with
    the default of one per vertical the whole vertical stops and every other candidate
    defers forever. The scheduler waits ``STALE_AFTER`` because a job may still be
    running; the news worker passes ``older_than=0`` when it starts, when none can be.
    """

    current = now or datetime.now(UTC)
    rows = list(
        await session.scalars(
            select(NewsCandidate)
            .where(
                NewsCandidate.status.in_(ACTIVE_STATUSES),
                func.coalesce(NewsCandidate.processing_started_at, NewsCandidate.updated_at)
                <= current - older_than,
            )
            .order_by(NewsCandidate.processing_started_at, NewsCandidate.id)
            .limit(limit)
            .with_for_update(skip_locked=True)
        )
    )
    rerun: list[UUID] = []
    for row in rows:
        stalled_in = row.status
        for run in await session.scalars(
            select(NewsPipelineRun).where(
                NewsPipelineRun.candidate_id == row.id, NewsPipelineRun.status == "running"
            )
        ):
            run.status = "failed"
            run.error_code = "news_processing_stale"
            run.error_detail = "The worker stopped before this stage finished."
            run.finished_at = current
        recoveries = int(
            await session.scalar(
                select(func.count())
                .select_from(NewsPipelineRun)
                .where(
                    NewsPipelineRun.candidate_id == row.id,
                    NewsPipelineRun.stage == STALE_RECOVERY_STAGE,
                )
            )
            or 0
        )
        session.add(
            NewsPipelineRun(
                candidate_id=row.id,
                stage=STALE_RECOVERY_STAGE,
                status="failed",
                attempt=recoveries + 1,
                idempotency_key=f"{row.id}:{STALE_RECOVERY_STAGE}:{recoveries + 1}",
                error_code="news_processing_stale",
                error_detail=f"Stalled in {stalled_in}.",
                started_at=current,
                finished_at=current,
            )
        )
        row.status = "failed"
        # A stalled re-verification keeps its marker, so the rerun re-verifies the edited
        # drafts instead of writing new ones over them.
        if row.error_code != REVERIFY_MARKER:
            row.error_code = "news_processing_stale"
        row.error_detail = f"The worker stopped while this candidate was in {stalled_in}."
        if recoveries < MAX_AUTOMATIC_RECOVERIES:
            rerun.append(row.id)
    await session.commit()
    return rerun


async def orphaned_candidates(
    session: AsyncSession, *, now: datetime | None = None, limit: int = 20
) -> list[UUID]:
    """Discovered candidates that no queued job will pick up."""

    settings = await settings_row(session)
    if not settings.enabled:
        await session.rollback()
        return []
    current = now or datetime.now(UTC)
    ids = list(
        await session.scalars(
            select(NewsCandidate.id)
            .where(
                NewsCandidate.status == "discovered",
                NewsCandidate.updated_at < current - ORPHAN_AFTER,
            )
            .order_by(NewsCandidate.updated_at, NewsCandidate.id)
            .limit(limit)
        )
    )
    await session.rollback()
    return ids
