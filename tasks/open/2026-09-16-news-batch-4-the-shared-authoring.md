---
id: 2026-09-16-news-batch-4-the-shared-authoring
title: News batch 4: the shared authoring brief for the crypto, tech and AI news verticals
status: in-progress
priority: P1
area: docs
owner: claude-opus-5
claimed_at: 2026-09-16T11:39:36Z
created_at: 2026-09-16T11:39:25Z
completed_at:
branch: claude/brave-hopper-8ezxba
depends_on: []
scope:
  - docs/news-2026-batch-4
---

# News batch 4: the shared authoring brief for the crypto, tech and AI news verticals

## Why

批次 4 要寫 34–45 篇、五語，分三個垂直。前三批的經驗是**撰稿指令一篇只被讀一次**，
規則會漂（批次 03 送出 13 個連到不存在文章的連結）。這批又比前三批多兩件事：

- 幣圈有法遵界線，寫錯的代價比 AI 新聞高。
- SEO 標準變了：`summary` 與 `faq` 區塊是這批要全面帶的，845 篇 life 只有 5 篇有 summary。

所以規格要先定死，內容才開工。

## Definition of done

- [x] `docs/news-2026-batch-4/BRIEF.md`：三個垂直共同的查證、格式、篇幅、翻譯規則。
- [x] `crypto.md`：只寫法規／技術／產業的界線、免責 callout 樣板與五語標記、一手來源白名單。
- [x] `tech.md`：非 AI 的範圍界線與一手來源。
- [x] `ai.md`：補漏範圍、索引改標題的三個陷阱、既有篇目表。
- [x] 既有篇目表由內容包直接產生，不是手抄。

## Steps

- [x] 以 `docs/ai-news-2026-09-mid/BRIEF.md` 為底本，標出「批次 4 新增」的部分。
- [x] 驗證幣圈一手來源真的連得到，並實際查成一則候選當範例。
- [x] 量出索引改標題的波及範圍，把實測數字寫進 `ai.md`。
- [x] 幣圈候選清單起頭：5 則已回一手來源驗過，可直接開稿（`candidates-crypto.md`）。
- [x] 科技與 AI 的候選清單改寫：科技 3 則已驗、AI 1 則已驗（9/15 缺口），
      另有 14 則已由官方 feed 確認日期、待讀原文（`candidates-tech-and-ai.md`）。
- [x] 官方 feed 對照表寫進 `BRIEF.md` 的查證章節與兩份候選清單。
- [x] 幣圈 11 則、科技 11 則已驗，**兩個垂直的重要新聞都到量**；AI 2 則已驗＋13 則已確認日期。
- [ ] 各垂直還缺 4–6 則「次要新聞」（科技已有第一則：Pixel Drop）。
      仍未掃過：Anthropic（無 feed）、Meta AI 產品線、DeepSeek、Qwen、Samsung（被擋）、台積電（403）、NCC。

## How to verify

規格本身沒有可執行的測試。可驗的是裡面的事實：

- `ai.md` 寫「30 個內容包、142 份語系文件」帶著指向索引的 `article` inline。
  重數的方法：走每個內容包每個語系的 `blocks`，數 `type == "article"` 且
  `slug == "ai-news-2026-january-september-index"` 的節點。**走 JSON 結構，不要用正規表示式。**
- `crypto.md` 的五語免責標記必須與 `pack_ingest.FINANCE_DISCLAIMER_MARKERS` 逐字相同。
- `ai.md` 的篇目表要能由 `apps/api/app/guides/content/ai-news-*.json` 重新產生。

## Notes

**幣圈的可行性已經驗過，不是假設。** 金管會、全國法規資料庫、MAS、日本 FSA、
ESMA、FCA、EUR-Lex、Federal Register API 都連得到；`sec.gov` 與 `openai.com` 實測 403，
BRIEF 的 fallback（官方 RSS、同一官站其他頁、各國 newsroom）涵蓋得了。

實際查成一則可用的候選並寫進 `crypto.md`：2026-06-30 立法院三讀通過《虛擬資產服務法》，
金管會新聞稿與法規內容頁都是一手來源，七種服務商、穩定幣須經央行與金管會許可、
12／21 個月過渡期都是新聞稿原文。

**查證過程本身示範了這批最大的風險。** 為了找法條，查證者一度**自行猜測**
全國法規資料庫的 `pcode`，抓到一個不存在的頁面。這件事寫進了 BRIEF 的查證規則：
猜識別碼、猜網址、猜條號都算捏造，即使猜對。先搜尋拿到真實網址，再抓那一頁。

**`ai.md` 的既有篇目表是程式產生的**，不是手抄——手抄一份 38 列的清單放進撰稿指令，
本身就是下一個漂移來源。

**免責標記的五語設計**與 `pack_ingest.FINANCE_DISCLAIMER_MARKERS` 一一對應，
兩邊要一起改。`lint_all` 逐語系檢查且不知道自己在看哪一語，所以任一標記命中即可。

**還沒做的：** 三個垂直的工作區（`docs/crypto-news-2026/`、`docs/tech-news-2026/`、
`docs/ai-news-2026-09-late/`）與其中的 `check_article.py`／`build_assets.py` 等工具，
留給各自的批次票。`check_article.py` 從批次 3 複製時要注意：它的
`["callout","link","link"]` 與 `["paragraph","paragraph"]` 斷言早於 relink／autolink，
直接複製會在正確的文章上失敗。

## 第二輪：科技與 AI 候選（claude-opus-5, 2026-09-16）

**最有用的發現是官方 feed。** `openai.com` 的網頁對 `curl` 與 WebFetch 都回 403，
但 `https://openai.com/news/rss.xml` 回 200，裡面 1,193 筆帶 `pubDate` 的項目、
2026 年就有 407 筆。這是 `BRIEF.md` 本來就寫的 fallback，但用來做候選清單特別好：
**日期是官方給的，不必從版面猜，也不必猜網址。**

實測可用：OpenAI、Google（`blog.google/rss/`）、Apple Newsroom（**Atom 格式**）、
Apple Developer、Windows。**Anthropic 兩個常見位址都 404，沒有 feed**，要抓網頁。
台灣 NCC 擋在安全驗證後面，要換管道。沒有 feed 的主管機關找結構化管道：
Federal Register 的公開 API 就是 `sec.gov` 被 403 擋掉時的官方刊登管道。

**查證結果：**

- **AI 的 9/15 缺口填掉了**：Google 在 2026-09-15 發布 Gemini 3.8 Live 與
  3.8 Live Extended Thinking，官方頁載明 97 種語言、開放範圍與方案限制，
  但**沒說地區**，要照實寫「官方未說明」。
- **OpenAI 在 9/15–9/16 沒有任何發布**（feed 最後一筆是 9/14）。整合站說的
  「Microsoft MAI」與「Altman 談 IPO」兩則都查不到合格的一手來源：
  前者官方貼文是 JS 算繪、拿不到日期，後者是 Fortune 專訪的轉述。
- **科技驗成三則**：Apple iPhone Duo（9/9，規格／售價／上市日都抄了原文）、
  9/9 發表會其餘硬體、歐盟 CRA 通報義務上路（9/11，24／72／14 小時天數都抄了原文）。
- **CRA 有一處要注意**：整合站寫「主要義務自 2027-12-11 起適用」，
  但執委會的頁面把 2027-12-11 寫成**開源軟體管理者**的通報起始日。
  開稿要讀 EUR-Lex 原文釐清，不可照抄。
- **AI 補漏的空間比想像大**：站上覆蓋最薄的三個月（3 月 3 篇、5 月 2 篇、6 月 3 篇）
  正好是 OpenAI 官方發布最密的區間（38／56／55 筆）。清單列了 10 則，
  含 3/19 併購 Astral（`uv`／`ruff` 的開發商，本站 API 就在用）與
  6/8 的 S-1 送件（**角度必須是對使用者的意義，不可寫成投資題材**）。

**寫進檔案的每一個日期與標題都對著 live feed 重驗過一次**，
含兩則同日不同篇的 5/5 項目與帶非 ASCII 連字號的 `GPT‑Live‑1`。
## 第三輪：掃完剩下的來源（claude-opus-5, 2026-09-16）

**幣圈的重要新聞到量了：11 則已驗（C1–C11）。** 最大的一塊是美國 GENIUS Act 的落地——
Federal Register API 查到四個主管機關在 2026 年分別提出實施規則（OCC 3/02、
FinCEN/OFAC 4/10、FDIC 4/10、NCUA 5/18），每則都有評論截止日。純法規題材，
完全落在站主定的界線內，四則可以合成一篇也可以拆開。
另加日本 FSA 兩則（2/16 金融審議會工作小組報告、7/23 加密資產業者的資安議題），
是從 FSA 自己的英文新聞稿索引讀到的。

**修正了一個會讓撰稿代理照著寫錯的錯誤**：C3 不是 SEC 單獨發布。
Federal Register 的 `agencies` 欄位是 Commodity Futures Trading Commission 與
Securities and Exchange Commission **聯名**。已改標題與說明。

**科技與 AI 各補了一批**：NVIDIA 併購 Hugging Face（9/3，$12,930,300,000，
平台規模數字都抄了原文；官方沒說完成日與監理條件，標成未說明），
加上 Vera Rubin／CUDA-Q／MediaTek 三則已確認日期。
台灣數發部四則，其中**主權 AI 語料庫那條線（9/15 徵集 + 7/24 客語語料）
是這一輪最適合本站讀者的題目**——台灣自己的語料，跨 AI 與公共政策，沒有既有文章寫過。

**又抓到一次整合站與官方不符**：搜尋摘要說「台馬二號海纜 3/7 全斷、5/25 修復」，
數發部的新聞發布頁上沒有這一則，只有 6/23 的**臺馬四號**海纜建設。

### 抓 feed 的兩個陷阱（已寫進 BRIEF）

1. **HTTP 200 不代表拿到 feed。** `news.samsung.com/global/feed` 回 200，
   但 body 是 Akamai 的 `Access Denied`。只看狀態碼會把拒絕當資料。
2. **feed 可能是死的。** `usb.org/rss.xml` 回 200、格式正確、有 10 筆 item，
   但最新一筆是 **2018-07-31**。

判斷方式：數 `<item>`／`<entry>`，並看最新一筆的日期，兩者都合理才算拿到。

### 這一輪確認的來源狀態

可用：NVIDIA newsroom、Meta engineering、IETF blog（多半是組織事務，價值低）。
不可用：Samsung（200 但被擋）、USB-IF（死的）、DeepSeek（401）、TSMC（403）、
CISA（403）、**MAS（這個容器完全連不到，MAS 那則穩定幣諮詢因此只能標待驗）**。
**Anthropic 試了四個常見位址全部 404，確認沒有 feed**，只能抓網頁。

**Federal Register API 是美國各機關最可靠的管道**，一次涵蓋 SEC、CFTC、FinCEN、
OCC、FDIC、NCUA，而且帶 `comments_close_on`。

寫進檔案的每個日期、機關與評論截止日都對著 live 來源重驗過一次。
## 第四輪：科技補到量（claude-opus-5, 2026-09-16）

科技從 8 則補到 **11 則已驗，到量**。三個垂直的重要新聞候選現在都夠站主圈選。

**新來源：Apple Developer News feed**（`developer.apple.com/news/rss/news.rss`，
142 筆、2026 年 57 筆）。上一輪只記了「可用」，這一輪才真的拿它掃——
**它是 Apple 平台政策變動的一手來源，比 Newsroom 更早也更具體**，T5 就是從這裡找到的。

三則新增：

- **T5 Apple 調整歐盟 App 商業條款**（8/18 公告、10/1 生效）是這批最強的一則。
  Core Technology Fee 改為 **5% 的 Core Technology Commission**、
  取消 Initial Acquisition Fee 與 Store Services Fee、允許並行替代支付。
  **最關鍵的是：Apple 全文沒有提到 DMA。** 這是一則對監理的回應，但官方沒這樣說，
  所以文章不可以把 DMA 寫成原因——候選清單裡特別標了這一點，
  它正是「廠商說了什麼就寫什麼、沒說的不補」的典型案例。
- **T6 Windows Project Zenith**（9/4）：開發者機種的 Windows 11 預設組態，
  本機不限流量跑 30B+ 模型，機器條件 64 GB 統一記憶體、250 GB/s 頻寬。
  官方沒說價格、日期、地區與 OEM 名單。
- **T7 September Pixel Drop**（9/15）：份量偏輕，**標成建議放「次要新聞」那一格**，
  不要當重要新聞充數。次要新聞每垂直要 4–6 則，這是科技的第一則。

順帶確認了幾件省時間的事：**USB-IF 的 feed 是死的（停在 2018）、
IETF 的多半是組織事務**，兩個都從「還沒查的方向」拿掉了，不要再花時間。
Apple Developer feed 裡還有四則平台政策（中國商店調整、醫材 App、
新增 11 種語言、巴西博弈執照）日期已確認、內容未讀，留在清單裡。
其中中國商店那則要小心政治敏感度，且要確認官方到底說了什麼。

T5／T6／T7 的日期與標題都對著 live feed 重驗過一次。
