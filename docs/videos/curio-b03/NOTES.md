# curio-b03 Lonely Planet 製作筆記

## 人物設定（2026-11-04）

2026-11-04，獨立評審給這集 34/60（`score.md`），沒有過門檻。最低的兩項是人物一致 4 分、沒有假字 4 分。具體問題：
- 惠勒夫婦在 #4、#55 被畫成兩個小男孩，在其他景被換成海鷗（#3）、山羊（#8、#9）、貓（#13、#14）。
- #94 的大股東畫成一匹馬，#112 的信託會副主席畫成鴿子，#113 畫成清潔工。
- #124 直接重用了 #113 那張圖。
- 假字出現在 #48 雜誌、#53 報紙、#70 牆上掛框、#98 黑板、#99 書頁。

第一版修正曾經把惠勒夫婦、副主席和大股東畫成有固定外型的人，站主（經協調者）2026-11-04 退回：系列規則優先。

### 不入畫

下面這些人都在世。照系列定案（curio-episode skill「人物：在世或未滿 70 年不畫本人」、`history-curiosity/README.md` §內容守則），以及這集 `brief.md` 第 57、94 行，他們一律不畫成人：不畫成可辨認的人，也不用動物、小孩或旁人代替他們。

| 人物 | 為什麼不畫 | 旁白講到他們的景怎麼畫 |
| --- | --- | --- |
| 東尼·惠勒 Tony Wheeler | 在世 | 只畫手、物件或地方：背包和硬幣、釘書機、打字機、地圖、破車、合約、店門的鐵捲門、作家節的空舞台 |
| 莫琳·惠勒 Maureen Wheeler | 在世 | 同上 |
| BBC 信託會副主席（2013） | 在世 | 只畫講台上的手、扶起打翻的茶杯的手 |
| 大股東（肯塔基地主，香菸起家） | 在世 | 只畫掛在柵欄上的牛仔帽、農舍和晾菸葉的穀倉 |
| 檢討報告的作者與評審 | 在世 | #124 只畫兩隻手闔上報告 |

只有一種情況可以畫人：無關的路人，而且不能代表上面任何一個人。這集保留的路人有記者、會計師、店員、雜誌創辦人和報攤小販。#116、#117 開車的西裝商人是 BBC 的比喻，不是真實人物。所以這集沒有需要固定外型的重複人物。

**年代限制**（貼在提示詞尾端）：
- 1972–75 的景：`set in the early 1970s; period-accurate 1970s clothes, tools and vehicles; no mobile phones, no computers, no plastic bottles, no modern cars`
- 2007–2015 的景：`set in 2007-2015; ordinary 2010s clothes, rooms and vehicles; no hard hats, no high-visibility vests`
- 有紙、合約、報紙、雜誌、講台、舞台、招牌的景，另外加 `no readable text, no letters, no signs with writing`。個別加句：
  - #98：`no writing, no chalkboard, no numbers`
  - #99：`no writing, no numbers`
  - #53：`no symbols`
  - #115：`no banners with writing`

### 改了 21 景的提示詞

改的景：#3 #4 #8 #9 #13 #14 #48 #53 #55 #66 #70 #94 #98 #99 #110 #112 #113 #114 #115 #117 #124。旁白、景的順序、秒數、運鏡和卡片都沒有動，`video.json` 其他欄位也沒有動，`youtube.description` 照舊。

- **惠勒夫婦的景**：
  - #3：長椅上的背包，加一隻拿著三枚硬幣的手。
  - #4：從正上方俯拍廚房桌上的釘書機和一疊書頁，畫面裡只有兩雙手和前臂。
  - #8、#9、#114：從背後看，車頂綁著行李的破車開離倫敦，開上往東的公路和沙漠公路。
  - #13：桌上的小書堆、打字機和茶壺，加一隻放上小書的手。
  - #14：一隻手拿著小書比在尺旁邊。
  - #55：俯拍合約，被圈起來的段落上蓋著一張背面朝上的撲克牌，就是旁白說的「那張牌」。
  - #66：一隻手從門邊掛鉤取下背包。
  - #110：一隻手在黃昏拉下小店的鐵捲門。
  - #115：峇里島作家節的空舞台，只有一支麥克風，畫面前緣一隻手舉著錄音機。
- **副主席**：#112 是講台上穿炭灰西裝袖子的手；#113 是一隻手扶起打翻的茶杯，代表「犯了錯」。
- **大股東**：#94 是掛在柵欄上的白色牛仔帽、農舍和晾菸葉的穀倉。
- **重複圖**：#124 是兩隻手闔上報告，夾著三張書籤，代表估太高、轉太慢、碰上壞時機。它不再跟 #113 共用 `trust-lectern-2-1-trim.jpg`。
- **假字**：
  - #48：雜誌創辦人摔下一本素色封面的雜誌。
  - #53：報紙改成素面，只畫一個箭頭。
  - #70：牆上掛框改成風景畫。
  - #98：不畫黑板，改成從一大疊鈔票上拿走一小疊。
  - #99：書頁改成六個闔上的素色文件夾。
- **動物**：#117 拿掉蝸牛，只留開車打呵欠的西裝商人。

第一版改過、這一版改回原本提示詞的景：#10 #12 #26 #108 #116。它們原本就只畫手、記者或比喻 BBC 的商業人士，沒有畫到在世的人，原圖也沒有被評審點名是壞圖。提示詞逐字還原，可以吃快取，不用重畫。

這次沒改的景有三類：
- 評審提到只畫手的 #30 #35 #62 #90 #91。
- 只畫物件或人物太小的 #40 #49 #64 #86 #87 #106 #123。
- 第一景 open-you。它本身就是那本黃色厚書，評審說鉤子成立。

**lint**：這個分支的 `docs/videos/lexicon.json` 少了 `BBC` 和 `TripAdvisor`（main 的 42b0585d1 已經加了），所以在這個 worktree 跑會出現 28 個「not in lexicon」錯誤，跟提示詞無關。換成 main 的 lexicon 跑，結果是 `curio-b03: 0 errors, 0 warnings`。

**還沒重畫**：下一次 keyframes 只會畫上面這 21 景。

## 正向改寫（2026-11-04）

規則：MiniMax image-01 沒有反向提示詞，寫 no／not／without 會把那個東西畫出來，所以 `data.prompt` 只寫要畫的東西（`history-curiosity/look.md` 第 21、72 行；W02 實證）。上面「年代限制」裡的 `no …` 尾句已經作廢，改成正向寫法：1970 年代的景寫 `set in the early 1970s; period-accurate 1970s objects／vehicles`，2007–2015 的景寫 `set in 2007-2015; ordinary 2010s office clothes and rooms`（只有物件的景寫 `… objects`）；不要字就寫 plain／blank 的紙、封面、看板，合約的字行畫成 `plain grey bars`，地圖畫成 `plain coloured land and sea shapes`。

改了 32 景：#3 open-sydney、#4 open-table、#8 road-van、#9 road-van-2、#10 road-map、#13 kitchen-type、#14 kitchen-staple、#28 deal-notary、#48 rival-publisher、#50 rubber-stamp、#53 editor-cheer-2、#54 tablet-cafe、#55 contract-circle、#57 put-lawyer-2、#58 put-finger、#66 backpack-hook、#70 ads-phone、#85 gavel-file、#86 rain-shop、#91 app-grid、#94 buyer-street-2、#98 calc-board、#99 calc-board-2、#106 trust-statement、#110 shutter-dusk、#112 trust-lectern、#113 trust-lectern-2、#114 van-highway、#115 van-highway-2、#117 van-slow-2、#120 homeoffice-wave、#124 close-answer-report。

- **在世的人的景**（惠勒夫婦 #3 #4 #8 #9 #10 #13 #14 #55 #66 #110 #114 #115、副主席 #112 #113、大股東 #94、報告作者 #124）：畫面用物件填滿（背包、釘書機與小書、打字機、地圖、破車、合約、鐵捲門、講台、牛仔帽），最多一隻穿袖口的手（`one hand in a sleeve cuff`），不留空白讓模型補臉。
  - #4、#124 原本是兩隻手，這次改成一隻手；#4 從 overhead shot 改寫成 top-down flat lay（同樣是俯拍）。
  - 破車的景（#8 #9 #114）都寫 `seen from behind … rear window packed with bags`，看不到駕駛座。
  - #66 原本的 empty desk 改成 cleared desk 加一箱打包好的文件夾，保留「離開」的意思，不留空桌面。
- **路人與比喻**（#28 #48 #50 #53 #54 #57 #58 #70 #85 #86 #91 #98 #99 #106 #117 #120）：只把否定句換成正向寫法，人物、動作、景別不變；背景寫 `a plain bare wall`。
- 長度都在 350 字元以內；沒有否定字的另外 84 個提示詞一個字都沒動（吃快取）。旁白、景的順序、秒數、卡片、camera 都沒改。
- 第一版把「blank」寫進太多景，lint 警告「blank 出現在 43／116 張」，把原本就寫 plain 的地方改回 plain 後消失。

**驗收**：`lint --slug curio-b03` 是 0 errors, 0 warnings；用 `\b(no|not|without|nobody|nothing|none|avoid)\b`（不分大小寫）再掃 `data.prompt`，剩 0 句。下一次 keyframes 要重畫這 32 景。

## 第三輪：在世人物只畫物件（2026-11-04）

第二輪 37/60（`score/curio-b03-r2/score.md`），「畫面與旁白對得上」4 分。原因是 #3 #8 #12 #13 #114 的提示詞只寫物件加一隻手，模型還是補出了臉（小男孩、動物頭、後窗乘客）。新規則：**旁白講到在世人物的景只畫物件，不畫手也不畫人**，用正上方俯拍或填滿畫面的靜物。只要畫面裡有手，模型就會補上身體和臉。提示詞只寫正向描述，約 250 字元以內，不寫畫風字。

改了 26 景：
- **在世人物 → 只畫物件**：
  - 惠勒夫婦：#3 open-sydney（兩個背包加三枚硬幣，代表一對夫妻）、#10 road-map、#12 flat-ask-2、#13 kitchen-type、#14 kitchen-staple、#20 jaisalmer（原本的駱駝夫容易被看成惠勒，改成城牆上一本攤開的黃色書）、#28 deal-notary（原本的公證人容易被看成惠勒，改成四張股票，其中一張分開放）、#62 put-handshake（反蓋的合約上交叉兩支鋼筆）、#66 backpack-hook（掛在門邊的背包，下方一箱打包好的文件夾）、#110 shutter-dusk、#115 van-highway-2（錄音機改成放在舞台邊）。
  - 副主席：#112 trust-lectern、#113 trust-lectern-2。
  - 報告作者：#124 close-answer-report。
  - #4、#55、#94 原本就只有物件，這次沒動。
- **同一台破車**（#8 road-van、#9 road-van-2、#114 van-highway）：三景用同一句描述，`a small 1970s pale blue van with a white roof, luggage piled on its roof rack under a canvas tarp over the rear window, a plain licence plate`，從高角度在車後拍，帆布蓋住後窗。車頂原本寫 cream，lint 判定和 look 的色盤重複，改成 white。
- **同一個律師**（#5 open-tease1、#56 put-lawyer、#58 put-finger）：三景都寫 `a middle-aged lawyer with short grey hair, a brown waistcoat and a white shirt`。他是不具名的綜合角色，可以畫臉。#5 這次也改了，跟另外兩景一致，所以要重畫。#58 拿掉圓眼鏡。
- **假字的來源**：
  - #101 ledger-book：空白帳頁畫成灰色橫條，拿掉只露眼睛的會計師。
  - #12、#13 的打字機：寫成 `a plain smooth metal panel`。
  - #8、#9、#114 的車牌：寫成 `a plain licence plate`。
  - #15 kitchen-shop：書脊寫成 `plain book spines in solid colours`。
  - #59 put-kettle：價格牌改成 `a plain paper tag`。
  - #119 movers-box：工人改成短髮、穿素色連身工作服，原本帽子上的符號就沒有地方出現。
- **其他**：#87 tower-night 只畫一棟樓和一扇亮窗，不畫人；#123 kerb-booklet 改成俯拍，石磚上擺滿三樣物件，讓畫面沒有空位。
- **檔案狀態**：這一輪開始時，#3 #4 #94 #115 的提示詞已經被別人改成和上一節不同的版本，這一輪以當時的檔案為準。

**驗收**：`lint --slug curio-b03` 是 0 errors, 0 warnings；否定字掃描剩 0 句。這 26 景下一次要重畫，重畫後要逐張開原圖看，畫面裡有臉就退回。
