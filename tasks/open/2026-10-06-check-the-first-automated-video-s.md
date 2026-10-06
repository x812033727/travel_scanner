---
id: 2026-10-06-check-the-first-automated-video-s
title: Check the first automated video's ko, ja and zh-CN thumbnails after the worker image has their fonts
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-10-06T00:16:42Z
completed_at:
branch:
depends_on: []
scope:
  - ops/video/package.json
---

# Check the first automated video's ko, ja and zh-CN thumbnails after the worker image has their fonts

## Why

Until `2026-10-05-video-worker-image-lacks-locale-thumbnail`, the video worker's image installed
only the Traditional Chinese and code fonts. `render --thumbnails-only` then threw
`@fontsource-variable/noto-sans-kr is not installed` for every owed locale,
`drawLanguageThumbnails` (`tools/video/automation/flow.mjs`) logged "<locales> thumbnails not
drawn, they keep the video's own: …" and went on, and `package` wrote the gap into
`skipped_thumbnail_locales`. Every automated video's language batch went up with the video's own
thumbnail, and nothing failed.

That ticket's pull request adds `@fontsource-variable/noto-sans-kr`, `-noto-sans-sc` and
`-noto-sans-jp` to `ops/video/package.json` and makes the image's smoke stage resolve every font
`tools/video/render/fonts.mjs` names. Whether the host's worker now draws them can only be seen
on the host, after a deploy rebuilds `video-worker`. No image has ever drawn a language thumbnail
there, so the first language batch after that deploy is also the first real run of the
`--thumbnails-only` path past `package`.

## Definition of done

- [ ] After the deploy that carries the fonts, the next automated video's language batch has
      `upload/thumbnails/<locale>.jpg` for ko, ja and zh-CN in its package, or its
      `skipped_thumbnail_locales` gives a reason other than "not installed" for each one missing.
- [ ] The worker log since that deploy has no "thumbnails not drawn" line that says
      "is not installed".

## Steps

- [ ] Confirm the deploy that holds the font PR has run and rebuilt `video-worker` (deploy
      timing follows the `deploy` skill's paid-video-work guard, because a deploy recreates the
      worker).
- [ ] In the container: `node -e 'import("./tools/video/render/fonts.mjs").then(f => Object.keys(f.FONT_PACKAGES).forEach(n => console.log(f.fontDir(n))))'`
      from `/opt/mokaair` prints five directories.
- [ ] Read the worker log for "thumbnails not drawn".
- [ ] Open one language batch's `upload/metadata.json` (`thumbnails`, `skipped_thumbnail_locales`)
      and look at its `upload/thumbnails/{ko,ja,zh-CN}.jpg` by eye: the right script, nothing
      cut off.

## How to verify

```bash
# On the host (prod-host-ops skill for access):
docker compose -f docker-compose.prod.yml exec -T video-worker sh -c 'cd /opt/mokaair && node -e "import(\"./tools/video/render/fonts.mjs\").then(f => Object.keys(f.FONT_PACKAGES).forEach(n => console.log(f.fontDir(n))))"'
docker compose -f docker-compose.prod.yml logs --timestamps --since <deploy time> video-worker | grep "thumbnails not drawn"
docker compose -f docker-compose.prod.yml exec -T video-worker sh -c 'cat /var/lib/mokaair/video-work/<slug>/upload/metadata.json' | grep -A8 '"thumbnails"'
```

## Notes

- Split from `2026-10-05-video-worker-image-lacks-locale-thumbnail` (its third Definition-of-done
  item and its last Step), which needed a deploy and host access; the code part closed with that
  ticket's pull request.
- Scope is `ops/video/package.json` only because a font still missing would be fixed there; the
  check itself changes no file. If the thumbnails fail for another reason (layout, words too
  long), file a new ticket against `tools/video/render`; a fix in
  `tools/video/automation/flow.mjs` is bound by the duration receipt
  (`docs/videos/long-form/review.json`).
