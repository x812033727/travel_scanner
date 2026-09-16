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
