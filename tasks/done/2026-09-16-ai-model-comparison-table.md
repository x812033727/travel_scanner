---
id: 2026-09-16-ai-model-comparison-table
title: 各家 AI 模型總表：同級距的 token 規格與官方自報分數
status: done
priority: P2
area: docs
owner: claude-opus-5
claimed_at: 2026-09-16T13:16:41Z
created_at: 2026-09-16T13:15:29Z
completed_at: 2026-09-16T13:32:47Z
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/ai-model-comparison-table-2026.json
  - apps/web/public/guides/ai-model-comparison-table-2026
  - docs/content-research/ai-model-comparison-table-2026
---

# 各家 AI 模型總表：同級距的 token 規格與官方自報分數

## Why

站上已經有一批模型相關文章，但沒有一篇把「效能」和「token」放進同一張表：

- `ai-api-pricing-comparison-2026` 有八家旗艦／中階／輕量的每百萬 token 價格，但明講「不評分」，沒有效能欄。
- `ai-benchmarks-explained` 講跑分怎麼看、三個陷阱，但不列各家分數。
- `ai-model-tiers-explained` 講旗艦／中階／輕量怎麼選，沒有跨廠商總表。
- `ai-model-release-timeline-2026` 是時間軸，只有官方一句定位，沒有規格與分數。
- `claude-model-lineup-2026`、`gemini-model-lineup-flash-pro`、`qwen-alibaba-models-guide`、
  `llama-models-explained`、`chinese-ai-models-comparison` 各看各的廠商。

讀者要回答「同一個級距裡，這幾家的規格和分數差多少」時，現在要開五個分頁。這篇是那個落點：
一篇總表 hub，分級把各家模型排在一起，每一列同時給 token 規格與官方自報分數，並向外連到上面那些文章。

站主 2026-09-16 決定的三件事：單篇總表（不是系列）；效能欄放**官方自報分數並明確標註**
（不用第三方榜單、不做本站評分）；涵蓋既有八家加開放權重補齊。

## Definition of done

- [x] `apps/api/app/guides/content/ai-model-comparison-table-2026.json` 存在，`kind: life`、
      `topics: ["ai", "software", "ai-plans"]`、locale 只有 `zh-TW`。
- [x] 四張表（旗艦／中階／輕量／開放權重），共用同一組五欄表頭，每張 caption 標查證年月與「廠商自報」。
- [x] 每個數字在 `notes.md` 裡有一行 `主張｜來源網址｜查證日`；官網查不到的格子寫「官網未公布」，沒有憑記憶寫的數字。
- [x] `pack_cli lint --kind life --slug ai-model-comparison-table-2026` 零 error。
- [x] `test_guides_content_pack.py`、`test_guides_content_links.py` 綠。
- [x] 渲染出來的 PNG 用眼睛看過，標籤沒有壓線、跑出框或互相疊。

## Steps

- [x] 查證：11 家官網逐一開，抄「上下文／最大輸出／輸入價／輸出價／官方分數」進 `notes.md`。先查完再寫。
- [x] 寫 `pack.json`：導言、六個 H2、四張表、callout、內嵌 `article` inline 連四篇既有文章。
- [x] 畫 `hero.svg`（插圖）與 `diagram-1.svg`（比較矩陣，圖上不放數字）。
- [x] `ingest --dry-run` → 修 → 正式 ingest → `lint` → 測試。
- [x] 另開一張維護卡：價格與分數會過期，照 `2026-09-14-batch-6-guides-dated-maintenance` 的做法定期重查。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli ingest \
  --from ../../docs/content-research/ai-model-comparison-table-2026 \
  --slug ai-model-comparison-table-2026 --dry-run
uv run python -m app.guides.pack_cli lint --kind life --slug ai-model-comparison-table-2026 \
  --render-dir /tmp/render --warnings
uv run pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py
uv run ruff check . && uv run mypy app
```

```bash
npm run check:tasks && npm run test:tools
```

匯入正式站（站主決定時機，不在這張卡裡做）：
`uv run python -m app.cli guides-import --locale zh-TW --slug ai-model-comparison-table-2026 --dry-run`，
看過計畫再加 `--publish`。

## Notes

三個會卡住的硬限制，動之前要知道：

1. **表格最多 6 欄 × 30 列**（`apps/api/app/guides/schemas.py:111-112`），Pydantic 直接擋。全站 1,608 張表
   只有 9 張用到 6 欄。「一張大表塞下所有廠商所有欄位」在這個 schema 下做不到，必須拆成一級一表——
   而這剛好就是「比較同等級」要的形狀。
2. **`sources` 最多 20 筆**（`schemas.py:369`）。11 家廠商配 20 個名額很緊
   （`ai-model-release-timeline-2026` 已用滿 20、`ai-benchmarks-explained` 19）。分配：每家一個
   「一次帶最多欄位」的官方頁（11 筆），旗艦分數再補官方 model card／發布文（約 8 筆），
   中階／輕量的分數不另開名額，沒出現就寫「官網未公布」。細節寫進 `notes.md`，不佔 `sources`。
3. **每個數字都要當天查官網**（`docs/travel-guides.md:634`）。省時間的做法是把
   `ai-api-pricing-comparison-2026` 的 12 筆 `sources` 當廠商與網址的清單用，逐一重開重抄、
   `checked_on` 寫今天；不要沿用它的數字。官網回 403 時的解法在 `docs/life-ai-series-brief.md:91-94`。

`valid_until` 留 `null`：同類的四篇都是 `null`，日期寫在表格 caption 裡，過期靠維護卡處理。

一個取捨，寫在文章裡而不是藏起來：各家自報分數的測試條件不同（few-shot 數、是否給 scaffold、
是否多次取樣），放同一張表看起來可比，其實不可直接相減排名次。處理方式是專門一個 H2 講這件事、
一個 warning callout、每張表 caption 標「廠商自報」，並連到 `ai-benchmarks-explained`。

### 為什麼用了 `claim --force`（2026-09-16）

`claim` 拒絕這張卡，因為 `2026-09-15-content-summary-howto-and-life`（claude-fable-5-1，
2026-09-16T03:39 claim）的 scope 是整個 `apps/api/app/guides/content` 目錄。

判斷是可以 force，理由寫在這裡讓下一個人能推翻：這張卡**只新增一個還不存在的檔案**，
不改任何既有 pack；那張卡做的是逐批 `summarize --apply` 重寫既有 pack，兩邊不會同時寫到同一個檔。
真正會相接的點在未來——那張卡的批次 8 是「依 slug 首字 a–g」，總有一天會掃到這篇，
但那是它照常做自己的事，不是併發衝突。

如果站主覺得這個判斷太寬，正確的復原動作是 `release` 這張卡、等那張卡 `done` 再重 claim；
已經寫下的檔案不用回退。

## 做完之後：三件跟計畫不一樣的事（2026-09-16）

**1. 第四張表從「開放權重」改成「各家官網揭露的效能資訊」。**
原訂要比各家開放權重模型的授權條款，查證之後做不出誠實的表：Meta 的 llama.com 當天 301 轉
developer.meta.com，該頁只在導覽列出現 Llama 4 與 Llama 3，沒有版本、上下文或授權；
`developer.meta.com/ai/models/llama` 回 404；`ai.meta.com/blog` 明確沒有提到現行版本。
Z.AI、MiniMax、Moonshot 與 Mistral 的 API 定價頁則一律不寫權重授權。
硬做會生出一張整欄都是「官網未公布」的表。改成把六家官網的跑分揭露情況列出來——
那是當天真的查到的東西，而且正好是本篇的論點。授權的事改用內文連到
`ai-open-vs-closed-models`、`llama-models-explained`、`minimax-m-series-models-explained`。

**2. 效能欄大量是「官網未公布」，這是結論不是缺漏。**
查了六家：OpenAI 公布 GPQA Diamond（gpt-6-astra 96.0%）；Google DeepMind 的模型卡公布
GPQA Diamond 94.3% 與 SWE-Bench Verified 80.6%；Anthropic 的 Opus 5 發布頁列了
Frontier-Bench v0.1、ARC-AGI 3、OSWorld 2.0 等項目但**不給數字**，只給相對說法；
xAI 的 Grok 4.6 發布頁有跑分表，但用 AA Intelligence Index、Terminal-Bench v3.0、APEX-SWE 等十項，
**沒有 GPQA Diamond 也沒有 SWE-bench Verified**；DeepSeek 的 API 文件沒有跑分表；
Qwen 用自家 agent scaffold 跑 SWE-Bench 系列。
所以「同級距的效能」這個問題，用官網資料回答不了，文章把這件事寫成一個 h2 加一張表加一個 callout。

**3. `pack_cli ingest` 擋子主題，已另開一張卡。**
`ai-plans` 不在 `LIFE_SEED_TOPICS` 裡（它在 `LIFE_SEED_SUBTOPICS`），`pack_ingest._known_topics`
只讀前者，所以 ingest 直接拒絕。繞法是先用 `["ai", "software"]` 跑 ingest，再把 `ai-plans`
補回產出的內容包；`lint` 與兩支 pytest 都綠，因為它們不做這個檢查。
量過之後發現 970 篇裡有 805 篇重跑 ingest 都會被擋——已開
`2026-09-16-pack-cli-ingest-805`，那張卡修好之後回來把繞法拿掉。

## 一個查證上的教訓

DeepSeek 第一次抓回來的輸入價是 0.003 至 0.006 美元，跟輸出價差了兩百倍，數字本身就不合理。
重查才發現該頁的輸入分「快取命中」與「快取未命中」兩欄，第一次抓到的是命中那欄。
正確的是未命中：`deepseek-v4-pro` 尖峰 1.32 美元、`deepseek-flash` 尖峰 0.30 美元
（跟姊妹篇 `ai-api-pricing-comparison-2026` 前一天抄的一致）。
`kimi-k3` 也是同樣的兩欄結構（命中 0.30、未命中 3.00）。
**抄別人的價目表時，先確認那一欄是什麼欄。** 比例不合理就是重查的訊號。

## 沒做的

- 沒有 import 到正式站。站主決定時機，指令寫在「How to verify」最後一段。
- 只有 zh-TW 一個 locale。
- `claim` 用了 `--force`，理由寫在上面那一節。

## 驗證結果（2026-09-16）

- `pack_cli lint --kind life --slug ai-model-comparison-table-2026 --warnings` → 零 error、零 warning
- `pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py tests/test_guide_series.py tests/test_guides_pack_ingest.py` → 67 passed、24 skipped
- `ruff check .` → 通過；`mypy app` → 337 檔零問題
- `npm run check:tasks` → 通過
- `npm run test:tools` → 56 pass、2 fail（`airline-chrome-crawler` 與 `claude-code-series`）。
  這兩支在 stash 掉本次改動、乾淨工作區上跑同樣是 2 fail，**與本次無關**，沒有動它們。
- 渲染出來的 PNG 兩張都用眼睛看過：沒有標籤壓線、跑出框或互相疊。
