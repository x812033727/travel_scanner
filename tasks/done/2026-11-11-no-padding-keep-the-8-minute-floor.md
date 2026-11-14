---
id: 2026-11-11-no-padding-keep-the-8-minute-floor
title: 原來如此、奇聞：8 分鐘下限保留，素材不夠就放後備，不硬寫
status: done
priority: P2
area: docs
owner: claude-opus-5.5-p06-p18-handoff
claimed_at: 2026-11-11T04:16:06Z
created_at: 2026-11-11T04:15:56Z
completed_at: 2026-11-11T04:16:36Z
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/dialogue-pilot-20261103
  - docs/videos/lessons/sothatswhy.md
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
---

# 原來如此、奇聞：8 分鐘下限保留，素材不夠就放後備，不硬寫

## Why

站主 2026-11-11：「稿子不用硬寫，品質為主，流暢的內容才重要」；同一天在 PR #2069 也決定「8 分鐘下限也幫我留著好了」，素材不夠要硬補的題目放後備。先前的說明寫「接近下限就多寫內容」（原來如此 README §4、§10.6，curio skill），跟這兩句相反；我一度改成「不設下限」，也跟 #2069 的決定不一致。

## Definition of done

- [x] 原來如此 README §9「長度」：8 分鐘下限保留、不硬寫、素材不夠就放後備（連到 material-20261111）；§4、§10.6 同步。
- [x] curio-episode skill（兩份）同一句改成不硬寫、放後備。
- [x] lessons/sothatswhy.md 記這個決定。

## Steps

- [x] 讀 #2069 的 `2026-11-11-curio-and-sothatswhy-length-follows-the`（已回退）與 `so-thats-why/material-20261111/README.md`。
- [x] 改文件；`node --test tools/skills.test.mjs` 7/7。

## How to verify

`grep -n "多寫內容" docs/videos/so-thats-why/dialogue-pilot-20261103/README.md .agents/skills/curio-episode/SKILL.md` 只剩「不要多寫內容」。

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.
- 2026-11-11：只改文件；lint 的 8 分鐘下限與 build_scenes 的字數檢查都不動（字數 `assert` 的下限是每集自己的 builder，新一集照 §9 自己決定）。認領 `--force`：curio skill 在已合併的 drive-ai-drama-layout 舊認領裡。
