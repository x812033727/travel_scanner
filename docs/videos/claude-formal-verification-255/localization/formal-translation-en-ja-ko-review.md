# EN / JA / KO translation self-review

Current source SHA: `e6e87e77f069a574d6e1d7f47bf2e5be031eb8566bb2edb71defa24ae4c2b99f`. Translation started at `232b4495b433041007c039630ec517b7e0b4948c3cd7a5a47da6ecd88cae8a15`; root’s subsequent change was confined to slide-table layout. All 105 worksheet source strings still match.

All three worksheets contain 105 captions, 7 chapters, title, complete description, tags and all three thumbnail words. Only assigned `text` values changed. No merge, paid generation, backend, git, source or claims action was run.

Three own passes completed: source semantics; natural spoken register; numbers, C types, scope and current worksheet budgets. Character counts do not establish actual synthesized dub fit.

| Locale | Final worksheet SHA | Lines within budget | Remaining |
|---|---|---:|---:|
| en | `03bc2d9cc223484a4593ff3f0a97152cc396bd604e5da300f24d95ecb4d8d7e3` | 105/105 | 0 |
| ja | `8196e242410ad889165878f77a4e620ce5d7f779769ce9556b7fc2027506b64b` | 104/105 | 1 |
| ko | `cfb509d14a94c35fbbc4c7942be416a89abb77bb8d562b8f4f27615eadc3a13c` | 97/105 | 8 |

## Remaining budget blockers

Complete meanings remain in these lines; their budgets were not edited.

| Locale | ID | Chars / budget | Excess |
|---|---|---:|---:|
| ja | cawx | 28 / 22 | +6 |
| ko | zfmi | 28 / 26 | +2 |
| ko | wunt | 39 / 25 | +14 |
| ko | cgit | 25 / 22 | +3 |
| ko | cawx | 30 / 19 | +11 |
| ko | 7ip9 | 47 / 39 | +8 |
| ko | 6x7t | 32 / 28 | +4 |
| ko | 4nfp | 37 / 30 | +7 |
| ko | 3u2q | 34 / 33 | +1 |

## Semantic checks

- Guard input is 0..255; capacity is 8 bytes; 1 terminator byte is reserved within those 8; acceptance iff 0..7.
- 255+1 is computed after integer promotion as int 256; only subsequent unsigned 8-bit narrowing stores 0. Eight bits and eight bytes remain distinct.
- Widened guard preserves the complete value in both calculation/casts and storage; widening after a prior narrowing would still retain 0.
- Only the widened guard has no counterexample in both SAT directions; reject-all is a symbolic comparison, not another executed C variant.
- The guard makes only a Boolean acceptance decision and never writes a data buffer.
- The counter is an independent program. Fixed limit and no outside counter writer permit the 256-step cycle argument; 0.25-second timeout alone proves no nontermination claim.
- Counter declaration and update cast are both widened; every 0..255 input exits and returns limit+1.
- Rocq checks AI-written proofs at compilation; tools bind results to the fixed statement and audit listed assumptions against an allowlist.
- Public formal statements compare normal/error-checked builds of the same program under the normal-build specified memory-budget premise, with equal allowed observable finite-record sets.
- No termination proof is supplied in this public release only; no conclusion that the entire study lacks termination work. Study 123 libraries/239 entries versus public release 60 entries/25 libraries retained.
- Both local examples have actual C comparisons; local enumeration/SAT/control-graph methods are not Rocq reproduction or certification of the whole application.
- Full description paragraphs, pinned original-code/results URL, and original-SVG provenance retained; thumbnails retain **255** and the source newline.

## Critique and applied fixes

- EN wunt, 6a2b, w9b4: initial small budget excesses shortened without removing numeric values or the acceptance obligation; final EN 105/105 fit.
- EN description/4nfp: phrasing keeps the absent halts proof restricted to this public release and avoids inferring a study-wide absence.
- EN fzz5: root independently requested “Capacity is 8 bytes; reserve 1 byte for the terminator.” Applied as the sole EN delta after root-reviewed snapshot 24f084fb3e9975f09e1fc60f57818d4eedcade0027f90d659725f4234bb8316c.
- JA/KO fzz5 and local-description paragraph: explicitly reserve the terminator byte within the stated 8-byte capacity.
- JA qmcd: explicitly names the 8-bit counter; kq36 explicitly says 256 steps; Rocqカーネル terminology kept consistent.
- JA wunt: retained 0,1,2,3,4 and five small selected values while shortening to 29 characters.
- KO: own spoken/semantic shortening reduced initial 61 budget excesses to 8; complete assumptions, numbers, negations and release scope retained in the remaining over-budget lines.
- No independent review of JA/KO was commissioned; root will assign cross-review.

## Titles and glossary

- en: Claude Formal Verification: What 255 Reveals About Code Guarantees
- ja: Claudeの形式検証研究：255から分かるプログラムの保証
- ko: Claude 형식 검증 연구: 255로 이해하는 프로그램의 보장

Product and acronym spellings stay `AI`, `Anthropic`, `C`, `Claude`, `RISC-V`, `Rocq`, `SAT`. Metadata’s code identifier `loop` remains Latin. No Chinese pronunciation aliases were invented, including for null lexicon entries. Worksheet glossary/boundaries were not edited.

EN also completed root’s independent review: the reviewed snapshot plus exactly the requested `fzz5` clarification bind to the final EN SHA above. JA and KO await root-assigned independent review.
