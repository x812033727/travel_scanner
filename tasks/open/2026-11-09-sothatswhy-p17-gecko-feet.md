---
id: 2026-11-09-sothatswhy-p17-gecko-feet
title: 原來如此事務所對話版：P17 壁虎黏得住，怎麼又能走得動？
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-focused-hopper
claimed_at: 2026-11-09T00:00:54Z
created_at: 2026-11-09T00:00:49Z
completed_at:
branch: claude/focused-hopper-zq70n8
depends_on: []
scope:
  - docs/videos/sothatswhy-p17-gecko-feet
  - docs/videos/lexicon.json
---

# 原來如此事務所對話版：P17 壁虎黏得住，怎麼又能走得動？

## Why

原來如此事務所對話版（所長＋小問）的下一集。題目照 `docs/videos/so-thats-why/refresh-20261101/EPISODES.md` 的 P17，
做法照 `docs/videos/so-thats-why/dialogue-pilot-20261103/HANDOFF.md`、README §9–§10，以及 PR #2048 的
`docs/videos/explainer-series/`（兩邊衝突時以共用區為準）。

## Definition of done

- [x] 稿子：獨立查核 `verify-1.md`、盲評 14 題全過、`lint` 0 錯誤，Claude 依站主授權核准。
- [x] 旁白兩個聲音、`check-audio`，核准；角色設定圖沿用系列。
- [x] 插圖畫完、另一個代理逐張放大檢查、分鏡評分 ≥ 49／70，核准分鏡。
- [x] 配樂（`sothatswhy-bed-r2.m4a`）→ 合成 → `qa` 11 項 → 成片送站主（`final`）。
- [ ] 上架確認、八語翻譯與配音、八語縮圖、語言包，站主核准。
- [x] 每過一關備份到 `transfer/sothatswhy-p17-gecko-feet`（`docs/videos/explainer-series/backup/tobranch.sh`）。

## How to verify

`node tools/video/cli.mjs status --slug sothatswhy-p17-gecko-feet`；`lint` 0 錯誤；站主在 /admin/videos 看過成片。

## Notes

- 2026-11-09：稿子四輪盲評才全過（5 → 3 → 2 → 0 題不過）；亞里斯多德那段整段刪掉（查核發現原文是爬樹、跟主線無關）。
  `Tokay`、`gecko` 依站主要求加進 `lexicon.json`，用英文念。
- `check-audio` 一直把「十億」聽成「十一」、「撕貼紙」聽成「是貼紙」、「腳趾」聽成「餃子」：改說法比重錄有效。
- 旁白 12:56；插圖報價 US$1.71（三 take 上限 US$5.14），2026-11-09 開始 `keyframes --takes 3`。
- 容器磁碟只剩約 6 GB，`.git` 裡有舊備份留下的約 4.8 GB loose objects（舊 tobranch 寫法），清理指令被自動模式擋下，等站主決定。
- 2026-11-09：站主要求刪 P07／P14 工作目錄騰空間。獨立代理第一次核對發現 P07 的 en/ja/ko 逐句配音等 741 檔（288 MB）、P14 三個 JSON 不在 GitHub；
  兩個工作目錄整個用新版 `tobranch.sh` 推到 `claude/backup-sothatswhy-p07-p14` 的 `local-20261109/<slug>/`（head 5683fbcf，verify 0），
  同一代理只看 GitHub 重跑 `coverage.sh`：兩集 missing 0、mismatches 0、`.SPLIT` 0 不符，才刪；磁碟 6.1 → 7.7 GB。
  兩邊都沒有的（早在 11-07 就沒了）：兩集繁中逐句旁白、P07 其餘五語與 P14 八語的逐句配音（成品配音在分支與 YouTube）。
- 2026-11-09：`keyframes --takes 3` 跑了約 4.5 小時，127 景裡 67 景三個 take 都沒過評審（多半是「半身畫成全身」「所長沒有鉛筆／灰髮一撮」）。
  照 PR #2048：不用 `--accept-best`，四個沒畫過圖的代理逐張看全圖加四格 2× 放大挑圖，挑中的用 `repin.py` 固定。
- 放大檢查三輪：第一輪 107 景挑到圖、20 景全不能用（小問帽兜拉起、馬尾丸子頭、飄浮問號、物件上有臉、三條腿壁虎）；
  改提示詞重畫後 15 景過；剩下 5 景都是小問，第三輪把特寫改半身（特寫一直出照片風）後 4 景過，
  `kid-dust-q` 照 #2048「三次不過換同章已過的圖」改用 `kid-tap-q` 的圖，旁白不變。127 張用 `repin.py` 固定，`pins.json` 放在工作目錄 `keyframes/`。
  教訓：`build_scenes.py` 禁用 no／not，修正要正面寫；小問的提示詞要明寫 hood folded down、bare black bob uncovered。
- 分鏡評分（兩個獨立代理）：50／70，補畫後 51／70，過門檻；2026-11-09 依站主授權核准分鏡。
  第四輪把腳趾捲起、小毛角度、頭髮粗細改成圖解重畫，結果長出臉和假字，退回原提示詞；只留下撕貼紙與四張重抽的角色。
  **坑：`keyframes --shot` 重畫會用同一個檔名蓋掉先前挑中的 take**，挑中的圖要先備份或另存。4 張舊圖靠伺服器同提示詞重現救回（byte 相同），4 張用放大檢查留下的副本補回（`*-pick.jpg`）。
  已備份到 `transfer/sothatswhy-p17-gecko-feet`（20799d61，verify 0）。
- 2026-11-09：合成 24271 格（約 13:29），-14 LUFS；`qa` 11／11（警告：縮圖大字與標題前 10 字重複，縮圖在關鍵影格前定案，未改）。
  先備份成片再 `review-push --gate final`，已送 /admin/videos 等站主核准；核准後 `review-pull` → `package` → `--gate publish`。
- 2026-11-09：站主核准成片與上架包。八語由四個代理翻譯（對齊 P07／P08），`i18n-merge` 全過；配音 ja 縮 4 句、id 縮片尾口頭禪；
  es／pt／th 中途 ECONNRESET，`speech-journal.mjs forget` 後重跑。八語縮圖逐張看過（en/ja/pt 原本被紅印章蓋住，改短）。
  th 說明加上 17 筆來源超過 5000 bytes，濃縮中段。
  **坑：非 worker 做的集，`languages.json` 不會自動從站上抄下來**，`package` 只打包 en/ja/ko；
  用 `/api/video/reviews/<slug>` 的 `locales` 照 `writeLanguages()` 寫進工作目錄後重打包，才有 8 軌。
  備份 `transfer/sothatswhy-p17-gecko-feet` 206b42b5（verify 0）後送語言包，`review-files --dry-run --gate languages`：dub／縮圖／字幕／說明各 8。
  剩：站主核准語言、上傳 YouTube、記下影片網址後 `npm run tasks -- done`。
