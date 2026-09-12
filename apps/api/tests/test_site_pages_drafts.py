"""The shipped drafts are the text a reader will be shown, so they are checked like code.

Two things nothing else guards. First, the five locale files are edited by hand and
independently: a paragraph added to one and forgotten in another produces a policy that
says less in Korean than it does in English, and no i18n check covers this directory
(`tools/check-i18n.mjs` reads `apps/web/messages`). Second, account erasure de-identifies
audit rows by matching one target shape, and that contract is held by convention alone.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from app.i18n import Locale
from app.site_pages.schemas import PAGE_SLUGS, PageDocument, PageSlug
from app.site_pages.service import initial_document, pending_requirements

LOCALES: tuple[Locale, ...] = ("en", "ja", "ko", "zh-TW", "zh-CN")
REFERENCE: Locale = "zh-TW"
API_ROOT = Path(__file__).resolve().parents[1]


def _shape(slug: PageSlug, locale: Locale) -> list[tuple[str, object, int]]:
    """Structure only: type, heading level and bullet count, never the translated text."""
    return [
        (block.type, getattr(block, "level", None), len(getattr(block, "items", ())))
        for block in initial_document(slug, locale).blocks
    ]


def _text(slug: PageSlug, locale: Locale) -> str:
    return " ".join(
        str(getattr(block, "text", "")) + " ".join(getattr(block, "items", ()))
        for block in initial_document(slug, locale).blocks
    )


@pytest.mark.parametrize("slug", PAGE_SLUGS)
def test_every_locale_has_the_same_document_shape(slug: PageSlug) -> None:
    """A translation may not quietly drop a section, a bullet or a heading level."""
    expected = _shape(slug, REFERENCE)
    for locale in LOCALES:
        assert _shape(slug, locale) == expected, (
            f"{locale}/{slug} does not match {REFERENCE}"
        )


@pytest.mark.parametrize("locale", LOCALES)
def test_no_locale_ships_a_filled_requirement(locale: Locale) -> None:
    """The owner supplies these. A value committed here would be published as a promise
    nobody made, which is the whole reason `pending_requirements` gates publication."""
    for slug in PAGE_SLUGS:
        document = initial_document(slug, locale)
        assert document.effective_date is None
        assert set(pending_requirements(slug, document)) >= {"effective_date"}
        for field, value in document.requirements.model_dump().items():
            assert value == "", f"{locale}/{slug}.{field} is pre-filled"


@pytest.mark.parametrize("locale", LOCALES)
def test_draft_json_matches_the_published_schema(locale: Locale) -> None:
    payload = json.loads(
        (API_ROOT / "app" / "site_pages" / "drafts" / f"{locale}.json").read_text("utf-8")
    )
    assert set(payload) == set(PAGE_SLUGS)
    for slug in PAGE_SLUGS:
        PageDocument.model_validate(payload[slug])


def test_privacy_describes_what_account_deletion_actually_leaves_behind() -> None:
    """`erase_account` keeps the `users` row (email rewritten to `<hex>@deleted.invalid`)
    and never touches `usage_accounts`/`usage_ledger`/`usage_reservations`. An earlier
    draft said retained accounting links "use a de-identified identity", which is not what
    the code does; the text must keep naming the account record that survives."""
    body = _text("privacy", "en")
    assert "account record itself is kept" in body
    assert "ledger records" in body


AUDIT_CALL = re.compile(r"AdminAuditLog\((.{0,800}?)\)\s*\n", re.S)
TARGET = re.compile(r"target=([^,\n]+)")
METADATA = re.compile(r"metadata_json=(\{.{0,400}?\})", re.S)
IDENTIFYING = re.compile(r"email|user_id|member_id|actor_email")


def test_audit_rows_naming_a_user_use_the_target_shape_erasure_rewrites() -> None:
    """Erasure rewrites `admin_audit_logs` with exactly two UPDATEs: `target ==
    f"user:{user_id}"` and `actor_user_id == user_id` (`community/jobs.py`). A row that
    carries an email or a user id inside `metadata_json` under any *other* target is
    therefore missed, and would outlive the account it names.

    Every call site satisfies this today. Nothing enforces it, which is why this exists:
    a new audit write that puts an identifier under a different target fails here rather
    than silently surviving erasure.
    """
    offenders: list[str] = []
    for path in (API_ROOT / "app").rglob("*.py"):
        source = path.read_text("utf-8")
        for match in AUDIT_CALL.finditer(source):
            block = match.group(1)
            metadata = METADATA.search(block)
            if not metadata or not IDENTIFYING.search(metadata.group(1)):
                continue
            target = TARGET.search(block)
            if target and "user:{" in target.group(1):
                continue
            line = source[: match.start()].count("\n") + 1
            shape = target.group(1) if target else None
            offenders.append(f"{path.relative_to(API_ROOT)}:{line} target={shape}")
    assert not offenders, (
        "audit rows carrying a user identifier outside a `user:{id}` target survive "
        "erase_account(): " + "; ".join(offenders)
    )
