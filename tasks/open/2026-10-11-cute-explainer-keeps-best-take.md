---
id: 2026-10-11-cute-explainer-keeps-best-take
title: Cute explainer keeps the judge's best take, as illustrated slides do, instead of blocking at keyframes
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-11T04:01:55Z
completed_at:
branch:
depends_on:
  - 2026-10-11-cute-explainers-own-series-prompts
scope:
  - tools/video/automation/flow.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/review/sync.mjs
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/review/sync.test.mjs
  - docs/videos/DRAMA-FLOW.md
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Cute explainer keeps the judge's best take, as illustrated slides do, instead of blocking at keyframes

## Why

On the illustrated-slides route a picture that still fails the judge after its takes is kept as
the best take (`--accept-best`) and listed for the owner. The drama route has no such path, and
the cute explainers of `2026-10-11-cute-explainers-own-series-prompts` run on the drama route: `flow.mjs` calls `acceptBestPictures`,
which returns null unless `illustrated(video)`; `media/keyframes.mjs` refuses `--accept-best` for
a non-illustrated video; `review/sync.mjs` `acceptedPicturesOf` lists kept pictures for
illustrated videos only. So a cute explainer with one shot of 100 to 140 that still fails after
3 takes x (1 + 2 prompt fixes) blocks with `prompt_fixes:keyframes` and waits for the owner's
retry ([`docs/videos/explainer-route/DESIGN.md`](../../docs/videos/explainer-route/DESIGN.md) section 5.2, "Pictures that keep failing", and 5.6). The three local pilots
were measured as slides, where about 80% passed on the first take and the rest could be kept.
The design left the code alone on purpose (option (b)): extending the three predicates also
changes which cuts are sent for manual review (`keyframes.mjs` warns that a drama's kept shot
could have its storyboard and cut approved on arrival with nobody asked to look), `sync.mjs` is
bound by the duration receipt, and none of it was prototyped.

## Definition of done

- [ ] A cute explainer (`isCuteExplainer(doc)`) keeps the judge's best take under the same
      conditions as an illustrated video, in the three places named above.
- [ ] A kept picture of a cute explainer is routed to manual review: its storyboard and cut are
      never approved on arrival without the owner being asked to look.
- [ ] A cast drama and `flat-explainer` behave exactly as before.
- [ ] Tests for the three predicates and the review routing; `docs/videos/DRAMA-FLOW.md` says
      which routes keep a best take; the receipt re-issued by an independent agent.

## Steps

- [ ] Ask the owner first whether the slides route's behaviour is wanted here (design section 9
      lists it as theirs to overrule), with the count of blocks seen on the first host episodes.
- [ ] Read the warning at `acceptBest` in `media/keyframes.mjs` before touching the predicate.

## How to verify

`node --test tools/video/media/look-keyframes.test.mjs tools/video/review/sync.test.mjs`; on the
host a cute episode with a failing shot reaches the keyframe gate with that shot listed as kept.

## Notes

- 2026-10-11 filed from the design's section 7, item 1.
