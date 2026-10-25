---
name: editable-explainer-skill
description: Build an editable educational animation from supplied facts. Use when precise labels, numbers or diagrams must remain easy to revise and verify.
---

# Editable teaching animation

Use one learning question and one concrete example. Agree on the expected result from supplied evidence before drawing. Do not describe generated footage or a model response as a real product test unless that test happened and its records exist.

## Workflow

1. Separate the supplied facts, editorial choices and missing information. Keep the actual source notes with the project.
2. Write a short visual sequence. Each state explains one thing and can be checked without relying on attractive motion.
3. Keep editable content in a data file and rendering behavior in source code. Deliver both. For the bundled dice example, see `../lab/lesson.json`, `../lab/render_lesson.py` and `../lab/install.txt`; its renderer supports only the documented dice case and zh-TW.
4. Validate data before rendering. Use an independent known answer, not merely the renderer's own count. Run a valid case, a modification and an invalid input. Preserve real output and exit codes.
5. Render still previews first. Check labels, clipping and the intended small-screen viewing size. Then render the actual video and measure its duration, dimensions and audio streams.
6. Change a meaningful parameter. Inspect every affected title, graphic, count, narration draft and subtitle draft. A parameter shown in the opening can also become stale.
7. Synthesize or record final narration, measure it, then set the real visual and caption timing. Designed scene windows are not measured speech alignment.
8. For each additional language, retain facts and limits but use natural phrasing. Check timing, pronunciation and captions separately. Do not claim changing a locale code translates a renderer.

## Completion evidence

Provide the editable files, reproducible commands, actual rendered media, measured media properties and the accepted checks. Keep failed checks and the fixes visible. Preserve source versions so a later edit does not silently reuse an old approval.

Only claim the output that exists. A silent example is not a narrated film. A source archive is not an installed Skill. A completed audio track is not an upload to YouTube Studio. Publishing remains a separate authorized action.
