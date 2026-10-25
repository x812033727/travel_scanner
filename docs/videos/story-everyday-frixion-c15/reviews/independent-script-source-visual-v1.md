# C15 FriXion｜87 句來源與一對一畫面獨立覆核

## 最新判定：v2 PASS（2026-10-23）

同一獨立審查者以[作者草稿 PR #1701](https://github.com/x812033727/travel_scanner/pull/1701) 新 head `665738706d90f7bddae20d1874cfb24dd878fe1d` 的實際 Git checkout bytes，重核前次 H1、V1 與整篇敘事連貫。**來源與預生成逐鏡文字覆核 PASS**；這不是兩位只看旁白的盲讀，也不代表站主稿件核准、實際配音 ≥480 秒、實際插畫畫面 ≥70%、付費媒體預算核准、成片驗收、上傳或發布。

| 新 head 的實際 PR checkout 檔案 | SHA-256 |
| --- | --- |
| [`script.md`](../script.md) | `81CB336C4E6B7FF09B3B54D14FAA90121607C4E89F81F1E3F2C7162D631672A4` |
| [`script-source-notes.md`](../script-source-notes.md) | `77F082979846CCA547E997EEAAC036AC9884B04B048B3CF87FD5D5E939A4BE99` |
| [`visual-plan.md`](../visual-plan.md) | `291F270CBD05E4DEC4727D8662E39D858B016D41AB6694639B63C3648965CC1C` |
| [`visual-plan.json`](../visual-plan.json) | `851B22774902D3E968B161E934CFE3533C4DB3B976A58C9A191EA99525DBF7FB` |

`git ls-files --eol` 四檔均為 `i/lf w/lf`；`Get-FileHash -Algorithm SHA256` 四值與作者新 head 的 Git blob 位元組一致。從前次審查 head `842c28156` 到新 head，內容差異僅涉及 `script.md` O13、來源備註的紙杯與溫域界線、`visual-plan.md`／`.json` 的 O07–O09 和 O13，另更新作者收據；無其他旁白或畫面提示詞變動。

| 前次 HOLD | 新版實際內容與重核 |
| --- | --- |
| **H1／O13** | 旁白改為「等到季節和氣溫變了，寫下的字還能保持同一個顏色嗎？」；配鏡改為窗外枯枝、作家查看抽象筆跡，**沒有**畫小幅升溫後立即變色。[PILOT Part 1](https://www.pilot.co.jp/media_english/005/)只記早期墨水升溫漸變與冷卻回復；[Part 2](https://www.pilot.co.jp/media_english/006/index.html)記舊 0–40°C 範圍對夏季超 40°C／寒地低於 0°C 不夠。新句是季節環境下的疑問，下一句 I01 接早期材料的不穩，E07–E11 再回答日常溫域難題；未把假設說成既有 FriXion 事故。**PASS**。 |
| **V1／O07–O09** | 三鏡均明寫 `unmarked paper cup`，畫面守則也明寫紙杯、無文字或不描摹原品花樣；與 [PILOT Part 1](https://www.pilot.co.jp/media_english/005/)所記 1976 Magic Cup 紙杯相符。**PASS**。 |

重新逐章讀完 87 句：Hook 的杯子／筆尖／無色／量產四個問題，依序由 Origin、Idea、Engine、Turn、Now 回收；新 O13 與 I01、E07–E11 前後一致，沒有把 1988 記憶型墨水或舊 0–40°C 門檻倒填成現行 FriXion 規格。重新機械對位：三表 87 個唯一 ID 同序，JSON 87 段旁白逐字等於 `script.md`，71 張 `shot` 的英文提示詞逐字等於 `visual-plan.md`；71 鏡均為 `MiniMax image-01`／`cute-mystery`，另有 16 張字卡。紙上估計全稿 **579.12 秒**、插畫句 **464.88 秒（80.27%）**，仍非實際配音與剪輯值。前次 V2 非阻斷提醒（T07 數字字卡避免被誤讀成實售總量）仍供成片驗收使用。

**任務看板狀態**：`npm run tasks -- done 2026-10-23-c15-frixion-script-source-visual-review` 寫出 `tasks/done/` 完成版後，回報 `tasks/open/` 原檔仍存在；未顯示明確的 `blocked by policy` 字樣。保留現場，沒有再嘗試刪除。因同 ID 同時存在，`npm run check:tasks` 目前 **exit 1**，明示 duplicate task ID；在執行 `done` 之前，該檢查為 exit 0（其他舊任務警告）。來源／配鏡 PASS 與這個看板檔案狀態分開判讀。

## 先前 v1 HOLD 記錄（已由 v2 差異重核解除）

**歷史判定：HOLD，H1 與 V1 已在上方 v2 解除。** 審查者 `/root/c15_frixion_independent_review`，不是劇本作者；審查日期 2026-10-23。基準為[草稿 PR #1701](https://github.com/x812033727/travel_scanner/pull/1701) 舊 head `842c28156a91b916454a42e241dde2e543f91079` 的全新 Git 工作樹；`165ee4b...` 到該 head 只修作者雜湊收據，劇本／視覺四檔內容未改。此審查不核准配音、圖片、成本、匯入、合併、上傳或發布。

## 內容雜湊與機械對位

| 實際 PR checkout 檔案 | SHA-256 |
| --- | --- |
| [`script.md`](../script.md) | `FAB7571AD64F338FD44C19AD2B60CB04FB70BC62A3D4BD8E70FF5E998B8AAF8E` |
| [`script-source-notes.md`](../script-source-notes.md) | `6102BBE94D970F2F2D344D4ADCECBC592C32A40C4805F1D26C319468C78F8B8E` |
| [`visual-plan.md`](../visual-plan.md) | `AB6EF77756ED8E6904AE22B7ACE8DB2D733338B7C4647658E319A2D19272F512` |
| [`visual-plan.json`](../visual-plan.json) | `6B33E813D57BAC2C1DAF0C29BBC2E6CAE9C784D80D23520D048C479271EB72DE` |

三表各有 **87 個不重複 ID**，次序相同；JSON 的 87 段旁白與 `script.md` 逐字相同。JSON 是 71 鏡 `shot`、16 張 `card`，最長連卡 2；`image_model` 為 `MiniMax image-01`，所有 `shot` 的 `look` 只含 `preset: cute-mystery`。圖片提示詞未含 PILOT、FriXion、ILLUSION、Magic Cup、可讀字或 logo 指令。以每分鐘 250 個中文字推算：全稿 579.4 秒，其中插畫句約 465.1 秒（80.3%）；這些都**不是實際配音或剪輯畫面時間**，不能當 480 秒與 70% 的正式通過證據。

## 獨立逐句來源結果

直接重開 [PILOT 開發故事 Part 1](https://www.pilot.co.jp/media_english/005/)、[Part 2](https://www.pilot.co.jp/media_english/006/index.html)、[現行消色 FAQ](https://www.pilot.co.jp/support/frixion/frixion_1.html)、[低溫回色 FAQ](https://www.pilot.co.jp/support/frixion/1334578774507.html) 和 [2017 年新聞稿](https://www.pilot.co.jp/press_release/2017/01/18/1010.html)；另核對 [US20060112851A1 專利公開頁](https://patents.google.com/patent/US20060112851A1/en)的 2004 優先權、2005 美國申請、2006 公開。專利只在來源備註中作背景，**沒有拿來補出未讀到的 1972 原件**。原廠 2024 回顧屬公司事後敘述；下列 PASS 只指旁白按原件範圍或明確歸屬敘述，不證明當年情景曾被獨立目擊。

| 全數核過的 ID | 直接可讀的依據與判定 |
| --- | --- |
| **H01–H08（8／8）** | 現行 FAQ 說橡膠摩擦熱使微膠囊的色變為無色；Part 1 記 1976 杯、2002 有色的 ILLUSION；Part 2 記透明化提問與量產門檻。H03 是假設語氣，沒有說橡膠真的把全部墨水刮走。**PASS**。 |
| **O01–O12（12／12）** | Part 1 的 `1970–1974`、`1975–1985` 段分別支持 1970 靈感、1972 申請／1975 取得、1976 加冷水變色的紙杯、1985 玩具。O02 與 O05 明示公司回顧。O09、O11、O12 是被這些用途支持的敘事推論。**PASS**。 |
| **O13（1／1）** | Part 1 記早期材料會隨升溫漸變、降溫回復；Part 2 記舊範圍 0–40°C、夏季超 40°C 或寒冷低於 0°C 可能不穩。原件沒有證實「房間**稍微**變暖」就足以令書寫自行改色。**HOLD：縮窄條件**，見 H1。 |
| **I01–I18（18／18）** | Part 1 的 `1986–1992`、`1993–2000`、`2001–2002` 段支持 1988 約 20°C 記憶型、微膠囊 10–15／5–10／2–3 μm、2002 ILLUSION 黑色變另一色仍可見。稿件把粒徑與筆尖 0.5／0.7 mm 分開；I05 沒把 20°C 當現行消色門檻。**PASS**。 |
| **E01–E15（15／15）** | Part 2 的 `2002–2006` 段支持歐洲行銷提議、法國舊墨水筆／另用修正工具的例子、舊 0–40°C 與後來 -20–65°C 研發溫域、2004 決定商品化後仍待量產。E04 把法國與全歐分開，E09 說清是 2024 回顧。**PASS**。 |
| **T01–T13（13／13）** | Part 2 的 `2006–2024` 段和 2017 新聞稿支持 2006 歐洲／2007 年 3 月日本、三日試賣**準備** 3000 支及接近原計畫三倍、初期 0.7 mm 與約半年後 0.5 mm。T07 明言沒有可直接換算的總銷量。**PASS**；T07 字卡仍應避免讓觀眾把兩個數字相乘，見 V2。 |
| **N01–N20（20／20）** | Part 2 記 2010 按壓式及筆尖乾燥難題；現行兩頁 FAQ 支持摩擦消色、高溫風險、約 -10°C 回色起點與 -20°C 可能較完整、摩擦或受損時不保證回復及不可寫證書／地址／答題卡。2017 稿寫約 65°C，現行 FAQ 寫 60°C；N07–N08 分別歸屬。N19–N20 是留言／訂閱收尾，不是史實主張。**PASS**。 |

## HOLD 與限縮修訂

| 編號 | 位置 | 問題、直接來源與可行修法 |
| --- | --- | --- |
| **H1** | `script.md` O13、配鏡 O13 | 「房間**稍微變暖**」把早期材料的溫度門檻說得比 [Part 1](https://www.pilot.co.jp/media_english/005/)及 [Part 2](https://www.pilot.co.jp/media_english/006/index.html)精確；兩頁只支持隨溫度改變與舊 0–40°C 範圍可能受夏天過熱／冬天過冷影響。改成有來源的季節條件，或刪去「稍微」且不暗示普通室溫小幅波動必然變色。配鏡的暖窗畫面跟著檢查。 |
| **V1** | `visual-plan.md`／`.json` O07–O09 | [Part 1](https://www.pilot.co.jp/media_english/005/)明說 1976 `Magic Cup` 是 **paper cup**。這三鏡進入具體 1976 段落，提示詞卻只有 `plain cup`，模型可能畫成陶瓷或玻璃杯，造成旁白未說出的錯誤材質印象。寫成無標誌紙杯，保留概念插畫；H04 的預告鏡可保持泛用杯。 |

**G1 已修復，非現行 HOLD**：前一版作者收據把 `visual-plan.json` 記作 `6D11E8F1…E8AF1`，原作者工作檔是 CRLF、47,216 bytes；Git 以 LF 收錄，從 PR head 新 checkout 的檔為 46,048 bytes、SHA-256 `6B33E813…71EB72DE`。`git ls-files --eol` 在原工作樹呈 `i/lf w/crlf`，新工作樹呈 `i/lf w/lf`。作者已在 `842c28156` **只修收據與 PR 說明**為提交後的 LF 雜湊，四個內容檔未改；本覆核以上表的 LF 位元組為準。

**V2 非阻斷提醒**：T07 字卡同時放「準備 3,000 支」與「銷售約為預計 3 倍」。旁白已說明不能直接算總量，卡片若維持並排，成片驗收時須確認觀眾不會讀成 9,000 支實售；拆成不同呈現或補「非總銷量」可減少誤解。[Part 2](https://www.pilot.co.jp/media_english/006/index.html)只給預備量和相對原計畫的倍數。

以上是作者修訂 O13 與 O07–O09 前的歷史 HOLD；新版雜湊和差異覆核結果見頂部 v2 PASS。此審查仍不是兩位只看旁白的敘事盲讀。站主劇本關卡需基於 v2 位元組；配音秒數、畫面時間、圖片品質及整片報價仍各自待實測／核准。
