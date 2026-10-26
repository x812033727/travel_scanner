# ES / PT / ID translation self-review

All three translator passes completed. This is translator self-review, not independent review. Only worksheet text fields were changed. No merge, backend, git, source, claims, audio, cache or paid action was run.

Current source SHA256: `e6e87e77f069a574d6e1d7f47bf2e5be031eb8566bb2edb71defa24ae4c2b99f`.
Translation started from freeze 232b4495 / speech 8028. Coordinator changed only five-small-examples.data.rows to one row; current source is e6e87e77. All 105 narration texts, metadata sources and worksheet budgets are unchanged. No worksheet regeneration.

Complete source meanings were retained. Static max_chars issues remain unresolved; actual dubbing and timing were not run. Paragraph structure and the full source-package URL match the source. Titles are under 100 characters, chapters under 30, tag lists under 500, and thumbnail headlines retain **255** and their line break.

| Locale | Lines | Chapters | Within static budget | Unresolved | Worksheet SHA256 |
| --- | ---: | ---: | ---: | ---: | --- |
| es | 105 | 7 | 78 | 27 | `864df775ca153d3b7e3876d31bf466e503e252c1e4be21a937cad0c40d2e9a3c` |
| pt | 105 | 7 | 67 | 38 | `7039ecdf73435aee76a45411456addb261e5601add0f9cd10e946f80d08d4ab6` |
| id | 105 | 7 | 77 | 28 | `496ec40177f66f52554f8f89ab85694ed675404dfce1946e75426a78422432ad` |

All non-text worksheet content matches its pre-edit immutable projection: sources, ids, scenes, todo flags, glossary, boundaries, max_chars and parts. Required names, scripts, URL, paragraph breaks, key numerical values and unsigned integer types were checked. Full per-line evidence, original/final SHA256, critique changes and unresolved text are in the accompanying JSON.

Critique corrections preserve AI as the author of a proof without treating it as a trusted prover, name the independent counter program, retain the Rocq kernel/compile timing, keep the complete memory premise and public-release-only halting scope, preserve the guard buffer-write limitation, and keep declaration/update repairs separate. Some over-budget sentences were deliberately expanded to retain these facts. The final spoken read also replaced literary comparison verbs with plain comparison verbs and Indonesian tak with standard spoken tidak.

Glossary: AI, Anthropic, C, Claude, RISC-V, Rocq, SAT and Theorem remain unchanged. The official proposition name halts remains unchanged in descriptions. Loop is localized as bucle (es), laco (pt; accented final spelling in the worksheet) and loop (id). Source titles in the worksheet glossary remain verbatim.

## es

Title: Claude y la verificación formal: qué garantiza un programa, explicado con 255

Unresolved static budgets (id: chars / max_chars):

- `z9dp`: 65 / 59 (+6).
- `bpnn`: 70 / 64 (+6).
- `c8r2`: 61 / 57 (+4).
- `qwaw`: 91 / 74 (+17).
- `4rff`: 72 / 43 (+29).
- `936d`: 91 / 68 (+23).
- `s57e`: 88 / 75 (+13).
- `yavq`: 65 / 63 (+2).
- `2zma`: 75 / 72 (+3).
- `4bqi`: 76 / 72 (+4).
- `w9b4`: 61 / 53 (+8).
- `dkjy`: 78 / 68 (+10).
- `u2xw`: 76 / 62 (+14).
- `rsx8`: 86 / 82 (+4).
- `zg4q`: 88 / 84 (+4).
- `cawx`: 65 / 38 (+27).
- `uqde`: 89 / 62 (+27).
- `5fga`: 76 / 58 (+18).
- `7ip9`: 100 / 79 (+21).
- `6x7t`: 110 / 57 (+53).
- `5u3j`: 56 / 47 (+9).
- `i2pt`: 79 / 74 (+5).
- `3u2q`: 87 / 66 (+21).
- `ucn4`: 90 / 71 (+19).
- `edry`: 72 / 50 (+22).
- `mhjn`: 40 / 28 (+12).
- `22tu`: 62 / 58 (+4).

Lines over the general 80-character readability guide: zfgp, qwaw, 936d, s57e, rsx8, zg4q, uqde, 7ip9, 6x7t, 3u2q, ucn4.
Independent review: pending coordinator assignment. Remaining uncertainty is native shortening and actual timing under the fixed source slots.

## pt

Title: Verificação formal com Claude: o que um programa garante, explicado com 255

Unresolved static budgets (id: chars / max_chars):

- `bpnn`: 67 / 57 (+10).
- `c8r2`: 55 / 50 (+5).
- `qwaw`: 82 / 66 (+16).
- `4rff`: 68 / 39 (+29).
- `fzz5`: 49 / 48 (+1).
- `936d`: 86 / 60 (+26).
- `yavq`: 58 / 56 (+2).
- `mfag`: 44 / 42 (+2).
- `zgkb`: 79 / 69 (+10).
- `gtuj`: 51 / 50 (+1).
- `2zma`: 80 / 64 (+16).
- `4bqi`: 72 / 64 (+8).
- `7d4v`: 53 / 52 (+1).
- `w9b4`: 56 / 47 (+9).
- `dkjy`: 80 / 61 (+19).
- `u2xw`: 72 / 55 (+17).
- `kq36`: 66 / 59 (+7).
- `qjaw`: 73 / 60 (+13).
- `p8te`: 61 / 55 (+6).
- `ey22`: 80 / 74 (+6).
- `rsx8`: 79 / 73 (+6).
- `zg4q`: 89 / 75 (+14).
- `cawx`: 59 / 34 (+25).
- `uqde`: 83 / 55 (+28).
- `5fga`: 72 / 52 (+20).
- `wi26`: 99 / 70 (+29).
- `7ip9`: 110 / 70 (+40).
- `6x7t`: 104 / 51 (+53).
- `5u3j`: 52 / 42 (+10).
- `cnnu`: 60 / 50 (+10).
- `cr5k`: 58 / 57 (+1).
- `3u2q`: 82 / 59 (+23).
- `ucn4`: 84 / 63 (+21).
- `bt2j`: 80 / 69 (+11).
- `mj65`: 65 / 61 (+4).
- `edry`: 72 / 45 (+27).
- `mhjn`: 40 / 25 (+15).
- `22tu`: 65 / 52 (+13).

Lines over the general 80-character readability guide: zfgp, qwaw, 936d, zg4q, uqde, wi26, 7ip9, 6x7t, 3u2q, ucn4.
Independent review: pending coordinator assignment. Remaining uncertainty is native shortening and actual timing under the fixed source slots.

## id

Title: Verifikasi formal Claude: arti jaminan program lewat angka 255

Unresolved static budgets (id: chars / max_chars):

- `bpnn`: 65 / 64 (+1).
- `4rff`: 58 / 43 (+15).
- `5iky`: 60 / 59 (+1).
- `zfmi`: 64 / 53 (+11).
- `dfhy`: 78 / 76 (+2).
- `4bqi`: 76 / 72 (+4).
- `xfvp`: 63 / 62 (+1).
- `cabc`: 52 / 50 (+2).
- `7d4v`: 87 / 59 (+28).
- `w9b4`: 58 / 53 (+5).
- `dkjy`: 77 / 68 (+9).
- `8ywa`: 64 / 63 (+1).
- `v9sd`: 67 / 62 (+5).
- `riuf`: 60 / 58 (+2).
- `ihny`: 75 / 74 (+1).
- `ey22`: 87 / 83 (+4).
- `cawx`: 54 / 38 (+16).
- `uqde`: 73 / 62 (+11).
- `5fga`: 61 / 58 (+3).
- `7ip9`: 119 / 79 (+40).
- `6x7t`: 104 / 57 (+47).
- `5u3j`: 62 / 47 (+15).
- `te3s`: 65 / 61 (+4).
- `3u2q`: 93 / 66 (+27).
- `bt2j`: 94 / 77 (+17).
- `mj65`: 89 / 68 (+21).
- `edry`: 67 / 50 (+17).
- `mhjn`: 37 / 28 (+9).

Lines over the general 80-character readability guide: 7d4v, ey22, rsx8, zg4q, 7ip9, 6x7t, 3u2q, bt2j, mj65.
Independent review: pending coordinator assignment. Remaining uncertainty is native shortening and actual timing under the fixed source slots.
