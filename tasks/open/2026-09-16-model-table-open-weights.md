---
id: 2026-09-16-model-table-open-weights
title: 模型總表補回開放權重表：十二家的參數、上下文與權重授權
status: in-progress
priority: P2
area: docs
owner: claude-opus-5
claimed_at: 2026-09-16T13:36:31Z
created_at: 2026-09-16T13:36:28Z
completed_at:
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

- [ ] 文章多一張開放權重表，欄位 `廠商｜模型｜參數規模｜上下文視窗｜權重授權`（五欄，跟另外三張一致）。
- [ ] 授權欄寫**正式名稱**（Apache 2.0、MIT、Llama 4 Community License 等），不寫「開源」這種含糊詞；
      自訂社群授權要跟 OSI 標準授權分得出來，排序把標準授權放前面，因為那是讀者真正要判斷的事。
- [ ] 每一列的授權與現行版本都經過對抗式驗證（兩個獨立懷疑者，一個攻授權名稱、一個攻版本現行性），
      兩票都沒推翻才進表；被推翻的寫進 `notes.md` 說明為什麼沒進。
- [ ] 原本那個「開放權重與授權，這篇沒有做成表」的 h2 拿掉或改寫，不要留下跟新表矛盾的段落。
- [ ] 仍然查不到的廠商，正文照實說查不到，不猜。
- [ ] `sources` 不超過 20 筆（目前 18 筆，只剩 2 個名額——這是這張卡最緊的限制）。

## Steps

- [ ] 用 workflow 一家一個 agent 查：Meta、阿里巴巴、DeepSeek、Mistral、Z.AI、MiniMax、
      Moonshot、Google、OpenAI、NVIDIA、Ai2、Microsoft。只讀廠商自己的官網、GitHub org 與 HF org。
- [ ] 每筆結果兩個懷疑者驗證，預設 refuted=true。
- [ ] 改 `build_pack.py` 加表、重跑、ingest、lint、pytest。
- [ ] 渲染圖如果因為新增章節而需要改，一併重畫並用眼睛看過。

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
