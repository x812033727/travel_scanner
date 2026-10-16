# Five Curio remasters

The owner requested new complete versions for later reupload, with narrated
condensed openings, end-screen links and music. English, Japanese and Korean
openings and full audio tracks follow the same new timeline as Traditional Chinese.

The working delivery directory is
`<home>/mokaair-work/curio-five-recuts-20261012` until the five
private Studio uploads and backend links have been checked. The verified VPS
copy and recovery commands are in [RESTORE-FROM-VPS.md](RESTORE-FROM-VPS.md).
`DELIVERY-INDEX.md` inside the working or restored directory links the films
and all language assets. The saved `delivery-index.json` records the original
delivery check; it is not a fresh post-restore acceptance result. Verify an
untouched restored snapshot with its `backup-verify.py` as described in
[RESTORE-FROM-VPS.md](RESTORE-FROM-VPS.md). Do not run the index writer in that
immutable snapshot: it rewrites manifest-listed files, and some evidence paths
still name the original working location. A new readiness review needs a
separate working copy and explicit rebasing of those evidence paths. The source
map also references separately retained original source directories.

| Topic | Directory | Final opening specification |
| --- | --- | --- |
| Roanoke / CROATOAN | curio-h02 | intro-specs.json |
| Area 51 | curio-u02 | u02-visual-specs.json |
| Tunguska | curio-h03 | h03-pronunciation-specs.json |
| Crop circles | curio-l08 | l08-wording-specs.json |
| Mary Celeste | curio-h01 | intro-specs.json |

Each `upload/` directory contains `final.mp4`, four caption files, three full
language WAV files, localized titles/descriptions/chapters, thumbnails,
`endscreen-setup.json` and checksums. Full media is kept outside Git.
The completed batch and final hashes are recorded in [DELIVERY-REPORT.md](DELIVERY-REPORT.md).
The new private Studio IDs and their separate backend project mapping are in
[STUDIO-AND-BACKEND-LINKAGE.md](STUDIO-AND-BACKEND-LINKAGE.md); the VPS recovery
procedure is in [RESTORE-FROM-VPS.md](RESTORE-FROM-VPS.md).
The path-only specification scrub and historical hash bindings are recorded in
[PORTABILITY.md](PORTABILITY.md).

The film order is the new narrated opening, the five-second channel bumper,
the original second chapter onward, and the approved 21-second outro with
Golden Hour by Telecasted. Source picture packets and body PCM are compared
with the retained originals, alongside full decode, exact frames/samples,
caption boundaries and audio levels.

For each new upload, position the best for viewer, subscription and
latest-upload elements in the **last 16 seconds**.
The preceding second is a visible CTA transition. The rendered slots themselves
are not clickable YouTube elements; the setup JSON supplies the exact new times.

Read [ASSEMBLER.md](ASSEMBLER.md) for rendering and the required metadata-only
end-screen timing correction, [RETAKES.md](RETAKES.md) for cached speech and repair
provenance, and [independent-review.md](independent-review.md) for editorial and
independent technical review.

Automated checks and sampled frames are separate from owner playback, upload,
publication and Studio acceptance. The original H01 Japanese body's existing
117/118 native-clear plus one owner-accepted `mtua` qualification is preserved.
The unchanged H01 reconstruction certainty and U02 declassification wording have
separate follow-up tickets; this opening remaster does not reapprove those bodies.
