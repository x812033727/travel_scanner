# S43 cold narrative read — 2026-10-20

## Scope and frozen inputs

Read only `docs/videos/curio-s43/video.json` and `script.md` for the episode, plus the repository's `curio-episode` and `youtube-video` rules and the exact `NARRATIVE_PANEL` in `tools/video/core/narrative.mjs`. I did not read prior S43 reviews, reports, claims, research, or briefs. I did not edit the repository, call the site, or generate media.

SHA256 at read:

- `video.json`: `2b15522f7d48afba6eae5f6487136d0ed85debd8b419cff22f4d209f87eede8b`
- `script.md`: `1bf9783c75ca9c93db3f1302b89b2e1bfaa3248321745beca6812039e76f5dac`

## Exact 13-question narrative panel

**Verdict: 13 yes, 0 no.** Twelve questions are required; `chapters_are_events` is advisory. This is a cold script assessment, not a factual source audit or a review of rendered audio and pictures.

| # | Panel ID | Yes/No | Script evidence and judgment |
| --- | --- | --- | --- |
| 1 | `scene_first` | **Yes** | `dn001` places Darwin in late August 1831, returning from North Wales to Henslow's letter at home; `dn002` gives the Beagle invitation. The first four lines remain in a concrete moment, with `dn005` introducing his reply. |
| 2 | `no_spoiler` | **Yes** | `dn005` asks whether the reply accepts or refuses, `dn007` asks what the captain's letter meant, and `dn008` asks what he read in Darwin's nose. The opener gives none of those later outcomes. |
| 3 | `one_line` | **Yes** | The body moves from Henslow's recommendation (`dn010`–`dn023`) to Darwin's refusal (`dn024`–`dn032`), the uncle's intervention (`dn037`–`dn050`), the captain's letter and meeting (`dn054`–`dn077c`), and Darwin's later nose recollection (`dn079`–`dn088`). The opening previews later moments, then the body starts at the recommendation; later references are callbacks with new developments. |
| 4 | `no_toc` | **Yes** | `dn014` asks what else the captain needed; `dn015` supplies a fellow gentleman. The chapter turns likewise use actions/questions rather than announcing a list or the video's structure. No narrated line says what sections will be covered. |
| 5 | `chapters_link` | **Yes** | Each handoff answers or advances the previous line: `dn009`→`dn010` (could Henslow decide? no); `dn023`→`dn024` (what reply? he wanted to go, before the refusal); `dn036`→`dn037` (who could persuade father? the uncle); `dn053`→`dn054` (can he commit? Henslow says wait); `dn065`→`dn066` (what were the hardships? forced close quarters); `dn078`→`dn079` (what other hesitation? the nose recollection). |
| 6 | `open_loops` | **Yes** | Questions and turns recur well within 90 seconds: e.g. `dn014`/`dn019`/`dn023` in the recommendation chapter, `dn041`/`dn049`/`dn053` around the uncle, and `dn069`/`dn073`/`dn074b`/`dn074d` during the meeting. The repository's estimated-timeline `narrativeProblems` check reports zero warnings at the stricter 45-second Curio cadence. |
| 7 | `payoffs` | **Yes** | The four major opener promises deliver new answers: `dn005`→`dn032` (refusal), `dn006`→`dn050` (father changed his mind), `dn007`→`dn057` (Darwin wrote that he was not going), `dn008`→`dn082` (captain doubted his endurance). The other declared loops also resolve, such as `dn075`→`dn076` (the captain meant to cool the plan) and `dn086`→`dn087` (27 December sailing). Adjacent questions resolve directly; distant ones name the original object/person again. |
| 8 | `no_recap` | **Yes** | Revisited facts move the story: `dn007` previews Wood's letter and `dn057` adds Darwin's reaction; `dn029` plants a compatibility worry and `dn074` reverses it after the meeting; `dn074d` says he bought nothing while undecided and `dn077c` shows him ordering equipment after deciding. These are developments or opener callbacks, not a repeated result. |
| 9 | `chapters_are_events` | **Yes** | Headings name changes/actions: “父親的顧慮使他先拒絕”, “舅舅帶著顧慮去見父親”, “伍德收到船長回信”, and “兩人在倫敦談明白狹窄的船”. “鼻子的說法，出現在多年後” names the source-provenance reveal rather than a generic conclusion section. |
| 10 | `outro_no_next` | **Yes** | `dn999a` answers the title, `dn999b` poses a viewer question, and `dn999c` invites subscription. None identifies another episode or file. |
| 11 | `opening_hooks` | **Yes** | After the homecoming scene (`dn001`–`dn003`), the first chapter offers at least four later moments without their outcome: reply (`dn005`), father and uncle (`dn006`), Wood receiving the captain's letter (`dn007`), and the captain noticing a nose (`dn008`). |
| 12 | `one_thread` | **Yes** | Darwin's decision and ability to board is the continuing concrete problem: he weighs the invitation (`dn003`), declines under his father's objection (`dn032`), regains permission (`dn050`), survives a second apparent loss (`dn057`), agrees after meeting FitzRoy (`dn077b`), and sails (`dn087`). |
| 13 | `no_detour` | **Yes** | Details that might seem subsidiary affect his place or decision: the unpaid position and route (`dn019`–`dn022`) explain his conditions; the uncle tests the alleged ship problems (`dn041`–`dn044`); the captain describes shared cabin, costs, and an exit option (`dn066`–`dn074a`); `dn074d`→`dn077c` turns packing from hesitation into commitment. There is no stand-alone unrelated segment or rapid list of scores/products. |

## Opener, payoffs, ending, and body timing

- The opener works as one arrival scene followed by four prospective hooks. It reaches the invitation in the first ~15 seconds, starts the questions at about 0:23, and ends at **0:56**. The first body line (`dn010`) immediately answers the opening handoff (`dn009`).
- The six chapter handoffs after the opener are causal or direct answers, as listed under question 5. The payoffs generally provide a new fact; the most important qualification is that the nose story is **Darwin's later recollection**, not an 1831 rejection recorded in the letters. `dn079` states the recollection, `dn081`–`dn083` explain the character inference and its failure, and `dn999a` gives the direct title answer: the nose did not get him rejected; the “almost” account is retrospective, and the cited contemporary letters contain no nose-based rejection.
- With the repository's `estimateTimeline` at 250 spoken units/minute and scene pauses, the whole narration is **10:46**. The opener is **0:56**; body runs **0:56–10:28 = 9:32**, clearing the Curio minimum of eight minutes. The outro is **0:18**. These are script estimates, not measured TTS or assembled-video durations.
- **Editorial timing concern, outside a failed panel question:** the title's nose claim does not enter the body until `dn079` at **9:33** (~89% of estimated runtime), and the explicit yes/no qualification arrives in `dn999a` at **10:28** (~97%). Most of the video is the documented boarding struggle rather than the nose anecdote. That struggle is relevant context and the script does ultimately answer the title, but viewers drawn specifically by the title wait almost the whole film for the evidence that distinguishes the later anecdote from the contemporary letters.
- A few adjacent question/answer beats (`dn014`→`dn015`, `dn069`→`dn071`, `dn073`→`dn074`, `dn086`→`dn087`) are short suspense devices rather than large reveals. They satisfy the panel and the tight hook cadence; the final recording will determine whether their repeated rhythm feels natural.

Read-only check: repository `narrativeProblems` on the estimated timeline with `TIGHT_CADENCE` returned **0 errors, 0 warnings**. That code check cannot establish the 13 human judgments or actual audio timing.
