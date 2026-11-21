# Curio S59 R9 blind narrative reader B

- Input: `docs/videos/curio-s59/script.md` only, plus the fixed narrative panel and its script-writing rules.
- Script SHA256 before review: `6c28555d04104c676f76414479f038f426893f940a183e2518e3e9abac22cc09`.
- Raw ballot frozen before the official CLI: [answers.json](r9-blind-b/answers.json).
- Independent vote: **13 yes of 13**; all 12 required checks pass. The chapter-name check is advisory and also yes.

The opening puts Puskás at the Paris academy before it raises the ventriloquism doubt. Its later moments are left unresolved: Dumoncel's attempt, Edison's sketch, and the secretary-room retest. The body follows the talking machine from the imprinted-signal idea through its first playback and the Paris checks. The failed first attempt is paid off by Dumoncel's later explanation about his distance from the mouthpiece and his successful practice. The script marks its return to the opening demonstration, and its final question invites the viewer's own judgment without naming another video.

Closest calls: `s59011` pauses to distinguish Edison's later recollection from the Paris record, but it gives a source limitation rather than a chapter plan. `s59059`–`s59064` describe hand-crank speed and playback pitch; the passage explains why one successful playback would not settle the later retest, and `s59064` returns to the Paris hand-cranked machine. Neither changes my yes vote for `no_toc` or `no_detour`.

Official CLI: `node tools/video/cli.mjs narrative --slug curio-s59 --answers …/r9-blind-b/answers.json --workdir /tmp/curio-s59-r9-blind-b-cli --json`. It exited `0` and reported `passed: true`, `failed: []`, and `advisory: []`. The isolated workdir, stdout, stderr, exit code, and copied [official record](r9-blind-b/official-narrative-record.json) are saved beside the ballot.

Script SHA256 after the CLI: `6c28555d04104c676f76414479f038f426893f940a183e2518e3e9abac22cc09`. All 13 quoted evidence lines were checked against the script text and matched exactly.
