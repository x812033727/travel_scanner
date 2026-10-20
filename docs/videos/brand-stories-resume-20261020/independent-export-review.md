# A01 r47 offline production-export review

Reviewer: `brand_resume_review`, independent of the export author. Date: 2026-10-20.

**PASS for offline export fidelity after two corrections.** This report covers the four exact files below. It does not approve historical claims, worker adoption, paid generation, actual audio duration, final media or publication.

## Exact reviewed files

Paths are relative to `docs/videos/brand-stories-resume-20261020/`.

| File | SHA-256 |
| --- | --- |
| `build.mjs` | `2ba3d51a3dfb8209cd3e4ecc461f1f2e680c8b1e20c86ff2ebb80622b859cb6b` |
| `production-status.json` | `328fae493260907c6f52bd93a906bb5560496d041adcf3e11d5579f24fed39af` |
| `A01-narration-cues.tsv` | `19b199ff2a9e7cbd0b10a7436e6fdffd2c50c39bd1bc42d946500e4f040d47f4` |
| `A01-shot-list.tsv` | `e7dc02e22899cf5212c9be49e8365a71abb50e4ab47cc48584d1d64ca507b6ae` |

The upstream editorial manifest is `323dc77c5ec678ef38c35204eb7865d46c8ca612b5e82f0a6083ddf70c59a24e`. The canonical handoff manifest is `3edb9c375bcef6b01adc4e7bd14eec3757dd907d16a175247f8468a063465fb2`. Both were read and hash-checked. The canonical package is `docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-worker-handoff-r47-canonical-20261019`.

## Independent checks

Read repository `AGENTS.md`, the `brand-story` skill, the export builder and outputs, canonical six chapter files, `worker-composed-video.json`, manifest and metadata delta. Existing r47 narrative and canonical reviews were read for their stated scope; their PASS results were not reissued as worker receipts.

Executed from the repository root:

```bash
node docs/videos/brand-stories-resume-20261020/build.mjs --check
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-worker-handoff-r47-canonical-20261019/build.mjs --check
```

Both commands returned exit code 0. An independently written read-only Python comparison also returned exit code 0 and verified:

- All 52 narration rows, including chapter, scene and line IDs, exactly match the canonical chapter text. All 50 shot rows exactly preserve template, visual mode, camera and prompt. The corresponding composed-video text and scene data agree. Line and scene IDs are unique.
- Scene membership uses the canonical composed-video claim lists. The exported lists cover exactly the 54 chapter claim IDs. All 54 remain `PENDING`; 15 have a plan-fact link and 39 retain `fact: null`. This is not source verification.
- There are 49 `shot` scenes with `visual: still` and one other scene. These counts do not establish the number of billable images or remaining paid requests.
- Every input SHA-256 listed in `production-status.json` matches its current file, including `metadata-delta.json`. All 12 publication metadata difference paths are retained with a decision-pending status.
- The actual body duration remains unknown, the duration gate remains false, and 450.4 / 414.1 / 383 seconds are explicitly model estimates. The 420–480 second requirement is identified as the A01 compact exception; it is not generalized to the series.
- The export does not grant host-write, paid-generation or upload permission. Its budget has a US$25 all-in cap, unknown actual spend and remaining balance, and no approved batch. The builder performs local file reads/writes only and makes no provider or host calls.

## Findings corrected during this review

1. The first export read publication differences from fields absent in the canonical manifest and produced `null`. The author changed it to read and hash-bind `metadata-delta.json`; the final export retains all 12 paths.
2. The first TSV export read `scene.claims` from chapter scenes, where that field is absent, leaving every membership cell empty. The author changed it to use composed-video membership and added scene/data equality and exact claim-set assertions. The independent comparison above confirms the corrected rows.

No unresolved export-fidelity defect was found in the exact reviewed files. No upstream manuscript, source claim, prompt, old review or approval was changed by this reviewer. No network request, paid generation, host operation, audio measurement or upload was performed. This packaging PASS must remain separate from the production HOLD and the user's execution instructions.
