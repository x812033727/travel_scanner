---
id: 2026-10-06-publish-onsen-kyoto-bus-zh-tw
title: Publish the zh-TW wording changes for the onsen and Kyoto bus guides
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-10-06T01:30:58Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/japan-onsen-ryokan-guide.json
  - apps/api/app/guides/content/kyoto-bus-subway-guide.json
---

# Publish the zh-TW wording changes for the onsen and Kyoto bus guides

## Why

Two published zh-TW guides lag behind their packs on main. Two wording PRs were merged and
deployed after the guides were last imported, but nobody ran the import for them:

- #1028 (`tasks/done/2026-09-20-lodging-tax-wording-site-wide.md`, its "dry-run 再
  `--publish`" box never ticked) changed 宿泊稅／宿泊税 to 住宿稅.
- #1001 (`tasks/done/2026-09-21-91-ci.md`) changed Kyoto's 「早上 6 點開門」 to 「早上 6:00 開門」.

Measured 2026-10-06 against the public API, normalizing both sides with `GuideDocument` and
hashing with `app.guides.service.document_hash`:

| slug | live zh-TW | live hash | repo hash (main cff4a6ac6) | differences |
| --- | --- | --- | --- | --- |
| `japan-onsen-ryokan-guide` | v8, modified 2026-09-20T09:33:35Z | `66c6ecf6…2a8d` | `cd4ad6ca…85f1` | 7 × 宿泊稅→住宿稅 in `description`, `blocks[0].text`, `blocks[2].text`, `blocks[3].caption`, `blocks[3].rows[3][0]`, `blocks[24].items[1]` (#1028) |
| `kyoto-bus-subway-guide` | v8, modified 2026-09-20T11:56:56Z | `865362fe…9caa` | `da86dc07…513c` | `blocks[18].items[0]` 6 點→6:00 (#1001); `blocks[22].text` 宿泊税→住宿稅 (#1028) |

Nothing else differs, so readers see an older wording and no wrong fact. The Kyoto translation
refresh (`2026-10-06-batch-005-nikko-kyoto-translations-refresh`) binds four locales to the live
zh-TW, so this publish should land first or that ticket binds to a hash that is about to change.

## Definition of done

- [ ] The owner has explicitly approved this publish (a choice question naming the two slugs and
      the diffs above, not a bare "ok").
- [ ] The public API's zh-TW documents for both slugs normalize to the repo packs' hashes
      (recompute them first; they are `cd4ad6ca…` and `da86dc07…` only while the packs are
      unchanged).
- [ ] Nothing else changed: en, ja, ko and zh-CN of both slugs are still `unpublished`, and the
      import touched no other slug.

## Steps

- [ ] Re-measure first. Fetch both slugs from
      `/api/travel/guides/howto/<slug>?locale=zh-TW` with the editorial User-Agent and confirm
      live is still v8 at the hashes above. If live moved, stop and find out who published.
- [ ] On the host, with the owner's go-ahead, follow
      `.agents/skills/content-pipeline/references/publish-runbook.md`. Stop if
      `/root/travel-scanner-deploy.hold` exists. Run `pg_dump` first and save a
      `guides-links-check --locale zh-TW` baseline.
- [ ] `guides-import --slug japan-onsen-ryokan-guide --slug kyoto-bus-subway-guide --locale zh-TW --dry-run`
      must show exactly two zh-TW `update`s and no other slug. Then run the same command with
      `--publish --actor-email <first ADMIN_EMAILS>`, then `guides-links-rebuild`. Compare the
      links check with the baseline (new findings only). A second dry-run must show `unchanged`.
- [ ] Verify (below), then tick the boxes and note the published version and hashes here.

## How to verify

```bash
cd apps/api
PYTHONUTF8=1 .venv/Scripts/python.exe ../../.agents/skills/content-pipeline/scripts/verify_public.py \
  --slug japan-onsen-ryokan-guide --slug kyoto-bus-subway-guide --kind howto --locale zh-TW --sitemap
```

Then compare each slug's public API `document` with the repo pack. Drop `version`,
`published_at` and `modified_at`, pass both through `GuideDocument.model_validate(...).model_dump(mode="json")`,
and compare `document_hash`. They must be equal, with zero field differences. The four other
locales of each slug must still return `"status":"unpublished"`.

## Notes

- On 2026-10-06 both packs pass `pack_cli lint --slug` with 0 errors. The onsen pack has
  one `no_summary` warning, which was already there before this ticket.
- Split out of `2026-09-20-correct-hakone-and-noboribetsu-bathing-tax` and
  `2026-09-20-correct-kyoto-flat-fare-bus-ic` on 2026-10-06 (claude-opus-5-5-board-closures).
  Those tickets' own corrections (#588, #593) are live. Only the later wording is not.
- Main, including #1001 and #1028, was deployed to production on 2026-10-06. That deploy did
  not write guide content: `guides-import` is a separate database write that needs the owner's
  consent. Neither slug is in `apps/api/app/guides/publish_holds.json`.
- The same 2026-10-06 measurement found the other three slugs of #1028 behind as well, by
  more than the 住宿稅 wording:
  - `tokyo-where-to-stay`: live v6, 2026-09-19T10:58Z, five published locales. Its zh-TW
    title, description and body were also rewritten by #565 and #660.
  - `osaka-kyoto-where-to-stay`: its description was rewritten by #565.
  - `kanazawa-2-day-itinerary`: it has the Shirakawa-go bus facts from #1007.

  The Tokyo and Osaka descriptions belong to the blocked
  `2026-09-14-answer-first-howto-descriptions`, which bulk-publishes 39 slugs. They are left
  out here on purpose. Publishing them is a visible SEO change with its own review, so a bare
  `--slug` for all five would carry changes this ticket has not checked. No open ticket
  covers publishing Kanazawa's #1007 bus facts. Review that diff, then file a ticket for it
  or fold it in here.
