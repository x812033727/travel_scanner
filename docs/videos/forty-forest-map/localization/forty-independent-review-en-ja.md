# ForTy en／ja 獨立字幕審稿

2026-10-25。審閱者未撰寫這兩語翻譯，未引用或沿用作者的self-critique；直接對照繁中原句、圖卡、claims證據範圍、詞表與實際譯文。只寫此報告，沒有修改repo／todo、執行merge或TTS，也沒有新派代理。

## 實際審閱版本與範圍

本次開始時兩語各87句；審稿期間作者已補成92句與metadata，故**最終實際審閱為兩語各92句，加標題、說明、tags、七章與縮圖文字**。不能把本報告標成只審了87句，也不把中途預期的stale當作原87句翻譯失敗。

最終綁定：

| 檔案 | SHA-256 |
| --- | --- |
| video.json，92句 | `a62a48382272fb4b9171f2c261b8f736c7516afca35417ccaa842757b04f8a6f` |
| i18n/en.json，92句 | `6c51a0300db3a701c9e52942bcdf28a8d78b9f55fb0e20f5a0252f9b9df173e4` |
| i18n/ja.json，92句 | `9fb2ae3836be1536f63ef76ba7e39d736a39b652547542ca501217a4b4f3c61e` |

版本過程：初次讀取video為`20bb4b24df9b9bcccaf2763598f7478a4a706e859f0e20909a09b9c4d5fca969`，EN87句`264ad17cfb3c03141f8be73e3442523a8ed28bde77f1b9990502989222dd8963`、JA87句`08eff2c51d5d4a1aeb5828f62686bc950f7f0e9bfde432e0efe092f18f36b73a`。再讀的92句版EN為`812e599f0d7d47a0e7ad32982412591a7da8d9b2a99d2e7ce320a4c234d9c7ef`、JA為`fa49fb1278700455fa8acc8a05cc3cbc1fff180b99fb08f44c3e65414a533126`，其中afyy仍是前版指令句。最終再讀確認只有afyy對應新問句更新，其他91句與metadata值未變，並已把這個delta納入審閱。

目前92個翻譯line ID均存在，兩語逐句source_hash與當前繁中原句相符。沒有把作者後來重蓋的hash當成語義證據；afyy的新譯文亦實際重讀，見下段。

## 建議修正：EN

以下以同一句的操作意義與必要術語為準；數字、座標與否定沒有發現錯譯。章名項屬低優先精確化。

| ID／欄位 | 類別／問題 | 目前 | 具體修法 |
| --- | --- | --- | --- |
| 8m2e | M1，指代歧義。來源要檢查「分數」與真實結果的對應；them緊接independent references，可能被讀成檢查參考資料本身。不是指原譯已證實反義，而是把操作對象寫清楚。 | To treat scores as chances of being right, use independent references, and check them against real outcomes. | To treat scores as chances of being right, use independent data; compare scores with real outcomes. |
| ncx4 | G1，版本語義。early annual series可被讀成較早時段的序列，沒有清楚保留官方early-release狀態。 | That introduction also shared an early annual series for 2017–2025. | That introduction also shared an early-release annual series for 2017–2025. |
| description（年度序列片語） | G1的metadata同處用語，與字幕一致寫明early-release；不改2020實算及刻意選樣的範圍。 | The early 2017–2025 annual series… | The early-release 2017–2025 annual series…（其餘原段保留） |
| w86h | R1，自然度。takes its green不是這裡自然的英語說法；最高分類→套用該色的操作可直說。 | Color by the highest score's class, and the red-boxed cell takes its green. | Color by the highest-scoring class, and the red-boxed cell turns green. |
| chapter:first-grid | 低優先metadata精確化。繁中是讀「綠格」；Forest Cell多帶了一層森林類型的稱呼，用green cell更貼原文及模型輸出語境。 | Read a Taiwan Forest Cell | Read a Green Cell in Taiwan |

EN計數：meaning／clarity 1、glossary 2個欄位（同一early-release問題）、readability 1、metadata精確化1；facts數字錯誤0、否定反轉0、已發現cue-order錯誤0。未虛填budget錯誤。

## 建議修正：JA

| ID／欄位 | 類別／問題 | 目前 | 具體修法 |
| --- | --- | --- | --- |
| ncx4 | G2，版本語義。「初期の年次系列」不如「早期公開版」清楚表達early-release，容易被理解成時序初期。 | その紹介では、2017〜2025年の初期の年次系列も共有されました。 | その紹介では、2017〜2025年の早期公開版の年次時系列も共有されました。 |
| description（年度序列片語） | G2的metadata同處用語。保留它與2020本片計算分開的句子，不改寫成已取得年度像素。 | 2017〜2025年の初期の年次系列 | 2017〜2025年の早期公開版の年次時系列 |

JA計數：glossary 2個欄位（同一early-release問題）；meaning、facts數字錯誤、否定反轉、其他術語／自然度與已發現cue-order錯誤均0。其餘92句未發現需要另改的實質問題，不為湊修正數改寫標準林業名詞。

## afyy：已完成的來源更新，非作者原87句失敗

root後來把來源改為：「把第二格填進紀錄前，這六個分數也能加回一嗎？」。先前指令句譯文對前版來源是忠實的；對新來源則應保留問句、6個分數與加回1。

目前最終實際讀到的譯文：

- EN：Before recording the second cell, do these 6 scores also add up to 1?
- JA：2つ目のマスを記録する前に、この6スコアも合計1になるでしょうか。

兩句已忠實對應新問句，沒有待修。若仍需另一個同義JA寫法，可用「2つ目のマスを記録する前に、この6スコアも足すと1になるでしょうか。」；現句本身可以保留，不要求為風格換句。

## 逐句核對索引

每個已譯ID都讀過。OK代表未發現本文範圍內的實質翻譯問題，不代表已經通過配音音檢、字幕時窗或成片QA。

| line ID | EN | JA |
| --- | --- | --- |
| 8aw6 | OK | OK |
| gngj | OK | OK |
| ep85 | OK | OK |
| jw6i | OK | OK |
| 5ur9 | OK | OK |
| m2p6 | OK | OK |
| erqz | OK | OK |
| t4w3 | OK | OK |
| 66nz | OK | OK |
| 3pse | OK | OK |
| v9fh | OK | OK |
| 7id9 | OK | OK |
| 2vcb | OK | OK |
| yiya | OK | OK |
| rrgq | OK | OK |
| fbc5 | OK | OK |
| gsa7 | OK | OK |
| 9wmz | OK | OK |
| jkby | OK | OK |
| 5nt9 | OK | OK |
| m8cb | OK | OK |
| p2ry | OK | OK |
| u5js | OK | OK |
| 7732 | OK | OK |
| yi97 | OK | OK |
| 2k27 | OK | OK |
| vk36 | OK | OK |
| gfes | OK | OK |
| e826 | OK | OK |
| svhy | OK | OK |
| 3gwz | OK | OK |
| 7iv8 | OK | OK |
| bxdi | OK | OK |
| anxa | OK | OK |
| up9r | OK | OK |
| 3p97 | OK | OK |
| 4av2 | OK | OK |
| 8hpb | OK | OK |
| ywu9 | OK | OK |
| u362 | OK | OK |
| eym7 | OK | OK |
| k3i2 | OK | OK |
| p9sg | OK | OK |
| dkq3 | OK | OK |
| w86h | 修正 R1：自然度 | OK |
| wh49 | OK | OK |
| 6ybg | OK | OK |
| xxju | OK | OK |
| endc | OK | OK |
| appe | OK | OK |
| beg8 | OK | OK |
| fe8z | OK | OK |
| ymf8 | OK | OK |
| 54sx | OK | OK |
| mfsh | OK | OK |
| 578j | OK | OK |
| 97h6 | OK | OK |
| 8mtz | OK | OK |
| 4amm | OK | OK |
| ux8j | OK | OK |
| y64h | OK | OK |
| afyy | OK：已同步新問句 | OK：已同步新問句 |
| f2ze | OK | OK |
| ckag | OK | OK |
| n37p | OK | OK |
| ecb8 | OK | OK |
| 8k4a | OK | OK |
| z33x | OK | OK |
| wnrz | OK | OK |
| ywz8 | OK | OK |
| ww8v | OK | OK |
| mx7g | OK | OK |
| 7qfx | OK | OK |
| hbci | OK | OK |
| sbkg | OK | OK |
| upmh | OK | OK |
| vb62 | OK | OK |
| 8m2e | 修正 M1：指代 | OK |
| bs4s | OK | OK |
| ci5j | OK | OK |
| 6ss6 | OK | OK |
| rume | OK | OK |
| pvkj | OK | OK |
| ncx4 | 修正 G1：early-release | 修正 G2：早期公開版 |
| j5kv | OK | OK |
| nqyj | OK | OK |
| wfb2 | OK | OK |
| 88pk | OK | OK |
| bu6j | OK | OK |
| hr4b | OK | OK |
| 4w7g | OK | OK |
| 39nc | OK | OK |

## 數字、術語與邊界核對結果

以下內容在兩語均與繁中一致，沒有發現要修的數字或條件：

- 六類與只存五個值；250總量／255無資料；零是有效值，無資料格排除。
- 原始林的原生樹種與無可見人為干擾；自然更新林含恢復中的次生林；人工栽植林的栽植／播種與本資料>40年條件；林木種植園的集約、少數樹種／同齡／規則間距及≤40年條件；輪伐期與當前樹齡分開。
- 樹作／農林複合的非木材農產品及油棕／橡膠／果園；OtherLand仍可包含都市樹木／稀疏木本，沒有譯成「裸地」或「完全無樹」。
- A請求121.4°E／24.7°N、10×10窗口、10m輸出尺度。原始五值[0,248,0,0,0]、加總248、Other=2、÷250後.992／.008、其餘四類0、六項和1與唯一最高。
- B指定像素中心121.42234°E／24.69528°N。pixel center／画素中心保留，沒有擴成偶數窗口的精確幾何中心或地面真值。
- B原始五值[0,86,0,1,77]、86+1+77=164、250−164=86、自然更新林與其他土地同為86並列最高、÷250同為.344、林木種植園.004、樹作／農林.308、其餘兩類0。
- 新四句算術／排錯f2ze、ckag、n37p、ecb8：.344+.344=.688、+.308=.996、+.004=1、另兩類0不改總和；總和不對時檢查漏項／小數位，名稱仍逐項對回。沒有把加總1譯成模型判對或機率已校準。
- B刻意選「各格最大分數最低」的例子，不是隨機精度抽樣；兩類並列與本圖依類別順序取首分開。EN的Our derived map、JA的この派生図保留本地範圍，沒有宣稱官方另行硬分類層也已測得此規則。
- 模型score與實際accuracy／正解率分開；未事後機率校準；99.2%正確機率的句子保留否定。8m2e只有上述操作對象指代可再清楚化，沒有數值或否定反轉。
- 2020基準資料五月公開、論文10月21日、2017–2025序列與當前2020兩格實算分開；沒有新增本次已測年度變化、重訓、官方App成功操作或現地經驗。
- DeepMind、ForTy、AlphaEarth、AI、Google名稱與大小寫保留。EN六類常規名、JA原生林／天然更新林／人工林／プランテーション林／樹木作物・アグロフォレストリー／その他の土地，各自前後一致；不因縮短而混淆兩種人工林。

## Metadata、時序與預算的實際覆蓋

已讀兩語全部標題／說明／tags／七章／三個縮圖文字欄位。EN標題56字元、JA35字元，皆小於100；兩語各7章，tags總長各96／48字元，無空欄或角括號。縮圖的**強調**與換行保留。資料署名Neumann等(2026)、Forest Typology 2020(v1)、DOI、CC BY4.0連結、裁切／補數／取首分類／重繪與資料包commit URL均保留；六類明寫包含OtherLand，不是六種森林。除前述版本片語與低優先EN章名外，未發現metadata需修的事實。

本次實際讀到的en／ja worksheet parts仍是captions，全部max_chars為null。可逐句檢查可讀性，但不能宣稱已驗證配音fit，也不把任意字數當作工具硬預算。EN8m2e修法99字元、EN ncx4修法75字元、EN w86h修法71字元、JA ncx4修法38字元；精確窗口預算若後續提供，仍要原生fit核對。

`captions/zh-TW.srt`在本次讀取時不存在，不能假稱逐時間碼對齊已驗收。worksheet有3筆非空boundaries（4av2、z33x、8m2e），兩語的「有效值→總和」「壓成標籤→並列不分高低」「用途／獨立參考→檢查結果」順序均未反轉；8m2e的指代問題已單列。其餘句子不另外捏造cue-order或時窗通過證據。

## 判定

**已獨立讀完目前92句與已提供metadata。EN採上述指代／版本／自然度修正，JA把early-release寫清楚；其餘數字、座標、否定與實證範圍未見問題。afyy已同步新問句，不列為失敗。** 這是翻譯內容審稿，沒有代替配音、字幕fit或最終影片QA；後續檔案hash改變時，本報告只綁上列版本，新增差異再作delta覆核。
