---
id: 2026-10-29-localize-four-retrieval-ai-concepts
title: Localize four retrieval AI concepts
status: done
priority: P2
area: docs
owner: codex-ai-retrieval-four-20261029
claimed_at: 2026-10-29T11:35:34Z
created_at: 2026-10-29T11:35:01Z
completed_at: 2026-10-29T12:28:48Z
branch: codex/localize-ai-retrieval-four-20261029
depends_on: []
scope:
  - apps/api/app/guides/content/ai-term-embedding.json
  - apps/api/app/guides/content/ai-term-semantic-search.json
  - apps/api/app/guides/content/ai-term-reranking.json
  - apps/api/app/guides/content/ai-term-retrieval-augmented-generation.json
  - apps/web/public/guides/ai-term-embedding
  - apps/web/public/guides/ai-term-semantic-search
  - apps/web/public/guides/ai-term-reranking
  - apps/web/public/guides/ai-term-retrieval-augmented-generation
---

# Localize four retrieval AI concepts

## Why

Embedding, Semantic Search, Reranking and Retrieval-Augmented Generation are
published only in Traditional Chinese. Add their missing English, Japanese,
Korean and Simplified Chinese documents and localized artwork, preserving each
published source. This is a bounded content-authoring step in the existing
all-article language-completion effort; production publication is a separate task.

## Definition of done

- [x] Confirm exact scope ownership and obtain a fresh read-only source snapshot.
- [x] Independently review the four source documents and the fresh baseline.
- [x] Produce all sixteen translations and localized artwork through the native pipeline.
- [x] Complete independent text, image and glyph review bound to final artifact hashes.
- [x] Assemble and install a verified exact-scope bundle, preserving normalized source documents, effective metadata and original asset bytes.
- [x] Pass appropriate local content checks and independent final review.
- [x] File an unclaimed dependent release task; require exact-head green PR CI and owner approval before merging.

## Steps

- [x] Check active worktree tasks, local/remote branch changes and open PRs; claim narrow scope.
- [x] Capture the four current public source rows and derive the exact-four native baseline.
- [x] Resolve source-readiness findings before starting translation; preserve failed attempts.
- [x] Prepare, translate, render and independently review all sixteen jobs.
- [x] Install the reviewed bundle and record authoring completion for its content PR; leave merge approval pending.
- [x] File the separate production-release task; do not import or publish under this task.

## How to verify

- Native pipeline status, schema/text invariant checks, render receipts and independent hash-bound reviews.
- Native bundle assembly and installation guards; source document/metadata/asset preservation.
- Appropriate content-pack and localization tests, `npm run check:tasks`, `git diff --check` and PR CI.
- Recheck ownership and source/target freshness before opening the content PR.

## Notes

- Claimed only after a read-only audit of 76 worktrees, 710 branch heads and
  44 open PRs found no active candidate-scope owner or overlapping committed
  candidate changes. Audit SHA-256:
  3d1412e6217d37a037e5d0eac75f8972d877da22147c937462a886b7e1f012b1.
- Reused a clean attached worktree on a new branch from main 1a0c641e6. The
  preceding release-records PR #1920 was separately authorized and merged as
  2464ad1c9, with all 22 CI checks and an independent documentation review.
  It required no deployment; its worktree remains separate.
- Fresh exact-four source snapshot captured 2026-10-29T19:31:11.950577+08:00
  through an actual exit-0 read-only transaction; source draft/public version 8,
  article version 2, no existing target locale rows. API runtime and deployed
  host HEAD 9dc9dca54 remained unchanged throughout. Snapshot SHA-256:
  1df6945ecb302cc3c0b448bd497f3876f7a3f622d2c502960ef973f14f8c5a2b.
- The unchanged native baseline builder was run with external output, then
  reduced to exactly the four actual native source rows and one sixteen-target
  batch. Source differences are empty. Baseline SHA-256:
  bdc10b0cf4788f2a27b516a53900d8780624a3a40e297954ccb26f8f31219d2f;
  binding SHA-256:
  97dece24f01f970c3e13ddea057ce54aa862ca04a61a8aa3e8378e67e0b13444.
  The retained native intermediate is not a global production census.
- Both independent gates passed: source-readiness review SHA-256
  de5043f6ca101b66e08098542aff3ced3f25d1994a3d9941559393d9ad5377ed;
  baseline review SHA-256
  71b792d1ae4608d4618d00338717a64168a264772205c15159060719d78fa5dd
  (34 checks). These complementary reviews bind the local candidate source
  quality and its equality with the fresh production rows.
- Native prepare exited 0 with sixteen jobs outside Git. The unchanged native
  ChatGPT-login pipeline ran from 2026-10-29T11:51:28Z to 12:00:33Z with three
  workers and zero automatic retries. Its actual overall exit was 1: four
  outputs introduced Arabic digits where the source used word numbers.
  Only the affected translated fields were corrected, then native materialize
  and final rendering passed. All original attempts and failures remain intact.
- Independent reviewers also requested natural English table captions. The four
  captions now say "Concept comparison; sources checked in 9/2026." while
  preserving the source numeric tokens. Every final edit was independently
  reviewed. All sixteen final text, image and glyph reviews passed, including
  actual inspection of three rendered images per job. Eighteen successful
  render executions include two English rerenders after caption corrections.
- Unchanged native bundle assembly exited 0 on 2026-10-29T12:13:01Z:
  four packs, sixteen publish locales, forty-eight assets, no source corrections
  and no hubs. Manifest SHA-256:
  1be206c2bbdd0fbdebf45a9a3c1dcdb378304c498e93ca2a00ce31336dbabe5b.
  Assembly is local preparation; installation and publication are distinct gates.
- The pre-PR ownership delta found no new competing owner or overlapping PR.
  Review SHA-256:
  5e66f2d77c5e63026bd0dd50a15d827867440299d34a71119984d2c67a585557.
- Private snapshots, raw attempts, render previews and per-job reviews are kept
  in the owner's durable evidence directory and must not enter Git. The native
  installer's repository-relative input guard used byte-identical ignored local
  mirrors with their own inventory and installation journal.
- At the earlier preparation checkpoint, no content installation, database
  writes or public release had occurred. Completed local installation is recorded
  below. Green CI and owner merge approval remain mandatory PR gates after
  local authoring is complete; this cohort has not been published.
- Local dependencies installed with `npm ci --no-audit --no-fund`, exit 0. npm
  reported engine warnings for several transitive packages on the existing
  Node v24.13.0 runtime; no runtime upgrade or dependency-file change was made.
- The actual Playwright 1.64.1 headless launch/close and Sharp 0.35.5 import
  passed. An initial presence check looked for the headed Chromium binary;
  the renderer uses the existing headless shell, so no browser install was needed.
- The separate annotation-link correction task concerns Vector Database and
  Chunking, not these four packs. It remains unclaimed and is not part of this scope.

## Local installation and verification

- The unchanged native installer wrote exactly four content packs and forty-eight
  new assets. Its original-pack backups, journal and per-article admission receipts
  are retained. Every authoritative input and ignored mirror remains byte-identical.
  The native installation verification passed all sixteen admitted jobs; receipt
  SHA-256: 16b0822019bbae43615e0f887231cdf78a11536e67a60eed197ead82b6261ba4.
- An actual second native installation exited 0 and changed neither bytes nor
  mtimes of all fifty-two content destinations and twelve original assets, nor
  any journal/receipt/input bytes. Replay receipt SHA-256:
  2cd2450a6d063281ddda92059d5a6b7fcef904aa593f4a70b4d7627a69cf15fb.
- Independent candidate review confirmed the four normalized zh-TW documents,
  effective metadata, source URLs/dates, article-link identities and original
  twelve assets are unchanged. Native serialization makes defaults explicit and
  sorts topics; raw original pack JSON formatting is not claimed unchanged.
- Actual local tests passed: 35 pipeline, 25 artifact/layout, 68 native bundle
  and installation, and 2 packaged-content/life-lint tests: 130 passed, zero
  skipped. Scoped lint has zero errors and four English text-length advisories
  (7,046 / 7,372 / 7,591 / 7,285 body characters). Full reviewed translations
  were retained. Translation character checks reported zero hits.
- Separate release task:
  `tasks/open/2026-10-29-release-localized-retrieval-ai-concepts.md`, open and
  unclaimed, depending on this task. No deployment or publication has occurred
  for the current sixteen translations. The overall language-completion task
  stays open; exact-head green CI and new owner merge approval remain required.
- Final installed-content and task-handoff review passed with no findings. It
  independently verified all fifty-two installed destinations, twelve originals,
  four original-pack backups, sixteen review bindings, complete private/mirror
  inventories and all actual test logs. Review receipt SHA-256:
  53212995b49be479bca6e108dd7b06b2659e5c44bbbc2235a3a7b32575caeed1.
  The task checker validated 2,240 task files and the whitespace check passed.

## Reviewed document identities

Four independent article reviewers accepted all sixteen final documents with
zero open findings. These are local content identities, not publication receipts.

| Article | Unchanged zh-TW source SHA-256 |
| --- | --- |
| ai-term-embedding | `5427f3806d20123ce788ba9df5e9e9c5dd6d4996bfed6757b011987d9bc3d9eb` |
| ai-term-reranking | `ceaa11b4ae343af8000ea77228250ded670e1658b3dbae4802c38ae1e26534e7` |
| ai-term-retrieval-augmented-generation | `79a0cfb9cf3918cff5b24b93db4fb03e18c03665701ff4d1bab909081f5968f1` |
| ai-term-semantic-search | `e9cedeaf5b85c3a7cba00d5129da1abf600de835e70358a0b7abab33dc7175a7` |

| Article / locale | Reviewed title | Normalized document SHA-256 |
| --- | --- | --- |
| ai-term-embedding / en | What Is an Embedding? Mapping Content into a Space for Comparison | `27b42f0bd9bb6d4f9a76fb05bbc6e7dcc547bde89fd5b629f2784dadffef625f` |
| ai-term-embedding / ja | 埋め込みベクトル（Embedding）とは：内容を比較可能な空間に配置する | `af3c34ea382fbc108bf5cbdac519cd2b07ba2c73fec2c21a8a40145c31f12bff` |
| ai-term-embedding / ko | 임베딩 벡터(Embedding)란: 콘텐츠를 비교 가능한 공간에 배치하기 | `de227a105fcc0af53accff091ba6b411592d36ad6855d989669a1e10b2d565bc` |
| ai-term-embedding / zh-CN | 嵌入向量（Embedding）是什么：把内容放进可比较的空间 | `c45e9ffe1ab6800410d67b268400e2fd23f22ed083ed11bd5a154fbc347ccb80` |
| ai-term-reranking / en | Reranking: From Finding Results to Putting Good Answers First | `1c70392bd88bb63ef2689b6d9d5cb6d87ac643bce257d9961301824e3ca2a6a4` |
| ai-term-reranking / ja | 再ランキング（Reranking）：見つける段階から、良い回答を上位に並べる段階へ | `f02bd240ab1d7da6428d0874255bcb9196eed705aadc78eb7dc81b8ce6fb4ed1` |
| ai-term-reranking / ko | 재정렬(Reranking): 찾아내는 것을 넘어 좋은 답을 상위에 배치하기 | `801b9a3f13f10c089685ca9807b81e8434232a42cc17bd601752cb87dbba4598` |
| ai-term-reranking / zh-CN | 重新排序（Reranking）：从找到内容到把好答案排在前面 | `b7698e97a13804c29b248e4bcffb3f7b96664d5774ea4d19c23634260a088113` |
| ai-term-retrieval-augmented-generation / en | What Is Retrieval-Augmented Generation (RAG)? Answers with Verifiable Evidence | `54b45eaebb1a96ca808a399115b0cbc28a1187eada9db77f8d6964ab5d7b4883` |
| ai-term-retrieval-augmented-generation / ja | 検索拡張生成（RAG）とは：回答に検証できる根拠を添える | `d03f74eba75f91eb99df258122b4e1872b1a3ac2f39e806d5f3ba40ab451b2f2` |
| ai-term-retrieval-augmented-generation / ko | 검색 증강 생성(RAG)이란: 답변에 확인 가능한 근거 붙이기 | `a8b9f82fdc308d0d3ed53c0947b849429b09c9e71eeecd02b06ab499e3d7100f` |
| ai-term-retrieval-augmented-generation / zh-CN | 检索增强生成（RAG）是什么：让回答附上可查的依据 | `83a8342ad06e7a5496b1c58b746e117dbb29229e18fc6c9211f7581b30b046b4` |
| ai-term-semantic-search / en | Semantic Search: Finding Relevant Content Through Different Wording | `2b0b9bfe638db2eb2cd511a6fb5b478914e91ec10a8a7e86e1f8e966ccb4264b` |
| ai-term-semantic-search / ja | セマンティック検索（Semantic Search）：異なる言い方で関連する内容を見つける | `48aa3f01afb98bc2191a07d35175ccb61cf65702ae45ece157e4de6ce29f687c` |
| ai-term-semantic-search / ko | 의미 검색(Semantic Search): 다른 표현으로 관련 콘텐츠 찾기 | `08706d03f6210de1ad55d68549924585013855d73ea50ca962b4605d467053db` |
| ai-term-semantic-search / zh-CN | 语义搜索（Semantic Search）：用不同说法找到相关内容 | `3d5b0fd59588b6c5805e99be667a91e47abb9238d633c6cfc8fc0f4cee16b3de` |
