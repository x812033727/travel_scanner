from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, cast
from uuid import UUID, uuid4

from redis.asyncio import Redis
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.guides import admin_service
from app.guides.models import (
    GuideArticle,
    GuideArticleLocale,
    GuideArticleRevision,
    GuideArticleTopic,
    GuideTopic,
)
from app.guides.schemas import GuideDocument, SourceRef
from app.i18n import Locale
from app.news_automation import ai
from app.news_automation.assets import ensure_assets, mark_assets_public
from app.news_automation.fetch import RedisHostRateLimiter
from app.news_automation.models import (
    LOCALES,
    NewsAssessment,
    NewsAutomationSettings,
    NewsCandidate,
    NewsEvidence,
    NewsPipelineRun,
)
from app.news_automation.policy import (
    document_fingerprint,
    event_date_problems,
    evidence_fingerprint,
    hard_policy_problems,
)
from app.news_automation.schemas import Vertical
from app.news_automation.service import audit, gate_for, settings_row
from app.news_automation.validation import revalidate_evidence
from app.problems import AppError
from app.site_pages.schemas import LinkBlock

ACTIVE_STATUSES = ("drafting", "verifying", "locale_review", "jev_review")
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
    candidate.status = "manual_review"
    candidate.error_code = code
    candidate.error_detail = detail[:4000]
    await session.commit()


async def _claim_capacity(
    session: AsyncSession, candidate: NewsCandidate
) -> NewsAutomationSettings | None:
    settings = await settings_row(session, lock=True)
    if not settings.enabled or candidate.status not in {"discovered", "failed"}:
        await session.rollback()
        return None
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
        return None
    candidate.status = "drafting"
    candidate.processing_started_at = datetime.now(UTC)
    reverify_requested = candidate.error_code == "news_reverify_requested"
    if not reverify_requested:
        candidate.error_code = None
    candidate.error_detail = None
    candidate.prompt_version = settings.prompt_version
    candidate.policy_version = settings.policy_version
    await session.commit()
    return settings


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


async def process_candidate(
    session: AsyncSession,
    redis: Redis,
    environment: Settings,
    candidate_id: UUID,
) -> str:
    candidate = await session.get(NewsCandidate, candidate_id)
    if candidate is None:
        raise AppError(404, "news_candidate_not_found", "找不到新聞候選")
    settings = await _claim_capacity(session, candidate)
    if settings is None:
        return "deferred"

    active_run: NewsPipelineRun | None = None
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
        if len(usable) < 2 or not any(row.is_first_party for row in usable):
            await _manual(
                session,
                candidate,
                "news_evidence_insufficient",
                "At least two evidence sources including one first-party source are required.",
            )
            return "manual_review"

        recent_titles = list(
            await session.scalars(
                select(NewsCandidate.source_title)
                .where(
                    NewsCandidate.id != candidate.id,
                    NewsCandidate.vertical == candidate.vertical,
                    NewsCandidate.status.in_(("manual_review", "shadow_review", "published")),
                )
                .order_by(NewsCandidate.created_at.desc())
                .limit(40)
            )
        )
        duplicate, confidence, duplicate_reasons = await ai.jev_duplicate_check(
            redis,
            environment,
            candidate.source_title,
            "\n".join(row.excerpt for row in evidence),
            recent_titles,
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
            await session.commit()
            return "duplicate"
        if duplicate == "manual":
            await _manual(
                session,
                candidate,
                "news_duplicate_uncertain",
                "Semantic duplicate check was uncertain.",
            )
            return "manual_review"
        await session.commit()

        reverify_requested = candidate.error_code == "news_reverify_requested"
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
            candidate.error_code = None
        else:
            active_run = await _start_run(
                session,
                candidate,
                "draft",
                provider=settings.writer_provider,
                model=settings.writer_model,
            )
            draft, usage, model = await ai.draft_article(environment, settings, candidate, evidence)
            await _finish_run(session, active_run, usage=usage, model=model)
            active_run = None
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
                await _manual(
                    session,
                    candidate,
                    "news_claim_source_invalid",
                    "Claim ledger cited non-evidence URLs: "
                    + "; ".join(unsupported_claim_urls[:5]),
                )
                return "manual_review"
            document = _source_locked(draft.document, evidence)
            draft_slug = draft.slug
            draft_event_date = draft.event_date
        date_problems = event_date_problems(
            draft_event_date,
            draft_slug,
            [
                row.source_date or row.retrieved_at.date()
                for row in evidence
                if row.role == "evidence"
            ],
        )
        if date_problems:
            await _manual(
                session,
                candidate,
                "news_event_date_invalid",
                "; ".join(date_problems),
            )
            return "manual_review"
        candidate.status = "verifying"
        await session.commit()

        verification_passed = False
        for verification_round in range(2):
            active_run = await _start_run(
                session,
                candidate,
                f"verification-{verification_round + 1}",
                provider=settings.verifier_provider,
                model=settings.verifier_model,
            )
            result, usage, model = await ai.verify_article(
                environment, settings, document, evidence
            )
            await _finish_run(session, active_run, usage=usage, model=model)
            active_run = None
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
            await _manual(
                session,
                candidate,
                "news_verification_failed",
                "Independent verification did not pass.",
            )
            return "manual_review"

        candidate.status = "locale_review"
        await session.commit()
        if reverify_documents is None:
            active_run = await _start_run(
                session,
                candidate,
                "translation",
                provider=settings.writer_provider,
                model=settings.writer_model,
            )
            translations, usage, model = await ai.translate_article(environment, settings, document)
            await _finish_run(session, active_run, usage=usage, model=model)
            active_run = None
            documents: dict[Locale, GuideDocument] = {
                "zh-TW": document,
                **translations.documents,
            }
        else:
            documents = {**reverify_documents, "zh-TW": document}
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
            localized = _source_locked(documents[locale], evidence)
            locale_passed = False
            for review_round in range(2):
                active_run = await _start_run(
                    session,
                    candidate,
                    f"locale-{locale}-{review_round + 1}",
                    provider=settings.verifier_provider,
                    model=settings.verifier_model,
                )
                locale_result, usage, model = await ai.review_locale(
                    environment, settings, document, locale, localized
                )
                await _finish_run(session, active_run, usage=usage, model=model)
                active_run = None
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
                                "document_sha256": document_fingerprint(localized),
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
                    localized = _source_locked(locale_result.corrected_document, evidence)
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
            documents[locale] = localized
            if not locale_passed:
                await _manual(
                    session,
                    candidate,
                    "news_locale_review_failed",
                    f"{locale} review did not pass.",
                )
                return "manual_review"

        documents = await ensure_assets(session, candidate, documents)
        problems: dict[str, list[str]] = {
            locale: hard_policy_problems(
                item,
                cast(Vertical, candidate.vertical),
                locale,
                source_count=len(usable),
            )
            for locale, item in documents.items()
        }
        candidate.lint_json = problems
        candidate.draft_bundle_json = {
            locale: item.model_dump(mode="json") for locale, item in documents.items()
        }
        if any(problems.values()):
            await _manual(
                session,
                candidate,
                "news_hard_checks_failed",
                "One or more locales failed hard checks.",
            )
            return "manual_review"

        article, versions = await _save_guide_bundle(
            session, candidate, draft_slug, draft_event_date, documents
        )
        candidate.status = "jev_review"
        await session.commit()
        active_run = await _start_run(
            session, candidate, "jev", provider="jev", model=environment.jev_model
        )
        decisions = await ai.jev_assessments(redis, environment, settings, candidate, documents)
        jev_run_id = active_run.id
        await _finish_run(
            session,
            active_run,
            usage={
                "input_tokens": sum(item.usage.get("input_tokens", 0) for item in decisions),
                "output_tokens": sum(item.usage.get("output_tokens", 0) for item in decisions),
            },
            metadata={"tiers": {item.locale: item.tier for item in decisions}},
        )
        active_run = None
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
        candidate.would_publish = all(item.tier == "act" for item in decisions)
        evidence_current, evidence_reasons = await revalidate_evidence(
            session, evidence, rate_limiter=RedisHostRateLimiter(redis)
        )
        latest_hash = evidence_fingerprint(
            [{"url": row.url, "content_hash": row.content_hash} for row in evidence]
        )
        if not evidence_current or latest_hash != candidate.evidence_hash:
            candidate.would_publish = False
            await _manual(
                session,
                candidate,
                "news_evidence_changed",
                "Evidence changed before publication: " + "; ".join(evidence_reasons[:3]),
            )
            return "manual_review"
        if not candidate.would_publish:
            await _manual(
                session,
                candidate,
                "news_jev_manual",
                "At least one locale was not approved by Jev.",
            )
            return "manual_review"

        fresh_settings = await settings_row(session)
        gate = await gate_for(session, fresh_settings, cast(Vertical, candidate.vertical))
        automatic = bool(getattr(fresh_settings, f"auto_publish_{candidate.vertical}"))
        if (
            not fresh_settings.enabled
            or fresh_settings.mode != "automatic"
            or not automatic
            or not gate.eligible
        ):
            candidate.status = "shadow_review"
            await session.commit()
            return "shadow_review"

        await mark_assets_public(session, candidate.id)
        candidate.status = "published"
        candidate.published_at = datetime.now(UTC)
        audit(
            session,
            None,
            "news_candidate_auto_published",
            f"news-candidate:{candidate.id}",
            candidate_id=str(candidate.id),
            article_id=str(article.id),
            model=environment.jev_model,
            prompt_version=candidate.prompt_version,
            evidence_sha256=candidate.evidence_hash,
        )
        await admin_service.publish_bundle(
            session,
            None,
            article.id,
            documents,
            versions,
            reason="Jev approved all five locales and the vertical gate was enabled.",
            automation_metadata={
                "candidate_id": str(candidate.id),
                "pipeline_run_id": str(jev_run_id),
                "model": environment.jev_model,
                "prompt_version": candidate.prompt_version,
                "policy_version": candidate.policy_version,
                "evidence_sha256": candidate.evidence_hash,
            },
        )
        return "published"
    except Exception as error:
        await session.rollback()
        candidate = await session.get(NewsCandidate, candidate_id)
        if candidate is not None and candidate.status not in {
            "published",
            "manual_review",
            "shadow_review",
            "duplicate",
            "rejected",
        }:
            candidate.status = "failed"
            candidate.error_code = type(error).__name__[:64]
            candidate.error_detail = str(error)[:4000]
        if active_run is not None:
            run = await session.get(NewsPipelineRun, active_run.id)
            if run is not None:
                run.status = "failed"
                run.error_code = type(error).__name__[:64]
                run.error_detail = str(error)[:4000]
                run.finished_at = datetime.now(UTC)
        await session.commit()
        raise
