# Peloton X12 v11 — independent blind narrative review A

## Blind read and fixed spoken verdict

I read the repository instructions and script-writing rules, then only `video.json` and `shorts.json` for this verdict. I used each long-form line's `say` when present (otherwise `text`), and each Short's `narration`. I had not read the brief, treatment, source material, author notes, history, other reviews, or visual-plan files when I fixed this verdict. This is a listening/story judgment, not a source check or a rendered-video QA result.

| Input | Verified SHA-256 |
| --- | --- |
| `video.json` | `c66ea0f17970f19d4a3b3a9df4e26286dcc4872f2258beb83a294026c26013b9` |
| `shorts.json` | `8602834e0e4d4baa09267c191492307b90dc823360ad69fc4af17ef0b9ba6f1d` |

**Verdict: return for a focused revision; 10 of the 12 required narrative answers are yes.** The Ohio plant is a real through-line, the opening withholds the February and July decisions, and the script is long enough to carry a substantive body. The remaining problems are payoff integrity and repeated facts. The count of 22 declared loops should not be used as evidence that 22 distinct, distant questions are paid off.

| Required question from `script-writing.md` | Answer | Spoken evidence |
| --- | --- | --- |
| 1. First four lines place us in a concrete moment | Yes | `x120101–104` put a dated Ohio announcement beside the newly bought US plant, the planned 2023 output, and the four-hundred-million-dollar commitment. |
| 2. Opening does not reveal later results | Yes | `x120105–109` name future decision moments but do not say “finish then sell,” “exit owned manufacturing,” or the invested amount. |
| 3. One story line without changing protagonists | Yes | Demand, the proposed Ohio capacity, the unfinished shell, outsourced production, and attempted sale follow the same plant decision. |
| 4. No spoken roadmap or enumerated agenda | Yes | The opening's February, July, and September lines are events with unanswered consequences, not a “first/second/third” program. The body generally advances by questions and decisions. |
| 5. Chapter openings follow the prior beat | Yes | `x120301`, `x120401`, and `x120501` answer the preceding capacity, February, and July questions. `x120601` moves into the originally planned output year. `x120201` supplies the demand that prompted the opening announcement. |
| 6. A hanging question at least every 90 seconds | Yes | The opening's future decisions stay open while body questions recur at `x120204`, `209`, `213`, `217`, `221`, then `304`, `307`, `312`, `315`, `319`, and at similar spacing later. This is a text-based cadence assessment. |
| 7. Every hanging question has a named, substantive later payoff | **No** | The opening's governing `x120110` asks *how* the planned car-making plant changed purpose, but its declared payoff `x120612` only says the FY2023 report has no recorded sale or proceeds. That late line repeats the status already given at `x120516`, without resolving the change-of-purpose question. `x120519` asks whether later income restores the plant's manufacturing job; `x120605` only says subscription growth cannot prove a need for new capacity. |
| 8. No fact or number retold without a meaningful callback | **No** | `x120220` already says Asian contractors still supply bikes and Precor's US facility keeps operating; `x120311` says essentially the same thing, without a new event or named callback. `x120401–405` restate the shell-to-sale decision several times before the June result moves the story. |
| 10. Outro does not point to another video | Yes | `x120612–614` stay with Ohio, ask a comment question, and invite subscription without naming a next episode. |
| 11. Opening teases at least three later unresolved moments | Yes | The February shell decision (`x120105–106`), July manufacturing decision (`107–108`), and September invested/recovery amount (`109`) are concrete future moments held short of their outcomes. |
| 12. One protagonist/object progresses chapter by chapter | Yes | The Ohio land becomes a promised assembly plant, then an unfinished shell slated for sale, then an asset still being marketed in FY2023. Precor and the Taiwan factories enter as decisions affecting that object. |
| 13. No unrelated detour or rapid product/score catalog | Yes | The FY2022 income and impairment run (`x120407–412`, `x120512–516`) is dense, but each figure tests whether Ohio's unused capacity or invested cash can be recovered. It remains on the central question, though the ledger-like delivery increases the risk of losing a listener. |

The nonblocking chapter-title question (9) is also **yes**: the six titles name demand, an Ohio assembly plan, sale, outsourcing, and delayed sale rather than generic “background” or “conclusion” slots.

The opening has 197 CJK characters across ten spoken lines, consistent with roughly 40–55 seconds at a natural Mandarin pace plus pauses. It starts in a specific moment and ends on the film's question. The 83-line body has about 2,324 CJK characters before the three-line outro, consistent with more than eight minutes once normal speech and scene pauses are included; duration remains an estimate until audio exists. New turns are generally within the requested 30–45-second window: chapter 2's questions at `x120204/209/213/217/221` and chapter 5's at `x120506/510/515/519` show the pattern. Many declared setups, however, resolve one or two lines later (`x120213→214`, `x120312→313`, `x120607→608`, `x120611→612`). Those are useful local transitions, not distinct distant payoffs. `x120105` and `106` also share `x120401`; the final opening question's assigned payoff is the already-reported unsold status. Give each major opening promise one later answer that adds information, and trim the duplicated supplier/Precor bridge.

### Standalone Shorts, spoken track only

| Short | Verdict | Evidence and limitation |
| --- | --- | --- |
| 1, invested money and sale status | **Pass provisionally** | Seven beats tell a complete February → June → July → September story: planned US$400m, about US$86.6m actually invested, and no sale reported in the September annual filing. The plan/spend/sale distinctions are spoken. About 154 CJK characters plus the English names suggests roughly 35–48 seconds with beat pauses, within 25–55 seconds, pending audio. |
| 2, subscription versus hardware | **Pass provisionally, weaker explanation** | Seven beats establish the planned Ohio factory, the February sale decision, opposing FY2022 income movements, July outsourcing, and September's still-unsold shell. The answer is audible without the long video: more subscription revenue does not establish demand for new machines. The spoken proof would be stronger if it said that an existing device or digital viewer can keep paying for classes; that example exists in the long script but not this Short's narration. About 140 CJK characters plus English names suggests roughly 33–45 seconds with pauses, pending audio. |

Neither Short has a measured runtime or rendered frame in the two reviewed JSON inputs, so these are spoken-story and estimated-length judgments.

## Visual-plan inspection after the spoken verdict

This section was added only after the spoken verdict above was fixed. `visual-plan.md` describes 90 illustration shots and six statistics cards; those counts match `video.json` (96 scenes in total). Its main visual grammar also matches most prompts: the Ohio object stays yellow-brown and inactive, existing production is lit teal, transaction envelopes remain unexchanged, and revenue/accounting figures are assigned to postproduction cards. The prompts for the Shorts' referenced shots preserve the intended distinctions in the important sale and money beats (`x12-b04-s01`, `x12-b05-s11`, `x12-b05-s16`). No prompt asks the image model to draw a brand name or readable text.

There are three concrete plan-to-input gaps to settle before producing frames:

1. `visual-plan.md` treats the unbuilt Ohio shell as a plan in chapter 3, but `x12-b03-s13` and `x12-b03-s17` prompts explicitly ask for a **completed** empty shell. The `s13` narration is a conditional (“if the machines cannot arrive”), while `s17` narrates proposed jobs. A generated completed building in `s17` could make a hypothetical stage look achieved. Keep the planned/hypothetical status legible in that image.
2. The visual plan requires Short 1 beat 1.2 to fit the yellow Ohio model, four plan chips, **and the existing teal factory** in the main safe area. The beat's `shorts.json` `crop_focus`/`recompose` mention only the Ohio model and chips, though its referenced main prompt `x12-b01-s04` includes the teal factory. The portrait instruction should name the third object if that comparison is essential.
3. The visual plan requires Short 2 beat 2.3 to show a bike, accessories, delivery box, and commercial equipment so “equipment revenue” is not read as bike unit sales. The portrait instruction reduces this to an equipment box and downward band, whereas `x12-b04-s10` names those category objects. Similarly, Short 1 beat 1.6's plan asks for invested coins and an empty receipts box, while its portrait instruction names only the Ohio shell and report. The empty box at 1.6 would also reveal beat 1.7's “no sale” answer early; the plan and beat sequence need one deliberate choice.

Both `shorts.json` portrait plans and all 14 beat-level portrait specs say `planned_not_rendered`. Every Short references an existing main scene and uses a 1080×1920 canvas. The listed main safe area is `x=80–900, y=258–1378`; captions are `x=80–900, y=1430–1595`, leaving the specified 180 px at right for platform controls. Those coordinates are internally consistent. A direct center crop from a 16:9 shot to 9:16 would retain only about **32%** of its width, particularly unsafe for the wide `x12-b05-s11` transaction table; the explicit native recomposition requirement is therefore necessary. It remains a requirement, not proof that the three objects survive in the actual Shorts.

The largest number card is also tight inside the stated 820 px main width: `US$86.6m` at 168 px measures about 795 px in Noto Sans CJK Regular and 842 px in its Bold face. That quick font-width check is a layout risk, not a rendered-frame measurement; the actual face, spacing, and effects may differ. The two FY comparison rows at 49 px have more room. Verify the large amount, captions, required objects, and interface overlap on 360 px phone frames after portrait generation. **No rendered image, audio, or 9:16 crop was inspected in this review, so neither visual quality nor final safe-area compliance is passed yet.**
