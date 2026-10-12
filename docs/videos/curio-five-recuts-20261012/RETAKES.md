# Bounded opening-audio repairs

`retake.mjs` works only on the five claimed opening fragments in the external
recut output root. It does not alter the published originals, upload a video,
change the specification, or claim owner listening. Run one operation at a time
per episode: it leases the common intro directory and all four locale directories.

Use these shared PowerShell arguments from the repository root:

```powershell
$repairArgs = @(
  '--spec', 'docs/videos/curio-five-recuts-20261012/intro-specs.json',
  '--sources', 'C:/Users/x8120/mokaair-work/curio-five-recuts-20261012/sources',
  '--out', 'C:/Users/x8120/mokaair-work/curio-five-recuts-20261012'
)
```

## Independent offline transcript

```powershell
node docs/videos/curio-five-recuts-20261012/retake.mjs second-opinion @repairArgs --slug curio-h02 --locale zh-TW --line intro01
node docs/videos/curio-five-recuts-20261012/retake.mjs second-opinion @repairArgs --slug curio-h02 --locale en --line intro06
node docs/videos/curio-five-recuts-20261012/retake.mjs second-opinion @repairArgs --slug curio-h03 --locale en --line intro04
```

The defaults use the existing `C:/Users/x8120/whisper/Scripts/python.exe` and
cached faster-whisper-small snapshot `536b0662742c02347bc0e980a01041f333bce120`.
Offline mode is required, hints are removed, and the recognizer receives only
the locale and WAV path. There is no download or paid API call. An optional
`--python` or `--model` selects another already-installed local runtime/model.

Each result records exact WAV SHA256, recognizer command, model-file hashes,
helper SHA256, raw stdout/stderr, intended/heard text, and the original Gemini
entry. The original complete check is copied into `second-opinion/`.
`check.json` and its flags remain unchanged. An existing result for the same WAV
is reused. The consumer rechecks the actual WAV and strict comparison through
`readSecondOpinionResolutions(directory, check)`.

Automatic equivalence allows case, punctuation, width and whitespace only, plus
conservative Chinese integer spelling in zh-TW. `一百一十` equals `110`; it does
not equal `111`, `1100`, or an omitted number. `銀光` and `螢光` differ. There is no
general phonetic or semantic exception.

## Explicitly reviewed Japanese pairs

The three U02 JA pairs were independently reviewed and accepted by the root
agent. They are an exact allowlist of the complete evidence package SHA256 and
three original WAV hashes. Changing either disqualifies the exception.
L08 JA intro05 has a separate explicitly reviewed package and exact WAV hash;
its accepted variants are the same readings of ひも/紐, 付けた/つけた and
野球帽/野球棒. This does not add a general Japanese homophone rule.

```powershell
$jaEvidence = 'C:/Users/x8120/mokaair-work/curio-five-recuts-20261012/curio-u02/intro/ja/independent-review-20261012/evidence.json'
node docs/videos/curio-five-recuts-20261012/retake.mjs reviewed-homophone @repairArgs --slug curio-u02 --locale ja --line intro02 --evidence $jaEvidence
node docs/videos/curio-five-recuts-20261012/retake.mjs reviewed-homophone @repairArgs --slug curio-u02 --locale ja --line intro05 --evidence $jaEvidence
node docs/videos/curio-five-recuts-20261012/retake.mjs reviewed-homophone @repairArgs --slug curio-u02 --locale ja --line intro06 --evidence $jaEvidence
node docs/videos/curio-five-recuts-20261012/retake.mjs reviewed-homophone @repairArgs --slug curio-l08 --locale ja --line intro05 --evidence C:/Users/x8120/mokaair-work/curio-five-recuts-20261012/curio-l08/intro/ja/independent-review-20261012/evidence.json
```

The embedded review preserves canonical kana and the reason for each exact
transcript pair. It is linguistic comparison of independent transcripts, not
owner playback or phoneme-level forced alignment. The original Gemini flags
remain available in the current check and its archived snapshot.

## One new take for one flagged line

```powershell
node docs/videos/curio-five-recuts-20261012/retake.mjs retake @repairArgs --slug curio-u02 --locale zh-TW --line intro05
node docs/videos/curio-five-recuts-20261012/retake.mjs retake @repairArgs --slug curio-h03 --locale ja --line intro03
node docs/videos/curio-five-recuts-20261012/retake.mjs retake @repairArgs --slug curio-h03 --locale ja --line intro05
node docs/videos/curio-five-recuts-20261012/retake.mjs retake @repairArgs --slug curio-h01 --locale en --line intro04
```

These commands keep the same text, original source voice and request body. Each
requires a current failed check bound to the exact current WAV and receipt.
At most two new takes are allowed per line. A line with an accepted independent
transcript cannot be repurchased through this utility.

Before the request, `intro/retakes/<locale>-<line>/attempt-1/before/` preserves the
old WAV, all available locale receipts/checks/timelines/narrations/captions, and
the shared timeline. Each attempt has its own request-hashed speech journal.
The client receives `attempts: 1`. An unknown outcome remains held across runs;
rerunning cannot open a new attempt to bypass that hold. Confirmed answers are
saved as a candidate WAV and receipt before committing to the current track.
Partially committed operations accept only their recorded before/after bytes.

A successful replacement sets the track receipt `aligned: false`, invalidates
shared duration/padding approval, and leaves the previous check flags in place.
After completing the intended retakes for one episode, realign all four tracks
and recheck all four. The unchanged clip hashes reuse their transcript cache.

```powershell
node docs/videos/curio-five-recuts-20261012/speech.mjs align @repairArgs --slug curio-u02
node docs/videos/curio-five-recuts-20261012/speech.mjs check @repairArgs --slug curio-u02
```

Substitute the episode slug as needed. If the same-text retake still fails,
review the exact new clip before deciding on the second bounded attempt. This
utility does not support changing `say`, migrating an opening identity, or
deleting/forgetting an uncertain paid journal.

## H03 Japanese pronunciation revision

The first same-text replacements for H03 JA intro03 and intro05 still failed.
The separately reviewed second revision preserves every visible caption and
changes only two `say` fields: `クリク` is spoken as `くりく`; `八千万本` is
spoken as `はっせんまんぼん` (80,000,000 trees). The original specs file remains
unchanged so previously started renders retain their source binding.

```powershell
node docs/videos/curio-five-recuts-20261012/prepare-h03-revision.mjs --old-spec docs/videos/curio-five-recuts-20261012/intro-specs.json --new-spec docs/videos/curio-five-recuts-20261012/h03-pronunciation-specs.json --sources C:/Users/x8120/mokaair-work/curio-five-recuts-20261012/sources --out C:/Users/x8120/mokaair-work/curio-five-recuts-20261012
```

The helper makes no paid request. It verifies that the two first retakes have
current failed checks, and that neither has already had a second retake. It
copies and hashes the complete existing intro tree into
`curio-h03/intro-revisions/revision-1/`, prepares revision two separately, and
installs it under continuous common and four-locale leases. The two old current
WAVs are removed only after the verified history copy. Every other raw take and
check entry is retained. All four receipt/check identities are explicitly bound
to the new spec; only Japanese identity changes. Shared QA remains invalidated.

Its readback must report exactly `ja/intro03` and `ja/intro05` pending. These are
the second and final extra takes for their lines. `intro/RETAKES_DISABLED` stops
the retake utility from making further purchases for H03. A partially installed
revision can resume only from its recorded before/after bytes; an interrupted
staging copy fails closed for inspection.

Use the revised spec for the subsequent H03 plan, synthesis, alignment, checks,
and assembly. Other episodes continue to use the original specs.

```powershell
$h03Args = @('--spec', 'docs/videos/curio-five-recuts-20261012/h03-pronunciation-specs.json', '--sources', 'C:/Users/x8120/mokaair-work/curio-five-recuts-20261012/sources', '--out', 'C:/Users/x8120/mokaair-work/curio-five-recuts-20261012', '--slug', 'curio-h03')
node docs/videos/curio-five-recuts-20261012/speech.mjs plan @h03Args
node docs/videos/curio-five-recuts-20261012/speech.mjs synthesize @h03Args --locale ja
node docs/videos/curio-five-recuts-20261012/speech.mjs align @h03Args
node docs/videos/curio-five-recuts-20261012/speech.mjs check @h03Args
```

## L08 original-language wording revision

The first same-text replacement for zh-TW intro07 still pronounced the name
incorrectly. The independently reviewed, source-equivalent replacement is
`多年後，其中一位老先生還說，後悔把這件事告訴大家。` The full source attributes
that regret to Doug; this wording retains the attribution to one of the two men
without adding a fact. The other seven opening lines and all dubbed scripts stay
unchanged. It uses a separate specs file; the original and H03 files stay intact.

```powershell
node docs/videos/curio-five-recuts-20261012/prepare-l08-revision.mjs --old-spec docs/videos/curio-five-recuts-20261012/intro-specs.json --new-spec docs/videos/curio-five-recuts-20261012/l08-wording-specs.json --sources C:/Users/x8120/mokaair-work/curio-five-recuts-20261012/sources --out C:/Users/x8120/mokaair-work/curio-five-recuts-20261012
$l08Args = @('--spec', 'docs/videos/curio-five-recuts-20261012/l08-wording-specs.json', '--sources', 'C:/Users/x8120/mokaair-work/curio-five-recuts-20261012/sources', '--out', 'C:/Users/x8120/mokaair-work/curio-five-recuts-20261012', '--slug', 'curio-l08')
node docs/videos/curio-five-recuts-20261012/speech.mjs plan @l08Args
node docs/videos/curio-five-recuts-20261012/speech.mjs synthesize @l08Args --locale zh-TW
node docs/videos/curio-five-recuts-20261012/speech.mjs align @l08Args
node docs/videos/curio-five-recuts-20261012/speech.mjs check @l08Args
```

Preparation archives the whole current intro tree and must expose exactly one
pending clip, `zh-TW/intro07`. All other raw clips are reused. The previous zh-TW
independent-review index is preserved in history and removed from the current
revision. Japanese and Korean evidence/index bytes remain unchanged, with their
unchanged source identities. This is the second and final extra take for this
line; `RETAKES_DISABLED` prevents further retakes. Assembly for L08 must receive
`l08-wording-specs.json` through its `--specs` argument.

## Offline verification

```powershell
node --check docs/videos/curio-five-recuts-20261012/retake.mjs
node --test docs/videos/curio-five-recuts-20261012/retake.test.mjs
node --test docs/videos/curio-five-recuts-20261012/prepare-h03-revision.test.mjs
node --test docs/videos/curio-five-recuts-20261012/prepare-l08-revision.test.mjs
```

The five offline tests cover:

1. Strict numeral preservation, wrong Chinese phonemes, Japanese alternatives,
   and English punctuation/case equivalence.
2. Model/command/WAV-bound independent evidence, unchanged original check,
   reuse without another transcription, and stale-WAV rejection.
3. Original-media history, same request/voice, invalidated QA, committed-resume
   idempotence, and the maximum of two new takes.
4. An uncertain POST held across invocations with exactly one mock dispatch.
5. Wrong flagged SHA and a competing live locale lease stopping before speech.

All tests use temporary local fixtures and mock speech/model calls; they do not
read credentials, contact the speech service, or claim audio acceptance.
The three revision tests additionally reject changes outside the exact two say
fields, verify complete history and unchanged raw WAVs with exactly two pending
requests and idempotent preparation, and refuse a revision after a prior second
retake.
The three L08 revision tests apply the same checks to its one exact wording
change, and additionally prove that old zh-TW resolution is removed while the
other locale review indices remain byte-identical.
