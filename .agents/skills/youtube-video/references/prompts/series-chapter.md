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
