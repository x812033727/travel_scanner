# ForTy R1 新稿：targeted 事實與metadata複核

查核日期：2026-10-25（Asia/Taipei）。本次是原查核者 news_verify 對編輯修訂稿的定向複核，另由 guard_review 獨立重驗metadata實際輸出；不是宣稱換了另一位完整首輪查核者。依root委派，只寫本收據，不改稿、不動音訊或生產狀態。

**結論：PASS（本次指定新稿的事實、算式、圖卡對應與發布metadata）。0未解must-fix、0 NOT FOUND、0本輪正文事實改動。** 這不代表旁白、字幕、節奏、成片或發布關卡通過。

## 綁定版本與範圍

- video.json SHA-256：`17011f955301898df35f8387c67df4929ecd3620b7db5b343d4d660f418f3387`
- claims.md SHA-256：`b5f43cc78a28da2f68c51945d2b9e7bf23012a5d19b8d0f6b6ba661f73b0c5f9`
- 原 verify-1.md SHA-256：`5bc134669e77a972707bc5782df7e7aa53bcc015f196264f0257edb2c6403f10`。舊稿REVISE原封保留，沒有把原收據升格或拿來綁新稿。
- 本次82場、85句、7章；85條claims與實際文字／line ID／scene ID完全對應。無say分歧，無超過40字句。
- 重讀全部85句與實際scene.data、檢查全部metadata，重核變更與刪除影響；並非只抽查已改句。`forty-script-r1.json`有34條變更紀錄，其中33條文字確實改寫，7iv8文字未變而移序；另刪14場15句。52句文字未改者也全部回讀，超過最低抽查三分之一。

## 舊稿R1-M1已解：實際上架說明有完整署名

本輪唯讀實際執行原生 `composeDescription`，不是只看JSON欄位：

```js
composeDescription({
  body: doc.youtube.description,
  timeline: estimateTimeline(doc),
  article: null,
  sources: doc.sources,
  assets: doc.assets,
  locale: 'zh-TW',
  tags: doc.youtube.tags,
  category: doc.category,
  campaign: doc.slug
})
```

獨立重得 **2561 UTF-8 bytes、7章、5條圖片credits，checkYoutubeFields=[]**。五asset均有author/url，五路徑各異，符合creditedAssets實際選取條件；每條輸出credit都有Neumann等（2026）、Forest Typology 2020 (v1)、CC BY4.0、改作及完整DOI。說明正文另有可點授權連結 `https://creativecommons.org/licenses/by/4.0/`、DOI `https://doi.org/10.25452/figshare.plus.32288616.v1`、完整題名／作者／版本與改作。這些文字確實進入合成說明，不只留在內部assets欄位。

2561 bytes包含估時七章；未帶timeline時是2295 bytes，兩者差異是參數，不是彼此矛盾。最終音訊產出後章節時戳仍須按實際timeline重做；本輪沒有音訊，未把估時當實測。所有外語metadata仍應保留來源、license URL與改作歸屬，需各自後續核對。

## 定向事實複核結論

| 項目 | 實際位置 | 本輪結果與依據 |
| --- | --- | --- |
| 本次真實讀格行動 | first-grid/8aw6 | CONFIRMED。確實取回官方2020 COG、裁切並計算A格；是本次製作工作，不是假造私人現地或長期林業經驗。SVG明列公開模型輸出／本片裁切計算。 |
| 三個開場問題 | gngj/ep85/jw6i | CONFIRMED。六類五band、A儲存值248、兩格本地同色皆有真實資料依據；問句沒有另宣稱新測量。第六類於7iv8/3p97回收，248單位於anxa/ywu9解答，同色差別於B並列及mx7g解答。 |
| 新聞日期仍正確 | one-promise/5ur9及data.kicker | CONFIRMED。口播本週，畫面保留DeepMind 2026-10-22介紹；查核日10/25仍屬本週。後段繼續分開五月基準、10/21論文、10/22早期年度消息。未把2020圖說成這週才首次公開。 |
| 原始／自然更新兩類 | erqz/t4w3與表格 | CONFIRMED。原生、無可見人為干擾和自然再生／恢復次生林仍在；刪除重述「不代表從未干擾」不等於把兩類混為一類。 |
| 第3／4類及40年proxy | 3pse/v9fh/7id9/2vcb/ci5j | CONFIRMED。第3類栽植／播種及本資料輪伐>40仍完整；第4類集約、少數樹種、同齡、規則間距、≤40仍完整。v9fh保留輪伐安排與當前樹齡不同，ci5j保留土地歷史／用途須另有參考，未將操作門檻改成衛星直接知道經營計畫。 |
| 第5／6類 | yiya/rrgq與表格 | CONFIRMED。第5類油棕／橡膠／果園、非木材農產品已合併在一句；第6類含城市樹木／稀疏木本仍在，沒有改成裸地。 |
| AlphaEarth與訓練 | 9wmz/jkby/5nt9 | CONFIRMED。多年觀測整理成數字是向量表示的白話化；畫面仍明列重要輸入之一。ForTy利用表示中的形狀／季節／生長線索與參考標註，依官方blog；未冒稱AlphaEarth的表示就是輸出檔五個類別整數或本次重訓。 |
| 年份／位置／有效值 | p2ry/u5js/7732/yi97/vk36/gfes/e826 | CONFIRMED。A請求座標121.4E/24.7N、指定格十乘十窗口與名目10m輸出仍正確。vk36六類完整儲存值合250、255另作nodata成立；gfes排除無資料，未把255帶入補數。 |
| A完整實算 | bxdi/anxa/up9r/3p97/4av2/ywu9/u362/eym7/k3i2/dkq3 | CONFIRMED。五值完整口述，248對第2類、其餘四類零；和248、補數2、248÷250=.992、2÷250=.008、其餘四分數0、合1且第2類唯一最高。去除完整六原始整數重唸未刪去任何非零結果或必要步驟。 |
| B完整實算 | 54sx/mfsh/578j/97h6/8mtz/4amm/ux8j/y64h | CONFIRMED。五值[0,86,0,1,77]，第2／4／5類非零對應正確、總和164、Other86；兩個86並列後共同除250=.344，1÷250=.004、77÷250=.308、另兩類0。六類分數仍完整，無漏掉第二個最高者。 |
| 並列與本地顯示 | appe/beg8/wnrz/ywz8/7qfx | CONFIRMED。B仍先揭露同區塊刻意挑低最大分數、非隨機精度抽樣；本圖取第一個最大者，沒有假借官方硬分類tie規則。新b-scale改用原有B完整分數SVG，位置在97h6明說並列之後。 |
| 先校準後年份 | sbkg/upmh/vb62/8m2e/bs4s/ci5j | CONFIRMED。移序沒有改變來源限制：未事後校準、需獨立參考、.992不能直接當99.2%單格判對機率。無accuracy/F1新數字，也無自稱已完成校準。 |
| 年度與2020範圍 | rume/pvkj/ncx4/j5kv/nqyj/88pk | CONFIRMED。五月基準公開，10/21是論文出版metadata，2017–2025早期序列另分；A/B仍只代表2020版本模型輸出。資料年／位置／六分數比較是編輯方法，沒有新年度像素結果或地面變化宣稱。Nature仍僅metadata/abstract，未宣稱讀過全文。 |
| 完整像素紀錄與CTA | bu6j/hr4b/4w7g/39nc | CONFIRMED／純CTA不作實測。保留年份、位置、六分數、所有最高者是本例可支持的紀錄方法；沒有承諾不存在的下載、文章或站內頁。 |
| 新標題／說明／縮圖 | youtube/thumbnail | CONFIRMED。「兩個台灣像素，算出六類結果」指每像素六分數，沒有宣稱兩格實際包含六種已確認土地。說明明列OtherLand、2020／early年度分界、B刻意選樣、無衛星底圖。縮圖五值→六類結果仍對應實作。 |
| 五張SVG | assets與各diagram | CONFIRMED。SHA全部與前輪及manifest相同，A/B數值、類別順序、長條比例、B並列／本地取首、座標、正northing顯示方向、[5,5]紅框及署名維持正確；新稿無實地面積或相鄰像素宣稱。 |

## 本輪重算輸入與結果

直接重讀本片data兩份完整原始數組，取[5,5]，用有號整數重算，沒有只信作者變更摘要：

| | A | B |
| --- | --- | --- |
| 五儲存值 | [0,248,0,0,0] | [0,86,0,1,77] |
| 五值和／Other | 248／2 | 164／86 |
| 完整六值 | [0,248,0,0,0,2] | [0,86,0,1,77,86] |
| 六分數 | [0,.992,0,0,0,.008] | [0,.344,0,.004,.308,.344] |
| 全部最高者 | [2] | [2,6] |
| 本圖顯示 | 2 | 2，因明列的本地取首規則 |

兩份JSON仍綁A SHA `867aa186e25b6a59ea5dcf32a100646d68497fa064d177e674f2674f42a362ba`、B SHA `4ebd1c412fe85576277d0b8c4ab96fce31254abe41b6c07ba3ca203220db101a`。模型score仍未事後校準；它們不是本地量出的accuracy或土地真值。

## Primary來源與本輪界線

沿用並重讀2026-10-25已取得官方原文及來源欄位，未新增需要全文才能證明的論文方法或精度數字：

- B：https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/ （HTTP200原文；日期／early序列／AlphaEarth／訓練線索）
- C：https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection （HTTP200原文；六類／40年proxy／尺度／未校準限制）
- F：https://api.figshare.com/v2/articles/32288616 （HTTP200 API；五月發布／五band／補數／除法／CCBY及DOI）
- N：https://www.nature.com/articles/s41597-026-08299-5 （只採官方出版metadata／abstract；直接頁驗證轉址，沒有全文HTTP200或全文已讀宣稱）
- G：https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif （前輪本日獨立206 Range解碼與本輪固定SHA原始JSON重算；沒有重抓整圖）
- L：https://creativecommons.org/licenses/by/4.0/ （前輪本日HTTP200；本輪修訂保留確切license URL）

## 原生檢查與尚未執行項目

實際執行 `node tools/video/cli.mjs lint --slug forty-forest-map --json`，cwd為本worktree，exit0、errors0、warnings5。警告為約25秒首章及完整算式中248／250／86／77的四個重複數字heuristic；不是未解事實錯誤。原標題heuristic已不再出現。

工具估1760 spoken units、507.2秒、8.4533分鐘，七章估時00:00／00:24／02:07／03:07／04:53／06:44／08:14。此為文字估時；本輪沒有TTS、音訊實測、音檢、字幕翻譯、媒體render或成片QA。事實PASS不能替代這些關卡。

沒有新must-fix或需要直接修改的事實；未觸發「超過3個事實改動再找另一位查核者」規則。新稿只按本收據的新SHA通過定向事實／metadata複核，原稿R1收據仍為REVISE。

## 34條變更紀錄逐項核對

以下由凍結變更紀錄與新稿實際文字逐一比對；7iv8只移序不改字，其餘33項改寫皆與原始來源／本輪重算相符。Before/After保留編輯修訂原文，本查核者未直接改稿。

| # | Scene / line | Before | After in frozen R1 | Verdict / evidence |
| --- | --- | --- | --- | --- |
| 1 | first-grid / 8aw6 | 本週十月二十二日，DeepMind介紹了ForTy森林地圖。 | 我從ForTy公開資料取出這個綠格，試著把顏色讀成紀錄。 | CONFIRMED; G + original A/B JSON re-read; local calculation / editorial question grounded in actual outputs |
| 2 | first-label / gngj | 這個二〇二〇年資料的格子，被塗成自然更新林。 | 地圖分六類，為什麼只存五個值？ | CONFIRMED; F official API200 + fixed source metadata; six classes / five bands / 250 total / 255 nodata |
| 3 | viewer-question / ep85 | 你可能會問：有樹，不就好了？ | 裡面的兩百四十八，到底是什麼單位？ | CONFIRMED; Original editorial instruction / transition; no new measured or official capability claim |
| 4 | read-more / jw6i | 讀類名、補分數，才看得到顏色沒寫完的資訊。 | 另一格同樣綠，讀出的結果也會一樣嗎？ | CONFIRMED; G + original A/B JSON re-read; local calculation / editorial question grounded in actual outputs |
| 5 | one-promise / 5ur9 | 跟著兩個真實格子，把五個值還原成六類結果。 | 本週DeepMind介紹ForTy，就從這兩格讀起。 | CONFIRMED; B official HTTP200 snapshot; announcement / model input / early annual series |
| 6 | label-meaning / m2p6 | 開頭那個自然更新林，描述的是森林怎麼形成。 | 這個綠格要讀的不只有樹，還有它們如何長成、用來做什麼。 | CONFIRMED; C official HTTP200 snapshot; preserved class definitions and operating conditions |
| 7 | planted-origin / 3pse | 人工栽植林主要由栽植或播種形成。 | 人工栽植林主要靠栽植或播種，這份資料的輪伐期條件是超過四十年。 | CONFIRMED; C official HTTP200 snapshot; preserved class definitions and operating conditions |
| 8 | tree-crop-definition / yiya | 至於油棕、橡膠和果園，會進到樹木作物與農林複合。 | 樹木作物與農林複合，包含油棕、橡膠、果園，生產的是非木材農產品。 | CONFIRMED; C official HTTP200 snapshot; preserved class definitions and operating conditions |
| 9 | keep-order / fbc5 | 把這六個名稱固定下來，後面每個數都要依序對回去。 | 這六類各有固定位置，讀數值時要連著名稱一起看。 | CONFIRMED; Original editorial instruction / transition; no new measured or official capability claim |
| 10 | alphaearth-input / 9wmz | 模型的重要輸入之一，是AlphaEarth把多年衛星觀測濃縮成的表示。 | AlphaEarth先把多年衛星觀測整理成一組數字。 | CONFIRMED; B official HTTP200 snapshot; announcement / model input / early annual series |
| 11 | signal-chain / jkby | ForTy再利用這些表示，找種植形狀、季節和生長週期的線索。 | ForTy使用這些數字，辨認種植形狀、季節和生長週期的線索。 | CONFIRMED; B official HTTP200 snapshot; announcement / model input / early annual series |
| 12 | stored-question / m8cb | 我們手上這個格子的分數，就藏在五個整數裡。 | 這個綠格的五個整數，就裝著這些類別的模型分數。 | CONFIRMED; G + original A/B JSON re-read; local calculation / editorial question grounded in actual outputs |
| 13 | pixel-record / p2ry | 先在這份像素紀錄填上資料年份和位置。 | 要找對這五個值，得先確認資料年份和位置。 | CONFIRMED; G + original A/B JSON re-read; local calculation / editorial question grounded in actual outputs |
| 14 | band-order / 2k27 | 讀值之前，把前五類的順序固定在這張表上。 | 讀值時把固定類別名放在旁邊，數字就不會換到其他類。 | CONFIRMED; Original editorial instruction / transition; no new measured or official capability claim |
| 15 | valid-or-missing / vk36 | 零是有效分數的儲存值，兩百五十五才是無資料記號。 | 六類的值合計兩百五十，兩百五十五另作無資料記號。 | CONFIRMED; F official API200 + fixed source metadata; six classes / five bands / 250 total / 255 nodata |
| 16 | missing-action / gfes | 遇到無資料就先停下，不把它拿進補數計算。 | 遇到無資料記號就先排除那一格，不把它當成分數。 | CONFIRMED; Original editorial instruction / transition; no new measured or official capability claim |
| 17 | a-valid / e826 | 這一格的五個值都有資料，也都在有效範圍內，可以繼續補第六類。 | 這一格的五個值都有效，可以補出其他土地，然後比較六類。 | CONFIRMED; G + original A/B JSON re-read; local calculation / editorial question grounded in actual outputs |
| 18 | sixth-value-question / 3gwz | 可是表上有六類，這裡為什麼只存五個值？ | 開頭少掉的第六類，要怎麼補回這張表？ | CONFIRMED; Original editorial instruction / transition; no new measured or official capability claim |
| 19 | residual-rule / 7iv8 | 第六類留在總量裡，用兩百五十扣回來。 | 第六類留在總量裡，用兩百五十扣回來。 | CONFIRMED (movement only); F official API200 + fixed source metadata; six classes / five bands / 250 total / 255 nodata |
| 20 | a-five-input / bxdi | 依序讀到零、兩百四十八、零、零、零。 | 這格五個值依序是零、兩百四十八、零、零、零。 | CONFIRMED; G + original A/B JSON re-read; local calculation / editorial question grounded in actual outputs |
| 21 | stored-value-meaning / anxa | 數值越大，表示這類得到的模型分數越高；它們不是面積或樹木的棵數。 | 兩百四十八是縮放儲存的分數值，不是樹木棵數，也不是平方公尺。 | CONFIRMED; G + original A/B JSON re-read; local calculation / editorial question grounded in actual outputs |
| 22 | a-sum / up9r | 先把這格的五個值相加，總和是兩百四十八。 | 其中兩百四十八是自然更新林，其餘四類為零，總和就是兩百四十八。 | CONFIRMED; G + original A/B JSON re-read; local calculation / editorial question grounded in actual outputs |
| 23 | a-zero-scores / eym7 | 原始林、人工栽植林、林木種植園和樹作類，這格都是零。 | 其餘四類的儲存值是零，換成分數也都是零。 | CONFIRMED; G + original A/B JSON re-read; local calculation / editorial question grounded in actual outputs |
| 24 | b-five-input / 54sx | 沿用相同類別順序，五值是零、八十六、零、一、七十七。 | 五個值依序是零、八十六、零、一、七十七。 | CONFIRMED; G + original A/B JSON re-read; local calculation / editorial question grounded in actual outputs |
| 25 | b-sum / mfsh | 八十六加一再加七十七，總和是一百六十四。 | 自然更新林八十六、林木種植園一、樹作七十七，合計一百六十四。 | CONFIRMED; G + original A/B JSON re-read; local calculation / editorial question grounded in actual outputs |
| 26 | b-regeneration-score / 97h6 | 自然更新林的八十六，變成零點三四四。 | 自然更新林和其他土地同為八十六，這次有兩項並列最高。 | CONFIRMED; G + original A/B JSON re-read; local calculation / editorial question grounded in actual outputs |
| 27 | b-scale / 8mtz | 每一項除以兩百五十，現在把各類攤開來讀。 | 兩項都除以兩百五十，得到相同的零點三四四。 | CONFIRMED; G + original A/B JSON re-read; local calculation / editorial question grounded in actual outputs |
| 28 | annual-forward / sbkg | 那把這種讀法用到新年度，資料年又該放在哪裡？ | 兩個綠格讀完後，這些分數能不能直接當作正確機率？ | CONFIRMED; C official HTTP200 calibration limitation; editorial question / transition |
| 29 | score-question / upmh | 這裡還有一個容易誤讀的地方：零點九九二，究竟代表什麼？ | 要用這些分數，得先分清模型分數和實際正確率。 | CONFIRMED; C official HTTP200 calibration limitation; editorial question / transition |
| 30 | year-in-record / 6ss6 | 把年份放進每一列紀錄，你才有辦法接上新的年度資料。 | 分數讀清楚後，再替同一列紀錄保留位置和資料年。 | CONFIRMED; Original editorial instruction / transition; no new measured or official capability claim |
| 31 | baseline-release / rume | 二〇二〇基準資料在五月就已公開，不能把它當成本週才出現。 | 二〇二〇基準資料在五月公開，描述的是那一年的土地狀態。 | CONFIRMED; F official API200: published May 2026; 2020 remains data year |
| 32 | annual-release / ncx4 | 開頭那次介紹，另外分享二〇一七到二〇二五年的早期年度序列。 | 那次介紹也分享二〇一七到二〇二五年的早期年度序列。 | CONFIRMED; B official HTTP200 snapshot; announcement / model input / early annual series |
| 33 | annual-next-input / bu6j | 想追年度變化，就把對應年份的輸出和獨立參考一起帶進來。 | 把年份、位置、六個分數和所有最高者，寫進同一列像素紀錄。 | CONFIRMED; Original editorial instruction / transition; no new measured or official capability claim |
| 34 | complete-pixel-record / hr4b | 還記得那個綠格，六個分數才把它讀完整。 | 這一列紀錄，就保住了單一綠色省略的資訊。 | CONFIRMED; Original editorial instruction / transition; no new measured or official capability claim |

## Deleted-line preservation check

| Deleted ID | Fact / function retained in the new script | Verdict |
| --- | --- | --- |
| mu7d | Editorial general-map observation removed; all actual A/B evidence and class distinction retained. | CONFIRMED; no necessary factual condition lost |
| pwc4 | Formation / use comparison retained in m2p6 and six class definitions. | CONFIRMED; no necessary factual condition lost |
| zpjv | Natural regeneration includes recovering secondary forest in t4w3; no assertion of never disturbed history. | CONFIRMED; no necessary factual condition lost |
| njnw | Class3 >40-year condition merged into 3pse and table. | CONFIRMED; no necessary factual condition lost |
| 3x99 | Rotation cycle versus present tree age remains explicit in v9fh. | CONFIRMED; no necessary factual condition lost |
| sd2k | Non-wood commodity meaning merged into yiya and table. | CONFIRMED; no necessary factual condition lost |
| icp9 | OtherLand still includes urban trees / sparse woody cover in rrgq and table. | CONFIRMED; no necessary factual condition lost |
| 528p | Model class-score meaning retained in m8cb and subsequent real-score calculations. | CONFIRMED; no necessary factual condition lost |
| us3c | Fixed band order retained in 2k27 and full table; original input vectors remain complete. | CONFIRMED; no necessary factual condition lost |
| 8qmt | Other residual remains explicit in 3p97; removing repetition does not remove derived value2. | CONFIRMED; no necessary factual condition lost |
| jd7t | Full A six raw integer repeat removed; five input values, residual2 and all six scores retained across bxdi/3p97/ywu9/u362/eym7. | CONFIRMED; no necessary factual condition lost |
| siyh | Full B six raw integer repeat removed; five inputs, residual86 and all six scores retained across 54sx/578j/97h6/8mtz/4amm/ux8j/y64h. | CONFIRMED; no necessary factual condition lost |
| mrsv | OtherLand86 and .344 now explicitly shared with class2 in 97h6 and 8mtz. | CONFIRMED; no necessary factual condition lost |
| jbsn | Two equal maxima now explicit earlier in 97h6, after B input and residual calculation. | CONFIRMED; no necessary factual condition lost |
| n6j6 | Class2/class6 equal score retained in 97h6,8mtz and complete score SVG; local tie rule remains wnrz. | CONFIRMED; no necessary factual condition lost |

## Unchanged-line full re-read register

All unchanged text was re-read, rather than only a random third. The following52 line IDs remain word-for-word equal to the original reviewed script; they were checked again with their current card data and position. The complete85-line/claim map was verified.

erqz, t4w3, 66nz, v9fh, 7id9, 2vcb, rrgq, gsa7, 5nt9, u5js, 7732, yi97, svhy, 7iv8, 3p97, 4av2, 8hpb, ywu9, u362, k3i2, p9sg, dkq3, w86h, wh49, 6ybg, xxju, endc, appe, beg8, 578j, 4amm, ux8j, y64h, 8k4a, z33x, wnrz, ywz8, ww8v, mx7g, 7qfx, hbci, vb62, 8m2e, bs4s, ci5j, pvkj, j5kv, nqyj, wfb2, 88pk, 4w7g, 39nc.

Final file bindings were rechecked at appendix generation; the old verify-1 hash is unchanged. No source, audio, flag, task-board, or production changes were made.
