# S62 R5 isolated blind reader B

I verified the official 13-question panel and `script.md` in that order, read only those two files before freezing the raw ballot, then opened the repository's narrative CLI and schema. No brief, claims, `video.json`, source, prior review, or other ballot informed the raw answers. I did not edit the script.

- Panel SHA-256: `15cfd34356840ae8036c91bc9d8b29f210be52aa761f28379a2bd9ed263fa5ad`
- Script SHA-256: `2d92a72e535f03b53c70c3aa3b52c218c035c1ee53eb1ca82d3d0a802a6cc091`
- Video SHA-256, checked after freeze: `e7d14243eefff747d94ed2f28193ab93c0af97646b2ff55de935161c7643067a`
- Frozen raw ballot: `/tmp/curio-s62-r5-blind-b-raw.md` (SHA-256 `d4e5abc5c78a233c2b8da24fef4d096728a5343e988abf095d80c9a1fedbf569`)
- Submitted answers SHA-256: `0bc20b8be58ac448d4c4811c30756caaf33f2145af9f1443329de4620ca76400`
- Official bound record SHA-256: `0fb1fbed170ee98c0d11affd6ef5989029a6fc322c66aae305858e23a037b340`
- Official record narrative hash: `85c4d37cd19c407a`
- Official record script hash: `29c26e9fd8a5fbd1eb78459d7dadb1d8c3c1b533459b6934a2e2c080588ee5a7`
- Official record panel rules SHA-256: `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`
- Official record panel narration SHA-256: `086d3daad13a5416a1f409b57034213a876c480b252b9cc6701b97a407ff3f01`
- Score: **10/13 Yes**, required **9/12 Yes**, optional **1/1 Yes**. Verdict: **FAIL**.

Required No answers from the frozen ballot:

- `one_line` — `[s62026]` jumps to publication of the first-night diagram, then `[s62027]` returns to what Galileo thought that night.
- `payoffs` — `[s62045]` asks where the third January 10 point went and offers only Galileo's possible occultation guess; the script never clearly resolves that point's whereabouts.
- `no_recap` — `[s62058]` repeats `[s62057]`'s fact that the faint point appeared only hours later, without an explicit recall cue.

The official binding used `node tools/video/cli.mjs narrative --slug curio-s62 --answers docs/videos/curio-s62/review/r5-isolated-blind-b.answers.json --workdir /tmp/curio-s62-r5-isolated-blind-b --json`. The CLI wrote round 1 to the isolated workdir; its expected exit code was 1 for three required No votes. The bound record was copied to `r5-isolated-blind-b.official-narrative.json`, with CLI stdout, stderr, and status saved under this prefix. The official CLI's 13 question texts matched the frozen panel exactly. The script hash remained unchanged after binding.
