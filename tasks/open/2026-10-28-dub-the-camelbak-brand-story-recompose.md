---
id: 2026-10-28-dub-the-camelbak-brand-story-recompose
title: Dub the CamelBak brand story: recompose it without burned subtitles
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-28T23:47:06Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/story.test.mjs
---

# Dub the CamelBak brand story: recompose it without burned subtitles

## Why

The owner wants foreign dubs for 「CamelBak水背上身，為何出口還得受咬？｜品牌故事」
(`story-everyday-camelbak-c14`, made by the host worker). Its language panel shows every dub as
skipped: since 2026-10-25 the story composer writes `subtitles: { burn_in: true }` for every story
(`tools/video/automation/story.mjs`, the owner's burned-subtitle trial), and the site only offers
dubs on a final whose zh-TW captions are switchable CC (`dubStoryNeedsSwitchableCC`). The owner
answered 「要配音」 on 2026-10-28, which takes this one episode out of the burn-in trial.

## Definition of done

- [ ] The CamelBak episode has an approved final with `subtitles.burn_in: false` (switchable zh-TW CC).
- [ ] Its dubs for the ticked locales are made, checked and approved, and the owner has uploaded them in Studio.
- [ ] Other stories keep the burn-in default.

## Steps

- [ ] Add a per-slug exception in the story composer (the file already keys other exceptions by
      slug, e.g. `shortC08Story`, `compactA01Story`): `story-everyday-camelbak-c14` keeps
      `burn_in: false`. Test it in `story.test.mjs`. PR, CI, merge, deploy (skill `deploy`).
- [ ] On the host (needs SSH; skill `brand-story` and `prod-host-ops`): deploying the composer
      does NOT rewrite an existing `video.json`. Recompose from the chapters, keep every paid
      asset (no new images or narration), re-assemble, re-run final QA, and push the final gate
      again; the owner re-approves the final.
- [ ] Then the publish confirmation must be approved again before the language panel lets
      dubs be made (「要先有核准的上架確認，才能再做一次」).
- [ ] Worker makes the dubs (ticked locales), languages gate, owner uploads tracks in Studio.

## How to verify

`/admin/videos` for the CamelBak story: the dub cells no longer read 跳過 and show progress;
the approved final has no burned subtitles (look at any frame).

## Notes

2026-10-28: filed from a cloud session with no SSH to the host, so nothing on the host was
touched. The repo copy of `docs/videos/story-everyday-camelbak-c14/video.json` still says
`burn_in: false`; it lags the host, which built the episode with burn-in.
