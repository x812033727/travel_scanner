# S38 PF018: blind human visual tiebreak

**Frozen verdict: HUMAN KEEP.** I recorded this verdict before opening `verify-95-r8ab-pf018-final-native-independent.md` or any earlier PF018 visual review. No media or manifest was changed.

## Evidence inspected before verdict

- `.agents/skills/curio-episode/SKILL.md`, “插圖怎麼驗收”: a judge-passed image is accepted unless it contradicts narration or source, or drifts from the cute cartoon style. The illustration need not reconstruct evidence exactly.
- `docs/videos/curio-s38/video.json`, PF018 narration: “他搭船沿河看，人們正把家當搬上平底貨船。” Prompt: a 1666 Thames cargo lighter, one older resident lowering a wooden household chest over a low rail onto the bare deck in overcast light.
- `/tmp/curio-s38-pepys-4200.txt`, lines 65816–65822, SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`: “Everybody endeavouring to remove their goods, and flinging into the river or bringing them into lighters that layoff”.
- Active `/workspace/.video-work/curio-s38/keyframes/manifest.json`, `shots.pf018`: selected `keyframes/pf018-1.jpg`, SHA-256 `837607f332ad31e267e308135daa7b7d1799d9dbc6ecc6f26c6959eeddf86aa0`, seed 1, judge **passed**, overall 9.29. The judge records a detail mismatch: two people holding an open box instead of the prompt's one person lowering a chest.
- I viewed the selected `/workspace/.video-work/curio-s38/keyframes/pf018-1.jpg` at its original 1280×720 resolution. Its file hash matches the manifest.

## Visual judgment

Two adult figures are actively gripping/handling a wooden chest or crate on the low, flat deck of a boat, with water behind them. This meaningfully illustrates **people bringing household goods into lighters**: the chest is a household good and the handling action is visible. It is already on the deck, so the image does not literally show the moment of crossing the side rail. That is a prompt detail mismatch, but it does not say the goods were never loaded or otherwise contradict Pepys's diary or the spoken line. The two figures also suit the narration's plural “people”.

The figures have adult faces and broadly period-looking simple clothing. I see no conspicuous modern object, extra limb, detached body part, or malformed hand that changes the action. The frame has no black bars. Flat shapes, expressive faces, muted colors, and drawn outlines fit the series' cute cartoon look; it does not look photographic, 3D, or painterly. The visible open top and lack of a shoreline reduce literal fidelity to the one-person prompt, but do not create a misleading factual claim under the series' acceptance rule.

**Disposition:** keep the active PF018 image. Do not rebind or redraw for this tiebreak.

## Post-freeze comparison with verify-95

After saving the verdict above, I read `verify-95-r8ab-pf018-final-native-independent.md`, which says **HUMAN REJECT**. We agree on the visible facts: two adults grip a chest already on the deck, with no shown shore-to-boat or over-rail movement; the boat, period setting, cartoon style, anatomy, and full frame are acceptable. We differ on whether the exact loading motion is mandatory. I apply the curio-episode rule that a judge-passed illustration needs rejection for a contradiction or style drift. Handling a household chest aboard a lighter suggests the goods-loading activity and does not contradict the diary or narration. The earlier review treats the missing crossing motion as grounds to reject. My blind **HUMAN KEEP** verdict remains unchanged.
