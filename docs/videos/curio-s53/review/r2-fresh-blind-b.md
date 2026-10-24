# S53 R2 script-only fresh blind panel B

Source: `narrative --slug curio-s53 --json` from the official video CLI. This panel read the CLI narration and its 13 questions only; `script.md` was hashed without reading its prose. No brief, claims, `video.json`, task, policy, media, or other review was used.

- `script.md` SHA-256: `b8fba10ed2e143eb677aaf389bb2c4d088cf7ecda8e376386788afe198852df4`
- Narration SHA-256: `99108c12e584ecbfe606d3bb0a091d3fe9e63ab13ccb8e67ac99dc9c3809204d`
- Narration hash basis: UTF-8 bytes of the parsed JSON `narration` string, with no added newline (10,353 bytes).

**Score: 9 yes, 4 no.** Line references use the IDs in the narration output.

| Official question ID | Score | Evidence |
| --- | --- | --- |
| `scene_first` | Yes | `s53001–s53004`: June 1907 San Francisco plaza; the park commission sets a deadline as residents may acquire cottages under contract. |
| `no_spoiler` | Yes | `s53002`, `s53006–s53009`: the opening poses the rent, moving cost, survey, and land questions without their later answers. |
| `one_line` | No | `s53020` gives August 1906, `s53038–s53039` reaches March 1907, then `s53049` returns to the early rental plan and `s53065` returns explicitly to August 1906. |
| `no_toc` | Yes | `s53006–s53008`, `s53048`, `s53083` ask story questions; no spoken sentence announces the video's sections or a content list. |
| `chapters_link` | Yes | `s53009→s53010` returns from the preview to the disaster; `s53032→s53033`, `s53048→s53049`, `s53068→s53069`, `s53083→s53084`, and `s53100→s53101` carry the prior object or question forward. |
| `open_loops` | Yes | Examples at `s53015`, `s53023`, `s53030`, `s53048`, `s53061`, `s53074`, `s53090`, `s53104`, `s53116`, `s53129`; no 90-second stretch lacks one. |
| `payoffs` | No | `s53095–s53097` asks whether the survey can trace every cottage in the charity-repaired context. `s53103–s53109` gives only results for 1,137 moved-cottage addresses, with no answer for the repaired subset. |
| `no_recap` | No | The first 20 cottages are stated twice at `s53029–s53030`; the 23 rent-loss cases are stated twice at `s53130–s53131`. These adjacent repetitions are not delayed callbacks. |
| `chapters_are_events` | Yes | Chapter starts `s53001`, `s53010`, `s53033`, `s53049`, `s53069`, `s53084`, `s53101` correspond to titles about an event or a finding. |
| `outro_no_next` | Yes | `s53997–s53999` revisits the land cost and asks for a subscription, with no next-episode mention. |
| `opening_hooks` | Yes | After `s53001–s53002`, the opening adds four concrete pending questions at `s53006–s53009`. |
| `one_thread` | Yes | The cottages and residents' problem of leaving public land runs through `s53005`, `s53017`, `s53058`, `s53072`, `s53084`, `s53110`, and `s53997`. |
| `no_detour` | No | `s53012–s53013` diverts to an unnamed park report and missing-person notices; `s53014` resumes the shelters. The notice detail never bears on cottage construction, clearing, moving, or land cost. |
