---
id: 2026-10-19-host-explainer-route-always-adds-the
title: Host explainer route always adds the curio music bed and asks two story readers
status: in-progress
priority: P2
area: tools
owner: claude-opus-5.5-curio-host
claimed_at: 2026-10-19T06:26:33Z
created_at: 2026-10-19T01:10:13Z
completed_at:
branch: claude/curio-host-music-two-readers
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# Host explainer route always adds the curio music bed and asks two story readers

## Why

站主 2026-10-19 要奇聞檔案局跟品牌故事一樣有配樂、一樣順。品牌故事的工人自己寫 `music`（`story.mjs` 的
`composeStory`），主機可愛解說路線卻要撰稿模型自己記得寫：`flow.mjs` 的 `settle()` 只替插圖投影片補配樂。
票 `2026-10-19-curio-keeps-the-brand-stories-hook` 已讓撰稿提示要求寫 `music`、lint 在缺配樂時警告，但模型漏寫時沒有東西補。
另外品牌故事的說故事盲評問兩位讀者（#1562），主機的解說路線（`flow.mjs` 約 3342 行）仍只問一位。

## Definition of done

- [x] 有系列設定的解說預設（`explainerProfile(preset)`）在 `drama.music_enabled` 不是 false 而且撰稿沒寫 `music` 時，
      `settle()` 補上 `CURIO_MUSIC`（或該系列自己的配樂設定）；配樂開關關掉時照舊刪掉。
- [x] 奇聞檔案局（cute-mystery）的說故事盲評跟品牌故事一樣問兩位讀者、兩位都否才算沒過。
- [x] 測試守住原來如此與 flat-explainer 的行為不變。

## Notes

- 認領前先確認 `2026-10-16-bind-story-audits-and-narration-to`（codex，`flow.mjs`）已經放手或合併。
- 改 `settle()` 不動提示字 digest；改盲評的 payload 會動 `PANEL_RULES_SHA256` 之外的 verifier payload digest，部署前同樣要
  主機沒有未完成的 cute-mystery 單集。

## 2026-10-19 做法（claude-opus-5.5-curio-host，分支 claude/curio-host-music-two-readers，疊在 #1577 上）

- `2026-10-16-bind-story-audits-and-narration-to` 經 #1588 放掉 `flow.mjs` 與 `automation.test.mjs` 後才認領。
- 配樂：`flow.mjs` 的 `SERIES_MUSIC` 表只有 `cute-mystery → CURIO_MUSIC`。`settle()` 在解說預設、撰稿沒寫 `music`
  時補一份複本；撰稿自己寫的配樂照留；`music_enabled === false` 照舊整個刪掉。原來如此（cute-cartoon）**沒有**
  放進表裡：站主只要求奇聞檔案局，補進去會讓每一集原來如此多一首付費配樂，算是行為改變。哪天站主要原來如此
  也一定有配樂，在表裡加一行就好。
- 盲評：`narrativeGate` 在 `format === "drama"` 而且 `video.look.preset === "cute-mystery"` 時問
  `STORY_PANEL_READERS`（2）位讀者，payload 各帶 `reader: 1|2`，用 `mergePanelVerdicts` 合併（任一位讀者引了行號答「是」
  就算過）。其他影片仍只問一位，payload 只有 `narration`、`questions`，紀錄裡沒有 `readers`。
- 部署前：cute-mystery 單集的盲評 payload 變了（多了 `reader`），主機上不能有盲評做到一半的 cute-mystery 單集。

