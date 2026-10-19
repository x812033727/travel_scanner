---
id: 2026-10-19-curio-s08-wooden-ox-flowing-horse
title: Curio S08 Wooden Ox and Flowing Horse new history episode
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-curio-s08
claimed_at: 2026-10-19T19:18:00Z
created_at: 2026-10-19T19:18:00Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s08
---

# Curio S08 木牛流馬到底長什麼樣？

## Why

站主要求持續製作新的歷史系列影片；S08 是未認領的 S 軸候選。《三國志》卷 33、35 留下 231 年木牛、234 年流馬的運糧紀錄；裴注所引《諸葛亮集》有一串木牛流馬形制文字，足以查清「書上寫了什麼」，卻不能直接畫出確定外形。軍糧問題在兩次使用後仍存在，是能沿史料推進的故事懸念。

## Definition of done

- [ ] 固定可讀文本並獨立覆核年代、來源層級與《諸葛亮集》形制文字。
- [ ] 完成企劃、逐句史料對照、約十分鐘繁中劇本、敘事盲讀和 lint；未核准的復原形狀只作假說。
- [ ] 依 `curio-episode` 關卡完成旁白、插圖、分鏡、配樂、字幕、影片與上架包；付費媒體與站台權杖留在工作目錄。

## Steps

- [x] 查無 S08 同題認領，持有 `docs/videos/curio-s08` 窄 scope；不改共用 `topics.json` 或其他集數。
- [x] 先核《三國志》卷 33 的建興九、十、十二年紀錄，以及卷 35 裴注引《諸葛亮集》；另一固定轉錄能核對關鍵詞但稀字有 OCR 錯誤。
- [x] 起草 A 案、研究筆記與逐句主張，處理小說增飾和現代復原說法的證據界線。
- [ ] 劇本／敘事／來源獨立覆核後進入媒體製作；與主代理協調付費插圖批次。

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s08`；`node tools/video/cli.mjs narrative --slug curio-s08`；來源逐句核對 `research.md` 固定版本。後續依序 `tts`、`check-audio`、`keyframes`、`qa`、`package`。

## Notes

2026-10-19：第一版可讀固定來源為 Ancient-China-Books `sanguozhi` commit `10a0b1ab3019d8821262f7402366d14fb4aaa102` 卷 33 p10/p11/p13 與卷 35 p13/p14/p17；第二轉錄為 daizhigev20 commit `4a6d6f2088825f132521d848c2ea86cf9c9a7620`，稀字有 OCR 錯誤。卷 33 說建興九年始以木牛運，十年作流馬木牛畢，十二年始以流馬運；十年「畢」不能解讀成兩者那年才發明。卷 35 說木牛流馬出諸葛亮之意，形制數字則是裴注引《諸葛亮集》，來源層次要明標。「一腳四足」、軸孔與尺寸不能單憑字面證明四腳步行或有幾個輪子；不以現代復原模型當古代原物。Needham 書是可查線索，雲端代理阻擋直接閱讀前不引其具體說法。小說第 102 回的司馬懿仿造和舌頭機關只作小說。

2026-10-19：A 案 `brief.md`、`research.md`、`claims.md`、`video.json`、`script.md` 已存檔。現稿 98 句、92 張插圖、4 張資料卡、10 個回收懸念，估 9.1 分鐘；`lint` 0 errors／0 warnings，`script.md` SHA256 `6f3a8c3fc98793d8b08888fb848762577aad8e6db6196ae4dcfe51fd69aa17a2`。開場的小說舌頭情節已停在結果揭曉前，末章章名改成發現。裴注本來有「舌著於腹」，但**轉舌即停**是小說第 102 回的動作，稿子已分清。TTS dry-run：98 句、約 2,170 Gemini 字元；MiniMax `keyframes --takes 3 --dry-run`：92 張，一次約 US$1.24、三輪上限約 **US$3.73**；目前未合成語音、未付費生圖。**下一步：**新讀者只看定稿做敘事 13 題盲讀，另一人固定原文抽核；通過後才進媒體關卡。請勿把前製草稿說成已獲站主逐字核准。

2026-10-19：第一位新讀者對上一版給 **9/13**：`no_spoiler`、`no_toc`、`chapters_link`、`no_recap` 未過；固定原文抽核沒有重大史實衝突，詳見 `docs/videos/curio-s08/verify-1.md`。我依具體行號集中修正，歷程和新加的兩句來源見 `verify-2.md`。**現行待再盲讀版本** `script.md` SHA256 `610088e368d54aad532322a43f5ba959caa637c666afe518c5cf80b3af527360`、`video.json` SHA256 `3ee02c5bbd8fa7b33a2dad4a7ad453356eb08915975e379eb331acd5bc51ca49`；95 句、89 張插圖、4 張資料卡、11 個懸念、估 9.1 分鐘，`lint` 0 errors／0 warnings。最新版 MiniMax dry-run：一輪約 US$1.20、三輪最多 **US$3.60**；Gemini dry-run 約 2,166 字元。**尚未獲最新版 13/13 盲讀，也沒有 S08 付費媒體。下一步是新讀者審此 exact SHA。**

2026-10-19：第二位完全獨立讀者對上段 SHA 給 **12/13**，只剩 `wood-035`／`wood-037`／`wood-038` 重述「流馬首次明載運輸」；四處新句史料抽核支持，另指出 `ox025` 的「作成」原為意譯，不宜用原文引號。修正刪 `wood-038`，`ox024`、`ox025` 轉成無引號的「完工」，`wood-026` 保留「作流馬木牛畢」原句；小說固定連結補足 40 字 commit。詳見 `verify-3.md`。**最新待新盲讀版** `script.md` SHA256 `58aa04c75fc1474ea281d8cd2a230e797c7e712388060a931a9c108b75b98dc1`、`video.json` SHA256 `80426b34dfd51d491066c561ff1810ce92607283f45f17a151e2eb9312360c58`，94 句、88 張插圖，`lint` 0 errors／0 warnings（約 9.0 分鐘，目標 9–11 分鐘）。TTS dry-run 94 句／約 2,148 Gemini 字元；MiniMax dry-run 88 張、一輪約 US$1.19／三輪最多 US$3.56。**未啟動 S08 付費媒體，也未作最新版敘事或劇本核准。下一步：新讀者只看此 exact SHA 回答 13 題，通過後再協調媒體。**

2026-10-19：第三位完全獨立讀者對上段 SHA 給 **8/13**；新發現是開場 `ox002` 提早說流馬、`ox023` 重述缺糧、`ox075` 問題未明確回答、`ox108` 軍紀岔開主線，以及 `ox025`「不是初造」不能排除流馬於 232 年初造。詳見 `verify-4.md`。已一次集中修訂：開場留名稱懸念，刪 `wood-023`，分清兩種「腳」的文字限度，將 `ox108` 改成卷 35 確載的「相持百餘日」，並限縮 232 年的首造說法。**現行待再盲讀版** `script.md` SHA256 `769a2b5257ba91b5fdd9da375357fc3ba9d299d0ef8d29a082400531b1c083af`、`video.json` SHA256 `a99a9cb1a6fef9fbd8c3cbb45974ee3aec418574986abb3909a0cb518191a69d`；93 句、87 張插圖、4 張資料卡，`lint` 0 errors／0 warnings，估 9.0 分鐘。**仍沒有 S08 付費媒體或現稿核准；下一步新讀者只讀此 exact SHA 回答 13 題，另對改寫的 231／232 與百餘日句做來源抽核。**

2026-10-19：第四位完全獨立讀者對上段 SHA 給 **10/13**：`payoffs`、`no_recap` 未過，另有章名事件化建議。來源抽核抓到更重要的一處：`ox065` 原把「牛不飲食」誤接到裴注引文，固定史書只有「而人不大勞」，後出小說有「牛馬不食」。已集中修正引文歸屬、兩個開場問題的明確回收、反覆問軸孔的末段，並把章名改為可見行動；詳見 `verify-5.md`。**現行待全新盲讀版本** `script.md` SHA256 `6423bd004802f6350c41bd0aa5e3e27bcdc7e31c343b314d6d8de98e7c01bdc3`、`video.json` SHA256 `96502f8729fd418696ab2111fa0f0e7ebea6f49aea85f106f6517c7988917f56`；93 句、87 張插圖、4 張資料卡，`lint` 0 errors／0 warnings，估 9.0 分鐘。TTS dry-run：93 句／約 2,146 Gemini 字元；MiniMax dry-run：87 張、一輪約 US$1.17／三輪最多 US$3.52。**沒有現稿 13/13、沒有 S08 劇本核准或付費媒體；下一步是新讀者只看此 exact SHA 回答 13 題並抽核改寫句。**
