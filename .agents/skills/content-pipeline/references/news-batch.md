# 五語系新聞／系列批次：路由

新聞（AI、科技、幣圈）與系列教學的產線活在 `docs/news-2026-batch-4/`。這一頁只告訴你讀什麼、跑什麼、哪裡別再開分岔；規則全文不在這裡。

## 讀

1. `docs/news-2026-batch-4/BRIEF.md`：共同規格（查證規則、內容包格式、summary 與 faq、研究紀錄、圖像、流程、自檢、翻譯、36 篇查出來的 12 種錯誤型態）。
2. 垂直補充：`docs/news-2026-batch-4/ai.md`、`docs/news-2026-batch-4/tech.md`、`docs/news-2026-batch-4/crypto.md`（站主定的界線、免責 callout）。
3. 代理提示（實際發過的版本；`<ROOT>` 與 `<SCRATCH>` 發出前換成絕對路徑）：`docs/news-2026-batch-4/agents/WRITER.md`、`FACTCHECK.md`、`SECOND-ROUND.md`、`TRANSLATE.md`、`REVIEW.md`；AI 與科技的版本在 `docs/news-2026-batch-4/agents/ai/` 與 `docs/news-2026-batch-4/agents/tech/`；分組審稿的做法在 `docs/news-2026-batch-4/agents/ai/REVIEW-GROUPS.md`。
4. 差異檔優先於規格：`docs/news-2026-batch-4/agents/DELTA-4-5.md`（只寫某日期之後的新聞）、`docs/news-2026-batch-4/agents/DELTA-4-6.md`（zh-TW-only）。新批次寫自己的 `DELTA-4-N.md`，開頭一句「這份文件的規則優先於各垂直規格裡與它衝突的句子」。
5. 交接：`docs/news-2026-batch-4/HANDOVER.md`（先讀 §3「定下來、接手的人不要再翻案的決定」與 §4「學到的」）；工具移植紀錄 `docs/news-2026-batch-4/PORT-NOTES.md`。

## 順序

研究紀錄（專責研究代理，JSON schema 照批次 4.5）→ zh-TW 稿 → 查核第一輪 → 第二輪（換人：重查改過的，加隨機三分之一）→ `merge_locale.py` 併入翻譯 → 逐語審稿者只交修正 JSON、不直接改 → `apply_corrections.py`（照檔案順序，條目有順序性）→ `normalize_locales.py`、`sync_captions.py` → `build_assets.py` → `align_links.py` 或 `pack_cli relink` → `update_index.py <vertical>`（原地更新索引文章；**不要**重跑 `build_*_index.py`，會覆蓋 relink 與翻譯）→ `pack_cli lint --kind life`。

## 跑

都從 `<ROOT>/apps/api`，用 venv python，`PYTHONIOENCODING=utf-8`。

- 單篇自檢：`<PY> <ROOT>/docs/news-2026-batch-4/check_article.py <SLUG>`；五語系加 `--full`；出圖後加 `--assets`。規則從 `app.guides` 匯入、不重抄；`docs/news-2026-batch-4/verticals.py` 依 slug 前綴決定垂直，認 `MOKAAIR_ROOT`。
- 翻譯錯字：`docs/news-2026-batch-4/translation_checks.py`（ja 的 cp932 編不出的字、ko 在 KS X 1001 之外的音節、en 與 ko 裡源文沒有的 CJK 引文；sonnet 的錯字只有這個抓得到）；房規空格 `docs/news-2026-batch-4/space_cjk.py`。
- 審稿者讀的對照檔：`docs/news-2026-batch-4/review_dumps.py`（段落對齊的 zh-TW 與目標語；別給審稿者 pack JSON）。
- `review_dumps.py`、`normalize_locales.py`、`sync_captions.py` 以 slug 前綴掃檔，`ai-news-` 也會掃到第三批的 38 篇：一律在後面列出明確的 slug。
- `update_index.py` 的 COUNT 規則（只守 AI 索引）會擋「數字＋兩個字＋新聞」這種寫法，改寫成「一月至九月」之類。
- slug 裡的日期在撰稿時可能就是錯的（GPT-Live 是 7/8 不是 7/9）；改名要同時改 BRIEF、檢查腳本、索引腳本與票的 scope。
- NCC 網站改成 SPA，舊新聞稿網址都失效：先確認入口再派研究。

## 逐語審稿分組

一組負責一對垂直的一個語言；ja／ko 審稿用 opus，en／zh-CN 用 sonnet 就夠。整批共通的 ko 修正（主詞「공식은／공식이」、統一成 가상자산）由協調者以 `coordinator_edit` 一次套用，不塞進每篇的清單；敬語語體的問題交給同一個代理統一修。發下去的術語表本身也會錯（ko「직접 검증하지 않았고」應為「직접 시험해 보지 않았고」），要留推翻它的管道。

## zh-TW-only 批次

照 `docs/news-2026-batch-4/agents/DELTA-4-6.md`：locales 只有 zh-TW；研究紀錄沒有 translations；沒有翻譯與逐語審稿；`check_article.py` **不帶 `--full`**（帶了必然 FAIL，不帶也不會漏掉任何 zh-TW 的檢查）；`--assets` 只查 zh-TW 的圖；`update_index.py` 不動（zh-TW-only 的索引增補另有做法，見 HANDOVER §1d）。

## 別再開分岔

`build_assets.py`、`check_article.py`、`update_index.py`、`merge_locale.py` 在 `docs/ai-news-2026-09`、`docs/ai-news-2026-09-mid`、`docs/ai-news-2026-ytd`、`docs/news-2026-batch-4` 各有一份；`news-2026-batch-4` 最新，`verticals.py` 是去重的嘗試。新批次擴充它、參數化它，不要複製第五份。`docs/ai-workflow-series/check_article.py` 用路徑匯入 batch-4 的 helper，是對的做法。

## 補既有文章的語系

不是新聞批次的事。先看目標的語系數與長度：五語系文章走 TRANSLATE 加逐語審稿；成批補語系用 `tools/article-localization/README.md` 的產線（Codex CLI 驅動，只產翻譯稿，不匯入、不發布）。
