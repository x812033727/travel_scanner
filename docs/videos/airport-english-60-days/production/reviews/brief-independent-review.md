# Independent review: airport outline brief correction

Reviewer: `airport_brief_independent_review`  
Reviewed on: 2026-10-08  
Workspace: `/workspace/airport-pr`  
Baseline: committed `HEAD` (`4c1b5ae8126b406ca9ecc3f130b2a214adfd0e1c`)  
Verdict: PASS for the narrow generator and brief changes. No blocking or non-blocking defects found.

## Scope and constraints

Read `AGENTS.md`, the `youtube-video` and `task-board` skills, the automated video reference, and the active remediation task. Independently reviewed the uncommitted changes in `tools/video/airport_english/prepare.mjs` and `prepare.test.mjs`, all 60 resulting briefs, and their current source/staging bindings. No source, staging, approval, or media files were modified. This report is the only file written by this review.

This is an engineering/content-consistency review, not an official outline, audio, final-video, package, or publication approval. Production audio was being generated concurrently and was outside this review. No assertion is made about rendered duration, voice quality, or completed media.

## Findings

- No severity P0–P3 findings within the reviewed scope.
- The new `### 選項 A：…` / `### 選項 B：…` headings conform to the actual exported `outlineOptions` parser in `tools/video/review/sync.mjs`. Both options have parsed titles, distinct summaries, and the exact current lesson's spoken opening hook. The worked-example heading does not conceal or add an outline option.
- Each first-question example follows the actual source sequence: question, three spoken lettered choices, exactly the ordered `evidence_ids` dialogue turns, the existing choose instruction with its 4,000 ms source pause, then the existing answer narration. The example does not claim a second replay after the choose instruction or substitute Conversation A for designated Conversation B evidence. Day35's three-turn Conversation A example was also inspected directly.
- Role labels are derived from the validated source roles (`T` → Traveler, `S` → Staff). The displayed correct letter/choice and quoted answer narration agree with the current canonical lesson.
- Option A accurately describes the generated lesson's section order. Option B is explicitly a proposed alternative and says that choosing B requires changing the script, captions, audio plan, and checks first. It is not represented as the current script.
- The change adds a concrete worked example to the brief; it does not insert new utterances into the lesson or media plans. Independent in-memory execution of the committed and current generators over all 60 lessons found all eight non-brief return fields identical for every lesson: 480 comparisons passed, including scripts, translations, teaching-audio plans, claims, caption plans, duration plans, metadata, and line entries.

## Verification performed

1. Ran the two focused regression tests against the actual official parser and the worked-example playback order: 2 passed, 0 failed.
2. Parsed all 60 on-disk briefs with the official parser: exactly 120 complete options, with the correct per-lesson hooks. Each on-disk brief equals current generator output.
3. Checked all 60 first-question examples against canonical lesson evidence, actual generated line order, roles, choice labels, 4,000 ms choose pauses, correct answers, and verbatim answer narration.
4. Compared all non-brief generator outputs with the committed generator as described above. Git also shows no canonical lesson or generated media-plan changes. The only changed files inside individual `dayNN` source directories are 60 briefs and 60 review-binding files.
5. Checked all 720 source generated-artifact hashes and all 60 staged review bindings, including staged lesson/profile/lexicon and linked-review hashes. All passed. Every binding equals its committed version except the intended `generated_artifacts["brief.md"]` hash.
6. Confirmed all 60 staged briefs exactly match the reviewed source briefs. No network service, production setting, paid request, or review mutation was invoked.

## Reviewed hashes

| Item | SHA-256 |
| --- | --- |
| `tools/video/airport_english/prepare.mjs` | `03fd93f79b1fd39e61f38cba730e7ea284dc0a61fbcbc985d529acfd1e2c36b5` |
| `tools/video/airport_english/prepare.test.mjs` | `d3bdfa5a4df63aad2b4fdb799f8a50b0d828999a449654fe1276a2d28536bc12` |
| Day01 `brief.md` | `9c37f1c466b7e8ea830985198f6d66272ff10441d68c85fbed95b54e55ed1748` |
| All 60 brief manifest aggregate | `1ded76ea11e820a93301265d1256df686be5c2d08867674514d692108f9d10ec` |

The aggregate hashes the UTF-8 concatenation, in day01–day60 order, of `dayNN`, one space, that brief's lowercase SHA-256, and a newline. Any subsequent brief/source change requires a current review and the applicable official hash-bound approval; this review does not authorize changing the already-approved Day01 brief.
