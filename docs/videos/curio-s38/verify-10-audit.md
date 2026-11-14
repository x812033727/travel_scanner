# S38 R8b prompt audit before additional image spending

**PASS for the frozen R8b2 prompt file only:** `/workspace/travel_scanner/docs/videos/curio-s38/video.json` SHA-256 `ca2bb866b0fb452607f20764f652c715f1447bc226f9df0a28bfc3b1d73cb1fc`. The next small image pilot still requires **human visual inspection** before the long still queue resumes. The two rejected R8a pilot JPEGs remain rejected.

## File and structure checks

| File / check | Result |
| --- | --- |
| R8a baseline `41f56c5b:docs/videos/curio-s38/video.json` SHA-256 | `65ba99a5f6e28aef6dffbbe63828f080025a0c20e61120a75304d5aaf0635426` |
| R8b2 `video.json` SHA-256 | `ca2bb866b0fb452607f20764f652c715f1447bc226f9df0a28bfc3b1d73cb1fc` |
| `script.md` SHA-256, unchanged | `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951` |
| `claims.md` SHA-256, unchanged | `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42` |
| Parsed JSON diff, R8a to R8b2 | Exactly **111 leaf changes**, each `scenes[*].data.prompt`. All 112 scene IDs, 112 narration lines, chapters, camera/visual fields, look, source, voice, music, and other JSON values are unchanged. |
| Curio look / people names | `look` remains exactly `{ "preset": "cute-mystery" }`; no direct historical personal names in any of the 111 image prompts. |
| Lint | `node tools/video/cli.mjs lint --slug curio-s38` exits 0 with **0 errors, 0 warnings**; 10.0 minute estimate. |

## Source and visual review

All **111** changed prompts were reviewed with the corresponding narration and S38 research/claims. **No prompt ID remains blocked** at this frozen hash.

- `pf001`, `pf002`, `pf071`, `pf072` now request grown English 1660s figures and, for the cheese shots, hard Parmesan with a smooth rind and no holes. They preserve the distinct first pit for Batten's wine/papers and second pit for Pepys and Penn's wine/cheese. The prompts do not assert the cheese's size, price, or later recovery.
- `pf005`, `pf073` now show an adult reader with an unlettered diary page and **empty desk space**. This removes a physical piece of cheese from scenes after burial, where its recovery is not documented. `pf109` and `pf110` also use unlettered pages; `pf076` calls for an unmarked letter sheet. Maps/plans in `pf016`, `pf025`, `pf027` are blank illustrative props and do not turn the reported oral exchanges into written testimony.
- `pf006` explicitly depicts an adult maid; `pf007` and `pf053` specify an adult male householder in a 1660s dressing gown; `pf012` leaves Jane's news oral without a physical note. These remove childlike or gender/period ambiguity from the first generated failure mode.
- Twelve alternating suffixes anchor adult 1666 English/British dress and period materials. Their final wording applies wood, brick, plaster or masonry only where an appropriate structure is visible, so a garden pit, Tower platform, boat, street or Moorfields crowd is not pulled into a modern classroom or an unrelated interior. There are 12 distinct suffixes distributed 9–10 times each.
- Later action sequence remains source-aligned: Pepys reports to the king and duke, asks for demolition, moves goods by cart and boat, observes the fire from the river, buries papers and then cheese in separate pits, sees the Deptford cargo watched before it is unloaded on September 6, and ends with no claimed recovery of the cheese. `pf040`, `pf059`, `pf076`, and `pf098` retain the R8a source corrections.

## Audit trail / boundary

R8b's initial SHA `ab93cbc5def915fcd082c5021be566c586c1e240daa40bd2b4cbed5de1f4eedb` and subsequent SHA `4910d26e9a36f46d41ef1fe298c01972f64de8e67a6b9ebfe070dee096ec791e` were **held** during review. The initial rotating suffixes sometimes named an interior for an outdoor shot, including pilot `pf002`; R8b2 neutralized those location cues. Final focused repairs removed post-burial cheese from `pf005`/`pf073`, made `pf006` adult, specified male period dressing gowns in `pf007`/`pf053`, and removed a note beside oral hearsay in `pf012`.

This PASS covers **prompt meaning and structure**, not generated image quality. R8a's first two auto-passed stills were human-rejected for childlike East Asian dress and a hole-riddled Swiss-style cheese. The next pilot must be inspected for adult English 1660s people, correct Parmesan, garden/outdoor staging, blank pages, and absence of modern objects before further image spending.
