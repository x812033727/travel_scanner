# Gemini language-review resubmission, 2026-10-07

The owner requested resubmission of these two videos after the YouTube package
consumer rejected their approved legacy language reviews:

- `gemini-skills-replace-gems-move-checklist`
- `gemini-4-argon-who-can-use-it`

The exact rejection was `video_youtube_languages_invalid`:
`舊語言審核缺少可驗證的來源清單與 metadata，請重新送審`.

## Cause and repair boundary

The normal language producer attached the existing descriptions, captions and
available dub tracks but omitted `metadata` and `languages_manifest`. Its content
hash covered a legacy speech/choice/parts artifact. The current consumer requires
the source manifest's actual hash, current approved publish/final identities,
branding and speech hashes, current selected parts and actual attachment proofs.
The renewed-final producer already has a separate binding path.

This operation stages only the two missing JSON proofs and resubmits the existing
language assets through the official review endpoint. It preserves the original
final and publish approvals, four selected locales, media bytes and all explicit
dub skips. It generates no new translation, image, speech, dub or video, and sends
no YouTube upload or publication request.

Both canonical worker states were `done`. Neither project had a YouTube ID,
schedule, upload session or synchronization state at preflight. All proposed source
identities and selected attachment hashes are checked again before submission.

## Validation and result

Both frozen candidates passed the deployed API's real `read_approved_package`
with actual attachment verification before submission. This preflight used a
read-only database transaction and an in-memory hypothetical approved review;
it did not change or manufacture a persisted approval.

Each official review POST ran once. Readback confirmed the exact new content
hash, selected attachment descriptors and original language payload. The original
canonical language artifact was archived, then atomically aligned to the exact
new source manifest. Local approval files remained unchanged.

| Video | New language status | Actual consumer result |
| --- | --- | --- |
| Skills/Gems | Pending | Correctly waits for the owner's English dub confirmation |
| Gemini 4 Argon | Approved automatically | Accepts the actual stored metadata, source manifest and selected attachments |

Skills/Gems manifest SHA-256:
`cdf0722fe76c989759f51d50037f89494a10ce9ede2a16d60b1281babea65695`.
Argon manifest SHA-256:
`7bf8822b7798f9d843b7eef451c9ce4291218be89347ac0d9d07e92caf2d258d`.

Independent post-validation rehashed all stored attachments and confirmed the
original approved final/publish identities, metadata, four selected locales,
language payloads, original language reviews and absence of delivery state.
Argon's actual composition passes. Skills/Gems now reports
`最新語言包尚未核准，請完成語言審核後再送出`; a separate in-memory approval
simulation passes its actual new stored bytes, proving the remaining blocker is
the owner gate. No old language decision was copied into the new review.

The Skills/Gems video has one existing English dub. Its fresh language review
waits for the owner. Japanese and Korean dubs retain their recorded quality/length
skips. Argon's three selected dubs retain their recorded skips, so its new review
was approved automatically under the existing rule.

## Native producer follow-up

The normal-producer repair is filed separately as
`2026-10-07-normal-video-language-submissions-omit-source`. Its source scope remains
held by another task. This operation is not a deployed native-emitter fix and does
not change the renewal implementation or PR #1359.
