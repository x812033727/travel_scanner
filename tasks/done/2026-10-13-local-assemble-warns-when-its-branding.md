---
id: 2026-10-13-local-assemble-warns-when-its-branding
title: Local assemble warns when its branding package is older than the host's
status: done
priority: P2
area: tools
owner: claude-opus-5-5-branding-pull
claimed_at: 2026-10-26T00:43:38Z
created_at: 2026-10-13T13:44:53Z
completed_at: 2026-10-26T01:00:50Z
branch: claude/gracious-bohr-2mjwx0
depends_on: []
scope:
  - tools/video/assemble/cli.mjs
  - tools/video/assemble/assemble.test.mjs
  - tools/video/compile/cli.mjs
  - tools/video/compile/compile.test.mjs
  - tools/video/core/branding.mjs
  - tools/video/core/branding.test.mjs
  - tools/video/branding/site.mjs
  - tools/video/branding/site.test.mjs
  - docs/videos/BRANDING.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Local assemble warns when its branding package is older than the host's

## Why

The channel outro was lengthened to 21 s with music and room for YouTube end-screen cards on
2026-10-12 (`mokaair-brand-package-v4-endscreen`), and installed on the production host only.
This machine's `<workdir>/_branding/current.json` stayed on `mokaair-brand-package-v2-cc`
(installed 2026-10-04), so the five 奇聞檔案局 recuts assembled locally on 2026-10-13 pinned the
old 3 s outro: no music, no end-screen room. Nothing said so; the owner found it watching the
cut. The local copy was brought to v4 by hand that day (`branding --install
~/mokaair-work/channel-outro-20261012/package-v4/channel`).

## Definition of done

- [x] A local `assemble`/`compile` of a new long video says, before it encodes, when the branding
      it is about to pin is not the one the site's worker uses (the id and hash of both), and
      how to install the current one; it does not silently go ahead.
- [x] It works offline (no site reachable): it says it could not compare, it does not fail.
- [x] BRANDING.md says local builds must match the host's package and how to check.

## Steps

- [x] Find where the host's current branding can be read without SSH (an existing /admin or
      automation endpoint, or the worker's report); if none exists, decide with the owner
      whether to add a read-only one or keep a checked-in expected id instead.
- [x] Add the comparison to the assemble/compile preflight, with tests.

## How to verify

`assemble` has no dry run; `compile --dry-run` and the tests show it without encoding:

```bash
node --test tools/video/branding/site.test.mjs tools/video/core/branding.test.mjs \
  tools/video/compile/compile.test.mjs tools/video/assemble/assemble.test.mjs
```

By hand, after #1860's endpoint is deployed: point `--workdir` at a scratch folder with an older
package installed (`branding --install`), run `compile --slug <series>-full --dry-run` or start an
`assemble` of a new video and read the `WARN branding:` line; `branding --pull` and it is gone.

## Notes

- Related: 2026-10-12-play-the-channel-intro-bumper-after (bumper position), being done on
  branch claude/bumper-after-condensation.
- 2026-10-26: the read-only endpoint the first step asks for exists
  (2026-10-26-pull-the-site-s-current-branding): `GET /api/video/media/branding` with a video
  tool token answers the worker's current id and hash (`brandingStatus` in
  tools/video/media/client.mjs), and `branding --pull` installs it.
- 2026-10-26 (claude-opus-5-5-branding-pull): done on the same branch as the endpoint
  (claude/gracious-bohr-2mjwx0), since the comparison needs it. `pinsDefault` in core/branding.mjs
  says when a build takes this machine's package (first build, adoption, an unpinned
  re-placement); only then do assemble and compile ask (`siteBrandingNotice` in
  tools/video/branding/site.mjs), once, with a 10-second deadline and no retries. Different: a
  `WARN branding:` line before encoding and again at the end; the build goes on, since an older
  package can be deliberate. No token or no site: a `not compared` / `could not compare` line.
- Claimed with `--force`: the overlapping claims are stale; 2026-10-24-manga-sticker-drama-pace
  (status review) already landed as #1836 and only its ticket was never closed.
- On the host the worker asks about its own volume, so it always matches and prints nothing; it
  costs one request per first build within the video tool token's per-minute window.
- Duration receipt rebound by an independent reviewer (`claude-pr-review-branding-site-check-20261026`,
  "Branding site check increment: 4 files" in docs/videos/long-form/review.md): PASS, the change
  moves no length and no bookend choice. Its out-of-scope notes: (1) `readCredentials` ran
  outside the try, so a credentials file that does not parse threw out of assemble; fixed (moved
  inside, with a test). (2) "Could equal packages warn?": no, the host's current.json `hash` is
  written by `installPackage` from `validateBranding` with the intro at the start, the same hash
  `readDefaultBranding` recomputes and checks here; pull.test and the compile test assert the
  equality. (3) The first `pinsDefault` assertion's message says "even with nothing installed"
  though the test installs a package first; `pinsDefault` reads no package, so the result is the
  same. Left as is: core/branding.test.mjs is a bound file and a message-only edit would need
  another receipt increment; fix it with the next change that touches that file.
- Codex review on #1860 (P2): for an explainer whose series package differs, the warning said
  `branding --pull` without `--series`, which updates only the channel default while this machine
  keeps reading the stale series registry. The advice now names `--series <remote.series>`.

