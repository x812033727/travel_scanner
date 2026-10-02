# 世人忘我，死敵記我｜製作覆核與攝製設計

2026-10-01。本輪逐集核對40集的衝突、轉折、結尾、人物/道具狀態，並對照設定、opening_30_seconds、continuity_notes與上一輪修訂；未發現新增可確定的劇情矛盾。以下是可實作的攝製設計與風險控制，並非渲染、試聽、母語翻譯或正式站驗收。

來源绑定：`061c82d31f88119d8cf764765075d6821720861c5dff3f41bc04dad3e473307e`（SHA-256 of JSON.stringify(source)）。完整機器可讀資料在 [production-design.json](./production-design.json)，共40集、8名角色、6個開場鏡頭。

## 交付與核准邊界

先完成zh-TW台灣口音版；ja/ko/en先做名詞與發音預備，中文版鎖定後各自TTS與CC。所有字幕為可開關CC，沒有繁中或外語燒錄字幕。劇內文件、鐘與標示是物件；關閉CC時仍需由鏡頭和原稿台詞理解。現有README或舊setting中燒錄／五語CC描述依此次新授權改為共享 [profile](../../production-20261001/profile.json)，不讓過期規格回流。

採Gemini veo-3.1-lite-generate-preview，1080p/24fps每次8秒素材；主要行為一鏡一動作，剪取3–6秒，餘反應/插入另片。沒有referenceImages或extension；不可freeze補時。此批正片採clips-only：紙證與觀察也有可信的手部、視線或環境動作；重要文字先核對再合成到動態插鏡。仍圖只供前製animatic，不能混稱完成動畫。原生模型音訊不用作台詞主軌，後製分角色人聲、音效、環境、配樂。

## 拍攝語言

山門記憶懸疑武俠；石、木、紙的實物可信度高於光效，法術僅關鍵三次；失憶用行為距離演，不用白眼與畫面反覆閃白。

橋的安全側與破口側固定；十二節點沿同一盆地地圖，緩壓、拔銷、儲能裂開分開因果。江照左掌、祁硯右腕紅繩全劇不鏡像。

江照在被忘記時不每集哭求；祁硯的精確記憶藏在順手照顧，傷後轉左手劍要有重量；阿杳用自己寫下的事重新建立信任。

只E1/18/28借淵施契；E34普通修為注石，E37機械拆除不施契。祁硯童年空白是頭傷，紅繩切斷不逆向抹去已存記憶，結局不補回所有記憶。

## 開場0–30秒

來源：[source.mjs:502](./source.mjs#L502)、[source.mjs:540](./source.mjs#L540)。以下秒數是剪輯目標，實際TTS與成片尚未量測；每格內若列反打/插入，拆成單動作素材後剪接，不能要求模型一次完成整段蒙太奇。

| 時間 | 機位 | 畫面行為 | 對白意圖與聲音 |
| --- | --- | --- | --- |
| 0–5秒 | 中近景；橋面安全側同軸 | 江照把孩子推到母親安全側，左掌契痕僅作剛施術後消退。 | 胡娘問你是誰；內心短句表達剛救過。；木裂後收音，孩子只喘息無新增聲線。 |
| 5–12秒 | 雙人中景；祁硯落地後停機位 | 祁硯拔劍叫江照姓名，右腕紅繩仍在袖內。 | 江照問你還記得我，不先宣布他是唯一例外。；落地與劍出鞘各短，不連續打鬥。 |
| 12–18秒 | 手部近景；江照左側固定 | 江照用劍鞘支住鬆木，不再施法。 | 先讓人離開破口。；木壓聲，不再出契印音。 |
| 18–22秒 | 中景；祁硯同側固定 | 祁硯抓住繩索穩住安全側。 | 動作代對白。；繩緊與呼吸。 |
| 22–26秒 | 中景；母子已在穩定區 | 母亲抱緊孩子離開危險邊界。 | 不再讓孩子突然回到破口。；脚步離場。 |
| 26–30秒 | 紙本追捕令與雙人分切；眼平 | 祁硯亮出真追緝令。 | 你救了人，但這道令是真的。；展紙與指節壓石欄短響，無硬令牌碰撞；末尾留懸問不用假打斷。 |

## 角色造型與表演

本輪已完成characters[].shot_looks目錄及scene.data.character_looks逐鏡選擇的工具整合；下列完整外觀資料已可隨新製作bundle傳入工人。原始故事source保持不變，原有按集looks仍可並存。候選episodes不是整集覆寫命令；鏡頭照cue選造型，同一人物的臉與身份保持一致。工具與資料已具備，實際角色圖、動作、聲音及成片仍待驗收。

| 角色 / 候選ID | 涉及集 | 造型與切換條件 | 來源 |
| --- | --- | --- | --- |
| qi-yan / qi-yan-cord-hidden | E1、E2、E3、E4、E5、E6、E7、E8、E9、E10、E11、E12、E13、E15、E16、E17、E18、E19、E20、E21、E23、E26、E27、E28、E29、E30、E31、E32、E33、E34、E35 | Adult East Asian man, 28, upright lean silhouette, straight black hair in a high neat knot with a matte dark pin, defined brows and a small old scar above the right temple. He wears an ivory-grey fitted robe with long narrow sleeves, a black narrow belt and practical black boots. His sword has a plain rectangular guard. No crown or ornate shoulder armour. An intact red cord is fully hidden at the RIGHT wrist under the narrow sleeve. It must not be visible. 除E8洗衣、E23對圖、E26被瞥見局部揭露及E35切斷鏡頭外。 | [source.mjs:82](./source.mjs#L82)、[source.mjs:540](./source.mjs#L540) |
| qi-yan / qi-yan-cord-visible | E8、E23、E26、E35 | Adult East Asian man, 28, upright lean silhouette, straight black hair in a high neat knot with a matte dark pin, defined brows and a small old scar above the right temple. He wears an ivory-grey fitted robe with long narrow sleeves, a black narrow belt and practical black boots. His sword has a plain rectangular guard. No crown or ornate shoulder armour. An intact red cord is briefly visible at the RIGHT wrist where the sleeve is raised. 只指定揭露鏡；E8/23/26隨後再遮。 | [source.mjs:82](./source.mjs#L82)、[source.mjs:949](./source.mjs#L949) |
| qi-yan / qi-yan-cord-cut | E35、E36、E37、E38 | Adult East Asian man, 28, upright lean silhouette, straight black hair in a high neat knot with a matte dark pin, defined brows and a small old scar above the right temple. He wears an ivory-grey fitted robe with long narrow sleeves, a black narrow belt and practical black boots. His sword has a plain rectangular guard. No crown or ornate shoulder armour. No red cord on either wrist; a shallow right-wrist injury is covered discreetly. Use the sword in his LEFT hand. E35切后；紅繩另入江照紙包。 | [source.mjs:82](./source.mjs#L82)、[source.mjs:2558](./source.mjs#L2558) |
| qi-yan / qi-yan-healed-no-cord | E39、E40 | Adult East Asian man, 28, upright lean silhouette, straight black hair in a high neat knot with a matte dark pin, defined brows and a small old scar above the right temple. He wears an ivory-grey fitted robe with long narrow sleeves, a black narrow belt and practical black boots. His sword has a plain rectangular guard. No crown or ornate shoulder armour. No red cord on the body. Only a faint healed right-wrist mark, no fresh wound. 數周/三个月后日常。 | [source.mjs:82](./source.mjs#L82)、[source.mjs:2784](./source.mjs#L2784) |
| a-yao / a-yao-fresh-wrist | E7、E8、E11、E12、E14、E18、E19、E22、E24、E25、E27、E28、E29 | East Asian teenage girl, 17, small wiry frame, short uneven black bob tucked behind one ear, wide alert eyes, a patched dusty plum jacket over grey cotton trousers and woven shoes. A healed crescent scar sits on her right forearm; she carries a flat cloth pouch with a broken wooden name tag. Practical, fully covered clothing; no glamorous makeup or sexualised styling. A separate recent RIGHT-wrist chafe is discreetly dressed and healing; the permanent crescent forearm scar remains distinct. 兩標記距離分開，不把舊疤塗成新血傷。 | [source.mjs:144](./source.mjs#L144)、[source.mjs:889](./source.mjs#L889) |
| a-yao / a-yao-wrist-healed | E32、E38、E39 | East Asian teenage girl, 17, small wiry frame, short uneven black bob tucked behind one ear, wide alert eyes, a patched dusty plum jacket over grey cotton trousers and woven shoes. A healed crescent scar sits on her right forearm; she carries a flat cloth pouch with a broken wooden name tag. Practical, fully covered clothing; no glamorous makeup or sexualised styling. The right-wrist chafe has healed. Keep only the permanent crescent scar on the right forearm. 依鏡頭實際出場選用。 | [source.mjs:144](./source.mjs#L144)、[source.mjs:2383](./source.mjs#L2383) |
| shen-que / shen-que-badge | E2、E8、E9、E15、E20、E21、E25、E26、E28、E33 | East Asian man, 22, compact athletic build, short tied-back black hair with a broad fabric band, round face and a healed cut on the lower lip. He wears a slate-grey trainee robe with white shoulder piping and plain leather forearm guards. A narrow practice sword hangs on his left hip. The sect badge is pinned on the LEFT chest. E33拆徽前；其它沒出場集不為展示徽章造鏡。 | [source.mjs:206](./source.mjs#L206)、[source.mjs:598](./source.mjs#L598) |
| shen-que / shen-que-injured-badge | E28、E33 | East Asian man, 22, compact athletic build, short tied-back black hair with a broad fabric band, round face and a healed cut on the lower lip. He wears a slate-grey trainee robe with white shoulder piping and plain leather forearm guards. A narrow practice sword hangs on his left hip. A LEFT-leg injury and LEFT-chest sect badge. After the injury, a cane supports him; no running. E33使用杖，拆徽那一拍後改injured-no-badge。 | [source.mjs:206](./source.mjs#L206)、[source.mjs:2142](./source.mjs#L2142) |
| shen-que / shen-que-hurt-no-badge | E33、E36 | East Asian man, 22, compact athletic build, short tied-back black hair with a broad fabric band, round face and a healed cut on the lower lip. He wears a slate-grey trainee robe with white shoulder piping and plain leather forearm guards. A narrow practice sword hangs on his left hip. A LEFT-leg injury requires a cane. No sect badge on the chest after removal; he stays at a fixed signal post. E33拆徽後、E36固定信號站不奔跑，E40才康復。 | [source.mjs:206](./source.mjs#L206)、[source.mjs:2442](./source.mjs#L2442) |
| shen-que / shen-que-recovered | E40 | East Asian man, 22, compact athletic build, short tied-back black hair with a broad fabric band, round face and a healed cut on the lower lip. He wears a slate-grey trainee robe with white shoulder piping and plain leather forearm guards. A narrow practice sword hangs on his left hip. His left leg has healed after three months. No cane and no sect badge. 三月後，不自動復職。 | [source.mjs:206](./source.mjs#L206)、[source.mjs:2843](./source.mjs#L2843) |
| qin-lu / qin-lu-no-keys | E33 | East Asian man, 43, broad-shouldered heavy frame, receding slicked-back black hair, close-shaven square face. He wears a dark rust robe under a short black sleeveless coat, has ink stains on his right thumb. His left sleeve has three parallel repair stitches. No mask, flowing hair or ceremonial crown. No keys in his hands or at his belt after handing them over. E33交鑰匙後鏡頭；E39只有書面證詞不造本人回憶鏡。 | [source.mjs:233](./source.mjs#L233)、[source.mjs:2442](./source.mjs#L2442) |

## 道具與空間連戲

依[source.mjs:36](./source.mjs#L36)、[source.mjs:2951](./source.mjs#L2951)；特殊道具以獨立參考圖與交接鏡追蹤，列出的外觀差異屬美術選擇，不能改原有劇情因果。

| ID | 唯一性 | 狀態 | 持有人與拍法 |
| --- | --- | --- | --- |
| contract | 江照左掌契印／借淵口令／施後痛；只三次 | E1第一次、E18第二次、E28第三次；E35停手未施，E34/37不是契術 | 江照施術；盆地十二節點只抹別人對江照的個人記憶；左掌按+口令+痛三件同集核對；法術音不可在普通注力/拆機復用。 |
| red-cord | 祁硯右腕完整紅繩與完整例外效力 | E1–7藏；E8露再藏；E23露收；E26瞥見收；E35斷→紙包；E39抽屜；E40無 | 祁硯佩→元衡切→江照紙包→抽屜；切斷不追溯抹記憶；避免鏡像或外露全劇；特寫有袖遮/取出/收回三態且不增加施術。 |
| written-memory | 紙證不消失、技能不消失，私人情感/經歷才被域内抹除 | 阿杳E18後讀自己的記錄；沈闕E28後讀傷前筆記；E39不寫假回憶 | 各人寫自己的事，見證不能充當主觀恢復；記錄與重建關係反應分鏡；小孩畫背面E32加日期再交回。 |
| prison-history | 羈押採集囚犯自傳記憶與江照域術兩種機制 | 母親姓名E14已找到；E24是死日對照；祁童年空白為頭傷不由契印治好 | 秦錄原件E20帶走留副本；E33原件安全保管；文件真相分層讀，禁止用滿段回憶重演把失去記憶補回。 |
| tools | 陳渡自用腰尺槌與給江照的備用工具袋兩套 | E12備袋到江→E30還到袋；E36袋出第一銅銷；E37其餘兩銷 | 陳腰工具從未空，江袋尺/木槌/拔銷器不凭空变金屬重鎚；先放壓為零再拔；每鏡只一操作，無導火索式瞬間全域崩塌。 |
| authority | 追緝令、祁私人印/繼承令、沈左胸徽、秦鑰匙是四套 | E9祁交私人印；E26交繼承令；E33沈拆徽秦交鑰匙；E40無徽 | 各本人交自己的物，不混稱門派令牌；不同材質大小；沈徽左胸，秦钥右腰，交出後不重生。 |
| network | 十二原有節點與70/30能量帳、普通修為能量石 | E20才知分配；E27模型試失敗；E34注力失大部分修為；E38回報板延遲不是節點故障 | 阿杳/陳渡等按本份守位，沈傷腿在固定信號站；零壓读值→拔三銷→儲能裂→逐節點檢查，少一环不能剪成奇蹟。 |

## 全40集攝製檢查

每集的完整cast、location、look候選、prop與CC檢查在JSON；下表只放該集獨有的主要拍法與最容易拍錯的地方。主鏡頭以一個主要動作為素材，其餘並列動作拆insert/反應。

| 集 | 主要鏡頭 | 風險 → 控制 | 來源 |
| --- | --- | --- | --- |
| 01 救過她，她卻問我是誰 | 救人後被母親當陌生人 | E1第二次塌橋又施一次法 → 支木抓繩普通動作，不再口令契印 | [source.mjs:540](./source.mjs#L540) |
| 02 真印不替內容作證 | 紙本追捕令的真印與內容疑問分開 | 證明令真等於指控也真 → 祁只承認令格式，爭取一天查證 | [source.mjs:598](./source.mjs#L598) |
| 03 把名字再說一次 | 祁說出未寫過的救人動作 | 胡娘短期見過被當舊記憶復活 → 區分新見面與舊情感，畫仍保存 | [source.mjs:655](./source.mjs#L655) |
| 04 劍停在舊地方 | 過招在卸肩步法停住 | 製造原稿沒有的新傷 → 只有示範卸力，祁右肩無新增傷 | [source.mjs:715](./source.mjs#L715) |
| 05 不是字自己消失 | 石碑凿痕被尺量出 | 字跡魔法消失破紙證規則 → 物理磨凿與舊新工具痕對比 | [source.mjs:771](./source.mjs#L771) |
| 06 罪狀比裂縫還新 | 舊封條與新罪日並排 | 此時已知70/30或全域解法 → 只提示壓力與取圖條件，數據留E20 | [source.mjs:830](./source.mjs#L830) |
| 07 妖物的家戶木牌 | 阿杳被帶走時藏家庭木牌 | 新腕傷變永久月牙疤 → 腕與前臂分開畫，原牌藏袋內 | [source.mjs:889](./source.mjs#L889) |
| 08 袖裡那條褪色紅繩 | 洗袖露出右腕紅繩又遮住 | 紅繩從此每鏡外露 → 露一次再藏，圖樣僅提示未知關聯 | [source.mjs:949](./source.mjs#L949) |
| 09 我簽過這張令 | 私人印放到檔案桌上 | 繼承令提前於E9交掉 → 只是私人印，繼承令留到E26 | [source.mjs:1008](./source.mjs#L1008) |
| 10 橋市日誌與騎縫號 | 連號與日記證明先下令三日 | 紙證找到就取消追令 → 追令仍在，人物行動仍受限 | [source.mjs:1065](./source.mjs#L1065) |
| 11 這裡不問姓名 | 阿杳帶兩成人走換班外廊 | 三人穿過只有小孩能過的通風道 → 此集是外門路，窄道單人留E12 | [source.mjs:1134](./source.mjs#L1134) |
| 12 一塊護身佩換兩道門 | 阿杳獨穿舊通風口拿到工具 | 成人縮身鑽同洞或陳工具消失 → 只有阿杳通過；給江為備用一套 | [source.mjs:1192](./source.mjs#L1192) |
| 13 你一直不吃那一口 | 祁順手挑走碗中苦葉 | 習慣變回憶完全恢復 → 不補童年畫面，保留祁說不清 | [source.mjs:1253](./source.mjs#L1253) |
| 14 拓本比名冊老 | 家戶紀錄第一次露出母名 | 母親新增回憶聲線 → 不造母親對白，只讀客觀紀錄 | [source.mjs:1311](./source.mjs#L1311) |
| 15 這份賞，我不領 | 未開賞瓶與牢房瓶批號一致 | 演員喝藥才發現毒多新情節 → 拒收且未開封，比號即可 | [source.mjs:1369](./source.mjs#L1369) |
| 16 南渡陣腳在滲霧 | 元衡把真危險和控制混在一起 | 把真裂霧危險全判造假 → 留真威脅，機械分管只為方案 | [source.mjs:1426](./source.mjs#L1426) |
| 17 那年是我簽的 | 江承認十五年前救男孩簽契 | 祁當場恢復童年  → 仍有頭傷空白，客觀記錄不當主觀回想 | [source.mjs:1487](./source.mjs#L1487) |
| 18 先寫下你看見的 | 第二次借淵後阿杳讀自己字跡 | 失憶把技能/文字全抹掉 → 保留她能讀與能行動，只關係生疏 | [source.mjs:1544](./source.mjs#L1544) |
| 19 自己寫的那張紙條 | 模型操作熟練但情感陌生 | 能做事就等於記得江 → 事實讀取和情感無法回來並列 | [source.mjs:1602](./source.mjs#L1602) |
| 20 分流總帳上的兩條管路 | 兩管70/30帳與獎賞名單亮出 | 比例早於本集解出或原件留桌 → 秦帶原件走，已保存複本仍在 | [source.mjs:1660](./source.mjs#L1660) |
| 21 三筆賞賜的日期 | 祁保留自己收賞日期不擦去 | 自證清白改删不利記錄 → 原數據完整，後面才正式轉移能量 | [source.mjs:1733](./source.mjs#L1733) |
| 22 她的名字不能再收走 | 先前審查紙挡住再拘捕 | 未有任何程序卻敵人突然停手 → 靠已有審查效力，阿杳保下半账 | [source.mjs:1791](./source.mjs#L1791) |
| 23 底簿下頁與頭傷診記 | 下半帳與頭傷日對上紅繩圖 | 陳渡成親見童年全知角色 → 來源是記錄，紅繩不治頭傷 | [source.mjs:1849](./source.mjs#L1849) |
| 24 把空白一格一格填回去 | 死日對照母親已知姓名 | E14已知姓名E24又當首揭 → 新資訊是死日；陳新碗不靠記得舊餐 | [source.mjs:1907](./source.mjs#L1907) |
| 25 禁止你記得 | 證物箱封上而未焚毀 | 箱已封卻又留散頁給對手 → 沈堅持封存，人證材料交代清楚 | [source.mjs:1966](./source.mjs#L1966) |
| 26 把位置還給你 | 祁把繼承令交回後全價買材料 | 紅繩跟權力一同失效 → 只是權力失去，紅繩完整仍保記憶 | [source.mjs:2024](./source.mjs#L2024) |
| 27 先保住這一尺 | 歪銷在零壓後被尺量出 | 帶壓拔銷或首測就成功 → 失敗先撤壓，修正需再測 | [source.mjs:2083](./source.mjs#L2083) |
| 28 忘了也能把字留下 | 第三次借淵救下沈的左腿 | 左腿受傷成右腿或第四次施術 → 前筆記後遺忘，江此後不能站穩 | [source.mjs:2142](./source.mjs#L2142) |
| 29 第一輪交班 | 阿杳維持材料班次 | 元衡已交記憶箱但E30又取 → 此時只发索引，箱仍在堂內 | [source.mjs:2198](./source.mjs#L2198) |
| 30 拿他，換回你的一生 | 江隔匣驗看仍接儲層的真記憶 | 箱取到等於失憶已治 → 匣內記憶片段未離儲層，江隔匣驗看並拒換；祁只交回備用工具袋 | [source.mjs:2257](./source.mjs#L2257) |
| 31 店家墊料的那一夜 | 十二節點由各人出資認領 | 江重傷仍扛梁奔跑 → 他說方案與條件，其他人搬運 | [source.mjs:2326](./source.mjs#L2326) |
| 32 先走出去的人 | 畫背新日期留下又還回去 | 加日期改畫原內容或阿杳腕仍新血 → 背面落日，腕已好舊前臂疤仍在 | [source.mjs:2383](./source.mjs#L2383) |
| 33 我不記得，但這是我的字 | 沈拆左胸徽，秦交右腰鑰匙 | 同一令牌代表所有人身份 → 各自物件獨立，秦交後不再掛腰 | [source.mjs:2442](./source.mjs#L2442) |
| 34 兩處遲到的回牌 | 普通修為注石讓兩人失大部分力量 | 被畫成第四次契印抹記憶 → 無左掌按/口令；損大部分非全部功力 | [source.mjs:2499](./source.mjs#L2499) |
| 35 窄梯前放下的手 | 右腕繩被切後江停在施契前 | 切繩追溯抹祁記憶或江再施 → 没有新施術，祁已有記憶仍存，改左手持劍 | [source.mjs:2558](./source.mjs#L2558) |
| 36 不用護盾的那一劍 | 沈固定站給信號後零壓拔第一銷 | 沈傷腿奔跑或有壓硬拔 → 拄杖固定岗，工具袋第一銷有來源 | [source.mjs:2615](./source.mjs#L2615) |
| 37 最後兩枚銅銷 | 其餘兩銷拔出才讓儲能裂開 | 新法術大爆炸救所有記憶 → 機械拆除，元衡活擒，舊記憶不返 | [source.mjs:2671](./source.mjs#L2671) |
| 38 十二處的第一輪測片 | 一塊遲到回報板補齊巡檢 | 通信延遲又造新節點故障 → 十二節點已驗，遲到是繩路通訊 | [source.mjs:2726](./source.mjs#L2726) |
| 39 公開對帳的那一天 | 抽屜放斷繩，新日記只寫真事 | 秦本人忽现或假回憶當治療 → 秦僅書面證詞，未記得的事不冒寫 | [source.mjs:2784](./source.mjs#L2784) |
| 40 橋市的兩碗麵 | 苦葉由江自己要求挑掉 | 最後以記憶全回來大團圓 → 祁無紅繩、沈無徽已康復；新的熟悉是三月相處 | [source.mjs:2843](./source.mjs#L2843) |

## 聲音、四語與CC

以下voice沿用來源合適提案，未試聽未驗收。zh-TW用自然台灣國語，音量不替代表演；其他三語先按同一角色身份試錄，母語審聽後可調voice。外語人名是發音草案，日/韓字形不當正式譯名定案。

| 角色 | 聲線與表演 | zh-TW / ja / ko / en發音草案 |
| --- | --- | --- |
| 江照 / jiang-zhao | Charon；臺灣國語；偏低、克制、有疲倦的乾笑；擬定 casting 未試聽。 | Jiāng Zhào / ジアン・ジャオ / 장 자오 / Jiang Zhao |
| 祁硯 / qi-yan | Orus；臺灣國語；字尾穩、語速稍慢，不靠大吼演情緒；擬定 casting 未試聽。 | Qí Yàn / チー・イエン / 치 옌 / Qi Yan |
| 元衡 / yuan-heng | Fenrir；臺灣國語；平聲威壓、少量氣音，不用誇張奸笑；擬定 casting 未試聽。 | Yuán Héng / ユエン・ホン / 위안 헝 / Yuan Heng |
| 阿杳 / a-yao | Kore；臺灣國語；清楚、警覺，不作幼童音；擬定 casting 未試聽。 | Ā Yǎo / アー・ヤオ / 아 야오 / A Yao |
| 陳渡 / chen-du | Puck；臺灣國語；粗礪溫暖、偶爾短促幽默，避免滑稽老頭；擬定 casting 未試聽。 | Chén Dù / チェン・ドゥー / 천 두 / Chen Du |
| 沈闕 / shen-que | Iapetus；臺灣國語；年輕男聲，清朗而節制，疑惑時不拖長尾音；擬定 casting 未試聽。 | Shěn Què / シェン・チュエ / 선 취에 / Shen Que |
| 秦錄 / qin-lu | Algenib；臺灣國語；沙啞、急促斷句，照冊念時語調平板；擬定 casting 未試聽。 | Qín Lù / チン・ルー / 친 루 / Qin Lu |
| 胡娘 / hu-niang | Aoede；臺灣國語；俐落溫厚、自然生活感；擬定 casting 未試聽。 | Hú Niáng / フー・ニアン / 후 냥 / Hu Niang |

- 借淵聲標只三次，普通能量石使用不同低而穩定聲；E35預備動作不觸發完整聲標。
- 紅繩沒有持續心跳式超能力提示；揭露時使用真布/繩摩擦，避免前段聲音劇透。
- E36/37先卸壓歸靜再木槌/拔銷，因果可在單聲道聽懂；結尾用煮食自然聲。

- 忘記江照的個人記憶≠失去識字、技能、客觀證據；四語術語表必須把記憶/記錄/認識/回想分開。
- 借淵保留專名與發音；僅在來源實際啟動／說出的段落錄對應take，依當下狀態演，不為重用而補造啟動。普通注力不可翻成借淵或spell同義。
- 紅繩右腕、契印左掌、沈左腿與左胸徽、阿杳右腕/右前臂每語系方向一致，不翻鏡。

旁白依來源[source.mjs:34](./source.mjs#L34)，不得跟本劇角色共用聲線。字幕出軌後逐條查說話者、標點、當地閱讀速度和轉場；翻譯要對每語音軌對時，不復制繁中CC時間碼。關鍵資訊不只靠左右聲道，必測mono與手機外放。

## 預告素材與留存

E1被救母親問你是誰、祁喊姓名、真追令；E5石碑被凿痕作最後一個新問題。禁紅繩完整圖、70/30、祁童年頭傷、E35斷繩和最終不恢復答案。

每次失憶後用同物不同反應回收情緒：母子畫、阿杳字、沈傷前紙。E20後高規則段每集一項證據對一個犧牲，E27失敗與E34失修為確保修法有成本。

先驗前5秒能聽懂衝突、30秒取得第一回報，再看30秒/1分鐘/3分鐘留存、換篇退出與實際點擊觀看的落差；不用空剪節奏或故意截斷已說一半的答案換點擊。百萬點閱是目標，沒有保證。

## 待完成驗收

- 紅繩藏／露／切斷、拆徽和交鑰匙已具完整命名造型與逐鏡工具，待實際畫面驗收。 按qi-yan-cord-hidden/visible/cut、shen-que-injured-badge/hurt-no-badge、qin-lu-no-keys切鏡；生成後查左右側、受傷後持劍手與已交出物件不重生。（E8、E23、E26、E33、E35、E36、E40）
- 三次術法、普通注力、機械卸壓需實際音色/手機外放驗證。 聽感混同會直接破壞世界規則。（E1、E18、E28、E34、E35、E36、E37）
- 阿杳（a-yao）明確17歲，Veo Lite I2V未驗證可生成其入鏡畫面。 目前首格I2V的allow_adult能力不代表允許未成年人顯影；不能把角色改為成年人，也不能以背影、局部、卡通風格或不提年齡當可保證捷徑。需經核可的手繪動畫或合法支援該年齡的供應商先做pilot、確認能力與交付再排量。僅畫外配音不因此自動受阻，逐鏡按實際可見人物判斷。（E7、E8、E11、E12、E14、E18、E19、E22、E24、E25、E27、E28、E29、E32、E34、E38、E39）
- E1無cast ID的被救孩子明確入鏡，不能直接以Lite全動態開拍。 具體年齡未載，不能捏造數字或新增角色年齡。整E1 provider constraint等待合法可支援未成年人的手繪/供應商pilot；無對白、背影或只拍被拉住不構成已驗證捷徑。（E1）
- 江照與祁硯現時28歲，來源另明訂兩人13歲的少年客觀回望。 來源source.mjs:2954、2961、2965有少年回望與13歲日期；E17、E23是相關往事揭露，但尚未把13歲入鏡分配到具體鏡頭。成人ID不全域標min13，不能把其40集全部誤擋；任何13歲回望須先指定獨立look、集與鏡，再驗證未成年動畫路徑。當前未建立未綁集的child look，亦不得把童年改成成人。（E17、E23）

- 使用已備妥的逐鏡造型資料做角色圖與動畫小樣，查同臉、方向、道具接觸與交接後狀態。
- zh-TW實際TTS、開場30秒剪輯、40集聲音/CC/全片驗收；之後ja/ko/en母語聽校。
- source變更需重驗hash；工具完成不代表付費生成、正式匯入、核准或上架已執行。

## 供應商能力：未成年入鏡尚未驗證

目前Veo 3.1 Lite的首格I2V路徑使用allow_adult；依[官方Veo能力文件](https://ai.google.dev/gemini-api/docs/veo)，不能把它當成未成年入鏡已支援。本輪只新增限制與來源，不改人物年齡、劇情或現有配音。

| 角色 ID | 明確視覺年齡 | 登記出場集（非每鏡都入鏡） | 年齡來源 |
| --- | --- | --- | --- |
| 阿杳 / a-yao | 17歲 | E7、E8、E11、E12、E14、E18、E19、E22、E24、E25、E27、E28、E29、E32、E34、E38、E39 | [source.mjs:147](./source.mjs#L147)、[source.mjs:148](./source.mjs#L148) |

江照/祁硯現時28歲；source.mjs:2954、2961、2965明訂客觀少年回望與當時13歲。E17、E23涉及往事揭露，但回望未排到明確鏡頭，所以不把成人ID全域min_age設13，也不建立未綁集的child look。確定少年入鏡時要獨立標記造型、集/鏡並先驗證製作路徑。E1另有無cast ID、未給確切年齡的被救孩子（source.mjs:505、2972）；已在episode.video_constraints標整E1停止等待，避免只查登記角色ID漏掉胡娘抱孩子的鏡頭。

character.video_constraints標記實際未成年人物；只有畫外聲不自動禁止中文配音。分鏡需區分說話者與畫面內人物，但不能靠背影、局部、卡通畫風或省略年齡宣稱繞過限制成功。必須保留原設年齡，先選手繪動畫或合法可支援相應年齡的供應商，做含該人物的pilot確認能力與效果再放量。此批不能宣稱已可直接全400集拍完；通過離線設計檢查也不代表供應商或成片已驗收。

## 2026-10-02 配音與聲音細節覆核

本輪只有來源文字與製作設計覆核，沒有實際TTS、試音、SFX音檔或成片驗收。新增performance_states、audio_cues、audition_scenes每筆均為proposed，綁定集數與來源。source_excerpt只供語境，不能整段念成台詞；line_samples僅逐字引用已有原台詞，其餘試音段落待本集定稿取樣。

- E1/E2真印追捕令改回紙本，展紙／壓石欄，E26繼承令牌仍是另一道具。
- 借淵專名一致不代表每次狀態都克隆同一take；E1已啟動後開始，E35/E37不加口令或第四次啟動。
- E1/E18/E28顫手、咳喘、短暫不能站立各自綁集；E34普通注力不作守淵。

### 角色表演狀態

| 角色 / state | 集數 | 演出重點 | 來源 |
| --- | --- | --- | --- |
| jiang-zhao / jiang-first-aftermath | E1 | 剛施法後虛弱、左手短暫顫抖；氣短但仍指引繩索救援；開場已在啟動後，不額外念借淵造成第二次。 | [source.mjs:589](./source.mjs#L589) |
| jiang-zhao / jiang-second-aftermath | E18 | 跪地咳喘、左掌灼痛；咳喘在救援句間，一次啟動到事後脫力，不反覆念口令。 | [source.mjs:1593](./source.mjs#L1593) |
| jiang-zhao / jiang-last-aftermath | E28 | 修為再減、短暫不能站；短氣少詞仍有還筆的主動性，不演死亡或突然滿力。 | [source.mjs:2189](./source.mjs#L2189) |
| jiang-zhao / jiang-low-power-tools | E34、E37 | 低修為仍能走路、用工具；動作後换氣，不把手工具節奏當吟唱；E37先卸壓才拆銷。 | [source.mjs:2549](./source.mjs#L2549)、[source.mjs:2717](./source.mjs#L2717) |
| qi-yan / qi-position-returned | E26 | 失去繼承位補給，仍有普通修為；交令牌句尾完整、承責而非賭氣；紅繩此時仍未斷。 | [source.mjs:2074](./source.mjs#L2074) |
| qi-yan / qi-injured-remembers | E35 | 右腕淺傷、紅繩斷，仍有記憶；短吸氣但自然叫江照，不突然陌生或記憶倒帶。 | [source.mjs:2606](./source.mjs#L2606) |
| a-yao / ayao-writing-not-recognition | E18 | 17歲，認得自己字但不認得江照；轉成禮貌陌生，不變失語、不識字或另一人格；扶人仍有同情。 | [source.mjs:1593](./source.mjs#L1593) |
| chen-du / chen-measures | E16 | 左膝不適，仍以普通測片判讀；58歲清楚敏捷，走階短吸氣而非全程顫音；與元衡的權威語氣分開。 | [source.mjs:1478](./source.mjs#L1478) |
| shen-que / shen-paper-evidence | E28 | 左小腿傷，只憑自己字相信救援；痛不蓋證據句，不突然恢復親歷記憶或直接倒戈。 | [source.mjs:2189](./source.mjs#L2189) |

### 聲音提示

- **rival-e01-paper（E1；foley）**：追捕令是紙上真印：展紙、壓石欄，不是金屬令牌；接E2／E9／E10同件紙證。 E26繼承令牌另設形狀與音色，不混物。 來源：[source.mjs:548](./source.mjs#L548)。
- **rival-e26-token（E26；dialogue）**：交繼承令牌才可用硬物短接觸，錯開受賞頁／責任句；不是交還或撕毀紙本追捕令。 來源：[source.mjs:2029](./source.mjs#L2029)。
- **rival-e18-second（E18；effect）**：第二次啟動聲標只一輪，繩索與事後咳喘分段；不每切鏡重播起動或添口令。 來源：[source.mjs:1549](./source.mjs#L1549)。
- **rival-e28-last（E28；effect）**：第三次最後啟動與普通拖索拉人分因果；沈闕醒來只認紙證，無記憶恢復鈴聲。 來源：[source.mjs:2147](./source.mjs#L2147)。
- **rival-e34-ordinary（E34；dialogue）**：普通注石用穩定底層，無借淵口令／完整聲標；十二回牌朗讀時降低底層。 來源：[source.mjs:2504](./source.mjs#L2504)。
- **rival-e35-no-activation（E35；dialogue）**：按掌後放下不帶啟動聲，不把「沒有喊出借淵」敘述念成口令。 斷繩真布聲、無抹除聲；祁仍認識江，右腕傷非昏迷。 來源：[source.mjs:2563](./source.mjs#L2563)。
- **rival-e37-tools（E37；foley）**：先壓力歸零，再量尺／拔銷／木槌各對動作，無施法聲。 最後笑聲只依定稿，不能新增可辨人物台詞；祁喊江照是現場。 來源：[source.mjs:2676](./source.mjs#L2676)。

### 待實作的試音段落

- **rival-four-men／E16**：jiang-zhao、qi-yan、yuan-heng、chen-du。取定稿測片、真危險及迫害解法爭論，同場男聲不全壓成一種古風低音。 驗收要聽：盲聽可分克制、查證、條件威壓和材料判讀。 元衡非低吼臉譜，膝傷不蓋量測，無新增借淵。 來源：[source.mjs:1431](./source.mjs#L1431)。
- **rival-broken-cord／E35**：jiang-zhao、qi-yan、yuan-heng。定稿取繩斷、放手、仍叫名字段；呼吸代替旁白重講規則。 驗收要聽：不會誤聽第四次啟動或立刻記憶消失。 右腕傷仍可說话，叫名不陌生，江沒有喊借淵。 來源：[source.mjs:2563](./source.mjs#L2563)。

先完成zh-TW台灣口音乾聲與多人辨識，再做通訊／環境／音樂處理、mono與手機外放。不同voice_name或文字規則不能代替試聽。逐鏡聲音、造型、道具須和實際演出對上，CC只作獨立可開關軌；ja/ko/en在中文版定案後各自配音、重新配時及母語聽校。本輪沒有修改來源、歷史版本或正式站，不代表新增設計已同步後台。
