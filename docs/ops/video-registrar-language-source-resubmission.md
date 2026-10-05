# Registrar language source resubmission

Project: `cloudflare-registrar-renewal-price-ai-agent`.

The owner explicitly requested a replacement language review for
“網域第一年便宜，第五年呢？Cloudflare 把續約價擺上搜尋結果，還讓 AI 代理能替你下單”.
The request authorizes supplementing existing successful results with their
verifiable source manifest and metadata. It does not authorize new speech
generation, approval, YouTube operations or deployment.

The deployed consumer reproduced `409 video_youtube_languages_invalid` with
“舊語言審核缺少可驗證的來源清單與 metadata，請重新送審” for approved legacy
review `2b5511ac-c76c-4585-a42a-85cd1498b5fd`. That review was created at
20:39:42.159945Z and owner-approved at 22:45:27.764923Z on 2026-10-04. Its ten
ReviewStore attachments and matching canonical sources have verified sizes,
stable file identities and SHA-256 values: four descriptions, four captions,
and the successful English and Japanese dub tracks. Korean retains the original
explicit Jev skip reason; no partial Korean track is attached as a completed dub.
Simplified Chinese has metadata and captions selected, without a dub.

The candidate binds the existing approved sources:

- Final review `cca331ef-ed04-47a6-bb27-8d720e68a807`, approved at
  16:20:43.225810Z, SHA-256
  `9486f51d9420c2ce52d7fded96703f3f090a10cf43f07d12e0950f460d8ecd18`.
- Publish review `75b86a9b-7b85-4494-9474-4e82b6d7c1a4`, approved at
  16:32:58.880801Z, original metadata SHA-256
  `cf71a3b47234726a62b0055d68a0ffcfef7e1012b229d1d6dde1f1ef131693f8`.
- Unchanged current multilingual metadata, 14,685 bytes, SHA-256
  `67c368ba3686431f2ae5b5a7b2d9bb6a0f37fbb00f535fffaa456063b2b9dd99`.
- Original language choice decision at 16:20:49.003211Z; source speech hash
  `c2bfbd6283dae674`; branding hash
  `a27622022d8d9e2f56221a81a1d7443ab241c40a37a515925784511f0416dcdd`.

The final review retains “成片 07:54，自動品管 4 項沒過：assemble、pace、captions、policy”.
Owner approval and these original findings are preserved. The supplement does
not waive a quality finding or claim that this review changes the final video.
Only the branding source key is present in the original final payload; absent
speech/compilation keys must remain absent rather than becoming invented nulls.

The new schema 1 manifest includes the source identities, exact choice decision,
unchanged locale payload and eleven attachment descriptors: the original ten
plus metadata. The review additionally attaches that manifest, for twelve refs.
The four description bytes match the existing localized metadata serialization.
The legacy canonical language manifest, original metadata, source files and
reviews are preserved.

Read-only evidence was sampled from 23:13:20.467111Z to 23:13:25.733925Z on
2026-10-04. Compact evidence SHA-256:
`8767dd0aa0d6b26b99c43d13a446a28a92b89ac0af991ab7742dc87824226f03`.
Full evidence SHA-256:
`1ff96b82be636e653a9cbb5a4958d51daa86f0582f60be123f7e92a0d57c4d9f`.
The snapshot confirmed the active effective owner, exact acknowledged retry,
unchanged choices, no active item jobs or item locks, no upload session, and no
existing fixed intent. These observations are snapshots and do not exclude a
later producer. A fresh launch preflight remains mandatory.

Protected settings SHA-256 is
`8682e20b9c721ae868afa6cef9fa2a7fe74cefef4d34381e5a633ad75ec5973e`;
uploader settings SHA-256 is
`e11a2c8f443bdee3a4e108a5efd44098dd942e33b79fcbcff769727e7a9cd8cf`.
The global media cap remains 20 dollars and the uploader remains disabled. No
paid call, source/settings write, provider retry or worker restart occurred.

The temporary builder and Registrar-only driver passed 14 zero-network Node
cases using the real request adapter and normal Automation language flow, plus
12 actual backend contract cases. Independent whole-source review found no
important blocker. Tests cover source/choice/decision drift, exact old payload
and refs, report-file appearance before dispatch, original Korean skip, permanent
intent refusal after lost/malformed/401/400 responses, and pending language state
preventing a legacy package resubmission. Backend fixture composition uses
`verify_files=False`; the ten real large attachments are established by the live
read-only byte proof rather than fabricated fixture files. No real approval or
database write occurs in these tests.

The bounded operation is two content-addressed small JSON PUTs and one review
POST. Its fixed durable receipt directory is:
`/var/lib/mokaair/video-work/cloudflare-registrar-renewal-price-ai-agent/review/ops/registrar-language-schema1-20261004`.
The driver saves intent before POST, raw response before parsing, then accepted
identity and readback. An existing intent permanently prevents another POST;
changing the directory cannot bypass this guard. Existing YouTube ID and
publish/removal timestamps are pinned exactly if present and never changed.
The operation uses no YouTube endpoint.

The frozen manifest is 4,239 bytes with SHA-256
`56699d993c077ed8011626a28b87073bce9ef3ca6f9521af51872e75d59f49a5`;
the review request is 3,797 bytes with SHA-256
`c31f2a841a3047db7c9e04abbf273d54448f477047af3801c520a7e872c85189`.
Freeze record SHA-256 is
`6bbabc3bd2692cca1e1fd451e670ef8169e6759c1d6c91e07623f58490d2ce4d`.

A fresh pure read-only preflight at 23:34:17.328653-23:34:22.481973Z confirmed
the original sources, ten stored attachments, owner, settings, acknowledged
retry, absent active upload/session, item jobs, locks and fixed intent. Full proof
SHA-256 is
`d01b21c1888f93f56c357c192a3b225b0aa0d119e444e7b7aed621d6e107f3dc`.
Only the canonical choice file's worker `synced_at` changed; locales and the
original choice decision remained exact. This existing driver exception was
verified against raw bytes without replacing the frozen baseline. Same-read
comparison proof SHA-256 is
`11dda3edcbd4941bcdd74b826247a2070ea0a19dcca6f635ef96e08155932dfd`.

Root completed the reviewed one-shot operation with exit 0 and empty stderr.
New language review `4b83ae77-ddce-438b-8121-10612541b5e0` is pending, with the
exact manifest hash above. The fixed namespace now contains durable submission
intent and response/acceptance/readback; it must never be submitted again or
bypassed with another namespace. Submission output SHA-256 is
`dc8941bc3c53306b6e41bdf8004b6958006905b7b2241d47b2d0c1d0fb9b0af2`.

Actual-only post-submit verification completed at
23:53:53.983698-23:53:59.462664Z with 30/30 guards passing. All twelve new and ten
old ReviewStore attachments match their actual sizes, SHA-256 values and stable
file identities. The stored metadata is exactly the original 14,685-byte current
file; the stored schema 1 manifest has the exact source, choice, locale payload
and attachment inventory. All five durable receipt files match their recorded
request, raw response and accepted/readback identities and remained stable.

The new review remains pending with no decision actor or timestamp. The original
language approval at 22:45:27.764923Z, final/publish approvals, canonical legacy
manifest, successful EN/JA tracks, exact KO skip, original choice, acknowledged
retry, effective owner and protected settings were preserved. No active item
jobs, item locks or exact-slug native marker were observed; these remain
snapshots rather than a lease or producer exclusion. Database sessions had zero
dirty, new or deleted objects throughout.

The actual consumer with `verify_files=True` returns
`409 video_youtube_languages_invalid` with
“最新語言包尚未核准，請完成語言審核後再送出”. This is the expected owner-review gate,
not the former missing source/metadata refusal. No hypothetical approval or
memory overlay was used. The reader ran once with exit 0, empty stderr and zero
HTTP/provider calls or remote filesystem/database/Redis data writes.

Final full evidence is 182,397 bytes with SHA-256
`0f64e1095102a76128d71868d5dc29d9dc793fae3364e5319a7236658c20049f`.
Compact evidence is 78,624 bytes with SHA-256
`0459a4ce070f07e2ec35adf6f822c6b64c8c5cd55d01563f34f0a6fab428f96d`.
Raw reader output is 132,909 bytes with SHA-256
`a1fcf5a0efefd3eb61c1f5a9b18431d20b280c845ba27c51f10c4484a04c7c8d`.
No speech generation, owner approval, source change, worker restart, deployment
or YouTube operation occurred. The source/metadata supplement is delivered for
owner review; submission is not approval, upload or publication.
