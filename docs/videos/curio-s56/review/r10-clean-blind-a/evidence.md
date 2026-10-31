# S56 R10 clean blind narrative reader A

- Frozen input: `docs/videos/curio-s56/script.md` SHA-256 `286b7d50bc21ee8c8c5f61d99a3744f988ca1cbdac2c80bef05237a74f585153` (verified before the ballot and after the CLI run).
- Frozen 13-answer ballot: `ballot.json` SHA-256 `5d1db05ae8ae82f65915710545ff543cde0b3cf09fbe6aab5d59a9d3b3c8ada2`. Each answer cites a scene ID and exact spoken line; all 13 quotations were checked against their scene blocks. The ballot was written before the official CLI run.
- Official result: 12 yes, 1 no; `passed: false`, required failure `no_recap`. CLI exit code `1`; stderr was empty. The unmodified CLI outputs are `cli.stdout.json`, `cli.stderr.txt`, and `cli.exit-code.txt`; its workdir record was copied to `narrative-record.json`.

## Deciding evidence

The later line `[s56174] 西岸大火隨後越河，與東岸新火連成一片。` restates the earlier `[s56079] 他寫，西岸大火後來過河，與東岸新起的火連成一片。` The nearby `[s56173]` calls back to the opening river, but the repeated fact was already stated in the body and adds no new result. I therefore answered `no_recap: no`. The other twelve checks were answered yes in the frozen ballot, with individual quotations there.

## Reproduction

```bash
NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/tmp/s56-r10-blind-a node tools/video/cli.mjs narrative --slug curio-s56 --answers /workspace/travel_scanner/docs/videos/curio-s56/review/r10-clean-blind-a/ballot.json --json
```

This was a script-only narrative read. No creative files or audio/Jev stages were changed or run.
