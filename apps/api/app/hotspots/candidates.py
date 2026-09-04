"""Turn an untrusted list of place names into rows that can be published, or reject them.

A candidate name may come from anywhere - an LLM, a blog, a spreadsheet - so nothing it
says is taken on trust. A row only becomes publishable when three independent checks
agree that the same real place is meant:

  1. Google Text Search finds a place for "<name> <city>"       -> identity
  2. A Wikipedia article sits within a kilometre of that place  -> location
  3. That article's Wikidata entity is named by the candidate   -> the same entity
     and is a kind of place worth visiting (P31 via classify_types)

The stored coordinates come from the Wikipedia article, never from Google, because
``DURABLE_COORDINATE_SOURCES`` deliberately excludes provider content: a place ID may be
kept indefinitely, a provider's coordinates may not.

Each rule below exists because a probe run against real Osaka and Kyoto candidates found
the row it lets through would have been wrong:

  - distance alone: 大阪城ホール (an arena) sits 0.3 km from 大阪城
  - titles alone: 金閣寺's article is 鹿苑寺, a correct match sharing no characters,
    so Wikidata aliases have to be consulted
  - containment alone: 大阪 ⊂ 大阪企業家博物館, so every broader place swallowed its
    neighbours until containment required the shorter name to be most of the longer
  - a low threshold: 天保山大橋, a bridge 30 m from 天保山大摩天輪, scores 0.67 on the
    shared prefix. The type gate does not help - a bridge is a legitimate attraction -
    so the threshold sits above it. In the probe every correct match scored 0.83 or
    better and every wrong one 0.67 or worse, which is where 0.75 comes from.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from difflib import SequenceMatcher
from urllib.parse import quote

from app.hotspots.discovery import classify_types, haversine_km

MAX_DRIFT_KM = 1.0
NAME_THRESHOLD = 0.75
CONTAINMENT_MIN_RATIO = 0.6
GEOSEARCH_RADIUS_M = 1200


@dataclass(frozen=True)
class CandidateInput:
    name: str
    city_code: str
    city_qualifier: str

    @property
    def query(self) -> str:
        return f"{self.name} {self.city_qualifier}".strip()


@dataclass(frozen=True)
class NearbyArticle:
    wikipedia_project: str
    title: str
    qid: str
    latitude: float
    longitude: float
    type_ids: frozenset[str] = frozenset()
    names: tuple[str, ...] = ()

    @property
    def article_url(self) -> str:
        return f"https://{self.wikipedia_project}/wiki/{quote(self.title.replace(' ', '_'))}"


@dataclass(frozen=True)
class CandidateResolution:
    candidate: CandidateInput
    lane: str
    reason: str
    google_place_id: str | None = None
    article: NearbyArticle | None = None
    category: str = "culture"
    name_score: float = 0.0
    drift_km: float | None = None

    @property
    def publishable(self) -> bool:
        return self.lane == "confirmed"


def fold(value: str) -> str:
    text = unicodedata.normalize("NFKC", value).casefold()
    return "".join(character for character in text if not character.isspace())


def name_score(candidate: str, other: str) -> float:
    left, right = fold(candidate), fold(other)
    if not left or not right:
        return 0.0
    if left == right:
        return 1.0
    if left in right or right in left:
        ratio = min(len(left), len(right)) / max(len(left), len(right))
        return 0.92 if ratio >= CONTAINMENT_MIN_RATIO else 0.40
    return SequenceMatcher(None, left, right).ratio()


def best_article_match(
    name: str, articles: list[NearbyArticle]
) -> tuple[NearbyArticle | None, float]:
    """Pick the nearby article whose title or any Wikidata name best fits the candidate."""
    best: NearbyArticle | None = None
    best_score = 0.0
    for article in articles:
        score = max(
            name_score(name, value) for value in (article.title, *article.names)
        )
        if score > best_score:
            best, best_score = article, score
    return best, best_score


def decide(
    candidate: CandidateInput,
    google_place_id: str | None,
    google_latitude: float | None,
    google_longitude: float | None,
    articles: list[NearbyArticle],
) -> CandidateResolution:
    if not google_place_id or google_latitude is None or google_longitude is None:
        return CandidateResolution(candidate, "rejected", "no_google_place")

    article, score = best_article_match(candidate.name, articles)
    if article is None:
        return CandidateResolution(
            candidate, "needs_review", "no_nearby_article", google_place_id
        )

    drift = haversine_km(
        article.latitude, article.longitude, google_latitude, google_longitude
    )
    category, type_status, type_reason = classify_types(set(article.type_ids))

    def outcome(lane: str, reason: str) -> CandidateResolution:
        return CandidateResolution(
            candidate=candidate,
            lane=lane,
            reason=reason,
            google_place_id=google_place_id,
            article=article,
            category=category,
            name_score=round(score, 3),
            drift_km=round(drift, 3),
        )

    if score < NAME_THRESHOLD:
        return outcome("needs_review", "name_mismatch")
    if drift > MAX_DRIFT_KM:
        return outcome("needs_review", "coordinates_disagree")
    if type_status == "rejected":
        # An administrative area is not somewhere you visit; do not queue it for review.
        return outcome("rejected", type_reason or "denylisted_type")
    if type_status != "auto_approved":
        return outcome("needs_review", type_reason or "unknown_type")
    return outcome("confirmed", "three_sources_agree")


def summarize(resolutions: list[CandidateResolution]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for resolution in resolutions:
        key = f"{resolution.lane}:{resolution.reason}"
        counts[key] = counts.get(key, 0) + 1
    return counts
