"""Discovery summaries reach the client as text, not as markup.

Ingested summaries carry provider HTML. The web client renders `summary` as a text
node — correctly, since interpolating provider markup would be an injection sink —
so an unsanitised summary shows the reader `<strong>` in the middle of a sentence.
Two of the six cards on the zh-TW home page did exactly that.

`base_item` is the single funnel every source passes through, so the cleaning
belongs there and these tests pin it at that level.
"""

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.discovery.sources import base_item


def _summary(raw: str) -> str:
    return base_item(
        "article",
        uuid4(),
        "Tokyo Station Ichibangai",
        "en",
        "TYO",
        datetime.now(UTC),
        summary=raw,
    ).summary


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (
            "There's <strong>shopping, dining, souvenir shopping</strong> - you name it.",
            "There's shopping, dining, souvenir shopping - you name it.",
        ),
        (
            "From <strong>delicious ramen to unique souvenirs</strong>, so much to enjoy.",
            "From delicious ramen to unique souvenirs, so much to enjoy.",
        ),
        ("<p>Two<br>lines</p>", "Two lines"),
        ("Caf&eacute; &amp; bar", "Café & bar"),
        ("  collapses   inner   space  ", "collapses inner space"),
        ("", ""),
    ],
)
def test_markup_never_reaches_the_reader(raw: str, expected: str) -> None:
    assert _summary(raw) == expected


def test_plain_summaries_are_left_alone() -> None:
    plain = "東京駅一番街は東京駅八重洲口地下に広がる大型商業施設だ。"
    assert _summary(plain) == plain


def test_the_length_cap_still_applies_after_cleaning() -> None:
    # The cap has to count characters the reader will see, not markup that is removed.
    raw = "<strong>" + ("あ" * 1300) + "</strong>"
    assert _summary(raw) == "あ" * 1200
