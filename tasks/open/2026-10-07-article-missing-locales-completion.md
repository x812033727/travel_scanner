---
id: 2026-10-07-article-missing-locales-completion
title: Complete all missing published travel and life article locales
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-07T04:49:38Z
completed_at:
branch: codex/article-locales-completion-20261029
depends_on: []
scope:
  - docs/article-localization/coverage-20261007.md
---

# Complete all missing published travel and life article locales

## Why

The owner requested every missing language for the published travel-information,
travel-guide and life-sharing articles. The 2026-10-07 read-only production
snapshot has 862 incomplete public articles and 3,448 missing public documents
(en, ja, ko and zh-CN). Existing translations must be reused rather than rewritten.

## Definition of done

- [ ] Every eligible public article in intel, howto and life has all five public languages.
- [ ] Source text, existing published translations and original images remain preserved.
- [ ] New text and image text have independent hash-bound reviews.
- [ ] Every released wave has guarded publication and public desktop/mobile verification.
- [ ] A fresh production inventory confirms zero missing eligible language documents.

## Steps

- [x] Audit production, repository, old translation work and concurrent task scopes.
- [x] Export a fresh full production snapshot and build a pinned repository-backed baseline.
- [x] Identify 116 existing unpublished locale documents in 29 life article packs.
- [x] Independently review, compile and rehearse the first reusable 2-article/8-locale wave.
- [ ] Translate and review travel articles, then remaining life articles, in waves of at most 20.
- [ ] Open narrow content/release tickets for each wave; merge, deploy and publish with receipts.
- [ ] Refresh production coverage after every release and close only after all eligible gaps are filled.

## How to verify

Use the full `export_snapshot.py` result and effective article visibility to count
published locale gaps. Run the official localization bundle guards, content lint
and applicable CI checks for every wave. Bind independent reviews to document,
asset and artifact hashes. Verify each released locale through public APIs and
the browser, including body, images, canonical, hreflang, links and mobile layout.

## Notes

- Snapshot captured 2026-10-07T04:45:46.904711+00:00. Eligible public cohort: 1,246 articles.
- intel: 21 incomplete articles / 84 locales; howto: 108 / 432; life: 733 / 2,932.
- Missing locales are en, ja, ko and zh-CN for every incomplete article. No missing
  target has a database draft. 116 target documents already exist in repository packs.
- All 96 database-only articles in this cohort already have five public languages;
  the original full export is retained, and the official builder is scoped to
  repository-backed records without excluding any missing target.
- Baseline includes 251 repository/database document differences. Database
  published documents remain authoritative; inspect each affected wave before translation.
- First exact reusable wave: marketing-mix-models and brand-tone-vibe-marketing.
  Current full review and corrections completed; the compiled prospective candidate
  passed 13 isolated same-deployed-image rehearsal cases. Final within-cohort
  related-reading labels were then corrected before the expanded content freeze.
- The fixed first content cohort contains 13 articles / 52 target documents.
  Singapore entry and powerbank final review passed before the Git freeze.
  All 13 packs lint with zero errors after the last two official installs.
  Inherited summary/length advisories remain.
- Release ticket 2026-10-07-release-localized-travel-life-wave-20261007 owns only
  publication evidence. Deployment/publication still require concrete approvals.
- All snapshots, model jobs, logs, review inputs and queue state live in the
  owner's persistent external work directory. Do not commit raw production data.
- Existing active batch-8 and Korea/source-correction scopes, unpublished hubs,
  private/expired articles and publish_holds remain excluded from automatic work.
- This program ticket owns coverage documentation only. Claim separate narrow
  content and release tickets before changing article packs, images or release records.
- No new translation or publication is claimed complete by this inventory.

### 2026-10-07 original authoring checkpoint and owner gate (historical)

First content PR #1365 is a draft at exact head
`3812fe2c9ae8c58d1eb0373d22529e76a27349c7`; all 21 check runs completed with
success, including full-stack smoke and release safety. It contains 13 articles /
52 independently reviewed target documents. No merge or deployment was performed.

The next content cohort contains Japan refund source correction + four missing
languages and four business-analysis articles / sixteen existing unpublished
targets: 5 articles / 20 independently reviewed targets. All five packs passed
scoped lint; the official refund install/replay was byte-identical. Publication
has separate refund and business-analysis release tickets. The fixed first13
cohort and its reviewed candidate were not expanded.

Cumulative local review readiness is 18 articles / 72 target documents. This is
not live publication. The latest full production inventory remains the retained
04:45 UTC snapshot: 862 incomplete eligible articles / 3,448 missing public
language documents. Completed production publications in this program: zero.
The full 862-article external queue preserves original pins, reviews, source
holds, attempts and the remaining work; source corrections and already active
scopes must not be blindly translated or overwritten.

The owner has been asked to choose whether to merge/deploy PR #1365, merge only,
or retain the draft. Until a choice arrives, keep production unchanged. Release
this coverage-only claim while waiting; resume by reclaiming it and reading the
persistent program state, exact current PR heads and fresh production guards.
This overall task stays open until a fresh production count is zero.

### Continued preparation after owner follow-up (historical checkpoint)

The owner requested continuation. Reclaimed this coverage-only task on
`codex/article-locales-wave3-20261007`, starting from the exact second content
head. At that observation both draft PRs had all21 successful checks at their heads.
No merge/deploy/publication choice was selected; preparation continues within
the authorized translation/review scope while those concrete choices remain
pending.

Twelve existing life packs / 48 targets are undergoing current source, ownership
and full independent text/image review. Separate six-pack content tasks will
own any resulting corrections. Hong Kong entry and Taiwan holiday sources are
being rechecked in parallel before new travel jobs. The original862-article
queue and latest production gap counts are unchanged; preparation is not
publication and this overall task is not done.

Earlier continuation checkpoint: the12 life/48 target final independent reviews were
aggregated verbatim (reviewSHA adbd51543953e233f37f32f3da5090037b998ecff963090bd14425677ad1aeb3;
evidenceSHA4a2f4883988c3f93c4c33abff7cf1b2110666f8c5c10d35f26679898af451f3b).
Official prospective compile is pending, so the prior18/72 completed local
readiness checkpoint remains unchanged. Taiwan/HK8 new targets remain under
final review;15 genuine Taiwan findings have been applied and rerendered with
original/failing artifacts preserved. Wave4 read-only audits filed explicit
Japan source-correction and Sapporo-route follow-ups without expanding wave3.
Global original production deficit3448 and completed_publications=[] remain
unchanged; no production content write, merge or deployment was performed by this program.

### Complete third-cohort authoring handoff

A later live observation confirms both first PRs were merged, at main commits
`a5b6905ae8e48a24f461aef750b1d069c5d0af79` and
`77a58c85a4912daad9a1d117364e5260d92a9cc6`. All240 first-eighteen content/media
files match their historical reviewed bytes and landed main. The new third branch
was rebased onto current main; no deployment or publication is inferred from merge.

All14 fixed third-cohort articles/56 targets now have genuine independent final
text/image/glyph/link reviews. Taiwan and Hong Kong completed unchanged official
assembly/install/replay with exact real journals/backups/admission guards. The
12 life/48 targets completed official prospective double-compilation on content
freeze `c4d0ce50e693e2bfa1a26366378af6f02ec625c1`; all158 output files match,
both verifications pass, and original review/source/database/media pins remain exact.
Verification SHA
`967d33f5393e479e73b571095474bd8fa08a6d4da56a60fddb64aea02310e48c`.
Public-safe evidence is recorded in the five scoped review notes and coverage file.

Authoring evidence now covers32 articles/128 targets (32 new,96 reviewed existing).
The previous durable ledger checkpoint is18/72; update it only against the final
third PR/head and its actual external compiler/installation evidence. Original
862 queue rows, source holds,3448 production deficit and zero program publications
must stay intact. The narrow release tickets and this global task remain open.

Local scoped checks pass. The complete Windows tools run exited1 with existing
platform issues and a newly filed project-lease test-import follow-up. The stock
path assertion and Windows speech-journal rename are already tracked by
`2026-10-07-accept-windows-separators-in-stock-fetch` and
`2026-10-07-preserve-speech-journal-writes-through-windows` in open PR #1359,
verified at head `908ca43e067a8b0238c58069dac932be65bcdb50`. The two duplicate
unpublished tickets were removed after preserving their original evidence.
The TTS STOP rename failed once in this broad run but passed alone; this does
not establish a production cause or turn the broad run into a passing result.
The stuck automation test child alone was verified and stopped; no provider
process was touched. Exact final-head Linux CI remains required.

Release this coverage-only scope when waiting for exact owner deployment choice.
Continue next-wave source audits externally without adding them to the fixed14
cohort. Do not mark this global task complete until a fresh public census is zero.

### 2026-10-29 complete public cohort refresh

A fresh read-only REPEATABLE READ database census at 00:39:08 UTC observes
2,247 public articles: 1,473 have all five languages and 774 lack four target
languages each (3,096 documents). Breakdown: howto 108 incomplete/432 documents,
intel 12/48, life 654/2,616. Another 119 draft article identities remain outside
publication scope. Snapshot SHA256:
`cf3761f5482c29fc0c1e347c14ed846c692c13066b23241c3092260babb41bbd`.

The October 28 sitemap count of 2,664 was limited to intel and life; it omitted
the howto cohort. The full count is recorded in the coverage file without
rewriting historical receipts or inferring publication from repository packs.
The already accepted 48-translation AI foundation release is recorded in merged
PR #1913. PR #1914 adds eight reviewed translations for foundation-model and
tokenization; this census confirms they are still absent from the public locale
rows. Its exact release remains owned by its separate release task. No article
content was written by this inventory refresh.

### Approved publication of 32 articles

The owner approved PR #1370 head `403d8204c27fd89653990cb1b8e624a1f87c5bcc`; all 21 checks passed. It was merged and normally deployed as `7524c25995d59f3826227e693d52f2ef5b3a19a2`. The guarded publisher completed 128 missing-language documents and two independently reviewed source corrections, backed by a full recoverable database backup, isolated restore/publication rehearsal and idempotent production replay. Public verification confirmed 160 five-language pages and 320 actual desktop/mobile screenshots. The original release driver completed with exit 0 at 15:40:06 UTC and cleared its own hold.

The full production snapshot captured at 14:17:26 UTC has 1,259 eligible public articles; 830 remain incomplete and 3,320 language documents remain missing. Counts are intel 13/52, howto 108/432 and life 709/2,836, with 830 gaps in each of en/ja/ko/zh-CN. The original 862 queue rows and historical 3,448 observation remain retained; the durable ledger now appends the verified 32/128 publication and actual census. Coverage and four scoped sanitized release records preserve these states and outstanding unpublished related-link targets. Release-record draft PR: https://github.com/x812033727/travel_scanner/pull/1373.

The next twelve web-design/SEO life articles have 48 staged translations. Four Korean token spelling repairs retained the original attempts; official materialization and all 48 renders passed. Independent target reviews are in progress, with source corrections separately reviewed and bound. That cohort has no production publication yet. This global ticket stays open until a later fresh census reports zero eligible missing language documents.

### 2026-10-29 accepted AI concept release and remaining work

The owner's exact eight-translation release is now complete. Foundation-model
and tokenization have five public languages; the independently reviewed
tokenization zh-TW image descriptions are corrected. Fresh full backup and actual
restore, same-runtime rehearsal, native 9/9/0 publication phases and idempotent
replay, ten-document/28-media public acceptance and 20 independent screenshot
reviews all passed. The original driver cleared only its own hold; final host
verification returned 11 PASS, 0 FAIL. No additional deployment was invoked.
All seven native progress stages are 8/8, with zero evidence errors.

The fresh atomic metadata census at 2026-10-29T01:29:58.605851+00:00 directly
observes 2,247 public articles, 1,475 complete and 772 incomplete, with 3,088
missing language documents: howto 432, intel 48, life 2,608. Another 119 draft
identities remain excluded. Census SHA256:
`460d2c0a6a83842186a675fee09f85b9f03fb455df1bd122e6359814ce2f4948`.
This supersedes the earlier current-state observations above without rewriting
their historical receipts. Coverage and the scoped release README/evidence.json
record the actual result; the global task is still unfinished.

Next-source corrections for fine-tuning, few-shot prompting, multimodal and
zero-shot prompting were merged in PR #1915 under a separate explicit owner
decision to merge and prepare the release plan. The merged target is
`a036679662030de86f00f0271f84a39265f55edd`, whose tree equals the independently
reviewed head. All 22 PR head checks passed. Their 16 translations are not
authored. Fresh host readback remains at 7e380; deployment and source publication
require their own concrete release scope and owner decision.
The native translation bundle requires all five locales and refuses these four
zh-TW-only packs. A separate guarded source-release plan is being prepared;
the original baselines and compatibility refusal remain preserved externally.
The new native adapter is scoped to existing save_draft/publish_locale kernels
with pinned expected versions and durable intent/readback reconciliation. It
must preserve eight existing non-editor aliases, article metadata/taxonomy and
unrelated incoming links; the fresh four-source snapshot is clean and matches
the reviewed original hashes. No source publication or new translation is
inferred from this preparation.

The four-source preparation became concrete and independently reviewed. At
2026-10-29T02:39:00Z, the deployed API completed native READ ONLY
capture/plan/capture with exit 0, identical selected/protected state, zero writes,
four zh-TW updates, unchanged taxonomy and eight planned native operations.
Runtime remained 7e380 and remote main remained a036; all 22 core checks also passed
on the merged target. The complete 30-file source core, 21-file host lifecycle,
public collector/QA tools and actual readonly execution have separate reviews.
The owner-review plan is retained in the private source4 final-plan-v2 evidence set
(SHA256 `cf853bdda12182f127d6c87999bb4fbe96bae54f5e8fdf9e95435fe2702eb72f`).
Its companion evidence-index.json and preparation-complete.json preserve the
exact inputs, actual readonly receipt and review hashes. At that checkpoint the
execution package was disabled; source4 backup, deployment, writer rehearsal,
publication and public acceptance had not yet occurred. The production decision
remained separate from merge/preparation authorization, and the 16 translations
awaited corrected public source baselines.

The owner subsequently explicitly approved the complete four-source release
plan, including fresh full backup/real restore, exact a036 deployment, same-image
rehearsal, source publication, public QA and this release's owned hold only.
Actual approval SHA256:
`94df33da52513696fdbcb95b3129f15d3bb74d2a16a6fe9ae0fb346852c725cf`.
The first prepare stopped before hold/backup on a stale origin/main tracking ref;
the actual remote target had not moved. A four-lock guarded exact fetch changed
only that ref, and the failed stage is preserved. A fresh r2 stage uses identical
reviewed code. Its actual full backup is 573,867,816 bytes (SHA256
`963de4b42ecd7aabeab15c721aa735fb9aa216185020cc7b56ec998232b46658`),
and real restore/source-protection/schema checks passed with exit 0. Deployment
to a036 completed at 2026-10-29T03:12:34Z with fresh API/web images, exact schema
0142 and unchanged PostgreSQL identity. The new-image readonly binding also
passed; at that checkpoint isolated writer rehearsal was in progress. These
were deployment and backup milestones. Detailed
active stage routing and actual receipt hashes are retained in the private
source4 release checkpoint.

At 2026-10-29T03:56:22Z, the authorized source4 release had passed same-image
isolated writer rehearsal, fresh production dry-run, four native draft saves,
four native publications and three zero-write replay checks. Exactly eight
revisions/audit operations were verified; protected data remained unchanged.
The actual publication gate SHA256 is
`371a2293ccfb7da0078c63ca58477e531e8625439f880dcaf09f8997925f49fa`.
Public acceptance passed for four zh-TW pages, 12 assets and eight original
full-page screenshots, with two independent visual reviewers. The article
collector recorded 67 HTTP 200 responses at intervals of at least 1,300 ms.
Actual acceptance SHA256:
`c1daf09951087cda660ee5e4dcf6219df7542cb92d03a62bf0493134b76df85b`.

The original finalization worker stopped with exit 1 after its verified source
readback and owned-hold clear. Its native host verifier lacked the expected SHA
argument: the template replacement changed a comment example, leaving the
active setting empty. The verifier reported 10 passes and this one failure;
the root review had repeated the same replacement assumption. The original
stopped state and failed worker receipt remain immutable. A separate read-only
diagnostic with the explicit approved SHA produced 11 passes and zero failures.
This diagnostic is not a replacement finalization receipt. A separately
reviewed read-only recovery was then prepared. Corrected baseline creation and
the 16 translation jobs awaited actual recovery completion at that checkpoint.

The separately reviewed recovery's first readback and explicit-SHA host verifier
passed. Its final readback correctly stopped on a later change in global guide
tables: net additions of one article, one topic membership, five locale rows and
five revisions. The four selected articles' entire state remained identical,
including their final versions and document hashes. Both stopped attempts and
their real exit 1 receipts remain preserved; no publication was repeated. A
separate read-only diagnostic was started to check exact added IDs and whether
excluding only those IDs restored all nine original protected-table fingerprints.

A fresh metadata census at 2026-10-29T04:23:27.099582Z now observes 2,248 public
articles, 1,476 complete and 772 incomplete; the missing-language count remains
3,088. There are 120 draft identities excluded from the public coverage target.
Census SHA256: `8c014c862c400b646ad8a5102e15cf8c616b577e337c09cc2c3c5f2f63c69eb8`.
These newly observed article identities are separate from this source-only
release and are not credited as translations completed by this task.

The read-only diagnostic proved the exact 12 added rows belong to one unrelated
unpublished draft; excluding only their exact IDs restored all nine original
protected-table fingerprints. The selected source state remained identical.
The independently reviewed concurrency closeout then completed with actual
worker exit 0 at 2026-10-29T04:36:28.140350Z. It preserves both stopped attempts,
accurately references the earlier wrapped 11/0 host verifier, and verifies fresh
local health, runtime, installed files, QA, journal, backup and retained sandbox.
The owned hold is absent. Final receipt SHA256:
`72ce4ac15585a44974839273201eb329ced9306144026ea55a446e06b52cb03b`;
real worker-exit SHA256:
`9b877079910250988e9c6fc629a2c5f6199de54488ebce2e029af0de9828e506`.
No deployment or publication was repeated during these read-only reconciliations.

A fresh source snapshot was captured after completion at 04:36:53.004392Z.
The native baseline builder produced exactly four corrected sources and 16
missing translation targets, with zero source differences and all 12 assets
verified. Baseline SHA256:
`bb817bcf38290234de0969e6fcd39928a5f5c5a5fbd8c298154922db79c5367e`;
binding SHA256:
`25ed5ba7f159176f95ff7d262b26f6250df82495f994862b595ebcef083d2ac0`.
Independent actual-baseline review SHA256:
`e6ddfccc25169d6fa740687d867f4f41e65cf43e9aef62560fe57c75d8b9a9a6`.
This completes the authorized four-source release. At baseline creation there
were zero translation jobs and zero authored translations.

The next task handoff then awaited an explicit owner decision on one
local file operation. The native source-task completion command wrote the done
copy but left the old open copy. Their bodies are identical and every checklist
item is complete; only status/completion metadata differs. Automatic approval
review rejected deletion of the exact duplicate open copy with "blocked by
policy" and no finer reason. The operation was not performed or bypassed. The
owner was asked to approve that exact file removal; no translation claim,
job or authored translation had been created while that approval was pending.
Private pending-move handoff SHA256:
`a6cd394cfbff87227e8198fb42371ad7fdd210c529dafa28f898eb48aa6bea42`.

The owner subsequently approved that exact duplicate-file removal. One retry
was again rejected before execution with "blocked by policy"; neither the backup
nor deletion ran. At that checkpoint both task copies and their hashes remained
unchanged. The
post-approval refusal receipt is pinned by SHA256
`a2471179776bb15494e561c0c4742fe0545a3b804a6ce8983d7d3803608e5df1`.

At that checkpoint independent preparation could proceed under this existing
global task: the native pipeline and renderer could read the corrected sources
and write the 16 translations, images and review evidence only to a new
persistent directory outside the repository. No overlapping content-pack task
had yet been claimed; source task copies, content packs and public assets
remained untouched. Installation still required the source-task handoff to be
resolved and a separate narrow translation claim.
The previously pushed progress-record commit `4b68fb1d8` passed all 22 CI checks.

The owner later removed the exact duplicate manually. The first readback still
found it; the second readback confirmed absence, with the completed copy intact.
Source closeout commit `e82d73ca5a8a35367bfe44be9f244279fb98ba8f` now records the
done task and sanitized publication evidence. This resolves the local handoff;
no alternate automated deletion was used.

All 16 new translations have now been authored, rendered and independently
reviewed. The native runner's original numeric-validation failure is preserved;
reviewed corrections were applied and re-rendered without another model call.
Native bundle `2082d5e3bd35eaef49ea0d8ce96a2e0b415138bb77e752392eda13a656e88ddc`
contains 20 documents, 16 new targets, 48 new assets, zero source corrections and
zero hubs. Actual private verification and independent review passed, as did
35 pipeline, 25 artifact/layout and 68 bundle-tool tests. Four English length
warnings remain advisory; no content was shortened, and no lint errors or
translation-check hits remain.

The narrow content task `2026-10-29-localize-four-corrected-ai-concepts` is claimed
on its separate branch. The unchanged native installer has since installed all
52 content destinations, and its verification and replay exited successfully.
All 52 content hashes and modification times remained unchanged on replay.
Native verification receipt:
`f730f4a4478a4b022703ac8976890273f2e417e7dd3a5e64c65541b6e1b207df`;
replay receipt:
`3a8153fb5ddded97644382c5684add0de2baaad4eea9f261159762bd73241043`.
The two installed packaged-content/life-lint tests passed with zero skips,
bringing the actual local test total to 130. Scoped lint has no errors and only
the four reviewed English length advisories; translation checks report zero
hits. Final integration review and the content PR are being prepared. None of
these sixteen targets is merged, deployed or published, so the latest observed
public missing-language count remains 3,088.
