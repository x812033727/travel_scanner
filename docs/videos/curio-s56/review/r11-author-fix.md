# S56 R11 作者前置結論移除與窄幅來源／畫面修稿

2026-10-20 UTC。這是針對 [R10 正式敘事 OR 合併 HOLD](r10-clean-merge.md)和 [R10 獨立來源／書面畫面 HOLD](r10-source-independent.md) 的**作者候選稿**，不是作者自判任何關卡 PASS。R10 兩位乾淨讀者均指出 `s56079` 先說出西岸大火過河合流，令 `s56174` 的片尾答案變成重複；正式 OR 為 12／13，唯一未過的必答題是 `no_recap`。來源覆核另指出 `s56112` 無據的「催車」，以及開場 `s56011`／`s56013` 在福斯特尚未回旅館收行李前，就畫出他手上的小箱子。R10 的正式 CLI、來源 HOLD 與任務均凍結後，才改這份 R11 稿。

| 凍結輸入 | R11 SHA-256 |
| --- | --- |
| `brief.md`（與 R10 相同） | `09f731c13f1037c963aa5774b936a43e1a187b5c4ae8d09ba158581a705f1a52` |
| `research.md`（與 R10 相同） | `59549e98e6ae258cedfc5b43e6684ecaa1102284d0dee13b0beef6443e4a6fb7` |
| `claims.md` | `8edaf18bee138c3dc88dd2e38e7eebd2c27a9e24158dc0bed696fb4e53904a80` |
| `video.json` | `297b576499068e12fb937bc6032394cf9408f8543065b762a95c6b26ef89cd72` |
| `script.md` | `38ef6dfdbb71bd0b59a441a4d41fc4a89b2b3aed288899a28ec902193b792d2c` |

## R10→R11 精確口說差異

| ID | R10 凍結句 | R11 作者候選句 |
| --- | --- | --- |
| s56079 | 他寫，西岸大火後來過河，與東岸新起的火連成一片。 | 那處火附近還有什麼，讓福斯特決定離開？ |
| s56112 | 箱子上了車，他立刻付錢，催車往北側走。 | 箱子上了車，他按約付錢，坐車往北側走。 |

`s56079` 不再提前交代河兩岸火勢合流；它轉成下一個近距離疑問，`s56081` 隨即用福斯特看見鄰近煤氣設施、因而後退的見聞作答。`s56080` 的小木屋仍在同一景，未改。原伏筆 `s56076→s56079` 改成 `s56076→s56174`，讓消防車分兵後西岸火勢是否越河到片尾才回收；新增 `s56079→s56081` 作煤氣設施的短伏筆。**`s56173`、`s56174` 及其主張列、畫面原樣保留**，片尾的合流是全稿唯一一次口說答案。沒有聲稱知道某一塊燃燒木塊完整跨河的路徑，也沒有聲稱若消防車未分兵必然能守住。

Foster F420–428 明記箱子上車後按約付款，F430–459 記他隨車北行並過橋；未記催促車夫。因此 `s56112` 只留下裝車、付款、坐車北行，`claims.md` 原有兩段固定來源和「先裝箱，不提前付款」畫面界線均保留。Foster F349–383 記新火旁有木屋和煤氣設施，他認為應離開；新 `s56079` 是對這段的問句，不替他增添恐懼或新的行動。`claims.md` 只有這兩個口說格更新，另把導言的 R10 作者候選時點改成 R11；其餘 **152** 列、引文與畫面界線沒有改。`brief.md`、`research.md`、YouTube description、章節、字卡、縮圖及其餘口說沒有改。

## R10→R11 精確書面畫面差異

| ID | R10 凍結 prompt | R11 作者候選 prompt |
| --- | --- | --- |
| s56011 | Wide shot, the traveler holds a small case beside a wooden bridge approach, faint fire glow | Wide shot, the traveler stands beside a wooden bridge approach at Sunday night, faint fire glow |
| s56013 | Close shot, a hand grips a small case beside the river railing, low fire glow | Close shot, a hand grips the river railing at Sunday night, low fire glow |
| s56079 | Close shot, the traveler backs away as two nearby fire fronts meet, soft shadowed light | Close shot, a man in a tan coat peers past burning wooden shanties on the South Side at Sunday night, ember light |

前兩景只拿掉當時尚未收拾的隨身箱，讓橋與河邊的開場鉤子留下；兩景均是星期日夜間，不展示某塊飛火穿越水面。`s56079` 原本把兩片火會合畫得太早，現在僅示意他走近東岸小木屋火點、尚未看見下一景的煤氣設施。三景鏡頭運動及其餘資料欄位不變。R10 獨立報告提到 `s56107` 的代詞可以更清楚；那是非阻斷的後續精度建議，本輪依合併任務只修三個阻斷畫面／口說問題。

## 作者機械檢查與下一關

作者保存的 R10 三檔本機原樣副本位於 `/tmp/s56-r10-r11-author-preimage/`，其 SHA-256 精確回到 R10 凍結：`video.json` `e54a6dfde678a536e81eac36c13360782e5e1efad6c2c30c694cefc5e01098f8`、`claims.md` `4fc2b9887afe5805340c553d7c099658ce5231d8f27b836c621842477f14a172`、`script.md` `286b7d50bc21ee8c8c5f61d99a3744f988ca1cbdac2c80bef05237a74f585153`。逐場 JSON 比較顯示只有上表 **2** 個口說、**3** 個 prompt、原伏筆一筆改接及新伏筆一筆；沒有刪場景或改動其他影片資料欄位。`claims.md` 除兩個口說格與導言時點外沒有其他變化。這些差異相對已凍結 R10，不聲稱更早 R6 全檔位元差分。

`node tools/video/cli.mjs script --slug curio-s56` 已重產劇本，`script.md === screenplay(video.json)`。R11 有 **154** 個唯一逐句 ID、`claims.md` **154** 列全文逐項一致、**121** 景（**118 shot／3 big**，shot **97.52%**）和 **18** 條有效且前設早於回收的伏筆。`narrative_hash=7673b92858cdf86b`、`speech_hash=9ae33c04c1986d95`。`node tools/video/cli.mjs lint --slug curio-s56 --json` 回 **0 errors／0 warnings**。在 **250 字元／分鐘的文字估計**下，開場 **59.33 秒**、正文 **11:39.63**；在 325 字元／分鐘下，開場 **48.33 秒**、正文 **9:26.87**。這不是 R11 實測 TTS。`npm run check:tasks` 和空白差分檢查結果見 R11 任務。

請未撰稿者依五檔 SHA 重新審固定來源、主張和書面畫面，再由兩位無前情讀者審 R11 敘事並正式 OR 合併；只有通過後才進政策與音訊關卡。R10 的盲評、來源 HOLD、政策停點和舊音訊均不能作 R11 判票。作者沒有代投獨立 PASS、盲評票或政策判定，也沒有執行付費 TTS、插圖、配樂、成片或發布。
