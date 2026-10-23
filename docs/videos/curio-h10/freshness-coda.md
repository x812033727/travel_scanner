# H10 2026 年身分研究後記：作者變更收據

日期：2026-10-16（Asia/Taipei）。此收據記錄修稿，**不是獨立事實查核或敘事盲評通過**。

- 前版 `video.json` SHA-256：`236E94B49168E52E57F6C063C9CD377FDF2086CC91FB0907932A3D13FC3389AC`；第 2 輪獨立查核 [verify-2.md](verify-2.md) 對它留下新鮮度 HOLD。
- 本版 `video.json` SHA-256：`4EF199C9FC35E0761004A64EF32434EEA483DFAF5B25AC4DB28D0C154C024680`；`script.md` SHA-256：`A4A64B02732D97C9DDB216B2CD42F789D95A0B0ADEB8AB3CE22B3C9CA679E596`。
- 已核准的 A 案 `brief.md` SHA-256 仍是 `AB081206F4055046C18B7A89016F05C9F885AA6BDD37EA3C2E2C661F2D74AA0D`，沒有改字。
- 新來源 [University of Waterloo 2026-05-06 原始公告](https://uwaterloo.ca/news/media/dna-matches-identify-four-more-sailors-franklin-expedition)：2026-10-16 直接開啟全文；公告明述再辨認四名遠征船員、累計六名。第 2 輪查核員同日用編輯用 User-Agent 取得 HTTP 200，記於 [verify-2.md](verify-2.md)。

## 精確修改

1. `dna-comparison` 的 `hf310a51` 仍回收 2024 年 Fitzjames 與紙條簽名的主線；台詞、畫面、loop 回收點都未改。
2. 在它之後新增 `later-identifications`／`h62e41a7` 與 `six-identifications`／`h14bd2a6`，各一句，先交代 2026 年五月又確認四人，再說累計六人。新畫面為不指涉真實研究者的卡通實驗桌與數字卡；沒有遺骸、死因或新航線示意。
3. 原 `identity-scope` 緊接後記，仍明說身分確認無法補出棄船以後的完整經歷。片尾仍回到紙條簽名，沒有把四人寫成紙條簽署者。
4. 新增 `H10-S10`／`H10-C17` 及兩句逐句映射，更新說明欄和來源列表；`loops.md` 只更新版號與後記位置，所有原問答 ID 未換。

## 本機檢查及待辦

- `node tools/video/cli.mjs script --slug curio-h10` 重新生成劇本；`lint --json` 為 0 errors、原有 2 個插畫提示詞 warnings。82 句，**估時** 9.829 分鐘；`script-timing.json` 為新稿的文字估算，不是音訊量測。
- 已核對 `video.json`、`script.md`、`line-claims.json` 的新句文字及來源一致；沒有啟動 TTS、產圖或任何付費呼叫。
- **下一關**：由新的獨立查核員對本版雜湊執行第 3 輪事實複查，至少直接核對新增兩句、卡片、說明欄與來源；由未讀過 H10 的獨立盲評者再答十三題。兩關都通過後才可送站主正式劇本審核，不能沿用前版通過。
