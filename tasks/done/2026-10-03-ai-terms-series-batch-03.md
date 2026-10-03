---
id: 2026-10-03-ai-terms-series-batch-03
title: AI 名詞系列第三批：10 個新詞專文
status: done
priority: P2
area: docs
owner: claude-opus-5-5-ai-terms-03
claimed_at: 2026-10-03T10:28:47Z
created_at: 2026-10-03T10:28:46Z
completed_at: 2026-10-03T12:13:28Z
branch: claude/sweet-ramanujan-1v06fx
depends_on: []
scope:
  - docs/ai-terms-series/batch-03
  - apps/api/app/guides/content/ai-term-reinforcement-learning.json
  - apps/web/public/guides/ai-term-reinforcement-learning
  - apps/api/app/guides/content/ai-term-kv-cache.json
  - apps/web/public/guides/ai-term-kv-cache
  - apps/api/app/guides/content/ai-term-overfitting.json
  - apps/web/public/guides/ai-term-overfitting
  - apps/api/app/guides/content/ai-term-interpretability.json
  - apps/web/public/guides/ai-term-interpretability
  - apps/api/app/guides/content/ai-term-data-poisoning.json
  - apps/web/public/guides/ai-term-data-poisoning
  - apps/api/app/guides/content/ai-term-world-model.json
  - apps/web/public/guides/ai-term-world-model
  - apps/api/app/guides/content/ai-term-vision-language-model.json
  - apps/web/public/guides/ai-term-vision-language-model
  - apps/api/app/guides/content/ai-term-reward-hacking.json
  - apps/web/public/guides/ai-term-reward-hacking
  - apps/api/app/guides/content/ai-term-local-inference.json
  - apps/web/public/guides/ai-term-local-inference
  - apps/api/app/guides/content/ai-term-rate-limit.json
  - apps/web/public/guides/ai-term-rate-limit
---

# AI 名詞系列第三批：10 個新詞專文

## Why

站主要求照第二批票上列的候選繼續補 AI 名詞系列：強化學習、KV 快取、過擬合、可解釋性、資料投毒、世界模型、
視覺語言模型、獎勵駭客、本機推論、速率限制。其中速率限制與本機推論在 `ai-glossary-50-terms` 只有一句話定義；
其餘是讀第一、二批專文時一定會碰到、卻沒有專文的詞。

規格在 [`docs/ai-terms-series/batch-03/`](../../docs/ai-terms-series/batch-03/brief.md)；
總索引與速查的連結、別名、摘要由 `2026-10-03-ai-terms-series-batch-02` 那張票（同一個 owner）處理，因為兩個檔案在那張票的範圍裡。

## Definition of done

- [x] 10 個內容包落在 `apps/api/app/guides/content/ai-term-*.json`，topics 含 `ai-terms`，各有 hero 與 diagram-1。
- [x] 每篇一輪獨立查核；第一輪改超過三處事實的 6 篇再換人做第二輪。
- [x] 每篇有 `summary` 區塊，由另一位代理逐句對照正文核實。
- [x] `intake_check.py --from-content` 全部 PASS；`pack_cli lint --kind life` 零 error、零 warning。
- [x] 20 張圖逐張目視，圖上數字與正文一致（示例數字我另外驗算過）。
- [x] 總索引、50 詞速查、`aliases.json` 接上 10 篇。
- [ ] 開 PR、合併。
- [ ] 部署後發布（要站主同意）：10 篇先發，總索引與速查最後。

## Steps

- [x] 寫 `brief.md`（第二批學到的規則前置）、`VERIFY.md`、`catalogue.json`。
- [x] workflow：撰稿 → 查核 → 條件式第二輪 → 摘要 → 摘要核對，10 篇分五組並行。
- [x] 收件：ingest、協調者修正、套摘要、看圖。
- [x] 接索引、速查與別名。
- [ ] PR。

## How to verify

```bash
cd apps/api
S=$(python3 -c "import json;print(' '.join('--slug '+t['slug'] for t in json.load(open('../../docs/ai-terms-series/batch-03/catalogue.json'))['terms']))")
uv run python -m app.guides.pack_cli lint --kind life $S --warnings
for s in $S; do [ "$s" = --slug ] || uv run python ../../.agents/skills/content-pipeline/scripts/intake_check.py --slug $s --from-content | tail -1; done
uv run pytest tests/test_guides_content_pack.py tests/test_guides_pack_ingest.py tests/test_guides_aliases.py -q
```

## Notes

- **未勾的項目：** 合併由站主在草稿 PR 上決定；部署後的正式發布交給 `2026-10-03-release-ai-terms-batches-02-03`。

- 查核數字與協調者收件時另改的地方在 [`ARTICLES.md`](../../docs/ai-terms-series/batch-03/ARTICLES.md)。
- workflow 每個只能同時跑 2 個代理（容器 4 顆 CPU），所以把同一份腳本開成五個 workflow 並行，各跑 2 篇。
- 「獎勵投機」是指派要求說明的譯名，但查不到 AI 語境的用例，正文不收；`獎勵駭客` 也只有二手網頁的用例，正文寫明譯名不統一。
- 「policy」本系列用「策略」，Google 繁中機器學習詞彙表用「政策」；世界模型與強化學習兩篇一致用「策略」。
- 發布時 `ai-term-world-model` 與 `ai-term-reward-hacking` 互連 `ai-term-reinforcement-learning`，三篇要同一批發。
