# S61 R4 isolated narrative reader A

2026-10-22 UTC. **Official narrative HOLD: 10/13 YES**, with required NO on `payoffs`, `no_recap`, and `no_detour`. I read only the frozen R4 `brief.md`, `script.md`, `video.json`, and the official thirteen-question narration payload. This is a story-shape vote, not a historical source or native-media review; I did not edit the creative files or use paid media.

| Input | SHA-256 |
| --- | --- |
| `brief.md` | `a81dcaa8a7feb3f2a75259bda56ed729480f7e27bd9487e4128d8791133df0ef` |
| `video.json` | `9a76f8880c75a04ef1322ac7264323ffb92b7dd8e648a1ffa992212f4c7d72a6` |
| `script.md` | `c677b03f9c45c8f4d3d788d73381253e4bb574cb9e420c136b8761cbb9658650` |

The exact [thirteen answers](r4-isolated-blind-a.answers.json) have SHA-256 `93bf4a74471d4dc8b943d835e531c4822044795a97dbff600a9f46a1876f524c`. Running `narrative --slug curio-s61 --answers docs/videos/curio-s61/review/r4-isolated-blind-a.answers.json --workdir /tmp/s61-r4-blind-a-official --json` produced [official bound record](r4-isolated-blind-a.official-narrative.json) SHA-256 `082a28b542be8b42d7a8114077f013eb671d8f1d70dae3635f4acdd0641ab6e4`, exit 1; [stdout](r4-isolated-blind-a.stdout.json), [stderr](r4-isolated-blind-a.stderr.txt), and [exit](r4-isolated-blind-a.exit.txt) are retained. Binding: narrative `4c030902579953d3`, script-check `573f1802b84c6660874bc5663e1b8be47431acc870f48e5a5c97f891a2a1c67a`, panel rules `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`, panel narration `8a9bf2a52bbe01d79e66886140b599531d2e6f8f731421c758b99fab0f16a8f5`. The creative file hashes were rechecked after the vote and did not change.

## Required NOs

- `payoffs`: [s61004] asks whether someone will **meet injured evacuees** moving to open ground. Its distant listed answer [s61081] says the army put up white tents so people who reached the Common had a place to stop. It neither names injured people nor says who received them; the question's concrete object is lost without a callback.
- `no_recap`: [s61022] establishes insufficient warning to citizens; [s61023] says people did not know the cargo, then [s61024] and [s61025] each repeat “沒有充分示警” in adjacent lines without a new result or explicit callback. The same warning shortfall is said multiple times.
- `no_detour`: after [s61066] delivers the all-clear, [s61069] through [s61086] spends about a minute on repeated ruin searches, area assignments, tents, churches, repaired buildings, and neighbor houses. Those facts show disaster relief, but the block does not advance the film's question of why the second alarm sounded or whether that second blast occurred; [s61091] later reopens that question.

The remaining ten questions received YES with cited lines in the answer JSON. In particular, the chapter seams now connect through actual event or question-answer pairs, and the opening does not reveal [s61095] before the final chapter. A second reader must vote independently on the same frozen script before the official per-question merge.
