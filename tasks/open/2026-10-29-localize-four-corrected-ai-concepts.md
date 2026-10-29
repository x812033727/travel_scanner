---
id: 2026-10-29-localize-four-corrected-ai-concepts
title: Localize four corrected AI concept articles
status: in-progress
priority: P2
area: api
owner: codex-next4-localization
claimed_at: 2026-10-29T06:04:45Z
created_at: 2026-10-29T05:56:27Z
completed_at:
branch: codex/ai-concepts-locales-20261029
depends_on:
  - 2026-10-28-correct-misleading-ai-concept-source-links
scope:
  - apps/api/app/guides/content/ai-term-fine-tuning.json
  - apps/api/app/guides/content/ai-term-few-shot-prompting.json
  - apps/api/app/guides/content/ai-term-multimodal-ai.json
  - apps/api/app/guides/content/ai-term-zero-shot-prompting.json
  - apps/web/public/guides/ai-term-fine-tuning
  - apps/web/public/guides/ai-term-few-shot-prompting
  - apps/web/public/guides/ai-term-multimodal-ai
  - apps/web/public/guides/ai-term-zero-shot-prompting
  - docs/article-localization/reviews/20261029-ai-concepts-next4.json
  - .l10n-source4-20261029
  - docs/article-localization/installations/.lock
  - docs/article-localization/installations/bundles/2082d5e3bd35eaef
  - docs/article-localization/installations/ai-term-fine-tuning.json
  - docs/article-localization/installations/ai-term-few-shot-prompting.json
  - docs/article-localization/installations/ai-term-multimodal-ai.json
  - docs/article-localization/installations/ai-term-zero-shot-prompting.json
---

# Localize four corrected AI concept articles

## Why

The four published AI concept articles have corrected zh-TW sources but still
need en, ja, ko and zh-CN. Source correction PR #1915 was deployed and published
separately; its task is complete. This task adds exactly sixteen translations,
preserving the four corrected source documents and all twelve original assets.
It continues the coordinator's completed private translation and review work;
it does not restart the older prepared jobs or reuse their old source baseline.

## Definition of done

- [x] A postpublication baseline pins the four actual corrected source documents and sixteen missing locales, with no source differences.
- [x] All sixteen private translations have independent text, visual and glyph reviews bound to the final documents, previews, assets and original CLI attempt evidence; no unresolved findings remain.
- [x] The native private bundle passes exact twenty-document/sixteen-target validation, with forty-eight packaged assets, zero source corrections and zero hubs.
- [ ] Install only the reviewed bundle through the native installer after this narrow claim; preserve all four zh-TW canonical documents, original assets and unrelated metadata.
- [ ] Recheck the installed bytes, GuideDocument/ArticlePack schemas, scoped lint, translation advisories and applicable native tests; independently review the complete integration diff.
- [ ] Record sanitized scope, document/asset/review/check hashes in the single scoped evidence JSON; open a content PR with no-auto-merge and verify its actual CI.
- [ ] Close this translation task only when its content requirements are complete; create a separate release-localized task open and unclaimed, depending on this task.

## Steps

- [x] Confirm the actual source release, finalization, fresh source snapshot and new baseline before translation.
- [x] Run the new exact sixteen private CLI jobs and preserve all attempts, including the original numeric-validation failure.
- [x] Apply independently requested corrections without extra model calls, re-materialize/re-render, and obtain final independent reviews for all sixteen documents.
- [x] Assemble a new private native bundle and complete its independent verifier review and actual mechanical validation.
- [x] Recheck open PR, remote-branch and local-worktree collisions; create this branch from the source task closeout commit and claim exactly the nine scoped paths.
- [ ] Have the coordinator run the unchanged native installer with the exact bundle manifest, baseline and private work directory.
- [ ] Verify installation and source preservation, run applicable checks, obtain independent integration review, record evidence, and prepare the content PR without automatic merge.
- [ ] Open the separate release task after content completion; require new action-time approval before any deployment or publication of these sixteen translations.

## How to verify

- Native private verification uses publish_bundle.verify_bundle as a pure file
  function, assemble_bundle.reviewed_document/localize_links, GuideDocument and
  ArticlePack validation, and scoped pack_ingest.lint_all. The publisher CLI's
  DB-backed dry-run is not an offline content check.
- After installation, run from apps/api:
  python -m app.guides.pack_cli lint --kind life --slug ai-term-fine-tuning --slug ai-term-few-shot-prompting --slug ai-term-multimodal-ai --slug ai-term-zero-shot-prompting
- Run the existing translation_checks.py for exactly these four slugs and read
  every advisory. Retain full translations when text_length warns.
- Run the relevant content-pack and localization pipeline/bundle/install tests,
  npm run check:tasks, and git diff --check. Record real exit codes and exact CI
  head results; an unrun or skipped check is not a pass.
- Compare all installed files to the hash-pinned private bundle; compare every
  zh-TW canonical hash below and all twelve original asset hashes to the new
  source baseline binding. Keep aliases, related, news_date and classification.

## Notes

- Branch base: source closeout commit e82d73ca5a8a35367bfe44be9f244279fb98ba8f,
  whose parent is deployed source commit a036679662030de86f00f0271f84a39265f55edd.
  The source task's exact obsolete open copy was removed manually by the owner;
  earlier automatic cleanup rejections and failed readbacks remain in private
  evidence. This translation task performs no cleanup.
- Corrected zh-TW versions and canonical document hashes:
  - ai-term-fine-tuning v10: e835a8eaeff22d888b1f8090703c0b998849dcc477de010fb09cebc0d1939729
  - ai-term-few-shot-prompting v12: f156b18dec9410b6c92f5b7e2866208b1eee4fb221f0c826261abf52c880e808
  - ai-term-multimodal-ai v12: 0c13a13cfa8909d81533ca563f8f688b62f9a1a35410409f7445b1cb9571b961
  - ai-term-zero-shot-prompting v12: cdb0f81143fbdcf55694fab817fd25e73fc0867ae35f2db3dcc1c859fceb3eba
- Fresh baseline SHA-256:
  bb817bcf38290234de0969e6fcd39928a5f5c5a5fbd8c298154922db79c5367e.
  Baseline binding:
  25ed5ba7f159176f95ff7d262b26f6250df82495f994862b595ebcef083d2ac0.
- Native private bundle manifest:
  2082d5e3bd35eaef49ea0d8ce96a2e0b415138bb77e752392eda13a656e88ddc.
  Private actual verification:
  1a288e93f5c5a9075c0a4030434d56f147ab071699ddb340e6ac010773387441.
  It checked twenty documents, sixteen new targets, forty-eight bundle assets,
  all twelve preserved originals, zero source corrections, zero hubs and zero
  lint errors. Translation checks reported zero hits. Four English text_length
  warnings remain advisory; no content was shortened.
  Independent actual-verification review:
  d61bce2ffe4123f5db0af2aaf195b619c0bffe721811bf059d679a1253cf7238.
- Independent final review cohort hashes:
  b5a93f0fd3f43aa739e49d140b63ae4a4fd8d4fa19321d22a722ca7915e63bd7
  (fine-tuning and few-shot); and
  9b359b1afc1142cb4dcbfc08e1e8dd5b2f2eefbbf40a8dd747491a848d169361
  (multimodal and zero-shot). Reviewers were separate from the Codex CLI
  translators; the coordinator applied their corrections. Raw attempts and
  correction histories remain outside Git, including the native runner's
  original nonzero outcome before the reviewed zero-model correction.
- Private verifier v2 independent code review:
  8f80aee39a8c285d056e7781958a207d2243247eb4bee175b234fee38923ebaa.
  It preserves native Windows prompt text-hash semantics and binds the one
  corrected Japanese job to its unique actual attempt without changing receipts.
- A fresh scope audit read forty-six open PR file lists (10,264 filenames) with
  no overlap; the planned remote branch did not exist. Seventy-six registered
  worktrees were checked. Two unchanged incomplete legacy checkouts and one
  missing legacy path were recorded without cleanup; no active source-content
  work conflicts with this batch. Repeat collision checks before the PR.
- Raw snapshots, jobs, full review records, screenshots and validation outputs
  stay in the owner's persistent private workspace. The scoped evidence JSON
  must contain portable hashes and outcomes, not machine paths, database or
  actor identifiers, secrets, or metadata from unrelated unpublished drafts.
- The four-source release approval does not authorize merge, deployment or
  publication of these sixteen translations. Keep the content PR labeled
  no-auto-merge; a draft alone does not prevent repository automation merging it.
- Installation is currently held: the native installer's path helper requires
  bundle, baseline and work beneath its repository root, while this batch's raw
  evidence must remain private outside Git. The coordinator and an independent
  reviewer are checking the existing external-input installation route. No
  installation was attempted, no native guard was weakened, and private inputs
  were not copied into the repository. Resolve this narrow integration step
  before the installation checklist item can be completed.
- The coordinator subsequently selected the existing native installation route:
  an exact, locally ignored working copy of the private baseline/jobs/bundle.
  The authoritative external files remain immutable. The seven added scope
  entries are only local generated inputs, the native lock, this manifest's
  journal/backups and four per-article admission receipts. They must be locally
  ignored before creation, remain untracked, and never enter Git or the PR.
  Full source/mirror inventories, original source bytes, twelve original assets
  and native code are checked before and after. The unchanged native installer
  owns content replacement and backups; replay must leave all fifty-two content
  destinations unchanged in both bytes and mtime and preserve original/mirror
  inputs. Preparing this route does not itself execute or approve an install.
