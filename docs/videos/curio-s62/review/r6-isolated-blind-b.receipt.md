# S62 R6 isolated blind reader B

I verified the official 13-question panel SHA-256, read that panel, verified `script.md` SHA-256, then read that script. Before freezing the raw ballot I read no other file, brief, claim, video, earlier review, ballot, CLI, or schema. The frozen ballot is JSON stored as `.raw.md`; it has never been edited after the freeze.

- Official panel SHA-256: `15cfd34356840ae8036c91bc9d8b29f210be52aa761f28379a2bd9ed263fa5ad`.
- `script.md` SHA-256 before reading and after binding: `0816b0a91b5b4e22571db7cf04b350b121dd56e364a57637f228a1d3f9d8a3c3`.
- Frozen raw ballot SHA-256: `068cd8726af7bb248f6c95ce7a9c7034f2b3fb865edf348f67dcbebcdadd6a71`; the submitted `.answers.json` is byte identical.
- Official bound record SHA-256: `2beb4bae504da43635fafdd123aa85c5c342652617db43acbb0ceb8c2c1696c3`.
- `video.json` SHA-256 after freeze: `9551bab89a03d91dc29afd103bdc383541fde1b10d8fb3b7de0eb218cbb6a7ad`.
- Official record narrative hash: `12dee2d6e454e303`; script hash: `f16660b0bf161c784beeb4bc4d2a171226566476a7c6e891519c3ec231ed2d07`.
- Official panel rules SHA-256: `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`; rendered narration SHA-256: `f2c9770aff87001890c29de3e1863152f2f7f0178f7f4296b3128efc2619fc38`.
- Verdict: **12/13 Yes** (required **11/12 Yes**, optional **1/1 Yes**), **FAIL**. Exact No ID: `no_recap`.

The opening says the next night was clouded (`[s62004]`). The body says January 9 was clouded again (`[s62041]`) without naming that earlier mention as a callback. That repeats the same observed fact. The raw ballot quotes `[s62041]` as its No evidence.

After freezing the ballot, I generated the current official panel and checked that all 13 question IDs and texts matched the frozen panel and every raw evidence quote matched its cited official narration line. I then ran `node tools/video/cli.mjs narrative --slug curio-s62 --answers docs/videos/curio-s62/review/r6-isolated-blind-b.answers.json --workdir /tmp/curio-s62-r6-isolated-blind-b --json` in a work directory that did not exist beforehand. The official CLI wrote round 1 there; exit code 1 was expected for the required No. Its bound answers are identical to the raw ballot. CLI stdout, stderr, status, and the binding were copied under this review prefix. I did not change the script, commit, or push.
