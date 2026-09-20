# Article localization work pipeline

`pipeline.py` stages full translations and translated SVG text using the installed,
ChatGPT-authenticated Codex CLI. It does not write article packs or public images,
import articles, or publish them. Use the API Python environment so the real
`GuideDocument` validator is available. `render.mjs` uses the repository's
Playwright and Sharp dependencies.

```powershell
uv run --project apps/api python tools/article-localization/pipeline.py prepare --batch batch-001 --include-existing
uv run --project apps/api python tools/article-localization/pipeline.py run --batch batch-001 --include-existing --workers 3
uv run --project apps/api python tools/article-localization/pipeline.py status --batch batch-001 --include-existing
node tools/article-localization/render.mjs --job docs/article-localization/work/gemini-markdown-basics/en
python tools/article-localization/test_pipeline.py
node --test tools/article-localization/artifact-integrity.test.mjs
```

Each invocation selects exactly one baseline batch or an explicit comma-separated
`--slugs` list of at most 20 source articles. `--locales en,ja,ko,zh-CN` narrows the
target languages. Defaults are all five languages and one worker; the maximum is
three workers. `--include-existing` creates image-only jobs for existing translated
bodies, preserving their prose. The original source locale is not unnecessarily
retranslated. Missing SVG companions are recorded for manual raster review.

The baseline must provide `articles` and `batches`. An article uses `slug`,
`source_locale`, `source_document`, `source_sha256`, `pack_path`, `pack_sha256`,
`missing_locales`, `locale_documents`, `status`, and optional `database`. A batch
uses `id` and an explicit `slugs` list. Document SHA-256 matches the application's
canonical JSON hash; file hashes cover actual bytes. The default baseline is
`docs/article-localization/baseline.json`.

## Resume, stop, and failure handling

Re-running a batch skips validated documents after rechecking hashes. Prepared
jobs retain their original inputs; a conflicting new baseline is refused instead
of overwriting work. Exclusive `running.lock` files prevent overlapping workers.
After a crashed process, verify the PID in that lock is no longer active before
removing that individual lock. Then explicitly reset the affected job.

Create `docs/article-localization/work/STOP` to stop starting jobs. Active CLI
calls finish and preserve their results. Remove that exact file to allow a later
run. An alternate sentinel can be selected with `--stop-file`.

Quota and authentication failures stop queued jobs and are never automatically
retried. Default transport retries are also zero. `--retries 1` or `2` permits
only explicitly recognized connection/502/503 failures; content, schema, quota,
and unknown failures still require review. No setting bypasses service limits.
The tool checks ChatGPT login and rejects configured API-key/custom providers.
Configured MCP servers are disabled only for the child invocation through the
CLI's dotted configuration override; global settings and credentials are intact.

```powershell
uv run --project apps/api python tools/article-localization/pipeline.py reset --slugs example-slug --locales en --reason "Resolved the recorded transport failure"
```

Reset stores the former receipt and reason. Do not reset a quota-blocked job until
the account limit has actually reset. To correct a failed translation without
another model call, edit only `translated-fields.json`, then run `materialize` for
that exact slug and locale. The next materialization reruns all field and schema
checks and records the edited field file hash. Source fields and attempt logs
must remain unchanged.

## Output and review contract

Each job lives at `docs/article-localization/work/<slug>/<locale>/`:

- `source.json`: immutable source document, fields, asset source bytes and hashes,
  baseline/database identity, and complete job hash.
- `fields.json`, `prompt.txt`, `output-schema.json`: exact translation input.
- `attempt-NN.jsonl`, `.stderr.txt`, `.output.json`, `.receipt.json`: actual CLI
  events, raw output, return code, timestamps, artifact hashes and available usage.
- `translated-fields.json`: all expected JSON-pointer translations, no missing or
  extra keys. Numeric/URL/inline-code tokens must survive. Long copied source
  prose, placeholder markers, wrong scripts, and schema size violations fail.
- `document.json`: schema-validated staged document; code, dates, metadata,
  structural links and identities are preserved. LinkBlock and rich-paragraph
  link URLs to the three verified public same-site routes (`/guides/howto`,
  `/destinations/hanoi`, `/destinations/singapore`) are mechanically changed to
  the target locale. Those destinations returned 200 without redirects and had
  matching `lang` and canonical in all five languages on 2026-09-20 (verification
  JSON SHA-256 `84dd8fcdd5102b61b314873a56096f91c5c9673c796b9cb1f8e495796d5a135f`).
  Other locale-prefixed Mokaair link routes, unapproved destination locales,
  aliases, and query/fragment variants stop materialization for review; external
  link URLs, source URLs and source check dates remain unchanged. Publication
  still requires a fresh route and article-state check. The known AI hero credit pair
  `Mokaair · AI 生成示意圖` / `AI 生成，非實拍` exposes two descriptive fields for
  translation while requiring the exact `Mokaair · ` attribution prefix and an
  `AI` disclosure in each result. Photographer names, credit source URLs and
  copyright/CC license identities remain immutable. Other credit formats are
  deliberately excluded until explicitly reviewed. A later publication
  assembly step independently applies article-link and publication checks.
  This field allowlist changes the immutable job hash for matching future jobs.
  Existing prepared/rendered jobs keep their original fields and receipts; use a
  new work root for a newly prepared job rather than rewriting staged inputs.
- `assets.json`: `{svg, public_svg, targets, source_sha256}` for each localized
  SVG. `svg` is an absolute staged path; public paths use locale suffixes.
- `assets/guides/<slug>/`: localized SVGs, rendered raster targets and preview
  PNGs. Local font-size adjustments may fit text into its original container;
  wording, coordinates and drawing shapes remain unchanged.
- `render-receipt.json`: per-SVG byte hash, dimensions, visible-text count,
  font adjustments, bounds/overlap issues, preview path, and raster target hashes.

`receipt.json` status `translated` means field/schema checks passed. `rendered`
means automated layout checks also passed. Neither status is editorial approval,
glyph verification, source-photo review, import, publication, or browser approval.
`reviewed`, `editorial_review_complete`, `visual_review_complete` and
`glyph_review_complete` stay false until a separate reviewer records evidence.
The root review should bind the canonical document hash and every final SVG and
raster byte hash, preferably in a separate `review.json`. A raster with no editable
SVG remains in `raster_review_required`; it is not assumed to be text-free.

An existing-language body whose only images are unresolved rasters gets an
explicit `mode: review-only`, `status: pending_review` job with an empty field
map. It stays in the queue and makes no translation calls. Its original raster
hashes are pinned. It cannot count as completed image review or disappear just
because there is no SVG text to translate.

## Artifact binding and legacy migration

Every new job pins `artifact-manifest.json` by byte SHA-256 in
`receipt.json.artifact_manifest_sha256`. The manifest records `binding_version`,
`job_sha256`, `stage`, `schema_validated`, and a `files` map from job-relative
paths to exact byte hashes. It covers source/field inputs, translated fields,
document, assets manifest, prompt/schema, all attempt files, every staged asset
(including SVGs, rasters and previews), and the render receipt when present.
The manifest excludes itself, `receipt.json`, and independent review files,
avoiding circular hashes. Added, removed, or changed artifacts invalidate resume.
The renderer verifies this binding and the original repository sources before
starting; it permits its own SVG font fitting while pinning every other input
through rendering, then binds all final outputs. First render needs no previous
render receipt. Changing only a receipt's status cannot make a job rendered.

Pre-binding pilot jobs intentionally cannot resume or render until explicitly
migrated. Preserve prior review evidence and run:

```powershell
uv run --project apps/api python tools/article-localization/pipeline.py materialize --slugs gemini-markdown-basics --locales en,ja,ko,zh-CN --reason "Upgrade pilot artifact binding; preserve attempts and reverify all render hashes"
node tools/article-localization/render.mjs --job docs/article-localization/work/gemini-markdown-basics/en
```

Run the renderer for each selected locale. Materialization makes **no model
calls**, revalidates fields/script/schema and source hashes, saves the former
receipt, render receipt and file hashes in `migration-NN.json`, reconstructs
the document/SVGs, and resets review flags. Every subsequent final document,
SVG, raster and preview hash must be compared with the saved pre-migration
hashes. Retain independent review only for exactly unchanged bytes; changed
artifacts require new review. Re-rendering changes the render receipt and
artifact-manifest hashes even if the actual article/media bytes stay the same.

Prepared jobs with **no attempts** can use the narrower migration:

```powershell
uv run --project apps/api python tools/article-localization/pipeline.py migrate-prepared --batch batch-001 --reason "Bind previously prepared inputs after verifying baseline hashes"
```

This verifies the immutable old job hash, source document/pack/assets and field
mapping, saves the former source/receipt/hash map, pins unresolved raster hashes,
and creates the binding. It refuses locked jobs, any prior attempt, and all
failure/quota statuses. It never restarts failed calls or consumes usage.

Chinese variant checks use conservative, confidently different character forms
per field, excluding inline code and URLs. Copying a traditional paragraph into
a Simplified Chinese result (or the reverse) fails even when the title was
translated. Text already valid in both scripts may remain unchanged. These
guards complement independent editorial review; they do not prove semantics or
completeness by themselves.

## Reviewed release flow

Start every release with a fresh read-only production snapshot from the exact deployed
revision. Do not reuse a historical `baseline.json` after repository or database drift.
Run `export_snapshot.py` through standard input inside the deployed API container, save
the JSON as `docs/article-localization/production-baseline.json`, and then run:

```powershell
uv run --project apps/api python docs/article-localization/build_baseline.py
```

Review `source-differences.json` before translating. The builder retains the live
document when repository and production differ, creates stable batches of at most 20,
and pins source pack, document, database, and asset hashes.

After translation, rendering, and an independent hash-bound review, assemble an
explicit batch by repeating `--slug` for each reviewed article:

```powershell
uv run --project apps/api python docs/article-localization/assemble_bundle.py `
  --baseline docs/article-localization/baseline.json `
  --work docs/article-localization/work `
  --slug example-slug `
  --output docs/article-localization/releases/batch-001
```

The assembler requires all five locale documents, preserves complete existing prose,
localizes internal links, copies only hash-pinned reviewed assets, and writes
`release-manifest.json`. Record its exact SHA-256 and use the same value thereafter.

Install the reviewed bundle into its content branch before opening that PR:

```powershell
uv run --project apps/api python docs/article-localization/install_bundle.py `
  --bundle docs/article-localization/releases/batch-001 `
  --baseline docs/article-localization/baseline.json `
  --manifest-sha256 <reviewed-manifest-sha256> `
  --work docs/article-localization/work
```

Installation changes repository packs and public assets only. Its durable journal
stores exact before/after bytes and supports idempotent resume. Per-job receipts bind
the completed journal, source job, artifact manifest, review, installed files, and
backups. Changed or incomplete evidence is refused.

Merge and deploy that content PR before database publication. Re-export the live
snapshot and stop if the deployed source version, visibility, hash, locale state, or
manifest authorization changed. In the deployed API environment, retain one durable
state directory and run `dry-run`, `drafts`, `publish-articles`, then `publish-hubs`
with `publish_bundle.py`. Every invocation uses the same exact bundle, baseline,
manifest SHA-256, state directory, active admin actor ID, and explicit deployed
repository root via `--deployed-root`. The dry-run and every write re-hash that root's
installed article packs and all manifest assets.

The publisher uses existing editorial services, serializable transactions, row and
advisory locks, version/document hashes, and a durable intent journal. Repository-only
articles remain five private drafts. Public articles publish only authorized locales;
hubs wait for exact public dependencies. Re-running reconciles committed operations
without duplicate revisions.

Finally run `report_progress.py` with explicit `--bundle`, `--journal`, and
`--browser-evidence` arguments. It never infers import, publication, or browser
verification from a staged translation; stale or conflicting evidence remains an issue.
