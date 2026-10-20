# R11 official narrative panel — curio-s49

**FAIL:** 11 of 13 questions passed; `payoffs` and `no_recap` failed. The CLI exited 1 as expected for failed required questions and wrote the round 3 receipt to `/workspace/.video-work/curio-s49/review/narrative.json`.

Blind readers [A](r11-fresh-blind-a.md) and [B](r11-fresh-blind-b.md) agreed on all 13 answers. The [merge audit](r11-merge-audit.json) applies the panel's rule that a question passes when either reader passes it. The [13-answer input](r11-merged-answers.json) quotes exact narration lines. The [CLI receipt](r11-official-panel-cli-receipt.json) is a copy of the record written by `narrative --answers`.

- Script file SHA256: `a9fb4bcc6e271609d79e34d2f4278cdb2c797d0fc8af32b52d4f68b3b1629259`
- Narration UTF-8 SHA256: `9811b993b5264414fec15d02ad36101985cfc856706afd9447baba8168dc9b5c`

| Question | A | B | Merged |
| --- | --- | --- | --- |
| `scene_first` | PASS | PASS | PASS |
| `no_spoiler` | PASS | PASS | PASS |
| `one_line` | PASS | PASS | PASS |
| `no_toc` | PASS | PASS | PASS |
| `chapters_link` | PASS | PASS | PASS |
| `open_loops` | PASS | PASS | PASS |
| `payoffs` | FAIL | FAIL | **FAIL** |
| `no_recap` | FAIL | FAIL | **FAIL** |
| `chapters_are_events` | PASS | PASS | PASS |
| `outro_no_next` | PASS | PASS | PASS |
| `opening_hooks` | PASS | PASS | PASS |
| `one_thread` | PASS | PASS | PASS |
| `no_detour` | PASS | PASS | PASS |

`payoffs`: `[moon104 10:23]` asks when lunar observations resume. `[moon105 10:28]`–`[moon106 10:34]` only rule out the rest of that month; `[moon107 10:40]`–`[moon108 10:45]` move to Saturn without a date or a stated final outcome. The opening `[moon006 00:31]` asks whether a second observation can be produced, while `[moon118 11:48]` establishes only that one selected reprint excerpt does not contain one.

`no_recap`: `[moon019 01:52]` establishes the existence and 1859 date of the reprint, then `[moon112 11:11]` states them again without a named callback. Reader A also found that `[moon010 00:58]` and `[moon011 01:03]` repeat the purpose of Herschel's Cape trip. Reader B found repeated satire judgments at `[moon119 11:55]`–`[moon122 12:13]`.
