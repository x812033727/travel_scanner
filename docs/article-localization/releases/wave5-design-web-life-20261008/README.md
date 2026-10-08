# 2026-10-08 design and performance locale preparation

Twelve published life articles now have reviewed local content packs for en, ja,
ko and zh-CN. This is preparation for a future production release. It does not
record a merge, deployment, database publication or public page acceptance.

The authoring task is `2026-10-07-localize-twelve-design-workflow-and-performance`.
The separate, unclaimed release task is
`2026-10-07-release-localized-design-web-life-wave5`.
Content draft PR: [#1378](https://github.com/x812033727/travel_scanner/pull/1378).

| Article | Added locales |
| --- | --- |
| lazy-loading-images | en, ja, ko, zh-CN |
| open-graph-sharing | en, ja, ko, zh-CN |
| rgb-cmyk-export | en, ja, ko, zh-CN |
| saas-paas-iaas-responsibility | en, ja, ko, zh-CN |
| sass-scss-workflow | en, ja, ko, zh-CN |
| wireframe-prototype-testing | en, ja, ko, zh-CN |
| ui-ux-learning | en, ja, ko, zh-CN |
| figma-design-basics | en, ja, ko, zh-CN |
| lottie-web-animation | en, ja, ko, zh-CN |
| core-web-vitals-diagnosis | en, ja, ko, zh-CN |
| pagespeed-performance-review | en, ja, ko, zh-CN |
| amp-website-decision | en, ja, ko, zh-CN |

All 48 locale documents received independent complete text, native image and
glyph review, bound to the actual translated documents and artifact hashes.
The application writer did not approve a target whose translated fields they
changed. Review raw-pin map SHA256:
`2c3d09dac1c51faa18698b400c3e35700129ddb467035c414db583701244a9a5`.

Four Traditional Chinese sources had five irrelevant AI glossary links replaced
with plain text retaining the same visible words. The exact pointers and genuine
independent correction hashes are recorded in
`docs/article-localization/source-corrections/wave5-web-life-20261008.md`.
The other eight full source documents, all original dates and 36 original media
files are unchanged. The official assembler normalized only the order of the
existing topics to the pinned baseline order; the multiset of topics and all
other root metadata are unchanged.

The original single CLI authoring invocation exited 1: 46 translated results and
two Korean results rejected for a protected extra digit in an equivalent primary
source term. Its original output and attempts remain preserved. Independent
proposals led to six repaired targets, followed by native image refinements and
new independent reviews. No translation provider retry occurred.

The unchanged official assembler executed once with exit 0. Its first external
post-check rejected topic ordering; a subsequent independent check confirmed
the exact baseline permutation and all other metadata. Read-only finalization
preserved that failure, the original successful child, all prior logs and bundle
bytes. The assembler was not invoked again.

Bundle manifest SHA256:
`58fe016c0fe00a1b3256fdf67a0718d2d6451ee9b90cc5feba1324d3eec28c01`.
The bundle contains 48 new locale documents, four approved source corrections
and 152 assets. Assembly receipt SHA256:
`75cc9b1549566408292607915af231fa8255b43a09742ea0b0de7e1e0f500671`.

The unchanged official local installer and identical-argv replay both exited 0.
The durable journal contains 164 operations. Complete captures include all 12
repository packs, all 152 manifest assets, the entire journal and its original
byte backups, and all 12 article installation receipts. Those captures were
byte-identical before and after replay. Original source media, source/fields,
provider attempts, full external jobs and the private staged inputs are unchanged.
The shared Windows lock file's incidental append bytes are reported separately
and are not included in the replay identity claim. Installation/replay receipt
SHA256:
`feb551e70b55ef01c407dfb24f5a5c040b2e5d8ac345f81fc34f32963674db16`.
An independent complete read-only audit of the installed packs, exact source
corrections, original media, reviews, attempts, backups and current replay maps
also exited 0 with no findings. Evidence SHA256:
`b21754830aecc2f4bd9b1261210d13c8e62eaf0a95b88f4be9af86daadbb96bc`.

Local validation completed with actual exit 0 for the task-board check, scoped
12-pack lint, translation checks, content-pack tests and localization-tool tests.
Content-pack tests recorded 9 passed and 5 skipped; localization-tool tests
recorded 68 passed. Lint retained 60 source-shaped no-summary warnings and 12
text-length warnings with zero errors; the approved documents were not shortened.
Actual local-check receipt SHA256:
`63189b50c0a1db69d136112e1422f06410a56f9badf2717b52ba1f27646f2b79`.
The content commit `7416a9ccbc83e5342319d47f0cf2e87bb9b4d160` passed all 21
actual CI checks. Exact-head receipt SHA256:
`dd4b1accd5189d63c27c77c0e280244d402da6a800482d4c02385acbb965bf4d`.
The final task-record commit is separately checked; these results do not claim
that any later commit automatically inherits the prior checks.

Local validation results and draft PR checks remain separate gates. Before any
merge, the exact current head must pass CI including release-safety. The release
task requires an explicit cohort choice, a fresh production snapshot and source
version checks, deployment preflight without hold bypasses, isolated rehearsal,
dry-run, a verified database backup and durable publication phases. Final
acceptance covers all 60 five-language pages on desktop and mobile, document
hashes, localized assets, links, hreflang and sitemap inclusion.

The prior 32-article publication and the separate 13-article draft PR #1374 are
outside this cohort. The October 8 Taipei snapshot still counted 830 incomplete
published articles after the first 32; locally prepared but unpublished cohorts
are not subtracted from that publication count. No global completion is claimed.

Private snapshots, actor/database identities, original CLI producer identifiers,
machine paths, native inspection images and complete provider logs remain in
the owner's persistent evidence storage outside Git. Local installation state
and staged inputs remain ignored; the repository keeps these sanitized records.
