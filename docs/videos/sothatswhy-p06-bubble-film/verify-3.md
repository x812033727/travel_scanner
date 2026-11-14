# 查核報告 3（sothatswhy-p06-bubble-film）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿，也沒有寫 verify-1.md）
- 日期：2026-11-14
- 範圍：2026-11-14 在第一章 p042「科學家叫它表面張力。」之後新加的一段 p187–p191（場景 `soap-drop`、`straw-water`、`bubble-jar`，`claims.md` C26），連前面 p039–p042 與後面 p043–p045 讀；三個新鏡頭的圖像提示詞；全片小問字數占比。其餘台詞沒有重查，結論沿用 verify-1.md。
- 來源：`claims.md` 只當線索，不採用它的引文。今天在新的空目錄重新 curl GET（都 200），HTML 去標籤轉純文字後讀全文：
  - Exploratorium（Ron Hipschman）〈Soap Bubbles: Soap〉annex.exploratorium.edu/ronh/bubbles/soap.html（200，4,798 bytes）：全文四段
  - Exploratorium（Ron Hipschman）〈Soap Bubbles: Bubble Formulae〉…/formulae.html（200，5,037 bytes）：全文
  - 兩頁都已在 `video.json` 的 `sources` 裡。
- 結論統計（5 句）：**正確 5、需改 0、錯誤 0**。圖像提示詞 3 個：相符 3。另有 1 處選修、1 處 `claims.md` 整理建議、1 項提醒。
- 字數：含標點計算，小問 p187 10 字；所長最長 25 字（p188，剛好到上限）。沒有拉丁字母、沒有阿拉伯數字。
- 小問占比（漢字，小問 ÷ 全部）：397 ÷ 2,089 = **19.0%**（169 句，所長 109、小問 60），≤ 20%，但離上限只剩 1 個百分點，之後再加小問台詞要先量。

## 一、需改的地方與理由

無。

## 二、逐句核對

| 行 | 現行台詞 | 結論 | 依據摘要與前後文 |
| --- | --- | --- | --- |
| p187（小問） | 肥皂是讓皮拉更緊嗎？ | 正確（說出常見的錯誤直覺） | Soap 頁："There is a common misconception that water does not have the necessary surface tension to maintain a bubble and that soap increases it"。前句 p041–p042 剛把「往內拉、想縮小的力氣」叫做表面張力，p025 說泡泡水是水加一點肥皂；「皮」沿用 p021 起的說法，問得自然 |
| p188（所長） | 剛好相反：肥皂讓表面張力，只剩清水的三分之一左右。 | 正確 | "but in fact soap decreases the pull of surface tension - typically to about a third that of plain water."「左右」對應 typically／about。25 字到上限 |
| p189（所長） | 清水拉得太用力，又乾得快，一下就破。 | 正確（簡化） | "The surface tension in plain water is just too strong for bubbles to last for any length of time. One other problem with pure water bubbles is evaporation: the surface quickly becomes thin, causing them to pop."「乾得快」＝evaporation、變薄而破，給小孩的說法可接受。也解掉 p188 留下的疑問：張力變小為什麼反而吹得出泡泡 |
| p190（所長） | 肥皂有點像一層蓋子，讓皮裡的水慢一點乾掉。 | 正確（比喻，分寸對） | "Because the greasy end of the soap molecule sticks out from the surface of the bubble, the soap film is somewhat protected from evaporation (grease doesn't evaporate) which prolongs the life of the bubble substantially."「有點像」「慢一點」＝somewhat protected，沒有說不會乾；「蓋子」跟 p026「肥皂夾在兩面」的三明治一致 |
| p191（所長） | 有人把泡泡封進罐子，不讓它乾，撐了三個月！ | 正確 | Soap 頁："I've blown soap bubbles on a watchglass glued to the bottom of a jar with a large mouth. Once I've sealed the jar … My longest lasting bubble survived for three months!"；Formulae 頁："You must have a good seal or the liquid will escape slowly and the bubble will pop from evaporation." "My longest lasting bubble survived for 3 months!" 「有人」＝作者本人；三個月是他最久的一次，「撐了三個月」沒有說每次都這樣。他用的是加大量甘油的長壽配方，片中沒提，見 S1。Plasterer 的 341／342 天兩頁不一致，片中沒用，對。後句 p043 小問「那它為什麼要縮成圓的？」：「它」回到泡泡、「縮」回到 p041 想縮小的力氣，隔了五句仍聽得懂，可接受 |

## 三、圖像提示詞

| 場景 | 台詞 | 結論 | 說明 |
| --- | --- | --- | --- |
| `soap-drop` | p187–p188 | 相符 | 一碗清水滴進一滴洗碗精＝肥皂加進清水；示意 |
| `straw-water` | p189–p190 | 相符 | 吸管尖一顆清水小泡泡破掉＝清水一下就破。p190 的「蓋子」也蓋在這張圖上，圖沒有畫肥皂膜，但不衝突 |
| `bubble-jar` | p191 | 相符 | 大玻璃罐裡小玻璃碟上一顆泡泡、蓋子蓋緊＝來源的 watchglass 加密封罐 |

## 四、選修建議（不影響結論）

| 編號 | 行 | 建議 |
| --- | --- | --- |
| S1 | p191 | 小孩可能回家照做卻撐不到三個月（作者用了甘油很多的配方、還用實驗室封膜）。不危險，片中也說「有人」，可不改；若要更準，可寫「有人用特別的泡泡水封進罐子，撐了三個月！」（22 字） |

## 五、`claims.md` 整理建議與提醒

| 編號 | 內容 |
| --- | --- |
| N01 | `claims.md`「不講、找不到來源的」一節仍寫「肥皂其實把表面張力降到約三分之一（Exploratorium soap 頁）：有來源，但會讓『表面張力』變成兩件事，第一版不講」，現在 C26 已經講了，這一條應刪掉或改成「2026-11-14 起在 p187–p191 講，見 C26」 |
| N02 | `i18n/` 的八個語系檔都還沒有 p187–p191（grep 不到），C26 自己也寫「新五句要補翻譯」。不是查核範圍，但出外語版前要補 |

## 六、結論

**通過。** 五句都出自 Exploratorium 原文，「三分之一左右」「有點像」「慢一點」照來源分寸；前接表面張力、後接「為什麼縮成圓的」都接得上；三張圖與台詞相符；小問占比 19.0%（接近上限）。沒有必改；S1、N01 選修，N02 是出外語版前的提醒。
