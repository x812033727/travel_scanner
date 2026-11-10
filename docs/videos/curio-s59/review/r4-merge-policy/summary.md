# S59 R4 — formal two-reader narrative OR merge and pre-media gate

2026-10-21 UTC. **Narrative PASS: 13/13 yes by the fixed OR rule. Pre-media policy HOLD: the independent source/claims audit passed, but the written-visual audit held `s59027`.** No creative file or paid media was changed by this merge.

| Frozen R4 input | SHA-256 |
| --- | --- |
| `research.md` | `d0077504f3dbe828363158a25c7e7dade955089f49dbb03a734893739e12467e` |
| `brief.md` | `9d68d7b4dad27f56b6dbc53f7890bc0db84590de3e445302f8f4836c286ac1e3` |
| `claims.md` | `e19a8aa75c7d61bbba54b4d747db3b7025ac34599964ac0c4c115fbacd8d8c0b` |
| `video.json` | `108db5d8ae5b540e396b1e9add3490c7ac8761e1aaa7dfd76b172edbadaba226` |
| `script.md` | `5b18eb40b5c3434599abbd939d3231fc30837e360bfaff0ea00d23cdca89cf48` |

Reader A's independently saved [raw ballot](raw-ballot-a.json) and [review](raw-review-a.md) were copied byte-for-byte from `../r4-blind-a/` after Reader B had fixed its own [raw ballot](raw-ballot-b.json) and [review](raw-review-b.md). The raw ballot hashes are respectively `62a38b963d75660afdc4a9c8c0bcb9e627f5a28dddad420bbea923d3639ee943` and `e19b677fa2c06b5786177efd6e5b548e4224222711ae87888da7a014be826e8b`. Both had 13 cited yes answers and no required or advisory no answers. Both original official receipts have the same panel-rules hash `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`, narration hash `8525c51f6baa78ff61793f954574f8ae26e2f3fa091d4b1eef9b8622a4a1b1fe`, script binding, and narrative binding.

The reproducible [merge runner](formal-merge.mjs) checks those input hashes, every cited quote against `video.json`, the official receipt bindings, and all five creative hashes before applying `mergePanelVerdicts`. Under the fixed OR rule, a cited yes from either reader passes a question; here **both** readers said yes for every question. The [merge audit](merge-audit.json) records each question's two-reader count, and [merged answers](merged-answers.json) preserve the official input format. Since A answered yes to all questions and is first in the merge order, the merged answers are byte-identical to A's raw ballot.

The runner invoked `node tools/video/cli.mjs narrative --slug curio-s59 --answers <merged-answers.json> --workdir <fresh /tmp directory> --json`. The independent official run exited **0** with `passed: true`, `failed: []`, `advisory: []`, and round 1. Its [CLI status](cli-status.json), [raw stdout](cli-stdout.json), [stderr](cli-stderr.txt), [exit code](cli-exit-code.txt), and [official narrative record](official-narrative-record.json) are archived. The official record SHA-256 is `2a9ecd16b5879e8169f77751430d69716fad7d36ff9853bef4bcdc4888e42d4a`; it is also byte-identical to A's receipt because the answers and round match. The runner verified all five creative hashes again after the CLI call.

The [pre-media policy gate](policy-gate.json) is **HOLD**. The frozen [independent source/written-visual audit](../r4-source-independent.md) (SHA-256 `6a90a86efe7553ee408f736fd814d44f87ff298eac71cdd288da057d154faef7`) finds source/claims **PASS**, but the `s59027` prompt asks an inventor to trace a groove with a **finger** while the spoken mechanism asks whether the groove drives a **needle/contact**. That is a written contradiction before generation. The gate blocks paid media pending a prompt-only correction and fresh written-visual review on the new `video.json` SHA. It is a local editorial pre-media decision, separate from later Jev, site approval, audio, and native-image checks. The R4 narrative result remains a record for these exact frozen bytes.
