"""Write the zh-TW original of the crypto index pack and its research record.

usage: build_index.py            -- (re)writes locales["zh-TW"] of crypto-news-2026-index.json
Link texts and cited sources are read from the eleven article packs, so a title that changed
in fact-checking cannot go stale here. Locales other than zh-TW that the file already holds
(title-only placeholders, or merged translations) are left as they are.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "apps/api/app/guides/content"
RESEARCH = ROOT / "docs/crypto-news-2026/research"
SLUG = "crypto-news-2026-index"
CHECKED = "2026-09-17"

GROUPS = [
    ("台灣", ["crypto-news-taiwan-vasp-act-20260630"]),
    ("美國：GENIUS Act 的規則草案", [
        "crypto-news-genius-act-occ-20260302",
        "crypto-news-stablecoin-aml-20260410",
        "crypto-news-fdic-genius-act-20260410",
        "crypto-news-ncua-genius-act-20260518",
    ]),
    ("美國：證券法的解釋與提案", [
        "crypto-news-sec-crypto-interpretation-20260323",
        "crypto-news-sec-regulation-crypto-assets-20260821",
    ]),
    ("歐盟", [
        "crypto-news-mica-transition-ends-20260701",
        "crypto-news-eba-psd2-mica-20260212",
    ]),
    ("日本", [
        "crypto-news-jfsa-working-group-20260216",
        "crypto-news-jfsa-cybersecurity-20260723",
    ]),
]

CREDIT = {"author": "Mokaair", "license": "© Mokaair", "source_url": None}
DIAGRAM_CAPTION = "讀法規新聞的第一步是分清楚文件的身分：已經生效、已經公布但還沒施行、還在徵詢意見的草案，或是建議與意見書；四種的法律效果不同。"


def p(text):
    return {"type": "paragraph", "text": text}


def h(text):
    return {"type": "heading", "level": 2, "text": text}


packs = {}
for _, slugs in GROUPS:
    for slug in slugs:
        packs[slug] = json.loads((CONTENT / f"{slug}.json").read_text(encoding="utf-8"))

blocks = [
    p("這份索引整理本站 2026 年的加密貨幣新聞解析，這一批的事件日落在 2026 年 2 月到 8 月之間。內容依台灣、美國、歐盟、日本四個地區編排，每一則都回到主管機關的公告、法規原文或聯邦公報，再連到完整的解析文章。"),
    p("本索引於 2026 年 9 月 17 日查核。本站沒有實測任何平台、錢包或代幣，也不提供投資、法律或稅務意見。這個系列只寫法規、技術與產業運作，不寫幣價、漲跌幅、市值與交易量，也不寫買賣時機。本站不比較、也不推薦任何資產、交易所、錢包與發行方；主管機關文件裡引用的市值、交易量這類行情數字，同樣不寫。各篇的查核日寫在各篇開頭，文件的狀態以各該主管機關當期公告為準。"),
    {"type": "summary", "items": [
        "這份索引依台灣、美國、歐盟、日本四個地區，整理本站 2026 年的加密貨幣新聞解析，每一篇都附官方來源與查核日。",
        "讀這類新聞的第一步是分清楚文件的身分：已經生效、已經公布但還沒施行、還在徵詢意見的草案，或是建議、意見書與研究報告。",
        "以各篇的查核日為準，台灣《虛擬資產服務法》已公布但施行日期未定，美國依 GENIUS Act 提出的幾份規則都還是草案，歐盟 MiCA 第 143 條第 3 項的過渡期已在 2026 年 7 月 1 日屆滿。",
    ]},
    h("先看文件的身分：生效、公布未施行、草案、建議"),
    p("同樣被叫作「新規」，法律效果差很多。這一批的焦點文件裡，自己印了生效日的是美國證券交易委員會（SEC）與商品期貨交易委員會（CFTC）聯名的解釋令：2026 年 3 月 23 日刊登於聯邦公報，DATES 欄寫的生效日就是這一天。它是主管機關對既有法律的解釋，文件自己寫明不創設新的法律義務。"),
    p("已經公布、還沒施行的是台灣的《虛擬資產服務法》：2026 年 6 月 30 日三讀、7 月 22 日制定公布，施行日期由行政院另定。再來是草案：美國的通貨監理局（OCC）、聯邦存款保險公司（FDIC）、全國信用合作社管理局（NCUA），以及金融犯罪執法網路（FinCEN）與外國資產管制辦公室（OFAC），都依 GENIUS Act 提出了規則草案；SEC 的 Regulation Crypto Assets 也是提案，意見截止日是 2026 年 10 月 20 日。"),
    p("還有一類是建議、意見書與研究報告：歐洲銀行管理局（EBA）的意見書是寫給各國主管機關的建議；日本金融審議會工作小組的報告是建議，金融廳公布的資安研究報告則是委外研究，金融廳明寫它不代表該廳見解。另外有一種新聞不是新文件，而是法律早就寫好的期限到了：歐盟加密資產市場規則（Markets in Crypto-Assets Regulation，MiCA）的過渡期在 2026 年 7 月 1 日屆滿。看到「某國已經規定」的標題，先回到原文件看它的類別與日期，是這個系列每一篇都在做的事。"),
    {"type": "table", "header": ["文件身分", "這一批裡的例子", "先看什麼"], "rows": [
        ["已生效的解釋", "美國 SEC 與 CFTC 聯名解釋令", "生效日與文件自己寫的範圍"],
        ["已公布、未施行", "台灣《虛擬資產服務法》", "施行日期公告了沒有"],
        ["徵詢意見的草案", "美國 OCC、FDIC、NCUA、FinCEN 與 OFAC、SEC 的提案", "意見截止日、有沒有定案規則"],
        ["建議、意見與研究", "EBA 意見書、日本金融審議會的報告、金融廳公布的委外研究與取組方針", "誰寫的、寫給誰、有沒有拘束力"],
    ], "caption": "2026 年 9 月 17 日查核；各文件的狀態以各篇文章的查核日為準，之後可能改變。"},
    {"type": "image", "src": f"/guides/{SLUG}/diagram-1.svg", "alt": "四格圖解：已經生效、公布未施行、徵詢中的草案、建議與意見書，各自先看什麼", "width": 1600, "height": 900, "caption": DIAGRAM_CAPTION, "credit": CREDIT},
    h("台灣：法律已公布，施行日期未定"),
    p("《虛擬資產服務法》把在我國境內為他人提供虛擬資產服務的業者分成七種，要依種類分別取得金管會的許可及許可證照；在我國發行穩定幣要向金管會申請許可，金管會許可前應會商中央銀行同意，發行人並須維持十足的準備資產。"),
    p("最容易被忽略的是時間。第 56 條把施行日期交給行政院決定，而第 55 條給已完成洗錢防制登記的業者、以及已依規定提供服務的金融機構的 12 個月申請期與 21 個月取得許可證照的期限，都從本法施行後起算；施行日期還沒有公告，這兩段期間就還沒有開始。在那之前，台灣現行的是洗錢防制登記制，金管會證券期貨局的專頁列有業者名單與更新日期。"),
    h("美國：一部穩定幣法律，幾個機關各自提出草案"),
    p("GENIUS Act（Guiding and Establishing National Innovation for U.S. Stablecoins Act，Public Law 119-27）的公法原文末尾記著 2025 年 7 月 18 日核准。它把支付型穩定幣的許可與監理分給幾個聯邦機關與各州，所以同一部法律會看到好幾份草案。OCC 的草案在 2026 年 3 月 2 日刊登，處理它所管轄機構的發行核准、準備資產與贖回。FinCEN 與 OFAC 的聯名草案在 4 月 10 日刊登，要把發行人納入銀行保密法，並要求制裁法遵計畫。"),
    p("FDIC 的草案同樣在 4 月 10 日刊登，處理受它監理的存款機構及其獲准發行的子公司，還有受它監理的相關保管業者；存款保險那一段的射程更寬，及於所有維持這類存款的受保存款機構。它提議把作為準備金的存款依法人存款規則保給發行人，不以穿透方式保給持有人。NCUA 的補充草案在 5 月 18 日刊登，寫明信用合作社不得自行發行、只能透過子公司。"),
    p("FDIC 與 NCUA 的草案都引 GENIUS Act 明文寫到，支付型穩定幣不受美國政府保證，也不受聯邦存款保險或股金保險保障，作相反陳述即屬違法；OCC 的草案則把這一點寫成對發行人的表示禁令。這四份都還是草案，定案規則可能不同；這四篇文章都寫了怎麼用案號、法規識別號或聯邦公報引註回到官方頁面查現況。"),
    p("證券法這一邊，解釋令與提案規則性質不同。2026 年 3 月的聯名解釋令把加密資產分成五類，說明哪些類別本身不是證券、投資契約什麼時候開始與結束；那是法律上的歸類，不是投資評價。2026 年 8 月的 Regulation Crypto Assets 則是 SEC 的提案規則，打算建立募集豁免與一個投資契約安全港，文件上沒有生效日。"),
    h("歐盟：過渡期屆滿，與支付規則的銜接"),
    p("MiCA 第 143 條第 3 項讓舊制底下已在營運的加密資產服務商先繼續提供服務，最遲到 2026 年 7 月 1 日；各會員國可以縮短這段緩衝，長度並不一致。歐洲證券及市場管理局（ESMA）的官方問答寫明，過渡期結束時仍未取得許可的機構必須停止提供加密資產服務，直到依 MiCA 取得許可為止，申請中並不延長期限；ESMA 並請客戶到名冊上確認自己的服務商是否已取得許可。"),
    p("EBA 的意見書處理另一個重疊：電子貨幣代幣同時落在支付服務指令（PSD2）與 MiCA 之下。EBA 先前以不行動函給了一段過渡期，依意見書所載到 2026 年 3 月 2 日結束（不行動函的執行摘要另印 3 月 1 日）；2026 年 2 月 12 日的意見書說明過渡期結束之後，建議各國主管機關依業者的授權與申請狀態分別處理。它的用字是建議，收件對象是主管機關，不是對業者直接生效的規則。"),
    h("日本：建議報告、後續立法與資安"),
    p("金融審議會工作小組的報告，日文版日期是 2025 年 12 月 10 日，英文暫譯本在 2026 年 2 月 16 日公布，核心建議是把加密資產的法律依據從資金決済法移到金融商品取引法。報告本身是建議；金融廳的「国会提出法案等」頁則載明相關法案在 2026 年 4 月 10 日提出、7 月 15 日成立，而該篇以它所引的金融廳頁面查核時，未見加密資產相關條文的施行日。"),
    p("2026 年 7 月 23 日，金融廳在官網公布一份委外的資安研究報告，封面日期是 2026 年 6 月 30 日，金融廳明寫報告不代表該廳見解。報告指出，它分析的事件裡有一類並未竊取簽章金鑰本身，而是竄改了簽章之前的系統元件。金融廳自己在 2026 年 4 月 3 日訂定的取組方針則寫，面對這類間接攻擊，光靠冷錢包無法確保加密資產的安全保管，必須強化包含外包商在內的整條供應鏈的資安管理體制。研究報告與取組方針都沒有新增法定義務或罰則，但取組方針訂了有日期的期待，例如自 2026 事務年度起要求全部加密資產交換業者做資安自我評估。"),
    {"type": "faq", "items": [
        {"question": "這個系列為什麼不寫幣價與行情？", "answer": "這是本站財經內容的編輯界線：只講制度與方法，不推薦商品。幣價、漲跌幅、市值、交易量與買賣時機變動快，也容易被讀成投資建議，所以一律不寫；主管機關文件裡引用的市值、交易量這類行情數字同樣不寫。罰鍰金額、資本額門檻與期限這類法規數字則會寫，並附官方來源與查核日。"},
        {"question": "草案什麼時候會變成正式規定？", "answer": "要看主管機關之後是否發布定案規則，本系列只寫各篇查核日讀到的狀態，不預測時程。美國的提案規則會先徵詢公眾意見，定案的內容也可能與草案不同。美國那幾篇都列了該案的案號、法規識別號或聯邦公報引註；其他地區的文章則列了文件在主管機關網站上的文號與公告頁，並說明怎麼回到那一頁確認現況。"},
        {"question": "這些外國規定跟台灣讀者有什麼關係？", "answer": "這些外國文件管的是各該法域的業者與發行人；各篇查核時，都沒有在這些外國文件裡讀到針對台灣使用者的規定。對台灣讀者的用處有兩個：看到「某國已經規定」的標題時，知道要先問那是生效的規則、草案還是建議；使用境外服務時，知道保障的界線在哪裡，例如 FDIC 與 NCUA 的草案都引法律明文寫到，支付型穩定幣不受聯邦存款保險或股金保險保障。台灣自己的制度，請看《虛擬資產服務法》那一篇。"},
        {"question": "文章會持續更新嗎？", "answer": "每一篇都是以查核日為準的新聞解析，不是即時追蹤。文件的狀態之後可能改變，例如草案定案、施行日期公告或名冊更新，所以每一篇都寫了自己回官方頁面查現況的方法。這份索引會在系列新增文章時更新。"},
    ]},
    {"type": "callout", "tone": "info", "title": "先看查核日，再看文件的身分", "text": "這份索引與各篇文章寫的都是查核日當天讀到的狀態：草案可能定案，施行日期可能公告，名冊與清單也會更新。引用之前，請回到文章列出的官方來源確認現況，並先分清楚那份文件的身分。"},
    {"type": "callout", "tone": "info", "title": "這篇是資訊整理，不是投資建議", "text": f"本文說明的是法規、技術與產業運作，不推薦任何加密資產、交易所、錢包或發行方，也不是投資建議，不含價格、漲跌幅與買賣時機。監理規定、登記狀態、上線時程與服務條件依主管機關與業者當期公告為準，本文查核日為 {CHECKED}。加密資產價格波動大、可能全額損失，且部分服務不受存款保險或投資人保護制度保障；實際適用請以官方公告或合格專業人員的意見為準。"},
]
sources = []
for heading, slugs in GROUPS:
    blocks.append(h(heading))
    for slug in slugs:
        doc = packs[slug]["locales"]["zh-TW"]
        blocks.append({"type": "link", "text": doc["title"], "url": f"https://mokaair.com/zh-TW/life/{slug}"})
        sources.append(dict(doc["sources"][0]))

document = {
    "title": "2026 年加密貨幣新聞總整理：法規、技術與產業的重點",
    "description": "依台灣、美國、歐盟、日本四個地區，整理本站 2026 年的加密貨幣新聞解析：《虛擬資產服務法》、美國依 GENIUS Act 提出的各機關規則草案、SEC 與 CFTC 聯名的解釋令與 SEC 的提案規則、歐盟 MiCA 過渡期與支付規則的銜接、日本金融廳公布的報告。只談法規、技術與產業運作，不談價格，每篇都附官方來源與查核日。",
    "hero": {"src": f"/guides/{SLUG}/hero.jpg", "alt": "原創插圖：左邊四個方格各放一個物件——條文與虛線圓、銀行建築、帶緞帶的印章、鎖頭——代表四個地區的監理文件，線條匯向右邊一張列著四個項目的清單", "width": 1600, "height": 900, "credit": CREDIT},
    "blocks": blocks,
    "sources": sources,
}

path = CONTENT / f"{SLUG}.json"
old = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
locales = dict(old.get("locales", {}))
locales["zh-TW"] = document
order = ["zh-TW", "en", "ja", "ko", "zh-CN"]
pack = {
    "slug": SLUG, "kind": "life", "destination_id": None, "topics": ["finance", "crypto"],
    "valid_until": None, "featured": False, "display_order": 199,
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
    "verified_facts": ["每一句都只重述十一篇已獨立查核文章裡寫過、且該篇 sources[] 撐得住的事實；索引不引入新的事實。"],
    "unverified_or_excluded": ["各篇排除的行情數字、業者名稱與名冊計數，索引同樣不寫。", "不寫篇數：讀者看得到的地方不寫會成長的數字（站主 2026-09-16 的規則）。"],
    "editorial_brief": "依地區編排的閱讀索引；開頭先教讀者分辨文件身分（已生效／公布未施行／草案／建議與意見書），不宣稱涵蓋所有公告，也不是即時追蹤。",
    "hero_label": "四個地區，一條閱讀路線",
    "diagram": {"title": "讀法規新聞，先看文件身分", "caption": DIAGRAM_CAPTION, "nodes": [
        ["已經生效", "看生效日與適用範圍"],
        ["公布未施行", "看施行日期公告了沒"],
        ["徵詢中的草案", "看意見截止與定案"],
        ["建議與意見書", "看寫給誰、有無拘束力"],
    ]},
})
record_path.write_bytes((json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))

text = "".join(b["text"] for b in blocks if b["type"] == "paragraph")
print("title", len(document["title"]), "description", len(document["description"]), "paragraph chars", len(text), "sources", len(sources))
