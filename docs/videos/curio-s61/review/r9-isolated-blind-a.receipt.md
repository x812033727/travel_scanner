# S61 R9 isolated blind reader A

Read order: official 13-question panel, then the complete `script.md`, then froze the raw ballot and its SHA-256 before reading the CLI or schema. No brief, source, video, claims, earlier reviews or ballots, or episode summary was read before the ballot froze.

- Panel SHA-256: `15cfd34356840ae8036c91bc9d8b29f210be52aa761f28379a2bd9ed263fa5ad`
- Script SHA-256: `e3f27c9da2b951fd744e9de48b2c64d665ef4f76cd6abaa4e323b43c5ebb9eb9`
- Raw ballot SHA-256: `b796935f2f96f75cd2e203adc9a8f5837548732b49e0667ebee5d6fa83bf3122`
- Result: **13/13 yes; passed true; CLI exit 0**. Failed required: none. Advisory: none.
- Official command: `node tools/video/cli.mjs narrative --slug curio-s61 --answers docs/videos/curio-s61/review/r9-isolated-blind-a.raw.json --workdir /tmp/s61-r9-blind-a --json`
- Original isolated record: `/tmp/s61-r9-blind-a/curio-s61/review/narrative.json`
- Bound record SHA-256: `6200e5439459844883e313f8dbc65020f0bdee2f0c3570e35c359edce6666b21`; `narrative_hash=905b9da092703d23`, `script_hash=d223d8285664b3408ab86e641dc0d548bf779c449e75c5d6258b4bf92506eda6`, `panel_rules_sha256=5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`, `panel_narration_sha256=0ad2b1316ce246f6d4508c3f0109db29ef7daa16b637271cb3087c98b561e923`, `round=1`.
- CLI stdout SHA-256: `4f56c58a7b86614aaaf384764de025aa1cb68d1e3a28892a988350e1e8a4ff91`; stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; exit file SHA-256: `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa`.

Artifacts: [raw ballot](r9-isolated-blind-a.raw.json), [bound record](r9-isolated-blind-a.bound.json), [CLI stdout](r9-isolated-blind-a.cli.stdout.json), [CLI stderr](r9-isolated-blind-a.cli.stderr.txt), and [CLI exit](r9-isolated-blind-a.cli.exit.txt). This is a narration-only blind vote; it does not assess sources, visuals, audio, or the finished video. No creative files were edited and no commit was made.
