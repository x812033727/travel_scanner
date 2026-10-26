"""Build an unapproved C04 successor; does not call any remote or media service."""
import copy
import hashlib
import json
import re
from pathlib import Path

DEST = Path(__file__).resolve().parent
OLD = DEST.parents[1] / "story-everyday-bubble-wrap-c04"
source = json.loads((OLD / "video.json").read_text())
old_claims = {}
for row in (OLD / "draft-lines.tsv").read_text().splitlines():
    chapter, ident, text, facts = row.split("\t")
    old_claims[ident] = facts

doc = copy.deepcopy(source)
doc["slug"] = "story-everyday-bubble-wrap-c04-remake-20261025"
doc.pop("series", None)  # A candidate must not bind a second video to the existing episode row.
doc["target_minutes"] = [12, 14]
doc["voice"]["style"] = "標準國語，咬字清楚，台北人平常說話的語調。說書人，像在跟朋友講一個等不及要分享的故事。有起伏、有戲：揭曉前刻意停一拍，問句上揚。關鍵數字放慢。語速像平常聊天，一秒四到五個字，句與句之間不拖。絕不平、絕不像在念稿。"
doc["voice"]["performance"] = "對一個人說話，利害與問題有好奇，機械設計用動作講清楚；公司回顧保留歸屬，不演歷史現場。"
doc["subtitles"] = {"burn_in": True}
doc["youtube"]["title"] = "泡泡紙怎麼救包裹？1957 年它還想貼牆｜品牌故事"
doc["thumbnail"]["data"] = {"headline": "一口氣救貨", "sub": "1957年還想貼牆", "brand": "BUBBLE WRAP", "tag": "品牌故事", "shot": "c04r-h02"}

open_rows = [
    ("H01", "你寄出去的東西，會不會只隔著兩張薄膜，就得承受一路搬運的碰撞？", "F01,F04;兩張膜構造配明示觀眾假想利害，非事故紀錄", "Close-up at a packing desk, one worried adult facing the camera while holding a raised-cell sheet beside an intact plain ceramic cup and an open unmarked carton, soft window light."),
    ("H02", "想像你站在包裝桌前，捏著一片鼓泡的透明材料；每格裡面封著的，只是空氣。", "F01;明示假想包裝桌，非歷史重建", "Medium shot at a packing desk, one adult facing the camera and gently pinching the edge of a plain translucent raised-cell sheet, overcast window light."),
    ("H03", "我覺得最有意思的是，這種小氣室原本被寫進牆面覆層的設計。", "F01,F02;旁白反應與已確認的牆面前提", "Close-up at a materials table, one curious adult holding a small raised plastic sample beside a blank wall, soft lamp light."),
    ("H04", "製造它的 Sealed Air，後來把這段起點寫進公司史。", "F02;公司回顧歸屬", "Medium shot at a materials desk, one anonymous adult opening a plain blank folder beside a raised-cell sample, soft lamp light."),
    ("H05", "可兩張膜之間那條細細的接縫，會讓這個設計碰到一道意外的難題。", "F01,F04;兩份核發專利的接合問題，未揭答案", "Close-up at a workbench, one technician tracing the narrow sealed edge of a raised plastic cell with a fingertip, soft side light."),
    ("H06", "今天跟著泡泡紙，看看一個牆面構想，怎麼遇上你寄包裹時的難題。", "editorial:點名題目與規模的承諾，非歷史人物行程", "Medium shot at a studio table, one anonymous maker looking from a plain embossed sheet toward an open unmarked carton, soft window light."),
    ("H07", "看起來只是封住一口空氣，它到底怎麼承擔保護貨物的工作？", "F01,F04;全片問題", "Close-up at a parcel table, one anonymous packer gently placing an intact plain cup beside a translucent cushioning sheet, soft overhead light."),
]

replacements = {
    "O01": "牆面要的，是又輕又軟的立體花紋；那份核發專利的做法，是用薄膜和背層把空氣封起來。",
    "O02": "那份後來在一九六二年核發的專利，發明人欄只列一位工程師。",
    "O03": "圖紙把牆面與家具覆層列為用途，表面的紋理則由一格格氣室撐起來。",
    "O11": "核發文本還提到，氣室表面能給家具柔軟的觸感。",
    "I01": "公司二○一三年的回顧，把下一站放在溫室：牆面方向沒起色後，他們試著拿氣室薄膜隔熱。",
    "I03": "這段歷史出自公司的回顧；可隔熱的點子，又怎麼被帶到易碎物旁？",
    "E20": "材料不停往前走，機器卻得把它一格格封好；這樣的設備，要怎麼讓兩張膜準時碰面？",
    "T01": "它讓兩張膜各走一列升溫滾輪，最後在氣室仍被托住時碰面；這是另一份核發專利的設備設計。",
    "T02": "公司在一九六○年成立；那年三月申請、後來核發的圖紙，把加熱、壓紋與冷卻接成了一條路。",
    "T03": "發明人欄這次列出兩位工程師；目標是薄膜不停前進時，形狀仍能保持穩定。",
    "T04": "你看著這兩列滾輪，可能會問：薄膜熱到容易變皺，還怎麼整齊送進凹槽？",
    "T13": "電腦原廠證實那年開始出貨；包材關聯，則只有氣泡材料公司的回顧。",
    "N01": "那是一層包住整張氣泡片的阻隔外層；剛才那份包裝專利的圖二十，把它畫在片材外圍。",
    "N04": "它是圖紙中的構想；這張圖本身，沒有替我們留下首次商用的日期。",
    "N13": "充氣後，材料仍要陪貨物走過多次轉手；原廠把這款產品定位在較重貨物的緩衝用途。",
    "N12": "手冊列的這款氣墊，每十二英吋一道孔線；長卷充氣後，就能沿線撕下一段。",
    "N15": "還記得開頭那面牆嗎？花紋換了工作，氣室負責受壓，接縫和製程負責把這口空氣留給貨物。",
    "N16": "如果是你，拆過最難忘的包裹時，最怕裡面哪樣東西撞壞？留言告訴我。",
    "N17": "想繼續看日用品怎麼換工作、背後又藏著什麼設計選擇，歡迎訂閱品牌故事。",
}

extra = {
    "O04": ("OA", "你若把這張薄膜拿在手上，期待的是輕；貼上牆，又希望凸起不會立刻塌掉。", "editorial;F01設計目標的觀眾視角", "Medium shot beside a blank wall, one anonymous adult holding up a lightweight raised plastic panel with a thoughtful face, soft grey window light."),
    "O10": ("OB", "我覺得有趣的是，空氣先成了一種造型工具；可花紋做得出來，真的就有人想把它貼上牆嗎？", "editorial;F01,F02用途與公司回顧的轉折", "Close-up at a design table, one anonymous maker gently tilting a raised plastic panel and studying its small air cells, soft lamp light."),
    "I05": ("IA", "如果換成你寄一件易碎物，光是外面看起來漂亮，應該沒辦法讓你放心把箱蓋封上。", "editorial:觀眾假想選擇，非測試結論", "Medium shot at a packing counter, one hesitant adult looking at an intact plain cup inside an open box, mild overhead light."),
    "I08": ("IB", "我反而覺得，這時候小泡泡才碰到真正嚴苛的考試：每次搬動，貨物都可能再壓它一次。", "editorial;F04反覆受壓的示意解讀", "Close-up at a packing table, one adult gently pressing a raised-cell sample between a plain cup and an unmarked box wall, soft side light."),
    "E03": ("EA", "你可以想成先鼓起一只小袋，溫度降了，袋子裡外的壓力關係也變了；不是封住就算完成。", "editorial比喻;F04核發文本冷卻縮扁問題", "Close-up at a materials bench, one anonymous technician examining a partly flattened plain air pouch with a puzzled face, soft overhead light."),
    "E08": ("EB", "我第一次讀這兩份設計時，注意到的就是這條窄窄的邊：泡泡的工作變了，連邊緣也得跟著換。", "editorial:旁白閱讀反應;F01,F04", "Close-up at a bench, one adult looking closely at the edge of a translucent raised-cell sheet, soft lamp light."),
    "E15": ("EC", "如果是你要寄的物品，泡泡扁下去時，空氣之外的薄膜也得派上用場。", "editorial;F04氣體與側壁抵抗主張，不當獨立性能測試", "Medium shot at a packing table, one anonymous adult examining an unbroken plain cup above a raised-cell pad, soft grey daylight."),
    "T03": ("TA", "你站在這種連續送膜的設備旁，可以把它想成接力：上一段交來的材料，不能等下一段慢慢準備。", "editorial:假想設備比喻;F05，不作實廠重建", "Wide shot in a neutral demonstration workshop, one adult facing the camera and watching two simple rollers carry a plain plastic strip, mild overhead light."),
    "T10": ("TB", "我覺得這段最有意思：看起來只是在做薄膜，圖紙其實一直在安排它什麼時候軟、什麼時候定住。", "editorial;F05逐段加熱冷卻的解讀", "Close-up in a simple workshop, one anonymous technician holding a firm raised plastic strip just beyond a plain roller, soft side light."),
    "T13": ("TC", "對你而言，這個例子把氣泡片的任務縮得很具體：箱子還得繼續走，裡面的東西就得有人保護。", "editorial;F07用途意義，不增加IBM採購事實", "Wide shot at a loading area, one anonymous porter carefully moving a plain closed crate on a hand trolley, overcast daylight."),
    "N09": ("NA", "你若負責包裝台，拿到的便不只是卷材，還多了一個得和出貨節奏配合的充氣步驟。", "editorial;F09手冊按需充氣的流程解讀", "Medium shot at a modern packing counter, one anonymous adult feeding a plain flat roll into a small unmarked inflation device, soft overhead light."),
    "N14": ("NB", "我喜歡這個小轉彎：一路走到這裡，連空氣該在哪裡出現、什麼時候離開，都成了產品的一部分。", "editorial;F09流程意義", "Close-up at a modern unpacking table, one adult gently flattening a deflated plain cushioning sheet beside an open carton, mild window light."),
}

rows = []
for ident, text, facts, prompt in open_rows:
    rows.append({"ident": ident, "text": text, "facts": facts, "old": None, "prompt": prompt, "chapter": "一口空氣，從牆面走進紙箱" if ident == "H01" else None})
chapter_names = {"先想讓牆面有花紋":"氣室先被畫成牆面花紋", "溫室只是過站":"氣室又被拿去做隔熱", "一九五九年的接縫":"兩張薄膜直接熔成接縫", "箱子裡的工作":"熱膜在滾輪上冷卻定形"}
for oldscene in source["scenes"][8:]:
    ident = oldscene["id"].split("-")[-1].upper()
    if ident not in ("O10","I11"):
        rows.append({"ident": ident, "text": replacements.get(ident, oldscene["lines"][0]["text"]), "facts": old_claims[ident], "old": oldscene, "chapter": chapter_names.get(oldscene.get("chapter"),oldscene.get("chapter"))})
    if ident in extra:
        eid, text, facts, prompt = extra[ident]
        rows.append({"ident": eid, "text": text, "facts": facts, "old": None, "prompt": prompt, "chapter": None})

scenes, claim_rows, narrative = [], [], []
line_for = {}
camera = ["push in", "pan left", "pull out", "pan right", "tilt up"]
chapter = ""
for i, row in enumerate(rows):
    ident = row["ident"]
    if row["chapter"]:
        chapter = row["chapter"]
    if row["old"]:
        scene = copy.deepcopy(row["old"])
    else:
        scene = {"template": "shot", "data": {"prompt": row["prompt"], "visual": "still"}}
    scene["id"] = "c04r-" + ident.lower()
    if ident == "T01":
        scene["template"] = "shot"
        scene["data"] = {"prompt":"Medium shot in a neutral demonstration workshop, one anonymous technician facing the camera while watching two plain strips of film meet at a simple roller, soft window light.","visual":"still"}
    if ident == "N12":
        # A single specified later product; do not imply the spacing applies to every air cushion.
        scene["data"]["prompt"] = "Close-up at a modern packing station, one anonymous adult tearing a single plain inflated cushioning strip along one perforated line, soft overhead light."
    if row["chapter"]:
        scene["chapter"] = chapter
    else:
        scene.pop("chapter", None)
    if scene["template"] == "shot":
        scene["data"]["camera"] = camera[i % len(camera)]
    # Spoken sentences are split at existing punctuation, never padded or time-stretched.
    text = row["text"]
    parts = [text]
    if len(text) > 41:
        candidates = [m.end() for m in re.finditer("[，；：]", text) if 16 <= m.end() <= len(text)-12]
        if candidates:
            split = min(candidates, key=lambda n:abs(n-len(text)/2))
            parts = [text[:split], text[split:]]
    scene["lines"] = []
    for j, part in enumerate(parts):
        lid = f"c04r{ident.lower()}{j+1}"
        line = {"id": lid, "text": part, "emotion": "自然親近，問句上揚" if part.endswith("？") else "說書語氣，自然有起伏"}
        if "IBM" in part:
            line["say"] = part.replace("IBM", "愛比欸姆")
            line["say_for"] = hashlib.sha256(part.encode()).hexdigest()[:12]
        scene["lines"].append(line)
        line_for.setdefault(ident, lid)
        narrative.append({"chapter": chapter, "id": lid, "text": part})
        claim_rows.append({"chapter": chapter, "scene": scene["id"], "line": lid, "text": part, "supports": row["facts"], "status": "PENDING_NEW_REVIEW"})
    scenes.append(scene)

# The answer, comment question and subscription invitation form one explicit outro.
outro = scenes[-3:]
scenes = scenes[:-3] + [{"id":"c04r-outro", "template":"outro", "data":{"title":"一口空氣，換了工作", "cta":"留言分享你最怕撞壞的東西"}, "lines":[line for s in outro for line in s["lines"]]}]
for c in claim_rows:
    if c["scene"] in {s["id"] for s in outro}:
        c["scene"] = "c04r-outro"
doc["scenes"] = scenes

loops = [("H01", "N15", "觀眾寄件時兩張薄膜怎麼承擔保護貨物的工作"), ("H03", "O01", "氣室最初在牆面設計中擔任什麼工作"), ("H05", "E07", "兩張膜的接縫如何換一種做法")]
loops += [("I03","I05","隔熱點子如何由公司回顧轉向易碎物緩衝"), ("T04","T06","熱薄膜變皺時如何整齊送進凹槽")]
for item in source["loops"]:
    # The old cold open is replaced; its four previews are not inherited.
    setup = next((r["ident"] for r in rows if r["old"] and r["old"]["lines"][0]["id"] == item["setup"]), None)
    payoff = next((r["ident"] for r in rows if r["old"] and r["old"]["lines"][0]["id"] == item["payoff"]), None)
    if setup and payoff:
        loops.append((setup,payoff,item["what"]))
# The new chapter turn asks about synchronizing the feeds, which T01 now answers.
loops = [(s, "T01" if s == "E20" else p, "兩張膜如何在連續設備中趕上彼此" if s == "E20" else w) for s,p,w in loops]
loops = [("OB" if s == "O11" else s,p,w) for s,p,w in loops]
doc["loops"] = [{"setup":line_for[s],"payoff":line_for[p],"what":w} for s,p,w in loops]

series = json.loads((OLD / "series.json").read_text())
original_series = copy.deepcopy(series)
series["target_minutes"] = 13
series["title"] = doc["youtube"]["title"]
series["image_model"] = "image-01"
series["look"] = {"preset":"cute-mystery"}

write = lambda file, value: (DEST / file).write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n")
write("video.json", doc)
write("series.json", series)
write("original-series-context.json",original_series)
write("narration-only.json", narrative)
write("claims.json", claim_rows)

script = ["# " + doc["youtube"]["title"], "", "狀態：10-25 新規則重製候選，尚未接受新來源覆核、雙盲、站主核准或付費製作。", ""]
previous = ""
for row in narrative:
    if row["chapter"] != previous:
        script += ["## " + row["chapter"], ""]
        previous = row["chapter"]
    script += [f"[{row['id']}] {row['text']}", ""]
(DEST / "script.md").write_text("\n".join(script))

claims = ["# C04 新版逐句來源映射（待獨立覆核）", "", "這是作者的查核待辦，不是 PASS 收據。原來源閱讀日期為 2026-10-22；本次沒有冒稱重新閱讀所有原件。", "", "原件與段落定位：`../../story-everyday-bubble-wrap-c04/source-matrix.md` 和 `verify-1.md`。新稿不可沿用舊稿的 PASS。", "", "| 句 ID | 旁白 | 來源／界線 | 狀態 |", "| --- | --- | --- | --- |"]
for row in claim_rows:
    claims.append(f"| {row['line']} | {row['text']} | {row['supports']} | PENDING |")
(DEST / "claims.md").write_text("\n".join(claims)+"\n")

brief = """# C04 泡泡紙｜10-25 新規則重製候選

本次依站主「繼續完成後台品牌故事未完成影片，並用新規則重製」及「可以參考 1844」製作新稿。
這是非付費、未核准的後續版本；保留原 C04 稿、原核准與既有媒體，沒有寫入後台或轉移 episode row。

## 問題

原本想貼在牆上的氣室薄膜，究竟憑什麼進入運輸箱、保護寄出去的物品？

## 一句答案

牆面覆層的氣室換成了包裝受力結構，熱封與後續設備設計處理留氣和連續進料；公司的回顧再提供包裝用途的例子。
這是技術用途與公司敘述支持的轉向，不是對銷量、首次客戶或每項性能的獨立證明。

## 站主觀點

採站主指定的 10-25 新規則和 #1844 製作方式，以一張薄膜換工作的因果主線，說給一位觀眾聽。
本稿仍是候選；站主原來核准的是舊 C04 特定文字，這裡不把製作請求當成新逐句稿的核准收據。

## 主線與來源界線

主角是一張封住空氣的薄膜。牆面造型 → 公司回顧的溫室隔熱 → 包裝受力 → 熱封接縫 → 連續進料 → 留氣及後來按需充氣。
三份專利依其列示的申請日期敘述，旁白說明的是後來核發文本，沒有拿申請日證明上市或工廠採用。
溫室與 IBM 1401 包裝關聯明示是 Sealed Air 的回顧；不把 IBM 當首位客戶，也不虛構交易現場。
NewAir 2017 年手冊只證明後來另一產品的使用流程，原廠性能宣稱沒有升格為獨立測試結論。

## 新規則

開場先給觀眾寄件的利害與「兩張薄膜」，再進假想包裝桌；只保留牆面設計和接縫難題兩個後段預告，不再預告溫室。
承諾句與全片問題後接 5 秒片頭。
每章有「你」和明示旁白反應；正文使用實質問題與工程轉折，不用清單灌長。結尾為答案、留言題與訂閱理由。
目標 13 分鐘，video.json 採 12–14 分鐘帶、自然每秒 4–5 字；實際 TTS 尚未生成，估字不能替代實測。
MiniMax image-01、精確 cute-mystery、still 插圖至少七成；繁中燒錄加 CC、其他語言仍依站主後續決定。
縮圖用 story- slug 的 bold layout d，主標「一口氣救貨」、副標「1957年還想貼牆」，採有表情的包裝者與氣泡片。
既定 5 秒片頭放開場後，21 秒 v4 片尾保留；本候選尚未取得實際品牌素材或產生播放器。

## 仍待完成

新稿的獨立來源覆核、雙盲、站主劇本核准與整片張數／預算核准；新 slug 的專屬帳戶、歷史費用讀回與停線測試；
實際旁白長度、音訊與插圖驗收、成片 QA、上傳包及站主看片。C04 舊 PASS 不適用本稿。
"""
(DEST / "brief.md").write_text(brief)

body = "".join(r["text"] for r in narrative)
han = len(re.findall(r"[\u4e00-\u9fff]",body))
notes = {
    "status":"UNAPPROVED_CANDIDATE",
    "author":"/root/remake_c04",
    "source_commit":"2b20c30d359fe5d93a4ea66f013a52fa20a35c05",
    "source_video_sha256":hashlib.sha256((OLD/"video.json").read_bytes()).hexdigest(),
    "reference_pr":1844,
    "slug":doc["slug"],
    "target_minutes":13,
    "narration_characters_with_punctuation":len(body),
    "narration_han_characters":han,
    "estimate_han_seconds_at_4_5":round(han/4.5,2),
    "measured_audio_seconds":None,
    "scenes":len(scenes),
    "lines":len(narrative),
    "shots":sum(s["template"]=="shot" for s in scenes),
    "cards":sum(s["template"] not in ("shot","outro") for s in scenes),
    "loops":len(doc["loops"]),
    "changes":["以五步開場取代四線索清單；僅兩個後段預告，利害問句另作開場setup", "每章加入觀眾視角和明示旁白反應，保留專利／公司回顧／實際銷售的界線", "12–14分鐘目標、自然4–5字語速、繁中燒錄字幕、滿版bold縮圖", "新slug，保留全部舊核准稿與既有媒體", "全部新事實主張仍待獨立覆核；新增假想場景與比喻標editorial"],
    "holds":["未生成TTS；字數估計不可當作13分鐘通過", "C系列新版slug尚無已啟用專屬預算路由；不得以泛slug繞過", "新來源覆核、雙盲、站主劇本及整片報價尚待完成", "原件支持的內容不足時不得以停頓、重述或加速補足時長"],
    "paying_calls":0,
    "backend_writes":0,
}
write("author-notes.json",notes)
print(json.dumps(notes,ensure_ascii=False))
