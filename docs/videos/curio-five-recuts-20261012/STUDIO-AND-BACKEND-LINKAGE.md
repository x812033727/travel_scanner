# Studio reupload and backend version map

The five remasters are **new video versions**. YouTube gives each new upload a
new video ID; it cannot replace the media at the original URL. A direct Studio
upload does not automatically update Mokaair's video admin record. Keep the
original backend project and its YouTube ID unchanged, and link each new ID to
a separate `-recut-20261012` project after Studio confirms the private upload.

| Episode | Original project and YouTube ID | New project | New private Studio ID |
| --- | --- | --- | --- |
| Roanoke | `curio-h02` · `6hswTvAftUA` | `curio-h02-recut-20261012` | `4gJhMFqYqC4` |
| Area 51 | `curio-u02` · `uZ9TlblvrCw` | `curio-u02-recut-20261012` | `NazQDspY5nk` |
| Tunguska | `curio-h03` · `b98IdS1MB78` | `curio-h03-recut-20261012` | `JjM04OmwBjU` |
| Crop circles | `curio-l08` · `mLxCEB_wSLk` | `curio-l08-recut-20261012` | `LQ0pV9vZdeA` |
| Mary Celeste | `curio-h01` · `efSy-Jxq-s8` | `curio-h01-recut-20261012` | `2gdgYmiYTSk` |

All five new uploads were subsequently read back in Studio as **private**,
processed full-length videos. Their four caption languages and three clickable
end-screen elements have also been read back. All 15 supplemental audio WAVs
were submitted, but Studio still reported them as processing at the latest
check; this is not a completed dub or owner playback result. The owner reserved
the public-release decision until final checks pass. The original H01, H02,
H03, U02 and L08 IDs must not be replaced, deleted or made public as part of
this batch. An additional private, same-title L08 ID `XSFNRORVuYo` exists and
is not part of this version map.

U02's English Studio description was trimmed by one redundant dossier sentence
after the upload because Studio's saved version measured 5,011 UTF-8 bytes.
The final Studio text was reloaded and matched the sidecar at
`<home>/mokaair-work/backup-receipts/curio-u02-studio-description.en.final.txt`
(4,970 UTF-8 bytes; SHA-256
`0f265f508d749999355e8a5262b97e0710f9b19745411644c7671d5763954277`).
Its chapters, sources and Golden Hour credit remain. The frozen upload package
was not changed. The backend import stores only Traditional Chinese metadata,
so this English Studio correction requires no backend reimport. The sidecar and
its receipt were copied to the VPS `operations/studio-overrides/` directory and
independently hash-checked.

Each separate backend project was imported with a 720p review preview,
thumbnail and Traditional Chinese caption attachment. Its imported `final`
review remains **pending**. At the latest authenticated backend readback, all
five new projects still had `youtube_video_id=null`; the original five IDs were
unchanged. The admin page currently hides the manual link form for these
pending imports. The proposed UI repair is a narrow, capability-guarded
private-link action that records the new ID without approving the review or
publishing the video. Until that repair is deployed and each ID is read back,
the backend linkage is incomplete.

Studio evidence is saved outside Git in
`<home>/mokaair-work/backup-receipts/curio-five-recuts-20261012-studio-progress.json`.
The final readback receipt must establish each new video's private setting,
duration, thumbnail, four published caption tracks, three published dubbed
audio tracks and the three clickable end-screen elements in the last 16
seconds. Backend readback must establish each new project's exact new ID and
confirm that each original project still holds its original ID. The separate
VPS backup must be verified before the C: delivery copy is removed; see
[RESTORE-FROM-VPS.md](RESTORE-FROM-VPS.md). Automated media QA does not stand
for the owner's full playback or public-release approval.
