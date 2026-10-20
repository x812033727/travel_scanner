# Meta X05 `cut` Shorts — independent source audit

**Verdict: PASS** for the exact current Shorts bytes. Both drafts keep announcements separate from completed layoffs, and AI-glasses **category sales** separate from Reality Labs revenue, operating loss, and any product-level profit. No source-bound correction remains. Reviewed 2026-10-20; no paid calls or new source downloads.

| Reviewed file | SHA-256 | Source |
| --- | --- | --- |
| `shorts.json` | `52e2812e2bbf409b3edab3e935dcf65f3768e79b0e9c0522a898e0b9d024dfd2` | Two `cut` Shorts |
| `video.json` | `9ec57716a952185ef4ba17b50493b851c8b60223145a0606a40d07deaabab85c` | Shot source, 84 current scenes |
| `/tmp/x03-meta-2022-10k.htm` | `09c65f4c5cc2cf6b9b9c799c8f4c04045556a9567d508a0c2e8112d15a8aafb8` | [Meta FY2022 Form 10-K](https://www.sec.gov/Archives/edgar/data/1326801/000132680123000013/meta-20221231.htm) |
| `/tmp/meta-2023.html` | `d3b91050396da40656d06dadd75984cc9fcd5eeedde01f2d8a5ac6a8caff91f0` | [Meta FY2023 Form 10-K](https://www.sec.gov/Archives/edgar/data/1326801/000132680124000012/meta-20231231.htm) |
| `/tmp/meta-2025.html` | `279019755c4435c94ab42d86c39b914f57c5ef3d63aafde5c4b0867ddccf4fa2` | [Meta FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm) |

I parsed the saved original SEC HTML directly. Each Short's `links` URL exactly matches its named SEC filing and a `video.json` source URL. All twelve `shot` IDs resolve to current long-video scenes. The selected visuals represent layoff **notices**, year-end headcount, category sales directions, division costs, and the lack of product accounts without adding contradictory factual detail.

## Short 1 — FY2022 versus FY2023 headcount

The FY2022 filing says headcount was **86,482 at December 31, 2022, up 20% year over year**. It dates the approximately **11,000-person layoff announcement to November 2022** and says a **substantial majority** of the affected people were still included in that year-end reported count. FY2023 Note 3 says Meta announced **three rounds of planned layoffs in March 2023**, approximately **10,000** people, and had completed those layoffs by December 31, 2023; a small portion of affected employees could still remain in reported headcount into 2024. FY2023 reported headcount was **67,317, down 22% year over year**. Thus completion and the company-wide year-end count are separate facts, not a count of departures caused solely by either announcement.

| Current element | Result |
| --- | --- |
| Both titles and the description | **PASS.** “Meta 宣布裁員，年底員工數怎麼反增兩成？” and the alternate “兩次裁員公告…” correctly specify announcements. Description gives the FY2022 `+20%` and FY2023 `−22%` comparators, the approximately 11,000 and 10,000 scopes, and the FY2023 completion qualifier. |
| Hook `x05-b01-s04` | **PASS.** “宣布裁員，年末增兩成？” and both spoken phrases distinguish the 2022 announcement from the later reported company count. |
| Setup `x05-b03-s06` and turn `x05-b03-s08` | **PASS.** November timing, approximately 11,000 affected people, and most still in the year-end headcount are direct FY2022 filing statements. “公告不是每個人當天離職” follows from most remaining counted even at year-end. |
| Proof `x05-b04-s06` and payoff `x05-b04-s07` | **PASS.** March 2023, three planned rounds, approximately 10,000, completion by year-end, and company count down more than 20% agree with FY2023 Note 3 and Headcount. The Short does not assert that the announced layoffs alone explain the entire 22% decrease. |
| Loop `x05-b04-s08` | **PASS.** “公告日不等於離職日” summarizes the timing distinction; the final question asserts no further quantitative fact. |

## Short 2 — AI-glasses sales versus RL operating loss

The FY2025 filing compares **FY2025 with FY2024**: RL revenue increased **$61 million, or 3%**, driven by increased **AI-glasses sales** and partly offset by decreased **Meta Quest sales**. It separately reports RL operating loss `(19,193)` versus `(17,729)` **US$ millions**, so the loss magnitude increased **$1,464 million ≈ 14.6 億美元**. The filing attributes that wider **division** loss to higher personnel costs, estimated losses on non-cancelable purchase commitments **for RL inventory**, and technology development costs. It does not give AI-glasses unit growth, an individual eyewear model's revenue, or eyewear product-level profit/loss. The two changes cannot establish that eyewear caused the division loss.

| Current element | Result |
| --- | --- |
| Both titles and the description | **PASS.** The titles say AI-glasses **sales increased** and name RL as the loss subject or ask whether product profit can be calculated. The description gives the FY2024 comparator, `$61m` division revenue gain, about `14.6 億美元` wider **operating** loss, and expressly rejects assigning the loss to glasses. |
| Hook `x05-b01-s06` and setup `x05-b06-s01` | **PASS.** Headline “AI眼鏡銷售增，RL虧更深？” keeps category sales and division loss in distinct subjects; narration and setup state the FY2025/FY2024 sales directions without claiming units sold or causation. |
| Turn `x05-b06-s02` and proof `x05-b06-s04` | **PASS.** The `$61m` gain is explicitly **whole-RL revenue**. `14.6 億美元` is the change in **operating-loss magnitude**, and the three named cost categories match the FY2025 RL explanation. |
| Payoff `x05-b06-s08` and loop `x05-b05-s14` | **PASS.** The filing's disclosures are division-level; the Short correctly says they do not supply eyewear product P&L. The closing question uses “AI 眼鏡銷售增加” rather than claiming an undisclosed unit increase. |

**Corrections required:** none for this SHA. Re-audit if a title, headline, narration, description, source URL, or reused shot changes.
