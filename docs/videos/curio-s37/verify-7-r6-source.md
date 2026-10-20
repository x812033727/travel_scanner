# Curio S37 R6 independent source and prompt audit

**Result: pass; 0 source or visual blockers found.** Repository episode files were read only. This is an audit of script, claim mapping, source text, and written prompts; no paid media generation or rendered-image inspection occurred. My sealed blind narrative review is `/tmp/curio_s37_r6_fresh_blind_seal.md` (13/13 Yes, recorded before opening these source files).

## Identity and coverage

| File/input | SHA-256 or identity |
| --- | --- |
| `docs/videos/curio-s37/script.md` | `40f08a2c803462115895102ab91cfbd192f209bd766a8bc070495c1b27cecc1f` — requested exact hash matched |
| `docs/videos/curio-s37/research.md` | `1ec72d72d9b22aa4ba06654ee07886a78b5a754605b404e0140d0e0776b42bbd` |
| `docs/videos/curio-s37/claims.md` | `bf58eec85d6579dc06ab20a9f6a35c396b777fe816f6aa5b5a3377577c412a7d` |
| `docs/videos/curio-s37/video.json` | `b9a5576809829ca60bb1388fca3bf387cf3a453c8498638101ac27620e2e4af4` — requested exact hash matched |
| Fresh pinned source fetch | `GITenberg/Letters-of-Pliny_2811` commit `959ded9fab0f9d54768d2dbfad860b79c864c4c8`, `2811.txt`, downloaded to `/tmp/curio_s37_r6_fresh_pinned_2811.txt`; SHA-256 `9f5fd6bc997d9386987a0d5ae184961f2c0f88f9a8912baa0cd7848687da4995`, exactly the hash in `research.md`. Letters LXV–LXVI are source lines 3500–3732. |
| Blind seal | `8df4869706f5ad9203b88d100a444033b7ad04f44896ba7e460e79a65059417a` |

The source itself identifies William Melmoth as translator and F. C. T. Bosanquet as reviser. It is a pinned English translation, not a checked Latin critical text. `research.md` states that limit correctly; neither script nor metadata asserts a certain calendar day or Latin wording. The source text's August 24 line (3520) is omitted from the narration, appropriately leaving the date dispute unresolved.

**Mechanical cross-check:** `script.md` has 91 spoken text lines; `claims.md` has 91 distinct ID rows; `video.json` has 91 distinct spoken line IDs across 89 scenes. Every spoken text and ID matches between claims and `video.json` in order, and every spoken text matches `script.md` in order: **0 mismatches**. There are 88 `shot` scenes with 88 nonempty, distinct prompts, followed by one `outro` scene containing `pl099`–`pl101` and no image prompt. No duplicate scene IDs or blank shot prompts. All claim source codes are defined by `research.md` (`L65a`–`L66d` or `EDIT`).

## All 91 spoken/claim/source rows

I read each source claim against the pinned translation. The following groups enumerate every row in narrative order; the cited source lines are the controlling evidence, including the mixed-source opening and ending. Each group also received a prompt check for every `shot` ID in it.

| IDs audited | Pinned source lines | Source and image judgment |
| --- | --- | --- |
| `pl001, pl002, pl003, pl004, pl005, pl006` | 3519–49, 3600–17, 3627–30, 3655–59, 3676–86, 3686–91 | Opening previews road, crowd, rescue ship, mother, uncle, and witnessing without reporting their results. The road and mother are the Misenum sequence. Six prompts keep it on the bay and do not put the nephew aboard the ship. |
| `pl007, pl008, pl009, pl010, pl020, pl011, pl012` | 3519–36 | Uncle's fleet command, mother's cloud alert, his meal/book, pine-like shape, changing cloud color, initial mountain uncertainty, and later Vesuvius identification align. Seven prompts stay with the uncle and cloud. |
| `pl013, pl014, pl015, pl016, pl017` | 3537–45 | Light vessel, invitation declined for assigned writing, Rectina's note, her villa at Vesuvius's foot, and sea escape align. Five prompts never show the nephew joining the voyage. |
| `pl018, pl019` | 3546–54; 3634–35 | The shift to rescue galleys and uncle's sailing align; the transition to the nephew remaining at Misenum is explicit. Two prompts show only the uncle in the harbor/vessel. |
| `pl114, pl047, pl048, pl021, pl049, pl050, pl051, pl046, pl052, pl023, pl053` | 3634–52 | Remaining study, bath/supper/uneasy sleep, unusual quake, mother and son seeking one another, small open court, Pliny's stated age 18 and Livy extracts, and Spanish friend's reproach align. Eleven prompts keep the night lamp setting, with faint dawn only at `pl053` as the source reaches morning. |
| `pl054, pl025, pl055, pl026, pl115` | 3652–60 | Dim morning, unstable buildings and narrow court, decision to leave town, crowd pressing from behind, and stopping at a distance from houses follow the source in order. Five prompts show dim dawn and departure, without recapping the same fact. |
| `pl056, pl057, pl058, pl027, pl059` | 3660–67 | Chariots rocking despite large stones, sea withdrawal, enlarged shore, stranded sea animals, and the black cloud on the other side align. Five prompts depict these as the nephew's observations. |
| `pl060, pl028, pl061, pl111, pl062, pl063, pl064` | 3666–78 | Black cloud/flashes/flame, Spanish friend's conditional advice about the uncle, the mother's and nephew's reply, friend's exit, and cloud concealing Capreae and the Misenum promontory align. Seven prompts show the bay/road, not an independently verified fire in the town. |
| `pl065, pl029, pl110, pl067, pl068` | 3679–86 | The mother begs, urges and commands him to flee; her age and limited ability to escape; her willingness to meet death if she was not the cause of her son's death; his refusal and taking her hand; her reluctant compliance and self-reproach all align. Five prompts place this exchange on the Misenum road. |
| `pl069, pl070, pl030, pl071, pl072, pl031, pl073` | 3686–97 | Initial light ash, approaching dark mist, fear of falling beneath the crowd, leaving the main road, sitting down, and room-like darkness align. Seven prompts move from dim daylight into ash darkness, without turning it into ordinary night. |
| `pl074, pl032, pl075, pl112, pl033` | 3694–3701 | Voices seeking relatives, fear for self/family, fear of death, pleas to gods, and an end-of-world belief are correctly framed as contemporary experience/belief. Five prompts keep the scene in the ash darkness. |
| `pl076, pl077, pl034, pl078, pl079, pl080, pl081, pl092, pl082` | 3702–15 | The town collapse/fire reports are expressly false; a temporary glow is perceived as approaching fire rather than the return of day; distant fire, renewed darkness, heavy ash, repeated shaking off, and Pliny's own fearful interpretation align. Nine prompts do not depict Misenum actually collapsed or on fire. |
| `pl083, pl035, pl036, pl084, pl085, pl037, pl113, pl086, pl087` | 3715–27 | Real daylight returns, sun remains dim, tired eyes and ash-covered objects, return to Misenum, anxious night with continuing quake and fearful predictions, and remaining until news of the uncle align. Nine prompts move from muted returning daylight (`pl083`–`pl084`) to interior/night lamplight (`pl037`–`pl087`). |
| `pl088, pl045, pl043, pl089, pl091, pl099` | 3563, 3600–17, 3625–30, 3719–27 | Stabiae shore death, discovery on the third day with intact clothing/no visible violence, Pliny's own conjecture about harmful vapor and weak throat, his eyewitness/immediate-report distinction, Tacitus's later question, and Misenum rather than Pompeii align. Five shot prompts depict the adult letter writer, never the younger man witnessing his uncle's final moment or a visible corpse; `pl099` is the outro. |
| `pl100, pl101` | `EDIT` | Audience question and subscription line make no historical fact claim; both are in the outro scene without prompts. |

**Focused checks:**

- `pl054` (script L139) says dawn is present yet faint; `pl025` (L143) supplies the new courtyard danger from shaking buildings (source 3652–55). `pl055` (L147) performs the departure; `pl026` (L151) adds the crowd's pressure and asks about stability (source 3655–60). These adjacent beats are not duplicate facts.
- `pl110` (script L217) is a fair, careful paraphrase of the mother's conditional willingness to die rather than cause her son's death (source 3679–83). It does not put a direct quotation in her mouth.
- `pl087` (script L349) only says the mother and son remained in Misenum awaiting news; it does **not** claim daylight returned after their anxious night. Its prompt is explicitly `low night oil-lamp light`, matching source 3720–27.
- `pl043` calls fatal vapor a conjecture, as the translation does at 3606–09; `pl089` says the uncle's shore death was learned afterward, consistent with the nephew at Misenum (3613–17 and 3627–30). No shot shows young Pliny in Stabiae or aboard the rescue vessel.
- Rumors (`pl076`–`pl077`) and end-of-world fear (`pl075`, `pl092`) are labeled as false report or fear, respectively. Visual prompts do not assert these as independently verified events.

**Minor, nonblocking precision notes:** `pl027` and `pl059` prompts place the observing son at or by the exposed shore, whereas the letter establishes the exposed shore and sea creatures but does not specify his exact footing (3663–67). This is illustrative spatial inference, not a contradiction. In the opening, the singular `這封信` in `pl003` can momentarily suggest one letter contains both later hooks, but `pl006` explicitly says the scenes belong to the same *set* of letters; the script and claims then separate LXV and LXVI. Neither issue changes the source result.

## Lint and boundary

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s37` exited 0: **0 errors, 0 warnings**, 91 lines, 1,957 spoken units, estimated 9.4 minutes, eight estimated chapters. `git status --short -- docs/videos/curio-s37` was empty after checking. No episode file was modified, and no TTS, images, music, or other paid media were requested. The prompt review cannot certify how a future generated picture actually renders; its precise result is 88/88 written prompts reviewed, with 0 prompt/source contradictions found.
