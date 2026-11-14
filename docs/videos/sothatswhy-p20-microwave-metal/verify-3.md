# 查核報告 3（sothatswhy-p20-microwave-metal）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿，也沒有寫 verify-1.md、verify-2.md）
- 日期：2026-11-14
- 範圍：2026-11-14 在第四章 p130 之後新加的「空著開」一段 p131–p143（場景 `oven-empty`、`empty-bounce`、`magnetron-glow`、`empty-bowl`、`chief-empty`，`claims.md` C22），連前一句 p130 與後一句 p144 讀；五個新鏡頭的圖像提示詞；全片小問字數占比。其餘台詞沒有重查，結論沿用 verify-2.md。
- 來源：`claims.md` 只當線索，不採用它的引文。今天在新的空目錄重新 curl GET（全部 200），HTML 去掉 script／style 與標籤轉純文字後 grep 並讀上下文，PDF 用 `pdftotext -layout`：
  - 美國 FDA〈Microwave Ovens〉（200，52,964 bytes）：開頭段、Cooking with Microwaves、Tips on Safe Microwave Oven Operation
  - Bloomfield〈What happens if you start the microwave oven with nothing inside?〉question-326（200，62,204 bytes；網站日期 1969-12-31 是佔位日期）：全文
  - Bloomfield〈Why are you required to have an item in the microwave oven while it is operating?〉question-483（200，62,977 bytes；1996-09-25）：全文
  - GE Appliances〈Spacemaker XL JVM1542 Owner's Manual〉（200，677,360 bytes）：Safety Information 全部，搜尋 empty／no food
- 結論統計（13 句）：**正確 13、需改 0、錯誤 0**。圖像提示詞 5 個：相符 5（1 處選修）。另有 2 處選修、1 處 `claims.md` 整理建議。
- 字數：13 句含標點計算，小問最長 12 字（p131）、所長最長 22 字（p142），都在上限內（小問 15、所長 25）。沒有拉丁字母、沒有阿拉伯數字。
- 小問占比（漢字，小問 ÷ 全部）：375 ÷ 2,157 = **17.4%**（163 句，所長 115、小問 48），≤ 20%。

## 一、需改的地方與理由

無。13 句都有來源支持，保留了來源的「有些」「可能」，接得上前後文。

## 二、逐句核對

| 行 | 現行台詞 | 結論 | 來源 | 依據摘要與前後文 |
| --- | --- | --- | --- | --- |
| p131（小問） | 那爐子空空的，按下去呢？ | 正確（提問） | — | 前句 p130「食藥署建議，用水和溫和的清潔劑，常常擦乾淨」，話題從爐子裡髒髒的（p128）轉到爐子裡空空的，同一個「爐子裡」的追問，接得上。問句不教人去按，答案 p143 是先看裡面 |
| p132（所長） | 食藥署也說，有些微波爐不能空著開， | 正確 | FDA | Tips："Some ovens should not be operated when empty."（就在清潔那一條的前一條，「也說」接 p130 的食藥署合理）。「有些」＝Some，沒有說每一台 |
| p133（所長） | 要看那一台的說明書。你猜為什麼？ | 正確 | FDA | 同條："Refer to the instruction manual for your oven."「你猜為什麼」引出下面的原理 |
| p134（所長） | 還記得嗎？微波在牆之間來回跑， | 正確（回呼） | FDA | "The microwaves are reflected within the metal interior of the oven"；回呼 p023「讓它在裡面來回跑，最後被食物吸收掉」，是點名回呼 |
| p135（所長） | 本來會被飯裡的水吸收掉。 | 正確 | FDA；Bloomfield 483、326 | FDA "where they are absorbed by food"、"Microwaves cause water molecules in food to vibrate"；483 "absorbed by the water in the food"；326 "no food (or rather no water-containing food)"。「飯」是故事裡的食物 |
| p136（所長） | 空空的，微波就在裡面越積越多。 | 正確 | Bloomfield 483 | "If there is no food in the cooking chamber, the microwaves build up in the cooking chamber until they are so intense…" |
| p137（所長） | 物理學教授說，多到最後，微波會倒流回去， | 正確 | Bloomfield 483、326 | 483 "large numbers of them flow backward through the pipe to the magnetron"；326 "will eventually find their way back to the magnetron"。「物理學教授說」是本集對 Bloomfield 的固定稱呼（p028、p039、p059、p074），不是新人物 |
| p138（所長） | 跑回做出微波的那個磁控管， | 正確（回呼） | Bloomfield 483；FDA | "flow … to the magnetron. These microwaves reenter the magnetron"；FDA "Microwaves are produced inside the oven by an electron tube called a magnetron"；回呼 p018「叫做磁控管」 |
| p139（所長） | 可能把它弄壞。 | 正確 | Bloomfield 483；GE | 483 "The magnetron begins to misbehave and can be damaged as a result."；326 "This situation is hard on the magnetron"。GE 說明書另寫 "Operating the microwave with no food inside for more than a minute or two may cause damage to the oven and could start a fire. It increases the heat around the magnetron and can shorten the life of the oven."，同方向。「可能」保留了 can／may |
| p140（所長） | 只放一個乾乾的空碗，也跟空著差不多。 | 正確（撰稿推論，合理） | Bloomfield 326；FDA | 326 "no food (or rather no water-containing food), those microwaves will not be absorbed"；FDA 陶瓷容器 "cannot be heated by microwaves"。乾碗沒有含水的食物，所以「差不多」是由兩句推出的合理推論，沒有說碗會碎或燒起來。`claims.md` 拿 GE「Do not microwave empty containers」當旁證，但那一句是在 Plastic cookware 的 guidelines 裡，講的是塑膠容器，見 N01 |
| p141（所長） | 因為陶瓷碗會讓微波穿過去，不會吸收。 | 正確 | FDA | "Glass, paper, ceramic, or plastic containers are used in microwave cooking because microwaves pass through these materials. Although such containers cannot be heated by microwaves…"；也呼應 p024 的「陶瓷」 |
| p142（所長） | 所以那位教授說，別讓微波爐空著開超過一兩秒。 | 正確 | Bloomfield 326 | "That's why you should never run a microwave empty for more than a second or two."「那位教授」＝p137 的物理學教授。GE 說明書的說法較寬（a minute or two），483 說 "any long periods of time"；片中採最嚴的說法並標明是教授說的，對小孩是安全的方向（見 S1） |
| p143（所長） | 按開始之前，先看看裡面有沒有放食物。 | 正確（撰稿的生活建議） | 由 FDA、Bloomfield 推出 | 不是來源原句，但完全落在 FDA "Some ovens should not be operated when empty" 與 Bloomfield 的建議之內。後句 p144 小問「要是真的冒火花了呢？」：原本接在 p130「髒東西可能冒火花」之後，現在中間隔了空著開一段；空著開一段沒有講火花，但全片主題就是火花，「真的冒火花」仍聽得懂，可接受 |

## 三、圖像提示詞

| 場景 | 台詞 | 結論 | 說明 |
| --- | --- | --- | --- |
| `oven-empty` | p131–p133 | 相符 | 打開的微波爐、空的玻璃轉盤，就是「空空的」 |
| `empty-bounce` | p134–p136 | 相符 | 空轉盤、金屬牆之間的淡藍波紋＝微波在牆之間來回、越積越多；示意 |
| `magnetron-glow` | p137–p139 | 相符（選修 S2） | 剖面、裝在空爐腔旁的銀色圓筒（磁控管）微微發橙光、爐腔擠滿波紋＝倒流回磁控管、熱起來（GE "increases the heat around the magnetron"）。示意，claims C22 已註明。前面寫 "three round plain knobs on the front"，跟其他鏡頭的 "smooth unmarked control panel and round plain buttons" 不一致 |
| `empty-bowl` | p140–p141 | 相符 | 乾的白色陶瓷空碗單獨放在轉盤上 |
| `chief-empty` | p142–p143 | 相符 | 所長指著打開的微波爐門、表情認真溫和，配「按開始之前先看看裡面」 |

## 四、選修建議（不影響結論）

| 編號 | 行 | 建議 |
| --- | --- | --- |
| S1 | p142 | 「別超過一兩秒」可能被八歲小孩聽成「空著按一秒沒關係」。來源原句如此，下一句 p143 也把結論落在「先看看裡面」，可不改。若要更穩，可改成「所以那位教授說，空的微波爐，一兩秒都別開太久。」—— 但這比來源嚴，也較拗口，不建議為此改 |
| S2 | `magnetron-glow` 提示詞 | 把 "three round plain knobs on the front" 改成其他鏡頭用的 "a smooth unmarked control panel and round plain buttons"，同一台爐子外觀才一致 |

## 五、`claims.md` 整理建議

| 編號 | 位置 | 建議 |
| --- | --- | --- |
| N01 | C22 原文 [6] | GE 的 "Do not microwave empty containers." 是 Plastic cookware 那一條 "Follow these guidelines" 的第 2 點，談的是塑膠容器，不宜當乾陶瓷碗的旁證。同一本說明書 Safety Information 的 FOODS 欄有更直接的一句："Operating the microwave with no food inside for more than a minute or two may cause damage to the oven and could start a fire. It increases the heat around the magnetron and can shorten the life of the oven."，可改引這句當 p139 的旁證，並在注意裡記下廠商說「一兩分鐘」、教授說「一兩秒」，片中採教授較嚴的說法 |

## 六、結論

**通過。** p131–p143 十三句都有來源支持、保留了來源的保留語氣，推論（乾碗、先看裡面）合理、不會誤導小孩，沒有不安全的說法；前接 p130 清潔、後接 p144 冒火花都接得上；小問占比 17.4%；字數都在上限內；五個新圖與台詞相符。沒有必改，S1–S2、N01 為選修。
