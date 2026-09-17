"""Write the zh-TW original of the tech index pack and its research record.

usage: build_tech_index.py       -- (re)writes locales["zh-TW"] of tech-news-2026-index.json
Same shape as build_crypto_index.py: link texts and cited sources are read from the thirteen
article packs, so a title that changed in fact-checking cannot go stale here, and locales other
than zh-TW that the file already holds are left as they are. The tech vertical carries no
disclaimer callout (tech.md), so there is one callout, not two.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "apps/api/app/guides/content"
RESEARCH = ROOT / "docs/tech-news-2026/research"
SLUG = "tech-news-2026-index"
CHECKED = "2026-09-17"

GROUPS = [
    ("消費硬體與晶片", [
        "tech-news-iphone-duo-20260909",
        "tech-news-apple-september-hardware-20260909",
        "tech-news-apple-m6-m5-ultra-20260825",
    ]),
    ("平台與軟體", [
        "tech-news-windows-project-zenith-20260904",
        "tech-news-pixel-drop-20260915",
    ]),
    ("運算基礎設施與半導體", [
        "tech-news-nvidia-vera-rubin-20260915",
        "tech-news-nvidia-cuda-q-20260914",
        "tech-news-nvidia-mediatek-20260831",
    ]),
    ("台灣：電信與數位政策", [
        "tech-news-taiwan-6g-spectrum-20260910",
        "tech-news-taiwan-matsu-cable-20260623",
        "tech-news-taiwan-sovereign-ai-corpus-20260915",
    ]),
    ("歐盟：資安法規與平台條款", [
        "tech-news-eu-cra-reporting-20260911",
        "tech-news-apple-eu-business-terms-20260818",
    ]),
]

CREDIT = {"author": "Mokaair", "license": "© Mokaair", "source_url": None}
DIAGRAM_CAPTION = "讀科技新聞的第一步是分清楚說法的種類：已經適用或開賣、已經發表而且有日期、只有預告或預覽版，或是研討會發言與廠商自己的推估；四種可以依賴的程度不同。"


def p(text):
    return {"type": "paragraph", "text": text}


def h(text):
    return {"type": "heading", "level": 2, "text": text}


packs = {}
for _, slugs in GROUPS:
    for slug in slugs:
        packs[slug] = json.loads((CONTENT / f"{slug}.json").read_text(encoding="utf-8"))

blocks = [
    p("這份索引整理本站 2026 年的科技新聞解析，這一批的事件日落在 2026 年 6 月到 9 月之間，題目的主體是硬體、作業系統與平台、電信與法規，不是 AI 模型本身。內容分成消費硬體與晶片、平台與軟體、運算基礎設施與半導體、台灣的電信與數位政策、歐盟的資安法規與平台條款五組，每一則都回到廠商的新聞稿與技術文件、主管機關的公告或法規原文，再連到完整的解析文章。"),
    p("本索引於 2026 年 9 月 17 日查核。本站沒有實測任何產品、軟體或服務，也不提供購買、升級或換機的建議；這個系列會整理官方定價、規格與條件的差異，但不做「該不該買」「哪一個比較好」的結論。廠商自己測到或宣稱的效能數字，一律寫成「Apple 表示」「NVIDIA 稱」，並連同對照機型、測試條件與「最高」這類限定詞一起寫；拿不到一手來源的數字不寫。各篇的查核日寫在各篇開頭，價格、上市時程與功能的適用地區以各該官方頁面當期公告為準。"),
    {"type": "summary", "items": [
        "這份索引依消費硬體與晶片、平台與軟體、運算基礎設施與半導體、台灣的電信與數位政策、歐盟的資安法規與平台條款五組，整理本站 2026 年的科技新聞解析，每一篇都附官方來源與查核日。",
        "讀科技新聞的第一步是分清楚說法的種類：已經適用或已經開賣、已經發表而且有日期、只有預告或還在預覽版，或是研討會上的發言與廠商自己的推估。",
        "以各篇的查核日為準，歐盟《網路韌性法》第 14 條的通報義務已自 2026 年 9 月 11 日起適用，iPhone Duo 在台灣 10 月 16 日開放預訂、10 月 23 日開始供貨，數位發展部的 6G 頻譜國際研討會沒有公布任何頻段或時程，臺馬四號海纜官方只寫「即將於近期完工」。",
    ]},
    h("先看說法的種類：已適用、已發表、預告、討論"),
    p("同樣是「新消息」，可以依賴的程度差很多。這一批裡，已經適用的例子是歐盟《網路韌性法》：第 71 條第 2 項讓第 14 條的通報義務提前自 2026 年 9 月 11 日起適用，製造商知悉遭積極利用的漏洞或重大資安事故後，要依 24 小時、72 小時等時限通報；整部規則原則上則要到 2027 年 12 月 11 日才適用。已經開賣的例子是 Apple 在 9 月 9 日發表的 iPhone 18 Pro 系列、Apple Watch Series 12、Apple Watch Ultra 4 與 AirPods 5，Apple 台灣版新聞稿寫 9 月 18 日開始供貨。"),
    p("第二種是已經發表、也給了日期，但還沒到：iPhone Duo 同樣在 9 月 9 日發表，Apple 繁體中文版新聞稿寫台灣時間 10 月 16 日晚上 8 點開放預訂、10 月 23 日開始供貨；Apple 調整歐盟地區 App 商業條款的公告在 8 月 18 日發布，主要更新自 10 月 1 日生效，範圍限於歐盟商店前台。看這一類消息要連地區一起看——同一則發表，各地的日期、價格與功能常常不一樣。"),
    p("第三種是預告與預覽版：Apple 說 iPhone Duo 對 Apple Pencil（USB-C）的支援「今年稍晚推出」，沒有給日期；NVIDIA 的 CUDA-Q Logical 在技術文件裡標示為預覽版，API 與行為都可能在之後的版本大幅變動，新聞稿描述它的可用性時卻只寫現已透過 GitHub 提供，全文沒有出現 preview 這個字；微軟的 Project Zenith 在兩篇公告裡都沒有價格、上市時程或適用地區；數位發展部說臺馬四號海纜「即將於近期完工」，那一篇引用的官方文件沒有寫出完工日。"),
    p("第四種是研討會上的發言與廠商自己的推估。數位發展部的 6G 頻譜國際研討會，新聞稿用的詞是探討與期盼；次長說全球 6G 預計於 2030 年起逐步商轉，那是他對國際局勢的判斷，不是台灣的時間表。NVIDIA 表示 DSX MaxLPS 能在同一場地電力額度內最高多出 40% 的 GPU；這個數字用在 Vera Rubin NVL72 時，官方文章自己標明是依 NVIDIA 的投影、限於合適的部署環境，而且要搭配機房電力規劃，不是量測結果。看到「某某已經推出」「某國已經決定」的標題，先回到原文件看它屬於哪一種，是這個系列每一篇都在做的事。"),
    {"type": "table", "header": ["說法的種類", "這一批裡的例子", "先看什麼"], "rows": [
        ["已經適用或已經開賣", "歐盟《網路韌性法》第 14 條的通報義務、Apple 9 月 18 日開始供貨的新機", "適用日或供貨日，以及適用的對象與地區"],
        ["已經發表、有日期", "iPhone Duo 在台灣的預訂與供貨日、Apple 歐盟 App 商業條款 10 月 1 日生效", "日期是哪個地區的、條件有沒有但書"],
        ["預告與預覽版", "Apple Pencil 支援「今年稍晚推出」、CUDA-Q Logical 預覽版、Project Zenith、臺馬四號海纜「即將於近期完工」", "有沒有確切日期、版本與價格"],
        ["研討與廠商推估", "6G 頻譜國際研討會的發言、NVIDIA 標明為投影的 40%", "誰說的、依據什麼條件、是不是量測結果"],
    ], "caption": "2026 年 9 月 17 日查核；各則的狀態以各篇文章的查核日為準，之後可能改變。"},
    {"type": "image", "src": f"/guides/{SLUG}/diagram-1.svg", "alt": "四格圖解：已經適用或開賣、已經發表有日期、預告與預覽版、研討與廠商推估，各自先看什麼", "width": 1600, "height": 900, "caption": DIAGRAM_CAPTION, "credit": CREDIT},
    h("消費硬體與晶片：規格、台灣售價與各自的條件"),
    p("Apple 在 2026 年 9 月 9 日發表 iPhone Duo，新聞稿稱為該公司第一款摺疊 iPhone：打開時內建 7.6 吋螢幕、闔起時外螢幕 5.4 吋，全球採 eSIM 專用設計，台灣售價新台幣 74,900 元起。那一篇另外整理了一件容易漏看的事：Apple 繁體中文版新聞稿寫首波是「超過 63 個國家和地區」，英文版與新加坡版寫的是超過 70 個，效能數字的「最高」在繁體中文版也有幾處被拿掉。同一天發表的 iPhone 18 Pro 系列、Apple Watch Series 12、Apple Watch Ultra 4 與 AirPods 5 另成一篇，重點是台灣定價與兩款手錶共用的「健康感測系統」；台灣版新聞稿的註腳寫明，高血壓通知功能在台灣不會一開始就推出，預計明年推出。"),
    p("8 月 25 日，Apple 發表 M6 與 M5 Ultra 兩顆晶片，由新款 Mac mini 與新款 Mac Studio 首發搭載。Apple 表示 M6 是 Apple 首款 2 奈米製程晶片，M5 Ultra 最高支援 512GB 統一記憶體與 1.2TB/s 頻寬；搭載 M6 的 Mac mini 台灣售價 NT$29,900 起，搭載 M5 Ultra 的 Mac Studio 為 NT$199,900 起。那一篇花了不少篇幅在一件事上：同一顆 M5 Ultra 的 AI 效能倍數，晶片新聞稿與 Mac Studio 新聞稿給的數字不同，測試月份與說法也不同，不能互換。這三篇的效能、續航與準確度數字都是 Apple 自己的測試或宣稱。"),
    h("平台與軟體：功能各自綁機型、地區與語言"),
    p("微軟在 9 月 4 日宣布 Project Zenith，為統一記憶體 64GB 以上、頻寬 250GB/s 以上的「開發者等級裝置」預先安裝開發工具並調整介面預設，並表示會先隨 AMD 的 Ryzen AI Halo 推出；兩篇微軟公告都沒有價格、上市時程或適用地區，也沒有提到台灣。"),
    p("Google 在 9 月 15 日發布 9 月 Pixel Drop，每一項功能各有自己的條件：鍵盤詐騙警示，公告寫的是從美國開始、適用 Pixel 6 以上機型；通知詐騙警示這次新增 9 個國家與 6 種語言；Pixel Watch 的更新只給 Pixel Watch 5，其中「主動建議」還要搭配 Pixel 11。那一篇引用的四份來源，名單裡都沒有出現台灣，Google 也沒有寫台灣被排除在外。"),
    h("運算基礎設施與半導體：估算、投影與申報書"),
    p("NVIDIA 在 9 月有兩則公告。9 月 14 日，NVIDIA 為開源的 CUDA-Q 平台新增 CUDA-Q Logical；技術文件把它定義為容錯量子運算的資源估算工具，不會把排程送上硬體執行，公告裡也沒有出現新的量子電腦。公告提到的「1,000 個邏輯量子位元只需要 150,000 個物理量子位元」，是 Iceberg Quantum 用這套工具得到的模型估算，不是已經做出來的硬體。9 月 15 日的 AI Infra Summit，兩篇官方公告裡沒有新晶片，談的是電力：NVIDIA 表示衡量 AI 機房的指標正從尖峰效能轉向每百萬瓦能產出多少 token。那一篇把夥伴實測、NVIDIA 自己的投影與 NVIDIA 轉述第三方的數字分開來寫。"),
    p("8 月 31 日，NVIDIA 與聯發科技宣布深化在 AI 基礎建設、邊緣 AI 運算與車用三個領域的合作，NVIDIA 並投資 35 億美元於聯發科技發行的可轉換公司債。新聞稿只寫了這個金額；發行總額 39 億美元、年息 0%、暫定的發行日與到期日這些條件，寫在聯發科技同一天向公開資訊觀測站申報的定價公告裡。NVIDIA 認購的是債券、不是股份，兩份新聞稿也都沒有發表新產品；本站不提供投資建議。"),
    h("台灣：頻譜、海纜與語料庫"),
    p("數位發展部在 9 月 10 日舉辦「頻譜政策領航：邁向6G新世代」國際研討會，討論 6G 的地面與非地面網路整合，以及 AI 帶來的頻譜需求；新聞稿沒有點名任何頻段，也沒有給台灣自己的 6G 時程，而《無線電頻率供應計畫》（114 年 2 月修正）全文沒有出現「6G」。6 月 23 日，數位發展部說明透過前瞻預算補助中華電信建置的臺馬四號海纜與馬祖四鄉微波站「即將於近期完工」；那一篇也整理了 2026 年 4 月 29 日臺馬三號北竿－東引段海纜全斷時，中華電信改開微波通訊備援的經過。"),
    p("9 月 15 日，數位發展部啟動「臺灣主權AI訓練語料庫」的民間語料徵集，邀請出版社與作家把出版品授權給 AI 訓練使用。官方的推動方式是無償授權；授權條款寫明此項授權不得再授權與轉讓，也寫明即使原語料資料後續停止提供使用，不影響已完成之訓練成果。至於退出，那一篇引用的四份官方文件只寫了「設有完善的退出下架申請管道」這一句，未見這個管道的網址、表單或處理時間。"),
    h("歐盟：通報義務上路，App 商業條款改版"),
    p("《網路韌性法》（Cyber Resilience Act）第 14 條的通報義務自 2026 年 9 月 11 日起適用，歐盟網路安全局（ENISA）同步啟用單一通報平台：製造商知悉遭積極利用的漏洞或重大資安事故後，至遲 24 小時內送早期警訊、72 小時內送完整通報。ENISA 的常見問答寫明，這項義務也適用於 2027 年 12 月 11 日前已上市的產品；平台目前是「初始運作量能」，只支援英文介面，第 15 條的自願通報功能還沒開放。"),
    p("Apple 在 8 月 18 日宣布調整歐盟地區的 App 商業條款：原本的核心技術費，改為對替代市集本身與透過替代市集或網站發布的 iOS、iPadOS App 收取的 5% 核心技術抽成，並允許 App 同時提供 Apple 應用程式內購買與替代付款選項，主要更新自 10 月 1 日生效。這些條款只適用於在歐盟商店前台上架的 App；那一篇引用的四個 Apple 頁面，都沒有提到台灣或其他地區是否會採用相同的條款。"),
    {"type": "faq", "items": [
        {"question": "這個系列為什麼不寫購買建議？", "answer": "這是本站科技內容的編輯界線：可以整理官方定價、規格與條件的差異，讓讀者自己判斷，但不寫「該不該買」「值不值得升級」「哪一支比較好」，也不把價格比較做成「現在買最划算」這類結論。官方定價會寫，並附來源與查核日；各篇的台灣售價都是查核日當天官方頁面的數字，實際定價與供貨以官方當期公告為準。"},
        {"question": "廠商給的效能數字，這個系列怎麼處理？", "answer": "一律歸因，並連同條件一起寫。本站沒有實測，所以「最高快 40%」「最精準」這類說法都寫成「Apple 表示」「NVIDIA 稱」或「Google 自己的說法」，並帶上對照機型、測試月份與「最高」這類限定詞，也會寫明它是實測、廠商自己的推估，還是轉述第三方的結果。同一件事在兩份官方文件裡數字不一樣時，兩個都列出來，不替廠商選一個。"},
        {"question": "這些新聞跟台灣讀者有什麼關係？", "answer": "各篇都會寫出台灣的狀況，寫不出來的就寫明官方沒有提。例如 Apple 的新機有台灣售價與台灣的預訂、供貨日，高血壓通知功能依台灣版新聞稿的註腳不會一開始就在台灣推出；Pixel Drop 的通知詐騙警示與 Audible 試用，台灣都不在官方名單上；Apple 的歐盟 App 商業條款與《網路韌性法》管的是歐盟市場；Project Zenith 的兩篇微軟公告都沒有提到台灣。讀者不能從外國的發表推論台灣已經買得到或已經適用。"},
        {"question": "文章會持續更新嗎？", "answer": "每一篇都是以查核日為準的新聞解析，不是即時追蹤。價格、上市時程、功能的適用地區與官方頁面本身都可能改變，有幾篇引用的就是會持續更新的官方頁面，所以每一篇都寫了怎麼回官方頁面查現況。這份索引會在系列新增文章時更新。"},
    ]},
    {"type": "callout", "tone": "info", "title": "先看查核日，再看是誰說的", "text": "這份索引與各篇文章寫的都是查核日當天讀到的狀態：售價與上市日可能調整，預覽版可能改版，法規的適用日與官方常見問答也會更新。引用之前，請回到文章列出的官方來源確認現況，並先分清楚那句話是已經適用的規定、已經發表的產品、預告，還是廠商自己的推估。本站沒有實測，也不提供購買或升級建議。"},
]
sources = []
for heading, slugs in GROUPS:
    blocks.append(h(heading))
    for slug in slugs:
        doc = packs[slug]["locales"]["zh-TW"]
        blocks.append({"type": "link", "text": doc["title"], "url": f"https://mokaair.com/zh-TW/life/{slug}"})
        sources.append(dict(doc["sources"][0]))

document = {
    "title": "2026 年科技新聞總整理：硬體、平台、電信與法規的重點",
    "description": "整理本站 2026 年的科技新聞解析，分成硬體、平台、運算基礎設施、台灣政策與歐盟法規五組：iPhone Duo 與九月新機、M6 與 M5 Ultra、Project Zenith、Pixel Drop、NVIDIA 三則公告、6G 頻譜研討會、臺馬海纜、主權 AI 語料庫、《網路韌性法》通報義務與 Apple 歐盟 App 條款。不做購買建議，廠商宣稱一律歸因，每篇都附官方來源與查核日。",
    "hero": {"src": f"/guides/{SLUG}/hero.jpg", "alt": "原創插圖：左邊四個方格各放一個物件——晶片、螢幕、發出電波的基地台、鎖頭——代表硬體、平台、電信與資安法規四類新聞，線條匯向右邊一張列著四個項目的清單", "width": 1600, "height": 900, "credit": CREDIT},
    "blocks": blocks,
    "sources": sources,
}

path = CONTENT / f"{SLUG}.json"
old = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
locales = dict(old.get("locales", {}))
locales["zh-TW"] = document
order = ["zh-TW", "en", "ja", "ko", "zh-CN"]
pack = {
    "slug": SLUG, "kind": "life", "destination_id": None, "topics": ["tech", "tech-news"],
    "valid_until": None, "featured": False, "display_order": 299,
    "locales": {name: locales[name] for name in order if name in locales},
}
if any(set(doc) == {"title"} for doc in pack["locales"].values()):
    pack = {"slug": SLUG, "_stub": "其他語系還只有標題（給各篇譯文的 link 比對用），譯文併入前不得提交。", **{k: v for k, v in pack.items() if k != "slug"}}
path.write_bytes((json.dumps(pack, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))

record_path = RESEARCH / f"{SLUG}.json"
record = json.loads(record_path.read_text(encoding="utf-8")) if record_path.is_file() else {}
record.update({
    "slug": SLUG,
    "title": document["title"],
    "event_date": "2026",
    "checked_on": CHECKED,
    "status": "editor-authored-index",
    "sources": sources,
    "verified_facts": ["每一句都只重述十三篇已經過兩輪獨立查核的文章裡寫過、且該篇 sources[] 撐得住的事實；索引不引入新的事實。"],
    "unverified_or_excluded": ["各篇排除的數字與說法（例如沒有一手來源的規格、廠商沒有公布的價格與時程），索引同樣不寫。", "不寫篇數：讀者看得到的地方不寫會成長的數字（站主 2026-09-16 的規則）。"],
    "editorial_brief": "依主題分組的閱讀索引；開頭先教讀者分辨說法的種類（已適用或開賣／已發表有日期／預告與預覽版／研討與廠商推估），不宣稱涵蓋所有科技新聞，也不是即時追蹤；不做購買建議。",
    "hero_label": "硬體、平台、電信、法規",
    "diagram": {"title": "讀科技新聞，先分四種說法", "caption": DIAGRAM_CAPTION, "nodes": [
        ["已適用或開賣", "看適用日、對象與地區"],
        ["已發表有日期", "看日期屬於哪個地區"],
        ["預告與預覽版", "看有沒有確切日期"],
        ["研討與推估", "看誰說的、條件是什麼"],
    ]},
})
record_path.write_bytes((json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))

text = "".join(b["text"] for b in blocks if b["type"] == "paragraph")
print("title", len(document["title"]), "description", len(document["description"]), "paragraph chars", len(text), "sources", len(sources))
