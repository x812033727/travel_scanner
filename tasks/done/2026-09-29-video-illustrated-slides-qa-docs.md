---
id: 2026-09-29-video-illustrated-slides-qa-docs
title: Illustrated slides: QA cadence item, disclosure rule and the channel documents
status: done
priority: P1
area: tools
owner: claude-fable-5-1
claimed_at: 2026-09-29T09:42:49Z
created_at: 2026-09-29T09:14:23Z
completed_at: 2026-09-29T09:47:41Z
branch: claude/sharp-brown-dh2x95
depends_on:
  - 2026-09-29-video-illustrated-slides-assemble
scope:
  - tools/video/qa/pace.test.mjs
  - tools/video/qa/checks.mjs
  - tools/video/qa/checks.test.mjs
  - tools/video/qa/cli.mjs
  - tools/video/qa/qa.test.mjs
  - docs/videos/README.md
  - docs/videos/DESIGN.md
  - docs/videos/ILLUSTRATED.md
  - .agents/skills/youtube-video/references/automated.md
  - .agents/skills/youtube-video/references/visuals.md
---

# Illustrated slides: QA cadence item, disclosure rule and the channel documents

## Why

最終關卡的 QA（`qa/cli.mjs` 184–192 行的 `pace` 項）只擋 15 秒；插圖投影片要在真實時間軸上用 `core/cadence.mjs` 的常數；揭露判斷（`qa/checks.mjs:175-177`）要知道授權配樂與風格化插圖不需揭露；頻道規格（`docs/videos/README.md` 第 29、69 行）還寫投影片沒有配樂。

## Definition of done

- [x] `pace` 項（id 不變）在 `illustrated(doc)` 時用 `cadenceProblems`：狀態 > 8 秒或 share < 0.5 不過，detail 印最長、平均、share。
- [x] `disclosureDecision`：漫劇一律勾；插圖投影片授權配樂＋風格化預設（tech-story、flat-explainer）→不需揭露；寫實預設或生成音樂→勾。
- [x] `docs/videos/README.md`（配樂、版型表加 shot、聲音表的新 style）、`DESIGN.md`（插圖投影片的非原創內容防線、CC-only）、`docs/videos/ILLUSTRATED.md`（2026-09-29 的決定、欄位、步驟、關卡、雜湊、節奏常數、成本表、說書規則、試片數字表），`automated.md`、`visuals.md` 對齊。
- [x] `SHORTS.md` L383 與 `DESIGN.md` 對 AI 音樂揭露的不一致寫進 `ILLUSTRATED.md`。

## Steps

- [x] `qa/cli.mjs`、`qa/checks.mjs`、`qa/pace.test.mjs`、`qa.test.mjs`、`checks.test.mjs`。
- [x] 文件。

## How to verify

```bash
npm run test:tools
node tools/video/cli.mjs qa --slug <smoke slug> --workdir <smoke workdir>   # pace detail 有 share；id 與 apps/api/app/video_automation/judge.py QA_ITEMS 一致
```

## Notes

`2026-09-27-video-languages-skill-docs`（已釋出）也列 README.md；先確認它沒人接手。

- 2026-09-29：做完。`qa` 的 `pace` 項在 `illustrated(doc)` 時用 `core/cadence.mjs` 在真實時間軸上量（超過 8 秒或插圖不到一半不過，平均太慢只是 warnings），`assemble` 項把 keyframes manifest 交給 `checksCurrent`；`disclosureDecision(doc, { musicSource })`：風格化預設＋授權配樂不揭露，`cinematic-3d`（`REALISTIC_PRESETS`）或生成配樂要勾。文件：`docs/videos/ILLUSTRATED.md`（新）、`README.md`、`DESIGN.md`、skill 的 `automated.md`、`visuals.md`。
