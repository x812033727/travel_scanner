# S49 R9 official merged narrative panel

**Result: FAIL — 12 of 13 questions pass.** Both independent readers failed the required `no_recap` check. The merge uses the official rule that a question passes when either reader says yes; here both said no. No script change was made in this integration.

## Exact basis

- Script file SHA-256, over original bytes: `10f912c63ba438c676372469e8e44a52a8252113efc22f3af9fb74f91ae22354`.
- Narrative string SHA-256, over UTF-8 bytes of the decoded `narration` field from `narrative --json`: `579d359cd086437f9363cacf655403cad71b5da8b22ec0104de832d89c1f5cc8`.
- Both [blind reader A](/workspace/travel_scanner/docs/videos/curio-s49/review/r9-fresh-blind-a.json) and [blind reader B](/workspace/travel_scanner/docs/videos/curio-s49/review/r9-fresh-blind-b.json) declare those same hashes; both were checked against fresh file and CLI output. Their complete findings and all 13 merged answers are in [the merged JSON](/workspace/travel_scanner/docs/videos/curio-s49/review/r9-official-panel-merged.json).

| Official question | Reader A | Reader B | Merged | Representative line IDs |
| --- | --- | --- | --- | --- |
| `scene_first` | Pass | Pass | Pass | `moon001`–`moon004` |
| `no_spoiler` | Pass | Pass | Pass | `moon004`–`moon008` |
| `one_line` | Pass | Pass | Pass | `moon009`, `moon032`, `moon056`, `moon079`, `moon100`, `moon112` |
| `no_toc` | Pass | Pass | Pass | `moon055`, `moon061`, `moon098` |
| `chapters_link` | Pass | Pass | Pass | `moon008`–`moon009`, `moon031`–`moon032`, `moon055`–`moon056`, `moon078`–`moon079`, `moon099`–`moon100`, `moon111`–`moon112` |
| `open_loops` | Pass | Pass | Pass | `moon026`, `moon038`, `moon050`, `moon061`, `moon073`, `moon083`, `moon094`, `moon104`, `moon111`, `moon128` |
| `payoffs` | Pass | Pass | Pass | `moon004`→`moon023`, `moon005`→`moon041`, `moon006`→`moon118`, `moon007`→`moon113`–`moon115` |
| `no_recap` | **Fail** | **Fail** | **Fail** | A: `moon014`–`moon015`; B: `moon023`, `moon026`–`moon027`, `moon029` |
| `chapters_are_events` | Pass | Pass | Pass | `moon001`, `moon009`, `moon032`, `moon056`, `moon079`, `moon100`, `moon112` |
| `outro_no_next` | Pass | Pass | Pass | `moon999a`–`moon999c` |
| `opening_hooks` | Pass | Pass | Pass | `moon004`–`moon007` |
| `one_thread` | Pass | Pass | Pass | `moon008`, `moon032`, `moon056`, `moon100`, `moon112`, `moon132` |
| `no_detour` | Pass | Pass | Pass | `moon108`–`moon109`, `moon111`–`moon112`, `moon123`–`moon130` |

## Shared failure, distinct evidence

Reader A found that `moon014` states the headline uses Herschel's real name, then `moon015` repeats the same headline fact while posing a question. Reader B found a separate cluster: `moon023` already limits the purported assistant's route to a story claim, `moon026`–`moon027` say the cited supplement, letter, and Royal Society material are supplied only through the report, and `moon029` repeats that the report did not supply the documents. Both clusters concern facts repeated before a meaningful later callback.

The answer file submitted to the official CLI is [r9-official-panel-answers.json](/workspace/travel_scanner/docs/videos/curio-s49/review/r9-official-panel-answers.json). The CLI wrote `/workspace/.video-work/curio-s49/review/narrative.json`, marked only `no_recap` failed, and exited **1**, as specified for a failed required question. The exact command, exit code, output, and record hash are in [the CLI receipt](/workspace/travel_scanner/docs/videos/curio-s49/review/r9-official-panel-cli-receipt.json).

R9 remains at the narrative gate. Policy/site and TTS/audio work were not run for this failed panel.
