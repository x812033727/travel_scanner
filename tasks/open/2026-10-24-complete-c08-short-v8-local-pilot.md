---
id: 2026-10-24-complete-c08-short-v8-local-pilot
title: Complete C08 short-v8 local pilot after owner and ledger gates
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-24T06:04:01Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08-short-v8/pilot-readiness.md
  - docs/videos/story-everyday-kikkoman-c08-short-v8/reviews/production
---

# Complete C08 short-v8 local pilot after owner and ledger gates

## Why

C08 的 36 句短版與 36 鏡方向已有站主核准，非付費機器稿和獨立來源查核也已完成。站主已核准本集 US$25 整支上限；仍沒有可歸因帳本、實測配音、插圖、成片或正式站讀回。這張票只接後續製片與逐關卡收據，不把前製完成當成可以上架。

## Definition of done

- [x] 站主已核准 `production-quote.md` 的 C08 專屬 US$25 整支上限與全部次數；在專屬帳本、歷史費用、供應商模型／價格和停線測試通過前，不送首筆付費請求。
- [ ] 有可讀回的 36 句繁中音檔、逐句轉寫／Jev 審核、真人聽音與正文至少 240 秒的實測；checked final 不超過 300 秒。
- [ ] 圖片、`v7e03` 卡片圖解、配樂、繁中 CC、按秒至少 70% 插圖及本機 `final.mp4` 均通過實物 QA，附費用與來源收據。
- [ ] 正式站匯入前另做同一 episode row 的 dry-run／狀態讀回，匯入後讀回 row ID；上傳與發布沿後續獨立關卡處理。

## Steps

- [x] 已核對 `pilot-readiness.md`、凍結來源 SHA、US$25 條件式報價與站主核准答覆，見 `owner-pilot-approval-20261024.md`；首筆付費仍 HOLD。
- [ ] 與預算路由任務協作，在正式站讀回單集帳戶與實際計價，保留未知請求，驗證 TTS、轉寫、Jev、圖像、評審、配樂共用硬停線。
- [ ] 先實測聲音與長度，再買圖；逐句有據重錄不超過報價次數。任一新稿都重新來源查核、盲讀與站主核准。
- [ ] 依實片做圖像、字幕、剪輯、QA、播放器驗收；逐步更新 `pilot-readiness.md` 和本票。

## How to verify

對照 `docs/videos/story-everyday-kikkoman-c08-short-v8/production-quote.md`；執行 `node tools/video/cli.mjs lint --slug story-everyday-kikkoman-c08-short-v8`、`node tools/video/long-form/cli.mjs check` 與本片 QA CLI，保存實際輸出、音檔／成片雜湊、片格時長、逐句辨識／Jev 及 API 預算帳本讀回。正式站只在連線、部署與該列狀態確認後做精確 dry-run／apply；不能用本機 SQLite 模擬替代。

## Notes

2026-10-24：這是尚未認領的後續票，前製 PR #1811、非付費核准來源和 36/36 差異收據均可讀；原 84 句專案不覆蓋。報價提出 30 圖每圖最多 3 次、6 後製字卡、36 句首錄加每句最多一次有據重錄、最多 72 次逐句轉寫、最多 2 批 Jev、一首配樂，整支 US$25 硬停線；**站主已核准 C08 本機試片的 US$25 上限**，精確範圍與輸入雜湊見 `owner-pilot-approval-20261024.md`。現行 C08 預算路由不存在；首筆付費仍 HOLD，直到帳本與全路由驗證。紙上念法展開後約 301.63 秒，不是實測失敗；若實片超過 300 秒，不可任意刪句或加速。正式站連線目前還需 Pageant 解鎖，沒有 dry-run／apply 成果。
