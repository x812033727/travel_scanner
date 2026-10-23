---
id: 2026-10-23-c16-bialetti-v4-blind-reader1
title: C16 Bialetti v4 blind narration reader 1
status: review
priority: P2
area: docs
owner: codex-c16-bialetti-v4-blind-reader1
claimed_at: 2026-10-23T05:44:54Z
created_at: 2026-10-23T05:44:50Z
completed_at:
branch: codex/c16-bialetti-blind-v4-reader1-20261023
depends_on: []
scope:
  - docs/videos/story-everyday-bialetti-c16/reviews/narration-v4-blind-reader1.md
---

# C16 Bialetti v4 blind narration reader 1

## Why

PR #1704 的新 81 句作者旁白需要一位與作者、其他讀者隔離的第一位盲讀者，先只看純旁白，再按精確投影保存敘事判斷。此票只管理本讀者的收據，不聲稱核准來源、配鏡、站主劇本或付費製作。

## Definition of done

- [x] 在讀取企劃、來源、舊評、規則或同伴輸出之前，以指定 81 行投影寫定 12 項獨立判斷與具體行號。
- [x] 確認投影 SHA-256 `90BC1CD0D65CB815B4111D7AAC4C4753F2DF028A6E74EDC4F20E8256133534BA`，並驗證與作者 head `a2853124dce795df65d2a42b522084bb72144438` 的 `script.md` 逐列 bytes 完全相同。
- [x] 將第一階段原文與盲讀後的規則/舊評對照保存到唯一收據，不改作者腳本或其他審查。
- [x] 收據與本票構成唯一差異的獨立 draft PR，base `codex/brand-story-bialetti-c16-script`，加上 `no-auto-merge` 並讀回。

## Steps

- [x] 只讀純旁白並封存第一階段收據；原始盲評 SHA-256 `1A3DBD0E3E588FBE9FCCBCCF34D43C330581FF10F08C1D78FF70EBDE90D1EF6A`。
- [x] 讀倉庫 task-board/brand-story 規則、PR #1704 與舊讀者收據；不改第一階段判斷。
- [x] 用極小 no-checkout/sparse 工作樹從精確作者 head 建本分支，窄 scope claim 成功。
- [x] 寫 `reviews/narration-v4-blind-reader1.md`，另列舊 HOLD 修復結果與 12 題規則對照。
- [x] 驗證 task、diff 與收據雜湊，推分支、開草稿 PR、加標籤與讀回。

## How to verify

- `Get-FileHash` 比對純旁白投影 SHA-256，從作者 `script.md` 提取的 81 行以 UTF-8、每列 `ID<TAB>旁白<LF>` 重建後須與純旁白檔 `Buffer.equals`。
- `node tools/tasks.mjs check` 與 `git diff --check`；`git diff --name-only a2853124dce795df65d2a42b522084bb72144438...HEAD` 應只列本收據與本票。
- PR 讀回 `baseRefName`、`headRefOid`、`isDraft` 與 `no-auto-merge` 標籤。

## Notes

- 第一階段不接觸其他檔案；整體 HOLD。舊版的章節銜接/回扣問題已於新版 L20→21、L71→72 解決；原廣告館藏重述也已刪。新 HOLD：L71-79 由可反覆使用直接歸因家庭留存，缺少同等力度的家庭動機證據；L26-29、50-52、60-63、72-79 局部冗贅；L42、58-59 口播過密。
- 收據第一階段原始檔位於 repo 外暫存；PR 裡的收據保存相同原文，再加盲讀後對照。現有草稿、CI 或本收據均非主人核准與製作授權。
- 草稿 PR：[#1737](https://github.com/x812033727/travel_scanner/pull/1737)，base 為作者分支；建立時 head `b21712232a06a389a8776c7860aa8a2ebcb9ba03`，draft 與 `no-auto-merge` 已讀回。
