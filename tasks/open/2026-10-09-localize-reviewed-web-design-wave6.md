---
id: 2026-10-09-localize-reviewed-web-design-wave6
title: Localize reviewed web design and reuse WordPress locales wave6
status: in-progress
priority: P1
area: docs
owner: codex-gpt6-root-wave6
claimed_at: 2026-10-09T13:06:48Z
created_at: 2026-10-09T13:01:47Z
completed_at:
branch: codex/article-source-audit-wave6-20261009
depends_on:
  - 2026-10-08-audit-next-web-design-locales-source
scope:
  - apps/api/app/guides/content/design-thinking-practice.json
  - apps/web/public/guides/design-thinking-practice
  - apps/api/app/guides/content/portfolio-case-study.json
  - apps/web/public/guides/portfolio-case-study
  - apps/api/app/guides/content/brand-identity-logo-brief.json
  - apps/web/public/guides/brand-identity-logo-brief
  - apps/api/app/guides/content/web-design-agency-brief.json
  - apps/web/public/guides/web-design-agency-brief
  - apps/api/app/guides/content/website-404-recovery.json
  - apps/web/public/guides/website-404-recovery
  - apps/api/app/guides/content/website-www-subdomains.json
  - apps/web/public/guides/website-www-subdomains
  - apps/api/app/guides/content/ai-design-prompt-workflow.json
  - apps/web/public/guides/ai-design-prompt-workflow
  - apps/api/app/guides/content/canva-design-workflow.json
  - apps/web/public/guides/canva-design-workflow
  - apps/api/app/guides/content/customer-journey-funnel.json
  - apps/web/public/guides/customer-journey-funnel
  - apps/api/app/guides/content/marketing-copywriting.json
  - apps/web/public/guides/marketing-copywriting
  - apps/api/app/guides/content/seo-domain-authority.json
  - apps/web/public/guides/seo-domain-authority
  - apps/api/app/guides/content/seo-trust-sensitive-topics.json
  - apps/web/public/guides/seo-trust-sensitive-topics
  - apps/api/app/guides/content/paid-vs-organic-marketing.json
  - apps/web/public/guides/paid-vs-organic-marketing
  - apps/api/app/guides/content/wordpress-blog-build.json
  - apps/web/public/guides/wordpress-blog-build
  - apps/api/app/guides/content/wordpress-comment-spam.json
  - apps/web/public/guides/wordpress-comment-spam
  - apps/api/app/guides/content/wordpress-performance-plugins.json
  - apps/web/public/guides/wordpress-performance-plugins
  - apps/api/app/guides/content/wordpress-reset-safely.json
  - apps/web/public/guides/wordpress-reset-safely
  - docs/article-localization/reviews/wave6-web-design-20261009
  - tasks/open/2026-10-09-release-localized-web-design-wave6.md
  - tasks/open/2026-10-09-windows-video-test-path-assertions.md
  - tasks/open/2026-10-09-windows-speech-journal-rename-failures.md
---

# Localize reviewed web design and reuse WordPress locales wave6

## Why

Seventeen active published life articles have 68 unpublished target languages.
Twelve need 48 newly authored documents; five already contain twenty target
documents that require fresh independent review rather than duplicate translation.
The completed source audit identifies 15 ordinary-word AI-glossary mislinks across
13 published sources. Eight current packs already contain ten desired removals;
five packs need one further removal each, preserving visible words and source dates.

## Definition of done

- [x] Apply only the exact five new source-pack removals and preserve all original inputs.
- [x] Independently review actual final sources and verify 13 genuine source-correction
      receipts against the original live database/publication guards.
- [x] Admit only reviewed desired source fields to a separately pinned baseline.
- [x] Independently review and repair the twenty existing target documents and images.
- [x] Author, materialize, render and independently review the 48 missing documents.
- [ ] Assemble/install the exact 17-article bundle, pass relevant content/tool checks,
      and open a reviewed content PR with green CI.
- [x] Record sanitized source/translation evidence and file a separate release task.

## Steps

- [x] Complete source audit and claim exact pack/media/evidence scopes.
- [x] Preserve originals, apply exact proposed changes, and obtain distinct final review.
- [x] Prepare new bound jobs only after source admission; keep old jobs unchanged.
- [x] Review existing work and author only genuine missing-language fields.
- [x] Apply independent findings as a third party, rerender and bind final review hashes.
- [ ] Assemble, validate, install and submit the complete content for review.

## How to verify

Use the unchanged official source_correction.verify_review, pipeline artifact
verification, assemble_bundle.py and install_bundle.py. Run selected pack lint,
content/link tests, translation checks and task validation; run affected pipeline
checks and require green CI on the concrete content PR. No publication or merge
authorization is inferred from previous 13-article approval or this authoring claim.

## Notes

Fresh original snapshot SHA: `ef3ef1cfeca66169cdb6f77499a2b3c4eec2230a805a46c08ab619203304c209`.
Independent source audit SHA: `2d128ca5a3dee8a403751e76d5f03cba41dcb839688d9bc51349fc1491245b0b`.
Exact proposal SHA: `ca957c510635e2c38d3b9e24996bb1a83b54b2f9dc3344e5d34adf012571735d`.
Independent proposal review SHA: `e759638b4601759e88a30f355b9f136c7f8f11061de2a792d14635feec3514f5`.

The independent source auditor proposes; a separate operator applies; a distinct
source reviewer reads the actual final source files. No future SOURCE PASS is implied.
Current primary reading found no concrete defect in the paid article's descriptive
SEO citation label or exact Google Ads hl=zh-Hant URL, so no metadata/date repair
is invented. Its old unowned paired task retains historical questions until this
narrow evidence and the eventual publication outcome can be reconciled there.
All private raw inputs, jobs and receipts stay outside Git. Previous 57 completed
articles, their media, production state and completion ledger are outside this scope.

## Actual source application checkpoint

Root's first local pre-write check exited 1 because proposal document references
were mistaken for documents; it created no application output and changed no packs.
The original script and execution logs remain preserved. A separately frozen V2
loads and verifies referenced file bytes before applying the unchanged full-source
guards. The one explicit corrected attempt exited 0 at 2026-10-09T13:12:11Z.
Only five packs changed, removing one link each. The other eight proposed source
corrections were already present and required no pack write. All 111 media files
and twenty existing target documents are unchanged; the completion ledger still
has SHA `3df618ed6f2c6142eddf50d31d0b57fdf4af95088b0c5e4aa9b72d8526f5f7da`.
Actual application receipt SHA:
`5319e0aa815df08386c7350fc7a752ecbc8dab1ea20505443ed4578c7cbb65d5`.
Original official-builder baseline SHA:
`c352dd802bb96795d706ab876ff6b05adce6f4ff3b49629f3f102b5103f95ea0`.
The later independent final SOURCE17 review passed with no blocking findings,
SHA `a6eb41d05f6e729918de26539aeb07108ae270c0a4f6cc2d8c72542e43e68c8c`.
All thirteen official exact-schema receipts verified against the untouched original
database guards. Only the two actually referenced source assets per article enter
official correction receipts; all 39 original source files and 111 total media files
have separate historical byte guards. The reviewer's original local seal refusal
and corrected successful seal remain preserved.

Initial baseline admission refused a frozen-copy/live-path mismatch before creating
jobs. A separately reviewed exact V2 retains all byte guards and binds the actual
frozen review copy to its recorded live input hash. Actual admission and prepare
exited 0 at 2026-10-09T13:32:36Z; baseline SHA
`5100ea5f07981a61c5d9072d966f96097da5d68a83f04de46b155679fb267bf0`.
Only twelve sources / 48 new full-language jobs were prepared. Existing twenty
target jobs remain deferred until their real corrected content is independently
approved and the later baseline rebind completes.

The design-thinking-practice/en pilot translated on one actual attempt and rendered
with zero automatic layout issues. Its final artifact manifest is
`3da582314b75d8260cd4896d2ab186aeeca7cfb9d169516cb0ead6056fc48fa6`;
independent target review is pending. The remaining translation run started with
three workers and zero retries. Only the existing ChatGPT-login CLI route is used.

Existing-target review read all twenty documents and forty original native images.
Root applied its exact 65 leaf / 104 phrase corrections in six documents across five
packs. Actual application receipt SHA
`8461928918c69bc570998a38c7a36dcda44309f061b96282553483bfeb7dd18e`.
Fourteen targets, all source documents/dates and all 111 media files remain unchanged.
An earlier local empty-parent-pointer refusal created no content writes and remains
preserved separately. Actual post-repair target approval and job binding are pending.


## Actual translation and reviewed-existing admission checkpoint

The existing twenty-document post-repair review passed at 2026-10-09T14:18:11Z,
SHA `5a6079e78fe29344be7842630f8237c9e79c391e892ce1b60133149a7581b351`.
Six complete corrected documents were reread; fourteen unchanged documents were
rebound to the same reviewer's genuine complete prior reading and forty native
image views. The correction proposer and final reviewer are the same independent
reader; the applicator is distinct. No extra actor independence is invented.

The 47-job continuation finished with actual exit 1: 42 new outputs translated,
the already finished pilot was skipped, and five full returned outputs were
rejected by protected numeric or URL checks. All 48 original one-shot provider
attempts and the actual failed exit remain retained. Root repaired exactly fourteen
field leaves in those five returned outputs without retrying the provider. All
48 complete new documents subsequently materialized and rendered successfully.
Automatic artifact checks are distinct from the still ongoing genuine manual
whole-text, native-image and glyph reviews.

The existing-target baseline admission's first actual execution passed preflight
but failed during backup on four Windows paths over 260 characters, before any
baseline or prepare call. Original failure and partial backup remain preserved.
The explicitly checked recovery used the unchanged reviewed V2 helper and a
shorter fresh destination. It completed actual exit 0 at 2026-10-09T14:51:30Z:
only six desired existing target documents and five corresponding pack hashes
were admitted; all source, original database, dates, media and unselected fields
were preserved. All original 48 job trees, including eleven installed reviews,
were byte-preserved, and twenty review-only jobs were then actually prepared.
Admitted baseline V2 SHA:
`3b908b57bfaf425bae75f3ffa31137a0c5d4fc26d284ed5fce17e9d8db92c300`.
Actual admission / prepare receipt SHA:
`9301215bf1e4a63e57bbacdd3bee46c014b48abeb3a09d68c9216c8c61809301`.

Source-fidelity and native-image findings are handled only through exact
independent proposals, a distinct applicator, preserved originals and fresh
artifact validation. This authoring checkpoint grants no publication, merge,
deployment or completion-ledger authority for these seventeen articles.

## Actual final authoring and local installation checkpoint

All earlier pending source, translation and artifact-review steps are now complete.
All 68 genuine target reviews were copied without authoring a new editorial PASS,
and the unchanged official validators passed with all original jobs byte-preserved.
Actual all68 review-pin map SHA:
`6b5540a208617790d35310b0fdfbcbbf8e469477667f0737d980a2028591bc42`.

The official assembler and bundle verifier both exited 0: 17 articles, 68 targets,
13 source corrections, 81 selected documents, 85 full-pack documents and 210 assets.
Actual assembly receipt SHA:
`11b37a08b5308cc58eecfde2b6299444fdb43b2af2eed345883945d6fd78a205`.
Independent complete artifact-integrity review found zero blocking findings,
SHA `5f1189be2af3f8a57d975c93f0140a18c72f5d60da153254e304a54a94a6ed8f`.

The actual installation-before inventory covers 1,204 packs and 6,606 public files,
SHA `7d61fc21fe1edbbde1c642c34a2559e69f4a8db5b206cbc2335eda824ebb37a2`.
It begins after the bounded source/existing-target edits, not before all authoring.
The separate exact auxiliary claim covers the private stage/journal/seventeen
receipts and lock. Official local install and identical-argv replay both exited 0;
all packs/assets, journal/backups and seventeen receipts were byte-identical.
Actual install/replay receipt SHA:
`4611e68349a1d5922c45995b72de2daca91692f9879591b85777d233607492b8`.
Original 111 media, full68 jobs, previous installation state and program ledger
were preserved. This performed no provider, host or publication calls.

Selected seventeen-pack lint exited 0 with 85 source-shaped no-summary warnings
and seventeen length warnings retained; the full translations were not shortened.
Translation character checks reported zero findings. Content/ingest/link tests:
76 passed, twelve skipped (eleven isolated PostgreSQL; one unavailable Chromium),
actual exit 0. Pipeline 35, artifact integrity 14 and release-safety 191 tests passed;
release-safety also skipped eighty tests. Task validation exited 0.
The complete Windows tools run exited 1, including an explicitly stopped own
stalled automation-test child. Existing import/lease/ffmpeg tasks and the two
new narrow Windows follow-up tickets retain the actual failures; no broad tools
PASS or successful POSIX run is claimed. WSL VM startup also failed locally.

Complete installation preservation audit has now passed. Final committed payload
evidence, concrete draft PR and its current green CI remain pending. The generated release
task stays open/unclaimed and depends on this authoring task. Only its exact task
file and the two generated follow-up files were added to this author's scope after
the installer completed; their implementation scopes are not claimed here.

## Actual complete independent local preservation checkpoint

The explicitly executed V6.1 readonly auditor completed with actual exit 0:
54,582 checks passed with no blocking findings. All 1,204 content packs and
6,750 current public files match the exact original preinstallation inventory
plus this bundle's selected changes and 144 new assets. All unselected content,
111 original cohort media, the complete 68 job trees, prior installation state
and the 57-article / 228-target completion ledger remain preserved.

The original V5 raw-root-key refusal (actual exit 1) and its logs remain sealed.
V6.1 explicitly records the official serializer's 51 absent-before empty default
additions: aliases={}, news_date=null and related=[] in each seventeen packs.
All seventeen topics lists use exact admitted baseline order with the same
original multisets. Every other existing raw root metadata key, value and JSON
type, including all date values, remains unchanged. No broad normalization
exception or automatic retry was used.

Actual complete audit report SHA:
`cac5100aca9da7f7419c09642ca1633af43cf3496c4212af0a918c0ad9ff79be`.
Actual Root execution receipt SHA:
`afd010e2b6e331a1d1ddeffea303676b6c9ed7e60e9a52c7edba87a3f9922a3a`.
Independent report/execution binding review SHA:
`59a849f433797521cb869de00128d31e496c35bc3cc4206895f86924ad7a89b6`.
This local checkpoint performs no provider, host, publication or ledger write.
