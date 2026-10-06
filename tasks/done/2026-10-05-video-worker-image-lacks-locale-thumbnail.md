---
id: 2026-10-05-video-worker-image-lacks-locale-thumbnail
title: The video worker image installs no Korean, Simplified Chinese or Japanese font, so it never draws language thumbnails
status: done
priority: P2
area: ops
owner: claude-opus-5-5-worker-locale-fonts
claimed_at: 2026-10-06T00:06:39Z
created_at: 2026-10-05T13:18:32Z
completed_at: 2026-10-06T00:26:49Z
branch: claude/worker-locale-fonts
depends_on: []
scope:
  - ops/video/package.json
  - tools/supply-chain.test.mjs
  - ops/video/Dockerfile
  - .github/dependabot.yml
  - .agents/skills/dev-and-ci/references/dependabot.md
---

# The video worker image installs no Korean, Simplified Chinese or Japanese font, so it never draws language thumbnails

## Why

`tools/video/render/fonts.mjs` names five font packages (`FONT_PACKAGES`). Since #1109 and #1111
(2026-10-01/02) a caption locale's own thumbnail is set in its own font: `ko` in
`@fontsource-variable/noto-sans-kr`, `zh-CN` in `-noto-sans-sc`, `ja` in `-noto-sans-jp`. The
video worker's image installs its packages from `ops/video/package.json` alone (`npm install` in
`ops/video/Dockerfile`), and that file, written on 2026-09-25 (#755), lists only
`noto-sans-tc` and `jetbrains-mono` of the five. The root `package.json` has all five, so
`tools/video` tests in CI and on a laptop never see the gap.

In the image, `render --thumbnails-only` calls `bundledCoverage(locale)` for each owed locale,
`fontDir("noto-sans-kr")` throws `@fontsource-variable/noto-sans-kr is not installed; run npm ci
in this checkout`, and the command exits non-zero. The worker's `drawLanguageThumbnails`
(`tools/video/automation/flow.mjs`) treats that as a note ("<locales> thumbnails not drawn, they
keep the video's own: …") and goes on, so `package` writes `skipped_thumbnail_locales` and every
automated video's language batch goes up with the video's own thumbnail. Nothing fails, so
nobody notices. That is the outcome `2026-10-02-video-worker-draws-the-language-thumbnails` was
meant to end.

Found while doing `2026-10-05-ops-video-package-json-s-fonts`. Read from the code; the host's
worker log was not checked (no host access in that session).

## Definition of done

- [x] `ops/video/package.json` installs `@fontsource-variable/noto-sans-kr`, `-noto-sans-sc` and
      `-noto-sans-jp` at the exact version `package-lock.json` resolves (5.3.0 on 2026-10-05),
      and they are gone from `WORKER_FONTS_NOT_INSTALLED_YET` in `tools/supply-chain.test.mjs`.
- [ ] The `Video worker image` workflow is green on the pull request (it builds the image and
      renders the example inside it).
- [ ] After a deploy, the next automated video's language batch has `thumbnails/<locale>.jpg`
      for ko, ja and zh-CN (or a `skipped_thumbnail_locales` reason other than "not installed").

## Steps

- [x] Add the three packages to `ops/video/package.json` (the weekly npm `video-worker` group in
      `.github/dependabot.yml` already matches `@fontsource-variable/*`, so it needs no change).
- [x] Drop the three from `WORKER_FONTS_NOT_INSTALLED_YET`; `node --test tools/supply-chain.test.mjs`.
- [x] Optional: have the image's smoke stage (`ops/video/Dockerfile`, target `smoke`) resolve
      every `FONT_PACKAGES` entry, so a font added to `fonts.mjs` alone fails the image build too.
- [ ] After deploy (coordinator, host): read the worker log for "thumbnails not drawn" and check
      one language batch's package.

## How to verify

```bash
node --test tools/supply-chain.test.mjs
# In the built image (docker build -f ops/video/Dockerfile --target worker .):
node -e 'import("./tools/video/render/fonts.mjs").then(f => Object.keys(f.FONT_PACKAGES).forEach(n => console.log(f.fontDir(n))))'
```

## Notes

- The three packages add about 14 MB to the image (noto-sans-jp 5.3 MB, -sc 4.7 MB, -kr 3.6 MB
  unpacked, measured from a local node_modules on 2026-10-05).
- Read from the code, no image the worker has run could draw them, so the first batch that has
  language thumbnails is likely also the first real run of that path past `package`; check that
  batch by hand.
- 2026-10-06 (claude-opus-5-5-worker-locale-fonts): the three fonts are in
  `ops/video/package.json` at 5.3.0, the version `package-lock.json` resolves for all five. The
  root `package.json` asks for `^5.3.0`; the existing test "the video worker installs exactly the
  versions package-lock.json resolves" holds the two files together.
- `WORKER_FONTS_NOT_INSTALLED_YET` is gone, map and loop, rather than left empty: the image's
  smoke stage now resolves every `FONT_PACKAGES` entry, so a font parked in that map would fail
  the image build anyway. The test is now plainly "the video worker installs every font
  tools/video draws with".
- The smoke step (`ops/video/Dockerfile`, target `smoke`, before `assemble/smoke.mjs`) calls
  `fontDir` for every `FONT_PACKAGES` name and `bundledCoverage` for the slide fonts and each
  `LOCALE_FONTS` locale, which reads each font's `index.css` the way `render --thumbnails-only`
  does. The example video has no caption locale, so `assemble/smoke.mjs` never reached those
  fonts; that is why the image built green without them. Checked locally: the one-liner prints
  five directories with the repository's node_modules and exits 1 with
  "@fontsource-variable/noto-sans-kr is not installed" in a copy that has only the TC and mono
  fonts. No Docker on this machine, so the image itself was not built here.
- Scope grew by `ops/video/Dockerfile` (the optional smoke step), and by one comment each in
  `.github/dependabot.yml` and `.agents/skills/dev-and-ci/references/dependabot.md`, which said a
  `video-worker` Dependabot pull request moving only fonts the worker does not install is green.
  The worker now installs all of them, so every such pull request that moves a font needs the
  copy into `ops/video/package.json`. Group patterns are unchanged.
- Definition of done 2 is this ticket's pull request's own `Video worker image` check (not one
  of the four required checks); it had not run when the ticket was closed, so it is not ticked.
  Read it before the pull request is marked ready.
- Definition of done 3 and the last Step (deploy, worker log, one language batch) moved to
  `2026-10-06-check-the-first-automated-video-s`; split because they need a deploy and the host.
