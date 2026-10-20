# S33 前製交接（2026-10-20）

題目：崔萬理等人為何先讚造字「神妙」，又向世宗上疏反對。站主尚未在 `/admin/videos` 選企劃或核劇本；本集**沒有**配音、購圖、音樂或成片。

## 定稿與覆核

| 檔案 | SHA-256／狀態 |
| --- | --- |
| `brief.md` | `b1cfc6aff2db4cf64a4f3e3fa1784d929d97f5a441ee23328101bf0c81f946a2`；後台能解析 A（推薦）與 B 兩選項。 |
| `script.md` | `3db98a782e552385def131784e1dc4c8096e2bceb36e10e58cb75a277e004815`；95 句，約 9.8 分鐘。 |
| `video.json` | `f88c9269709a34272a58ccc6bb59bdacf1b417d0a95e10c8bcb99ab6b4f572ef`；93 景、87 插圖提詞、5 短引卡、12 個伏筆。 |
| `claims.md` | `496caad73962337fbc9b18640f8f1cdf276dbd210af3af90432d3b8451807581`；正文 `hj001`–`hj092` 各有來源節點。 |

來源是 `research.md` 固定 commit 的三卷《世宗實錄》XML（SHA 見該檔）；第三方鏡像尚未對韓國官方掃描。逐句作者覆核見 `verify-1.md`，獨立原文二讀及修改差分見 `verify-r2-source.md`、`verify-r3-source-delta.md`、`verify-r4-source-delta.md`、`verify-r6-source-delta.md`。最新版雙盲：R6 11/13、R7 13/13；按系列「同題兩人皆 No 才不過」規則為 13/13，R6 的兩項具體疑慮和保留理由見 `verify-r6-r7-editorial.md`。`lint` 0 errors、3 個畫面用詞重複 warnings；`npm run tasks -- check` 通過，有其他任務的既有 warnings。

## 後台關卡

2026-10-20 已執行 `review-push --gate outline` 與 `review-push --gate script`。第一次 outline 提交綁較早 `brief.md` SHA `d7253dd958046067b7cb47f32f3eac2991d703dee88cbebf2a0ebd04db1178f9`，工具未解析出選項；隨後已將同一 A/B 內容轉為工具接受的選項格式，重新提交綁上表新版 SHA。Jev 對新版建議 **A**；CLI 同時明說本機 `hand_pushed` 須站主逐關決定，故 Jev 建議**不是站主核准**。`review-pull --gate outline` 和 `--gate script` 均回 exit 3 `waiting for the owner`。請在後台按上表 `brief.md` 雜湊認新版卡片；如舊零選項卡仍可見，以新版為準。

待站主真正選案及核此劇本後，用 `review-pull` 把兩項決定與精確檔案雜湊記回本機，才進行 TTS／音質檢查。插圖有 87 景，仍需整集一次報價與授權；之後按系列畫風製作、原生尺寸查看嚴重矛盾、分鏡站台審核、成片與字幕 QA、Shorts 和上架包。所有卡片和素材應維持史料歸屬；尤其 `是月` 不得被改成造字／成書的某個單日。

## 後續：站台核准 R7，政策修訂為 R8

13:22 UTC 本機從網站 `review-pull` 真實取得 A 大綱核准（網站決定 08:37:51.658928Z，`brief.md` SHA `b1cfc6aff2db4cf64a4f3e3fa1784d929d97f5a441ee23328101bf0c81f946a2`）與 R7 劇本核准（08:37:55.235935Z，`script.md` SHA `3db98a782e552385def131784e1dc4c8096e2bceb36e10e58cb75a277e004815`）。兩關確實是後台站主決定，不是 Jev 自動通過。

R7 配音前政策預檢卻因業配 0.36 超過 0.30 而 FAIL。只把 `hj999c` 的口播訂閱邀請改成中性來源連結提示，片尾畫面的訂閱圖形仍在；R8 劇本 SHA `1a1d52712593055ed5d427696b273bdc7cf28de7736ef90c5ee98a0431a3556e`、`video.json` `e0d7fed0c81ce7db2ff2a971e177d4fdef831d5bea5afe6523804f9d8ad965ae`、`claims.md` `2f38d279e7eb2d6b34584c9ed853e3de1efd695a6d5a87921685d5c116e68fd0`；新版政策一次通過（立場 0.86、建議 0.01、業配 0.01）。作者差分見 [verify-r8-source-delta.md](verify-r8-source-delta.md)；root 另一人獨立來源／書面畫面 PASS `/tmp/s33-r8-root-independent-source-visual.md`。`lint` 0 errors、4 warnings，新增警告僅因片尾不口播訂閱。87 張圖的乾跑報價一輪約 US$1.17、三輪最高約 US$3.52，無實際支出。

R8 尚待兩名新盲讀者審敘事並重送網站劇本卡。**R7 的真實站台核准對 R8 已失效**；R8 未合成語音、未付費製圖、未生成音樂或成片。使用者授權採推薦方案可供下一步在明確記錄本機代決與站台 pending 的情況下推進；兩種狀態須分開。需重測實際旁白正文 ≥8 分鐘，再做原生畫面 pilot、完整素材、片頭片尾與上架包。

## 最新：R9 雙盲未過，R10 等待獨立審查

上段為 R8 時點快照。R8 雙盲皆判 `no_recap` No；R9 消除重複並補來源內的答辯，獨立來源／書面畫面審查 PASS（[收據](verify-r9-source-independent.md)），但兩名全新 R9 盲讀者又皆判 `payoffs` No：開場問四天後上書的精確時機原因，原文未交代。R10 作者只修 `hj005`、`hj019`、`hj086` 及相應伏筆／claims；[完整差分及五檔 SHA](verify-r10-source-delta.md)。開場估 44 秒、正文 1,916 漢字、95/95 主張對齊，`lint` 0 errors。接手者須先獨立來源／畫面差分與兩名**全新**劇本盲讀者對 R10 同一 SHA 完成 13 題，再做 R10 exact policy 與劇本 gate。R7 站台真實核准、R9 政策 PASS 都不可移作 R10 核准；未買 TTS、圖像或音樂。合成後量測正文 ≥8 分鐘，通過全句音質檢查，再按整集報價上限做原生插圖 pilot。

## 14:25 UTC 最新：R10 語音仍有 32 旗標，暫停開畫

上段的「待」為當時狀態；R10 已有 [獨立來源差分 PASS](verify-r10-source-independent.md)、[新雙讀合併 PASS](reviews/narrative-r10-merged.md)（A 一項 No 保留）、[精確政策 PASS](reviews/policy-r10.json)。網站 R10 劇本卡手動送出後仍 pending；本機另以使用者持續授權記 `LOCAL DELEGATED` exact R10 劇本核准，勿稱網站站主核准。頻道聲音合成 98 句，定點補錄 11 句一次後，實測開場 48.833 秒、正文 **9:41.533**、片尾 21.767 秒、總旁白 10:52.133。全句音檢由 35 旗標降至 **32 旗標**，詳 [音訊收據與硬停點](verify-r10-audio.md)。尚未送 audio gate 或製作插圖；付費圖帳仍 US$0，三景 1K pilot 的上限與驗收見 [計畫](reviews/art-pilot-r10.md)。需取得獨立第二轉錄或實聽核對，才能判斷其餘近音疑點；不可重複盲補錄並虛稱音訊零旗標。片頭、片尾圖形、配樂、MP4、連結包均未製作。
