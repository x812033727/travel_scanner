---
id: 2026-10-28-localize-two-ai-concept-life-guides
title: Localize two AI concept life guides into four languages
status: done
priority: P1
area: api
owner: codex-gpt6-ai-concepts-20261028
claimed_at: 2026-10-28T13:35:22Z
created_at: 2026-10-28T13:34:08Z
completed_at: 2026-10-28T14:12:48Z
branch: codex/localize-ai-concepts-20261028
depends_on: []
scope:
  - apps/api/app/guides/content/ai-term-tokenization.json
  - apps/web/public/guides/ai-term-tokenization
  - apps/api/app/guides/content/ai-term-foundation-model.json
  - apps/web/public/guides/ai-term-foundation-model
---

# Localize two AI concept life guides into four languages

## Why

The owner requested continued completion of missing travel-information and life
article languages. These two public AI concept life articles have no English,
Japanese, Korean or Simplified Chinese documents in the repository or the fresh
selected production snapshot. This narrow content child of the existing
missing-locale program adds the eight documents and translates all text-bearing
artwork. Foundation-model's source remains unchanged. Tokenization needs two
explicitly reviewed alternative-text and matching SVG description corrections;
its article body, original JPEG, visible diagram text and geometry remain intact.

## Definition of done

- [x] Fresh production source/visibility/version and target-absence bindings pass, and full source text/artwork review finds no unresolved blocking issue.
- [x] All eight translations and their artwork pass schema/layout checks and independent hash-bound text, glyph and actual visual review.
- [x] Native assembly, installation and replay pass; only independently approved tokenization source alt/SVG metadata corrections may differ from the original sources.
- [x] Applicable content checks pass and the guarded content PR handoff is prepared; a separate release task owns deployment/publication and public acceptance.

## Steps

- [x] Check current branches, worktrees, open PR file scopes, old jobs and publish holds before claim.
- [x] Export the selected read-only production snapshot and build the scoped native baseline.
- [x] Complete current primary-source and actual original-image review before starting translation.
- [x] Prepare and run the unchanged native pipeline using the current ChatGPT login, at most three workers, no quota/auth retries and an external STOP sentinel.
- [x] Render every job, obtain independent reviews and apply only recorded corrections with retained failed attempts.
- [x] Assemble/install/replay, verify preservation, run scoped checks and prepare the content/release PR cycle.

## How to verify

Use the unchanged build_baseline.py, pipeline.py, render.mjs, assemble_bundle.py
and install_bundle.py with exact selected slugs/locales. Verify independent
review hashes against final native artifact manifests; schema success is not
editorial or visual acceptance. Run native pipeline/artifact/layout checks,
content-pack checks and task validation. CI must provide the real PostgreSQL
release-safety gate. Keep raw production data, jobs and reviews outside Git.

## Notes

- At 2026-10-28T13:31:16 UTC, a bounded repeatable-read snapshot from deployed
  `911443f2d0fb102dbe501d265849746af185a787` confirmed all seven sources public,
  active and unexpired, with clean published drafts and no target locale rows.
  The original ten-candidate snapshot also covers three held travel articles;
  this content scope selects only tokenization and foundation-model.
- All seven published canonical documents exactly match repository sources;
  no repository-only description preservation admission is needed.
- Scoped seven-article baseline SHA256:
  `d62d596e344498f584795b0be3eaa8c81b3f0ce82bbbafe10cf2ef889867bd11`.
  This is a selected-article baseline, not a whole-site census.
- The completed earlier 48-translation production release is separate. Its
  receipt PR #1913 does not authorize merging or publishing this new cohort.
- Travel source-correction tasks and the twelve-article AI income/investing
  batch retain their existing scope; no held or other-owned article is included.
- Initial preparation covered seven AI candidates and 28 unstarted jobs. Full
  source review found general labeling text incorrectly linked to the Token
  article in fine-tuning, few-shot-prompting and multimodal-ai; these are excluded
  pending explicit source corrections. Knowledge-cutoff requires a separate full
  refresh of its thirteen time-sensitive sources and is also excluded. Their
  original prepared inputs remain outside Git, without model calls or edits.
- The unpublished task id/title/scope was narrowed from seven, then three, to two before
  any translation attempt or content change. The original seven-source baseline
  and fresh snapshot remain immutable evidence of the candidate inventory.
- All 44 open PR file lists were checked, including the full exact-head local
  diff for a 9,286-file PR whose API result stopped at 3,000. No selected path
  overlaps were found; the native ownership survey also found no active task.
- Complete zero-shot source review additionally found the phrase about product
  evaluation in an appliance-manual example linked to the AI-evals article.
  That source is also held for explicit correction, rather than silently fixing
  its meaning only in translations. No translation attempts were made for it.
- Actual source-image review also found tokenization's hero and diagram
  descriptions claimed details not depicted. The two alt strings and matching
  SVG desc metadata have an exact correction candidate. It must receive an
  independent native source-correction receipt before application or tokenization
  translation. Original candidate jobs/baselines remain unchanged; corrected
  jobs use a new work root and a derived baseline retaining the old database pins.
- Foundation-model alone passed full text/primary-source and actual image
  review, and its four native translation calls have started. Its inputs remain
  the original clean published document.
- Tokenization's source correction now has independent native approval:
  `9653389d926c83b7015bff4827c6084ef95f3c147fc4a177e4b22f8905dad980`.
  Root applied only the two approved alt changes and matching SVG desc changes
  locally after verify_review passed. Four native old/new renders have identical
  pixels; original JPEG bytes, visible SVG text/geometry and body are unchanged.
  The actual public diagram SVG and unchanged JPEG are bound in the native
  receipt; editable hero.svg companion hashes/pixel identity are separately bound
  by independent evidence. No production document has been changed.
- All eight final translations passed independent full-text, glyph and actual
  image review, with sixteen rendered target previews and zero open findings.
  Foundation-model Japanese received two count-word fixes from its reviewer;
  tokenization Japanese initially failed the native numeric guard on five
  Arabic-digit forms. The reviewer supplied equivalent Japanese kanji forms,
  root applied only those five fields, and materialize/render/review passed.
  Original attempts and failures remain intact; no model retry or guard bypass.
- Corrected authoring baseline SHA256:
  `2a77df5832dbbd833495faeb101073e434865736051d60fc15876b80bd5835df`.
  Its tokenization document has the approved corrections while its original
  database version/hash pins remain unchanged. Foundation-model's complete
  baseline article row is unchanged. Independent integration review SHA256:
  `a6265c834908ca1393739ec4c96568fa024a5ea932d80e8d90d3f1fc0b360d75`.
- Independent final review indexes/evidence SHA256:
  - Foundation en/ja: `3e27a2116de0245f96422d4f49fd89cf6f5378cd046df159967b65bc8d97b49f`.
  - Foundation ko/zh-CN: `dd69291094ab97e88cc72b803f9ff87b956426aa321ace682e3deecf4671fa7c`.
  - Tokenization en: `81750d413bdbcf49806eab7584c72aa4a07795f9edf910a56c37cdd3e6e03fd3`.
  - Tokenization ja: `b29f8e94c07d1c6cd0fd9fa969c6d117ce41da784a9a11ee5c783f51b9ef520b`.
  - Tokenization ko/zh-CN: `63ceef674e79c2052d8a460dd008d6bd7418b77cece38661f6a8340c87d5eb88`.
- Native assembled manifest SHA256:
  `26e5a4626ea069118ea232383e15c20d149ff09246ce1ce7839caf4d45eeeffe`.
  It contains two packs, twenty-six assets, eight new translations and one
  tokenization zh-TW source-correction operation. This is the local planned
  publication scope, not a production dry-run or publication result.
- Native installation succeeded with twenty-eight operations. Replay preserved
  all thirty-two scoped content/asset file hashes and modification times;
  the two installation receipts were rewritten with identical bytes, as the
  existing installer normally does. A first broad modification-time assertion
  caught those receipt rewrites; no content drift or hidden failure was ignored.
- The installer requires repository-relative inputs, so its input mirror is
  locally ignored and byte-identical to the external baseline, jobs and bundle.
  No source snapshot, model output or raw operational evidence is committed.
- Scoped pack lint checked two entries: zero errors, with English text-length
  advisories of 7,255 and 7,057 characters retained without shortening. Content
  pack pytest passed 9 tests with 5 database-dependent skips; translation glyph
  checks reported zero hits. The real PostgreSQL gate remains CI's responsibility.
- Separate unclaimed tasks retain release work, four misleading AI source links,
  zero-shot image text, knowledge-cutoff freshness and the existing held travel
  source corrections. Current authoring does not reduce the public backlog count.
- Existing native validation passed: pipeline 35, artifact/render-layout 25,
  baseline/assemble/install/progress 68, and source-correction publisher 6
  (6 PostgreSQL variants skipped locally). Validation summary SHA256:
  `5a1d47e36a4aa30d29f6ef0f3e946b5b2662b184107667327cd54fabbacf6f4e`.
  The first full docs run hit eleven Windows long-path errors in temporary
  atomic-backup files. The unchanged suite passed all 68 using a short basetemp,
  including its isolated Git fixture; both failed and successful logs remain.
- Native assembly materializes schema defaults (`news_date: null`, `aliases: {}`,
  `related: []` and empty image descriptions) and takes the baseline topic order
  `[ai, ai-terms, tutorial]`, replacing `[ai, tutorial, ai-terms]`. Topic membership
  is unchanged, but the array order is an actual serialized change, not merely
  a schema default. Source preservation is asserted on canonical documents;
  raw JSON formatting and missing-versus-default keys are not byte identity.
- Independent installed-source/asset/journal review passed with zero findings.
  Review SHA256:
  `05aa7c6383dd1cf57843800667f334fcb7decdfac4d5f9620ba71f49e59d99bb`.
  All eight review chains, twenty-six bundle assets, twenty-eight operations,
  four rollback backups and 192 ignored input-mirror files were verified.

- Final pre-PR ownership review checked 43 open PRs, all 247 remote heads and
  73 registered worktrees. No competing content claim, committed scope change
  or landed target translation was found; the 9,286-file PR was checked beyond
  the API's 3,000-file cap. Two old unrelated QA checkouts have missing indexes,
  making every tracked path appear deleted; they were preserved without repair
  and are recorded as incomplete-checkout limitations, not competing edits.
  Ownership review SHA256:
  `76cdaa43b2f9239cb07e491084ac9c40afaf18bb581a3c2639784f9da5d08dc2`.
- Content/task work is ready for a draft PR with `no-auto-merge`. CI, owner merge
  approval, deployment and publication remain distinct subsequent gates.
- The task tool wrote the completed copy but Windows retained the open copy.
  An exact comparison found only status/completion-time differences; the stale
  open copy was then removed, preserving the complete finished task.

## Final canonical translation documents

| Article | Locale | Title | Document SHA256 |
| --- | --- | --- | --- |
| ai-term-foundation-model | en | What Is a Foundation Model? | `144df57833a0491b6702e381521e268886b9b0c22f705b98e772cd983c4afc77` |
| ai-term-foundation-model | ja | 基盤モデル（Foundation Model）とは | `93ad7e557bf8e33ff625dbe1a3ee93e45c42149a2d7200a2ef0774ceb2e50f8b` |
| ai-term-foundation-model | ko | 파운데이션 모델(Foundation Model)이란 무엇인가 | `0a74ada6de3856bb9a944f740c5b11f47ecf71f607efb5fb4d6196262904ff98` |
| ai-term-foundation-model | zh-CN | 基础模型（Foundation Model）是什么 | `f3075643714ff898a5af0a5ee4736e56a6139d6e725e06c94a6b962df20bb65d` |
| ai-term-tokenization | en | What Is Tokenization? Splitting Text Before It Enters a Model | `fb816d02e8ffd6cc9e14df87bb5d9c1d42d5b2023c47f19d060177dea0584b48` |
| ai-term-tokenization | ja | トークン化（Tokenization）とは：テキストをモデルに渡す前の分割 | `54966a696831a5ea8b7a51b4d54231e472d703087702073d3d85915e865990d9` |
| ai-term-tokenization | ko | 토큰화(Tokenization)란: 모델에 입력되기 전 텍스트 나누기 | `923c9f31a2aa1ae3a7b2d4b7ecf315351af4924885cce90a25f1fe06cf3c5b8a` |
| ai-term-tokenization | zh-CN | 分词（Tokenization）是什么：文本进入模型前的切分 | `d97c1ba683124c82ba19a65919cf260e01e414771e2b50f763c2863e61867ce6` |
