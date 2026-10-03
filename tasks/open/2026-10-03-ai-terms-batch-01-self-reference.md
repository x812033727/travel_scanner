---
id: 2026-10-03-ai-terms-batch-01-self-reference
title: 第一批 AI 名詞專文有 52 篇「本文／這篇」超過一次
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-03T12:04:01Z
completed_at:
branch:
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

- [ ] scope 裡每篇「本文／這篇」（含 description、圖說）最多一次，改寫成「以下」「這裡」或刪掉主詞，不改事實。
- [ ] `intake_check.py --slug <s> --from-content` 對每篇 self-reference 一項是 ok。

## Steps

- [ ] 逐篇改、逐篇跑 intake_check。

## How to verify

```bash
cd apps/api
for s in $(sed -n '/^scope:/,/^[a-z_]*:/p' ../../tasks/open/2026-10-03-ai-terms-batch-01-self-reference.md | grep -o 'content/[a-z0-9-]*' | cut -d/ -f2); do
  echo "$s $(.venv/bin/python ../../.agents/skills/content-pipeline/scripts/intake_check.py --slug $s --from-content | grep self-reference)"
done
```

## Notes

- 只動措辭。改完要發布，這批文章已上線。
