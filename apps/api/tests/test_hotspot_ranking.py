from datetime import date

from app.hotspots.ranking import (
    RankingInput,
    calculate_depth_value,
    score_deep_hotspots,
    score_hotspots,
)


def test_ranking_rewards_recent_interest_and_growth() -> None:
    results = score_hotspots(
        [
            RankingInput("rising", 85, 20_000, 10_000, date(2026, 8, 30)),
            RankingInput("steady", 95, 12_000, 12_000, date(2026, 8, 30)),
        ]
    )

    assert [item.hotspot_id for item in results] == ["rising", "steady"]
    assert results[0].growth_rate == 1.0
    assert results[0].growth_score == 100
    assert results[0].sources == ("curated_catalog", "wikimedia_pageviews")
    assert results[0].is_estimate is False


def test_ranking_marks_cold_start_catalog_values_as_estimates() -> None:
    result = score_hotspots([RankingInput("seed", 90)])[0]

    assert result.pageviews_current is None
    assert result.growth_rate is None
    assert result.confidence_score == 35
    assert result.sources == ("curated_catalog",)
    assert result.is_estimate is True


def test_depth_value_and_ranking_keep_local_value_dominant() -> None:
    assert calculate_depth_value(locality=80, distinctiveness=80, feasibility=80, evidence=80) == 80
    results = score_deep_hotspots(
        [
            RankingInput("deep", 70, 100, depth_score=95),
            RankingInput("popular", 70, 1_000_000, depth_score=70),
        ]
    )
    assert [item.hotspot_id for item in results] == ["deep", "popular"]
    assert results[0].quality_score == 95
