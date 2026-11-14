# S38 R8a prompt-only visual precision pass

2026-10-20. The R8 [script](script.md) and [claim ledger](claims.md) remain byte-for-byte identical to the independent R8 source and audio gates; script SHA-256 `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`, claims SHA-256 `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`. Before any paid image request, the coordinating agent applied three **prompt-only** fixes suggested by the R7/R8 independent reviewers:

- `pf040`: describe fire spreading upstream and downstream around the bridge, rather than ambiguous “both sides” that might mean only the two banks.
- `pf076`: show Pepys writing the letter on an unmarked sheet, without inventing an identified messenger or a documented handoff.
- `pf098`: place one foreground evacuee among a densely crowded Moorfields, so the generated frame cannot suggest the field was empty.

The resulting `video.json` SHA-256 is `65ba99a5f6e28aef6dffbbe63828f080025a0c20e61120a75304d5aaf0635426`. `lint --json` still reports 0 errors and 0 warnings; `status` retains the exact script and 0-flag audio approvals. All earlier 111-prompt checks were bound to the previous JSON hash and are not represented as having seen this version.

An independent reviewer then checked the parsed R8→R8a diff, exact hashes and the three amended prompts against the pinned diary. [The focused audit](verify-9-audit.md) **passes**: exactly those three prompt leaves changed; `script.md` and `claims.md` are unchanged; `pf040` matches diary L65897–65901, `pf076` L66004–66012, and `pf098` L66102–66109. Lint remains 0 errors / 0 warnings. The audit file SHA-256 is `9b78bc510f974616d2b987b192322da9e699a54bac48f296d83e751e441d5e25`. This clears the static prompt gate; generated images still need visual QA. The pre-quoted US$4.58 image-plus-music ceiling remains in force.
