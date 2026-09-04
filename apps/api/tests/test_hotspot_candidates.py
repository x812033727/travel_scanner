"""Each case here is a row a weaker check let through when probed against real data."""

from app.hotspots.candidates import (
    CandidateInput,
    NearbyArticle,
    best_article_match,
    decide,
    name_score,
    summarize,
)

OSAKA_CASTLE = (34.687_315, 135.526_201)
KIYOMIZU = (34.994_856, 135.785_046)


def candidate(name: str, city: str = "大阪") -> CandidateInput:
    return CandidateInput(name=name, city_code="KIX", city_qualifier=city)


def article(
    title: str,
    qid: str,
    latitude: float,
    longitude: float,
    *,
    types: tuple[str, ...] = ("Q23413",),  # castle
    names: tuple[str, ...] = (),
    project: str = "ja.wikipedia.org",
) -> NearbyArticle:
    return NearbyArticle(
        wikipedia_project=project,
        title=title,
        qid=qid,
        latitude=latitude,
        longitude=longitude,
        type_ids=frozenset(types),
        names=names,
    )


def test_an_alias_confirms_a_match_that_shares_no_characters() -> None:
    # 金閣寺's article is 鹿苑寺. Comparing titles alone would reject a correct match.
    rokuon = article("鹿苑寺", "Q270983", 35.039_444, 135.729_167, names=("金閣寺", "Kinkaku-ji"))
    best, score = best_article_match("金閣寺", [rokuon])

    assert best is rokuon
    assert score == 1.0


def test_a_neighbouring_landmark_does_not_win_on_distance_alone() -> None:
    # 大阪城ホール is an arena 0.3 km from the castle; a distance-only check took it.
    hall = article("大阪城ホール", "Q1092700", 34.696_9, 135.531_9, types=("Q18674739",))
    castle = article("大坂城", "Q321242", *OSAKA_CASTLE, names=("大阪城",))
    best, _ = best_article_match("大阪城", [hall, castle])

    assert best is castle


def test_a_broader_place_cannot_swallow_a_candidate_that_merely_starts_with_it() -> None:
    # 大阪 ⊂ 大阪企業家博物館, which used to score 0.92 and matched the whole city.
    assert name_score("大阪企業家博物館", "大阪市") < 0.75
    assert name_score("天保山大摩天輪", "天保山") < 0.75
    # A short name that really is most of the longer one still counts.
    assert name_score("宇治平等院", "平等院") >= 0.75


def test_a_shared_prefix_neighbour_is_held_back_by_the_calibrated_threshold() -> None:
    # 天保山大橋 is a bridge 30 m away scoring 0.67; the type gate allows bridges, so
    # only the threshold separates it from the ferris wheel the candidate names.
    bridge = article("天保山大橋", "Q11442325", 34.655_0, 135.428_0, types=("Q12280",))
    assert 0.62 <= name_score("天保山大摩天輪", "天保山大橋") < 0.75

    result = decide(candidate("天保山大摩天輪"), "ChIJ-wheel", 34.654_8, 135.428_2, [bridge])

    assert result.lane == "needs_review"
    assert result.reason == "name_mismatch"
    assert not result.publishable


def test_an_administrative_area_is_rejected_rather_than_queued() -> None:
    city = article("大阪市", "Q35765", 34.693_7, 135.502_2, types=("Q1749269",))

    result = decide(candidate("大阪市"), "ChIJ-city", 34.693_8, 135.502_3, [city])

    assert result.lane == "rejected"
    assert result.reason == "denylisted_type"


def test_the_same_name_in_another_city_is_held_back_by_the_distance_check() -> None:
    # Searching Google for "清水寺 大阪" while Wikipedia answers with Kyoto's temple.
    kyoto = article("清水寺", "Q221716", *KIYOMIZU, types=("Q44539",))

    result = decide(candidate("清水寺"), "ChIJ-osaka-temple", 34.664_0, 135.512_0, [kyoto])

    assert result.lane == "needs_review"
    assert result.reason == "coordinates_disagree"
    assert result.drift_km is not None and result.drift_km > 1.0


def test_three_agreeing_sources_are_publishable() -> None:
    castle = article("大坂城", "Q321242", *OSAKA_CASTLE, names=("大阪城",))

    result = decide(candidate("大阪城"), "ChIJ-castle", 34.687_4, 135.526_0, [castle])

    assert result.lane == "confirmed"
    assert result.reason == "three_sources_agree"
    assert result.publishable
    assert result.google_place_id == "ChIJ-castle"
    assert result.article is not None
    assert result.article.article_url == "https://ja.wikipedia.org/wiki/%E5%A4%A7%E5%9D%82%E5%9F%8E"


def test_a_candidate_google_cannot_find_never_reaches_review() -> None:
    result = decide(candidate("不存在的地方"), None, None, None, [])

    assert result.lane == "rejected"
    assert result.reason == "no_google_place"
    assert result.article is None


def test_no_article_nearby_goes_to_a_human_rather_than_being_dropped() -> None:
    result = decide(candidate("三十三間堂", "京都"), "ChIJ-hall", 34.987_9, 135.771_7, [])

    assert result.lane == "needs_review"
    assert result.reason == "no_nearby_article"


def test_summary_counts_every_lane_and_reason() -> None:
    castle = article("大坂城", "Q321242", *OSAKA_CASTLE, names=("大阪城",))
    resolutions = [
        decide(candidate("大阪城"), "ChIJ-a", 34.687_4, 135.526_0, [castle]),
        decide(candidate("不存在"), None, None, None, []),
    ]

    assert summarize(resolutions) == {
        "confirmed:three_sources_agree": 1,
        "rejected:no_google_place": 1,
    }
