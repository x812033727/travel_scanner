from __future__ import annotations

import base64
import hashlib
import json
import math
import re
from datetime import UTC, date, datetime
from typing import Any, cast
from urllib.parse import urlsplit
from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy import and_, case, func, inspect, or_, select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.ai.catalog import MODEL_CATALOG, Capability
from app.guides import admin_service
from app.guides.models import (
    GuideArticle,
    GuideArticleLocale,
    GuideArticleRevision,
    GuideArticleTopic,
)
from app.guides.schemas import GuideDocument, Kind, article_slug
from app.guides.service import _target as guide_target
from app.hotspots.ai_search import research_model
from app.i18n import Locale
from app.models import AdminAuditLog, User
from app.news_automation.assets import mark_assets_public
from app.news_automation.duplicates import (
    DUPLICATE_UNCERTAIN,
    HUMAN_PROVIDER,
    similar_titles,
)
from app.news_automation.fetch import RedisHostRateLimiter
from app.news_automation.models import (
    LOCALES,
    NewsAssessment,
    NewsAsset,
    NewsAutomationSettings,
    NewsCandidate,
    NewsEvidence,
    NewsPipelineRun,
    NewsSource,
)
from app.news_automation.policy import (
    EVIDENCE_REFRESH_MARKER,
    ZH_DRAFT_READY,
    document_fingerprint,
    event_date_problems,
    evidence_fingerprint,
    evidence_present,
    evidence_site_count,
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
    ModelOptionView,
    ModelsWrite,
    ProviderName,
    RunView,
    SettingsView,
    SettingsWrite,
    SourcePatch,
    SourceView,
    SourceWrite,
    StatsView,
    Vertical,
)
from app.news_automation.validation import (
    refresh_evidence,
    revalidate_evidence,
    validate_source_configuration,
)
from app.problems import AppError

# The news stages run through the guide-search adapters in app.hotspots.ai_search, so a
# vendor's dropdown offers the catalog models that can serve that adapter.
MODEL_CAPABILITY: dict[ProviderName, Capability] = {
    "openai": "responses_json_schema_strict",
    "anthropic": "anthropic_structured_output",
    "minimax": "responses_json_schema_strict",
    "gemini": "gemini_structured",
}


def model_options() -> dict[ProviderName, list[ModelOptionView]]:
    return {
        provider: [
            ModelOptionView(
                value=entry.id,
                label=entry.label,
                description=entry.note,
                status=entry.status,
            )
            for entry in MODEL_CATALOG[provider]
            if capability in entry.capabilities
        ]
        for provider, capability in MODEL_CAPABILITY.items()
    }


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


HELD_BUNDLE_SCHEMA = "mokaair-news-held-bundle-ingestion-v1"
HELD_STATE_SCHEMA = "mokaair-news-held-bundle-state-v1"
HELD_REVIEW_SCHEMA = "mokaair-news-held-bundle-draft-review-v1"
HELD_INGESTION_ACTION = "news_held_bundle_ingested"
HELD_INGESTION_STATUSES = frozenset({"manual_review", "shadow_review", "needs_redraft", "failed"})


def held_bundle_digest(value: object) -> str:
    """Whole JSON, including value types; unlike the editorial fingerprint, omit nothing."""
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False
        ).encode("utf-8")
    ).hexdigest()


def _held_row(row: Any) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for column in inspect(type(row)).column_attrs:
        value = getattr(row, column.key)
        if isinstance(value, datetime):
            value = value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)
            value = value.isoformat(timespec="microseconds")
        elif isinstance(value, (UUID, date)):
            value = str(value)
        elif isinstance(value, bytes):
            value = {"base64": base64.b64encode(value).decode("ascii")}
        result[column.key] = value
    return result


async def _held_live_jobs(redis: Redis, candidate_id: UUID) -> list[str]:
    """Read candidate and judge jobs, including retained hashes and live queue registries.

    Redis failure propagates: an unavailable queue is not evidence that it is idle.
    """
    prefixes = (f"news-candidate-{candidate_id}-", f"news-judge-{candidate_id}-")
    live: set[str] = set()
    for prefix in prefixes:
        async for key in redis.scan_iter(match=f"rq:job:{prefix}*"):
            status = await redis.hget(key, "status")
            if isinstance(status, bytes):
                status = status.decode("ascii")
            if status not in {"finished", "failed", "stopped", "canceled"}:
                live.add(key.decode() if isinstance(key, bytes) else str(key))
    members = list(await redis.lrange("rq:queue:news", 0, -1))
    for registry in ("rq:wip:news", "rq:scheduled:news", "rq:deferred:news"):
        members.extend(cast(list[bytes | str], await redis.zrange(registry, 0, -1)))
    for member in members:
        text = member.decode() if isinstance(member, bytes) else str(member)
        if text.startswith(prefixes):
            live.add(text)
    return sorted(live)


async def held_bundle_snapshot(
    session: AsyncSession, redis: Redis, candidate_id: UUID, *, lock: bool = False
) -> dict[str, Any]:
    """Capture every selected row/column, including full evidence and append-only history.

    ``lock`` is for ingestion's caller-owned transaction. PostgreSQL NOWAIT refuses a
    worker/editor rather than waiting and applying an old snapshot after they finish.
    Nested JSON is preserved verbatim; only mapped UUID/date/binary values are encoded.
    """

    async def rows(model: Any, condition: Any) -> list[dict[str, Any]]:
        statement = select(model).where(condition).execution_options(populate_existing=True)
        if lock:
            statement = statement.with_for_update(nowait=True)
        return sorted(
            (_held_row(row) for row in await session.scalars(statement)),
            key=lambda row: str(row["id"]),
        )

    with session.no_autoflush:
        candidates = await rows(NewsCandidate, NewsCandidate.id == candidate_id)
        if not candidates:
            raise AppError(404, "news_candidate_not_found", "找不到新聞候選")
        candidate = candidates[0]
        state: dict[str, Any] = {"candidate": candidate}
        state["source"] = await rows(NewsSource, NewsSource.id == UUID(candidate["source_id"]))
        for key, model in (
            ("evidence", NewsEvidence),
            ("runs", NewsPipelineRun),
            ("assessments", NewsAssessment),
            ("assets", NewsAsset),
        ):
            state[key] = await rows(model, model.candidate_id == candidate_id)
        article_id = candidate["guide_article_id"]
        article_condition = GuideArticle.id == UUID(article_id) if article_id else False
        state["article"] = await rows(GuideArticle, article_condition)
        state["locales"] = await rows(
            GuideArticleLocale,
            GuideArticleLocale.article_id == UUID(article_id) if article_id else False,
        )
        locale_ids = [UUID(row["id"]) for row in state["locales"]]
        state["revisions"] = await rows(
            GuideArticleRevision, GuideArticleRevision.article_locale_id.in_(locale_ids)
        )
        state["topics"] = await rows(
            GuideArticleTopic,
            GuideArticleTopic.article_id == UUID(article_id) if article_id else False,
        )
        targets = [f"news-candidate:{candidate_id}", f"news-source:{candidate['source_id']}"]
        if article_id:
            targets.extend(
                [
                    guide_target(UUID(article_id)),
                    *[guide_target(UUID(article_id), locale) for locale in LOCALES],
                ]
            )
        state["audits"] = await rows(AdminAuditLog, AdminAuditLog.target.in_(targets))
        state["live_jobs"] = await _held_live_jobs(redis, candidate_id)
    return {
        "schema": HELD_STATE_SCHEMA,
        "candidate_id": str(candidate_id),
        "captured_at": datetime.now(UTC).isoformat(),
        "state": state,
        "sha256": held_bundle_digest(state),
    }


def _legacy_navigation_url(url: str) -> bool:
    """Only known listing forms; a path under one of these listings is still an article.

    This is a conservative structural restriction, not proof that a retained page was
    non-evidence. The separate full-body review and saved-document guards supply that.
    """
    parts = urlsplit(url)
    if parts.scheme != "https" or parts.query or parts.fragment:
        return False
    roots = {
        "www.theverge.com": {
            "/news",
            "/policy",
            "/tech",
            "/gadgets",
            "/ai-artificial-intelligence",
        },
        "www.coindesk.com": {"/policy", "/newsletters", "/business", "/tech", "/markets"},
    }
    path = parts.path.rstrip("/")
    if parts.netloc in roots:
        return path in roots[parts.netloc]
    return (
        parts.netloc == "techcrunch.com"
        and re.fullmatch(r"/(?:category|tag)/[a-z0-9]+(?:-[a-z0-9]+)*", path) is not None
    )


def _navigation_reference_key(url: str) -> tuple[str, str] | None:
    """Treat ordinary publisher URL aliases as citations to the same listing."""
    try:
        parts = urlsplit(url)
        scheme = parts.scheme.lower()
        if scheme not in {"http", "https"} or parts.hostname is None:
            return None
        if parts.username is not None or parts.password is not None:
            return None
        if parts.port not in {None, 80 if scheme == "http" else 443}:
            return None
        return parts.hostname.lower(), parts.path.rstrip("/")
    except ValueError:
        return None


def _document_cites_navigation(value: object, urls: set[str]) -> bool:
    """Match complete links, including inline prose, without matching article descendants."""
    if isinstance(value, dict):
        return any(_document_cites_navigation(item, urls) for item in value.values())
    if isinstance(value, list):
        return any(_document_cites_navigation(item, urls) for item in value)
    if not isinstance(value, str):
        return False
    selected = {_navigation_reference_key(url) for url in urls}
    for token in re.findall(
        r"https?://[^\s<>\"'\[\]{}“”‘’「」『』«»]+", value, flags=re.IGNORECASE
    ):
        key = _navigation_reference_key(token.rstrip(".,;:!?。，；：！？)）"))
        if key is not None and key in selected:
            return True
    return False


async def repair_held_navigation(
    session: AsyncSession,
    redis: Redis,
    candidate_id: UUID,
    manifest: dict[str, Any],
    review: dict[str, Any],
    *,
    manifest_sha256: str,
    review_sha256: str,
    actor: User | None = None,
) -> dict[str, Any]:
    """Dry-run or remove explicitly reviewed legacy listings in the caller's transaction.

    Every removed row is archived in a genuine actor audit. Saved documents, claim text,
    sources, assets, append-only history and retry/judge caps remain unchanged. A changed
    evidence hash invalidates old review eligibility; this never fetches, approves,
    commits or queues anything. CLI intent and transaction handling are separate.
    """
    from app.auth.service import effective_admin_capabilities, user_is_suspended

    manifest_keys = {
        "schema",
        "candidate_id",
        "operation_id",
        "expected_snapshot",
        "review_sha256",
        "evidence_ids",
        "reason",
    }
    review_keys = {
        "schema",
        "candidate_id",
        "reviewer",
        "reviewed_at",
        "conclusion",
        "evidence_sha256",
        "documents_sha256",
        "claim_ledger_sha256",
        "navigation",
    }
    if (
        set(manifest) != manifest_keys
        or set(review) != review_keys
        or manifest["schema"] != "mokaair-news-held-navigation-repair-v1"
        or review["schema"] != "mokaair-news-held-navigation-review-v1"
        or manifest["candidate_id"] != str(candidate_id)
        or review["candidate_id"] != str(candidate_id)
        or manifest["review_sha256"] != review_sha256
        or not isinstance(manifest["reason"], str)
        or len(manifest["reason"].strip()) < 20
        or not isinstance(review["reviewer"], str)
        or not review["reviewer"].strip()
        or review["conclusion"] != "navigation_repair_only"
        or any(
            not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None
            for value in (manifest_sha256, review_sha256)
        )
    ):
        raise AppError(422, "news_navigation_manifest_invalid", "導航修補與獨立審查規格不符")
    try:
        operation_id = str(UUID(manifest["operation_id"]))
        reviewed_at = datetime.fromisoformat(review["reviewed_at"])
    except (ValueError, TypeError, AttributeError) as error:
        raise AppError(422, "news_navigation_manifest_invalid", "操作編號或審查時間不符") from error
    if (
        operation_id != manifest["operation_id"]
        or reviewed_at.tzinfo is None
        or not (0 <= (datetime.now(UTC) - reviewed_at).total_seconds() <= 86400)
    ):
        raise AppError(422, "news_navigation_manifest_invalid", "操作編號或審查時間不符")
    with session.no_autoflush:
        if actor is not None and (
            not actor.is_active
            or actor.deleted_at is not None
            or user_is_suspended(actor)
            or "content.manage" not in await effective_admin_capabilities(session, actor)
        ):
            raise AppError(403, "news_navigation_actor_required", "需要具內容管理權限的操作者")
        snapshot = await held_bundle_snapshot(session, redis, candidate_id, lock=actor is not None)
        state = snapshot["state"]
        expected = manifest["expected_snapshot"]
        if (
            not isinstance(expected, dict)
            or set(expected) != {"schema", "candidate_id", "captured_at", "state", "sha256"}
            or expected["schema"] != HELD_STATE_SCHEMA
            or expected["candidate_id"] != str(candidate_id)
        ):
            raise AppError(409, "news_navigation_state_changed", "完整修補快照不符")
        if (
            held_bundle_digest(expected["state"]) != expected["sha256"]
            or expected["sha256"] != snapshot["sha256"]
        ):
            raise AppError(409, "news_navigation_state_changed", "候選、來源或完整歷史已變更")
        try:
            captured = datetime.fromisoformat(expected["captured_at"])
        except (ValueError, TypeError) as error:
            raise AppError(409, "news_navigation_snapshot_expired", "修補快照已過期") from error
        if (
            captured.tzinfo is None
            or not 0 <= (datetime.now(UTC) - captured).total_seconds() <= 900
        ):
            raise AppError(409, "news_navigation_snapshot_expired", "修補快照已過期")
        candidate = state["candidate"]
        if (
            candidate["status"] not in {"manual_review", "shadow_review"}
            or candidate["guide_article_id"] is None
            or candidate["published_at"] is not None
            or state["live_jobs"]
            or any(row["status"] == "running" for row in state["runs"])
            or len(state["source"]) != 1
            or not state["source"][0]["enabled"]
            or state["source"][0]["scan_lock_until"] is not None
            or len(state["article"]) != 1
            or len(state["locales"]) != len(LOCALES)
            or {row["locale"] for row in state["locales"]} != set(LOCALES)
            or any(
                row["published_version"] is not None or row["published_at"] is not None
                for row in state["locales"]
            )
        ):
            raise AppError(
                409, "news_navigation_busy", "候選必須保留五語草稿且沒有發布或執行中的工作"
            )
        started = candidate["processing_started_at"]
        if started is not None and not any(
            row["status"] in {"succeeded", "failed"}
            and row["finished_at"] is not None
            and datetime.fromisoformat(started)
            <= datetime.fromisoformat(row["finished_at"])
            <= datetime.now(UTC)
            for row in state["runs"]
        ):
            raise AppError(409, "news_navigation_busy", "缺少原生工作的完成紀錄")
        if any(row["action"] == "news_navigation_evidence_repaired" for row in state["audits"]):
            raise AppError(409, "news_navigation_operation_used", "已有修補紀錄；請先讀取原收據")
        ids = manifest["evidence_ids"]
        if (
            not isinstance(ids, list)
            or not ids
            or any(type(value) is not str for value in ids)
            or len(set(ids)) != len(ids)
        ):
            raise AppError(422, "news_navigation_selection_invalid", "需要不重複的精確證據編號")
        chosen = [row for row in state["evidence"] if row["id"] in ids]
        retained = [row for row in state["evidence"] if row["id"] not in ids]
        if (
            len(chosen) != len(ids)
            or not retained
            or not any(row["url"] == candidate["canonical_url"] for row in retained)
        ):
            raise AppError(422, "news_navigation_selection_invalid", "必須保留原始報導與實際證據")
        urls = {row["url"] for row in chosen}
        site = urlsplit(candidate["canonical_url"]).hostname
        if any(
            not _legacy_navigation_url(row["url"])
            or urlsplit(row["url"]).hostname != site
            or row["is_first_party"]
            for row in chosen
        ):
            raise AppError(422, "news_navigation_not_listing", "只能處理已獨立確認的同站導覽頁")
        documents = {
            row["locale"]: GuideDocument.model_validate(row["draft_json"]).model_dump(mode="json")
            for row in state["locales"]
        }
        if any(_document_cites_navigation(document, urls) for document in documents.values()):
            raise AppError(
                409, "news_navigation_still_cited", "先透過原有草稿編輯修正仍被引用的導航頁"
            )
        # Historical claims remain authoritative provenance, even after a draft edit.
        # This repair cannot remove any URL they cite or rewrite the ledger itself.
        ledger = candidate["claim_ledger_json"]
        if not isinstance(ledger, list) or any(not isinstance(claim, dict) for claim in ledger):
            raise AppError(422, "news_navigation_review_mismatch", "主張來源規格不符")
        for claim in ledger:
            claim_urls = claim.get("source_urls", [])
            if not isinstance(claim_urls, list) or any(type(url) is not str for url in claim_urls):
                raise AppError(422, "news_navigation_review_mismatch", "主張來源規格不符")
            if _document_cites_navigation(claim_urls, urls):
                raise AppError(409, "news_navigation_claim_source", "導航頁仍被原始主張紀錄引用")
        document_hashes = {
            locale: held_bundle_digest(document) for locale, document in documents.items()
        }
        if (
            review["evidence_sha256"] != held_bundle_digest(state["evidence"])
            or held_bundle_digest(review["documents_sha256"]) != held_bundle_digest(document_hashes)
            or review["claim_ledger_sha256"] != held_bundle_digest(candidate["claim_ledger_json"])
            or not isinstance(review["navigation"], list)
            or len(review["navigation"]) != len(chosen)
        ):
            raise AppError(
                422, "news_navigation_review_mismatch", "獨立審查未綁定完整來源、主張與五語草稿"
            )
        proofs = review["navigation"]
        if any(
            not isinstance(proof, dict)
            or set(proof)
            != {
                "evidence_id",
                "url",
                "classification",
                "excerpt_sha256",
                "reason",
                "current_source",
                "current_source_sha256",
                "source_artifact_sha256",
            }
            or type(proof["evidence_id"]) is not str
            for proof in proofs
        ):
            raise AppError(422, "news_navigation_review_mismatch", "每個導航頁需要完整獨立判斷")
        by_id = {proof["evidence_id"]: proof for proof in proofs}
        if len(by_id) != len(proofs) or set(by_id) != set(ids):
            raise AppError(422, "news_navigation_review_mismatch", "導航頁審查編號不符")
        for row in chosen:
            proof = by_id[row["id"]]
            if (
                not isinstance(row["excerpt"], str)
                or not row["excerpt"].strip()
                or not isinstance(proof["source_artifact_sha256"], str)
                or re.fullmatch(r"[0-9a-f]{64}", proof["source_artifact_sha256"]) is None
                or not isinstance(proof["current_source"], dict)
                or proof["current_source_sha256"] != held_bundle_digest(proof["current_source"])
                or proof["url"] != row["url"]
                or proof["classification"] != "system_navigation"
                or proof["excerpt_sha256"] != hashlib.sha256(row["excerpt"].encode()).hexdigest()
                or not isinstance(proof["reason"], str)
                or len(proof["reason"].strip()) < 20
            ):
                raise AppError(422, "news_navigation_review_mismatch", "導航頁全文或判斷不符")
            current = proof["current_source"]
            if (
                set(current) != {"url", "resolved_url", "fetched_at", "status", "title", "excerpt"}
                or current["url"] != row["url"]
                or type(current["status"]) is not int
                or current["status"] != 200
                or not isinstance(current["resolved_url"], str)
                or current["resolved_url"].rstrip("/") != row["url"].rstrip("/")
                or not isinstance(current["title"], str)
                or not current["title"].strip()
                or not isinstance(current["excerpt"], str)
                or not current["excerpt"].strip()
            ):
                raise AppError(422, "news_navigation_review_mismatch", "需要可讀的當前導航頁全文")
            try:
                fetched_at = datetime.fromisoformat(current["fetched_at"])
            except (ValueError, TypeError) as error:
                raise AppError(
                    422, "news_navigation_review_mismatch", "來源讀取時間不符"
                ) from error
            if (
                fetched_at.tzinfo is None
                or not 0 <= (reviewed_at - fetched_at).total_seconds() <= 86400
            ):
                raise AppError(422, "news_navigation_review_mismatch", "來源讀取時間不符")
        new_evidence_hash = evidence_fingerprint(retained)
        plan = {
            "candidate_id": str(candidate_id),
            "operation_id": operation_id,
            "before_sha256": snapshot["sha256"],
            "removed_evidence": chosen,
            "retained_evidence": retained,
            "before_evidence_hash": candidate["evidence_hash"],
            "after_evidence_hash": new_evidence_hash,
            "documents_sha256": document_hashes,
            "fresh_verification_required": True,
            "model_calls": 0,
            "queue_calls": 0,
            "applied": False,
        }
        if actor is None:
            return plan
        row = await session.get(NewsCandidate, candidate_id, populate_existing=True)
        assert row is not None
        for item in await session.scalars(
            select(NewsEvidence).where(NewsEvidence.id.in_([UUID(value) for value in ids]))
        ):
            await session.delete(item)
        row.evidence_hash = new_evidence_hash
        row.would_publish = False
        row.error_code = "news_navigation_evidence_repaired"
        row.error_detail = "已封存並移除獨立確認的舊導航證據；需要重新查核五語草稿"
        audit(
            session,
            actor,
            "news_navigation_evidence_repaired",
            f"news-candidate:{candidate_id}",
            operation_id=operation_id,
            manifest_sha256=manifest_sha256,
            review_sha256=review_sha256,
            reviewer=review["reviewer"],
            reason=manifest["reason"],
            before_candidate=candidate,
            before_source=state["source"],
            before_evidence=state["evidence"],
            after_evidence=retained,
            before_snapshot_sha256=snapshot["sha256"],
            documents_sha256=document_hashes,
            claim_ledger=candidate["claim_ledger_json"],
            navigation_review=proofs,
            fresh_verification_required=True,
            queue_calls=0,
        )
        await session.flush()
        after = await held_bundle_snapshot(session, redis, candidate_id, lock=True)
        for key in state:
            if key not in {"candidate", "evidence", "audits"} and held_bundle_digest(
                state[key]
            ) != held_bundle_digest(after["state"][key]):
                raise AppError(409, "news_navigation_state_changed", "修補期間其他完整狀態已變更")
        if held_bundle_digest(retained) != held_bundle_digest(after["state"]["evidence"]):
            raise AppError(409, "news_navigation_state_changed", "保留來源有非預期變更")
        changed = after["state"]["candidate"]
        allowed = {"evidence_hash", "would_publish", "error_code", "error_detail", "updated_at"}
        if any(
            held_bundle_digest(candidate[key]) != held_bundle_digest(changed[key])
            for key in candidate
            if key not in allowed
        ):
            raise AppError(409, "news_navigation_state_changed", "候選有非預期變更")
        old_audits = {item["id"]: item for item in state["audits"]}
        new_audits = {item["id"]: item for item in after["state"]["audits"]}
        if len(new_audits) != len(old_audits) + 1 or any(
            held_bundle_digest(new_audits.get(key)) != held_bundle_digest(value)
            for key, value in old_audits.items()
        ):
            raise AppError(409, "news_navigation_state_changed", "原始審核紀錄有非預期變更")
        return {**plan, "applied": True, "after_snapshot": after}


async def ingest_held_bundle(
    session: AsyncSession,
    redis: Redis,
    candidate_id: UUID,
    manifest: dict[str, Any],
    review: dict[str, Any],
    *,
    manifest_sha256: str,
    review_sha256: str,
    actor: User | None = None,
) -> dict[str, Any]:
    """Validate, or atomically save an owner-authored five-language draft.

    Actor None is a read-only dry run. A review is a dated, trusted administrator's
    provenance document, never a model assessment or permission to publish. The CLI
    pins its raw bytes and records a durable intent before calling the write path.
    Caller must commit once on success and roll back any exception. Original cached
    drafts, status, errors, decisions, retry count and judge history remain untouched.
    """
    from app.auth.service import effective_admin_capabilities
    from app.news_automation.pipeline import _save_guide_bundle

    required = {
        "schema",
        "candidate_id",
        "operation_id",
        "slug",
        "event_date",
        "expected_snapshot",
        "documents",
        "review_sha256",
    }
    if set(manifest) != required or manifest["schema"] != HELD_BUNDLE_SCHEMA:
        raise AppError(422, "news_ingestion_manifest_invalid", "草稿匯入規格不符")
    if manifest["candidate_id"] != str(candidate_id):
        raise AppError(422, "news_ingestion_candidate_mismatch", "候選與內容包不符")
    operation_id = str(UUID(manifest["operation_id"]))
    if operation_id != manifest["operation_id"] or manifest["review_sha256"] != review_sha256:
        raise AppError(422, "news_ingestion_review_mismatch", "審稿收據或操作編號不符")
    if any(
        len(value) != 64 or any(c not in "0123456789abcdef" for c in value)
        for value in (manifest_sha256, review_sha256)
    ):
        raise AppError(422, "news_ingestion_digest_invalid", "檔案雜湊不符")
    with session.no_autoflush:
        if actor is not None and (
            not actor.is_active
            or "content.manage" not in await effective_admin_capabilities(session, actor)
        ):
            raise AppError(403, "news_ingestion_actor_required", "需要具內容管理權限的操作者")
        snapshot = await held_bundle_snapshot(session, redis, candidate_id, lock=actor is not None)
        state = snapshot["state"]
        previous = [
            row
            for row in state["audits"]
            if row["action"] == HELD_INGESTION_ACTION
            and row["metadata_json"].get("operation_id") == operation_id
        ]
        if previous:
            # No implicit replay, even when the caller knows a previous save completed.
            raise AppError(409, "news_ingestion_operation_used", "此操作已有保存紀錄；請讀取原收據")
        expected = manifest["expected_snapshot"]
        if (
            set(expected) != {"schema", "candidate_id", "captured_at", "state", "sha256"}
            or expected["schema"] != HELD_STATE_SCHEMA
            or expected["candidate_id"] != str(candidate_id)
            or held_bundle_digest(expected["state"]) != expected["sha256"]
            or held_bundle_digest(expected["state"]) != snapshot["sha256"]
        ):
            raise AppError(409, "news_ingestion_state_changed", "候選、來源或完整歷史已變更")
        captured = datetime.fromisoformat(expected["captured_at"])
        if (
            captured.tzinfo is None
            or not 0 <= (datetime.now(UTC) - captured).total_seconds() <= 900
        ):
            raise AppError(409, "news_ingestion_snapshot_expired", "匯入快照已過期")
        candidate_state = state["candidate"]
        if (
            candidate_state["status"] not in HELD_INGESTION_STATUSES
            or candidate_state["published_at"] is not None
            or state["live_jobs"]
            or any(row["status"] == "running" for row in state["runs"])
        ):
            raise AppError(409, "news_ingestion_busy", "候選已發布或仍有工作執行中")
        processing_started = candidate_state["processing_started_at"]
        if processing_started is not None:
            # Native holds retain the original claim clock. Require a completed native
            # run after that clock; a bare clock is not proof that its worker stopped.
            started = datetime.fromisoformat(processing_started)
            now = datetime.now(UTC)
            if started > now or not any(
                row["status"] in {"succeeded", "failed"}
                and row["finished_at"] is not None
                and started <= datetime.fromisoformat(row["finished_at"]) <= now
                for row in state["runs"]
            ):
                raise AppError(409, "news_ingestion_busy", "處理時間缺少已完成的原生工作紀錄")
        if len(state["source"]) != 1 or state["source"][0]["scan_lock_until"] is not None:
            raise AppError(409, "news_ingestion_source_busy", "来源不存在或掃描尚未結束")
        if candidate_state["guide_article_id"] is not None:
            raise AppError(409, "news_ingestion_guide_exists", "已有文章；請使用原有草稿編輯流程")
        if article_slug(manifest["slug"]) != manifest["slug"] or len(manifest["slug"]) > 120:
            raise AppError(422, "news_ingestion_slug_invalid", "文章網址代稱不符")
        if manifest["slug"] in admin_service.RESERVED_SLUGS:
            raise AppError(422, "news_ingestion_slug_invalid", "文章網址代稱已保留")
        if set(manifest["documents"]) != set(LOCALES):
            raise AppError(422, "news_locale_bundle_incomplete", "五個語言版本必須完整")
        documents = {
            cast(Locale, locale): GuideDocument.model_validate(value)
            for locale, value in manifest["documents"].items()
        }
        evidence = [row for row in state["evidence"] if row["role"] == "evidence"]
        if not evidence:
            raise AppError(422, "news_evidence_insufficient", "缺少保存的來源證據")
        source_refs = sorted(
            [
                {"title": row["title"], "url": row["url"], "checked_on": row["retrieved_at"][:10]}
                for row in evidence
            ],
            key=lambda row: row["url"],
        )
        pending: dict[str, list[str]] = {}
        for locale, document in documents.items():
            admin_service._validate_document(document, None)
            if (
                sorted(
                    [item.model_dump(mode="json") for item in document.sources],
                    key=lambda row: row["url"],
                )
                != source_refs
            ):
                raise AppError(422, "news_ingestion_source_mismatch", "草稿來源與保存證據不符")
            problems = hard_policy_problems(
                document,
                cast(Vertical, candidate_state["vertical"]),
                locale,
                source_count=len({row["url"] for row in evidence}),
            )
            if any(not problem.startswith("no_hero:") for problem in problems):
                raise AppError(422, "news_ingestion_policy_failed", "; ".join(problems))
            pending[locale] = problems
        event_day = date.fromisoformat(manifest["event_date"])
        if candidate_state["event_date"] != event_day.isoformat() or event_date_problems(
            event_day,
            manifest["slug"],
            [
                date.fromisoformat(row["source_date"] or row["retrieved_at"][:10])
                for row in evidence
            ],
        ):
            raise AppError(422, "news_event_date_invalid", "日期與候選或來源不符")
        document_sha = {
            locale: held_bundle_digest(doc.model_dump(mode="json"))
            for locale, doc in documents.items()
        }
        review_keys = {
            "schema",
            "candidate_id",
            "reviewer",
            "reviewed_at",
            "conclusion",
            "documents_sha256",
            "evidence_sha256",
            "candidate_evidence_hash",
            "blocking_content_problems",
            "pending_policy_problems",
        }
        if (
            set(review) != review_keys
            or review["schema"] != HELD_REVIEW_SCHEMA
            or review["candidate_id"] != str(candidate_id)
            or not isinstance(review["reviewer"], str)
            or not review["reviewer"].strip()
            or review["conclusion"] != "draft_ingestion_only"
            or review["blocking_content_problems"] != []
            or held_bundle_digest(review["documents_sha256"]) != held_bundle_digest(document_sha)
            or review["evidence_sha256"] != held_bundle_digest(state["evidence"])
            or review["candidate_evidence_hash"] != candidate_state["evidence_hash"]
            or held_bundle_digest(review["pending_policy_problems"]) != held_bundle_digest(pending)
        ):
            raise AppError(422, "news_ingestion_review_mismatch", "審稿收據未綁定五稿與完整來源")
        reviewed = datetime.fromisoformat(review["reviewed_at"])
        if reviewed.tzinfo is None or reviewed > datetime.now(UTC):
            raise AppError(422, "news_ingestion_review_mismatch", "審稿時間不符")
        result = {
            "candidate_id": str(candidate_id),
            "operation_id": operation_id,
            "applied": False,
            "committed": False,
            "saved_in_transaction": False,
            "documents_sha256": document_sha,
            "pending_policy_problems": pending,
            "approval": False,
            "queued": 0,
            "model_calls": 0,
            "publication_verified": False,
        }
        if actor is None:
            return result
        if await _held_live_jobs(redis, candidate_id):
            raise AppError(409, "news_ingestion_busy", "候選仍有佇列工作")
        candidate = await session.get(NewsCandidate, candidate_id)
        assert candidate is not None
        provenance = {
            "operation_id": operation_id,
            "manifest_sha256": manifest_sha256,
            "review_sha256": review_sha256,
            "reviewer": review["reviewer"],
            "reviewed_at": review["reviewed_at"],
            "before_sha256": snapshot["sha256"],
            "evidence_sha256": review["evidence_sha256"],
            "author_kind": "owner",
            "held_retry_count": candidate.retry_count,
            "documents_sha256": document_sha,
            "pending_policy_problems": pending,
        }
        article, versions = await _save_guide_bundle(
            session,
            candidate,
            manifest["slug"],
            event_day,
            documents,
            actor=actor,
            provenance=provenance,
            commit=False,
        )
        audit(
            session,
            actor,
            HELD_INGESTION_ACTION,
            f"news-candidate:{candidate_id}",
            **provenance,
            article_id=str(article.id),
            locale_versions=versions,
            candidate_evidence_hash=candidate.evidence_hash,
            document_fingerprints={
                locale: document_fingerprint(doc) for locale, doc in documents.items()
            },
        )
        await session.flush()
        return {
            **result,
            "saved_in_transaction": True,
            "article_id": str(article.id),
            "locale_versions": versions,
        }


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
    # An empty model means the guide search's model for that vendor, else the planner's,
    # as configured in the admin AI settings; the job resolves it the same way.
    runtime = await load_runtime_settings(session)
    return SettingsView(
        enabled=row.enabled,
        mode=cast(Any, row.mode),
        writer_provider=cast(Any, row.writer_provider),
        writer_model=row.writer_model,
        verifier_provider=cast(Any, row.verifier_provider),
        verifier_model=row.verifier_model,
        editor_provider=cast(Any, row.editor_provider),
        editor_model=row.editor_model,
        judge_enabled=row.judge_enabled,
        judge_provider=cast(Any, row.judge_provider),
        judge_model=row.judge_model,
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
        model_options=model_options(),
        default_models={
            provider: research_model(runtime, provider) for provider in MODEL_CAPABILITY
        },
        updated_at=row.updated_at,
    )


async def update_models(session: AsyncSession, actor: User, payload: ModelsWrite) -> SettingsView:
    """Change only the writer, verifier, final editor and judge models, through a settings save."""
    current = await settings_view(session)
    # The judge's switch is the news page's, and a page loaded before the judge existed names
    # no judge vendor. What this save does not choose is left out of it, so update_settings
    # keeps it from the row it locks.
    left_out = {"judge_enabled"}
    if "judge_provider" not in payload.model_fields_set:
        left_out |= {"judge_provider", "judge_model"}
    chosen = payload.model_dump(exclude=left_out)
    if chosen == current.model_dump(include=set(chosen)):
        return current
    stored = current.model_dump(include=set(SettingsWrite.model_fields) - left_out)
    settings = SettingsWrite.model_validate({**stored, **chosen})
    return await update_settings(session, actor, settings)


async def update_settings(
    session: AsyncSession, actor: User, payload: SettingsWrite
) -> SettingsView:
    row = await settings_row(session, lock=True)
    # What the agreement figures measure: the three roles every story runs through and the
    # two versions. The judge decides after them, so a change of judge restarts nothing.
    before = {
        "writer_provider": row.writer_provider,
        "writer_model": row.writer_model,
        "verifier_provider": row.verifier_provider,
        "verifier_model": row.verifier_model,
        "editor_provider": row.editor_provider,
        "editor_model": row.editor_model,
        "prompt_version": row.prompt_version,
        "policy_version": row.policy_version,
    }
    values = payload.model_dump()
    # Models left out of the payload keep their stored value (see SettingsWrite), the judge's
    # among them, and so does the judge's switch.
    for key in set(ModelsWrite.model_fields) - payload.sent_models():
        values[key] = getattr(row, key)
    if values["judge_enabled"] is None:
        values["judge_enabled"] = row.judge_enabled
    major_change = any(values[key] != value for key, value in before.items())
    # The owner removed the shadow gate on 2026-09-25: the final editor and Jev's last call
    # decide each article, so auto-publish no longer waits for labelled days, and a model
    # change no longer switches it off. The agreement figures still restart, for reference.
    if major_change:
        for vertical in ("ai", "tech", "crypto"):
            setattr(row, f"shadow_started_at_{vertical}", datetime.now(UTC))
    for vertical in ("ai", "tech", "crypto"):
        if values[f"auto_publish_{vertical}"] and values["mode"] != "automatic":
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
        judge_enabled=values["judge_enabled"],
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
        judge_decision=cast(Any, row.judge_decision),
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
    status: list[str] | None = None,
    vertical: Vertical | None = None,
) -> CandidatePage:
    criteria: list[Any] = []
    if status:
        criteria.append(NewsCandidate.status.in_(status))
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
    waiting_on_duplicate = row.status == "manual_review" and row.error_code == DUPLICATE_UNCERTAIN
    article = (
        await session.get(GuideArticle, row.guide_article_id)
        if row.guide_article_id is not None
        else None
    )
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
        similar_titles=await similar_titles(session, row) if waiting_on_duplicate else [],
        article_slug=article.slug if article is not None else None,
        article_kind=cast(Kind, article.kind) if article is not None else None,
    )


async def reject_candidate(
    session: AsyncSession, actor: User, candidate_id: UUID, payload: CandidateAction
) -> CandidateDetail:
    row = await session.get(NewsCandidate, candidate_id, with_for_update=True)
    if row is None:
        raise AppError(404, "news_candidate_not_found", "找不到新聞候選")
    if row.status not in {
        "manual_review",
        "shadow_review",
        "needs_evidence",
        "needs_redraft",
        "failed",
        "duplicate",
    }:
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
    if row.error_code == "news_navigation_evidence_repaired":
        raise AppError(409, "news_candidate_not_refreshable", "先更新修補後保留的來源")
    if row.status not in {
        "manual_review",
        "shadow_review",
        "needs_evidence",
        "needs_redraft",
        "failed",
    }:
        raise AppError(409, "news_candidate_not_retryable", "這個候選目前不能重跑")
    _queue_new_draft(row, payload.reason)
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
    row = await session.get(
        NewsCandidate, candidate_id, with_for_update=True, populate_existing=True
    )
    if row is None:
        raise AppError(404, "news_candidate_not_found", "找不到新聞候選")
    if row.error_code == "news_navigation_evidence_repaired":
        raise AppError(409, "news_candidate_not_refreshable", "先更新修補後保留的來源")
    ingested_redraft = row.status == "needs_redraft" and await _ingested_bundle_available(
        session, row
    )
    if row.status not in {"manual_review", "shadow_review", "failed"} and not ingested_redraft:
        raise AppError(409, "news_candidate_not_retryable", "這個候選目前不能重新查核")
    await _queue_reverify(session, row, payload.reason)
    handoff = await _held_ingestion_handoff(session, row)
    audit(
        session,
        actor,
        "news_candidate_reverify_requested",
        f"news-candidate:{row.id}",
        reason=payload.reason,
        retry_count=row.retry_count,
        **handoff,
    )
    await session.commit()
    return await candidate_detail(session, row.id)


async def _held_ingestion_audit(session: AsyncSession, row: NewsCandidate) -> AdminAuditLog | None:
    """A durable native owner save fence, even if its Guide is later edited."""
    if row.guide_article_id is None:
        return None
    with session.no_autoflush:
        saved = await session.scalar(
            select(AdminAuditLog)
            .where(
                AdminAuditLog.target == f"news-candidate:{row.id}",
                AdminAuditLog.action == HELD_INGESTION_ACTION,
            )
            .order_by(AdminAuditLog.created_at.desc(), AdminAuditLog.id.desc())
            .limit(1)
        )
    if (
        saved is None
        or saved.actor_user_id is None
        or saved.metadata_json.get("system_actor") is not False
        or saved.metadata_json.get("author_kind") != "owner"
        or saved.metadata_json.get("article_id") != str(row.guide_article_id)
    ):
        return None
    return saved


async def _held_ingestion_handoff(session: AsyncSession, row: NewsCandidate) -> dict[str, object]:
    saved = await _held_ingestion_audit(session, row)
    return (
        {"held_ingestion_audit_id": str(saved.id), "article_id": str(row.guide_article_id)}
        if saved is not None
        else {}
    )


async def _held_ingestion_pending(session: AsyncSession, row: NewsCandidate) -> bool:
    """Only a committed native reverify/refresh handoff ends the initial draft fence.

    A late scheduler/judge job or a marker alone cannot replace the reviewed bundle.
    Once handed off, the owner's later ordinary retry keeps its existing behaviour.
    """
    saved = await _held_ingestion_audit(session, row)
    if saved is None:
        return False
    held_retry = saved.metadata_json.get("held_retry_count")
    if type(held_retry) is not int:
        return True
    with session.no_autoflush:
        handoffs = await session.scalars(
            select(AdminAuditLog).where(
                AdminAuditLog.target == saved.target,
                AdminAuditLog.action.in_(
                    ("news_candidate_reverify_requested", "news_candidate_evidence_refreshed")
                ),
                AdminAuditLog.created_at >= saved.created_at,
                AdminAuditLog.actor_user_id.is_not(None),
            )
        )
        for handoff in handoffs:
            metadata = handoff.metadata_json
            retry = metadata.get("retry_count")
            if (
                metadata.get("system_actor") is False
                and metadata.get("held_ingestion_audit_id") == str(saved.id)
                and metadata.get("article_id") == str(row.guide_article_id)
                and type(retry) is int
                and held_retry < retry <= row.retry_count
            ):
                return False
    return True


async def _ingested_bundle_available(session: AsyncSession, row: NewsCandidate) -> bool:
    """One narrow route out of a missing-Guide hold, through ordinary fresh reverify.

    Require the genuine actor-owned native save, all five current whole documents and
    versions, and their actual revision rows. No editorial-fingerprint exemptions, asset
    edits, partial cache, review declaration or automatic draft run can grant this route.
    """
    saved = await _held_ingestion_audit(session, row)
    if saved is None:
        return False
    metadata = saved.metadata_json
    if (
        metadata.get("article_id") != str(row.guide_article_id)
        or metadata.get("candidate_evidence_hash") != row.evidence_hash
    ):
        return False
    article = await session.scalar(
        select(GuideArticle)
        .where(GuideArticle.id == row.guide_article_id)
        .with_for_update(nowait=True)
        .execution_options(populate_existing=True)
    )
    if article is None:
        return False
    locales = list(
        await session.scalars(
            select(GuideArticleLocale)
            .where(GuideArticleLocale.article_id == row.guide_article_id)
            .order_by(GuideArticleLocale.locale, GuideArticleLocale.id)
            .with_for_update(nowait=True)
            .execution_options(populate_existing=True)
        )
    )
    if {item.locale for item in locales} != set(LOCALES):
        return False
    versions = {item.locale: item.version for item in locales}
    hashes = {item.locale: held_bundle_digest(item.draft_json) for item in locales}
    if (
        any(item.published_version is not None for item in locales)
        or held_bundle_digest(versions) != held_bundle_digest(metadata.get("locale_versions"))
        or held_bundle_digest(hashes) != held_bundle_digest(metadata.get("documents_sha256"))
    ):
        return False
    for item in locales:
        revision = await session.scalar(
            select(GuideArticleRevision).where(
                GuideArticleRevision.article_locale_id == item.id,
                GuideArticleRevision.version == item.version,
            )
        )
        if (
            revision is None
            or revision.action != "created"
            or revision.created_by_user_id != saved.actor_user_id
            or held_bundle_digest(revision.document_json) != hashes[item.locale]
        ):
            return False
    return True


async def refresh_candidate_evidence(
    session: AsyncSession,
    actor: User,
    candidate_id: UUID,
    payload: CandidateAction,
    redis: Redis | None = None,
) -> CandidateDetail:
    """Re-check a candidate held for changed evidence against the current pages.

    Each evidence page is fetched again and its current text replaces the stored excerpt and
    hash. The saved five-locale article then goes through the fact check, the locale reviews
    and Jev's last call again, against the new text; the old verification no longer matches
    the evidence, so nothing can be published on it. A story already judged distinct stays
    distinct: that decision is carried to the new evidence.
    """

    try:
        row = await session.get(
            NewsCandidate,
            candidate_id,
            with_for_update={"nowait": True},
            populate_existing=True,
        )
    except DBAPIError as error:
        sqlstate = getattr(error.orig, "sqlstate", None) or getattr(
            error.orig, "pgcode", None
        )
        if sqlstate != "55P03":
            raise
        await session.rollback()
        raise AppError(
            409, "news_navigation_refresh_busy", "來源修補仍有編輯或處理中的工作"
        ) from error
    if row is None:
        raise AppError(404, "news_candidate_not_found", "找不到新聞候選")
    if (
        row.status != "manual_review"
        or row.error_code not in {"news_evidence_changed", "news_navigation_evidence_repaired"}
        or row.guide_article_id is None
    ):
        raise AppError(409, "news_candidate_not_refreshable", "這個候選不是在等來源更新")
    repair: dict[str, Any] | None = None
    before_evidence: list[dict[str, Any]] | None = None
    if row.error_code == "news_navigation_evidence_repaired":
        if redis is None:
            raise AppError(409, "news_navigation_refresh_unavailable", "無法確認修補工作是否完成")
        # The repair is a separate, committed operation. Lock its complete held state
        # before fetching retained pages so an editor, worker or another refresh cannot
        # turn the saved receipt into an authorization for a different evidence set.
        try:
            snapshot = await held_bundle_snapshot(session, redis, candidate_id, lock=True)
        except DBAPIError as error:
            sqlstate = getattr(error.orig, "sqlstate", None) or getattr(
                error.orig, "pgcode", None
            )
            if sqlstate != "55P03":
                raise
            await session.rollback()
            raise AppError(
                409, "news_navigation_refresh_busy", "來源修補仍有編輯或處理中的工作"
            ) from error
        state = snapshot["state"]
        repairs = [
            item for item in state["audits"]
            if item["target"] == f"news-candidate:{candidate_id}"
            and item["action"] == "news_navigation_evidence_repaired"
            and item["actor_user_id"] is not None
            and item["metadata_json"].get("system_actor") is False
        ]
        if len(repairs) != 1:
            raise AppError(409, "news_navigation_receipt_missing", "找不到有效的人工導航修補紀錄")
        repair = repairs[0]
        receipt = repair["metadata_json"]
        before = receipt.get("before_evidence")
        retained = receipt.get("after_evidence")
        current = state["evidence"]
        if (
            not isinstance(before, list)
            or not isinstance(retained, list)
            or not all(
                isinstance(item, dict)
                and isinstance(item.get("id"), str)
                and isinstance(item.get("url"), str)
                for item in before
            )
            or not all(
                isinstance(item, dict)
                and isinstance(item.get("id"), str)
                and isinstance(item.get("url"), str)
                for item in retained
            )
            or not retained
            or len({item["id"] for item in before}) != len(before)
            or len({item["id"] for item in retained}) != len(retained)
            or not {item["id"] for item in retained} < {item["id"] for item in before}
            or held_bundle_digest(retained) != held_bundle_digest(current)
            or row.evidence_hash != evidence_fingerprint(current)
            or receipt.get("fresh_verification_required") is not True
            or receipt.get("queue_calls") != 0
        ):
            raise AppError(409, "news_navigation_receipt_mismatch", "保留來源或修補收據已變更")
        retained_ids = {item["id"] for item in retained}
        removed_urls = {
            item["url"] for item in before
            if item["id"] not in retained_ids
        }
        if (
            state["live_jobs"]
            or any(item["status"] == "running" for item in state["runs"])
            or len(state["source"]) != 1
            or not state["source"][0]["enabled"]
            or state["source"][0]["scan_lock_until"] is not None
            or state["candidate"]["published_at"] is not None
            or state["candidate"]["would_publish"]
            or len(state["locales"]) != len(LOCALES)
            or {item["locale"] for item in state["locales"]} != set(LOCALES)
            or any(
                item["published_version"] is not None or item["published_at"] is not None
                for item in state["locales"]
            )
        ):
            raise AppError(409, "news_navigation_refresh_busy", "來源修補仍有工作或五語草稿不完整")
        documents = [
            GuideDocument.model_validate(item["draft_json"]).model_dump(mode="json")
            for item in state["locales"]
        ]
        if (
            any(_document_cites_navigation(document, removed_urls) for document in documents)
            or _document_cites_navigation(state["candidate"]["claim_ledger_json"], removed_urls)
        ):
            raise AppError(409, "news_navigation_still_cited", "五語草稿或主張仍引用已移除的導航頁")
        if held_bundle_digest(receipt.get("claim_ledger")) != held_bundle_digest(
            state["candidate"]["claim_ledger_json"]
        ):
            raise AppError(409, "news_navigation_receipt_mismatch", "原始主張紀錄已變更")
        before_evidence = current
    evidence_query = select(NewsEvidence).where(NewsEvidence.candidate_id == row.id)
    if repair is not None:
        evidence_query = evidence_query.with_for_update(nowait=True).execution_options(
            populate_existing=True
        )
    evidence = list(await session.scalars(evidence_query))
    previous_hash = row.evidence_hash
    distinct = (
        await session.scalar(
            select(NewsAssessment.id)
            .where(
                NewsAssessment.candidate_id == row.id,
                # Jev's or an editor's answer, or the judge's: "pass" is the verdict the
                # judge stores for "not a duplicate" and for nothing else.
                NewsAssessment.assessment_type.in_(("duplicate", "judge")),
                NewsAssessment.verdict == "pass",
                NewsAssessment.evidence_hash == previous_hash,
            )
            .limit(1)
        )
        is not None
    )
    changed, problems = await refresh_evidence(
        session,
        evidence,
        rate_limiter=RedisHostRateLimiter(redis) if redis is not None else None,
    )
    if problems:
        await session.rollback()
        raise AppError(
            409, "news_evidence_refresh_failed", "無法讀取最新來源：" + "; ".join(problems[:3])
        )
    row.evidence_hash = evidence_fingerprint(
        [{"url": item.url, "content_hash": item.content_hash} for item in evidence]
    )
    if distinct:
        session.add(
            NewsAssessment(
                candidate_id=row.id,
                assessment_type="duplicate",
                verdict="pass",
                provider=HUMAN_PROVIDER,
                reasons_json=[payload.reason],
                details_json={"basis": "evidence_refreshed", "previous_evidence": previous_hash},
                evidence_hash=row.evidence_hash,
                prompt_version=row.prompt_version,
                created_by_user_id=actor.id,
            )
        )
    await _queue_reverify(session, row, payload.reason, marker=EVIDENCE_REFRESH_MARKER)
    handoff = await _held_ingestion_handoff(session, row)
    repair_metadata: dict[str, Any] = {}
    if repair is not None:
        repair_metadata = {
            "navigation_repair_audit_id": repair["id"],
            "before_evidence": before_evidence,
            "after_evidence": sorted(
                (_held_row(item) for item in evidence), key=lambda item: item["id"]
            ),
        }
    audit(
        session,
        actor,
        "news_candidate_evidence_refreshed",
        f"news-candidate:{row.id}",
        reason=payload.reason,
        changed_urls=changed,
        previous_evidence_sha256=previous_hash,
        evidence_sha256=row.evidence_hash,
        **repair_metadata,
        **handoff,
        **({"retry_count": row.retry_count} if handoff else {}),
    )
    await session.commit()
    return await candidate_detail(session, row.id)


async def clear_duplicate_candidate(
    session: AsyncSession, actor: User, candidate_id: UUID, payload: CandidateAction
) -> CandidateDetail:
    """An editor answers an uncertain duplicate check with "not a duplicate".

    The answer is stored as a duplicate assessment for the current evidence, which the
    pipeline honours instead of asking Jev again, and the candidate carries on: from its
    article when it already has one (like a re-verify), otherwise from a new draft.
    """

    row = await session.get(NewsCandidate, candidate_id, with_for_update=True)
    if row is None:
        raise AppError(404, "news_candidate_not_found", "找不到新聞候選")
    if row.status != "manual_review" or row.error_code != DUPLICATE_UNCERTAIN:
        raise AppError(409, "news_candidate_not_duplicate_uncertain", "這個候選沒有在等待重複判定")
    session.add(
        NewsAssessment(
            candidate_id=row.id,
            assessment_type="duplicate",
            verdict="pass",
            provider=HUMAN_PROVIDER,
            reasons_json=[payload.reason],
            details_json={},
            evidence_hash=row.evidence_hash,
            prompt_version=row.prompt_version,
            created_by_user_id=actor.id,
        )
    )
    from_article = row.guide_article_id is not None
    if from_article:
        await _queue_reverify(session, row, payload.reason)
    else:
        _queue_new_draft(row, payload.reason)
    audit(
        session,
        actor,
        "news_candidate_duplicate_cleared",
        f"news-candidate:{row.id}",
        reason=payload.reason,
        from_article=from_article,
        retry_count=row.retry_count,
    )
    await session.commit()
    return await candidate_detail(session, row.id)


async def reopen_candidate(
    session: AsyncSession, actor: User, candidate_id: UUID, payload: CandidateAction
) -> CandidateDetail:
    """The owner takes back a story the review judge closed.

    The story returns to the list it was in, under the hold it was closed in, for the owner
    to decide. The judge's answer to that hold stays on the row, so it is not judged again,
    and nothing is recorded as the owner's decision: taking a story back decides nothing yet.
    """

    row = await session.get(NewsCandidate, candidate_id, with_for_update=True)
    if row is None:
        raise AppError(404, "news_candidate_not_found", "找不到新聞候選")
    if (
        row.status not in {"rejected", "duplicate"}
        or row.judge_decision not in {"reject", "duplicate"}
        or row.human_decision is not None
    ):
        raise AppError(409, "news_candidate_not_reopenable", "這個候選不是 AI 結案的，不能拿回來")
    verdict = await session.scalar(
        select(NewsAssessment)
        .where(
            NewsAssessment.candidate_id == row.id,
            NewsAssessment.assessment_type == "judge",
        )
        .order_by(NewsAssessment.created_at.desc())
        .limit(1)
    )
    stage = (verdict.details_json or {}).get("stage") if verdict is not None else None
    closed_as = row.status
    # error_code was kept when the judge closed it, so the row is back in its hold.
    row.status = "needs_redraft" if stage == "redraft" else "manual_review"
    row.judge_decision = "manual"
    audit(
        session,
        actor,
        "news_candidate_reopened_by_owner",
        f"news-candidate:{row.id}",
        reason=payload.reason,
        closed_as=closed_as,
        restored_status=row.status,
        hold=row.error_code,
    )
    await session.commit()
    return await candidate_detail(session, row.id)


def _queue_new_draft(row: NewsCandidate, reason: str | None) -> None:
    """Send the candidate back for a new draft. ``reason`` is the person's; the judge
    passes None, and what a person decided and wrote then stays as it is (the judge hands
    a draft a person confirmed back to them instead of ordering a new one over it)."""

    row.status = "discovered"
    row.error_code = None
    row.error_detail = None
    row.retry_count += 1
    if reason is None:
        return
    row.human_reason = reason
    # A new draft replaces the one the owner may have confirmed.
    row.human_decision = None


async def _queue_reverify(
    session: AsyncSession,
    row: NewsCandidate,
    reason: str | None,
    marker: str = "news_reverify_requested",
) -> None:
    """Run the edited guide drafts through the checks again instead of drafting anew.

    ``reason`` is the person's and becomes ``human_reason``; the judge passes None.
    """

    if row.guide_article_id is None:
        raise AppError(409, "news_draft_unavailable", "候選尚未建立可編輯的五語草稿")
    locale_rows = list(
        await session.scalars(
            select(GuideArticleLocale)
            .where(GuideArticleLocale.article_id == row.guide_article_id)
            .order_by(GuideArticleLocale.locale, GuideArticleLocale.id)
            .with_for_update(nowait=True)
            .execution_options(populate_existing=True)
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
    row.error_code = marker
    row.error_detail = None
    row.retry_count += 1
    if reason is not None:
        row.human_reason = reason


async def approve_candidate(
    session: AsyncSession, actor: User, candidate_id: UUID, payload: CandidateAction
) -> CandidateDetail:
    """The owner confirms a Traditional Chinese draft for publication (2026-09-25).

    The candidate is queued again; the pipeline then translates the other four locales,
    reviews and checks them, saves the article and publishes it. The same action runs the
    second stage again when it stopped on a translation or a check.
    """

    row = await session.get(NewsCandidate, candidate_id, with_for_update=True)
    if row is None:
        raise AppError(404, "news_candidate_not_found", "找不到新聞候選")
    confirmed = row.human_decision == "publish"
    waiting = row.status == "manual_review" and row.error_code == ZH_DRAFT_READY
    stalled = (
        confirmed
        and row.status in {"manual_review", "failed"}
        and row.error_code not in {"news_evidence_changed", "news_navigation_evidence_repaired"}
    )
    if not (waiting or stalled) or not await verified_zh_draft(session, row):
        raise AppError(409, "news_candidate_not_approvable", "這個候選目前不能確認發布")
    if not confirmed:
        row.human_decision = "publish"
        row.human_major_error = False
        session.add(
            NewsAssessment(
                candidate_id=row.id,
                assessment_type="human",
                verdict="publish",
                reasons_json=[payload.reason],
                details_json={"stage": "zh_draft"},
                evidence_hash=row.evidence_hash,
                prompt_version=row.prompt_version,
                created_by_user_id=actor.id,
            )
        )
    row.human_reason = payload.reason
    row.status = "discovered"
    row.error_code = None
    row.error_detail = None
    row.retry_count += 1
    audit(
        session,
        actor,
        "news_candidate_publish_confirmed",
        f"news-candidate:{row.id}",
        reason=payload.reason,
        again=confirmed,
        retry_count=row.retry_count,
    )
    await session.commit()
    return await candidate_detail(session, row.id)


async def verified_zh_draft(session: AsyncSession, row: NewsCandidate) -> GuideDocument | None:
    """The stored Traditional Chinese draft, when a passing verification matches it."""

    encoded = row.draft_bundle_json.get("zh-TW")
    if not encoded:
        return None
    document = GuideDocument.model_validate(encoded)
    verification = await _latest_pass(session, row, "verification")
    if verification is None or verification.details_json.get(
        "document_sha256"
    ) != document_fingerprint(document):
        return None
    return document


async def _latest_pass(
    session: AsyncSession, row: NewsCandidate, assessment_type: str
) -> NewsAssessment | None:
    return cast(
        NewsAssessment | None,
        await session.scalar(
            select(NewsAssessment)
            .where(
                NewsAssessment.candidate_id == row.id,
                NewsAssessment.assessment_type == assessment_type,
                NewsAssessment.verdict == "pass",
                NewsAssessment.evidence_hash == row.evidence_hash,
            )
            .order_by(NewsAssessment.created_at.desc())
        ),
    )


async def publication_bundle(
    session: AsyncSession, row: NewsCandidate, redis: Redis | None = None
) -> tuple[dict[Locale, GuideDocument], dict[Locale, int]]:
    """Every check a publication needs, on the saved five-locale article.

    Shared by the publish button and the pipeline's second stage. One evidence page is
    enough here; automatic publication asks for two websites or a first-party page before
    it gets here, and for the final editor and Jev's last call on every locale.
    """

    if row.guide_article_id is None:
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
    if not evidence_present(evidence):
        raise AppError(422, "news_evidence_insufficient", "發布至少需要一個來源的證據")
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
            source_count=evidence_site_count(evidence),
        )
        for locale, document in documents.items()
    }
    if any(problems.values()):
        raise AppError(422, "news_hard_checks_failed", "硬性格式或政策檢查未通過")
    latest_verification = await _latest_pass(session, row, "verification")
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
    return documents, versions


async def publish_news_bundle(
    session: AsyncSession,
    row: NewsCandidate,
    actor: User | None,
    documents: dict[Locale, GuideDocument],
    versions: dict[Locale, int],
    *,
    reason: str,
    metadata: dict[str, Any],
) -> None:
    """Publish the checked five-locale article; ``publish_bundle`` commits."""

    if row.guide_article_id is None:
        raise AppError(409, "news_candidate_not_publishable", "這個候選目前不能發布")
    await mark_assets_public(session, row.id)
    row.status = "published"
    row.published_at = datetime.now(UTC)
    await admin_service.publish_bundle(
        session,
        actor,
        row.guide_article_id,
        documents,
        versions,
        reason=reason,
        automation_metadata={
            "candidate_id": str(row.id),
            "evidence_sha256": row.evidence_hash,
            "prompt_version": row.prompt_version,
            "policy_version": row.policy_version,
            **metadata,
        },
    )


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
    if row.error_code == "news_navigation_evidence_repaired":
        raise AppError(409, "news_candidate_not_publishable", "先更新修補後保留的來源")
    try:
        documents, versions = await publication_bundle(session, row, redis)
    except AppError as problem:
        if problem.code != "news_evidence_changed":
            raise
        # The pages moved after the article was checked. Hold it for changed evidence, as the
        # pipeline's second stage does, so the editor is offered the re-check against the
        # current pages. Otherwise a ready article can neither publish nor be refreshed
        # (2026-09-27: ai-news-google-project-suncatcher-20260924).
        row.status = "manual_review"
        row.error_code = "news_evidence_changed"
        row.error_detail = problem.detail[:4000]
        await session.commit()
        raise
    row.human_decision = "publish"
    row.human_reason = payload.reason
    row.human_major_error = payload.major_error
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
    await publish_news_bundle(
        session,
        row,
        actor,
        documents,
        versions,
        reason=payload.reason,
        metadata={"human_override": True},
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
    handed_back = await session.scalar(
        select(func.count())
        .select_from(NewsCandidate)
        .where(NewsCandidate.status == "needs_redraft", NewsCandidate.judge_decision == "manual")
    )
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
        judge_handed_back=int(handed_back or 0),
        pipeline_runs=int(run_totals[0] or 0),
        pipeline_failures=int(run_totals[1] or 0),
        input_tokens=int(run_totals[2] or 0),
        output_tokens=int(run_totals[3] or 0),
    )
