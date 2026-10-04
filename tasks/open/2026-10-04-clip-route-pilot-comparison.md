---
id: 2026-10-04-clip-route-pilot-comparison
title: 《偶的江湖》第 1 集用 Hailuo 網頁方案試播：寫 22 分鐘劇本、伺服器畫關鍵影格、Hailuo H3 做片段、匯入合成，量點數與畫質後定畫面等級
status: in-progress
priority: P1
area: ops
owner: claude
claimed_at: 2026-10-04T14:52:34Z
created_at: 2026-10-04T02:48:09Z
completed_at:
branch: claude/vibrant-cray-mdpjzx
depends_on: []
scope:
  - docs/videos/pilots/ou-de-jianghu-e01-hailuo
  - docs/videos/ou-de-jianghu-e001
---

# 《偶的江湖》第 1 集用 Hailuo 網頁方案試播

## Why

站主 2026-10-04 決定《偶的江湖》的片段直接走 Hailuo 網頁方案（hailuoai.video，站主的 Max 帳號），不再跑 Kling、Hailuo、伺服器三路比價（本票原本的範圍，已改掉）。整部 780 集的錢與產能取決於第 1 集量到的數字：一集約 440 鏡、約 1,900 片段秒；H3 2K 每秒 12 點（2026-10-04 實測一支），Max 每月 27,000 點，全片段一集約 22,800 點、hybrid 約 9,120 點；同時只跑 2 支，一支 5 秒約 4 分 40 秒，全片段一集約 20 小時生成。圖生影片的關鍵影格上傳、768P 的點數與輸出尺寸、2K 縮成 1080p 的畫質都還沒量過。

## Definition of done

- [ ] 第 1 集〈幽皇之女〉的 22 分鐘劇本（`docs/videos/ou-de-jianghu-e001/video.json` 與 `script.md`）過了 lint、查核、聽眾審稿與劇本關卡；名台詞的等價句在劇本最上面標出，站主核可（路線圖決定第 16 項）。
- [ ] 關鍵影格由伺服器畫、judge 通過；每個片段鏡在 Hailuo 以關鍵影格當首格生成 H3（2K 為主，抽 10 鏡另做 768P 對照），下載無水印版，用 `clips import --provider hailuo-web --plan hailuo:max --credits <差額> --judge` 匯入。
- [ ] `docs/videos/pilots/ou-de-jianghu-e01-hailuo/ledger.csv` 每支一列：鏡號、解析度、秒數、送出前後點數、送出到完成時間、輸出寬高與 fps、浮水印、QC 結果、第 0 格 PSNR、judge 分數、備註。
- [ ] 合成出第 1 集，`README.md` 寫結論：一集實際用掉的點數與小時、2K 與 768P 的取捨、畫面等級（clips／hybrid／stills）定案，以及換算到第一、二季 24 集與一個 Max 月能做幾集。

## Steps

- [ ] 0. 前提：第 1 集是 22 分鐘，普通漫劇上限 8 分鐘，要走 long-anime-v1（`docs/videos/LONG-ANIME-PRODUCTION.md`）；先查它接不接受 `open_ended: true` 的作品（企劃包 `plan.json` 的 long-anime-policy gap）。不接受就先開票補政策，或把第 1 集當沒有 production profile 的手動試播集處理（`clips import` 只收沒有 profile 的集）。
- [ ] 1. 撰稿：照企劃包 `season-01.json` 第 1 集與 `setting.json` 寫 video.json（人物表逐字沿用、外觀提示詞用 setting 的 appearance），跑 lint、查核、聽眾審稿，送劇本關卡給站主。
- [ ] 2. look 與關鍵影格走伺服器（約 440 張 × US$0.134，重拍上限約三倍），storyboard 核准。
- [ ] 3. Hailuo：要在站主自己的電腦上做。雲端 session 沒有瀏覽器工具；內建瀏覽器也傳不了本機檔案，要用 Claude in Chrome 的檔案上傳，或 Playwright 用 `launchPersistentContext` 指向站主登入過的 profile。比例預設 21:9 要改 16:9；H3 時長是 4–15 秒整數，照 `clips --dry-run` 的需求秒數；每支送出前後記點數；下載走「全部下載 → 無水印下載」。程序在 `.agents/skills/animation-production/references/providers-and-plans.md` §1.2 與 `stage-preconditions.md` 最後一節。
- [ ] 4. 每支 `clips import`；H3 2K 輸出是 2560×1440、24 fps，`assemble` 會重編進 1080p 30 fps 的時間軸，畫質要看一眼。
- [ ] 5. 配樂、合成、字幕、成片；寫 README 結論與 ledger。
- [ ] 6. 量到的 Hailuo 數字另開 tools 票更新 `providers-and-plans.md` 與 `episode_estimate.mjs` 的 PLANS（本票不改 skill）。

## How to verify

```bash
node tools/video/cli.mjs status --slug ou-de-jianghu-e001        # clips generated 後面列出 imported: hailuo-web N
node .agents/skills/animation-production/scripts/run_report.mjs docs/videos/ou-de-jianghu-e001/video.json
npm run check:tasks
```

## Notes

- 2026-10-04 改範圍：原本是 Kling CLI、Hailuo 網頁、伺服器 Lite 三路比價；站主決定直接用 Hailuo，比價取消。
- 事前估算（未驗）：全片段一集 2K 約 22,800 點，佔 Max 一個月 84%；hybrid 約 9,120 點，一個 Max 月約 3 集。Max 點數用完後的無限模式只給 Hailuo 2.0／2.3，不含 H3。
- 關鍵影格要是 judge 通過的那一張，否則第 0 格 PSNR < 22 會 `needs_review`；`clips import` 看不出浮水印，下載完自己看右下角。
