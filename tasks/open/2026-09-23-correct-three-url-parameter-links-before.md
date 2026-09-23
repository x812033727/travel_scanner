---
id: 2026-09-23-correct-three-url-parameter-links-before
title: Correct three URL parameter glossary links before localization
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-23T13:57:03Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/https-certificate-setup.json
  - apps/api/app/guides/content/dns-records-troubleshooting.json
  - apps/api/app/guides/content/cloudways-ssl-setup.json
---

# Correct three URL parameter glossary links before localization

## Why

Three published Traditional Chinese website guides link the visible word `參數`
to `ai-term-model-parameters`, although their surrounding paragraphs discuss URL
or query parameters. The same wrong destination exists in the repository,
published document, draft and latest revision. These articles were excluded from
localization batch023 so the incorrect meaning is not copied into four languages.

## Definition of done

- [ ] Replace only the three structured article inlines listed below with plain
      text inlines containing exactly `參數`; preserve all other document fields,
      metadata, source dates, source URLs and images.
- [ ] Independently review the exact three semantic changes and validate the packs.
- [ ] Land the correction through a scoped PR with required CI.
- [ ] Complete a separate guarded source revision/publication using the existing
      publication service, a fresh source/version comparison and backup; preserve
      any new editor changes or changed visibility. Merge alone is not publication.
- [ ] Verify the visible text remains unchanged and the incorrect public links
      are absent; record new source versions before any localization claim.

## Steps

- [ ] Claim this task after checking cross-worktree scope ownership.
- [ ] Reconcile a fresh production snapshot with the recorded source versions.
- [ ] Correct `/blocks/13/inlines/1` in `https-certificate-setup`.
- [ ] Correct `/blocks/3/inlines/1` in `dns-records-troubleshooting`.
- [ ] Correct `/blocks/15/inlines/1` in `cloudways-ssl-setup`.
- [ ] Finish review, CI, publication and browser acceptance as separate states.

## How to verify

Compare parsed GuideDocument models before/after and allow exactly the three
listed inline changes: `{type: article, kind: life, slug:
ai-term-model-parameters, text: 參數}` becomes `{type: text, text: 參數}`.
Run scoped `pack_cli lint --slug` for each pack plus `npm run check:tasks` and
`git diff --check`. Use the source-correction publication runbook for actual
revision, concurrency and visibility checks. Do not run an automatic link rebuild
that would recreate these links.

## Notes

Read-only finding recorded at 2026-09-23T13:37:33Z against main
`e4476b843d43eaa603737b2adef270dfa0368e1c`. All three articles were version 2,
with Traditional Chinese locale/published version 4; no correction was applied.

Evidence:
`C:/Users/x8120/.codex/article-localization-release/batch023-candidate-inventory/source-correction-inventory-v1.json`
SHA256 `e00c865a1cccc092159efde3ce8646b913a2d962f28de8fe93bea7b1ee4fdf95`.
The inventory binds complete source rows, pack hashes and all three surrounding
paragraphs. Its source snapshot SHA256 is
`c13a30df55708b43398333172e6d5b0afc3aba16b5d6419e7fb21be141df1daa`.
These are historical baselines, not permission to overwrite later changes.

Keep this task separate from the already reviewed cable-label glossary correction
(PR690) and the four domain/billing guides selected for batch023.
