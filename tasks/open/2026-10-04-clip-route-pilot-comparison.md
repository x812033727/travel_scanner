---
id: 2026-10-04-clip-route-pilot-comparison
title: 試拍比價：同兩鏡在 Kling CLI、Hailuo 網頁、伺服器 Lite 各生一支，量點數、解析度、速度、PSNR 後定整部的片段路線
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-10-04T02:48:09Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/pilots/clip-route-comparison-20261004
---

# 試拍比價：同兩鏡在 Kling CLI、Hailuo 網頁、伺服器 Lite 各生一支，量點數、解析度、速度、PSNR 後定整部的片段路線

## Why

站主要做 22 分鐘一集、12 集一季的長篇漫劇（企劃包 `docs/videos/series-plans/ou-de-jianghu`）。一集約 440 鏡，片段路線決定整部的錢與產能：伺服器 Veo Lite 一集 clips 約 US$300、Hailuo Max 2K 約 US$169、Kling Ultra 約 US$122（最後這個是第三方的「一支 5 秒 40 點」，沒有人驗過）。三條路線的價目與限制在 `.agents/skills/animation-production/references/providers-and-plans.md`，但 Kling 付費方案在 CLI 上有沒有 1080p、每支扣幾點、3–4 秒的片段怎麼算，Hailuo 的圖生影片上傳、768P 的點數與輸出尺寸、Hailuo 2.3 無限模式的畫質與慢隊列速度，全部未驗。在花幾千美元之前，用同樣兩個鏡頭在三條路線各做一支，把數字量出來。

## Definition of done

- [ ] 同一部試拍的同兩個鏡頭（一個 3 秒對白鏡、一個 6–8 秒動作或運鏡鏡），各在 Kling CLI、Hailuo 網頁（H3 2K 與 768P）、伺服器 Veo Lite 1080p 生成至少一支，首格都用通過 judge 的關鍵影格。
- [ ] `docs/videos/pilots/clip-route-comparison-20261004/ledger.csv` 每一支一列：路線、方案、模型、要求的解析度與秒數、送出前後點數與差額、月費攤的美元、送出到完成的時間、輸出寬高／fps／秒數、有沒有音軌、有沒有浮水印、`clips import` 的 QC 結果與第 0 格 PSNR、judge 分數、主觀備註（角色是否像設定圖、動作是否自然、有沒有自己切鏡）。
- [ ] `README.md` 寫結論：每條路線一集 440 鏡的實測換算（點數、美元、小時）、哪條路線整部用、哪些鏡頭類型例外，以及還沒解決的事。
- [ ] 量到的數字另開一張 tools 票更新 `providers-and-plans.md` 與 `episode_estimate.mjs` 的 PLANS（本票不改 skill）。

## Steps

- [ ] 0. 試拍素材：在後台建一部 one-off 漫劇試拍（slug 建議 `ou-de-jianghu-pilot`），用期一的角色（沈歸鶴、姬無霜）寫 4 個鏡頭：A 對白鏡 3 秒（鎖定）、B 動作鏡 6 秒（推進）、C 運鏡鏡 8 秒（橫搖）、D 對白鏡 3 秒（備用）。跑 `look`、`keyframes` 到每鏡的關鍵影格通過 judge，`review-pull` 核准 storyboard；`clips --slug <SLUG> --dry-run` 抄下每鏡的需求秒數與 clip prompt。伺服器約 US$3–5。
- [ ] 1. Kling：站主買一個月 Pro（首月 US$25.99），自己在瀏覽器完成 `kling login`（代理不碰 `~/.kling/.credentials`）。`kling account` 記 `membershipType` 與 `availableRemainCredits`。`kling file_upload` 傳 A 與 B 的關鍵影格；`kling image_to_video --model kling-video-v3_0 --first_image <A> --duration 3`（或 4）與 `--first_image <B> --duration 6`，都傳 `enable_audio=false`、`prefer_multi_shots=false`，提示詞用 dry-run 的 clip prompt；每支送出前後各跑一次 `kling account`，差額就是點數。再用 B 做一支 `--duration 8`，看 8 秒扣多少。`query_tasks` 記送出與完成時間。`ffprobe` 記寬高、fps、秒數、音軌。若列出的模型仍只有 720p，記下來，這條路線的 1080p 就是沒有。
- [ ] 2. Hailuo（站主的 Max 帳號，代理在站主登入的 Claude in Chrome 或 Playwright persistent profile 裡操作；內建瀏覽器傳不了關鍵影格）：`/create/image-to-video`，上傳 A 的關鍵影格當首格，H3、16:9（預設 21:9 要改）、2K、4 秒；再做 B 的 H3 2K 6 秒、A 的 H3 768P 4 秒。「創建」旁的扣點數與送出前後餘額各記一次；下載走「全部下載 → 無水印下載」，右下角看一眼沒有浮水印。另做一支 Hailuo 2.3 1080p 6 秒（A 的首格），當無限模式的畫質樣本；慢隊列速度無法在點數用完前量，記為未量。
- [ ] 3. 伺服器對照：`node tools/video/cli.mjs clips --slug <SLUG>` 用 Veo 3.1 Lite 1080p 把 A、B 買下來（固定 8 秒，各 US$0.64 加 judge），帳本與 `clips/manifest.json` 就是數字。
- [ ] 4. 每一支外部片段 `node tools/video/cli.mjs clips import --slug <SLUG> --shot <id> --file <mp4> --provider kling-mcp|hailuo-web --plan <方案> --credits <差額> --usd <月費攤> --judge --note "<路線、模型、解析度、秒數、送出與完成時間>"`，同一鏡第二支加 `--force` 前先把第一支的結果抄進 ledger。記 QC 結果、第 0 格 PSNR、judge 分數。
- [ ] 5. 把三條路線的每秒點數與美元換算到一集 440 鏡（clips、hybrid、stills 三個等級）、一季 12 集，寫進 README 的結論表；比畫質時三條路線的 A 鏡並排截第 0 格與第 60 格。
- [ ] 6. 開 tools 票更新 skill 的價目表與估價腳本；在 `ou-de-jianghu` 的 README 成本一節引用本票的結論。

## How to verify

```bash
ls docs/videos/pilots/clip-route-comparison-20261004/   # ledger.csv、README.md、每支的 ffprobe 輸出
node tools/video/cli.mjs status --slug <SLUG>           # clips generated 後面列出 imported: kling-mcp N, hailuo-web N
node .agents/skills/animation-production/scripts/run_report.mjs <VIDEO_DOCS>/video.json   # 匯入的與買的分開列
npm run check:tasks
```

ledger.csv 每列都要有送出前後兩個點數讀數、ffprobe 的寬高與 fps、`clips import` 的結束碼；缺一項就不算量到。

## Notes

- 事前估算（未驗，2026-10-04）：一集 440 鏡約買 1,900 秒。Hailuo H3 2K 每秒 12 點（實測）、768P 7 點（推算）；Max 27,000 點／月 US$199.99，一集 clips 2K 約 22,800 點 ≈ US$169 月費攤，一個 Max 月做 1 集 clips 或 3 集 hybrid，同時只跑 2 支、一支 5 秒約 4 分 40 秒。Kling 假設標準模式一支 5 秒 40 點，Ultra 26,000 點／月 US$180，一集 clips 約 17,600 點 ≈ US$122，同時 4 支；Pro 3,000 點只夠試拍。伺服器 Lite 1080p 固定 8 秒 US$0.64 一支，一集 clips 約 US$300。
- 決定規則（站主 2026-10-04 同意的順序）：Kling 一支 4 秒 ≤ 45 點且 1080p 確認 → 整部走 Kling Ultra；Hailuo 2.3 無限模式畫質可用 → 長篇改走 Hailuo Max 固定月費；兩者都不成立 → 留在伺服器 Lite，hybrid 等級。
- 不在本票：改 production profile、改 skill 價目、生成試拍以外的任何集。試拍的 slug 沒有 production profile，`clips import` 才收得了外部路線。
- 關鍵影格的 sha256 要抄進 ledger 的 input_sha256 欄，首格不是那張圖的片段第 0 格 PSNR 會 < 22 而 `needs_review`。
- Kling 帳號 2026-10-04 是 NORMAL、0 點、只列 720p 模型；本票第 1 步之前站主要先付費。
