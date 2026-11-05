---
id: 2026-10-29-release-localized-four-corrected-ai-concepts
title: Release localized four corrected AI concepts
status: done
priority: P1
area: docs
owner: codex-next16-release-preparation
claimed_at: 2026-10-29T07:19:07Z
created_at: 2026-10-29T06:24:49Z
completed_at: 2026-10-29T11:21:17Z
branch: codex/release-ai-concepts-next16-20261029
depends_on:
  - 2026-10-29-localize-four-corrected-ai-concepts
scope:
  - docs/article-localization/releases/2026-10-29-ai-concepts-next4
---

# Release localized four corrected AI concepts

## Why

The content task authored, independently reviewed and locally installed sixteen
translations for four corrected, published zh-TW AI concept articles. This task
owns the separate content PR/CI handoff and production release. Local tests and
installation receipts do not merge, deploy or publish those translations.

## Definition of done

- [x] Complete independent documentation review, open the content PR with no-auto-merge and record all applicable CI results on its exact current head.
- [x] Obtain exact-head merge approval after required checks; inspect the full pending deployment range and migration scope before proposing a release.
- [x] Fresh production source/version/draft/published/target guards match the admitted bundle and baseline; stop on unapproved drift.
- [x] New action-time owner authorization covers full backup/actual restore, deployment, actual-image isolated rehearsal and exactly sixteen target publications under an owned release hold.
- [x] Native publication, fresh persisted readback and zero-write replay pass, with all four source documents and unrelated rows preserved.
- [x] Public acceptance covers twenty pages, sixty source/localized assets and forty original desktop/mobile captures, including independent visual review and canonical/hreflang/sitemap/link checks.
- [x] Write sanitized release evidence, complete progress accounting, clear only this release's hold after acceptance and pass final runtime/health verification.

## Steps

- [x] Read the completed content task and docs/article-localization/reviews/20261029-ai-concepts-next4.json; retrieve the authoritative private baseline, jobs, bundle and review proofs using their hashes.
- [x] Complete document review and content PR/CI. Keep no-auto-merge until the owner authorizes the exact reviewed head.
- [x] Inspect merged target, pending range, migrations and fresh production state; prepare the exact release plan and obtain action-time authorization.
- [x] Verify full backup and actual restore, deploy through the existing release lifecycle and rehearse with the actual deployed image.
- [x] Use the unchanged native publisher, approved operator, durable journal, version/source guards and exact locale allowlist; verify fresh state and replay.
- [x] Capture public pages with sequential requests at least 1300 ms apart, the editorial user agent, settled fonts/header/layout and retained original screenshots; obtain independent acceptance.
- [x] Record actual release/finalization evidence, close this task and clear only the owned hold after all gates pass.

## How to verify

Follow the current article-localization and deploy skills and
ops/release/README.md. The actual candidate native publish_bundle dry-run passed;
it is not the future deployed-image rehearsal or fresh publication journal.
Compare fresh source canonical
hashes, locale versions and dirty/publication state using a fresh session. Native
progress reporting is historical journal accounting, not a live-state query.

After publication, verify public API/HTML, all assets, internal links,
canonical/hreflang, sitemap and desktop/mobile views for all twenty pages.
External requests use Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com).
Keep raw snapshots, operator IDs, host paths, backups and screenshots outside
Git; release documents contain sanitized hashes, counts and public paths.

## Notes

- Exact cohort: ai-term-fine-tuning, ai-term-few-shot-prompting,
  ai-term-multimodal-ai and ai-term-zero-shot-prompting. Add en, ja, ko and zh-CN
  to each: four articles, sixteen targets, zero source corrections and zero hubs.
- Manifest SHA-256:
  2082d5e3bd35eaef49ea0d8ce96a2e0b415138bb77e752392eda13a656e88ddc.
  Baseline:
  bb817bcf38290234de0969e6fcd39928a5f5c5a5fbd8c298154922db79c5367e.
  Baseline binding:
  25ed5ba7f159176f95ff7d262b26f6250df82495f994862b595ebcef083d2ac0.
- Preserved source canonical hashes and baseline published versions:
  - fine-tuning v10: e835a8eaeff22d888b1f8090703c0b998849dcc477de010fb09cebc0d1939729
  - few-shot-prompting v12: f156b18dec9410b6c92f5b7e2866208b1eee4fb221f0c826261abf52c880e808
  - multimodal-ai v12: 0c13a13cfa8909d81533ca563f8f688b62f9a1a35410409f7445b1cb9571b961
  - zero-shot-prompting v12: cdb0f81143fbdcf55694fab817fd25e73fc0867ae35f2db3dcc1c859fceb3eba
- Native local installation/replay and sixteen admission checks passed.
  Independent actual-install review:
  9a9c377bec8a7df70c8b7a4d61b780aa7ce3efc33b706d4bd741d7e9fe0454ef.
  Content-only integration review:
  1e7a4d5f7cbeadec4dc40f67581f7832d474a7189a347bad0dd7cf1bfe4f117b.
  Installed packs contain twenty documents with forty-eight new assets;
  twelve originals remain unchanged. All 130 local tests passed with zero skips,
  installed lint had zero errors/four English length advisories, and translation
  checks had zero hits.
- Private inputs remain authoritative. Their ignored working-tree mirrors,
  native journal/backups and admission receipts are local installation data,
  never Git/PR content or proof of production publication.
- Content PR #1919 has merged at
  f33af2e656204f89910740a945913268edfd513a after the owner's merge approval.
  The approved content head was 26b0d4256641ecc3a7a6ded5a48008ee3f6e5235.
  Records PR #1916 also merged, as
  9dc9dca54b4cc2660fefe635ef76c42d5a82dd8f, after the rebased head a841248
  passed all 22 fresh checks and independent patch-equivalence review. The
  merged target tree equals that tested head. Its own main-commit run also
  passed all 22 validation checks (four update checks succeeded; announce was
  skipped). The complete deployed a0366796..9dc9dca5 range has two commits and
  64 no-rename paths: 52 content and 12 documentation/task paths, with no
  migrations, application, dependency, compose, configuration or ops changes.
- The owner authorized merging the content/records PRs and preparing a concrete
  release plan, including the candidate dry-run. This does not authorize a
  backup, restore, deployment, publisher write phases or public capture for
  these sixteen translations. The source-only
  PR #1915 release and previous eight/forty-eight translation releases do not
  authorize this cohort.
- The actual candidate dry-run passed with sixteen start_translation operations,
  sixteen target publications and zero hubs. Eight admitted SELECT statements
  completed, with zero rejected statements; the selected native snapshot and
  all nine protected source/history sections remained unchanged. The candidate
  journal has no pending operation and no completed write phases, and must not
  be reused for publication. This is not a PostgreSQL-enforced read-only
  transaction: the unchanged native dry-run uses its own locking transaction.
  Candidate receipt SHA-256:
  63c83f59e9cc7420577852be7319997c57dd8afad1fa6776a52a6bb9ef66d190.
  Independent actual review:
  39c39bb579293fddd0e597305b7cafdb0ed959af006d268426cef09e647865f2.
  No production content write, deployment, backup or public capture is claimed.
  This task remains in progress; its release completion requirements stay open.
- Pre-claim scope checks covered seventy-six registered worktree task trees,
  matching local/remote branches and forty-seven open PR file lists. There was
  no competing active release scope; the sole ticket-file match was the
  dependent content PR #1919 itself. The native claim succeeded on
  codex/release-ai-concepts-next16-20261029 from the merged content commit.
- The existing Route A publisher remains the intended content path:
  dry-run, drafts, publish-articles and publish-hubs with one durable journal.
  The expected plan is sixteen start_translation drafts, sixteen target
  publications, zero hubs and zero source corrections. Candidate dry-run proved
  that plan; a fresh live journal and deployed-image isolated rehearsal remain
  required. Do not use the source-only correction
  writer or create a replacement publisher for this cohort.
- Local reinspection matched all twelve pinned native modules, the four-article
  manifest, forty-eight bundle assets and original baseline. The old preparation
  note predates actual installation and review; those steps are now complete.
  Native installation did not alter the authoritative job receipts or artifact
  manifests: all 375 original/mirrored input files remained byte-identical.
- The detailed plan, runtime/source probes, raw snapshots, scripts and code
  review receipts stay in the owner's private persistent workspace. Actual
  preparation has verified selected-source/target guards, protected state,
  the candidate-selected operator, runtime identities and dependency metadata.
  Fresh execution-time guards, owner authorization, full backup/actual restore,
  actual-image rehearsal, publication, forty-image public acceptance and
  finalization remain future gates.
- The concrete seven-step release plan is now ready for the owner's separate
  execution decision, SHA-256
  d5ab7ad55685efd114be9ae6b4c6bf6fc744b4f241df3daf0769d5a71ec88073.
  Final disabled tools are CORE v5, CONTENT v2, public collector v2 and QA
  assembler v4. Independent code/data/contract reviews passed; the final
  cross-package review covers all required QA, publication, rehearsal, link,
  plain-text and process-exit fields. The plan preserves true process exits,
  explicit approval, fresh guards, actual restore and deployed-image rehearsal,
  a new publication journal, original public evidence and the final unlocked
  11/0 verification. No future production result or owner approval is filled in.
- Superseding execution status: after reviewing that exact complete plan, the
  owner explicitly approved full backup/actual restore, fixed-target deployment,
  same-image rehearsal, sixteen publications, twenty-page/sixty-asset/forty-image
  acceptance and only this release's verified hold lifecycle. The actual quote
  and message reference are retained privately. Fresh execution preflight and
  final authorized-binding review now proceed; no production phase is claimed
  complete merely because execution is authorized.
- Actual execution has now completed full backup/restore, fixed-target deployment,
  same-image rehearsal, sixteen native publications and fresh readback/replay.
  Independent actual publication review passed (SHA-256
  9b9763e99421239ddbd5b90f8300569f7c4f4d3862fc4e923217938f79e2e7a7),
  including all four unchanged source rows and metadata, twenty canonical
  documents, thirty-two revisions and thirty-two audit rows. The first public
  acceptance run stopped with true exit 1 after retrieving twenty API documents
  and sixty assets: its sitemap validator expected five alternates, whereas the
  existing site contract includes those five plus x-default pointing to English.
  Original failed evidence is retained. A separately reviewed XML checker
  correction now requires the exact five canonical language URLs plus the
  unique English x-default URL. The fresh corrected collector completed with
  true exit 0; twenty pages, sixty assets and forty original screenshots passed
  mechanical checks and two independent visual reviews. All forty-four new
  unpublished-target references were confirmed as visible plain text through
  actual API/DOM evidence. Aggregate acceptance SHA-256:
  c2c6c7905366e2486b3b10a7d8fff68d70648d79faa6bf5cd005fa69cecb20b9.
  Static-image viewing limits are recorded in the independent reviews. The
  separately reviewed corrected-QA finalization completed with true accepted
  worker exit 0, cleared only its owned hold and passed the unmodified explicit
  target verifier with 11 PASS / 0 FAIL. Original publisher bytes and evidence
  remain unchanged; the full backup and restored database remain retained.
- Finalization receipt SHA-256:
  93cfcb6d3fea7480c7e63f4eb7a8f000a5b2e8125ef86e5d05d714bcac7cfeb0;
  independent actual finalization review:
  b9aabca709895fe28f0b013c39fffa05fc6533a2a4c3e215f2fdd0cd9c6fa87e.
  The first export's timestamp-format error and its narrowly reviewed
  export-only correction are preserved separately from successful finalization.
- Fresh read-only census at 2026-10-29T19:12:37.10031+08:00 found 2,250 public
  articles: 1,482 complete, 768 incomplete and 3,072 missing public language
  documents, excluding 120 draft articles. All selected twenty versions matched
  and all published locale rows were clean. Census SHA-256:
  a05fe520294807a3fc7b4303f9185dab19e9bb294afc987d5316703066c9cd3a;
  independent actual census review:
  cbe8fdfd22832e57c3ab8cac9a3869343d0e5f9c3124d4db2580bacb1e714eae.
  These actual totals are not calculated from an older snapshot.
- Native historical progress exited 0 and confirmed all sixteen target locales
  through all seven stages, with no report-wide errors or target issues. Its
  original twenty-entry input retains four zh-TW accounting notices because
  those unchanged sources have no new publication operation in this journal;
  their preservation/public acceptance is proved separately. Report SHA-256:
  bf11dce4665feb25c7884bc9f92c0681e90af02e452234c4572a287a149b2ecf.
- Sanitized release records are in
  docs/article-localization/releases/2026-10-29-ai-concepts-next4/. The broader
  all-article language task remains open. Two misleading annotation links found
  during next-batch selection have a separate unclaimed source-correction task;
  no source edit or next-batch translation is claimed by this release.
