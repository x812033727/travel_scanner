# X05 Meta｜v14 三鏡失敗後的離線提示詞提案

**此為 v14 試圖後的原始離線提案；三項候選詞後來寫入 v15，現況見 [v15 作者差異收據](visual-prompt-v15-author.md)。** 當時現稿 SHA-256 為 `b1abe20a31daaae50ba580c386cb4038689cc594b5320a97b0bf69f49de3f054`。三張試驗圖及缺陷見 `image-pilot-v14.md`。以下按「完整成人執行一個動作」或「兩組易辨物件」縮減視覺元素；保留旁白、來源數字、鏡頭 ID、卡片揭曉時點及每鏡最多三次的生成界線。

| 鏡頭與旁白功能 | 候選 MiniMax `data.prompt`（英文原文，尚未使用） | 要由下輪驗證的畫面關卡 |
| --- | --- | --- |
| `x05-b01-s04`／`m050104`：11 月裁員消息已發布，年底總人數仍未揭曉。 | `Medium view in a quiet office corridor. One complete adult office worker, with head, neck, torso, both arms and legs visible, walks past several unused chairs while carrying one plain sealed envelope. A small jar with an opaque dark cover rests on a side table; nothing inside the jar is visible. Bare walls and solid-coloured objects.` | 信封必須封口、成人不可從信封或罐中長出；成人軀幹與四肢相連；罐中數量不可見；無招牌、紙字或可讀標記。 |
| `x05-b03-s03`／`m050303`：廣告送達更多，降價後廣告收入反少。 | `Overhead view of a bare wooden table with only two widely separated groups of plain objects. The left group has a modest pile of smooth ivory ad tiles beside a larger pile of plain copper coins. The right group has a clearly larger pile of the same ivory ad tiles beside a smaller pile of the same plain copper coins. No people, containers, sheets, labels, symbols or writing.` | 右側象牙色廣告片較多、銅幣較少；兩種物件各自只用一種顏色，不再出現紅珠或不明容器；左右比較在 16:9 小畫面仍清楚，無字。 |
| `x05-b06-s13`／`m050614`：兩部門合計的正數已由旁白揭曉，但畫面不搶先印精確值。 | `Medium view of one complete adult office worker standing behind a bare worktable. The worker, with an attached head, neck, torso and both arms visible, lifts the lid of a plain pale-green compartment to reveal a short stack of smooth pale-green blocks. A taller sage-green stack stands on one side of the compartment and a shorter terracotta weight stands on the other side. Plain background and solid-coloured objects.` | 同一名成人只做掀蓋動作，頭頸軀幹和雙手連接；綠色高堆、陶紅短砝碼、盒內正數堆三者位置易分；無紙張、對話框、偽字或精確數字。 |

這些候選詞避免 `report/chart/page/notice/scale` 一類容易讓模型畫出虛構字的道具，並將先前生成出的「信封裡的人頭」和「盒上浮頭」改為完整站立成人；`x05-b03-s03` 刪去原本重疊的托盤、價杯、收入盆三套容器。**這仍是待驗證假設**：全局可愛畫風可能再次自行加入角色、偽字或多餘物件，不能把提示詞修訂視為畫面合格。

如採納任一候選詞，先只改對應三個 `data.prompt`，重新凍結整份 `video.json` 的 SHA-256，完成獨立來源差異與兩位全新盲讀，並保持 `STOP`。審查通過後才可對必要鏡頭各做一次小批實測及人工看圖；不能直接跑餘下鏡頭或把 v14 三張失敗圖放進預覽。每次呼叫前再核美元帳本、月度額度和使用者 **US$25 含 Shorts／重試／稅費硬上限**。
