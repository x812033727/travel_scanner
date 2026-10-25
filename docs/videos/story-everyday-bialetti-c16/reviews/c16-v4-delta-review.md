# C16 Bialetti｜c160601 條件句獨立差異覆核

日期：2026-10-23。審查者 `codex-c16-v4-delta-review`。對象為作者草稿 [PR #1704](https://github.com/x812033727/travel_scanner/pull/1704) 的精確 head `a2853124dce795df65d2a42b522084bb72144438`；對照舊 head `09e24dc11b9d0e3549a7c31f80d33db79d56ec82`。上一輪獨立 [PR #1733](https://github.com/x812033727/travel_scanner/pull/1733) 對舊 bytes 的 `c160601` HOLD 仍是歷史紀錄，本收據只裁決新 bytes。

## 輸入與差異

用 `git show a285312:<path>` 取得原始 Git blob bytes，Python `hashlib.sha256` 重算：

| `docs/videos/story-everyday-bialetti-c16/` 下的檔案 | bytes | SHA-256 | 對 09e24dc |
| --- | ---: | --- | --- |
| `script.md` | 13,914 | `726D18010F59F7C436D3906D37A8E55E9D24FE9040C6E617E6FEEE8E076876F2` | 只改 `c160601` |
| `script-source-notes.md` | 8,583 | `385331396DC5341B58B25E3471AA62051C6EBDA98D214DBEAA9A0130F2223F90` | 縮窄 c160601 界線及紙上字數 |
| `visual-plan.md` | 15,043 | `8C49EB8099583C261CDC30290F00AC61FD1DBFF219CA2F8175944760F5B41299` | bytes 未變 |
| `visual-plan.json` | 21,290 | `8BEAD3AD93C03B3A481D3B7D1CD2A091E0D763200206EC992A7274B58C1260AE` | bytes 未變 |

`git diff 09e24dc a285312` 共改 `script.md`、來源註記、作者收據和作者任務註記四檔；沒有改兩份配鏡。逐 ID 解析顯示只有 `c160601` 的旁白列改字，其餘 80 句不變。新 head 有 81 個唯一旁白 ID、81 個 Markdown 鏡頭 ID、81 個 JSON 鏡頭 ID，三者同序；Markdown／JSON 的 ID、kind、鏡頭與字卡文字逐欄 **81/81 相同**，72 `shot`、9 `stats`。

## `c160601` 判定：PASS

舊句直述「隔天早晨，爐邊的人又把同一只壺旋開」，可能被聽成某一戶的具體隔日紀錄。新句「**因為下回想煮一杯時，只要旋開壺身、重裝水與咖啡粉，這只壺就能重新上爐。**」以「下回想」為條件，說明器具再次使用的能力，沒有主張一位可辨認的人何時真的做過。它在 `c160519` 問「為何還願意讓壺留在爐邊」後立即給出可拆開、再裝料、再上爐的日常理由；`c160602–608` 再承接公司回顧、持續生產和功能總結，不重返廣告館藏話題。

2026-10-23 直接重開[國立 Museo Omero〈Moka〉原頁](https://museoomero.it/en/opere/moka/)；HTTP 200。館方描述兩半壺身以旋合開閉、下部水室、裝咖啡粉的漏斗濾器，以及加熱後水穿過粉層上升。這些支持「旋開、再裝水與咖啡粉、可重新上爐」的結構性概述；頁面沒有提供任何特定家庭隔日行為，而新旁白也未聲稱有。這是敘事概述，不是逐步沖煮指示；館方也明說壺身須旋合關閉。後續影像若描繪加熱，仍須保持壺身正確旋合。

同 ID 配鏡沿用「第二個**概念**清晨」、匿名人物、原創無標誌壺，水與粉在桌上等待裝入；它沒有畫特定歷史家庭，也沒有畫未旋緊的壺正在加熱。新旁白的條件語氣使這鏡可讀為功能示意。舊視覺 bytes 未改，故這輪對鏡 **PASS**。

依 [PR #1720](https://github.com/x812033727/travel_scanner/pull/1720) 對舊版未變 78 句／鏡的核讀、[PR #1733](https://github.com/x812033727/travel_scanner/pull/1733) 對 `c160212` 與 `c160417` 的 PASS，加上本輪 `c160601` PASS，**此精確四份 blob 的逐句來源與配鏡文字為 81/81 PASS**。M16 角色身分、M17 發明／權屬／訴訟仍不下定論。本裁決不代替兩位只看新旁白的全新盲讀、站主核稿、實際 TTS 時長、插圖時間占比或付費製作核准；沒有編輯作者檔案、生成媒體、合併、匯入、上傳或發布。

`npm run check:tasks` 在本次任務結案前 exit 0（2,082 檔，既有警告）。`npm run tasks -- done` 寫出 `tasks/done` 後留下本工作樹新建的、未追蹤 `tasks/open` 副本；前輪同型精確刪除已遭 `blocked by policy`，本輪沒有重試清理。提交只包含本收據及 `tasks/done`，不包含未追蹤副本；本機結案後的任務檢查不能代表提交樹。
