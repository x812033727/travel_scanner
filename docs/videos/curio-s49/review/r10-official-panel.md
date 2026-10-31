# S49 R10 official merged narrative panel

**Result: FAIL — 12 of 13 questions pass.** Both fresh readers failed the required `payoffs` question. The official merge rule passes a question if either reader says yes; `payoffs` fails because both said no. No author file was changed during this integration.

## Exact basis

- Script file SHA-256, over original bytes: `c6389ff27c36856a914442644b71f746c66a89ddb1bd8f0f14a3f086d09fa51c`.
- Narration string SHA-256, over UTF-8 bytes of the decoded `narration` field from `narrative --json`: `85b3b2473e49caa9cfe8fc8ccfe2525599e9f932208bdb1480dad9860b3695c0`.
- [Reader A](/workspace/travel_scanner/docs/videos/curio-s49/review/r10-fresh-blind-a.json) and [reader B](/workspace/travel_scanner/docs/videos/curio-s49/review/r10-fresh-blind-b.json) declare those same hashes. Their complete findings and all merged official questions are in [the merged JSON](/workspace/travel_scanner/docs/videos/curio-s49/review/r10-official-panel-merged.json).

| Official question | Reader A | Reader B | Merged | Representative line IDs |
| --- | --- | --- | --- | --- |
| `scene_first` | Pass | Pass | Pass | `moon001`–`moon004` |
| `no_spoiler` | Pass | Pass | Pass | `moon004`–`moon008` |
| `one_line` | Pass | Pass | Pass | `moon009`, `moon032`, `moon056`, `moon079`, `moon100`, `moon112` |
| `no_toc` | Pass | Pass | Pass | `moon008`, `moon055`, `moon111` |
| `chapters_link` | Pass | Pass | Pass | `moon008`→`moon009`, `moon031`→`moon032`, `moon055`→`moon056`, `moon078`→`moon079`, `moon099`→`moon100`, `moon111`→`moon112` |
| `open_loops` | Pass | Pass | Pass | `moon004`, `moon015`, `moon028`, `moon038`, `moon050`, `moon061`, `moon073`, `moon083`, `moon094`, `moon104`, `moon111`, `moon121`, `moon128` |
| `payoffs` | **Fail** | **Fail** | **Fail** | `moon018`→`moon019`; A also cites `moon022`→`moon023` |
| `no_recap` | Pass | Pass | Pass | `moon003`→`moon009`, `moon024`→`moon093`, `moon123`–`moon125` |
| `chapters_are_events` | Pass | Pass | Pass | `moon001`, `moon009`, `moon032`, `moon056`, `moon079`, `moon100`, `moon112` |
| `outro_no_next` | Pass | Pass | Pass | `moon999a`–`moon999c` |
| `opening_hooks` | Pass | Pass | Pass | `moon004`–`moon007` |
| `one_thread` | Pass | Pass | Pass | `moon008`, `moon016`, `moon041`, `moon070`, `moon091`, `moon118`, `moon132` |
| `no_detour` | Pass | Pass | Pass | `moon096`, `moon103`, `moon108`, `moon123`, `moon125`, `moon130` |

## Shared failure

`moon018` asks where a reader can turn up the claimed *Edinburgh Journal of Science* supplement. `moon019` only says that the article itself claimed that source. Neither reader found an explicit, source-bounded answer saying whether a checkable issue can be located, or where. Reader A also found that `moon022` asks whether each named witness left original material, while `moon023` addresses only the asserted transmission route and actual letters. A revision should answer the supplement question directly and either answer the broader witness-material question or narrow its wording.

The [answer file](/workspace/travel_scanner/docs/videos/curio-s49/review/r10-official-panel-answers.json) was submitted to the official CLI. It wrote `/workspace/.video-work/curio-s49/review/narrative.json` at round **2**, marked only `payoffs` failed, and exited **1**, as specified for a failed required question. The exact command, exit code, output, record summary and hashes are in [the CLI receipt](/workspace/travel_scanner/docs/videos/curio-s49/review/r10-official-panel-cli-receipt.json).

R10 remains at the narrative gate.
