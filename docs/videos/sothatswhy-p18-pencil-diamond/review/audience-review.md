# Independent Audience Review — `sothatswhy-p18-pencil-diamond` (Round 2)

- **Episode:** `sothatswhy-p18-pencil-diamond` — 〈鉛筆芯和鑽石都是碳，為何鑽石怕一敲、鉛筆還能通電？｜原來如此事務所〉
- **Runtime:** `08:23` total (`503.44s`: `08:02.4` body / `14,472` frames + `00:21.0` endscreen / `630` frames at 30 fps)
- **Review Stage:** Round-2 Re-Review (post-fix re-assembly after `audio/p009.wav` re-voicing)
- **Reviewer Role:** Independent general-audience YouTube viewer (direct audio check of `audio/p009.wav` + spot-checked neighboring WAVs, visual inspection of `thumbnail.jpg` & `/tmp/p18-assembled-16up.jpg`, and full audit of `video.json`, `captions/zh-TW.srt`, `timeline.json`, and `checks.json`)
- **Overall Score:** **9.1 / 10**
- **Verdict:** **PASS**

---

## Artifacts Inspected

1. `/home/antigravity/mokaair-work/videos/sothatswhy-p18-pencil-diamond/audio/p009.wav` (`10.310s`, SHA-256 `60d8fe87...`, approved `2026-11-23T05:02:43Z`) — direct ear/audio verification of re-voiced line `p009` (`這猜想先記好`), plus spot checks on `p001.wav`, `p002.wav`, `p008.wav`, `p010.wav`, `p026.wav`, and `p051.wav`.
2. `/tmp/p18-assembled-16up.jpg` — 16 evenly spaced frames from re-assembled `final.mp4` (`503.437s` = `08:23`, `checks.json` `"ok": true`, `"problems": []`).
3. `/home/antigravity/mokaair-work/videos/sothatswhy-p18-pencil-diamond/thumbnail.jpg` — rendered `heimao-left` thumbnail (`最硬鑽石竟怕鐵鎚一敲？` / `同是碳原子，鉛筆芯還能點亮小燈`).
4. `/home/antigravity/x812033727/travel_scanner/docs/videos/sothatswhy-p18-pencil-diamond/video.json` — 50 scenes / 50 lines (`25` `nobody: true` object/mechanism shots = `50.0%`, `25` character shots: `7` 所長 / `18` 小問), 10 narrative loops, 9 verified sources.
5. `/home/antigravity/mokaair-work/videos/sothatswhy-p18-pencil-diamond/captions/zh-TW.srt` — 100 cues spanning `00:00:00,000 --> 00:08:01,295` (`481.30s`, `2,068` content characters, `4.30 chars/s` over SRT span / `4.29 chars/s` over body; max inter-cue gap `281ms`).

---

## Dimension Scores

| Dimension | Score | Viewer Notes |
| --- | :---: | --- |
| **Thumbnail** | **9.0 / 10** | Full-bleed `heimao-left` layout with high curiosity and instant three-clue visual storytelling: shocked 2.5-head chibi 小問 holding a yellow pencil lower-left, giant dazzling diamond splitting under an iron hammer strike upper-right, and a warm glowing miniature bulb at the end of a dark graphite smudge trail lower-right. Subject-named yellow/white black-stroked copy (`最硬鑽石竟怕鐵鎚一敲？` / `同是碳原子，鉛筆芯還能點亮小燈`) reads sharply even at mobile feed scale. |
| **Opening Hook** | **9.2 / 10** | Immediate everyday entry (`00:00–00:09`, hand smudged from pencil drawing) paired with a crisp double paradox (same carbon as diamond, yet diamond fears a hammer blow), escalated by `00:21` with Mohs 1–2 vs 10 and the pencil-line light bulb, followed by a tight non-spoiler promise (`00:21–00:29`) that keeps viewers locked in. |
| **Visual Craft** | **9.1 / 10** | Cohesive warm theatrical-light rich-gouache look across all 16 sampled frames; consistent 2.5-head chibi model fidelity, generous headroom, and clean five-fingered hands for 小問 and 所長. Balanced `50.0%` (`25/50`) wordless `nobody: true` mechanism/object shots make every physics beat tangible (wooden 4-peg sphere, wide-gap layered honeycombs, Taiwanese park jungle gym, glowing cyan electron highway, unlit diamond circuit, soft-vs-hard pencil strokes, and the full-bench recap prop shot before a clean `Mokaair` endscreen). Zero garbled in-frame text. |
| **Pacing & Clarity** | **9.0 / 10** | One sticky central metaphor ("同一盒木球與小木棍") cleanly unlocks every chapter—graphite layer slip, 1.5× density gap, scratch hardness vs cleavage toughness (glass-cup analogy), free fourth-hand electron highway, rare blue-diamond exception, in-plane vs across-plane resistance, graphite/clay ratio, and scientific model epistemology. All 10 open loops pay off, safety (`只接安全九伏特乾電池、別碰插座`) is stated naturally, and the `08:02` body flows smoothly with zero dead-air freezes (max SRT cue gap `281ms`). |
| **Subtitles & Audio Hygiene** | **9.0 / 10** | Round-1's sole `must_fix` defect (`audio/p009.wav`) is completely resolved: `這猜想先記好，等一下量給你看` is crisp, natural, and completely free of the previous `先住著` slur. Clean broadcast loudness (`-14.1 LUFS`, true peak `-1.9 dBTP`, music bed `-33.5 LUFS`), natural Taipei Mandarin cadence from `Sulafat` (所長) and `Leda` (小問), and 100 synchronized SRT cues with zero timestamp errors. |
| **Overall** | **9.1 / 10** | **PASS — Ready for Google Drive backup and `review-push --gate final`.** |

---

## Round-1 → Round-2 Verification

| # | Round-1 Item | Severity | Round-2 Verification Result | Evidence |
| :---: | --- | :---: | :---: | --- |
| **1** | `audio/p009.wav` slurring `先記著` as `先住著` | `must_fix` | **FIXED & VERIFIED** | Updated `video.json` line `p009` with `"say": "這猜想，先記好！等一下量給你看！……"` (`say_for: "e4051137200f"`), re-synthesized `audio/p009.wav` (`10.310s`, SHA-256 `60d8fe87...`, approved `2026-11-23T05:02:43Z`), and re-assembled `final.mp4` (`503.437s` = `08:23` total / `08:02.4` body). Direct audio inspection confirms `這猜想先記好，等一下量給你看` is crisp, natural, and completely slur-free; `timeline.json` binds `p009` cleanly to frames `1967–2281` (`01:05.567–01:16.033`, SRT cues `#15–#16`). |
| **2** | Post-reassembly regression check (`final.mp4`, `checks.json`, `thumbnail.jpg`, `zh-TW.srt`) | Verification | **VERIFIED CLEAN** | `checks.json` passes with `"ok": true` and `"problems": []` (`-14.1 LUFS`, `-1.9 dBTP`, keyframe PSNR `40.88–45.02 dB`). All 16 sampled frames in `/tmp/p18-assembled-16up.jpg`, `thumbnail.jpg`, and all 100 cues in `captions/zh-TW.srt` show zero regressions or newly introduced defects. |

---

## `must_fix`

*(None — empty. All blocking items are resolved and verified. Ready for Google Drive backup and `review-push --gate final`.)*

---

## `nice_to_have`

1. **Exact `text` vs `say` parity on `p009` (non-blocking):** `audio/p009.wav` cleanly speaks `這猜想先記好`, while `video.json` `text` and `captions/zh-TW.srt` cue `#15` still display `這猜想先記著`. Meaning is identical and non-distracting in live playback; aligning `text` to `say` on future episodes when substituting a Chinese character keeps CC 100% verbatim.
2. **SRT em-dash (`——`) cue-boundary splits (non-blocking):** Six paired cues split `——` across consecutive captions (`#25/#26`, `#41/#42`, `#59/#60`, `#67/#68`, `#75/#76`, `#77/#78`), plus a few mid-word line wraps (`這兩 / 個`, `「 / 一般的鑽石」`). Totally legible on YouTube CC; keeping `——` intact on a single cue would polish readability further in future runs.
3. **Thumbnail top-right hammer/headline overlap (non-blocking):** In `thumbnail.jpg`, the trailing yellow `一敲？` overlaps the top of the hammer head and the white subline's final `燈` kisses the diamond's upper-left border. The heavy black outline preserves strong legibility at mobile size, so no remake is needed.
4. **Second-half pacing headroom (non-blocking):** Overall body pacing sits at `4.30 chars/s` (over SRT span) with 13 `pause_after_ms: 500` beats in `p038–p050` yielding gentle `250–281ms` SRT gaps. It feels natural and unhurried with zero dead air, though trimming a few `500ms` beats on future episodes would keep average pace closer to `≥4.4 chars/s`.
