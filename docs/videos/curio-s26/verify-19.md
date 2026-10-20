# S26 second-seed QA and ten-shot repair gate — 2026-10-20

The approved spoken script and 82/82 clean audio are unchanged. After the first 81 stills, seven source cards, 33 targeted redraws, six factual redraws and one wine/empty-plate redraw, the 14 remaining machine failures each received exactly one second seed. The full log is `/tmp/s26-keyframes-pass5-technical.log`.

| Item | Exact result |
| --- | --- |
| Prior `video.json` SHA-256 | `32a23d36fedf55ba41f0cb99c801584d79e8dfbab6235e48b7bd2c124fcade47` |
| Selected keyframes manifest SHA-256 | `94dd17130e6e1a3065fe60954f0a19cab4a06eea906b7b6d7a01112f5bc6f302` |
| Selected file integrity | 74/74 file hashes match manifest |
| Native-size receipt | `/tmp/s26-pass5-native-final.md` SHA-256 `b04634085273a7e51446fa05977238cb244c56b60354d9c90e6fca0cea944705` |
| Ledger after pass | US$1.9025 of US$3.37 whole-episode cap; 135 images, 135 image judges, one music; zero reservations |
| Remaining official machine failures | `ma013,ma018,ma051,ma056,ma098,ma083,ma086` (seven) |
| Machine-passed but native-size factual blocks | `ma009` bread with Rousseau's empty plate; `ma102` later quadriga monument at 1789 Versailles; `ma101` electric lamp/open marked magazine in 1841 |
| Blocked union | Ten illustrated scenes; no unsupported best-take override used |

`keyframes --accept-best` is unavailable for this video's `format: "drama"`. A judge's PASS cannot override a visible material contradiction, and a human visual WATCH cannot clear an official machine FAIL. Other new selections have only stylized or nonessential differences under the Curio native-size threshold; see the exact receipt.

For the ten blocked scenes, the new `video.json` SHA-256 is `e6e2d8fc45ec03131b5c5260027daf6b456110eaf2928311fc3e2f574374d34a`. Its JSON diff consists **only** of ten `scenes[].data.prompt` fields: `ma009,ma013,ma018,ma051,ma102,ma056,ma101,ma098,ma083,ma086`. Narration, IDs, all seven source cards, camera, look, chapters, thumbnail and metadata are unchanged. The independent source/period receipts are `/tmp/s26-pass6-root-source-period-audit.md` SHA-256 `b040209d0b2c15e44dd63b1aea52a9760d83b80f7c187167914bc8b649ac1e80` for the three factual scenes and `/tmp/s26-pass6-seven-root-audit.md` SHA-256 `4911176bb899664d3b5f6852833612d15fc2ba09a2c93beb0f5cde7d75587795` for the seven official failures. They PASS the exact combined preview. Formal project lint has zero errors and five existing/cosmetic warnings; runtime is still estimated 8.55 minutes with 82 lines. The seven cards leave 74/81 illustrated scenes (91.36%) and no adjacent card pair.

Prepaid dry-run with `--shot ma009,ma013,ma018,ma051,ma102,ma056,ma101,ma098,ma083,ma086 --takes 1` lists exactly ten shots and no end frames, approximately US$0.135 gross for one image and judge each. All other selected shots should come from their valid caches. The local media ledger before pass is US$1.9025, with zero reservations; projected actual after ten successful requests is US$2.0375, below the US$3.37 hard stop. Shared-rate count at preflight is 54 S26 image calls in the rolling hour; check again immediately before the paid command. After generation, all new selected files require another original-size material/source review and a sealed manifest and ledger before storyboard review.
