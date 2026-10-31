# S49 R17 `moon016` prompt — independent paper review

2026-10-22 UTC. **PASS for one bounded native retake of `moon016` only.** This is a paper decision on the exact R17 files, not acceptance of a generated image, the full storyboard, audio, final film, or publication. I made no paid call or creative edit.

## Exact change boundary

I independently read the raw files and reversed the single R17 prompt string in each file. The new string occurred exactly once in `video.json` (as a JSON string) and once in `claims.md`. The reversed **whole-file raw bytes** yielded the recorded R16 SHA-256 values, not just an equivalent parsed object:

| File | Current R17 SHA-256 | SHA-256 after replacing only the one R17 string with R16's |
| --- | --- | --- |
| `video.json` | `5cb5211ff2cbe6eeb503859dc1c4cb078dbad9dfa77671bb816144ddf267a802` | `77905b41c1f15d5c799181c7dedd4c031c50dcbbbeba741943ca2e4236e59b8b` |
| `claims.md` | `33e07a082a41f42a720b5be972a8767ff2a5d7a31a27e06aa256883a544545ea` | `7aec3277c9a70120ff8638834c0efcd8502a1cf3984e40b3519ac2adf681c027` |

The changed JSON leaf is `scenes[15].data.prompt`, with ID `moon016`. The matching `claims.md` row changes only its visual description. All other 128 scenes, including the first fifteen individually accepted prompts and cameras, are byte-identical to R16 after that reversal. `script.md` remains SHA-256 `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`, and the `moon016` narration remains 「報導沒有只靠名氣；它又搬來一份學術刊物的增刊。」 The earlier 15 native KEEP decisions are therefore unaffected; the old `moon016` take remains human REJECT despite its machine PASS.

## Source and visual claim

The fixed 1859 Locke-attributed reprint at `/tmp/curio-moon-source/62779-0.txt` has SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`. Its title material (L152–165) says the New York *Sun* articles were “FROM THE SUPPLEMENT TO THE EDINBURGH JOURNAL OF SCIENCE”; its following body (L168 onward) speaks as if it were a journal addition. That is evidence of the **claim within the reprinted hoax**, not independent evidence that a physical 1835 Edinburgh supplement survives or was issued. The script's later `moon018`–`moon019` lines explicitly ask where that supplement can be found and state this research did not obtain an original. The R17 prompt does not name or print an actual supplement, identify a real buyer, or ask for a facsimile.

R17 asks for one fully grown, grey-haired, sideburned reader in an 1835 New York newspaper setting. His one action is lifting a **small, thin, unlettered booklet** from a bare counter; a separate **blank broadsheet lies flat**. Daylight comes from the shopfront. This directly targets the rejected native take's young-looking figure, modern adjustable lamp, and raised large broadsheet. The booklet, customer, and counter are conceptual staging of the *Sun*'s assertion. Keep any title, caption, or later composite from presenting the drawing as an extant 1835 Edinburgh artifact; the current claims row calls it an imagined report scene.

## Checks and release boundary

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s49 --json` exits 0 with **zero errors and zero warnings** (131 lines). The private `/workspace/.video-work/curio-s49/STOP` exists. I independently queried the ledger: **US$0.6615**, 49 image calls, 49 judge calls, zero music, and zero reservations. This is under the documented **US$5.30 cumulative image/judge/music ceiling**, leaving US$4.6385 before any further charge.

Release only **one `moon016` retake** with the usual bounded command and EXIT trap restoring `STOP`, then inspect its original native JPEG directly for adult age, 1835 era, booklet in hand, blank broadsheet flat, no modern fixture, and no misleading printed artifact. A machine PASS alone is insufficient; reject the image if any material contradiction remains. Do not start `moon017` or a bulk batch on this paper PASS. The remaining-art batching decision needs its own strategy receipt and the native `moon016` result.
