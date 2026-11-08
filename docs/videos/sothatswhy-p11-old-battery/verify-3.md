# 查核報告 3（sothatswhy-p11-old-battery）

- 查核者：Claude（第三輪獨立查核代理，未參與撰稿與前兩輪）
- 日期：2026-11-08
- 範圍：`verify-2.md` 之後改過的 10 句台詞 p018、p052、p116、p125、p134、p135、p168、p169、p174、p175（commit b45631cb「P11 round 5」對 `script.md` 的差異，行號取自 `video.json`），連同前後句一起讀；另核對 `claims.md` 引用這些句子的地方是否與 `script.md` 一致。
- 方法：用 curl（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`）重新抓下並讀原文，全部回 200：
  - Apple〈If your iPhone or iPad gets too hot or too cold〉https://support.apple.com/en-us/118431（publish_date 05142026）
  - Apple〈iPhone battery and performance〉https://support.apple.com/en-us/101575
  - Apple〈Maximizing performance〉https://www.apple.com/batteries/maximizing-performance/
  - Apple〈Important safety information for iPhone〉https://support.apple.com/guide/iphone/important-safety-information-iph301fc905/ios
  - Google〈Understand your Pixel battery〉https://support.google.com/pixelphone/answer/15738128?hl=en
- 結論統計（改過的台詞 10 句）：**OK 10、FIX 0、NOT FOUND 0**。`claims.md` 有 3 處引用或出處要改（K1–K3，見第三節），不影響台詞。

## 一、逐句核對

| 行 | 現在的句子 | 結論 | 來源 | 依據 |
| --- | --- | --- | --- | --- |
| p018 | 聽起來很怪吧？我們走進這顆老電池裡看看。 | OK（承諾，比喻） | — | 不是事實主張。「走進」是想像的說法，接下來 p021 起確實進入電池（水壺比喻、p051 起的水垢），承諾有兌現。前句 p015–p017 的兩個預告也都在片中回收（p116、p051–p056）。 |
| p052 | 就像家裡的熱水壺，用久了，裡面會黏上一層白白硬硬的東西， | OK（比喻＋生活常識） | — | 熱水壺的水垢是白色、硬的礦物沉積，屬一般常識。改成「就像」後明確是比喻，與 p055「不是真的水垢，是很像水垢的一層薄膜」一致，不會讓小孩以為電池裡真的有水垢。 |
| p116 | 原來這就是想不到的原因！ | OK | Apple 101575 | 回收 p015「那一下黑掉，有一個你想不到的原因」。前句 p114–p115「手機會搶先一步，自己關機，保護裡面的零件」對上「the system will perform a shutdown to preserve these electronic components. While this shutdown is intentional from the device perspective, it might be unexpected by the user.」——「想不到」正是 Apple 的「unexpected by the user」。後句 p117「多半沒有壞」不變。 |
| p125 | 對！一點都沒錯。 | OK（歸納） | Apple 101575 | 肯定 p123–p124 小問說的「壺裡的水、壺有多大，還有壺嘴多寬，是三件事」。Apple 頁面把 state of charge、maximum capacity、peak power（impedance）分開說明，是三個不同的量，肯定成立。三者並非互不影響（低電量也會暫時讓 impedance 上升），但這點緊接著由 p126–p129「水少了，再碰上窄壺嘴，就容易倒不夠」交代，「三件事」說的是三個不同的東西，不是互不相干，不衝突。原句「電量還多，不代表壺還大、壺嘴還寬」拿掉後，這個結論由 p033–p036、p097 與 p123–p124 帶到，沒有遺失事實。 |
| p134 | 那公園那麼冷…… | OK | — | 情境回想，接 p132–p133「天氣冷，壺嘴也會暫時變窄一點」（Apple 101575「impedance will temporarily increase … in a cold temperature environment」）。沒有新主張。與 p001「今天好冷喔」一致。 |
| p135 | 我好像快想通了！先不說， | OK | — | 敘事鋪陳，把答案留到 p171–p173 由小問自己說出。舊句「難怪在冷冷的公園，它一下就黑掉了」的因果現在由 p172「天氣又冷」承擔，沒有遺失。 |
| p168 | 那我剛剛在公園， | OK | — | 改成「剛剛」與 p001「我剛剛在公園拍松鼠」一致（舊句「那天」與開場的時間矛盾，現在修好了）。 |
| p169 | 手機到底發生什麼事？ | OK | — | 問句，答案在 p171–p173，各點依據見 verify-2（Apple 101575 的 peak power、impedance、低溫）。 |
| p174 | 對，就是這樣！下次冷天手機突然黑掉， | OK | Apple 118431；Apple 101575 | 「冷天」把建議限定在低溫造成的關機。118431：「Using an iOS or iPadOS device in very cold conditions outside of its operating range might temporarily shorten battery life and could cause your device to turn off.」101575：低溫時「You're more likely to experience unexpected shutdowns」。 |
| p175 | 先別怪它，帶回暖和的地方，再開機試試。 | OK（安全，見第二節） | Apple 118431；Apple〈Maximizing performance〉；Apple 101575 | 118431：「Battery life will return to normal when you bring your device back to higher ambient temperatures.」Maximizing performance：「When using your device in a very cold environment, you may notice a decrease in battery life, but this condition is temporary. Once the battery's temperature returns to its normal operating range, its performance will return to normal as well.」101575：「For a low battery state of charge and colder temperatures, performance-management changes are temporary.」順序是先回暖再開機，跟來源一致；「試試」沒有保證一定開得起來（老電池、低電量時可能還要充電），措辭有保留。 |

## 二、p174–p175 的安全判斷，以及與 p167 是否衝突

1. **是否正確**：正確。三個 Apple 來源都說低溫造成的影響是暫時的、回到正常溫度就恢復。沒有任何來源說回暖後不能開機。
2. **對小孩是否安全**：安全。
   - 動作只有「帶回暖和的地方」與「按開機」，不涉及拆機、充電器或插電。
   - 先回暖再開機的順序也避開了低溫充電：118431「If your iOS or iPadOS device gets too cold, it might not charge or could stop charging」，手機自己會擋，片中也沒叫小孩在冷天充電。
   - 「暖和的地方」可能被理解成暖爐、吹風機旁邊嗎？風險低：中文「暖和」指舒服的溫暖，不是熱；而且片中 p087–p090 已教過「大約超過三十五度就太熱」、p160「別在大太陽底下充」，前後文足以擋住這個誤解。118431 的使用範圍是 0–35°C，同頁過熱時也是「Move your device to a cooler environment」。不需要改。
   - 從很冷的戶外拿進室內可能有凝結水氣，查過的來源都沒有提，片中也不必提，判為不需處理。
3. **與 p167 是否衝突**：不衝突。
   - p167「要是它鼓鼓的、很燙，就別用也別充，馬上告訴大人」（Google 15738128：鼓脹時「Let it sit unused for several days until the battery naturally drains」，不要按壓、撬開、自己修；Apple 安全資訊：「If you suspect damage to iPhone or the battery, discontinue use of iPhone」）。
   - p174–p175 限定「冷天突然黑掉」，情境是冷，不是「很燙」；「鼓鼓的」是外觀上的損壞徵兆，p167 對任何情況都優先。兩句的條件不重疊，`claims.md` 也已寫明「熱或鼓脹的情況由 p167 的安全句處理，不適用這句」。
   - 舊句「它多半是在保護自己」可能讓小孩把任何黑掉都當成沒事；新句限定冷天並給出具體步驟，比舊句更安全。

## 三、`claims.md` 引用核對

逐條找了 `claims.md` 提到這 10 句的地方。引文文字都與 `script.md` 一致（p174–p175 的引文省略了句首「對，就是這樣！」，屬節錄，可以）。以下三處行號或出處名稱不對：

| # | 位置 | 原文 | 結論 | 建議改成 |
| --- | --- | --- | --- | --- |
| K1 | 〈意見與比喻〉第二點 | p125「對！一點都沒錯。」（小問 p124–p125 自己說出三件事） | FIX（行號錯：小問說三件事是 p123–p124，p125 是所長） | p125「對！一點都沒錯。」（小問 p123–p124 自己說出三件事） |
| K2 | 〈意見與比喻〉最後一點 | 依 [16] Apple 118431（低溫造成的關機是暫時的，回到正常溫度就恢復）與 p133–p134 的冷天段落 | FIX（行號錯：冷天段落是 p132–p133，p134 是小問「那公園那麼冷……」） | 依 [16] Apple 118431（低溫造成的關機是暫時的，回到正常溫度就恢復）與 p132–p133 的冷天段落 |
| K3 | 〈來源〉第 16 條 | 16. Apple, About iPhone batteries / Maximizing battery life（verify-2 補：停在車裡的高溫、低溫關機是暫時的、遊戲與相機是重度使用）. https://support.apple.com/en-us/118431 | FIX（頁名不對：118431 的標題是 "If your iPhone or iPad gets too hot or too cold"） | 16. Apple, If your iPhone or iPad gets too hot or too cold（verify-2 補：停在車裡的高溫、低溫關機是暫時的、遊戲與相機是重度使用）. https://support.apple.com/en-us/118431 |

另外 K2 括號裡的「低溫造成的關機是暫時的」是改述：118431 原句是低溫「could cause your device to turn off. Battery life will return to normal when you bring your device back to higher ambient temperatures」，〈Maximizing performance〉才有「this condition is temporary」。意思相符，可以不改；要更貼原文，可以在 K2 的括號後加上「；[5] "this condition is temporary"」。

## 四、順帶發現（不在這次範圍，未改）

- `brief.md` 的章節表仍是舊句：第 65 行章尾「那天我的手機到底發生什麼事？」（現在是 p168–p169「那我剛剛在公園，手機到底發生什麼事？」），第 66 行收尾「下次突然黑掉，先別怪它」（現在限定冷天，並改成「帶回暖和的地方，再開機試試」）。只是企劃文件，不影響影片，建議下次改稿時順手同步。
