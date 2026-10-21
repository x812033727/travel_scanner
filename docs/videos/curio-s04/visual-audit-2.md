# S04 full first-pass frame audit

2026-10-20: MiniMax `keyframes --takes 1` completed the 91 illustrated scenes after the earlier 33-frame pause. Twelve previously acceptable selected frames remained cached. The episode ledger at first-pass exit was **US$1.582** against the delegated whole-episode image-and-music ceiling of **US$3.77**. The full-size selected-file notes are in `/tmp/curio-s04-live-qa.md`. Contact-sheet generation was skipped because the CLI did not find Chromium under its default Playwright path; the final cache-only run will set `PLAYWRIGHT_BROWSERS_PATH=/tmp/curio-playwright` to create the sheets.

The machine judge left 22 `needs_review` shots: `jingzhou-navy`, `cao-withdraws`, `ride-to-ning`, `why-surrender`, `water-sickness`, `ning-freed`, `not-anger`, `zhou-audience`, `ask-sunyu`, `take-shu`, `turn-north`, `letter-first`, `people-unsettled`, `life-length`, `baqiu-death`, `age-thirtysix`, `move-lukou`, `letter-warns`, `after-letter`, `novel-last-order`, `novel-cry-question`, `novel-lusu`. Its pass is not sufficient visual approval: it passed a modern road and a ballpoint pen.

Manual full-size review blocked 12 selected shots for a material source, era or action conflict:

| ID | Visible blocker |
| --- | --- |
| `ning-freed` | Generated gate glyph/watermark rather than an unlettered Han outpost. |
| `cao-ren-hears` | Later uniform/parade and a visible invented `明` on the gate; report arrival is lost. |
| `sudden-illness` | A comfortable upright pose does not convey the quoted severe illness. |
| `regret-plan` | The supposed regret is a cheerful map display. |
| `age-thirtysix` | Modern painted asphalt road/sign and duplicate child figure at Baqiu. |
| `meet-at-wuhu` | Modern-looking wheeled funeral trailer and cheerful greeter. |
| `chengpu-takes` | Modern rank-tab uniform on the new Nanjun governor. |
| `novel-liuzhang` | Ballpoint pen in the novel's ancient riverboat scene. |
| `novel-sigh` | Smiling figure in place of the novel's long sigh. |
| `after-letter` | Modern pen and visible bottom-right generated logo/watermark. |
| `novel-last-order` | The final address to soldiers has no visible address/action and fails the image judge. |
| `famous-cry` | Neutral silent stare instead of the novel's shouted cry. |

The `cute-mystery` preset intentionally draws chibi proportions. Proportions alone were not used to reject a still; the blocker list concerns a misleading prop, setting or action. The history-reader desk shots are modern editorial illustrations and do not purport to reconstruct a Han study. Only the 12 material prompt leaves were changed; the exact revised `video.json` SHA-256 is `9de9df01dc4be9a3e0eebf98c000704aaf0b40f12d2f5dba0e32ce14c6daff46`. Lint is 0 errors/0 warnings. Independent source/period/action review first identified the five novel shots' missing book-page boundary and `after-letter`'s parchment; a focused recheck passed after all five visible page borders were restored, `after-letter` used paper, and the accidental `cao-busy` wording change was removed. Script, claims, audio and the other 79 picture prompts did not change.

The bounded second run uses `keyframes --takes 2` to preserve accepted cache, retry machine failures with the judge's concrete fixes, and regenerate the 12 human-blocked frames. All newly selected frames require another manual check before assembly.

## Bounded second pass

The second pass finished with **91/91 selections and 83/91 machine passes** at an episode ledger of **US$2.068/3.77**. Eight IDs still have `needs_review`: `ride-to-ning`, `take-shu`, `people-unsettled`, `life-length`, `letter-warns`, `novel-liuzhang`, `novel-sigh`, and `after-letter`. The failed takes stay in the manifest; none is accepted into the cut. The pass log is `/tmp/curio-s04-repair-pass2.log`.

The last four fiction scenes exposed a judge conflict with a paper border enclosing the whole picture: the judge repeatedly called that border letterboxing or a bad frame. `novel-liuzhang` also drew a modern laptop. The new prompt keeps the novel visibly separate with an **open, unlettered storybook inside the foreground** of a full-frame ancient scene. It also simplifies horse mounting, the small route counter, camp map, and letter images to address the other four failures. Exactly those eight `data.prompt` leaves changed after the second run. Independent static review found that a proposed stirrup would be too early for the late Han scene, so `ride-to-ning` now depicts mounting a horse without that prop. The exact `video.json` SHA-256 is **`266720c91045cc556bf0637f719ddf5452fc038e9bbae12bb49e8dae0c24a334`**; independent source/fiction-cue recheck **PASS**, lint **0 errors/0 warnings**. Bounded `keyframes --takes 2` pass three is running; all new selected frames still need full-size human review. Script, claims and audio remain frozen.

## Third-pass selection and no-spend proposal

Pass three finished with **89/91 machine passes** and an episode ledger of **US$2.22/3.77**. Its two failed IDs are `ride-to-ning` (the model repeatedly shows a rider already mounted) and `novel-sigh` (an outer paper margin is repeatedly judged as letterboxing). Full-size inspection also rejected machine-passed `novel-liuzhang` (a modern badged peaked cap) and `after-letter` (a modern red pen and invented writing). Other inspected new selections show the relevant ancient action or a harmless diagram.

The no-spend revision replaced those four scenes and the adjacent `novel-last-order` scene with five sourced `big` cards. The extra novel card keeps the fiction label visible through the instruction to soldiers. Independent source and fiction-boundary review passed at `video.json` SHA-256 **`a175ec21d6cea449df9b3000cee77d55a3dbfc9da4361637ed7897e79f01f7b6`**. The cache-only `keyframes` rerun generated zero images, selected 86/86 judged pictures, and kept the episode ledger at **US$2.2165/3.77**.

## Final full-size review and storyboard gate

The four contact sheets and suspect selected files were reviewed again at full size. One more machine-passed scene, `right-rib-1-trim.jpg`, showed an arrow held at the waist and blood on the ground while `s04029` says a stray arrow struck Zhou Yu's right ribs. It was replaced by a history-labeled card: `《三國志》〈周瑜傳〉` / `右脅中箭` / `南郡陣前，一支流箭射中周瑜`. An independent check confirmed the card against the pinned SZ54 passage `瑜親跨馬擽陣，會流矢中右脅` and found no implied link to Zhou Yu's later death. The other selected frames have no clear material period or source contradiction; modern desks shown as present-day source-reading illustrations were not treated as ancient reenactments. Two lower-scoring files (`given-command-1.jpg`, `cao-threat-question-1.jpg`) also received independent native-size material review: tiny red/black mouth-edge artifacts were judged cosmetic, without a false injury or modern microphone, and their command/map scenes fit the narration.

Final `video.json` SHA-256: **`ebe848b17ccbc255297fce93ee7791e9b5ffbff01353ff6d66c027e25e164a25`**. Final cache-only `keyframes` generated **zero** new images in 12 seconds, selected **85/85** machine-passed stills, and left the ledger **US$2.2165/3.77**. All **six** cards cite the relevant source; **85/91 = 93.4%** of body scenes remain illustrated, with at most **three** adjacent cards. Lint is 0 errors and one nonblocking word-frequency warning (`timber` in 30 of 85 picture prompts). The rendered seven-state contact sheet visually shows the six cards and outro.

The 92 spoken lines and `script.md` SHA-256 `2201aaa948660f2375d60d5fe598a87c4a61e10d22cf32c137c2702d1ba494ac` never changed. The current storytelling-panel input SHA-256 `f83c643777d995114f2b60eca609952e706e6e30dc22fbb0a084facdb7eb0528` exactly matches the earlier independent 13/13 reading. Because the tool's narrative binding also includes scene templates, the original sealed answers were transparently re-recorded for this visually revised manifest; **this was not a new blind reading**. The prior receipt is preserved as `review/narrative-before-visual-rebind.json` in the work directory. Under the user's standing instruction to proceed with recommended choices, the local storyboard gate was approved at 2026-10-20 03:33 UTC, manifest SHA-256 prefix `cd79da789412`. No rejected frame is selected into the cut.
