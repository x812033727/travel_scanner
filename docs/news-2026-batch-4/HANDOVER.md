# 交接：新聞批次 4（2026-09-17 收工時的狀態）

這份文件給接手的人或模型。它記的是 **PR #544 的分支 `claude/brave-hopper-8ezxba` 上現在有什麼、
還缺什麼、怎麼接著做**。規格在 [`BRIEF.md`](BRIEF.md)、[`crypto.md`](crypto.md)、[`tech.md`](tech.md)、
[`ai.md`](ai.md)；工具的取捨在 [`PORT-NOTES.md`](PORT-NOTES.md)。

站主的指示是「幣圈和科技的先全部寫，AI 挑補漏那幾則」，並指定**先交幣圈這批驗收**。
所以這個 session 只做了幣圈（批次 4.1）。科技 13 篇與 AI 12 篇**還沒有任何文章**，
研究、獨立查核與逐篇修正清單都已在這個目錄裡。

收工的原因不是做完，是**帳號用量上限**：Opus 的子代理在 2026-09-17 下午連續被月用量與週用量上限切斷
（週上限 2026-09-19 07:00 台北時間重置），最後幾步由協調者自己在主對話裡收尾。

## 1. 幣圈十一篇加索引的現況

「查核」欄是獨立查核代理核對的主張數與改動處數；兩個數字的是做了第二輪。
五語指 zh-TW、en、ja、ko、zh-CN。

| 代號 | slug | 查核 | 語系 | 圖檔 | 狀態 |
| --- | --- | --- | --- | --- | --- |
| C1 | `crypto-news-taiwan-vasp-act-20260630` | 87 條／改 7 | 五語 | 五語 | 待逐語審稿 |
| C2 | `crypto-news-mica-transition-ends-20260701` | 86／18 | 五語 | 五語 | 待逐語審稿 |
| C3 | `crypto-news-sec-crypto-interpretation-20260323` | 107／9 | 五語 | 五語 | 待逐語審稿 |
| C4 | `crypto-news-sec-regulation-crypto-assets-20260821` | 108／20，第二輪再改 9 件 | 五語 | 五語 | 待逐語審稿；zh-CN 見 2.4 |
| C5 | `crypto-news-eba-psd2-mica-20260212` | 96／9 | 五語 | 五語 | 待逐語審稿 |
| C6 | `crypto-news-genius-act-occ-20260302` | 98／12 | 五語 | 五語 | 待逐語審稿 |
| C7 | `crypto-news-stablecoin-aml-20260410` | 96／13，第二輪 41／12 | **zh-TW、en、zh-CN** | 三語 | **缺 ja、ko**（見 2.1） |
| C8 | `crypto-news-fdic-genius-act-20260410` | 96／6 | 五語 | 五語 | 待逐語審稿 |
| C9 | `crypto-news-ncua-genius-act-20260518` | 92／13，第二輪 58／10 | 五語 | 五語 | 待逐語審稿 |
| C10 | `crypto-news-jfsa-working-group-20260216` | 111／10 | 五語 | 五語 | 待逐語審稿 |
| C11 | `crypto-news-jfsa-cybersecurity-20260723` | 104／12 | 五語 | 五語 | 待逐語審稿 |
| 索引 | `crypto-news-2026-index` | 約 160 條／14 條發現已全數套用 | **zh-TW、en** | 二語 | **缺 ja、ko、zh-CN**（見 2.2） |

每篇的查核報告在 [`factcheck-draft/`](factcheck-draft)，研究紀錄（含 `factcheck` 欄位、每條事實的逐字引文）
在 [`../crypto-news-2026/research/`](../crypto-news-2026/research)。
十一篇的 zh-TW 都過了 `check_article.py`；**沒有任何一篇被匯入或發布**。

## 2. 還沒做完的事（依順序）

### 2.1 C7 的 ja 與 ko

zh-TW 經兩輪查核定稿；en 與 zh-CN 已併入。ja、ko 還沒翻。研究紀錄的 `translation_status` 寫了同一件事。

```bash
cd apps/api
# 做法一：照 agents/TRANSLATE.md 派翻譯代理。
# 做法二：協調者自己翻——l10n.py 把 zh-TW 的字串依序編號，譯文照同樣順序寫成 JSON 陣列再組回去，
#         區塊、表格形狀、摘要句數與 FAQ 題數由程式保證一致（zh-CN 就是這樣做的）。
uv run python ../../docs/news-2026-batch-4/l10n.py dump  crypto-news-stablecoin-aml-20260410
uv run python ../../docs/news-2026-batch-4/l10n.py build crypto-news-stablecoin-aml-20260410 ja strings-ja.json
uv run python ../../docs/news-2026-batch-4/merge_locale.py crypto-news-stablecoin-aml-20260410 ja crypto-news-stablecoin-aml-20260410.ja.json
```

合併後在研究紀錄補 `translations.ja`／`translations.ko`（hero_label、圖解 title、caption 逐字等於該語言
image 區塊的 caption、四組 nodes），再跑 2.5 的出圖。用語對齊同批已完成的 FDIC、OCC 兩篇
（決済用ステーブルコイン／지급결제용 스테이블코인、金融犯罪取締ネットワーク（FinCEN）、外国資産管理室（OFAC）、
금융범죄단속네트워크(FinCEN)、해외자산통제국(OFAC)）。

### 2.2 索引的 ja、ko、zh-CN

**三個語言的標題已經定案，不可更動**——其他十一篇的第一個結尾連結已經逐字引用它們。
標題存在研究紀錄 `docs/crypto-news-2026/research/crypto-news-2026-index.json` 的 `planned_titles`：

- ja `2026年 暗号資産ニュース総まとめ：法規制・技術・業界の重要動向`
- ko `2026년 가상자산 뉴스 총정리: 규제·기술·산업의 핵심`
- zh-CN `2026 年加密货币新闻总整理：法规、技术与产业的重点`

索引的 zh-TW 是產生器 [`build_crypto_index.py`](build_crypto_index.py) 寫的（連結標題與 `sources[]` 直接讀十一篇內容包），
**要改繁中正文就改產生器再重跑，不要直接改內容包**。索引不在 `check_article.py` 的清單裡；
翻完用 `merge_locale.py` 併入，再以 `ArticlePack.model_validate` 與 `lint_document` 檢查
（只允許 `raw_internal_url` 與 `text_length` 兩種 warning）。讀者看得到的地方不寫篇數（站主規則）。

**在索引補齊之前，十一篇的 `check_article.py --full` 都會多出三條
「ja／ko／zh-CN link text must be the title of crypto-news-2026-index」**——那是索引缺語系造成的，
不是文章壞了；索引一補齊就回到 `OK`（補齊前 C1–C6、C8–C11 都是 `--full --assets OK`）。CI 不受影響。

### 2.3 逐語審稿（整個階段還沒開始，這是剩下最重要的一關）

規格 [`agents/REVIEW.md`](agents/REVIEW.md)：每語言一位審稿代理，**只交修正清單**，
由 `apply_corrections.py` 統一套用（避免多個代理同時寫同一個 JSON）。翻譯階段已經知道要看的點：

- **ko**：C3 把 crypto system／network 譯成「가상 시스템／가상 네트워크」，存疑；
  `암호자산`（歐盟、日本法語境）與 `가상자산`（台灣法、美國法語境、索引標題）會同頁出現，確認是否照語境區分即可；
  IDI 有「부보예금취급기관」與「예금취급기관」兩種寫法。
- **ja／ko**：share insurance 在 FDIC 篇是「持分保険／지분보험」，在 OCC、NCUA 兩篇是「出資金保険／출자금보험」，要統一。
- **ja**：C1 同時用「仮想資産」（台灣那部法與它定義的七種業者）與「暗号資産」（一般語境）——譯者是刻意的
  （寫成「暗号資産交換業者」會撞上日本資金決済法自己的法定類別），請確認；C10 表格的刑名用了「拘禁刑」、
  工作小組名稱是從英文名回譯的，來源頁沒有日文名。
- **en**：C1 標題 `Third Reading for Taiwan's Virtual Asset Service Act: …` 與主圖標語 `56 articles, start unset`
  （articles 指條文）可以更自然；C10 表格把來源的 `1 years` 寫成 `1 year`。
- **zh-CN**：見 2.4。
- 審稿建議改介面名、機關名時，先查該語言的官方頁再決定（批次 3 的教訓：12 筆不採用的建議多數是
  把只對繁中讀者有用的註記塞回其他語言）。

### 2.4 兩個語系是在翻譯代理被切斷的情況下併入的

- **C4 的 zh-CN**：譯者在「最後一輪大陸用語微調」途中被切斷，併入的是微調前的版本（結構與事實無虞，用語待審）。
  研究紀錄的 `translations` 四語由協調者補寫。
- **C7 的 en**：譯者修完 en 並重新合併後、開始 ja 之前被切斷；en 沒有經過它自己的 `--full` 自檢
  （協調者讀過全文，限定詞與歸因都在）。zh-CN 是協調者用 `l10n.py` 翻的。
- **索引的 en**：譯者併入 en 後被切斷，沒有回報；協調者只做了 schema 與 lint 檢查，沒有逐句對讀。

### 2.5 出圖、manifest 與 contact sheet

```bash
cd apps/api
export CHROMIUM_BIN=<Chromium 或 Edge 的路徑>          # Windows 上必須設；容器裡 /opt/pw-browsers 會自動找到
uv run python ../../docs/news-2026-batch-4/build_assets.py crypto --slug=<slug>   # 局部
uv run python ../../docs/news-2026-batch-4/build_assets.py crypto                 # 全部補齊後跑一次
```

主圖是 `build_assets.py` 裡逐篇的原創構圖（`_DRAWINGS`，十一篇加索引都有），`hero.alt` 已改寫成實際畫面。
**全垂直的 `manifest.json` 與 contact sheet 還沒產生**（`--slug` 局部執行不寫這兩樣）。
協調者逐張看過的是：C1–C3、C5、C6、C8、C10、C11 八篇的 en／ja／ko 圖解與 en 主圖，
以及索引 en、C7 en 圖解與 zh-CN 主圖；**zh-TW／zh-CN 的圖解、ja／ko 的主圖、C4 與 C9 的圖沒有人看過**，
全部補齊後請看一次 contact sheet（`BRIEF.md`：代理看不到自己畫的圖）。

### 2.6 relink 與 autolink

`BRIEF.md` 要求內容定稿後才跑，所以還沒跑：

```bash
cd apps/api
uv run python -m app.guides.pack_cli relink   --prefix crypto-news- --dry-run   # 先看 diff，再 --apply
uv run python -m app.guides.pack_cli autolink --prefix crypto-news- --dry-run
```

跑完結尾的 `link` 會變成帶 `article` inline 的 `rich_paragraph`（`check_article.py` 與 `align_links.py` 兩種形狀都認得）。
標題若再改，用 [`align_links.py`](align_links.py) `--apply` 把所有結尾連結的文字對齊到目標文章的現行標題。

### 2.7 出刊當天要重查的活資料

- C1：金管會證期局名單（10／1／18 家，頁面標 2026-09-03 更新）；全國法規資料庫的「最後生效日期：未定」。
- C2：ESMA 各國過渡期對照表（PDF 內部修改時間 2026-05-19，文章逐列清點 27 列）。
- C7：`sources[3]` 是聯邦公報依案號的官方查詢（2026-09-17 回 1 筆、Proposed Rule）。
- C8：FDIC 刊登清單頁上 RIN 3064–AG19 只有 2026-04-10 那一列（該頁用 en dash）。
- C3：Federal Register API 的 `corrections` 仍為空。
- C5：EBA 不行動函 PDF 是活檔（`Last-Modified` 2026-02-17）。
- C10：金融廳「国会提出法案等」頁第 221 回國會那一區；01.pdf 的 bytes。
- 美國五份草案若出現定案規則或展延公告，文中「未見／草案」的句子要一起改。

### 2.8 匯入與發布（不在這個 PR 的範圍，但接手的人一定會碰到）

- 一律 `guides-import --slug …`，先跑不帶 slug 的 `--dry-run` 看有沒有別人的積壓。
- **sitemap 上限**：`SITEMAP_LIMIT` 是 1,000 列，2026-09-15 線上已約 980 列；這批是 12 個內容包 × 5 語系 = 60 列，
  超過時最舊的頁面會**無聲地**從 sitemap 消失。先做完 `tasks/open/2026-09-14-sitemap-split-before-1000-rows` 再發。
- 幣圈是 YMYL：站主逐篇看過「有沒有變相推薦標的、風險講得夠不夠」是 4.1 那張票 Definition of done 的一部分，機器擋不住。

### 2.9 科技 13 篇與 AI 12 篇

沒有開始。照幣圈同一條線跑：撰稿 → 獨立查核（改超過十處或動到骨幹就第二輪）→ 協調者讀全文、改 `hero.alt`
→ 翻譯 → 逐語審稿 → 出圖 → 索引 → relink／autolink → 驗證。`check_article.py` 的 `RELATED`、
`build_assets.py` 的 `_DRAWINGS` 與 `verticals.py` 的 `order_base`（科技還是 `None`）要先填。
`agents/` 裡的四份規格換掉工作區與補充規格的檔名就能用。

## 3. 這一輪定下來、接手的人不要再翻案的決定

- **`checked_on`**：`corrections-crypto.md` 寫「一律填 2026-09-16」，`BRIEF.md` 寫「實際查證當天」。
  依「BRIEF > 修正清單」：C2–C11 的撰稿代理當天重抓每一條 `sources[]` 並讀到 body，所以是 **2026-09-17**；
  C1 維持 09-16（那是它真正的查核日）。
- **美國聯邦規則的事件日＝聯邦公報刊登日**（slug 尾碼與 `news_date`），作成／通過／署名日另外明寫在文章裡。
  `corrections-crypto.md` 對 FDIC 傾向 04-07，站主圈選的 slug 清單是 04-10；照 slug 清單。
- **生效日：照來源印的寫。** FDIC 的聯邦公報文件自己印了 `January 18, 2027, or 120 days after … if earlier`，
  照印並歸因；NCUA 全文沒印日期，只寫公式。不可自己換算。
- **來源自己的矛盾照印不訂正**：FinCEN/OFAC 草案的 1022.220 對 1020.220、EBA 兩份文件的日期、
  OCC 的 PART 15 標題、EBA PDF 的 `andthe`。`corrections-crypto.md` 有兩處要求訂正，與 `BRIEF.md` 型態 7 衝突，照 BRIEF。
- **否定句必須指得到 `sources[]`**：「未見定案規則」這類句子，要嘛把能承載它的官方頁放進 `sources[]`
  （C7 用聯邦公報依案號的官方查詢、C8 用 FDIC 的刊登清單頁），要嘛限縮成現有來源撐得住的說法（C9、C6）。
- **C1 的第二個連結改指 MiCA 那篇**：原本指向的〈電子支付與電子票證〉只有 zh-TW，四個譯文沒有標題可連。
- **C11 不點名個案**：報告的十個個案（交易所、協議）整串拿掉；報告自己聲明個案不代表責任歸屬，一串名字會被讀成黑名單。
- **用語**：日本法的「暗号資産」在繁中一律譯「加密資產」（首次出現附日文），「虛擬資產」留給台灣的法律；
  OCC 的中文名統一為「通貨監理局」、NCUA 為「全國信用合作社管理局」。
- **標題、摘要、圖上不放來源沒印的清點數字**（「27 國四種緩衝」「四層申報」都拿掉了）；
  來源自己編號的（條文的 (1)–(10)、`five key elements`）可以寫。
- **主管機關文件裡的行情數字一律不寫**（市場規模、市值、交易量、轉引 CoinMarketCap／TRM 的數字）；
  開戶數、帳戶分布、罰鍰、資本額門檻這類不是行情，可以寫。

## 4. 這一輪學到的（寫給下一個協調者）

- **第二輪查核不是形式。** NCUA 第二輪推翻的，正是第一輪自己新寫進去、沒人查過的那一句；
  SEC 提案第二輪抓到三個「第一輪報告寫對、套進內容包時沒套滿」的限定詞。
- **翻譯是第三道查核。** 三篇是譯者回頭抓到的：FDIC 的 subpart B 在中文有歧義（英譯照字面變成「提供準備金的業者」，
  條文是「以提供保管服務為業者」）；OCC 摘要的「單日…一成」比條文的「單一 24 小時期間…10%」鬆；
  日本審議會那篇的摘要與圖解寫了正文沒有的兩項建議。請譯者回報「我懷疑原稿有錯的地方」，並真的去查。
- **`check_article.py` 看不到的兩件事**：摘要裡的中文數字（「一成」躲過數字比對）；
  摘要的事實有沒有出現在正文（只比對阿拉伯數字）。十一篇的「摘要 ⊆ 正文」是協調者人工對過的。
- **撰稿者系統性地壓掉但書來湊字數**（每篇都卡在 2,9xx／3,000）。查核規格要明寫「字數爆了就精簡敘述，不可刪但書」，
  第二輪專門回頭掃 `except`／`unless`／`or`／`may`／`in its discretion`。
- **環境**：`pypdf` 在系統 Python，不在 `apps/api/.venv`；多個代理同時跑不要用 `uv run`（搶鎖），直接用 venv 的 python；
  Windows 上 `CHROMIUM_BIN` 要指到 Playwright 的 headless shell 或 Edge；聯邦公報正規頁回 `Request Access` 擋阻頁，
  全文用 `federalregister.gov/documents/full_text/text/…txt` 或 govinfo 的 PDF；`sec.gov` 對 curl 回 403。
- **用量**：一篇走完撰稿、查核、翻譯約 90–130 萬 subagent tokens（第二輪另加 25–30 萬）。
  十個代理同時跑會在幾小時內撞到用量上限；被切斷的代理用 `SendMessage` 對原 id 續跑，比重開便宜
  （C9 的譯者續跑 13 次工具呼叫就收完）。要求譯者「每完成一個語言就先合併存檔」，被切斷時才不會白做。
- **代理遇到「Output blocked by content filtering policy」**（兩次，都在大段逐字貼來源原文的時候）：
  檔案通常已經寫好，重派或續跑時要求它用「位置＋前後十來個字」描述，不要整段貼。
