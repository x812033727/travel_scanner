# H04 來源圖卡主導版｜離線分鏡轉換（2026-10-14）

站主選定改為來源圖卡主導的投影片；先前「插畫至少佔 50%」屬舊版規格，**不再用作本版門檻**。這份轉換只改 `video.json` 和本資料夾的原創 SVG；不修改已付費 MiniMax 原圖、manifest、媒體帳本、工作區時間軸或後台核准。

## 精確變動

- `video.json` SHA-256：`d89273ced1dcc39d15de99aaf31de38d4834f1364c54a465bf5d2a5d2647646c`。`script.md` 仍是 `7366c0d7b972880b78daaf3327dc650c1417034a45b39ac11a15efc9cc2d3757`。
- 88 個場景的 ID、順序、章節、主張 ID 和 100 句旁白的 ID、文字、順序均保留。原本 49 個 `shot` 已全部轉成正式渲染器支援的來源圖卡／文字資料卡；現在 `shot=0`。沒有把 MiniMax judge 的 PASS 當成人工採用，也沒有把先前退件的模型圖納入正式畫面。
- 新增 8 個帶來源與「非復原」界線的原創 SVG；原有 5 個來源 SVG 與 3 張有授權的歷史文件裁切續用。現行場景模板：`compare 19`、`big 18`、`stats 15`、`steps 15`、`diagram 13`、`table 4`、`screenshot 3`、`bullets 1`。相鄰相同模板最長兩張；開頭依次為日期統計、兩張不同資訊圖、問題卡、文件頁碼卡、流程卡，避免三張近乎一樣的照片式卡連續播放。
- 模型段以資料卡清楚區分「模型假設、後續地形測量、1959 年雪層未知」；搜救段以卷宗觀察、調查推論和仍未知分層。2022 年較新的鄰近雪板痕跡另標時間與地點，沒有當成事故當夜影像。縮圖移除已無 `shot` 的圖像引用；正式縮圖仍待成片階段審查。
- `youtube.description` 的畫面揭露改成文件裁切和原創資料圖卡；移除舊版情境插畫宣告。逐鏡的來源、使用界線與授權仍在 `assets`、`claims.md`、`sources`。可重讀的一次性替換清單是 [source-led-conversion-20261014.py](source-led-conversion-20261014.py)，其 49-shot 前置條件會阻止誤重跑。

## 離線檢查與未過關項目

- `node tools/video/cli.mjs lint --slug curio-h04-v2`：**0 errors、0 warnings**。全部 13 個被引用 SVG 均通過 XML 解析，沒有缺圖；100 個 line ID 均唯一。
- 用**先前**的 15,827 格／30 fps、8:47.57 時窗唯讀試算：100 個畫面狀態，最久 7.7 秒、平均 5.3 秒，`paceProblems=[]`，純投影片的 `cadenceProblems=[]`。舊 `timeline.json` SHA-256 為 `12b18320ed0e246b25ace3ea844f55bbc91f17374e95bc87c85fe1d2bd9b6790`，其中場景類型仍記載舊 `shot`；此試算**不能**冒稱新時間軸、音訊核准或成片驗收。
- SVG 內的事實字與來源放在中上部；共用 `.t-diagram .paper` 淺色底可能延伸到可關閉 CC 之後，720p/1080p 的完整渲染與實際字幕安全區仍要逐段看。新卡與前後深色模板的色階、文字密度、連戲和完整有聲草剪也尚未人工驗收；目前只完成離線 schema、節奏與來源界線檢查。
- 下一關：獨立敘事盲審／來源讀稿 → 用既有 100 句 WAV 無新付費語音的方式重建精確時間軸 → 用新 SHA 送後台音訊核准 → 渲染後看聽連續段與字幕安全區 → 正式成片 QA、縮圖、上架包及站主驗收。前一版的音訊核准不覆蓋這次 `video.json` 與場景模板變動。尚無 H04 新版 `final.mp4`，也沒有上傳或發布。

## 後續關卡讀回（同日）

- 獨立敘事盲審經符合工具格式的逐題 `[line-id]` 證據提交後為 **11/11 PASS**；審查結果 SHA-256 為 `3836a07c033b018ed47be68cbbb4ec12a9ce6a90bfd9a0617dfae6a8523fedcd`。初次沒有方括號的提交僅是工具格式錯誤，原回答與修正格式的檔案都保留在工作區 `review/`。
- `tts --dry-run` 顯示 99 個要求、0 句待合成；`tts --refresh-evidence` 重用 99 句，沒有新付費語音。新版 `timeline.json` SHA-256 為 `967955adb1a861e3facbdd69285654a2a293b7a275b8bfe6745ced283a97e2f5`，100 句／88 場景／15,827 格（8:47.57）。逐句音訊與時窗未變，`narration.wav` SHA-256 仍為 `f6eeaff7f57e66453262a962ad382e84f00867f1c404c102f6d1c5b90cdb3abd`。
- `check-audio`：100/100 句完成，83 句逐字一致、11 句僅同音字或語助詞差異、6 句經 Jev 判為可接受、0 句標記；本次 0 次轉寫與 0 次 Jev 呼叫。`review-push --gate audio` 成功後，`review-pull` 從後台讀回**精確新版 SHA 已依設定自動核准**；本機 `status` 的 `narration approved` 為 `[x]`。這只證明旁白關卡，不代表新圖卡、CC、成片或上架已驗收。

## 本機圖卡渲染與抽查（同日）

- `node tools/video/cli.mjs render --slug curio-h04-v2` 結束碼 0：**100 個畫面狀態已繪製、0 個重用、耗時 501 秒**；產出工作區 `contact-sheet.png`、`frames/` 和 `thumbnail.jpg`。`frames/cache.json` 所列 100 個狀態均無渲染問題。英文、日文、韓文各自的縮圖字尚未提供，工具沿用中文縮圖並給出提示；這不是多語縮圖已核准。
- 逐張看了完整聯絡表，放大抽查片頭帳篷與留物圖卡、1959 年結案書足跡／鞋子裁切、證據分層圖、模型與舊雪的對照圖卡。示意圖有可見的「畫面示意／非現場復原」界線；結案書裁切保留 `1959 結案書 · PD-RU-exempt · 裁切` 標示，沒有把文字裁切冒充事故照片。抽查的主要資訊未見裁字；完整有聲連續審看仍待做。
- **字幕安全區待修核**：在 1920×1080 的實際影格中，三張結案書 `screenshot` 的頁碼／解說字幕行落在約 `y=909–946`；部分 `stats`／`compare` 的來源行也落在約 `y=910–950`。畫面下 15% 從 `y=918` 開始，這些行可能與開啟的 YouTube CC 重疊。來源 SVG 主文多在安全區內，但淡色圖卡底板有的延伸至約 `y=948`。目前只檢查無 CC 的 1080p 影格，未做 720p 或播放器實際字幕疊圖；不能宣稱字幕安全已通過。下一步應用真實 CC 疊圖核對，必要時把這些重要頁碼／來源文字移至較高位置，再重建時間軸與核准。

## 字幕安全區修正與重驗（同日，覆蓋上段待修核狀態）

- 在 `video.json` 中，按有可見來源／頁面說明的場景逐一加入 `data.cc_safe: true`，共 **59/88 場景、69/100 畫面狀態**：`compare 19`、`stats 15`、`steps 15`、`table 4`、`diagram 3`、`screenshot 3`。條件為 `bullets/compare/steps/table/stats` 的字串 `data.source`，或 `diagram/screenshot/photo` 的字串 `data.caption`；本集沒有符合條件的 `bullets`、`photo`。新版 `video.json` SHA-256 為 `49957205075ea66a5d8602489c204b4cc9d2e1d4ed0cc5a8a04d86c766be353b`；除這 59 個旗標外，場景 ID／順序／揭露、旁白與資料欄位均未改動。移除旗標後的內容摘要在前後均為 `0585d4d956dc086710561589e55ebd271d3573b5622ede06406cf186980e8826`，逐句文字摘要均為 `bc1d17e5b8cd9660a21792bb6f164087b484423ad08d34fe44198e633e0686f9`。
- `lint` 為 **0 errors、0 warnings**；敘事審查仍是 `11/11 PASS`，`narrative_hash=6b76fa2d8f1cd22a`，`speech_hash=939e267cecc8f2cb`。既有核准檔 SHA-256 `2246183bcf2c42f1136b30a20a9da17d4eb2697522860494672ae8c8e2b79e1e`、時間軸 SHA-256 `967955adb1a861e3facbdd69285654a2a293b7a275b8bfe6745ced283a97e2f5`、旁白 WAV SHA-256 `f6eeaff7f57e66453262a962ad382e84f00867f1c404c102f6d1c5b90cdb3abd` 均未變。這次版面旗標沒有改動語音或先前核准的聲音時間軸。
- 重跑 `render` 結束碼 0：**69 畫面重繪、31 重用、398 秒**，目前仍是 88 場景／100 狀態，`frames/cache.json` 無問題。新的影格 manifest SHA-256 `62b54a0c402f4e10fa9eb3abc43adade5efbfe640f471d3231ada2866674dfe6`；`status` 顯示影格已渲染、旁白已核准。
- 用現行 SRT 的 **101 個真實字句與時窗**，在渲染影格上模擬 1080p／720p 兩行 CC：Noto Sans TC，1080p 字級 48、行高 60、底距 54，720p 等比縮小；逐行深色半透明底。修正前有 **55 場景／65 狀態**的來源或說明文字進入畫面底部，47 場景與兩行字框直接相交；重繪後對 **88 場景／100 狀態**重掃，**0 場景／0 狀態**在底部帶有來源文字，**0 直接相交**。另掃全部 59 個旗標場景／69 狀態，底部 `y=900–954` 的來源色像素為 0，來源色最下緣 `y=864`，低於 1080p 下 15% 起點 `y=918`。這是本機字幕疊圖與像素檢查；實際 YouTube 播放器的字幕樣式及使用者位置仍可能不同。
- 後驗報告和可目視的 1080p／720p 疊圖在工作區 `review/cc-overlay-qa-after-20261014/`：`report.json`、`opening-search-1080p-cc.png`、`footprint-count-720p-cc.png`、`document-footprints-slot-1080p-cc.png`、`slab-edge-displaced-720p-cc.png`。這四個曾有風險的樣本，來源／頁面說明文字下緣約為 `y=860–865`，在兩行 CC 字框上方且未相交。修正前的對照圖另保存在 `review/cc-overlay-qa-20261014/`，不可拿來代表現況。
- 目前 `thumbnail.jpg` 左側的「鞋在帳內」題字清晰，右側約六成是空白深色區塊，視覺重心失衡；現版 `shot=0` 後，縮圖模板沒有主體圖可填入。**縮圖尚未視覺核准**。可在不買新素材的前提下，從本集已列來源的 1959 年結案書裁切或原創來源圖卡選一個主體作為後續縮圖修訂；本次未改縮圖資料、原圖、旁白或核准。

## 原創縮圖與本機成片 QA（同日，覆蓋上段縮圖待修狀態）

- 在 `thumbnail.data.asset` 引用本資料夾原創的 `diagrams/thumbnail-original.png`，並在 `assets[]` 註明「Mokaair original」、1959 年結案書第 385–386 頁的來源界線及「非現場照片／現場復原」。PNG SHA-256 為 `f2a14012ff6273b6139876ec163adede0c621f6c9eb3c507c2b618c112a96542`；對應 SVG 原件是 `diagrams/thumbnail-original.svg`。沒有使用舊的 `thumbnail-subject.png`，也沒有購入素材。現行 `video.json` SHA-256 為 `558ea4721c855c57ace664533d044f99bfb852c07cdde6dcdfe496c1fc9a1cfa`。除縮圖引用和資產標示外，上一節的 59 個 `cc_safe` 旗標、場景、旁白及時間軸都未變。
- `lint` 仍是 **0 errors、0 warnings**；重跑 `render` 結束碼 0，**0 狀態重繪、100 狀態重用**。新的 `thumbnail.jpg` 為 1280×720、約 61 KB，SHA-256 `f0640e4c64484f47ee443c794ec9f91a93a3113a9e126d9fb2cc655b88dad852`。全尺寸目視：左側橘色「鞋在帳內」清楚，右側帳篷與鞋子圖示填滿原本空白的主體區，兩區不遮擋；按 Lanczos 縮至 320×180 後，主標和圖示仍可辨。縮小樣本留在工作區 `review/thumbnail-original-320.png`。模板的機械檢查也通過，但這仍不是站主對縮圖的人工核准。
- 初次本機 `assemble` 結束碼 0，88/88 段編碼；縮圖更新後再次 `assemble` 結束碼 0，**0/88 段重編**，`checks.json` 為 `ok=true`、`problems=[]`。共有 16,607 格、264 個影格與投影片的 PSNR 檢查（最低 37.75 dB），整體音量 −14.1 LUFS、true peak −0.9 dBFS。`ffprobe` 讀回 H.264 1920×1080／30 fps、AAC 48 kHz 立體聲，長 **553.600 秒（9:13.600）**、90,428,857 bytes。縮圖不在影片影格內，因此第二次總片仍與基線逐 byte 相同：`final.mp4` SHA-256 `ae9b62809dae82eaf96059fb4474c485f28d969f5d3ce47fd723303da1d88f0e`。縮圖後 `visual_hash=e09a59d5032d2d18`，`speech_hash=939e267cecc8f2cb`。
- 重跑 `captions` 產生 101 個繁中 cue；現行字幕 manifest 無問題。工作區 `languages.json` 只記錄 `{ "locales": {}, "decided_at": null }`，明示站主**尚未決定**額外語言，並未代站主選擇「只出繁中」。隨後 `qa --slug curio-h04-v2` **11/11 PASS**，含合成、渲染、旁白、節奏、繁中字幕、後設資料、事實、連結、縮圖格式、政策和揭露。`timeline.json` SHA-256 仍為 `967955adb1a861e3facbdd69285654a2a293b7a275b8bfe6745ced283a97e2f5`，`narration.wav` 仍為 `f6eeaff7f57e66453262a962ad382e84f00867f1c404c102f6d1c5b90cdb3abd`。這是本機 QA；**未送 final gate、未建立上傳包、未上傳或發布**。

## 成片核准與繁中上傳包（同日，更新以上待送審狀態）

`review-push --gate final` 已送出上節的 11／11 QA、720p 預覽及正式縮圖，後台回覆 **approved**；`review-pull --gate final` 回覆 `final: approval recorded`，核准綁定同一 `final.mp4` SHA-256 `ae9b62809dae82eaf96059fb4474c485f28d969f5d3ce47fd723303da1d88f0e`。這是成片關卡核准；站主如在上傳前完整看聽發現問題，仍須回到製作階段修正。

`package --slug curio-h04-v2` 已建立工作區 `upload/`，含正式 MP4、縮圖、繁中 CC、繁中標題說明和 `metadata.json`；上傳包檢查 **4／4 PASS**，metadata SHA-256 `47c57e842945…`。語言仍是 `decided_at:null`。上架關卡提交與讀回、語言選擇、YouTube Studio 上傳及發布另行記錄，不能由本段推定完成。

`review-push --gate publish` 回覆 **approved**，`review-pull --gate publish` 回覆 `upload package approved (metadata.json 47c57e842945)`。這核准的是上傳包，**沒有 YouTube 上傳或發布**；其他語言選擇與 Studio 操作仍待站主。
