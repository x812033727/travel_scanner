# Peloton X12 v11 — independent blind narrative review B

**Verdict: return the long-form narration for revision (10/12 required story checks pass).** Checks 7 and 8 fail on the spoken words. The two Shorts pass as standalone, approximately 35–44-second scripts. This is a script and plan review, not a fact-check, audio measurement, image inspection, or render QA.

I read the repository guidance, brand-story skill, and script-writing guide first. I then verified and read only the frozen `video.json` and `shorts.json` inputs before judging narration. I did not read the brief, treatment, sources, author notes, history, or another review. For audible wording I used each line's `say` when present, otherwise `text`.

| Frozen input | SHA-256 |
| --- | --- |
| `video.json` | `c66ea0f17970f19d4a3b3a9df4e26286dcc4872f2258beb83a294026c26013b9` |
| `shorts.json` | `8602834e0e4d4baa09267c191492307b90dc823360ad69fc4af17ef0b9ba6f1d` |

## Spoken-only checks

The numbered rows are the twelve required checks in `script-writing.md`; its chapter-name question (9) is advisory and is excluded from the denominator.

| Check | Verdict | Evidence from spoken lines |
| --- | --- | --- |
| 1. First four lines enter a concrete moment | **Yes** | `x12-b01-s01` gives 2021-05-24 and the Ohio announcement; `s02–s04` place the existing Precor factories against a proposed 2023 plant and its roughly US$400m plan. This is a dated business event rather than a dramatized human scene, but it is specific enough to locate the listener. |
| 2. Opening withholds later results | **Yes** | `b01-s05–s09` name the February, July, and September moments without giving the sale decision, manufacturing destination, or actual investment/recovery figures. `s10` asks the central question. |
| 3. One chronological story line | **Yes** | The Ohio plant moves from proposed capacity (`b02–b03`) to a shell earmarked for sale (`b04`), then to a stranded asset after outsourcing (`b05`) and delayed sale (`b06`). Supply and revenue context serve that change. |
| 4. No spoken roadmap or chapter list | **Yes** | No line announces the video's structure. The opening's three later moments are unresolved events, not a list of sections. |
| 5. Chapter openings answer or follow the previous ending | **Yes** | `b02-s21 → b03-s01` asks and answers what the new site would assemble; `b03-s19 → b04-s01` reveals February's disposition; `b04-s13 → b05-s01` reveals July's manufacturing decision; `b05-s19 → b06-s01` moves into the planned production year. |
| 6. Questions and suspense recur | **Yes, timing-sensitive** | Questions recur throughout `b02–b06`. The longest apparent gap between *literal* questions is `b04-s11 → b05-s06`, about a minute under a normal reading estimate, but `b04-s13` introduces the unresolved July order between them. That gives roughly 40–45 seconds to the next new question. Actual voice timing still needs measurement against the stricter 30–45-second target; it plainly satisfies the panel's 90-second ceiling on the script. |
| 7. Every pending question has a named answer | **No** | `b05-s06` asks **who** will handle Ohio after the Taiwan change. `b05-s07` says construction, redevelopment, and finding a buyer are a separate workstream, but never names who owns it. `b05-s17` later says the work consumes capital and management time, still without a direct answer to the “who.” State the responsible actor if the record supports one, or ask what work remains instead. The three distant opening payoffs themselves are distinct: February's sale plan at `b04-s01`, July's outsourcing at `b05-s01–s02`, and September's invested amount plus absent sale proceeds at `b05-s12–s16`. |
| 8. Facts are not replayed as fresh information | **No** | `b02-s25–s27` establish Precor's existing US sites and commercial role, then `b02-s28` restates both. Asian contractors continuing to supply bikes appears at `b02-s20`, `b02-s29–s30`, and `b03-s11`. `b03-s12–s13` restate the same machine-arrival limit. These are near repeats, not distant callbacks with new payoffs. Keep the strongest instance of each and use the freed space for the next Ohio decision. |
| 10. Outro does not advertise the next video | **Yes** | `x12-outro-s01–s03` answer, invite a viewer choice, and ask for subscription without naming a future episode. |
| 11. Opening has at least three later unresolved moments | **Yes** | February's revised disposition (`b01-s05–s06`), July's Taiwan line change (`s07–s08`), and September's investment/recovery question (`s09`) are in later-story order and do not give their answers. |
| 12. One changing protagonist/object | **Yes** | The recurring yellow-brown Ohio site is proposed, designed, left without its production job, offered for sale, and still delayed. The longest time away from it is the supply-chain setup in `b02`, which returns to why that site was planned. |
| 13. No unrelated detour or spoken catalog | **Yes, with density risk** | The hardware/subscription figures in `b04` and `b06`, and spending/impairment figures in `b05`, each bear on whether Ohio needed manufacturing capacity or produced sale proceeds. They are connected by questions and qualifications rather than simply enumerated. `b05-s11–s18` is dense with accounting distinctions; trimming the repeats identified above would give these different kinds of dollars more room to land. |

The cold open contains about 197 spoken Han characters, approximately **49–57 seconds** using 4.2–5 characters/second plus about one second per scene for pauses/transitions. The body from `b02-s01` through `b06-s11` contains about 2,324 Han characters across 83 scenes, approximately **9.1–10.6 minutes** on the same assumption. The body therefore has substantive material beyond eight minutes; this is a text-based timing estimate, not a measured audio duration.

## Standalone Shorts, narration first

| Short | Spoken verdict | Estimated duration |
| --- | --- | --- |
| `short-1` | **Pass.** Its own hook asks how much was invested and whether a September sale happened; it distinguishes the US$400m plan from US$86.6m already invested, adds the July manufacturing turn, and answers that no sale proceeds were reported. A viewer does not need the long video. | About **38–44 s** (154 Han characters, seven beats). |
| `short-2` | **Pass.** It poses whether growing subscriptions could restore the Ohio plant's use, gives the equipment/subscription divergence, explains that subscription revenue is not a new-machine order, and ends with the plant still for sale. It is a different angle from Short 1. | About **35–40 s** (140 Han characters, seven beats). |

Both estimates fall within the requested 25–55 seconds. Spoken English names still need ordinary voice audition if either cut is produced.

## Visual and portrait plans, checked after the spoken verdict

The long-form `look` is exactly `{"preset":"cute-mystery"}`. Its 90 `shot` prompts use anonymous conceptual models and repeatedly prohibit legible text and logos; the recurring yellow-brown Ohio model, teal existing plants, unopened envelopes, and empty collection box support the story's object and unanswered questions. Six `stats` cards distinguish revenue, invested capital, impairment, and sale price on screen. The `thumbnail` data names Peloton as the brand, but this JSON alone cannot prove its final size, placement, or color.

One visual-plan mismatch remains: the opening preview shots `b01-s05`, `s07`, and `s09` resemble the later February, July, and September topics, but they are separately described images rather than the *same* payoff image prescribed in `script-writing.md` for recognisable teaser callbacks. The September payoff is a `stats` card (`b05-s12`), unlike the opening ledger shot. Reuse or deliberately match each later payoff composition at production time without showing its result in the opening.

Both Shorts declare `portrait_plan.status: planned_not_rendered` and specify native 1080×1920 recomposition, right-side platform clearance, separate main/caption safe boxes, and per-beat crops. Their referenced long-form shot IDs exist. Short 2's revenue-down beat refers to `b04-s10`, whose long-form prompt is a product/category still life; its portrait plan adds an income band, so a new composition is necessary. The plan asks for a 360px phone and live Shorts-interface check. No rendered frames or phone playback were supplied here, so legibility, occlusion, motion, and actual 9:16 crop remain unverified.

**Revision target:** answer or rephrase `b05-s06`, remove the nearby Precor/Asian-line/machine repeats, then re-time the `b04-s13 → b05-s06` hook span in spoken audio. Preserve the February, July, and September payoffs and the separate investment-versus-sale distinction.
