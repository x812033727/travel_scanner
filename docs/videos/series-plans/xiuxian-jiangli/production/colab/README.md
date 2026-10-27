# Colab 路線：在 Google Colab 直接打 MiniMax API 做第 1 集

站主 2026-10-27 定：不用海螺網頁、不用站上伺服器，在 Colab 用 MiniMax API 生 H3 影片。這條路線 `animation-production` 的 skill 列為「CLI／MCP 另選方案」，這裡是它的第一次實作。

## 檔案

| 檔 | 是什麼 |
| --- | --- |
| `e001-jobs.json` | 工作清單：3 張定妝照（image-01，3:4）、45 張首格（image-01，16:9，帶該鏡第一個角色的定妝照當 `subject_reference`）、42 支片段（H3 v2 圖生影片，正文與 SHA-256 逐字等於 `../e001-plan-lock.json` 的鎖定正文，秒數照鎖定的 `buy_s`）。小樣 s33–s35、靜圖 s10／s19／s31 不買片段。由 `video.json` 與鎖定檔產生，**改分鏡要重產、重鎖**。 |
| `xiuxian_e001_minimax.ipynb` | 筆記本。`STAGE` 依序 `refs` → `pilot_frames` → `pilot_clips` → `poll` →（站主看過小樣）→ `frames` → `clips` → `poll` → `report`。每次付費請求寫一筆收據到 Drive 的 `receipts.jsonl`；`MAX_USD` 總停損；take 上限首格 3、片段 2；`ONLY_SHOTS` 加 `REDO` 重做單鏡。 |

## API 形狀（照 `apps/api/app/video_media/providers/minimax.py` 的 adapter，不是猜的）

- 圖：`POST {BASE}/v1/image_generation`，`{model:"image-01", prompt, aspect_ratio, response_format:"base64", n:1, prompt_optimizer:false, subject_reference:[{type:"character", image_file:<data URL>}]}`；提示含 Avoid 要 **< 1500 字**（jobs 已檢查，最長 1466）；`base_resp.status_code` 0 才成功。
- 片段：`POST {BASE}/v2/video_generation`，`{model:"MiniMax-H3", resolution:"2K"|"768P", duration:4..15, content:[{type:"text",text}, {type:"image_url", image_url:{url:<data URL>}, role:"first_frame"}]}`；查 `GET {BASE}/v2/query/video_generation/{task_id}`，`task.status` 是 `queued`／`running`／`succeeded`／`failed`，成功時 `task.content.url` 是影片；1026／1027 是內容被拒、2013 是參數錯。H3 有首格時**不能帶參考圖**（官方，互斥），所以臉只靠首格。
- 國際站 `https://api.minimax.io`，中國站 `https://api.minimaxi.com`。

## 錢（platform.minimax.io，2026-10-03 讀；在帳號上核對）

| 項 | 一次 | 上限 |
| --- | --- | --- |
| 定妝照 3 張 | US$0.01 | US$0.03 |
| 首格 45 張 | US$0.16 | US$0.47 |
| 片段 42 支、169 秒、2K | US$21.97 | US$43.94 |
| 小樣 3 支 | US$1.56 | US$3.12 |

比海螺網頁（期望 2,749 點，約 US$34 月費攤）便宜，而且不用站主的瀏覽器。768P 便宜四成（每秒 US$0.08），小樣先用 2K 看畫質再決定。

## 跟鎖定包不同的地方（這條路線自己的風險）

1. **首格的臉**：image-01 的 `subject_reference` 一次只收一張人像，兩人鏡（s01、s07、s12、s15、s16、s26、s34、s39、s42）只帶第一個角色的定妝照，第二個人靠文字；catalog 也註明「subject_reference 不保證同一張臉」。小樣要先看 s34（兩人）的臉。不行的備案：那幾鏡改用 H3 的參考生影片（最多 9 張參考圖、不帶首格），但產線的 `clips import` 要首格 PSNR，得手放。
2. **沒有 judge**：首格與片段都沒有站上的 judge 評分，靠人在 Colab 逐張看（筆記本每張都顯示）。
3. **嘴型**：H3 對「speaks a short Mandarin line」的反應跟海螺網頁同一個模型，照《種田》的經驗會動嘴，但本集還沒驗。
4. **方括號運鏡**：正文用 H3 官方的運鏡句子（鎖定檔已組好），不用 2.3 的方括號。

## 拿回產線

1. 本機先做聲音：`node tools/video/cli.mjs tts --slug xiuxian-jiangli-e001`（或《種田》的 `local/rec.sh` 流程），拿到 `timeline.json`；再跑 `shot_plan.mjs --timeline` 看買的秒數有沒有變（全部 ≤ 4 秒，應該不變）。
2. 把 Drive 的 `xiuxian-jiangli-e001/` 拿回 `<VIDEO_WORKDIR>/xiuxian-jiangli-e001/`：`refs/`、`first-frames/sNN-tK.png`、`clips/sNN-tK.mp4`、`receipts.jsonl`。
3. 兩條接法：
   - **照《種田》3D 國漫版**：`docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/assemble-v4.mjs <video.json> <overlays.json> <edit.json> <workdir> <out.mp4>`，它直接讀 `first-frames/` 與 `clips/`，疊面板、切素材、配樂；要寫一份 `edit-e001.json`（片名卡、名牌、分場調色、配樂 cue）。面板樣式要從淡藍改成藍金色書頁。
   - **走產線**：每支 `node tools/video/cli.mjs clips import --slug xiuxian-jiangli-e001 --shot sNN --file clips/sNN-t1.mp4 --provider external --usd 0.52 --note "route=colab-minimax-api task=<task_id>"`；但 import 會對產線自己畫的關鍵影格算第 0 格 PSNR，這條路線的首格不是產線畫的，要先把 Colab 的首格放進 keyframes manifest（還沒做過，見 `stage-preconditions.md`）。先走上面那條。
4. 收工：收據裡每支的 `prompt_sha256` 要等於 `e001-plan-lock.json` 的；`report` 那格印總花費；實際 take 數回填 `e001-lock-package.md` 第 9 節。
