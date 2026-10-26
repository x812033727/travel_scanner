# ForTy 正式稿：逐句主張與示範證據

確認日期：2026-10-25。這是本次video.json的撰稿證據對照，不是獨立事實審查或成片通過收據。brief已凍結，A採用紀錄見production-decision.md。

## 證據層級與來源界線

- CITED：source-facts.md的F01–F22與各primary URL。Nature僅出版metadata／abstract，未宣稱全文已讀。
- RUN-A／RUN-B：data/actual-roi-result.json、data/actual-uncertain-roi-result.json、data/independent-results.json及data-review.md。讀的是已公開2020模型輸出，不是重訓、地面真值或年度變化測試。
- ED：觀眾提問、從同一輸出展開的算術意義與操作選擇，並非公司新主張、實測新事件或站主私人經歷。公式值另綁RUN或CITED。
- 正式五張SVG均登記於video.assets，來源DOI10.25452/figshare.plus.32288616.v1、CC BY4.0；本片改作：裁切、Other補數、取首分類與圖表。原創圖無衛星底圖，不冒充App操作。

## 逐句主張

R1逐句對照實際video.json；保留所有現存line ID，刪除重述句並按新順序重編claim ID。前五原始值A/B各完整口述一次，補數與換算保留必要數字。問題與原創判讀不是新增量測。

c1｜我從二〇二〇年的台灣資料，取出這個ForTy綠格。｜RUN-A：本次2020公開資料取樣與像素紀錄｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜first-grid／8aw6
c2｜地圖分六類，為什麼只存五個值？｜CITED：六類與五儲存band，source-facts F15｜https://api.figshare.com/v2/articles/32288616｜2026-10-25｜first-label／gngj
c3｜裡面的兩百四十八，到底是什麼單位？｜ED：對真實A值248提問；非新增單位主張｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜viewer-question／ep85
c4｜另一個像素同樣是綠色，讀出的結果也會一樣嗎？｜RUN-A/B＋ED：兩指定格本地同色，問題停在完整結果前｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜read-more／jw6i
c5｜本週DeepMind介紹ForTy，就從這兩格讀起。｜CITED：2026-10-22研究介紹，source-facts F03｜https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/｜2026-10-25｜one-promise／5ur9
c6｜這個綠格要讀的不只有樹，還有它們如何長成、用來做什麼。｜ED：由六類定義展開其形成與用途意義｜https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection｜2026-10-25｜label-meaning／m2p6
c7｜先看原始林，它要求原生樹種，沒有可見人為干擾。｜CITED：source-facts.md F05｜https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection｜2026-10-25｜primary-definition／erqz
c8｜自然更新林則以自然長回來為主，也含恢復中的次生林。｜CITED：source-facts.md F06｜https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection｜2026-10-25｜regeneration-definition／t4w3
c9｜如果森林是人種的，又要怎麼放進這張表？｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection｜2026-10-25｜planted-question／66nz
c10｜人工栽植林主要靠栽植或播種，這份資料的輪伐期條件是超過四十年。｜CITED：source-facts.md F07｜https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection｜2026-10-25｜planted-origin／3pse
c11｜輪伐期說的是從種下、經營到再次採收的安排，和這棵樹現在幾歲不同。｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection｜2026-10-25｜rotation-meaning／v9fh
c12｜林木種植園的經營更密集，常有少數樹種、同齡和規則間距。｜CITED：source-facts.md F08｜https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection｜2026-10-25｜plantation-pattern／7id9
c13｜它採用的輪伐期條件，是四十年或以下。｜CITED：source-facts.md F08｜https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection｜2026-10-25｜plantation-cycle／2vcb
c14｜樹木作物與農林複合，包含油棕、橡膠、果園，生產的是非木材農產品。｜CITED：source-facts.md F09｜https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection｜2026-10-25｜tree-crop-definition／yiya
c15｜剩下的其他土地，也可能包括城市樹木或稀疏木本。｜CITED：source-facts.md F10｜https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection｜2026-10-25｜other-definition／rrgq
c16｜這六類各有固定位置，讀數值時要連著名稱一起看。｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection｜2026-10-25｜keep-order／fbc5
c17｜可是隔著衛星影像，模型能從哪裡讀出這些差別？｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection｜2026-10-25｜signal-question／gsa7
c18｜AlphaEarth先把多年衛星觀測整理成一組數字。｜CITED：source-facts.md F12｜https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/｜2026-10-25｜alphaearth-input／9wmz
c19｜ForTy使用這些數字，辨認種植形狀、季節和生長週期的線索。｜CITED：source-facts.md F12｜https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/｜2026-10-25｜signal-chain／jkby
c20｜訓練還要搭配專家與區域資料標記的地點，讓觀測線索對回土地類型。｜CITED：source-facts.md F13｜https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/｜2026-10-25｜training-reference／5nt9
c21｜這個綠格的五個整數，就裝著這些類別的模型分數。｜CITED：source-facts.md F15｜https://api.figshare.com/v2/articles/32288616｜2026-10-25｜stored-question／m8cb
c22｜要找對這五個值，得先確認資料年份和位置。｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜pixel-record／p2ry
c23｜位置用東經一百二十一點四、北緯二十四點七。｜RUN-A：本次2020指定像素、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜requested-coordinate／u5js
c24｜指定格周圍取十乘十格，紅框只標出我們要算的那一格。｜RUN-A：本次2020指定像素、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜a-window／7732
c25｜十公尺網格是輸出尺度，不是每棵樹的定位清單。｜CITED：source-facts.md F14｜https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection｜2026-10-25｜grid-scale／yi97
c26｜讀值時把固定類別名放在旁邊，數字就不會換到其他類。｜CITED：source-facts.md F15｜https://api.figshare.com/v2/articles/32288616｜2026-10-25｜band-order／2k27
c27｜六類的值合計兩百五十，兩百五十五另作無資料記號。｜RUN-A：本次2020指定像素、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜valid-or-missing／vk36
c28｜遇到無資料記號就先排除那一格，不把它當成分數。｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜missing-action／gfes
c29｜這一格的五個值都有效，可以補出其他土地，然後比較六類。｜RUN-A：本次2020指定像素、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜a-valid／e826
c30｜欄位名稱要跟著值走，單看一串數字分不出是哪一類。｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection｜2026-10-25｜keep-value-label／svhy
c31｜開頭少掉的第六類，要怎麼補回這張表？｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜sixth-value-question／3gwz
c32｜第六類留在總量裡，用兩百五十扣回來。｜CITED：source-facts.md F15｜https://api.figshare.com/v2/articles/32288616｜2026-10-25｜residual-rule／7iv8
c33｜這格五個值依序是零、兩百四十八、零、零、零。｜RUN-A：本次2020指定像素、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜a-five-input／bxdi
c34｜兩百四十八是縮放儲存的分數值，不是樹木棵數，也不是平方公尺。｜CITED F15＋ED：量化分數單位，非樹木數或面積｜https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection｜2026-10-25｜stored-value-meaning／anxa
c35｜其中兩百四十八是自然更新林，其餘四類為零，總和就是兩百四十八。｜RUN-A：本次2020指定像素、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜a-sum／up9r
c36｜兩百五十減兩百四十八，其他土地得到二。｜RUN-A：本次2020指定像素、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜a-other／3p97
c37｜補完後先檢查，六個值都要在零到兩百五十之間，總和也要回到兩百五十。｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜six-value-check／4av2
c38｜這些儲存值，要怎麼換成零到一的模型分數？｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜normalization-rule／8hpb
c39｜每一項都除以兩百五十；自然更新的森林這一類，兩百四十八就得到零點九九二。｜RUN-A：本次2020指定像素、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜a-regeneration-score／ywu9
c40｜其他土地的二，除完是零點零零八。｜RUN-A：本次2020指定像素、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜a-other-score／u362
c41｜其餘四類的儲存值是零，換成分數也都是零。｜RUN-A：本次2020指定像素、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜a-zero-scores／eym7
c42｜把六項分數加起來，剛好是一。｜RUN-A：本次2020指定像素、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜a-total／k3i2
c43｜這是同一個總量的拆分，不是六次互不相關的打分。｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜shared-total／p9sg
c44｜比較這六項，只有自然更新的森林這一類，分數最高。｜RUN-A：本次2020指定像素、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜a-unique／dkq3
c45｜選最大值來畫分類，紅框格就呈現它的綠色。｜RUN-A：本次2020指定像素、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜a-score-result／w86h
c46｜這個動作叫取最大值，選的是類別，不會留下所有分數。｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜argmax-action／wh49
c47｜所以紀錄上要寫，自然更新的森林這一類單獨最高，並附上完整六個分數。｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜a-annotation／6ybg
c48｜只看綠格能讀類名，展開數值才知道這格的分布。｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜a-simple-expanded／xxju
c49｜另一個同來源格子，也能這樣乾脆地選出來嗎？｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜b-forward／endc
c50｜換到同一區塊的另一格，這次刻意挑最高分最低的位置。｜RUN-B：刻意選低最大分數、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜b-selected-grid／appe
c51｜這是閱讀練習，不是拿隨機樣本估整張圖的精度。｜RUN-B：刻意選低最大分數、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜b-selection-purpose／beg8
c52｜五個值依序是零、八十六、零、一、七十七。｜RUN-B：刻意選低最大分數、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜b-five-input／54sx
c53｜自然更新林八十六、林木種植園一、樹作七十七，合計一百六十四。｜RUN-B：刻意選低最大分數、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜b-sum／mfsh
c54｜兩百五十減一百六十四，其他土地得到八十六。｜RUN-B：刻意選低最大分數、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜b-other／578j
c55｜自然更新林和其他土地同為八十六，這次有兩項並列最高。｜RUN-B：刻意選低最大分數、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜b-regeneration-score／97h6
c56｜兩項都除以兩百五十，得到相同的零點三四四。｜RUN-B：86÷250=.344，兩最高者相同；其餘分數見完整圖｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜b-scale／8mtz
c57｜林木種植園的一，變成零點零零四。｜RUN-B：刻意選低最大分數、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜b-plantation-score／4amm
c58｜樹木作物與農林複合的七十七，變成零點三零八。｜RUN-B：刻意選低最大分數、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜b-crop-score／ux8j
c59｜原始森林和人工栽植的森林，分數都等於零。｜RUN-B：刻意選低最大分數、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜b-zero-scores／y64h
c60｜如果只能塗一種顏色，畫面會選哪一個？｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜one-color-question／8k4a
c61｜只選一個顯示，是把六項分數壓成一個標籤；並列者不會因此自動分出高低。｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜label-compression／z33x
c62｜我們這張衍生圖，用類別順序取第一個最高者。｜RUN-B：刻意選低最大分數、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜local-tie-rule／wnrz
c63｜所以這個像素，也塗成自然更新的森林這一類的顏色。｜RUN-B：刻意選低最大分數、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜b-green-label／ywz8
c64｜還記得開頭那個綠格嗎，它的最高者只有一個。｜RUN-A：本次2020指定像素、公開資料與本地實算｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜a-b-comparison／ww8v
c65｜把這兩個像素擺在一起，同樣的顏色就不再是同樣的資訊。｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜a-b-comparison／mx7g
c66｜你的紀錄要留下自然更新林和其他土地並列，再註明取首顯示。｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜b-annotation／7qfx
c67｜需要比較結果時，就讀這條註記，而不是讓顏色替你省略答案。｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜use-annotation／hbci
c68｜兩個綠格讀完後，這些分數能不能直接當作正確機率？｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/｜2026-10-25｜annual-forward／sbkg
c69｜要用這些分數，得先分清模型分數和實際正確率。｜ED：對模型分數語義的操作判斷｜https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection｜2026-10-25｜score-question／upmh
c70｜它是模型分數，還沒有做事後的機率校準。｜CITED：source-facts.md F19｜https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection｜2026-10-25｜uncalibrated-score／vb62
c71｜要把分數當成正確機率，還得用獨立參考，檢查分數和真實結果是否相符。｜CITED：source-facts.md F19｜https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection｜2026-10-25｜calibration-reference／8m2e
c72｜所以不能直接說，這格有百分之九十九點二的機率判對。｜CITED：source-facts.md F19｜https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection｜2026-10-25｜not-correctness／bs4s
c73｜模型看見的是觀測線索，土地歷史和經營用途還要對照參考資料。｜CITED：source-facts.md F11｜https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_forest_typology_forest_typology_2020_v1_0_collection｜2026-10-25｜reference-needed／ci5j
c74｜分數讀清楚後，再替同一列紀錄保留位置和資料年。｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/｜2026-10-25｜year-in-record／6ss6
c75｜二〇二〇基準資料在五月公開，描述的是那一年的土地狀態。｜CITED：source-facts F01／F04，公開時間與基準年分開｜https://api.figshare.com/v2/articles/32288616｜2026-10-25｜baseline-release／rume
c76｜正式資料論文在十月二十一日出版。｜CITED：source-facts.md F02｜https://www.nature.com/articles/s41597-026-08299-5｜2026-10-25｜paper-date／pvkj
c77｜那次介紹也分享二〇一七到二〇二五年的早期年度序列。｜CITED：source-facts.md F03｜https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/｜2026-10-25｜annual-release／ncx4
c78｜一個位置可以多出不同年份的輸出，分類問題也能沿時間展開。｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/｜2026-10-25｜time-dimension／j5kv
c79｜要比較同一處，先固定位置，再保留每年的類別順序和六分數。｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/｜2026-10-25｜annual-reading-fields／nqyj
c80｜只換顏色，會把剛才看到的並列和分數差距藏起來。｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/｜2026-10-25｜color-change-reading／wfb2
c81｜同樣地，二〇二〇的兩格，只能回答這個版本的輸出長什麼樣。｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜baseline-scope／88pk
c82｜把年份、位置、六個分數和所有最高者，寫進同一列像素紀錄。｜ED：同一A/B輸出完成一列紀錄，非年度新量測｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜annual-next-input／bu6j
c83｜這一列紀錄，就保住了單一綠色省略的資訊。｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜complete-pixel-record／hr4b
c84｜你常用地圖看哪種環境？｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜complete-pixel-record／4w7g
c85｜訂閱，一起讀懂AI的真實輸出。｜ED：編輯提問／操作選擇／由本例展開的判讀；非新量測｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜complete-pixel-record／39nc
c86｜第二格的像素中心在東經一百二十一點四二二三四。｜RUN-B：指定像素中心longitude=121.42233836084972，四捨五入至小數5位；非窗口幾何中心｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜b-pixel-center／fe8z
c87｜北緯二十四點六九五二八，用這個位置對回紅框。｜RUN-B：指定像素中心latitude=24.695276083224126，四捨五入至小數5位；對回ROI指定格[5,5]｜https://storage.googleapis.com/nature-trace/export_rasters/forest_typology_2020_v1_0/raster_51R_20_1_4.tif｜2026-10-25｜b-pixel-center／ymf8

## 實算完整紀錄

### A：固定座標的六類輸出

- 輸入：請求121.4°E、24.7°N，source row4067／col2070；10×10窗口col2065／row4062，指定ROI像素[5,5]。此點是所選格心，不是偶數窗口精確幾何中心。
- 前提：官方前五類順序，儲存0–250；255為nodata。A五值均有效。資料名目10m輸出，非逐樹實地量測。
- 動作：讀[0,248,0,0,0]，有號整數加總248；Other=250−248=2；六值[0,248,0,0,0,2]各除250。
- 預期：完整六分數可重算，最大者與本地衍生標籤一致。
- 觀察：[0,.992,0,0,0,.008]，第2類自然更新林唯一最高。分數和1，並不表示經過機率校準。
- 證據：data/actual-roi-result.json與完整小TIF（scratch），獨立解碼與小檔重開一致。Agrid開場可見；A分數圖只在相應計算揭露後出現。
- 畫面：a-five-input、a-sum、a-other、a-regeneration-score、a-other-score、a-zero-scores、a-total、a-score-result、a-annotation。

### B：刻意挑出的不同結果

- 輸入：同一已讀512×512 block；排除五格邊界，252004候選中選六類最大分數最低者，兩處同最低時取row-major第一個。source row4012／col2295；ROI指定格[5,5]。不是隨機抽樣，不估全圖精度。
- 動作：讀[0,86,0,1,77]，加總164；Other=250−164=86；六值[0,86,0,1,77,86]各除250。
- 預期：完整六分數保留所有最大者；顯示時另依本片明列的取首規則。
- 觀察：[0,.344,0,.004,.308,.344]；第2及第6類並列最高，沒有唯一最高。本地NumPy first-maximum顯示第2類；未核對官方硬分類層的tie規則。
- 證據：data/actual-uncertain-roi-result.json及data/independent-results.json；所選格與全100格原值獨立吻合。B分數圖在並列揭曉後才出現；comparison在完整B結果之後。
- 畫面：b-five-input、b-sum、b-other、b-regeneration-score、b-scale、b-plantation-score、b-crop-score、b-zero-scores、local-tie-rule、b-annotation。

### 同輸入的簡單做法對照與應用

同一批A/B原值已產出分類格網與六分數。只讀本地取首色塊，兩指定格都呈第2類；完整分數使A唯一最高、B並列的差別可被保留。這不是另一組測試，也不主張一般聊天工具或計算機無法算術。觀眾完成的註記是A「第2類唯一最高」與B「第2／6類並列；本圖取首顯示第2類」。

### 實作時間、版本與來源

2026-10-25；Python3.12.14、rasterio1.5.2／GDAL3.12.2、NumPy2.5.4。公開COG generation1777582191968217，原始五band、小TIF、座標與完整收據在research-demo.md及scratch實作包。獨立73項PASS是資料審查，沒有拿它當作這份正文已過事實／敘事審查。

## 圖卡、metadata與授權的額外核對

- 六類英文名稱與ID按source-facts.md F05–F10；字卡可保留英文，口播用繁中。OtherLand含部分有樹土地，不能簡化成裸地。
- 40年為此資料的操作proxy；輪伐期不等於當前樹齡。圖卡所寫超過40年／40年或以下分別對應F07／F08。
- 前五儲存0–250與Other補數對F15；nodata255對原始COG與獨立資料審查。
- 2020為資料年；Figshare五月公開，正式論文2026-10-21，研究介紹2026-10-22與早期2017–2025序列，分別對F01／F02／F03。日期不補未提供時區。
- 數學符號、完整小數留字卡；旁白用中文數字完整讀出。未把.992／.344當實際正確率，未使用全域accuracy或類別F1填長度。
- YouTube說明欄的B刻意選樣、2020／年度界線與圖表改作都與本次資料一致；沒有新增第三個地點、法律建議、碳權主張或年度像素結果。
- 五張SVG來源：Neumann等(2026), Forest Typology2020(v1), https://doi.org/10.25452/figshare.plus.32288616.v1 ，CC BY4.0；各asset.source/license/author/url已寫入video.json；composeDescription將實際列出圖片來源，本文也保留可點DOI與CC BY4.0授權連結。

## 與企劃不同的地方

- 依root授權與首次盲讀的實質問題作R1：開場從本次讀取真實綠格的行動開始，不先唸類名或分數；三個具體疑問在正文回收，最後短接本週研究消息。仍小於30秒。
- 六類核心、40年操作proxy兩側、形成／用途與模型輸入均保留；壓縮重複提醒。A原始五值移到實算旁，非零值與類名當下對應，不要求跨章記憶欄位。
- A/B原始五值各完整唸一次；刪除完整六個原始整數的再次口述，保留補數、除法、非零分數及其餘零分數。B先清楚揭露兩項最高值相等，再換成共同.344與其餘分數。
- 兩例後先解釋未校準分數，再談資料年與新年度序列；章末完成年份、位置、六分數、所有最高者的一列紀錄，接三句片尾。
- metadata標題依root推薦改為「Google ForTy 森林地圖：兩個台灣像素，算出六類結果」，是同一已採用A的編輯包裝調整，未改frozen brief。說明明列六類含OtherLand。
- 說明本文補Neumann等(2026)、Forest Typology2020(v1)、可點DOI及CC BY4.0連結、裁切／補數／取首分類／重繪改作。五asset加author/url並使用可列出的短署名；未修改任何SVG。
- 聲音provider/name/style不動，無performance覆寫，仍以emotion表演。無source_guide，不捏造站內文章；無shot／Shorts。

## 我懷疑但沒動的事

- 首章小於30秒與既有30–60秒heuristic不同；服從已採用的概念實算路線，不為消警拉長。
- 必要公式會重用輸入與分母，保留完整數學。沒有套用「數字只能說一次」或「故事一定要人類主角」的假規則。
- 縮圖仍是合法文字配置，原生不能直接取diagram當capture；主體由協調者另行處理，不宣稱已完成。
- 不修改brief、voice/style、sharedlexicon或SVG。新稿不增加未登記英文詞，保留DeepMind／ForTy／AlphaEarth既有用法。

## 進度

R1已寫完82場景、85句與85條逐句主張。原生schema及lint零錯；工具估1760 spoken units、507.2秒（8:27.2）。首章24.73秒；55句帶emotion，約64.7%；82個估計狀態平均6.2秒、最長12.3秒，無超過15秒；outro固定三句共41 spoken units。

五項heuristic警告保留：已批准小於30秒首章，以及248／250／86／77在輸入、加總、補數與除法中的必要重用。標題措辭警告已隨root授權的新標題消除，沒有為消警省略算式。

原生composeDescription已實際產生五筆圖片來源；本文DOI與CC BY4.0連結保留，合成說明共2561 bytes，小於5000-byte上限。自查收據與修正前後／刪句紀錄在scratch forty-script-r1.json；原始負面盲評未改寫，R1尚待獨立facts與新盲讀，不聲稱已通過。以上是文稿估算，未TTS、音檢或測得實際旁白長度。


## 指定像素位置補全

依root最後小範圍指示，在B刻意選樣說明後、原始五值前，新增b-pixel-center一景兩狀態、fe8z／ymf8兩句及c86／c87。經緯度取自data/actual-uncertain-roi-result.json的selected_pixel，保留像素中心語義，非10×10窗口精確幾何中心，也不是地面真值。

說明欄新增已公開commit的本片資料包連結，供對照原始值、座標與選樣規則：
https://github.com/x812033727/travel_scanner/tree/e0c70c899/docs/videos/forty-forest-map/data

這項metadata補充是可定位輸入，沒有新增下載／安裝教學，也不是模型API或官方App操作。上方R1自查秒數屬當時版本；本次位置補全的最新原生估時另記scratch forty-location-completion.json。原始盲評分數與no原文保留，不自稱敘事已全數通過。沒有呼叫TTS。

## B六分數總量檢查增補

初始真實音訊timeline總長478.2秒，片尾前正文466.533秒。採用具資訊增益的B逐步加總與抄錄回查，不拉長停頓、慢播或刪改原87句。新中間數值是本片由已核對B輸出所作的十進位加法，不是新的官方效能主張；加總通過不是校準、精度或欄位名稱皆正確的充分條件。

c88｜把第二格填進紀錄前，這六個分數也能加回一嗎？｜RUN-B＋ED：由[0,.344,0,.004,.308,.344]原創推導；.344+.344=.688；+.308=.996；+.004+0+0=1.000；抄錄與類名回查操作非新量測｜https://doi.org/10.25452/figshare.plus.32288616.v1｜2026-10-25｜b-sumcheck-open／afyy
c89｜兩個零點三四四相加，得到零點六八八。｜RUN-B＋ED：由[0,.344,0,.004,.308,.344]原創推導；.344+.344=.688；+.308=.996；+.004+0+0=1.000；抄錄與類名回查操作非新量測｜https://doi.org/10.25452/figshare.plus.32288616.v1｜2026-10-25｜b-sumcheck-pair／f2ze
c90｜再加零點三零八，得到零點九九六。｜RUN-B＋ED：由[0,.344,0,.004,.308,.344]原創推導；.344+.344=.688；+.308=.996；+.004+0+0=1.000；抄錄與類名回查操作非新量測｜https://doi.org/10.25452/figshare.plus.32288616.v1｜2026-10-25｜b-sumcheck-crops／ckag
c91｜最後加零點零零四，剛好是一，另外兩類的零不改變總和。｜RUN-B＋ED：由[0,.344,0,.004,.308,.344]原創推導；.344+.344=.688；+.308=.996；+.004+0+0=1.000；抄錄與類名回查操作非新量測｜https://doi.org/10.25452/figshare.plus.32288616.v1｜2026-10-25｜b-sumcheck-finish／n37p
c92｜總和不對，就檢查漏項和小數位，類別名稱仍要逐項對回。｜RUN-B＋ED：由[0,.344,0,.004,.308,.344]原創推導；.344+.344=.688；+.308=.996；+.004+0+0=1.000；抄錄與類名回查操作非新量測｜https://doi.org/10.25452/figshare.plus.32288616.v1｜2026-10-25｜b-sumcheck-repair／ecb8

## 音檢近音詞改寫第一輪

兩次原生重錄後仍有七句近音歧義，依獨立聽眾改詞候選採用像素與完整森林類別口語說法。自然更新的森林這一類＝自然更新林、原始森林＝原始林、人工栽植的森林＝人工栽植林；不增減六類、不更改數字、算步、唯一／並列、否定或年份。僅改上述七句；已通過的85句保留。舊WAV與全部原生旗標／轉寫另存歷史，不手動清旗。新七句仍須合成與真實音檢，不以改稿當音檢通過。
