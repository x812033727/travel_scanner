from __future__ import annotations

import math
from datetime import UTC, datetime
from typing import Any, cast
from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy import and_, case, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.guides import admin_service
from app.guides.models import GuideArticleLocale
from app.guides.schemas import GuideDocument
from app.i18n import Locale
from app.models import AdminAuditLog, User
from app.news_automation.assets import mark_assets_public
from app.news_automation.fetch import RedisHostRateLimiter
from app.news_automation.models import (
    LOCALES,
    NewsAssessment,
    NewsAutomationSettings,
    NewsCandidate,
    NewsEvidence,
    NewsPipelineRun,
    NewsSource,
)
from app.news_automation.policy import (
    document_fingerprint,
    evidence_fingerprint,
    gate_result,
    hard_policy_problems,
)
from app.news_automation.schemas import (
    AssessmentView,
    CandidateAction,
    CandidateDetail,
    CandidatePage,
    CandidateSummary,
    EvidenceView,
    GateView,
    RunView,
    SettingsView,
    SettingsWrite,
    SourcePatch,
    SourceView,
    SourceWrite,
    StatsView,
    Vertical,
)
from app.news_automation.validation import revalidate_evidence, validate_source_configuration
from app.problems import AppError


def audit(
    session: AsyncSession,
    actor: User | None,
    action: str,
    target: str,
    **metadata: object,
) -> None:
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id if actor else None,
            action=action,
            target=target,
            metadata_json={"system_actor": actor is None, **metadata},
        )
    )


async def settings_row(session: AsyncSession, *, lock: bool = False) -> NewsAutomationSettings:
    statement = select(NewsAutomationSettings).where(NewsAutomationSettings.id == 1)
    if lock:
        statement = statement.with_for_update()
    row = await session.scalar(statement)
    if row is None:
        row = NewsAutomationSettings(id=1)
        session.add(row)
        await session.flush()
    return row


def source_view(row: NewsSource) -> SourceView:
    return SourceView(
        id=row.id,
        name=row.name,
        url=row.url,
        format=cast(Any, row.format),
        role=cast(Any, row.role),
        vertical=cast(Any, row.vertical),
        is_first_party=row.is_first_party,
        enabled=row.enabled,
        scan_interval_minutes=row.scan_interval_minutes,
        allowed_redirect_hosts=row.allowed_redirect_hosts_json,
        config=row.config_json,
        etag=row.etag,
        last_modified=row.last_modified,
        last_scanned_at=row.last_scanned_at,
        next_scan_at=row.next_scan_at,
        last_status=row.last_status,
        last_error=row.last_error,
        consecutive_failures=row.consecutive_failures,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


async def list_sources(session: AsyncSession) -> list[SourceView]:
    rows = await session.scalars(select(NewsSource).order_by(NewsSource.name, NewsSource.url))
    return [source_view(row) for row in rows]


async def create_source(session: AsyncSession, actor: User, payload: SourceWrite) -> SourceView:
    row = NewsSource(
        name=payload.name,
        url=payload.url,
        format=payload.format,
        role=payload.role,
        vertical=payload.vertical,
        is_first_party=payload.is_first_party,
        enabled=payload.enabled,
        scan_interval_minutes=payload.scan_interval_minutes,
        allowed_redirect_hosts_json=payload.allowed_redirect_hosts,
        config_json=payload.config,
        created_by_user_id=actor.id,
    )
    session.add(row)
    try:
        await session.flush()
        if row.enabled:
            await validate_source_configuration(row)
        audit(session, actor, "news_source_created", f"news-source:{row.id}", url=row.url)
        await session.commit()
    except AppError:
        await session.rollback()
        raise
    except Exception as error:
        await session.rollback()
        if "unique" in str(error).casefold():
            raise AppError(409, "news_source_exists", "這個新聞來源已存在") from error
        raise
    return source_view(row)


async def update_source(
    session: AsyncSession, actor: User, source_id: UUID, payload: SourcePatch
) -> SourceView:
    row = await session.get(NewsSource, source_id)
    if row is None:
        raise AppError(404, "news_source_not_found", "找不到新聞來源")
    before = source_view(row).model_dump(mode="json")
    values = payload.model_dump(exclude_unset=True)
    if "allowed_redirect_hosts" in values:
        values["allowed_redirect_hosts_json"] = values.pop("allowed_redirect_hosts")
    if "config" in values:
        values["config_json"] = values.pop("config")
    if values.get("enabled") is True:
        row.next_scan_at = datetime.now(UTC)
    for key, value in values.items():
        setattr(row, key, value)
    if row.is_first_party and row.role != "evidence":
        raise AppError(422, "news_source_role_invalid", "第一方來源必須設定為 evidence")
    source_definition_fields = {
        "url",
        "format",
        "role",
        "vertical",
        "is_first_party",
        "enabled",
        "allowed_redirect_hosts_json",
        "config_json",
    }
    try:
        if row.enabled and source_definition_fields.intersection(values):
            await validate_source_configuration(row)
        audit(
            session,
            actor,
            "news_source_updated",
            f"news-source:{row.id}",
            before=before,
            after=source_view(row).model_dump(mode="json"),
        )
        await session.commit()
    except AppError:
        await session.rollback()
        raise
    except Exception as error:
        await session.rollback()
        if "unique" in str(error).casefold():
            raise AppError(409, "news_source_exists", "這個新聞來源已存在") from error
        raise
    return source_view(row)


async def validate_source_now(session: AsyncSession, actor: User, source_id: UUID) -> SourceView:
    row = await session.get(NewsSource, source_id)
    if row is None:
        raise AppError(404, "news_source_not_found", "找不到新聞來源")
    try:
        await validate_source_configuration(row)
        row.last_status = "validated"
        row.last_error = None
        audit(
            session,
            actor,
            "news_source_validated",
            f"news-source:{row.id}",
            url=row.url,
        )
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    return source_view(row)


async def delete_source(session: AsyncSession, actor: User, source_id: UUID) -> None:
    row = await session.get(NewsSource, source_id)
    if row is None:
        raise AppError(404, "news_source_not_found", "找不到新聞來源")
    candidate_count = int(
        await session.scalar(
            select(func.count()).select_from(NewsCandidate).where(NewsCandidate.source_id == row.id)
        )
        or 0
    )
    if candidate_count:
        raise AppError(409, "news_source_in_use", "來源已有候選紀錄，只能停用不能刪除")
    await session.delete(row)
    audit(session, actor, "news_source_deleted", f"news-source:{row.id}", url=row.url)
    await session.commit()


async def gate_for(
    session: AsyncSession, settings: NewsAutomationSettings, vertical: Vertical
) -> GateView:
    row = (
        await session.execute(
            select(
                func.count(NewsCandidate.id),
                func.coalesce(
                    func.sum(
                        case(
                            (
                                or_(
                                    and_(
                                        NewsCandidate.would_publish.is_(True),
                                        NewsCandidate.human_decision == "publish",
                                    ),
                                    and_(
                                        NewsCandidate.would_publish.is_(False),
                                        NewsCandidate.human_decision == "reject",
                                    ),
                                ),
                                1,
                            ),
                            else_=0,
                        )
                    ),
                    0,
                ),
                func.coalesce(
                    func.sum(case((NewsCandidate.human_major_error.is_(True), 1), else_=0)), 0
                ),
            ).where(
                NewsCandidate.vertical == vertical,
                NewsCandidate.human_decision.is_not(None),
                NewsCandidate.would_publish.is_not(None),
                # Only candidates whose five-locale bundle actually reached Jev count.
                NewsCandidate.status.in_(
                    ("shadow_review", "manual_review", "published", "rejected")
                ),
            )
        )
    ).one()
    return gate_result(
        vertical,
        started_at=getattr(settings, f"shadow_started_at_{vertical}"),
        labelled=int(row[0] or 0),
        agreements=int(row[1] or 0),
        serious_false_positives=int(row[2] or 0),
        min_days=settings.min_shadow_days,
        min_candidates=settings.min_shadow_candidates,
        min_agreement=settings.min_human_agreement,
    )


async def settings_view(session: AsyncSession) -> SettingsView:
    row = await settings_row(session)
    gates = {
        vertical: await gate_for(session, row, vertical) for vertical in ("ai", "tech", "crypto")
    }
    return SettingsView(
        enabled=row.enabled,
        mode=cast(Any, row.mode),
        writer_provider=cast(Any, row.writer_provider),
        writer_model=row.writer_model,
        verifier_provider=cast(Any, row.verifier_provider),
        verifier_model=row.verifier_model,
        global_concurrency=row.global_concurrency,
        per_vertical_concurrency=row.per_vertical_concurrency,
        min_shadow_days=row.min_shadow_days,
        min_shadow_candidates=row.min_shadow_candidates,
        min_human_agreement=row.min_human_agreement,
        jev_act_confidence=row.jev_act_confidence,
        auto_publish_ai=row.auto_publish_ai,
        auto_publish_tech=row.auto_publish_tech,
        auto_publish_crypto=row.auto_publish_crypto,
        prompt_version=row.prompt_version,
        policy_version=row.policy_version,
        gates=gates,
        updated_at=row.updated_at,
    )


async def update_settings(
    session: AsyncSession, actor: User, payload: SettingsWrite
) -> SettingsView:
    row = await settings_row(session, lock=True)
    before = {
        "writer_provider": row.writer_provider,
        "writer_model": row.writer_model,
        "verifier_provider": row.verifier_provider,
        "verifier_model": row.verifier_model,
        "prompt_version": row.prompt_version,
        "policy_version": row.policy_version,
    }
    major_change = any(getattr(payload, key) != value for key, value in before.items())
    values = payload.model_dump()
    if major_change:
        for vertical in ("ai", "tech", "crypto"):
            values[f"auto_publish_{vertical}"] = False
            setattr(row, f"shadow_started_at_{vertical}", datetime.now(UTC))
        values["mode"] = "shadow"
    for vertical in ("ai", "tech", "crypto"):
        if values[f"auto_publish_{vertical}"]:
            gate = await gate_for(session, row, cast(Vertical, vertical))
            if not gate.eligible:
                raise AppError(
                    409,
                    "news_gate_not_met",
                    f"{vertical} 尚未達到自動發布門檻：{', '.join(gate.reasons)}",
                )
            if values["mode"] != "automatic":
                raise AppError(409, "news_mode_shadow", "影子模式不能開啟自動發布")
    for key, value in values.items():
        setattr(row, key, value)
    row.updated_by_user_id = actor.id
    audit(
        session,
        actor,
        "news_settings_updated",
        "news-settings:1",
        major_change=major_change,
        auto_publish={
            vertical: values[f"auto_publish_{vertical}"] for vertical in ("ai", "tech", "crypto")
        },
    )
    await session.commit()
    return await settings_view(session)


def candidate_summary(row: NewsCandidate) -> CandidateSummary:
    return CandidateSummary(
        id=row.id,
        vertical=cast(Vertical, row.vertical),
        status=cast(Any, row.status),
        source_title=row.source_title,
        canonical_url=row.canonical_url,
        event_date=row.event_date,
        would_publish=row.would_publish,
        human_decision=cast(Any, row.human_decision),
        error_code=row.error_code,
        error_detail=row.error_detail,
        guide_article_id=row.guide_article_id,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


async def list_candidates(
    session: AsyncSession,
    *,
    page: int,
    limit: int,
    status: str | None = None,
    vertical: Vertical | None = None,
) -> CandidatePage:
    criteria: list[Any] = []
    if status:
        criteria.append(NewsCandidate.status == status)
    if vertical:
        criteria.append(NewsCandidate.vertical == vertical)
    total = int(
        await session.scalar(select(func.count()).select_from(NewsCandidate).where(*criteria)) or 0
    )
    rows = await session.scalars(
        select(NewsCandidate)
        .where(*criteria)
        .order_by(NewsCandidate.updated_at.desc(), NewsCandidate.id)
        .offset((page - 1) * limit)
        .limit(limit)
    )
    return CandidatePage(
        candidates=[candidate_summary(row) for row in rows],
        total=total,
        page=page,
        pages=max(1, math.ceil(total / limit)),
    )


async def candidate_detail(session: AsyncSession, candidate_id: UUID) -> CandidateDetail:
    row = await session.get(NewsCandidate, candidate_id)
    if row is None:
        raise AppError(404, "news_candidate_not_found", "找不到新聞候選")
    evidence = await session.scalars(
        select(NewsEvidence)
        .where(NewsEvidence.candidate_id == row.id)
        .order_by(NewsEvidence.is_first_party.desc(), NewsEvidence.retrieved_at)
    )
    assessments = await session.scalars(
        select(NewsAssessment)
        .where(NewsAssessment.candidate_id == row.id)
        .order_by(NewsAssessment.created_at)
    )
    runs = await session.scalars(
        select(NewsPipelineRun)
        .where(NewsPipelineRun.candidate_id == row.id)
        .order_by(NewsPipelineRun.started_at)
    )
    documents = {
        cast(Locale, locale): GuideDocument.model_validate(document)
        for locale, document in row.draft_bundle_json.items()
        if locale in LOCALES
    }
    return CandidateDetail(
        **candidate_summary(row).model_dump(),
        evidence=[
            EvidenceView(
                id=item.id,
                role=cast(Any, item.role),
                is_first_party=item.is_first_party,
                url=item.url,
                title=item.title,
                retrieved_at=item.retrieved_at,
                source_date=item.source_date,
                content_hash=item.content_hash,
                excerpt=item.excerpt,
            )
            for item in evidence
        ],
        assessments=[
            AssessmentView(
                id=item.id,
                assessment_type=item.assessment_type,
                locale=cast(Locale | None, item.locale),
                verdict=item.verdict,
                confidence=item.confidence,
                provider=item.provider,
                model=item.model,
                reasons=item.reasons_json,
                details=item.details_json,
                created_at=item.created_at,
            )
            for item in assessments
        ],
        runs=[
            RunView(
                id=item.id,
                stage=item.stage,
                status=item.status,
                attempt=item.attempt,
                provider=item.provider,
                model=item.model,
                input_tokens=item.input_tokens,
                output_tokens=item.output_tokens,
                error_code=item.error_code,
                error_detail=item.error_detail,
                metadata=item.metadata_json,
                started_at=item.started_at,
                finished_at=item.finished_at,
            )
            for item in runs
        ],
        documents=documents,
        claim_ledger=row.claim_ledger_json,
        lint=row.lint_json,
        human_reason=row.human_reason,
        human_major_error=row.human_major_error,
    )


async def reject_candidate(
    session: AsyncSession, actor: User, candidate_id: UUID, payload: CandidateAction
) -> CandidateDetail:
    row = await session.get(NewsCandidate, candidate_id, with_for_update=True)
    if row is None:
        raise AppError(404, "news_candidate_not_found", "找不到新聞候選")
    if row.status not in {"manual_review", "shadow_review", "failed", "duplicate"}:
        raise AppError(409, "news_candidate_not_reviewable", "這個候選目前不能退件")
    row.status = "rejected"
    row.human_decision = "reject"
    row.human_reason = payload.reason
    row.human_major_error = payload.major_error
    session.add(
        NewsAssessment(
            candidate_id=row.id,
            assessment_type="human",
            verdict="reject",
            reasons_json=[payload.reason],
            details_json={"major_error": payload.major_error},
            evidence_hash=row.evidence_hash,
            prompt_version=row.prompt_version,
            created_by_user_id=actor.id,
        )
    )
    audit(
        session,
        actor,
        "news_candidate_rejected",
        f"news-candidate:{row.id}",
        reason=payload.reason,
        major_error=payload.major_error,
    )
    await session.commit()
    return await candidate_detail(session, row.id)


async def retry_candidate(
    session: AsyncSession, actor: User, candidate_id: UUID, payload: CandidateAction
) -> CandidateDetail:
    row = await session.get(NewsCandidate, candidate_id, with_for_update=True)
    if row is None:
        raise AppError(404, "news_candidate_not_found", "找不到新聞候選")
    if row.status not in {"manual_review", "shadow_review", "failed"}:
        raise AppError(409, "news_candidate_not_retryable", "這個候選目前不能重跑")
    row.status = "discovered"
    row.error_code = None
    row.error_detail = None
    row.retry_count += 1
    row.human_reason = payload.reason
    audit(
        session,
        actor,
        "news_candidate_retried",
        f"news-candidate:{row.id}",
        reason=payload.reason,
        retry_count=row.retry_count,
    )
    await session.commit()
    return await candidate_detail(session, row.id)


async def reverify_candidate(
    session: AsyncSession, actor: User, candidate_id: UUID, payload: CandidateAction
) -> CandidateDetail:
    row = await session.get(NewsCandidate, candidate_id, with_for_update=True)
    if row is None:
        raise AppError(404, "news_candidate_not_found", "找不到新聞候選")
    if row.status not in {"manual_review", "shadow_review", "failed"}:
        raise AppError(409, "news_candidate_not_retryable", "這個候選目前不能重新查核")
    if row.guide_article_id is None:
        raise AppError(409, "news_draft_unavailable", "候選尚未建立可編輯的五語草稿")
    locale_rows = list(
        await session.scalars(
            select(GuideArticleLocale).where(GuideArticleLocale.article_id == row.guide_article_id)
        )
    )
    documents = {
        item.locale: GuideDocument.model_validate(item.draft_json).model_dump(mode="json")
        for item in locale_rows
    }
    if set(documents) != set(LOCALES):
        raise AppError(422, "news_locale_bundle_incomplete", "五個語言版本必須完整")
    row.draft_bundle_json = documents
    row.status = "discovered"
    row.error_code = "news_reverify_requested"
    row.error_detail = None
    row.retry_count += 1
    row.human_reason = payload.reason
    audit(
        session,
        actor,
        "news_candidate_reverify_requested",
        f"news-candidate:{row.id}",
        reason=payload.reason,
        retry_count=row.retry_count,
    )
    await session.commit()
    return await candidate_detail(session, row.id)


async def publish_candidate(
    session: AsyncSession,
    actor: User,
    candidate_id: UUID,
    payload: CandidateAction,
    redis: Redis | None = None,
) -> CandidateDetail:
    row = await session.get(NewsCandidate, candidate_id, with_for_update=True)
    if row is None:
        raise AppError(404, "news_candidate_not_found", "找不到新聞候選")
    if row.status not in {"manual_review", "shadow_review"} or row.guide_article_id is None:
        raise AppError(409, "news_candidate_not_publishable", "這個候選目前不能發布")
    evidence = list(
        await session.scalars(select(NewsEvidence).where(NewsEvidence.candidate_id == row.id))
    )
    evidence_hash = evidence_fingerprint(
        [{"url": item.url, "content_hash": item.content_hash} for item in evidence]
    )
    if evidence_hash != row.evidence_hash:
        raise AppError(409, "news_evidence_changed", "來源內容已變更，請重新查核")
    evidence_current, evidence_reasons = await revalidate_evidence(
        session,
        evidence,
        rate_limiter=RedisHostRateLimiter(redis) if redis is not None else None,
    )
    if not evidence_current:
        raise AppError(
            409,
            "news_evidence_changed",
            f"來源內容或來源政策已變更，請重新查核：{'; '.join(evidence_reasons[:3])}",
        )
    if len([item for item in evidence if item.role == "evidence"]) < 2 or not any(
        item.is_first_party for item in evidence
    ):
        raise AppError(422, "news_evidence_insufficient", "發布需要兩個證據來源及一個第一方來源")
    locale_rows = list(
        await session.scalars(
            select(GuideArticleLocale).where(GuideArticleLocale.article_id == row.guide_article_id)
        )
    )
    documents = {
        cast(Locale, item.locale): GuideDocument.model_validate(item.draft_json)
        for item in locale_rows
    }
    row.draft_bundle_json = {
        locale: document.model_dump(mode="json") for locale, document in documents.items()
    }
    if set(documents) != set(LOCALES):
        raise AppError(422, "news_locale_bundle_incomplete", "五個語言版本必須完整")
    problems = {
        locale: hard_policy_problems(
            document,
            cast(Vertical, row.vertical),
            locale,
            source_count=len([item for item in evidence if item.role == "evidence"]),
        )
        for locale, document in documents.items()
    }
    if any(problems.values()):
        raise AppError(422, "news_hard_checks_failed", "硬性格式或政策檢查未通過")
    latest_verification = await session.scalar(
        select(NewsAssessment)
        .where(
            NewsAssessment.candidate_id == row.id,
            NewsAssessment.assessment_type == "verification",
            NewsAssessment.verdict == "pass",
            NewsAssessment.evidence_hash == row.evidence_hash,
        )
        .order_by(NewsAssessment.created_at.desc())
    )
    if latest_verification is None:
        raise AppError(409, "news_verification_required", "請先重新查核後再發布")
    if latest_verification.details_json.get("document_sha256") != document_fingerprint(
        documents["zh-TW"]
    ):
        raise AppError(409, "news_verification_stale", "繁中草稿已修改，請重新查核")
    locale_assessments = list(
        await session.scalars(
            select(NewsAssessment)
            .where(
                NewsAssessment.candidate_id == row.id,
                NewsAssessment.assessment_type == "locale_review",
                NewsAssessment.verdict == "pass",
                NewsAssessment.evidence_hash == row.evidence_hash,
            )
            .order_by(NewsAssessment.created_at.desc())
        )
    )
    latest_by_locale: dict[str, NewsAssessment] = {}
    for assessment in locale_assessments:
        if assessment.locale is not None:
            latest_by_locale.setdefault(assessment.locale, assessment)
    if set(latest_by_locale) != set(LOCALES) or any(
        latest_by_locale[locale].details_json.get("document_sha256")
        != document_fingerprint(document)
        for locale, document in documents.items()
    ):
        raise AppError(409, "news_locale_review_required", "五個語言都必須通過語系檢查")
    versions = {cast(Locale, item.locale): item.version for item in locale_rows}
    if set(versions) != set(LOCALES):
        raise AppError(422, "news_locale_bundle_incomplete", "五個語言版本必須完整")
    await mark_assets_public(session, row.id)
    row.status = "published"
    row.human_decision = "publish"
    row.human_reason = payload.reason
    row.human_major_error = payload.major_error
    row.published_at = datetime.now(UTC)
    session.add(
        NewsAssessment(
            candidate_id=row.id,
            assessment_type="human",
            verdict="publish",
            reasons_json=[payload.reason],
            details_json={"major_error": payload.major_error},
            evidence_hash=row.evidence_hash,
            prompt_version=row.prompt_version,
            created_by_user_id=actor.id,
        )
    )
    await admin_service.publish_bundle(
        session,
        actor,
        row.guide_article_id,
        documents,
        versions,
        reason=payload.reason,
        automation_metadata={
            "candidate_id": str(row.id),
            "evidence_sha256": row.evidence_hash,
            "prompt_version": row.prompt_version,
            "policy_version": row.policy_version,
            "human_override": True,
        },
    )
    return await candidate_detail(session, row.id)


async def report_major_error(
    session: AsyncSession, actor: User, candidate_id: UUID, payload: CandidateAction
) -> CandidateDetail:
    """Record a post-publication safety incident and stop that vertical's autopilot."""

    row = await session.get(NewsCandidate, candidate_id, with_for_update=True)
    if row is None:
        raise AppError(404, "news_candidate_not_found", "找不到新聞候選")
    if row.status != "published":
        raise AppError(409, "news_candidate_not_published", "只有已發布候選可回報重大錯誤")
    settings = await settings_row(session, lock=True)
    setattr(settings, f"auto_publish_{row.vertical}", False)
    setattr(settings, f"shadow_started_at_{row.vertical}", datetime.now(UTC))
    settings.updated_by_user_id = actor.id
    row.human_decision = "reject"
    row.human_reason = payload.reason
    row.human_major_error = True
    session.add(
        NewsAssessment(
            candidate_id=row.id,
            assessment_type="human",
            verdict="reject",
            reasons_json=[payload.reason],
            details_json={"major_error": True, "post_publication_incident": True},
            evidence_hash=row.evidence_hash,
            prompt_version=row.prompt_version,
            created_by_user_id=actor.id,
        )
    )
    audit(
        session,
        actor,
        "news_post_publication_major_error",
        f"news-candidate:{row.id}",
        reason=payload.reason,
        vertical=row.vertical,
        category_auto_publish_disabled=True,
    )
    await session.commit()
    return await candidate_detail(session, row.id)


async def stats(session: AsyncSession) -> StatsView:
    rows = await session.execute(
        select(NewsCandidate.status, func.count()).group_by(NewsCandidate.status)
    )
    by_status = {status: int(count) for status, count in rows}
    run_totals = (
        await session.execute(
            select(
                func.count(NewsPipelineRun.id),
                func.coalesce(func.sum(case((NewsPipelineRun.status == "failed", 1), else_=0)), 0),
                func.coalesce(func.sum(NewsPipelineRun.input_tokens), 0),
                func.coalesce(func.sum(NewsPipelineRun.output_tokens), 0),
            )
        )
    ).one()
    return StatsView(
        pending_review=by_status.get("manual_review", 0) + by_status.get("shadow_review", 0),
        failed=by_status.get("failed", 0),
        published=by_status.get("published", 0),
        queue_by_status=by_status,
        pipeline_runs=int(run_totals[0] or 0),
        pipeline_failures=int(run_totals[1] or 0),
        input_tokens=int(run_totals[2] or 0),
        output_tokens=int(run_totals[3] or 0),
    )
