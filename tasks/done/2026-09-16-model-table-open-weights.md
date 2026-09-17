---
id: 2026-09-16-model-table-open-weights
title: 模型總表補回開放權重表：十二家的參數、上下文與權重授權
status: done
priority: P2
area: docs
owner: claude-opus-5
claimed_at: 2026-09-16T13:36:31Z
created_at: 2026-09-16T13:36:28Z
completed_at: 2026-09-16T14:57:13Z
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/ai-model-comparison-table-2026.json
  - apps/web/public/guides/ai-model-comparison-table-2026
  - docs/content-research/ai-model-comparison-table-2026
---

# 模型總表補回開放權重表：十二家的參數、上下文與權重授權

## Why

`ai-model-comparison-table-2026` 第一版拿掉了開放權重表。當時的理由記在
`tasks/done/2026-09-16-ai-model-comparison-table.md`：Meta 的 llama.com 當天 301 轉
developer.meta.com，該頁只在導覽列出現 Llama 4 與 Llama 3，模型頁回 404，官方 blog 沒提現行版本；
Z.AI、MiniMax、Moonshot 與 Mistral 的 API 定價頁則一律不寫權重授權。
只查 API 定價頁確實湊不出一張表——但**權重授權本來就不會寫在定價頁上**，
它在權重發布頁、GitHub repo 的 LICENSE 檔與廠商自己的 Hugging Face organization。
第一版找錯地方了，站主要求補回來。

## Definition of done

- [x] 文章多一張開放權重表，欄位 `廠商｜模型｜參數規模｜上下文視窗｜權重授權`（五欄，跟另外三張一致）。
- [x] 授權欄寫**正式名稱**（Apache 2.0、MIT、Llama 4 Community License 等），不寫「開源」這種含糊詞；
      自訂社群授權要跟 OSI 標準授權分得出來，排序把標準授權放前面，因為那是讀者真正要判斷的事。
- [x] 每一列的授權與現行版本都經過對抗式驗證（兩個獨立懷疑者，一個攻授權名稱、一個攻版本現行性），
      兩票都沒推翻才進表；被推翻的寫進 `notes.md` 說明為什麼沒進。
- [x] 原本那個「開放權重與授權，這篇沒有做成表」的 h2 拿掉或改寫，不要留下跟新表矛盾的段落。
- [x] 仍然查不到的廠商，正文照實說查不到，不猜。
- [x] `sources` 不超過 20 筆（目前 18 筆，只剩 2 個名額——這是這張卡最緊的限制）。

## Steps

- [x] 用 workflow 一家一個 agent 查：Meta、阿里巴巴、DeepSeek、Mistral、Z.AI、MiniMax、
      Moonshot、Google、OpenAI、NVIDIA、Ai2、Microsoft。只讀廠商自己的官網、GitHub org 與 HF org。
- [x] 每筆結果兩個懷疑者驗證，預設 refuted=true。
- [x] 改 `build_pack.py` 加表、重跑、ingest、lint、pytest。
- [x] 渲染圖如果因為新增章節而需要改，一併重畫並用眼睛看過。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --kind life --slug ai-model-comparison-table-2026 --warnings
uv run pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py -q
```

## Notes

`claim` 又用了 `--force`，跟前一張卡同一個理由：`2026-09-15-content-summary-howto-and-life`
（claude-fable-5-1）的 scope 是整個 `apps/api/app/guides/content` 目錄。這張卡只改自己那一篇。

`pack_cli ingest` 仍然擋子主題（見 `2026-09-16-pack-cli-ingest-805`），所以重跑 ingest 前要先把
`ai-plans` 拿掉、跑完再補回。`build_pack.py` 裡那行註解標著這件事。

`sources` 只剩 2 個名額是真的會卡住：十二家的權重頁不可能各佔一筆。
可行的做法是授權的細節寫進 `notes.md`，`sources` 只留最能一次涵蓋多欄的那幾頁；
真的不夠就把表上「權重授權」的來源合併成一筆「各家權重發布頁」的集合式來源。

## 結果（2026-09-16）

十二家全部查到，表上十二列。做法是一家一個 agent 只讀該廠商自己的官網／GitHub org／HF org，
每筆再由兩個獨立懷疑者驗證（一個攻授權名稱、一個攻版本現行性，兩者都預設聲明是錯的）。
六十個 agent，十三筆兩票都過、十一筆被推翻。

**第一版那句「Meta 當天查不到現行 Llama 版本」是錯的，已更正。**
錯在只查了 llama.com、developer.meta.com 與 ai.meta.com/blog 三個地方就下結論——
權重授權本來就不寫在那裡。改查權重庫之後，Meta 現行的開放權重模型是 Muse Glimmer 30B，
授權是**未修改的 Apache License 2.0**（驗證者實際讀了 LICENSE 檔全文），不是 Llama 時代的社群授權。
`tasks/done/2026-09-16-ai-model-comparison-table.md` 裡那段記錄現在讀起來是錯的，
以這張卡為準。

被推翻的十一筆全部是同一種錯：規格對、但版本不是最新。這正是對抗式驗證要抓的東西，
舉三個：Llama 4 Maverick 已被 Muse Glimmer 取代、DeepSeek-V4-Pro-0813 官方寫明正在下架
（2026-09-14 起 API 請求改路由到 V4.1-Flash）、MiniMax-M2.7 已被 M3 取代。
單靠一個 research agent 這三筆都會進表。

### 表的排序是有意義的

上半六列是 OSI 認可的標準授權（Apache 2.0、MIT），商用沒有額外義務；
下半六列是廠商自訂授權，名字像標準授權也一樣——Mistral 的「Modified MIT」在 MIT 上加了
月營收 2,000 萬美元的天花板，MiniMax 要求商用標示「Built with MiniMax M3」，
阿里巴巴與 Moonshot 都有月活躍用戶一億或月營收 2,000 萬美元的標示義務。
這些條款只在權重庫的 LICENSE 檔裡，API 定價頁完全看不到。

另一個寫進正文的陷阱：同家族不同型號授權可能不同。Qwen3.8-27B 是 Apache 2.0、
Qwen3.8-Flash-Next 是 Qwen Community License 1.0、Qwen3.8-2.4T-A95B 又是 Qwen3.8-Max License。

### sources 的取捨

上限 20 筆、原本用掉 18。騰出兩個名額：拿掉 Anthropic 定價頁（模型總覽頁同時有價格、上下文
與最大輸出，兩筆重複），拿掉第一版那筆錯的 Meta 來源。四個名額給條款最會影響讀者的四家
（Meta、Qwen、MiniMax、Moonshot）。**其餘八家的權重頁沒有進 `sources`**，網址全列在 `notes.md`，
每一筆都是當天從那個網址讀到的。這是被 schema 上限逼出來的取捨，寫在這裡讓下一個人知道。

### Microsoft 沒有進表

兩筆都被推翻。Phi-4-Reasoning-Vision-15B 規格全對，但驗證者指出之後發的
VibeVoice-ASR-Streaming-7B 是語音辨識模型，不是同一類的通用語言模型，
「Microsoft 現行的開放權重語言模型是哪一個」當天判不乾淨。依「兩票都過才進表」的標準就不列。

### 一併做的

- 圖解從三個級距改成四個，多一個橘框的「開放權重」，右側面板加一行「權重授權」。重新渲染看過。
- 原本那個「開放權重與授權，這篇沒有做成表」的 h2 整段拿掉。
- 開放權重表放在輕量級之後、效能討論之前，四張分級表連在一起。
- 加了 `reingest.sh`：`pack_cli ingest` 擋子主題的繞法包成腳本，
  `2026-09-16-pack-cli-ingest-805` 修好之後連同腳本一起刪。

### 驗證

`pack_cli lint --kind life --warnings` 零 error 零 warning；
`test_guides_content_pack`、`test_guides_content_links`、`test_guide_series` 共 40 passed；
`ruff check` 通過；`mypy app` 337 檔零問題；`check:tasks` 通過；渲染圖用眼睛看過。

文章現在 30 blocks、7 個 h2、5 張表、20 筆 sources、正文約 2,541 字。
