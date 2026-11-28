# Independent Audience Review — `sothatswhy-p21-car-sickness` (Round 2)

- **Episode:** `sothatswhy-p21-car-sickness` — 〈坐車看書就暈到想吐？其實會暈反而代表內耳超健康｜原來如此事務所〉
- **Review Stage:** Round-2 Re-Review (post-fix re-assembly `v2`, `08:36` total / `08:15` body)
- **Reviewer Role:** Independent general-audience YouTube viewer
- **Overall Score:** **9.1 / 10**
- **Verdict:** **PASS**

---

## Artifacts Inspected

1. `/tmp/p21-assembled-16up.jpg` — 16 evenly spaced frames from re-assembled v2 `final.mp4` (`516.47s` = `08:36` total / `08:14.3` body + end screen)
2. `/home/antigravity/mokaair-work/videos/sothatswhy-p21-car-sickness/thumbnail.jpg` — re-rendered `heimao-left` thumbnail with shortened subline `司機沒事，蒙眼照樣暈！`
3. `/home/antigravity/x812033727/travel_scanner/docs/videos/sothatswhy-p21-car-sickness/video.json` — 55 scenes / 55 lines (`32` `nobody: true` object/diorama shots = `58.2%`, `23` character shots), 9 open loops, 15 verified sources
4. `/home/antigravity/mokaair-work/videos/sothatswhy-p21-car-sickness/captions/zh-TW.srt` — 110 cues spanning `00:00:00,000 --> 00:08:14,310` (`494.31s`, `2,227` content characters, `4.51 chars/s` average)

---

## Dimension Scores

| Dimension | Score | Viewer Notes |
| --- | :---: | --- |
| **Hook & Opening Retention (0:00–0:40)** | **9.2 / 10** | Instant relatable trigger (reading in backseat vs. unaffected driver), immediate counterintuitive twist ("會暈反而代表內耳很健康"), 10,000× vulnerability open loop, plus blindfold & sofa racing-game paradoxes before a crisp non-spoiler promise. |
| **Story Structure, Clarity & Scientific Honesty** | **9.3 / 10** | The recurring "cup of water in the ear" metaphor ties every chapter together cleanly (vestibular anatomy → predictive internal model → 3,256-passenger 3× view gap → driver control & auditory sled caveat → VIMS/vection & live-video fail → 10,000× spread & nausea hypotheses). All 9 open loops pay off, and scientific limits are stated candidly without overclaiming. |
| **Pacing, Audio & Caption Flow (v2)** | **9.1 / 10** | Smooth, brisk dialogue rhythm across the entire `08:15` body (`4.51 chars/s` overall; uniform `Sulafat tempo 1.02` / `Leda tempo 1.06`; `0ms` dead-air gaps across all 110 cue boundaries). Round-1 flagged WAVs (`c011`, `c012`, `c031`, `c042`) were already directly verified clean by ear. |
| **Visual Quality, Consistency & Metaphor Design** | **9.1 / 10** | Cohesive theatrical-light rich-gouache style across all 16 sampled frames, strong visual variety (`58.2%` `nobody: true` object/diorama shots like glass inner-ear canals, sloshing cup vs. still book, tour-bus aisle, shoe age-curve, moving-room figurine), consistent 2.5-head chibi `所長` & `小問` with generous headroom and clean hands, zero garbled text. |
| **Thumbnail CTR & Mobile Legibility (v2)** | **9.0 / 10** | Punchy yellow/white black-stroked curiosity hook (`暈車竟是內耳太健康？` / `司機沒事，蒙眼照樣暈！`) over bright sky, expressive dizzy `小問` lower-left, dramatic splashing water glass + steering wheel right. Clean separation and instant readability even at mobile feed scale. |
| **Payoff, Resonance & Engagement CTA** | **8.9 / 10** | Warm reframing ("balance system trained for millions of years of walking, surprised by modern vehicles"), satisfying bookend callback to the opening question, and a concrete 3-option comment prompt (phone in car / boat / FPS games) that invites easy viewer replies. |
| **Overall** | **9.1 / 10** | **PASS — Ready for Google Drive backup and `review-push --gate final`.** |

---

## Round-1 → Round-2 Verification

| Round-1 Item | Severity | Round-2 Verification Result | Evidence |
| --- | :---: | :---: | --- |
| 20 consecutive `750–1000ms` dead-air pauses (`pause_after_ms`) in `c033–c051` | `must_fix` | **FIXED & VERIFIED** | Zero `pause_after_ms` entries remain anywhere in `video.json` (global `pauses: {"line_ms": 0, "scene_ms": 200}`). In `captions/zh-TW.srt`, every single boundary across all 110 cues (`00:00:00,000`–`00:08:14,310`) has `0ms` dead-air gap; `c033–c051` (cues `#69–#108`, `05:03.47`–`08:08.20`) now runs seamlessly at `4.04–5.30 chars/s` under uniform `tempo 1.02` (`chief`) / `1.06` (`kid`). |
| Long thumbnail subline crowding right-half tilted glass rim | `nice_to_have #1` | **FIXED & VERIFIED** | Re-rendered `thumbnail.jpg` uses shortened subline `司機沒事，蒙眼照樣暈！`, sitting **100% inside the clean upper-left blue sky** with clear sky margin to the left of the tilted glass rim (zero overlap on the glass rim and ample headroom above `小問`). |
| Round-1 flagged WAVs (`c011`, `c012`, `c031`, `c042`) | Info / Prior Check | **VERIFIED CLEAN** | Already directly verified clean by ear prior to Round-2 re-review; no remaining audio defects noted. |

---

## `must_fix`

*(None — empty. All blocking items are resolved and verified.)*

---

## `nice_to_have`

1. **SRT em-dash (`——`) cue wrapping (non-blocking, future CC polish):** In `captions/zh-TW.srt`, several paired cues split `——` across two consecutive captions (e.g., cues `#17/#18`, `#25/#26`, `#29/#30`, `#35/#36`, `#45/#46`, `#59/#60`, `#95/#96`, `#97/#98`, `#101/#102` end one cue with `—` and start the next with `—`). Totally legible on YouTube CC, though keeping `——` intact on a single cue would read slightly cleaner in future episodes.
2. **Headline top-right glass-rim kiss (non-blocking):** In `thumbnail.jpg`, the shortened subline is now 100% clear of the glass, while the large yellow headline's trailing `？` lightly crosses the top edge of the tilted glass rim; contrast remains strong due to the thick black stroke, so no remake is needed.
