# 查核報告 3（sothatswhy-p01-wireless-energy）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿，也沒有寫 verify-1.md、verify-2.md）
- 日期：2026-11-14
- 範圍：2026-11-14 在第四章 p125 之後新加的電動牙刷一段 p125a–p125k（場景 `brush-stand`、`chief-brush-why`、`brush-wet`、`brush-peg`、`chief-peg`，`claims.md` C30），連前面 p123–p125 與後面 p126–p128 讀；五個新鏡頭的圖像提示詞；全片小問字數占比。其餘台詞沒有重查，結論沿用 verify-2.md。
- 來源：`claims.md` 只當線索，不採用它的引文。今天在新的空目錄重新 curl GET，HTML 去掉 script／style 與標籤轉純文字後讀上下文：
  - Chris Woodford, Explain that Stuff〈Wireless chargers〉（200，66,095 bytes；頁首 "Last updated: April 28, 2023"）：開頭、Ordinary chargers、Induction chargers 全段與各圖說
- 結論統計（11 句）：**正確 10、需改 1、錯誤 0**。圖像提示詞 5 個：相符 5。另有 1 處選修。
- 字數：含標點計算，小問最長 15 字（p125a，剛好到上限）、所長最長 24 字（p125f），都在上限內。沒有拉丁字母、沒有阿拉伯數字。
- 小問占比（漢字，小問 ÷ 全部）：405 ÷ 2,231 = **18.2%**（163 句，所長 113、小問 50），≤ 20%。

## 一、需改的地方與理由

| 編號 | 嚴重度 | 行 | 現行台詞 | 問題 | 建議句 |
| --- | --- | --- | --- | --- | --- |
| F01 | 必改（因果會誤導小孩） | p125k（所長） | 所以牙刷站得穩穩的，不會像手機那樣滑開。 | 前句 p125j 講的是「兩圈線又近又正，鐵柱還把磁場集中送過去」，接「所以牙刷站得穩穩的」，八歲小孩會聽成「磁場把牙刷吸住、所以站得穩」。來源說站穩是鐵柱在物理上卡住牙刷：「It's not just to stop the toothbrush wobbling about」、圖說「The bottom of an electric toothbrush has a hole in it so it sits securely on the "peg" on the base」。磁場集中是讓能量傳得比較有效率（"so energy is passed more efficiently"），不是讓牙刷站穩。回呼手機滑開的用意可以留，只要把原因換成鐵柱 | 「鐵柱也卡住牙刷，不會像手機那樣滑開。」（18 字） |

## 二、逐句核對

| 行 | 現行台詞 | 結論 | 依據摘要與前後文 |
| --- | --- | --- | --- |
| p125a（小問） | 我的電動牙刷，也是放上去就充！ | 正確（小孩的聯想） | 前句 p124–p125 講車票卡要多近、要看線圈；小孩從「放上去」聯想到牙刷，「也是」回指前面的手機充電板（p053）。15 字到上限 |
| p125b（所長） | 對，同一招。底座裡有一圈線，牙刷底部也有一圈。 | 正確 | "it's the power behind everything from rechargeable toothbrushes and phone charging mats"；"The primary coil is in the charger base … The secondary coil is in the base of the toothbrush"；"A Powermat uses exactly the same principle as an electric toothbrush charger"。「一圈線」沿用 p026、p053 的說法 |
| p125c（小問） | 為什麼牙刷要這樣充？ | 正確（提問） | — |
| p125d（所長） | 一個科普網站說，最主要是為了安全。 | 正確 | "Safety is the main reason for using an induction charger in the bathroom"。標明是科普網站的說法，沒有誇大來源的分量 |
| p125e（所長） | 浴室很濕，牙刷常常是濕的。 | 正確 | "the base of your toothbrush, which typically gets wet"；「浴室很濕」是常識 |
| p125f（所長） | 這樣充電，牙刷底下沒有插頭，也沒有露出來的電線。 | 正確 | "you don't need a power cable or exposed leads coming out of the base of your toothbrush"。沒有說防水 |
| p125g（所長） | 電動刮鬍刀常用這種充電，也是同一個原因。 | 正確 | "Electric shavers often use induction chargers for the same reason."「常用」＝often |
| p125h（所長） | 而且充電的底座上，有一根包著塑膠的小鐵柱。 | 正確（選修 S1） | "it has an iron peg on top of it covered in plastic"。來源描述的是那一型牙刷；片中說「充電的底座上」，沒有說每一款都有，但聽起來是通則，見 S1 |
| p125i（所長） | 牙刷一放上去，那圈線就剛好圍著鐵柱。 | 正確 | 圖說 "It's fitted at the very base of the brush and sits around the little iron peg on the charger stand"；"The copper coil … running around the hole" |
| p125j（所長） | 兩圈線又近又正，鐵柱還把磁場集中送過去。 | 正確（前半撰稿推論、後半原文） | "the core concentrates the magnetism (magnetic "flux") from the primary coil into the secondary coil"；「又近又正」是兩圈線套在同一根柱子上的合理推論，也回呼 p117–p121 的「對正」「離得近」 |
| p125k（所長） | 所以牙刷站得穩穩的，不會像手機那樣滑開。 | **需改（F01）** | 見上。後句 p126 小問「鍋子也要放正中間嗎？」：原本接在 p125 之後要回跳到 p119 的「正中間」；現在 p125k 提到手機滑開（p112–p119），反而讓 p126 的「也要放正中間」更順，銜接改善 |

## 三、圖像提示詞

| 場景 | 台詞 | 結論 | 說明 |
| --- | --- | --- | --- |
| `brush-stand` | p125a–p125b | 相符 | 白色電動牙刷立在圓形充電座上、底座一點綠光＝在充電 |
| `chief-brush-why` | p125c–p125e | 相符 | 所長拿著牙刷微笑解釋 |
| `brush-wet` | p125f–p125g | 相符 | 濕的檯面、牙刷和底座上有水珠、底座是無縫塑膠殼＝浴室濕、沒有露出的電線 |
| `brush-peg` | p125h–p125i | 相符 | 剖面：底座銅線圈繞著中間一根短柱，牙刷底部第二圈線圍著同一根柱子＝來源的 Artwork 與圖說；示意（claims C30 已註明） |
| `chief-peg` | p125j–p125k | 相符 | 所長把牙刷放回底座；F01 改句後（鐵柱卡住牙刷）也相符 |

## 四、選修建議（不影響結論）

| 編號 | 行 | 建議 |
| --- | --- | --- |
| S1 | p125h | 照 `claims.md` C30 注意 4「不說每一款電動牙刷都有鐵柱」，把通則語氣放軟：「而且很多牙刷底座上，有一根包著塑膠的小鐵柱。」（22 字） |

## 五、結論

**修正後通過。** 十一句的事實都出自 Explain that Stuff 原文，「最主要」「常用」照來源分寸；前接車票卡距離、後接鍋子放中間都順；小問占比 18.2%；圖文相符。必改 1 項：F01 p125k 的「所以」會讓小孩以為是磁場讓牙刷站穩，換成「鐵柱也卡住牙刷」。S1 選修。
