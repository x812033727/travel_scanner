# A01 packaging portability correction — 2026-10-19

Status: **independent packaging equivalence review passed; awaiting new exact-version merge approval**. Baseline commit: `cd12083117f456935a94be45f7c9f5b020d253eb`. See the [independent review](independent-equivalence-review.md). This is a packaging correction, with no new story revision, verifier receipt, owner approval, host import, paid work, or publication.

## What changed

Ten historical Markdown files contained private local paths. Those paths are now logical `<repo>` / `<home>` locations. A local Markdown link becomes its original label plus an inline logical locator, so it does not claim the historical target exists in this partial package. Some r43 targets are absent from the packaged subset; the locator still describes the original reviewed file and line. Public source URLs, report findings, verdicts, reviewed-manifest references, and all other wording are unchanged.

The two r44 builders now distinguish original raw report/readback provenance hashes from actual portable packaged-file hashes. Their `source-map.json` files remain byte-identical. The current manifests bind the redacted copies through `packaged_reference_sha256`. The r45 source map is also unchanged.

The r45 builder pins both its current source manifest and the historical owner-approved r44 manifest. It verifies every current r44 output against the historical output hash map, then validates the unchanged owner-direction JSON against the historical identity. Existing independent reports retain their original reviewed identities; they are not reissued for the portable manifests.

Only downstream build pins, packaging manifest hashes, metadata provenance fields and handoff README provenance text were rebound. The canonical handoff continues to supersede the original handoff for adoption. Original handoff chapters/composed content and its CHANGES REQUESTED report remain unchanged; its original raw manifest is retained here.

## Evidence

- [Machine-readable receipt](receipt.json): exact old/new SHA-256 for each modified original file, all unchanged original files, five original/current manifest pairs, and checks. It is outside the manifests to avoid a self-referential hash cycle.
- `historical-manifests/`: five byte-identical original manifests. Their historical raw report hashes are provenance, not hashes of the redacted current copies. Both existing nested r43 manifests also remain unchanged.
- A private, create-only backup outside the repository preserves all 103 original files. Its receipt SHA-256 is `52814f60cc78802aedbd6088cd0070240829517c3fbedee6f0436ddb3dadd36f`. Private source paths and raw reports are not republished. Original source worktrees were not edited.
- Original owner-direction JSON SHA-256 remains `06008d40ba253ffdbf3d3017fac0a3fe27e95e24b27d7c1ac09e49d1272be02a`.

## Current portable manifests

| Package | SHA-256 |
| --- | --- |
| `A01-editorial-candidate-20261019-r44` | `a2a82be58698b6062e343a55e375c5bccd88ccd4d2ee596fc6ded400bc9db234` |
| `A01-r44-main-rebuild-20261019` | `b1641880b551941dc0c253ff82c6954f3c37ab9514fed8a9be5e61523664d8e1` |
| `A01-editorial-candidate-20261019-r45` | `896615541683e620eb6e79468d8d304f146ad932700a7f044d5a1eb9784888f6` |
| `A01-worker-handoff-r45-20261019` | `7ba60fd949319420444a3236eec1180f02543a4f8d406e89b089f34b722f5fdf` |
| `A01-worker-handoff-r45-canonical-20261019` | `73cf375736d13a899e261000d1ad694f876e4f1101e2e9454210c1063dd9e4e4` |

## Verification scope

The main-rebuild, r45, original handoff and canonical handoff `build.mjs --check` pass on the current checkout. The canonical composition remains six chapters, 51 scenes, 53 narration lines, 55 PENDING claims, 15 plan-fact mappings, 40 passage-only mappings, eight loop pairs and six source URLs; lint has zero errors and 39 warnings. All candidate files, chapter files, composed video, lexicon, semantic maps and owner direction are compared byte-for-byte against the baseline.

The historical editorial r44 `--check` already failed `stale output: validation.json` before this correction: its frozen 40-warning validation differs from current main's 43-warning lint. That historical output is intentionally unchanged. The separate main-rebuild check passes and the current r45 narrows those warnings to 40. This correction does not claim the old checkout-dependent report was rerun successfully.

Repository hygiene checks scan tracked paths; the new evidence files are also checked directly for private-path patterns. Exact test outcomes and unchanged-file hashes are in the author's receipt. The subsequent independent review verifies that receipt against baseline Git blobs and reruns the r45 and canonical builders.
