---
id: 2026-10-24-pin-c08-owner-cap-receipt-to
title: Pin C08 owner cap receipt to approved scope
status: done
priority: P1
area: tools
owner: Codex-C08
claimed_at: 2026-10-24T06:35:48Z
created_at: 2026-10-24T06:35:42Z
completed_at: 2026-10-24T06:38:05Z
branch: codex/c08-kikkoman-canonical-preflight-20261024
depends_on: []
scope:
  - tools/video/automation/story.mjs
  - tools/video/automation/story.test.mjs
---

# Pin C08 owner cap receipt to approved scope

## Why

PR #1811 的獨立合併前審查發現 `c08ShortPaidProblem` 接受工作目錄自填的任意正數 `cap_usd`；舊測試甚至要求 `quote_usd: 26, cap_usd: 26` 通過。站主只核准 C08 短版繁中本機試片整支 US$25，原報價與核准收據均有內容雜湊。現時付費 API／CLI 還有其他 HOLD，但這個弱門檻必須在未來帳本開通前收緊。

## Definition of done

- [x] C08 只有在原版站主核准收據仍與 repo 釘選雜湊一致、工作目錄收據指向核准當時的報價 SHA、且整支 cap 恰為 US$25 時，這一層付費預檢才通過。
- [x] 自填 US$26、錯誤核准／報價雜湊、缺少 repo 核准文件都被拒絕；C08 凍結專案的正向測試仍通過。
- [x] 針對 C08 的測試 1/1、任務板與差異空白檢查通過；完整 CI 是 PR 合併關卡，合併前維持全路由付費 HOLD。

## Steps

- [x] 在 `story.mjs` 釘選核准檔 SHA、舊報價 SHA 與 US$25，將 repo 根目錄傳給預檢。
- [x] 更新 `story.test.mjs` 的正反例；刪除把 US$26 當作合格的舊斷言。
- [x] 完成針對性檢查與獨立唯讀審查；未經單集帳本／歷史費用及供應商價格核對，不送任何付費請求。

## How to verify

`node --test --test-name-pattern 'C08 short-v8 adopts only its frozen project and has a separate paid cap receipt' tools/video/automation/story.test.mjs` 通過 1/1；`npm run check:tasks` 通過 2148 票、`git diff --check` 通過。Windows 上整份 `node --test tools/video/automation/story.test.mjs` 在測試檔層級以 exit 3221226505 中止，沒有逐項失敗資訊；Linux CI 最新 head 的四項檢查仍須通過才可合併。

## Notes

站主答覆「核准 C08 本機試片，US$25 上限」。`owner-pilot-approval-20261024.md` SHA-256 為 `54d973ab2c46a1b0caa1a207dba4b390fa04084727810a527bbf3eea67d9c607`；其內記錄核准前報價 SHA-256 `28f983bc35272c216ce9026855bf881e0b29f03eadd7169f908d1284d2926948`。本票只修一層預檢，不建立 C08 帳本、不解鎖 `story-everyday-` 付費路由，也不做實際媒體請求。

獨立唯讀審查確認：這一層只要求工作目錄收據**引用**核准前報價 SHA，沒有驗證現行 `production-quote.md` 的內容雜湊；該檔在核准後因狀態文字更新，現行 SHA 不同。站主核准文件本身明列數量／US$25 範圍並由 repo 檔案雜湊鎖定，C08 的全路由付款仍另受 API／CLI 停線限制。C09 尚有一張未認領的 worker guard 票涵蓋這兩個檔案，後續要協調並重測。
