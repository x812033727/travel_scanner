# S02 現版獨立盲讀與來源抽核

查核日：2026-10-19。劇本 [`script.md`](script.md) SHA-256 `6b53fb1722aa3922f51e5bc79c54d21a99a7de34a1111227e7a3c1f47b89c664`；92 句、91 張插圖、七章、預估 8.1 分鐘，系列 lint **0 errors、0 warnings**。

未參與本集撰稿的讀者先只讀凍結劇本，獨立回答 `narrative` 十三題：**13／13 通過**。其答案暫存 `/tmp/curio-s02-frozen-blind-20261019.json`；將引文中的行號區間轉成工具接受的個別 `[s02001]` 格式後，`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s02 --answers /tmp/curio-s02-frozen-blind-gate-20261019.json` 正式記錄為通過。格式轉換未改讀者判斷。

讀者其後對照固定原文抽核：`s02013` 的「整齊軍隊」僅歸《三國志》〈吳主傳〉本傳；`s02029` 在明示回呼後才引用裴注《吳歷》的舟船器仗與曹操稱讚；`s02089`–`s02090` 是兩引書與小說比較後的有界推論，沒有重說孫權轉船場面。先前來源審查所列的視覺修正見 [`verify-1.md`](verify-1.md)。

唯一非旁白問題是 `video.json` 兩組懸念的回收 ID 偏移；已改為 `s02005`→`s02054`、`s02006`→`s02058`，劇本文字與上述雜湊完全未動。此通過紀錄只涵蓋前製文字與來源，不替代後續的旁白聽檢與插圖驗收。
