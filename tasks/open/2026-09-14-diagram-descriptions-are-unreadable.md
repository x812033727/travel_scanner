---
id: 2026-09-14-diagram-descriptions-are-unreadable
title: 498 SVG diagrams hide their fares and times from every crawler
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-14T13:48:24Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/schemas.py
  - apps/web/lib/content-blocks.ts
  - apps/web/components/content-blocks.tsx
  - apps/web/components/content-blocks.test.tsx
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
- [ ] The visible layout on first paint is unchanged.
- [ ] No SVG markup is inlined into the page (see Notes).

## Steps

- [ ] Add an optional `description` to `ImageBlock` on **both** sides — the Pydantic model in
      `apps/api/app/guides/schemas.py` and the TypeScript mirror in `apps/web/lib/content-blocks.ts`
      — validated with the existing optional-text helper.
- [ ] Render it inside the existing `<figure>` in `ContentBlocks`' image branch, as a
      `<details><summary>` under the figcaption: in the DOM and crawlable even while collapsed.
- [ ] A one-off `tools/` script lifts the `<title>`/`<desc>` out of
      `apps/web/public/guides/**/diagram-*.svg` into the content packs.
- [ ] Skip the ones whose `<desc>` merely restates the `alt` — about five already do.

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
