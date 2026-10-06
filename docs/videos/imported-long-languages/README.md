# Continue the six imported long videos

The season-one cuts were imported through `tools/video/import`, which submitted
their finished media without creating a standard rendering project. This isolated
adapter recovers the existing script and timing so the owner's selected languages
can be made and submitted. It never replaces or renders the approved Chinese cut.

The six allowed slugs are `ai-real-world-01-image-trust`,
`ai-real-world-02-confident-errors`, `ai-real-world-03-machine-internet`,
`ai-real-world-04-tasks-and-jobs`, `ai-real-world-05-uneven-abilities`, and
`ai-real-world-06-digital-yesman`. Episode 01 uses the original approved cut; a
separately authored opening revision must obtain its own review before adoption.

After an owner-approved bookend renewal, the original batch deliberately fails its final
SHA fence. Use `prepareRenewedBatch` exported by `runner.mjs` with the original portable
manifest, fresh `readRemote`, `{slug,workdir}` handoff sources and a new separate output.
Each source must contain a `renewal-language-source.json` and a real subtitle-verified
script/body timing adapter produced by `tools/video/review/renewal-handoff.mjs`.
Preparation preserves the original batch and its paid worksheets/uncertain receipts,
archives the previous progress and replaced runtime, freezes the current runtime and
pins the new final/source files. It leaves STOP in place. Inspect previous paid requests
before explicitly continuing; preparation authorizes no translation or dub retry.

The renewed base publish review must approve the exact source contract's metadata SHA
before any language review is sent. A base-only package can retain unfinished selected
languages as pending. The runner validates the real source contract before every native
command and binds cumulative language manifests to that base publish, new final and
branding. Captions and chapters use the new intro offset. A lost language POST answer
is journaled and never automatically resubmitted. Source contracts do not stand in for
original TTS/checks or claim that a planned target voice narrated the retained Chinese cut.

## Inputs and preparation

Media stays outside Git. `preflight.mjs` reads the paired site's current reviews,
matches the latest valid final review to each imported MP4, and saves only the
relevant state. It does not print or copy the video tool credential.

```text
node docs/videos/imported-long-languages/preflight.mjs --imports IMPORT_DIR --out RECEIPT_DIR
node docs/videos/imported-long-languages/prepare.mjs --source-season SEASON_DIR --import-base IMPORT_DIR --output NEW_BATCH_DIR --dry-run
node docs/videos/imported-long-languages/prepare.mjs --source-season SEASON_DIR --import-base IMPORT_DIR --output NEW_BATCH_DIR
```

Preparation verifies the six frozen original cuts, source sentences, original WAV
sample counts, captions and timing. It copies the inputs into an isolated portable
bundle and creates a language-only script/timeline adapter. Absolute original
timing endpoints are mapped onto the tool's 30-fps timing grid; the original MP4
keeps its 24-fps video and Hanhan narration. The adapter voice config is the target
Gemini dub voice, not a claim about how the Chinese narration was made.

No `checks.json` or fabricated approval is created. The runner pulls the real
hash-bound final approval and checks it again before every submission. Source,
prepared timing, script, lexicon and original media hashes remain pinned.

## Run and resume

```text
node docs/videos/imported-long-languages/runner.mjs --manifest NEW_BATCH_DIR/manifest.json --dry-run
node docs/videos/imported-long-languages/runner.mjs --manifest NEW_BATCH_DIR/manifest.json --phase all --max-units 100 --apply
```

Dry-run is the default. `--phase translations` makes metadata and captions;
`--phase dubs` continues existing translations' selected dub tracks. `all` handles
both, visiting the six projects in rounds. Progress, API receipts and events live
beside the manifest. Reuse that manifest to resume instead of preparing over it.

Each successful batch contains the cumulative ready parts so a new pending review
cannot discard another language. A dub is ready only after a complete audio check,
with a receipt bound to its exact track, translation and clip hashes. A skipped or
unchecked dub cannot supply the caption timing. Existing uploaded tracks keep
their state when their bytes are unchanged.

The runner stops for changed final approval or language choices, invalid source
hashes, credentials or quota problems. It does not run the general automation
loop, start new videos, tidy media, change owner choices, or call YouTube. A STOP
file in the isolated work base stops it between units. Inspect an abandoned
`runner.lock` and confirm no process remains before removing that specific lock.

## Portable worker job

`package-runtime.mjs --manifest NEW_BATCH_DIR/manifest.json` freezes the tested
video tools and skill references inside the bundle's root. Its receipt records
every copied runtime file hash. This command is for an initial batch whose runtime
does not yet exist; it resolves a portable manifest through `relative_paths.root`.
A renewed batch prepared with `prepareRenewedBatch` already includes the reviewed
runtime and new receipt, with previous runtime bytes preserved separately, so do
not run the initial runtime command over it. On the host, use a separate one-shot container from
the existing video-worker image, the existing paired home volume, and a private
batch subdirectory of the work volume. The container can resolve its dependencies
through a `node_modules` symlink to `/opt/mokaair/node_modules`; no credentials are
copied into the bundle. The regular worker has no `auto.json` at the batch parent
and does not adopt this job.

For subscription stages on that host, explicitly set both
`MOKAAIR_SITE=http://web:3000` and
`VIDEO_LANGUAGE_API_ORIGIN=http://api:8000`. Only model-stage POSTs use the
existing internal API directly, with the same token permissions. This avoids the
web relay's 295-second deadline and uses a bounded 1,020-second native HTTP
request. Other origins are rejected; other routes use their existing transport.
POST requests are not automatically retried because a timeout can lose the answer
after the model has already completed.
The runner also writes `language-stage-journal.json` before each subscription-stage
dispatch. It binds the exact request to the final/source and batch namespace,
persists successful answers before returning them to automation, and reuses those
answers after restart. A dispatch left running or without a confirmed result holds
the project across later invocations. Preserve that journal and inspect the existing
result; removing a lock or restarting the runner does not authorize another paid call.
Paid stage receipts flush the file and POSIX parent directory before dispatch or
return. In the approved-final source mode, each translator/reviewer entry checks
STOP and freshly verifies the current source, owner choices and selected stage
configuration, including between two stages in the same invocation. Owner drift
holds the next stage while retaining the already paid answer unchanged.

An interrupted translated worksheet is preserved and checked against a fresh
source worksheet before reuse. It must still pass a fresh independent caption
review and the standard merge validation before becoming a ready translation.
Source or budget differences pause the project rather than overwrite that work.

## Acceptance

```text
node --test docs/videos/imported-long-languages/*.test.mjs
npm run check:tasks
```

Check the persisted backend language payload and attached hashes in addition to
the local progress file. `languages: approved` can mean a batch has only metadata,
captions, or explicitly skipped dubs. A ready dub stays pending until the owner
uploads it in Studio and confirms that action. Completing this job does not by
itself approve the separate upload package, publish a video, or establish human
audio acceptance.

`status.mjs --manifest NEW_BATCH_DIR/manifest.json --out RECEIPT.json` reads the
current review IDs, part states and attached hashes using the existing pairing.
Keep receipts outside Git; they are operational snapshots rather than approval.

For a changed, current human-approved final, use the independent
`prepareApprovedFinalBatch({manifestFile,handoffs,out,readRemote})` entry in
`runner.mjs`. It requires verified `approved-final-body-range` handoffs for the
existing six-video allowlist. Its current doc, lexicon, body timeline, approved
SRT/AAC evidence and exact final come from those handoffs. Every old file is
archived under `retained-source/original-batch`; old translations, worksheets,
uncertain paid calls and progress never appear in active resume paths. A fresh
namespace and reviewed runtime are frozen and the batch remains stopped.
The namespace binds local receipts; synchronous stages do not treat it as a remote
idempotency key. The mutable `languages.json` sync timestamp is excluded from source
inventory; the immutable contract and fresh site reads still pin owner choices.
Keep exact-lexicon child batches beneath the same parent directory. The new-source
runner holds `.approved-final-language-runner.lock` in that parent in addition to
its per-batch lock, so sibling producers run serially. Inspect both locks after a
crash; clearing them does not clear an unknown stage receipt.
Existing costs/unknown-call accounting remain charged and backend budgets stay
unchanged. The original `prepareRenewedBatch` source equality rule still applies
to unchanged retained-body renewals and rejects this new source mode.

Before allowing paid continuation, run the actual frozen native captions and
`dub --dry-run` against the current source, pull only the real final decision,
and prove changed final bytes fail. A disposable fit fixture can test dry-run
mechanics; it is not a ready translation and must stay outside the operational
batch. No script/audio/listening approval is inferred from a final decision.
The current-source runner wraps every native command's speech fetch with a local
intent/result journal for synthesis, transcription and audio judging. It saves the
exact wire request before dispatch and the complete raw response before the native
client reads it. A lost response, interrupted intent or corrupt receipt holds the
slug across routes and payloads; native retry loops receive a local 409 and cannot
send another paid POST. The one exception is the speech route's own 502
`upstream_unavailable` with that JSON code: the route never reached the API, so
nothing ran or was charged. The journal removes that intent and returns the answer
unchanged, and the native client's bounded retry goes out and is journaled like a
first answer. Every other answer that is not 2xx, including 503
`upstream_unavailable`, 504 `video_speech_answer_lost` and a gateway's HTML 502,
still holds the slug. This needs a site that serves #1272 (production does since
c12e159d0); an older site answers that 502 for a lost answer too. A batch keeps the
journal its runtime froze, so one frozen before this exception still holds the 502
until it is prepared again. Completed WAV/JSON responses replay across restarts with
their original billable header. Source, namespace, owner choice and fresh public
speech configuration must still match. Retained-body batches keep their original
transport. Applying any phase still requires fresh source/account/budget checks;
these local receipts do not authorize production activation or publication.
Offline `dub --dry-run` only validates the new source's timing and fit mechanics.
