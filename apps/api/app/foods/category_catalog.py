"""Site-wide cuisine categories and the dish → category mapping.

Categories are the third browsing axis of the merchant directory (city → area →
category). They are seeded once, then maintained from the admin panel; the
``DISH_CATEGORIES`` map lets every seeded merchant inherit categories from the
signature dishes it is linked to.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass

from app.foods.catalog import FOOD_SEEDS
from app.i18n import LOCALES

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True)
class CategorySeed:
    slug: str
    names: Mapping[str, str]
    display_order: int


def _c(slug: str, zh_tw: str, zh_cn: str, en: str, ja: str, ko: str, *, order: int) -> CategorySeed:
    return CategorySeed(
        slug=slug,
        names={"zh-TW": zh_tw, "zh-CN": zh_cn, "en": en, "ja": ja, "ko": ko},
        display_order=order,
    )


CATEGORY_SEEDS: tuple[CategorySeed, ...] = (
    _c("sushi", "壽司", "寿司", "Sushi", "寿司", "스시", order=1),
    _c("seafood", "海鮮", "海鲜", "Seafood", "海鮮", "해산물", order=2),
    _c("ramen", "拉麵", "拉面", "Ramen", "ラーメン", "라멘", order=3),
    _c("noodles", "麵食", "面食", "Noodles", "麺類", "면 요리", order=4),
    _c(
        "rice-dishes", "飯食／粥品", "饭食／粥品", "Rice & Congee", "ご飯もの・粥", "밥·죽", order=5
    ),
    _c(
        "dim-sum-dumplings",
        "點心／餃子",
        "点心／饺子",
        "Dim Sum & Dumplings",
        "点心・餃子",
        "딤섬·만두",
        order=6,
    ),
    _c(
        "bbq-grill",
        "燒烤／烤肉",
        "烧烤／烤肉",
        "BBQ & Grill",
        "焼肉・焼き鳥",
        "구이·바비큐",
        order=7,
    ),
    _c(
        "fried-tempura",
        "炸物／天婦羅",
        "炸物／天妇罗",
        "Fried & Tempura",
        "揚げ物・天ぷら",
        "튀김·덴푸라",
        order=8,
    ),
    _c(
        "hotpot-soup",
        "火鍋／湯品",
        "火锅／汤品",
        "Hot Pot & Soups",
        "鍋・スープ",
        "탕·찌개",
        order=9,
    ),
    _c("curry", "咖哩", "咖喱", "Curry", "カレー", "카레", order=10),
    _c(
        "teppan-okonomiyaki",
        "鐵板／大阪燒",
        "铁板／大阪烧",
        "Okonomiyaki & Teppan",
        "お好み焼き・鉄板",
        "오코노미야키·철판",
        order=11,
    ),
    _c(
        "home-style",
        "定食／家常菜",
        "定食／家常菜",
        "Set Meals & Home-style",
        "定食・家庭料理",
        "정식·백반",
        order=12,
    ),
    _c("street-food", "街頭小吃", "街头小吃", "Street Food", "屋台グルメ", "길거리 음식", order=13),
    _c(
        "hawker-market",
        "熟食中心／市場攤",
        "熟食中心／市场摊",
        "Hawker Centres & Markets",
        "ホーカー・市場",
        "호커센터·시장",
        order=14,
    ),
    _c("cafe-tea", "咖啡／茶飲", "咖啡／茶饮", "Cafés & Tea", "カフェ・喫茶", "카페·차", order=15),
    _c(
        "desserts-sweets",
        "甜點／糕餅",
        "甜点／糕饼",
        "Desserts & Sweets",
        "スイーツ・菓子",
        "디저트·과자",
        order=16,
    ),
    _c(
        "izakaya-bar",
        "居酒屋／酒吧",
        "居酒屋／酒吧",
        "Izakaya & Bars",
        "居酒屋・バー",
        "이자카야·바",
        order=17,
    ),
    _c("fine-dining", "高級料理", "高级料理", "Fine Dining", "高級料理", "파인다이닝", order=18),
)

CATEGORY_SEEDS_BY_SLUG: dict[str, CategorySeed] = {seed.slug: seed for seed in CATEGORY_SEEDS}

# Every national dish maps to the categories a merchant serving it belongs to; the
# first entry is the primary category when a merchant has no explicit override.
DISH_CATEGORIES: dict[str, tuple[str, ...]] = {
    "jp-sushi": ("sushi", "seafood"),
    "jp-ramen": ("ramen",),
    "jp-tempura": ("fried-tempura",),
    "jp-okonomiyaki": ("teppan-okonomiyaki", "street-food"),
    "jp-takoyaki": ("street-food", "teppan-okonomiyaki"),
    "jp-tonkatsu": ("fried-tempura", "home-style"),
    "jp-udon": ("noodles",),
    "jp-soba": ("noodles",),
    "jp-yakitori": ("bbq-grill", "izakaya-bar"),
    "jp-wagashi": ("desserts-sweets", "cafe-tea"),
    "kr-kimchi": ("home-style",),
    "kr-bibimbap": ("rice-dishes", "home-style"),
    "kr-bulgogi": ("bbq-grill",),
    "kr-samgyeopsal": ("bbq-grill",),
    "kr-tteokbokki": ("street-food",),
    "kr-japchae": ("home-style",),
    "kr-samgyetang": ("hotpot-soup",),
    "kr-naengmyeon": ("noodles",),
    "kr-hotteok": ("street-food", "desserts-sweets"),
    "kr-gimbap": ("rice-dishes", "street-food"),
    "th-pad-thai": ("noodles", "street-food"),
    "th-tom-yum": ("hotpot-soup", "seafood"),
    "th-green-curry": ("curry", "home-style"),
    "th-som-tam": ("street-food",),
    "th-khao-man-gai": ("rice-dishes",),
    "th-boat-noodles": ("noodles", "street-food"),
    "th-mango-sticky-rice": ("desserts-sweets", "street-food"),
    "th-massaman-curry": ("curry", "home-style"),
    "th-khao-soi": ("noodles", "curry"),
    "th-moo-ping": ("street-food", "bbq-grill"),
    "tw-beef-noodle-soup": ("noodles",),
    "tw-xiaolongbao": ("dim-sum-dumplings",),
    "tw-lu-rou-fan": ("rice-dishes", "home-style"),
    "tw-oyster-omelet": ("street-food", "seafood"),
    "tw-stinky-tofu": ("street-food",),
    "tw-bubble-tea": ("cafe-tea",),
    "tw-gua-bao": ("street-food",),
    "tw-pineapple-cake": ("desserts-sweets",),
    "tw-danzai-noodles": ("noodles",),
    "tw-scallion-pancake": ("street-food",),
    "sg-chicken-rice": ("rice-dishes", "hawker-market"),
    "sg-laksa": ("noodles", "hawker-market"),
    "sg-chilli-crab": ("seafood",),
    "sg-char-kway-teow": ("noodles", "hawker-market"),
    "sg-bak-kut-teh": ("hotpot-soup",),
    "sg-kaya-toast": ("cafe-tea", "desserts-sweets"),
    "sg-satay": ("bbq-grill", "hawker-market"),
    "sg-rojak": ("street-food", "hawker-market"),
    "sg-fish-head-curry": ("curry", "seafood"),
    "sg-ice-kacang": ("desserts-sweets", "hawker-market"),
    "hk-dim-sum": ("dim-sum-dumplings",),
    "hk-roast-goose": ("bbq-grill",),
    "hk-wonton-noodles": ("noodles",),
    "hk-egg-tart": ("desserts-sweets", "cafe-tea"),
    "hk-pineapple-bun": ("cafe-tea", "desserts-sweets"),
    "hk-claypot-rice": ("rice-dishes",),
    "hk-milk-tea": ("cafe-tea",),
    "hk-cart-noodles": ("noodles", "street-food"),
    "hk-siu-mei": ("bbq-grill", "rice-dishes"),
    "hk-congee": ("rice-dishes",),
    "vn-pho": ("noodles",),
    "vn-banh-mi": ("street-food",),
    "vn-bun-cha": ("bbq-grill", "noodles"),
    "vn-goi-cuon": ("street-food", "home-style"),
    "vn-banh-xeo": ("street-food",),
    "vn-cao-lau": ("noodles",),
    "vn-com-tam": ("rice-dishes",),
    "vn-bun-bo-hue": ("noodles",),
    "vn-egg-coffee": ("cafe-tea",),
    "vn-che": ("desserts-sweets",),
}


def categories_for_dishes(
    dish_slugs: tuple[str, ...], extras: tuple[str, ...] = ()
) -> tuple[str, ...]:
    """Ordered, de-duplicated categories for a merchant: dish-derived first, extras last."""

    ordered: list[str] = []
    for dish_slug in dish_slugs:
        for category_slug in DISH_CATEGORIES.get(dish_slug, ()):
            if category_slug not in ordered:
                ordered.append(category_slug)
    for category_slug in extras:
        if category_slug not in ordered:
            ordered.append(category_slug)
    return tuple(ordered)


def validate_names(names: Mapping[str, str]) -> None:
    if set(names) != set(LOCALES):
        raise RuntimeError(f"names must cover exactly the site locales: {sorted(names)}")
    if any(not value.strip() or len(value) > 255 for value in names.values()):
        raise RuntimeError("localized names must be non-empty and at most 255 characters")


def validate_category_catalog() -> None:
    if len(CATEGORY_SEEDS) != 18:
        raise RuntimeError("category catalog must contain exactly 18 categories")
    slugs = [seed.slug for seed in CATEGORY_SEEDS]
    if len(set(slugs)) != len(slugs):
        raise RuntimeError("category slugs must be unique")
    if any(not SLUG_PATTERN.match(slug) for slug in slugs):
        raise RuntimeError("category slugs must be lowercase kebab-case")
    orders = [seed.display_order for seed in CATEGORY_SEEDS]
    if len(set(orders)) != len(orders):
        raise RuntimeError("category display orders must be unique")
    for seed in CATEGORY_SEEDS:
        validate_names(seed.names)
    dish_slugs = {seed.slug for seed in FOOD_SEEDS}
    if set(DISH_CATEGORIES) != dish_slugs:
        missing = sorted(dish_slugs - set(DISH_CATEGORIES))
        unknown = sorted(set(DISH_CATEGORIES) - dish_slugs)
        raise RuntimeError(f"dish categories out of sync: missing={missing} unknown={unknown}")
    for dish_slug, category_slugs in DISH_CATEGORIES.items():
        if not category_slugs:
            raise RuntimeError(f"dish {dish_slug} needs at least one category")
        if len(set(category_slugs)) != len(category_slugs):
            raise RuntimeError(f"dish {dish_slug} lists a category twice")
        unknown_categories = [slug for slug in category_slugs if slug not in CATEGORY_SEEDS_BY_SLUG]
        if unknown_categories:
            raise RuntimeError(
                f"dish {dish_slug} references unknown categories {unknown_categories}"
            )


validate_category_catalog()
