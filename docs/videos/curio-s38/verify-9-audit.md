# Curio S38 R8a focused still-prompt audit

2026-10-20. **PASS for the three prompt edits before paid art.** No episode files were edited and no media was made in this audit.

## Exact version and change scope

| File | SHA-256 | Result |
| --- | --- | --- |
| `docs/videos/curio-s38/script.md` | `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951` | Identical to R8 and to HEAD |
| `docs/videos/curio-s38/claims.md` | `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42` | Identical to R8 and to HEAD |
| `docs/videos/curio-s38/video.json` | `65ba99a5f6e28aef6dffbbe63828f080025a0c20e61120a75304d5aaf0635426` | Matches expected R8a hash; R8 baseline was `3dbe6dd23eedef3ff999801f6e548ab69ea480ee8a2b00095e78e1d48ec837b9` |

A recursive parsed-JSON comparison against the R8 baseline yielded **exactly three leaf changes**: `/scenes/39/data/prompt` (`pf040`), `/scenes/75/data/prompt` (`pf076`), and `/scenes/97/data/prompt` (`pf098`). All other JSON fields, including narration, camera, timing order, and scene IDs, are identical.

Pinned source remains GITenberg Pepys diary commit `68fcf49f70ee793b989a6fd0464264d55beb4451`, `4200.txt` SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`. R8 full check is documented in `verify-8-blind.md` and `verify-8-source.md`; this report checks the three changed visuals directly against the pinned diary.

| Still | Current prompt assessment |
| --- | --- |
| `pf040` | **Pass.** Script/claim say Pepys saw fire farther above and below the bridge from the boat (script line 171; claims line 46). Diary L65897–65901 says he took a boat below and above the bridge and saw the fire extend in both directions. A riverboat view, stone bridge, spreading fire and smoky afternoon light fit the dated journey. The upstream/downstream wording fixes the former ambiguous “both sides” geography. |
| `pf076` | **Pass.** Script/claim say he wrote Coventry asking permission to pull down houses (script line 319; claims line 82). Diary L66004–66012 explicitly says he proposed writing and “I wrote to Sir W. Coventry”; Pen went that night. A diarist writing on an unmarked sheet by lamplight is direct, period-sensible illustration. Removing the prior messenger also removes an unrecorded delivery action. |
| `pf098` | **Pass.** Script/claim say Moorfields was full of displaced people guarding goods (script line 409; claims line 104). Diary L66102–66109 says he walked there, found it “full of people,” and that everyone kept their goods together. One prominent person with many families and goods in the open Moorfields background conveys the documented crowd without a specific invented incident. Grey daylight fits the September 5 walk. |

`node tools/video/cli.mjs lint --slug curio-s38` exited 0 with **0 errors and 0 warnings** on the R8a video hash. The source and period checks found no material contradiction in these three edited prompts; generated pictures still require their own image review.
