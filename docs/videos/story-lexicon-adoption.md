# Adopt X10's manually composed story dictionary before first speech

`story-everyday-ebay-paypal-x10` was composed directly in `docs/videos/`, without the story worker's
`auto.json` or chapter files. Its `series.json` identifies a story, so TTS correctly requires an
immutable per-story dictionary. The worker's `story-lexicon-migrate` command requires genuine worker
state and must not be used for this episode. `story-lexicon-adopt` is limited to this slug and pins
the same genesis version that a new story would get: the current shared dictionary plus the plan's
`eBay` and `PayPal` names as `null` when absent.

The command needs the **actual media workbase** used for later TTS. The argument is the base, not
the slug directory; the command appends the slug. The base must already exist, be outside the repo,
and have no symlink in its path. The story's work directory must be absent or empty. A different,
empty base is not evidence that speech was never made elsewhere, so an independent operator must
check that history and explicitly attest to it in the review. The tool cannot prove that negative
from a single filesystem path.

## Review and command

```bash
# Read-only: prints every check, the exact source/snapshot hashes and an unconfirmed review template.
node tools/video/cli.mjs story-lexicon-adopt --slug story-everyday-ebay-paypal-x10 --workdir /absolute/real/media/base

# Save the template as a JSON file outside the story work directory, then fill only these fields:
#   confirmed_no_prior_speech: true   (after checking the actual media history)
#   independent: true
#   reviewer: an identifiable independent person or agent
#   reviewed_at: a past ISO 8601 timestamp with timezone
# Recheck the filled receipt and current bytes without writing:
node tools/video/cli.mjs story-lexicon-adopt --slug story-everyday-ebay-paypal-x10 --workdir /absolute/real/media/base --review /absolute/path/review.json

# Pin only after the report says allowed and the reviewer has checked its source hashes.
node tools/video/cli.mjs story-lexicon-adopt --slug story-everyday-ebay-paypal-x10 --workdir /absolute/real/media/base --review /absolute/path/review.json --apply
```

`--json` prints the same report as structured JSON. `--apply` requires `--review`; both the normal
and JSON dry runs write nothing. A changed `video.json`, `series.json`, shared dictionary, workbase
or review fails the exact-byte check. The receipt binds SHA-256 of both story documents, the shared
dictionary and proposed snapshot, the absolute workbase, and the reviewer's no-prior-speech decision.
The review template starts with `confirmed_no_prior_speech: false` and `independent: false`; it is
never silently approved.

Before either lease, and again under the project and shared-dictionary writer leases, the command
also requires: no pending lexicon transaction, no project/base `STOP`, no worker `auto.json` or
chapters, no recheck audit, no timeline, no `audio/` or `narration.wav`, no approvals, and no other
work files. The X10 `video.json` must name this exact slug; `series.json` must be a story with the
two plan names. It refuses other slugs. A successful apply publishes immutable version, event,
review and adoption records, selects `current.json`, reads back the strict chain and exact source
hashes, writes a committed work receipt, then clears both intents. The adoption record and work
receipt identify the reviewed manual origin. The shared dictionary and worker state stay unchanged.

The existing committed-transaction recovery handles a crash after the receipt. A crash before the
receipt leaves the intents in place and holds speech for operator review. Once the command reports
`already_pinned`, a rerun changes nothing. After pinning, `tts --dry-run` can plan with the strict
reader; synthesizing narration remains a separate paid production step.
