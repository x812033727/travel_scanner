---
id: 2026-09-12-community-smoke-econnreset-stays-unexplained-after
title: Community smoke ECONNRESET stays unexplained after the metric race was fixed
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-12T06:10:42Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/e2e/community.spec.ts
---

# Community smoke ECONNRESET stays unexplained after the metric race was fixed

## Why

2026-09-07-community-read-metric-concurrency 是因為「full-stack smoke 紅」和「日誌裡一堆
uq_community_metric 重複鍵」被一起觀察到才開的。2026-09-12 那張票把 metric 的競態修掉了
（`policy.metric()` 改成 `ON CONFLICT DO NOTHING`，重複鍵再也不會產生錯誤），但那**不是
reset 的成因**：沒有任何一次觀察把兩者連起來，原票自己也反覆寫明 causality is not established。

剩下沒人解釋的是這個：community 的 e2e 在 full-stack smoke 裡會間歇性拿到
`apiRequestContext.fetch: read ECONNRESET`，其中幾次伴隨 Next 的 `Unexpected end of JSON input`
（`load-manifest.external.js` 讀 manifest）。重複鍵的噪音現在消失了，下一次重現會乾淨很多
——這就是把它單獨拉出來的理由，而不是讓它繼續混在一張已經修好的票裡。

## Definition of done

- [ ] community 的 full-stack smoke 連續十次不出現 ECONNRESET。
- [ ] 若成因是 Next 的 dev manifest 併發產生，修法不是重跑、也不是用 retry 包住症狀。

## Steps

- [ ] 用下面 Notes 的 run 清單重新核對失敗現場，先判斷 reset 落在 Next 還是 API。
- [ ] 看 service logs 裡 `destination stream closed early` 與 manifest JSON 兩條線索誰先出現。

## How to verify

`cd apps/web && npx playwright test e2e/community.spec.ts --project=desktop-chromium`
搭配 repository 的 full-stack 設定；CI 那一側看 `full-stack-smoke` job。

## Notes

原票記下的實例（2026-09-08 前後，hotel-content 系列）：run 34148381308、34174165077
（job 101900157817）、34179147187（job 101914466661）、34179865798（job 101916593263）、
34184188769（job 101929120412）、34186584624（job 101936049093）。

失敗點不固定：`community.spec.ts:30` 的 registerAndVerify、`:189` 的 GET /community/me、
`:336` 的 mail-recovery、mobile 的 `:55`。共同點只有 ECONNRESET 本身。

2026-09-12：metric 那一半已修並有回歸測試（見原票），所以之後的重現不會再有
uq_community_metric 的日誌噪音混在裡面。不要把失敗 job 重跑當成修好。
