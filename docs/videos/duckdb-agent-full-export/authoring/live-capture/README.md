# DuckDB live operation capture — PREP only

This bundle has not started a browser, CLI demo command, media encoder, network,
TTS, ASR, upload or paid request. Child preparation only read source files, made
new files under this directory, compiled JavaScript syntax and parsed the Python
AST. Root alone may execute after full code read and independent static review.

`capture.mjs` runs one local capture process. It holds the normal same-PID lease
of the existing DuckDB project and refuses every prior lease, including dead
takeover. Original E850/W948, source111/8 targets and four held records are
verified against Root's full baseline before and after. A fixed exclusive
`B/capture-once` directory and fresh output directory prevent replay/overwrite.

The only CLI program is the existing SHA-pinned official DuckDB 2.0 binary.
Original published SQL and CSV are copied byte-for-byte to a NEW runtime; old
output files and runlogs are never copied. During live browser recording, the
original console accepts only the six fixed commands in `capture-plan.json` in
order. It genuinely executes each process and displays that process's exact
current stdout; a readback command with empty stdout separately shows fresh file
metadata and an actual full-byte equality result. Complete argv, stdout, stderr,
exits, screenshots and timing events stay on disk.

The view labels itself 本片原創操作視窗 / 操作重現2026-10-27 /
原創虛構教學資料 / 無配音. It is not a DuckDB official interface, AI inference
test or performance/token/cost comparison. Its 1,200-row source is the existing
original fixture dated2026-10-25. Agent preview displays40 and omits1,160;
strict-late export must contain480 full matching records. Including the240
exactly-on-time records changes the intended list to720. A separate standard
CSV parser checks every field of every480/720 row; Parquet readback CSV must
match strict CSV bytes.

Browser requests are restricted to its own127.0.0.1 loopback server and locally
installed bundled fonts. No arbitrary shell, URL or filename is accepted by the
fixed `/run` endpoint. No credentials are loaded. Source/provider/voice/styles,
canonical media/cache/state, QA/history, globalASR slot and settings are untouched.
The native WebM is retained. A single H.264/yuv420p/faststart encode maps only the
video, with no speed/frame-rate override. Actual fps/duration are read from
ffprobe, not assumed. Target output is75–100s/1920×1080/0audio; raw and MP4
durations must agree within0.12s and the whole MP4 must decode. Reading pauses
are normal operation-viewing time, not narration timing or an8-minute body claim.

## Root admission

Before execution, create `B/root-capture-release.json` as a new local dispatch
record, not server or quality approval. Required fields:

```json
{
  "kind": "ROOT_local_DuckDB_live_capture_dispatch",
  "owner": "/root",
  "no_TTS_ASR_or_paid": true,
  "no_external_network": true,
  "max_cli_commands": 6,
  "max_capture_seconds": 120,
  "helper": {"file":"ABSOLUTE_CAPTURE_MJS","bytes":0,"sha256":"ACTUAL"},
  "plan": {"file":"ABSOLUTE_CAPTURE_PLAN_JSON","bytes":0,"sha256":"ACTUAL"},
  "baseline": {"file":"ABSOLUTE_ROOT_BEFORE_INPUTS_JSON","bytes":0,"sha256":"ACTUAL"},
  "task_claim": {"file":"ABSOLUTE_OWN_TASK_FILE","bytes":0,"sha256":"ACTUAL"},
  "static_review": {"file":"ABSOLUTE_INDEPENDENT_REVIEW_JSON","bytes":0,"sha256":"ACTUAL"},
  "issued_at_utc":"ACTUAL",
  "expires_at_utc":"ACTUAL_WITHIN_30_MINUTES"
}
```

All descriptors must be the real file/byte/SHA descriptors, not these placeholders.
Own task must normally be in-progress under codex-duckdb-20261025. Root freshly
checks actual producers/STOP/LEASE and confirms no existing D output. Execution:

```sh
PLAYWRIGHT_BROWSERS_PATH=/workspace/work/playwright node --use-env-proxy \
  /workspace/work/ai-tech-next/duckdb-live-capture-20261027/prepare/capture.mjs execute
```

No HOME or other credential/system env variable is changed; normal inherited
proxy/TLS remain. `PLAYWRIGHT_BROWSERS_PATH` selects the already-installed browser
and encoder for this command only. Every child command has its own timeout;
recording dispatches are limited to120s and the release to30min. Failures leave
raw media, logs and a truthful completion; no automatic new process/retry.

## Actual output contract

D=`/workspace/work/videos/_duckdb-live-capture/duckdb-agent-full-export`:

- `live-demo.silent.mp4`, `live-demo-usage.txt`, `recording-manifest.json` are the
  three intended new backend source-material attachments after Root acceptance.
- `live-demo.raw.webm`, `raw/`, `runtime/`, `logs/`, `screens/` retain actual native
  recording/inputs/outputs and provenance; binaries do not go into Git.
- `B/capture-once/completion.json` records true ok/error, PID, six step exits,
  oracle/encode/probe/decode exits, released native lease and descriptors of the
  three assets, raw WebM and MP4 probe. It is not actual Root tool-exit evidence.

Root must separately record actual tool exit, independently inspect the footage
and verify the full CSV/MP4 evidence before any append-only backend delivery.
This helper cannot upload or approve anything. It creates no M4A, CC, final
film, bookends, foreign dub or language batch, and makes no listening/QA claim.
