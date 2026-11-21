# Curio S38 R6 fresh source and prompt audit

Frozen R6 review after blind seal `/tmp/curio_s38_r6_fresh_blind_seal.md`. No author files or media edited.

## Integrity and source

- Script SHA-256 `87750646298ca30cfbce4139c4777080b1914ddc3595dc4a733685e439658168` — match.
- Video SHA-256 `3452b0259d36534aca7863bb6c7240634bf8bf75cee7497662c79e8d8633c9ef` — match.
- Claims SHA-256 `71eb9ac7f5318f27453ee2dff3568efa2e2bd3679d935e6d65981ceb38d0c517` — match.
- Fresh Pepys `4200.txt` from GITenberg commit `68fcf49f70ee793b989a6fd0464264d55beb4451` SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d` — match; September 2–6 diary lines 65784–66176 read.

## Blocking source chronology

1. **Tom Hater arrival is late in the script.** The diary says Pepys returned, found Hater with salvaged goods, invited him to lodge, and only then did new reports force Pepys to pack (L65939–65945). R6 presents packing at `pf047`, cellar at `pf048`, garden at `pf049`, then introduces the guest at `pf050`. The guest’s short uneasy sleep occurred after the work (L65952–65954), so the sentence mixes an early arrival with a late outcome. This violates source order even though each isolated action is real.
2. **Garden and cellar are swapped.** The diary says he carried much of his goods into the garden by moonlight, then Hater helped move money and iron chests into the cellar, and then gold bags/account books went to the office (L65945–65950). R6 says cellar first at `pf048`, garden second at `pf049`; `pf048` even says `先`. The corresponding `pf048` and `pf049` scene sequence repeats this inversion.

Source order for a repair: Hater arrives and is invited; fire news forces packing; goods go to the garden; Hater helps move money and iron chests to the cellar; important papers/gold bags go to the office or separate boxes; later Hater rests poorly. No other source-factual blocker was found in the September 2–6 run.

## Requested target transitions and prompts

| ID | Frozen R6 judgment | Pinned diary comparison |
|---|---|---|
| `pf040` | Pass | Diary L65897–65900: Pepys boats below and above the bridge and sees fire extended in both directions. The bridge prompt fits that bridge-sided visual bridge. |
| `pf075` | Pass | Diary L66004–66011: afternoon discussion in garden, then Pen goes that night to arrange Woolwich/Deptford workers for the morning. Night departure prompt fits. |
| `pf076` | Pass | Diary L66008–66012: Pepys writes Coventry for Duke of York demolition permission; no reply. Letter prompt depicts this separate written request, not the earlier oral Whitehall report. |
| `pf077` | Pass | Diary L66011–66012 says he received no answer; the waiting image has no invented response. |
| `pf085` | Pass | Diary L66072–66077: Pepys takes his wife and gold by boat to Woolwich about 2 a.m.; moonlight is explicit. Other passengers may be outside the cropped frame. |
| `pf094` | Pass | Diary L66092–66095 moves directly from scorched Barking Church to Pepys ascending its steeple. Church tower approach is a supported transition. |

The `pf076` messenger is a schematic delivery cue: the diary establishes a letter was written but does not name its carrier. This is an unverified illustrative prop, not a false historical statement. The `pf040` prompt’s “both sides of a stone bridge” is read as above and below London Bridge along the river, not two separate bridges.

## All 112 claim and text alignments

All 112 claim IDs are present exactly once and ordered `pf001`–`pf112`; all 112 claim texts match their `video.json` line texts byte for byte; all 112 script narration texts match the same line texts; scene IDs equal line IDs. All evidence tags are within `D2a`–`D6` or `EDIT`; `pf111` and `pf112` are editorial invitations. Source meaning is accurate except the two chronology inversions above.

| ID | Source tag | Individual claim/source result |
|---|---|---|
| `pf001` | D4a | Pass |
| `pf002` | D4a | Pass |
| `pf003` | D4a,D3 | Pass |
| `pf004` | D5 | Pass |
| `pf005` | D4a,D6 | Pass |
| `pf006` | D2a | Pass |
| `pf007` | D2a | Pass |
| `pf008` | D2a | Pass |
| `pf009` | D2a | Pass |
| `pf010` | D2a | Pass |
| `pf011` | D2a | Pass |
| `pf012` | D2a | Pass |
| `pf013` | D2a | Pass |
| `pf014` | D2a | Pass |
| `pf015` | D2a | Pass |
| `pf016` | D2a | Pass |
| `pf017` | D2a | Pass |
| `pf018` | D2a | Pass |
| `pf019` | D2a | Pass |
| `pf020` | D2a | Pass |
| `pf021` | D2a | Pass |
| `pf022` | D2a | Pass |
| `pf023` | D2b | Pass |
| `pf024` | D2b | Pass |
| `pf025` | D2b | Pass |
| `pf026` | D2b | Pass |
| `pf027` | D2b | Pass |
| `pf028` | D2b | Pass |
| `pf029` | D2b | Pass |
| `pf030` | D2b | Pass |
| `pf031` | D2b | Pass |
| `pf032` | D2b | Pass |
| `pf033` | D2b | Pass |
| `pf034` | D2b,D4a | Pass |
| `pf035` | D2c | Pass |
| `pf036` | D2c | Pass |
| `pf037` | D2c | Pass |
| `pf038` | D2c | Pass |
| `pf039` | D2c | Pass |
| `pf040` | D2c | Pass |
| `pf041` | D2c | Pass |
| `pf042` | D2c | Pass |
| `pf043` | D2c | Pass |
| `pf044` | D2c | Pass |
| `pf045` | D2c | Pass |
| `pf046` | D2c | Pass |
| `pf047` | D2c | Chronology blocker in sequence |
| `pf048` | D2c | Chronology blocker in sequence |
| `pf049` | D2c | Chronology blocker in sequence |
| `pf050` | D2c | Chronology blocker in sequence |
| `pf051` | D2c,D3 | Pass |
| `pf052` | D3 | Pass |
| `pf053` | D3 | Pass |
| `pf054` | D3 | Pass |
| `pf055` | D3 | Pass |
| `pf056` | D3 | Pass |
| `pf057` | D3 | Pass |
| `pf058` | D3 | Pass |
| `pf059` | D3 | Pass |
| `pf060` | D3 | Pass |
| `pf061` | D3 | Pass |
| `pf062` | D3 | Pass |
| `pf063` | D3 | Pass |
| `pf064` | D3,D4a | Pass |
| `pf065` | D4a | Pass |
| `pf066` | D4a | Pass |
| `pf067` | D4a | Pass |
| `pf068` | D4a | Pass |
| `pf069` | D4a | Pass |
| `pf070` | D4a | Pass |
| `pf071` | D4a | Pass |
| `pf072` | D4a | Pass |
| `pf073` | D4a | Pass |
| `pf074` | D4b | Pass |
| `pf075` | D4b | Pass |
| `pf076` | D4b | Pass |
| `pf077` | D4b | Pass |
| `pf078` | D4b | Pass |
| `pf079` | D4b | Pass |
| `pf080` | D4b | Pass |
| `pf081` | D4b | Pass |
| `pf082` | D4b,D5 | Pass |
| `pf083` | D5 | Pass |
| `pf084` | D5 | Pass |
| `pf085` | D5 | Pass |
| `pf086` | D5 | Pass |
| `pf087` | D5 | Pass |
| `pf088` | D5 | Pass |
| `pf089` | D5 | Pass |
| `pf090` | D5 | Pass |
| `pf091` | D5 | Pass |
| `pf092` | D5 | Pass |
| `pf093` | D5 | Pass |
| `pf094` | D5 | Pass |
| `pf095` | D5 | Pass |
| `pf096` | D5 | Pass |
| `pf097` | D5 | Pass |
| `pf098` | D5 | Pass |
| `pf099` | D5 | Pass |
| `pf100` | D5 | Pass |
| `pf101` | D5 | Pass |
| `pf102` | D5,D6 | Pass |
| `pf103` | D6 | Pass |
| `pf104` | D6 | Pass |
| `pf105` | D6 | Pass |
| `pf106` | D5,D6 | Pass |
| `pf107` | D6 | Pass |
| `pf108` | D6 | Pass |
| `pf109` | D6 | Pass |
| `pf110` | D4a,D6 | Pass |
| `pf111` | EDIT | Pass (nonfactual invitation) |
| `pf112` | EDIT | Pass (nonfactual invitation) |

## All 111 still alignments

Exactly 111 scenes have a nonempty still prompt and `visual: still`; the only unprompted scene is the `pf112` outro. Scene order and IDs match narration. The still prompts are cartoons and do not assert precise clothing, prop dimensions, or eyewitness status. Except for the chronology embodied by `pf048`–`pf049`, I found no prompt contradiction.

| ID | Prompt result |
|---|---|
| `pf001` | Pass |
| `pf002` | Pass |
| `pf003` | Pass |
| `pf004` | Pass |
| `pf005` | Pass |
| `pf006` | Pass |
| `pf007` | Pass |
| `pf008` | Pass |
| `pf009` | Pass |
| `pf010` | Pass |
| `pf011` | Pass |
| `pf012` | Pass |
| `pf013` | Pass |
| `pf014` | Pass |
| `pf015` | Pass |
| `pf016` | Pass |
| `pf017` | Pass |
| `pf018` | Pass |
| `pf019` | Pass |
| `pf020` | Pass |
| `pf021` | Pass |
| `pf022` | Pass |
| `pf023` | Pass |
| `pf024` | Pass |
| `pf025` | Pass |
| `pf026` | Pass |
| `pf027` | Pass |
| `pf028` | Pass |
| `pf029` | Pass |
| `pf030` | Pass |
| `pf031` | Pass |
| `pf032` | Pass |
| `pf033` | Pass |
| `pf034` | Pass |
| `pf035` | Pass |
| `pf036` | Pass |
| `pf037` | Pass |
| `pf038` | Pass |
| `pf039` | Pass |
| `pf040` | Pass |
| `pf041` | Pass |
| `pf042` | Pass |
| `pf043` | Pass |
| `pf044` | Pass |
| `pf045` | Pass |
| `pf046` | Pass |
| `pf047` | Pass |
| `pf048` | Sequence blocker shared with claim order |
| `pf049` | Sequence blocker shared with claim order |
| `pf050` | Pass |
| `pf051` | Pass |
| `pf052` | Pass |
| `pf053` | Pass |
| `pf054` | Pass |
| `pf055` | Pass |
| `pf056` | Pass |
| `pf057` | Pass |
| `pf058` | Pass |
| `pf059` | Pass |
| `pf060` | Pass |
| `pf061` | Pass |
| `pf062` | Pass |
| `pf063` | Pass |
| `pf064` | Pass |
| `pf065` | Pass |
| `pf066` | Pass |
| `pf067` | Pass |
| `pf068` | Pass |
| `pf069` | Pass |
| `pf070` | Pass |
| `pf071` | Pass |
| `pf072` | Pass |
| `pf073` | Pass |
| `pf074` | Pass |
| `pf075` | Pass |
| `pf076` | Pass |
| `pf077` | Pass |
| `pf078` | Pass |
| `pf079` | Pass |
| `pf080` | Pass |
| `pf081` | Pass |
| `pf082` | Pass |
| `pf083` | Pass |
| `pf084` | Pass |
| `pf085` | Pass |
| `pf086` | Pass |
| `pf087` | Pass |
| `pf088` | Pass |
| `pf089` | Pass |
| `pf090` | Pass |
| `pf091` | Pass |
| `pf092` | Pass |
| `pf093` | Pass |
| `pf094` | Pass |
| `pf095` | Pass |
| `pf096` | Pass |
| `pf097` | Pass |
| `pf098` | Pass |
| `pf099` | Pass |
| `pf100` | Pass |
| `pf101` | Pass |
| `pf102` | Pass |
| `pf103` | Pass |
| `pf104` | Pass |
| `pf105` | Pass |
| `pf106` | Pass |
| `pf107` | Pass |
| `pf108` | Pass |
| `pf109` | Pass |
| `pf110` | Pass |
| `pf111` | Pass |

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s38`: 0 errors, 0 warnings; estimate 9.9 minutes, 112 lines. Lint does not catch the source order issue.

**Frozen R6 judgment: BLOCKED by two September 2 chronology inversions at `pf047`–`pf050`; named target transitions/prompts pass.**
