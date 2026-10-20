# X08 v10 independent blind narrative review

**Verdict: FAIL.** Nine of the twelve required `NARRATIVE_PANEL` checks pass; `one_line`, `no_recap`, and `no_detour` fail. The optional chapter-title check passes. I read only the frozen `video.json`, `shorts.json`, `script.md`, and the `NARRATIVE_PANEL` contract. This is a narrative and scene-data review, not a source audit or a rendered-media review.

| Frozen artifact | SHA-256 | Match |
| --- | --- | --- |
| `video.json` | `51185ca049c60cac3f009457a833b449f66bfafeb10fae8a5dee6076a94ea619` | PASS |
| `shorts.json` | `440ceee9649b30af2bd64ff1205bf38bff47d0be381b1b544cccff4601e2d543` | PASS |

## Panel scores

| Check | Required | Score | Evidence and judgment |
| --- | --- | --- | --- |
| `scene_first` | Yes | PASS | `x080101` / `x08-b01-s01` opens on a dated filing at a Toronto court; `x080102` immediately places the still-open stores in that moment. |
| `no_spoiler` | Yes | PASS | The filing in `x080101` is a flash-forward, but `x080103` holds back what happens to the stores, while `x080108–x080109` withhold the margin and holiday outcomes. The first chapter does not disclose those later results. |
| `one_line` | Yes | **FAIL** | After the May 2 closure at `x080510` / `x08-b05-s10`, `x080512` explicitly says “回到一月的退出決定”; chapter 6 then resumes FY2014 exit accounting at `x080601` / `x08-b06-s01`. That is a second rewind after the permitted opening flash-forward. The 2012 cost return at `x0803a04` is a smaller earlier example. |
| `no_toc` | Yes | PASS | `x080512` asks which cost the January decision put on the books; it is a story question, not an outline of sections. No narration line announces a numbered agenda. |
| `chapters_link` | Yes | PASS | The first lines pick up live objects/questions: leases `x080107→x080201`, opened stores and sales `x080234→x080301`, possible improvement `x080318→x080401`, board decision `x080443→x080501`, and exit charge `x080512→x080601`. The last link is clear despite its chronological rewind. |
| `open_loops` | Yes | PASS | Store fate `x080103`, annual margin `x080230`, next-year cost coverage `x080312`, holiday result `x080439`, and impairment cause `x080604` keep questions open across the body. The longest gap between spoken question lines is roughly 192 nonspace characters (`x0803a03→x0803a10`), well short of 90 seconds at ordinary narration pace. |
| `payoffs` | Yes | PASS | The seasonal test at `x080109` gets a specific negative answer at `x080440`; cost coverage at `x080312` gets the FY2014 shortfall at `x080435–x080438`; the open stores from `x080102–x080103` are closed by `x080510`, with `x080502` explicitly recalling the opening filing. The final audience dilemma `x080616` is a discussion prompt, not a withheld event result. |
| `no_recap` | Yes | **FAIL** | `x080310` already gives FY2013 selling, general and administrative expense as about US$910m. `x0803a05` says the same FY2013 figure again without an explicit callback. `x0803a06` also computes the already-established margin/expense gap, which `x080438` later repeats as a comparison. |
| `chapters_are_events` | No | PASS | The six titles name filing, lease purchase, disappointing sales, operational changes, board approval, and the exit charge reveal (first lines `x080101`, `x080201`, `x080301`, `x080401`, `x080501`, `x080601`). They are actions or findings rather than generic functions. |
| `outro_no_next` | Yes | PASS | `x080617` asks for a subscription but does not name a next video, episode, or file. |
| `opening_hooks` | Yes | PASS | After the filing scene, at least three distinct results remain unresolved: store fate `x080103→x080510`, whether the promising early margin survives `x080108→x080305`, and the holiday test `x080109→x080440`. `x080110` adds the larger “why Canada?” question. |
| `one_thread` | Yes | PASS | The Canadian store network's ability to pay for itself remains identifiable from the open stores and leases `x080102–x080107`, through inventory and operating losses `x080306–x080311`, to the board and exit `x080440–x080501`. The employee trust at `x080505–x080509` resolves a stake introduced at `x080105`. |
| `no_detour` | Yes | **FAIL** | `x0803a01–x0803a09` interrupts the move from FY2013 results to FY2014 action with another accounting pass: floor area, FY2012 and FY2013 SG&A, their gap, two depreciation figures, and two interest figures. Its uninterrupted run of figures largely reworks the cost problem already established at `x080309–x080311`; the narrative only resumes with the next-year inventory question at `x0803a10`. |

## Story and packaging observations

The opening is 202 nonspace characters, about 7% of the 2,877-character long narration. Proportional to the declared 8–11 minute target, that projects to roughly **34–46 seconds**, within the requested 30–60 seconds; actual TTS timing is not present in the allowed artifacts. It starts in a concrete scene and carries at least three real unanswered outcomes. Its many hooks are distinct enough to follow, although `x080107–x080110` stacks four hints/questions in quick succession.

Question marks recur about every 20–25 seconds on a rough 4–5 characters/second reading, with the largest gap around 38–48 seconds (`x0803a03→x0803a10`). This meets a 30–45 second hook cadence in substance and easily meets the panel's 90-second ceiling, but several neighboring questions feel mechanical: `x080208` asks whether stores can open on time, then `x080210` asks when they will open; `x080230` asks whether early margin lasts, then `x080304` asks nearly the same question before the answer. The dense FY2012/FY2013 cost passage makes that cadence feel like interrogation around a list.

The main “why” is eventually supported by new facts: disappointing sales and clearance `x080301–x080307`, gross margin below operating expense `x080309–x080311` and `x080435–x080438`, a holiday season without the needed lift `x080440`, and management's no-profit-before-2021 assessment `x080441`. The final answer `x080615` is accurate as a synthesis within the story but adds no new causal detail; the stronger payoff is spread across those earlier beats. The last three spoken lines are synthesis `x080615`, an audience choice `x080616`, and a generic subscription CTA `x080617`. The CTA follows the audience question immediately, so the last emotional beat is weaker than the decision itself.

The January/May ordering is the clearest continuity break: `x080501–x080503` covers January 14–15, `x080510` jumps to the May 2 all-closed status, then `x080512–x080601` sends the viewer back to January/FY2014 for the exit charge. The chapter 6 handoff is verbally explicit, but it still asks the viewer to replay the decision after the closure outcome has been delivered.

Most stats cards display a figure on the same scene as its spoken reveal: `x08-b03-s05` (14.9%), `x08-b04-s24` (+1.6%), and `x08-b06-s01` (US$5.105b) do not expose a later chapter's result. Two presentation choices do preempt local suspense. The chapter 5 title **「董事會批准停止加拿大營運」** answers `x080443` (“董事會會繼續等嗎？”) before `x080501` speaks the answer. The prompt for `x08-b04-s35`, displayed with `x080435–x080436`, depicts a cost stack already larger than the sales tally before `x080438` states the shortfall. `x08-b04-s32` also repeats the FY2013 US$1.317b sales figure in its label after `x080302` gave it. The other inspected prompts use anonymous objects or withheld folders and do not visibly disclose later numeric results.

## Standalone Shorts

| Short | Length from text | Standalone judgment |
| --- | --- | --- |
| `story-everyday-target-x08-short-1` | 191 nonspace narration characters; roughly 38–48 seconds at 4–5 characters/second, before pauses. **25–55 seconds plausible, unverified.** | **PASS with caveat.** The six beats answer the narrow title question: the 133 stores did not close on announcement day, and all were closed by May 2 (`x08-b05-s04`, `x08-b05-s11`). It correctly avoids inventing the exact last-store date. The first beat says “當時” and “同日” before the following beat supplies January 15, and the final beat `x08-b01-s10` opens a larger “why fail?” question that this Short does not answer. |
| `story-everyday-target-x08-short-2` | 187 nonspace narration characters; roughly 37–47 seconds at 4–5 characters/second, before pauses. **25–55 seconds plausible, unverified.** | **PASS with caveat.** It answers its own cash-versus-charge premise (`x08-b06-s02–s03`) and explains the near-zero investment value (`x08-b06-s05–s08`). The last beat `x08-b06-s11` opens “where do operating losses fit?” and cuts before giving the distinction, so the ending functions as a long-video teaser rather than a complete final beat. |

Neither Short has a recorded duration in the allowed files. Both text estimates can cross 55 seconds if spoken slowly with long beat pauses; the timing verdicts require rendered audio to confirm.
