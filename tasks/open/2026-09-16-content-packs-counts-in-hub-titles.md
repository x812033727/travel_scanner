---
id: 2026-09-16-content-packs-counts-in-hub-titles
title: "Content packs: counts in the three live hub articles and the 82 links to the glossary index"
status: in-progress
priority: P2
area: docs
owner: claude-opus-5
claimed_at: 2026-09-16T08:54:15Z
created_at: 2026-09-16T06:14:00Z
completed_at:
branch: claude/hub-pack-counts
depends_on:
  - 2026-09-16-stop-showing-article-counts-and-lesson
scope:
  - apps/api/app/guides/content/ai-search-terms-index.json
  - apps/api/app/guides/content/ai-terms-index.json
  - apps/api/app/guides/content/gemini-guide.json
  - apps/api/app/guides/content/ai-agents-explained.json
  - apps/api/app/guides/content/ai-context-window-explained.json
  - apps/api/app/guides/content/ai-glossary-50-terms.json
  - apps/api/app/guides/content/ai-hallucination-fact-check.json
  - apps/api/app/guides/content/ai-reasoning-models-explained.json
  - apps/api/app/guides/content/ai-term-agent-loop.json
  - apps/api/app/guides/content/ai-term-agent-memory.json
  - apps/api/app/guides/content/ai-term-agent-orchestration.json
  - apps/api/app/guides/content/ai-term-agent-skills.json
  - apps/api/app/guides/content/ai-term-agent2agent-protocol.json
  - apps/api/app/guides/content/ai-term-agentic-engineering.json
  - apps/api/app/guides/content/ai-term-agentic-rag.json
  - apps/api/app/guides/content/ai-term-agentops.json
  - apps/api/app/guides/content/ai-term-artificial-intelligence.json
  - apps/api/app/guides/content/ai-term-automatic-speech-recognition.json
  - apps/api/app/guides/content/ai-term-benchmark.json
  - apps/api/app/guides/content/ai-term-chunking.json
  - apps/api/app/guides/content/ai-term-content-credentials.json
  - apps/api/app/guides/content/ai-term-context-compaction.json
  - apps/api/app/guides/content/ai-term-context-engineering.json
  - apps/api/app/guides/content/ai-term-context-rot.json
  - apps/api/app/guides/content/ai-term-deep-learning.json
  - apps/api/app/guides/content/ai-term-deepfake.json
  - apps/api/app/guides/content/ai-term-diffusion-model.json
  - apps/api/app/guides/content/ai-term-direct-preference-optimization.json
  - apps/api/app/guides/content/ai-term-embedding.json
  - apps/api/app/guides/content/ai-term-evals.json
  - apps/api/app/guides/content/ai-term-few-shot-prompting.json
  - apps/api/app/guides/content/ai-term-fine-tuning.json
  - apps/api/app/guides/content/ai-term-foundation-model.json
  - apps/api/app/guides/content/ai-term-generative-ai.json
  - apps/api/app/guides/content/ai-term-graph-rag.json
  - apps/api/app/guides/content/ai-term-guardrails.json
  - apps/api/app/guides/content/ai-term-harness-engineering.json
  - apps/api/app/guides/content/ai-term-human-in-the-loop.json
  - apps/api/app/guides/content/ai-term-hybrid-search.json
  - apps/api/app/guides/content/ai-term-in-context-learning.json
  - apps/api/app/guides/content/ai-term-jailbreak.json
  - apps/api/app/guides/content/ai-term-knowledge-distillation.json
  - apps/api/app/guides/content/ai-term-knowledge-graph.json
  - apps/api/app/guides/content/ai-term-llm-as-a-judge.json
  - apps/api/app/guides/content/ai-term-llmops.json
  - apps/api/app/guides/content/ai-term-loop-engineering.json
  - apps/api/app/guides/content/ai-term-lora.json
  - apps/api/app/guides/content/ai-term-machine-learning.json
  - apps/api/app/guides/content/ai-term-mixture-of-experts.json
  - apps/api/app/guides/content/ai-term-model-context-protocol.json
  - apps/api/app/guides/content/ai-term-model-parameters.json
  - apps/api/app/guides/content/ai-term-multi-agent-system.json
  - apps/api/app/guides/content/ai-term-multimodal-ai.json
  - apps/api/app/guides/content/ai-term-open-source-ai.json
  - apps/api/app/guides/content/ai-term-open-weights.json
  - apps/api/app/guides/content/ai-term-pretraining.json
  - apps/api/app/guides/content/ai-term-prompt-caching.json
  - apps/api/app/guides/content/ai-term-prompt-chaining.json
  - apps/api/app/guides/content/ai-term-prompt-engineering.json
  - apps/api/app/guides/content/ai-term-prompt-injection.json
  - apps/api/app/guides/content/ai-term-quantization.json
  - apps/api/app/guides/content/ai-term-react-reasoning-acting.json
  - apps/api/app/guides/content/ai-term-red-teaming.json
  - apps/api/app/guides/content/ai-term-reranking.json
  - apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json
  - apps/api/app/guides/content/ai-term-rlhf.json
  - apps/api/app/guides/content/ai-term-sandbox.json
  - apps/api/app/guides/content/ai-term-semantic-search.json
  - apps/api/app/guides/content/ai-term-small-language-model.json
  - apps/api/app/guides/content/ai-term-spec-driven-development.json
  - apps/api/app/guides/content/ai-term-subagent.json
  - apps/api/app/guides/content/ai-term-supervised-fine-tuning.json
  - apps/api/app/guides/content/ai-term-system-prompt.json
  - apps/api/app/guides/content/ai-term-test-time-compute.json
  - apps/api/app/guides/content/ai-term-text-to-image.json
  - apps/api/app/guides/content/ai-term-text-to-speech.json
  - apps/api/app/guides/content/ai-term-text-to-video.json
  - apps/api/app/guides/content/ai-term-token.json
  - apps/api/app/guides/content/ai-term-tokenization.json
  - apps/api/app/guides/content/ai-term-tool-calling.json
  - apps/api/app/guides/content/ai-term-transformer.json
  - apps/api/app/guides/content/ai-term-vector-database.json
  - apps/api/app/guides/content/ai-term-vibe-coding.json
  - apps/api/app/guides/content/ai-term-zero-shot-prompting.json
  - apps/api/app/guides/content/what-is-a-large-language-model.json
  - docs/ai-search-series/ARTICLES.md
  - docs/ai-search-series/catalogue.json
  - docs/ai-terms-series/ARTICLES.md
  - docs/ai-terms-series/revise_glossary.py
  - docs/gemini-series/lessons/00.md
  - tasks/open/2026-09-15-content-summary-howto-and-life.md
---

# Content packs: counts in the three live hub articles and the 82 links to the glossary index

## Why

站主要求全站不再顯示會成長的數字，理由是「篇數會一直增加」。#533 拿掉了程式與版面上的篇數，
並把系列卡從首頁搬到主題頁。部署後系列卡顯示的是中心文章自己的標題與描述，而這三篇的內容本身有數字：

| 內容包 | 寫死的數字 |
| --- | --- |
| `gemini-guide` | 描述與開頭段「開發工具的**五十篇**教學」 |
| `ai-terms-index` | 標題「AI 名詞總索引：**81 個概念**，從 Loop Engineering 到生成式 AI」；描述與開頭段「把 81 個概念分成八組」 |
| `ai-search-terms-index` | 標題「…名詞總索引：**10 篇**看懂差在哪」；描述與開頭段「連到**十篇**專文」；「不必按順序讀完十篇」；文末連到名詞總索引的連結文字「AI 名詞總索引：81 個概念」 |

原本首頁那張 Gemini 卡顯示的「50 篇完整教學」是程式覆寫的；#533 拿掉覆寫後，露出的就是這篇自己的描述。

改 `ai-terms-index` 的標題還牽動 **82 篇已上線文章**：它們在文末用完整舊標題當連結文字。
`ArticleInline.text` 是存在每篇內容包裡、照原樣渲染的（`content-blocks.tsx`），不會跟著目標文章的標題變，
所以只改標題的話，這 82 篇裡還是看得到「81 個概念」。站主選擇同一個 PR 一起改。

## Definition of done

- [x] 三篇中心文章的標題、描述與開頭段不再有會成長的數字。
- [x] 82 篇的連結文字換成新標題。
- [x] 會把舊標題寫回去的來源一起改：`revise_glossary.py`，以及系列目錄與 lesson 原稿。
- [ ] 85 篇已重新匯入正式站，主題頁的系列卡與文章內連結都看不到這些數字。

## Steps

- [x] 新標題保留原本搶的查詢詞：`AI 名詞總索引：從 Loop Engineering 到生成式 AI`、
      `GEO、AEO、AIO 與 SEO 名詞總索引：四個縮寫差在哪`（「四個縮寫」是標題本身列的四個詞，不會成長）。
- [x] 描述與開頭段只拿掉數字，其他句子不動。「五個地方」「四個縮寫」「這四篇是骨幹」「另有三篇」是固定清單，不是目錄大小，保留。
- [x] 82 篇只換 `"text": "<舊標題>"` 這一個字串，不碰其他內容。
- [x] 在 `2026-09-15-content-summary-howto-and-life` 票裡留言：這 85 個檔已經改過，批次提交前先 rebase。

## How to verify

```bash
grep -rl "81 個概念" apps/api/app/guides/content | wc -l      # 0
grep -rl "10 篇看懂差在哪\|五十篇教學" apps/api/app/guides/content | wc -l   # 0
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life
cd apps/api && uv run pytest tests/test_guides_content_pack.py
```

部署後以 `--slug` 限定匯入這 85 篇（**不要不帶 `--slug`**，會把暫緩的 206 篇一起發布），
然後看 `/zh-TW/life/topics/ai` 的系列卡與 `/zh-TW/life/ai-term-agent-loop` 文末的連結。

## Notes

`apps/api/app/guides/content` 整個目錄被 `2026-09-15-content-summary-howto-and-life`（claude-fable-5-1，
in-progress）佔著，而且它接下來的批次正好是 `ai-term-` 與 `gemini-`。站主在 2026-09-16 明確決定不等，
所以這張票用 `--force` claim，並在那張票裡留言。改動都是單行字串替換，對方 rebase 時多半自動合併。

未發布內容包裡的數字（`claude-code-tutorials`、`codex-learning-hub`、`claude-code-build-todo-app` 的描述，
以及 73 個包正文的「第 N 篇」）拆到 `2026-09-16-unpublished-content-packs-hub-descriptions-and`。
