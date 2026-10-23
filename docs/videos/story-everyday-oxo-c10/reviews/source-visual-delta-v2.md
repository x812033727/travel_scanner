# C10 OXO｜修訂後來源與圖片提示詞獨立差異覆核

審查日：2026-10-22。審查者：codex-c10-delta-review，與劇本作者不同。**本次差異 PASS：80／80 句的來源判定與 80／80 鏡的文字提案均通過；仍待兩位只讀旁白的盲讀、實際配音時長、站主稿件與成本核准。** 這是對原審查 HOLD 的定點重新判定，沒有生成圖片、旁白或成片。

## 版本及覆核範圍

- 草稿 [PR #1689](https://github.com/x812033727/travel_scanner/pull/1689)，修訂提交 `4ebac4606079ba725f8a337c8a25e75d4aefbb52`。
- `script.md` SHA-256：`748FB2E160F14FF94A43599350455282E68B11EED71CE9CAFE8E425B1209D721`。
- `visual-plan.json` SHA-256：`C2F2D0BDA82E02312FF83155054E9E9AEEFFA9BBBD8EB439EB3DF2C676CE2E47`。
- `visual-plan.md` SHA-256：`73D188D0FE05229284F38456121FE40A6EE73BDCD2CCDE2169F2BD93C5CED00E`。
- 原[逐句與逐鏡審查](independent-script-source-review.md)綁定舊稿，只將它作為未改 ID 的逐項證據。Git 差異顯示 80 句旁白僅 `c100308` 改寫；視覺 JSON 修改該鏡、八個原 HOLD 圖片提示詞、`c100503` 展會提示詞及共通契約。重新比對當前稿：劇本和 JSON 各有 80 個不重複 ID，順序一致；71 `shot`、9 `stats`。

## 原 HOLD 的新判定

| ID／範圍 | 判定 | 直接來源與界線 |
| --- | --- | --- |
| `c100308` 旁白 | PASS | [2000 年《Los Angeles Times》對設計參與者的採訪](https://www.latimes.com/archives/la-xpm-2000-sep-14-cl-20664-story.html)記團隊製作大量泡棉模型，並用扭、轉、推、拉、擠等手腕／手部動作測試。新稿只說模型放在桌上、比較不同動作的控制；「不是外形漂不漂亮」是編輯性的設計對比，未聲稱某位受訪者試握。採訪是事後回憶，不當成當期測試日誌。 |
| `c100308` 圖片 | PASS | 畫面改為兩個無標誌概念泡棉模型與匿名設計師的鉛筆手，沒有受訪者試握場面。[Cooper Hewitt 館方圖錄](https://www.cooperhewitt.org/wp-content/uploads/2014/11/Beautiful_Users_Designing_for_People.pdf)也記設計團隊將多種材質原型攤桌探索；鉛筆圈形狀是明示的概念插圖，不是原始草圖重建。 |
| `c100102`、`104`、`105`、`206`、`214`、`310`、`511`、`514` 圖片 | PASS | 八條 `prompt` 已移除人物、品牌及館名，即使原句以否定方式出現也不再餵給圖片模型。保留匿名、無標誌、不可當作史實現場的界線。 |
| `c100503`、`visual_contract` | PASS | 額外移除展會與館名。對當前 JSON 71 條 `shot.prompt` 及共通契約，以 OXO／Good Grips／MoMA／Smart Design／Farber／Betsey／Sam／Moore／Gourmet Show 及中文對應名稱逐一掃描，命中零筆。`stats` 由後製排字，未納入圖片模型提示詞。 |

原審查其餘 79 句旁白與未改的視覺提案仍依舊版各 ID 判定及相同文字；本收據只補差異，合併後為 80／80 來源 PASS、80／80 視覺文字提案 PASS。`visual-plan.md` 已與 JSON 改動同向，但**未驗收實際生成畫面**。圖數 71／80 也不能證明插圖在正文秒數佔比達 70%。本集尚無實測配音 480 秒、盲讀、站主稿件核准或本機試片費用核准；不得進入付費製作。
