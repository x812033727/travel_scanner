---
id: 2026-09-24-ai-cost-article-opus-55
title: 文章〈成本、品質、延遲〉的成本試算改用 Claude Opus 5.5
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-09-24T08:10:38Z
created_at: 2026-09-24T08:08:40Z
completed_at:
branch: claude/ai-cost-article-opus-55
depends_on: []
scope:
  - apps/api/app/guides/content/ai-workflow-cost-quality-latency.json
  - apps/web/public/guides/ai-workflow-cost-quality-latency/diagram-1.svg
---

# 文章〈成本、品質、延遲〉的成本試算改用 Claude Opus 5.5

## Why

試作影片〈AI 模型怎麼挑〉（`docs/videos/ai-model-choice/`）改編自已發布的生活文章 `ai-workflow-cost-quality-latency`（只有 zh-TW）。影片的說明欄和片尾都請觀眾到文章看「完整算式與比較表」。

兩邊的數字對不上：
- **文章**：2026-09-18 查證，旗艦用 Claude Opus 5（每百萬 token 5／25 美元），算出單一旗艦 0.03、級聯 0.0114、並行互審 0.1004 美元，級聯省 62%。
- **影片**：Claude Opus 5.5 在 2026-09-22 發布，標準價 4／20 美元，同一天 Opus 5 被列為 legacy。站主 2026-09-24 決定影片改用 Opus 5.5 計，結果是 0.024／0.0096／0.0944 美元，級聯正好省 60%。

站主選擇把文章也改成 Opus 5.5，讓觀眾點進去看到的數字和影片一致。

## Definition of done

- [ ] 文章裡所有用到 Opus 5 價格的地方都改成 Opus 5.5 重算的數字，包括摘要、正文、表格、callout、FAQ 與圖解 `diagram-1.svg`；算法與假設不變（輸入 3,000、輸出 600 token，三成升級，評審讀 4,200 寫 200）。
- [ ] 其他三個單價當天重新核對官方頁：Claude Sonnet 5、Gemini 3.5 Flash-Lite、gpt-6-astra（OpenAI 定價頁已轉址到 `developers.openai.com/api/docs/pricing`）；`sources` 的 `checked_on` 改成核對當天。
- [ ] 換人查核一輪，走 skill `content-pipeline` 的查核提示。
- [ ] 部署後匯入正式站，確認 `https://mokaair.com/zh-TW/life/ai-workflow-cost-quality-latency` 顯示新數字。

## Steps

- [ ] 認領；從 origin/main 開分支。
- [ ] 改 pack 與圖解。數字可以直接對照影片的 `docs/videos/ai-model-choice/claims.md` c6–c8 與 `verify-2.md` 的算式。
- [ ] 查核代理（換人）→ 修正 → PR → 綠燈合併 → 部署 → 匯入（照 `content-pipeline` 的 publish runbook，一定要帶 `--slug`）。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli ingest --from <workdir> --slug ai-workflow-cost-quality-latency --dry-run
```

打開正式站的文章頁，確認表格和圖解的數字和影片一致。

## Notes

- 查核第 2 輪提出一個沒動的疑點：Opus 5.5 的 thinking 無法關閉。如果 thinking token 也按輸出計費，600 個輸出 token 的假設對 Opus 5.5 比對 Opus 5 更樂觀。改文章時要查 Anthropic 的 thinking 文件，決定要不要在假設旁邊註明。
- Anthropic 沒有把 Opus 5.5 稱為旗艦，陣容最上層是 Fable 5.1。文章裡的「旗艦」只是流程中的角色名稱，第一次出現時要寫清楚是以哪個型號計算。
