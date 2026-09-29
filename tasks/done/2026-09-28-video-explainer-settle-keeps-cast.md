---
id: 2026-09-28-video-explainer-settle-keeps-cast
title: 單集解說片的 settle() 留下寫手的角色
status: done
priority: P2
area: tools
owner: claude-fable-5-1
claimed_at: 2026-09-29T09:52:24Z
created_at: 2026-09-28T16:51:24Z
completed_at: 2026-09-29T09:52:25Z
branch: claude/sharp-brown-dh2x95
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/series.test.mjs
---

# 單集解說片的 settle() 留下寫手的角色

## Why

#904（`26a5bfb95`，「原來如此事務所」扁平解說漫劇）在 `tools/video/automation/flow.mjs` 的 `settle()` 裡，用 :259-261 把解說片的角色清空（解說片沒有角色，預設也不歸寫手改）。但緊接著 :266-272 的 `format === "drama" && series` 分支，又把 `settled.characters` 設回寫手回傳的 `video.characters`。

後台表單建立的解說片一律是單集（`create_one_off`），一定帶著 `state.series`，所以在唯一會走到的路徑上，清空的保證失效了。寫手只要回傳任何一個角色，lint 就會擋下（`tools/video/core/drama.mjs:301`），接著最多再叫寫手 3 次（`MAX_LINT_FIXES`），最後 `retryLater`，而不是由工具安靜地處理掉。

2026-09-28 部署 `717e1628` 後的稽核找到的：一個代理在 origin/main 的程式上重現，另一個代理試著反駁，最後確認。`settle()` 帶角色 `[{id:'host'}]`、`stylePreset:'flat-explainer'`、`cast:[]`，`series:null` 時回 `[]`，`series:{kind:'one-off'}` 時回 `[{id:'host',…}]`。唯一的測試（`series.test.mjs:947`）給寫手的是空角色，所以抓不到。

## Definition of done

- [x] 單集解說片（`series.kind === 'one-off'` 且 `stylePreset === 'flat-explainer'`）的 `settle()` 結果永遠沒有角色，不管寫手回了什麼。
- [x] 其他單集與長篇系列的角色處理不變。

## Steps

- [x] 在 `settle()` 裡讓解說片的清空在系列分支之後生效（或讓系列分支跳過解說片）。
- [x] `series.test.mjs` 加一個寫手回傳角色的單集解說片案例。

## How to verify

```bash
node --test "tools/video/automation/*.test.mjs"
```

## Notes

同一次稽核判定：Shorts 從寫手的第一版稿子存下、沒等查核（`flow.mjs:1346` 在 verify 之前）不算缺陷，因為 `from-episode` 是手動的，而且 Shorts 的 qa 要求綁定該 Short 稿子雜湊的 verify.json。
- 2026-09-29：修在 `2026-09-29-video-illustrated-slides-worker` 的同一次 `settle()` 改寫裡：系列分支在 `look.preset === "flat-explainer"` 時一律給 `[]`。測試在 `automation.test.mjs`（「an explainer one-off keeps no cast whatever the writer returned」）。`--force` 認領的理由：scope 與 `2026-09-28-sothatswhy-shorts-from-episode`（過期的 in-progress）重疊，該票只剩 ffmpeg 實跑，沒有動 `settle()`。
