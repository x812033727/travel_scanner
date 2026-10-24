---
id: 2026-10-24-quote-c08-short-v8-local-pilot
title: Quote C08 short-v8 local pilot without paid calls
status: done
priority: P1
area: docs
owner: codex-root-c08-quote
claimed_at: 2026-10-24T05:57:56Z
created_at: 2026-10-24T05:57:51Z
completed_at: 2026-10-24T06:03:03Z
branch: codex/c08-kikkoman-canonical-preflight-20261024
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08-short-v8/production-quote.md
  - docs/videos/story-everyday-kikkoman-c08-short-v8/pilot-readiness.md
---

# Quote C08 short-v8 local pilot without paid calls

## Why

C08 的 36 句短版稿與分鏡已獲站主核准，且已建立可由影片工具選取的頂層機器稿。但本集沒有付費試片核准、可歸因帳戶、實測語音或成片。要讓站主審核整支上限，先列出精確張數、嘗試次數、供應商公開價格與仍未解的帳本風險，並讓後台接手者看到每個 HOLD。

## Definition of done

- [x] 一份只綁定已核准短版來源雜湊的整支條件式報價，列出圖片、字卡、旁白、配樂最高次數與 US$25 停線；不把估額冒稱硬上界。
- [x] 一份逐關卡就緒表，分開列前製、真實配音／成片、正式站匯入與上傳狀態。
- [x] 沒有付費請求、預算解鎖或後台正式站寫入。

## Steps

- [x] 對照凍結旁白、逐鏡和機器稿，核對 36 句／36 鏡、30 `shot`／6 `stats` 及 `v7e03` 的後製圖解。
- [x] 對照 MiniMax／Google 官方價目、API 當前預留額與 C 系列帳戶清單，計算可見估額及可能提前停線的風險。
- [x] 獨立只讀審查逐項驗算報價、重試計數、來源及未完成關卡，修正發現的文字問題。

## How to verify

`git diff --check`；`npm run check:tasks`。獨立審查需對照 `docs/videos/story-everyday-kikkoman-c08-short-v8/video.json`、`duration-receipt-20261024.md`、`apps/api/app/video_budget/models.py`、`apps/api/app/video_media/admin_api.py`、`apps/api/app/video_speech/admin_api.py` 及當天官方價格；驗算 90×0.0035=0.315、90×0.01=0.90、1×0.08=0.08、90×1.032192=92.897280、72×0.151552=10.911744、72×1.032192=74.317824、2×0.002688=0.005376。報價在 `production-quote.md`，關卡在 `pilot-readiness.md`。

## Notes

2026-10-24：報價只供站主審核，不代表核准 C08 費用。Google 影像評審 US$0.01／次只是 repo 規劃值，保留上界達 US$1.032192／次；硬停線可能無法跑滿 90 張圖片請求。所有送出後失敗／未明的請求仍占次數並留帳。`v7e03` 是六張後製字卡之一，不能算成第 31 張圖片，也不能把現在的文字預覽當作圖解完成。紙上 301.63 秒不代表實片超時；真人聽音與實測 240–300 秒皆未完成。C08 不在現行 `C_SERIES_PILOT_LIMITS_USD`，未核實單集路由與歷史費用前持續 HOLD。

獨立審查回報：30/6、36 句、來源雜湊與價格算式均正確；要求把失敗／未明請求也占次數、付費音訊 QA 次數上限寫清楚，已修訂為最多 72 次逐句轉寫與 2 次 Jev 批次。
