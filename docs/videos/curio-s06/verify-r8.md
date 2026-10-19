# S06 round 8 independent verification — qualified blind read

Frozen script: `script.md` SHA-256 `bfcb714f53b9b19b79ac8779eb459f55fd8eda92f9938d1fe0e342149b90b9a0`. I checked the 81 spoken lines in `video.json` against the 81 rows in `claims.md`; every ID and line matched. I then checked those rows against the four original texts at the commits pinned in `video.json`, and compared all 80 shot prompts with their paired narration. The final CTA is scene 81 and has no picture prompt.

## Blindness disclosure and panel result

This was **not a strict narration-only blind read**. Before sealing answers, I read the required Curio skill, the frozen script, and the current 13-question panel. While locating the narration field in `video.json`, I also printed the full objects for `gs001`, `gs002`, `gs074`, and `gs076`. That exposed picture prompts for the first three IDs and outro card data. I had **not** read `claims.md`, `research.md`, any pinned source passage, prior review contents, or task notes before sealing. After sealing, I read the claims and pinned passages. A later directory listing showed names of prior review files; I did not open their contents.

Raw answers were sealed at `/tmp/curio-s06-blind-raw-r8.json` (SHA-256 `021317dd02edc3e96b8875027fc6883165b57aaa482fbafafd88d69ada236c5f`). I ran:

```sh
VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s06 --answers /tmp/curio-s06-blind-raw-r8.json
```

It exited **1**, with **12 yes and 1 required no**: `chapters_link`. The canonical round 8 verdict was copied to `/tmp/curio-s06-canonical-verdict-r8.json` (SHA-256 `a3e9ea01077c87144b06ac136390e6a7de919aad8cc661b43b4c544ef5237f6d`). `gs020` ends the novel chapter by asking whether the history gives the doctor the same name: 「換成史書，還找得到同一個名字嗎？」 The next chapter opens at `gs022` with the arrow and 「嘗」, leaving that precise question untouched until `gs033`. Revising the `gs020` question to lead into the historical arrow account would connect the chapters while retaining the later name reveal. A wholly fresh narration-only reader should recheck the repaired script.

## Pinned-source check: 81/81 lines

| Pin | Original passage used |
| --- | --- |
| G | [〈關羽傳〉 lines 17–18](https://github.com/Ancient-China-Books/sanguozhi/blob/10a0b1ab3019d8821262f7402366d14fb4aaa102/OEBPS/Text/036.htm#L17-L18): undated left-arm wound and next paragraph's Jian'an 24 Fan campaign |
| H | [〈華佗傳〉 lines 28, 30](https://github.com/Ancient-China-Books/sanguozhi/blob/10a0b1ab3019d8821262f7402366d14fb4aaa102/OEBPS/Text/029.htm#L28-L30): Cao Cao's headwind, later illness, Hua Tuo's death, and Cao Chong |
| C | [〈曹沖傳〉 line 19](https://github.com/Ancient-China-Books/sanguozhi/blob/10a0b1ab3019d8821262f7402366d14fb4aaa102/OEBPS/Text/020.htm#L19): 倉舒, age 13, Jian'an 13 death, Cao Cao's grief |
| N | [《三國演義》第七十五回 lines 29, 32, 39](https://github.com/Ancient-China-Books/sanguoyanyi/blob/761813427eb5685c395804493f9fbd7ad8dc7d8d/OEBPS/Text/451.html#L29-L39): right-arm Fan story, named physician, chess, treatment, and farewell |

**79 lines** are supported by their pinned passages or clearly framed as questions or interpretation. Two details need correction:

| Line | Spoken wording | Original and issue |
| --- | --- | --- |
| `gs001` | 「一位背著藥囊的醫生到了」 | N line 32 says 「臂挽青囊」: he carried the bag on his arm, not on his back. 「帶著藥囊」 would preserve the scene without changing the carried position. |
| `gs046` | 「曹操要華佗專治頭風」 | H line 28 records recurring 「頭風」. H line 30 later says 「得病篤重，使佗專視」 but does not identify this later illness as headwind. The line combines the passages more specifically than the source allows. |

The central chronology is supported with its stated limit: G line 17 gives no surgery date or doctor's name; G line 18 dates the Fan campaign to Jian'an 24 (219 CE); H line 30 places Hua Tuo's death before Cao Chong's illness; C line 19 dates Cao Chong's death to Jian'an 13 (208 CE). This rules out Hua Tuo reaching the **novel's 219 Fan tent**. It does not identify or exclude the unnamed doctor in G's undated earlier treatment.

## Picture-prompt check: 80/80 shots

**72 prompts** paired with the narration without an observed conflict. Two prompts materially conflict with the described object or state:

| Line | Prompt wording | Narration/source conflict |
| --- | --- | --- |
| `gs016` | “a plain empty armrest and a folded cloth” | The narrated proposal is a **pillar with a ring** and head covering; N line 32 likewise has 「立一標柱，上釘大環」. An armrest substitutes a different prop. |
| `gs119` | “an empty shallow bronze vessel” | The line says the historical account records blood in the vessel; G line 17 says 「臂血流離，盈於盤器」. “Empty” reverses that detail. |

Six further pairing issues are weaker and can be handled during prompt refinement: `gs001` omits the medicine bag, `gs011` omits the 青 color of the bag, `gs014` depicts the physician entering instead of Guan Yu extending his right arm, `gs047` obscures that Hua Tuo was taken into custody, `gs115` cues a child with a small chair before the next line answers who fell ill, and `gs074` shows a chronicle versus chessboard although the spoken choice is meal table versus chessboard. These are not additional source-claim failures.

## Story-body length

Using the current `video.json` and `estimateTimeline` at 250 spoken units per minute and 30 fps, the story core from `gs007` through `gs074` is **497.33 s (8:17.33)**, excluding the first six-line opening chapter and the final `gs076` CTA. Narration excluding the CTA but including that opening is **531.47 s (8:51.47)**; all spoken scenes including the CTA estimate **538.07 s (8:58.07)**. Branded intro/outro time is outside this estimate.

This is **an estimate, not current measured-audio proof**. `/workspace/.video-work/curio-s06/timeline.json` has 76 scenes while current `video.json` has 81: the timeline lacks `gs116`–`gs121` and retains deleted `gs070`. Only 54 of 81 current WAV takes match their current request keys and file hashes; 27 are missing or stale. The conservative core estimate clears 480 s by 17.33 s, so regenerate the narration timeline after script repair before asserting the measured eight-minute floor.

Only this verification report was added; the frozen script, `video.json`, claims, and media were not edited in this audit.
