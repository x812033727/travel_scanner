# 解說系列共用（奇聞檔案局＋原來如此事務所）：教訓

兩個旁白解說系列都會遇到的教訓。共同規則見 `docs/videos/explainer-series/README.md`；只跟其中一個系列有關的，寫在 `curio.md` 或 `sothatswhy.md`。

寫法：一條一段，最新的放最上面。開頭寫日期、哪一集（slug）、誰發現的，接著寫發生什麼、為什麼、下次怎麼做。
已經變成正式規則的，搬進規則檔，這裡留一行「已升為規則：<檔案>」。

這份會自動同步到雲端硬碟兩個系列的 `_規則與教訓/教訓/解說系列共用教訓.md`（docs/videos/rules-sync）。

## 2026-11-25 · sothatswhy-p02-cloud-rain-flow · 首支 Google Flow 動靜混剪長片實戰教訓與去 GitHub 化定案
站主核定首支 Google Flow 動畫化試作長片 P02（39 支 Flow 動態＋40 張 1376×768 厚塗靜圖，468 點、0 重拍，獨立盲審 9.03/10），並將實戰踩坑與架構優化收斂為雙系列共用新規則：
- **先 0 點數 `Nano Banana 2.1` 生圖 QA 才花 12 點生片＋雙專案隔離**：有角色鏡與無人科普／歷史空景分置兩個 Flow 專案，避免人物參考圖污染純物理或空景畫面；全部首尾格先 0 點數出圖、人工逐張驗過構圖（防站上書桌／陽台護欄、防所長耳筆、防小問戴眼鏡、防水壺壺嘴無透明氣態間隙）才進 `Omni 1.2 Flash`，並下載 0 額外點數 720p 原檔後製 Lanczos 升 1080p30＋`-an` 去原聲。
- **Flow 安全過濾詞與 16:9 比例靜默重置陷阱**：小問影片提示詞寫 `"8-year-old / girl / child / bare face / thrusts"` 會觸發未成年過濾，一律改寫 `"the cute 2D cartoon mascot character in a navy coat with yellow hood"`（奇聞 H/G/F 軸亦避開血腥／暴力直擊詞）；在 Flow 從 Video 切回 Image 時比例常靜默跳回 `1:1`，每次生圖必確認寬銀幕並程式驗 `1376×768`。
- **多鏡位剪輯與 P03+ 留存紅線**：依 Unique Story Beats 切鏡；`> 7.5s` 長 Flow 鏡自動切「全景＋`1.24x` 關鍵動作慢放特寫＋尾格運鏡」，`> 6.5s / > 9.5s` 靜圖切 2–3 段交替 `beat-motion-v5`；依盲審回饋新增紅線：**單章不連超 3 顆靜圖、單靜圖規劃 ≤ 8 秒**。
- **逐句 CPS 自動巡檢＋MiniMax 日文單位避雷＋`TP=-1.5` 裕度**：中文配音合成後掃描每句字速（`< 3.5` 或 `> 7.0` 必抽聽），成功攔截 Gemini `p088` 雙重朗讀；日文 MiniMax 把 `500トンも` 誤唸為 `500もんも`，含數字＋外來語量詞需抽聽或加平假名／空白防呆；混音雙階段 `loudnorm` 設 `TP=-1.5` 可預留 AAC 編碼裕度，確保雙引擎 `loudnorm` 與 `ebur128` 穩定落在 `-14.0 ± 1.0 LUFS`、`TP ≤ -1.0 dBTP`。
- **`heimao-left` 本機字體鎖定**：離線算圖 `templates.mjs` HTML 時若未將 `https://video.local/...` 改指本機 `@fontsource-variable/noto-sans-*`，數字會退回系統襯線體；鎖定本機字體後 9 語系（含先前爆框的 `vi`）全數過關。
- **成片盲審後定稿腳本直存雲端、0 GitHub Commit**：盤點發現 `docs/videos/` 已膨脹至 `1.58 GB`（前 4 大項題庫池與舊劇 PNG 佔 `1.40 GB`）。自本集起新集盲審定稿腳本、`i18n`、審片報告一律直存雲端 `製作檔/<slug>/腳本定稿/` 並透過 `cli.mjs import` 上後台，不再進 GitHub。
- 已升為規則：`docs/videos/explainer-series/FLOW-PRODUCTION-RULES.md`、`docs/videos/history-curiosity/CURIO-FLOW-CHECKLIST.md`、`docs/videos/explainer-series/README.md`、`docs/videos/so-thats-why/CURRENT.md`、`docs/videos/history-curiosity/README.md`。

## 2026-11-18 · 奇聞檔案局／原來如此事務所 · 縮圖全面升級正宗黑猫研究院（`@qiqiqushi0`）滿版置頂雙行粗黑邊＋「巨型代表物×戲劇衝突／反應」公式
站主連看兩系列縮圖後指出：「縮圖可能要思考一下應該要放題目的代表性標誌或圖形或物品，如果真的沒有再用現在這樣，不然好像縮圖沒有甚麼魅力而且每一部都長得差不多」「可以參考黑貓研究所」「試試看用黑貓那樣全版的圖再放字看看」。實際抓取拆解黑猫研究院（`@qiqiqushi0`）高點閱原片縮圖（泡麵計時器、SEIKO 石英革命、充電器安規標誌）並對比我們原先的左字右圖分割版（`layout: "e"`／`subject: "right"`）與暗調全版圖後，確認三個決定點擊率的關鍵差異並定案為兩系列統一規格：
- **版型全面改採滿版置頂雙行粗黑邊（`thumbnail.data.layout: "heimao"`／`"heimao-left"`，禁設 `subject`）**：取消分割側欄、底部黑漸層、印章與膠囊；置頂第一行 `headline` 用純亮黃 `#FFE600`＋`22px` 圓角純黑外框（**單行不換行、≤ 10 單位**；外語濃縮在 ≤ 約 20 拉丁字元以保手機 `320px` 寬度字高 `≥ 24 px`），第二行 `sub` 用純白 `#FFFFFF`＋`15px` 純黑外框（**單行 ≤ 14 字**，外語零孤字換行），大標與副標嚴禁破梗答案。當巨型主體衝入右上角天空時改用 `"heimao-left"` 置頂靠左。
- **高明度晴空藍亮底（上 30% 乾淨留白）取代暗調壓黑**：第一次試做全版圖時沿用正片劇場暗調並在底部壓黑漸層，手機小圖反而顯得沉悶；黑猫研究院原廠縮圖一律用**高明度晴空藍或明亮暖光底**，上方 30% 乾淨留白襯托黑框亮黃白字，在 YouTube 淺色與深色推薦列表縮到 `320×180` 時對比度最高，且完全避開右下角時間戳記。
- **下 70% 第一優先畫「巨型題目代表物／標誌 ＋ 戲劇衝突或誇張表情反應」**：不只擺單一靜態死物，更禁止每集習慣性放 `Ada` 或小問半身大頭照撞臉——第一優先把**題目最具辨識度的代表性物品、標誌或物理反差放大成主角，並搭配衝突道具或角色崩潰／驚呼反應**（如巨型發光航海懷錶 H4 配抱頭震驚的皇家天文學家、收費站柵欄擋住膠卷喇叭配噴金幣的杜比號角、左邊鉛筆芯斷裂 vs 右邊鑽石切開玻璃板、巨型方框吹出七彩圓泡泡配小問驚呼）；**只有當題目確實沒有具體代表性物品或圖形時，才退回單純的角色誇張表情特寫**。縮圖更新後必跑九語 `render --thumbnails-only` 逐張目視檢查，並同步更新後台 `/admin/videos` 的上架包（`publish`）與多語包（`languages`）。
- 已升為規則：`AGENTS.md`、`.agents/skills/curio-episode/SKILL.md`、`docs/videos/so-thats-why/thumbnails.md`、`docs/videos/so-thats-why/dialogue-pilot-20261103/README.md`、`docs/videos/explainer-series/README.md`、`tools/video/templates/templates.mjs`、`tools/video/qa/thumbnail.mjs`、`tools/video/core/lint.mjs`。

## 2026-11-14 · sothatswhy-p12-qr-code／奇聞檔案局 · 鎖死兩系列不同人物造型設定圖（2.5 頭身 vs 3.5 頭身）與無人物件鏡佔比（45%–65% `nobody: true`）
站主指出「也不一定每一個畫面要都有人；另外原來如此系列幫我確定人的造型，因為別的對話畫得怪怪的；奇聞就是另外一個造型的人，兩系列不同」。追查根因有二：(1) 舊版 `docs/videos/so-thats-why/series-sheets/` 只放了兩張早期 MiniMax `passed: false` 失敗圖（所長耳垂掛黃鉛筆像耳環、小問半閉豆豆眼＋無指圓手），且《奇聞檔案局》在 Repo 內完全沒有正式設定圖檔，導致不同對話各自憑文字生圖或漏寫頭身比，在「劇場級動畫光影」下把 Q 版角色拉成 6–7 頭身寫實大人或兩系列撞臉；(2) 早期防 MiniMax 空景亂長人臉的舊規則寫「不要大量空景、物件交給人拿」，導致代理把超過六七成的原理解釋鏡都硬塞角色站樁講話。定案如下：
- **兩系列標準角色設定圖正式進版控並徹底分家（嚴禁混用）**：
  - **《原來如此事務所》（`sothatswhy-*`）**：鎖死 **2.5 頭身圓頭大眼 Q 版比例（`2.5-head chibi`）** 雙角色，`ImagePaths` 必傳 Repo 內 `docs/videos/so-thats-why/series-sheets/characters/chief/chief-canon-v2.png`（所長：深棕黑低馬尾帶銀灰挑染、粗黑圓框眼鏡、雙耳乾淨無耳後鉛筆、芥末黃針織外套配白襯衫）與 `kid/kid-canon-v2.png`（小問：亮黑平瀏海短髮＋頭頂呆毛、圓亮大眼有高光、深墨藍牛角釦雨衣配亮黃垂領帽兜、空手無筆記本）。
  - **《奇聞檔案局》（`curio-*`）**：鎖死 **3.5 頭身修長繪本／劇場動畫比例（`3.5-head slender theatrical anime`）**，串場檔案局研究員 `ada` 的 `ImagePaths` 必傳 `docs/videos/history-curiosity/series-sheets/characters/ada/ada-canon-v2.png`（黑色微捲齊下巴短髮＋側分斜瀏海、暗酒紅細圓框眼鏡、褪色青雙排釦風衣配米白高領毛衣；單集跨 ≥ 4 鏡出場的可入畫歷史人物亦先產 3.5 頭身專屬設定圖鎖臉）。
- **畫面不必每鏡都有人（`nobody: true` 佔全集約 45%–65%）**：內建 `generate_image` 畫純物件不會亂長人臉，兩個系列全集應有約 **45%–65%** 鏡頭設為 `"nobody": true`（聚焦純機制剖面、日常物件微距、數量對照、歷史器物與建築環境），角色鏡頭約 **35%–55%** 只留給開場反常、提問猜測、關鍵發現與轉折收束拍。
- 已升為規則：`AGENTS.md`、`.agents/skills/curio-episode/SKILL.md`、`docs/videos/explainer-series/README.md`、`docs/videos/so-thats-why/series-sheets/README.md`、`docs/videos/history-curiosity/series-sheets/README.md`、`docs/videos/so-thats-why/look.md`、`docs/videos/history-curiosity/look.md`。

## 2026-11-14 · sothatswhy-p12-qr-code · 成片獨立觀眾視角評分關卡（修完才推後台與備份）與八語 MiniMax 配音防呆
站主定案「把觀眾評分加入流程，修完後才推後台跟備份」，將獨立觀眾體驗審查與 P12 八語逐句驗音抓出的跨系列規則收進兩個解說系列共用流程：
- **成片獨立觀眾評分關卡（先修完再備份與 `review-push`）**：兩個解說系列在 `assemble` 與 `qa`（11/11）通過後，禁止直接備份或送審，必須先派**未參與撰稿與生圖的獨立子代理**扮演一般 YouTube 觀眾，同時檢視縮圖（含變體與八語縮圖）、標題說明欄、前 30 秒留存、無字插圖理解度、色溫節奏與收尾互動，寫出 `review/audience-review.md`（六項各 ≥ 7.5／10、總均 ≥ 8.0／10）；凡抓到縮圖裁切、圖解難懂、畫面疲勞或角色瑕疵，**一律先重繪／重組並重過 `qa` 11/11，確認零待修問題後才執行 Google Drive 完整備份與 `review-push --gate final`**。
- **厚塗水粉畫風的色溫呼吸與淺冷底示意圖**：採用暖金窗光＋厚塗水粉後，避免連續十幾鏡維持同一種暖棕木桌色調；每 6–8 鏡應安排明亮冷調藍天窗景、戶外日光或深藍夜空／太空冷色場景換氣，且純機制／數量對比鏡優先用淺米白或冷灰桌面襯托高對比色道具，確保手機小螢幕一目了然。
- **八語 MiniMax 配音（`dub --provider minimax`）跨語系發音防呆**：P12 八語共 1,272 句全數跑過 `check-audio --second-opinion` 抓出四類必防陷阱：(1) **印尼文（`id`）禁寫 `&`**：MiniMax 會把 `&` 唸成英文字母 `"FT"`，一律寫成 `dan`，並避開 `-k k-` 跨詞連音（如 `kotak kecil` 連音吞成 `kota kecil`）；(2) **越南文（`vi`）禁寫千分位句點 `.` 與全大寫詞**：`7.089`、`4.296` 會被當成小數點唸錯，四位數以上改寫成無分隔符 `7089` 或文字；全大寫強調詞（如 `CÙNG LÚC`）易被拼讀或糊音，一律用正常大小寫；單字母等級加分類詞（`mức H`），並避開聲調近音歧義（`hộp sửa`「修正盒」易聽成 `hộp sữa`「牛奶盒」，改用 `hộp cứu hộ`）；(3) **西／葡文（`es`／`pt`）單字母防連讀**：`Si H`／`Se H`／`Nível Q` 易與前後母音連讀成 `CH` 或 `nível que`，改寫為 `En nivel H`／`No nível Q`；(4) **泰文（`th`）緊窗口少塞英文縮寫**：泰語短句夾英文 `QR` 會觸發語種切換停頓而衝破 `fit.json` 時間窗，緊湊句優先用自然泰語指代（如 `ป้ายร้าน`）；若伺服器 Gemini ASR 偶發在轉寫開頭漏出 `"thought"` 觸發 `leaked word`，微調該句 1–2 字重錄即可刷新轉寫。
- 已升為規則：`AGENTS.md`、`.agents/skills/curio-episode/SKILL.md`、`docs/videos/explainer-series/README.md`、`docs/videos/so-thats-why/dialogue-pilot-20261103/README.md` §9／§10.4／§10.8。

## 2026-11-14 · curio-p17 · 成片先過「獨立一般觀眾視角評分挑刺」並修完，才備份雲端與推後台
站主在 `curio-p17`（1666 倫敦大火與 666 預言）製作中途請沒參與撰稿生圖的獨立代理以一般觀眾視角實看樣片、九語縮圖與文稿打分挑刺，一次抓出機器 `lint`／`qa` 容易放過、但真實觀眾一秒出戲的五類問題，並定案「把觀眾評分加入標準流程，修完才推後台跟備份」：
- **成片必過獨立一般觀眾評分關卡**：本集實測印證上一條（P12）定案的關卡——`assemble`、`qa`（11/11）只代表機器格式合格，獨立子代理以一般觀眾視角實看成片 `final.mp4`、九語縮圖與說明欄，一次抓出下列五類機器放過的破綻；全部修完並重過 `qa` 後，才照既定順序做雲端硬碟完整備份與 `review-push --gate final`。
- **縮圖大標硬上限 ≤ 6 單位與外語副標孤行目視檢查**：`curio-p17` 初版 `headline` 寫了 9 個單位（`666燒掉倫敦\n**誰是真兇？**`），在 layout `e` 不僅觸發手機 `< 24 px` 字級警告，更把第一行尾端切字；縮成 `666燒城\n**誰背鍋？**`（6 單位）後字級飽滿不裁切。同時八語外語縮圖的 `sub` 渲染後必須逐張目視檢查，修掉第二行只掉下單一孤字（如英文 `sea`、西文 `barco`）的尷尬斷行。
- **拼讀不一致的古典／英國英文姓氏必補音標式英文 `say`**：`Samuel Pepys` 英文正確讀音是 `/piːps/`（Peeps），若只在詞典標 `null` 交給 Gemini 自由發揮，同一集 12 次出場會飄出「佩皮斯／皮普斯／ピプス」三種唸法，一般觀眾一聽就覺得不專業；凡拼寫與實際讀音落差大的英文專有名詞（`Pepys`、`Worcester`、`Thames`），必須在單集 `story-lexicon` 補音標式英文讀法（如 `"Pepys": "Peeps"`）鎖死全片與拉丁語系配音發音一致。
- **同一集嚴禁混用新舊兩種畫風**：中途升級畫風時，若前段保留舊版平塗黑框大頭卡通、中後段才切劇場級厚塗水粉，一般觀眾連看會像兩部不同動畫拼貼；全片所有關鍵影格必須 100% 統一畫風。
- **災難／審訊場的情緒光影與 17 世紀道具考證**：火災逃生與陰鬱法庭場不可套千篇一律的悠閒午後暖陽，應改用火光橘紅冷暖高反差光或陰天冷藍窗光；年代物件需防現代穿幫與物理懸空（如 1666 年倫敦不可畫現代圓形橡膠腳輪手推車、現代白磁盤、對折賀卡式雙開信件或懸空無支撐木匾，應明寫木輻條鐵箍輪推車、粗陶／錫镴盤與三摺火漆羊皮紙信）。
- 已升為規則：`AGENTS.md`、`.agents/skills/curio-episode/SKILL.md`、`docs/videos/history-curiosity/look.md`、`docs/videos/history-curiosity/README.md`、`docs/videos/explainer-series/README.md`。

## 2026-11-14 · curio-m17／curio-p17／sothatswhy-p12 · 兩個解說系列全面改採「劇場級動畫光影×厚塗水粉質感」內建生圖與泰語 Hashtag 修正
站主確認升級樣張後指定兩個旁白解說系列（奇聞檔案局、原來如此事務所）「以後用這樣的風格」，並同步收攏 `curio-m17` 抽檢與 `curio-p17` 實作抓到的跨系列規則：
- **生圖路線（兩個系列全面停用 MiniMax 生圖）**：所有關鍵影格一律改由代理內建 `generate_image`（`AspectRatio: "16:9"`）生成，再以 `keyframes import --provider external --usd 0` 匯入，**嚴禁退回 MiniMax `image-01`**；遇到 `gemini-3.1-flash-image` 配額冷卻時，先完成八語翻譯、配音與 `check-audio`，分批等待配額恢復。`video.json` 仍保留 `"look": { "preset": "cute-mystery" }`（奇聞）或 `"cute-cartoon"`（原來如此）以通過系列身分與版型檢查。
- **角色設定卡鎖定（含跨鏡歷史人物）**：除了原來如此的 `chief`／`kid` 與奇聞的串場研究員外，奇聞單集內只要同一位可入畫歷史人物（過世滿 70 年）跨超過 3–4 鏡出場，就必須先用 `generate_image` 產出該人物的固定設定圖（鎖死髮色、髮型與主色年代服裝），之後每鏡出場都在 `ImagePaths` 傳入設定圖（重繪既有鏡頭時一併傳入前一版構圖圖檔），避免像 `curio-m17` 瑪麗・雪萊六鏡換六套穿搭與髮色。
- **五大畫面質感配方與防留白／防招牌字實戰句**：每鏡英文 Prompt 必帶 `High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background.`；桌面物件近景必須明確補上背景顏料塗滿四邊最外層像素（避免厚塗水粉自動留出畫紙白邊），街道外景必須寫 `plain unadorned walls with zero hanging shop signs`（避免木招與布招冒出亂碼字母）；匯入前必切四格 2 倍放大圖由獨立子代理逐張審過（含地圖／地球儀方位與時代道具考證，避免 1816 年出現插電檯燈或地球儀插錯國家）。
- **泰語系 Hashtag 組合母音與 5,000 bytes 說明欄上限**：`tools/video/core/metadata.mjs` 的 `hashtagsFrom` 原本用 `/[^\p{L}\p{N}_]/gu`，把泰文上下母音與聲調（Unicode `\p{M}` Combining Mark）全部削光，導致 `#ปีที่ไร้ฤดูร้อน` 變成亂碼子音串 `#ปทไรฤดรอน`；已修正為 `/[^\p{L}\p{M}\p{N}_]/gu`。同時外語（尤其泰文，每字 3 UTF-8 bytes）說明欄組完後務必壓在 `< 4,500` bytes 安全區間，避免貼上完整來源清單與補回母音後衝破 YouTube 5,000 bytes 硬上限。
- **首尾呼應提示詞節制與收尾章名份量**：十步架構全片「如開頭說的／還記得開頭…嗎？」顯性提示詞留頭尾最多 2 次即可，中段直接講事實，避免 11 分鐘出現 8 次像照大綱打勾；最後一章 `chapter` 標題要寫收束全片因果的總結句，不要拿單一花絮烏龍當最後一格章名。
- 已升為規則：`AGENTS.md`、`.agents/skills/curio-episode/SKILL.md`、`docs/videos/history-curiosity/look.md`、`docs/videos/explainer-series/README.md`、`tools/video/core/metadata.mjs`。

## 2026-11-13 · curio-s42／curio-w02／story-b01／sothatswhy-p18／sothatswhy-p23 · 一般觀眾視角六支連看檢討
站主請 AI 以一般觀眾視角連看頻道最新六支影片，抓出五個跨集重複出現的結構問題：
- **對話做片漏寫 `pauses`／`still_motion` 與「一句一景」抵銷緊湊停頓**：用 Claude 對話配對影音權杖做片走本機 `cli.mjs`，不跑主機 `settle()`，S42 與 B01 漏寫就退回 300／700 毫秒舊停頓；而寫了 `line_ms: 0` 的集數若把稿子切成一句一景（S42 92 句／73 景、B01 137 句／137 景、P23 71 景裡 50 景單句），每句結尾都變成 `scene_ms` 換景停頓，`line_ms: 0` 形同虛設。同角色同節拍連續 2–3 句要併進同一個 `scene.lines[]`。
- **Gemini 把 `voice.style` 語速打折**：寫「一秒四到五個字」甚至「一秒五個字以上」時，`Sulafat`／`Leda` 實測常落在 3.6–4.3 字／秒，不到站主定的 4.4 字／秒下限；可在 `voice` 加 `"tempo": 1.08`–`1.15` 用 `ffmpeg atempo` 不變調微加速達標。
- **縮圖破梗或選空白靜物**：P23 縮圖直接寫「鏡子沒翻左右／翻的是前後」把全片答案講完；W02 縮圖右框放一本闔上的無字紅皮書，手機列表毫無吸睛度。縮圖只寫反常識衝突或硬數字、嚴禁破梗答案，右圖必選誇張表情或強烈反差。
- **內部查核與作畫備註寫進公開說明欄**：S42、W02、B01 在 `youtube.description` 寫史料算式與「誰過世超過四百年、誰不畫臉」，像內部工程紀錄；一律留在 `claims.md`，說明欄只留給觀眾看的鉤子、受眾、章節、乾淨來源與系列 hashtag（`#奇聞檔案局`、`#原來如此事務所`、`#品牌故事`）。
- **外語標題漏系列名、留言區零置頂引導**：外語 `i18n/<locale>.json` 統一帶八語定版系列後綴；每支上架包交付一則低門檻二選一置頂留言草稿並勾選系列播放清單。
- 已升為規則：`.agents/skills/curio-episode/SKILL.md`、`docs/videos/explainer-series/README.md`、`docs/videos/packaging-refresh-20261111/README.md`、`.agents/skills/youtube-video/references/publish.md`。

