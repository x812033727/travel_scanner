# Independent changed-requirement CSV review

PASS: exact ordered 720-row changed-requirement artifact; 240 exact-on-time rows and original strict 480-row subset unchanged. Portable runner path needs adaptation.

Observation: 2026-10-25T23:27:54.863094+00:00 to 2026-10-25T23:27:55.093728+00:00. Standard-library read-only inspection; no DuckDB/script run, network or source/repository/backend/task/paid mutation.

The variant correctly means **剛好準時或晚到**: delivered and `actual_days >= promised_days`. Here the promise is 3 days, so exact 3 plus late 4/5 qualify; early 2 and in-transit records do not. Avoid describing this as all generic 準時.

Independent CSV recomputation confirms 1,200 input rows (960 delivered / 240 in transit), exactly 720 output records in parcel_id order, and equality of every output column. Independent LF CSV serialization also equals the actual output bytes. The variant has 240 rows each with days_late 0, 1 and 2 (R1/R2/R3 each240); no early rows. Its positive-late subset is exactly the original 480 strict rows.

Draft input, original scratch input and formal episode data/input/parcels.csv are byte-identical. The existing formal/original strict CSV files are still byte-identical and match the independently recomputed strict predicate.

| Actual file | Bytes | SHA-256 |
| --- | ---: | --- |
| `demo/input/parcels.csv` | 28850 | `02d8fdef3bb5014189e139b8ad2f3a87f210bf68d0974da3158bbdf78b5b4ac4` |
| `demo/output/due-or-late.csv` | 10852 | `fe709f321f03e1334e9ed1ee2b48ded4a5458382a8eff6c1d6af464ce105cf8c` |
| `demo/variant.sql` | 358 | `8b03857aff59d94067a2805c80dd6ed3dc75e6581e9bcfd8c9c77a2a7372a1f6` |
| `demo/setup.sql` | 350 | `27628b19c4093ce9cd3016d5b0da84eb5ba557c25b8a6b92bb447c2fc826c654` |
| `run_variant.py` | 2068 | `8cdedf36822f62ebd17aca1d0dbfbcaf4a0fecebf6a61cf8343bdf90814542b1` |
| `demo/variant-results.json` | 316 | `781fb2ffa42eeab2e3d69927c07c7ec84510bf2f6e37ba9ccf223f49fc68819c` |
| `runlogs/variant.command.json` | 259 | `bdb3c41c69c30eecc9a671a5a0286918fe9ae9999d5c3804c22a6fa12c71ce2d` |
| `runlogs/variant.stdout.txt` | 42 | `46691c468502755c2c78dc49f75dada27cb763793029f388a8e4c0160410b725` |
| `runlogs/variant.stderr.txt` | 63 | `8cb8f3d80b51c08acfb75c217f1bbd8424be4b4530c58cd71956eb51f52c47a8` |
| formal `data/output/late-followup.csv` | 7252 | `7a09b5c5cd0477366bf3dd8897104540952572543487017b9f0d0e1f360624a5` |

The saved results count/zero-days/hash fields all match the actual CSV. The helper source SQL literal equals the saved variant.sql. Reviewer validation checks every column; the original helper itself only compared parcel IDs before reporting success.

The exact saved command is `../fifth-demo/bin/duckdb -no-init -agent :memory: -f demo/variant.sql` from `/workspace/work/ai-tech-next/fifth-draft`, with saved exit 0 and stdout count 720. stderr is the ordinary agent-mode startup line. Setup disables automatic extension install/load, sets one thread and 128MB limit, and reads the explicit original CSV schema.

The executable resolves to `/workspace/work/ai-tech-next/fifth-demo/bin/duckdb`: 77,526,584 bytes, SHA-256 `c41f957db5645d545a9caef430994cf262d24fad9297fef70c691395aadb43fb`. This equals the original reviewed fixed 2.0.0 CLI binary receipt. No fresh process execution or network verification occurred. The saved historical success receipt is not a new independent execution. The helper path to sibling fifth-demo is scratch-specific and cannot be presented as a portable episode-local instruction.

Recommended copy: variant SQL/setup, output CSV, variant-results, three exact runlog files, and helper source—14308 bytes total—while reusing the existing identical formal data/input/parcels.csv. Keep original CC0 teaching-code/fixture and separate DuckDB MIT notices. Do not copy the CLI binary.

Preserve original argv/cwd as historical evidence. Adapt a separate portable rerun helper/SQL to the chosen episode data root and pinned `data/bin/duckdb`, update explicit relative paths and generate new subset hashes. Do not silently rewrite old logs to claim the new paths were executed. Keep the original strict 480-row artifact and clearly label the 720-row CSV as the explicit >= requirement change.
