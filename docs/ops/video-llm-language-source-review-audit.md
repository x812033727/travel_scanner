# LLM language source review audit

The owner requested source/metadata repair for the video titled
「大型語言模型是什麼？會接話，為什麼不等於查到資料？｜AI 名詞十分鐘」.
A production title query identified exactly one project:
`ai-term-large-language-model`, ID `d81b7b79-89ed-4137-8584-21a66d2ae189`.
The video slug was established from its actual title, not inferred from the
article slug `what-is-a-large-language-model`.

The requested legacy-language defect does not reproduce for this project.
At both 2026-10-04 23:23:49.970279Z and 23:23:54.811890Z, the deployed actual
`read_approved_package(..., verify_files=True)` passed. The owner's persisted
choice is `locales={}`, decided at 15:36:31.277219Z: original Traditional Chinese
only. There are no language-review rows to repair or existing translated
attachments to resubmit. This is a completed request audit; no new review was
submitted.

## Approved source and actual consumer result

The latest approved publish review is
`cbf8689a-a38a-48fc-bce8-51e15188980d`, with content SHA-256
`0420dd643a2f855d97682f90032098b7bfe93ba074285e90a1d113fb78b28797`.
The latest approved final review is
`20e62a79-4a76-4639-a218-4a09d5ce226c`, with content SHA-256
`aec91b1ffb5d5e18a8348432bbc9ab7cd4bad98459d3349b4c5e24cde850685b`.
Their identities, complete public payloads/files, statuses and original decision
timestamps remained unchanged between the two reads.

The returned actual package has:

- `default_language="zh-TW"`, `localizations={}` and captions only for `zh-TW`.
- `approval_pin.publish` equal to the publish identity above,
  `approval_pin.languages=null` and `approval_pin.choice={}`.
- Full final size 363,549,695 bytes and final hash equal to the final review and
  metadata `final_sha256`.
- Branding hash
  `a27622022d8d9e2f56221a81a1d7443ab241c40a37a515925784511f0416dcdd`,
  equal to the actual final payload and package metadata.

The actual final payload contains `branding_hash`; its `speech_hash` and
`compilation_hash` keys are absent. The audit preserves key absence instead of
inventing explicit null source fields.

All five publish attachments and all three final-review attachments were read
from their real ReviewStore files at both ends. Each was a regular, non-symlink
file with the expected complete byte count and SHA-256, and stable file identity,
size and modification time while hashing.

| Review | Role | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| publish | captions_zh-TW | 14,360 | `e641fdd7efc5be38bca1e97afad79066cb8b34f4f553c64251fbca8fe4fcd1cd` |
| publish | description_zh-TW | 2,891 | `f6bbea7ca6a9c9db758b6346351c0b0c0f2895cb9b063aca2fe5d5297fe32002` |
| publish | final | 363,549,695 | `aec91b1ffb5d5e18a8348432bbc9ab7cd4bad98459d3349b4c5e24cde850685b` |
| publish | metadata | 4,632 | `0420dd643a2f855d97682f90032098b7bfe93ba074285e90a1d113fb78b28797` |
| publish | thumbnail | 137,077 | `30d9fc6484a375fe17acec9b7acb46e9701e7d9c9547a59e7ec2ac246eb0c56e` |
| final | preview | 41,361,703 | `e5fff77f47dd7fc8f05bf8a718c88677eebdb2d6b72ec5c761ff8f0b5be85db5` |
| final | contact_sheet | 1,510,009 | `0e08bdade8618553c7a8ae529a16f173f9ecc84842f1af170d56d3f5eaabdcf5` |
| final | thumbnail | 137,077 | `30d9fc6484a375fe17acec9b7acb46e9701e7d9c9547a59e7ec2ac246eb0c56e` |

The deployed source modules used for this actual check were:

- `app/video_youtube/language_package.py`:
  `74b8abfa8baa1e69cf9c7876015d08b21b6907c77c796e36fd76fb8f12887ecb`.
- `app/video_youtube/sync.py`:
  `76c962cc2ea009d965950cee551babab3ea6030756b4fc37a4e9eb5d62b4f7b7`.

## Protected state and limits

The project reports the stage string `on YouTube`, but its actual
`youtube_video_id`, `youtube_publish_at` and `youtube_removed_at` are all null.
There is no upload session or `youtube_sync` state. The stage string does not
establish upload or publication. No YouTube action was attempted.

The current owner is active with effective role `owner`, user ID
`42917354-9946-4f7e-be83-5d5526f8d5e1`. Owner, choice, retry IDs, approved sources
and these protected configuration hashes remained identical at both reads:

- Automation settings:
  `8682e20b9c721ae868afa6cef9fa2a7fe74cefef4d34381e5a633ad75ec5973e`.
- Uploader configuration:
  `e11a2c8f443bdee3a4e108a5efd44098dd942e33b79fcbcff769727e7a9cd8cf`;
  uploader disabled.

No active scoped media or durable-stage jobs were observed. A narrow worker
process check found no same-slug argument, and the fixed candidate namespace
`/var/lib/mokaair/video-work/ai-term-large-language-model/review/ops/llm-language-schema1-20261005`
and its POST intent were absent. These observations are snapshots, not leases.

The native paths `/opt/mokaair/docs/videos/ai-term-large-language-model/video.json`
and the corresponding canonical language/metadata files were absent. This limits
a native-source inspection; it does not establish failure of the real approved
ReviewStore package. No generated-source search or regeneration was performed.

The SQL transactions were explicitly read-only, with zero dirty/new/deleted
session objects at both ends. This operation used SSH for reads only: zero HTTP
calls, provider calls, paid calls, host-file writes, review submissions, approvals,
worker restarts, YouTube actions or deployments. No credential was printed or
stored in evidence. The only repository changes are this audit and its task notes.

## Evidence

Local evidence files are in `<temp>`; the full proof retains complete public
source/review records, actual returned packages and first/end file verification.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `mokaair-llm-language-package-readonly-20261005-evidence.json` | 65,639 | `2f3b4c338bd24e36c67df9c5e85a5fb387074c26465279690a669532ba0dcb28` |
| `mokaair-llm-language-package-readonly-20261005-compact.json` | 5,460 | `7cd0a5feebd043562b6ff54fd32d09a2b87e9aafdbeb6e883289babed8e04c00` |
| `mokaair-llm-language-package-final-readonly-20261005.log` | 61,786 | `919cd175a407f777eccd46b610f72226044a54febc4b47068430984dc7695764` |
| `mokaair-llm-language-package-readonly-20261005-publish-metadata-original.json` | 4,632 | `0420dd643a2f855d97682f90032098b7bfe93ba074285e90a1d113fb78b28797` |

The source-bound local evidence assertions passed all 21 checks, including both
actual consumer passes, eight genuine file references, exact source identities,
original-only choice, no language review, clean sessions and protected-state
stability. No hypothetical approved language review or mock media was substituted
for the production package.

There is no missing-language attachment repair to perform for this exact video
at this snapshot. Do not add a locale, manufacture a legacy review or submit an
unrelated package to match the number of videos in the owner's request. Any
future language choice or different review requires its own fresh source audit.
