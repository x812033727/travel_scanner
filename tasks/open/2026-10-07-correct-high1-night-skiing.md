---
id: 2026-10-07-correct-high1-night-skiing
title: Correct High1 night skiing claim in winter guide and diagram
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-07T05:44:19Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/korea-ski-resorts-2026-2027.json
  - apps/web/public/guides/korea-ski-resorts-2026-2027/diagram-1.svg
  - docs/article-localization/source-corrections/20261007-high1-night
---

# Correct High1 night skiing claim in winter guide and diagram

## Why

The published guide says High1 closes at 16:00 and offers no night skiing. Its own
cited official 25/26 ticket rules provide a 15:00 start valid through 20:00 after
16:00-18:00 grooming. KTO's daytime hours do not establish a no-night rule.
The source must be corrected before adding four missing translations.

## Definition of done

- [ ] Independently approve exact source-document and diagram corrections.
- [ ] Distinguish 25/26 ticket evidence from unannounced 2026/27 season hours.
- [ ] Apply through a hash/version-bound source-correction receipt and guarded release.

## Steps

- [x] Record the contradiction against the operator's primary evidence.
- [ ] Review document pointers /blocks/2/rows/4/3, /blocks/3/description and
      /blocks/14/text plus diagram text index 33 and matching SVG description.
- [ ] Make concise diagram wording readable at >=15px and render for review.
- [ ] Preserve all unaffected source/photos/assets and prepare corrected locale jobs.

## How to verify

Read https://www.high1.com/ski/contents.do?key=750 and the cited KTO page,
https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=251052.
Bind the genuine independent correction review to current public versions, before
and after documents/assets. Test source-correction verification and public output.

## Notes

- Independent finding SHA ad308609b7ac3c809f66078e410a98514c46fce3d497ed814ff716f5cd43cfdf.
- Source SHA 3b0d7c2566c5309780a3558aecbc7bd7ebadece602b577fcae00c754ec0b296f.
- Pack SHA 9e53d30f01d6312621847f37549637a11a7ea62a6e630a0ca2a39315c7e4c5b0.
- Operator evidence SHA a260c340731791a15cf2bb45c618d47c82df404d1b0d9be5731c448c03f26ef7.
- Diagram wording must remain season-qualified (for example, 25/26 票券含夜間；
  時段查官網), with no unsupported 2026/27 night-operation promise.
- A further primary-source audit found Yongpyong's 20-minute/16-km KTX travel
  example under a TAXI heading. Audit the guide's shuttle attribution across its
  body, accessibility description and citation before approving this whole source.
- No translation was started and no source/publication change was applied.
