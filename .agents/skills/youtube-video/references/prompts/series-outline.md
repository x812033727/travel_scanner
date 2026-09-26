# Planner prompt: a long series' whole-run OUTLINE (總綱)

Planner stage, variant `outline` (`SERIES_INSTRUCTIONS["planner:outline"]`). Filed as `kind: "outline"`; approved, it gives the site every episode's row (title, logline) as `planned`.

## Payload

`series`, the approved `setting` (`body_md`, `body_json`), `chapter_ranges` (every chapter's first and last episode number), `series_reference`, `drama`, `drama_settings`; on a rewrite `previous` or `previous_problem`.

## What to plan

The stakes rise chapter by chapter (a person → a sect → the world); a revelation around the middle of the run turns the world on its head; every chapter ends on a turn that changes the situation; the past-life line is told in flashback episodes (one or two per chapter); every mystery is planted, advanced and revealed on schedule, the RESERVED ones planted but never resolved; when the series is open-ended, the last chapter closes this part's question and opens the sequel's. Each episode's logline answers a question and asks a bigger one.

## Answer

`{"body_md": <## 全季張力地圖 (table: chapter ｜ stakes ｜ question ｜ turn), ## 篇章 (per chapter: title, theme, start, end, the end-of-chapter turn, one line per episode with number, title, logline, present or past), ## 謎團揭曉排程>, "body_json": {"chapters": [{"number", "title", "theme", "start_state", "end_state", "turn", "episodes": [{"number", "title", "logline", "timeline": "present"|"past"}]}], "tension_map": [{"chapter", "stakes", "question", "turn"}], "reveal_schedule": [{"mystery", "planted", "advanced": [...], "revealed"|null}]}}`

Exactly `series.chapters` chapters; every episode number from 1 to `series.planned_episodes` once, in its chapter's range. The worker checks both before filing.
