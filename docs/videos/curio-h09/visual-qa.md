# H09 分鏡文字獨立檢查

- 結果：**PASS（生成前文字分鏡）**
- 檢查日期：2026-10-15（台北時間）
- 原文字分鏡 `video.json` SHA-256：`4797571A473BD2F608EF0A40E95A989B4B51231BA208A88C30044653A1D7E7A1`
- `script-draft.md` SHA-256：`361ECEA6E3FFDF8283F7B3C1C325E1C9B83FA122E67AACB3C637A41BDCA11F83`
- 範圍：對照草稿旁白、場景文字、卡片、插畫提示詞、主張標記、來源與影片說明；未檢查實際生成圖片、音訊或成片。

## 對照結果

1. 草稿的 95 個有行 ID 的旁白行，依序串接後與 `video.json` 的 100 個音段逐字一致；僅忽略空白，合計 2,649 個字元。B18、F05、F06、F07、F08 五行各拆成雙場，沒有增刪旁白文字。
2. 全片 100 場：92 個 `shot` 插畫鏡頭、7 張 `big` 字卡、1 個 `outro`。92 個 `shot` 都有提示詞；固定畫風為 `cute-mystery`。所有場景引用的 `H09-Cxx` 均可在 `claims.md` 找到。
3. 2026 年現場時序一致：10 月 13 日先踏查 Taraia 沙洲；10 月 14 日已用無人機查看 Taraia，並以磁力儀和側掃聲納展開潟湖調查，資料仍待分析。水力探針直接接觸與後續清淤仍寫成計畫，不作為已完成事項。
4. `video.json` 的來源清單與 YouTube 說明納入[普渡大學 2026-10-14 現場公告](https://www.purdue.edu/newsroom/2026/Q4/earhart-expedition-update-underwater-survey-of-taraia-object-begins/)，明確說尚未公布 Taraia 物件鑑定結果。
5. 畫面提示以模糊潟湖影像、空白器材、未解讀儀器畫面及條件式對照呈現；沒有把 Taraia 畫成已確認的飛機或挖掘成果。2024 年豪蘭附近的深海岩石與 Taraia 潟湖目標分開。

## 配音讀法修正後的綁定

與上一版 `video.json` SHA-256 `F3159462A1B030FE197E2B35D552D6AE74B3EF40587B6C4ACDAE2842AE2766D2` 比對，唯一修改是音段 `h1j3jy6q` 的 `say` 覆寫：刪掉重複的「研究團體」，改為「這些殖民地文件的抄本和掃描，是後來由提加研究團體公布的。」場景 ID、`text`、提示詞、卡片及主張標記均未改。工具 `narrativeHash` 前後同為 `c86a4a4f74475bcd`，`visualHash` 前後同為 `3baa6d38a808fbad`，因此上述文字分鏡 PASS 仍適用；`speechHash` 則由 `bcd031d4d477c8f2` 改為 `31ed2734d0317ba9`。正式 `script.md` 的 speech footer 也已隨之重產，舊劇本關卡若綁舊檔案雜湊，須以後台讀回確認目前核准狀態。

## 限制與後續

本次 PASS 只適用於上述原版檔案雜湊所指的文字分鏡，不代表實際插畫已驗收。插畫生成後仍須逐張檢查是否遵守不預先宣告發現的提示；成片及發布前須重查普渡大學與 ALI 的最新公告。如畫面、旁白 `text` 或來源內容改動，本次檢查需重做。

## 2026-10-15 七鏡付費小樣與提示詞修訂

首輪只產出 7／92 鏡、11 次圖片與 11 次評審；媒體帳本記錄 US$0.1485，預留額為零。`low-fuel-warning`、`uncertain-broadcasts` 各三輪均被評審標為 `needs_review`。人工逐張冷看也發現 `itasca-waits` 水手似乎浮在船外、`radio-0843` 手部與人物比例不自然、`radio-silence` 手勢偏離耳機、`search-plane-island` 的飛機有擬人眼睛及可見乘員；這些鏡頭即使評審顯示 pass，也不視為人工驗收通過。舊版小樣保留作診斷證據，本集 `STOP` 暫停檔仍在。

只改六鏡的 `data.prompt` 構圖：`itasca-waits`、`low-fuel-warning`、`radio-0843`、`radio-silence`、`uncertain-broadcasts`、`search-plane-island`。後兩鏡改用另一座 1930 年代電台的木殼接收機與遠距俯視的海軍水上飛機，避開多餘人物和擬人飛機；不在提示詞重複系列畫風或調色。修訂後 `video.json` SHA-256 為 `C8EA0BB8352FFEE86A2B7D113D1256C86321045EE39C18A8D8E94381A70B5075`，已核准 `script.md` SHA-256 仍為 `7294FD9410349DCBA89347631DF46A551C8A6C570A58983BE11E58A073FA41D5`。獨立複核確認六鏡與原旁白及主張相符；其餘 86 鏡提示詞、旁白正文與固定 `cute-mystery` 風格未改。`lint` 為 0 錯誤、原有 3 項敘事啟發式警告。新版須重新付費產圖並逐張冷看，尚無新版插畫 PASS，也尚未送分鏡關卡。

## 2026-10-15 新版系列規則的全片複核

主線分支納入更新後的 `curio-episode` 規則，故上述「僅改六鏡」與人工退圖結論只是舊版檢查記錄，不能作為目前的開畫清單。另一張窄票逐鏡修訂 92 張插畫提示詞，並由未改稿者獨立終審；現行 `video.json` SHA-256 為 `4BA994EE7838E8E324B40DC9364E48E62212D7E9FB83FEE8B3E49C19C8F2A8C9`。與上一提交比對，91 個 `prompt` 改動；非提示詞欄位只有 Z01 的 `text`、`say`、`say_for` 精修，F03 已在先前提交。送審工具重產的現行 `script.md` SHA-256 為 `D63D46A3E93F7469B9A610CDBD83FB599A1A313D9AAA0A0233EF02C1951C9F82`，後台已讀回此雜湊的站主核准；F2890AA3… 是送審前檔案的舊雜湊。音訊仍須依現行稿重錄與復核。

獨立文字分鏡終審 **PASS（未等於圖片 PASS）**：100 場中 92 張插畫、7 張卡片、1 張片尾，`look` 仍只有 `cute-mystery`；提示詞以單一匿名人物、可見動作與表情為主，各章有遠、中、近景。`direction-not-track` 保持同一條位置線兩端，`search-scale-limits-b` 不把 1937 年表面搜索畫成現代聲納搜尋；Taraia 異常仍是待辨認物件，無已找到飛機的畫面。`lint` 0 錯誤、3 項既有節奏警告，`check:tasks` 與 `git diff --check` 通過。

依目前系列驗收規則重新冷看已付費七鏡：`hour-later-call`、`radio-0843`、`radio-silence`、`search-plane-island` 的 judge 通過圖可以接受；四張的完整 image key 均與付費 manifest 精確相符，原提示詞已恢復以吃快取。`itasca-waits` 即使 judge 通過仍須重畫，因船員站在船外水面且把低矮的豪蘭珊瑚島畫成高山，會誤導歷史地貌。`low-fuel-warning`、`uncertain-broadcasts` 各三輪仍為 `needs_review`，改提示詞後須重判或重畫。媒體帳本仍為 US$0.1485，`STOP` 未移除；接下來只處理有證據的三鏡，其他已合格圖不再加做人工退圖門檻。92 張的整集分鏡卡與實際圖片驗收仍待完成。

## 2026-10-15 首批 28 鏡圖片稽核與暫停

正式劇本更正為 `E9404ADD9954E66AA6C26FC3725D7C0ABD09D91B9E571ED2631C152E4579633C`，音訊時間軸已更新並送審，尚未取得新版音訊核准。現行 `video.json` SHA-256 為 `708349B5F1DF8DA03B0BAF1820B008E9BB0CC9E7BC385F27771D74C019BECC4E`；固定畫風仍為 `cute-mystery`。92 張中的前 28 鏡有 manifest 記錄，其中 27 鏡有 selected image，`pilot-sees-empty` 未完成。媒體帳本為 48 次圖片和 48 次評審，累計 US$0.648、零預留；H09 專屬 `STOP` 已恢復。此段只記錄目前可見的圖片，不把前 28 鏡或全片標為 PASS。

獨立逐圖檢查指出三張已選圖的實質問題：`search-from-howland`、`colorado-over-gardner` 把低矮珊瑚環礁畫成高山；`colorado-seaplane` 的 7.18 分 judge 通過圖讓飛機與甲板人物融合，並出現輪子卻沒有可辨認的浮筒，無法對上「水上飛機」的旁白。`pilot-sees-empty` 首張失敗圖也有山崖，尚無 selected image。這四鏡需在新提示詞下定向重畫與複看。`one-way-radio` 三輪未通過自動評審，末張只有約 2 px 黑邊、內容可讀；`captain-reads-line` 三輪未通過是通用示意地圖的偽字問題，沒有宣稱已知航路。依現行系列規則，這兩鏡先保留候選圖並在完成全片後判斷是否以附註 `accept-best`，不因偽字獨自加購重畫。

提示詞僅對上述有證據的鏡頭及尚未生成、易誤畫高地的低環礁鏡頭補地貌限制：`search-from-howland` 改為海面搜索；`colorado-seaplane` 要求人物與具浮筒的完整飛機分離；`colorado-over-gardner`、`pilot-sees-empty` 要求低平沙環與潟湖；後段相關鏡頭沿用相同地貌約束。新提示詞尚未重新產圖或驗收；通過檢查、提示詞不變的圖保留原付費快取。下一步須先讀回新版音訊的站主核准，再定向重畫、繼續 92 鏡並逐張核對成品與來源。

## 2026-10-15 音訊核准後的定向重畫

站主新版音訊核准已讀回，`timeline.json` SHA-256 `69E3FF3DC95E6EF3811044DC765EEEEEE79D02E28F2F829C68B95171A2691BC2`。定向重畫及獨立冷看後，現行 `video.json` SHA-256 `2B84A62E17B47FA7B5BC8905CD9E01D148A619FF348610318E15E2AD87F39389`；前 28 鏡有 28 張 selected image，0 張 `needs_review`，媒體帳本共 59 圖／59 評審、US$0.7965、零預留。仍只完成 28／92 鏡，未形成全片分鏡 PASS。

`search-from-howland` 換成海上搜索近景，沒有高山；望遠鏡像眼鏡且景別比提示近，但不改變史實。`colorado-over-gardner` 顯示海上低平淺色島，沒有山、人或殘骸。`pilot-sees-empty` 兩次帶島沙景仍在遠景畫山，故改為機艙內飛行員向下搜索的近景；新圖左側有少量低平海岸，沒有山地或失蹤者。`one-way-radio` 改為無帽無線電員，`captain-reads-line` 改為單線空白紙，兩張新圖均無先前的徽章與地圖偽字，judge 通過；耳機雙側、直尺彎曲只是示意細節。

`colorado-seaplane` 舊圖把人物和輪式飛機融合，已淘汰。第一輪新圖的第 2 張有單浮筒、人物分離，但尾翼「NA.」使 judge 未過。此片 `format: drama`，程式的 `keyframes --accept-best` 只允許 illustrated 路線，不能把那張以例外方式標成已通過，因此沒有繞過評審；再次簡化成海上戰艦與離艦水上飛機的遠景，新 selected image judge 9.29／10 通過。畫面可辨雙翼與浮筒，沒有偽字或人物融合；浮筒呈雙條、下方有一個小輪點，屬示意機型誤差，與[美國海軍記載的 O3U Corsair](https://www.history.navy.mil/content/history/museums/nnam/education/articles/from-the-cockpit--stories-of-naval-aviation/naval-aviation-and-the-search-for-amelia-earhart.html)不完全相同，後續分鏡應讓站主看到此畫面。28 鏡目前可續跑生成，完整 92 鏡仍須逐張查核。

## 2026-10-15 全部 92 鏡插畫與分鏡關卡

現行 `video.json` SHA-256 `72E29DCF4C62A2C58B7F1AE6B701FBD7DDD7FBD2467687A370A3C436B822C1A7`，只在已核准正文之外改有據鏡頭的 `data.prompt`；正式劇本 SHA-256 仍為 `E9404ADD9954E66AA6C26FC3725D7C0ABD09D91B9E571ED2631C152E4579633C`，已核准音訊時間軸仍為 `69E3FF3DC95E6EF3811044DC765EEEEEE79D02E28F2F829C68B95171A2691BC2`。`lint` 0 錯誤、原有 3 項節奏警告。最後 `keyframes/manifest.json` SHA-256 `4E8D778DEDB8A67816E37E11304A9028A5C021C7F8513AB2153B9F47C0654FFA`：92／92 鏡有 selected image、0 鏡 `needs_review`，178 次圖片與 178 次評審入帳 US$2.403、零預留；H09 專屬 `STOP` 已恢復。這是本機模型價目與媒體帳本，不是供應商發票。

逐張冷看覆蓋全部 92 鏡，另由獨立檢查者核對四頁聯絡表（24／24／24／20 鏡）：鏡頭順序、圖檔存在與 SHA-256 皆吻合，無空白黑格、新的史實矛盾或重大畫風漂移。已選圖中 `colorado-seaplane` 仍只是可愛插畫中的通用水上飛機，並未標示為 O3U 精確機型；此限制已隨聯絡表讓站主看見。退圖範圍限於會誤導旁白或來源的高地、虛構實物、錯置的聲納圖與顯著畫風問題；單純偽字或卡通細節不另重畫。

整批在 `instruments-survey-a` 提交逾時時留下 US$0.0035 本機預留且無 job ID。正式站資料庫在 05:16 及 05:17–05:18 UTC 兩次唯讀查詢 `slug=curio-h09, kind=image, shot_id=instruments-survey-a` 均為零筆；後端先提交工作紀錄，再呼叫供應商。保留逾時證據後，只釋放這一筆預留，再定向送出該鏡，首張評審通過；未清除其他成本或改種子繞過不明請求。

最終 `deep-sea-sonar-2024` 換為研究員手持**獨立的模糊聲納紙圖**，不把人物畫進螢幕，也不把訊號畫成已確認飛機；`drone-survey-a` 換為帳篷內操作員，不再把尼庫馬羅羅畫成高島。規劃中的水力探針與清淤畫面只見準備器材，沒有已出土物件。四頁聯絡表已送 `/admin/videos`；站主核准後，`review-pull --gate storyboard` 於 `2026-10-15T05:43:44.681Z` 讀回上述 manifest 精確雜湊。分鏡關卡已過，成片、字幕與最終 QA 尚未驗收。
