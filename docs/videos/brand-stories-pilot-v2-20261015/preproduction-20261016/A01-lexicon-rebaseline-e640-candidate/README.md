# A01 80→81 lexicon rebaseline, 2026-10-17 — offline candidate, HOLD

This is a **new** candidate for the captured `e6403c824aac…` shared lexicon. The older
[`835e09df…` two-term candidate](../A01-lexicon-rebaseline-candidate/README.md)
and its review stay unchanged and cannot authorize this 23-term transition. This
directory only reads local files. It has no host, database, provider, install,
retry, STOP/LEASE or paid-work command. Every result keeps production on `HOLD`.

## Frozen before and after

- Historical A01 tip: exactly 80 links, tip index `c7ddb6b57966…`, source
  composite `cf39296d597d…`, manifest `ada7ff185978…`. The checked-in
  `A01-host-inspect-candidate` pins must remain byte-for-byte unchanged.
- Historical lexicon: `ebfa590a69b4…`, 295 terms, preserved in
  `A01-round10-candidate/evidence/round9-lexicon.json`.
- Host-origin 2026-10-17 read-only capture: tar SHA-256
  `02b8631af6133227088a86d6eae7bff0bd152aa2e72b48198cec30741e964499`;
  mounted lexicon `e6403c824aac13b4c0a1ae737e8a597a8bf60c353e9faf0cc4915c3214114a30`,
  318 terms. The capture and raw SQL/budget outputs are outside Git at
  `C:/Users/x8120/.codex/captures/A01-20261017-095816-2a72b1e1/`.
- Only 23 exact terms were added. No old term was removed or edited. The exact
  names and values are frozen in `EXPECTED_ADDITIONS`; several have non-null
  spoken forms. The 80-link inspector must reject the current capture for
  **only** `SOURCE_DRIFT_FROM_TIP`; all other A01 source hashes match the tip.

The local plan on that capture produced event ID
`lexicon-rebaseline-e6403c824aac13b4`, plan SHA-256
`b76ed8f0dc99ff392535dada601a599ba51fd0f5464aab39dcdc6cfdd6aef24f`,
and proposed after-source composite `90b82e2fa03bb850bd40519aea4d71780c5efd85d90b0d3ba7d9629700530ba2`.
It checked 126 scenes and 184 actual spoken lines from all six chapter files and
`video.json`. The added terms have zero runtime-matcher hits, and the existing
speech substitutions, glossary entries and unknown-term results are unchanged.
This is local byte analysis, not a production write or permission to make one.

## Run locally

All paths must be absolute local paths. The CLI fixes both real lexicon hashes
and the historical 80-link pins; its programmatic hash overrides exist for
synthetic fixtures and are not CLI options. An override is accepted only when
the snapshot root is below the OS temporary directory and contains the exact
`A01-LEXICON-E640-OFFLINE-FIXTURE.json` marker (`schema_version: 1`, A01 slug,
`synthetic_fixture: true`). An overridden 80→81 check requires that marker in
both roots. No production capture has or should have this marker.

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-lexicon-rebaseline-e640-candidate/rebaseline.mjs `
  --snapshot C:\path\to\immutable-80-event-capture `
  --old-lexicon C:\path\to\round9-lexicon.json
```

`--prepare` requires **fresh external raw bytes** for an independent review
and an owner-authorized record receipt. Both must bind this candidate ID,
exact plan SHA, exact before/after source and lexicon hashes, and all 23
additions. The receipt additionally binds the review-byte SHA and records
`record_only: true` and `lexicon_file_writes: 0`. It must identify a different
operator and a new owner approval reference. Names or reference strings are
not authentication; review and authorization must be verified outside this
tool. Do not fabricate a PASS or reuse the two-term review/approval. No real
review or receipt has been supplied, so no 81st event bytes are approved.

After a separately reviewed, authorized append, `--before <80-root> --after
<81-root> --old-lexicon <file>` can compare two independently captured immutable
roots. It requires exactly the old 80 events plus the proposed event, exact
review/receipt/index/manifest bytes, unchanged old audit and receipt bytes,
and the fixed new source. It still reports `LOCAL_81_EVENT_TRANSITION_PASS`
with `production_status: HOLD`; it cannot prove host origin, freshness or an
exclusive writer window. The older `A01-host-transition-export-candidate`
imports the two-term candidate and **cannot** validate this transition;
a separate reviewed e640 readback binding is needed before host adoption.

## Required independent checks before any host write

1. Authenticate the capture provenance, old lexicon anchor and complete
   80-link chain. Recheck the mounted lexicon and all source hashes immediately
   before a proposed append. A later shared-lexicon change invalidates this plan.
2. Independently inspect each of the 23 exact additions and its spoken value.
   Confirm the deployed TTS/glossary matcher and all 184 A01 spoken lines have
   no semantic change; the local repository matcher alone does not prove the
   older deployed worker's behavior.
3. Review the new plan and append adapter separately. Require an exclusive
   writer window covering both the shared lexicon and A01 audit paths, a
   crash/partial-write and rollback plan, fresh STOP/LEASE/job/budget preflight,
   exact owner approval for named host paths, and a second full host readback.
4. Keep the real script/narrative approval, exact-file review receipt, worker
   race repair, media QA and the US$25 paid cap as separate gates. This
   candidate neither clears the historical uncertain job nor starts A01,
   B18 or the five later films.

## Verification

```powershell
node --check docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-lexicon-rebaseline-e640-candidate/rebaseline.mjs
node --test docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-lexicon-rebaseline-e640-candidate/rebaseline.test.mjs
```

The synthetic tests exercise the 80→81 chain, old-history tampering, review
binding, exact 23-term delta, each added term's runtime match and interrupted
append. Fixture reviews and approvals are synthetic and are never production
evidence.
