# 一張好票長什麼樣

`npm run tasks -- new` 寫出的骨架就是這五節；範本裡的佔位句要換掉，不要在下面再加一份同名段落。好的範例：`tasks/done/2026-09-14-release-drivers-own-deploy-hold.md`（長版，含事故時間線與不碰正式站的驗證法）、`tasks/done/2026-09-06-post-deploy-verification-fixes.md`（短版，量測數字進 Why）。

```markdown
---
id: YYYY-MM-DD-slug            ← 與檔名相同，工具自動產生
title: 一行，別人會怎麼稱呼這件事
status: open | in-progress | blocked | review   （done 由 `done` 指令設）
priority: P0 outage | P1 next | P2 normal | P3 someday
area: api | web | ops | tools | docs | meta
owner: / claimed_at: / branch:  ← claim 寫入
depends_on: []                 ← 縮排清單，不是 [id]
scope:                         ← 每一條是這張票可以改的路徑，窄到只剩會改的
  - apps/web/lib
---

# <title>

## Why
沒看過這件事的人需要的脈絡：問題是什麼、怎麼發現的、量到的數字、影響誰。
事故要有時間線。決定與否決的方案寫在這裡，之後的人才不會再提一次。

## Definition of done
- [ ] 可觀察的結果，不是實作步驟（「dry-run 在 main 上 exit 0」，不是「修 82 筆」）。
- [ ] 每一項都能被驗證命令證明。

## Steps
- [ ] 子任務，做到哪勾到哪；順序有意義時寫成先後。
- [ ] 不要先接 CI 再修錯，第一次跑就會紅。

## How to verify
可以直接貼去跑的命令與預期輸出；點擊流程寫到能照做。

## Notes
發現、決定、死路；工作區在哪；下一個人先做什麼。
非持有者結案時加一節「### <日期> 標記完成（由站主授權，非原持有者）」：證據（PR、部署）與每個沒勾的項目去了哪裡。
```

規矩：

- Why 寫給沒看過的人；DoD 寫結果；Steps 寫做法；verify 寫命令。四節混在一起的票，下一個人要重讀整段對話才能接。
- 票裡不放個資、金鑰、主機連線方式；正式站的操作寫成「站主同意後跑什麼」，票不是授權。
- 發現但不在 scope 內的事：另開一張票，`depends_on` 或 Notes 互相指；不要順手擴 scope。
- 停手時：Steps 打勾到實際進度、Notes 寫工作區與狀態檔在哪、`npm run tasks -- release <id>`。
- 結案時：`npm run tasks -- done <id>` 會警告沒勾的項目；沒勾的要在 Notes 交代去向，不要為了綠燈勾掉。
