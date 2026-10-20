# S56 R6 獨立史料、主張及書面畫面覆核 — PASS

2026-10-20 UTC。我未撰寫 S56 R6。於 [作者凍結交接](r6-author-fix.md)後，獨立重取固定原文並核對 [R5 來源 HOLD](r5-source-independent.md) 的修處。**目前五檔雜湊的史料、逐句主張與書面畫面關卡 PASS。**此票不代表敘事盲評、實際生成畫面、實測語音或付費媒體放行。

## 凍結輸入與原文

| 檔案 | 本次重算 SHA-256 |
| --- | --- |
| `brief.md` | `09f731c13f1037c963aa5774b936a43e1a187b5c4ae8d09ba158581a705f1a52` |
| `research.md` | `59549e98e6ae258cedfc5b43e6684ecaa1102284d0dee13b0beef6443e4a6fb7` |
| `claims.md` | `998828f1c155adade66fed0943aca1dd20a7cab11e7902dfd4ccdda4aec957ef` |
| `video.json` | `8a784899560b00f51fbb9b0b17cb60c7f788bfcbabf0a6e7ea3e9f654ed08b7d` |
| `script.md` | `65b7423f682b25f962bc2536a0c96064ea326afbbc64fae5bbaa324816710efb` |

五值皆與作者 R6 凍結表一致。重新下載 [Foster 固定版](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt)，全文 SHA-256 為 `59d5d0740ecf20583374d499ab3aff481c000d45d20685b548490b90fc3062ee`；[Loesch 固定版](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt)，全文 SHA-256 為 `d1e6575eb2af0a36a99aacfc9c94817f38e460db81746cd4cc95199e18d1f011`。兩值與 `research.md` 相同。Foster 是 1871 年家書的 1923 年家人抄本印刷版；Loesch 是 1925 年回憶，不能把其時刻當官方逐分紀錄。

## R5 HOLD 修處

| 位置 | 來源與書面畫面覆核 |
| --- | --- |
| `s56151–s56153` | Loesch 說約早上六點**搭車向北**到 Fullerton／Racine 的友人家借住 [L516–522](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L516-L522)；白天在 North／Fullerton 一帶走動 [L537–545](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L537-L545)；**日落前返回**借住處 [L578–584](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L578-L584)。原文不說白天最後一段路的方位。R6 `s56152` 只問日落前在哪裡安身，`s56153` 只答回到清早借住的屋子；兩列都補了清晨定位及日落返抵引文。`s56151` 畫面只見木街面與籬笆著火；`s56152` 只畫他在北側街道停步，無方向提示、無難民隊伍；`s56153` 只畫借住處門前和附近草地，未重建精確路徑。Loesch 另說大批難民**多往西**過 Webster Avenue 橋 [L560–575](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L560-L575)，R6 沒有再把他們與洛許的返抵畫成同一路線。木街面和籬笆供火延燒亦見 [L547–557](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L547-L557)。 |
| `s56154–s56155` | R5 重述「回到暫住處」的 `s56154` 已整景刪除；ID、場景、主張列皆不存在。`s56153` 之後直接進入草地及南側火勢。 |
| `s56166–s56167` | Loesch 自述星期二**約 1:30**，最後房屋將燒到草地前大雨落下 [L601–613](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L601-L613)。R6 `s56166` 口說句與主張列都以「洛許回憶」歸屬此鐘點，並限於此避難地；雨景只有田野落雨，未畫全城同分鐘熄滅。`s56167` 只收回未用的浸布逃離備案，符合原文雨先到、眾人沒有跑過草火。 |

保留的 [R4 獨立來源覆核](r4-source-independent.md)及 [R5 除 HOLD 外的覆核](r5-source-independent.md)承接其餘未更動的史料判斷。R5 五檔只有雜湊和審閱紀錄，工作區未留 R5 原檔快照，因此不能重做**逐位元** R5→R6 差分；上表核的是 R5 HOLD 所列變動在目前凍結 R6 的實際文字、引文與畫面。R6 相對 R5 審閱紀錄少一口說句、一景，研究全文雜湊未變。`claims.md` 導言仍寫「R5 作者修稿」；這是過期版本標示，與逐句事實或連結無衝突，若整理須重凍結五檔。

## 機械核對與關卡界線

`video.json` 有 **170** 個唯一遞增的逐句 ID、**137** 景（134 插圖景、3 字卡）、**7** 章、**17** 個有效且前設早於回收的 loop。`claims.md` 恰有 **170** 列，ID 和口說全文依序逐一相同，每列至少一個來源；**258** 個連結全指向兩個固定 commit 的指定原文，行號均在重新下載的全文內。`script.md` 與程式 `screenplay(video.json)` 逐位元一致。

`node tools/video/cli.mjs lint --slug curio-s56 --json` 為 **0 errors／0 warnings**；`git diff --check HEAD -- docs/videos/curio-s56` 通過。按工具的文字估計，250 字元／分鐘時開場 **59.57 秒**、正文 **769.07 秒**；325 時開場 **48.50 秒**、正文 **624.30 秒**。均達 30–60 秒開場和 8 分鐘正文的規劃門檻。59.57 秒離上限很近；實測 TTS 若超過 60 秒，需在音訊關卡重檢。

R5 史料與書面畫面 HOLD 已在上述 R6 雜湊解除。下一關可交給**兩位未接觸前情的讀者**各自正式盲評；本票不代替盲評、R6 TTS 聽審、生成插圖驗收或成片檢查。
