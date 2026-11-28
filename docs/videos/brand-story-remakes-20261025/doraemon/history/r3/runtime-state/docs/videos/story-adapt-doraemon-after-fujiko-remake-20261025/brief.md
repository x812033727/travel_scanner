# Doraemon remake｜R3作者候選

## 問題

新故事到底是誰在寫，而一直留下來的原作署名，又承擔什麼工作？

## 一句答案

各版本有具體的新寫作者；原作的角色、世界與解釋方法，為這些新工作提供基礎。保存原紙、接續大長篇、寫電影腳本、把文字做成動畫、寫小說、手繪漫畫、電影漫畫與舊作再版，分別是不同工作，要按版本與職稱讀署名。

## 站主觀點

作者提案觀點：熟悉名字能把觀眾帶進作品，但理解它如何繼續，需要看見眼前的人具體做了什麼。旁白用「我覺得／我喜歡」標記自己的反應，不把意見當當事人的未公開心理，也不替站主宣稱已核准此觀點。角色是fiction，這條製作工作史仍屬非虛構。

## 單一主線與新答案

從むぎわら把稿轉寫到另紙、保留下原件的動作出發，接到2019年他鼓勵辻村承接腳本，再追到辻村／八鍬如何處理科學資料、原短篇的解釋方法、友情動機、時長、台詞與小說媒介。末段只用具體版次的漫畫／2025／2026署名回應原作與新寫工作如何並存，沒有逐年電影片單。

開場前兩句對觀眾說話、帶三十年與可能認錯寫作者的利害；前六句已到具體稿紙、助手、未落筆的動作。只預告一個未來事件：帶著五、六本科學雜誌的會議，停在如何讓冒險成立之前；單一點名與規模的承諾句之後，以全片主問句收束。每章開頭給新的有源動作，每章都有你／我。23個作者loop均列setup/payoff；c05只問導演要求，c06/c07給當事人工作要求與回應，不掛電影友情答案，仍待fresh原生讀者判斷。最後三句依序答案、留言題、訂閱理由，不預告下一支。

## 來源邊界

研究三檔固定SHA保留，原raw、索引、原後台快照與9份相關舊原件先核對後建立protected-inputs清冊。既有42筆下載及搜尋工具快取分開；本輪沒有新增raw下載。A01–A07只從已保全的官方／當事人原語段落補精確作者錨點，不改研究檔，也不是獨立核驗。

2017書籍特設頁是むぎわら的事後署名留言，不是1996同期或臨終紀錄；2019第三回起接手自述使用CoroCoro官方對談的搜尋工具快取，origin本輪HTTP503，沒有裝成原HTML200。1996逐頁上墨／ネーム／結局邊界仍未取得，不能編。回憶出版、上映、單行本與電子版日期分清；沒有讀完整130頁回憶書或160頁縮印腳本。藤本弘與合作人安孫子素雄分清；不使用臨終命令、單一總接班人、AI、欺詐代筆或公司內部審批傳說。D29只說官方豪華碟片的附件介紹列出腳本，不假稱本輪讀過附件。

## 畫面與預告回收

MiniMax image-01，look唯一為{"preset":"cute-mystery"}，無style／negative擴寫。全正文使用合法shot模板的匿名概念插圖，規劃插圖占比100%、卡片0，超過70%且無連續卡片。只出現匿名手部／背影、空白稿紙格紙、無字書、一般工具。英文prompt禁品牌、產品、真人名、logo、可讀字、真人肖像，尤其不出現可識別哆啦A夢角色、剪影、部位或招牌道具，也不複製漫畫、照片、電影、信件或真實文件。

唯一前向事件預告h04及回收b08所有拆分scene，完整原生image request相同。image-reuse-plan.json以目前source和Stage.imageKey做純本機重算，不是實際manifest或cache命中證明。正式製片先回收takes1；預告前核live cache與實檔SHA，miss即停，兩端各自judge，裁切後選定同file SHA並核組片引用才能成立。actual_same_asset_verified=false。

## 製作與交付

series target_minutes固定13。最終3101 native spokenUnits、135行、115個shot、23個有後續新答的作者loop；開場200、voiced CTA56，兩者均包含在3101內。刪相鄰重述後低於約3500的容量目標，保留容量風險；4.5units/s純口播算式689.11秒不是實聲。正常免費lint的完整結果見native-author-lint-r3.json；soft包括14.5分鐘的正常間隔估值、長shot估值、空白紙面概念重複與刻意同圖的相鄰回收。完整收據照保留，不能把機械節奏零警告當fresh讀者通過。

R2已真實完成native1 merge，shared HOLD是payoffs／no_recap／no_detour；R3刪除筆名旁枝與兩組重述，改寫無法用訪談回答的友情懸念。章名advisory及B單票scene_first不作本次改稿要求。R2 SOURCE PASS／verify僅留歷史，不沿用為R3核准；新SOURCE差分與fresh native2均待root另派，實際native計數保留1，本作者未準備或重抽新blind。

實聲body必須720–840秒，包含cold open及voiced CTA，排除新增5秒片頭與21秒v4片尾，共26秒。估算不能代替實聲，不降低13、不慢播、不插空白、不重述補時。聲音沿台灣STORY_VOICE_STYLE與正常Gemini Sulafat object；本片字典已自行走正常immutable初始化，僅1 version，念法仍待獨立審。

繁中主版試燒字幕加CC；預設後續八語en/ja/ko/es/pt/id/vi/th，保留乾淨主片、原圖、dry voice、M&E及source-bound CC/text。語言媒體均待中文成片後正常製作。5秒正式片頭放開場後；21秒正式v4片尾素材與版本待驗，沒有借舊片。

新slug為story-adapt-doraemon-after-fujiko-remake-20261025，作品族群仍為品牌故事，不以改前綴偷借預算。這支nonC新片獨立US$25精確帳戶、全片quote與protected admission均未建立；不借原帳戶、別集帳戶、歷史owner決定或批准。無paid/provider/backend/owner/Git操作。runtime在/workspace/work/brand-story-20261025/doraemon-audit/author-r3/free-runtime，media在repo與runtime外的/workspace/work/brand-story-20261025/doraemon-audit/author-r3/media。

## 當前狀態

這是R3作者候選，非獨立QA。SOURCE／fresh native雙讀者／念法／實聲與720–840秒／書面及實圖／owner所有關卡pending；作者沒有verify-1、自PASS、自verify或批准。免費正常lint為機械結構檢查，soft warnings照原樣保留。原舊媒體本機不可讀，不宣稱已保全、沒曾存在或曾獲本輪核准；本次新製作不以取回舊付費媒體為先決條件。
