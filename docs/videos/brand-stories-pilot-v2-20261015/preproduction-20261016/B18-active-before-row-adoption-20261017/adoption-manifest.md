# B18 active-input adoption backup

2026-10-17. This directory holds exact pre-change bytes from the active pilot package before the independently reviewed B18 worker row and short review receipt were copied in. It is a local Git backup, not a production snapshot.

| Original active file | Backup file | Pre-change SHA-256 |
| --- | --- | --- |
| `episodes/B18.json` | `episodes-B18.json` | `2150ff1b5a3a25d99ffadbe617ee746e42c93b3e24ef814a64d05f8149b00565` |
| `episodes/reviews/B18.json` | `review-B18.json` | `3a7bb438fc9ad1717d2d7fd902a4b238d85804fa394328b54730ead05d986834` |
| `stories.json` | `stories.json` | `3a87dff10ed597c68b01588244e5bd3443dfa69af13d97fbd8e411a81d32cd01` |
| `README.md` | `README.md` | `55229ab3cec55e86e6141787f2eea943743e361d0ea6068b4c64081b5bb24683` |

The active A01 input file SHA-256 was `6cc831355e173a80f64e56eefdb1d1253621aba31aff472dad096006bbfd98b7`; it was not edited. The A01 object serialized from the previous and rebuilt `stories.json` is byte-equivalent (15,590 UTF-8 bytes under the same JSON serialization).

The adopted B18 input file SHA-256 is `209fb773139e96afd5a56f373b6f0843eca902f81b374c19bcd9bc8a4d78e3dd`, and its independent short receipt SHA-256 is `124b4bea3e08a14e5402370c678b8d53d7f61c6180db5e80c6d4aeff52278114`. The receipt binds canonical story SHA-256 `3c43dc0c0eccdb063cc1e62d756c48ce2a476c5bfe1a70b74799c8f3cfc475f1`. The new compiled two-row file SHA-256 is `07a71fc18c3aa12d426dcc1c9ecd30e59c150079a1e83d868b7024c09670c999` after each of two consecutive builds. No host import or media work is implied.

The historical `B18-worker-input-name-trim-candidate-20261017/build.mjs --check` asserts that the **active** B18 review is stale. That assertion was true before this adoption and is now false by design, so rerunning it against the changed active path exits 1. Its immutable candidate manifest still passes `manifest.mjs --check`. The current active pilot `build.mjs --draft` and twice-run `--write`, the 27 plan tests, and the API `check_story_file` pass; the historical candidate can be replayed only with the backed-up old review in an isolated checkout. Do not alter the pinned candidate or mistake this stale-review assertion for a failure of the adopted receipt.
