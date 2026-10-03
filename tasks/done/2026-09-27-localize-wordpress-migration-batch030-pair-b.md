---
id: 2026-09-27-localize-wordpress-migration-batch030-pair-b
title: Localize WordPress host and aftercare guides batch030 pair B
status: done
priority: P1
area: docs
owner: codex-batch030-pair-b
claimed_at: 2026-09-27T11:11:53Z
created_at: 2026-09-27T11:11:38Z
completed_at: 2026-09-27T11:33:37Z
branch: codex/article-localization-030-pair-b
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-host-migration.json
  - apps/api/app/guides/content/wordpress-migration-aftercare.json
  - apps/web/public/guides/wordpress-host-migration
  - apps/web/public/guides/wordpress-migration-aftercare
---

# Localize WordPress host and aftercare guides batch030 pair B

## Why

These two published WordPress migration articles have only a zh-TW version. Add complete en, ja, ko and zh-CN text plus text-bearing artwork, while preserving their published source and correcting the unrelated AI-token link only in the new locales. PR #855 owns the separate zh-TW source correction and must be merged and published before this batch can be released.

## Definition of done

- [x] Five-language packs with complete translated title, description, body, tables, callouts, image text/alt/caption, source titles and internal labels.
- [x] Twenty-four new language-suffixed hero SVG/JPG and diagram SVG assets render cleanly; six original assets remain unchanged.
- [x] Source/version, link behavior, lint, tests and image QA are recorded in a hash-bound external receipt; content commit only, no standalone PR or production write.

## Steps

- [x] Claim narrow scopes, pin production zh-TW v4 and compare current repository/image bytes.
- [x] Translate both full documents and SVG labels without propagating the unrelated `ai-term-token` link.
- [x] Render JPG variants, inspect all images, run pack and link checks.
- [x] Commit only these packs/assets/task after validation.

## How to verify

Run focused `uv run python -m app.guides.pack_cli lint --slug ...`, API pack/link tests, web unresolved-link tests, SVG rendering/bounds checks, and `npm run check:tasks`. Verify production baseline/version and original assets against the pinned read-only capture.

## Notes

- Base: origin/main `f44555bb97153fa05cf3ca565ffa28db473e86d3`; the two source packs and original assets did not change from the 2026-09-27 inventory baseline `227aae75cc3d6ac0461117d529881f059b176433`.
- Fresh public read-only capture: `<home>\.codex\article-localization-release\batch030-pair-b\pair-b-fresh-public-baseline.json`, SHA-256 `4367bd61f933b58f7cc6759265bac55a50ba020db5c122af7ecf8650d221caf4`. Both articles remain public only in zh-TW, document version 4; six original image bytes match public, repository and origin/main. Public document differs from the pack only by the API default empty image description.
- Full DB read-only source capture from #855 at 10:42 UTC: `<home>\.codex\article-localization-release\batch030-link-fix\two-source-20260927T104224Z.json`, SHA-256 `691b8d21df7c04caedb1e4c911bc63fffbd3403f516d1126a9b10fab6d49916e`. Both article v2, zh-TW published/draft locale v4. Host published SHA `20354724ebd32eefcee48a0c08ae23b78a4a6ac7cdf200474fc0600f109628e3`; aftercare published SHA `da363c3847673c9994627c1271186d7214d5d0385edca5a369e7f59db519170c`.
- PR #855 source-link fix content commit `cfc703a913976ffc01aac91c094ae031d71a5f65` remains unmerged/unpublished. Its owner released task scope in handoff `cb79f79f`; new translations must use plain text for the ordinary word 「標記」 and must not link `ai-term-token`. Before release, #855 must be merged and its exact zh-TW source correction published with fresh version checks.


- Validation: 504 checks passed in `<home>\.codex\article-localization-release\batch030-pair-b\pair-b-validation.json` (SHA-256 `599e3e9b9318752afbba54a2f3b686eb4355bbc434a95d3435ac8348f3531e1d`); 24 new assets, six unchanged originals matched live/public bytes, 16 full-resolution SVG renders visually checked via contact sheets. API focused tests 67 passed/5 skipped; ContentBlocks web test 65 passed. Pack lint exit 0 with existing no-summary guidance and en length advisory. #855 remains a release prerequisite.
