# ForTy：PT／ID獨立字幕與metadata review

查核日：2026-10-25。依caption-review.md以繁中實際旁白／圖卡、claims、lexicon、worksheet glossary／boundaries比對；查核者不是兩語譯者。本輪只寫此scratch報告，不改repo／todo、不執行git／TTS／付費模型。

**結論：兩語均ready after the fixes。PT 3項、ID 4項，共7項；數字／日期／座標／算式的事實錯誤0項。** afyy因root後改成問句而stale，需以新繁中正常生成worksheet並merge，不能手改hash。

## 實際讀取版本與覆蓋

開始時兩語只有87／92句、metadata空。審查期間作者已合併新增5句及metadata；我重新讀入5句、完整metadata，最後確實覆蓋**兩語各92／92句＋title／description／tags／7chapters／thumbnail**，不是把最早87句審查冒充全92。

| 項目 | 實際綁定SHA256 |
| --- | --- |
| 最終對照繁中video.json | `a62a48382272fb4b9171f2c261b8f736c7516afca35417ccaa842757b04f8a6f` |
| 最終claims.md | `3d24d2befb8022f2af1bdeacad596d0d86e6e2187a4e969ffff5a3935296bcda` |
| PT i18n/pt.json | `3e60467fbc92d7232bac1f910cac89505f732fd058c612133659e631a3e9626b` |
| ID i18n/id.json | `b9bda42ee64932b095a0f0e5f540fa6bd912443373cf685561431f5116893baf` |
| lexicon.json | `aa414e403385008766c93001c7b3fd825da9927b36e893f29f4dd376100ab46a` |

完整92句首次讀入時繁中SHA為`683751ef63552d747d7a6b3eeb170102304606b249ff115c85e3e3ca4c73e68d`。之後root把afyy改問句，我逐ID比較該snapshot與a62a版：只有afyy文字改變，其餘91句完全相同，並補審新問句。上述PT／ID檔仍保留舊afyy，故兩個stale修正列入清單。

最新繁中afyy：**把第二格填進紀錄前，這六個分數也能加回一嗎？**

## PT：3項修正

| ID | 類型／問題 | Current | Suggested |
| --- | --- | --- | --- |
| afyy | meaning／stale。現譯是舊版指令，未保留新版待答問句及「也能加回一」。 | Antes de registrar o segundo pixel, some as 6 pontuações para conferir o total. | **Antes de registrar o segundo pixel, as 6 pontuações também somam 1?** |
| sbkg | meaning。原文問能否「直接」把score視為正確機率；現譯缺直接，可能變成一般地問分數是否能成為機率，削弱後續校準限制。 | Após ler os 2 pixels, essas pontuações podem ser probabilidades de acerto? | **Após ler os 2 pixels, podemos tratar essas pontuações diretamente como probabilidades de acerto?** |
| ecb8 | meaning。原文要求類別名稱仍須逐項對回；mantenha…junto只要求放在一起，沒有明確保留核對正確類別的動作。總和1本來無法抓到類名對錯，這一步宜明說檢查。 | Se a soma estiver errada, confira omissões e casas decimais; mantenha cada nome de classe junto do valor. | **Se a soma não bater, confira omissões e casas decimais; confira também a classe de cada valor.** |

候選字元數分別67／96／94；目前worksheet沒有max_chars，這些數字不是已通過的配音時間預算。若後續有實測budget衝突，保留問句、直接解讀限制及逐值核對類別，不為縮字丟掉條件。

## ID：4項修正

| ID | 類型／問題 | Current | Suggested |
| --- | --- | --- | --- |
| afyy | meaning／stale。仍是舊版「先相加檢查總量」指令；新版應是能否也加回1的問句。 | Sebelum mencatat piksel kedua, jumlahkan 6 skornya untuk memeriksa total. | **Sebelum mencatat piksel kedua, apakah 6 skornya juga berjumlah 1?** |
| wnrz | meaning。原文陳述我們衍生圖實際採用的first-maximum規則，現譯pilih為命令式，變成叫觀眾選，應恢復「本圖如何選」。本地歸屬及依順序的條件要保留。 | Pada peta turunan kami, pilih yang pertama berskor maksimum menurut urutan kelas. | **Peta turunan kami memilih kelas berskor tertinggi yang pertama dalam urutan.** |
| 3pse | readability。dari tanam或tebar benih的動詞搭配不自然；應用自然的被動／名詞形式，保留主要由栽植／播種及本資料>40年條件。 | Hutan tanaman berasal terutama dari tanam atau tebar benih; syarat daur tebang data ini lebih dari 40 tahun. | **Hutan tanaman terutama ditanam atau disemai; data ini mensyaratkan daur tebang lebih dari 40 tahun.** |
| 7qfx | readability。memuat seri hutan…／keterangan tampil yang pertama搭配生硬，seri也容易讀成「序列」；應明白說兩類同為最高，再記下顯示第一個。 | Catatanmu harus memuat seri hutan regenerasi alami dan lahan lain, serta keterangan tampil yang pertama. | **Catat hutan regenerasi alami dan lahan lain sama-sama tertinggi; tulis: yang pertama ditampilkan.** |

四候選均保留既有類名／40年／本地選擇歸屬；未改為官方硬分類tie規則，亦未指定ID1為勝者。沒有自行編寫或合併任何source_hash。

## 核心內容逐組核對：沒有其他實質錯誤

| 範圍 | 兩語結果 |
| --- | --- |
| 開場2020／台灣／本次讀格 | 8aw6保留第一人稱及2020資料年與台灣取樣，沒有改成2026現況或私人現勘。 |
| 六類／40年／OtherLand | 第3類>40、第4類≤40及輪伐期≠當前樹齡保留；第5類含非木材農產品；OtherLand仍可含城市樹木／稀疏木本。兩人工林類在各語內維持不同名稱。 |
| AlphaEarth與訓練 | 專名拼寫與glossary一致，多年觀測表示／線索／參考標註未變成本輪重訓。 |
| A座標／尺度 | 121.4°E／24.7°N、10×10、名目10m與「不是逐樹定位」否定保留；PT／ID用小數逗號符合語言慣例。 |
| B五位小數中心 | fe8z／ymf8均為121,42234°東經、24,69528°北緯，沒有東西南北反轉或小數位遺漏；仍稱像素中心。 |
| 250／255 | 250是完整六值總量，255是nodata；兩語均保留先排除無資料，不把它當score。 |
| A完整算步 | [0,248,0,0,0]、和248、Other2、248÷250=.992、2÷250=.008、其餘四類0、合1、第2類唯一最高，皆忠實。 |
| B完整算步 | [0,86,0,1,77]、和164、Other86、兩個86÷250=.344、1÷250=.004、77÷250=.308、另兩類0，皆忠實。 |
| 新五句加總 | f2ze／ckag／n37p兩語均.344+.344=.688、+.308=.996、+.004=1並保留另兩類0；不是新增模型分數／精度。ecb8 PT核對動作見修正表。 |
| B刻意選樣／tie／本地取首 | 最低最高分的刻意選樣、非隨機精度抽樣、兩類並列、只顯示一類不解決tie、本圖取首等意義保留。ID wnrz／7qfx依上表修語氣與句法。 |
| 校準與正確率 | vb62／8m2e／bs4s均保留未事後校準、需獨立參考、不能直接說99.2%判對。PT sbkg的「直接」須補；其餘沒有把score翻成已驗證accuracy。 |
| 年份／日期／early series | 2020基準五月公開、論文10/21、2017–2025早期年度序列與2020兩格範圍保留，未宣稱本次已取得年度像素或地類真值。 |
| 口吻／CTA／術語 | PT維持você，ID維持kamu／kami；第一人稱未丟。ForTy／AlphaEarth／DeepMind／AI拼寫一致；CTA未加不存在的下載、法規或土地決策建議。 |

## Metadata／7章／thumbnail

兩語title、description、tags、七章及thumbnail均已實讀。原生metadataStatus顯示title／description／tags／全部七章current、無orphan；thumbnailStatus=current。沒有缺欄、空字或超100字標題。

原生唯讀composeMetadata（estimateTimeline、article null、正式sources／6assets、locales pt/id）實得：

| Locale | 合成標題字元數 | 合成說明UTF-8 bytes | 原生problems |
| --- | ---: | ---: | --- |
| PT | 82，含Legendado標記 | 3218 | [] |
| ID | 69，含Sub Indo標記 | 3089 | [] |

說明均保留OtherLand英文及本地解釋、Neumann／完整資料名／2020版本、DOI、CC BY4.0 URL、改作、公開資料包URL、B刻意選樣及2020／2017–2025界線。六筆圖片credits隨原生compose保留。七章依原順序與動作翻譯；thumbnail三詞欄位齊全，headline的`**`與換行保持，數字5／6正確。這些項目沒有需要為了填表而改的問題。

## Cue／字數／配音預算的實際界線

目前兩個worksheet parts=['captions']，92個line項目**沒有max_chars**。不能把沒有預算誤報成全部通過配音預算。原文字串>80字者PT34句、ID30句；它們多含長類名或多子句，原生caption工具可分cue，不能只因整句>80便聲稱已產出的cue溢出或必須刪事實。

實際`captions/zh-TW.srt`本輪不存在；本工作目錄也未找到其他SRT。因此沒有聲稱看過新92句實際時間切點。已按worksheet提供的三組boundaries核對4av2／z33x／8m2e：兩語都依原順序說範圍後總和、壓成一標籤後並列限制、獨立參考後結果對照，未見條件／數字先後反轉。後續正式CC與dub仍需用最新音訊timing跑原生檢查，不能用本語義review替代。

## Verdict與統計

- PT：ready after3fixes；meaning3，facts0，glossary0，cue order0，readability無額外強制改句，metadata0，thumbnail0。afyy是已知source更新造成的stale。
- ID：ready after4fixes；meaning2，readability2，facts0，glossary0，cue order0，metadata0，thumbnail0。afyy同為stale。
- budget／實際字幕閱讀速度：本輪缺max_chars及SRT，未認證、未捏造通過；不是額外內容錯誤。
- 總計7個具體修正；全92句＋metadata已覆蓋，但以上指定SHA檔案修前不標final ready。只回修法，沒有改譯文或清除任何旗標。
