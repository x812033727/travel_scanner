---
id: 2026-10-07-enable-verified-sapporo-localization-route
title: Enable verified Sapporo localization route
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-07T08:30:15Z
completed_at:
branch:
depends_on:
  - 2026-10-07-enable-verified-hong-kong-localization-routes
scope:
  - tools/article-localization/pipeline.py
  - tools/article-localization/test_pipeline.py
  - tools/article-localization/README.md
  - docs/article-localization/route-verification-sapporo-20261007.json
  - .agents/skills/article-localization/SKILL.md
  - .claude/skills/article-localization/SKILL.md
  - .agents/skills/article-localization/references/pipeline.md
---


# Enable verified Sapporo localization route

## Why

The Sapporo2027 festival source links to /destinations/sapporo, which the current
localization guard correctly refuses because it is not yet in its verified list.
Five real public destination pages have now been checked, but proof alone has
not changed the guard. Add this one route without expanding query/fragment rules.

## Definition of done

- [ ] Only literal /destinations/sapporo is admitted for the five proven locales.
- [ ] Existing query, fragment, malformed host/path, alias and port refusals remain.
- [ ] Meaningful full-materialization tests prove correct locale replacement and
      preservation of external source/citation URLs; refused cases write nothing.
- [ ] Genuine independent code review, applicable tests and skill-twin checks pass.
- [ ] Public-safe route proof retains actual status, HTML language, canonical,
      source/body hashes and a genuine paced capture timeline.

## Steps

- [ ] Recheck current main/PR/worktree ownership after the Hong Kong tool task lands.
- [ ] Adopt only verified public-safe five-language proof; preserve raw captures.
- [ ] Add one route, update the counted policy and test/refusal evidence.
- [ ] Independently review and record exact code/content hashes.

## How to verify

Run the actual pipeline unit tests, Ruff and applicable artifact/skill checks.
Verify all five public route bodies and metadata, not merely200 shells. Do not
reuse an old target review if a final materialized job or tool input changes.

## Notes

Five-route public proof SHA:
`a438cc3f266b095d88e30b2661d80af915c7237f4398ade2e40d856e4429e842`.
Actual old-guard refusal proof SHA:
`fe0e5a13b3a87cd8ca4ee8ebad97759fd600196864a16d23b1cac663ebbef162`.
The festival full-source PASS receipt SHA is
`45ac79cf4a321732be412a2c0ba2fe1ca18e10031fc915f1bbf9b1447aaadf65`.
This source PASS does not approve target translations, code or publication.

The separate existing repo /description rewrite still needs genuine repository
preservation admission before assembly. Historical2026 venue/zoo information is
explicitly labelled as precedent, not a2027 promise. The actual source image is
legible despite preserved small mechanical text-rectangle intersections; the
review read visible ink, not just the warning list. This open dependency task is
outside the fixed14-article wave3 cohort and changes no article by itself.
