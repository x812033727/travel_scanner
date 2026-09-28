---
id: 2026-09-28-localize-four-wordpress-growth-and-launch
title: Localize four WordPress growth and launch guides (Batch033)
status: done
priority: P2
area: docs
owner: codex-batch033
claimed_at: 2026-09-28T01:37:45Z
created_at: 2026-09-28T01:37:39Z
completed_at: 2026-09-28T02:14:14Z
branch: codex/article-localization-033-wordpress-growth
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-ad-placement.json
  - apps/api/app/guides/content/wordpress-blog-build.json
  - apps/api/app/guides/content/wordpress-business-site.json
  - apps/api/app/guides/content/wordpress-local-to-live.json
  - apps/web/public/guides/wordpress-ad-placement
  - apps/web/public/guides/wordpress-blog-build
  - apps/web/public/guides/wordpress-business-site
  - apps/web/public/guides/wordpress-local-to-live
---

# Localize four WordPress growth and launch guides (Batch033)

## Why

Four published WordPress guides still have only their Traditional Chinese
document. Their English, Japanese, Korean and Simplified Chinese public API
responses have `status=unpublished` and no document. Each guide also has an
editable, text-bearing hero SVG and diagram SVG. This task owns only these four
guides; Batch031/032 and the other WordPress guides are separate work.

## Definition of done

- [x] All four packs contain complete en, ja, ko and zh-CN documents alongside
      the byte-preserved published zh-TW source, with translated metadata,
      headings, body, tables, callouts, image text/alt/captions, source titles
      and article-link labels.
- [x] The text-bearing hero and diagram each have reviewed four-language SVGs,
      with matching rendered raster hero covers and retained credits.
- [x] Local pack lint, structural/content/link review, relevant tests and
      full-size visual checks pass. Publication and production QA are separate.

## Steps

- [x] Create an isolated worktree and claim the eight exact pack/asset paths.
- [x] Verify current public zh-TW v4 documents against normalized main packs.
- [x] Translate and review sixteen missing locale documents.
- [x] Produce and inspect 32 SVGs and 16 raster hero covers.
- [x] Run local validation and prepare a reviewable handoff.

## How to verify

Run `uv run python -m app.guides.pack_cli lint --slug <slug>` for all four
slugs in `apps/api`, followed by relevant API/content-link tests. Run
`npm run check:tasks` and scope-appropriate repository checks. Compare every
translated document's block structure, numbers, links, technical tokens,
source URLs/dates and credits with the pinned source; inspect all localized
figures at full size and confirm text fit.

## Notes

Base main `4b6c5cd99fa9eab3b658d5b6cf639cb001f8fc3e`; the four source
pack Git blob IDs in task order are `c3d4bbbb03082f861d4ea5a286c95b4c478d6d68`,
`34c783c5cb4e054d5153a6fc8129c8a72b23b3db`,
`9bb7136956db008e4682295720618262703fd3a0`, and
`9f5b24b8cdf558cd278a43d8e7955efae07b390c`. A read-only public API
check at task start found all four published with only zh-TW document v4.
GuideDocument-normalized source and public document hashes match exactly:

| Slug | Published zh-TW SHA-256 |
| --- | --- |
| `wordpress-ad-placement` | `65befeece176569fbd7b6ef80a8b61af5e92bfda6613338966d3e85f05407afa` |
| `wordpress-blog-build` | `e90738e066cae12a93dacf5d40ce4eb37993078b8eb61c12311cf8f786592189` |
| `wordpress-business-site` | `ad0a798d92be76d9c8e4c1c9400df58698914069480077f6c3840605d65f2e30` |
| `wordpress-local-to-live` | `02d3216a4a534b06912a835386738aab7a4e27ab438d005ceb7bb982a5dff0d6` |

The public API adds the schema's empty image description; no editorial source
text differs after normalization. Recheck production version and hash before
any later release because this pin is an authorship baseline, not a publish gate.

Source correction dependency: `wordpress-blog-build` zh-TW block `[5]`
`rich_paragraph.inlines[1]` currently has
`{"type":"article","text":"標記","kind":"life","slug":"ai-term-token"}`.
This ordinary verb does not refer to the AI token glossary. The correction is
exactly `{"type":"text","text":"標記"}`, preserving the visible sentence.
The currently published zh-TW v4 SHA-256 is
`e90738e066cae12a93dacf5d40ce4eb37993078b8eb61c12311cf8f786592189`.
Target languages should use plain text at this position. Do not import this
batch until the source correction has its own task/PR, is published, and the
translation baseline has been rebound to the corrected live version and hash.

Local completion on 2026-09-28: all 16 target GuideDocuments parse and retain
the source block types/counts, source URLs and dates, article targets, credits,
technical structure, and original root metadata. The pinned zh-TW JSON is
unchanged byte-for-byte. Every translated figure exists at the referenced path;
all 16 JPG covers are 1600 x 900. Thirty-two localized SVGs passed Edge
rendered text bounds (zero canvas/card overflows) and full-size visual review.
The four pack-lint runs passed with only advisory no-summary warnings inherited
from the source and English length guidance. Related content-pack, link, and
alias tests passed (17 passed, 7 skipped); guide-link tests passed (6 passed,
6 skipped). `npm run check:tasks` and `git diff --check` passed. Numeric-token
review confirmed three apparent mismatches were formatting/translation only:
September 14, 2026; Korean first-party source; and Korean four-stage diagram.
After rebasing on `origin/main` 2fa7bf1e, all four source pack blobs still
match the pinned baseline, and the normalized zh-TW SHA-256 values above
remain unchanged. Publication, import, and production/browser checks remain
separate.
