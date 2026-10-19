# Curio S19 R5 independent source and visual audit

Frozen `docs/videos/curio-s19/script.md` SHA-256: `a68cc615c3d79ad7b1cac7002d5a20179b2f6cc09b1e739071e4f479e0d7eb5a`. Blind answers were sealed before opening S19 evidence in `/tmp/curio-s19-blind-a68cc615.json` (SHA-256 `b489fca0cdfa1b0edbc505fa24afc45ee650ed65d9f512ad4c163fab5c4962b0`). Canonical `/workspace/.video-work/curio-s19/review/narrative.json` passed 13/13, round 5.

## Independent source verification

- Fetched pinned 1887 *Le Rappel* transcription to `/tmp/curio-s19-rappel-77985.txt`; SHA-256 `91d3e9397aca543f900c9babd37fd2489097677a3eb378f5944e5af7af14f9ec`, matching `research.md`. Lines 89–92 describe the protesters' imagined twenty-year shadow; lines 133–140 report Eiffel's twenty-year operating right and later Paris City discretion. These lines contain no compulsory demolition order.
- Fetched pinned 1913 *L’Illustration* transcription to `/tmp/curio-s19-illustration-38842.txt`; SHA-256 `db280680282f567c9510a13b2fd83b576b0ab66dd8817d5cfca7bd7f06a7a22b`, matching `research.md`. Lines 1676–1693 report repeated Eiffel Tower–Washington wireless exchanges and a planned longitude measurement; this passage does not give a municipal keep-or-demolish decision.
- All 110 `video.json` narration IDs have exactly one `claims.md` row; wording matches exactly, with no missing or orphan IDs. All 130 source links in `claims.md` use the two correct pinned revisions and existing source line numbers. The mapped substantive claims sampled against both full passages showed no source contradiction. `lint --slug curio-s19 --json` returned 0 errors / 0 warnings.
- Original 1887 agreement, 1909 municipal disposition, and official radio history remain unverified. Current narration expressly limits its conclusion to the read newspapers and avoids claiming wireless saved the tower.

## Story length and visuals

`estimateTimeline` gives opening 41.2 s; story body from second chapter to outro 498.733 s = 8:18.733 (99 lines); outro 15.4 s. This is an estimate with only 18.733 s margin over the eight-minute floor. Recheck against measured current-script TTS before production approval.

All 100 illustration prompts were paired with adjacent narration. No blocking contradiction was found at the prompt stage. Watch the generated keyframes for these nonblocking risks:

- `eiffel-020`: the prompt's `one visitor looking uneasily at an imagined fairground` could render a visitor as physically present in 1887, whereas the narration says foreigners had not yet arrived and the petition imagined their reaction.
- `eiffel-056`: narration says people had only geometric drawings, but the prompt focuses on an engineer `facing an unseen construction site`, a weak match that could obscure the drawing argument.
- `eiffel-059`: narration concerns curves of the tower's four *edges* from wind calculations; the prompt focuses on a single curved iron brace, potentially changing the visual object.
- Internal `video.json` loop `ea110→ea111` says `鉚接鐵皮柱`; the source (`boulonnée`) and narration say `螺栓鐵皮柱`. This is a metadata wording mismatch, not spoken narration.

No paid media was generated or source files edited in this audit. Before sealing the S19 blind answers, exposure was limited to the task's title/hash, the general curio skill and narrative procedure, and S19 script/video narration; no prior S19 claims, research, review, or ticket was opened.
