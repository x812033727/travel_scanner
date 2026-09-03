"""Build the Kanto expansion bootstrap (Tokyo additions plus Yokohama and Kamakura).

The Tokyo rows come from a Gemini-curated list of 100 attractions; Yokohama and
Kamakura are new extension destinations of Tokyo that follow the secondary-city
contract (10 general + 3 urban-local + 2 day-trip places, at least one food area).
Like tools/generate_secondary_hotspots.py the output is a checked-in offline catalog:
coordinates come from Wikidata / Wikipedia (never from Google), rows that already
exist in another bootstrap file are skipped, and production never runs this script.
"""

from __future__ import annotations

import json
import re
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
HOTSPOTS = ROOT / "apps" / "api" / "app" / "hotspots"
OUTPUT = HOTSPOTS / "kanto_expansion_bootstrap.json"
EXISTING_FILES = (
    "bootstrap.json",
    "deep_bootstrap.json",
    "secondary_bootstrap.json",
    "food_area_bootstrap.json",
)
USER_AGENT = "TravelScannerKantoCatalog/1.0 (curated bootstrap builder)"
JA = "ja.wikipedia.org"
EN = "en.wikipedia.org"


@dataclass(frozen=True)
class Spec:
    title: str | None
    name: str
    english: str
    category: str
    duration: int
    provenance: str = "gemini"
    depth: tuple[str, int] | None = None  # (depth_kind, access_minutes)
    project: str = JA
    slug: str | None = None


def _s(
    title: str | None,
    name: str,
    english: str,
    category: str,
    duration: int,
    *,
    provenance: str = "gemini",
    depth: tuple[str, int] | None = None,
    project: str = JA,
    slug: str | None = None,
) -> Spec:
    return Spec(title, name, english, category, duration, provenance, depth, project, slug)


# The Gemini list in its original order. Entries that resolve to a Wikidata item the
# catalog already carries (淺草寺, 東京晴空塔, 上野公園, ...) are skipped at build time and
# reported, so the whole list stays here as the audit trail of what was reviewed.
TOKYO: tuple[Spec, ...] = (
    _s("浅草寺", "淺草寺", "Senso-ji", "culture", 90),
    _s("仲見世通り", "仲見世商店街", "Nakamise-dori", "shopping", 60),
    _s("東京スカイツリー", "東京晴空塔", "Tokyo Skytree", "viewpoint", 120),
    _s("東京ソラマチ", "東京晴空街道", "Tokyo Solamachi", "shopping", 120),
    _s("すみだ水族館", "墨田水族館", "Sumida Aquarium", "family", 90),
    _s("上野恩賜公園", "上野恩賜公園", "Ueno Park", "nature", 120),
    _s("恩賜上野動物園", "上野動物園", "Ueno Zoo", "family", 150),
    _s("東京国立博物館", "東京國立博物館", "Tokyo National Museum", "culture", 150),
    _s("国立西洋美術館", "國立西洋美術館", "National Museum of Western Art", "culture", 120),
    _s("アメヤ横丁", "阿美橫丁", "Ameyoko", "food", 90),
    _s("かっぱ橋道具街", "合羽橋道具街", "Kappabashi Kitchen Town", "shopping", 90),
    _s("隅田公園", "隅田公園", "Sumida Park", "nature", 60),
    _s("渋谷スクランブル交差点", "澀谷十字路口", "Shibuya Scramble Crossing", "viewpoint", 30),
    _s("渋谷スクランブルスクエア", "SHIBUYA SKY", "Shibuya Sky", "viewpoint", 90),
    _s("忠犬ハチ公像", "忠犬八公像", "Hachiko Statue", "viewpoint", 20),
    _s("渋谷PARCO", "澀谷 PARCO", "Shibuya PARCO", "shopping", 90),
    _s("宮下公園", "宮下公園", "Miyashita Park", "shopping", 60),
    _s("明治神宮", "明治神宮", "Meiji Jingu", "culture", 90),
    _s("代々木公園", "代代木公園", "Yoyogi Park", "nature", 90),
    _s("竹下通り", "竹下通", "Takeshita Street", "shopping", 60),
    _s("裏原宿", "裏原宿", "Ura-Harajuku", "shopping", 90),
    _s("表参道ヒルズ", "表參道之丘", "Omotesando Hills", "shopping", 90),
    _s("根津美術館", "根津美術館", "Nezu Museum", "culture", 90),
    _s("代官山T-SITE", "代官山蔦屋書店", "Daikanyama T-Site", "shopping", 90),
    _s("新宿御苑", "新宿御苑", "Shinjuku Gyoen", "nature", 120),
    _s("東京都庁舎", "東京都廳展望室", "Tokyo Metropolitan Government Building", "viewpoint", 60),
    _s("歌舞伎町", "歌舞伎町", "Kabukicho", "nightlife", 120),
    _s("思い出横丁", "回憶橫丁", "Omoide Yokocho", "food", 90),
    _s("新宿ゴールデン街", "新宿黃金街", "Golden Gai", "nightlife", 90),
    _s("東急歌舞伎町タワー", "東急歌舞伎町 TOWER", "Tokyu Kabukicho Tower", "shopping", 120),
    _s("中野ブロードウェイ", "中野百老匯", "Nakano Broadway", "shopping", 120),
    _s("サンシャインシティ", "太陽城", "Sunshine City", "family", 180),
    _s("乙女ロード", "池袋乙女路", "Otome Road", "shopping", 90),
    _s("東京駅", "東京車站丸之內站房", "Tokyo Station", "culture", 60),
    _s("皇居", "皇居與二重橋", "Imperial Palace", "culture", 90),
    _s("皇居東御苑", "皇居東御苑", "Imperial Palace East Gardens", "nature", 90),
    _s("丸の内仲通り", "丸之內仲通", "Marunouchi Naka-dori", "shopping", 60),
    _s("三菱一号館美術館", "三菱一號館美術館", "Mitsubishi Ichigokan Museum", "culture", 90),
    _s("銀座四丁目交差点", "銀座四丁目十字路口", "Ginza 4-chome Crossing", "viewpoint", 30),
    _s("GINZA SIX", "GINZA SIX", "Ginza Six", "shopping", 120),
    _s("伊東屋", "伊東屋銀座本店", "Itoya Ginza", "shopping", 60),
    _s("日本橋 (東京都中央区)", "日本橋麒麟之翼", "Nihonbashi Bridge", "culture", 30),
    _s("コレド室町", "COREDO 室町", "Coredo Muromachi", "shopping", 90),
    _s("東京タワー", "東京鐵塔", "Tokyo Tower", "viewpoint", 90),
    _s("増上寺", "增上寺", "Zojoji Temple", "culture", 60),
    _s("六本木ヒルズ", "六本木之丘森大樓", "Roppongi Hills", "viewpoint", 150),
    _s("国立新美術館", "國立新美術館", "National Art Center Tokyo", "culture", 120),
    _s("東京ミッドタウン", "東京中城", "Tokyo Midtown", "shopping", 120),
    _s("麻布台ヒルズ", "麻布台之丘", "Azabudai Hills", "viewpoint", 120),
    _s(
        "チームラボボーダレス", "teamLab Borderless 麻布台之丘", "teamLab Borderless", "family", 150
    ),
    _s("芝公園", "芝公園", "Shiba Park", "nature", 60),
    _s(
        "東京都庭園美術館", "東京都庭園美術館", "Tokyo Metropolitan Teien Art Museum", "culture", 90
    ),
    _s("築地場外市場", "築地場外市場", "Tsukiji Outer Market", "food", 90),
    _s("豊洲市場", "豐洲市場", "Toyosu Market", "food", 120),
    _s("豊洲 千客万来", "千客萬來", "Toyosu Senkyaku Banrai", "food", 120),
    _s("チームラボプラネッツ", "teamLab Planets TOKYO", "teamLab Planets", "family", 120),
    _s("お台場海浜公園", "台場海濱公園", "Odaiba Marine Park", "beach", 90),
    _s("レインボーブリッジ", "彩虹大橋", "Rainbow Bridge", "viewpoint", 60),
    _s(
        "ダイバーシティ東京 プラザ",
        "DiverCity Tokyo Plaza",
        "DiverCity Tokyo Plaza",
        "shopping",
        120,
    ),
    _s("FCGビル", "富士電視台本社大樓", "Fuji TV Building", "viewpoint", 90),
    _s("東京ビッグサイト", "東京國際展示場", "Tokyo Big Sight", "culture", 60),
    _s("葛西臨海公園", "葛西臨海公園", "Kasai Rinkai Park", "family", 180),
    _s("秋葉原", "秋葉原電器街", "Akihabara Electric Town", "shopping", 120),
    _s("秋葉原ラジオ会館", "秋葉原無線電會館", "Akihabara Radio Kaikan", "shopping", 90),
    _s("神田明神", "神田明神", "Kanda Myojin Shrine", "culture", 60),
    _s("神田古書店街", "神保町古書街", "Jimbocho Book Town", "shopping", 90),
    _s("両国国技館", "兩國國技館", "Ryogoku Kokugikan", "culture", 120),
    _s("すみだ北斎美術館", "墨田北齋美術館", "Sumida Hokusai Museum", "culture", 90),
    _s("江戸東京博物館", "江戶東京博物館", "Edo-Tokyo Museum", "culture", 150),
    _s(
        "スターバックス リザーブ ロースタリー 東京",
        "星巴克臻選東京烘焙工坊",
        "Starbucks Reserve Roastery Tokyo",
        "shopping",
        60,
    ),
    _s("目黒川", "目黑川櫻花林蔭道", "Meguro River Cherry Blossoms", "nature", 90),
    _s("蔵前", "藏前", "Kuramae", "shopping", 90),
    _s("清澄庭園", "清澄庭園", "Kiyosumi Gardens", "nature", 60),
    _s("東京都現代美術館", "東京都現代美術館", "Museum of Contemporary Art Tokyo", "culture", 120),
    _s("谷中銀座", "谷中銀座商店街", "Yanaka Ginza", "shopping", 90),
    _s("根津神社", "根津神社", "Nezu Shrine", "culture", 60),
    _s("神楽坂", "神樂坂", "Kagurazaka", "food", 90),
    _s("浜離宮恩賜庭園", "濱離宮恩賜庭園", "Hamarikyu Gardens", "nature", 90),
    _s("旧芝離宮恩賜庭園", "舊芝離宮恩賜庭園", "Kyu Shiba Rikyu Garden", "nature", 60),
    _s("六義園", "六義園", "Rikugien", "nature", 90),
    _s("小石川後楽園", "小石川後樂園", "Koishikawa Korakuen", "nature", 90),
    _s("等々力渓谷", "等等力溪谷", "Todoroki Valley", "nature", 90),
    _s("国営昭和記念公園", "昭和紀念公園", "Showa Memorial Park", "nature", 180),
    _s("高尾山", "高尾山", "Mount Takao", "nature", 300),
    _s("下北沢", "下北澤", "Shimokitazawa", "shopping", 120),
    _s("自由が丘", "自由之丘", "Jiyugaoka", "shopping", 120),
    _s("ハーモニカ横丁", "吉祥寺口琴橫丁", "Harmonica Yokocho", "food", 90),
    _s("井の頭恩賜公園", "井之頭恩賜公園", "Inokashira Park", "nature", 120),
    _s("三鷹の森ジブリ美術館", "三鷹之森吉卜力美術館", "Ghibli Museum", "family", 150),
    _s("東京ドームシティ", "東京巨蛋城", "Tokyo Dome City", "family", 180),
    _s("題経寺", "柴又帝釋天", "Shibamata Taishakuten", "culture", 120),
    _s("戸越銀座商店街", "戶越銀座商店街", "Togoshi Ginza", "food", 90),
    _s(
        "江戸東京たてもの園",
        "江戶東京建築園",
        "Edo-Tokyo Open Air Architectural Museum",
        "culture",
        150,
    ),
    _s("東京ディズニーランド", "東京迪士尼樂園", "Tokyo Disneyland", "family", 480),
    _s("東京ディズニーシー", "東京迪士尼海洋", "Tokyo DisneySea", "family", 480),
    _s("サンリオピューロランド", "三麗鷗彩虹樂園", "Sanrio Puroland", "family", 240),
    _s("よみうりランド", "讀賣樂園", "Yomiuriland", "family", 300),
)

# Extension destinations: the order is the editorial contract shared with
# secondary_bootstrap.json (10 general, 3 urban-local deep, 2 day-trip deep).
YOKOHAMA: tuple[Spec, ...] = (
    _s("みなとみらい21", "橫濱港未來21", "Minato Mirai 21", "viewpoint", 180),
    _s("横浜赤レンガ倉庫", "橫濱紅磚倉庫", "Yokohama Red Brick Warehouse", "shopping", 90),
    _s("横浜中華街", "橫濱中華街", "Yokohama Chinatown", "food", 120, provenance="editorial"),
    _s("山下公園", "山下公園", "Yamashita Park", "nature", 60, provenance="editorial"),
    _s(
        "横浜ランドマークタワー",
        "橫濱地標塔",
        "Yokohama Landmark Tower",
        "viewpoint",
        90,
        provenance="editorial",
    ),
    _s(
        "カップヌードルミュージアム 横浜",
        "杯麵博物館",
        "Cup Noodles Museum Yokohama",
        "family",
        120,
        provenance="editorial",
    ),
    _s("三渓園", "三溪園", "Sankeien Garden", "nature", 120, provenance="editorial"),
    _s(
        "横浜美術館", "橫濱美術館", "Yokohama Museum of Art", "culture", 120, provenance="editorial"
    ),
    _s(
        "横浜港大さん橋国際客船ターミナル",
        "大棧橋",
        "Osanbashi Pier",
        "viewpoint",
        60,
        provenance="editorial",
    ),
    _s(
        "元町 (横浜市)",
        "元町商店街",
        "Motomachi Shopping Street",
        "shopping",
        90,
        provenance="editorial",
    ),
    _s(
        "野毛 (横浜市)",
        "野毛小路",
        "Noge",
        "nightlife",
        120,
        provenance="editorial",
        depth=("urban_local", 18),
    ),
    _s(
        "港の見える丘公園",
        "港見丘公園",
        "Harbor View Park",
        "viewpoint",
        60,
        provenance="editorial",
        depth=("urban_local", 26),
    ),
    _s(
        "横浜市開港記念会館",
        "橫濱市開港紀念會館",
        "Yokohama Port Opening Memorial Hall",
        "culture",
        60,
        provenance="editorial",
        depth=("urban_local", 34),
    ),
    _s(
        "横浜・八景島シーパラダイス",
        "八景島海島樂園",
        "Hakkeijima Sea Paradise",
        "family",
        300,
        provenance="editorial",
        depth=("day_trip", 55),
    ),
    _s(
        "称名寺 (横浜市)",
        "稱名寺",
        "Shomyoji Temple",
        "culture",
        90,
        provenance="editorial",
        depth=("day_trip", 65),
    ),
)

KAMAKURA: tuple[Spec, ...] = (
    _s("高徳院", "鎌倉大佛高德院", "Kotoku-in", "culture", 60),
    _s("鶴岡八幡宮", "鶴岡八幡宮", "Tsurugaoka Hachimangu", "culture", 90, provenance="editorial"),
    _s("長谷寺 (鎌倉市)", "長谷寺", "Hase-dera", "culture", 90, provenance="editorial"),
    _s("小町通り", "小町通", "Komachi-dori", "food", 90, provenance="editorial"),
    _s("建長寺", "建長寺", "Kencho-ji", "culture", 90, provenance="editorial"),
    _s("円覚寺", "圓覺寺", "Engaku-ji", "culture", 90, provenance="editorial"),
    _s("由比ヶ浜", "由比濱", "Yuigahama Beach", "beach", 120, provenance="editorial"),
    _s(
        "鎌倉高校前駅",
        "鎌倉高校前站",
        "Kamakurakokomae Station",
        "viewpoint",
        30,
        provenance="editorial",
    ),
    _s("明月院", "明月院", "Meigetsu-in", "nature", 60, provenance="editorial"),
    _s("源氏山公園", "源氏山公園", "Genjiyama Park", "nature", 60, provenance="editorial"),
    _s(
        "報国寺 (鎌倉市)",
        "報國寺竹林",
        "Hokoku-ji Bamboo Garden",
        "nature",
        60,
        provenance="editorial",
        depth=("urban_local", 18),
    ),
    _s(
        "銭洗弁財天宇賀福神社",
        "錢洗弁財天",
        "Zeniarai Benten Shrine",
        "culture",
        60,
        provenance="editorial",
        depth=("urban_local", 26),
    ),
    _s(
        "稲村ヶ崎",
        "稻村崎",
        "Inamuragasaki",
        "viewpoint",
        60,
        provenance="editorial",
        depth=("urban_local", 34),
    ),
    _s(
        "江の島",
        "江之島",
        "Enoshima",
        "nature",
        240,
        provenance="editorial",
        depth=("day_trip", 55),
    ),
    _s(
        "新江ノ島水族館",
        "新江之島水族館",
        "Enoshima Aquarium",
        "family",
        150,
        provenance="editorial",
        depth=("day_trip", 65),
    ),
)

CITIES: dict[str, tuple[Spec, ...]] = {"NRT": TOKYO, "YOK": YOKOHAMA, "KMK": KAMAKURA}
EXTENSION_CITIES = ("YOK", "KMK")

# Reviewed coordinates for places whose Wikipedia page or Wikidata item carries no
# usable coordinate. Each entry names the public page the coordinate was read from.
COORDINATE_OVERRIDES: dict[tuple[str, str], tuple[float, float, str]] = {
    (JA, "渋谷スクランブルスクエア"): (
        35.6585,
        139.7022,
        "https://www.shibuya-scramble-square.com/",
    ),
    (JA, "忠犬ハチ公像"): (35.6590, 139.7006, "https://www.city.shibuya.tokyo.jp/"),
    (JA, "裏原宿"): (35.6665, 139.7065, "https://www.gotokyo.org/tc/spot/62/index.html"),
    (JA, "代官山T-SITE"): (35.6497, 139.6994, "https://store.tsite.jp/daikanyama/"),
    (JA, "乙女ロード"): (35.7300, 139.7175, "https://www.gotokyo.org/tc/spot/13/index.html"),
    (JA, "銀座四丁目交差点"): (35.6717, 139.7650, "https://www.ginza.jp/"),
    (JA, "伊東屋"): (35.6725, 139.7663, "https://www.ito-ya.co.jp/"),
    (JA, "コレド室町"): (35.6867, 139.7738, "https://mitsui-shopping-park.com/urban/muromachi/"),
    (JA, "チームラボボーダレス"): (
        35.6603,
        139.7423,
        "https://www.teamlab.art/e/borderless-azabudai/",
    ),
    (JA, "豊洲 千客万来"): (35.6455, 139.7862, "https://www.toyosu-senkyakubanrai.jp/"),
    (JA, "チームラボプラネッツ"): (35.6491, 139.7897, "https://www.teamlab.art/e/planets/"),
    (JA, "神田古書店街"): (35.6957, 139.7576, "https://jimbou.info/"),
    (
        JA,
        "スターバックス リザーブ ロースタリー 東京",
    ): (35.6484, 139.6975, "https://www.starbucks.co.jp/roastery/"),
    (JA, "目黒川"): (35.6440, 139.6990, "https://www.gotokyo.org/tc/spot/23/index.html"),
    (JA, "蔵前"): (35.7030, 139.7900, "https://www.gotokyo.org/tc/spot/1652/index.html"),
    (JA, "丸の内仲通り"): (35.6800, 139.7635, "https://www.marunouchi.com/"),
    (JA, "谷中銀座"): (35.7273, 139.7660, "https://www.yanakaginza.com/"),
    (JA, "東京ビッグサイト"): (35.6298, 139.7940, "https://www.bigsight.jp/"),
    (JA, "ハーモニカ横丁"): (35.7036, 139.5795, "https://hamoyoko.jp/"),
    (JA, "戸越銀座商店街"): (35.6160, 139.7160, "https://www.togoshiginza.jp/"),
    (JA, "小町通り"): (35.3215, 139.5515, "https://www.city.kamakura.kanagawa.jp/"),
    (JA, "源氏山公園"): (35.3231, 139.5450, "https://www.city.kamakura.kanagawa.jp/"),
    (JA, "野毛 (横浜市)"): (35.4494, 139.6284, "https://www.welcome.city.yokohama.jp/"),
    (JA, "元町 (横浜市)"): (35.4408, 139.6499, "https://www.motomachi.or.jp/"),
    (JA, "みなとみらい21"): (35.4573, 139.6329, "https://minatomirai21.com/"),
}

# Wikidata still points these at a former venue or at a river mouth, so the reviewed
# coordinate wins even though an item coordinate exists.
PREFER_OVERRIDE = {(JA, "チームラボボーダレス"), (JA, "目黒川")}

# Existing curated rows are keyed by Wikidata item; anything that resolves to one of
# them is a duplicate of the current catalog and must not be re-added.
DEPTH_REASON = "保留地方歷史、生活紋理或自然特色，適合避開第一線地標後深入探索。"


def get_json(url: str, params: dict[str, str]) -> dict[str, Any]:
    request = Request(f"{url}?{urlencode(params)}", headers={"User-Agent": USER_AGENT})
    for attempt in range(3):
        try:
            with urlopen(request, timeout=30) as response:
                result = json.load(response)
            time.sleep(0.75)
            return result
        except HTTPError as exc:
            if exc.code == 429 and attempt < 2:
                time.sleep(10 * (attempt + 1))
                continue
            raise
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2**attempt)
    raise AssertionError("unreachable")


def wikidata_entities(qids: list[str]) -> dict[str, dict[str, Any]]:
    found: dict[str, dict[str, Any]] = {}
    for start in range(0, len(qids), 50):
        payload = get_json(
            "https://www.wikidata.org/w/api.php",
            {
                "action": "wbgetentities",
                "format": "json",
                "ids": "|".join(qids[start : start + 50]),
                "props": "claims",
            },
        )
        found.update(payload.get("entities", {}))
    return found


def wikipedia_pages(project: str, titles: list[str]) -> dict[str, dict[str, Any]]:
    """Map every requested title to its resolved page (or None when missing)."""

    resolved: dict[str, dict[str, Any]] = {}
    for start in range(0, len(titles), 50):
        batch = titles[start : start + 50]
        payload = get_json(
            f"https://{project}/w/api.php",
            {
                "action": "query",
                "format": "json",
                "formatversion": "2",
                "titles": "|".join(batch),
                "redirects": "1",
                "prop": "pageprops|coordinates",
            },
        )
        query = payload.get("query", {})
        remap = {
            item["from"]: item["to"]
            for item in [*query.get("normalized", []), *query.get("redirects", [])]
        }
        pages = {page["title"]: page for page in query.get("pages", []) if not page.get("missing")}
        for title in batch:
            final = title
            seen: set[str] = set()
            while final in remap and final not in seen:
                seen.add(final)
                final = remap[final]
            page = pages.get(final)
            if page is not None:
                resolved[title] = page
    return resolved


def existing_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for filename in EXISTING_FILES:
        rows.extend(json.loads((HOTSPOTS / filename).read_text(encoding="utf-8")))
    return rows


def slug_for(city_code: str, spec: Spec) -> str:
    if spec.slug:
        return spec.slug
    ascii_name = re.sub(r"[^a-z0-9]+", "-", spec.english.casefold()).strip("-")[:70]
    return f"{city_code.casefold()}-{ascii_name}"


def build_city(
    city_code: str, specs: tuple[Spec, ...], used_qids: set[str], existing_names: set[str]
) -> tuple[list[dict[str, Any]], list[str]]:
    by_project: dict[str, list[str]] = {}
    for spec in specs:
        if spec.title:
            by_project.setdefault(spec.project, []).append(spec.title)
    pages = {
        (project, title): page
        for project, titles in by_project.items()
        for title, page in wikipedia_pages(project, titles).items()
    }
    qids = sorted(
        {
            qid
            for page in pages.values()
            if (qid := (page.get("pageprops") or {}).get("wikibase_item"))
        }
    )
    entities = wikidata_entities(qids) if qids else {}

    rows: list[dict[str, Any]] = []
    skipped: list[str] = []
    problems: list[str] = []
    for spec in specs:
        page = pages.get((spec.project, spec.title)) if spec.title else None
        qid = (page.get("pageprops") or {}).get("wikibase_item") if page else None
        override = COORDINATE_OVERRIDES.get((spec.project, spec.title or ""))
        if qid and qid in used_qids:
            skipped.append(f"{city_code} {spec.name} ({spec.english}) = {qid} already curated")
            continue
        if spec.name.casefold() in existing_names or spec.english.casefold() in existing_names:
            skipped.append(f"{city_code} {spec.name} ({spec.english}) already curated by name")
            continue
        if page is None and override is None:
            problems.append(f"{spec.title!r} ({spec.english}): page not found, no override")
            continue

        latitude = longitude = None
        coordinate_source = ""
        extra_source: str | None = None
        claims = entities.get(qid, {}).get("claims", {}) if qid else {}
        p625 = claims.get("P625", [])
        value = p625[0].get("mainsnak", {}).get("datavalue", {}).get("value", {}) if p625 else {}
        page_coordinates = (page.get("coordinates") or []) if page else []
        if override is not None and (spec.project, spec.title or "") in PREFER_OVERRIDE:
            latitude, longitude, extra_source = override
            coordinate_source = "curated_coordinate"
        elif "latitude" in value and "longitude" in value:
            latitude, longitude = value["latitude"], value["longitude"]
            coordinate_source = "wikidata_p625"
        elif page_coordinates:
            latitude, longitude = page_coordinates[0]["lat"], page_coordinates[0]["lon"]
            coordinate_source = "wikipedia_coordinates"
        elif override is not None:
            latitude, longitude, extra_source = override
            coordinate_source = "curated_coordinate"
        else:
            problems.append(f"{spec.title!r} ({spec.english}) = {qid}: no reviewed coordinate")
            continue
        if qid:
            used_qids.add(qid)

        title = page["title"] if page else None
        source_urls: list[str] = []
        if page:
            source_urls.append(f"https://{spec.project}/wiki/{quote(str(title).replace(' ', '_'))}")
        if qid:
            source_urls.append(f"https://www.wikidata.org/wiki/{qid}")
        if extra_source:
            source_urls.append(extra_source)
        record: dict[str, Any] = {
            "slug": slug_for(city_code, spec),
            "name": spec.name,
            "local_name": title or spec.title or spec.english,
            "aliases": [spec.english],
            "city_code": city_code,
            "category": spec.category,
            "latitude": latitude,
            "longitude": longitude,
            "wikipedia_project": spec.project if page else None,
            "wikipedia_title": title,
            "wikidata_item_id": qid,
            "source_urls": source_urls,
            "coordinate_source": coordinate_source,
            "recommended_duration_minutes": spec.duration,
            "is_deep_travel": spec.depth is not None,
            "provenance": spec.provenance,
        }
        if spec.depth is not None:
            depth_kind, access = spec.depth
            record.update(
                {
                    "depth_kind": depth_kind,
                    "depth_score": 82,
                    "depth_reason": DEPTH_REASON,
                    "access_minutes": access,
                    "depth_components": {
                        "locality": 84,
                        "distinctiveness": 83,
                        "feasibility": 80,
                        "evidence": 80,
                    },
                }
            )
        rows.append(record)
    if problems:
        raise RuntimeError(f"{city_code}: unresolved specs:\n  " + "\n  ".join(problems))
    return rows, skipped


def check_extension_contract(city_code: str, rows: list[dict[str, Any]]) -> None:
    if len(rows) != 15:
        raise RuntimeError(f"{city_code}: extension cities need 15 rows, got {len(rows)}")
    deep = [row for row in rows if row["is_deep_travel"]]
    kinds = Counter(row["depth_kind"] for row in deep)
    if kinds != {"urban_local": 3, "day_trip": 2}:
        raise RuntimeError(
            f"{city_code}: deep rows must be 3 urban_local + 2 day_trip, got {kinds}"
        )
    categories = Counter(row["category"] for row in rows)
    if len(categories) < 5 or max(categories.values()) > 6:
        raise RuntimeError(f"{city_code}: category spread {dict(categories)} breaks the contract")
    deep_categories = Counter(row["category"] for row in deep)
    if len(deep_categories) < 3 or max(deep_categories.values()) > 2:
        raise RuntimeError(f"{city_code}: deep category spread {dict(deep_categories)} too narrow")
    if not any(row["category"] == "food" for row in rows):
        raise RuntimeError(f"{city_code}: every destination needs a reviewed food area")


def main() -> None:
    existing = existing_rows()
    used_qids = {row["wikidata_item_id"] for row in existing if row.get("wikidata_item_id")}
    existing_names_by_city: dict[str, set[str]] = {}
    for row in existing:
        names = existing_names_by_city.setdefault(row["city_code"], set())
        for value in (row.get("name"), row.get("local_name"), row.get("wikipedia_title")):
            if value:
                names.add(str(value).casefold())
        names.update(str(value).casefold() for value in row.get("aliases", ()))

    output: list[dict[str, Any]] = []
    all_skipped: list[str] = []
    for city_code, specs in CITIES.items():
        print(f"collecting {city_code} ({len(specs)} specs)", flush=True)
        rows, skipped = build_city(
            city_code, specs, used_qids, existing_names_by_city.get(city_code, set())
        )
        if city_code in EXTENSION_CITIES:
            check_extension_contract(city_code, rows)
        elif any(row["is_deep_travel"] for row in rows):
            raise RuntimeError(f"{city_code}: expansion rows must not be deep-travel rows")
        output.extend(rows)
        all_skipped.extend(skipped)

    slugs = [row["slug"] for row in output]
    if len(set(slugs)) != len(slugs):
        raise RuntimeError("expansion slugs must be unique")
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(output)} rows to {OUTPUT}")
    for line in all_skipped:
        print(f"skipped: {line}")


if __name__ == "__main__":
    main()
