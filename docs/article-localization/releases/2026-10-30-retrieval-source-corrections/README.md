# Corrected retrieval sources: published and verified

Hybrid search, knowledge graph and Agentic RAG have been updated in published
zh-TW. The final host check passed **11/0** on 2026-11-09T07:16:38.745854+00:00; the original
owned hold was cleared only after the accepted gates. A new four-source baseline
was built at 2026-11-09T07:57:31.764434+00:00 and independently verified. GraphRAG remains
unchanged. This completes this source-release task; whole-site localization is
still unfinished, and no next-sixteen translation jobs were started.

The release used existing runtime `693ce5bdec4633c72bf3ee2c0717244af123ddc7`. It performed no
deployment or migration; schema `0145_video_youtube_reports` was already present.
The owner's approval bound plan `b2549e4d`, package `22c9d0d2` and the original
carried hold. Full portable hashes and counts are in [evidence.json](evidence.json).

## Accepted November 9 r2 execution

| Gate | Actual result | Evidence / independent review |
| --- | --- | --- |
| Full backup and isolated restore | 625,122,763-byte dump; complete restore, roles, labels, identity and protected data verified | `f13f5aa9` / `4ea086f9` |
| Same-image rehearsal | 172 public tables; 3 drafts + 3 publications; 6 revisions and 6 audits; zero-write replay | `7f1aebe5` / `e5eab3e1` |
| Production | 3 drafts + 3 publications; exact documents and versions; both replays wrote zero | `1842ab42` / `c360e038` |
| Public acceptance | 3 pages, 9 unchanged assets, 6 new original screenshots; two independent visual reviews | `e02555c6` / `d119d8d0` |
| Evidence installation | Actual host/client completion and exact readback | `cc58993c` / `6741b603` |
| Final host and logs | Expected held 10/1, owned hold clear, new free 11/0; complete continuous log evidence | `596edc7b` / `8c805d99` |
| Four-source baseline | Four source rows, versions 12/10/10/8, no source differences, no jobs | `872688a9` / `831d6494` |

The full dump SHA-256 is `b27a16bbfbe55661053a8e33fd2fedd4d74bf0d760fe2aa6460666e3ef7a7d63`.
The new strict nine-category protection window began at this r2 backup's
`before_capture`, digest `d70132a3`. Historical `154fe762` remains a different
window. Isolated fingerprints use `sha256-sorted-row-digests-v2`; they are not
relabelled old-algorithm results. The exact authorized revision/audit increments
were verified while other protected guide data remained unchanged.

## Published source baseline

| Source | Previous → published version | Normalized document SHA-256 |
| --- | --- | --- |
| ai-term-hybrid-search | 10 → 12 | `972610411149ea1010e2e8b0a23d4086181e0cb18de0dc222ae771e43dba46c5` |
| ai-term-knowledge-graph | 8 → 10 | `64f41fb947553be82d8eb0e8641265d8ed721ce5965875ffb09dd3df12f3f7be` |
| ai-term-agentic-rag | 8 → 10 | `bb7772cb28692526d8ed07068bbde4f58b47f8fa59efbb19a0257d491cea0895` |
| ai-term-graph-rag | 8 → 8 | `1c0dea04721fd72d34051a5c46abc7db2c58e05757465ce81abf9c49636bafca` |

The new official snapshot was captured after the actual finalization review.
It matches the four repository packs, twelve original assets and runtime hold
configuration; the complete GraphRAG row is unchanged. The selected baseline
contains four sources and sixteen missing translations, with no source
differences. Its native intermediate is not a whole-site production census.

## Public verification and stopping boundary

All original HTTP, DOM, network and six screenshot bytes remain unchanged.
Two reviewers actually viewed the six originals. Mobile diagrams deliberately
scroll horizontally; a separate successful three-page keyboard/end-scroll check
and three right-edge images confirm access to their right side. Touch gestures
were not tested. The first supplemental check failed in its local request-drain
logic and is retained separately; it was not treated as successful evidence.

The final raw review covers 207 files and nine complete log-source snapshots.
Backups, isolated resources and all previous failures are retained. No cleanup
commands ran. Resource retention is based on the last accepted identities,
complete execution history and final receipt, without claiming a new final
container inventory. No database dump, owner identity, environment, database IDs,
machine paths or raw private logs are included in Git.

At 2026-11-09T15:19:51.663634+08:00, a new read-only census counted 2,501 public articles: 1,737 have all five public languages, while 764 lack 3,056 language documents (764 each in en, ja, ko and zh-CN). It excludes 163 unpublished drafts and does not re-review body or artwork quality. These three source corrections do not reduce that translation backlog.

The following chronology is historical. Statements about pending work, failed phases or a retained hold below describe their dated checkpoints; they do not supersede the completed r2 outcome above.

## Historical November 9 r1 failure and r2 preparation

The latest failed-attempt diagnosis strongly supports memory exhaustion in the
isolated PostgreSQL, not a production database failure: its 2 GiB limit was
reached, cgroup recorded one OOM kill, and the backend sorting `video_stage_jobs`
received signal 9 at the failing query time. No native draft/publication ran.
The accepted full backup, original failed attempt, exact hold and four isolated
resources remain preserved and were freshly checked by readonly evidence
`07003475` and independent review `d13a3347`.

A disabled r2 candidate replaces full-row sorting with sorting SHA-256 digests
of every complete row; it retains duplicate counts and all protected predicates.
Real local PostgreSQL 17.11 tests reproduced the old OOM with 9,000 large rows;
the candidate completed two identical full fingerprints with a PostgreSQL peak
of 70,152,192 bytes and no OOM. Thirteen semantic cases also passed (`f7624462`).
These tests do not replace actual host restore or rehearsal. The new fixed
package `22c9d0d2`, plan `b2549e4d` and static bindings `65782f1d` passed final
independent preparation review `b48a1216` before the owner's later r2 approval.

Seven fresh preparation observations passed independent review `a9686b55`:
102 recorded native commands and all seven outer processes exited 0. The four
source documents, selected nine-category state, runtime and seventeen files
remain fixed. Global protected state differs from the prior backup in six
category fingerprints and net row counts. This does not identify which writer
changed it or prove insert-only changes. The new plan explicitly starts a new
strict window at its own backup.before_capture, requires a fresh full restore,
and preserves the historical failed attempt and protection evidence. The
original hold remained. At that preparation checkpoint, no new enabled context,
payload or host root existed; the current execution above supersedes that state.

The owner approved the new current-runtime plan `5243c266` and fixed package
`d2413497`. Fresh action evidence and the actual execution payload received
independent review before installation. Installation and prepare completed with
true child exit 0; their independent reviews are `c4e22c96` and `e9fce918`.
The new release owns its deployment hold. The earlier hold was not adopted.

The complete database dump contains 624,774,959 bytes (SHA-256
`04a075c05687193d345166ec3e947ce3d64d0005ef36d1c45ea8a62aab5da8ae`).
It was actually restored into new isolated PostgreSQL. Backup/restore main and
phase result are byte-identical, SHA-256
`e1ac79c0778d3ee09b33e2ae928314651b8debb39179d8eb15e5d6d5743e6de8`;
the true child exited 0. Independent review `bbfb83ab` verifies the same-image
API, inherited and owned labels, resource/network/role restrictions, and exact
selected article plus nine protected-category comparisons before/clone/after.
The five live services and seventeen runtime content/asset files stayed unchanged.

The accepted backup review was appended and read back unchanged. Same-image
rehearsal then failed in its first read-only whole-table fingerprint operation,
before any draft or publication command. Its true child exited 1; original
result `d414b1dc` and completion `4ea43494` are retained. The reported connection
closed during transaction rollback; the native command did not exceed an outer
deadline. Root-cause diagnosis is still read-only. Independent failure review
`78af90e0` confirms this boundary without relabelling rehearsal as successful.

A new fixed read-only capture after failure (`5d557249`, 05:12 UTC) confirms the
original four source documents at 10/8/8/8 and unchanged API/web runtime and
seventeen content/asset files. No production publication, public acceptance,
final host 11/0 or new four-source baseline occurred. Own hold, backups, isolated
resources and all previous attempts remain retained. No deployment, migration,
automatic retry or cleanup occurred.

## Earlier preparation checkpoint, 2026-11-09 (superseded)

The owner approved the October 30 r3 plan `621c9750` / package `c41507e9`.
Model usage limits interrupted that attempt before an enabled context, actual
payload or r3 host installation was produced. The approval is preserved; it
does not bind the changed live runtime or a different tool package.

Fresh read-only observations show no deployment hold, pause or drain marker.
The old hold's removal actor and reason are unknown, so its absence is not
evidence of this release's successful finalization. Original r1/r2 evidence,
r2's eight proof hashes and four isolated resources remain retained. A new
current-runtime plan is being prepared with a new own hold and a new complete
backup/restore window; it is not yet authorized for execution.

Seven preparation transports completed with true exit 0 and empty stderr.
Their 94 native command records comprise 64 raw-stream records and 30 logger
metadata records; private logger payloads were not exported. The four source
documents and 17 runtime content/assets still match the reviewed preparation.
Native read-only planning passed with the original selected state `f13fd663`;
the new global observation `154fe762` is not an execution protection baseline.

Preparation index SHA-256:
`8e12d33f4fbbaa705da5df3f3158d0b4591c67a25a5eda070c0bcc23f8ba12b4`.
Private current evidence set (outside Git):
`article-locales-20261029/source3-current-release-preparation-20261109-01`.
No new backup, restore, publication, public acceptance, final host 11/0, baseline or
hold removal has been performed during this resume. The whole-site census is
764 incomplete public articles / 3,056 missing public locale documents;
163 unpublished drafts are excluded.

The current official host verifier separately passed all eleven checks at
03:59 UTC, with true exit 0 and empty stderr; raw output SHA-256
`a525b4e52c63ebdca8b813683cd17ed5712f0dbdc6bae69b7c56227e4c3fc7bd`.
This is a preparation baseline, not acceptance of an unpublished release.
The verifier performs a brief existing-lock probe and HTTP GET requests.

## Historical October 30 evidence

The sections below preserve the original failure and preparation chronology.
Their references to an existing hold or awaiting r3 approval describe the
October 30 checkpoint and are superseded by the current status above.

### Retained failed attempts

| Attempt | Actual result | Boundary |
| --- | --- | --- |
| r1 | Install succeeded; prepare exited 1 | Required review field was missing, before hold or database phase body. |
| r2 | Install and prepare succeeded; backup exited 1 | Full dump and isolated restore exited 0, but isolated API validation failed before API start or clone comparison. |

R2 backup child `1861887` ran from 14:43:35 to 14:48:58 UTC. Its fixed validator
required three labels, while the created container had six. Exact read-only
inspection confirmed the additional three were inherited Docker Compose labels
from the same pinned image. The container's complete label map equalled the
image's labels plus this release's three ownership labels. The remaining API
validation conditions passed against the recorded actual inspection. This
diagnosis does not turn the failed backup phase into a successful phase.

At the 14:58–14:59 UTC read-only check, the three-source state still matched
`f13fd663129212acbf2cc776a8548789b54bdfdd2fd7b09c8c917bcc1fc57770`.
The protected global set changed from `8f673f0b…` to `b0dc4fcd…`, with differences
in six of nine categories. A later read-only identity query observed two news
articles created at 14:56:52 and 14:56:56 UTC, after the failed backup ended.
Counts and creation times alone do not prove that these were the only changes,
or identify the writer. The original r2 protection window remains failed.

No rehearsal, production publication, public acceptance, final host acceptance
or new source baseline ran. R2's own deployment hold, dump, isolated database,
created API, private material and all intents/results remain retained. The hold
must not be cleared merely because this attempt stopped. No r2 file, failed
intent or approval may be overwritten or relabelled as successful.

## Historical October 30 evidence and proposed next action

Private execution evidence set (outside Git):
`article-locales-20261029/retrieval-source3-execution-02`.
No database dump, owner identity, environment secrets or private raw streams
are included in this repository.

| Evidence | SHA-256 |
| --- | --- |
| Actual backup failure review | `0b0c75fa4a37b56804d708bb49b7e892c38b8bbf553d7b9656d2f8a21262b8a7` |
| Actual protection-window drift review | `c21aa5666effacb8f2781eeafde8110353af788e95764ebd66c99a9f7beddc1a` |
| Label provenance readback | `beeef71f58812f696fe4088d4460e3923621f953f1a9515e3840d1c75a0cef4a` |
| New guide identity readback | `14ef0a4282302bee59aa2bdeb530cf161538a12406ca91925963eeb11b23325a` |

A separate recovery proposal is being prepared locally: retain r2, carry its
exact existing hold forward without a deployment gap, and use a new attempt,
new full backup and new isolated resources. Its strict data protection checks
must remain intact. R3 has not been approved or installed. A concrete reviewed
plan and fixed tools are required before a new owner decision.

### R3 preparation complete; awaiting a new owner decision

Final plan SHA `621c9750a93bf042076f6969c2bc3277373e3bec0b57020a4e5fe4e833194fe6`; fixed package `c41507e950c44066b483f94ccaa3284c3bf1a584291493459b985717bccb0d6f`.
Final independent review `873feb0802096f9c876c6b4119e2359e1a4c130bec2904889306ae1a920672b0` and preparation seal `7814f31263b05107ab47243268b8f3600abd4a6c1bdd3ae24f917841b9dc94bb` bind the reviewed files.
The fresh adapter passed 66 independent cases; code/model tests are not live phase acceptance.
Six preparation captures and 73 native records at 15:34 UTC remain preparation-only evidence.
R2 backup remains FAILED and its original data-protection window remains drifted.
No r3 owner approval, enabled context, installable actual payload or host installation exists.
The existing r2 hold remains owned and retained; a new approved attempt must carry its exact identity forward.
After successful publication, public QA, new 11/0 and four-source baseline, close out; do not start next16.
Private plan evidence: `article-locales-20261029/retrieval-source3-execution-02/recovery-plan-01/RELEASE-PLAN.md`.
