# Route B reviewed bundle compiler

`prepare_route_b_bundle.py` turns a reviewed Route B batch (agent translation, one
independent reviewer per locale, content PR merged) into the schema-1 bundle that
`publish_bundle.py` already verifies and publishes through its durable journal. It
exists because a dry-run followed by a bare `guides-import --publish` has no journal and
cannot close a source change that lands between the two commands, while
`assemble_bundle.py` needs Route A job artifacts (`receipt.json`, `review.json`,
`source.json`) that a Route B batch never had. The compiler does not invent those
artifacts and is not a second writer: the only writer stays `publish_bundle.py`.

What it never does: open a database, contact the production host, write the
repository's packs, public images or `publish_holds.json`, write inside the candidate,
or authorize anything. A compiled bundle is an input for review, nothing more.

## Inputs

Each input is a file whose SHA-256 you pass on the command line. The compiler hashes
the exact bytes it then parses, so a value written inside a file never vouches for that
file. All JSON is strict UTF-8; a repeated key is refused.

### Candidate (`route-b-candidate-v1`)

A frozen copy of the reviewed content, built from the merged Git blobs, outside the
repository:

```text
<CANDIDATE>/candidate-manifest.json
<CANDIDATE>/packs/<slug>.json                  # the full five-language ArticlePack
<CANDIDATE>/public/guides/<slug>/<name>.<ext>  # every image the reviewed documents use
```

```json
{
  "schema": "route-b-candidate-v1",
  "source_git_commit": "<40-hex commit the blobs came from>",
  "articles": [{"slug": "<slug>", "pack_path": "packs/<slug>.json", "pack_sha256": "<hex>"}],
  "assets": [{"path": "public/guides/<slug>/<name>.<ext>", "sha256": "<hex>"}]
}
```

Every listed pack and image is re-hashed, selected or not. Paths must have exactly these
shapes; `..`, absolute paths, backslashes and symbolic links are refused. A candidate may
hold several waves; the selection decides what ships.

### Review (`route-b-review-v1`)

One entry per reviewed slug and locale, bound to hashes rather than to files:

```json
{
  "schema": "route-b-review-v1",
  "evidence_sha256": "<hex of the private evidence: correction lists, renders>",
  "targets": [
    {
      "slug": "<slug>",
      "locale": "en",
      "status": "PASS",
      "translator": "<who translated or applied corrections>",
      "reviewer": "<someone else>",
      "reviewed_at": "2026-09-29T05:00:00+00:00",
      "source_sha256": "<normalized document_hash of the source the translation used>",
      "document_sha256": "<normalized document_hash of the reviewed document>",
      "assets": {"/guides/<slug>/diagram-1-en.svg": "<hex>"},
      "checks": {"text": true, "visual": true, "glyph": true, "links": true},
      "open_findings": 0
    }
  ]
}
```

`document_sha256` and `source_sha256` use `app.guides.service.document_hash` over the
`GuideDocument`-normalized document, the definition the baseline and the publisher use.
`assets` lists every image the document references and, optionally, the same-stem SVG
master of a raster it references (`hero-en.svg` beside `hero-en.jpg`); nothing else.
Unresolved findings, including an open source-summary question like T2's, keep
`open_findings` above zero or keep the slug in `publish_holds.json`; either refuses.

### Baseline

The output of `build_baseline.py` from a fresh `export_snapshot.py` of the deployed
revision, unchanged. Each selected article must carry its database identity, article and
locale versions, draft and published hashes, normalized documents, `status`, metadata,
target lists and provenance, and every value must agree with the others (the compiler
recomputes `locale_work` and `locale_provenance`). A public API projection, as Route B's
translation step pins, has no identity or versions and is refused. Build the baseline
after the content PR is deployed: the publisher compares the deployed pack with the
bundle in any case, and a selected locale the repository already holds must then be the
reviewed document exactly.

## Running it

```bash
uv run --project apps/api python docs/article-localization/prepare_route_b_bundle.py \
  --candidate <CANDIDATE>/candidate-manifest.json --candidate-sha256 <SHA256> \
  --review <WORK>/review.json --review-sha256 <SHA256> \
  --baseline <WORK>/baseline.json --baseline-sha256 <SHA256> \
  --slug marketing-mix-models --slug brand-tone-vibe-marketing \
  --locale en --locale ja --locale ko --locale zh-CN \
  --output <WORK>/bundle-t1
```

The selection is every `--slug` times every `--locale`, at most twenty slugs. It may be
narrower than the review (one wave, or fewer locales) but never wider. Run one wave per
bundle; a different locale set per slug is a separate bundle.

It prints `{"status": "compiled", "manifest_sha256": ...}` and exits 0, or prints
`{"status": "refused", "reason": ...}` to stderr and exits 1. Reasons never contain
document text.

## Output

```text
<WORK>/bundle-t1/release-manifest.json      # schema 1, exactly as publish_bundle reads it
<WORK>/bundle-t1/route-b-provenance.json    # the separate receipt below
<WORK>/bundle-t1/packs/<slug>.json          # the candidate pack, natively re-serialized
<WORK>/bundle-t1/public/guides/<slug>/...   # only images the selected documents use
```

- Each article entry has `locales` = `publish_locales` = the selected locales, `hub:
  false`, no source corrections and no repository preservations.
- Images: what the selected documents reference, plus a reviewed same-stem SVG master.
  The source diagram, other locales' images and other waves' images stay out; the
  publisher refuses an unused asset in a targets-only bundle, while the full pack and its
  source images remain in the deployed repository.
- `route-b-provenance.json` records the manifest SHA-256, the three input pins, the
  candidate commit, the baseline commit and capture time, the hold list's hash, the
  compiler's own hash, and each target's translator, reviewer, review time, source and
  document hashes and images. It says `"authorizes_production": false`.
- The same inputs give byte-identical output, so a second person can recompile and
  compare the manifest SHA-256.
- The compiler writes into a hidden staging directory beside the output, runs
  `publish_bundle.verify_bundle` on it, and renames it into place only when that passes.
  A refusal at any point removes the staging directory: no manifest is left behind.
- The output must be a new directory outside the repository and outside the candidate.

## What it refuses

| Input | Refused when |
| --- | --- |
| Pins | A pin is missing, malformed or differs from the file; any candidate pack or image differs from its candidate hash |
| Paths | A candidate path is not `packs/<slug>.json` or `public/guides/<slug>/<name>.<ext>`, escapes the candidate, or is a symbolic link |
| Review | Status is not `PASS`; the reviewer is the translator; a check is not `true`; `open_findings` is not 0; the time is not ISO 8601 with a zone or is in the future |
| Stale review | Its `source_sha256` is not the baseline source: the source changed after review |
| Changed content | A selected document's hash differs from the review, an image differs from the review or from the baseline's copy, or an image exceeds 300 KB |
| Selection | A repeated slug or locale, an unknown locale, more than twenty slugs, a slug outside the candidate or baseline, or a slug×locale the review does not cover |
| Targets | The source locale is selected; the target already has a database row (draft or published) in the baseline; the target is not a baseline publication target; a repository copy of the target differs from the reviewed document |
| Source | No database identity (a public projection); missing or inconsistent fields; status other than `published` (hidden, expired, draft); `valid_until` in the past; the source locale has an unpublished edit or its hash differs from the pinned publication |
| Untouched text | The source or any other existing locale in the pack differs from the baseline; kind, destination, topics, expiry, `featured` or order differ |
| Gates | The slug is in `publish_holds.json`; the slug is a hub (`gemini-guide`, `claude-code-tutorials`, `ai-terms-index`); the pack sets `aliases` for a selected locale (the publisher writes documents only) |
| Output | The output exists, or lies inside the repository or the candidate |

Version 1 creates missing locales only. A correction to published text goes through
`source_correction.py` and Route A; replacing an existing locale, a hub and aliases are
outside this compiler.

## Handoff to the publisher

1. Review `release-manifest.json` and `route-b-provenance.json` together: the slugs,
   locales and images are exactly the approved wave, and the hashes match the review.
   Record the manifest SHA-256; every later step uses that one value.
2. Confirm the deployed revision contains the content PR, then take a fresh snapshot.
   If anything selected drifted from the baseline, rebuild the baseline and recompile.
3. In the deployed API environment, with the same bundle, baseline, manifest SHA-256,
   `--deployed-root`, actor and one durable state directory, run
   `publish_bundle.py ... dry-run`, then `drafts`, `publish-articles` and `publish-hubs`
   (`bundle-release.md` §5 in the `article-localization` skill has the full commands).
   Each phase re-verifies the bundle, the deployed pack and images, the live versions,
   hashes and visibility, and reads the deployed hold list again. A stop is resumed with
   the same bundle and state directory, never a new one.
4. A rerun after success writes nothing. A fresh baseline taken after publication lists
   the new locales as existing, so the compiler refuses to compile them again.

Compiling does not lift a hold and is not consent. Every production step still needs
the owner's explicit approval, a verified backup and the four-lock and hold rules in
`ops/release/README.md`.

## Tests

`test_prepare_route_b_bundle.py` uses synthetic packs, images, reviews and baselines
only. It covers deterministic output, acceptance by `verify_bundle`, exact wave
selection, every refusal above, failure after writing, and the CLI. Its database cases
compile against a real article, then run the actual output through all four publisher
phases: the source locale, root metadata and unselected locales stay unchanged, a replay
writes nothing, source drift stops the publisher, a lost response or a failure before
commit resumes exactly once, and a hold added after compiling still blocks publication.

```bash
uv run --project apps/api pytest -q -o asyncio_mode=auto docs/article-localization/test_prepare_route_b_bundle.py
RUN_INTEGRATION_TESTS=1 uv run --project apps/api pytest -q -o asyncio_mode=auto docs/article-localization/test_prepare_route_b_bundle.py
```

The PostgreSQL cases, including a second session holding the publisher's advisory lock
or the article row lock, skip without `RUN_INTEGRATION_TESTS=1` and an isolated
PostgreSQL; the `release-safety` job in `article-localization.yml` runs them. A skip is
not evidence. That CI service is not the deployed API image either: a same-image
isolated rehearsal, a fresh approved snapshot, a verified backup, the deployment and the
public browser acceptance stay separate release gates with their own tickets.
