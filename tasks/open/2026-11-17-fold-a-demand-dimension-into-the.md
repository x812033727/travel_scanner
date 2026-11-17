---
id: 2026-11-17-fold-a-demand-dimension-into-the
title: Fold a demand dimension into the pool audience score
status: in-progress
priority: P2
area: tools
owner: claude-fable-heimao-topics
claimed_at: 2026-11-17T01:16:15Z
created_at: 2026-11-17T01:16:15Z
completed_at:
branch: claude/wizardly-albattani-is0lls
depends_on: []
scope:
  - tools/video/curio/pool
  - tools/video/so-thats-why/pool
  - tools/video/pool-admin
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools
  - apps/api/tests/test_video_pools.py
  - apps/web/components/admin-video-pools.tsx
  - apps/web/components/admin-video-pools.test.tsx
  - apps/web/lib/video-pools-messages
  - apps/web/lib/video-pools-copy.ts
---

# Fold a demand dimension into the pool audience score

## Why

站主 2026-11-17：擴充池本來就有獨立觀眾評分，照參考頻道觀看數歸納的選題四問要整合進去，不另立一套。站主定了三件事：併成一個總分、
先只評可成題的題案、門檻維持 6.5 看總分；並要求把這個機制寫進擴充池的流程。量測與四問的出處在 `docs/videos/channel-review-20261116/README.md`。

## Definition of done

- [x] 兩個池的題案 `audience` 多一項 `demand`（四個是非題換算 1–10），`score =（五項平均 × 5 + demand）÷ 6`，五項平均留在 `base`。
- [x] `build`／`check` 擋：可成題沒有需求分、需求分與答案不符、總分不符公式、可成題總分低於 6.5。
- [x] 奇聞 77 組、原來如此 154 組可成題由獨立評審答完四問，紀錄在各池 `reviews/demand-20261117.json`；總分低於 6.5 的改成後備。
- [x] 後台資料包、API 欄位、後台頁面與五個語系帶出需求分。
- [x] 兩個池 README 的〈獨立觀眾評分〉寫進第六項與「擴充時的順序」。
- [ ] PR 合併。

## Steps

- [x] 兩份 `render.mjs`：`DEMAND_QUESTIONS`、`demandScore`、`blendedScore`、`validateDemand` 與兩條關卡。
- [x] 六位獨立評審分批答四問；每批三組重複題，24 個答案全部一致。
- [x] 寫回 `themes.json`、重排名次、重建兩池與 `pools.json`。
- [x] 測試與文件。

## How to verify

```bash
node --test tools/video/curio/pool/pool.test.mjs tools/video/so-thats-why/pool/pool.test.mjs tools/video/pool-admin/bundle.test.mjs
node tools/video/pool-admin/bundle.mjs check
cd apps/api && uv run pytest tests/test_video_pools.py
cd apps/web && npx vitest run components/admin-video-pools.test.tsx
```

## Notes

- 結果：奇聞可成題 77 → 23（54 組改後備），原來如此 154 → 84（70 組改後備）。改後備的題案 `material.was` 是 `ready`、`missing` 寫總分；
  要還原就把 `verdict` 改回 `ready` 並調門檻或換算，`base` 都留著。
- 需求分布偏低：奇聞 0 題 25、1 題 40、2 題 9、3 題 3；原來如此 0 題 89、1 題 62、2 題 3。原來如此池的可成題幾乎都是通用科學現象，
  「規格或誰收錢」只有 4 組、「大公司或日本品牌」0 組。下一批擴充先照四問挑方向。
- 基準初評 `reviews/audience-20261114.json` 的題案原本不受 6.5 關卡限制；併分後 API 測試（可成題都要過門檻）會紅，
  所以有需求分的題案一律看總分，基準只豁免「要有 rounds」。這多改了奇聞 14 組、原來如此 3 組。
- 沒動：奇聞池單題層的 156 筆觀眾分數仍是五項；品牌故事沒有池子；`producer` skill 的評分表（scope 在票 `2026-11-03-skill-ai`）。
- 四問來自三個頻道最新 200 支的標題分組，是相關不是因果；分數是代理的判斷。
- 2026-11-17 續：需求分接到奇聞池的單集題（`core.mjs` 的 `readDemand`）。篩了 G、P、U 三類還沒用到的 536 題（中三題 18、中兩題 109），
  替中三題的 16 題補五項評分（另兩題已評過），並替先前已評的 106 題補答四問，172 題已評的單集題都用併分排名。
  單集題沒有門檻。原來如此池的單題層沒有動。下一步可做：中兩題的 109 題補五項評分；其他分類 969 題與原來如此池照同樣方式篩。
- 2026-11-17 再續：中兩題的 109 題補五項評分（94 題新評）。127 題候選裡 42 題總分在 6.5 以上。已評單集題 266 題。
- 2026-11-17 三續：奇聞池其餘六類 797 題單集題篩完（中三題 6、中兩題 59），寫進 `reviews/demand-20261117-rest.json` 並掛到 pool.json。
  原來如此池篩了 555 組題案（中兩題 1 組）與兩個分類 858 題（中兩題以上 39 題），只存紀錄 `reviews/demand-20261117-screen.json`，build 不讀。
  原來如此其餘五類 2,756 題沒篩。下一步：奇聞 65 題補五項評分；原來如此用那 39 題組新題案。
- 2026-11-17 四續：奇聞其餘六類中兩題以上的 65 題補五項評分，29 題總分 6.5 以上。已評單集題 331 題，6.5 以上 92 題。
- 2026-11-17 五續：wave58–71 來源查無，已全數移到暫緩（票 `2026-11-17-so-that-s-why-waves-89`）。站主指正品牌故事與參考頻道黑猫研究院來的題都歸奇聞：
  商業與品牌類改用品牌四問（`DEMAND_QUESTIONS_W`），現有 53 題重答、12 題補五項評分。
- 2026-11-17 六續：站主選「全部 270 題分批收」。`reference-heimao-20261031/topics.json` 的商業與品牌方向依觀看數排序，已做三批：
  wave72（第 1–25 名＋印表機墨水）、wave73（第 26–50 名）、wave74（第 51–80 名）。可單獨成集並入選 11、10、7 題，總分過 6.5 的 3、5、2 題。
  wave72 初評只有 1 題過關，站主選「先改包裝再續收」；wave73 起研究代理交稿就寫 40–110 字的短問句。
  **接手的人從第 81 名往下排第七十五批**：題號 N7401 起、研究代理 ZT1–ZT4、覆核 R751–R754。做法與教訓都在池 README 的第七十二到七十四批三節：
  請求一律經同一支會記錄、會拒發被擋網域的工具；流傳版本要有實際讀到的樣本文章；代編號的網址要有頁面給連結；主編每批抽查三題。
  工具與說明檔放在工作階段的暫存區、沒有進 repo；要重建的話照 README 那三節的「做法」寫。
- 入選核心 1629；已評單集題 357 題，6.5 以上 104 題。
- 2026-11-17 七續：站主選「先停」黑猫方向，改問怎麼有效率增加 6.5 分以上的題，選「先改包裝單集題、再改長題案」。
  奇聞單集題：總分 6.0–6.5 的 50 題改寫 question、hook、payoff 後複評，39 題上升、29 題過 6.5（6.5 以上的單集題 104 → 133）。問句越長效果越大。
  奇聞長題案：36 組改片名、追問與章節講法，23 組採用且都過 6.5（可成題長題案 23 → 46）。
  原來如此長題案：29 組改寫後平均升幅 −0.03，沒有採用任何一組；那個池的片名已經夠好，改包裝沒有空間。做法、校正方式與雜訊的註記在奇聞池 README〈獨立觀眾評分〉。
  還沒做：奇聞中一題、尚未評分的 499 題單集題（估過關率約兩成）；舊題庫檔裡 5 題 6.0–6.5 的單集題。
- 2026-11-17 八續：奇聞中一題、還沒評過的 499 題單集題評完（`reviews/audience-20261117-one.json`），116 題總分過 6.5。
  入選單集題已評 856 題，6.5 以上 249 題。下一步最划算的是把這批落在 6.0–6.5 的 97 題送去改包裝（49 題問句超過 150 字）。
- 2026-11-17 九續：中一題那批 6.0–6.5 的 88 題改包裝（`audience-20261117z-repack4`–`7`），41 題採用且都過 6.5。入選單集題 6.5 以上 290 題。
  沒做：舊題庫檔裡 6.0–6.5 的 14 題（寫回位置與批次檔不同）；N2501 的 answer_target 被覆核註記蓋掉，題卡待修。
