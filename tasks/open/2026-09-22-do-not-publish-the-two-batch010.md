---
id: 2026-09-22-do-not-publish-the-two-batch010
title: Do not publish the two batch010 Singapore guides until their review gate clears
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-09-22T02:05:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/singapore-4-day-itinerary.json
  - apps/api/app/guides/content/singapore-changi-airport-mrt-simplygo-guide.json
---

# Do not publish the two batch010 Singapore guides until their review gate clears

## Why

PR #635 merged as `d52af4d9` on 2026-09-22T01:55:14Z with **zero reviews**, while
its own description said to keep it a draft:

> Keep this PR draft. Before merge or publication, independently review the v4
> content and the fare source correction, publish a versioned zh-TW correction
> through the existing editorial flow, repin the resulting live source, resolve
> the formal pipeline's numeric-equivalence and verified Singapore food-directory
> link gates, then rerun current-head CI and a scoped import dry-run.

None of that happened. The content is now in `main`, so the next person who runs
a publish can ship it without ever seeing that sentence.

**Nothing is live yet.** #635 wrote repository content and images only; the four
new locales are unpublished and no production write was made. The exposure is
the *next* publish, not the current site.

**There is no code-level guard.** `guides-import --publish` publishes "each
imported locale whose public version differs from the pack"
(`apps/api/app/cli.py`), and there is no per-slug hold, no `skip_publish` and no
held-article list. A bare `guides-import --publish` over the packaged content
directory would ship both of these guides. This task is the hold.

### What is unresolved

1. **An unapproved source correction is in the zh-TW pack.** The published zh-TW
   v6 fare table said `40.2 km 以上` for 257 cents; `d52af4d9` changed it to
   `超過 40.2 km`, and wrote the matching boundary into all five locales
   (`超过 40.2 km`, `Over 40.2 km`, `40.2 km超`, `40.2 km 초과`). #635 cites
   SimplyGo Adult Fares putting 39.3–40.2 km at 256 cents and only **over**
   40.2 km at 257 cents. The direction looks right, but #635 itself states this
   correction "has **not** been published or independently approved", and the
   repository now disagrees with the live published source until it is.
2. **The batch010 validator gate is still open** —
   `2026-09-21-validate-equivalent-singapore-guide-numbers-and`: 112
   numeric/token warnings unresolved, two clear English SVG subtitle omissions
   and four condensed-duration fields awaiting an editorial decision, plus the
   verified-route filter rejecting `/foods?city=singapore`.
3. **No independent editorial review exists.** The PR carries zero reviews.

## Definition of done

- [ ] Both guides are either published deliberately after every item below is
      satisfied, or their unreviewed content is reverted from `main`.
- [ ] The Changi fare boundary is approved and published as a new versioned
      zh-TW source through the editorial flow, and the live source is repinned.
- [ ] The batch010 validator task is done. It is
      `2026-09-21-validate-equivalent-singapore-guide-numbers-and`, filed by PR
      #639, which had not merged when this task was written -- so it is named
      here rather than in `depends_on`, which only accepts tasks already on the
      board. Link it once #639 lands.
- [ ] An independent editorial review has accepted the v4 wording, eligibility,
      source facts and image legibility.

## Steps

- [ ] Until every box above is ticked, do **not** run `guides-import --publish`
      in a way that reaches these two slugs.
- [ ] Decide with the site owner whether to hold the content in `main` (current
      state) or revert `d52af4d9` and re-merge after review.
- [ ] Consider whether `guides-import` should grow a real per-slug hold, so a
      future unreviewed merge cannot be published by a bare `--publish`. A task
      file only stops someone who reads the board.

## How to verify

Before any publish that could touch these slugs, run the import with
`--dry-run` and confirm neither `singapore-4-day-itinerary` nor
`singapore-changi-airport-mrt-simplygo-guide` appears in the plan:

```
guides-import --dry-run --publish
```

To publish other guides while this hold stands, restrict the run with repeated
`--slug` arguments rather than importing the whole directory.

## Notes

`d52af4d9` changed 12 files, +4,953 / -21: both pack JSONs, eight new locale
SVGs, one existing SVG and the batch task file.

The `hold.py` mechanism in `ops/release/` is **not** the right tool here. It
blocks the whole deploy on the production host via
`/root/travel-scanner-deploy.hold`; it is not per-article and would stop
unrelated releases.
