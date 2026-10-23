# H06 來源圖卡路線與離線驗收（2026-10-14）

站主已選擇「來源圖卡主導的投影片，調整原先 50% 插畫比例」。這是視覺規格變更；先前 50% 只保留在舊小樣紀錄作歷史比較，不再當成本版交付門檻。MiniMax 原圖及 manifest 的機器分數都沒有因改版而變成可用媒體，也沒有再花圖像或語音費用。

## 正式分鏡變更

- `video.json` SHA-256：`36f8be92d26b1a740cb858aadedd79ae3380dda8b059daa394016f399cef0ce8`。轉換對照在 [`source-card-route-20261014.mjs`](source-card-route-20261014.mjs)，列出每一個原 `shot` 的新圖卡與可見來源，不是依旁白自動生成的通用卡。腳本只供稽核本次轉換；它預期 48 個舊 shot，不應對已轉換檔再次執行。
- 82 個場景全部保留原 ID、排序、章節、claims 與 101 句 `id`／逐字文字／順序；48 個未經人工驗收的 MiniMax `shot` 逐景改成有來源的原生卡。現在是 `big` 33、`compare` 27、`stats` 9、`bullets` 3、`steps` 3、原創 `diagram` 4、授權 `photo` 3，**0 `shot`**。`look` 已移除，影片說明與 `berlin-staff-corridor` 的過時 AI 插圖揭露已改為圖卡、史照及非重建說明。純投影片不再使用付費 keyframes／illustrated storyboard 分支。
- `big` 的來源印在可見 `data.sub`；`compare`、`stats`、`bullets`、`steps` 的來源印在可見 `data.source`。編輯提問卡明寫「編輯提問」；來源字卡是原始資料的整理，**不冒稱判決原頁、實際檢體、人物影像或發掘現場**。保留的三張歷史照片仍沿用 `assets-provenance.md` 的作者、年代、用途和權利註記。
- 兩張運河 SVG 的「非現場／非警方文件」說明由原圖 y=834 搬到 y=218，避免說明文字進入畫面下緣的 CC 區。其餘兩張 SVG 的來源／圖解標記原已在 y=218。外層 `.t-diagram .paper` 仍鋪滿卡面，不能只靠修改 SVG 避免淺色板與 CC 底板相接；要在實際 720p、1080p 畫面分開檢查**文字遮蓋**和**底板相碰**。

## 知識界線與查核

1. 病院章的兩個起點只列為判決保留的不同記述；沒有編造先說名字的人、會面場面或安德森肖像。法院卡分開民事繼承請求、1967 前審證據評價、1970 法律審駁回。法院未裁定她就是尚茨科夫斯卡，也未裁定主觀動機。
2. DNA 卡先列安德森的**保存組織與頭髮彼此相符**，才列與**皇后已知母系參照不符**；毛赫爾是**尚茨科夫斯卡的母系旁系親屬**，其相符結果只支持另一個身分線索。母系序列能為同母系親屬共享，不能單獨給一人確定本名。卡片沒有基因字母、未核機率、假試管或假檢驗輸出。
3. 墓地卡把 1970 年代末找到第一墓、1991 正式發掘及 2007 第二墓碎片分開；44 件與約 70 公尺只用 PLOS ONE 原文支持的數字。第二墓結果為阿列克謝和**一名姊妹**；PLOS 報告不以該 DNA 單獨替姊妹填瑪麗亞或安娜塔西亞的個別墓位。兩墓五名子女到齊則依另一篇 2009 年家族研究表達。
4. 新卡沒有增加旁白外的獨立主張。法律、DNA 及兩墓的來源對應 [`claims.md`](claims.md) c02–c20；PLOS ONE 2009 開放原文已複核墓地時間、44 件、距離、三種 DNA 比對和姊妹個別身分的界線。一九七〇年判決仍據既有第三方保存掃描查核，不把其託管網址說成法院官網。

## 離線機械檢查與待補關卡

- `node tools/video/cli.mjs lint --slug curio-h06-v2 --json`：0 errors、0 warnings；估時 8.2039 分、101 句。`renderProblems(video, repoRoot)`：`[]`，涵蓋圖卡欄位、4 個 SVG 存在與安全語法、3 張史照在 `assets[]`。
- **僅以變更前已核音訊的 14,677 幀時間窗作讀取式投影**：98 個畫面狀態、平均 5.0 秒、最長 8.0 秒，沒有超過純投影片 15 秒的狀態。這不是新 `timeline.json`、正式時長回讀或影片聲畫驗收；新圖卡未改 101 句，但視覺資料變更仍會改時間軸內容雜湊。
- 新的 `video.json`／原創 SVG 必須按現行 `youtube-video` 流程再做獨立敘事盲審、重建 `timeline.json`、逐句音訊沿用核對、以**新精確 timeline SHA** 在後台聽審核准。先前核准的 `8c825dd0…` 只綁舊時間軸。若不需要 keyframes，新版 storyboard 程序應由正式工具按純投影片判斷，不可把舊退件 manifest 當作已過。
- 還需在隔離預覽做開場 3 張圖解與資料卡、法院連續卡、DNA 兩種母系參照、兩座墓與片尾的正常速度聲畫檢查；尤其 27 張 `compare` 和 33 張 `big` 的重複節奏、姓名長字在手機版、可見來源行、兩行 CC 的安全區、史照不是案發現場等。此頁只證明**分鏡資料可讀且來源界線已寫明**，不等於渲染、成片、QA、站主最終接受或上傳。

舊 `brief.md` 保留原 outline 核准所綁的位元組，因此仍描述插畫方案；本變更與站主在同日的路線選擇及本收據一起構成新視覺規格，不把舊 brief 的句子當成現行畫面狀態。

## 來源圖卡版敘事窄修與暫停關卡（2026-10-14，後續狀態）

上述 `36f8be92…`、101 句與 98 個投影狀態，是首次轉換完成當時的快照。新的獨立盲審在第 18 輪以 `no_recap` 判否：`s4mq` 已交代第一墓少一男一女，`jqxi` 又問五名子女是否齊全，緊接 `ufh6` 才回答。為保留第一墓缺口與第二墓的結論，只刪除 `jqxi` 及 `script.md` 對應一句；同場 PLOS／PNAS 比較卡仍以資料欄呈現「核對五名子女是否齊全」。來源索引 c13–c15 也已移除 `jqxi`，沒有改寫史實或重錄。

此時 `video.json` SHA-256 為 `b79f6a9d1a675c21fdba87dca0f9e7871e66f162752d9c6888e76ab927870b35`；82 景、100 句、0 `shot`，`lint` 0 errors／0 warnings，靜態估 8.143 分。第二位只讀當下 CLI 敘事的新盲審者第 20 輪仍以 `no_recap` 判否，這次指出片尾 `4s6y` 重講中段 `bp4e` 的母系比對。兩輪有效結果均存於外部 `review/narrative.json` 的各輪答案檔；其中第 18 輪當前收據已被第 20 輪覆寫，輸入原件分別保存在 `source-slides-blind-round18-validated.json` 與 `source-slides-blind-round19-answers.json`。兩份初始裸行號答案被 CLI 當作格式錯誤，已留存但不計入敘事輪次。

依 `youtube-video` 的兩輪未過規則，已請站主決定是否刪除 `4s6y` 及其單獨圖卡，或授權一個帶明示回扣的新錄句。**在站主選定前，H06 不重建音訊、不渲染、不擴批媒體**。舊 `8c825dd0…` 音訊核准仍只對應先前分鏡；以上改動尚無新版時間軸核准。

## 站主窄修後的八分鐘實測與來源增量草案（同日，更新以上暫停狀態）

站主選擇**刪除 `4s6y` 與 `end-blank-motive` 單獨卡，不重錄**。`script.md`、c17 查核索引與分鏡同步更新。新盲審第 21 輪 11/11 PASS；`tts --dry-run` 為 94 要求、0 待合成，`tts --refresh-evidence` 重用 94 個要求、0 新付費語音。此 99 句／81 景版本的 `timeline.json` SHA-256 `fccdaf93ab053928639479e353c556effc45b9c5facae2dc0bdcc0fb616ff389`，**14,397 格／30 fps＝479.9 秒**，離正式規格的正文八分鐘差 0.1 秒。此時間軸未送新版音訊核准，不能渲染或成片；片頭片尾、靜音與慢播都不能替正文補足。

為補上**新的事實事件**而非灌水，已離線在 2007 年第二墓揭曉前增加 `grave-search-attempts` 來源卡與 `[dm7x]`：「第一座墓之後，幾次尋找附近第二座墓，都沒有結果。」[Coble 等，PLOS ONE 2009 原研究導論](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0004838)記載第一墓發現後多年內曾幾次找附近第二墓，直到 2007 年才發現碎片；句子不指定未見於來源的搜尋者或次數。它承接 `[xz9y]` 的空位，並由 `[v2jq]` 回答。c12 與查核索引已做增量核對。

這份**尚未錄音的候選稿** `video.json` SHA-256 `f8bd0f0f6542d09ee7d0b5f81ff60e82287730263e7a042b6983c3d2fd49a6e8`，82 景／100 句／0 `shot`；`lint` 0 errors／0 warnings，獨立第 22 輪敘事盲審 11/11 PASS。`tts --dry-run` 顯示 95 個要求、**只有 `[dm7x]` 一句待合成，約 24 個計費字元**。五句舊快取的退審或站主已刪錄音均不適合重用。新一句超出先前兩句重錄範圍，已另請站主授權一次；在讀回授權前不合成。合成後須實測是否超過 480 秒、逐句查音及取得新 `timeline.json` 雜湊的後台核准。

## `dm7x` 單句授權後的正式聲音與字幕安全區（同日，更新以上待授權狀態）

站主授權 `[dm7x]` 僅合成一次。`state.json` 本輪 `tts` 收據為 95 個要求、**1 句新合成、24 個計費字元**、0 fallback；正式旁白 SHA-256 `a2031cd8db018fdb707423e8e54e63537eb0fc177b2957dd18907ea44da500b6`。`timeline.json` 實測 **14,582 格／30 fps＝486.07 秒（8:06.07）**，82 景、100 句，SHA-256 `8683ca0e61c7e8bf83cd5e390618435467e21da1e3329eed125f216a0c31ac05`。`check-audio` 回讀 100 句、60 exact、25 同音、15 Jev 判讀、4 舊旗標獲清除、8 舊旗標保留，未漏查；本輪只轉錄新錄的 `[dm7x]`，其文字與稿子 **exact**，無新 Jev 呼叫。站主已在後台聽審並核准此精確時間軸；本機 `approvals.json` 於 `2026-10-14T06:56:23Z` 記錄同一 SHA，`status` 顯示旁白已核准。第 22 輪獨立敘事盲審 11/11 PASS 仍對應現行稿。

來源卡的可見來源行與兩行可關閉 CC 曾靠近畫面下緣。現行 `video.json` 在 **45 景**加 `data.cc_safe: true`：`bullets`、`compare`、`steps`、`table`、`stats` 中有 `data.source` 的卡，以及 `diagram`、`screenshot`、`photo` 中有 `data.caption` 的卡。此欄只把卡面下界向上留出 80 像素，沒有動旁白、景 ID、順序、模板或揭露；`video.json` SHA-256 為 `93d9aee5109dc819cc894650a79efbff60c71eb7dd1733db20b37eb1ff57dcb5`。變更後 `lint` 仍為 0 errors／0 warnings，`status` 仍讀到原精確音訊核准，`timeline.json` SHA 仍為 `8683ca0e…`。實際渲染與字幕疊圖另記於下節，不能只靠 CSS 宣稱畫面已驗收。

## 正式畫格與兩行 CC 疊圖抽查（同日）

`render --slug curio-h06-v2` 正常退出：**97 個狀態新繪、0 重用、643 秒**；`frames/cache.json` 有 97 個 key、**0 個 problem**，`contact-sheet.png` 與 `thumbnail.jpg` 已落在片外工作目錄。再讀 `status` 為旁白已核准、畫格已渲染、字幕已寫出，下一關是 `assemble`；正文尚未合成成片，也未完成正常速度聲畫驗收。渲染後 `timeline.json` SHA 仍為 `8683ca0e…`，`video.json` SHA 仍為 `93d9aee5…`，`lint` 0／0。

人工看過整張 97 格聯絡表：開場五個示意／來源卡、三張史照、法院、兩份檢體與兩座墓的卡片均有可辨識內容；未見照片風格的假現場、假人物、假檢驗字樣或明顯超框。這是靜態總覽，不能代替成片在正常速度的節奏與聲畫檢查。

另將**實際 1920×1080 畫格** `hook-canal-rail` 和 `grave-which-sister` 各疊上兩行中文 CC 黑底，再縮至 1280×720；四張 QA 圖在工作目錄 `review/cc-two-line-{hook-canal-rail,grave-which-sister}-{1080,720}.png`。兩組均目視確認來源／解說行和 CC 黑底之間有空隙，沒有遮字或底板相碰。疊字是本地排版壓力測試，不是播放器實際顯示的 CC；播放器與整片字幕同步仍待成片後檢查。

`thumbnail.jpg`（SHA-256 `8655f97daea7fdbc125bb48f4b579bc3c3e2bc3a54f0da02ee09db69f3078242`）的「她是公主？」主字在 1280×720 和 320×180 都可讀；副字在 320×180 太小，畫面右側約六成是完全空白的深綠主體區。這是**縮圖視覺待修**，不能把本次渲染視為縮圖已核准；此輪沒有另生圖或改縮圖文字。

## 現行縮圖版本的本機成片基線與 QA（同日）

`assemble --slug curio-h06-v2` 正常退出，**82／82 景已編碼、15,362 格／30 fps**；片頭在正片第 1,613 格（53.77 秒）之後插入。`checks.json` 記 `ok: true`、0 個 problem、246 個畫格 PSNR 抽查全過（最低 39.94 dB）、整合響度 -14.1 LUFS、true peak -0.9 dBFS，`visual_hash=f4eb5b81e975981e`。`ffprobe` 實測 `final.mp4` **512.100 秒（8:32.10）**、1920×1080 H.264／30 fps、AAC 48 kHz 雙聲道、84,181,227 bytes；SHA-256 `f6eb1afd271d774fde36300bf57e63287e9a1013cf85c9ff7b7dc55a532eee3a`。正文仍是 14,582 格／486.07 秒，音訊核准的 `timeline.json` SHA `8683ca0e…` 未變；成片時長包含品牌片頭片尾，不拿來補正文八分鐘。

品牌片頭插入後重新執行 `captions`，繁中 CC 為 100 cues、0 problem，`captions/manifest.json` 與現行 speech／branding hash 相符。第一次 `qa` 是 **10／11**：只因工作目錄原本沒有 `languages.json`，舊版 `captionLocalesOf(null)` 預設要求 en／ja／ko 字幕；其他十項全過。依語言流程在工作目錄以 `writeLanguages` 記入 `{"locales": {}, "decided_at": null}`，明確表示**站主尚未決定其他語言**，不是代站主選「只出繁中」。重建繁中 CC 後重跑 `qa`，正式 `review/qa.json` 為 **11／11 PASS**，包括 7 章 metadata、14 個連結、來源查核、節奏、縮圖機械規格及 Jev 政策檢查；同一 MP4 SHA 未變。

這是**現行留白縮圖的本機基線**。後續若採用另一張原創圖解作縮圖主體，需核對新的 visual hash、重跑 render／assemble／captions／qa；本輪尚未送 final review、取得成片核准、製作上架包或上傳。

## 原創縮圖接入與新版成片 QA（同日，更新以上縮圖待修狀態）

已在本機實看右側有主體的原創縮圖，尚待站主對成片與縮圖作最後檢視。正式 `thumbnail.data.asset` 現指向 [`diagrams/thumbnail-original.png`](diagrams/thumbnail-original.png)，`assets[]` 記錄原件 [`diagrams/thumbnail-original.svg`](diagrams/thumbnail-original.svg) 與 **Mokaair original** 授權；秤、問號與 DNA 圖樣是現代編輯符號，不是安德森本人或歷史現場。PNG SHA-256 為 `ed5f298bf07a5265b600fdd9d7f4030b0434a965f86ff672d4f3ec90039f1ec9`，SVG SHA-256 為 `4543ea9b2eb70ad9215cbebad476e53a1cec33980e8a51d07217e1ae603e019c`。本次只新增縮圖 asset 與來源記錄；沒有改旁白、場景、景 ID、揭露或正文時間窗。`video.json` SHA-256 更新為 `23407e470961d4b84968fe935c66851c8fdd91acd58669f6487157e51e8e570e`；`lint --json` 仍為 0 errors／0 warnings，已核准的 `timeline.json` SHA-256 仍為 `8683ca0e61c7e8bf83cd5e390618435467e21da1e3329eed125f216a0c31ac05`。

`render` 正常退出：97 個畫格狀態全重用，**0 個重繪、0 problem**，新版 `thumbnail.jpg` 為 1280×720，SHA-256 `ebbaf0f942fe5662ef2d2571076bd386a5865c1090e07e0d49d587187ec0cea1`；另縮至 320×180 實看，主標可讀，右側秤與問號圖樣可辨，不再是空白主體區。手機版 QA 預覽存於工作目錄 `review/thumbnail-mobile-320x180.png`。新 `frames/manifest.json` 的 `visual_hash=f5a3062c2268f422`。

`assemble` 再次正常退出：**82／82 已有景片全重用，0 個重新編碼**；`checks.json` 記 `ok: true`、0 problem、15,362 格、246 格 PSNR 抽查最低 39.94 dB、-14.1 LUFS、true peak -0.9 dBFS，並綁定新 `visual_hash=f5a3062c2268f422`。`ffprobe` 仍為 512.100 秒、1920×1080 H.264／30 fps、AAC 48 kHz 雙聲道、84,181,227 bytes；`final.mp4` SHA-256 **維持** `f6eb1afd271d774fde36300bf57e63287e9a1013cf85c9ff7b7dc55a532eee3a`。重新執行 `captions` 後，繁中仍為 100 cues、0 problem；本機 `review/qa.json` 為 **11／11 PASS**，其中縮圖機械檢查列 1280×720 JPEG、74 KB，並通過旁白核准、渲染、成片、節奏、字幕、metadata、事實、連結、政策與揭露項。

本次組片後、送審前的 `status` 為旁白已核准、畫格已渲染、影片已組片、字幕已產出，final video 尚未核准。新版縮圖接入沒有觸發任何付費媒體產製，也沒有動到其他語言未決定的 `languages.json`。後續成片審核與上傳包狀態以下節為準。

## 成片核准與上傳包（同日，更新以上待送審狀態）

已用 `review-push --gate final` 送出 11／11 QA、720p 預覽與正式縮圖；後台回覆 **approved**，`review-pull --gate final` 回覆 `final: approval recorded`，本機記錄綁定 `final.mp4` SHA-256 `f6eb1afd271d774fde36300bf57e63287e9a1013cf85c9ff7b7dc55a532eee3a`。這是成片流程核准；站主仍可在上傳前看完整片並指出需要修改之處。

`package --slug curio-h06-v2` 已建立 `upload/`：MP4、縮圖、繁中 CC、繁中標題說明及 `metadata.json`。上傳包檢查 **4／4 PASS**，`metadata.json` SHA-256 `85cfef873939…`；其他語言的 `languages.json` 仍為 `decided_at:null`，代表站主尚未選擇。上架關卡提交與回讀、語言選擇及 YouTube Studio 上傳均另行記錄，不能由本段推定完成。

`review-push --gate publish` 回覆 **approved**，隨後 `review-pull --gate publish` 回覆 `upload package approved (metadata.json 85cfef873939)`。這只核准上述上傳包，**沒有 YouTube 上傳或發布**；其他語言選擇與 Studio 操作仍待站主。
