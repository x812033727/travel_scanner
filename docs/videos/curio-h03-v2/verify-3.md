# curio-h03-v2 查核第三輪（開場預告）

- 查核 2026-10-13，Claude Opus 5.5（獨立查核代理，不是改寫開場的那一個）。`video.json` 一個字都沒動。
- 範圍：`git diff HEAD -- video.json` 裡新增或改過的旁白（第 1 章與五句正文），以及拿掉的 `tg1f`–`tg1i`、`tg1k`–`tg1m`
  造成的連帶影響。對照 `claims.md`、`verify-1.md`、`verify-2.md`、`NOTES.md`〈開場預告 2026-10-13〉。

## 改過或新增的句子

| id | 句子 | 結果 |
| --- | --- | --- |
| `tg1o` | 說不通的，還不只這一件。 | OK（不是事實主張） |
| `tg1p` | 一九二七年，有人順著倒樹走到正中央，找一個坑。 | OK（`tg3a`、`tg3e`、`tg3o`） |
| `tg1q` | 他把沼澤裡一個圓坑的水抽乾，底下會是什麼？ | OK（h21 只抽乾其中一個；「他」指 `tg1p` 那個人，就是庫利克，指對了；不帶年份，正確） |
| `tg1r` | 一九四六年，一篇小說寫的就是那一聲。 | OK（h28） |
| `tg1s` | 二〇二五年，有人去追最常被引用的那個數字。 | OK（h33） |
| `tg2j` | 那天早上，離爆心更近的帳篷被撞得搖晃。 | OK（h5 原文「更靠近爆心的埃文基人帳篷被撞得搖晃」；比較的基準是開場那個交易站的男人，下一句 `tg2k` 點出埃文基人） |
| `tg3c` | 它們不是亂倒的。 | OK（`tg3d` 揭曉） |
| `tg4i` | 那個圓坑底下，露出來的不是鐵。 | OK（h21） |
| `tg5c` | 那篇小說裡，爆炸來自一艘外星核動力太空船。 | OK（h28） |
| `tg6h` | 那篇評論指出，那個面積錯了。 | OK（h33：面積高估是二〇二五年評論追出來的，歸給評論更準） |

## 拿掉開場句的連帶影響

- 「全部朝外倒」改由 `tg3d` 第一次講，`tg7g`「剛剛那些朝外倒的樹」指得到；帳篷改由 `tg2j` 第一次講；
  `tg2g` 的回呼指向 `tg1j`，仍在開場。標題「森林倒了，坑在哪裡？」、縮圖「樹站著／沒有坑」（`tg3j`、`tg3q`）不受影響。
- **註記（不必改）**：說明欄第 1 段的「六十四公里外的人被掀下椅子」現在只在說明欄，旁白不再講距離。事實本身是
  h4 查核過的，說明欄可以保留；若要旁白也撐著，可以不動。
- **註記（舊的，不是這一輪造成的）**：`tg2a`／`tg2g` 說「那幾個亮著的晚上」，開場 `tg1j` 只說「那天晚上」。h6、h27
  支持「事後幾個晚上都亮」，所以不算錯；若要一致，可把 `tg1j` 改成「那天晚上起，從西伯利亞到歐洲，夜空一連亮了好幾晚。」

## 結論

10 句改過或新增的旁白全部 OK，沒有新的事實、數字、年份或名字，代詞都指對人。沒有必改項目，不需要第四輪。

## 盲評修改查核 2026-10-13

- 查核 2026-10-13，Claude Opus 5.5（獨立查核代理，沒有參與這四輪改寫）。`video.json` 一個字都沒動。
- 範圍：上一節之後的改動，也就是 `NOTES.md`〈查核第三輪修正〉、〈盲評修正〉、〈盲評修正第二輪〉、〈盲評修正第三輪〉列的每一句，
  對照 `git diff HEAD -- video.json`。上一節已判過的 `tg1o`–`tg1s`、`tg2j`、`tg3c`、`tg4i`、`tg5c`、`tg6h` 不重判。
- 今天重開的來源（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一主機間隔 1.2 秒以上，全部 200）：
  L07（波隆那大學專書章 PDF）、APS、N115、N19、BB25、EB（2026-09-01 存檔）、OSU。

### 改過或新增的句子

| id | 句子 | 結果 |
| --- | --- | --- |
| `tg1j` | 那天晚上起，從西伯利亞到歐洲，夜空一連亮了好幾晚。 | OK。N115「For several days after, the night skies glowed over Asia and Europe」；EB「abnormally bright nighttime skies in Siberia and Europe for some time after the event」；L07 記 6/30 到 7/3 有 159 筆、之後到 7/28 還有約二十筆，並說只有 6/30 起的才算這件事（6/21–29 的十四筆被判為不可靠、地方性），所以「那天晚上起」也對。範圍 L07 寫愛爾蘭阿馬到克拉斯諾亞爾斯克，「西伯利亞到歐洲」成立 |
| `tg2m` | 消息早就有了，為什麼沒有人走進那片森林？ | OK。「消息早就有了」＝h8（十二天後見報）、h9（觀測站當天徵集）。註記：埃文基人就住在那一帶（`tg2k`），「沒有人」聽得出是指去調查的人；N115 的原話是「No scientific expeditions … for nearly 20 years」，可以不改 |
| `tg2s` | 沒人走進那片森林，是因為那一帶根本走不進去。 | **要改**。N115 把空窗期的原因寫成兩個：「partly due to its remote location and partly due to distractions such as World War I, the Russian Revolution, and the ensuing civil war」。「走不進去」本身有來源（N115「so inaccessible that he could not reach it」、APS「harsh conditions … foiled」，講的是一九二一年那一趟），但這一句把它講成十三年空窗的唯一原因，丟了戰爭與革命那一半。改成：**「沒人走進那片森林，原因之一是那一帶根本走不進去。」**（不加新事實，仍點名回答 `tg2m`）。若要把另一半也講出來，可用「沒人走進那片森林，一半是因為戰爭和革命，一半是因為那一帶根本走不進去。」，但那要先在 `claims.md` h12 補上 N115 的戰爭／革命那一句 |
| `tg3q` | 不只正中央，到今天，方圓一萬五千平方公里之內都沒有。 | OK。C4 不變：L07「have ever been found in an area of 15 000 km2」＋N19／EO／EB 撐「到今天」；「不只正中央」對上一九二七年爆心沒有坑（N115、EB、APS「there was no impact crater」）。省掉的「坑」字由上一句 `tg3o` 與卡片「沒有坑」補足 |
| `tg4p` | 一塊都沒有找到，到今天也沒有人找到大塊的。 | OK。前半是庫利克那三年（OSU「trying and failing to find it」，h23）；後半是 C5 的「macroscopic」限定（L07），N19 2019「no one found fragments」、EB 只記毫米以下的碎片。下一句 `tg4q`／`tg4r`（微小碎屑、無法確定有關，N115「could not be conclusively tied to the blast」）接得上，不矛盾 |
| `tg4ad` | 照這個說法，那幾晚的光來自彗尾散開的塵埃。 | OK。APS「The dust and particles that caused the glow could have been debris from the disintegrated comet's tail」；L07 記 Zotkin 的結論是「ice particles from the comet tail」。「照這個說法」把它鎖在彗星說之內，旁白沒有替它背書，APS 的「could have been」由這個歸屬保住；彗星說本身的地位由 `tg7v`（還在爭論）交代。「塵埃」是 APS 的字，L07 寫冰晶，不衝突 |
| `tg4x` | 這個說法一直留到今天。 | OK（文字不動，只換場景；h27） |
| `tg6k` | 所以那八千萬棵倒樹，從一開始就高估了。 | OK。BB25 兩句都在：面積「overestimated by a factor of about four」，棵數「inflating the number of fallen trees by a factor of about four」——評論明說的是**棵數**被高估，不只是面積。「從一開始」＝一九三三年那次粗估就是從高估的面積換算出棵數。仍是當流傳的數字講，沒有給「正確棵數」 |
| `tg7b` | 開頭那個問題的答案是：它衝進大氣，在半空中炸開。 | OK。空中爆炸在每一個來源裡都是事實語氣：N115「exploded in the skies over Siberia」、EB「Because the object exploded in the atmosphere … no impact crater」、EO「The explosion, an airburst」、APS 連彗星說都寫「the object that exploded in the atmosphere was a comet」。h40 懸著的是**天體是什麼**（小行星還是彗星），不是它有沒有在空中炸開，兩說都是空爆，所以這一句沒有越過紀錄；它也沒有說「從來沒有落地」，h42 的限制守住了。下一句 `tg7c` 用「主流的估計」交代高度的地位 |
| `tg7i` | 所以那個找不到的坑，根本沒有形成。 | **建議改**。原句「所以地上沒有坑」是觀察（對上 L07「no crater ever found」）；新句變成「坑根本沒有形成」的因果斷言，而三句之後 `tg7n`「二〇〇七年有一隊人說，湖底像撞擊坑」、`tg7q`「沒有結論」——切科湖假說主張的正是一塊碎片砸出了坑（h38，DISPUTED）。「那個找不到的坑」不限定是哪一個，聽起來會被 `tg7n` 打臉。把它鎖在庫利克在爆心找的那個坑，EB「no impact crater」、N08「That is why there is no impact crater」完全撐得住，切科湖（離爆心約八公里）也留在懸案裡：**「所以庫利克在爆心要找的那個坑，根本沒有形成。」**（仍點名回呼 `tg3o`／`tg4b` 與標題「坑在哪裡」） |

### 刪掉的句子

| id | 原句 | 結果 |
| --- | --- | --- |
| `tg2v` | 他沒有走到。 | OK。章名「一九二一年那趟，他沒走到」與卡片「0 次／走到爆心」仍在，事實不缺；`tg2u` 的 `reveal: 2` 讓兩格同時出現，卡片內容不變 |
| `tg3f` | 那是他第一次走到那裡。 | OK。`tg3a` 已講 |
| `tg3r` | 大塊的碎片也沒有。 | OK。事實與「大塊」限定詞併進 `tg4p`；`no-crater` 卡片沒有提碎片，不用改 |
| `tg3s`–`tg3u` | 後面那幾年，他又帶隊回去了幾次／每一次都在找同一樣東西／一塊鐵。 | OK。h19 不再進旁白，沒有別的句子依賴它；「找的是鐵」由 `tg2q`、`tg4i`、`tg4o` 交代。註記：抽乾蘇斯洛夫坑在 APS 是「Over three successive expeditions … when he finally drained one」，旁白先講抽坑、再講 `tg4o`「接著三年」，順序略有前後，但 `tg4o` 的「接著」可讀成一九二七年之後（OSU「the better part of the next three years」），不算錯，可以不改 |
| `tg4k` | 他抽的那個坑裡，始終沒有大塊殘骸。 | OK。抽坑的結果由 `tg4i`／`tg4j`（老樹樁）交代，沒有句子因此懸空 |
| `tg6a` | 還記得那八千萬棵倒樹嗎？ | OK。第 6 章從 `tg6b` 起，「它的來歷」的「它」指上一章 `tg5r`「最常被引用的那個數字」，指得到 |

### 文件註記（不是觀眾看得到的字，我不改檔）

- `claims.md` 有幾處跟著舊稿：h27 沒提 `tg4ad` 與 APS 的「could have been」；「不是來源主張的句子」裡 `rail-ends-at-the-forest` 還引舊的 `tg2m`；
  h5、h6、h14、h19、h22、h33 的場景清單仍列著不再使用的插圖（`tents-shuddering`、`steadying-on-a-pole`、`reading-without-a-lamp`、
  `sieve-of-grit`、`boots-back-on-the-trail`、`silted-floor-of-the-pit`、`finger-stops-on-a-figure`）。下一個動 `claims.md` 的人請一起對齊。

### 結論

10 句改過、新增或移動的旁白：8 句 OK，2 句要改——`tg2s`（必改：把兩個原因講成一個）、`tg7i`（建議改：「坑根本沒有形成」不限定會跟切科湖那一段相衝）。
刪掉的 9 句沒有留下沒有來源或互相矛盾的句子。`tg7b` 的「答案是」沒有越過紀錄：空爆是所有來源的事實語氣，h40 懸的是天體種類。
兩句照上表替換後不需要再一輪查核（替換句只收窄說法，沒有新事實）。

## 第四到六輪修改查核 2026-10-13

- 查核 2026-10-13，Claude Opus 5.5（獨立查核代理，沒有參與第四到六輪改寫）。`video.json` 一個字都沒動。
- 範圍：上一節之後的改動，也就是 `NOTES.md`〈盲評修正第四輪〉、〈盲評修改查核的修正〉、〈盲評修正第五輪〉、〈盲評修正第六輪〉列的句子，
  對照目前 `video.json` 的旁白順序。`tg2s`、`tg7i` 照上一節的替換句套用，逐字相符，不重判。
- 今天重開的來源（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一主機間隔 1.2 秒以上，全部 200）：
  OSU、N115、APS、N08（存檔）、BB25、AOP、J19（存檔）。L07 的一九二五／一九三〇兩句沿用 `verify-1.md` #25、`verify-2.md` #25 當天的逐字引文。

### 改過、移動或新增的句子

| id | 句子 | 結果 |
| --- | --- | --- |
| `tg2j` | 有目擊者說，離爆心更近的帳篷被撞得搖晃。 | OK。OSU 是當事人的回憶：「As Akulina later recalled, something suddenly hit her tent … the tent shook again knocking them over」，所以「有目擊者說」有字面依據。「更近」OSU 沒寫，但 N115 寫了「Those closest to the event reported being blown into the air」——同時撐「目擊者說」與「離爆心更近」，旁白取的是較輕的 OSU 版本。沒有寫成伊爾庫次克徵集到的報告，正確（OSU 只說「later recalled」，沒說何時、向誰說）。註記（不必改）：開場的交易站男人已經在三十幾句之前，「更近」的比較對象現在要靠觀眾自己回想；不算錯。`claims.md` h5 可以補 N115 那一句當「更近」的出處 |
| `tg2h` | 地震儀和氣壓計上的紀錄，也等了很久。 | OK。L07：地震波「published only in 1925 (Voznesenskij 1925)」、氣壓紀錄「associated with the TE some twenty years later (Whipple 1930; Astapovich 1933)」。「也」接 `tg4t` 切科湖「要很久以後才變成線索」，兩件都是後來才被連回，並列成立 |
| `tg2i` | 它們要到一九二五年和一九三〇年，才被連回那個早上。 | OK。新位置在庫利克一九二七年走到爆心、抽坑、「接著三年」之後，在一九三〇年彗星說之前。句子自己帶兩個年份，又是「要到…才」的回頭說法，聽不出「連回」發生在一九二七年以後；一九二五早於庫利克抵達，但旁白沒有說它在他挖的時候發生。下一句 `tg4u`「他還在挖的時候，別人已經開始往天上找了」講的是一九三〇年彗星說，不是地震紀錄，不會把一九二五年誤掛到挖坑那幾年。「那個早上」仍是全片固定指一九〇八年六月三十日的說法（`tg2b`、`tg2c`、`tg7ac`），搬到第 4 章沒有指錯 |
| `tg7q` | 湖底的事沒有結論，那天早上有沒有人喪生？ | **建議改（低）**。前半 OK（h38，同 `tg7n`–`tg7p`）。後半的問句把範圍限在「那天早上」，但答案 `tg7s`–`tg7t` 的來源 J19 寫的是「at least 3 passed away (immediately or later) as a direct consequence」——包括事後才過世的；AOP 也是「casualties caused by the Tunguska event」，不限當天。問句比證據窄，觀眾會把「至少三人」聽成當天早上死的。改成：**「湖底的事沒有結論，有沒有人因為那一聲喪生？」**（「那一聲」是全片固定指這場爆炸的說法，`tg1e`、`tg1r`、`tg4r`；不加新事實，`tg7r` 的點名回收不用動） |
| `tg7s`–`tg7r` | 二〇一九年一篇論文統計，倒樹區內外至少三十人／其中至少三人因此過世／也有資料只記兩則未經證實的報告／有沒有人喪生，也沒有結論。 | OK。文字沒變，今天重開兩邊逐字仍在：J19「inside and near the tree-fall area were at least 30 people … at least 3 passed away (immediately or later)」；AOP「Apart from two unconfirmed reports there are thought to have been no human casualties」。一邊說至少三人、一邊說只有兩則未證實的報告且認為沒有傷亡，h39 判 DISPUTED，「沒有結論」是準確的摘要，沒有說「無人傷亡」也沒有把三人講成定論。（OSU「At least two others appear not to have been so fortunate」、N115「very few human casualties」也在這個範圍內，旁白不必加。）「也」接 `tg7q` 的湖底，仍成立 |
| `tg5c` | 開頭說的那篇小說裡，爆炸來自一艘外星核動力太空船。 | OK。指回 `tg1r`「一九四六年，一篇小說寫的就是那一聲」，就是同一篇；事實同 h28（OSU「an atomically-powered space craft from another planet blew up over Siberia」） |
| `tg6h` | 開頭說的那場追查，追到的是：那個面積錯了。 | OK。指回 `tg1s`（二〇二五年有人去追那個數字）＝`tg6b` 的期刊評論。BB25 兩件都寫了：根源是面積——「Astapovich's preliminary guess based on the area of devastation that he overestimated by a factor of about four」；棵數是結果——「inflating the number of fallen trees by a factor of about four」。這一句講根源（面積），兩句之後 `tg6k` 講結果（棵數高估），合起來和評論一致；「追到的是」的對象是面積，沒有說棵數沒問題，不衝突 |
| `tg3a` | 開頭那趟一九二七年的路，他終於走到了。 | OK。指回 `tg1p`「一九二七年，有人順著倒樹走到正中央」；「他」＝`tg2x` 六年後再出發的庫利克；APS「Kulik's team made the arduous journey to Tunguska in 1927」、N115 一九二七年抵達（h15） |
| `tg4f` | 開頭說的那個圓坑，他決定把水抽乾。 | OK。指回 `tg1q`「他把沼澤裡一個圓坑的水抽乾」；緊接 `tg4e` 蘇斯洛夫坑，APS「when he finally drained one」（h21）。句子不帶年份，沒有把抽坑鎖在一九二七年 |

### 刪掉的句子

| id | 原句 | 結果 |
| --- | --- | --- |
| `tg6j` | 一邊是假設，一邊是後來量到的。 | OK。假設（`tg6f` 八千平方公里）與量到的（`tg6i` 四分之一左右、`tg3g` 兩千一百五十）都還在旁白裡 |
| `tg6n` | 他們追的是一條引用鏈。 | OK。引用鏈由 `tg6m` 與 `tg6p`–`tg6t` 一步一步交代（BB25：一九三三 → 一九三四 → 一九八二 → 照抄） |
| `tg6o` | 每一篇都只是引上一篇。 | OK。同上；`tg6t`「被當成不用附出處的事實」仍有 BB25「as if it were an established fact that needs no citation」撐著 |
| `tg2g` | 還記得那幾個亮著的晚上嗎？ | OK。不是事實句；夜光由 `tg1j`、`tg2a`、`tg4w` 交代，沒有句子依賴它 |

### 文件註記（不是觀眾看得到的字，我不改檔）

- `claims.md` h5 只引 OSU；「更近」與「目擊者說」的另一個出處是 N115「Those closest to the event reported…」，可補進去。
- `claims.md` h33 的場景清單仍列著已拿掉的 `four-links-of-a-chain`；h10 的場景現在在第 4 章（`seismograph-drum`、`rolls-on-a-shelf`），清單本身不用改，但若有章節註記要跟著移。
- APS 另有一句「guarded it zealously from outsiders – one reason it took nearly two decades」，和 `tg2s` 的「原因之一」相容，可當 h12 的旁證；旁白不必改。

### 結論

9 列改過、移動或新增的旁白：8 列 OK，1 句建議改——`tg7q`（低：問句「那天早上」比 J19 的「immediately or later」窄，改成「湖底的事沒有結論，有沒有人因為那一聲喪生？」）。
`tg2h`／`tg2i` 搬到第 4 章沒有暗示錯的年份；`tg7r` 的「沒有結論」準確；`tg6h` 講面積、`tg6k` 講棵數，合起來和 BB25 一致。
刪掉的 4 句沒有留下沒有來源的句子。替換句只收窄說法，沒有新事實，套用後不需要再一輪查核。
