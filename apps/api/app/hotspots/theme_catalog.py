"""Hotspot themes: the seasonal tags and shop types layered over ``category``.

A hotspot keeps its single ``category`` (culture, nature, shopping …) and gains any
number of themes: a season it is known for (賞櫻, 賞楓 …) with the months that apply,
or the kind of shop it is (藥妝, 電器 …). The taxonomy is seeded from here once and
then maintained from the admin panel, like ``app.foods.category_catalog``; which
hotspot carries which theme lives in ``theme_bootstrap.json`` next to this file.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Literal

from app.i18n import LOCALES

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ThemeKind = Literal["season", "shop"]
THEME_KINDS: tuple[ThemeKind, ...] = ("season", "shop")
SEASON_THEME_COUNT = 6
SHOP_THEME_COUNT = 8


@dataclass(frozen=True)
class ThemeSeed:
    slug: str
    kind: ThemeKind
    names: Mapping[str, str]
    # Default months of a season theme, empty for a shop type. A link in
    # theme_bootstrap.json (or an administrator) may override them per hotspot.
    months: tuple[int, ...]
    display_order: int


def _t(
    slug: str,
    kind: ThemeKind,
    zh_tw: str,
    zh_cn: str,
    en: str,
    ja: str,
    ko: str,
    *,
    months: tuple[int, ...] = (),
    order: int,
) -> ThemeSeed:
    return ThemeSeed(
        slug=slug,
        kind=kind,
        names={"zh-TW": zh_tw, "zh-CN": zh_cn, "en": en, "ja": ja, "ko": ko},
        months=months,
        display_order=order,
    )


# Default months follow Honshu; Hokkaido, Korea and Taiwan bloom and freeze on
# other calendars and override them per hotspot in theme_bootstrap.json.
THEME_SEEDS: tuple[ThemeSeed, ...] = (
    _t("sakura", "season", "賞櫻", "赏樱", "Cherry Blossoms", "桜", "벚꽃", months=(3, 4), order=1),
    _t(
        "autumn-leaves",
        "season",
        "賞楓",
        "赏枫",
        "Autumn Leaves",
        "紅葉",
        "단풍",
        months=(10, 11),
        order=2,
    ),
    _t("ski", "season", "滑雪", "滑雪", "Skiing", "スキー", "스키", months=(12, 1, 2, 3), order=3),
    _t(
        "fireworks",
        "season",
        "花火",
        "花火",
        "Fireworks",
        "花火",
        "불꽃놀이",
        months=(7, 8),
        order=4,
    ),
    _t(
        "illumination",
        "season",
        "燈飾",
        "灯饰",
        "Winter Illuminations",
        "イルミネーション",
        "일루미네이션",
        months=(11, 12, 1, 2),
        order=5,
    ),
    _t(
        "snow-scenery",
        "season",
        "賞雪",
        "赏雪",
        "Snow Scenery",
        "雪景",
        "설경",
        months=(12, 1, 2),
        order=6,
    ),
    _t(
        "drugstore",
        "shop",
        "藥妝",
        "药妆",
        "Drugstores & Cosmetics",
        "ドラッグストア・コスメ",
        "드럭스토어·화장품",
        order=11,
    ),
    _t("electronics", "shop", "電器", "电器", "Electronics", "家電量販店", "전자제품", order=12),
    _t(
        "department-store",
        "shop",
        "百貨",
        "百货",
        "Department Stores & Malls",
        "百貨店・モール",
        "백화점·쇼핑몰",
        order=13,
    ),
    _t(
        "outlet",
        "shop",
        "Outlet 暢貨中心",
        "奥特莱斯",
        "Outlet Malls",
        "アウトレット",
        "아울렛",
        order=14,
    ),
    _t("souvenir", "shop", "伴手禮", "伴手礼", "Souvenirs & Gifts", "お土産", "기념품", order=15),
    _t(
        "vintage",
        "shop",
        "二手古著",
        "二手古着",
        "Vintage & Second-hand",
        "古着・リユース",
        "빈티지·중고",
        order=16,
    ),
    _t(
        "anime-hobby",
        "shop",
        "動漫周邊",
        "动漫周边",
        "Anime & Hobby",
        "アニメ・ホビー",
        "애니메이션·취미",
        order=17,
    ),
    _t(
        "market-street",
        "shop",
        "商店街／市場",
        "商店街／市场",
        "Shopping Streets & Markets",
        "商店街・市場",
        "상점가·시장",
        order=18,
    ),
)
THEME_SEEDS_BY_SLUG: dict[str, ThemeSeed] = {seed.slug: seed for seed in THEME_SEEDS}
SEASON_THEME_SLUGS: frozenset[str] = frozenset(
    seed.slug for seed in THEME_SEEDS if seed.kind == "season"
)
SHOP_THEME_SLUGS: frozenset[str] = frozenset(
    seed.slug for seed in THEME_SEEDS if seed.kind == "shop"
)


def validate_names(names: Mapping[str, str]) -> None:
    if set(names) != set(LOCALES):
        raise RuntimeError(f"names must cover exactly the site locales: {sorted(names)}")
    if any(not value.strip() or len(value) > 255 for value in names.values()):
        raise RuntimeError("localized names must be non-empty and at most 255 characters")


def validate_months(months: Iterable[int]) -> None:
    values = list(months)
    if len(set(values)) != len(values) or any(
        not isinstance(month, int) or isinstance(month, bool) or month not in range(1, 13)
        for month in values
    ):
        raise RuntimeError(f"months must be distinct integers between 1 and 12: {values}")


def validate_theme_catalog() -> None:
    if len(THEME_SEEDS) != SEASON_THEME_COUNT + SHOP_THEME_COUNT:
        raise RuntimeError(
            f"theme catalog must contain exactly {SEASON_THEME_COUNT} season "
            f"+ {SHOP_THEME_COUNT} shop themes"
        )
    slugs = [seed.slug for seed in THEME_SEEDS]
    if len(set(slugs)) != len(slugs):
        raise RuntimeError("theme slugs must be unique")
    if any(not SLUG_PATTERN.match(slug) for slug in slugs):
        raise RuntimeError("theme slugs must be lowercase kebab-case")
    orders = [seed.display_order for seed in THEME_SEEDS]
    if len(set(orders)) != len(orders):
        raise RuntimeError("theme display orders must be unique")
    if len(SEASON_THEME_SLUGS) != SEASON_THEME_COUNT:
        raise RuntimeError(f"expected {SEASON_THEME_COUNT} season themes")
    for seed in THEME_SEEDS:
        if seed.kind not in THEME_KINDS:
            raise RuntimeError(f"theme {seed.slug} has unknown kind {seed.kind}")
        validate_names(seed.names)
        validate_months(seed.months)
        if seed.kind == "shop" and seed.months:
            raise RuntimeError(f"shop theme {seed.slug} must not carry months")
        if seed.kind == "season" and not seed.months:
            raise RuntimeError(f"season theme {seed.slug} needs default months")


validate_theme_catalog()
