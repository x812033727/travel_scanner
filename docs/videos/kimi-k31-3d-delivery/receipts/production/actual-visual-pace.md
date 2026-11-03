# Actual Kimi visual pacing audit

Result: **no pacing change is required by the normal 15-second rule**. The pinned source has 110 visual states, with a longest hold of 14.2 seconds after the normal rounding (exactly 425 frames / 30 = 14.166667 seconds). There are zero holds over 15 seconds, zero invalid reveal capacities, and zero terminal-typing hold failures. No threshold or template behavior was changed.

Inputs were read only:

- Source: `/workspace/work/travel-scanner-kimi-k31/docs/videos/kimi-k31-3d-delivery/video.json`, 45933 bytes, SHA256 `9686969c66cfd9329c28e0f75d62c22830930b609479560d896e3e087829958b`.
- Actual body timeline: `/workspace/work/videos/kimi-k31-3d-delivery/timeline.json`, 46550 bytes, SHA256 `12287e1bb53102d5ab4f8cf3082aa4f08445007343955f569f4bc09d79387fba`.
- Body: 21922 frames at 30 fps = 730.733333 seconds. All 114 original measured line sample counts were used. Existing narration and line audio hashes were retained as timeline evidence; no audio file was independently rehashed or checked in this audit.
- Exact hashes of the lexicon and all normal functions used or inspected are in `inputs.json`.

## What the normal functions do

`tools/video/core/cadence.mjs:24` (`slideStates`) opens a state on the first line of a scene and every later line with a truthy `reveal`. A reveal on the first line changes the opening state; it does not add a second state at the same timestamp. Each hold ends at the next visual state, or the end of the body. Timing comes from the actual line start frames; seconds are rounded to one decimal.

`tools/video/qa/pace.mjs:17,42` sets `MAX_STATE_SECONDS = 15` and fails only states whose rounded seconds are greater than 15. The actual report from that unchanged function is:

> 110 slide states, the longest 14.2 s; none over 15 s

`tools/video/templates/templates.mjs:318,332` (`sceneProblems`, `visibility`) validates reveal capacity and determines the actual elements shown. Bullets can reveal one per item; a screenshot has capacity one only if it has a highlight. Code and big cards have capacity zero. Every multi-state scene in the current source changes a supported element between consecutive states; the proof records those element indices.

`tools/video/qa/pace.mjs:25` (`terminalHoldProblems`) and `tools/video/templates/terminal/terminal.mjs:98` (`terminalSeconds`) separately require human typing plus a 0.5-second reading margin to fit inside its existing state. Typing does not create extra states for the 15-second rule. `tools/video/assemble/plan.mjs:35` plays transitions inside the state. **This source has no terminal scenes**: both commands currently use the `code` template. There is no typing allowance to credit or remove.

## Longest holds and the suspected scene

| Scene | Actual state duration(s), seconds | Interpretation |
|---|---|---|
| `run-ring-command` | 14.166667 | Single code state; normal 14.2, passes |
| `run-filled-command` | 13.033333 | Single code state; normal 13.0, passes |
| `tolerance-is-purpose` | 12.3 / 5.5 / 6.866667 | Three valid bullet states |
| `handoff-three-files` | 12.2 / 7.133333 / 7.1 | Three valid bullet states |
| `download-moment` | 6.866667 / 9.7 | Image first, then its existing highlight |
| `one-delivery` | 4.933333 / 5.166667 / 4.7 / 4.366667 | Four valid bullet states, not one static 19.166667-second hold |

For `one-delivery`, each of its four lines has `reveal: 1`. These are **increments**, so its timeline reveals are cumulative `1, 2, 3, 4`; the four bullet items are shown successively. Frame intervals are `1094–1242`, `1242–1397`, `1397–1538`, `1538–1669`. Normal `visibility` confirms shown indices `[0]`, `[0,1]`, `[0,1,2]`, `[0,1,2,3]`.

There is no supported benefit from adding reveals here: the current four reveals already match its capacity of four. Adding reveals to either command card or any big card would exceed capacity zero. No generic intra-line cut schedule exists in the normal timeline builder. Such edits would not be valid fixes and are not proposed.

## Exact proposal and proof

The proposed RFC 6902 JSON patch is the empty array in `proposed-visual-only.patch.json`:

```json
[]
```

No source field, audio/text/say/ID/order/voice/chapter/claim/asset, visual field, timing or cut is changed. This is the minimal concrete proposal because the current state calculation already passes.

`audit.mjs` calls the normal pure `buildTimeline` with the exact 114 `audio_samples` values from the actual timeline. It adds back the existing line hash references and normal `speechHash`, then asserts deep equality to the actual timeline. The resulting `candidate.timeline.json` is also **byte-identical** to the actual timeline: 46550 bytes, SHA256 `12287e1bb53102d5ab4f8cf3082aa4f08445007343955f569f4bc09d79387fba`. Both body totals remain 21922 frames; speech hash remains `a75a68a86268df4e`. The candidate's normal 15-second result is identical.

`current-states.json` contains all 110 normal states, template capacities and native visibility calculations. `proof.json` records the assertions; `audio-sample-identity.json` lists the 114 sample counts and inherited audio hashes; `freeze.json` binds every generated proof file. A second agent independently read the normal state, capacity and typing functions and confirmed this interpretation.

Only this new scratch directory was written. No native CLI, rendering, ASR, auth, paid operation, Git, production file, hold or running process was used or changed. In particular, PID 304867 was not inspected, interrupted or otherwise touched. Existing render/audio/check failures and artifacts remain intact. This calculation is a pacing audit, not a rendered-frame review, audio pass, QA approval or replacement for the producer's normal checks after ASR finishes.
