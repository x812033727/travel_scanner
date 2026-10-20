# S53 R3 fresh blind narrative review A

Scope: the 13 official questions embedded in the output of `NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s53 --json`. I read no brief, claims, video.json, tasks, prior reviews, media, or site files. Verdict: **11 pass, 2 fail**.

Hashes are separate because the CLI narration string and the script file are different review artifacts:

- Script file bytes, `docs/videos/curio-s53/script.md`: `06f5fda2ff565fa20ab698fa1a4ffcf4e4528beffc94ce16a0185c95aaaf7548` (hashed without opening its prose).
- Parsed JSON narration string as UTF-8: `0a33a405997285f75fbe1870bbd27ada63f10f352162a76f9066ca26c1bf9d2e`.

| Question | Verdict | Evidence and reason |
| --- | --- | --- |
| `scene_first` | Pass | `s53001`–`s53004` put cottages in 1907 San Francisco squares and give the Park Commission a dated clearing action. |
| `no_spoiler` | Pass | `s53002`, `s53004`, and `s53006`–`s53008` set up the deadline and questions; `s53071` withholds the missed-deadline outcome until later. |
| `one_line` | Pass | The preview at `s53001` resets to the disaster at `s53010`, then advances through construction `s53028`, purchase `s53058`, clearing `s53069`, and survey `s53101`. |
| `no_toc` | Pass | `s53006`–`s53008`, `s53048`, and `s53083` ask story questions; they do not announce sections or list the video structure. |
| `chapters_link` | Pass | The six handoffs have concrete links: `s53009`→`s53010`–`s53011`, `s53027`→`s53028`, `s53048`→`s53049`, `s53068`→`s53069`, `s53083`→`s53084`, and `s53100`→`s53101`. The first is the permitted reset to the disaster behind the cottages. |
| `open_loops` | Pass | Hooks at `s53006`, `s53023`, `s53048`, `s53061`, `s53068`, `s53083`, `s53097`, `s53104`, `s53111`, `s53116`, `s53123`, and `s53129` keep the body supplied with unresolved specifics within 90-second intervals. |
| `payoffs` | **Fail** | Rent and moving-cost questions do pay off (`s53006`→`s53057`–`s53058`; `s53007`→`s53073`, `s53091`–`s53092`). But `s53116` asks if a cottage can remain when its land lease ends; `s53117` says the survey cannot predict that outcome. This leaves the question as phrased unanswered. The audience-choice prompt `s53998` is a reflection rather than a factual promise. |
| `no_recap` | Pass | `s53069` explicitly recalls the opening deadline in `s53002`. The later figures concern different measures: moved cottages `s53084`/`s53087`, buyers `s53110`, and buyers paid in full `s53113`. |
| `chapters_are_events` | Pass | The headings anchored by `s53001`, `s53010`, `s53028`, `s53049`, `s53069`, `s53084`, and `s53101` name events, situations, or findings. |
| `outro_no_next` | Pass | `s53997`–`s53999` end with the rent issue, a viewer choice, and a subscription invitation; no next installment is mentioned. |
| `opening_hooks` | Pass | After the square scene `s53001`–`s53005`, `s53006`–`s53009` plant payment, moving-cost, survey, and land questions. |
| `one_thread` | Pass | The movable cottage and its site run from ownership `s53004`–`s53005` through contract `s53048`/`s53060`, removal `s53072`, relocation `s53084`, and surveyed land tenure `s53103`/`s53115`. |
| `no_detour` | **Fail** | Lumber sourcing and transport `s53019`–`s53022`, the allocation-category list `s53033`–`s53036`, and the room-count inventory `s53039`–`s53044` occupy blocks without advancing the opening's moving, land, and payment problem. |

The two failed questions are script-level findings only. No author text, media, or site files were changed.
