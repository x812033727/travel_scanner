---
id: 2026-09-21-localize-seoul-airport-tmoney-batch009
title: Localize Seoul airport and T-money guides in five languages
status: done
priority: P1
area: docs
owner: codex-batch009-seoul
claimed_at: 2026-09-21T20:04:19Z
created_at: 2026-09-21T20:03:45Z
completed_at: 2026-09-22T07:15:28Z
branch: codex/article-localization-batch-009-seoul
depends_on: []
scope:
  - apps/api/app/guides/content/incheon-airport-to-seoul.json
  - apps/api/app/guides/content/seoul-subway-t-money-guide.json
  - apps/web/public/guides/incheon-airport-to-seoul
  - apps/web/public/guides/seoul-subway-t-money-guide
---

# Localize Seoul airport and T-money guides in five languages

## Why

These two published Seoul transport guides have only zh-TW. Their linked airport,
subway, T-money and Climate Card explanations need en, ja, ko and zh-CN documents
and translated diagrams without exposing links to unpublished locale targets.

## Definition of done

- [x] Both articles have reviewed five-language documents and localized text diagrams.
- [x] Published zh-TW edits, source facts, author credits and locale-aware links are preserved.
- [x] Pack/image checks and an independent review pass before the content PR.

## Steps

- [x] Pin production published zh-TW v6 and current repository SHA.
- [x] Review live/repository differences and Seoul City 2026 Climate Card notice.
- [x] Translate and render 8 missing locale documents and 8 SVG variants.
- [x] Review exact fields, images, sources, links and source correction.
- [x] Run relevant pack/content checks, open PR after preceding batches.

## How to verify

Run scoped pack lint for both slugs, GuideDocument and image checks, translation
field parity/numeric/URL/credit checks, SVG desktop/mobile render inspection,
`npm run check:tasks`, and the applicable API/content tests. Verify source and
document hashes against the pinned production snapshot before publication.

## Notes

- Production read-only inventory on 2026-09-21: both article identities v2 active,
  each only zh-TW document v6 published. A repeatable-read, read-only DB query
  normalized the exact published revisions with `GuideDocument`; canonical SHA-256
  values are `ccddadb8649e6a5fc71b29fa2627bedff3499ba3f22b58ea2248472470c73011`
  and `c7fe9b0643013d7d5bfb5a4db56f40d1382a811bed3e2d42c515b055e1ee23c1`.
  The initial public API payload included transport-only `version`, `published_at`
  and `modified_at` fields and gave incorrect document hashes. Those v1 attempts
  were quarantined; the corrected v2 baseline rebinds all translation jobs.
- Current branch began at remote main `51e716da6c789e7eeba4c36ad1780095e89b4e48`.
  The c5d9 worktree packs are older; do not use them as translation source.
- Merged PR #565 (commit `d11178863d1a2a35ddfff17be65bcc2a63514194`)
  changed answer-first descriptions in both repository packs. Its task
  `2026-09-14-answer-first-howto-descriptions` remains stale `review` despite the
  merge, so this task was claimed with `--force` after verifying no active writer;
  the old task file is untouched.
- The original live document and reconciled source, with the existing PR #565
  descriptions plus a bounded Climate Card date correction, are pinned under
  `C:\Users\x8120\.codex\article-localization-release\batch009-seoul`.
  Seoul City's official notice says prepaid 30-day top-ups ended Aug 31, final
  prepaid use Sep 29, postpaid use Sep 30, while short passes continue.
- Current main `apps/web/lib/foods.ts` accepts `?city=seoul` as an alias and has
  tests, superseding an older open task that called the filter ignored. Preserve
  that query while localizing only its locale prefix. Internal article links
  must respect each target locale's actual publication state.
- Historical rejected staging is `C:\Users\x8120\.codex\article-localization-release\batch009-seoul\work-v4`;
  `baseline-reconciled-v4.json` SHA-256 is
  `cf8aab4bed5840282497bbb22673a787beb0872278726dab7c51373d4515d049`.
  Earlier v1 transport-payload jobs, v2 first translations, and v3 intermediate
  SVG correction are retained as history but must not be installed. v4 had 8/8
  canonical `GuideDocument` materializations and 8/8 SVG renderer layout passes,
  but an independent review rejected all eight jobs with ten findings.
- The original zh-TW Incheon SVG itself clipped the terminal badge and right
  labels and drew route lines through long labels. Only eight `<text>` nodes
  changed: the T1/T2 badge, Seoul Station name and time, Myeongdong/Gangnam bus
  times, and the three route labels. The AREX Express text also moved from
  `x=620,y=440` to `x=620,y=410`; paths, shapes and 1600×900 size stayed fixed.
  Original asset SHA-256 `a933d1d5b0a619cce0842eb82bfe86cf065ae9faf49840191e0f444a50c5ebaa`;
  final `a97d6383b93bad6656ee0a95bbcaa40f8943bc53d55efbad97bd61226dd9dff8`.
  The original and final source previews plus the exact per-field migration
  receipt are outside the repository; `source-svg-label-migration-v4.json`
  SHA-256 is `6e7890d58e2fd2ef4ab170bfefbd56890d61d9715e82434c84db0677ff2085f7`.
- Six existing rasters were visually inspected: train, bus, platform, ticket
  machines and gates are site photographs with incidental real-world signage,
  not authored text overlays. Preserve their author/license and bytes. All
  four Incheon and four Seoul language previews were inspected for truncation,
  overlap, missing glyphs, fare numbers and the source diagram correction.
  The v4 hash-bound review rejected 0/8 approvals; none of its flags are reused
  for v5. New independent editorial/image review remains outstanding before
  setting acceptance flags or assembling a bundle.
- Independent-review candidate packet SHA-256
  `e71fbcadc614aa6aa36536d5824fd53ce5419b084d1e5094ab53885a4e13818e`
  is stored outside the repository as `review-candidate-v4.json`; its flags
  deliberately remain pending. The exact live-to-candidate prose diff is in
  `source-reconciliation-v2.json` beside it. Pipeline tests 32/32, artifact
  binding tests 14/14, SVG layout tests 3/3, and `npm run check:tasks` passed;
  the task checker only reported existing stale/overlapping tasks, including
  the already-merged #565 task described above. Assembly, installation and
  the PR wait for the independent reviewer and the preceding batch releases.

- v5 source correction addresses all ten independent review findings (S009-01
  through S009-07 and I009-01 through I009-03). Seoul City's 2026-08-31
  announcement additionally confirms prepaid Climate Card 30-day top-ups ended
  and postpaid passes end 2026-09-30; short-term passes continue. The current
  guide compares existing-card and newly purchased-card break-even totals,
  excludes free transfers from paid-ride counts, names covered outer-city
  station ranges, separates the cash-only Climate Pass from Climate Card
  short-term passes, and explains Seoul-to-airport exit-only use of AREX
  all-stop trains. Source text corrections are bound in
  `source-reconciliation-v5.json` SHA-256
  `ae433aad6502fc91967722c401a1a87a39bc169091fa552bdafd23db18dedf45`.
- v5 uses `baseline-reconciled-v5.json` SHA-256
  `002fe9f6b1cdd5e8c198e59fcb107bfa596723d7fd632b75d9bed51760a5006c`
  and staged `work-v5`. Corrected Seoul source document SHA-256 is
  `adeb04a9a0d3a4f72659a1b540ef9750a915432314bb415c12ba440611e49c44`;
  its SVG SHA-256 is `87864eaba7663f064914bafecc36f56f58e05170446f9f66e57bd2bb63ea0dad`.
  Incheon source document and source SVG remain bound to their prior verified
  hashes; its four target translations changed only at the reviewed typo, taxi
  category, and duplicate Korean-label pointers. The source Seoul SVG Q3
  polygon became a rounded selection box so its secondary line no longer
  touches a diagonal edge; target Q1/Q2 labels and the Incheon English bus
  label were shortened after full-size visual inspection.
- The new unapproved reviewer packet is `review-candidate-v5.json` SHA-256
  `ac7d1c20c8519e4ed3518044bc2d86fa92478000b02dd68e81ee5ab53f65d33f`;
  the exact v4-to-v5 document/SVG/hash diff is `v4-to-v5-diff.json` SHA-256
  `1701f402b8b7831cfd5e5c458287a631f2736f6f1fa0a52374ed40c6c1ca02d0`.
  `qa-v5.json` SHA-256 `bca053aae53c46602b8c242b626f5ba72a0823e173cd3fddf2432585b2bb592c`
  records 8/8 schema/field/render passes, 10 full-size source/target image
  inspections and 10 downscaled 390px previews. Pipeline 32/32 and artifact/
  layout 17/17 tests passed; task check exited 0 with existing stale warnings.
  Scoped Incheon pack lint has only the prior no-summary warning. Seoul pack
  lint currently reports `diagram_number_not_in_text: 13` because its corrected
  source SVG is in this worktree while the repository zh-TW pack still contains
  the earlier live v6 text. Candidate source text carries 13; rerun pack lint
  after independent approval and pack assembly. No candidate pack, PR, or
  production write was made in this correction round.

- The second independent review rejected v5 0/8. Its immutable receipt is
  `C:\Users\x8120\.codex\article-localization-release\batch009-seoul\review-v5.json`,
  SHA-256 `e564ee481dfd67531cff5f17ed836921da793a57f31dbf29d494cb9c871e37af`.
  Eight findings cover AREX Express versus all-stop last trains; N6002 airport
  direction, T1/T2 times, adult/child fare, T2 bay and ticket issuance; all
  night-bus travel times' terminal basis; Seoul City's conflicting descriptions
  of short-term Climate Card suburban coverage; and the overseas-card payment
  fee excluded from face-value break-even counts. Neither prior rejection was
  promoted to approval.
- v6 corrects 14 zh-TW source-document fields plus the two source SVGs, and
  rebuilds all eight target `GuideDocument` and SVG artifacts from that source.
  AREX all-stop services after 23:00 are distinguished by terminal and actual
  destination without asserting one universal last train. N6002 T1 citybound
  last departure is 04:40, adult/child fare 17,000/10,000 won, T2 boarding bay
  B1 30; 03:20 belongs to the reverse direction. The four bus travel times and
  the Incheon diagram now label their T1/T2 basis. Airport-origin ticketing is
  per route/operator. Seoul short-term-pass suburban coverage remains explicitly
  unresolved because official pages conflict; passengers are directed to check
  the current product guidance and each station. Break-even counts are labeled
  as face-value examples excluding the average 3.7% overseas-card fee and ask
  readers to recompute from the actual total charge, counting a new card only
  when purchased. Source URL/check dates and live v6 editorial baseline remain
  bound; six existing scene photos and their author/license bytes are untouched.
- Final unapproved v6 staging is `work-v6-final2`; `baseline-reconciled-v6.json`
  SHA-256 `4a3d4b5f0128ec7ef1b3c0fcedf217836d3c92b67a30771d83485dc300f9c9b4`,
  `source-reconciliation-v6.json` SHA-256
  `fcd0e4761b4525be0f15ec9ac7dd412aed447861638882d51b0903377eef00b6`.
  Source Incheon/Seoul SVG SHA-256 values are
  `386681e6fa613f297b48cc085d2e91038898b29d6e7c5d281f41689949f510f9`
  and `aa9195d4634e7389cce2dd6d5086f73320042fbe5d04d68cc40604430d8c43ad`.
  The new `review-candidate-v6.json` SHA-256 is
  `f7466c2ab64779d72e6334a472f7d60e53c20481fc0d4583ce009ce44329e20b`;
  `v5-to-v6-diff.json` SHA-256 is
  `7db6dcf4fc52be67dc9c2e0710076408091e6f6032966f5267fd9098dc80dad1`;
  `qa-v6.json` SHA-256 is
  `76085ee6acf405245e878898be5c9c602a40b87afad3b568154360e6218d842b`.
  All 8 target docs passed schema/field/URL/credit checks, all 8 SVGs passed
  automated layout; 2 source and 8 target images were examined at full size
  plus 390px previews. Pipeline tests 32/32, artifact/layout tests 17/17,
  `git diff --check`, and task check passed (existing stale-task warnings).
  Repository pack lint remains pending because the corrected source documents
  have deliberately not yet been assembled into the older repository packs.
  No PR, deployment, import, or production write was done. Fresh independent
  editorial/visual review must approve v6 before any pack assembly.

- The third independent review rejected v6 0/8. Immutable `review-v6.json`
  SHA-256 is `8a13a668736e454bfaaa6945173afd325587b3576579a38e045aed0af2639d7f`.
  Its 18 previously identified issues were resolved; three new issues were
  Seoul Station City Airport Terminal's 18:50 new check-in cutoff despite its
  19:00 service end, distinct standard versus deluxe/large taxi night rates,
  and the qualified bus-to-bus group transfer discount when one card pays
  multiple riders (which does not carry over to metropolitan rail).
- v7 corrects exactly four zh-TW source text fields across the two documents
  and the matching fields in all eight target documents. It updates the
  verification dates for the three official sources to 2026-09-22. The source
  documents have canonical SHA-256 `0101b5451e54207a029880d2ab1d86999b6cb4e6aff61f14bee915cf0c305120`
  (Incheon) and `39f86e1dee5e1e58206faadf953520ec5dad6ff010cb69c0987794c55c8387cb`
  (Seoul). The source SVGs, eight translated SVGs and eight previews are
  byte-identical to v6 because none depicts those changed claims.
- The unapproved v7 baseline is `baseline-reconciled-v7.json` SHA-256
  `20ff436f9fc789b645ffef7e3c59c4760d83b720fbac644c63b497c858eeb540`;
  source reconciliation SHA-256 is
  `ab234c9484f96c0ee4c822c164426bd9bb06366ececa6faa48cabf77e433abfc`.
  The exact candidate `review-candidate-v7.json` SHA-256 is
  `641001e068a64f54e860c0732bd2b572055b5b5c68a8c23e1cdd9ac0a75baf8f`;
  `v6-to-v7-diff.json` SHA-256 is
  `55db0cc61fe8432b9b23671062dbed10bbf1593418fc17df482e951538254576`.
  `qa-v7.json` SHA-256 is
  `dcc5ae6689f1ff0b60a88977d6b566827da45f0bc023178d7e8a6543036db791`.
  `work-v7` contains eight bound, schema-valid, fully rendered target documents;
  each passes numeric/URL/code field protection, source URL/date/credit and
  same-locale link checks. The eight visual previews were re-inspected at 390px;
  prior full-size inspection carries forward on identical bytes. Pipeline tests
  32/32, renderer/artifact tests 17/17, `git diff --check`, and task check pass
  (only pre-existing stale/overlapping task warnings). Scoped pack lint and
  pack assembly await independent v7 approval. No PR or production write.

- v7 and v8 independent reviews remained rejected; v9 source repairs used official
  AREX, International Taxi and Seoul transfer-discount evidence checked on
  2026-09-22. The v9 independent content review approved all eight translations
  and SVGs: `review-v9.json` SHA-256
  `ff0d31a8b159543cfc5223b122e6f5bb03e76d71e06cac58a8b54f9d2a12f0a4`.
  Assembly lint caught one 14px English diagram label. v10 changed only
  `/assets/0/text/19` to a shorter equivalent with 15px type; canonical English
  document and the other seven jobs remain identical. Independent v10 approval
  is `review-v10.json` SHA-256
  `b85cdec54fdc43d6d98f03dadbf73829f107c687b473f35d469546b61372869b`,
  bound to `review-candidate-v10.json` SHA-256
  `2300504675bcd8326ae4dba62a87e97bc912efc1a0a83a25283e2c1e16abe3f5`.
- v10 repository assembly dry-run and apply receipts are stored outside the
  repository (`repository-assembly-v10-dry-run.json` SHA-256
  `7a729e84ccd8801fcd07131a757766806ff3c0fb4016e14ec7bdaac38ad49168`,
  `repository-assembly-v10.json` SHA-256
  `1ff2c895a818dde2a318b7ec4ebe1cbce685a7e3326579c9e8a16be08b674871`).
  They pin two five-language packs, two corrected source diagrams, and eight
  localized diagrams. Both scoped pack lints passed with only non-blocking
  summary/length warnings. Import/production dry-run and publication remain
  outstanding; source versions and content hashes must be refreshed first.
- Local validation: article-pack/content-links tests 12 passed, 5 PostgreSQL
  skips; bundle assembler/publisher tests 53 passed, 42 integration skips with
  the documented `asyncio_mode=auto` setting and integration disabled. The
  first test invocation without this required setting errored at async fixture
  setup and is not counted as a pass. Task check passed with pre-existing stale
  and overlapping task warnings.

### 2026-09-22 completed release and task handoff

PR #642 is merged. Both guides were imported and published in all five locales at
production checkout `7195fef5a6bfc4fdff50a1e9f8ff06bcc710bd47`. Batch009 manifest
`be19510c836d9ebe3d95c8fc4b2723d376dfd0a9071fcdec6af5741d33b43cdd` completed
10 draft and 10 publish operations, no pending intent, and an unchanged rerun.
Five desktop plus five mobile cases per article passed body, images, canonical,
hreflang and locale-link QA. Sitemap pagination terminated after 1000 + 820 rows
for the combined008/009 release, with all target URLs in XML. Fresh backup was
verified by pg_restore --list; health passed and the owned hold was cleared.

Immutable shared release receipt: `C:/Users/x8120/.codex/article-localization-release/batch008-009-release-receipt-20260922.md`,
SHA256 `96c8e7418ac40452e0fb6b498c0df09505f6ed926682f97ef4b22199b3f3cc33`. The earlier pending/rejected notes above are
historical evidence; the approved v10 and completed production release supersede
the pending status without erasing those findings. This closes this task only.
