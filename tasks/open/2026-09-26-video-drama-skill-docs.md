---
id: 2026-09-26-video-drama-skill-docs
title: Video drama T9: the youtube-video skill gains the drama route and its prompts
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-26T01:53:45Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-drama-media-client
scope:
  - .agents/skills/youtube-video
  - .claude/skills/youtube-video
---

# Video drama T9: the youtube-video skill gains the drama route and its prompts

## Why

代理照 skill 做事。漫劇路線要有自己的 reference：一次性設定、主幹與關卡、指令、成本、坑、提示詞；`formats.md` 要多「D. AI 漫劇」；`tools/skills.test.mjs` 會檢查 skill 裡提到的路徑存在，所以排在 T2 之後。

## Definition of done

- [ ] `.agents/skills/youtube-video/references/drama.md`、`prompts/planner-drama.md`、`prompts/writer-drama.md`、`prompts/verifier-drama.md`；`formats.md` 加 D 節；`SKILL.md` 的路線表加漫劇。
- [ ] `.claude/skills/youtube-video` 位元組相同（`npm run test:tools` 的比對過）。
- [ ] 描述裡提到的每個路徑都存在。

## Steps

- [ ] 寫 reference 與提示詞 → 同步 .claude 副本 → 跑測試。

## How to verify

```bash
npm run test:tools
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。
