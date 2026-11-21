# Curio S59 R9 — blind narrative reader A

## Verdict

**Fail:** 12 of 13 answers are yes; 11 of 12 required answers are yes. The required `no_detour` check is no. All 13 answers and one exact spoken quote per answer are in [answers.json](r9-blind-a/answers.json). I froze that ballot before running the official CLI.

The stretch at s59062–s59064 leaves the Paris question about whether the operator supplied the voice to answer a separate question about a duet's pitch with a clockwork drive. The script itself marks the return to the hand-cranked machine:

> [s59064] 杜蒙塞爾另記，規律的鐘錶機構讓二重唱重播得較好；可巴黎院士要查的，仍是那台手搖機。

The hand-speed limitation at s59060–s59061 can help explain why a retest might differ, but the duet and alternative drive do not add evidence about the suspected ventriloquism. That complete question-and-answer turn is a detour under panel question 13.

## Procedure and integrity

- Read only `script.md`, the fixed `NARRATIVE_PANEL` questions and instructions in `tools/video/core/narrative.mjs`, and the relevant narrative rules in `script-writing.md`. Did not read the brief, sources, claims, video file, author notes, or other readers' work.
- Script SHA-256 before and after: `6c28555d04104c676f76414479f038f426893f940a183e2518e3e9abac22cc09`.
- Frozen ballot SHA-256 before and after CLI: `e5e5165beba5c59d59216df86229f7ebb2f732432ba9aa5f6cb8d7becad9820f`.
- Ran `node tools/video/cli.mjs narrative --slug curio-s59 --answers docs/videos/curio-s59/review/r9-blind-a/answers.json --workdir /tmp/curio-s59-r9-blind-a.jhcjm6sl --json` in an isolated workdir. Its exit code was `1`, as expected for a failed required answer; stderr was empty. The CLI record says `passed: false` and `failed: ["no_detour"]`. Its internal `round: 1` counts runs in this fresh workdir, while this is the editorial R9 ballot.

## Artifacts

- [Frozen answers](r9-blind-a/answers.json)
- [Official narrative record](r9-blind-a/official-narrative-record.json)
- [CLI stdout](r9-blind-a/cli-stdout.json), [stderr](r9-blind-a/cli-stderr.txt), [exit code](r9-blind-a/cli-exit-code.txt), and [workdir](r9-blind-a/cli-workdir.txt)
