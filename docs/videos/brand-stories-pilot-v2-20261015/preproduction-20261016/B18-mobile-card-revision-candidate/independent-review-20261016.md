# B18 `idea-s027` mobile card: independent review

Reviewed 2026-10-16, read-only against the isolated candidate. **Limited PASS for this one static card.** I did not approve the authored chapters, source claims, full film, host import, or paid production.

## Exact change and render

- I reran `verify.mjs` locally. It confirmed source `idea.json` SHA-256 `159a25dc1a13ac1247467507064625f3599db535500c67a88c490cebaff763b1` and source synthetic `video.json` SHA-256 `3e39c24f64b1a719fa338db39578fbf1e31f1f95058b66c8544f934f3bffff7e`.
- Independent `git diff --no-index` comparisons of each source JSON against the generated temporary output show exactly one changed field in each file: `idea-s027.data.subtitle`, from `兩份沿革記載\nJ-Net21 記載\n發明協會記載` to `兩份資料，兩種說法`. Titles, source badge, lines, claims, and other scenes are unchanged.
- Revised temporary `idea.json` SHA-256: `fed58f73da9ec724cc6151b36ad806e62013eefe0db97d0914de702c0b3c4121`. Revised temporary `video.json`: `a95537f505e42d0f731b3280bf63fc543aea7e8906c8293e1a95decb09ebfd3e`.
- Official renderer reported `renderer_problems: []`. The regenerated 320×180 PNG SHA-256 is `2c777428a427d93fb1bde88461c732bb5854d96e951d51c6c05a7ec3e7bc3dd5`, matching the saved `idea-s027-320x180.png`; full frame SHA-256 is `67dd10c38773016eca8a626a7e31ff9d7b79ad3be9941b00f0b2878b3be6c00b`.

## Visual and attribution verdict

At the image's native 320×180 size, the main title, one-line subtitle, and `J-Net21／發明協會` badge are readable and do not clip or overlap. The shorter subtitle states that two accounts differ, without presenting them as one established event. The unchanged title and badge still name both publishers. Adjacent narration in `idea-s027` through `idea-s030` attributes the playing-card account to J-Net21, the business-card account to the invention association, and says the two records cannot identify one unique moment. This checks the candidate's internal attribution and wording; it does not independently verify either external source.

## Remaining gates

This is one static-card check. Full-cut display duration, captions covering the card, and player playback remain untested. The B18 authored candidate still has 65 `UNCHECKED` claims, and its #1518 chapter adoption blockers remain. No source approval, production media, paid call, import, or publication follows from this review.
