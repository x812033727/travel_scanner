---
id: 2026-10-07-localization-japan-route-and-citation-guards
title: Support verified Japan and Korea routes and Japanese citation titles
status: done
priority: P1
area: tools
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T05:01:25Z
created_at: 2026-10-07T05:01:19Z
completed_at: 2026-10-07T06:11:02Z
branch: codex/article-missing-locales-20261007
depends_on: []
scope:
  - tools/article-localization/pipeline.py
  - tools/article-localization/test_pipeline.py
  - tools/article-localization/README.md
  - .agents/skills/article-localization/references/pipeline.md
  - docs/article-localization/route-verification-20261007.json
---

# Support verified Japan and Korea routes and Japanese citation titles

## Why

The all-missing-languages pilot cannot materialize valid Japan translations:
Tokyo, Osaka/Kyoto, Seoul and Jeju links are absent from the verified-route list,
and Japanese official citation titles embedded in a zh-TW source are incorrectly
flagged as copied untranslated prose. These are preparation gates, not production outages.

## Definition of done

- [x] Verify four destination routes in all five public languages with no redirects,
      correct html lang/canonical and substantial actual content.
- [x] Localize only these verified exact routes; queries, fragments and unapproved routes still refuse.
- [x] Preserve an already-Japanese official citation title for ja without exempting body prose or Chinese titles.
- [x] Demonstrate regressions fail before the change and focused tests pass afterward.
- [ ] Include the guarded change and sanitized route proof in a reviewed PR.

## Steps

- [x] Audit active scopes and PRs for pipeline.py; no active task/PR overlaps.
- [x] Read all twenty public route responses and pin raw HTML/content hashes outside repo.
- [x] Add four routes, the citation-title exception and regression coverage.
- [x] Run all 33 pipeline tests and scoped ruff checks successfully.
- [x] Obtain independent code review of 58 positive/negative cases.
- [ ] Pass applicable CI checks on the exact content PR head before merge.

## How to verify

Run `tools/article-localization/test_pipeline.py` and scoped ruff. The route test
checks all five target locales, both link locations, untouched citations/external
URLs and rejection without output artifacts. The citation test accepts the actual
Japanese official title while rejecting the same copied text in body prose and
an untranslated Chinese source title. Route response proofs are committed in
`docs/article-localization/route-verification-20261007.json`.

## Notes

- Fresh route proof checked 2026-10-07T05:00:49.793810+00:00, private evidence SHA
  `f8c3eceafe8518aff1f3e8a71fc5d50c67395fd88f0c4ac17763e1488f0e502d`.
- Twenty selected URL responses: HTTP 200, no redirect, exact locale/canonical,
  real localized H1 and body. Additional verified routes are not automatically allowed.
- Final public proof SHA 123c7c8a1256857eaad685da2bfc9f9a4bd38482a3985bae4d9ec03e4e022564.
- Independent final review SHA d01a1ad27bb9850154f8f2fa71525d55d9c4f9c5c5f6681a80727b781ad1015b.
  Numeric/URL/code validator ASTs remain unchanged. Query, fragment, wrong host,
  trailing slash and unapproved routes still refuse; copied body text still refuses.
- The two regressions failed against the previous tool (one failure, one error).
  All 33 tests pass after the change; scoped ruff passes.
- Numeric/URL/code-token guards remain strict. Independent translation corrections
  retain written-out number forms where the original source uses words.
- Existing immutable job inputs and attempt logs remain untouched. `materialize`
  rechecks corrected translated-fields and newly verified routes without another model call.
- A separate source-audit finding in the refund article prevents that article's
  release; the new tool behavior does not override source review or publication holds.

### Content PR handoff

PR: https://github.com/x812033727/travel_scanner/pull/1365.
Authoring, exact independent review, local validation and local installation/replay
are complete for this ticket's selected scope. Required GitHub checks and merge
remain enforced PR gates; marking this authoring ticket done does not claim those
checks are green. The PR remains draft pending owner approval.
Production deployment, publication and public desktop/mobile verification remain
open in 2026-10-07-release-localized-travel-life-wave-20261007.
Any unchecked CI/merge/publication lines above are handed to those explicit gates,
not waived or reported as completed.
