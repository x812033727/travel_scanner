# S56 R6 作者修稿與獨立覆核交接

2026-10-20 UTC。這是依 [R5 獨立史料與書面畫面 HOLD](r5-source-independent.md)做的**作者候選稿**，不構成自我核准。R5 盲評前的敘事修正保留；本輪只處理洛許返抵借住處的行走方向、畫面及雨的回憶時間歸屬。

| 檔案 | R6 SHA-256 |
| --- | --- |
| `brief.md` | `09f731c13f1037c963aa5774b936a43e1a187b5c4ae8d09ba158581a705f1a52` |
| `research.md` | `59549e98e6ae258cedfc5b43e6684ecaa1102284d0dee13b0beef6443e4a6fb7` |
| `claims.md` | `998828f1c155adade66fed0943aca1dd20a7cab11e7902dfd4ccdda4aec957ef` |
| `video.json` | `8a784899560b00f51fbb9b0b17cb60c7f788bfcbabf0a6e7ea3e9f654ed08b7d` |
| `script.md` | `65b7423f682b25f962bc2536a0c96064ea326afbbc64fae5bbaa324816710efb` |

## R5 → R6 精確修正

- `s56152` 現在只問「日落之前，洛許會在哪裡安身？」；`s56153` 只答「他回到清早借住的屋子。」不宣稱白天最後一段路往北。他約早晨六點搭車到 Fullerton／Racine 借住 [L516–522](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L516-L522)，日落前回到暫住處 [L578–584](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L578-L584)；原文沒有寫白天返程方向。主張列改引用這兩段定位與返抵文字。
- `s56152` 的畫面改成北側街道上的洛許，沒有朝北空地的方向提示，也不和搬家難民同鏡。那些難民多數往西過 Webster Avenue 橋 [L560–575](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L560-L575)，不再藉畫面把兩條路線混成一條。`s56153` 畫面只示意借住處門口與附近草地；`s56151` 同時去掉未證的「洛許正朝北走」畫面動作，只拍他看見木街面／籬笆起火。
- 刪去緊接 `s56153`、再說一次回到暫住處的 `s56154` 整景，使問答之後直接轉到草地和南側火勢。`s56166` 改成「洛許回憶，星期二凌晨約一點半，大雨趕在火燒到草地前落下。」；精確時刻明示為 Loesch **1925 年回憶** [L601–613](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L601-L613)。`s56167` 仍只回收未用的浸布備案，不重講雨。

`claims.md` 與口說句同步，`script.md` 由 `video.json` 重新產生；`brief.md` 僅更新下一關狀態，`research.md` 固定原文和來源界線未變。

## 作者機械檢查與下一關

`node tools/video/cli.mjs lint --slug curio-s56 --json` 回 **0 errors／0 warnings**。稿內有 **170** 個唯一、遞增的逐句 ID、**137** 景（134 插圖景、3 字卡）、七章及 **17** 個仍指向現存 ID 的伏筆；`claims.md` 恰有 170 列並逐句一致，產生的 `script.md` 每句各收一次。`git diff --check HEAD -- docs/videos/curio-s56` 通過。

計時器在 250 字元／分鐘估計開場 **59.57 秒**、正文 **12:49.07**；在更快的 325 下開場 **48.50 秒**、正文 **10:24.30**，皆符合開場 30–60 秒及正文至少 8 分鐘的文字規劃。開場逐字未改，59.57 秒上界仍很緊；這些不是 R6 實測 TTS。R4 音訊與 33 個尚未清除的旗標仍只屬舊稿 [收據](../verify-4.md)。

請由**未撰稿者**在上述五檔精確雜湊重新核對修處來源、主張表與書面畫面；通過後才由兩位**無前情**讀者各自完成正式 13 題盲評，再按 OR 規則合併。作者不自給來源 PASS 或盲評票；新稿未進行 TTS、插圖或成片。
