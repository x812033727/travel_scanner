# S26 final two-shot art preflight — 2026-10-20

The 82-line spoken script, approved audio and all source claims are unchanged. This receipt covers paid image passes after [verify-19.md](verify-19.md) and the last source-safe resolution of their remaining blockers. The S26 `format: "drama"` does not permit `--accept-best`; every illustrated scene must pass the normal judge and original-size factual review.

| Check | Exact result before this final paid pass |
| --- | --- |
| Current `video.json` SHA-256 | `2050264bcfd766bf2f87a4d6a0876d0b61f7672fa974da4f90150016aae76231` |
| Independent source and structure audit | `/tmp/s26-pass9-root-three-final-audit.md` SHA-256 `c2d89f7c8073a058cf260669ab7f7d10c7e891d0b94ee8d36abd2743ab4ef543`, PASS |
| Prior selected manifest SHA-256 | `242e2683ef212bf8d4e975b1d4cc767d780b18e9c56ad3621b87a8eaa377d318` |
| Whole-episode ledger | US$2.105 of the approved US$3.37 cap; 150 images, 150 image judges, US$0.08 music, zero reservations |
| Shared rate preflight | 36 image requests in the rolling 60 minutes across local episode ledgers at 09:16 UTC; no S26 STOP file |
| Storyboard | Not sent for owner review yet; no owner approval claimed |

Pass 6 generated ten targeted takes for US$0.135, pass 7 generated four second seeds for US$0.054, and pass 8 generated one third seed for US$0.0135; the combined ledger is US$2.105. Pass-7 selected `ma009`, `ma051` and `ma098` pass the judge and original-size source review. Pass-8 `ma013` scored as passed but its neckcloth became a detached cartoon head; that is a material block even though the model passed it. `ma102` still has a judge failure and the prior picture moves the carriage toward the camera; `ma083` still has fake text and an extra figure in the supposedly empty archive drawer.

The present exact preview changes only `ma013` and `ma102` prompts and converts `ma083` to a short attributed source card. It does not alter narration, scene IDs, order, chapters, audio, look, or other selected visual prompts. The Karr card quotes **un livre daté de 1760**, explicitly as Karr's April 1843 claim, and states that the excerpt gives neither a book title nor a page number. The independent audit confirms its wording and placement. The body has 73/81 illustrated scenes (90.12%) and at most one card in a row. Formal lint reports zero errors and five existing cosmetic prompt warnings.

`keyframes --shot ma013,ma102 --takes 1 --dry-run` names exactly those two shots and no end frames or obsolete `ma083` image request. It estimates about US$0.027 for two image-and-judge pairs, making projected episode spend US$2.132, below the hard cap. Generate only those two normal takes, then inspect both selected images at native size, seal the resulting manifest and ledger, and refresh the narrative hash after the source-card change before submitting the genuine storyboard owner gate. No manual best-take override or invented site approval is allowed.
