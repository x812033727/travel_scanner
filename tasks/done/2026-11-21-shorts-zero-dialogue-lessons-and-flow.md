---
id: 2026-11-21-shorts-zero-dialogue-lessons-and-flow
title: Shorts zero-dialogue: lessons and Flow route rules from the 2026-11-21 Flow remake of 社畜地獄 e01-e06
status: done
priority: P2
area: docs
owner: claude-opus-5-5-shorts-flow
claimed_at: 2026-11-21T15:25:26Z
created_at: 2026-11-21T15:25:12Z
completed_at: 2026-11-21T15:36:29Z
branch: claude/shorts-flow-lessons-20261121
depends_on: []
scope:
  - docs/videos/lessons/shorts.md
  - docs/videos/shorts-drama/PRODUCTION-ROUTES.md
  - docs/videos/shorts-drama/series/shechu-hell.md
---

# Shorts zero-dialogue: lessons and Flow route rules from the 2026-11-21 Flow remake of 社畜地獄 e01-e06

## Why

站主 2026-11-21 要「用 Flow 試做 short，照檢討過的新流程」，做了《社畜地獄》e06，接著要求「原本的 1–5 先掃過、整個重製、完整備份」，並說「有需要紀錄的教訓與規則要更新上去」。

這一輪是第一次由代理自己操作 Google Flow（不是站主手動）。`PRODUCTION-ROUTES.md` 路線 B 還寫著「站主在 Flow 生片」、預設 Veo 3.1，跟現況不符：Flow 現在預設 Omni 1.2 Flash，Veo 3.1 Fast／Quality 標示 12/5 停用，介面也換成代理對話式。重製過程中盲評、審稿、審片抓出的問題，有些是新規則沒寫到的（例如五集用同一套結構、轉折鏡變成預告、首格重點道具掉出安全區）。

## Definition of done

- [x] `docs/videos/lessons/shorts.md` 最上面有 2026-11-21 的教訓條目（Flow 代理操作、批次生成、首格安全區與連戲、系列結構重複、成片審片抓到的問題與便宜修法）。
- [x] `PRODUCTION-ROUTES.md` 路線 B 改成代理可自己操作的現況：模型、點數、批次請求、核准、下載方式（Chrome 攔截下載送本機）、注意事項。
- [x] `series/shechu-hell.md` 記下重製版 e01–e06 的題目與結構，以及系列層級的避重複規則。
- [x] `npm run check:tasks`、`npm run test:docs-videos` 通過；開 PR。

## Steps

- [x] 寫教訓條目。
- [x] 改 PRODUCTION-ROUTES 路線 B。
- [x] 更新社畜地獄系列檔。
- [x] 跑檢查、開 PR。

## How to verify

`npm run check:tasks && npm run test:docs-videos`；讀三個檔的新段落，確認跟本票 Notes 的事實一致。

## Notes

- 製作檔不在 repo：`<home>\mokaair-work\shorts-flow\`（本機）與雲端硬碟 `AI/備份/Shorts/社畜地獄/workdir/shechu-hell-e0N/`。
- 規則改動只寫在 repo，雲端由 `docs/videos/rules-sync` 同步。
