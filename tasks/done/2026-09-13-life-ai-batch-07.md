---
id: 2026-09-13-life-ai-batch-07
title: 生活分享 AI 系列批次 07：本機與開源模型（20 篇）
status: done
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-14T17:48:51Z
created_at: 2026-09-13T11:56:00Z
completed_at: 2026-09-14T19:28:22Z
branch:
depends_on:
  - 2026-09-13-life-ai-series-tooling
  - 2026-09-13-life-ai-series-catalogue
  - 2026-09-13-life-ai-batch-01
scope:
  - apps/api/app/guides/content/local-llm-why-and-when.json
  - apps/api/app/guides/content/ollama-getting-started.json
  - apps/api/app/guides/content/lm-studio-getting-started.json
  - apps/api/app/guides/content/local-llm-hardware-requirements.json
  - apps/api/app/guides/content/llama-models-explained.json
  - apps/api/app/guides/content/gguf-quantization-explained.json
  - apps/api/app/guides/content/open-webui-chat-interface.json
  - apps/api/app/guides/content/ollama-with-code-editors.json
  - apps/api/app/guides/content/local-rag-chat-with-your-documents.json
  - apps/api/app/guides/content/gpt-oss-openai-open-weights.json
  - apps/api/app/guides/content/gemma-google-open-models.json
  - apps/api/app/guides/content/qwen-local-deployment.json
  - apps/api/app/guides/content/whisper-local-transcription.json
  - apps/api/app/guides/content/stable-diffusion-comfyui-setup.json
  - apps/api/app/guides/content/local-ai-on-mac-mini.json
  - apps/api/app/guides/content/local-ai-gpu-buying-guide.json
  - apps/api/app/guides/content/huggingface-guide.json
  - apps/api/app/guides/content/self-host-ai-on-vps.json
  - apps/api/app/guides/content/local-vs-cloud-ai-cost.json
  - apps/api/app/guides/content/openrouter-multi-model-api.json
  - apps/web/public/guides/local-llm-why-and-when
  - apps/web/public/guides/ollama-getting-started
  - apps/web/public/guides/lm-studio-getting-started
  - apps/web/public/guides/local-llm-hardware-requirements
  - apps/web/public/guides/llama-models-explained
  - apps/web/public/guides/gguf-quantization-explained
  - apps/web/public/guides/open-webui-chat-interface
  - apps/web/public/guides/ollama-with-code-editors
  - apps/web/public/guides/local-rag-chat-with-your-documents
  - apps/web/public/guides/gpt-oss-openai-open-weights
  - apps/web/public/guides/gemma-google-open-models
  - apps/web/public/guides/qwen-local-deployment
  - apps/web/public/guides/whisper-local-transcription
  - apps/web/public/guides/stable-diffusion-comfyui-setup
  - apps/web/public/guides/local-ai-on-mac-mini
  - apps/web/public/guides/local-ai-gpu-buying-guide
  - apps/web/public/guides/huggingface-guide
  - apps/web/public/guides/self-host-ai-on-vps
  - apps/web/public/guides/local-vs-cloud-ai-cost
  - apps/web/public/guides/openrouter-multi-model-api
---

# 生活分享 AI 系列批次 07：本機與開源模型（20 篇）

## Why

`docs/life-ai-series.md` 的批次 07。生活分享專區今天是空的，站主要至少 200 篇 AI 工具的介紹與教學，
分十一批產出；這張票是其中一批，scope 精確到這二十篇的內容包與圖片目錄，和其他批次可以同時進行。

開工前先讀 `docs/life-ai-series.md` 的「經驗記錄」與批次 01 票的 Outcome。

## Definition of done

- [x] 二十個 `apps/api/app/guides/content/<slug>.json`（zh-TW），每篇：hero（自繪插圖渲染的 `hero.jpg` 或 Commons 照片）、
      至少一張自繪 `diagram-1.svg`、≥3 個 h2、一表、一 callout、sources 每筆有 `checked_on`、至少一個站內 `link`；
      合作連結只在總表標了的篇、只放文章真的用到的段落。
- [x] 沒有任何產品 logo、字標、圖示或介面截圖；照片只來自 Commons 的 CC0／PD／CC BY／CC BY-SA，授權由 Commons API 讀回。
- [x] 方案、價格、模型名、額度都在寫作當天查官網；查不到的寫「以官網為準」。
- [x] `guides-pack lint --kind life` 沒有 error；每張 hero 與圖解渲染成 PNG 後人工看過；`test_guides_content_pack.py` 全綠。

## Steps

這二十篇（slug · 標題 · topics · 圖 · 合作 · 易變）：

1. `local-llm-why-and-when` · 為什麼要在自己電腦跑 AI：隱私、離線與成本 · ai, software · 圖：插
2. `ollama-getting-started` · Ollama 入門：Windows、Mac 安裝與第一個模型 · ai, tutorial · 圖：插 · 易變
3. `lm-studio-getting-started` · LM Studio 入門：圖形介面跑本機模型 · ai, tutorial · 圖：插 · 易變
4. `local-llm-hardware-requirements` · 跑本機模型要什麼電腦：記憶體、顯示記憶體與 Apple Silicon · ai, gadgets · 圖：照
5. `llama-models-explained` · Llama 模型家族：授權與版本 · ai · 圖：插 · 易變
6. `gguf-quantization-explained` · 量化是什麼：GGUF、Q4、Q8 怎麼選 · ai, tutorial · 圖：插
7. `open-webui-chat-interface` · Open WebUI：給本機模型一個像 ChatGPT 的介面 · ai, tutorial · 圖：插
8. `ollama-with-code-editors` · 把本機模型接到編輯器：Continue、Cursor 與 Ollama · ai, tutorial · 圖：插 · 易變
9. `local-rag-chat-with-your-documents` · 本機 RAG：跟自己的文件聊天 · ai, tutorial · 圖：插
10. `gpt-oss-openai-open-weights` · OpenAI 的開放權重模型 gpt-oss：怎麼跑、和 ChatGPT 差在哪 · ai · 圖：插 · 易變
11. `gemma-google-open-models` · Gemma：Google 的開源模型怎麼用 · ai · 圖：插 · 易變
12. `qwen-local-deployment` · 本機跑 Qwen：中文表現與設定 · ai, tutorial · 圖：插 · 易變
13. `whisper-local-transcription` · 用 Whisper 本機轉錄逐字稿：會議與訪談 · ai, tutorial · 圖：照
14. `stable-diffusion-comfyui-setup` · 本機跑 Stable Diffusion 與 Flux：ComfyUI 入門 · ai, tutorial · 圖：插 · 易變
15. `local-ai-on-mac-mini` · Mac mini 當家用 AI 伺服器 · ai, gadgets · 圖：照 · 易變
16. `local-ai-gpu-buying-guide` · 為 AI 選顯示卡：顯示記憶體優先與預算配置 · gadgets, ai · 圖：照 · 易變
17. `huggingface-guide` · Hugging Face 入門：找模型、看授權、下載 · ai, tutorial · 圖：插
18. `self-host-ai-on-vps` · 在 VPS 上自架 AI 服務：Ollama＋Open WebUI · tutorial, software · 圖：插 · 合作：H
19. `local-vs-cloud-ai-cost` · 本機 vs 雲端 AI 成本試算 · ai, software · 圖：插 · 易變
20. `openrouter-multi-model-api` · OpenRouter：一把金鑰用遍各家模型 · ai, tutorial · 圖：插 · 易變

- [x] 認領後從總表抄出指派，一篇一個撰稿代理、每波最多七個，代理照 `docs/life-ai-series-brief.md` 產出工作區。
- [x] 每篇落地就 `guides-pack ingest`；被拒的退回修。
- [x] `guides-pack lint --render-dir` 逐張看圖；跑測試；更新這張票；commit。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --render-dir /tmp/renders --catalogue ../../docs/life-ai-series.md
cd apps/api && uv run pytest tests/test_guides_content_pack.py tests/test_guide_partner_links.py -q
npm run check:tasks
```

部署後在主機：`python -m app.cli guides-import --actor-email <admin> --dry-run`，再 `--publish`。

## Notes

- 前三批旅遊文章的經驗：兩篇一個代理會在半小時左右撞到額度，一篇一個代理、先寫檔再寫報告最穩。

## Outcome (2026-09-14)

- 二十篇全部完成並匯入：`apps/api/app/guides/content/<slug>.json` 與 `apps/web/public/guides/<slug>/{hero.jpg,hero.svg,diagram-1.svg}`；hero 全部自繪（總表標「照」的四篇也自繪，避免產品外形、logo 與介面），每張 hero 與圖解都渲染成 PNG 逐張看過。
- 檢查：`pack_cli lint --kind life --catalogue ../../docs/life-ai-series.md` 零 error（僅既有的 `pack_not_in_catalogue` 與 sitemap 預算警告，sitemap 已到 926/1,000 列）；`pytest tests/test_guides_content_pack.py tests/test_guide_partner_links.py`：63 passed、28 skipped；`npm run check:tasks` 通過。
- 來源：每篇 11–20 筆，全部官方或一手（docs.ollama.com／ollama.com、lmstudio.ai、huggingface.co 模型卡與 API、GitHub LICENSE 原文、ai.google.dev、developer.meta.com、docs.openwebui.com、docs.continue.dev、cursor.com、docs.comfy.org、black-forest-labs、stability.ai、openrouter.ai、apple.com/tw、support.apple.com、nvidia.com、amd.com、台電電價表），`checked_on` 2026-09-14；審稿時逐篇用 curl、Hugging Face API、Wayback 原始快照與 JSON-LD 複核關鍵數字（審稿記錄在工作區 review-log.md）。
- 沒有合作連結（`self-host-ai-on-vps` 的 H 標記只是允許，repo 內無聯盟網址）。
- 授權逐版本核對後與總表指派不同的事實（正文照官網寫）：Gemma 4 全系列 Apache 2.0，Gemma 3／3n 仍是 Gemma Terms 且 HF 受管制；Meta 沒有比 Llama 4 更新的 Llama，主力改為 Muse（Muse Spark 只有 API，Muse Glimmer 30B 開放權重 Apache 2.0），歐盟限制只在 Llama 3.2 多模態；FLUX.2 [klein] 4B Apache 2.0 但 9B 與 FLUX.2 [dev] 非商用，SDXL Turbo 的 HF 標籤仍寫非商用但 LICENSE 檔已是 Community License；Qwen3.5／3.6／3.8-27B 皆 Apache 2.0，只有 Qwen3.8-Flash-Next 是 Qwen Community License 1.0；gpt-oss 另有 safeguard 兩款（2025-09-18）；Whisper HF 標 apache-2.0、GitHub 為 MIT。
- 產品現況與指派不同：LM Studio 條款只給「個人與／或內部商業用途」授權、下載頁主打 Bionic、另有 llmster；Hugging Face CLI 為 `hf`，會跑運算的 Space 需付費方案；Cursor 沒有自訂端點、自備金鑰只對聊天模型有效且請求仍經 Cursor 伺服器；Open WebUI v0.6.6 起有 50 人／30 天的品牌標示條款、Python 3.13 不支援；Qwen3.5 不再支援 `/nothink` 軟開關；OpenRouter 手續費分 5.5%／8%，免費模型 20 rpm、50 或 1,000 次／天；Claude Max 官網只寫「From $100」；Mac mini 當天預訂中（9 月 22 日開售）、M6 16GB 為 153GB/s、M5 Pro 另有 48GB 選項。
- 官方文件內部不一致時擇一並註明出處：Ollama 預設上下文 4096（FAQ）vs 依顯示記憶體 4k／32k／256k（context-length）、AMD ROCm v7（gpu）vs 5.7／6.2（FAQ）；Open WebUI README 9 種 vs 文件 13 種向量資料庫；Whisper turbo 809M（README）vs 798M（model-card）；FLUX.2 klein 4B 顯示記憶體三處不同。
- 取得資料的做法：openai.com 與 help.openai.com 對本環境 403，改讀 Wayback `id_` 原始快照（回應是 gzip，要 `--compressed`）；amd.com 要 `--http1.1` 加瀏覽器 UA，規格在內嵌 JSON；developer.apple.com 文件走 `tutorials/data/documentation/...json`；apple.com/tw 商品頁售價在 JSON-LD；台電電價表用 PDF。
- 標題與總表：三篇在撰稿後調整了標題（Mac mini、成本試算、Whisper），`docs/life-ai-series.md` 批次 07 列已同步。
- 代理統計：二十個 Opus 撰稿代理，每篇 16–31 分鐘、20–34 萬 token，本批沒有撞到額度。
- 合併後：部署，然後在主機跑 `python -m app.cli guides-import --actor-email <admin> --dry-run`（應為二十篇 `create`），再 `--publish`。
