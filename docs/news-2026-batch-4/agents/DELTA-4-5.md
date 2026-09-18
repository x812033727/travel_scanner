# 批次 4.5（2026-09-16 起的新聞）：對三個垂直既有規格的差異

批次 4.5 沿用 4.1～4.3 的代理規格（`agents/`＝幣圈、`agents/tech/`＝科技、`agents/ai/`＝AI），只有下面幾件事不同。
指派訊息會告訴你 slug、垂直、第二個結尾連結的目標與 `display_order`；**這份文件的規則優先於各垂直規格裡與它衝突的句子**。

1. **沒有前期修正清單**：`corrections-<vertical>.md` 裡沒有你的 slug 的段落，規格裡要你「讀你的 slug 那一段」「`corrections_applied` 逐條回應」的地方一律跳過，
   `corrections_applied` 寫 `[]`。前期研究紀錄在 `docs/news-2026-batch-4/research/<slug>.json`（2026-09-18 由探索代理寫成），那一份仍然**對你有拘束力**：
   `must_not_write`、`not_said`、`overlaps_existing_article`、`sourcing_notes` 照 4.3 的規則處理；`sources` 也從那裡起手。
2. **`display_order` 照指派訊息**（AI 接 161 起、科技接 313 起、幣圈接 211 起，由 `check_article.py` 的 `RELATED` 順序決定），規格裡那張 4.x 的號碼表不適用。
3. **第一個結尾連結的文字用索引現行標題，逐字照抄**：
   - AI：`2026 年 AI 新聞總整理：1 月至 9 月的重點與生活應用` → `https://mokaair.com/zh-TW/life/ai-news-2026-january-september-index`
   - 科技：`2026 年科技新聞總整理：硬體、平台、電信與法規的重點` → `https://mokaair.com/zh-TW/life/tech-news-2026-index`
   - 幣圈：`2026 年加密貨幣新聞總整理：法規、技術與產業的重點` → `https://mokaair.com/zh-TW/life/crypto-news-2026-index`
   這次索引標題**不改**，所以 `check_article.py` 不應再留下「link text must be the title of <索引>」那條 FAIL；規格裡說那條允許的句子不適用。
4. **第二個結尾連結**指向指派訊息給的**既有已發布文章**（不是同批在寫的文章），text 打開那個內容包抄它 zh-TW 的 `title`，逐字相同；`check_article.py` 對它不應有 FAIL。
5. **`checked_on` 與正文的查核日**寫你實際重抓來源那一天（`date +%F`，台北時間），研究紀錄、內容包每條 source、第二段、表格 caption 一致；前期研究紀錄裡的 `2026-09-18` 只是探索代理的日期。
6. **事件日**：以前期研究紀錄的 `event_date` 與 `event_date_basis` 為準（已換算台北時間）；slug 的日期後綴、`news_date`、正文第一段的日期三者一致。
7. **工作區**：研究紀錄的最終版寫到各垂直的工作區（AI `docs/ai-news-2026-09-late/research/`、科技 `docs/tech-news-2026/research/`、幣圈 `docs/crypto-news-2026/research/`），不是 `docs/news-2026-batch-4/research/`。
8. **AI 第二輪查核規格**（`agents/ai/SECOND-ROUND.md`）第 1 項指向的第一輪規格檔，改讀 repo 內的 `docs/news-2026-batch-4/agents/ai/FACTCHECK.md`。
9. 網路請求：User-Agent 一律 `Mokaair-editorial`（主機拒絕時退回 curl 預設 UA，不可自訂別的），**任何請求的 UA、標頭、查詢字串、表單都不得帶入任何人的 email 或個人資料**；`openai.com/index/*` 的 403 是間歇性的，讀不到就換 `cdn.openai.com`／`developers.openai.com`／對方公司的稿，不要用 Wayback，也不要因此換掉一手來源。
