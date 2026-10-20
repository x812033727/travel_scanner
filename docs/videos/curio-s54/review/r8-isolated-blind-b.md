# S54 R8 isolated narrative blind B

Verdict: **FAIL, 11/13 yes**. The required no_recap and no_detour checks fail. This is a narration-only audience judgment, not a source or visual audit. I read the official output of node tools/video/cli.mjs narrative --slug curio-s54 after hashing the five author files, and did not read earlier S54 reviews or the author research. The exact captured panel output has SHA-256 3f05ee4433d458dc0c320b167ae08b8078798a0294407f637cd2b697c7ad26bc.

## Frozen author files (SHA-256)

| File | SHA-256 |
| --- | --- |
| brief.md | b10fa670558f3a0e6fb7296c77ee3979e7faf2d5f9ee22ac3b9172c5ba5b236d |
| research.md | 47642150198fa8dcc9a9991a5be9497dfd1f0db4a3085ff3f7d74f7f53126336 |
| claims.md | 0b7d0c2817f57be52f2b05a16771a8984cdf308942f0114cffc8d2cce237eadd |
| script.md | b9981a1b503504e48b452b2a37ddc42731ee7a4bcc6096dd6d7f79ec9d25438c |
| video.json | 100128600cbd4027bd2855fb904336fb12655bf203cd370c1a60d0bbcb508726 |

## Audience answers

| ID | Answer | Evidence and judgment |
| --- | --- | --- |
| scene_first | Yes | s54001 places a sender at a counter on 10 January 1840. |
| no_spoiler | Yes | s54007 withholds the missing word; the opening does not give its content. |
| one_line | Yes | s54075 pivots from the implemented low rate and cash to the delayed stamp in the same payment story. |
| no_toc | Yes | s54035 poses a specific problem of proving payment; the narrative does not announce a content list. |
| chapters_link | Yes | s54021 asks how to avoid collection at the door; s54022 begins the next chapter with prepayment. Other chapter starts likewise answer or advance the prior turn. |
| open_loops | Yes | Questions recur throughout, including s54081 before the January counter scene. There is no apparent 90-second gap without one. |
| payoffs | Yes | s54120 reveals the omitted “不”; s54116 answers the opening's stamp-use date, and s54089 supplies the teased diary count. |
| no_recap | **No** | s54085 repeats the point already made at s54031–s54032: prepayment spares collection from the recipient at delivery. It adds no new consequence and has no named callback. |
| chapters_are_events | Yes | The chapter “一月十日，人潮先到” is borne out by s54082's account of counter chaos; the other headings name a date, decision, or event. |
| outro_no_next | Yes | s54999 invites a subscription without naming another episode. |
| opening_hooks | Yes | The opening plants the diary count (s54004), counter trouble (s54005), missing word (s54006), and old fee (s54008), withholding their specifics. |
| one_thread | Yes | s54035 states the concrete challenge that carries the rate, cash, and stamp through the chapters: how a paid letter proves it was paid. |
| no_detour | **No** | s54140 opens a separate used-stamp cancellation question after the use date has been answered at s54116. The red-ink passage s54141–s54143 explains reuse prevention, not why the stamp lagged the low rate. |

The machine-readable answers, each with one quoted line, are in r8-isolated-blind-b.json. No author file was edited.
