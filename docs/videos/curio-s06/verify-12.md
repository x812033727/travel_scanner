# S06 ninth script candidate: R8 source, transition and picture repairs

The R8 reader audited the exact preceding script `bfcb714f…` in `verify-r8.md`. Its 12/13 narrative receipt failed `chapters_link`; the reader disclosed that three picture prompts were visible before their narration answers were sealed, so that round is a qualified read rather than strict narration-only clearance. It also found two source wording errors and eight picture pairings needing repair. No paid S06 pictures were ordered.

This candidate is `script.md` SHA-256 `e068b9f6a6ea0c5f151e105c4612ac8643f2ae123211649197ee099809f70f04`, narrative hash `4f52c60fc3a68f6a`, 81 spoken lines and 80 still prompts. `claims.md` matches all 81 IDs and spoken texts; lint reports 0 errors and 0 warnings. It awaits a new **strict narration-only** reader, a fresh pinned-source/prompt check, and measured narration. The previous R8 receipt must not be reused for this hash.

## Repairs made against the fixed original texts

- `gs001` now says the arriving physician **帶著藥囊**, matching the novel's `臂挽青囊` without saying he wore it on his back. The picture shows a satchel over his arm; `gs011` shows the blue-green bag carried from the arriving boat. Novel pin N, chapter 75, lines 29–39.
- `gs046` now distinguishes Cao Cao's later **serious illness** for which he ordered Hua Tuo to attend him from the earlier `頭風` episode. The historical text says `得病篤重，使佗專視` after an earlier headache passage; it does not identify the severe illness as that headache. Hua's departure, claim about his wife's illness and Cao Cao's summons remain unchanged. Historical pin H, lines 28 and 30.
- `gs020` now asks which event begins Chen Shou's treatment account, and the next chapter answers at `gs022` with the `流矢`. `gs023` supplies the source's `嘗` while `gs116` no longer repeats the quoted arrow term. The later question about the unnamed doctor still pays off at `gs033`. Historical pin G, lines 17–18.
- `gs014` now pictures the right arm extended as spoken. `gs016` shows the proposed **post and ring** with head covering, not an armrest; the novel says Guan Yu rejects that restraint. `gs119` shows blood in the vessel, consistent with `盈於盤器`. `gs047` shows Hua escorted into custody. `gs115` no longer cues a child before the answer. `gs074` presents the spoken meal versus game contrast. Novel pin N and history pins G/H as assigned in `claims.md`.

At 250 spoken units per minute, the new timeline estimates 539.77 s total and 499.03 s (8:19.03) for the story body `gs007–gs074`, excluding opening and CTA. This is **not** actual TTS duration; existing WAVs and the older timeline are stale. Do not buy images until the new exact-hash read passes and regenerated audio proves at least 480 s of story body.
