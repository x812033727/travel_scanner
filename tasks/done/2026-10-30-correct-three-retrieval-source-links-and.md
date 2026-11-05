---
id: 2026-10-30-correct-three-retrieval-source-links-and
title: Correct source links and first-use terms in three retrieval articles
status: done
priority: P2
area: docs
owner: codex-retrieval-source-corrections
claimed_at: 2026-10-30T08:15:26Z
created_at: 2026-10-30T00:54:30Z
completed_at: 2026-10-30T08:35:56Z
branch: codex/retrieval-source-corrections-20261030
depends_on: []
scope:
  - apps/api/app/guides/content/ai-term-hybrid-search.json
  - apps/api/app/guides/content/ai-term-knowledge-graph.json
  - apps/api/app/guides/content/ai-term-agentic-rag.json
---

# Correct source links and first-use terms in three retrieval articles

## Why

翻譯前原文審查確認一處誤導內鏈，以及三篇首次外文術語缺中文說明。
核心技術說明與當日讀取的官方來源一致；這是窄範圍來源修正，不是整篇重寫。

- **P2 — hybrid-search**：`locales.zh-TW.blocks[8].inlines[1]` 的「參數」
  連到 `ai-term-model-parameters`。上下文說的是 RRF 排名融合設定，目的稿
  定義的是模型權重與偏差，會誤導讀者。最小修正是改為保留同字的純文字 inline。
- **P3 — hybrid-search**：description／摘要首次出現 RRF，正文只有英文全名；
  首次補「倒數排名融合（RRF）」，正文可保留英文全名。摘要首次 AI 補
  「人工智慧（AI）」或直接使用中文。
- **P3 — knowledge-graph**：description／`blocks[2]` 的 RDF、`blocks[18]`
  的 JOIN、description 的 GraphRAG 首次未附中文。最小修正是首次補
  「資源描述框架（RDF）」、「聯結（JOIN）查詢」與
  「圖譜檢索增強生成（GraphRAG）」。
- **P3 — agentic-rag**：`blocks[2]` 的「反思 token」首次沒有詞元中文；
  改為「反思詞元（reflection tokens）」，可同段補
  「自我反思式檢索增強生成（Self-RAG）」。保留其特定訓練機制與一般
  Agentic RAG 的區分，不改成所有代理式檢索都需要 Self-RAG。

首次外文帶中文依 `content-pipeline/SKILL.md` 的讀者優先規則。
`ai-term-graph-rag` 原稿沒有確認的阻擋內容問題，不在本修正 scope。

## Definition of done

- [x] 僅三篇 scope 內 zh-TW 原文完成上述最小修正；原素材及其他文章不變。
- [x] 完整新舊來源 hashes、diff 與獨立 source-only 審查可核對；原文與舊證據保留。
- [x] 原生文件驗證、scoped lint、任務檢查與 diff check 通過，未混入翻譯內容。
- [x] 來源發布交接明列新鮮正式來源 baseline、版本／dirty／資產 guards、獨立
  審查與另行發布授權；只有來源修正實際發布並驗收後，才可建立翻譯新 baseline。

## Steps

- [x] 登記 2026-10-30 唯讀審查確認的 P2／P3 問題與精確來源 hashes；未認領。
- [x] 接手前查 tasks／worktrees／remote branches／open PR 碰撞，再認領這張窄票。
- [x] 等目前 retrieval 批次發布後 fresh census，再讀確切候選的正式來源全文、
  draft／published versions、dirty、metadata 與資產，和本票原稿 pins 比對。
- [x] 只修改上述誤導內鏈與首次術語，保存舊原文，取得獨立 source-only 審查。
- [x] 準備可審查來源 PR 與後續發布交接；未獲授權不 merge、deploy 或 publish。
- [ ] 來源修正發布與公開驗收完成後，以新快照／新 baseline 接續確切缺漏語系。

## How to verify

- 使用原生 `GuideDocument` 驗證與 `lint_document`，僅驗三篇 scope；核對修正前後
  完整 zh-TW 文件、原素材 hashes 與內鏈語意，不能只靠 lint 判定內容正確。
- `npm run check:tasks` 與 `git diff --check`。
- 獨立 reviewer 逐項核對最小 diff；新正文需和新鮮正式 source snapshot 綁定。
- 翻譯啟動前另核實際來源發布／公開驗收與新 baseline，不沿用本票的歷史語系資訊。

## Notes

### 2026-10-30 原始登記（歷史）

2026-10-30 審查時 repo HEAD：
`de9230aea6c1af27adda51f916e933e96028b83e`。

| 原稿（scope 內 JSON） | 審查時 raw SHA-256 |
| --- | --- |
| ai-term-hybrid-search | `36b6642bef262a0fb75dec5e42538cd3ececf870ad03d7df55672e5f82a845b5` |
| ai-term-knowledge-graph | `d8ab77b326210d28cba056ee4735f0e642b1aa1a043c966b14fb325032d06861` |
| ai-term-agentic-rag | `cff1f499126158f004d44ed75035ad4fbcd73e5d92daa44c3d74329369fbd833` |

私有完整唯讀審查證據 SHA-256：
`24bda6b87d83b9f5487e547dd1a02dc9d24e442004d66c27d424066de646c4e7`。
該審查涵蓋四篇全文、18 個本機 article 目的稿、12 個原素材、八次實際圖像檢視，
以及八個原列官方來源的當日 HTTP 200 和內容核對；四篇原生 schema／lint
零錯誤、零警告。沒有因此宣稱正式站來源版本或公開語系仍與歷史快照一致。

這張票保持 open、owner 空白，只登記接續工作；沒有編修來源或開始翻譯。
不宣稱目前缺少任何特定數量的語系。現行 embedding／semantic-search／reranking／
retrieval-augmented-generation 發布批次不在 scope，GraphRAG 也不在修正 scope。
原稿既有 checked_on 未改成本日；後續僅能按實際重新查核更新。
本票與廣泛補語系目標允許準備本機修正，不構成 merge、正式站寫入或發布授權。


### 2026-10-30 source-only corrections and release handoff

Fresh read-only capture at 08:23:26 UTC used deployed commit
`5c105c01b448c9997e70beac2abd787bf46c4222`; all 15 native commands and the
outer capture exited zero. The four selected articles are public, active and
clean, with no target-locale database rows. Hybrid-search is source v10;
knowledge-graph, agentic-rag and unchanged graph-rag are source v8. All article
metadata versions are 2. Current database source documents equal repository
packs, deployed pack bytes and all twelve deployed assets.

Only the three listed zh-TW documents changed: one misleading model-parameter
link became the same visible plain text, and first-use Chinese terminology was
added. Sources, checked_on dates, metadata, other articles and image bytes are
unchanged. Independent source-only review passed with zero open findings:
`cf2142fe43ce00aaebc35ed78d3244a6b1f88460093975b41caa70f2b46cd5e8`.
Fresh snapshot SHA-256:
`9abb9ffde5af48277ebea6a7deff129bbc53fda5c074aed66d4298e7cad666e7`.

| Source | Published normalized SHA-256 | Candidate normalized SHA-256 |
| --- | --- | --- |
| ai-term-hybrid-search | `c8914e425ab7ae1122c3e1ba446e242c26129ffa90269f699441f2be3059fb64` | `972610411149ea1010e2e8b0a23d4086181e0cb18de0dc222ae771e43dba46c5` |
| ai-term-knowledge-graph | `2a3e86ebe444de922a0c4bd38f7ce2594fa544a41698437a3469b0385cad334c` | `64f41fb947553be82d8eb0e8641265d8ed721ce5965875ffb09dd3df12f3f7be` |
| ai-term-agentic-rag | `67544b228a953cf4e2bae62d65e700eafd942120dbae7807f25d8c545a467485` | `bb7772cb28692526d8ed07068bbde4f58b47f8fa59efbb19a0257d491cea0895` |

Validation: scoped native pack lint checked all three documents with no
findings; existing content-pack tests passed 9, with 5 PostgreSQL cases skipped
because isolated integration services were not enabled locally. Task and
whitespace checks passed. CI will verify the final committed candidate.

The remaining operational checklist item is explicitly delegated to
`2026-10-30-release-corrected-retrieval-concept-sources`, an open, unclaimed
release task. Source publication and public acceptance are not completed by
this content PR. Merge, deployment and publication require their separate
authorization; rebuild the baseline after actual publication before translating
these three articles. GraphRAG is unchanged and is not part of this correction.
