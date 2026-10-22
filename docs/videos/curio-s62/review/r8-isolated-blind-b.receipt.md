# R8 isolated blind reader B — official narrative receipt

- Isolation: read only the official 13-question panel, then `script.md`, before freezing the raw 13-answer ballot in `/tmp/s62-r8-blind-b/raw.json`. No brief, sources, video, claims, earlier ballots, or episode summary informed the ballot.
- Panel SHA-256: `15cfd34356840ae8036c91bc9d8b29f210be52aa761f28379a2bd9ed263fa5ad`.
- Script SHA-256: `c638b0d28cfbf6b398cd3bb541160685403bf3936fcd1613bc958921623e4326`.
- Frozen raw ballot SHA-256: `3404319488f314caffc37307521afed23a9a8d8349fb6c7b2fd2156d468efc98`.
- Official command: `node tools/video/cli.mjs narrative --slug curio-s62 --answers /tmp/s62-r8-blind-b/raw.json --workdir /tmp/s62-r8-blind-b --json`.
- CLI exit: `0`; stdout recorded in `.cli-stdout.json`; stderr empty and recorded in `.cli-stderr.txt`.
- Verdict: **passed**, 13 of 13 yes, no failed or advisory checks, round 1. The bound official verdict is in `.official-narrative.json`.
- Bound record: `narrative_hash` `edc7d2005d74f93c`; `script_hash` `5a78e1e249ba70941f3426628946c07f0db2a0547112f88cc26395ccdeb673af`; `panel_rules_sha256` `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`; `panel_narration_sha256` `c55c979f774539c2932f18c417091b0804d6b40e569f276ccee180923ffbfe86`.
- No media or creative files edited. No commit made.
