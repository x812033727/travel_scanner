---
id: 2026-10-20-curio-s47-wright-first-flight
title: Source and outline Curio S47 Wright first flight
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T13:18:56Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s47
  - tasks/open/2026-10-20-curio-s47-wright-first-flight.md
---

# Source and outline Curio S47 Wright first flight

## Why

站主請持續做新的歷史系列長片，S41／S43／S44／S45／S46 各有前製或畫面關卡。本票另開 S47：用萊特兄弟 1903-12-17 四趟飛行解釋流行的「只有 12 秒」及當天電報 57 秒／後述 59 秒的來源差異。素材須固定版本、保留見證等級，畫面用原創可愛插畫，不冒充 1903 年照片。

## Definition of done

- [x] 有可重新下載、核 SHA 的參與者文字與 NPS 小冊，逐個重要事實標出原文行段及不可推論處。
- [x] A／B 大綱和推薦 A 已落地；100 句 R1 劇本、`video.json`、逐句 `claims.md` 與靜態檢查可交下一位獨立查核者。
- [x] R6 精確版本通過另一人來源／書面畫面差分、兩位全新盲讀的正式合併裁決及一次 Jev 政策檢查；網站大綱與劇本 `hand_pushed` 關卡仍待進行。**此票的前製完成不代表影片完成**。

## Steps

- [x] 比對既有 S 軸題庫及開啟任務，選不重複的萊特兄弟「四次飛行」。
- [x] 下載 GITenberg 固定 commit 的 Wright 後述與 NPS 小冊，核對 SHA；寫 `research.md` P01–P16。
- [x] 寫 `brief.md` A／B、推薦 A，明確區分電報小冊轉錄與參與者後述。
- [x] 寫首版可愛插圖劇本、提示詞與 `claims.md`，生成 `script.md`，`lint` 0 errors／0 warnings。
- [x] 寫 `verify-1.md` 記版號、靜態估時、影音製作邊界與下一關。
- [x] 獨立查核、兩位全新盲讀與 Jev 政策已對同一 R6 精確版本通過；本地推薦 A 和劇本已備好交網站審核，旁白與原生圖仍屬後續關卡。

## How to verify

在 repo 根目錄：

```bash
VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s47 --json
npm run test:docs-videos
npm run check:tasks
```

第一項已於 2026-10-20 執行，0 errors／0 warnings；後兩項由整體 PR 協調者在推送前重跑。劇本未經聲音實測，不可引用估時當成成片時長。

## Notes

本環境 NPS／Gutenberg 網站直接抓取被 403 擋住；GITenberg GitHub API 和固定 raw 連結可用，兩份來源與 SHA 都在 [`research.md`](../../docs/videos/curio-s47/research.md)，毋須從頭搜尋。R1 精確檔案 SHA、講稿 100 句、保守估時正文 8:07.1、等待的審查與原生畫面風險均在 [`verify-1.md`](../../docs/videos/curio-s47/verify-1.md)。NPS 作者解釋 57 秒是電報傳送差錯；本稿把它保留為**作者判斷**，不宣稱核過電報原紙。旁白／繪圖／配樂未付費，網站尚無任何 S47 推送或核准。所有媒體關卡依 `curio-episode`、`youtube-video`。2026-10-20 交回協調者等待另一人獨立查核與兩位盲讀；此任務若轉手，請先對 `verify-1.md` 所列 SHA 再比對目前檔案。

2026-10-20 R1 獨立來源與書面畫面審核判 **HOLD**；R2 已按逐項意見修正並記於 [`verify-2.md`](../../docs/videos/curio-s47/verify-2.md)。R2 凍結 `script.md` SHA `14ee6c750eb9f335ef11d9f52d57a6c202f29bf7084c258d7afd2e75555b09ef`、`video.json` SHA `e1d76c9335511afd3faf28a56de9fe7450aec90817e1b9886d209265327a725e`、`claims.md` SHA `d0e514de7adc028fbe5ca58694343efbf56ea5417f97b664df59180c1bc5407f`。100/100 句逐字相符、lint 0 errors／0 warnings、325 單位／分鐘的正文靜態估時 8:08.7。R2 仍待新的獨立來源／畫面差分與兩位全新盲讀；不能沿用 R1 結果或宣稱站台核准。交還協調者前請先核三檔 SHA。

2026-10-20 R2 獨立來源／文字畫面差分 **PASS**，但兩位新敘事盲讀各 11/13、10/13，`no_recap` 與 `chapters_are_events` 共同 No，另 B 判 `no_spoiler` No，故 R2 正式 **FAIL**。R3 窄修已凍結，詳細差分、估時與待審關卡見 [`verify-3.md`](../../docs/videos/curio-s47/verify-3.md)。R3 `script.md` SHA `d4572e39a9f08d5bbeaab8b3c81354e3a5877d8b85682d11fb72599759e361ff`、`video.json` SHA `9d97c4e50fbca0c3cc5854f45e147ddf4a3f4dc89ca38453990425454a1cdd7d`、`claims.md` SHA `5a416f85fb3bf78646bf31e6edeef7327bd9e08c4eac3c664c61c9bd8176ac3c`；lint 0／0、100 句逐字相符，保守靜態正文 8:09.3。R3 仍待**新的**獨立來源／畫面差分及兩位全新盲讀；R2 PASS 不移用，無站台核准或媒體支出。

2026-10-20 R2 後續：另一位審核者重新對固定 W/N 全文與 R1 HOLD 清單核對，判[新稿來源和書面畫面差分 PASS](../../docs/videos/curio-s47/review/r2-source-independent.md)；兩位全新敘事盲讀、政策、站台及媒體仍待進行，沒有付費語音或圖片。

2026-10-20 R2 雙盲結果：兩位此前未讀 S47 的讀者對相同 R2 SHA 分別答 11/13 與 10/13，均判 `no_recap`、`chapters_are_events` No；B 另判 `no_spoiler` No。正式敘事 **FAIL**，詳見 [`verify-2.md`](../../docs/videos/curio-s47/verify-2.md) 與原報告 `review/r2-blind-{a,b}.md`。R3 應刪 `wr019/020` 的立即重複和片尾四趟重述，把章名改為事件，並檢查開場 `wr006/007` 是否提前給結果；不得新增無來源飛行數字。來源差分 PASS 只適用 R2 原版，不會自動轉移到改寫後的口播。無付費媒體或站台核准。

2026-10-20 R3：作者修訂後，另一位審核者按 W/N 固定文本與 R2 PASS 清單核對改動，判[精確 R3 來源和書面畫面差分 PASS](../../docs/videos/curio-s47/review/r3-source-independent.md)。這不是 R3 敘事或實際圖像的裁決；仍須兩位全新盲讀同一 R3 版本。無付費媒體或站台核准。

2026-10-20 R3 新雙盲 [A 9/13、B 10/13](../../docs/videos/curio-s47/verify-4.md)，共同必答 `no_spoiler`、`no_recap` No，正式敘事 **FAIL**。R4 要把開場斷軸／山坡失敗留在結果之前，刪 8 匹門檻與修機期望的相鄰重述，並把電報秒數問題問成來源可以回答的比較；另檢查 `wr008` 是否像目錄。修後重凍結、重做來源差分與新雙盲，不能直接沿用 R3 PASS。無付費媒體或網站核准。

2026-10-20 R4：精確凍結雜湊見 [`verify-5.md`](../../docs/videos/curio-s47/verify-5.md)；另一位覆核者以固定 W/N 文本對新開場、八匹後的新增經驗、修機期望及電報差兩秒重核，判[來源及書面畫面差分 PASS](../../docs/videos/curio-s47/review/r4-source-independent.md)。這不是敘事或原生圖 PASS；兩位真正全新 R4 盲讀仍待完成，無付費媒體或網站核准。

2026-10-20 R4 [新雙盲](../../docs/videos/curio-s47/verify-6.md) A 12/13、B 11/13，共同必答 `no_recap` No，正式敘事 **FAIL**。R5 集中修 `wr084/094`、`wr092/095` 電報兩秒比較時的明確回呼；另檢查 B 指出的 `wr064` 機頭控制問題是否得到原文可支持的答案。重新凍結、獨立查核及兩名新讀者後才能前進，無付費媒體／站台核准。

2026-10-20 R5 作者窄修與機械自查見 [`verify-7.md`](../../docs/videos/curio-s47/verify-7.md)。`wr064` 改問前舵控制難處，`wr065` 直接用 W 回答；電報段明確回呼 `wr084`／`wr092` 的兩數，再新增 N 轉錄未報地面英尺數與 W 後述的比較。精確 `script.md` SHA `e3d615643941c04d2c17f6fa39d185306ff9c3993eebb62ed1947d87bc92b392`、`video.json` `a421a3b05102fecb533ef09120a4e992897c284f9a2924421b5d27f04fcffbae`、`claims.md` `831a556638d57de46b282af0d4eab7fd9c3ae037c421b7cf2747d273543c19bd`。100/100 句逐字相符、lint 0／0；250 單位／分鐘含停頓的開場 57.33 秒，325 單位／分鐘估正文 8:13.4，均僅靜態估算。**R5 須由另一人來源／書面畫面差分、兩名真正新讀者盲讀**，R4 PASS 不移用。無站台核准、付費媒體或成片。

2026-10-20 R5 [獨立來源與書面畫面差分](../../docs/videos/curio-s47/review/r5-source-independent.md) **PASS**：重開 W/N 固定全文，`wr065` 是 W 首趟前舵轉動難處之一，`wr093–095` 明確區分 W 後述地面距離與 N 轉錄電報缺的數字、編者對兩秒差的判斷，書面提示詞沒有冒充原電報。此 PASS 綁上列精確 R5 雜湊，**不是**敘事盲讀或實際生成圖裁決；仍需兩位真正新讀者，無站台核准、付費媒體或成片。

2026-10-20 R5 [兩名全新讀者盲讀](../../docs/videos/curio-s47/verify-8.md)各 12/13，兩人共同把必答 `no_recap` 判 **No**：`wr097` 片末又說 `wr091` 已在電報中說的四趟；A 另指 `wr010–011` 連續重說重量／馬力，B 提醒操控片段的相似回述。正式敘事 **FAIL**。R6 只修真正重複，保留 `wr093` 明確「回看剛才」及其新數據對照；改稿後重做來源及兩名新盲讀，付費媒體與站台仍未開始。

2026-10-20 R6 作者窄修、來源界線與機械自查見 [`verify-9.md`](../../docs/videos/curio-s47/verify-9.md)。`wr011` 分開引擎重量與整機重量並設新伏筆；`wr076–079` 分開著地結果、奧維爾的後述判斷與小冊 11:40 新時點；`wr085` 改給小冊低空／強風原因；`wr097` 改用小冊所引威爾伯觀點收尾，不再重念電報四趟。精確 `script.md` SHA `0dd8a74680d53b3133401b03495454df79564c23a0335dace21c8f13e38d3603`、`video.json` `3d8e87514a92de3ac42a2c3fadb23d5e1e0a54033be36daf27a9265506e15d45`、`claims.md` `9675fb565211d4d2cc80a038aa18ea29db62a396bcf8cb0a7d6d214b77a090ae`。100/100 句逐字相符、lint 0／0，325 單位／分鐘靜態正文 8:15.8。**R6 尚須另一人查來源／書面畫面及兩位真正全新盲讀**；R5 來源 PASS 不移用，未站台核准、未買媒體。

2026-10-20 另一人重開固定 W/N 來源，對精確 R6 改動[獨立史料與書面畫面差分 PASS](../../docs/videos/curio-s47/review/r6-source-independent.md)：引擎與整機重量、第三趟著地與操控解釋、小冊低空原因、Wilbur 後述均各有原文支撐，提示詞未冒充測量原件。兩名真正新讀者的 R6 敘事裁決仍待，來源 PASS 不等於影片或網站核准。

2026-10-20 R6 [正式關卡紀錄](../../docs/videos/curio-s47/verify-10.md)：兩名全新讀者分別 12/13、13/13，A 對 `no_recap` 判 No，B 判 Yes 並給新比較／回呼例證；依 `mergePanelVerdicts` 合併 **PASS**，分歧與工藝備註完整保留。精確口播的一次 Jev 政策檢查 HTTP 200、`passed: true`；本地推薦企劃 A 及 `script.md` SHA `0dd8a74680d53b3133401b03495454df79564c23a0335dace21c8f13e38d3603` 交站台審核。網站大綱／劇本 `hand_pushed` 尚未提交或核准，未付費製作任何媒體，沒有成片。

2026-10-20 [網站與旁白關卡續作](../../docs/videos/curio-s47/verify-11.md)：僅將 `brief.md` 兩個 A／B 標題改成工具可辨識格式；兩選項送站台、Jev 推薦 A，但人工推送網站大綱及劇本均 **pending**。私有 `approvals.json` 記站主既有「採推薦」指示的**本地委派**選案與劇本雜湊，不冒充網站核准。語音預檢 100 請求、約 2740 計費字元、Gemini Sulafat 可用；實際語音與查核另記。舊 `brief.md` 獨立來源收據的雜湊已被兩個標題格式修正改變，需另看精確差分；劇本、來源與提示詞未變。

2026-10-20 Gemini Sulafat 實際旁白已製作：100 個請求、2740 計費字元、總長 11:18.77，其中 30–60 秒濃縮開場量得 54.20 秒，正文 10:10.07。[首次完整音訊檢查](../../docs/videos/curio-s47/review/r6-audio-check-1.md)查 100/100 句、0 漏查，**22 旗標，結束碼 1**；11 句高風險差異先待真正獨立聽者或第二套盲轉寫核對。無可信獨立音訊證據時不清旗標、不開畫；尚無圖片、配樂、成片或可點片尾連結。精確 SHA、站台待審及下一步詳見 [`verify-11.md`](../../docs/videos/curio-s47/verify-11.md)。
