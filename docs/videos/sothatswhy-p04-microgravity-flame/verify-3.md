# 查核報告 3（sothatswhy-p04-microgravity-flame）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿，也沒有寫 verify-1.md、verify-2.md）
- 日期：2026-11-14
- 範圍：2026-11-14 在 p108 之後新加的「太空站失火怎麼滅」一段 p109–p118（場景 `chief-putout`、`chief-worse`、`cargo-ship`、`cloth-flame`、`chief-earth-safe`，`claims.md` C26），連前一句 p108 與後面 p119–p121 讀；五個新鏡頭的圖像提示詞；全片小問字數占比。其餘台詞沒有重查，結論沿用 verify-2.md。
- 來源：`claims.md` 只當線索，不採用它的引文。今天在新的空目錄重新 curl GET，HTML 去掉 script／style 與標籤轉純文字後讀上下文：
  - NASA Space Station Research Integration Office〈Studying Combustion and Fire Safety〉（200，304,300 bytes；頁首 "Dec 26, 2023"）：開頭段、CIR／FLEX／FLEX-2／ACME 段、BASS 段、BASS-II、SoFIE-GEL、Saffire 段與圖說、Confined Combustion
- 結論統計（10 句）：**正確 9、需改 1（字數超限）、錯誤 0**。銜接 1 處建議改（改的是舊句 p121）。圖像提示詞 5 個：相符 5。另有 2 處選修。
- 字數：含標點計算（同 verify-2 的算法），小問 p109 12 字；所長 p110 **26 字，超過 25 字上限**；其餘所長最長 25 字（p112、p115）。沒有拉丁字母、沒有阿拉伯數字。
- 小問占比（漢字，小問 ÷ 全部）：394 ÷ 2,178 = **18.1%**（163 句，所長 109、小問 54），≤ 20%。

## 一、需改的地方與理由

| 編號 | 嚴重度 | 行 | 現行台詞 | 問題 | 建議句 |
| --- | --- | --- | --- | --- | --- |
| F01 | 必改（字數上限） | p110（所長） | 美國太空總署說，滅太空的火，要看火的樣子和燒的東西。 | 內容正確（BASS 段 "Putting out fires in space must consider flame geometry, characteristics of the materials, and methods used to extinguish it"），但含標點 26 字，超過所長 25 字上限 | 「美國太空總署說，太空滅火要看火的樣子和燒的東西。」（24 字） |
| F02 | 建議改（銜接） | p121（所長，舊句） | 太空站上有一組實驗，發現不一定。 | 新句 p118 剛說「有一組研究滅火藥劑的實驗，還發現了一件怪事」，隔兩句小問後 p121 又說「太空站上有一組實驗」，聽起來像另一組實驗；其實兩句指的都是 FLEX（來源："FLEX, which analyzed the effectiveness of fire suppressants, led to the discovery of a type of cool flame"；p122–p124 的液滴實驗就是 FLEX）。把 p121 改成回指，新段的鉤子才明確兌現 | 「剛剛那組實驗就發現：不一定。」（14 字） |

## 二、逐句核對

| 行 | 現行台詞 | 結論 | 依據摘要與前後文 |
| --- | --- | --- | --- |
| p109（小問） | 太空站失火了，要怎麼滅？ | 正確（提問） | 前句 p108「大多一分鐘左右火就滅了，可能是盒子裡氧氣快沒了」，從「火自己滅」轉到「人要怎麼滅」，接得上 |
| p110（所長） | 美國太空總署說，滅太空的火，要看火的樣子和燒的東西。 | **需改（F01，字數）** | BASS 段 "must consider flame geometry, characteristics of the materials, and methods used to extinguish it"。火的樣子＝flame geometry、燒的東西＝characteristics of the materials；methods 由 p111 接上 |
| p111（所長） | 在地上好用的滅火方法，到太空可能沒用， | 正確 | 同段 "because methods used on the ground could be ineffective"；「可能」＝could |
| p112（所長） | 甚至讓火更糟。所以比較大的火，他們不在太空站上燒。 | 正確（前半原文、後半撰稿推論；選修 S1） | "or even make the flame worse."；後半：Saffire 段只說在離站後的無人貨運船上做、因而能燒比較大的火；太空站上仍有 CIR 的小型燃燒實驗，所以限定「比較大的火」是對的。「所以」把理由接在「地上的方法可能沒用」上，來源給的理由是 p114 的不讓太空人冒險，見 S1 |
| p113（所長） | 等貨運太空船離開、上面沒有人了，才點火研究。 | 正確 | "conducted aboard uncrewed Cygnus cargo spacecraft after they depart the station"。貨運船靠站時太空人會進去搬貨，「上面沒有人了」說得通 |
| p114（所長） | 這樣燒大一點的火，太空人也不會有危險。 | 正確 | "which makes it possible to test larger fires without putting crew members at risk" |
| p115（所長） | 他們發現，把艙裡的空氣變稀一點，火就蔓延得比較慢。 | 正確（簡化） | "Results on flame spread in microgravity … show that reducing pressure slows down that spread."「空氣變稀」是氣壓降低給小孩的說法，可接受；沒有給數字，也沒有說太空人這樣滅火 |
| p116（所長） | 這些研究，幫忙挑選太空船裡用的材料， | 正確 | 開頭段 "Combustion investigations contribute to the safety … by guiding selection of spacecraft cabin materials" |
| p117（所長） | 也讓地上的防火更安全。 | 正確（選修 S2） | "This research also contributes to fire safety on Earth"。「讓…更安全」比 contributes 稍強，見 S2 |
| p118（所長） | 有一組研究滅火藥劑的實驗，還發現了一件怪事。 | 正確 | "FLEX, which analyzed the effectiveness of fire suppressants, led to the discovery of a type of cool flame, where the fuel continued "burning" … after extinction of the visible flame."「怪事」由 p121 起的冷焰兌現。後句 p119–p120 小問「火熄了，就是不燒了吧？」接得上；p121 的指涉見 F02 |

## 三、圖像提示詞

| 場景 | 台詞 | 結論 | 說明 |
| --- | --- | --- | --- |
| `chief-putout` | p109–p110 | 相符 | 所長認真聽、舉手做小心的手勢；小問提問時畫面是所長在聽，接著她回答，可接受 |
| `chief-worse` | p111–p112 | 相符 | 所長搖食指、表情認真＝「可能沒用，甚至讓火更糟」 |
| `cargo-ship` | p113–p114 | 相符 | 一艘小貨運太空船獨自飄在地球上空＝離站、沒人；卡通示意，不是 Cygnus 實物 |
| `cloth-flame` | p115–p116 | 相符 | 金屬艙裡一條布、細細的小火慢慢爬＝Saffire 燒布（來源圖說 "A sample of fabric burns inside an uncrewed Cygnus cargo spacecraft"）與「蔓延得比較慢」 |
| `chief-earth-safe` | p117–p118 | 相符 | 所長微笑手放胸口＝地上更安全；p118 的情緒標「賣關子」，跟圖的溫和笑容不衝突 |

## 四、選修建議（不影響結論）

| 編號 | 行 | 建議 |
| --- | --- | --- |
| S1 | p112 | 拿掉「所以」，讓理由留給 p114：「甚至讓火更糟。比較大的火，他們不在太空站上燒。」（23 字） |
| S2 | p117 | 照 contributes 放軟一點：「也幫忙讓地上的防火更安全。」（13 字） |

## 五、結論

**修正後通過。** 十句內容都有 NASA 原文支持，「可能」「比較大的火」「比較慢」都照來源的分寸；圖文相符；小問占比 18.1%。必改 1 項：F01 p110 含標點 26 字超過上限，換成建議句。建議 F02 把舊句 p121 改成回指「剛剛那組實驗」，新段結尾的鉤子才不會被聽成另一組實驗。S1、S2 選修。
