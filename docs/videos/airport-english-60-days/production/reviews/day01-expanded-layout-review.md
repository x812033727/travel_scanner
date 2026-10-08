# Day01 expanded dialogue: static layout review

Reviewer: `/root/airport_measured_pacing` (AI), 2026-10-08T16:33:21.805Z.

Decision: **PASS for the16newstaticstates**. This is a static visual preflight, not full video QA, audio approval, or proof of finished CC/media.

Source: `/workspace/airport-pr/docs/videos/airport-english-60-days/production/day01/video.json`. The full111scene official render plan supplied chapter/header context; only the16affected A07/A08/B09/B10 states were captured. Canonical sources, staging, production media and approvals were not changed.

- Source file SHA256: `8530ca55d4124820db6fb90bc20753df9b033f953b1095b7beb2702d17d7ff7e`.
- Exact source visual hash: **`ce49ed808e318b0d`**.
- Official theme hash: `17fcf59dd1a1f4ac`.
- Source hash rechecked unchanged at report time: `True`.
- Renderer: official `renderPlan` and `openRenderer`, 1920×1080 Chromium captures, bundled fonts, all external requests refused by renderer.
- Independent read-only DOM measurements after each official capture: English minimum **90px**, maximum **3rows**, zero official overflow/font/load errors.
- CC safe band begins at **y=950.4px** (bottom12%); lowest visible quote/source/phase text ends at **y=831px**, leaving at least **119.4px** before that band. Template content boundary is948px (132px bottom reserve).
- No translated text is burned into these frames. Actual four-language CC cues still require final media testing.
-16PNG stills total8,160,844bytes; contact sheet and script are confined to the separate external render directory.

The16state contact sheet and fullresolution A08 card were visually inspected. Quotes remain readable with complete words, appropriate line breaks and no clipping. Traveler/Staff labels, phase instructions and chapter headers remain clear.

| Semantic occurrence | Scene | Actual English font px | Actual rows | Lowest content text y | Static result |
| --- | --- | ---: | ---: | ---: | --- |
| first-A07 | `s-ecef54ee` | 90 | 2 | 759.0 | PASS |
| first-A08 | `s-eba4922e` | 96 | 3 | 823.8 | PASS |
| connect-A07 | `s-56dd7db1` | 90 | 2 | 759.0 | PASS |
| connect-A08 | `s-6398fcc4` | 96 | 3 | 823.8 | PASS |
| practice-A07 | `s-aae63e64` | 90 | 2 | 759.0 | PASS |
| practice-A08 | `s-86c077fd` | 96 | 3 | 823.8 | PASS |
| first-B09 | `s-8dbd4386` | 100 | 3 | 831.0 | PASS |
| first-B10 | `s-ec68bac9` | 100 | 3 | 831.0 | PASS |
| connect-B09 | `s-c8cbe6bb` | 100 | 3 | 831.0 | PASS |
| connect-B10 | `s-cb36e3c2` | 100 | 3 | 831.0 | PASS |
| practice-B09 | `s-fcf5abb3` | 100 | 3 | 831.0 | PASS |
| practice-B10 | `s-53f73739` | 100 | 3 | 831.0 | PASS |
| review-A07 | `s-9b54dc57` | 90 | 2 | 759.0 | PASS |
| review-A08 | `s-a2dc6607` | 96 | 3 | 823.8 | PASS |
| review-B09 | `s-1d12274f` | 100 | 3 | 831.0 | PASS |
| review-B10 | `s-3a072069` | 100 | 3 | 831.0 | PASS |

Artifacts:

- [Contact sheet](day01-expanded-render/contact-sheet.png)
- [Representative A08](day01-expanded-render/s-eba4922e.png)
- [Machine-readable report](day01-expanded-layout-review.json)
- Reproduction script: `day01-expanded-render/check-layout.mjs`.

Scope limits: these are settled static frames. Entrance animations, real caption timings/overlays, spoken-language correctness, soundtrack selection, final encoded video, and the formal11itemQA require their respective later checks. No approval record was created.
