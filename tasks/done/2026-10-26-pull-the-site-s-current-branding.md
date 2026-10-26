---
id: 2026-10-26-pull-the-site-s-current-branding
title: Pull the site's current branding package over a read-only endpoint (branding --pull)
status: done
priority: P2
area: tools
owner: claude-opus-5-5-branding-pull
claimed_at: 2026-10-26T00:23:16Z
created_at: 2026-10-26T00:21:45Z
completed_at: 2026-10-26T00:37:57Z
branch: claude/gracious-bohr-2mjwx0
depends_on: []
scope:
  - apps/api/app/config.py
  - apps/api/app/video_media/admin_api.py
  - apps/api/app/video_media/branding.py
  - apps/api/app/video_media/schemas.py
  - apps/api/tests/test_video_media_branding.py
  - apps/web/app/api/video/media/[...path]/forward.ts
  - apps/web/app/api/video/media/[...path]/route.test.ts
  - tools/video/media/client.mjs
  - tools/video/branding/cli.mjs
  - tools/video/branding/pull.test.mjs
  - tools/video/cli.mjs
  - docker-compose.prod.yml
  - docs/videos/BRANDING.md
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
---

# Pull the site's current branding package over a read-only endpoint (branding --pull)

## Why

The channel intro and outro (`intro.mp4`, `outro.mp4`, `manifest.json`) stay out of git
(docs/videos/BRANDING.md). They live only on the owner's computer and in the production worker's
work volume (`_branding/<hash>/`), so a cloud container has none: S01, S09 and S18 were assembled
in the cloud on 2026-10-19 and came out with no intro or outro, and the S-axis third batch
(`2026-10-19-curio-s-axis-third-batch-s29`) waits on the owner to hand the package over by hand.
A cloud session has no SSH key either. On 2026-10-26 the owner chose a read-only download over
uploading the files into each session.

## Definition of done

- [x] With a video tool token, `node tools/video/cli.mjs branding --pull` installs on any machine
      the exact package the site's worker builds with (same branding hash), after the same media
      checks as `--install`; it downloads nothing when the machine already has it.
- [x] `--series sothatswhy` does the same for the series package; `--dry-run` downloads and
      checks without installing.
- [x] The API serves only the two files a current.json names, never anything else on the volume
      (older packages, cuts, a symlink out of `_branding`), and says why when there is nothing.
- [x] BRANDING.md and the curio-episode skill's cloud steps say how.

## Steps

- [x] `apps/api/app/video_media/branding.py`: read `_branding/current.json` (and the series one)
      from the read-only work volume, with the tool's own validation.
- [x] `GET /video/media/branding`, `/branding/series/{series}`, `/branding/files/{sha256}` on the
      media router (video tool token, the download shares the media download limit).
- [x] The web forwarder `apps/web/app/api/video/media/[...path]` passes the three through.
- [x] `brandingStatus` / `downloadBrandingFile` in `tools/video/media/client.mjs`; `branding --pull`
      in `tools/video/branding/cli.mjs`.
- [x] Tests: `apps/api/tests/test_video_media_branding.py`, the forwarder's route test,
      `tools/video/branding/pull.test.mjs`.
- [ ] After deploy: from a cloud container, `branding --pull --dry-run` against mokaair.com
      (needs a token the owner allows), then `--pull`.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_media_branding.py tests/test_video_media_api.py -q
cd apps/web && npx vitest run "app/api/video/media"
node --test tools/video/branding/*.test.mjs tools/video/media/*.test.mjs
# after deploy, with a token (NODE_USE_ENV_PROXY=1 in a cloud container)
node tools/video/cli.mjs branding --pull --dry-run
node tools/video/cli.mjs branding --pull && node tools/video/cli.mjs branding --json
```

The installed hash must equal the host's `branding --json` (`docker compose … exec -T video-worker
node tools/video/cli.mjs branding --json`).

## Notes

- Closed in its own pull request; the unticked step (a real `branding --pull` against
  mokaair.com) can only run after the deploy, with a token the owner allows. Record it here or in
  the follow-up ticket when it is done.
- Claimed with `--force`: the overlapping claims (2026-10-12 outro, 2026-10-14 curio skill,
  2026-10-17 lexicon migrate/revise, 2026-10-18 S-axis pilot, 2026-10-24 compilation episodes)
  are all stale and none has an open pull request on these files. Two week-old Codex drafts
  (`codex/a01-0134-precompat-20261019`, `codex/a01-exact-media-dispatch-fence-20261017`) change
  other hunks of `video_media/admin_api.py`; the new routes are at the end of the file and the
  only shared line is the `from app.video_media import …` import.
- The routes live under `/video/media` so the existing web forwarder (token check, streaming,
  byte ranges) carries them with three route lines instead of a new proxy.
- The API reads the work dir from `get_settings().video_work_dir` (an env setting, not a runtime
  override), so the description routes do not touch the database.
- Not verified here: that the api container's user can read `_branding/<hash>/*.mp4` written by
  the worker (uid 1001). The compilation download already reads files the worker writes on the
  same volume, so it should; if `/branding` answers `video_branding_broken` with "not a file
  under _branding" on the host, check the modes.
- The host still decides what is current: `branding --install` on the worker. Nothing here writes
  to the volume, and there is no way to push a package to the host through the site.
- Follow-up that can now be done: `2026-10-13-local-assemble-warns-when-its-branding` (compare the
  local current with `GET /api/video/media/branding` before an assemble).
