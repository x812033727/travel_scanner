"""Opt-in real API/PG/Redis/RQ/S3/SMTP recovery; no mocked application services."""

from __future__ import annotations

import hashlib
import io
import json
import os
import time
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import httpx
import pytest
from PIL import Image

from tests.support.community_service_runtime import CommunityRuntime, eventually, loopback

pytestmark = pytest.mark.skipif(
    os.environ.get("COMMUNITY_SERVICE_RECOVERY_E2E") != "1"
    or os.environ.get("RUN_INTEGRATION_TESTS") != "1",
    reason="Needs explicit opt-in and loopback PostgreSQL/Redis/MinIO/Mailpit",
)


@pytest.fixture(scope="module")
def runtime(tmp_path_factory: pytest.TempPathFactory) -> Iterator[CommunityRuntime]:
    runtime = CommunityRuntime(tmp_path_factory.mktemp("community-recovery"))
    try:
        runtime.start()
        yield runtime
    finally:
        runtime.close()


def completed(runtime: CommunityRuntime, user_id: str, kind: str = "mail") -> bool:
    job = runtime.job(user_id, kind)
    return job["status"] == "completed" and not job["has_payload"]


def test_stopped_worker_preserves_mail_and_restarts(runtime: CommunityRuntime) -> None:
    runtime.stop("worker")
    runtime.stop("sweeper")
    member, user_id, email = runtime.member("restart", verify=False)
    runtime.request(member, "POST", "/auth/request-verification", status=202)
    pending = runtime.job(user_id)
    assert pending["status"] == "pending" and pending["has_payload"]
    assert pending["attempts"] == 0
    assert runtime.redis is not None
    assert runtime.redis.llen("rq:queue:community") > 0
    runtime.start_workers()
    token = runtime.mail_token(email, "verify")
    runtime.request(member, "POST", "/auth/verify-email", token=token)
    replay = runtime.request(member, "POST", "/auth/verify-email", status=400, token=token)
    assert replay["code"] == "community_token_invalid"
    eventually(lambda: completed(runtime, user_id))
    assert runtime.request(member, "GET", "/auth/me")["email_verified"]
    runtime.record("worker_restart", durable_pending=True, actual_mail=True, one_use_token=True)


def test_redis_outage_and_sweeper_recover_lost_wakeup(runtime: CommunityRuntime) -> None:
    sender, sender_id, _ = runtime.member("sender")
    reader, reader_id, _ = runtime.member("reader")
    for actor, target in [(sender, reader_id), (reader, sender_id)]:
        runtime.request(actor, "PUT", f"/community/profiles/{target}/follow")
    thread = runtime.request(sender, "POST", f"/community/conversations/{reader_id}", status=201)
    route = f"/community/conversations/{thread['id']}/messages"
    cursor = runtime.request(reader, "GET", "/community/events/cursor")["cursor"]
    body = {"body": "Durable message", "idempotency_key": "isolated-first-message"}
    first = runtime.request(sender, "POST", route, status=201, **body)
    runtime.stop("worker")
    runtime.stop("sweeper")
    mail_member, mail_id, mail_email = runtime.member("redis", verify=False)
    runtime.request(mail_member, "POST", "/auth/request-verification", status=202)
    assert runtime.job(mail_id)["status"] == "pending"
    assert runtime.redis is not None
    # Explicitly discard only our DB's transient RQ wakeup, never its durable PG job.
    assert runtime.redis.delete("rq:queue:community") == 1
    event_ids: list[int] = []
    with reader.stream("GET", "community/events", params={"after": cursor}) as stream:
        assert stream.status_code == 200
        lines = stream.iter_lines()
        for line in lines:
            if line.startswith("id: "):
                event_ids.append(int(line[4:]))
            if line == ": keepalive":
                break
        assert event_ids and event_ids == sorted(set(event_ids))
        runtime.redis_proxy.outage(True)
        try:
            refused = runtime.request(
                sender,
                "POST",
                route,
                status=503,
                body="Must not persist",
                idempotency_key="outage-message",
            )
            assert refused["code"] == "session_check_unavailable"
            assert (
                runtime.sql(
                    "SELECT count(*) AS n FROM community_messages "
                    "WHERE idempotency_key='outage-message'"
                )[0]["n"]
                == 0
            )
            assert any(line == "event: unavailable" for line in lines)
        finally:
            runtime.redis_proxy.outage(False)
    runtime.start_workers()
    token = runtime.mail_token(mail_email, "verify", seconds=90)
    runtime.request(mail_member, "POST", "/auth/verify-email", token=token)
    eventually(lambda: completed(runtime, mail_id))
    replay = runtime.request(sender, "POST", route, status=201, **body)
    assert replay == {"id": first["id"], "replayed": True}
    messages = runtime.request(reader, "GET", route + "?after=0")["items"]
    assert [item["id"] for item in messages] == [first["id"]]
    second = runtime.request(
        sender,
        "POST",
        route,
        status=201,
        body="After recovery",
        idempotency_key="isolated-second-message",
    )
    assert second["id"] > first["id"]
    expected_event = runtime.sql(
        "SELECT max(id) AS id FROM community_events WHERE recipient_id=$1::uuid "
        "AND kind='message' AND target=$2",
        reader_id,
        thread["id"],
    )[0]["id"]
    assert expected_event > event_ids[-1]
    resumed: list[int] = []
    with reader.stream(
        "GET", "community/events", headers={"Last-Event-ID": str(event_ids[-1])}
    ) as stream:
        assert stream.status_code == 200
        for line in stream.iter_lines():
            if line.startswith("id: "):
                resumed.append(int(line[4:]))
            if line == ": keepalive":
                break
    assert resumed == [expected_event]
    notifications = runtime.request(reader, "GET", "/community/notifications")["items"]
    assert sum(item["kind"] == "message" for item in notifications) == 2
    runtime.record(
        "redis_outage",
        fail_closed=True,
        sse_unavailable=True,
        durable_catchup=True,
        idempotent_message=True,
        sweeper_actual_mail=True,
    )


def test_smtp_real_backoff_and_expired_mail_are_distinct(runtime: CommunityRuntime) -> None:
    member, user_id, email = runtime.member("smtp", verify=False)
    runtime.smtp_proxy.outage(True)
    try:
        runtime.request(member, "POST", "/auth/forgot-password", status=202, email=email)
        eventually(lambda: runtime.job(user_id)["attempts"] == 1)
        failed = runtime.job(user_id)
        assert failed["status"] == "pending" and failed["has_payload"]
        remaining = runtime.sql(
            "SELECT EXTRACT(EPOCH FROM (available_at-now())) AS seconds "
            "FROM community_jobs WHERE id=$1",
            failed["id"],
        )[0]["seconds"]
        assert 110 < remaining <= 120
        restored = time.monotonic()
    finally:
        runtime.smtp_proxy.outage(False)
    token = runtime.mail_token(email, "reset", seconds=210)
    assert time.monotonic() - restored >= 105  # Never accelerate product retry timestamps.
    runtime.request(
        member,
        "POST",
        "/auth/reset-password",
        token=token,
        password="isolated-recovered-password-5831",
    )
    eventually(lambda: completed(runtime, user_id))
    assert runtime.job(user_id)["attempts"] == 1
    runtime.stop("worker")
    runtime.stop("sweeper")
    expired, expired_id, expired_email = runtime.member("expired", verify=False)
    runtime.request(expired, "POST", "/auth/request-verification", status=202)
    old_job = runtime.job(expired_id)
    # Separate synthetic expired fixture: completion must NOT count as delivery.
    runtime.sql(
        "UPDATE community_jobs SET created_at=now()-interval '31 minutes' WHERE id=$1",
        old_job["id"],
    )
    runtime.start_workers()
    eventually(lambda: completed(runtime, expired_id))
    with httpx.Client(trust_env=False) as client:
        messages = client.get(
            runtime.mailpit + "/api/v1/search", params={"query": f"to:{expired_email}"}
        ).json()["messages"]
    assert messages == []
    runtime.record(
        "smtp_outage",
        retry_attempts=1,
        actual_backoff_seconds=120,
        sweep_interval_seconds=60,
        actual_reset_mail=True,
        expired_mail_not_delivered=True,
    )


def test_s3_upload_and_erasure_recover_without_destroying_storage(
    runtime: CommunityRuntime,
) -> None:
    member, user_id, email = runtime.member("storage")
    content = io.BytesIO()
    Image.new("RGB", (16, 12), "blue").save(content, format="PNG")
    raw = content.getvalue()
    created = runtime.request(
        member,
        "POST",
        "/community/media/uploads",
        status=201,
        content_type="image/png",
        size=len(raw),
        alt="Private recovery image",
    )
    upload = created["upload"]
    assert loopback(upload["url"]).port == runtime.s3_proxy.port
    with httpx.Client(trust_env=False) as client:
        response = client.post(
            upload["url"], data=upload["fields"], files={"file": ("fixture.png", raw, "image/png")}
        )
    assert response.is_success
    media_id = created["id"]
    runtime.s3_proxy.outage(True)
    try:
        error = runtime.request(member, "POST", f"/community/media/{media_id}/complete", status=503)
        assert error["code"] == "community_storage_unavailable"
        assert (
            runtime.sql("SELECT width FROM community_media WHERE id=$1::uuid", media_id)[0]["width"]
            == 0
        )
    finally:
        runtime.s3_proxy.outage(False)
    processed = runtime.request(member, "POST", f"/community/media/{media_id}/complete")
    assert (processed["width"], processed["height"]) == (16, 12)
    keys = [f"images/{media_id}.webp", f"thumbs/{media_id}.webp"]
    for key in keys:
        assert runtime.s3.head_object(Bucket=runtime.bucket, Key=key)["ContentLength"] > 0
    runtime.request(member, "POST", "/auth/request-deletion", status=202)
    token = runtime.mail_token(email, "delete")
    retained_session = runtime.client()
    retained_session.cookies.update(member.cookies)
    runtime.s3_proxy.outage(True)
    try:
        runtime.request(
            member, "POST", "/auth/delete-account", status=202, token=token, confirmation="DELETE"
        )
        assert member.get("auth/me").status_code == 401
        # Test the pre-deletion credential too; merely clearing the response
        # cookie would not prove server-side revocation during the S3 outage.
        assert retained_session.get("auth/me").status_code == 401
        eventually(lambda: runtime.job(user_id, "delete_account")["attempts"] == 1)
        assert runtime.job(user_id, "delete_account")["status"] == "pending"
        assert (
            runtime.sql("SELECT email FROM users WHERE id=$1::uuid", user_id)[0]["email"] == email
        )
        for key in keys:
            assert runtime.s3.head_object(Bucket=runtime.bucket, Key=key)["ContentLength"] > 0
    finally:
        runtime.s3_proxy.outage(False)
    eventually(lambda: completed(runtime, user_id, "delete_account"), seconds=210)
    erased = runtime.sql(
        "SELECT email,password_hash,is_active FROM users WHERE id=$1::uuid", user_id
    )[0]
    assert erased["email"].endswith("@deleted.invalid")
    assert erased["password_hash"] is None and erased["is_active"] is False
    assert runtime.sql("SELECT alt,deleted_at FROM community_media WHERE id=$1::uuid", media_id)[0][
        "deleted_at"
    ]
    remaining = runtime.s3.list_objects_v2(Bucket=runtime.bucket).get("Contents", [])
    assert not set(keys).intersection(item["Key"] for item in remaining)
    runtime.record(
        "s3_outage",
        quarantine_preserved=True,
        processed_real_image=True,
        access_revoked_before_retry=True,
        actual_erasure_after_recovery=True,
    )


def publish(
    runtime: CommunityRuntime,
    member: httpx.Client,
    title: str,
    *,
    previous: dict[str, Any] | None = None,
) -> dict[str, Any]:
    fields = {
        "title": title,
        "body": "Synthetic original content without instructions.",
        "locale": "zh-TW",
        "destination": "Tokyo",
    }
    if previous:
        post = runtime.request(
            member,
            "PUT",
            f"/community/posts/{previous['id']}",
            status=200,
            version=previous["version"],
            **fields,
        )
    else:
        post = runtime.request(member, "POST", "/community/posts", status=201, **fields)
    runtime.request(
        member, "POST", f"/community/posts/{post['id']}/publish", version=post["version"]
    )
    pending = runtime.request(member, "GET", f"/community/posts/{post['id']}/draft")
    runtime.request(
        runtime.admin,
        "PUT",
        f"/admin/community/posts/{post['id']}",
        action="approve",
        version=pending["version"],
        reason="Reviewed isolated fixture",
    )
    return runtime.request(member, "GET", f"/community/posts/{post['id']}")


def fingerprint(post: dict[str, Any]) -> str:
    value = [post["locale"], post["title"] + "\n\n" + post["body"]]
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def translation_state(runtime: CommunityRuntime) -> tuple[int, int, int]:
    return (
        runtime.sql("SELECT count(*) AS n FROM community_translations")[0]["n"],
        runtime.sql("SELECT COALESCE(sum(characters),0) AS n FROM community_translation_budgets")[
            0
        ]["n"],
        runtime.sql("SELECT count(*) AS n FROM usage_ledger")[0]["n"],
    )


def member_usage(
    runtime: CommunityRuntime, user_id: str
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    # Compare the actual member balance and complete existing ledger values, not
    # just a global row count that could miss an in-place charge or unrelated write.
    return (
        runtime.sql("SELECT * FROM usage_accounts WHERE user_id=$1::uuid ORDER BY id", user_id),
        runtime.sql("SELECT * FROM usage_ledger WHERE user_id=$1::uuid ORDER BY id", user_id),
    )


def test_translation_http_failure_cache_budget_and_recovery(runtime: CommunityRuntime) -> None:
    member, user_id, _ = runtime.member("translate")
    usage_before = member_usage(runtime, user_id)
    post = publish(runtime, member, "Provider retry source")
    assert runtime.upstream is not None
    upstream = runtime.upstream
    request = {"kind": "post", "target_id": post["id"], "locale": "en"}
    before = translation_state(runtime)
    size = len(post["title"] + "\n\n" + post["body"])
    try:
        for index, mode in enumerate(["unavailable", "malformed"], 1):
            upstream.configure(mode)
            problem = runtime.request(
                member, "POST", "/community/translations", status=503, **request
            )
            assert problem["code"] == "community_translation_unavailable"
            assert translation_state(runtime) == (before[0], before[1] + size * index, before[2])
            assert (
                runtime.request(member, "GET", f"/community/posts/{post['id']}")["body"]
                == post["body"]
            )
        upstream.configure("success")
        result = runtime.request(member, "POST", "/community/translations", **request)
        assert result["machine_translated"] is True
        cached_calls = upstream.calls
        cached_state = translation_state(runtime)
        assert cached_state == (before[0] + 1, before[1] + size * 3, before[2])
        assert runtime.request(member, "POST", "/community/translations", **request) == result
        assert upstream.calls == cached_calls and translation_state(runtime) == cached_state
        runtime.settings(translation_characters_per_month=cached_state[1])
        other = {**request, "locale": "ja"}
        problem = runtime.request(member, "POST", "/community/translations", status=429, **other)
        assert problem["code"] == "community_translation_limit"
        assert upstream.calls == cached_calls and translation_state(runtime) == cached_state
        runtime.settings(translation_characters_per_month=100000)
        assert runtime.request(member, "POST", "/community/translations", **other)[
            "machine_translated"
        ]
        assert upstream.calls == cached_calls + 1 and not upstream.errors
    finally:
        upstream.configure("success")
        runtime.settings(translation_characters_per_month=100000)
    assert member_usage(runtime, user_id) == usage_before
    runtime.record(
        "translation_failure",
        real_http_parser=True,
        reservation_retained=True,
        cache_no_recharge=True,
        budget_rejected_before_http=True,
        member_ledger_unchanged=True,
    )


def test_translation_rechecks_revision_after_real_http_barrier(runtime: CommunityRuntime) -> None:
    member, user_id, _ = runtime.member("revision")
    usage_before = member_usage(runtime, user_id)
    first = publish(runtime, member, "First source revision")
    assert runtime.upstream is not None
    upstream = runtime.upstream
    upstream.configure("success", hold=True)
    before = translation_state(runtime)
    client = runtime.client()
    client.cookies.update(member.cookies)
    request = {"kind": "post", "target_id": first["id"], "locale": "ko"}
    with ThreadPoolExecutor(max_workers=1) as pool:
        pending = pool.submit(client.post, "community/translations", json=request)
        try:
            assert upstream.arrived.wait(15), "The real provider request never reached the barrier"
            draft = runtime.request(member, "GET", f"/community/posts/{first['id']}/draft")
            latest = publish(runtime, member, "Second source revision", previous=draft)
        finally:
            upstream.release.set()
        response = pending.result(timeout=40)  # Propagates thread/network failures.
    assert response.status_code == 409 and response.json()["code"] == "community_version_conflict"
    assert translation_state(runtime)[0] == before[0]
    assert translation_state(runtime)[2] == before[2]
    assert (
        runtime.sql(
            "SELECT count(*) AS n FROM community_translations WHERE source_hash=$1",
            fingerprint(first),
        )[0]["n"]
        == 0
    )
    upstream.configure("success")
    result = runtime.request(member, "POST", "/community/translations", **request)
    assert result["machine_translated"]
    assert (
        runtime.sql(
            "SELECT count(*) AS n FROM community_translations WHERE source_hash=$1",
            fingerprint(latest),
        )[0]["n"]
        == 1
    )
    calls = upstream.calls
    state = translation_state(runtime)
    assert runtime.request(member, "POST", "/community/translations", **request) == result
    assert upstream.calls == calls and translation_state(runtime) == state
    assert not upstream.errors
    assert member_usage(runtime, user_id) == usage_before
    runtime.record(
        "translation_revision",
        deterministic_http_barrier=True,
        stale_response_409=True,
        stale_cache_absent=True,
        new_fingerprint_cached=True,
        member_ledger_unchanged=True,
    )
