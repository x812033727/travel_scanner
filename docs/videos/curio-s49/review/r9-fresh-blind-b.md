# S49 R9 fresh blind narrative review — panel B

**Basis:** Only the `narration` and 13 official `questions` returned by `NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s49 --json` were read. SHA-256 of the UTF-8 narrative string: `579d359cd086437f9363cacf655403cad71b5da8b22ec0104de832d89c1f5cc8`. The byte hash of `docs/videos/curio-s49/script.md` is `10f912c63ba438c676372469e8e44a52a8252113efc22f3af9fb74f91ae22354`; its prose was not read. No brief, claims, video metadata, tasks, or prior reviews were read.

**Result:** 12 pass, 1 fail.

| Official question | Result | Line-based judgment |
| --- | --- | --- |
| `scene_first` | Pass | `moon001`–`moon004`: an August 1835 New York paper reaches readers and presents Herschel and a purported assistant. The document and missing letter make the first four lines a concrete scene. |
| `no_spoiler` | Pass | `moon004`–`moon008` raise the letter, optics, corroboration, and press-response questions without giving their later answers. |
| `one_line` | Pass | `moon009`→`moon032`→`moon056`→`moon079`→`moon100` develops the same newspaper story. `moon112` introduces a later reprint as the source through which earlier press reactions, including `moon117`, are uncovered. |
| `no_toc` | Pass | `moon008`, `moon055`, `moon078`, and `moon111` are story questions, with no announcement of an upcoming section plan. |
| `chapters_link` | Pass | `moon008`→`moon009` returns to Herschel's name; `moon031`→`moon032` to the heavy tube; `moon055`→`moon056` to the first view; `moon078`→`moon079` to the shape; `moon099`→`moon100` to smoke; `moon111`→`moon112` to editors' responses. |
| `open_loops` | Pass | The body keeps questions active well inside 90 seconds, including `moon026`, `moon038`, `moon044`, `moon050`, `moon055`, `moon061`, `moon073`, `moon078`, `moon083`, `moon094`, `moon104`, `moon111`, `moon116`, `moon126`, and `moon128`. |
| `payoffs` | Pass | The delayed opening hooks point back to their subjects: assistant's letter `moon004`→`moon023`, light `moon005`→`moon041`, second observation `moon006`→`moon118`, and editors `moon007`→`moon111`–`moon115`. Nearby payoffs include first image `moon055`→`moon056`, winged shape `moon078`→`moon079`, fire `moon098`→`moon100`, and Jacoby's source `moon128`→`moon129`. The supplement's checkability resolves at `moon027`, after `moon018`. |
| `no_recap` | **Fail** | The absent independent paperwork is repeated in one short run. `moon023` says the assistant's transmission route is not an actual located letter; `moon026`–`moon027` say the named supplement, letter, and Royal Society papers reach readers only through the article; `moon029` again says the article has not supplied those documents. The last statement adds no evidence before the instrument sequence starts. |
| `chapters_are_events` | Pass | The headings at `moon001`, `moon009`, `moon032`, `moon056`, `moon079`, `moon100`, and `moon112` describe developments or reveals: a paper appears, a name is borrowed, a mirror is described, lunar life appears, a fire occurs, and a reprint reveals responses. |
| `outro_no_next` | Pass | `moon999a`–`moon999c` offer a viewer question, source links, and subscription, with no next episode or video preview. |
| `opening_hooks` | Pass | After the first scene, `moon004`–`moon007` supply four concrete unresolved moments: letter, optical fix, second observation, and skeptical editors. |
| `one_thread` | Pass | The paper and the problem of apparent verification connect the opening `moon001`–`moon008`, reported lunar scenes `moon056` and `moon079`, the interruption `moon100`, later reactions `moon111`–`moon130`, and conclusion `moon132`. |
| `no_detour` | Pass | Saturn at `moon108` is a brief continuation of the report's claims. The press and publisher material `moon112`–`moon130` bears directly on the opening question at `moon007` about whether others believed it. |

**Focused fix:** In the source-document stretch, retain the question and one clear answer at `moon026`–`moon027`, then move into the mirror at `moon030`; the additional nonproduction statement at `moon029` is the clearest repeat.
