---
id: 2026-11-01-theme-paper-skill-lint-settle
title: 奇聞檔案局的小卡一律紙底（theme paper）：skill、lint 警告、主機 settle 預設
status: done
priority: P2
area: tools
owner: claude-opus-5-5-curio-paper
claimed_at: 2026-11-01T04:56:43Z
created_at: 2026-11-01T04:44:06Z
completed_at: 2026-11-01T05:00:58Z
branch:
depends_on: []
scope:
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
  - tools/video/core/curio.mjs
  - tools/video/core/curio.test.mjs
---

# 奇聞檔案局的小卡一律紙底（theme paper）：skill、lint 警告、主機 settle 預設

## Why

站主 2026-11-01 看了 B03 的紙底卡片後說「可以用紙白底」「跟AI科技的一樣」「奇聞檔案局之後如果有用到的小卡也都用成這樣」。
奇聞檔案局（curio- slug、主機 cute-mystery 單集）的卡片今天預設是深色主題；AI 新聞片用 `theme: "paper"`（`docs/videos/PAPER.md`）。
要讓之後每一集不用人記得就是紙底。

## Definition of done

- [x] `curio-episode` skill 定案表加一列：小卡 `theme: "paper"`（站主 2026-11-01），.agents 與 .claude 兩份一致
- [x] `curioWarnings`（`tools/video/core/curio.mjs`）在 curio- slug 沒寫 `theme: "paper"` 時警告，附測試
- [ ] （移到票 2026-11-01-cute-mystery-settle-theme-paper）主機 `settle()`（`tools/video/automation/flow.mjs`）對 cute-mystery 預設 `settled.theme = "paper"`（writer 沒寫時），附測試；
      縮圖照舊深色 bold 版型（PAPER.md：thumb 不套紙底）；關鍵句帶 `keys` 不加（字幕燒錄在同一區）

## Steps

- [x] 以 origin/main 的 curio.mjs、curio.test.mjs、skill 為底改（main 已加 burn_in 警告，舊分支版本會衝突）
- [ ] （移到另一張票）flow.mjs 在 `settled.subtitles = … burn_in: preset === "cute-mystery"` 那行之後加 theme
- [x] `npm run test:tools`（2,753 pass）

## How to verify

`node --test tools/video/core/curio.test.mjs`；`node --test tools/video/automation/automation.test.mjs`；`npm run test:tools`。

## Notes

- 2026-11-01 開票時 `claim` 被拒：scope 與三張舊票重疊（2026-10-14-curio-episodes-keep-the-series-look、2026-10-18-curio-s-axis-pilot-s01-red、
  2026-10-25-redo-episode），三張都 in-progress 7–18 天、前兩張的分支已不在遠端。`--force` 被自動模式擋下，等站主決定（釋出舊票或允許 --force）。
- curio-b01／b02／b03 已各自在 video.json 寫 `theme: "paper"`（票 2026-10-31-b01-shimano-b02-lonely-planet-b03）。
- 2026-11-01 站主選「釋出三張舊票」，已釋出並註記。flow.mjs／automation.test.mjs 另被 2026-10-24-manga-sticker-drama-pace-visible-camera、2026-10-25-fixprompts-look-blocked-sheet-prompt 認領，主機預設拆到另一張票等它們。
- 2026-11-01 完成：curio.mjs／curio.test.mjs／兩份 skill 以 origin/main 版本為底再加紙底規則（這條分支落後 main，合併時這幾個檔只會看到這次的新增）。
