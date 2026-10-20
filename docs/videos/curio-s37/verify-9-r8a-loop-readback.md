# Curio S37 R8a focused loop readback

**Verdict: PASS.** The two declared payoff pointers now reach the first supported answers. All 22 loop mappings are defensible. The R8 source/visual audit remains applicable because only those two metadata values changed.

## Exact change proof

| File | Current SHA-256 |
|---|---|
| `script.md` | `a838e16572f4a40c3d79c5874087900a8e8b808fceb35db9a03642bcc3412a62` |
| `video.json` | `8d4b1a2c4cc85dad3e5f500eff643c4a7d7ecc70998443097e3a62c58f72a51c` |
| `claims.md` | `ce7491625af59f27549fe4621e18917082946602474a99c1ea72e4f9f27d997a` |

I took the current raw `video.json` bytes, reversed exactly one occurrence of each new payoff (`pl053 → pl025` back to `pl054`, and `pl030 → pl072` back to `pl071`), and hashed the reconstructed bytes. The result is the frozen R8 `video.json` SHA-256, `a83c3d0aa14ea6bb4bf09392f86d95c31101b9175e38afb50961aa692a45765b`. Thus these two `loops[].payoff` strings are the entire byte-level JSON diff; all scene data and prompts are unchanged.

| Loop | Readback |
|---|---|
| `pl053 → pl025` | `pl053` asks whether the narrow courtyard remains safe at dawn (script line 133); `pl025` answers that nearby buildings shake and the courtyard is too narrow to remain safely (line 143; pinned Pliny L3652–3655). |
| `pl030 → pl072` | `pl030` asks whether they can see their footing when the dark mist arrives (script line 237); `pl072` says daylight disappears as soon as they sit down (line 245; pinned Pliny L3689–3693). `pl031` then makes the blackness explicit by the shut-room, lights-out comparison. |

The other 20 loop mappings retain the R8 audit's defensible setup/payoff reading. All 22 setup IDs occur before their payoff IDs. The current file has 89 scenes, 91 spoken lines and 88 nonempty still prompts. `claims.md` IDs/text and script spoken text match video line IDs/text in order, with no mismatch. The unchanged script and claims hashes, plus the exact JSON reconstruction, preserve the original 91/91 claim and 88/88 prompt review and the 13/13 blind narrative seal.

## Lint

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s37` exited 0: **0 errors, 0 warnings**; estimated 9.3 minutes and 91 lines. No repository files or Git index entries were edited by this reviewer, and no media was generated.
