# Citation video runtime exclusion and retained-answer check — 2026-10-07

This record concerns only `ai-citation-check` and the private continuation operation
`<home>/mokaair-work/ai-teaching-continuation-20261007` (`OP`). It separates the
pre-dispatch host exclusion snapshot from the subsequently authorized local TTS
producer and its filesystem recovery. The checks below made no provider request,
changed no production file, and did not approve audio, a final, upload or publication.

At `2026-10-07T08:43:46–50Z`, a fresh host filesystem/process read and a PostgreSQL
repeatable-read, read-only transaction established:

| Check | Actual result |
| --- | --- |
| Citation project | `44f3fcd6-7ae0-4636-a4c6-82a3edaedb52`, stage `outline approved`, last sync `2026-09-28T11:47:10.150700Z` |
| Current review inventory | Only approved outline `948b2d65-6c71-4a62-a338-6fb4f5fd3de9`; SHA `82c127758c451209330ad591e41c2fae2fb0f1a3ec57bb3bf015ea4ace8eab02`, decided `2026-09-28T12:16:03.098513Z` |
| Citation durable stage jobs | None of any status; the query also read all globally queued/running/uncertain stage jobs |
| Citation media jobs | None; the query also read globally queued/submitted media jobs |
| Citation project exclusions | No drop, retry request, acknowledged retry, YouTube video or selected-language decision |
| Host canonical directory | `/var/lib/docker/volumes/travel_scanner_video_work/_data/ai-citation-check` absent; consequently no canonical citation STOP, LEASE, auto state, language journal or speech journal |
| Host global STOP | Absent |
| Observed host native/operator processes | No citation argument; the separate R6 operator remained live |

The database child actually exited 0. The first SSH envelope printed its complete
read result, then exited 1 because a CRLF here-document terminator was interpreted
after the Python read. A later supplementary Bash envelope likewise printed its
complete result but encountered a trailing CRLF command. Neither error caused a
mutation. A final direct Python-stdin SSH read actually exited 0 at
`2026-10-07T08:46:32.196364Z` and independently reconfirmed canonical/global-STOP
absence, the exact 18-slug exclusion, all four profile scopes, and the bounded
archive-path result below. These envelope failures are not reported as passed
whole-command checks.

The existing renewed-final operation at `/root/renewed-finals-20261007` excludes
citation by its exact `source-bundle/plan.json`, SHA
`007892da4723aef6cc0a6181beec6886f8dd97e990e9b154c27d5b32132d87b0`.
Its 18 source entries and expected final-review identities cover the six
`ai-real-world-01` through `ai-real-world-06` episodes and these twelve other slugs:

- `ai-agents-explained-what-they-cost`, `ai-price-war-gpt-6-sol-vs-opus-5-5`, `ai-real-jobs-chart`
- `always-on-agent-explained`, `free-vs-paid-ai-plans-2026`, `google-vids-free-ai-video-omni-1-1`
- `openai-agents-broke-in`, `openai-devday-2026-recap`, `rtx-spark-local-ai`
- `siri-ai-ios-27-how-to-get-it`, `vibe-coding-first-website-2026`, `why-openai-killed-sora`

The live profiles independently restrict their native request namespaces to:

| Manifest scope | Request namespace | Selected source slugs |
| --- | --- | --- |
| `languages/lexicon-161` | `8de27f94-6c76-4e65-9559-ac2a81952b9f` | EP01, EP05 |
| `languages/lexicon-empty` | `4417288b-70db-48b3-9609-17567d16ef36` | EP02, EP03, EP04 |
| `languages/lexicon-native-literal-Anthropic-null` | `0d2b961b-1525-48f6-8917-176cd7785f2e` | EP06 |
| `languages-r6/lexicon-native-literal-Anthropic-null` | Same retained EP06 namespace | EP06 only |

R3 and R5 were held, exited 1, and their recorded producers were dead. R6 was
running and selected only EP06's remaining Simplified Chinese metadata/CC work.
Its driver explicitly excludes EP04 and allows no paid media regeneration or
YouTube operation. EP04's original translator journal remains `unknown`, key
`4039831d425dab778d4fad837d6cc426175cff7058deb59632f86e3b5d8b7792`, under
`languages/lexicon-empty/work/ai-real-world-04-tasks-and-jobs/`.
No citation continuation changes, consumes, clears or retries that request.

The host-driver source was also read. Its transport permits only the exact cohort,
and its fresh decision guard compares approved final review ID, full content SHA,
decision time and the corresponding approval audit. The database probe requires
exactly one `video_review_approved` audit whose actor equals the decision maker
and whose slug, gate and SHA match that final. Its idle guard reads actual worker
processes, global durable jobs and upload inactivity. This audit inspected those
guards but did not rerun all 18 human-authority/upload probes; it does not certify
every renewed final's current actor role or full package readiness. No human
identity or secret is reproduced here.

A read-only named-path scan of the host work volume through depth five found no
path named for citation, including inspected archive/recovery branches. The local
canonical `<home>/mokaair-work/videos/ai-citation-check` was also absent. These
bounded observations do not prove that no opaque, deeper or external backup can
exist. The operator separately checked available backup inventories before the
new bounded launch. Absence of stage/media rows alone is not proof about a speech
request: the native speech journal remains the authority for sent/held answers.

After the exclusion snapshot and the operator's backup check, the operator launched
one private native TTS producer at `2026-10-07T08:44:55Z`, PID `18744`, using
`OP/media/ai-citation-check`. It used the actual pulled outline approval and no
force mode. This new producer is distinct from the earlier no-citation-flight
snapshot and excludes a second launcher. At `08:46:08.693716Z` its persisted
operation receipt reports exit 1: Windows EPERM prevented the native confirmed
journal temp from replacing its sent receipt. Twenty-three raw takes were already
cached; this was not a complete narration or accepted audio.

The interrupted request was
`fb9bd9cf0d11741832c10e0b3e0ef7f6932840164795756a6f859cb8dbbd0e93`.
The operator preserved its original sent JSON, full confirmed temp, complete WAV
and proof under `OP/recovery/<request-sha>/`, then promoted only those received
confirmed bytes at `2026-10-07T08:47:23.064Z`. The recorded promotion has zero
network calls. A single native continuation was launched at `08:47:24Z`, PID
`18414`; it must reuse this exact confirmed answer and keep all current cached takes.

An independent read-only check of the immutable recovery copies actually exited 0
at `2026-10-07T08:48:32.354Z`:

| Preserved artifact | Actual bytes | SHA-256 |
| --- | ---: | --- |
| Original sent receipt | 1,065 | `e559c86b12f068b6921dd80c3c96dc031e8a832b8eeef593119f0f8fabf592e4` |
| Complete confirmed temp `.18744.tmp` | 1,243 | `56ac178e9d90d4797b13d062f2cd41bfc679f2b8465b214aedd8ae3ab137ec27` |
| Full provider WAV | 2,008,364 | `189a5520a1bb1d694273824a685502c9330ea3d8dcab06d057a24f6d10346402` |

Both receipts have the exact native schema-1 `speech` transition, identical full
request, request SHA and original `sent_at` (`08:45:58.062Z`). The confirmed time
is native ISO `08:46:07.970Z`, after sent time; its declared full WAV SHA and bytes
match the preserved answer. Native WAV helpers validate mono, 16-bit, 48,000 Hz
audio with 1,004,160 samples. Billable characters are 111, matching the current
native request's expected 111. Original PID `18744` was dead.

Rebuilding the current caller's plan with native `loadProject` and `planRequests`
finds exactly one complete matching body: `order-matters#0`, scene `order-matters`,
lines `ci116`–`ci119`. All ten pinned original source files still match. The
promotion receipt binds the same complete archived bytes. At the independent
read, those four lines were present in the current cache (43 total cached takes)
and the live request journal had been released. Native release after durable cache
is expected; disappearance alone is not evidence of successful TTS completion.

The first independent attempt to inspect the original live temp stopped on ENOENT
because the operator had already promoted it. The successful review therefore
binds the preserved original copies and verifies the completed local promotion
after the action; it is not described as a pre-action independent approval.

Strict promotion of this already-received, full source-bound answer preserves the
native no-dispatch guard without repeating a provider request. Any later sent,
held, partial, changed or unbound receipt must remain preserved and block dispatch.
This receipt authorizes no journal forget/reset, extra producer, force retake,
canonical work replacement, host lock change, review approval, upload or publishing.

## Completed inline ASR receipt recovery

The later native ASR producer, PID `4436`, exited 1 at
`2026-10-07T09:03:55.215448Z` after another Windows EPERM rename. Sixty-six
heard-text cache rows were retained. The interrupted schema-1
`speech/transcribe` request was
`aae664f9bdb24a313087bacce0460dc6a820fa1e11f885ed614422cb566af46d`.
Its original sent time was `09:03:44.059Z`; the complete confirmed temp records
`09:03:54.201Z` and the full answer `路標不是證據本身，更不是保證書。`.

An independent read-only native-body audit exited 0 at
`2026-10-07T09:06:51.598Z`, before promotion. It compared the live receipts with
the immutable copies in `OP/recovery/<request-sha>/`, checked the native schema,
same recorded request fields and sent epoch, chronological ISO timestamps, full answer
hash, original producer death and archived audio equality. Rebuilding all 143
current raw-clip requests found exactly one match: `ci131`, scene
`source-function`. The native 48 kHz mono WAV was downsampled with the caller's
WAV helpers to the exact 16 kHz request. The current native default has no
language or terms field; `hintTerms` returned an empty list.

| Preserved artifact | Actual bytes | SHA-256 |
| --- | ---: | --- |
| Original sent receipt | 340 | `54617d1d59a5ea03941106b147bb7a0e7ae48da0e324a0886834dd1d8e4e7384` |
| Complete confirmed temp `.4436.tmp` | 560 | `90dcd5f1026208b46d509a5c872767cfcb5a518dab8150c588a5ce73fd7ea87e` |
| Source raw `ci131.wav` | 317,804 | `1ce2e715c5d1d1aa1a05951d97568f2c792a84f2ddec95b5c9ceaf59f53d8b2e` |
| Rebuilt request WAV | 105,964 | `81505fa805e93ce3fde69fae3ce0241c1e44a03ec353f90a1159482e461edb09` |

The complete native answer JSON hashes to
`dd9e36dc02a531626f57a6cd19d9df72a27364a071338ed245b9b33607f7796c`.
The operator's persisted `promotion.json` records actual local promotion at
`2026-10-07T09:07:09.615Z`, zero network calls and complete native-body matching.
It binds the same sent/temp/raw/request-WAV pins, verifies PID `4436` is dead,
and reads back the exact confirmed-temp SHA after the guarded rename. The
independent review subsequently read this promotion receipt. A single native
continuation used session `87161`; its log filename is
`20261007T090710Z-audio-check-confirmed-resume.log`. This recovery establishes
only reuse eligibility for an already-received answer. It is not audio QA approval.

## Later unresolved sent ASR request

At `2026-10-07T09:10:08Z`, the operator observed session `87161` become an unknown
process. The continuation log is empty and has no exit receipt, so this is process
loss rather than a known endpoint failure. The local check contains 68 heard-text
rows, including the recovered `ci131`; the next request has only a sent journal.
The private STOP remains present. Fresh process inspection found no local native
TTS or ASR producer; unrelated free offline rendering processes may still run.

The unresolved request is
`5f7cbb48ab7a326474e12293c3748be97720963d6bdbf619f3177362a929c037`,
sent at `2026-10-07T09:07:25.020Z`. Its schema-1 `speech/transcribe` JSON is 339
bytes with SHA
`301f66c5d2c8e50a52cdcd6e29c3a6381372b9095279bd0d10ce389e2128f9d9`.
There is no confirmed temp, inline answer or matching heard-text cache row.

An independent read-only audit exited 0 at
`2026-10-07T09:24:52.844Z`. The exact current native request reconstruction over
all 143 clips found one match: `ci037`, scene `not-found`. Its valid current take
is a 282,284-byte raw WAV with SHA
`415a716b433b70ce591e833bfbdeb3870030b879908217e5b11d6701f55aac71`.
The native 16 kHz request is 94,124 bytes with SHA
`9c9e10d22db24997e7a7380947a9140f0471d27dc24d6ae6d03203dbf8e7c4a8`.
The full JSON body, with the native empty-term/default-language behavior, hashes
to the exact sent request key. STOP bytes hash to
`c309e6e472ee224e570ef06afb5d0a12dc0edf618f29d2a5d357557243e2993a`.

Fresh read-only host reconciliation completed at `2026-10-07T09:27:10Z` against
production revision `2024304170c6b43ecb4259e6b4fb0ce8a60d9893`. Deployed
`video_speech/admin_api.py` and `checking.py` match the reviewed local code hashes
`ca9cb6b703909b6a8b30f5356b104ab21f680093a69609dd0d7e2dda4c08de16`
and `ed33f963a64db22a62db861f5a418fe285f616c4affbc4d80ac25ef489faa9a5`.
The transcribe route has only POST, calls Gemini synchronously, and returns the
text in memory. It does not persist a transcript, native body SHA or retrievable
answer. The native client also supplies no request hash or idempotency key to
that route. No secret material or provider-account billing was inspected.

A read-only database window from `09:07:20Z` through `09:09:00Z` found zero
Gemini provider-request rows, zero video-speech provider-response rows and zero
speech/transcribe usage-ledger rows. This route bypasses those generic durable
meters; their absence does not prove zero charge. Bounded API access logs contain
transcribe HTTP 200 events at `09:07:24.194857034Z` and
`09:07:35.179099475Z`. The latter follows the local sent time, but neither log
retains this native request SHA or the actual answer. It is temporal evidence of
server completion, not a source-bound transcript or a billing resolution.

No retrievable complete answer bound to this request and epoch was found.
The request remains unknown and must stay preserved with STOP. Neither a 200
access entry nor an absent usage row permits promotion, retry, reset or forget.
This read-only reconciliation dispatched no provider request and grants no
audio, language, final, upload or publishing approval.
