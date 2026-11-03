---
id: 2026-11-03-comedy-story-review-gate
title: 漫劇與短劇的故事企劃評分審核：盲評打分、笑點門檻、不過就改
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-wangwang
claimed_at: 2026-11-03T10:29:45Z
created_at: 2026-11-03T10:29:44Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/animation-preproduction/references/comedy-review.md
  - .agents/skills/animation-preproduction/scripts/comedy_review.mjs
  - .agents/skills/animation-preproduction/SKILL.md
  - .claude/skills/animation-preproduction/SKILL.md
  - tools/comedy-review.test.mjs
---

# 漫劇與短劇的故事企劃評分審核：盲評打分、笑點門檻、不過就改

## Why

站主 2026-11-03：故事企劃要有審核機制，用分數判斷能不能過，不行就再修改，一定要有笑點、要有趣。

## Definition of done

- [x] 評分表、門檻、流程寫進 `animation-preproduction` skill（`references/comedy-review.md`，SKILL.md 兩份同步）。
- [x] `comedy_review.mjs`：`packet` 產生盲評包、`score` 合分並以結束碼判定；`tools/comedy-review.test.mjs` 盯著評分表與文件一致、門檻、格式檢查。
- [x] 第一次實際使用：汪汪社畜 EP1 跑了六輪（54 → 66 → 71 → 75 → 73 → 73），紀錄在 `docs/videos/wangwang-office-e01/comedy-review/`。
- [ ] 站主決定 EP1 停在 73 之後怎麼辦（接受、調門檻，或換題材）；門檻 80 可能高於 LLM 評審的天花板，要用真實數據校準。
- [ ] 門檻用第一季的 YouTube 數據校準。

## How to verify

```bash
node --test tools/comedy-review.test.mjs tools/skills.test.mjs
node .agents/skills/animation-preproduction/scripts/comedy_review.mjs score docs/videos/wangwang-office-e01/video.json docs/videos/wangwang-office-e01/comedy-review/round-3/judge-*.json
```

## Notes

- 評審是另開的代理，只讀 `packet.md`，每輪換新的一組，角色依作品挑（Shorts 觀眾、上班族、養狗的人）。
- 三輪裡每一輪都有評審說罐頭笑聲尷尬；站主要了笑聲，所以保留兩處並把意見交給站主。
- `score` 用目前的 `video.json` 驗鏡號；改過鏡號的舊輪次重算不了，舊輪的結果記在該集的 `comedy-review/README.md`。
