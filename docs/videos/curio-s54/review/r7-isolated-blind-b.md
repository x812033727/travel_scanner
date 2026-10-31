# S54 R7 isolated blind panel B

**Verdict:** 11 Yes, 2 No. The failed questions are `payoffs` and `no_recap`.

I read the official output of `node tools/video/cli.mjs narrative --slug curio-s54`: the rendered narration, chapter headings, and 13 audience questions. I did not read the five author files as prose, source material, or any other review. This is a narrative judgment, not a historical fact check.

The five author files match `author-freeze-7.md` by SHA-256:

| File | SHA-256 |
| --- | --- |
| `research.md` | `47642150198fa8dcc9a9991a5be9497dfd1f0db4a3085ff3f7d74f7f53126336` |
| `brief.md` | `21f69885d15e85cb2e30a8e7a6407fde7d9e9ead5b6097250a61e8e2f1b8eba6` |
| `claims.md` | `d721b5117622d10d1ce046936d8cd96effe96c94bdbc39b694f4c026aef5b0a8` |
| `video.json` | `049ad513e7e5600a331e71ccdc2bda308a244a971074caffb8df16cbb9b3f87d` |
| `script.md` | `3c8f44af5d1af7a8f5c65e71e8866faa12d32ff0ff09e89f408291b132791684` |

| Audience question | Answer | Evidence from the blind narration |
| --- | --- | --- |
| `scene_first` | Yes | s54001–s54003 place a sender and clerk at a post office counter on 10 January 1840, handling and weighing a letter. |
| `no_spoiler` | Yes | s54002–s54007 leave the missing stamp, payment trouble, diary number, and missing word unresolved. |
| `one_line` | Yes | After the opening, the story moves from the old rate and Hill's proposal through August, December, January, and May. |
| `no_toc` | Yes | Transitions pose story questions; s54083 returns to the opening letter without announcing a section list. |
| `chapters_link` | Yes | s54008→s54009 answers the old-rate question; s54042→s54043 answers who sets the date; s54107→s54108 begins the stamp authorization answer. |
| `open_loops` | Yes | Unresolved turns recur within 90 seconds, for example s54029, s54042, s54054, s54069–s54074, s54081, s54098, s54107, and s54118. |
| `payoffs` | **No** | s54110 asks who opposed sales at the three general post offices. s54111 says only “the department” (部門), leaving which department unclear. |
| `no_recap` | **No** | s54075 says stamps still awaited printing; s54104 again says adhesive stamps were still being printed, without an explicit callback. |
| `chapters_are_events` | Yes | The seven headings identify a counter transaction, old letter and parcel route, envelope proposal, law, trial, crowd, and stamp use. |
| `outro_no_next` | Yes | s54997–s54999 close on the letter, sources, and subscription without naming another video. |
| `opening_hooks` | Yes | s54004 raises the diary number, s54005 the payment trouble, and s54006–s54007 the missing word after the first scene. |
| `one_thread` | Yes | The problem of prepaid postage before stamps follows Hill's proposal, cash collection, and eventual usable stamps. |
| `no_detour` | Yes | Old rates motivate prepayment; January crowds expose the cash bottleneck; May supply and cancellation test the stamp as payment proof. |

The machine-readable answers are in `r7-isolated-blind-b.json`.

I passed that file back to the official CLI with `--answers` and an isolated `/tmp` workdir. Its verdict has 11 Yes, 2 No, exactly the two failures above, with no malformed evidence. The CLI exits 1 because required questions failed.
