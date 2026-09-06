"""Give the 28 imported merchants the English label their name column is for.

Revision ID: 0052_repair_trend_merchant_names
Revises: 0051_guide_run_gemini

``FoodMerchant.name`` is the catalog's English label: ``merchant_names`` reads it for the
``en`` locale and lets Japanese and Korean fall back to it. The trend sweep collected
``name_zh``, which is how Chinese travel writing refers to a shop, and ``trend_import``
put that straight into ``name``. Measured on the live site on 2026-09-07: 28 of the 110
published merchants answered an ``X-Travel-Locale: en`` request with a Chinese name —
「咖哩碗泰菜館」 where the Thai signboard says Charmgang.

The importer now reads ``name_en`` from the batch file, but it never touches a row that
already exists, so the rows already in the database need this.

Every update is conditional on the row still holding that exact Chinese name, so a shop
an administrator has since renamed by hand is left alone. Thailand and Vietnam also get
the Chinese name written into ``names_json``: their script is not one of the five site
locales, so ``merchant_names`` has no original to fall back to and a Chinese reader was
reading ``name`` itself.
"""

import json
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0052_repair_trend_merchant_names"
down_revision: str | None = "0051_guide_run_gemini"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# (slug, the Chinese name the row holds today, the shop's own English label)
NAMES: tuple[tuple[str, str, str], ...] = (
    ("tokyo-fuglen-tokyo", "Fuglen Tokyo 挪威咖啡館", "FUGLEN TOKYO"),
    ("tokyo-camelback-sandwich-espresso", "Camelback 三明治咖啡", "CAMELBACK sandwich&espresso"),
    ("tokyo-yuan-su-jiao-zi-lou", "原宿餃子樓", "Harajuku Gyozaro"),
    ("tokyo-the-roastery-by-nozy-coffee", "The Roastery 咖啡烘焙館", "THE ROASTERY BY NOZY COFFEE"),
    ("tokyo-hattifnatt", "HATTIFNATT 童話樹屋咖啡", "HATTIFNATT Koenji"),
    ("osaka-kyoto-he-wu-ji-xin-ben-dian", "鶴屋吉信 本店", "Tsuruya Yoshinobu Main Store"),
    ("fukuoka-manu-coffee", "瑪奴咖啡 大名店", "manu coffee Daimyo"),
    ("fukuoka-nejikemon", "蔬菜捲串屋 Nejikemon", "Nejikemon"),
    ("fukuoka-bai-jin-cha-fang", "白金茶房", "Shirogane Sabo"),
    ("fukuoka-coffee-county-fukuoka", "COFFEE COUNTY 福岡店", "COFFEE COUNTY Fukuoka"),
    ("sapporo-fabulous", "FAbULOUS 咖啡藝廊", "FAbULOUS"),
    ("okinawa-ohacort", "oHacorté 水果塔專賣店（港川本店）", "oHacorté Minatogawa"),
    ("okinawa-houkiboshi", "Houkiboshi 黑糖可麗露（港川本店）", "Houkiboshi Minatogawa"),
    ("okinawa-faidama", "食堂faidama", "Shokudo faidama"),
    ("okinawa-c-c-breakfast-okinawa", "C&C BREAKFAST 沖繩早餐店", "C&C BREAKFAST OKINAWA"),
    ("bangkok-restaurant-potong", "波通餐廳", "Restaurant Potong"),
    ("bangkok-charmgang", "咖哩碗泰菜館", "Charmgang"),
    ("bangkok-jok-prince", "王子戲院豬肉粥", "Jok Prince"),
    ("bangkok-khao-ekkamai", "米飯泰式餐廳", "Khao Ekkamai"),
    ("chiang-mai-the-goodcery-space", "好物雜貨咖啡", "The Goodcery Space"),
    ("chiang-mai-flo-coffee-brewers", "芙洛手沖咖啡", "Flo Coffee Brewers"),
    ("taipei-dong-qu-fen-yuan", "東區粉圓", "Dongqu Fenyuan"),
    ("kaohsiung-hao-shuang-huang-bu-zong-dian", "蠔爽 黃埔總店", "Hao Shuang Huangpu"),
    (
        "yokohama-yuan-zu-kare-tantanmian-zheng-hu-zong-ben-dian",
        "元祖咖哩擔擔麵 征虎總本店",
        "Ganso Curry Tantanmen Masatora",
    ),
    ("yokohama-chuan-ben-wu-cha-pu", "川本屋茶舖", "Kawamotoya"),
    ("tainan-jin-de-chun-juan", "金得春捲", "Jin De Spring Rolls"),
    ("tainan-xiu-an-bian-dan-dou-hua", "修安扁擔豆花", "Xiu An Do Hua"),
    ("tainan-tai-cheng-shui-guo-bing-dian", "泰成水果冰店", "Tai Cheng Fruit Shop"),
)
KEEP_CHINESE_FOR = ("TH", "VN")
EMPTY_NAMES = ("{}", "null", "")


def _apply(*, forward: bool) -> None:
    bind = op.get_bind()
    if "food_merchants" not in set(sa.inspect(bind).get_table_names()):
        return
    for slug, chinese, english in NAMES:
        old, new = (chinese, english) if forward else (english, chinese)
        bind.execute(
            sa.text("UPDATE food_merchants SET name = :new WHERE slug = :slug AND name = :old"),
            {"new": new, "old": old, "slug": slug},
        )
        # names_json is json, not jsonb, so compare and write the whole value.
        bind.execute(
            sa.text(
                """
                UPDATE food_merchants
                   SET names_json = CAST(:names AS json)
                 WHERE slug = :slug
                   AND country_code IN :countries
                   AND (names_json IS NULL OR TRIM(names_json::text) IN :empty)
                """
            ).bindparams(
                sa.bindparam("countries", expanding=True),
                sa.bindparam("empty", expanding=True),
            ),
            {
                "names": json.dumps({"zh-TW": chinese} if forward else {}, ensure_ascii=False),
                "slug": slug,
                "countries": list(KEEP_CHINESE_FOR),
                "empty": list(EMPTY_NAMES) if forward else [json.dumps({"zh-TW": chinese},
                                                                       ensure_ascii=False)],
            },
        )


def upgrade() -> None:
    _apply(forward=True)


def downgrade() -> None:
    _apply(forward=False)
