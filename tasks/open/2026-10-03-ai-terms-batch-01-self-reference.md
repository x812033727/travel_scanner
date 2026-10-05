---
id: 2026-10-03-ai-terms-batch-01-self-reference
title: 第一批 AI 名詞專文有 52 篇「本文／這篇」超過一次
status: in-progress
priority: P3
area: docs
owner: claude-opus-5-5-ai-terms-self-reference
claimed_at: 2026-10-05T06:55:47Z
created_at: 2026-10-03T12:04:01Z
completed_at:
branch: claude/ai-terms-self-reference
depends_on: []
scope:
  - apps/api/app/guides/content/ai-term-prompt-engineering.json
  - apps/api/app/guides/content/ai-term-harness-engineering.json
  - apps/api/app/guides/content/ai-term-loop-engineering.json
  - apps/api/app/guides/content/ai-term-agentic-engineering.json
  - apps/api/app/guides/content/ai-term-vibe-coding.json
  - apps/api/app/guides/content/ai-term-spec-driven-development.json
  - apps/api/app/guides/content/ai-term-llmops.json
  - apps/api/app/guides/content/ai-term-agentops.json
  - apps/api/app/guides/content/ai-term-prompt-chaining.json
  - apps/api/app/guides/content/ai-term-artificial-intelligence.json
  - apps/api/app/guides/content/ai-term-generative-ai.json
  - apps/api/app/guides/content/what-is-a-large-language-model.json
  - apps/api/app/guides/content/ai-term-foundation-model.json
  - apps/api/app/guides/content/ai-term-transformer.json
  - apps/api/app/guides/content/ai-term-mixture-of-experts.json
  - apps/api/app/guides/content/ai-term-small-language-model.json
  - apps/api/app/guides/content/ai-term-model-parameters.json
  - apps/api/app/guides/content/ai-term-token.json
  - apps/api/app/guides/content/ai-term-tokenization.json
  - apps/api/app/guides/content/ai-context-window-explained.json
  - apps/api/app/guides/content/ai-term-system-prompt.json
  - apps/api/app/guides/content/ai-term-few-shot-prompting.json
  - apps/api/app/guides/content/ai-term-zero-shot-prompting.json
  - apps/api/app/guides/content/ai-term-in-context-learning.json
  - apps/api/app/guides/content/ai-term-context-compaction.json
  - apps/api/app/guides/content/ai-term-context-rot.json
  - apps/api/app/guides/content/ai-term-agent-memory.json
  - apps/api/app/guides/content/ai-agents-explained.json
  - apps/api/app/guides/content/ai-term-agent-loop.json
  - apps/api/app/guides/content/ai-term-multi-agent-system.json
  - apps/api/app/guides/content/ai-term-subagent.json
  - apps/api/app/guides/content/ai-term-agent-orchestration.json
  - apps/api/app/guides/content/ai-term-react-reasoning-acting.json
  - apps/api/app/guides/content/ai-term-tool-calling.json
  - apps/api/app/guides/content/ai-term-model-context-protocol.json
  - apps/api/app/guides/content/ai-term-agent2agent-protocol.json
  - apps/api/app/guides/content/ai-term-agent-skills.json
  - apps/api/app/guides/content/ai-term-vector-database.json
  - apps/api/app/guides/content/ai-term-hybrid-search.json
  - apps/api/app/guides/content/ai-term-chunking.json
  - apps/api/app/guides/content/ai-term-rlhf.json
  - apps/api/app/guides/content/ai-term-evals.json
  - apps/api/app/guides/content/ai-term-benchmark.json
  - apps/api/app/guides/content/ai-term-llm-as-a-judge.json
  - apps/api/app/guides/content/ai-hallucination-fact-check.json
  - apps/api/app/guides/content/ai-term-multimodal-ai.json
  - apps/api/app/guides/content/ai-term-diffusion-model.json
  - apps/api/app/guides/content/ai-term-text-to-image.json
  - apps/api/app/guides/content/ai-term-automatic-speech-recognition.json
  - apps/api/app/guides/content/ai-term-text-to-speech.json
  - apps/api/app/guides/content/ai-term-deepfake.json
  - apps/api/app/guides/content/ai-term-open-weights.json
---

# 第一批 AI 名詞專文有 52 篇「本文／這篇」超過一次

## Why

讀者優先規則（`.agents/skills/content-pipeline/SKILL.md` 不變的規矩第 4 條、`intake_check.py` 的 self-reference 上限）要求
「本文」「這篇」全篇最多一次。第一批 AI 名詞專文是在這條檢查之前寫的，2026-10-03 掃描有 52 篇出現 2 到 3 次（含 description）。
第二、三批收件時都已壓到一次；2026-10-03 新加的摘要裡一次都沒有。

## Definition of done

- [x] scope 裡每篇「本文／這篇」（含 description、圖說）最多一次，改寫成「以下」「這裡」或刪掉主詞，不改事實。
- [x] `intake_check.py --slug <s> --from-content` 對每篇 self-reference 一項是 ok。

## Steps

- [x] 逐篇改、逐篇跑 intake_check。
- [ ] 合併後把 52 篇重新匯入正式站（`guides-import --slug ... --locale zh-TW --publish`）：publish after merge (coordinator, owner consent)。

## How to verify

```bash
cd apps/api
for s in $(sed -n '/^scope:/,/^[a-z_]*:/p' ../../tasks/open/2026-10-03-ai-terms-batch-01-self-reference.md | grep -o 'content/[a-z0-9-]*' | cut -d/ -f2); do
  echo "$s $(.venv/bin/python ../../.agents/skills/content-pipeline/scripts/intake_check.py --slug $s --from-content | grep self-reference)"
done
```

## Notes

- 只動措辭。改完要發布，這批文章已上線。
- 2026-10-05（claude-opus-5-5-ai-terms-self-reference）：用 `intake_check.py` 自己的 `SELF_REF` 與
  `block_texts` 計數（title＋description＋區塊文字），改前 116 次、52 篇全部超過上限（40 篇 2 次、12 篇 3 次）；
  改後 52 次，每篇剛好 1 次。
- 保留的那一次都在 description：52 篇的 description 都以「本文……為例／本文用……」交代範圍，第一批裡原本就只有
  一次的篇（`ai-term-deep-learning`、`ai-term-embedding`、`ai-term-context-engineering`）留的也是 description
  那一次，所以正文的 64 處全部改寫：
  開頭交代範圍的句子改成「以下……」「這裡……」「接下來……」，段落已經有「以下」的改用「這裡」；
  「本文沒有執行這項實驗」改成「這裡沒有執行這項實驗」；`ai-term-token` 的「它與本文的文字 token 同名」改成
  「它與這裡談的文字 token 同名」；`ai-term-vector-database` 的「這篇虛構例子」改成「這個虛構例子」；
  `ai-term-zero-shot-prompting` 的「本文是在教你驗證摘要忠實度」改成「這個例子是在教你……」；
  `ai-term-text-to-speech` 的圖說「本文引用架構」改成「所引用架構」；`ai-term-agent-loop` 原本接在「本文」後的
  「它討論的是執行機制」改成「這裡討論的是執行機制」，免得「它」被讀成那個示例。
- 沒有改任何事實、數字、來源或 `checked_on`；改動是 52 個檔案各 1 到 2 行的逐字替換（64 處），每處替換前確認
  原句在檔內只出現一次，JSON 格式不變。
- 驗證：52 篇逐篇跑 `intake_check.py --slug <s> --from-content`，全部 exit 0、零 FAIL、self-reference = 1
  （改前同一指令唯一的 FAIL 就是這一項）；其餘 WARN（不在 manifest、找不到 hero title、「規格」當一般用語、摘要／
  描述帶量詞）是原本就有的。`pack_cli lint --slug ×52`：52 entries checked、exit 0；
  `pytest tests/test_guides_content_pack.py`：9 passed、5 skipped。這台機器上一篇 intake_check 要 50 到 70 秒，
  52 篇用 4 個並行跑約 15 分鐘。
- 這批 JSON 不在 `docs/videos/long-form/review.json` 的收據裡。`docs/ai-terms-series/release-manifest.json`
  記錄的是 #486 發布時的 SHA256（早已和現況不同，#1177 加摘要時就變了），是歷史紀錄，沒有測試讀它，沒改。
- 還沒做：正式站重新匯入（文章已上線，要合併後由協調者在站主同意下跑 `guides-import --slug <52 篇> --locale zh-TW
  --dry-run` 再 `--publish`），見 Steps 未勾的一項。
