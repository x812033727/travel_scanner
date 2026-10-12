# Offline recut assembler

`recut.mjs` reads the audited external `source-map.json` and this directory's
`intro-specs.json`. It requires four aligned, checked opening tracks produced by
`speech.mjs`; it makes no server or paid calls.

```powershell
node docs/videos/curio-five-recuts-20261012/recut.mjs --dry-run
node docs/videos/curio-five-recuts-20261012/recut.mjs --slug curio-h02
node docs/videos/curio-five-recuts-20261012/recut.mjs
```

The default output root is
`C:/Users/x8120/mokaair-work/curio-five-recuts-20261012`. Overrides are
`--output-root`, `--source-map`, `--specs`, and `--brand-dir`. A dry run checks the
five originals' final/body hash bindings and reports missing opening inputs. It
does not render or write files.

The original work directories are read only. In particular, H01 uses the native
delivery selected in `source-map.json`, including its existing Japanese review
qualification. That qualification is copied into provenance and QA; it is not
converted into a new clean native-language approval. The code resolves junctions
before checking that source and output directories are disjoint.

An opening audio flag can be cleared only by the separate `retake.mjs`
`readSecondOpinionResolutions` validator: it must identify the exact current WAV,
intended text and a strictly matching independent offline transcript. The original
`check.json` remains unchanged. Every flagged line must resolve; shared alignment,
padding, duration, narration/timeline/caption hashes and receipts still have to
pass. QA records the original flags, the resolved IDs and immutable evidence
file hashes. There is no skip-check option and no owner-listening claim.
The validator additionally supports the three explicitly reviewed U02 Japanese
homophone comparisons, each pinned to its exact WAV and review-package hash;
that narrow review is reported separately from exact/numeric transcript matches.

The new edit has four pieces:

1. The 30–60 second common opening. Every image is extracted from the delivered
   source scene segment, with a gentle 3% push. The default is its midpoint;
   an explicitly reviewed line may set `source_frame` to a zero-based integer
   inside that segment. Unselected keyframe candidates are never used. The four
   new voices share the same frame windows.
2. The existing five-second channel bumper.
3. The original body, starting exactly at `timeline.chapters[1].start_frame`.
   The old hook is removed. Original scene video packets are copied; no full-body
   picture re-encode occurs. Body sound is trimmed on the 48 kHz sample grid.
4. The verified 21-second v4 outro with Golden Hour by Telecasted. Music is only
   in the existing bookends; the assembler does not add a body music bed.

Every locale gets the same exact duration and body start. New opening speech is
normalized to about −14 LUFS. Existing body audio is preserved as PCM before the
one final AAC encode for the Chinese video; foreign delivery tracks are WAV.
The audio gate accepts −18 to −11 LUFS and true peak no higher than −0.2 dBTP
(−0.1 dBTP for the final AAC). These are acceptance limits, not a claim that the
original body was renormalized.

U02 uses `--specs docs/videos/curio-five-recuts-20261012/u02-visual-specs.json`.
It changes only `intro02.source_frame` to 316 of the 395-frame
`secret-compare-versions` segment, after both comparison columns have appeared.
The exact extracted frame and source segment were independently inspected and
hashed; their evidence is in the output root's `u02-visual-probe/`. Its former
small delivery records and end-screen correction receipts are preserved under
`curio-u02/visual-revisions/u02-intro02-before-20261012T134203Z/`. This visual
revision reuses the existing checked audio, then requires a new final QA,
end-screen metadata correction and contact-sheet review.

Each `<slug>/upload/` contains the new `final.mp4`, three WAV dubs, four SRT files,
four localized descriptions, original available thumbnails, revised metadata,
chapters, checksums, and `endscreen-setup.json`. Metadata starts with no new
YouTube video ID and binds all new captions/dubs to the new final hash. Original
reference/image credits and localized chapter titles are retained. Music credit
is added in each language.

All localized titles and descriptions are checked before rendering against 100
and 5,000 Unicode characters respectively. The U02 English description, including
the added music credit, is 4,949 characters in the current aligned plan.

End screens still need setup in YouTube Studio: import template `oxEtlA8GWas`, use
latest upload / best for viewer / subscribe, and place the elements during the
last **16 seconds**. Exact approved-v4 frame inspection found full CTA icons at
+4.000/+4.033 seconds, faint icons at +4.500, and clear slots at +5.000/+5.500.
The first second of the earlier 17-second recommendation covers the transition.
The rendered outro provides the visual slots, not clickable YouTube elements.

After all five renders pass, run the metadata-only correction:

```powershell
node docs/videos/curio-five-recuts-20261012/endscreen-timing.mjs --require-all
```

The frozen batch assembler initially emits the old 17-second
setup. This mandatory postprocessor validates the approved outro and reviewed
probe evidence, moves only the Studio metadata interval to the clear +5-second
canvas, binds it into package metadata/QA/checksums, and refreshes the delivery
index. It verifies all film/audio/CC hashes before and after and records the
unchanged hashes, original JSON backups and correction receipt under each
episode's `postprocess/endscreen-timing-20261012/`. It does not re-encode or modify
any film, audio or caption. `--dry-run` previews; `--slug` can limit the episode;
without `--require-all`, pending final QAs are skipped. A repeat run is idempotent.

`<slug>/qa.json` is written as incomplete while rendering, failed on an error,
and passing only after full AV decode, exact decoded frame count, A/V duration,
loudness, unchanged body packet hashes (decoded frame hashes if container headers
differ), unchanged body PCM hashes, caption boundaries, and source hashes before
and after. `source-provenance.json` freezes the small source records and initial
hashes; the final QA records all inputs. No original approval, owner playback,
upload, publication, or Studio end-screen acceptance is claimed.

## Integration smoke

```powershell
node docs/videos/curio-five-recuts-20261012/recut-smoke.mjs
```

This builds an explicitly synthetic, isolated source under the external output
root, invokes the real assembler and real FFmpeg, and checks its 1,740-frame
result. It verifies body picture packet retention, sample-exact four-language
sound, old-hook caption removal, the new 00:35 body caption boundary, localized
chapter/credit preservation, and reset publication fields. It does not contact
speech services or write into any original episode.

The 2026-10-12 run passed at
`assembler-smoke-1791809473016/output/curio-h02/qa.json` under the external root.
That is test evidence only, not completion of the five requested recuts.
The updated gates passed another integration smoke at
`assembler-smoke-1791810500623/output/curio-h02/qa.json`; the delivery-index
consumer independently verified that synthetic package.

## Refresh delivery status

```powershell
node docs/videos/curio-five-recuts-20261012/delivery-index.mjs
```

This writes `delivery-index.json` and `DELIVERY-INDEX.md` in the external output
root. It rehashes completed videos, all four CC files and three WAV tracks,
checks their final-video bindings, description files, checksums, end-screen
intervals and opening evidence freshness. Missing or changed artifacts remain
incomplete. The H01 Japanese source qualification and any applied independent
opening reviews stay visible. Technical QA and owner playback / Studio setup /
upload / publication are separate fields.

## Extract visual review sheets

```powershell
python docs/videos/curio-five-recuts-20261012/contact-sheets.py --slug curio-h02
```

This requires Pillow and FFmpeg and makes no API calls. After a final QA passes,
it decodes the bound final once and selects exact frame numbers for every new
opening scene midpoint, the bumper, body start/end, and the v4 end-screen canvas.
The source reference pictures are checked against their QA hashes. The output
is `<slug>/visual-review/`: 3×3 sheets with a 640×360 picture per cell, labels
outside the picture, and a hash-bound `review-manifest.json`. Extraction does
not claim a human visual judgment or complete video playback. Omitting `--slug`
processes only episodes whose final QA already passes.
