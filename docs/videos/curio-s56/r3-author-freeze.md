# S56 R3 author freeze and independent review handoff

2026-10-20 UTC. This is the author revision for the five required failures in the [R2 official OR merge](review/r2-isolated-merge.md): `one_line`, `chapters_link`, `payoffs`, `no_recap`, and `no_detour`. It is a frozen input for a new independent source and written visual audit and two isolated narrative readers. The author has not judged this revision's source or narrative gates as passed.

| File | SHA-256 |
| --- | --- |
| `script.md` | `b76995caa74f0a1f65b068d9e115659d7c48678600b80e9ff502e641a6505152` |
| `video.json` | `0196dcf2d80fd79e2d64ad58d8e768959373073f961a4c6c1322f552b768d95a` |
| `claims.md` | `613316600ea6f61f11f2ad7f8656655346a214c66fa080a5acb88cba40d00b99` |
| `brief.md` | `a17b3ac122723c1229bdb1bcf1af2c546b7665407bad5677a24658ad50583dfd` |
| `research.md` | `59549e98e6ae258cedfc5b43e6684ecaa1102284d0dee13b0beef6443e4a6fb7` |

## Author changes

- The opener [s56005]–[s56013] stops before the new fire behind Foster is revealed. [s56070]–[s56073] return to that east bank with named callbacks and add the letter's 80-yard and 400-yard observations at the point of discovery. [s56029]–[s56033] state the prior night's non-crossing once and move into the city's wooden fuel.
- Loesch's north-side night account, previously R2 `s56127`–`s56143`, now occupies R3 `s56117`–`s56133`; Foster's 3 a.m. bridge and dawn account, previously R2 `s56117`–`s56126`, now occupies R3 `s56134`–`s56143`. The ID remap is sequential, and scene prompts moved with their events. The next chapter therefore reaches Monday morning after both night accounts. [s56014], [s56117], and [s56145] answer the preceding chapter's concrete question in their first sentence.
- [s56102] asks about the small belongings Foster left out of his trunk; [s56108] answers that he had no time to pack them. The source says he let those items take their chance, so the narration does not claim a witnessed fate for each object. [s56163]–[s56167] describe Loesch's well-water plan for wet wraps, then say rain arrived before that plan faced the grass fire.
- [s56109]–[s56113] keep only the car's escape action and the hotel's ignition, removing the fare negotiation. The biscuit stop is replaced at [s56143] with the continued north-side fire. [s56145]–[s56155] move from lost water to the northward evacuation without repeating the shortage.
- `brief.md` now matches the withheld opening result, the order of the two night witnesses, the omitted fare detail, and the limited rain payoff. The pinned F and L research files and `video.json`'s two source URLs remain unchanged. No witness is shown seeing a tracked ember cross the river, the pumping station's destruction firsthand, or a proven counterfactual rescue.

## Mechanical checks and production boundary

`node tools/video/cli.mjs script --slug curio-s56` regenerated `script.md` from this `video.json`. `node tools/video/cli.mjs lint --slug curio-s56` returned **0 errors, 0 warnings**, with a 00:59 opener and an estimated 14.4-minute total. The file has seven chapters, 176 unique ascending spoken-line IDs, 176 matching `claims.md` rows with pinned source line links, 141 scenes (137 written `shot` prompts and four `big` cards), and 17 ordered setup/payoff loops. The 199-Han-character opener is inside the 30–60-second lint window; the 2,752-Han-character body is about **8.47 minutes** at the fastest approved planning pace of 325 Han characters per minute. Actual eight-minute body duration still requires TTS measurement. `git diff --check` passed.

The opening remains the first chapter, so the series' five-second intro is placed after it in assembly. The established 21-second outro has the final 16 seconds reserved for YouTube Studio's clickable end-screen elements. The description still contains the two pinned source links and the channel link; `youtube.video_id` remains null, so actual end-screen targets await private upload and Studio verification. No TTS, images, music, or other paid media were generated in this revision.

Next: an independent reviewer should reopen both fixed-source texts, verify every changed narration line and written image prompt against the frozen hashes, then pass the same script to two fresh isolated narrative readers. No author self-review receipt substitutes for those gates.
