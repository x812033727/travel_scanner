---
id: 2026-10-05-host-verify-sh-derives-the-up
title: host-verify.sh derives the up-service set and alembic head, and accepts the AI-drama-off exit 4
status: in-progress
priority: P2
area: tools
owner: claude-opus-5.5
claimed_at: 2026-10-05T02:28:36Z
created_at: 2026-10-05T02:27:58Z
completed_at:
branch: claude/angry-mcclintock-5fc7c7
depends_on: []
scope:
  - .agents/skills/deploy
  - .claude/skills/deploy
---

# host-verify.sh derives the up-service set and alembic head, and accepts the AI-drama-off exit 4

## Why

`.agents/skills/deploy/scripts/host-verify.sh`, the read-only post-deploy verifier, gave two false
FAILs on the 2026-10-05 deploy of 8e8598cf0 and needed a hand edit for a third value:

1. `UP_COUNT=13` was hard-coded; `docker-compose.prod.yml` has had `video-ai-worker` (api image,
   profile `video`) since, so the check printed `up=14/13` with all 14 containers Up and 0 restarts.
2. `ALEMBIC_HEAD="0122_video_anime_production"` was hard-coded, so every deploy with a migration
   (0124 that day) had to sed it before sending.
3. `video-worker-started` required zero `auto exited with` lines, but with AI drama switched off in
   the admin video settings the worker's `auto` hits a pending drama job every round, the API answers
   `video_ai_drama_disabled` ("AI 漫劇已停用，待執行的工作不會送出模型請求") and `auto` exits 4
   (`EXIT.external`) by design. That was the state before and after the deploy.

## Definition of done

- [x] The services expected Up come from the compose file at the live HEAD (`config --services` for
      the three profiles, minus `restart: "no"` one-shots, which must be `Exited (0)`), compared by
      name with `missing_up=` / `extra_up=` in the verdict.
- [x] The alembic head comes from the api image (`alembic heads`, exactly one), and `alembic current`
      must equal it.
- [x] An `auto exited with 4` whose previous non-knock line carries the drama-off message is counted
      apart (`auto_exit4_drama_off=`); knock_failed<=1 and not_paired=0 still hold.
- [x] SKILL.md and references/post-deploy.md no longer tell the reader to edit those values; the
      `.claude` copy of SKILL.md is byte-identical.

## Steps

- [x] Rewrite sections 3, 5 and 10 of the script; only `EXPECTED_SHA` is left to fill in.
- [x] Exercise the new logic locally against stubbed docker/compose output (13 scenarios).
- [x] Run it once, read-only, against the host: 2026-10-05 ~02:42Z with EXPECTED_SHA=8e8598cf0 gave
      TOTAL pass=11 fail=0: `up=14/14 missing_up=none extra_up=none oneshot_exited0=1/1`, alembic
      `heads=1 current=0124_video_review_subject (head)` read from the image, and
      `auto_exited=0 auto_exit4_drama_off=6` (the log shows the drama-off message on the line right
      before each `video-worker: auto exited with 4`). No profile WARN.
- [x] Update SKILL.md, post-deploy.md, the Claude copy.

## How to verify

```bash
bash -n .agents/skills/deploy/scripts/host-verify.sh
cmp .agents/skills/deploy/SKILL.md .claude/skills/deploy/SKILL.md
npm run test:tools
```

and on the host, the usage in references/post-deploy.md: every check PASS with the live SHA filled in.

## Notes

- `docker compose config` without `--services` would print the resolved environment, `.env` values
  included, so the one-shot services are read with awk from the compose file itself (`restart: "no"`
  under a service at two-space indent); `config --services`/`--profiles` print names only.
- `config --profiles` lists every profile in the file; one outside `PROFILE_NAMES` prints a WARN,
  because neither the expected list nor `ps` would see its services.
- The drama-off message is matched by the UTF-8 bytes of 漫劇已停用 written in octal (`printf`), keeping
  the script ASCII like the rest; the Shorts knock's `video-worker: shorts:` lines are skipped when
  looking for the line before the exit, because the knock loop runs beside `auto`.
- A stale api image would carry an old head and pass `alembic-head`; `containers-rebuilt-this-deploy`
  is the check that catches a stale image, so the two are read together.
