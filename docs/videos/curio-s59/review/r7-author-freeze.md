# S59 R7｜紙盤、轉速段落與回呼修訂凍結

2026-10-21 UTC。**作者凍結，待全新獨立史料／書面畫面覆核及兩位隔離敘事盲讀；付費媒體 HOLD。** [R6 正式合票](r6-merge-policy/summary.md)固定 OR 是 12／13，兩位都在 `no_recap` 投 NO（A 指 `s59098`，B 指 `s59062`）；A 另投 `no_detour` NO，B 的有據 YES 使該題形式上過關。[R6 獨立來源覆核](r6-source-independent.md)則找到 `s59017` 把槽畫在紙盤、`s59013` 路徑措詞含混，以及研究 P06 忽略針與薄片中間的彈簧／橡膠。R7 同時窄修這些具名位置。

| 凍結創作檔 | R7 SHA-256 |
| --- | --- |
| `research.md` | `39a48f08ca01dfa18009e9c1819684d03b92c52656952affd3266a574d88067d` |
| `brief.md` | `9d68d7b4dad27f56b6dbc53f7890bc0db84590de3e445302f8f4836c286ac1e3` |
| `claims.md` | `73711de13ce73791e409118b923eceb9d35425a84a63b6fc8b20ddba816e1c58` |
| `video.json` | `c78a0329f901d05450440ac7244345e5a375ebbacf361c187cec1036bfcc767e` |
| `script.md` | `d024ba3a7fed6c94b90320097de6289273278b65c7e1ebaef727b86ec861e57f` |

[結構化差分](r7-author-structured-diff.json) SHA-256 `5254d29999dc8fd54fe13a1f83e6e98fa4809c83369547c197cf6b80d7704467`。我將七個 R7 JSON 葉節點、新研究 P06、五個逐句表列逆換，`script.md` 的工具生成 `narrative`／`speech` 尾註亦依舊 JSON 重算，**五份 R6 原始位元組 SHA 全部精確復原**。R7 JSON 僅改 `s59013` 台詞／提示詞、`s59017` 提示詞、`s59059`、`s59062`、`s59064`、`s59098` 台詞；逐句表同改五行（`s59064`、`s59098` 的來源／畫面備註也相應更新）。`visualHash` R6 `3deadad1dfc94743` → R7 `3e39a4b9868072e1`；`narrativeHash` R6 `0b0423546b1b067e` → R7 `f20dc827b7998950`。

## 史料與敘事意圖

- [E5195–5206](https://github.com/GITenberg/Edison--His-Life-and-Inventions_820/blob/b100fab326616897d87d7e296672f5f916624d32/820.txt#L5195-L5206) 說**承盤刻槽、紙盤蓋在上面、電磁鐵壓針讓紙盤留下訊號凸痕**。`s59013` 口播現在明分承盤與紙盤，提示詞只示意壓針在紙盤留下點劃痕；`s59017` 去掉紙盤有槽的指令，改為紙盤有凸起點劃痕。兩景仍是愛迪生晚年回憶的概念插畫，並非巴黎實物。
- [D6872–6885](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L6872-L6885) 明載針由彈簧支承，橡膠墊傳遞薄片振動。研究 P06 補足這層中介，消去「針貼著薄片」的錯覺；R6 的 `s59040–41` 原已分兩句講明，未再改。
- [D6955–6976](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L6955-L6976) 先說回放反覆磨淺壓痕與音量／清晰度，再說搖速改變音高但仍可辨腔調，以及歌曲常走調、另一套鐘錶機構重播二重唱較好。`s59059` 現回答 `s59054` 的錫箔疑問並問「旁人重聽」；`s59062` 只給**腔調仍可辨**的新資訊，不再重述 `s59060–61` 的快尖／慢低；`s59064` 明說鐘錶機構是**另記**的比較，收回巴黎院士要查的手搖機。這個比較是器械重播可靠性的背景，**不聲稱巴黎當天用鐘錶機構或因速度導致杜蒙塞爾初試失敗**。
- [D6999–7013](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L6999-L7013) 的匿名來信盯著普斯卡斯的嘴，[D7035–7049](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L7035-L7049) 記杜蒙塞爾之後自行重試。`s59098` 現以「還記得會場那封腹語來信嗎？」**點名回呼**，說明換操作員為何直接檢驗那個疑慮，不再重講 `s59044／46` 的薄片與壓痕機制。`s59099` 才交代當事人說自己的重試結果。

`script` CLI 已重生 `script.md`，110 句、100 `shot`、10 `big`、12 組伏筆。`lint --json` 0 error／0 warning、工具估全片 13.40 分鐘；扣除開場九句與末兩句，正文 **2,633 漢字**，按每分鐘 325 字的最快估算 **8.10 分鐘**，實際仍待語音。`npm run test:docs-videos` 236／236、`npm run check:tasks` exit 0（其他長期認領票有既存警告）。這是作者預檢，不是新一輪的獨立 PASS。R7 的研究、逐句表、分鏡與劇本雜湊都不同於 R6 審核綁定者，故須重新獨立核源、審書面畫面、兩位隔離盲讀、正式合票；網站站主卡片及之後的音訊／原生插圖驗收亦另算。未達關卡前不作付費呼叫。
