# Planner prompt: one CHAPTER'S DETAILED OUTLINE (篇章細綱)

Planner stage, variant `chapter` (`SERIES_INSTRUCTIONS["planner:chapter"]`). Filed as `kind: "chapter"` with `chapter_number`; approved, the chapter's episodes become `ready` with their beats, and the worker starts them in order.

## Payload

`series`, the approved `setting` and `outline`, `chapter_number`, `chapter_range`, `chapter_outline` (the outline's row for this chapter: keep its titles and loglines unless the note says otherwise), `previous_chapters`, `recaps` (what actually happened in the episodes made so far), `episodes_so_far`, `mysteries`; on a rewrite `previous` or `previous_problem`.

## What to engineer, per episode

- A HOOK inside the first 20 seconds; a CONFLICT settled by the end; a TURN halfway; a CLIFFHANGER as the last beat, typed `danger | reveal | choice | reversal | emotion`.
- SETUPS planted and PAYOFFS paid, by mystery id; TENSION as five scores 1–5 for the five beats (opening, first half, midpoint, second half, ending), never flat, ending ≥ 4.
- Adjacent episodes never end on the same cliffhanger type; a payoff at least every 3–4 episodes; the chapter's last episode ends on a reveal or reversal that changes the meaning of something seen earlier in the chapter.
- One place or two, 2–4 characters, no recap of what came before; the leads' bond advances one notch per chapter, shown, not said.

## Answer

`{"body_md": <## 本篇, then ### 第 N 集 with 標題, 一句話, 開場鉤子, 主要衝突, 轉折, 結尾懸念（類型）, 埋下 / 回收, 張力曲線, 出場角色, 場景, 主題句>, "body_json": {"chapter", "episodes": [{"number", "title", "logline", "timeline", "hook", "conflict", "turn", "cliffhanger": {"type", "text"}, "setups": [ids], "payoffs": [ids], "tension": [5 ints], "characters": [ids], "locations": [...], "theme"}]}}`

Exactly the episodes of `chapter_range`. The worker refuses a missing beat, a flat or unfinished tension curve, or two adjacent episodes with the same cliffhanger type, and asks once more.

## With the retention rules (a binge genre, docs/videos/BINGE.md)

When `genre_spec.retention` is true (every genre preset but `xianxia-bonds`), the prompt carries the genre section and `RETENTION_RULES`, and each episode also names:

- `hook_type`: `question | danger | image | line | reversal`; the hook is spoken inside about 5 seconds, so it is a line or a picture, not a mood.
- `lead_arc`: `wins | suffers | mixed`; the lead never only suffers two episodes in a row.
- `satisfaction`: at least two `{beat: opening | first_half | midpoint | second_half | ending, type: <a satisfaction id of the genre>}`, the first in `opening` or `first_half`; satisfaction and trouble alternate (right after a satisfaction, a bigger problem); the ids are `SATISFACTION_TYPES` (`face_slap`, `identity_reveal`, `counter_kill`, `level_up`, `first_clear`, `betrayer_punished`, `villain_humbled`, `hidden_power`, `public_vindication`, `rescue`, `reversal`).
- Any four episodes in a row pay off at least one thread (`payoffs`).

body_md adds 開場鉤子（類型）, 爽點（節拍與類型）, 主角走向 to each episode; body_json adds `hook_type`, `lead_arc`, `satisfaction` to each. The worker (`retentionProblem`) and the site (`_retention_problem`, 422 `video_series_doc_invalid`) both refuse a chapter outline that breaks these. On a hands-off series the document then goes to the checker (`verifier-series-doc.md`) before it is filed.
