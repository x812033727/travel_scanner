# S49 R45｜`moon044` 第二張原圖與裁圖獨立原尺寸驗收

2026-10-22 UTC。**第二張原圖 HUMAN REJECT；第二張裁圖畫面內容 HUMAN REJECT，裁圖滿框亦 FAIL；本景維持 TECHNICAL HOLD。**我不是 R45 提示詞作者，分別以原生 **1280×720** 查看兩張實檔。這是單景人眼驗收，不是整集 storyboard 或成片驗收；本審沒有付費呼叫、修改私人圖單、解除 STOP 或動用 `--accept-best`。

## 凍結文字與來源界線

- `video.json` SHA-256 `c1b1d2d8cbc160580d33f36b98a93e0cfbe8cdd4e0e0b65a591991404275d360`；`claims.md` SHA-256 `155e9ed04fe2fa83d7e13e79f12c94d44c45a357d7a822e9d068938c109a8753`。`moon044` 旁白問「連費用都有了；紙上的鏡片究竟鑄出來了嗎？」；R45 prompt 要一名想像中的 1830 年代**明顯中年成人**玻璃工匠，灰鬢、面紋、寬肩、樸素年代工衣，查看**空圓模**，柔和爐光，工場延伸至寬畫幅**四邊**。claims 同列明示「虛構報導的想像畫面，非真實月面或器材」。`look.preset=cute-mystery`，`format=drama`。[R45 非作者紙審](r45-moon044-full-frame-independent-paper.md) SHA-256 `4c31c32bb49517b575f4bb1fd6b6ba45d29bd5b67308b96d5a323f153ba54a81` 的 PAPER PASS 只適用書面候選，不能替原圖驗收。
- 固定 P05 的 Locke 名下 1859 重印本 [L435–489](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L435-L489) 在**虛構報導**內寫估價、鑄模和鑄鏡；[Jacoby 評論](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4125)不提供真實鑄鏡的獨立證據。兩圖都沒有宣稱是存世赫歇爾器材或實際工場，也沒有可讀文字、數字、標誌或可明確認出的現代機器；此來源界線沒有成為退件理由。

## 兩張原尺寸畫面

| 私人實檔 | SHA-256 | 人眼判斷 |
| --- | --- | --- |
| `/workspace/.video-work/curio-s49/keyframes/moon044-2.jpg` | `3060dc41cbe3cd7b8229c6f2cb283d858013eae8a6d213d8ce194380413e540d` | **HUMAN REJECT**。頂端 y=0–64、底端 y=658–719 是全寬黑色影像帶；R45 明示滿框後仍未填滿四邊。畫面內容也有下述成人、服裝及模具問題。 |
| `/workspace/.video-work/curio-s49/keyframes/moon044-2-trim.jpg` | `ba4c77931da5a6ac5999ead9067bbe1df5e67462bfd3dc2457018a5cb2a3d8a3` | **畫面內容 HUMAN REJECT**；上方 y=0–7、下方 y=716–719 仍有全寬近黑影像帶，滿框亦 FAIL。裁掉大部分黑邊沒有修復主體內容。 |

黑邊行數由原尺寸目視及只讀逐行像素核對：上述行中每行至少 99% 像素的三色通道值均低於 16／255。兩圖畫的是同一名灰髮人物把雙手擱在圓形物邊緣，工場有暖色柔光。人物灰髮與額上兩道皺紋是年齡線索，但巨大圓頭與眼睛、光滑童顏、短小手臂和小手，使其看起來像灰髮 Q 版孩童；**不能清楚讀作提示詞要求的中年成年工匠與寬肩成人體態**。交領、黃邊的青色袍服也不像可辨認的 1830 年代英國樸素玻璃工工衣；沒有上一張畫面清楚的工作圍裙。前景米色圓盤的中央近乎平坦，只有淺色輪廓，**無法清楚讀出空心的圓形鑄模**，容易看成實心板或淺盤。背景只是模糊的架子與方形物件，不能憑此認定為現代器材。卡通暖色調大致在 `cute-mystery` 範圍，沒有單獨構成退件理由；幼態人物與不明模具才是裁圖即使滿框也不應 KEEP 的內容問題。[R44 首張原尺寸獨立驗收](r44-moon044-first-native-independent-visual.md) SHA-256 `fac9f40b10266986fc946e8dfaccf120f21b93a6745fff6aece7ebf6c53e838e` 曾判首張裁圖的成人圍裙與空模**內容**可用；此結論不適用於這張新的第二圖。

## 機器狀態與停批

第二次失敗圖單封存 `/workspace/.video-work/curio-s49/review/r45-moon044-second-native/manifest-failed.json` SHA-256 `b3bb3d88332c61f2c655aee9d591700a3cda96f518e163d478f841d73e6e30dc` 記 `judge.overall=9.71`、`judge.passed=false`、`scores.frame=0`、`needs_review=true`，問題為上下 letterbox；暫選的只是上述裁圖。此機器結論與人眼所見黑邊一致，但其餘機器分數不推翻人眼對人物、年代工衣和模具的退件。現行 active manifest SHA-256 `3c9a5df3ef20c6be0a965179c1f6e14ebf56a5ad47774f21f46d043d60d64339` 仍是 **34 張 KEEP**，沒有 `moon044` 入選。

`drama` 格式在 `tools/video/media/keyframes.mjs` 的 `acceptBest()` 禁止 `--accept-best`；裁圖不能改寫失敗的 judge 或升格正式 KEEP。**重複黑邊且第二圖內容亦退件：維持 STOP、`moon044` TECHNICAL HOLD，不再購買媒體，也不接續 `moon045`。**
