---
id: 2026-11-11-curio-skill-pause-savings-per-series
title: curio-episode skill：停頓預設的片長換算分系列寫（原來如此每句只少 0.1 秒）
status: done
priority: P2
area: docs
owner: claude-opus-5.5-p06-p18-handoff
claimed_at: 2026-11-11T01:58:53Z
created_at: 2026-11-11T01:41:36Z
completed_at: 2026-11-11T01:58:54Z
branch:
depends_on: []
scope:
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
---

# curio-episode skill：停頓預設的片長換算分系列寫（原來如此每句只少 0.1 秒）

## Why

PR #2069 在 curio-episode skill 加了一句：「停頓拿掉後同一份稿子估出來的片長會變短（每句少 0.3 秒、每景少 0.55 秒）」。
這對奇聞檔案局是對的（它的句子沒寫 `pause_after_ms`，預設 300 毫秒變 0）；但同一段說這是兩個系列的預設，而原來如此事務所每句本來就寫 `pause_after_ms: 100`，
套用後每句只少 0.1 秒（甚至不變，因為每句自己的停頓優先），照 0.3 秒估會把原來如此的片長估得太短。

## Definition of done

- [x] 說明分系列寫：奇聞每句少 0.3 秒、每景少 0.55 秒；原來如此每句不變（或照 `2026-11-11-sothatswhy-line-pauses-via-pauses-line-ms` 改完後少 0.1 秒）、每景少 0.55 秒。
- [x] 兩份 skill 一字不差（`npm run test:tools` 會比對）。

## Steps

- [x] 站主同意後直接改在 PR #2069 的分支上（不等合併）。

## How to verify

`npm run test:tools`（.agents 與 .claude 的 skill 一致性）。

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

- 接在 PR #2069（票 `2026-11-11-series-default-tight-pauses-and-beat`，在那個 PR 的分支上）之後做。
- 2026-11-11：從 PR #2069 的檢查拆出來；如果 #2069 還沒合併，也可以直接在那個 PR 改。
- 2026-11-11（claude-opus-5.5-p06-p18-handoff）：站主選「推到 #2069 分支」。在 `claude/youthful-albattani-m1ih5z` 加一個 commit（cb019c3b），
  只改兩份 curio-episode SKILL.md 的那一行：奇聞每句少 0.3 秒、原來如此每句只少 0.1 秒（指向 dialogue-pilot README §10.6）、兩者每景少 0.55 秒；
  「接近 8 分鐘下限」改成「接近片長下限」（原來如此的下限不是 8 分鐘）。`node --test tools/skills.test.mjs` 7/7。
  認領時 `--force`：scope 跟已以 #2057 合併、沒結案的 `2026-11-10-drive-ai-drama-layout` 重疊。
