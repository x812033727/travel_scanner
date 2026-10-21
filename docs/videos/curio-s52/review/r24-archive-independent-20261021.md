# S52 R24 independent archive prompt paper review — PASS

2026-10-21 UTC. **PASS for the single `s52014` written prompt correction.** It resolves the material location contradiction in the R23 HOLD: the archive now contains a sketch of a ship, not a full ship beside a dock worker. This is a paper decision on the prompt, not acceptance of a generated image or the completed storyboard.

## Source and scene

The fixed local Kippis text has SHA-256 `c723fd1d180efb3c55e783fc156018741cb9bc7b1402c3a490f50a65b31f9956`. At L598–624 it says that, on **3 April 1768**, Mr Stephens informed the Royal Society that a bark had been taken up for the expedition. The `s52014` narration, “四月三日，學會接到消息：船已經找到了。”, is a fair short rendering of that later account. It does not assert a same-day eyewitness scene. Kippis is a later narrative, not the dispatch itself.

The revised prompt has one anonymous clerk place an **unlettered sailing-ship sketch** beside a sealed dispatch on a lectern in a generic eighteenth-century archive room. The arrangement is spatially coherent. The sketch, dispatch, clerk, room, and afternoon light are illustrative staging, not documented original objects, a named person's likeness, or a recorded time of day. Nothing in the prompt presents them as such. I find no new material source or visual contradiction in this one changed scene; the native image will still need its own visual check.

## Exact change boundary

- Current `video.json` SHA-256: `cf3211e99155afd7cd71c715f6c6fd6055c43975a3a20e199b4582dda6f13677`, matching the R24 structured diff.
- The new prompt string occurs exactly once. Replacing it with the diff's old string restores R23 SHA-256 `86f9b98339a6e29b73446709ebb923f323e77277076a698c718952df725acd81` byte for byte. Recursive parsed-JSON comparison finds exactly **one** changed leaf, `scenes[13].data.prompt` (`s52014`), among 113 scenes. No narration, camera, or other scene changed.
- Reversing the eight recorded R23 light edits from that restored R23 file yields R22 SHA-256 `3e380aa29543a868dd643f588834e188d48c481da4c36e0a738a17968af9ad41`. `s52001` and `s52002` prompts and cameras stay identical through both reversals. The current prompts exactly match the R21 accepted `s52001` prompt and R22 accepted `s52002` prompt; cameras remain `pan right` and `drift left`, respectively. Their native KEEP decisions remain untouched.
- Local `lint --slug curio-s52 --json` exits `0` with **0 errors and 0 warnings**.

At review time `/workspace/.video-work/curio-s52/STOP` remained an empty regular file. The private ledger SHA-256 remained `f5df12777013c85e0e40f079f42864b3b5c66a8754453ed68c447bb63737a301`: **US$0.0675**, 5 images, 5 judge calls, and zero reservations, below the existing **US$4.46** episode ceiling. I made no paid call and no creative edit. Before treating the two prior images as reusable for a wider art batch, the tool still needs to verify their per-shot request and judge matches, and each new native image needs direct inspection.
