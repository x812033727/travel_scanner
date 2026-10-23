# C15 FriXion narration: independent blind reader v2-2

- Scope: `narration-only.txt` (87 ID-tagged spoken lines), SHA-256 `01C8CC99F90B3883310BA2E6AF6EEDB76DAC82D1A453A6EEF372D2DDC15272BA`.
- Rubric: the 13 questions in `NARRATIVE_PANEL`, `tools/video/core/narrative.mjs:266-280`.
- Blind boundary: I recorded these judgments after reading only the two items above. I did not inspect the treatment, source notes, visual plan, full script, prior reviews, PR or commit history, or the other reader's receipt. This is a narrative read, not a fact check.
- Verdict: **HOLD**. Eleven of twelve required questions are Yes; `no_recap` is No. The optional chapter-title question is No because the provided narration has IDs but no chapter titles to assess.

| # | Panel ID | Required | Yes/No | Line-ID evidence and judgment |
|---|---|---|---|---|
| 1 | `scene_first` | Yes | **Yes** | H01 places a person at a desk making an error and rubbing the mark; H02 stays with that sheet of paper. H04 also supplies a dated historical moment within the first four lines. |
| 2 | `no_spoiler` | Yes | **Yes** | H04-H07 raise the cup-to-pen, capsule-to-tip, marketing-request, and retail questions without answering why the marks disappear or when the pen reaches a store. H01-H03 show the apparent disappearance but withhold its cause until N04-N06. |
| 3 | `one_line` | Yes | **Yes** | After the preview, O01-O11 move from color-changing material to cups and toys, I01-I17 to stable ink and a writing pen, E01-E14 to transparent correction and manufacture, T01-N03 to release and later pen engineering, and N04-N18 to the present mechanism and use. N04 explicitly returns to the opening sheet rather than retelling the history. |
| 4 | `no_toc` | Yes | **Yes** | H04-H07 are dated moments ending in questions; H08 asks how those decisions connect. No line tells the viewer an order of chapters, numbered list, or plan for the video. |
| 5 | `chapters_link` | Yes | **Yes** | H08's cup-to-pen question leads to the origin of the changing material at O01. O13 asks whether written color can remain stable and I01-I03 answer it. I18's transparency question is answered by E01-E03. E15's sale-date question leads directly to T01. T13's exposed-tip question leads directly to N01-N03. |
| 6 | `open_loops` | Yes | **Yes** | The body keeps short intervals between unresolved questions or turns: O06/O10/O13, I06/I14/I18, E05/E07/E15, T04/T09/T13, and N04/N13. No apparent 90-second stretch lacks one at normal spoken pace. |
| 7 | `payoffs` | Yes | **Yes** | H03's scrape-away alternative returns explicitly at N04-N06; O13's color stability gets I03-I05; I18's transparency request gets E01-E05; E15's retail question gets T01; T13's exposed tip gets N01-N03; N13's unsafe-paper question gets N14-N15. The late H07 store question is paid with the named FriXion and year at T01. |
| 8 | `no_recap` | Yes | **No** | H07 already says that in 2004 the company decided to commercialize the pen. E12 states the same 2004 commercialization decision again as a new chronological event, without explicitly recalling the opening promise; “啟動專案” adds a consequence but does not remove the duplicated decision. H05/I11 is another close preview/body overlap, although I11 adds the two-to-three-micrometer answer. N16 explicitly says “回頭看” and is a proper callback, so that line is not the reason for this No. |
| 9 | `chapters_are_events` | No | **No** | The blind input shows H/O/I/E/T/N line IDs (for example H01, O01, I01, E01, T01, N01), not chapter names. I cannot verify that chapter titles name events from this input. This optional No is an evidence limit, not a claim that actual titles are functional. |
| 10 | `outro_no_next` | Yes | **Yes** | N19 asks the viewer about their own paper; N20 asks for a subscription. Neither announces a next video, episode, or file. |
| 11 | `opening_hooks` | Yes | **Yes** | After H01-H03, H04 asks why the 1976 cup was not a pen, H05 asks if smaller capsules can pass the tip, H06 stops before naming the marketer's requested change, and H07 asks when the commercialized pen reaches shops. Each points to a later answer. |
| 12 | `one_thread` | Yes | **Yes** | The same writing-and-rewriting problem starts at H01-H03; O11-O13 explain why a color-changing cup's material is not yet usable ink, I01-I17 solve stability and tip passage but expose the remaining visible mark, E01-E05 turn that into transparent correction, T01-T03 deliver a pen that can rewrite, and N13-N18 bound its proper use. |
| 13 | `no_detour` | Yes | **Yes** | O05-O07 carry the material toward a usable product; T04-T12 ask whether the same capsule ink can serve denser Japanese writing; T13-N03 ask whether that same pen can work without a cap; N04-N18 explain the mechanism and the resulting paper choices. These sections advance the pen's usefulness and limits rather than introducing an unrelated subject or list. |

## Required repair

At E12, make the repeated 2004 decision an explicit callback to H07, or keep that fact only once while preserving H07's unresolved store question and T01's answer. Recheck `no_recap` after the change. No author-script edit is made in this reader branch.
