# C16 Bialetti｜作者劇本與逐鏡預檢收據

日期：2026-10-23（台北時間）。此收據由作者 `codex-c16-script` 撰寫；**獨立來源／逐鏡 PASS 的依據是另一位審查者的收據，不是作者自簽**。兩位盲讀、站主劇本核准、付費及成片驗收仍未完成。

## 已採用企劃綁定

| 檔案／狀態 | SHA-256 |
| --- | --- |
| 已採用 `treatment.md` | `1B82057CE1CA064C84829F64F2D5B4679CC2E9CCA74F14F24964650636282EEE` |
| 已核 `source-matrix.md` | `3705477A06ED4395C44D57882951349B0D8D16DAF8D946DC86CECEC9ADF1D713` |
| 站主採用 Treatment 收據 | `37F28906D4B29CD9DAF133E73BAFB9C321CFC4D3AD0DE1DED5CCC5F27CC07DE0` |
| 分支起點／Treatment PR #1698 head | `e32a2b5f05b38e4fe25ba7db5738e5b2e48aa2f4` |

## 作者稿雜湊

| 檔案 | SHA-256 |
| --- | --- |
| `script.md` | `1F92C7016D71488D4553E9D3AF246A41B2CC8435CC1A19468BED0106212CE22F` |
| `visual-plan.json` | `47B7720D7F4408927CDFCF7B3FA42E8A35E6F06AE30EE2284A1E5D9AE170E664` |
| `visual-plan.md` | `F625C5EF9873D7D5D72CF4ED4DF6B174040B0D24A8A22953A45686F0FC770C1B` |
| `script-source-notes.md` | `A650E4B7A4A7BA0FBCE2C279242C7B447DC5ED6C656168C98045EE96E7978C0A` |

## 作者預檢

- 85 個唯一句 ID 和 85 鏡 JSON／閱讀版分鏡按順序一對一；74 張候選原創插圖與 11 張後製字卡，最長連卡 1 張。
- 逐句表每個事實句都有 M01–M18 矩陣 ID 或明確標作留言／訂閱邀請；圖片 `shot.prompt` 沒有品牌、產品、畫家或歷史人物的姓名。看過 `look` 僅含 `preset: cute-mystery`，模型記為 MiniMax `image-01`。
- 濃縮開場紙上約 54 秒；第 2–6 章共 2,216 個中文字元及標點，以每分鐘 250 字元粗估約 532 秒。**沒有 TTS 音檔，也未實測正文達 480 秒**；鏡數 74/85 不能代替插圖時間占比。
- 沒有把洗衣傳說當史實，沒有宣稱一九三三年有已讀原始專利，沒有指稱小鬍子角色像父親或兒子，沒有裁定 M17 的發明人／權屬／訴訟，沒有報家庭比例、總銷量或固定壺內壓力。
- `npm run check:tasks` 在此腳本 worktree exit 0，驗 2,080 票；有既存逾期／重疊警告，沒有本任務錯誤。逐句與配鏡來源未由作者自行判 PASS。

## 七鏡視覺窄修（2026-10-23）

[獨立逐句來源與配鏡首輪收據](independent-script-source-visual-review.md)將 **85/85 旁白來源判 PASS，但總體 HOLD**：`c160106`、`c160508`、`c160510`、`c160511` 把 1957 年《Fiera di Milano》雜誌印刷頁誤導成展場直立海報；`c160602`、`c160604`、`c160605` 把不同館的物件紀錄誤導成當前或同場展櫃。作者只改這七列的 `visual-plan.md` 與對應 JSON 的 `camera`／`prompt`，其餘 78 鏡及 85 句旁白、來源註記原始 bytes 不變。新版改為素面雜誌頁和彼此分隔的館藏資料夾／目錄卡；原廣告與真實藏品仍不重畫。

機械差異比對以首輪收據的 PR blob 為基準，確認 JSON 與 Markdown 恰好同改七個 ID；當時視覺 Markdown SHA-256 `8BFECB74AA53597E9ABF099B497E3F124C056F3AA617BD356DE149005A9B935A`、JSON `573D4A485E4611B475558C83D0A3CC0BE5A20D672E37F700919BCEFD128DE91B`。同一審查者對這七鏡差異判 PASS，但順看發現相鄰的 `c160607` 仍有一處海報誤指；見下一段。作者沒有把七鏡 PASS 冒稱當時整套 PASS。

## 相鄰鏡 c160607 窄修（2026-10-23）

原審查者[七鏡差異覆核](independent-script-source-visual-review.md)判七鏡 PASS，但順看相鄰鏡找到 `c160607` 仍以空白海報指涉 1957 年雜誌印刷廣告，因此當時整套維持 **85/85 旁白來源 PASS、84/85 配鏡 PASS、1 鏡 HOLD**。作者在該覆核提交 `e70f5fa3f072fce2d5ae773653113ade8f11eb5d` 之後，只把 `c160607` 的第三份時間線物件改為一頁完全無字的素面雜誌紙，同步 Markdown 與 JSON；原廣告仍未重畫。對 `e70f5fa3f` 兩份原始 blob 作機械差異比對，恰好只改這一個 ID。劇本、來源註記、其餘 84 鏡的 bytes 與 SHA-256 不變；新版視覺 SHA-256 見上表。同一審查者對作者修訂 head `3d569b59133241f764263897c36fc1a0084db557` 的四份 Git blob 與相鄰鏡頭完成最終差異覆核，`c160607` 判 PASS。

## 獨立裁決與後續關卡

[同一位非作者審查者的最終收據](independent-script-source-visual-review.md)對上表四份精確 blob 判定 **逐句來源 85/85 PASS、配鏡文字 85/85 PASS**；M16 人物身分與 M17 發明／權屬／訴訟仍未定論。作者若改任何劇本或分鏡輸入，須記新雜湊並重核變更範圍。仍須由兩位新鮮讀者只拿旁白正文盲讀因果與節奏，再交站主審劇本與逐鏡；整支張數、嘗試次數與費用另待站主核准。此裁決沒有授權媒體生成、匯入、上傳或發布。
