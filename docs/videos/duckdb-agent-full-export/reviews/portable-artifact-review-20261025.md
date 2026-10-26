# Independent portable DuckDB artifact review

PASS for complete ordered CSV artifact and preserved provenance checks; portable-copy documentation/manifest edits required.

Read-only observation: 2026-10-25T23:13:01.579528+00:00 to 2026-10-25T23:13:02.339901+00:00. No DuckDB/demo/verifier/package script execution, network fetch, original mutation, repository/backend/task or paid/media work.

## Independent CSV result

Python standard-library CSV independently read the original fixture and recomputed `status = delivered AND actual_days > promised_days`, sorted by parcel_id. The source is exactly P0001–P1200 in order with unique IDs; all 1,200 rows match the documented fictional generation rule (including route and blank in-transit actual-days).

- Input: 1200 rows; delivered 960, in transit 240.
- Expected/output/readback: 480/480/480 rows, all ordered records exactly equal; R2 = 240, R3 = 240.
- Independent LF CSV serialization is byte-for-byte identical to late-followup.csv. Actual CSV and parquet-readback.csv are also byte-identical.
- Actual agent preview contains 40 data rows (first 20 + last 20), explicit 1,160 omitted-row marker and total 1,200; this display truncation is not lost source or exported data.

| Actual artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `input/parcels.csv` | 28850 | `02d8fdef3bb5014189e139b8ad2f3a87f210bf68d0974da3158bbdf78b5b4ac4` |
| `output/late-followup.csv` | 7252 | `7a09b5c5cd0477366bf3dd8897104540952572543487017b9f0d0e1f360624a5` |
| `output/parquet-readback.csv` | 7252 | `7a09b5c5cd0477366bf3dd8897104540952572543487017b9f0d0e1f360624a5` |
| `output/late-followup.parquet` | 3067 | `a21195f2c67b1fa195007f103e6388699e825b4e7d044243c4411f33ed59ce22` |

Parquet is 3,067 bytes with PAR1 header/trailer and plausible metadata framing. This review does not decode the binary payload or rerun the recorded CLI readback; the independent result is that the preserved readback CSV matches all 480 expected records. The original CLI readback argv, success receipt and streams remain available.

## Provenance and historical-manifest boundaries

- Current package raw is 24,424,037 bytes; its independently computed SHA matches package-check.json and selected official release asset digest. Current 77,526,584-byte binary hash and 1,072-byte MIT license hash also match saved review receipts. This is local receipt consistency, with no new network authentication of the source.
- All ten saved command records use `-no-init`; stdout/stderr byte receipts match actual files. The deliberate typo produces one startup text line followed by a valid JSON error line, not one whole-stream JSON object.
- `license-code-review.json` says every run uses `-init /dev/null`. That is stale wording: saved argv, run_demo.py and current README/KIT use `-no-init`. Omit this receipt from the narrow subset or explicitly label the discrepancy; do not silently treat it as the observed command.
- `kit-manifest.json`: 54 entries; 0 missing and 0 size/hash mismatches against originals.
  Excluded-payload references retained by this historical manifest: `output/report-preview.png`, `sources/duckdb-cli-code.raw`.
- `manifest.json`: 93 entries; 0 missing and 0 size/hash mismatches against originals.
  Excluded-payload references retained by this historical manifest: `bin/duckdb`, `output/fifth-followup-kit.zip`, `output/report-preview.png`, `sources/duckdb-agent-doc.html`, `sources/duckdb-agent-news.html`, `sources/duckdb-cli-code.raw`, `sources/duckdb-cli-package.raw`, `sources/duckdb-migration.html`, `sources/duckdb-news.html`, `sources/duckdb-release.json`, `sources/mermaid-releases.json`.

The old manifests truthfully describe their earlier scratch/kit sets, including files that the narrower episode subset should omit. A new subset-only manifest must be built after copying and editing. Historical package receipts may mention intentionally absent archive paths when clearly labeled as original-download provenance.

## Recommended portable subset

The JSON gives an exact candidate list of 57 files, 102,849 bytes before parent README/manifest edits:

- README/KIT, CC0 notice, original run_demo.py and verify_demo.py, fixture description/input, three SQL files, results and artifact-verification receipts.
- Complete CSV, Parquet, readback CSV and the original 4,362-byte self-contained HTML report; it is a useful readable output rather than an external snapshot.
- All runlogs, including version, both preview modes, reverse-order hash, intentional-typo formatting, full export and Parquet readback.
- DuckDB MIT text, selected release asset metadata, package checksum receipt, and small relevant `.http.json` origin/URL/hash receipts. Preserve MIT separately from CC0; external source text is not relicensed by CC0.

Exclude binary, 24 MB archive, all external full HTML and full-text/large release snapshots, full shell.cpp, unrelated candidates, PNG/ZIP, raw topic/collision inventories and old manifests. PNG/ZIP are unnecessary for row-level reproducibility. Do not carry package_demo.py/fetch_sources.py into the narrow kit as-is.

Parent should adapt README/KIT to included paths, explain that run_demo.py needs the fixed CLI/archive retrieval first, make links resolve, and generate a fresh portable manifest. No runnable-without-CLI or fresh Parquet-decoding claim is made.
