# Audience Review — `sothatswhy-p29-https` (Round 2 Re-Review)

- **Episode**: 網址小鎖頭竟然會騙人？幾乎所有釣魚站都有 HTTPS｜原來如此事務所 (`sothatswhy-p29-https`)
- **Runtime**: `08:27` total (`08:06.5` body / `14,595` frames + `00:21` endscreen / `630` frames at 30 fps)
- **Reviewer Role**: Independent general-audience YouTube viewer (direct visual inspection + ear verification of rendered WAVs, SRT timing, and `video.json`)
- **Overall Score**: **9.0 / 10**
- **Verdict**: **PASS**

---

## Dimension Scores

| Dimension | Score | Notes |
| --- | :---: | --- |
| **Thumbnail** | **9.2 / 10** | Full-bleed `heimao-left` layout with immediate visual storytelling: alarmed chibi 小問 on the lower-left, giant cracked emerald padlock + sly domino-masked bandit + wax-sealed envelopes on the right. Subject-named yellow headline (`HTTPS小鎖頭會騙人？`) and shortened white subline (`多一個S到底防了誰？`) read effortlessly at mobile scale, with clean blue-sky separation between the subline and the broken shackle/sparks. |
| **Opening Hook** | **9.1 / 10** | Hooks within the first 6 seconds on a relatable contradiction ("Chrome 竟然宣布把小鎖頭撤掉"), escalates by `00:20` with the 11% comprehension stat and the "almost all phishing sites use HTTPS" twist, and sets up a clear promise (`h004`–`h005`) without spoiling the explanation. |
| **Visual Craft** | **8.9 / 10** | Consistent theatrical-light rich-gouache look across all 16 sampled frames, clean 2.5-head chibi model fidelity for 所長 and 小問, and `40/63` (`63.5%`) wordless `nobody: true` mechanism/object shots that make abstract TLS mechanics (CA hierarchy, CT glass archive, Diffie-Hellman paint mixing, cotton-padded envelopes, ECH nested envelope) intuitive with zero text clutter. |
| **Pacing & Clarity** | **8.9 / 10** | Brisk `5.62 chars/s` active speech (`4.77 chars/s` across the full `08:06.5` body), organic Q&A hooks every 30–45 s, and all 11 narrative loops cleanly paid off—culminating in the actionable "free gems" URL typo catch (`h020 → h055 → h058 → h060`). All Round-1 `1.7s` dead-air freezes are eliminated, and climax turns snap cleanly at `~0.56s`. |
| **Subtitles & Audio Hygiene** | **8.8 / 10** | All Round-1 factual/sync blockers are verified resolved by ear on the actual WAV files (`h051` clearly says `2026年3月`, `h060` clearly says `收件人`, `h034` matches `真私章` verbatim, `h035`/`h037`/`h055` match subtitles verbatim). Clean broadcast mix (`-14 LUFS`, `-2 dBTP`, `-33.3 LUFS` music bed) with natural Taipei Mandarin delivery from Sulafat + Leda. |

---

## Round-1 → Round-2 Fix Verification

| # | Round-1 Finding | Round-2 Direct Verification | Status |
| :---: | --- | --- | :---: |
| **1** | **`h051` spoken year (`2020` vs `2026`)** | Listened directly to `audio/h051.wav`: clearly and unmistakably speaks **「二零二六年三月發布的網際網路新加密規格……」** (`2026年3月`, matching IETF RFC 9849). Confirmed that `review/check.json`'s `"二零二零年三月"` was strictly an ASR misrecognition artifact from the earlier pass. | **PASS** |
| **2a** | **`h034` audio-vs-subtitle sync (`真私章`)** | Listened directly to re-synthesized `audio/h034.wav`: speaks **「解不開！真私章只驗身分，這回調出來鎖信的臨時鑰匙用完就銷毀，下次重調，這叫前向保密。」** Matches `video.json` and `zh-TW.srt` (cues 67–68) verbatim. | **PASS** |
| **2b** | **`h035`, `h037`, `h055` audio-vs-subtitle sync** | Listened directly to `h035.wav`, `h037.wav`, and `h055.wav`: `h035` matches cues 69–70 verbatim; `h037` speaks 「影印的人沒有那個真正的印章……」(matching cues 73–74 verbatim); `h055` matches cues 109–110 verbatim (with a natural conversational breath/「欸」 before the question). | **PASS** |
| **2c** | **`h060` spoken wording (`收件人`)** | Listened directly to `audio/h060.wav`: clearly and unmistakably speaks **「收件人是好是壞得靠自己認」** (matching cue 119 verbatim; `check.json`'s `"收信人"` was an ASR artifact). | **PASS** |
| **3** | **Pacing / consecutive `~1.7s` dead-air pauses in `h048`–`h059`** | Audited every inter-turn gap in `captions/zh-TW.srt` across `h040`–`h062`: zero `1400ms` (`~1.7s`) freezes remain anywhere in the video (max SRT gap across the entire second half is `1.18s` on chapter/beat transitions; `pause_after_ms` capped at `600–850ms`). All three rapid climax turns are snappy: `h050→h051` = **558 ms**, `h055→h056` = **571 ms**, `h058→h059` = **561 ms**. | **PASS** |
| **Bonus** | **`thumbnail.jpg` subline overlap** | Inspected rendered `thumbnail.jpg`: shortened subline **「多一個S到底防了誰？」** sits entirely inside the clean upper-left sky/cloud zone with wide open blue-sky clearance to the left of the broken padlock shackle, red sparks, and masked bandit. Zero overlap. | **PASS** |

---

## `must_fix`

*(None — empty. Ready for Google Drive backup and `review-push --gate final`.)*

## `nice_to_have`

1. **TTS polyphone polish (`h034.wav`)**: In `h034`（「這回調出來……下次重調」）, Gemini TTS reads the polyphone `調` closer to 4th-tone `diào` rather than 2nd-tone `tiáo` (as in `調顏料` / `h032`'s `say: "調和顏料"`). Completely intelligible in context and verbatim to the caption, so no remake needed; worth noting for future TTS `say` prompts whenever bare `調` means "mix".
2. **Exact `text` vs `say` parity on `h038` & `h043`**: Two lines intentionally expand shorthand wording in `say` for smoother speech (`h038` caption `全對上才寄信` vs spoken `全對上才正式寄出信件`; `h043` caption `由伺服器自限` vs spoken `由伺服器自己限制`). Meaning is identical and non-distracting; aligning `text` to `say` on future episodes keeps captions 100% word-for-word.
3. **SRT line-wrap splits**: Automated caption wrapping splits a few compound words across cues/lines (e.g., cues 3–4 `百 / 分之十一`, cue 41 `連 / 結`, cue 49 `Safari 要 / 求`). Standard for auto-timed SRT and perfectly readable at speed, though semantic wrap hints would make CC even cleaner.
4. **Shot scale consistency (`kid-photocopy-cert-trap`, frame 9 of 16-up)**: Chibi 小問 appears playfully miniature standing atop the wooden desk next to an oversized magnifying glass rather than seated behind the desk as in neighboring office shots—charming and defect-free, just a minor scale quirk to keep consistent in future scripts.
