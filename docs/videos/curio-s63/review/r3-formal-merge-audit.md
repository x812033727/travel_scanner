# S63 R3｜正式雙人盲讀合併審核

2026-10-22 UTC。**HOLD：13 題敘事關卡 11／13，兩項必答題共同否決。**此紀錄先於任何 R4 作者修稿產生；兩位讀者的原始答卷、各自的官方 CLI 結果及來源封存檔均保持原樣。

## 綁定與重播

R3 凍結 `video.json` SHA-256 `00cb544ad03d325f8eb666c3d037bf8a0aa3df1026c5c528ae54749a7d8e5090`；`script.md` SHA-256 `557427e904b22b40e8f326f9acd7947950c507c089ee6cee5dd4ea5be68dc37d`。兩份獨立盲讀綁同一官方腳本內容雜湊 `4b8e3ccff19e369d5d4117c0054d0567cc0ddb9cb625ac0da4390e64e70e9a4f`、題目規則雜湊 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75` 和官方旁白稿雜湊 `1dadc85e9a86fd59c538b5df1c8e8e9ec93797bc4e865288dca5dd0230f6623b`。兩位的 13／13 句證據均逐一匹配官方定時旁白行。

[讀者 A 原票](r3-isolated-blind-a.raw.json) SHA-256 `9a52d55e9a3ecb785643a0d0760675019b945768a9d815bca7f17ca865251952`，11／13；[讀者 B 原票](r3-isolated-blind-b.raw.json) SHA-256 `3e70afaf249330cdaf2549807466cdf036409868adf166ec0864b59aee1dd08f`，10／13。兩份各自的 [A 綁定回條](r3-isolated-blind-a.bound.json)、[B 綁定回條](r3-isolated-blind-b.bound.json) 和官方 receipt 均隨本 PR 保存。

對兩份原票各執行 `panelVerdict`，再用程式碼中的 `mergePanelVerdicts` **逐題 OR**：任一讀者的引句「是」足以讓該題通過，只有兩人都答「否」才是合併否決。[正式合併紀錄](r3-formal-merged-narrative.json) SHA-256 `1cb1c1af506578ced251e429390de03452cb696ab3dde26f7e7a3ab252199272`，保留兩位個別答卷；[合併答卷](r3-formal-merged-answers.json) SHA-256 `ce507a0992784034ea6f602fc91165722006ae85465417913241cf8c7d92b34e`。用該答卷在全新隔離工作目錄重播官方 `node tools/video/cli.mjs narrative --slug curio-s63 --answers <合併答卷> --workdir <隔離目錄> --json`，exit **1**，失敗題目完全一致。[CLI 狀態](r3-formal-merged-cli-status.json)與[官方綁定回條](r3-formal-merged-cli-receipt.json)已保存；工作目錄裡的 `round=1` 只是該新目錄首次記錄，不是作者版次。

| 題目 | A | B | 正式合併 |
| --- | --- | --- | --- |
| `no_spoiler` | 否，`s63009` 已說爬出箱 | 否，同句 | **否** |
| `no_recap` | 否，`s63015` 重述十三歲被帶往工廠 | 否，`s63029` 重述房租／洗衣 | **否** |
| `no_detour` | 是 | 否，`s63016` 工廠數字像岔出故事 | 是；作者修稿可一併精簡 |

R3 的[獨立史料／書面畫面覆核](r3-source-visual-independent.md)仍是其所綁版本的 PASS，但敘事關卡 **HOLD**，不能進語音、插圖或其他付費媒體。後續作者 R4 修改會使 R3 盲讀綁定失效，須另取來源／畫面重審與兩位全新、只看 R4 劇本的盲讀；不可沿用這兩份原票宣稱通過。
