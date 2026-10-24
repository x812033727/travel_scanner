# C08 Kikkoman short-v8 production project

The exact owner-approved 36 narration lines and 36 visual directions were projected from the frozen files in [the original C08 source folder](../story-everyday-kikkoman-c08/short-v8/README.md). This top-level folder gives the short revision its own resolvable `--slug story-everyday-kikkoman-c08-short-v8`. The historical `story-everyday-kikkoman-c08` folder and its 84-line script stay intact. The current `brand-stories-everyday-reversals` series plan points C08 episode 8 to the short slug. A guarded import updates that existing episode row; the historical project remains a separate source folder, never a second backend episode row.

## Frozen source and projected bytes

- Approved narration: `../story-everyday-kikkoman-c08/reviews/v8-short-narration-candidate-20261024.md`, SHA-256 `040d9a499ddb864f62ebf0edcc948cc58439ffa13d0dae0ce5a9475297ee5d69`.
- Approved visual direction: `../story-everyday-kikkoman-c08/reviews/v8-short-visual-plan-candidate-20261024.md`, SHA-256 `0676e76a4c9d49b12ece74df1835a72ce264eabb24a3158635921f57244dd241`.
- Independent 36/36 narration and visual review: `../story-everyday-kikkoman-c08/reviews/v8-short-independent-review-20261024.md`, SHA-256 `f3a988efcad84a3d97779f10dd0d5cf34b7ad0d4ccf62db12ce357aa771326fb`.
- `visual-plan.json` is byte-for-byte the nested frozen projection. `video.json` differs only by a `say`/text-hash-bound `say_for` on `v7be06`, reading displayed `MoMA` as `紐約現代藝術博物館` in Taiwan Mandarin; all 36 `text` values, IDs, scene directions and order are unchanged. [Independent text pronunciation review](pronunciation-review-20261024.md) passed; real audio listening remains HOLD. The `explainer` video category supports the approved six `stats` cards; the backend episode and worker belong to the `story` series. The Markdown copies repair relative links and describe the new C08-only duration decision.
- `story-lexicon/` is the initial pinned pronunciation snapshot generated from the current shared `docs/videos/lexicon.json` (SHA-256 `a055c83f97376dc2b179e04fa0eeb092d67c9987420b1fe6264f3f5b5af0107d`) and this project's `series.json` names. The strict reader verifies the genesis chain, lexicon hash `97e2c4582aca65899d66253914a955256a673484a97966f40013d1275fc2e8f2`, and event hash `783a192013e5d27bb9e3728c111f4e82bdd04829326830caeeca61285e3aeb17`. This pre-authored project already has `video.json`, so the worker cannot use the usual empty-story genesis; it reads this frozen snapshot instead. The snapshot does not approve any actual voice or paid TTS.

Do not regenerate these files with the ordinary chapter writer. The worker must check the frozen project before it starts C08 and before each continuation. A mismatch is a hold for a human review, never a reason to replace these files with the old 84-line project or a fresh model draft.

## Local nonpaid checks

```sh
node tools/video/cli.mjs lint --slug story-everyday-kikkoman-c08-short-v8
node tools/video/cli.mjs status --slug story-everyday-kikkoman-c08-short-v8
```

The source package has an earlier preflight in `../story-everyday-kikkoman-c08/short-v8/preflight-20261024.md`. Its 273.97-second body and 299.97-second total are **paper estimates**, not measured audio or video. The reviewed `MoMA` pronunciation gives a newer paper estimate of 275.63 seconds for the body and 301.63 seconds with bookends. [The duration receipt](duration-receipt-20261024.md) states the exact measured pass criteria. The owner [approved](owner-pilot-approval-20261024.md) the [conditional whole-film quote](production-quote.md) with a US$25 cap, but the dedicated C08 ledger and provider readback do not exist yet; no paid request may start. Current unresolved work includes the `v7e03` flat spout card diagram, illustrated body seconds, actual audio/visual QA, backend dry-run and authorized import, upload and publication. The script/visual and cost approvals do not prove those steps complete.
