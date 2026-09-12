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
from app.site_pages.schemas import PAGE_SLUGS, REQUIRED_FIELDS, PageDocument, PageSlug
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
def test_every_locale_carries_the_owner_supplied_requirements(locale: Locale) -> None:
    """These five values were supplied by the site owner on 2026-09-12 and are published
    verbatim on the page, so every locale must carry them and no locale may carry one the
    page does not ask for: `about` and `contact` declare only three fields in
    REQUIRED_FIELDS, and a retention promise rendered on `/about` would be a commitment
    nobody made for that page."""
    for slug in PAGE_SLUGS:
        requirements = initial_document(slug, locale).requirements.model_dump()
        required = set(REQUIRED_FIELDS[slug])
        for field, value in requirements.items():
            if field in required:
                assert value.strip(), f"{locale}/{slug}.{field} is empty"
            else:
                assert value == "", f"{locale}/{slug}.{field} is set but not required"


@pytest.mark.parametrize("locale", LOCALES)
def test_effective_date_is_never_committed(locale: Locale) -> None:
    """The owner sets this in the admin on the day they publish, so publication stays
    gated here and the date on the page is the day it genuinely went public. It is also
    the one requirement `pending_requirements` adds on its own, so a committed date would
    make a fresh environment publishable without anyone deciding to."""
    for slug in PAGE_SLUGS:
        document = initial_document(slug, locale)
        assert document.effective_date is None, f"{locale}/{slug} ships an effective_date"
        assert pending_requirements(slug, document) == ["effective_date"], (
            f"{locale}/{slug} is blocked by something other than the date"
        )


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
