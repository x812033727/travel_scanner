# S58 R9｜正式雙盲敘事合併

2026-10-21 UTC。**R9 書面畫面獨立重查 PASS，敘事正式固定 OR 為 12／13 YES、必須項 `no_recap` NO；官方 CLI exit 1、`passed:false`，付費媒體仍 HOLD。** [R8 來源口播覆核](../r8-source-independent.md)已對同 SHA 劇本判史料 PASS；[R9 提示詞覆核](../r9-visual-independent.md)確認本版只修 `s58144` 畫面，沒有材料包裹與鳥程混畫。

[A 原票](raw-ballot-a.md)與[B 原票](raw-ballot-b.md)逐位元組複製自 `../r9-blind-a.md`、`../r9-blind-b.md`，SHA-256 分別為 `24f1d8da3305f6d977a33f7a2bf6936f791a666f9ba1e1b30e8458fefddf3c2e`、`1d765c9032bd9fa0186e65db5ae4958eb382fda679ac296601cf42a9f6e7be0a`。兩位都是 11 YES／2 NO：A 否 `no_recap`、`no_detour`，B 否 `one_line`、`no_recap`。固定 OR 對各題接受任一讀者帶場景 ID 的 YES，因此後兩項個別異議不使整體失敗；共同的 `no_recap` 仍阻擋。官方 `PANEL_RULES_SHA256=5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`。

[轉錄程式](build-merge.mjs)由完整原票製作兩份官方形狀答卷、[逐題稽核](merge-audit.json)與[合併答案](merged-answers.json)，不改變任何票。[正式 CLI 收據](cli-status.json)、原樣 stdout／stderr、退出碼及[官方紀錄](official-narrative-record.json)均封存；五份創作檔前後 SHA 與 [R9 作者凍結](../r9-author-freeze.md)一致，官方紀錄 SHA-256 `7cf414bed25343845ddcde9127c3b03edeb5596612bba702fda9991af737682e`。

## R10 修訂證據

- A：`s58061` 已說保住第二輛車，`s58062` 接著重說「第二輛車還在」。後句只須問追兵逼近後往哪裡藏。A 另認為片尾的十二小時鳥程偏離批量郵信問題；R10 可把問題接回同一封求助鴿信的進城路段，仍分清六天材料往返。
- B：`s58088` 已說當地負責人採用薄膜，`s58089` 接著又說「郵務改收透明薄膜」。後句只須交代舊紙法停止。B 另指出 `s58083` 在 11 月 21 日抵圖爾後跳回出城前的巴黎狀態；R10 應在圖爾當時的紙製流程裡向前敘述。`s58003`／`s58015` 重說出城郵袋目的也可同步刪掉後者重述。

R10 若改口播，必須重凍結五 SHA、再由非作者查來源與書面畫面、兩位新盲讀；本輪任何票不能套到改稿。
