---
id: 2026-09-19-review-117-flagged-foreign-guides
title: Review the 117 introductions the foreign-place rule flagged beyond the vetted 52
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-19T08:01:09Z
completed_at:
branch:
depends_on: []
scope:
  - docs/catalog-content-reviews/2026-09-19-foreign-guides-unreviewed.json
---

# Review the 117 introductions the foreign-place rule flagged beyond the vetted 52

## Why

On 2026-09-19 `guides-foreign-place-scan` (PR #559) read all 6,061 approved hotspot introductions
and flagged 165 as describing another country. The owner chose to reject only the 52 that
`2026-09-13-reject-public-guides-about-another-country` had checked by hand; the other **117 are still
approved and public**. They were never read one by one.

A glance says most are genuinely misplaced: Busan's 國際市場 carries JNTO statistics about the
"Japan market", Huế's 孝陵 and 场钱桥 carry Taiwan travel blogs, Sapporo's 圓山公園 carries Taipei's
Yuanshan. But the rule also misfires: `6da32c2d` is NAVITIME's page for the Shibuya MEGA Don Quijote
itself, flagged as Thailand. Rejecting all 117 blind would remove good content with the bad.

By country of the hotspot: 韓國 50, 越南 41, 台灣 15, 日本 11. The full list, with title, URL, locale
and the rule's reason, is `docs/catalog-content-reviews/2026-09-19-foreign-guides-unreviewed.json`.

## Definition of done

- [ ] Every one of the 117 is marked in the JSON as `reject` or `keep`, with a one-line reason for each `keep`.
- [ ] The `reject` rows are rejected on the host and no longer public; the `keep` rows stay approved.
- [ ] Rule misfires that repeat (a shape, not a single row) are written down for whoever tunes `foreign_place`.

## Steps

- [ ] Read each row: open the URL when the title is not conclusive; judge against the hotspot, not the city.
- [ ] Put the `keep` ids in a skip list and run the scan with `--skip-ids-file`, list only, to confirm the
      remaining findings are exactly the `reject` rows.
- [ ] With the owner's go-ahead, run the same command with `--apply --actor-email` (see the host commands in
      `docs/catalog-content-reviews/2026-09-13-misplaced-guides.md`), then re-run list-only and expect 0.

## How to verify

```bash
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-foreign-place-scan --skip-ids-file <keep-list>
```

After the apply this lists nothing.

## Notes

- `eff4dc8f-6ea0-4392-abed-f7bf7d6e0e72` (Funliday's 西公園 page under Fukuoka) was already skipped on
  2026-09-13 and is not among the 117.
- The scan counts each (guide, locale) once; the same article can appear under two hotspots.
