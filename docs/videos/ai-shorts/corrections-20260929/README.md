# 2026-09-29 Shorts corrections

The owner requested corrections after the live audit of 15 pending Shorts. This directory holds the three revised lab scripts and the dated final-review submission helper. The 12 season-one cuts use `docs/ai-video-season-01/tools/rebuild_shorts.py` and its adjacent correction notes. Original experiments, old renders and prior review evidence remain intact.

Media, independent `verify.json` files, full-decode logs and authenticated backend receipts live outside Git in the dated `shorts-fixes-20260929` work directory. The final external manifest identifies the exact build directory, script hash and video hash for each corrected Short.

## Verification and resubmission

From the repository root, with an external manifest containing `entries: [{ slug, directory, document_sha256, final_sha256 }]` (a bare array also works):

```powershell
node docs/videos/ai-shorts/corrections-20260929/operations/review.mjs --action audio --manifest <MANIFEST.json> --receipts <OUTSIDE_REPO>
node docs/videos/ai-shorts/corrections-20260929/operations/review.mjs --action qa --manifest <MANIFEST.json> --receipts <OUTSIDE_REPO>
node docs/videos/ai-shorts/corrections-20260929/operations/review.mjs --action submit --manifest <MANIFEST.json> --receipts <OUTSIDE_REPO>
node docs/videos/ai-shorts/corrections-20260929/operations/review.mjs --action confirm --manifest <MANIFEST.json> --receipts <OUTSIDE_REPO>
```

Install each independently authored `verify.json` into its build only after comparing `document_sha256` with the exact `script.json` bytes. The audio action reuses a completed check only when both its words and ordered audio bytes match. A failed check is retained until its audio or words change; repeated recognition is not used to obtain a favorable answer.

The QA action runs the existing twelve checks and writes an additional binding for the script, final video, QA report, narration check, independent fact receipt and measured layout receipt. Submission refuses stale bindings, uploads the preview and evidence, and sends only `gate: final`. It does not create an upload package, call the publish gate, change settings or start the scheduler. Reloaded review hashes, QA items and attachment hashes must match the submitted values. `confirm` independently reloads the current final record again.

## Remaining owner decisions

At correction time, the shared channel stance was empty. The following proposed editorial principles were presented to the owner and have **not** been applied without their answer:

> 以可追溯來源與可重現實測為依據；區分事實、推論與意見；單次實驗不推廣成普遍結論；交代 AI 能力的版本、條件與限制；尊重隱私及素材授權。

The twelve cuts' parent videos have approved final reviews but no public full-video URL. Their metadata/link checks must remain incomplete until a real public URL exists. No review URL or invented address substitutes for that link. Automated narration matching, fact verification and technical checks do not establish owner listening, phone playback acceptance, YouTube upload or publication.
