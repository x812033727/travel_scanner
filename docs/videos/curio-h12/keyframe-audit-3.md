# H12 final selected-keyframe audit before storyboard review

2026-10-17. This receipt covers the 86 selected illustrated scenes in `<home>/mokaair-work/videos/curio-h12`. It does not record owner approval or a finished video.

| Evidence | SHA-256 / result |
| --- | --- |
| Approved spoken `script.md` | `408E3C8BAAFC0063B0B53410B579D14BA09D650753DB466A409E59470F9A620B` (93 lines, unchanged) |
| Approved `timeline.json` | `792DC6C9D010FA7EE94884F7631CD3362D1496AF600A2BF7A14381A0D767F699` (body 08:04.200, unchanged) |
| Visual `video.json` | `5AC5C6CEB1DF801BE0FCFD109BE8EE1CE291BEDFBD16F1D91D9EB11BDC94C13D` |
| Selected `keyframes/manifest.json` | `F61238CD938140C8467501B376183A1865DC20D18DFCCC2FFA91504C26A475AB` |
| Local `media/ledger.json` | `9B8C6A05F719FC0A6109B62F9F7CAAD1955349B9796FE10D484C51AABFCE6F51` |

The preceding six image-repair passes and their rejected takes remain in the media workdir and earlier audits. In the final bounded pass, `slate-later` seed 3 was rejected (painterly style, letter on slate); `extinguish-time` reused the cached `work-date-inference` seed 1 image and received its own 9.29/10 PASS judgment. This pass added one image and two judge calls, US$0.0235 in the local media ledger. The five-episode shared stop ledger was reconciled to H12 US$4.185/6 and batch US$25.0295/39, both conservative estimates rather than vendor invoices.

`slate-later` had exhausted three takes and two prompt revisions. Its selected image now points to same-chapter `slate-entry-3.jpg`, SHA-256 `1BD67BCF5524C7B8007932057068127907FB6157508533AACD0F8C4072AE6360`. The source was independently judged 10/10 PASS for the same prompt and camera. The target manifest records `reused_from` and retains the rejected take under `rejected_takes`; no rejected image was relabelled as passed. The source and target occur at 166.47–172.67 and 182.30–187.27 seconds, separated by two scenes, so the repeat is visible as a return to the slate.

`extinguish-time` and `work-date-inference` use the same approved slate-and-pot picture at 193.27–197.03 and 201.13–206.83 seconds, with one 4.10-second intervening scene and the same `push in` move. The slate carries the first line, and the pot joins the inference later; the short-range visual repeat is conspicuous and should be inspected by the owner. Other deliberate same-file pairs are `kitchen-door`/`kitchen-work` (over 130 seconds apart) and `poem-recalled`/`kitchen-recalled` (about 19.4 seconds apart).

An independent reader inspected all four current contact sheets against the narrated lines and checked high-risk selected images at full size. All 86 selected files exist, are 1280×720, and match their manifest SHA-256; all selected judgments pass and `needs_review` is false. No selected image was found to directly reverse a narrated fact, or to be photographic, fully 3D, or letterboxed. This is not a claim of zero editorial defects. `platform-height`, `box-location`, `box-height`, and `inspector-lands` convey their stated location or height weakly; `coat-left` and `others-clothes` differ in coat colour. The owner should consider those shots along with the repeated slate/pot sequence.

`lint --slug curio-h12` returned zero errors and seven warnings, including the two repeated visual prompts. `keyframes --shot slate-later,extinguish-time --takes 1` kept both selected images without any new generation and rebuilt four contact sheets. The CLI status now marks keyframes drawn and storyboard approval pending. The storyboard may be sent for owner review; rendering and assembly must wait for a hash-bound storyboard approval.
