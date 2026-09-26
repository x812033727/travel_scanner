---
id: 2026-09-26-video-drama-skill-docs
title: Video drama T9: the youtube-video skill gains the drama route and its prompts
status: done
priority: P2
area: docs
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T06:56:21Z
created_at: 2026-09-26T01:53:45Z
completed_at: 2026-09-26T07:01:40Z
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

- [x] `.agents/skills/youtube-video/references/drama.md`（關卡、一次性設定、18 步主幹、指令、`video.json` 重點、品檢與重做、成本、坑、站主從後台發起）、`prompts/planner-drama.md`（故事聖經與大綱）、`prompts/writer-drama.md`（劇本與分鏡，含 FIX mode 給修鏡頭用）、`prompts/verifier-drama.md`（連貫性與設定一致；改編時兼查事實）；`formats.md` 加「D. AI 漫劇」；`SKILL.md` 的路線表與 reference 表加漫劇。
- [x] `.claude/skills/youtube-video` 位元組相同（`npm run test:tools` 的比對過）。
- [x] 描述裡提到的每個路徑都存在（疊在 T5 的分支上，`tools/video/media/*.mjs` 都在；T7 的 `assemble/drama.mjs` 在另一條分支，文件只用文字提，沒寫路徑）。

## Steps

- [x] 寫 reference 與提示詞 → 同步 .claude 副本 → 跑測試。

## How to verify

```bash
npm run test:tools
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。
