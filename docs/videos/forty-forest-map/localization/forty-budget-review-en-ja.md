# ForTy縮句獨立複核：EN／JA final

2026-10-25。下列先行紀錄在JA-only階段完成，當時EN尚無候選。**EN final現已完成，新增版本與40索引結果見文件後半「EN final追加」**；保留先行來源綁定，不把舊JA-only收據冒充當時已審EN。

**JA結論：18項中17項語義可採，ci5j 1項需保留必要性；ncx4 early-release修正可採。** 所有數字、否定、森林類別及步驟未見其他實質錯誤。這是字句／字元指引審查，沒有原生合成或實際fit通過聲明。

## 輸入綁定

| 項目 | SHA256／版本 |
| --- | --- |
| forty-budget-proposals-en-ja.json | `5c93414db432f44fa5488709fabed190fb35541068fdd97993a4951152aa5261`；status=partial，JA complete，EN pending且proposals=[] |
| 實際繁中video.json | `a62a48382272fb4b9171f2c261b8f736c7516afca35417ccaa842757b04f8a6f` |
| 實際i18n/ja.json | `5c72c16792a52168733f7fa03db7214e8e32a96139858999e5ec6577ac2aa9e6` |
| 目前ja.todo.json | `e1e004ac6da9cdfc30e5e0791d47242e2e18f54c759fe000eb176b8aa7a55af7` |
| current native budget audit | `c734477992e99ce18192142a8c1031298668128dd96f4c79e377c29fafde36e9`，speech_hash=`7d55bafd91bc907f` |

候選檔記錄的舊JA i18n SHA是3f468d…2d4e，實際我讀到上表5c72c…9e6，已據實分清。逐條比對：18項old_text均與實際current i18n相符，source也都與a62a繁中相符；不是只信候選作者的meaning_check。root已採metadata early-release等修正，本輪不重套、不覆寫metadata。

## ci5j需修：保留「還要／需要」對照參考資料

繁中：模型看見的是觀測線索，土地歷史和經營用途還要對照參考資料。

候選：

> モデルが見るのは観測の手がかりです。土地の履歴や経営上の用途は参照資料と照合します。

「照合します」變成直接敘述對照動作；原意是這些資訊**仍需另行對照**，沒有聲稱本片或模型已查完土地歷史。建議保留必要性：

> **モデルが見るのは観測の手がかりです。土地の履歴や経営上の用途は参照資料との照合が必要です。**

實數45字，最新max_chars=45。完整保留觀測線索、土地履歷、經營用途與參考資料，不須為縮句把未完成要求說成已完成資訊。本輪未寫回譯文或hash。

## ncx4 early-release：修正可採

- Current：その紹介では、2017〜2025年の初期の年次系列も共有されました。
- Proposal：**その紹介では、2017〜2025年の早期公開版の年次時系列も共有されました。**
- 38字／目前max39。2017–2025、年度時序及分享來源均保留；早期公開版清楚對應early-release，不會把「早期」誤讀成資料只含較早歷史年份。此修正尚未在我讀取的current JA captions中套用。

## 其餘17候選：可採範圍

1. 8aw6保留2020／台灣／ForTy與取出綠格；日語省略私は仍以敘述者為隱含主詞，不新增第三方量測。
2. gngj保留6分類／只存5值／疑問；5ur9保留今週、DeepMind介紹ForTy與2格閱讀，未稱2020資料本週首發。
3. rrgq完整保留可能包含、都市樹木與木本植生；沒有縮成只有喬木或裸地。
4. AlphaEarth多年觀測→數值、10m輸出尺度且非逐樹定位、五值有效→補第6類→比較六類、缺的第6類與250減其餘總和，都保留。
5. B同一區塊、刻意選最小最高分、非隨機精度樣本仍在；1色條件、A唯一最高分類、score不能直接當正確機率及尚未事後校準的否定均保留。
6. 4w7g「地図でよく見る環境は？」仍問用地圖常看哪種環境，未改成哪張地圖或哪個地方；11字在13字指引內。outro共享視窗是否實際容納仍由原生fit判斷。
7. jw6i及appe最新預算已容納原文，候選正確採keep_current_already_fits，沒有為舊清單強制縮句。

e826的「その他の土地を補い」在數值語境中可理解。若root希望更明確，可選**5つの値は全て有効で、その他の土地の値を補い6分類を比べられます。**（33／38），補一個值字不改模型／分類含義；此為可選清晰度改善，不列額外must-fix。

## 最新字元指引與未完成事項

18個原候選均在目前native max_chars內，沒有新增超者；ci5j建議45／45也在內。這不是聲音長度／閱讀速度保證，沒有實際合成、調速或改時槽。凡之後native fit不符，應保義再修，不刪數字、必要性或否定。

統計：JA18候選＝17可採＋1需修；另ncx4修正可採。EN pending／0候選／0已審。metadata屬root已採事項，未納入本輪改動。只寫scratch，未改repo／todo／聲音，也未建立新代理。

## JA18完整逐項表

| ID | Actual zh-TW source | Frozen JA candidate | Chars / current max | Independent verdict |
| --- | --- | --- | --- | --- |
| 8aw6 | 我從二〇二〇年的台灣資料，取出這個ForTy綠格。 | 2020年の台湾データからForTyの緑色マスを取り出しました。 | 32 / 34 | ACCEPT meaning; actual native audio fit not yet tested |
| gngj | 地圖分六類，為什麼只存五個值？ | 6分類なのに保存値は5つだけなのはなぜですか。 | 23 / 28 | ACCEPT meaning; actual native audio fit not yet tested |
| jw6i | 另一格同樣綠，讀出的結果也會一樣嗎？ | 別のマスも同じ緑色ですが、読み取る結果も同じなのでしょうか。 | 30 / 30 | ACCEPT; current original already fits |
| 5ur9 | 本週DeepMind介紹ForTy，就從這兩格讀起。 | 今週DeepMind紹介のForTyを2マスで読みます | 27 / 27 | ACCEPT meaning; actual native audio fit not yet tested |
| rrgq | 剩下的其他土地，也可能包括城市樹木或稀疏木本。 | 残るその他の土地には都市の樹木やまばらな木本植生も含まれることがあります。 | 37 / 37 | ACCEPT meaning; actual native audio fit not yet tested |
| 9wmz | AlphaEarth先把多年衛星觀測整理成一組數字。 | AlphaEarthが多年の衛星観測をまず数値にまとめます。 | 30 / 33 | ACCEPT meaning; actual native audio fit not yet tested |
| yi97 | 十公尺網格是輸出尺度，不是每棵樹的定位清單。 | 10メートル格子は出力尺度で、個々の木の位置一覧ではありません。 | 32 / 34 | ACCEPT meaning; actual native audio fit not yet tested |
| e826 | 這一格的五個值都有效，可以補出其他土地，然後比較六類。 | 5つの値は全て有効で、その他の土地を補い6分類を比べられます。 | 31 / 38 | ACCEPT meaning; actual native audio fit not yet tested |
| 3gwz | 開頭少掉的第六類，要怎麼補回這張表？ | 冒頭で欠けた第6分類を、表にどう補いますか。 | 22 / 24 | ACCEPT meaning; actual native audio fit not yet tested |
| 7iv8 | 第六類留在總量裡，用兩百五十扣回來。 | 第6分類は250から他の合計を引いた残りです。 | 23 / 25 | ACCEPT meaning; actual native audio fit not yet tested |
| appe | 換到同一區塊的另一格，這次刻意挑最高分最低的位置。 | 同じ区画の別のマスへ移ります。今回は最高スコアが最も低い位置を意図的に選びます。 | 40 / 41 | ACCEPT; current original already fits |
| beg8 | 這是閱讀練習，不是拿隨機樣本估整張圖的精度。 | 読み取り練習で、全図の精度推定用の無作為標本ではありません。 | 30 / 33 | ACCEPT meaning; actual native audio fit not yet tested |
| 8k4a | 如果只能塗一種顏色，畫面會選哪一個？ | 1色だけなら、画面はどちらを選びますか。 | 20 / 26 | ACCEPT meaning; actual native audio fit not yet tested |
| ww8v | 還記得開頭那個綠格嗎，它的最高者只有一個。 | 冒頭の緑マスは最高が1分類だけでしたね。 | 20 / 25 | ACCEPT meaning; actual native audio fit not yet tested |
| sbkg | 兩個綠格讀完後，這些分數能不能直接當作正確機率？ | 2つの緑色マスを読んだ今、スコアはそのまま正解確率でしょうか。 | 31 / 36 | ACCEPT meaning; actual native audio fit not yet tested |
| vb62 | 它是模型分數，還沒有做事後的機率校準。 | モデルスコアで、事後の確率校正はまだ行われていません。 | 27 / 28 | ACCEPT meaning; actual native audio fit not yet tested |
| ci5j | 模型看見的是觀測線索，土地歷史和經營用途還要對照參考資料。 | モデルが見るのは観測の手がかりです。土地の履歴や経営上の用途は参照資料と照合します。 | 42 / 45 | REVISE: preserve need for independent reference checks; exact45-char replacement above |
| 4w7g | 你常用地圖看哪種環境？ | 地図でよく見る環境は？ | 11 / 13 | ACCEPT meaning; actual native audio fit not yet tested |

EN status at this receipt: pending, no candidates supplied or reviewed. Preserve this JA-only input binding when appending later EN findings.

## EN final追加：40索引全部覆核

本追加前JA-only報告SHA為`47f7b8ca6ddcb7a44dbdde60228de09f5bfb2376f5602d060b4fec95d4ac9531`，已保留於此。只擴充本scratch報告，沒有改repo／todo／音訊／hash／門檻，也未重新審整篇非候選旁白。

**EN結論：40索引＝34項語義可採、5項建議修正、1項4w7g保留完整環境問句／單句未解。** 39個非null候選均在最新actual sheet字元指引內；「字元內」未被寫成已合成fit。另8m2e及ncx4修正可採；w86h修正與40索引重複，不重複計數。

### 新版本與來源差異

| 項目 | 實際讀取SHA256／版本 |
| --- | --- |
| final候選forty-budget-proposals-en-ja.json | `75d439e6e74aa2fdd8cb141ae63406d42e23d984c334f53a09e12f606ccbe9bb`；status=final，EN complete_with_one_unresolved |
| 最新繁中video.json | `2b689e3f9e2f38d8da58b5fd1d5d999a2ef5d8e917102680a8c6de06cd859ca6` |
| 最新claims.md | `71a1f1ac335b880e9b68819f5dc4c7e165c47a6fbf1f2f094d4fc21d50b78f36` |
| 實讀EN i18n | `8f0765649847d8e88860617ff8fb1b6a817d5c2a8f1faae9c45195bfc464e5fc` |
| 最新actual EN sheet | `28dc205389a3df3e476511fe9a3b85971d83f9121f5c57f5ac937e56aa4df4b5` |
| 另核對當前JA i18n | `0169b9c40450cbb088795f7a0a1d851a833c52d07711f6836eaf0952c17ed1a1` |

final候選的capture SHA早於上述current i18n，沒有沿用其capture hash假稱是新檔。逐條核對40索引的old_text，全部與實際EN檔相符，39個非null字元數亦與實際文字一致。

以先前a62a來源snapshot機械比較2b689新來源，只改jw6i／ywu9／dkq3／6ybg／y64h／ywz8／mx7g七句：格→像素、自然更新林→自然更新的森林這一類、唯一最高→單獨最高等口語化。逐項讀過差異；數字、六類對應、唯一／並列、否定與問句均不變。本輪40候選使用新實際來源對照，未把正常語義相同的carry-forward當成新的事實錯誤。

### 五項建議修正

| ID | 候選問題 | 保義建議 | 建議字元／最新max |
| --- | --- | --- | --- |
| t4w3 | `mainly regrows`把「主要靠自然再生」過度壓成「主要長回」，自然形成的條件只剩類名暗示。定義宜把主要自然再生明說，保留secondary在此為secondary regrowth的含義。 | **Naturally regenerating forest: mostly natural regrowth; secondary included.** | 75／77。definition卡片語式；secondary接前面的regrowth，未新增第7類。若偏好完整secondary forest措辭，可保全文交真fit，勿硬刪自然成因。 |
| dkq3 | 刪naturally後，regenerating forest也可能泛指栽植林等長回來的森林；目前65字預算已能保留完整第2類名，沒有必要承擔這個歧義。 | **Of all 6, only naturally regenerating forest scores highest.** | 60／65；6與only都保留。 |
| ywz8 | 同上，第2類完整自然再生條件宜保留；最新71字時窗比原45字指引寬。 | **So it gets the naturally regenerating forest color too.** | 55／71；所以、也與本格套色均保留。 |
| 5ur9 | `Read 2 cells.`過度像無指涉的命令，丟掉「這兩格」的具體銜接；可用更順的本週介紹＋讀這兩格。 | **DeepMind showed ForTy this week. Read these 2 cells.** | 52／52；showed指官方本週介紹，不宣稱2020資料首次推出。 |
| sbkg | `After both green cells, are scores directly chances…`句法生硬；宜保留可否直接解讀的問句，而非把score／chance硬接為同一個名詞述語。 | **After 2 green cells, can scores directly mean chances of being right?** | 69／71；兩個綠格、其後討論、directly與正確機率都保留。 |

以上是作者／root可正常放入worksheet的候選；未直接代其merge。glossary_aliases不是獨立保義證據：尤其第2類natural這個區分，在新預算足夠時應保留。

### 4w7g完整環境問句：維持unresolved，不merge null

final檔此項text=null、action=unresolved_do_not_merge，是正確的保護動作。最佳完整候選：

> **What environments do you usually view on maps?**

46字／actual max25。保留環境類型、平常／常用、地圖三個概念；不是問哪張圖或只問任何地圖內容。`What do you view on maps?`會刪掉環境範圍，不採。可以保留current全文或此46字保義候選，交outro共享視窗原生fit。此處沒有聲稱單句25字內已找到同樣自然完整的短句，也沒有自行調速或搬秒數。

### 另兩項修正可採，其他metadata不重套

- **8m2e**：`To treat scores as chances of being right, use independent reference data; compare scores with real outcomes.` 為109／111，明確比較的是scores與真實結果，不是把references這個最近的複數代詞誤接到them；沒有聲稱已校準或已查真值。
- **ncx4**：`That introduction also shared an early-release annual series for 2017–2025.` 為75／最新77。early-release明確是早期公開版，年份與年度序列保留，不把它說成只包含歷史較早年份。
- **w86h**：58／64，最大分數的類別→紅框格轉綠，語義可採，與40索引同一項不重複加總。
- EN／JA description、EN first-grid章名與thumbnail是root已採metadata事項，仍不屬本輪重套範圍。

### 其餘候選：數字／否定／步驟核對

10×10與紅框只標一格、native species／visible disturbance、OtherLand可含城市樹木及稀疏木本、AlphaEarth多年觀測、10m輸出而非逐樹定位、固定欄名、排除nodata、第6類用250減其他5值總和、刻意挑最低最高分與非隨機全圖精度樣本、0.004加到1且另兩類0、單色／first-maximum本地規則、模型分數vs實際accuracy、尚未post-hoc calibration、土地歷史／用途要對參考、2020／五月／本版本輸出範圍均保留。未見新增數字錯誤或否定反轉。

`appe`的chosen for the lowest maximum score仍明確是目的性選樣，與後句非random說明一致；`ww8v`的top class在最高score的既有語境中可讀為最高分分類，未把它當土地品質或類別ID大小。這些縮法是本片局部回呼，不作官方新類名。

兩個可選清晰度改善，不另外列must-fix：

- beg8可用`Reading practice, not random sampling for overall map accuracy`（62／64），明講overall／整圖；現候選的map accuracy在語境中仍指地圖整體表現。
- e826可用`5 values are valid; derive other land's value, then compare 6 classes.`（70／71），明說補的是值；現候選可依數值語境理解，不宣稱填造實際土地。

### JA先行結論如何適用新版

JA18候選先前17可採＋ci5j需保留必要性的結論不變；ncx4 early-release修法可採。當前JA檔ci5j保留完整原句`参照データと照合する必要があります`，本來就有必要性；**有問題的是42字縮句候選，不是這份current全文**。合併時採先行報告45字保義句，或保留current全文交真fit，不要用省掉必要性的候選覆蓋。當前ncx4字幕仍是初期の年次系列，root可正常採38字早期公開版修法。

所有本輪數據／字元比較取自實際current sheet。沒有把root提供的92句音檢／總時長當作本查核者親聽或外語合成fit證據。本輪未TTS、未改譯文、未清任何flags。

## EN40完整逐項表（final）
| ID | Current zh-TW source | Frozen EN candidate | Chars / actual max | Independent verdict |
| --- | --- | --- | --- | --- |
| 7732 | 指定格周圍取十乘十格，紅框只標出我們要算的那一格。 | Take 10×10 cells around the target; red marks just the cell we'll calculate. | 76 / 76 | ACCEPT meaning only; actual native dub fit still required |
| jw6i | 另一個像素同樣是綠色，讀出的結果也會一樣嗎？ | Another cell is green too. Will it give the same results? | 57 / 70 | ACCEPT meaning only; actual native dub fit still required |
| 5ur9 | 本週DeepMind介紹ForTy，就從這兩格讀起。 | DeepMind introduced ForTy this week. Read 2 cells. | 50 / 52 | REVISE; exact meaning-preserving candidate above |
| m2p6 | 這個綠格要讀的不只有樹，還有它們如何長成、用來做什麼。 | Read not just the trees in this green cell, but how they grew and their use. | 76 / 89 | ACCEPT meaning only; actual native dub fit still required |
| erqz | 先看原始林，它要求原生樹種，沒有可見人為干擾。 | Primary forest: native tree species, no visible human disturbance. | 66 / 71 | ACCEPT meaning only; actual native dub fit still required |
| t4w3 | 自然更新林則以自然長回來為主，也含恢復中的次生林。 | Naturally regenerating forest mainly regrows, including secondary regrowth. | 75 / 77 | REVISE; exact meaning-preserving candidate above |
| rrgq | 剩下的其他土地，也可能包括城市樹木或稀疏木本。 | Lastly, other land may include urban trees or sparse woody plants. | 66 / 73 | ACCEPT meaning only; actual native dub fit still required |
| 9wmz | AlphaEarth先把多年衛星觀測整理成一組數字。 | AlphaEarth first turns years of satellite readings into numbers. | 64 / 64 | ACCEPT meaning only; actual native dub fit still required |
| jkby | ForTy使用這些數字，辨認種植形狀、季節和生長週期的線索。 | ForTy uses them for clues to planting patterns, seasons and growth cycles. | 74 / 83 | ACCEPT meaning only; actual native dub fit still required |
| p2ry | 要找對這五個值，得先確認資料年份和位置。 | Find the right 5 values: first check data year and place. | 57 / 60 | ACCEPT meaning only; actual native dub fit still required |
| yi97 | 十公尺網格是輸出尺度，不是每棵樹的定位清單。 | 10 m is the output grid scale, not a list of tree locations. | 60 / 67 | ACCEPT meaning only; actual native dub fit still required |
| 2k27 | 讀值時把固定類別名放在旁邊，數字就不會換到其他類。 | Keep fixed class names beside values so numbers stay with their class. | 70 / 72 | ACCEPT meaning only; actual native dub fit still required |
| gfes | 遇到無資料記號就先排除那一格，不把它當成分數。 | Exclude any no-data cell; don't count its marker as a score. | 60 / 64 | ACCEPT meaning only; actual native dub fit still required |
| e826 | 這一格的五個值都有效，可以補出其他土地，然後比較六類。 | All 5 values are valid; derive other land and compare all 6 classes. | 68 / 71 | ACCEPT meaning only; actual native dub fit still required |
| svhy | 欄位名稱要跟著值走，單看一串數字分不出是哪一類。 | Keep field names with values; numbers alone don't identify a class. | 67 / 67 | ACCEPT meaning only; actual native dub fit still required |
| 3gwz | 開頭少掉的第六類，要怎麼補回這張表？ | How do we fill the opening's class-6 gap here? | 46 / 47 | ACCEPT meaning only; actual native dub fit still required |
| 7iv8 | 第六類留在總量裡，用兩百五十扣回來。 | Class 6 is 250 minus the other 5 values' sum. | 45 / 49 | ACCEPT meaning only; actual native dub fit still required |
| dkq3 | 比較這六項，只有自然更新的森林這一類，分數最高。 | Of all 6, only regenerating forest scores highest. | 50 / 65 | REVISE; exact meaning-preserving candidate above |
| w86h | 選最大值來畫分類，紅框格就呈現它的綠色。 | Use the top-scoring class; the red-boxed cell turns green. | 58 / 64 | ACCEPT meaning only; actual native dub fit still required |
| xxju | 只看綠格能讀類名，展開數值才知道這格的分布。 | Green gives a class name; values reveal its score distribution. | 63 / 74 | ACCEPT meaning only; actual native dub fit still required |
| appe | 換到同一區塊的另一格，這次刻意挑最高分最低的位置。 | Now another cell in this block, chosen for the lowest maximum score. | 68 / 80 | ACCEPT meaning only; actual native dub fit still required |
| beg8 | 這是閱讀練習，不是拿隨機樣本估整張圖的精度。 | Reading practice, not random sampling to assess map accuracy. | 61 / 64 | ACCEPT meaning only; actual native dub fit still required |
| y64h | 原始森林和人工栽植的森林，分數都等於零。 | Primary forest and planted forest are 0. | 40 / 61 | ACCEPT meaning only; actual native dub fit still required |
| n37p | 最後加零點零零四，剛好是一，另外兩類的零不改變總和。 | Last, add 0.004 for exactly 1; the other 2 classes' zeros leave it unchanged. | 77 / 81 | ACCEPT meaning only; actual native dub fit still required |
| ecb8 | 總和不對，就檢查漏項和小數位，類別名稱仍要逐項對回。 | Wrong sum? Check missed terms and decimal places; match each class name. | 72 / 78 | ACCEPT meaning only; actual native dub fit still required |
| 8k4a | 如果只能塗一種顏色，畫面會選哪一個？ | If only one color is shown, which class is chosen? | 50 / 51 | ACCEPT meaning only; actual native dub fit still required |
| wnrz | 我們這張衍生圖，用類別順序取第一個最高者。 | Our map picks the first top-scoring class in class order. | 57 / 63 | ACCEPT meaning only; actual native dub fit still required |
| ywz8 | 所以這個像素，也塗成自然更新的森林這一類的顏色。 | So it gets the regenerating forest color too. | 45 / 71 | REVISE; exact meaning-preserving candidate above |
| ww8v | 還記得開頭那個綠格嗎，它的最高者只有一個。 | Remember the first green cell: just one top class | 49 / 49 | ACCEPT meaning only; actual native dub fit still required |
| mx7g | 把這兩個像素擺在一起，同樣的顏色就不再是同樣的資訊。 | Put both side by side: same color, different information. | 57 / 69 | ACCEPT meaning only; actual native dub fit still required |
| hbci | 需要比較結果時，就讀這條註記，而不是讓顏色替你省略答案。 | To compare results, read the note; don't let color hide the answer. | 67 / 79 | ACCEPT meaning only; actual native dub fit still required |
| sbkg | 兩個綠格讀完後，這些分數能不能直接當作正確機率？ | After both green cells, are scores directly chances of being right? | 67 / 71 | REVISE; exact meaning-preserving candidate above |
| upmh | 要用這些分數，得先分清模型分數和實際正確率。 | To use scores, first separate model scores from real accuracy. | 62 / 68 | ACCEPT meaning only; actual native dub fit still required |
| vb62 | 它是模型分數，還沒有做事後的機率校準。 | These scores lack post-hoc probability calibration. | 51 / 55 | ACCEPT meaning only; actual native dub fit still required |
| ci5j | 模型看見的是觀測線索，土地歷史和經營用途還要對照參考資料。 | The model sees clues; check land history and management use against reference data. | 83 / 87 | ACCEPT meaning only; actual native dub fit still required |
| 6ss6 | 分數讀清楚後，再替同一列紀錄保留位置和資料年。 | Once scores are clear, keep location and data year in the same row. | 67 / 73 | ACCEPT meaning only; actual native dub fit still required |
| rume | 二〇二〇基準資料在五月公開，描述的是那一年的土地狀態。 | Released in May, the baseline describes land conditions in 2020. | 64 / 75 | ACCEPT meaning only; actual native dub fit still required |
| 88pk | 同樣地，二〇二〇的兩格，只能回答這個版本的輸出長什麼樣。 | These two 2020 cells only show what this version's output looks like. | 69 / 78 | ACCEPT meaning only; actual native dub fit still required |
| hr4b | 這一列紀錄，就保住了單一綠色省略的資訊。 | This row keeps what a single green color leaves out. | 52 / 56 | ACCEPT meaning only; actual native dub fit still required |
| 4w7g | 你常用地圖看哪種環境？ | What environments do you usually view on maps? | 46 / 25 | KEEP_FULL_UNRESOLVED; no null merge; environment/maps/habit retained for actual outro fit |

Final EN table totals: 40 indexed entries = 34 meaning-acceptable, 5 recommended revisions, 1 full environment question with unresolved single-line guideline. Extra8m2e/ncx4 fixes accepted; w86h counted once. JA findings above remain separately version-bound. No all-passed/native-fit claim is made.
