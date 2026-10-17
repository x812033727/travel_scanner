# B14 味之素：正式章節格式原型

**僅完成免費本機格式轉換，尚不可當作正式工作者已完成或可直接製作。** 原repo、來源、row、全文、分鏡和既有審查均未改；沒有API、模型、媒體、主機或付費呼叫。

## 保留及實際執行

- 凍結正文section二的48段、2161編輯字數逐字重建為96個有ID的片段；不是掃全檔regex，也沒有把section四的9組loops算成旁白。原段ID／UTF-16範圍／順序／每鏡串接／全文串接完全一致，無新增pause或say。
- 83鏡原順序不變：75插畫、8數字／來源卡，72個預定不同插畫。prompt、camera、預定image_asset_key都逐字保留；cute-mystery/image-01及CC burn_in:false保持。
- 三組共圖仍為S004→S022、S005→S060、S006→S073；95%數字留S075。相同look/camera/prompt與seed1條件的請求cache key相同；沒有實際選圖檔或SHA。
- 8卡用既有native title：text→title、scope→subtitle、source→tag。官方TEMPLATE_SPECS及slideHtml執行，原卡所有字串都在visibleText，HTML已存card-html/。FDA研究條件、GRAS分類及95%的公司／用途／市場範圍均未刪。未做像素或手機版面驗收。
- 34 CID對應79列完整原段上下文claim，全部UNCHECKED。10列有多來源候選而source=null，不任選一頁。CID→must_verify原索引逐列寫在mapping；這是作者映射，仍待獨立核對，未借用row review的pass當章稿PASS。
- 9組原loop的setup／payoff陣列與所有對應line IDs保存在mapping；native scalar錨點採完整視窗最後一行，原文沒有省略。官方composeStory＋advanceStory本機relint實跑；75鏡shot_reading為0 traps，cute gate為0 errors。

## 尚待完成

1. **真lint保留：17處、8詞發音字典缺項。** FDA、CPU、Shigeo、Nakamura、ABF、Akito、Kitano、FC-BGA。使用同A29/A16的既存fixture；沒有用null或臆造讀音消音，也未聲稱已讀當下主機字典。
2. **正式採用尚無安全入口。** 一般row import會讓writer重寫；readChapterAnswer拒絕含title的origin/idea/engine/turn，hook/now雖可解析仍不是lossless claim installer。需要依精確輸入／series／六章hash採用並保留待查的流程。
3. **保留一項可選編輯建議，不是硬門檻。** 原全文獨立覆核寫「可在正式章稿合併」，worker source-map亦寫T03a/T04「可合併」；這是相鄰語意可精簡、不可為湊長度再重複的建議。frozen storyboard以S066–S069連續測試流程承接兩段，本包逐字保留，沒有把未合併列成違規或必須先改稿的阻擋。詳row-fullscript-adoption-gap.json（沿用首次報告檔名，內文已澄清）。
4. **片長僅估計。** 純旁白含hook在230–250字／分約518.64–563.74秒；官方預設timeline為593.667秒，hook53秒、最長鏡9.167秒。後者含96片段各300ms、82鏡間各700ms、尾1500ms及frame rounding，不能當TTS實測或以空白補片長。片頭5秒、片尾21秒另外計，最後16秒連結區尚未綁實際上架元素。
5. **24 warnings原樣留存。** 其中3處敘事掛鉤警告為99、92、126秒；其他含通用prompt用字、角色漫劇craft建議、tag數和縮圖重複。不能把角色對話規則直接改寫旁白故事；也不能宣稱實際聽稿／敘事已過。
6. **計數差異沒有刪字。** 編輯2161 vs官方2103：11個「〇」未被官方regex計入，Latin詞壓成2單位另少47；完整正文仍逐字一致。
7. **圖片、卡片與人物待真驗收。** image_asset_key無原生still綁定欄位，只在sidecar；data.source是clip裁切，不拿來假裝共圖。原cast保留但未綁到匿名鏡頭，也不生成真人肖像。卡片保留可讀出處及S編號，正式觀眾呈現仍須審核。真正verifier/listener/narrative、發音、TTS、圖片、render、owner看片與上傳全部待完成。

## 交付檔

- chapters/、series.json：六章與原worker metadata形狀。
- mapping.json：全部source／CID／fact／逐字切片／完整loop窗／image共用／card欄位對照。
- fullscript-reconstruction.json：明確section邊界與48段逐字重建。
- compose-lint-evidence.json：真官方合併、17項errors及24 warnings。
- shot-reading-evidence.json、card-adapter-evidence.json、card-html/：實際本機工具輸出，不是成片驗收。
- readiness.json、row-fullscript-adoption-gap.json：可用範圍與未完成事項。
- input-pins.json的repo相對路徑與hand-off pins可供獨立重算；lexicon另指明snapshot fixture，沒有私人絕對路徑寫入包內。

## 交付前澄清

依root指出的原文重新讀取兩份來源，修正把「可合併」讀成硬要求的報告錯誤。首次readiness／說明／gap／pins保留於history/readiness-r1；六章、series、旁白、分鏡、原有17項字典錯誤、compose與mapping均未更改。correction-manifest.json保存精確前後hash及補讀來源。
