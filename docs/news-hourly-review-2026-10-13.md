# New hourly AI news holds — 2026-10-13

## Scope and baseline

Owner selected new arrivals from 2026-10-11 onward. The 2026-10-07 and
2026-10-10 backlog cohorts remain with their existing owners; no old candidate
was retried or decided here. The authenticated `/zh-TW/admin/news` read at
11:34 Asia/Taipei showed **50 review, 25 redraft, 3 execution failures, 592
published, 933 rejected** across *all* cohorts. These are not new-cohort
totals. The scanner, automatic mode, AI judge and AI/TECH/CRYPTO auto-publish
switches were on. The current judge was Claude Opus 5.5.

The new held candidates identified on the queue were Evernorth, Bitmine,
Clarity and Apple/Huxe in review, plus Meta Muse in redraft. Queue labels show
source dates, which are not candidate arrival dates: the Huxe source is dated
October 10, but its saved Guide article was created October 11 at 04:47:45
Taipei. This is an exact-ID operating receipt, not a census of all news
produced since October 11.

## Decisions and persisted evidence

| Candidate | Decision and readback |
| --- | --- |
| [Evernorth](https://mokaair.com/zh-TW/admin/news?queue=published&tab=review&candidate=392499e0-d820-4676-aba7-f01b06632527) `392499e0-d820-4676-aba7-f01b06632527` | Saved article `541bb635-d186-4bb0-b45a-410f11f9d237`, zh-TW version 2 at 11:35. Changed the lock-up reference from selling to transfer restrictions, rewrote the neutral company-holdings description, and removed a redundant disclaimer callout. Clicked `重新查核` once. Readback: all five hard checks clear, `AI 代審・最後一關: 發布`, candidate `已發布`, site published count 593. |
| [Bitmine](https://mokaair.com/zh-TW/admin/news?queue=rejected&tab=review&candidate=02207914-e20f-4b3d-93b3-b041083de817) `02207914-e20f-4b3d-93b3-b041083de817` | Rejected with reason: the article is primarily about ETH accumulation, a 5% holding goal, a projected time to goal and staking returns. A synonym swap would only evade the `買進` hard check. The six-week estimate is a media extrapolation, not a company commitment. Readback toast said `已退件，移到「已退件」清單`; rejected count rose 933 → 934 and review count fell 49 → 48. Saved five-locale article `9bc62613-e018-4786-89a5-3230efdefd85` was never published. |
| [Clarity](https://mokaair.com/zh-TW/admin/news?queue=published&tab=review&candidate=08ff40b0-30a1-4944-bc9c-bce7a0ff336d) `08ff40b0-30a1-4944-bc9c-bce7a0ff336d` | AI hand-back identified Derek Lowrey's statement wrongly attributed to CoinDesk in zh-TW, en and ja. The stored evidence explicitly attributes it to Lowrey. Edited only the relevant paragraph in each locale of article `1a34de91-cb86-44c6-b2f0-eb67da1d9e78`. Readback: zh-TW v2 11:40:24, en v2 11:40:52, ja v2 11:41:18, all unpublished at save. Clicked `重新查核` once at ~11:42; the AI final judge then approved publication. Readback: `已發布`, five public article links, site published count 593 → 594. |
| [Meta Muse](https://mokaair.com/zh-TW/admin/news?queue=rejected&tab=review&candidate=eed553a6-baaa-4e03-b5bc-449d10c54c97) `eed553a6-baaa-4e03-b5bc-449d10c54c97` | This Decrypt report was held at `news_locale_review_failed` for zh-CN and incorrectly categorized CRYPTO. Before a paid rewrite, compared it with the already [published The Verge article](https://mokaair.com/zh-TW/life/ai-news-meta-muse-wonder-models-20261012): both cover the October 12 Muse Wonder / Wonder Full launch, Muse Code / API access and Meta's performance claims. Decrypt adds benchmarks and prices, but no separate launch event. Rejected with an audited same-event reason; readback: `已退件`, redraft count 25 → 24, rejected count 934 → 935. Existing public article still rendered. No new Guide article was generated. |
| [Apple/Huxe](https://mokaair.com/zh-TW/admin/news?queue=published&tab=review&candidate=b5eb2cd8-f007-454f-b2ad-694e945f9cde) `b5eb2cd8-f007-454f-b2ad-694e945f9cde` | Guide `d6ac9cdd-56de-44e6-aef9-b9dbe13d65a9` was created October 11. The AI judge found that zh-TW summary/table and ja table described Huxe's planned app removal, service stop and user-data deletion as completed. Corrected those exact passages and saved zh-TW v2 at 11:50:55 and ja v2 at 11:51:22. Normal `重新查核` returned `source_content_changed` for TechCrunch; the live candidate had all five hard checks clear but was still held. Clicked `用最新來源重新查核` once with an audit reason and the corrected saved five-language article. Readback: `查核: 通過`, all five translation reviews passed, `AI 代審・最後一關: 發布`, candidate `已發布`, published count 594 → 595. |

## Public-page checks

For Evernorth, the public [zh-TW](https://mokaair.com/zh-TW/life/crypto-news-evernorth-nasdaq-listing-20261012), [zh-CN](https://mokaair.com/zh-CN/life/crypto-news-evernorth-nasdaq-listing-20261012), [en](https://mokaair.com/en/life/crypto-news-evernorth-nasdaq-listing-20261012), [ja](https://mokaair.com/ja/life/crypto-news-evernorth-nasdaq-listing-20261012) and [ko](https://mokaair.com/ko/life/crypto-news-evernorth-nasdaq-listing-20261012) pages all rendered an article heading, summary and FAQ in the browser. zh-CN and en initially hit `429 Too Many Requests`, then rendered normally on a later read.

For Clarity, the public [zh-TW](https://mokaair.com/zh-TW/life/crypto-news-us-regulators-after-clarity-20261011), [zh-CN](https://mokaair.com/zh-CN/life/crypto-news-us-regulators-after-clarity-20261011), [en](https://mokaair.com/en/life/crypto-news-us-regulators-after-clarity-20261011), [ja](https://mokaair.com/ja/life/crypto-news-us-regulators-after-clarity-20261011) and [ko](https://mokaair.com/ko/life/crypto-news-us-regulators-after-clarity-20261011) pages all rendered an article heading, summary and FAQ. The corrected Lowrey sentence was read back on zh-TW, en and ja public pages.

For Apple/Huxe, the public [zh-TW](https://mokaair.com/zh-TW/life/ai-news-apple-huxe-deal-20261010), [zh-CN](https://mokaair.com/zh-CN/life/ai-news-apple-huxe-deal-20261010), [en](https://mokaair.com/en/life/ai-news-apple-huxe-deal-20261010), [ja](https://mokaair.com/ja/life/ai-news-apple-huxe-deal-20261010) and [ko](https://mokaair.com/ko/life/ai-news-apple-huxe-deal-20261010) pages all rendered an article heading, summary and FAQ. The corrected future-planned wording was read back in the zh-TW summary and table and ja table.

## Boundary candidates not changed

Two October 10 source-dated redrafts remain unassigned to this operation:
[chatbot safety research](https://mokaair.com/zh-TW/admin/news?queue=redraft&tab=review&candidate=3dd103c9-684f-4712-a3bd-e1715d9dc8b9)
`3dd103c9-684f-4712-a3bd-e1715d9dc8b9` and
[Visa stablecoin study](https://mokaair.com/zh-TW/admin/news?queue=redraft&tab=review&candidate=e0fee63a-ce83-4d71-b6a7-c5093001b227)
`e0fee63a-ce83-4d71-b6a7-c5093001b227`. Their source or event dates
cannot establish candidate creation time. The older 208-ID cohort snapshot was
captured October 10 at 08:36 Taipei, but its exact-ID file is unavailable;
the admin list displays event date when present and its run tab omits start
times. The user selected October 11 onward, so neither candidate received a
new paid run, publication or rejection here. This is an ownership/time boundary,
not an approval of either draft.

## Operating constraints and follow-up

- A single batched, read-only production SSH census was automatically denied
  with `blocked by policy` and no more specific reason. No alternate SSH
  command was attempted. The admin browser supported bounded per-candidate
  work but does not expose candidate creation times for the two boundary cases.
- Do not infer backlog completion from the queue totals; most visible holds
  belong to the separately owned older cohorts. After these five decisions,
  the live *all-cohort* snapshot was 46 review, 24 redraft, 3 failures, 595
  published and 935 rejected.
- The fixed Decrypt feed's wrong CRYPTO classification can hide duplicates of
  published AI articles: `duplicates.py` screens within the candidate's
  vertical. This same-event miss is filed as
  `tasks/open/2026-10-13-detect-duplicate-hourly-news-events-across.md`.
  Candidate-category correction remains separately tracked in
  `tasks/open/2026-10-10-add-audited-held-news-category-correction.md`.
- A separate [draft PR #1479](https://github.com/x812033727/travel_scanner/pull/1479)
  fixes false positives for reported or negated crypto trading words. It is
  not merged or deployed and did not change these candidate outcomes.
