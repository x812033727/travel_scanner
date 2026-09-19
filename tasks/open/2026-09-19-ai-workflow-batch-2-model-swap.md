---
id: 2026-09-19-ai-workflow-batch-2-model-swap
title: 教學系列「多模型 AI 工作流」批次 2：把別的模型接進 Claude Code 與 Codex（5 篇）
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-19T11:21:14Z
completed_at:
branch: claude/ai-teaching-news-expansion-wa6kur
depends_on: []
scope:
  - apps/api/app/guides/content/ai-workflow-claude-code-custom-model.json
  - apps/api/app/guides/content/ai-workflow-codex-model-providers.json
  - apps/api/app/guides/content/ai-workflow-glm-coding-plan.json
  - apps/api/app/guides/content/ai-workflow-ollama-coding-agent.json
  - apps/api/app/guides/content/ai-workflow-litellm-gateway.json
  - apps/api/app/guides/content/ai-workflow-tutorials.json
  - apps/api/app/guides/series_data/ai-workflow.json
  - docs/ai-workflow-series
  - apps/web/public/guides/ai-workflow-claude-code-custom-model
  - apps/web/public/guides/ai-workflow-codex-model-providers
  - apps/web/public/guides/ai-workflow-glm-coding-plan
  - apps/web/public/guides/ai-workflow-ollama-coding-agent
  - apps/web/public/guides/ai-workflow-litellm-gateway
  - apps/api/tests/test_guide_series.py
---

# 教學系列「多模型 AI 工作流」批次 2：把別的模型接進 Claude Code 與 Codex（5 篇）

## Why

站主 2026-09-19 要求「新增 AI 的更多相關教學，workflow 串接或是 GLM 本地端之類的 model
串接 codex、claude」。批次 1（#553，12 篇＋目錄篇）把觀念到營運走完了，但整組文章都把命令列
工具背後的模型當成給定的：站上沒有任何一篇講怎麼把 Claude Code 指到別的端點、Codex 的
`model_providers` 怎麼寫、GLM 的訂閱方案怎麼接、本機 Ollama 接得上哪一支工具，或是怎麼自架
一個同時服務兩者的閘道。這五篇補的就是這一段，登記在同一個 `ai-workflow` 系列的新群組 E。

## Definition of done

- [x] 五個內容包（`display_order` 412–416）通過 `check_article.py <slug> --assets`。
- [x] 目錄篇多一節「換模型」，內文與表格都連到五篇，`check_article.py` 仍然 OK。
- [x] `series_data/ai-workflow.json` 重新產生：17 篇、群組 A–E、四條路線（新增 `swap`）。
- [x] 五組圖檔（hero.svg／hero.jpg／diagram-1.svg）建好，hero 在位元組上限內。
- [x] `pack_cli lint --kind life` 0 errors；`pytest tests/test_guide*` 全綠；`npm run check:tasks` 綠。
- [ ] 站主決定要不要發布；發布後照批次 1 的做法先部署再 `guides-import --slug` 六篇同一趟。

## Steps

- [x] 查證：Claude Code 的 llm-gateway／llm-gateway-connect／llm-gateway-protocol／env-vars／
      model-config 五頁、Codex 的 config-basic／config-advanced／config-reference 三頁、
      docs.z.ai 的 Claude Code／devpack overview／pricing 三頁、Ollama 的 openai／faq 兩頁、
      LiteLLM 的 Claude Code Quickstart／Codex／proxy quick_start／anthropic_unified 四頁。
- [x] 撰稿五篇，每篇的 `verbatim_quote` 都先用程式對抓下來的頁面比對過才寫進研究紀錄。
- [x] `models-seen.json` 補 glm-5.3、glm-5.3-flash、glm-4.7、glm-4.5-air 四筆（31 → 35 筆）。
- [x] `series.py` 的 `SLUGS` 加五個 slug；`build_catalogue.py` 加群組 E、第四條路線與五篇的
      level／platforms／aliases／prerequisites／related；`build_assets.py` 加五個 `_DRAWINGS`。
- [x] `build_catalogue.py --related` → `pack_cli relink --slug` ×5 → `autolink --slug` ×5 →
      `prune_autolinks.py`（13 條建議保留 8 條）。
- [x] `tests/test_guide_series.py` 的 ai-workflow 斷言從 12／四群／三路線改成 17／五群／四路線。
- [ ] 人眼看過五張 hero 與五張圖解（這一輪沒有重建 contact sheet，見下方「留給下一位」）。

## How to verify

```bash
cd apps/api
for s in ai-workflow-claude-code-custom-model ai-workflow-codex-model-providers \
         ai-workflow-glm-coding-plan ai-workflow-ollama-coding-agent \
         ai-workflow-litellm-gateway ai-workflow-tutorials; do
  ./.venv/bin/python3 ../../docs/ai-workflow-series/check_article.py "$s" --assets
done
./.venv/bin/python3 ../../docs/ai-workflow-series/build_catalogue.py --check
./.venv/bin/python3 -m app.guides.pack_cli lint --kind life | grep -c "error:"   # 0
./.venv/bin/python3 -m pytest tests/test_guide_series.py tests/test_guides_content_pack.py \
  tests/test_guides_pack_ingest.py tests/test_guides_content_links.py -q
```

## Notes

- **查核的分工**：批次 1 是一篇一個撰稿代理加一位獨立查核代理。這一輪由同一個模型撰稿並自檢，
  沒有第二位代理做獨立查核。每一條 `verbatim_quote` 都用程式對照過當天抓下來的頁面（見
  `unverified_or_excluded` 的說明），但「查核不能由撰稿者自己做」這條規則這一輪沒有滿足，
  發布前值得由另一個代理再走一次 `factcheck/` 的流程。本工作區沒有這五篇的 `factcheck/` 報告。
- **官方文件互相矛盾的兩處**，兩篇都照實寫出來，沒有替任何一頁背書：
  1. Codex：設定參考頁寫 `wire_api` 的 `responses` 是唯一支援的值，進階設定頁講
     `model_verbosity` 時卻仍提到「使用 Chat Completions 的供應商」。
  2. Z.ai：Claude Code 設定頁的預設對應寫 GLM-4.7／GLM-4.5-Air，方案總覽頁卻寫所有方案支援
     GLM-5.3，而且送往 GLM-4.7 的請求會自動改由 GLM-5.3-Flash 處理。
- **檢查器的誤判**：`check_article.py` 的 `model_ids_in` 正則會把 `CLAUDE_CODE_MAX_CONTEXT_TOKENS`、
  `claude_code_zai_env.sh`、`GEMINI_API_KEY` 這種字串當成模型 id，在程式區塊裡是 FAIL（在正文
  裡只是 WARN）。這一輪的繞法是把那些字串移出程式區塊，不是放寬檢查；下一批如果常撞到，
  正則應該要求 id 後面不能接 `_`＋大寫，或加一份例外清單。
- **`prune_autolinks.py` 多剪一個詞**：`標記`。這一批的「標記」指的是模型 id 裡的標記與
  「逐一標記支援與否」，不是 token，autolink 會把它連到 `ai-term-token`。
- **環境**：這一輪在 Linux 容器跑。容器沒有 CJK 字型，Chromium 會把中文畫成空白方塊；
  解法是把 Noto Sans CJK TC 的 Regular 與 Bold 裝到 `~/.fonts` 再 `fc-cache -f`
  （`github.com/notofonts/noto-cjk` 的 `raw.githubusercontent.com` 路徑可以抓，
  `github.com/.../raw/...` 會被回 403）。`apps/api` 的 venv 用 `uv sync --frozen` 建。

### 留給下一位

- 沒有重建 `manifest.json` 與 contact sheet（那是全量建置，會動到批次 1 的十三組圖）。
  要人眼審圖時，跑不帶 `--slug` 的 `build_assets.py`，再看 `docs/ai-workflow-series/` 下的
  contact sheet；本工作區的五張新圖目前只有機器檢查（尺寸、位元組上限、SVG 規則、
  圖上數字都出現在正文）過關。
- `README.md` 的交接段落還停在批次 1，發布後要補上批次 2 的發布紀錄。
- 五篇都沒有實測：本站沒有訂閱 GLM Coding Plan、沒有架過 LiteLLM、沒有對任何第三方端點送出
  請求。每一篇都在正文與研究紀錄裡寫明了這一點，發布前不要把它拿掉。
