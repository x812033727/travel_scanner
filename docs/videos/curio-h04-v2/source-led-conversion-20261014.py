"""One-time, auditable replacement of H04's unaccepted generated shots.

Run from the repository root. This edits only this episode's video.json. The
original paid image receipts and workdir remain untouched. Do not rerun after
the source-led conversion: the exact 49-shot precondition intentionally fails.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path("docs/videos/curio-h04-v2")
VIDEO = ROOT / "video.json"
S1 = "1959 結案書，第 384–387 頁"
S2 = "1959 帳篷鑑定，第 303–304 頁"
S3 = "1959 Tempalov 證詞，第 309–312 頁"
S4 = "1959 Slobtsov 證詞，第 298–300 頁"
S5 = "Gaume、Puzrin 2021 雪板模型"
S6 = "Puzrin、Gaume 2022 後續考察"
S11 = "Interfax 2019 檢方複查說明"
S12 = "Interfax 2020 檢方記者會"


def diagram(name: str) -> dict:
    return {"template": "diagram", "data": {"svg": f"{ROOT.as_posix()}/diagrams/{name}.svg"}}


def big(kicker: str, text: str, sub: str) -> dict:
    return {"template": "big", "data": {"kicker": kicker, "text": text, "sub": sub}}


def stats(title: str, value: str, label: str, source: str, note: str = "") -> dict:
    item = {"value": value, "label": label}
    if note:
        item["note"] = note
    return {"template": "stats", "data": {"title": title, "stats": [item], "source": source}}


def compare(title: str, left: tuple[str, str], right: tuple[str, str], source: str) -> dict:
    return {"template": "compare", "data": {"title": title,
        "left": {"heading": left[0], "points": [left[1]]},
        "right": {"heading": right[0], "points": [right[1]]}, "source": source}}


def steps(title: str, entries: list[tuple[str, str]], source: str) -> dict:
    return {"template": "steps", "data": {"title": title,
        "steps": [{"title": a, "detail": b} for a, b in entries], "source": source}}


def table(title: str, rows: list[list[str]], source: str) -> dict:
    return {"template": "table", "data": {"title": title,
        "columns": ["資料", "可說到哪一步"], "rows": rows, "source": source}}


# Keep these in episode order so a reviewer can audit the visual rhythm without
# reading the implementation. Each entry preserves its original lines/claims.
REPLACEMENTS = {
    "opening-search": stats("搜救紀錄｜找到帳篷", "2 月 26 日", "1959 年，北烏拉山區", S1),
    "tease-fabric": big("1959 年帳篷鑑定｜四月", "**帳篷布待鑑定**", "切口方向將在報告回答｜來源：鑑定第 303–304 頁"),
    "tease-file": diagram("closure-index-card"),
    "tease-paper": steps("六十多年後｜重新提問", [("2021 模型", "測試小雪板是否可能延後滑動"), ("條件式答案", "不是重現事故當夜")], S5),
    "tease-expedition": stats("後續觀察｜先留下疑問", "2022.01", "兩位當地嚮導走進鄰近山坡", S6),
    "opening-question": big("搜救卷宗留下的核心疑問", "**九人為何離帳？**", "1959 年結案書、後來的研究，回答範圍不同"),
    "trail-search-start": steps("循卷宗往山下看", [("空帳篷", "2 月 26 日發現"), ("殘留足跡", "方向指向山下")], S1),
    "camp-platform-context": diagram("search-record-card"),
    "search-later-weather": big("證據時間差｜卷宗", "**現場已經過一段時間**", "搜救所見不能直接當成事故當夜的完整樣貌"),
    "remaining-boots": diagram("search-evidence-limit"),
    "tent-opening-empty": compare("留物能推論，不能目擊", ("可據以推論", "有人突然離開帳篷"), ("無目擊紀錄", "九人逐一從哪裡出去"), S1),
    "tent-opening-question": diagram("fabric-question-card"),
    "trail-downhill": steps("殘留足跡的方向", [("山坡", "仍能辨認的部分"), ("下方", "指向谷地與森林")], S1),
    "forest-edge-absence": compare("林邊的兩種線索", ("足跡", "靠近林緣後被雪蓋住"), ("火堆", "現場留有火堆殘跡"), S1),
    "fire-site-two": stats("火堆附近", "2 人", "卷宗記錄的發現位置", S1),
    "search-two-times": steps("帳篷裂口的兩個時間點", [("2 月", "搜救者發現帳篷"), ("4 月", "鑑定人檢查布料")], f"{S1}；{S2}"),
    "fabric-workbench": table("帳篷鑑定檢查什麼？", [["切口", "判別由哪一面形成"], ["布料內側", "觀察細微損傷"]], S2),
    "spring-empty-ravine": stats("五月的搜救結果", "4 人", "在溪溝附近被找到", S1),
    "archive-closed-folder": stats("結案決定", "5 月 28 日", "伊凡諾夫簽署", S1),
    "archive-many-pages": table("結案書的四頁", [["384–386", "記錄經過與發現"], ["387", "寫到結案原因"]], S1),
    "archive-ribbon": big("1959 年結案書", "**卷宗在這裡停下**", "它沒有指名當夜滑落的雪板｜來源：結案書第 387 頁"),
    "empty-speaking-room": compare("記者會的說法與待解問題", ("2020 年說法", "提出雪崩解釋"), ("仍待說明", "雪怎樣在那片坡上動起來"), S12),
    "slope-small-feature": compare("不同尺度的坡度", ("整段山坡", "平均看來不算很陡"), ("局部條件", "模型檢驗短而較陡的地形"), S5),
    "camp-open-question": big("雪板模型要回答的問題", "**為何不是立刻滑？**", "研究者測試可能的延遲機制｜來源：Gaume、Puzrin 2021"),
    "model-paper-card": steps("2021 年小型雪板模型", [("提出假設", "局部地形、弱層與搭帳切坡"), ("測試延遲", "風搬雪可能增加負載")], S5),
    "cohesive-snow": compare("雪板是什麼？", ("連成片的雪", "上層可能整塊移動"), ("不是", "整座山同時崩落的說法"), S5),
    "smooth-surface": diagram("ground-and-snow"),
    "ground-step-context": stats("藏在雪下的前提", "局部階梯", "不能從遠景照片直接量出", S5),
    "snow-platform-cut": steps("模型中的搭帳切坡", [("切出平台", "改變坡面幾何"), ("失去支撐", "上方雪層條件因此改變")], S5),
    "quiet-platform": big("模型條件｜不是現場重演", "**不一定立刻滑動**", "切坡後仍需負載累積｜來源：Gaume、Puzrin 2021"),
    "model-snow-sample": compare("延遲還需要什麼？", ("已有條件", "局部地形、弱層與切坡"), ("尚需條件", "逐漸增加的雪上負載"), S5),
    "wind-ridge": diagram("wind-load-conditions"),
    "drift-deposition": stats("模型中的變化", "負載增加", "風吹雪在上方逐漸堆積", S5),
    "measurement-tools": table("當夜缺少完整測量", [["雪厚與強度", "不能逐項還原"], ["風搬雪量", "沒有當夜完整量測"]], S5),
    "small-slab-remains": compare("規模別說大了", ("模型測試", "小規模雪板可能滑動"), ("沒有證明", "整座山大規模崩落"), S5),
    "wind-softens-edge": steps("雪面痕跡可能改變", [("滑動之後", "若有留下低矮邊界"), ("風與時間", "可能使邊界不再清楚")], S5),
    "science-next-evidence": steps("模型之後，去看什麼？", [("論文", "提出可檢驗的條件"), ("後續考察", "回到可能營地附近")], S6),
    "survey-drone": diagram("field-measurement-boundary"),
    "survey-step-close": stats("無人機測量", "局部較陡", "為地形前提增加依據", S6),
    "survey-two-researchers": compare("量得到的，與量不到的", ("後續地形", "無人機量到地表起伏"), ("1959 年雪層", "弱層狀態沒有當夜實測"), S6),
    "snow-return-season": steps("下一次冬季考察的規劃", [("原計畫", "回到雪地"), ("想測試", "雪層與穩定度")], S6),
    "nearby-avalanche-context": diagram("nearby-slab-boundary"),
    "separate-ridge": compare("兩個時間與地點", ("2022 年", "鄰近山坡的新痕跡"), ("1959 年", "不是事故當夜同一片雪"), S6),
    "field-camera-back": stats("相機留下什麼？", "事後痕跡", "沒有拍到雪板滑動過程", S6),
    "softer-snow-block": compare("新痕跡與模型不是完全相同", ("較新的雪板", "雪更軟，坡更陡"), ("2021 年模型", "條件式機制，非現場復原"), S6),
    "natural-slope-no-cut": compare("搭帳平台是差別", ("模型假設", "帳篷上方切坡"), ("新痕跡下方", "沒有被切出的搭帳平台"), S6),
    "field-weather": steps("原定測試與現實限制", [("計畫", "量雪層與穩定度"), ("當時天氣", "試驗未能照計畫完成")], S6),
    "same-evidence-folders": table("這些文章談的是同一次考察", [["研究作者", "介紹後續觀察"], ["ETH、EPFL", "介紹同一批觀察"]], "Puzrin、Gaume 2022；ETH、EPFL 2022"),
    "closing-folder": big("回到證據的重量", "**未知仍在**", "不能因此把所有傳說當成等量證據"),
}

ASSETS = {
    "search-record-card": ("1959 closure record pp. 384-387; abstract date/place card, no site reconstruction", "https://dyatlovpass.com/case-files-384-387-ru"),
    "fabric-question-card": ("1959 tent examination pp. 303-304; abstract unanswered question, not a trace of the canvas", "https://dyatlovpass.com/case-files-303-304-ru"),
    "closure-index-card": ("1959 closure record pp. 384-387; page-index schematic, not document facsimile", "https://dyatlovpass.com/case-files-384-387-ru"),
    "search-evidence-limit": ("1959 closure record pp. 385-386; observation/inference/unknown schematic", "https://dyatlovpass.com/case-files-384-387-ru"),
    "ground-and-snow": ("Gaume and Puzrin 2021 model and Puzrin and Gaume 2022 terrain observations; not a site profile", "https://www.nature.com/articles/s43247-020-00081-8"),
    "wind-load-conditions": ("Gaume and Puzrin 2021 conditional wind-loading model; no incident-night measurements", "https://www.nature.com/articles/s43247-020-00081-8"),
    "field-measurement-boundary": ("Puzrin and Gaume 2022 follow-up; terrain measurement does not measure 1959 snow layers", "https://www.nature.com/articles/s43247-022-00393-x"),
    "nearby-slab-boundary": ("Puzrin and Gaume 2022 follow-up; nearby newer traces are not 1959 event footage", "https://www.nature.com/articles/s43247-022-00393-x"),
}


def main() -> None:
    doc = json.loads(VIDEO.read_text(encoding="utf-8"))
    shots = {scene["id"] for scene in doc["scenes"] if scene["template"] == "shot"}
    if shots != set(REPLACEMENTS):
        raise SystemExit(f"Expected exactly these 49 old shots; missing={shots - set(REPLACEMENTS)} extra={set(REPLACEMENTS) - shots}")
    if len(shots) != 49:
        raise SystemExit(f"Expected 49 old shots, found {len(shots)}")
    old_lines = [(line["id"], line["text"]) for scene in doc["scenes"] for line in scene["lines"]]
    for scene in doc["scenes"]:
        replacement = REPLACEMENTS.get(scene["id"])
        if replacement:
            scene.update(replacement)
    for name, (source, url) in ASSETS.items():
        doc["assets"].append({"path": f"{ROOT.as_posix()}/diagrams/{name}.svg", "source": f"Mokaair original schematic based on {source}", "license": "Mokaair original", "url": url})
    doc["thumbnail"]["data"].pop("shot", None)
    doc.pop("look", None)
    doc["youtube"]["description"] = doc["youtube"]["description"].replace(
        "畫面包含有來源的歷史文件裁切、原創概念圖及情境插畫。概念圖不是一九五九年的實測剖面；情境插畫不是當晚攝影，也不代表逐人行動紀錄。",
        "畫面以有來源的歷史文件裁切與原創資料圖卡說明。圖卡不是一九五九年的現場攝影、實測剖面或逐人行動復原。",
    )
    new_lines = [(line["id"], line["text"]) for scene in doc["scenes"] for line in scene["lines"]]
    if old_lines != new_lines or any(scene["template"] == "shot" for scene in doc["scenes"]):
        raise SystemExit("Narration changed or a shot remains; refusing to write")
    VIDEO.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Converted {len(shots)} shots across {len(doc['scenes'])} scenes; preserved {len(new_lines)} lines")


if __name__ == "__main__":
    main()
