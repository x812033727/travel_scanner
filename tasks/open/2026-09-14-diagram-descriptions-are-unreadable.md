---
id: 2026-09-14-diagram-descriptions-are-unreadable
title: 498 SVG diagrams hide their fares and times from every crawler
status: review
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-19T09:28:46Z
created_at: 2026-09-14T13:48:24Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/api/app/guides/schemas.py
  - apps/api/tests/test_guide_rich_blocks.py
  - apps/web/lib/content-blocks.ts
  - apps/web/components/content-blocks.tsx
  - apps/web/components/content-blocks.test.tsx
  - apps/web/components/guides/article-page.tsx
  - apps/web/components/admin-guides-panel.tsx
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - tools/lift-diagram-descriptions.py
---

# 498 SVG diagrams hide their fares and times from every crawler

## Why

Every localized guide document carries exactly one SVG diagram, and those diagrams hold facts
that appear nowhere else in the article body. `korea-ktx-srt-ticket-guide/diagram-1.svg`'s
`<desc>` alone states 52,200 KRW, 2h11m, 44 trains a day and per-station fares for six stations,
across 37 `<text>` nodes.

`ContentBlocks` draws it as `<img src="...svg">`, so a crawler — and every AI answer engine —
gets the `alt` string and the figcaption and nothing else. This is textbook text-in-images, and
it is the one genuinely extraction-hostile thing left in an otherwise fully server-rendered
article path. The SVGs are already authored correctly (`role="img"`, `aria-labelledby`, a
`<title>` and a long factual `<desc>`); the loss is purely that the file is referenced rather
than its description carried in the block.

## Definition of done

- [ ] A diagram's long description is in the article's server HTML, in the language of the
      document, for every localized document that has one.
- [x] The visible layout on first paint is unchanged.
- [x] No SVG markup is inlined into the page (see Notes).

## Steps

- [x] Add an optional `description` to `ImageBlock` on **both** sides — the Pydantic model in
      `apps/api/app/guides/schemas.py` and the TypeScript mirror in `apps/web/lib/content-blocks.ts`
      — validated with the existing optional-text helper.
- [x] Render it inside the existing `<figure>` in `ContentBlocks`' image branch, as a
      `<details><summary>` under the figcaption: in the DOM and crawlable even while collapsed.
- [x] A one-off `tools/` script lifts the `<title>`/`<desc>` out of
      `apps/web/public/guides/**/diagram-*.svg` into the content packs.
- [x] Skip the ones whose `<desc>` merely restates the `alt` — about five already do.

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest
```

Then build and `curl` an article with a diagram and confirm the fares appear in the HTML.

## Notes

**Do not inline the SVG markup.** `contentImageSrc` validates the *path*, not the file's
contents, so inlining would make any future SVG a script-injection surface — in a codebase that
went out of its way to keep JSON-LD non-executable.

Measured while filing `2026-09-14-aio-article-citations-and-llms-txt`; not done there because it
crosses into `apps/api` and needs a content-pack migration over 398 packs, which would have
tripled that task's review surface.

### 2026-09-19 done in repo (claude-fable-5-1)

On `claude/travel-scanner-pr-552-rpq36m`. The content-pack migration itself is **not run here**:
other agents were editing packs in the same checkout, so the coordinator runs it once (below).
The first definition-of-done box stays open until that run is merged and imported on the host.

- `ImageBlock.description`: `PlainText`, default `""`, max 4000 (a paragraph's ceiling), declared
  after `caption` in `apps/api/app/guides/schemas.py`; mirrored as `description?: string` plus the
  `isOptionalText` guard in `apps/web/lib/content-blocks.ts`. Every existing pack validates
  unchanged, and the importer's plan compares both sides through the model, so a document
  without a description still reads `unchanged`. New test
  `test_image_description_is_optional_plain_text` in `apps/api/tests/test_guide_rich_blocks.py`.
- `ContentBlocks`' image branch, inside the `<figure>` after the `<figcaption>`, text only and
  folded by default:
  `<details class="text-sm leading-6 text-[var(--muted)]"><summary class="cursor-pointer py-2.5 font-semibold">{labels.imageDescription ?? alt}</summary><p class="whitespace-pre-wrap pb-2">{description}</p></details>`.
  The toggle's words are `ContentBlockLabels.imageDescription` (optional: a caller that passes
  none gets the alt, never a blank toggle), fed by `guides.imageDescriptionToggle` in
  `common.json` (article page) and in `admin.json` (admin preview), five locales, one key each.
  The admin editor spreads `{ ...block }` on edit, so a description survives an admin save.
- `tools/lift-diagram-descriptions.py` (stdlib only; `--dry-run`, `--slug` repeatable,
  `--content-dir`/`--public-dir` for a copy). Reads `/guides/<slug>/diagram-*.svg`: the shared
  `diagram-<n>.svg` (1356 blocks) and the per-locale `diagram-<n>-<locale>.svg` (360). Takes the
  `<desc>` text (entities resolved, whitespace normalised), skips it when it equals the block's
  `alt` **or its `caption`** (the caption is already in the figcaption; all 444 of those are exact
  duplicates), writes only `description` (placed after `caption`), only in the pack tooling's
  formatting, and refuses a pack that would not round-trip byte-for-byte. Idempotent: a second
  run writes nothing. Verified in write mode on a scratch copy of four packs: the diff is the
  `description` lines alone, the second run reports `unchanged`, `load_packs` accepts the result.
- Dry run over the repository (`python3 tools/lift-diagram-descriptions.py --dry-run`): 1055 of
  1056 packs carry a diagram, 571 packs would change; 1716 diagram blocks: **877 lifted, 395
  skipped as restating the alt, 444 skipped as restating the caption, 0 without a `<desc>`, 0
  unusable** (none over 4000 chars, none with HTML-like or control text). Largest document after
  lifting is about 30 KB against the 110 KB pack limit. The "about five" in Steps undercounted:
  395 diagrams' `<desc>` is the alt verbatim.
- Left alone on purpose: the `<title>` (the accessible name, which `alt` already carries);
  `pack_ingest._document_text` (the diagram-number rule must keep comparing the SVG's labels
  against the article body, not against the SVG's own `<desc>`); `readingMinutes` (folded text).

**Coordinator, from the repository root, once nobody else is editing packs:**

```bash
python3 tools/lift-diagram-descriptions.py --dry-run | tail -1   # 571 would change; lifted 877
python3 tools/lift-diagram-descriptions.py
python3 tools/lift-diagram-descriptions.py --dry-run | tail -1   # 0 would change; unchanged 877
git diff --stat -- apps/api/app/guides/content | tail -1        # 571 files changed, insertions only
(cd apps/api && uv run pytest tests/test_guides_content_pack.py tests/test_guides_pack_ingest.py tests/test_guide_rich_blocks.py -q)
npm run lint:web && npm run typecheck:web && npm run check:i18n && npm run test:web
```

**Host, after the merge is deployed.** The descriptions reach the published documents only
through `guides-import`; the plan reads each changed document as `update` (every locale of the
pack, so leave `--locale` off) and everything else as `unchanged`:

```bash
# the slugs whose pack the merge changed; <merge> is the merge commit on main
git diff --name-only <merge>^ <merge> -- apps/api/app/guides/content | sed 's#.*/##; s#\.json$##' | sort -u > /root/diagram-slugs.txt
SLUG_ARGS=$(sed 's/^/--slug /' /root/diagram-slugs.txt | tr '\n' ' ')   # ~571 slugs, one command line
cd /root/travel_scanner
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-import \
  --actor-email <admin> --publish --dry-run $SLUG_ARGS > /root/diagram-import-dryrun.json
# expect: taxonomy unchanged everywhere, locale actions update/unchanged, no create
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-import \
  --actor-email <admin> --publish $SLUG_ARGS
```

Then `curl -s https://<host>/zh-TW/guides/<kind>/korea-ktx-srt-ticket-guide | grep -c '52,200'`
should be non-zero: the SRT fare is in the HTML, inside the folded `<details>`.
