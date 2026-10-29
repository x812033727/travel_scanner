---
id: 2026-10-29-release-localized-four-corrected-ai-concepts
title: Release localized four corrected AI concepts
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-29T06:24:49Z
completed_at:
branch:
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

- [ ] Complete independent documentation review, open the content PR with no-auto-merge and record all applicable CI results on its exact current head.
- [ ] Obtain exact-head merge approval after required checks; inspect the full pending deployment range and migration scope before proposing a release.
- [ ] Fresh production source/version/draft/published/target guards match the admitted bundle and baseline; stop on unapproved drift.
- [ ] New action-time owner authorization covers full backup/actual restore, deployment, actual-image isolated rehearsal and exactly sixteen target publications under an owned release hold.
- [ ] Native publication, fresh persisted readback and zero-write replay pass, with all four source documents and unrelated rows preserved.
- [ ] Public acceptance covers twenty pages, sixty source/localized assets and forty original desktop/mobile captures, including independent visual review and canonical/hreflang/sitemap/link checks.
- [ ] Write sanitized release evidence, complete progress accounting, clear only this release's hold after acceptance and pass final runtime/health verification.

## Steps

- [ ] Read the completed content task and docs/article-localization/reviews/20261029-ai-concepts-next4.json; retrieve the authoritative private baseline, jobs, bundle and review proofs using their hashes.
- [ ] Complete document review and content PR/CI. Keep no-auto-merge until the owner authorizes the exact reviewed head.
- [ ] Inspect merged target, pending range, migrations and fresh production state; prepare the exact release plan and obtain action-time authorization.
- [ ] Verify full backup and actual restore, deploy through the existing release lifecycle and rehearse with the actual deployed image.
- [ ] Use the unchanged native publisher, approved operator, durable journal, version/source guards and exact locale allowlist; verify fresh state and replay.
- [ ] Capture public pages with sequential requests at least 1300 ms apart, the editorial user agent, settled fonts/header/layout and retained original screenshots; obtain independent acceptance.
- [ ] Record actual release/finalization evidence, close this task and clear only the owned hold after all gates pass.

## How to verify

Follow the current article-localization and deploy skills and
ops/release/README.md. Native publish_bundle dry-run is a DB-backed release gate
and has not been run for this translation cohort. Compare fresh source canonical
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
- PR/CI, merge, deployment, publication and public acceptance for these sixteen
  translations are pending. The source-only PR #1915 release and previous
  eight/forty-eight translation releases do not authorize this cohort.
- No production write, deployment, publisher dry-run or public capture is
  claimed for this translation cohort. This task is open and unclaimed.
