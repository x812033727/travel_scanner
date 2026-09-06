from typing import Any

import pytest

from app.config import Settings
from app.hotspots import simplified_names as module
from app.hotspots.simplified_names import (
    SimplifiedBatch,
    SimplifiedName,
    acceptable,
    apply_conversions,
    convert_names,
    stored_label_count,
)


class FakeProvider:
    name = "gemini"
    model = "gemini-3.8-flash"

    def __init__(self, batches: list[SimplifiedBatch | Exception]) -> None:
        self.batches = batches
        self.payloads: list[dict[str, Any]] = []
        self.closed = False

    async def structured(
        self, _schema: type, _name: str, instructions: str, payload: dict[str, Any]
    ) -> tuple[SimplifiedBatch, dict[str, int]]:
        self.payloads.append(payload)
        self.instructions = instructions
        result = self.batches[len(self.payloads) - 1]
        if isinstance(result, Exception):
            raise result
        return result, {"input_tokens": 10, "output_tokens": 5}

    async def close(self) -> None:
        self.closed = True


def batch(*pairs: tuple[str, str]) -> SimplifiedBatch:
    return SimplifiedBatch(
        items=[SimplifiedName(traditional=t, simplified=s) for t, s in pairs]
    )


def test_acceptable_keeps_conversions_and_rejects_rewrites() -> None:
    assert acceptable("曼谷大皇宮", "曼谷大皇宫") is True
    assert acceptable("高尾山", "高尾山") is True
    # A different name of the same length is the failure the length check cannot catch,
    # but a name of a different length always is.
    assert acceptable("倫披尼公園", "是樂園") is False
    assert acceptable("素帖山雙龍寺", "双龙寺") is False
    # Names written the same way in both scripts are legitimately unchanged.
    assert acceptable("東京", "东京") is True
    # Latin, digits and punctuation must survive untouched.
    assert acceptable("中部電力 MIRAI TOWER", "中部电力 MIRAI TOWER") is True
    assert acceptable("中部電力 MIRAI TOWER", "中部电力_MIRAI_TOWER") is False


@pytest.mark.asyncio
async def test_only_replies_that_pass_the_check_are_kept(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provider = FakeProvider(
        [
            batch(
                ("曼谷大皇宮", "曼谷大皇宫"),
                ("高尾山", "高尾山"),
                ("倫披尼公園", "是樂園"),
                ("東京鐵塔", "东京铁塔"),
            )
        ]
    )
    monkeypatch.setattr(module, "research_provider", lambda *_a, **_k: provider)

    report = await convert_names(
        ["曼谷大皇宮", "高尾山", "倫披尼公園", "東京鐵塔"], Settings()
    )

    assert report.converted == {"曼谷大皇宮": "曼谷大皇宫", "東京鐵塔": "东京铁塔"}
    assert report.unchanged == ["高尾山"]
    assert [pair[0] for pair in report.rejected] == ["倫披尼公園"]
    assert report.calls == 1
    assert provider.closed is True
    assert "never 黎明寺" in provider.instructions


@pytest.mark.asyncio
async def test_a_name_the_model_skipped_is_reported_not_guessed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provider = FakeProvider([batch(("曼谷大皇宮", "曼谷大皇宫"))])
    monkeypatch.setattr(module, "research_provider", lambda *_a, **_k: provider)

    report = await convert_names(["曼谷大皇宮", "還劍湖"], Settings())

    assert report.converted == {"曼谷大皇宮": "曼谷大皇宫"}
    assert report.missing == ["還劍湖"]


@pytest.mark.asyncio
async def test_names_are_batched_and_deduplicated(monkeypatch: pytest.MonkeyPatch) -> None:
    provider = FakeProvider([batch(("甲", "甲")), batch(("乙", "乙"))])
    monkeypatch.setattr(module, "research_provider", lambda *_a, **_k: provider)

    report = await convert_names(["甲", "甲", "乙"], Settings(), batch_size=1)

    assert [payload["names"] for payload in provider.payloads] == [["甲"], ["乙"]]
    assert report.calls == 2


@pytest.mark.asyncio
async def test_one_failed_batch_does_not_end_the_run(monkeypatch: pytest.MonkeyPatch) -> None:
    provider = FakeProvider([ValueError("boom"), batch(("曼谷大皇宮", "曼谷大皇宫"))])
    monkeypatch.setattr(module, "research_provider", lambda *_a, **_k: provider)

    report = await convert_names(["甲", "曼谷大皇宮"], Settings(), batch_size=1)

    assert report.converted == {"曼谷大皇宮": "曼谷大皇宫"}
    assert len(report.errors) == 1


def test_stored_label_count_reports_what_a_run_would_touch() -> None:
    rows: list[dict[str, Any]] = [
        {"name": "曼谷大皇宮", "names": {"zh-CN": "曼谷大皇宫", "ja": "王宮"}},
        {"name": "暹羅海洋世界", "names": {"zh-CN": "暹羅海洋世界"}},
        {"name": "高尾山"},
    ]

    assert stored_label_count(rows) == 2


def test_a_row_only_loses_its_label_in_the_step_that_could_replace_it() -> None:
    """Clearing every label up front let a failed run write the stripped rows out."""
    rows: list[dict[str, Any]] = [
        {"name": "曼谷大皇宮", "names": {"zh-CN": "曼谷大皇宫", "ja": "王宮"}},
        {"name": "暹羅海洋世界", "names": {"zh-CN": "暹羅海洋世界"}},
    ]

    # A run that converted nothing must not be able to empty anything, because the
    # caller refuses to write at all; applying an empty map is the last line of defence.
    assert apply_conversions(rows, {"曼谷大皇宮": "曼谷大皇宫"}) == 1
    assert rows[0]["names"]["zh-CN"] == "曼谷大皇宫"
    assert rows[0]["names"]["ja"] == "王宮"  # other locales are untouched
    # The second row had no conversion, so its stale label goes rather than survive.
    assert "zh-CN" not in rows[1]["names"]


def test_conversions_are_written_onto_the_matching_seed_only() -> None:
    rows: list[dict[str, Any]] = [
        {"name": "曼谷大皇宮", "names": {"ja": "王宮"}},
        {"name": "高尾山", "names": {}},
    ]

    assert apply_conversions(rows, {"曼谷大皇宮": "曼谷大皇宫"}) == 1
    assert rows[0]["names"] == {"ja": "王宮", "zh-CN": "曼谷大皇宫"}
    assert rows[1]["names"] == {}
