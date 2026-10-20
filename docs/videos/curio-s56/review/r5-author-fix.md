# S56 R5 作者修稿與獨立覆核交接

2026-10-20 UTC。這是**作者候選稿**，不構成獨立史料、畫面或盲讀 PASS。修稿依據是兩位無前情讀者的 [R4 正式合併](r4-clean-merge.md)：12／13，`no_recap` 共同否決；其餘個別疑點亦作小幅修正。

| 檔案 | R5 SHA-256 |
| --- | --- |
| `brief.md` | `404156118c92079b8dd36e89e28025e18582dd365ef36721b840da0390de27a0` |
| `research.md` | `59549e98e6ae258cedfc5b43e6684ecaa1102284d0dee13b0beef6443e4a6fb7` |
| `claims.md` | `5accac0eac72bb257e0da9e60895c3007fc345f6b4576b614c6a674ec5eecf16` |
| `video.json` | `01589b2c33986b92b4fa62504b186e023c2ea0425d82ed5a19a802ad35206cdc` |
| `script.md` | `8556a4a41665cc2c3b660710016669dcee2aa5bd94bf4f13d3868ddfb3194753` |

## R4 → R5 小幅修正

- 開場章名改為「福斯特停在南支河東岸」，不先說出背後新火的結果。第二章只留 `s56015` 一句「十月三十一日家書」定位，移除 `s56016–s56017` 的家人抄本與編者說明；版本譜系仍由 [研究](../research.md)和[說明欄](../video.json)交代。這回應 A 的 `no_spoiler`、`no_detour` 個別否票；家書日期及前夜火事見 [F161–171](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L161-L171)、[F204–256](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L204-L256)。
- `s56058` 一句回答教堂屋頂先起火，刪去同一景的 `s56059` 重述；保留下一句 `s56060` 消防員上屋頂的**新動作**。見 [F293–328](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L293-L328)。
- 刪去 `s56089–s56090` 整景對磚石街區與信心的提前複述，讓 `s56091–s56092` 從旅館前距離轉成「前面的商業區能擋住火嗎？」；下一章 `s56093–s56095` 才交代建築材料與福斯特原先的判斷，之後 `s56103` 給出失守結果。見 [F376–414](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L376-L414)。
- `s56152` 的問題改問洛許往北何處可停，`s56153` 立即答他退到草地旁已暫住之處；不再發問其他住戶的去向而改答洛許。見 [L578–590](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L578-L590)。
- `s56166` 一次交代星期二約一點半的大雨趕在草火前落下；`s56167` 只回收浸布穿越草地的備案沒有派上用場，避免同一句雨又說一次。Loesch 的晚年回憶見 [L578–613](https://github.com/GITenberg/Personal-Experiences-During-the-Chicago-Fire-1871_66433/blob/08931a6f2629fd4b8be37b1ec548857d48d17eb9/66433-0.txt#L578-L613)；不將雨誇成同一分鐘撲滅全城。

同步更新 `claims.md` 的逐句文字及刪除列，由 `video.json` 重新產生 `script.md`；`brief.md` 只更新失效的下一關狀態，`research.md` 原文未改。R4 原版五檔仍在私有 `/workspace/.video-work/curio-s56/review/r4-input-snapshot/`，保留 [R4 音訊收據](../verify-4.md)的歷史可追溯性。

## 作者機械檢查與下一關

`node tools/video/cli.mjs lint --slug curio-s56 --json` 回 **0 errors／0 warnings**：171 個唯一、遞增的逐句 ID，138 景（135 插圖景、3 字卡）、七章、17 個仍指向現存 ID 的 setup/payoff loops。`claims.md` 恰有 171 列，ID 與口說文字逐句相同；產生的 `script.md` 每句各收一次。工具估計開場 **00:59**、總旁白 **13.91 分鐘**，推估正文約 **12.93 分鐘**；這不是 R5 真實 TTS 時長。R4 的 [實測](../verify-4.md)正文約 13:03，但其 176 句音檔與 R5 的 171 句新稿不相符，且音檢尚有 33 旗標。

下一步由**未撰稿者**按上表五個雜湊重新核史料、主張列與書面畫面；之後再由兩位**無前情**讀者各自回答正式 13 題並按 OR 規則合併。作者不自給來源 PASS 或盲評票。敘事過關前不沿用 R4 的政策、核准或音訊放行，也不做新 TTS、插圖或成片。
