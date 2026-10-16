# A01 80→81 transition and export gate — offline only, HOLD

This sibling candidate joins the exact, append-only lexicon event from
[`A01-lexicon-rebaseline-candidate`](../A01-lexicon-rebaseline-candidate/README.md)
to the database, budget, filesystem and release readback contract of
[`A01-host-export-candidate`](../A01-host-export-candidate/README.md). It reads
only caller-supplied local files. It has no host, database, browser, provider,
STOP/LEASE, installer, retry or paid-work command. A local PASS always reports
`production_status: HOLD`, `installation_allowed: false` and
`paid_work_allowed: false`.

The original 80-link [`inspect.mjs`](../A01-host-inspect-candidate/inspect.mjs)
remains unchanged and **must reject** the after snapshot at 81 links. This tool
does not reset an old pin, rewrite one of the 80 events, or count a made-up
reviewer/approval string as an authenticated human decision. The copied
readback validations in `inspect-transition-export.mjs` mirror the older
80-link exporter; changing either module requires its own review and tests.

## Inputs

All six paths must be absolute local paths. The production-shaped CLI uses the
historical 80-link pins and exact old/new shared-lexicon hashes already frozen
in the reviewed rebaseline candidate; any changed host bytes fail closed.

1. `--before`: a separately retained, complete immutable A01 snapshot with
   exactly the original 80 `story/recheck-audit/<event>/` directories. Its
   current shared lexicon may have the *one observed* drift, but the 80-link
   anchor, every historical index/evidence/receipt and tip must match the
   externally pinned original. This is not a repaired or repinned copy.
2. `--after`: a **different** immutable snapshot with those same 80 events plus
   exactly one proposed lexicon-rebaseline event and its record-only receipt.
   The source bytes must equal that 81st tip. The transition verifier checks
   exact proposed review, receipt, author manifest and index bytes, as well as
   all old history. The two snapshots must have separate capture roots.
3. `--old-lexicon`: the separately saved original shared lexicon bytes.
4. `--before-pins`: a separately recorded JSON pinset with exactly `id`,
   `links=80`, `install_receipt_sha256`, `tip_index_sha256`,
   `source_composite_sha256` and `archive_index_manifest_sha256`. Apart from
   `id`, every field must equal the checked-in historical 80-link pins. Do not
   calculate these pins from a copy after a failure.
5. `--after-pins`: an independently recorded JSON pinset with those six fields,
   `links=81`, plus `state_sha256`. The first six fields must equal the transition
   verifier's recalculation; `state_sha256` binds the next input's exact bytes.
6. `--state`: the sanitized readback JSON from the existing host-export contract.
   Its `archive` source, manifest and tip hashes must equal the 81-link result.
   The code checks the A01 series/episode/project, release hashes, STOP/LEASE
   record shape, journal and media inventory shape, every stage/media job,
   US$25 ledger arithmetic and media-budget links. It does not itself prove
   the caller's inventories are complete, fresh or truly from the host.

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-host-transition-export-candidate/inspect-transition-export.mjs `
  --before C:\path\to\immutable-80 `
  --after C:\path\to\immutable-81 `
  --old-lexicon C:\path\to\original-lexicon.json `
  --before-pins C:\path\to\before-pins.json `
  --after-pins C:\path\to\after-pins.json `
  --state C:\path\to\sanitized-state.json
```

Exit 0 is `LOCAL_TRANSITION_EXPORT_BINDING_ONLY`: only the supplied local bytes
agree. Any mismatch exits nonzero and lists a code. No input or output is
written by the inspector. Its programmatic `syntheticFixture`/lexicon-hash
overrides are reserved for marked roots under the OS temporary directory; the
CLI has no override flags.

## Local checks and operational boundary

```powershell
node --check docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-host-transition-export-candidate/inspect-transition-export.mjs
node --test docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-host-transition-export-candidate/inspect-transition-export.test.mjs
```

The synthetic tests exercise an exact 80→81 transition; old-inspector refusal;
altered old index/journal, altered new index/review/receipt/source, missing or
extra event and altered external pin; changed state archive, budget, media-job
link, STOP shape, inventory path, release hash and state file. Fixture review
and owner-reference strings are explicitly synthetic.

On 2026-10-17, the focused suite passed **6/6** under the repository-documented
bundled Node 24.19.0 (`node --check` also passed for both `.mjs` files). The
system Node 24.13.0 stalled during `fs.cpSync` on this Unicode worktree, as
documented in `dev-and-ci/references/local-env.md`; that terminated run is not
counted as a pass. The tests use one shared synthetic 80-event fixture.

**Production remains HOLD.** A fresh host-origin capture, complete independent
inventory, separate human review and owner-approved exact host paths are still
required. Existing worker paths have no shared lock covering both A01 audits
and the shared lexicon; a private fixture lock or point-in-time STOP/LEASE read
does not establish an exclusive writer window. The active #1528 per-story
lexicon format has no worker/TTS migration or A01 host adoption yet. Any
different lexicon bytes, 82nd event or alternate migration layout require a
new reviewed transition rather than relaxing this exact gate. Round19's offline
editorial PASS does not install its chapters, clear historical narrative FAIL,
create `story/reviews/script-review.json`, generate media, authorize B18/five
films, or publish to YouTube.
