# Curio L08 / H01 language delivery

**L08 and H01 are delivered as private videos, with English, Japanese and Korean audio, captions, titles and descriptions.** Both backend IDs are bound and their approved-package consumers pass all 59 checks. No public release is included.

Final verification: 2026-10-12T13:00:00.774913Z. Studio shows all nine added components per episode Published. Both existing-ID syncs completed as private; native approved-package consumers rehashed the attachments with `verify_files=true` under read-only transactions that rolled back.

| Delivery check | [L08 · crop circles](https://youtu.be/mLxCEB_wSLk) | [H01 · Mary Celeste](https://youtu.be/efSy-Jxq-s8) |
|---|---|---|
| Original cut | Approved original preserved | Approved 081b cut adopted and preserved |
| Native audio checks | EN/JA/KO: 134/134 each | EN/KO: 118/118; JA: 117/118 plus one owner-accepted clip |
| Local media / captions / package | Verified | Verified with the explicit acceptance below |
| Studio metadata / added CC | Three languages Published | Three languages Published |
| Studio alternate audio | EN/JA/KO Published, WAV | EN/KO WAV and JA derived MP3 Published; saved Studio proof below |
| Language review | af24584f… approved and pulled | 77cb3d4e… approved at 12:53:16.345988Z and pulled, exit 0 |
| Native approved-package consumer | 59 checks PASS, four CC / three dubs, exact ID bound | 59 checks PASS, four CC / three dubs, exact ID bound |
| Private backend sync / metadata | Completed; exact bound ID and four title/description pairs | Completed for efSy-Jxq-s8, private; four title/description pairs were exact before sync from the same approved package |

## Source and original media

The source JSON files remain byte-identical to the imported bb7a production handoff. All 756 translated line entries match the current TC source hashes; metadata, seven chapters per episode and thumbnails are current. The only subsequent text edits are 11 L08 JA lines, one L08 KO line and four H01 JA lines; other line objects and metadata are unchanged. The independent source/text delta review is `source-i18n-final-delta.review.md` (SHA 8c805d4c…). Existing repository validation passed 199/199; that is separate from delivery evidence.

| Preserved artifact | SHA-256 |
|---|---|
| L08 source video.json | `52b151aeda490b8f181d35205c81ddd85317b1412bfdd946e4d27aff12e124d1` |
| L08 original final.mp4 | `46960294ef657d60aba73d62945267d64d7565b039b6705e897c61012315b180` |
| L08 original TC SRT | `a3e073135a8ddcbd0605f2a61e3b5ce241305455e8a75619f4b73234cfdaa7ff` |
| H01 source video.json | `4640edd2f1019570f736e9123022b3577a754ebfa7a67a1fc7b25446ea46ec95` |
| H01 original final.mp4 | `081b4631b45ceb4c88dc5c889bbdf161bceae7eb6dca7b7a2434ff3efc289742` |
| H01 adopted body.mp4 | `9db31e3853a3133141575166956c0e6a1baa56043f4b6ef5f9566e938c7083bd` |
| H01 original TC SRT | `44f56c3e7467b53cd4731fdabf6bbbc14652bb866921cad36ee2b1f9ec8c10ae` |

H01's approved final review is `4c10879f-bf85-45bf-a729-1072a7aabd57`. Guarded native adoption receipt f9bcc997… preserves the exact approved cut and current foreign-language caches; the superseded 15c final and unapproved 473a reassembly are not delivery sources.

## H01 Japanese acceptance and Studio format

The owner listened to and accepted only the existing `mtua` clip, SHA `35877b9ae05adf807feca4699ba4466ccd5a56c6a55076e74a9505b683788c0a`, in receipt `owner-h01-mtua-accepted-20261012.json` (SHA 2f272a5f…). The native record remains **117/118 with one flag**, with **one separate manual acceptance**; it is not native 118/118 or whole-video listening.

Studio rejected the JA WAV. After exact owner permission (a51f339c…), the failed track was deleted and replaced by an MP3 derived from the same verified WAV. No new speech was generated. The canonical/backend package remains WAV; the Studio delivery format differs and is explicitly recorded:

| JA delivery artifact | SHA-256 / evidence |
|---|---|
| Original verified WAV | `ab4d6f3c99f13019204eb5eef59faf8d1414cf2536800282ef4b1ba48ee526b3` |
| External Studio MP3, 27,898,604 bytes | `036a05e9f5f90310f63b2861e7e7b0269420d8545a411cfda30d17a9fef43f83` |
| MP3 local QA | `h01-studio-mp3-fallback/ja.qa.json`, SHA 5e7754fc…; independent review cf06671f… |
| Actual Studio acceptance | `h01-studio-all-three-published-proof.txt`, SHA `176623542e32ae8fa733253754f75bec388ef4e34a124275b88e95b080858568`; screenshot `.png`, SHA `b94a2083d1a93167919dcfbd063ecefd9c783593b6df1ebcb2a4210afbae9013`; all nine components Published at approximately 12:53 UTC |

The MP3 is 320 kbps / 48 kHz stereo. Complete decoding yields exactly 33,475,200 frames / 697.4 seconds, with all-sample comparison at zero offset (correlation >0.999999697, signal/error 62.18 dB). Original WAV/clip/owner pins remain unchanged. This verifies a faithful lossy transcode, not PCM byte equality or YouTube's encoded audio identity.

## Caption and metadata readback

Official downloads contain **1,051 exact cues** across eight tracks: cue numbering/order, timestamps, spaces and internal line breaks match. Counts TC/EN/JA/KO are L08 **134/134/136/138** and H01 **118/119/141/131**; split cues still cover 134/118 source lines per language.

Every downloaded SRT is exactly its packaged file plus one terminal LF. The original strict CRLF-only checker correctly remains **NOT_READY**. Its failure is retained alongside the independent exact-content/format-only diagnosis; no source, checker or upload was altered to manufacture a byte-exact PASS. Evidence: `caption-diagnostic-1791807646592.json` (5a790802…) and `.conclusion.md` (437eda88…). L08's post-sync four title/description pairs, private state and processed state are exact. H01's official pre-sync readback verified the same fields against the same approved package (8df01487…); the completed native private sync then applied that package and retained all four existing captions. No additional H01 post-sync official read is claimed. The final bound consumer independently confirms its exact backend ID and approved package identities.

## Backend identities and decisive receipts

Audit directory: `<home>/mokaair-work/video-language-l08-h01`. `L08-H01-DELIVERY-FINAL.json` indexes full receipt paths, sizes and hashes; historical failures and intermediate runs remain in that directory instead of being repeated here.

| Evidence | L08 | H01 |
|---|---|---|
| Local package proof | d6a63695… | 7f3f7a8e… with explicit owner acceptance |
| Publish review | `d259401a-f720-480d-af51-f5e22b5bb523` approved | `bc10c500-7fbd-4bb7-80b1-3b111dc8fa1e` approved |
| Language review | `af24584f-3c5e-4058-a987-6fad21e3c613` approved | `77cb3d4e-8e3f-4af8-8f46-c0d76d33f4c4` approved and pulled |
| Manifest SHA-256 | `f8457b8b9bf0104f6e1568a2f7d7993f865844fd9981d28ef21f6f5dbb9be679` | `bfce8d81418c367e4f69c74aa83b05e75d0d68e77cb9a603e89ef772570af066` |
| Native language push/pull | Approved pull 3f946b74… | Upload complete 14178385…; approved pull `stages/curio-h01-languages-pull-2026-10-12T12-53-56-306Z-c4ac978d-40a5-4f0b-88fb-9c1b0503d0da/receipt.json`, SHA `f96fa87955005912b62662e93d4c232a4ed48b2d4dd75fae5a9f925cfaae54d2` |
| Native consumer after ID binding | `l08-consumer-postbind-1791808112182.json`, SHA `988423af99cdf877d4435fb77e975a0686b14b26ae9d207eb66a2904268d672e`, 59 checks PASS | `h01-consumer-postbind-1791809997096.json`, SHA `b0869b5efdca71a7052ab012f7d877e6007fba92f077d5467e94ea21c157c691`, 59 checks PASS |
| Private sync / official readback | `l08-admin-private-sync-complete.txt`, bf53b431…; `l08-official-postsync-1791807983784.json`, 32fa6b21… | `h01-admin-private-sync-complete.txt`, SHA `6ff99dc3eee38a186533196e5d650bd96838d62b0d0b111903edc41ba246cae4`; screenshot SHA `0d225de9fcc2bf262e82da9f12e7ce2d7f4ae86580ca24268485c9a15d5f409c`; pre-sync official readback `h01-official-private-1791809045142.json`, 8df01487… |

H01's completed acknowledgment explicitly records native 117/118 plus one owner-accepted clip and the JA WAV-to-MP3 Studio substitution. The approved backend manifest retains the verified original WAVs; the actual Studio MP3 has its own derivation proof above. Historical transport/storage failures remain preserved; this task changed no server quota setting and deleted no review-store content.

## Completion boundary

The completion record separates delivered Studio assets, backend-approved source files and the exact owner audio acceptance. Historical transport/storage failures and intermediate checks remain in the audit directory; they do not replace the final receipts above.

No full-video human listening, complete player playback, public publication or remote encoded-dub byte equality is claimed. Only the specified H01 mtua clip was explicitly listened to by the owner. Source/translations and this record belong in Git; media, runtime receipts and OAuth state stay outside Git.

Task: [complete-curio-l08-and-h01-language](../../tasks/done/2026-10-12-complete-curio-l08-and-h01-language.md).
