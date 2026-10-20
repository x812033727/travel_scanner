# X14 Airbnb frozen-script independent source audit — HOLD

Audited 2026-10-20 UTC. **HOLD for the long film and therefore the frozen package.** The two Shorts, long-film numeric cards, thumbnail, and YouTube metadata have no separate material source blocker. Two long-film narration passages need correction and a new frozen hash before source clearance. This is a source verdict, not an assessment of TTS, final pictures, or production readiness.

I read the repository `AGENTS.md`, the brand-story rules and `youtube-video/references/story.md`, then `source-matrix.md`, `line-source-matrix.md`, `shorts-source-matrix.md`, and the frozen `video.json` and `shorts.json`. I did not use the earlier `reviews/source-audit-independent.md`, `treatment.md`, or author notes to reach this verdict. The frozen file SHA-256 values match the assigned bytes:

| Artifact | SHA-256 | Checked scope |
| --- | --- | --- |
| `video.json` | `9eccafcb326cebca68d266114d744fbae3fa8c770aa20f081d6dd8e28e7ff8ce` | 133 scenes, 135 narration lines, 30 stats cards, thumbnail, title/description/tags, source URLs |
| `shorts.json` | `d678fd8db68586aeb2b64220004069d4c0e5ca023732841777ba33b7054edfaa` | 2 Shorts, 16 narration/headline pairs, titles/descriptions/links |

I independently downloaded the **exact SEC URLs** in `source-matrix.md` with HTTP 200 and computed hashes over the response bytes, not extracted text. All four match the matrix:

| SEC original | Downloaded bytes | Downloaded SHA-256 |
| --- | ---: | --- |
| [A1, 2020 Form 10-K](https://www.sec.gov/Archives/edgar/data/1559720/000155972021000010/airbnb-10k.htm) | 2,521,385 | `253c29e43012a62bf28b46ca69538d06994173398a49efa0e8a0b4d5d29f4331` |
| [A2, 2020 Q4 shareholder letter](https://www.sec.gov/Archives/edgar/data/1559720/000119312521056952/d147144dex991.htm) | 427,883 | `9cab0c90a7dee23d2663103af33ad9d11234ac383eefeca528e1f63b0376be33` |
| [A3, 2021 Q4 shareholder letter](https://www.sec.gov/Archives/edgar/data/1559720/000119312522043371/d251410dex991.htm) | 508,751 | `49605a7f787f9bd5fc9c30b58c3e9b35c13fb4f03f75ea676530ca20910e23be` |
| [A4, 2022 Q4 shareholder letter](https://www.sec.gov/Archives/edgar/data/1559720/000119312523039008/d451233dex991.htm) | 510,232 | `2e8d8f02457f3faf05c02555e365532f8b32b5cd60dd410b7a585e074c832ca1` |

## Blocking findings

1. **Guest refund eligibility is conflated with host support eligibility** (`x140302`–`x140308`, especially `x140304`, `x140306`, `x140307`). The narration introduces the extenuating circumstances cancellation policy, says a check-in **must** be March 14–May 31, then says June check-ins are outside that window and moves directly to what an eligible guest can receive. A1 distinguishes two rules. Its guest-policy paragraph says guests who booked on or before March 14 and could not travel due to the pandemic were eligible for a full cash refund or, in some cases, travel credit. Its separate host-support paragraph says **“The reservations eligible for this $250 million host program”** had a March 14–May 31 check-in date. A1 does not establish that a June check-in was outside guest refund eligibility. The May 31 cutoff and the June counterexample must be explicitly attached to the **US$250m host support program**, and the guest refund explanation must be kept separate. The source matrix itself describes the cutoff as a host-support condition; the frozen narration crosses that boundary.

2. **Nearby and long-stay demand growth is given an unsupported full-year scope** (`x140416`–`x140418`; `x140415` sets the context). The narration says demand within 50 miles, 50–300 miles, and for long stays was above the prior year “當年”, without a second-half limit. A1 says **“starting in the second half of 2020, demand from guests grew year-over-year”** for precisely those three categories. It does not supply a full-calendar-2020 comparison for them. State that the year-over-year growth began in the **second half of 2020**, with the same period comparison, in the spoken line(s). This period qualifier is material because the film otherwise uses explicit full-year 2020 numbers nearby.

## Remaining claim checks

The 135 long-film narration lines match `line-source-matrix.md` by ID and text; the 16 Short narrations match `shorts-source-matrix.md` by text. I checked every material number and period in those lines and in all 30 stats cards against A1–A4, including the following boundaries:

- A1 describes March–April 2020 cancellations of nights and experiences exceeding **gross** new nights and experiences booked **during those months**. The opening, repeated narration, thumbnail shorthand, and long YouTube description do not turn that into an annual net-negative claim; the narration and description explicitly state the two-month scope.
- The 2019/2020/2021/2022 annual **net Nights and Experiences Booked** figures are 326.9m / 193.2m / 300.6m / 393.7m. The 2020 decline is 41%. The film and cards keep these separate from GBV, revenue, guest counts, and Q4 **gross nights booked** shares. A1 gives 2019/2020 revenue US$4.805bn / US$3.378bn (about −30%) and a 6% increase in GBV per net Night and Experience Booked as a partial offset; the narration attributes that explanation to the company.
- A1 states **up to** US$250m for eligible hosts; the 25% base is what a host would have received under their own cancellation policy. The US$17m Superhost fund is separate. The US$205.1m 2020 payments are primarily for hosts under the extenuating circumstances policy and are a revenue reduction, not identified as the total payout of the US$250m commitment. The hypothetical 100 → 40 → 10 cards are marked as an example, and their arithmetic is correct. The blocker above concerns only the spoken transfer of the host program's date window to guests.
- A1 reports approximately 5.6m active listings at both 2019 and 2020 year-end; A4 reports 6.6m at 2022 year-end. The script and cards avoid treating these totals as a cohort retention measure. A1 supports the April 2020 US$2bn term loans, May reduction of about 1,800 employees (about one quarter), marketing/investment cuts, and promotion of local/non-urban stays. Loans are identified as financing, not revenue. The product decision is not claimed as an isolated cause of 2022 profit.
- The approximately US$4.6bn **2020 full-year GAAP net loss** includes about US$2.8bn of IPO-triggered RSU expense and US$868.5m of **full-year** noncash warrant remeasurement (A1). The Shorts and long film do not substitute A2's US$827m **Q4-only** warrant figure or infer a residual “true pandemic loss”.
- A3 gives 2021 Q4 **gross nights booked** shares of 22% for stays of at least 28 nights versus 16% in 2019 Q4, and over 90% of active listings accepting 28-night-or-longer stays at 2021 Q4 end. Its 2021 Q4 US$55m net profit is kept distinct from the full-year US$352m net loss. A4 gives 2022 Q4's 21% long-stay share, 44% cross-border share versus 47% in 2019 Q4, and 51% high-density urban share versus 59% in 2019 Q4. A4 also gives 2022 revenue US$8.4bn (up 40%) and GAAP net income US$1.9bn, its first full profitable year. The second Short's title, description, narration, and on-screen headlines preserve those periods and avoid assigning profit to long stays alone.

Minor spoken clarity after the blockers are fixed: `x140513` says “這類長住” after mentioning both >7-day stays and ≥28-night stays. The adjacent `x140512` and card show that ≥28 nights is intended, but repeating “二十八夜以上” in the narration would make the >90% listing-setting denominator unmistakable to audio-only viewers.

**Re-audit trigger:** correct the two blocking passages in the final `video.json` and its source-bound script/matrix, regenerate the frozen SHA-256, and check any affected on-screen or metadata text before a PASS receipt. The Shorts are factually clear at their current hash; if their bytes change, they need renewed checking too. I changed no script or JSON.
