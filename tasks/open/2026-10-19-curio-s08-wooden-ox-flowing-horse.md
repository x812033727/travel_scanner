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

2026-10-19：第五位從未看本集舊稿的讀者對上段 SHA 給 **11/13**，唯一必答未過是 `wood-025` 沒明示回呼而第三次平述 231 木牛運糧；章名建議題也未過。來源抽核指出 `wood-073`／`wood-094` 不能說不知道孔對應哪類木件，因裴注已有「前軸孔／前脚孔／前杠孔」等名稱。這一輪改為明示「運」與「畢」的回呼，開場章名寫糧隊出發，孔位界線限於**完整連接次序與唯一復原**；詳見 `verify-6.md` 與 `blind-5.json`。**現行待全新盲讀版本** `script.md` SHA256 `8f4346554d24203b8c38aecfdb20059dd3dc7922452412406678546534023f6a`、`video.json` SHA256 `5058f34fc1e908ac6b42360126ac17eef7d8db537c38ae90d6b10f72cc83d676`；93 句、87 張插圖、4 張資料卡，估 9.1 分鐘，`lint` 0 errors／0 warnings。**沒有現稿 13/13、沒有 S08 劇本核准或付費媒體。**

2026-10-19：第六位全新讀者對上段 SHA 給 **12/13**；唯一必答未過是 `wood-066` 提早念「日行二十里」，到 `wood-104` 又念「群行者二十里」卻沒明示回呼。上一輪的 `wood-025` 回扣和章名已獲本輪通過；固定原文抽核亦無實質矛盾。已只從 `ox066` 刪去與當句重量問題無關的「日行二十里」，在 `ox104` 完整保留特行／群行新資訊，詳見 `verify-7.md`、`blind-6.json` 與封存答案。**現行待最後獨立覆核版本** `script.md` SHA256 `dac8ec628f68e5902c05257fb789f5591f1804bebd6d2f9146ac80fc3c794fbf`、`video.json` SHA256 `daec765ef4d2ac28a13b2b28d655b2f6fce5130972255593becded6dc5f4c3b4`；93 句、87 張插圖、4 張資料卡，估 9.0 分鐘，`lint` 0 errors／0 warnings。**沒有現稿 13/13、沒有 S08 劇本核准或付費媒體。**

2026-10-19：第七位全新讀者對現行 `dac8ec628f68e5902c05257fb789f5591f1804bebd6d2f9146ac80fc3c794fbf` 劇本盲讀 **13/13**，現稿 `no_recap` 已過；裴注所引的特行／群行里數也用固定卷 35 抽核，無實質史料衝突。原始答卷見 `blind-7.md`；同證據寫入 `narrative-answers.json` 後，工具 `narrative --answers` 顯示 passed，詳見 `verify-8.md`。劇本和來源文字保持此 SHA 不變。**下一步：**依站主 2026-10-19「以你推薦的就好不用問我，一直做完所有影片」廣泛委託，準確註明站主未逐字審稿地記錄 A 案／劇本本機核准，再跑 TTS 和 `check-audio`；S08 插圖仍需等共享 MiniMax 時段安排。

2026-10-19 20:42 UTC：S08 A 案 outline／精確劇本 script 本機關卡已依站主廣泛委託記錄，備註明寫**站主未逐字審稿**；Gemini Sulafat `tts --dry-run` 93 句／約 2,156 字元、月額度足夠，正式 TTS 已啟動（工作目錄 `curio-s08/tts-run.log`）。完成後先跑 `check-audio`，任何發音問題只修有問題的句子並重做必要查核。S08 插圖尚未啟動，等 S03／S30 共享 MiniMax 額度安排。

2026-10-19 21:24 UTC：首版 Gemini 93 句約 09:51；`check-audio` 初次列 30 句複查並對 `ox079` 回 `OTHER`。30 句按原稿重唸後約 09:48，再查降至 **12 句標記**，但 `ox079` 仍無法判定。五句高風險處一次作來源安全的口語修訂，原始與新稿的 SHA、逐句原因見 `docs/videos/curio-s08/verify-9.md`。**目前新稿 `script.md` SHA256 `6a9218c4a2ce2a159c141a0aebb634fcfa9e1af0140b8e3b13d06c608b407111`，93 句、87 張插圖，lint 0／0；尚待新讀者重做 13 題與五句來源抽查，不沿用舊版 13／13。**收到新 exact-SHA 覆核通過後，重綁 script 關卡、只重唸改動句並重跑音檔複核；S08 插圖仍未啟動。

2026-10-19 21:31 UTC：`6a9218…` 獨立讀者回 **12／13**，只因 `ox066` 的「一歲糧」在 `ox068` 平述為「一年的糧食」；五句來源抽核通過。已僅改 `ox068` 為明答「不能」並補出未說供幾人吃，避免再述同一載重片語。**現行待全新讀者覆核稿** `script.md` SHA256 `6499e8521bf040c7cc5fe8557dccaca15623b0ff13bf2f1a1cc99bf7e7e06233`、`video.json` SHA256 `57250cf3c6d91d107f9e7b7e40388b51e9177c8c5d8eed271bfe8f18390f6903`；93 句、87 張插圖，lint 0／0。詳見 `verify-9.md`，此稿尚無 13／13 與新劇本核准，沒有 S08 插圖。

2026-10-19 21:36 UTC：`6499e852…` 新獨立讀者再回 **12／13**，`ox066`→`ox068` 已過，唯一 `no_recap` 問題是開場 `ox007`「一腳四足」到正文 `ox057` 再念未明說回扣；固定來源與畫面描述檢查無實質矛盾。已對全文開場／正文重複作一輪掃描，僅將 `ox057` 改為「開頭那句」明示回扣、補原句在木牛段及相鄰「方腹曲頭」。**現行待全新讀者覆核** `script.md` SHA256 `54974b5cb36c0f3ecbc889fe4bc84c185a4bcd53f75964a47d684e1d307c4113`、`video.json` SHA256 `721671fbce11eb96d6d3d502505a7ab83a2e100d5f06db5deff12e1fdf1e63d4`；lint 0／0，尚無新 13／13 或重核准，沒有 S08 插圖。歷次原始結果保存在 `verify-9.md` 列出的路徑。

2026-10-19 21:49 UTC：新讀者對現行 `54974b5cb36c0f3ecbc889fe4bc84c185a4bcd53f75964a47d684e1d307c4113` **13／13 全過**，確切答卷與史料邊界見 `docs/videos/curio-s08/verify-10.md`。`review-push --gate script` 已送站台；代理依站主廣泛委託於本機重新核准確切稿，備註明寫站主未親自逐字審此次改稿。TTS dry-run 93 句中 6 句需合成、約 166 個 Gemini 字元；已啟動只重念改動句。**下一步：**等待 TTS 完成，全文 `check-audio`，只對真正有問題的句子重念或逐句修訂；音檔清楚前不啟動 S08 插圖，且需與主代理協調共用 MiniMax 額度。

2026-10-19 21:56 UTC：現稿 Gemini Sulafat 93 句音檔完成，實測 **09:51.633**；第一次現稿 `check-audio` 標 10 句，定向重錄該 10 句後再查 93／93，仍有 **7 句標記、退出碼 1**。詳見 `docs/videos/curio-s08/verify-11.md`（列確切句號、聲音雜湊、機器報告及未解風險）。沒有本機可用的第二 ASR 或人工實聽；已 `review-push --gate audio` 送站台待審，**沒有假稱旁白已核准**。S08 付費插圖尚未開始，需等音訊問題解決與共用 MiniMax 排程。
