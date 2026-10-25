# Korean independent caption and metadata text review

Status: FIXES_REQUIRED. Preparation-only text review; timing unverified.

Reviewed all 143 translated lines, 6 chapter names, title, full description, 6 tags and 3 thumbnail fields against the canonical Traditional Chinese source, visible slide facts, source mapping, glossary and worksheet text cue boundaries. This reviewer did not translate the material. Merged Korean text matches the reviewed worksheet text.

| id | problem | current | suggested |
| --- | --- | --- | --- |
| r305031 | Meaning / attribution: 發行人 in this prospectus-backed statement is the issuing company; 출판사 changes that attribution to a publisher. Keep the source's issuer qualification. | 출판사의 구상에서 구매자는 노트를 넘겨받으며 저자의 자리도 넘겨받습니다. | 발행사의 구상에서 구매자는 노트를 넘겨받으며 저자의 자리도 넘겨받습니다. |
| thumbnail:headline | Thumbnail meaning: 把空白賣全球 explicitly says the blank product is sold worldwide. The current slogan retains the world but drops selling. | 빈 페이지를 세계로 | 빈 페이지를 전 세계에 팔다 |
| r320012 | Readability: 이익 결말 is an unnatural noun combination in Korean and obscures the source's written-ending metaphor. Preserve the narrator's first-person opinion. | 저는 더욱 이렇게 생각합니다. 브랜드는 창작을 권하지만, 회사의 이익 결말까지 써 놓지는 않았습니다. | 저는 더욱 이렇게 생각합니다. 브랜드는 창작을 권하지만, 회사가 이익을 내는 결말까지 써 놓지는 않았습니다. |

The financial, date and historical qualifications checked include the 2013 market capitalization (not revenue), the 2016 whole-equity valuation (not cash received), 79 stores at the end of 2016, first trademark filing on 1997-11-26, the FY2025 report period, the 2013-scoped contracts and average production-to-launch interval, old notebook type versus modern brand, first-person opinions, partial shareholder-loan principal forgiveness, and the 2026 same-half comparison. No additional factual or cue-order fixes were identified.

The worksheet has no max_chars budgets. Ninety-one full line entries exceed the approximate 40-character Korean guide; this is a preparation flag, not a finding that required qualifications should be removed. Source text boundaries were checked for clause order only. There is no reviewed timed SRT or actual TTS timeline, so spoken pace, cue duration, splitting and actual fit still require later media review. This report is not media PASS, final approval or owner approval.

## Exact reviewed input SHA-256

- `canonical_video`: `/workspace/work/brand-story-20261025/c03-submission-root/docs/videos/story-everyday-moleskine-c03-remake-20261025/video.json` — `65ca1b602a5048e4f6af7c721bf1bd15abf152616c07d179f6ff5b6350c02005`
- `translation`: `/workspace/work/brand-story-20261025/c03-submission-root/docs/videos/story-everyday-moleskine-c03-remake-20261025/i18n/ko.json` — `2bf3d36cb1ec35872c5b81cc336534df315687564b92cad4dd958d191276f97d`
- `worksheet`: `/workspace/work/brand-story-20261025/media/story-everyday-moleskine-c03-remake-20261025/i18n/ko.todo.json` — `c7e3534006471f2cf0984f2094b43f8ca8c3bf0e2684b5633835ec3af245a5a8`
- `claims`: `/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c03/claims.md` — `eabe20e67a544eff53d10ed97fe3bdc1c9737a00041bba2f5d951943d73a57fb`
- `lexicon`: `/workspace/work/brand-remakes-source/docs/videos/lexicon.json` — `e91a7de47dfe80156ad3acb21b8a6ee02e6978d6bf085e42c926aa138f9c19d5`
- `review_prompt`: `/workspace/work/brand-remakes-source/.agents/skills/youtube-video/references/prompts/caption-review.md` — `e95c973686da098ea76dcbe4e3c41cbfe0148967e3a6f17840cd478ab3f3bd9a`

Verdict: ready after the fixes. Counts: meaning 1; facts 0; glossary 0; cue order 0; readability 1; budget 0; metadata 0; thumbnail 1.
