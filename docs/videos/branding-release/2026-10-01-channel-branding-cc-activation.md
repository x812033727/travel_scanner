# CC reminder intro activation and existing-cut revisions

The owner approved the v2 opening and selected “先改尚未上架與之後影片” on
2026-10-01. The selected package is now the production and Windows first-build
default. A default change alone does not replace an existing cut or its approvals.
The existing three-second like/share/bell outro is unchanged.

## Selected assets

| Identity | Value |
| --- | --- |
| Package | `mokaair-brand-package-v2-cc` |
| Selection SHA-256 | `a27622022d8d9e2f56221a81a1d7443ab241c40a37a515925784511f0416dcdd` |
| Intro | 150 frames / 5 seconds; `50a53efa54fe5158a166390c7f46518c052be1af005f99a5f3c57e530b0bb67d` |
| Outro | 90 frames / 3 seconds; `8d9546a6042bdc30e0ac597d4eb1452d9e84edc588424027df8f7378ccecf6b1` |

The intro adds the CC icon and “開啟 CC 字幕”. Its original audio packets and
decoded PCM were verified unchanged. Package preparation, desktop/mobile frames
and the synthetic integration test are recorded in
[the preview receipt](2026-10-01-channel-branding-cc-preview.md).

## Default installation actually performed

Production activation completed at **2026-10-01 08:11:19 UTC**, exit 0. The
already-deployed installer ran against the exact existing worker image and work
volume; no application image was built, pulled or deployed.

- Checkout: `7606ff50d719fb4eb61f64b63e3bc1c58a832255`.
- Worker before and after: `cd84e05d1495ab88c93d518f6306772ed5626ee56014af8d87b7052a5555605d`.
- Image: `sha256:8e41d781e3935764c98e3219b028f40eddc394fa58fe84a84ceb55d504f44ee2`.
- Receipt root: `/root/mokaair-channel-branding-cc-20261001-a27622022d8d`.
- Reviewed driver SHA-256: `8d14dcc7f3debf0f00189f0cb9c97f5dbb3203b7e074a0867dbbe8d8499bf6dd`.

The driver held the four deployment locks, acquired its own release hold and
global STOP, waited for the idle worker and stopped that exact container. A
network-disabled one-shot used the same immutable image, with home/docs read-only.
Dry-run, before-current comparison, installation, asset SHA/spec checks and full
decode passed. The original container was restarted and independently read and
decoded the persisted v2 assets. Its source hashes remained unchanged. Only this
operation's STOP and hold were cleared after success.

The installer preserved the old current in history and both v1 media files.
Existing pin/check/timeline/approval/auto/upload-metadata files were compared
before and after while the worker was stopped; they were unchanged. The driver
itself rebuilt, submitted, uploaded and published **zero** videos.

Windows `C:/Users/x8120/mokaair-work/videos/_branding/current.json` was also
installed with the same selection. The previous current was preserved in history;
55 existing cut metadata files remained identical, and both installed assets
passed full decode. Existing per-video pins are deliberately preserved.

A fresh read-only worker readback at 10:14:24 UTC still selected the same package
and exact intro/outro hashes. The original container was running, with no global
STOP and no release hold. The production code revision remained `7606ff50`.

## Coverage and publication identity

The fresh production inventory contains 55 rows:

| Group | Count | Treatment |
| --- | ---: | --- |
| Long videos with confirmed published YouTube IDs | 11 | Preserve videos and URLs |
| Existing completed long cuts without uploaded IDs | 17 | Prepare new independent cuts; renew approvals before use |
| First-build long projects | 7 | Next first build uses v2; missing source/visual stages remain their own work |
| Long project without a local source project (`ai-model-choice`) | 1 | No existing opening established; source work remains incomplete |
| Shorts | 15 | Outside the agreed long-video branding workflow |
| Dropped projects | 4 | Preserve dropped state |

At 08:02:34 UTC the linked channel's complete upload playlist was read successfully:
12 entries, comprising the 11 public videos matching stored project IDs and one
unlisted OAuth demonstration. No additional entry matched the 11 pending projects'
exact title/campaign identity. Shared article URLs alone were not treated as video
identity; Google Vids, AI plans and AI pricing have distinct cuts using shared sources.
The complete channel was read again at 10:14:26 UTC: the same 12 entries, 11 public
project IDs and no active project upload sessions or VPS jobs.

The 11 pending projects' `stage="on YouTube"` is a **next-step** report from
`reviewPush`, not publication evidence: each has exactly one `on_youtube` checklist
item with `done=false`. They have no YouTube ID, publication timestamp, upload
session, API sync state or VPS job. The new renewal guard accepts this explicit
pending checklist, while refusing completed or ambiguous upload states.

## Independent existing-cut candidates

Media and account evidence stay outside Git under
`C:/Users/x8120/mokaair-work/channel-intro-20260930/brand-package-v2-cc/`.

`rollout/final-coverage.json` rehashed all 17 original/candidate full files and
the Windows current/assets at 10:19:40 UTC. It binds the fresh review and complete
channel inventories. All 17 completed unuploaded long cuts have new local finals;
three new finals are present on the site (one approved externally, two pending),
and 14 await explicit owner renewal after code deployment. This operation uploaded
and published no YouTube videos.

| Source group | Count | External evidence |
| --- | ---: | --- |
| Original season imports | 6 | `isolated-revisions/completion-receipt.json` and each cut's `manifest.json` |
| Completed v1 cuts with retained bodies | 6 | `isolated-v1-revisions/manifest.json` and each cut's `receipt.json` |
| Earlier completed slides from approved full attachments | 5 | `rollout/legacy-host-sources-proof.json`; candidate QA in `isolated-legacy-revisions/` |

The six season sources were bound to the latest approved final review and rehashed
after rendering. Their 24fps picture and 96kHz mono audio needed normalization to
30fps and 48kHz stereo; original files remain unchanged, but the normalized picture
and sound are re-encoded. No motion interpolation or new narration was used. AAC
timestamp gaps were preserved using hard silence compensation with zero soft
stretch. Final duration differs from source picture plus bookends by at most one
30fps frame. Captions moved exactly five seconds; the zero chapter stays at zero
and later chapters move five seconds. All six passed complete decoding, frame and
audio duration checks, caption bounds and source hashes. Across 24 speech windows,
48 comparisons have zero sample offset and correlation at least 0.9999798.

The six v1 cuts use their retained bodies, rather than prepending another opening
to an already-branded final. Their existing caption/chapter timing is preserved.
The original body/final/pin/approval/upload artifacts remain unchanged. All six
new candidates passed full decode, frame counts, three decoded body-frame samples,
and exact full-length decoded PCM comparison with their approved v1 finals.
An independent check compared all **98,229 body picture packets**: payload,
PTS, DTS and durations were identical to the approved v1 cuts. All 12 mobile-width
intro/outro stills showed the selected CC reminder and original CTA without clipping.
Their inherited timestamp gaps are retained: actual durations match the old final;
they are not trimmed to a nominal frame-count duration.
Candidate metadata binds the new final and branding hashes and points to verified
caption/thumbnail files. Original metadata and old dub references are preserved
separately; unbound source dubs are not advertised as candidate attachments or approvals.

For the five earlier slides, the approved publish attachment with role `final`
matches the latest approved final review SHA and differs from the 720p `preview`.
The exact stored full files and sizes were verified on the host before copying.
The old `package.final_sha256` field in those packages contains a metadata hash;
it was not used to identify the MP4.

All five legacy candidates passed full decode, exact source/body hashes, every
body packet payload/flags and PTS/DTS shifted by five seconds, three decoded body
frames each, all 25 caption tracks, metadata and real seek audio windows. Their
new finals measure -14.0 LUFS, with true peaks -0.9 dBFS (four) or -1.0 dBFS (jobs),
and no profile problems. All 40 canonical source files remain unchanged.
For RTX/Sora/jobs, the original audio/container end extends past the last picture:
only the maximum-PTS body packet materializes that inherited final-frame hold
(66.667/33.333/33.333 ms); outro begins at original actual AV end plus five seconds.
AAC is re-encoded. Gap lengths persist, but frame grouping moves the visible
gap boundary by 640 samples (13.333 ms), within one AAC frame. Eighteen actual
playback seek windows, including three after gaps, align at +5 seconds with zero
best lag and correlation at least 0.9999928. This is not a claim of bit-identical
audio or a sample-exact complete timeline.

## Review and remaining execution boundary

Imported episode 04 has new final review `404dfcb2-6041-4fef-843e-65b305f7f0cd`,
content SHA `bfbda5ac2783bc5ead96a9b0d6a9dd98e9edd4c28ff983dc12092846e76c59ea`.
Episode 06 has new final review `593ebdc1-d249-4a69-80da-5fd1ea1ac87f`, content SHA
`917525ff5d1a371aa0ce1c6c7987f38d411e8c3fb9f57d20890ce6e2d03c54bd`.
Both previews, thumbnails and shifted captions persisted with their exact submitted
hashes and were pending on submission. A subsequent read-only review refresh found
episode 04's new review had been approved externally; episode 06 remained pending.
This operation did not make that approval or infer full playback from it. Original
approved final decisions and their attachments remain available as history.

Episode 05's first pending revision reported true peak +0.3 dBFS. A new isolated
candidate gently attenuates only body 413.30–413.60 seconds by 2 dB with 50 ms ramps.
Using H.264-copy/PCM internal staging avoids an extra intermediate AAC generation:
the accepted final measures -14.7 LUFS / -1.3 dBFS with no profile problems. Its
15,908 frames, full decode, body picture packets, unchanged captions/chapters and
seven audio windows passed. All tested windows have zero lag; internal PCM outside
the 300 ms change is bit-identical. Failed intermediate AAC attempts remain in the
external evidence. Corrected final SHA is
`d75c405d65b595e6e6d855f759e93046975fc9db755f792b759cfb2a0c5694d4`.
Its guarded replacement was submitted and read back at 09:31:28 UTC as pending
review `68ea82d7-ed07-42f8-9895-17ec30db9856`, with no technical profile problems.
All three submitted attachment hashes/sizes persisted exactly. The failed prior
pending review `db1c0946-8ffb-4c6d-a875-a6df5b344759` is superseded; the original
approved final remains in history. The new cut is not upload-ready.

Episodes 01/02/03 have already-approved language batches. The 11 other cuts have
approved publish packages. Ordinary import or a new final alone cannot revoke
those old approvals, so these 14 require the explicit renewal operation; old
approval files are never deleted and `--force` is not used.

The backend implementation adds owner `GET/POST /admin/videos/{slug}/final-renewal`:
complete-state version, old final ID/SHA and uploaded attachment bytes are checked
under the project lock. Upload activity is refused. Old final/publish/languages/dubs
authorizations are superseded with audit records and retained attachments; the new
final is forced to human pending. Ordinary worker resends cannot overwrite its
evidence, auto-approve it or restore a completed stage. Later package/language
submissions must bind the new final review and media/branding hashes.

The backend, candidate CLI, five-locale owner control and downstream source guards
are implemented and independently reviewed in draft PR #1077, **not merged or
code-deployed**. Staging uses a new output directory and preserves original media,
pins and approvals. The website verifies a local preview's bytes, checks fresh
owner state, submits the replacement once, then reads back its manual-pending
identity. Publish/language/dub producers bind the new final review, current choices,
branding and actual attachment hashes; old worker snapshots remain held.

Validation passed after narration-locale compatibility: 177 related API tests,
full API ruff, full mypy app (447 files) and tests (340 files); 93 focused tools
tests; 1,046 complete tools tests with two existing skips before the final main
update; 40 rebased focused web tests; web lint, typecheck and five-locale i18n.
Independent probes fed actual Node manifests to the Python consumer: 136 scenarios
across English and Traditional Chinese, including 130 compose calls and six producer
rejections, with no unexpected result. The final English R4 report SHA is
`a2cc9f698a53dd3ace9d3e4406a069c7d53181946ed52024e7486b311ca77671`;
the exact producer/consumer source hashes and both R4 reports are bound in
`rollout/renewal-narration-validation.json`.
The complete local web run stalled without completed-suite evidence and was
terminated with exit -1; full web acceptance remains a CI gate. These checks do
not establish owner playback or live website acceptance.

The implementation task `2026-10-01-long-video-renewal-tools-and-ui` is complete.
Canonical worker adoption after owner approval, imported manual-package transfer
and compilation source handoff remain explicitly held in the unclaimed dependent
task `2026-10-01-hand-off-owner-approved-renewed-finals`. This release does not
manufacture missing production evidence or automatically continue those projects.

Main's narration-aware packaging is reconciled with both the renewal guard and
language consumer. Approved narration and automatic zh-TW files are retained;
selected original-language metadata must match the approved default text, and
an original-language dub is explicitly skipped without attaching a duplicate track.
The actual YouTube transport still hardcodes zh-TW default-language fields; that
pre-existing non-zh-TW limitation is recorded in the unclaimed task
`2026-10-01-youtube-narration-request-transport`. All 17 cuts in this rollout are
zh-TW. Offline consumer acceptance is not real YouTube acceptance for other narration.

All 14 renewal staging inputs and body hashes were prepared outside the repository
in `rollout/renewal-stage-inputs.json`. Legacy metadata adapters only copy verified
caption bytes and map chapter fields in candidate directories. No staging upload
or renewal POST for these 14 has been performed. A final read-only refresh at
10:14 UTC confirmed the same three site revisions (04 externally approved, 05/06
pending), 11 public project videos, zero upload sessions/VPS jobs and the unchanged
v2 default in the original running worker, with no hold or STOP.

Before each renewal, refresh both publication/activity evidence and owner version;
submit once and inspect persisted review IDs, hashes, pending state and retained
history. Stale or ambiguous outcomes require a readback, not a blind retry. Owner
full playback/listening, new approval, language-package acceptance and YouTube
upload/publication have not been performed by this operation.
