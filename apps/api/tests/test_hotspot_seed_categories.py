"""A seed's category is what the planner reads, so it has to say what the place is.

`secondary_bootstrap.json` was written with three rows per city per category, and the
categories were handed out to fill that quota rather than to describe the places: a shrine,
a wetland, a monastery and a mountain all arrived as `shopping`. The planner maps the
「想逛街」 interest straight onto `category="shopping"`, so those rows put Itsukushima
Shrine in front of someone who asked for shops.
"""

from __future__ import annotations

from collections import Counter

from app.hotspots.catalog import HOTSPOT_SEEDS

# Words that name a place people visit for what it is, not for what it sells.
NOT_SHOPPING = (
    "神社", "寺", "宮", "城", "公園", "博物館", "美術館", "瀑布", "濕地", "湖", "山",
    "Park", "Museum", "Temple", "Shrine", "Lake", "Falls", "Valley", "lagoon",
)

# Places whose name reads like something else and which really are shopping. Each one needs
# a reason, because the point of the rule is that a quota-filled category cannot hide here.
SHOPPING_EXCEPTIONS = {
    "暹羅百麗宮": "Siam Paragon: 宮 is the mall's own name, not a palace",
    "博多運河城": "Canal City Hakata: a shopping complex called a 城",
    "宮下公園": "RAYARD MIYASHITA PARK: shops and a hotel built over the park",
    "代官山蔦屋書店": "Daikanyama T-Site: 代官山 is the district, the place is a bookshop",
    "東京中城": "Tokyo Midtown: 城 belongs to the Japanese rendering of Midtown",
}


def test_a_shopping_seed_is_somewhere_people_shop() -> None:
    offenders = []
    for seed in HOTSPOT_SEEDS:
        if seed.category != "shopping" or seed.name in SHOPPING_EXCEPTIONS:
            continue
        hits = [word for word in NOT_SHOPPING if word in seed.name]
        if hits:
            offenders.append(f"{seed.slug} {seed.name} reads like {'/'.join(hits)}")
    assert not offenders, (
        "these are filed as shopping but named like somewhere else; correct the category in "
        "CATEGORY_CORRECTIONS, or add the name to SHOPPING_EXCEPTIONS with a reason:\n"
        + "\n".join(offenders)
    )


def test_every_shopping_exception_is_still_a_shopping_seed() -> None:
    """An exception that no longer applies should be deleted, not left to rot."""
    shopping = {seed.name for seed in HOTSPOT_SEEDS if seed.category == "shopping"}
    assert set(SHOPPING_EXCEPTIONS) <= shopping


def test_the_four_places_the_audit_named_are_no_longer_shopping() -> None:
    by_slug = {seed.slug: seed for seed in HOTSPOT_SEEDS}
    assert by_slug["sdj-q11541912"].category == "nature", "榴岡公園 is a park"
    assert by_slug["hij-q41977"].category == "culture", "廣島城 is a castle"
    assert by_slug["hij-q191763"].category == "culture", "嚴島神社 is a shrine"
    assert by_slug["tae-q624313"].category == "nature", "八公山 is a mountain"


# The eight values a seed may carry. Nothing outside this set reaches the planner's
# interest mapping, and a typo would otherwise sit in the data unnoticed.
KNOWN_CATEGORIES = {
    "culture", "nature", "viewpoint", "shopping", "food", "family", "beach", "nightlife",
}


def test_the_catalogue_as_a_whole_is_varied_without_a_quota() -> None:
    """Variety is a property of the catalogue, not something to demand of every city.

    Asserting it per city is what produced the quota: three of each kind in each of them,
    which put a shrine under shopping and a Noh museum under nature. Gyeongju really is
    mostly cultural and Chiang Rai's deep list really is hills.
    """
    counts = Counter(seed.category for seed in HOTSPOT_SEEDS)
    assert set(counts) == KNOWN_CATEGORIES
    assert counts.most_common(1)[0][1] < len(HOTSPOT_SEEDS) * 0.5
    assert min(counts.values()) >= 5
