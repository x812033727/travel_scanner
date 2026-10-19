---
id: 2026-10-19-curio-s30-xuanzang-departure-history-episode
title: Curio S30 Xuanzang departure history episode
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-s30
claimed_at: 2026-10-19T18:02:42Z
created_at: 2026-10-19T18:02:39Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s30
---

# Curio S30 Xuanzang departure history episode

## Why

站主授權在 S34 後連續製作約十支新歷史影片，選題依編輯建議辦理。S30「玄奘怎麼在出境禁令下走向印度」有完整《大慈恩寺三藏法師傳》敘事，但這部門徒傳記兼有頌揚和神異情節；需要清楚區分傳記記述、其他文獻可核實的事與不可驗的內心／對話。

## Definition of done

- [x] `docs/videos/curio-s30` 有 8–10 分鐘可讀劇本、來源筆記、逐句事實表與可渲染插圖分鏡。
- [x] 系列 lint 零錯誤，盲讀故事關卡通過；未經核准不啟動有費用的語音或生圖。

## Steps

- [x] 檢查沒有其他 S30 認領，建立窄 scope。
- [x] 查核《大慈恩寺三藏法師傳》與其他傳世文本的出境時間、關卡與回程，記錄後出門徒傳記的限制。
- [x] 完成 brief、research、claims、video.json、script.md、verify-1.md。
- [x] 跑 lint、說故事盲讀、文件測試並交接。

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s30`；`node tools/video/cli.mjs script --slug curio-s30`；`npm run test:docs-videos`；`npm run check:tasks`。逐句主張與古籍章段對照，找另一位不看研究筆記的讀者盲讀。

## Notes

- 與其他集共用工作分支 `codex/curio-s34-endurance-20261019`，只持有 `docs/videos/curio-s30`，不改題庫或其他集。
- 2026-10-19：固定版《大慈恩寺三藏法師傳》全文可從 GitHub `garychowcmu/daizhigev20` 的 commit `4a6d6f2088825f132521d848c2ea86cf9c9a7620` 讀取；傳記卷一明寫「貞觀三年秋八月」出發，即 629 年，但其他年表有 627 說，劇本不把未解歧見講成確切公元年。來源全文的臨時複本在 `/tmp/curio-s30-bio.txt`。
- 2026-10-19：編劇交接：`brief.md`、`research.md`、`claims.md`、`video.json`、`script.md`、`verify-1.md`、`blind-1.md` 已齊；旁白雜湊 `9df8082746dcf33f`，97 句、95 張靜圖、約 9.5 分鐘。另一位查核者逐句檢查 xz001–xz095，盲讀 13/13 題通過，`narrative --answers` 已寫入工作目錄且通過。`lint` 零錯誤零警告；`npm run test:docs-videos` 236 tests passed，`npm run check:tasks` 通過；最後幾處來源標註調整後旁白文字與雜湊不變。
- 下一步是依 Curio 流程完成大綱／劇本審核，再啟動 TTS、旁白檢查、插圖與成片；目前沒有為 S30 啟動有費用的媒體製作。本票等共同 PR 結案時再移到 `tasks/done/`。
