# M09 English dub: 13:52 UTC gateway failure evidence

## Exact held request

- The English dub stopped on a 64-character Gemini TTS request, “Remember those names? The small upper dial listed ancient games.” The local speech journal still records `status=held`, `path=speech`, `sent_at=2026-10-16T13:52:06.429Z`, `held_at=2026-10-16T13:52:06.897Z`, and `why=no usable answer came back (HTTP 502)`.
- Request body SHA-256: `22c2a8a38039b40008d89a7208f532fc69e949fe11a7355247f121926447036e`. The untouched journal JSON at `<VIDEO_WORKDIR>/curio-m09/audio/speech-journal/<request-sha>.json` has file SHA-256 `BB2DA6BA8413274483C1A2F5CF3C508D5DFD1B672EEB80CFDF2510AD1961A48F`.
- The first 53 English WAV takes were cached before this request. Their 3,062 billable characters exactly equal the change in the server-side Gemini speech quota counter; the held 64 characters were absent. This counter is a pre-dispatch Redis reservation, not a Google invoice, so it is corroboration rather than the deciding evidence.

## Host evidence, read only

The saved PuTTY `hostinger2` session reached the production host. A filtered read of `/var/log/nginx/error.log` found **one** `/api/video/speech` error from 13:52:05 through 13:52:09 UTC:

```text
2026/10/16 13:52:07 [error] ... connect() failed (111: Connection refused) while connecting to upstream, client: [redacted], server: mokaair.com, request: "POST /api/video/speech HTTP/1.1", upstream: "http://127.0.0.1:8091/api/video/speech", host: "mokaair.com"
```

The `travel_scanner-web-1` container's `StartedAt` was `2026-10-16T13:52:25.330578628Z`, after that failed POST. The contemporaneous deployment log was `deploy_20261016_134930.log`. The Nginx `connect() failed` entry means Nginx could not open a connection to the web upstream; this request did not enter the web route, API, or Gemini. The held 64-character request therefore could not have incurred Gemini TTS usage. No Gemini provider dashboard or invoice was queried; the conclusion rests on the network failure before the provider path.

To repeat the filtered host read without displaying the client address, run the following in PowerShell with the existing saved PuTTY session:

```powershell
& 'C:\Program Files\PuTTY\plink.exe' -batch -load hostinger2 -l root "grep -E '2026/10/16 13:52:0[5-9]' /var/log/nginx/error.log | grep -F '/api/video/speech' | sed -E 's/client: [^,]+,/client: [redacted],/'; docker inspect -f '{{.State.StartedAt}}' travel_scanner-web-1"
```

## Recovery boundary

This receipt records evidence only. The held journal remains in place; no `forget`, retry, paid call, or other journal change was made during the investigation. Before resuming, preserve and hash a copy of the exact held JSON, then clear only the above request SHA and use the 53 cached takes. Keep the existing M09 multilingual budget reservation and reconcile actual usage after the resumed run.
