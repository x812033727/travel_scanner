# C08 short-v8 duration decision and measurement boundary

The owner selected a 4–5-minute rewrite of **C08 only** and approved the exact short-v8 narration and visual direction after seeing a paper body estimate of 273.97 seconds and paper body plus 5-second intro and 21-second outro estimate of 299.97 seconds. The text-only reading proxy is 236.64 seconds. These three numbers are planning calculations; there is no synthesized narration or assembled film, so none is an actual runtime.

The later `v7be06.say` candidate spells out the visible `MoMA` as `紐約現代藝術博物館` for Taiwan Mandarin speech while preserving the approved `text`. With that pronunciation candidate, the same estimator reads 993 spoken units, 238.32 seconds of text-only proxy, 275.63 seconds of body and **301.63 seconds with the same 26 seconds of bookends**. This is another paper estimate, about 1.63 seconds above the final-cut cap; it is neither a measured failure nor a waiver. Independent [text pronunciation review](pronunciation-review-20261024.md) passed; actual TTS/listening is a separate HOLD gate.

The short-duration predicate also binds the 36 ordered line IDs and approved visible texts to SHA-256 `31041c60a61f7612878e07417aaf7b7b914a70e04ad49ab395de6e8918c6d7d9`. A changed narration character loses the short exception and returns to the ordinary 480-second body floor; later media references can change without changing this text binding. The worker separately checks the entire approved source projection before backend start and on continuation.

The authorized measured policy for this exact `story-everyday-kikkoman-c08-short-v8` video is:

1. The current unwrapped narration timeline must contain at least 240 seconds of body at 30 fps. Intro and outro frames cannot fill a short body.
2. The checked final cut with its selected intro and outro must contain at most 300 seconds at 30 fps.
3. The timeline, speech hash, selected bookend frames and checked final frame count must match. Paper estimates and target metadata cannot substitute for them.
4. If the measured result misses either bound, hold for a precise edit and new owner review. Do not change voice speed, drop approved narration, or stretch bookends to force a pass.

The shared everyday series stays at its 10-minute planning target. The original 84-line C08 slug and all other episodes keep their existing duration rules. A green source projection or local lint is not a measured duration receipt, a media purchase authorization, or a release approval.
