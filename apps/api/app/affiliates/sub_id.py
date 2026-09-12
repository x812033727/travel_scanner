"""The one place an affiliate sub_id is built, and the gate every one passes through.

A sub_id is attribution data: it is sent to an affiliate network and stored in
``affiliate_clicks``. It must describe the *click*, never the person who made it.
A value that varies per member lets a network join our traffic into a profile of
one person across every site they use, and the two values this module replaced
were ``uuid5`` — deterministic, so anyone holding the namespace string can confirm
a guessed ``user.id`` by recomputation.

``coarse_sub_id`` builds the only shape we send: closed catalog labels joined by
underscores, empty segments dropped. ``safe_sub_id`` is the gate at each egress.

**What the gate does and does not prove.** It is a shape-and-content check, not a
proof of provenance: it rejects anything that is not spelled like one of our
labels, and anything carrying a long hex run (every UUID spelling this repository
has shipped). It cannot tell that ``aff_hotel_tokyo_zh-TW`` was built here rather
than typed by hand, so it does not make a future leak impossible — it makes the
leaks we have actually had impossible, and makes a new one loud. The durable
guarantee is that both egress points call it and that
``tests/test_affiliate_sub_id.py`` fails when a new derivation site appears.
"""

from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)

#: The three label families this codebase sends: ``aff_`` (member-initiated
#: clickouts), ``dst_`` (curated destination offers), ``svc_`` (travel services).
SUB_ID_RE = re.compile(r"(?:aff|dst|svc)_[A-Za-z0-9][A-Za-z0-9._-]{0,59}\Z")

#: Long hex runs are how every identifier we have leaked was spelled: ``uuid5``
#: and ``uuid4`` both render as 32 hex characters via ``.hex``. No catalog label
#: in this repository — destination id, area code, locale, module — comes close.
_HEX_RUN = re.compile(r"[0-9a-fA-F]{16,}")

_UNSAFE = re.compile(r"[^A-Za-z0-9.-]+")

MAX_SUB_ID = 64


def _segment(value: object) -> str:
    return _UNSAFE.sub("-", str(value)).strip("-")


def coarse_sub_id(
    prefix: str,
    kind: str,
    destination_id: str | None,
    locale: str,
    placement: str | None = None,
) -> str:
    """Build a sub_id from catalog labels only.

    Empty segments are dropped rather than rendered as ``__``, so a click with no
    resolved destination yields ``aff_hotel_zh-TW`` and one in Tokyo yields
    ``aff_hotel_tokyo_zh-TW``. That keeps the value readable in partner reporting
    and keeps the no-destination case byte-identical to the label this repository
    already sent to Klook.
    """
    parts = (prefix, kind, destination_id, locale, placement)
    return "_".join(_segment(part) for part in parts if part)[:MAX_SUB_ID]


def is_catalog_sub_id(value: str | None) -> bool:
    """Whether ``value`` has the shape this module builds: a known prefix, catalog
    characters only, and no identifier-length hex run. Shared by the egress gate and
    by reporting, which must not echo a legacy member-derived value back to an admin."""
    candidate = value or ""
    return bool(SUB_ID_RE.fullmatch(candidate)) and not _HEX_RUN.search(candidate)


def safe_sub_id(value: str | None, *, rebuild: str) -> str:
    """Return ``value`` if it is one of our labels, otherwise ``rebuild``.

    Fail-closed: an unrecognised value is never forwarded, because the only way a
    value gets here unrecognised is that something built it outside this module.

    The rejected value is deliberately never logged — if the gate is doing its
    job, that string is the identifier we are trying not to disclose, and a log
    line is a second place it would leak to.
    """
    if value and is_catalog_sub_id(value):
        return value
    logger.warning(
        "affiliate sub_id rejected at egress and rebuilt from catalog labels; "
        "a caller is constructing sub_id outside app.affiliates.sub_id"
    )
    return rebuild
