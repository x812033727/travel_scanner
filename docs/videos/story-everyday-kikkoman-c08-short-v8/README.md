# C08 Kikkoman short-v8 production project

The exact owner-approved 36 narration lines and 36 visual directions were projected from the frozen files in [the original C08 source folder](../story-everyday-kikkoman-c08/short-v8/README.md). This top-level folder gives the short revision its own resolvable `--slug story-everyday-kikkoman-c08-short-v8`. The historical `story-everyday-kikkoman-c08` folder and its 84-line script stay intact. Both slugs refer to C08 episode 8 in the **same** `brand-stories-everyday-reversals` series plan; they must never become two backend episode rows.

## Frozen source and projected bytes

- Approved narration: `../story-everyday-kikkoman-c08/reviews/v8-short-narration-candidate-20261024.md`, SHA-256 `040d9a499ddb864f62ebf0edcc948cc58439ffa13d0dae0ce5a9475297ee5d69`.
- Approved visual direction: `../story-everyday-kikkoman-c08/reviews/v8-short-visual-plan-candidate-20261024.md`, SHA-256 `0676e76a4c9d49b12ece74df1835a72ce264eabb24a3158635921f57244dd241`.
- Independent 36/36 narration and visual review: `../story-everyday-kikkoman-c08/reviews/v8-short-independent-review-20261024.md`, SHA-256 `f3a988efcad84a3d97779f10dd0d5cf34b7ad0d4ccf62db12ce357aa771326fb`.
- `video.json` and `visual-plan.json` are byte-for-byte copies of the nested frozen projection. The Markdown copies only repair relative links and describe the new C08-only duration decision; their spoken lines and visual directions are unchanged.

Do not regenerate these files with the ordinary chapter writer. The worker must check the frozen project before it starts C08 and before each continuation. A mismatch is a hold for a human review, never a reason to replace these files with the old 84-line project or a fresh model draft.

## Local nonpaid checks

```sh
node tools/video/cli.mjs lint --slug story-everyday-kikkoman-c08-short-v8
node tools/video/cli.mjs status --slug story-everyday-kikkoman-c08-short-v8
```

The source package has an earlier preflight in `../story-everyday-kikkoman-c08/short-v8/preflight-20261024.md`. Its 273.97-second body and 299.97-second total are **paper estimates**, not measured audio or video. [The duration receipt](duration-receipt-20261024.md) states the exact measured pass criteria. Current unresolved work includes independent `MoMA` pronunciation review, the `v7e03` flat spout diagram, illustrated body seconds, whole-film supplier quote and owner cost cap, actual audio/visual QA, backend dry-run and authorized import, upload and publication. The approved text/visual direction does not authorize those steps.
