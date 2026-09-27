---
id: 2026-09-27-news-automation-doc-still-says-the
title: news-automation doc still says the deploy script lacks the news profile
status: done
priority: P3
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-27T03:00:56Z
created_at: 2026-09-27T03:00:54Z
completed_at: 2026-09-27T03:02:32Z
branch: claude/continue-incomplete-task-b3237e
depends_on: []
scope:
  - docs/news-automation.md
---

# news-automation doc still says the deploy script lacks the news profile

## Why

`docs/news-automation.md` §Switching it on, step 1, told the reader that the host deploy
script passes only `--profile hotspots` and that `--profile news` had to be added as a host
change the owner decides. The script has passed `--profile news` since 2026-09-24
(owner-approved, backup `.bak-20260924-news`), which the deploy skill's runbook already
records. Anyone following the doc would ask the owner for a change that already happened
or, worse, edit the script a second time. Found by the 2026-09-25 skills coverage pass
(PRs #767–#778), which compared the repo docs with what the skills now say.

## Definition of done

- [x] Step 1 states the current fact: an ordinary deploy starts and rebuilds the two news
      services because the script carries the profile, and the reader is told how to check
      on the host, since the script is not in git.
- [x] The rest of the doc and the `prod-host-ops` skill's news-ops reference agree with it.

## Steps

- [x] Rewrite step 1 of §Switching it on.
- [x] Confirm `.agents/skills/deploy/references/runbook.md` says the same (2026-09-24/25,
      `grep -- --profile /root/deploy-travel-scanner.sh`).

## How to verify

```bash
git diff origin/main -- docs/news-automation.md
grep -n -- "--profile" docs/news-automation.md .agents/skills/deploy/references/runbook.md
```

On the host, `grep -- --profile /root/deploy-travel-scanner.sh` lists `hotspots`, `news`
and `video`.

## Notes

- The same pass listed three more stale statements that this ticket does not touch,
  because other open tickets own those files:
  - `docs/videos/README.md` rows 74–75 still say Azure is the voice provider and the channel
    voice is 「還沒選」, while the voice has been Gemini's Sulafat since PR #725. Ticket
    `2026-09-24-video-pilot-ai-model-choice` has that step, and the worker image carries a
    copy of the README (`2026-09-25-the-video-worker-s-docs-volume`).
  - `ops/nginx/README.md` (the /ads.txt paragraph) and `ops/nginx/mokaair.conf.example` say
    `Google-Adstxt` is not a verified crawler because `05-crawler-ranges.conf` is built from
    `googlebot.json` only. `tools/nginx-crawler-ranges.mjs` has read `special-crawlers.json`
    as well since #566 (2026-09-19), so the exemption's stated reason is wrong even though
    the exemption itself (a 429 reads as "no ads.txt") still holds. Both files sit in the
    scope of `2026-09-22-ads-txt-is-exempt-from-the`, still in progress.
  - `ops/nginx/README.md` check 2 says `cd /srv/travel-scanner/current`; the host runs from
    `/root/travel_scanner`. The `prod-host-ops` skill already notes it, and the file is in
    the scope of `2026-09-23-scrub-host-details-from-docs`.
- `apps/api/app/guides/publish_holds.json` (two Singapore guides) was also flagged, but its
  gate ticket `2026-09-21-validate-equivalent-singapore-guide-numbers-and` is still open, so
  the holds stand.
