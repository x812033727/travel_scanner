"""What `parse_airalo` refuses before it parses anything.

The feed comes from one hardcoded official URL, so the guard is not defending against a
stranger — it is defending against the day that URL answers with something it should not.
That is worth testing precisely, because the guard is a byte scan and a byte scan is exactly
the kind of thing that works for the encoding it was written against and quietly fails for
the next one.
"""

from datetime import UTC, datetime

import pytest

from app.travel_services.jobs import FEED_LIMIT, parse_airalo

NOW = datetime(2026, 9, 14, tzinfo=UTC)

FEED = """<?xml version="1.0" encoding="{label}"?>
<rss><channel>
  <item>
    <id>airalo-jp-1</id>
    <title>Moshi Moshi 1 GB - 7 days</title>
    <link>https://www.airalo.com/japan-esim/moshi-moshi-1gb-7days</link>
    <price>4.50 USD</price>
  </item>
</channel></rss>"""

HOSTILE = """<?xml version="1.0" encoding="{label}"?>
<!DOCTYPE rss [<!ENTITY lol "lollollollollol">]>
<rss><channel><item><id>a</id></item></channel></rss>"""


#: Codec -> (the label XML may declare, the byte order mark the parser needs).
#: expat rejects `UTF-16-LE`/`UTF-16-BE` as declared labels — the declaration says `UTF-16`
#: and the BOM is what tells it the byte order — so an encoding cannot simply be named twice.
ENCODINGS = {
    "utf-8": ("UTF-8", b""),
    "utf-16-le": ("UTF-16", b"\xff\xfe"),
    "utf-16-be": ("UTF-16", b"\xfe\xff"),
}


def encoded(template: str, codec: str) -> bytes:
    label, bom = ENCODINGS[codec]
    return bom + template.format(label=label).encode(codec)


@pytest.mark.parametrize("encoding", list(ENCODINGS))
def test_a_document_type_declaration_is_refused_in_every_encoding(encoding: str) -> None:
    """The bug this file was written for.

    `bytes.upper()` folds ASCII only. In UTF-16 every ASCII character is interleaved with a
    NUL, so `<!DOCTYPE` on the wire is `3C 00 21 00 44 00 ...` and the old scan matched
    neither literal — while `ElementTree` honours the encoding declaration and would have
    parsed it anyway.
    """
    with pytest.raises(ValueError, match="Unsafe feed"):
        parse_airalo(encoded(HOSTILE, encoding), NOW)


@pytest.mark.parametrize("encoding", list(ENCODINGS))
def test_an_ordinary_feed_still_parses_in_every_encoding(encoding: str) -> None:
    """The other half: a guard that refuses good feeds is not an improvement.

    Dropping NUL bytes before the scan cannot hide anything a real feed contains, because
    NUL is not a valid XML character in any encoding — this is what pins that claim.
    """
    products = parse_airalo(encoded(FEED, encoding), NOW)
    assert [product.title for product in products] == ["Moshi Moshi 1 GB - 7 days"]
    assert products[0].source_key == "airalo:airalo-jp-1"
    assert products[0].facts.country_codes == ["JP"]
    assert products[0].facts.validity_days == 7
    assert products[0].facts.data_gb == 1.0


def test_an_oversized_feed_is_refused_before_it_is_parsed() -> None:
    # The other half of the denial-of-service defence, and the half that does not depend on
    # encoding at all. Kept here so removing either one fails a test.
    with pytest.raises(ValueError, match="Unsafe feed"):
        parse_airalo(b"<rss/>" + b" " * FEED_LIMIT, NOW)


def test_the_scan_reads_the_whole_body_not_just_its_start() -> None:
    # A declaration cannot be hidden behind padding, in any encoding.
    body = b"<!-- " + b"x" * 50_000 + b" -->" + encoded(HOSTILE, "utf-16-le")
    with pytest.raises(ValueError, match="Unsafe feed"):
        parse_airalo(body, NOW)
