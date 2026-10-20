# S26 illustrated storyboard handoff — 2026-10-20

The current episode keeps the same 82 spoken lines, audio and music. The final `video.json` SHA-256 is `032cef0a877504d678dd731930571bb2ccf301369beb7f6a104d7c1ccd36d7a8`. The last source-card change is confined to `ma102`; its question and all other narration remain byte-equivalent. Independent exact source/sequence review PASS is `/tmp/s26-ma102-root-final-audit.md` SHA-256 `137fe316cbaaa65c7a6b452057679e7fb5bb3aefc8a70369cccdd2619884b8ad`.

`ma013` final illustrated take `keyframes/ma013-1-trim.jpg` SHA-256 `f2d8d86ca44ffdce35d293b266d7177818c69e6db2a312bfecda9ec0dc4a7179` passed the normal judge (9.29/10) and two original-size human reads: one attached, period-dressed gentleman beside the door, without the earlier detached-head artifact. `ma102` received two normal takes after an unbilled MiniMax ReadTimeout; neither passed the judge. Its first take was source-safe but scored zero on style; its second had a stray animal and missing harnessed horses. As `format: "drama"` cannot `--accept-best`, neither image was selected as approved. The final card reads `坎潘事後回憶 / 一點鐘離開凡爾賽 / 接著記下車旁的呼喊`. Campan's pinned text SHA-256 `032cf8eb51c71e3222830c7b9db659259538d1e860eef7c0f2ce155b15dbf91a` says the King and Queen set off from Versailles at one o'clock, then records the crowd's bread cry. The card does not state that she witnessed the scene or give away the next spoken answer.

| Final handoff check | Evidence |
| --- | --- |
| Normal selected images | 72/72 judge PASS; all 72 selected image SHA-256 values match their files; `ma102` is a card, not a selected failed image |
| Selected manifest | `/workspace/.video-work/curio-s26/keyframes/manifest.json` SHA-256 `9480c377f89de043003e2d7f97e33cceac449782aa24cc878632e7b430ca5919` |
| Still/card cadence | 72/81 body scenes illustrated (88.89%), maximum one consecutive card |
| Project lint | Zero errors, five existing cosmetic prompt warnings; 82 lines, estimated 8.5 minutes |
| Media ledger | US$2.1455 of approved US$3.37 whole-episode cap, zero reservations; cache-only final rebuild generated zero images |
| Storytelling panel | Genuine script-only answers SHA-256 `424f96818ae2ed2ab221e2ace168b90102928d440d64df99acd07674378ba841`, official 13/13 PASS after both source cards; narrative hash `b1e0b8cdd78dea38`, verdict SHA-256 `36039fc4585cea63c0579ca22efcdc0f479995d9ff5927754e6de24551e97c8d` |
| Contact sheets | `keyframes/contact-sheet-01.png` SHA `0ff8da60…`, `-02.png` SHA `9ef77a82…`, `-03.png` SHA `7547dc39…` |

`review-push --gate storyboard` submitted this exact current board to `/admin/videos`; the command reported **pending owner review**, log `/tmp/s26-storyboard-review-push.log` SHA-256 `424b9aeb8ffd45080e886a7dd2d81bf5b8bcedc7b053690aa26ecf843a2946bd`. No owner storyboard decision, render, final video, YouTube upload, or clickable Studio elements are claimed. After the genuine `review-pull` approval, render and assemble with the installed local 5-second animated intro after the 32–47-second condensed opening and 21-second animated outro, with final 16 seconds reserved for Studio's two video elements and subscribe element. The release description must include source and channel URLs, captions, thumbnail and chapter timestamps.
