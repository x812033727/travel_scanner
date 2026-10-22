# r47 source-delta verification — 2026-10-19

Reviewer: root `codex-gpt6-a01`, coordinating the revision; the artifact builder
and text edits were produced by a separate author agent. This is a bounded
source/mapping comparison, not a third blind narrative review or a fresh
retrieval of the historical sources.

Reviewed manifest SHA-256:
`323dc77c5ec678ef38c35204eb7865d46c8ca612b5e82f0a6083ddf70c59a24e`.
Video SHA-256:
`50eda967324abcfc66b2f6d76e251649344cb841178aa79e36bf57dc63eebbc2`.

**PASS for the declared delta and preservation of source relationships.**

## Independent comparison

A separate assertion script compared the actual r46/r47 JSON and claim files,
without accepting the author's change report as the comparison result:

- Exactly six retained narration fields differ: r44l001, r44l041, r44l042,
  r44l044, r44l045 and r44l047.
- The last chapter marker moves from now-zipper to now-aisle. All surviving
  scene and line identities remain; their chronological order is unchanged.
- Only now-answer/r44l050/q055 is removed. Its claim summarizes ground movement
  and the pocket-related stow problem already supported by q042 and q050–q053.
- All 54 surviving claim rows are byte-identical and PENDING. All 50 surviving
  scene prompts, data and claim memberships are identical. All three outro
  lines remain identical.
- All eight setup/payoff pairs, six public URLs, lexicon, voice, thumbnail,
  music, captions and other top-level video fields remain identical. Only the
  opening loop's explanation changes.
- Source-alignment rows equal r46 minus q055. The source map's source indices
  and claim memberships equal r46 minus q055; its snapshot and historical
  prototype/year caveats are unchanged. The series differs only in its status
  note.

## Reading the six changed lines against retained claims

| Line | Retained evidence | Boundary |
| --- | --- | --- |
| r44l001 | q001, q050–q053 | Introduces the known stow failure without revealing the remove-and-stow remedy. No additional failure event is asserted. |
| r44l041 | q046–q047 | The existing overpacking observation leads to a narrator question about the zipper, answered by its recorded result. |
| r44l042 | q047–q049 | Preserves the no-jam result and thickness preference. The cabin transition does not claim a documented testing order. |
| r44l044 | q049–q050 | Explicitly recalls the opening failure instead of treating the known outcome as a new mystery. |
| r44l045 | q048, q050–q052 | Contrasts aisle and storage dimensions, then asks where volume increased. It supplies no measurements or assertion that this particular case passed a particular aisle. |
| r44l047 | q052, q054 | Retains pocket expansion and asks about the final judgment. The answer remains one of the reporter's preferred cases, not the only winner. |

Historical source dates and annotation wording are not renewed by this review.
The earlier q028 annotation caveat remains documented in the r46 source-delta
report. No new factual-answer claim or source URL was introduced.

## Checks and limits

Root reran the frozen builder with `--check`: 50 scenes, 52 lines, 54 claims,
eight loops, zero lint errors and 39 retained warnings. All frozen output
hashes matched. The 45-second cadence check has zero gaps at 250/275/300 CPM.

Estimated body durations are 450.4/414.1/383.0 seconds; actual TTS is unmeasured.
`duration_gate_passed=false` remains correct. Formal verifier/listener receipts,
the 420–480-second audio gate, guarded adoption, final media and owner viewing
remain unfinished. This report supplies no host or paid-production authority.
