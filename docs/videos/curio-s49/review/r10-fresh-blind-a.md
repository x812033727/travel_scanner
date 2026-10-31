# S49 R10 fresh blind narrative review — panel A

**Result: 12 pass, 1 fail.** I reviewed only the JSON output of the narrative CLI command. I hashed `script.md` as raw bytes without reading its prose. No brief, claims, `video.json`, tasks, or earlier reviews informed this panel.

| SHA-256 target | Digest |
| --- | --- |
| **Script file bytes**: `docs/videos/curio-s49/script.md` | `c6389ff27c36856a914442644b71f746c66a89ddb1bd8f0f14a3f086d09fa51c` |
| **Narration string UTF-8** from the narrative CLI JSON | `85b3b2473e49caa9cfe8fc8ccfe2525599e9f932208bdb1480dad9860b3695c0` |

| Official question ID | Verdict | Narrative evidence |
| --- | --- | --- |
| `scene_first` | Pass | `moon001`–`moon004`: August 1835 New York newspaper, its claim, Herschel, and a purported messenger establish a concrete document event. |
| `no_spoiler` | Pass | `moon004`–`moon008` raise the letter, optical, second-observation, and editor questions without their answers. `moon003` is scene context. |
| `one_line` | Pass | `moon009`, `moon032`, `moon056`, `moon079`, `moon100`, `moon112`, `moon132` follow the same newspaper claim from construction to reception. The 1859 reprint at `moon112` is the evidence frame for the 1835 response quoted at `moon117`, not a second retelling. |
| `no_toc` | Pass | `moon008`, `moon028`, `moon055`, `moon098`, `moon111` ask about the next concrete claim or response; none lists the video's planned sections. |
| `chapters_link` | Pass | `moon008`→`moon009`, `moon031`→`moon032`, `moon055`→`moon056`, `moon078`→`moon079`, `moon099`→`moon100`, and `moon111`→`moon112` carry a named question, object, or consequence across every boundary. |
| `open_loops` | Pass | Questions recur at `moon018`, `moon038`, `moon055`, `moon061`, `moon073`, `moon083`, `moon098`, `moon111`, `moon121`, and `moon128`; nearby prompts also fill the intervals. |
| `payoffs` | **Fail** | `moon018` asks where the cited supplement can be found. `moon019` merely repeats that the article claimed it as a source; no later line plainly answers availability or location. `moon022` asks about **each** named witness's original material, while `moon023` speaks chiefly to the claimed route and letters. Give the supplement a source-supported answer, and answer or narrow the all-witness question. |
| `no_recap` | Pass | `moon003`→`moon009` and `moon024`→`moon093` are identifiable callbacks. The figures at `moon123`–`moon124` are assessed at `moon125` without repeating them. |
| `chapters_are_events` | Pass | Chapter openings `moon001`, `moon009`, `moon032`, `moon056`, `moon079`, `moon100`, and `moon112` correspond to happenings or reveals named in their headings. |
| `outro_no_next` | Pass | `moon999a`–`moon999c` ask for a response, give source links, and invite subscription without announcing another installment. |
| `opening_hooks` | Pass | `moon004`–`moon007` hold four distinct later questions open after the first scene. |
| `one_thread` | Pass | `moon006`, `moon041`, `moon070`, `moon095`, `moon118`, and `moon132` keep returning to the test of whether precise claims amount to independently checkable observation. |
| `no_detour` | Pass | `moon010`–`moon012` establish borrowed authority; `moon030`–`moon053` build the supposed optical mechanism; `moon065`–`moon075` escalate claimed details; `moon112`–`moon132` test reception. Each serves the opening question. |

**Specific revision:** After `moon018`, state what a reader can actually inspect of the alleged journal supplement, with support for that statement. For `moon022`, either state which original materials can be checked for the named witnesses or ask the narrower letter question that `moon023` answers.
