# H10 日文翻譯獨立審稿（第 1 輪）

日期：2026-10-16（Asia/Taipei）。審核對象為 `C:/Users/x8120/mokaair-work/videos/curio-h10/i18n/ja.todo.json`，SHA-256 `2B30CC825DE24375AC5FE4D47734BC7B74EF96B1B724EC92DDA78CB96AB95C53`；對照繁中 `video.json` SHA-256 `A43541019B57D0EF624A6AF2573C728CC5009894121EE9DE6E8BBF5623EC8C57`。審稿員未修改工作表、來源或媒體。

**結論：HOLD，2 處必修。** 一句日文字幕會把動詞切斷；說明欄首句應區分發現沉船和確認船員身分。修後重新計算工作表雜湊並複核，才可合併日文翻譯；配音時槽和發音仍待實測。

| 欄位或 ID | 問題 | 現文 | 建議的最小修法 |
| --- | --- | --- | --- |
| `h2a5e43b` | 本機 `cuePieces` 把 `亡くなる` 切成 `亡く`／`なる`；兩張字幕之間切開同一個動詞。 | `身元は分かっても、船を離れてから亡くなるまでの経緯はまだ分かりません。` | `身元は判明しましたが、船を離れてから亡くなるまでの経緯はまだ不明です。`（35／48 字；`cuePieces` 在逗號後自然切開）。保留棄船至死亡的整段經歷仍未明。 |
| `description` 首句 | `乗組員の発見` 把本集的「人員身分確認」寫得像搜到人員本身；影片與後文分開說明沉船發現、2024 年菲茨詹姆斯及 2026 年四名船員的身分鑑定。 | `…どのようにエレバス号とテラー号、そして乗組員の発見につながったのでしょうか。` | 改為 `…どのようにエレバス号とテラー号の発見、そして乗組員の身元確認につながったのでしょうか。`。保留後文 2024、2026 年的敘述。 |

## 複核範圍

- `parts = metadata,captions`；82／82 句 ID、場景、繁中來源文字與順序對應 `video.json`，7／7 章名及標題、說明、標籤的來源欄也一致。所有譯文都有值，82／82 句均低於 `max_chars`；7 句超過約 40 字的建議值，但未超硬上限，最長 `h1020a89` 49／54 字。這不證明合成語音能放進時槽。
- 本機以 `cuePieces` 複查全 82 句及帶原文 `boundaries` 的 20 句，除 `h2a5e43b` 外，未見切斷日文詞語或倒置數字／因果。`h28b2255` 的 Greenhithe 是 1845 年出航地，不是 Greenwich；日文 `グリーンヒス` 可對應此地名，本輪不要求改字，實際讀音留待配音 QA。
- 出發時 134 人與補給船離開後 129 人分清楚；1847 年 5 月 28 日紙條、1848 年 4 月 22 日棄船及 4 月 25 日補記的「明日＝26 日」沒有改成已證實的出發日期。1854 年 Rae、1869 年 Inukpujijuk 標圖與翻譯者的角色分開；2014 年岸上鐵件與 Erebus、2016 年 Sammy Kogvik 的見聞與 Terror、9 月 18 日確認也分開。2024 年 Fitzjames 與 2026 年 5 月新增四人、累計六人的身分研究沒有被說成補齊了全員最後行程。
- 標題 25 字、7 個章名各 10 字以內、標籤譯文合計 36 字；標題與標籤未擅加頻道名。縮圖三欄均有譯文，保留 `\n` 與 `**`。說明欄保留 2026-10-16 查核日與 AI 插畫的非證據重建揭露。

史實交叉參照 [Parks Canada 遠征歷史](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/histoire-history/expedition)、[因紐特知識](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/inuit/qaujimajatuqangit)、[Terror 發現紀錄](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/archeologie-archeology/decouvertes-discoveries/terror)及 [Waterloo 2026 年身分研究公告](https://uwaterloo.ca/news/media/dna-matches-identify-four-more-sailors-franklin-expedition)。本輪是翻譯審稿，不代替前述來源的劇本史料查核、後續配音試聽或站主上傳決定。
