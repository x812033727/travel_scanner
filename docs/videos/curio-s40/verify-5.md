# S40 R4a still-prompt repair handoff

2026-10-20. The independent R4 [blind seal](verify-r4-blind.md) records **13/13 Yes** on exact script SHA-256 `b255fb2ae6cefbed88b9913e1be046f5ffc0fd35cf1b94d06347460f96f7e7b3`. The independent [source and visual audit](verify-r4-source-visual.md) re-opened the three pinned texts and passed **83/83 spoken claims** and all corrected citation ranges, while holding five still prompts. No R4 media was generated.

The five prompt blockers were `cl019` (palace instead of Plutarch's guarded tomb), `cl031–cl033` (an invented written Dolabella note and three physical travel bundles), and `cl055` (a sealed basket despite the guard opening it to inspect the figs). R4a changes exactly those five `scenes[*].data.prompt` leaves. A parsed JSON diff against the R4 commit found **no other changed field**. `cl019` stays at the guarded stone tomb; `cl031–cl033` depict a discreet oral exchange and the queen hearing news with empty hands; `cl055` shows an unsealed, opened wicker fig basket. All five retain one main visible action/subject and do not assert which death method occurred.

| Frozen R4a file | SHA-256 |
| --- | --- |
| `video.json` | `f4386a4f14882c5e169f7dabd14023c33beff770d3ac15fc46202246db4afec3` |
| `script.md` | `b255fb2ae6cefbed88b9913e1be046f5ffc0fd35cf1b94d06347460f96f7e7b3` (unchanged) |
| `claims.md` | `ee568874c7b4198186e70eec5683a17a55f969cf657002b01360b8b5c258499c` (unchanged) |

`lint --slug curio-s40 --json` is **0 errors / 0 warnings**, 84 spoken lines including outro, estimated full 9:15 and story body about 8:32. The R4 narrative/source pass remains bound to the unchanged script and claims. The subsequent independent [R4a focused audit](verify-r4a-focused.md) passed all five amended prompts on this exact JSON hash; generated art still requires separate visual review. This handoff is the coordinating author's change receipt, not the independent R4a audit.
