---
id: 2026-09-27-correct-wordpress-migration-tag-links-batch030
title: Correct WordPress migration tag links Batch030
status: review
priority: P1
area: api
owner: codex-batch030-token-link-fix
claimed_at: 2026-09-27T10:41:49Z
created_at: 2026-09-27T10:41:42Z
completed_at:
branch: codex/article-localization-batch030-token-link-fix
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-host-migration.json
  - apps/api/app/guides/content/wordpress-migration-aftercare.json
---

# Correct WordPress migration tag links Batch030

## Why

Two published Traditional Chinese WordPress migration guides use structured links from the ordinary word「標記」to the unrelated AI glossary article `ai-term-token`. In `wordpress-host-migration` block 12, it means a restricted marker used to identify requests reaching the new host. In `wordpress-migration-aftercare` block 4, it means analytics tag settings. Both should be plain text. This task was split from `2026-09-23-correct-five-unrelated-ai-glossary-links-before`; its other three website links remain there.

## Definition of done

- [ ] Both reviewed pack inlines and, under a later authorized source update, both public `zh-TW` revisions show the same visible text without linking to `ai-term-token`.
- [ ] All other article fields, images, metadata, visibility and existing revisions are preserved; the source update stops on a production version conflict.

## Steps

- [x] Capture both full production rows in a single read-only repeatable-read transaction and verify published/draft v4 against the unmodified repository models.
- [x] Change only `/blocks/12/inlines/1` and `/blocks/4/inlines/1` from article links to plain-text `標記`; verify visible text and all other fields unchanged.
- [x] Pass focused pack lint, content-pack tests and task validation.
- [x] Open a standalone draft PR without automatic merge; keep this task open for the later production source update.
- [ ] After separately authorized, guarded deployment and backup, update only these two `zh-TW` source revisions with exact version/hash checks, then verify public links.

## How to verify

From `apps/api`, run `.venv/Scripts/python.exe -m app.guides.pack_cli lint --slug wordpress-host-migration` and the same for `wordpress-migration-aftercare`, plus `.venv/Scripts/python.exe -m pytest tests/test_guides_content_pack.py -q`. From the repo root, run `npm run check:tasks`. The external exact-change receipt at `C:\Users\x8120\.codex\article-localization-release\batch030-link-fix\exact-correction-review.json` must report `PASS_EXACT_TWO_INLINE_CORRECTIONS`.

## Notes

Fresh full production source at 2026-09-27 10:42:29 UTC: `C:\Users\x8120\.codex\article-localization-release\batch030-link-fix\two-source-20260927T104224Z.json`, SHA256 `691b8d21df7c04caedb1e4c911bc63fffbd3403f516d1126a9b10fab6d49916e`. Both articles are active/published article v2; only `zh-TW` is present, with published/draft locale v4. Published hashes: host migration `20354724ebd32eefcee48a0c08ae23b78a4a6ac7cdf200474fc0600f109628e3`, aftercare `da363c3847673c9994627c1271186d7214d5d0385edca5a369e7f59db519170c`. `source-review-before.json` SHA256 `6bb004e701fc26f65289230236457d055d5c88c22486826bccc917b20081fdd5` verifies full document and metadata equality with Git at `227aae75cc3d6ac0461117d529881f059b176433`. No production write has been made. Merging the PR alone will not update the live database; a later guarded source correction must use a fresh snapshot and stop if v4 or these hashes moved.

Offline exact-diff receipt `exact-correction-review.json` SHA256 `75edfbdb9fcb6277913b7569e53bcabff4a4f1d241ad7a9b85bca4da3e98363a` proves one inline object changed per pack, visible text and every other normalized field unchanged. Both scoped pack lints passed with only existing `no_summary` advisories; `tests/test_guides_content_pack.py` passed (9 passed, 5 skipped); `npm run check:tasks` and `git diff --check` passed.

Draft PR [#855](https://github.com/x812033727/travel_scanner/pull/855) has the `no-auto-merge` label. Its content commit is `cfc703a913976ffc01aac91c094ae031d71a5f65`. It is intentionally unmerged and undeployed at this handoff; do not mark this task done until the guarded live source update and public verification are complete.
