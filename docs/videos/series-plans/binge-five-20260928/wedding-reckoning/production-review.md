# 喜宴未散，清算開始｜製作覆核與攝製設計

2026-10-01。本輪逐集核對40集的衝突、轉折、結尾、人物/道具狀態，並對照設定、opening_30_seconds、continuity_notes與上一輪修訂；未發現新增可確定的劇情矛盾。以下是可實作的攝製設計與風險控制，並非渲染、試聽、母語翻譯或正式站驗收。

來源绑定：`f64f1b02f5cd04d95675fabe1dca6af27fd0cae983bb23ca3a6f4fc22cfdf701`（SHA-256 of JSON.stringify(source)）。完整機器可讀資料在 [production-design.json](./production-design.json)，共40集、8名角色、6個開場鏡頭。

## 交付與核准邊界

先完成zh-TW台灣口音版；ja/ko/en先做名詞與發音預備，中文版鎖定後各自TTS與CC。所有字幕為可開關CC，沒有繁中或外語燒錄字幕。劇內文件、鐘與標示是物件；關閉CC時仍需由鏡頭和原稿台詞理解。現有README或舊setting中燒錄／五語CC描述依此次新授權改為共享 [profile](../../production-20261001/profile.json)，不讓過期規格回流。

採Gemini veo-3.1-lite-generate-preview，1080p/24fps每次8秒素材；主要行為一鏡一動作，剪取3–6秒，餘反應/插入另片。沒有referenceImages或extension；不可freeze補時。此批正片採clips-only：紙證與觀察也有可信的手部、視線或環境動作；重要文字先核對再合成到動態插鏡。仍圖只供前製animatic，不能混稱完成動畫。原生模型音訊不用作台詞主軌，後製分角色人聲、音效、環境、配樂。

## 拍攝語言

象牙白與冰藍婚宴、土灰橘線倉區、暖灰尾聲；文件只拍一項差異和一個作決定的人，不把120分鐘拍成翻頁簡報。

婚宴知棠在畫面左、承川右、中央桌原件靠遠端；老倉圖固定南主門、東安全出口、北備用出口，跨方位前先補空間全景。

知棠先手抖再停筆；妹妹由護袋、護地址到推資料夾共同決策。反派先維持體面，失控用呼吸變化而非全程怒吼。

E1現世婚紗有頭紗、E2–3婚紗無頭紗、E4後褲裝；E1/5/15前世火場褲裝。銀方錶與三份授權文件均有唯一物件身分。

## 開場0–30秒

來源：[source.mjs:526](./source.mjs#L526)、[source.mjs:562](./source.mjs#L562)。以下秒數是剪輯目標，實際TTS與成片尚未量測；每格內若列反打/插入，拆成單動作素材後剪接，不能要求模型一次完成整段蒙太奇。

| 時間 | 機位 | 畫面行為 | 對白意圖與聲音 |
| --- | --- | --- | --- |
| 0–5秒 | ECU→CU；鎖定筆的金屬反光後小幅拉開 | 火光映在筆上，褲裝知棠貼住封閉南主門；無火焰吞人 | 知棠說原稿第一句；是親歷記憶；近呼吸、遠火聲，不加慘叫 |
| 5–11秒 | CU；門縫固定視角 | 門外只見承川半張臉和金領帶夾 | 承川依原稿說她簽完便沒有用途；台詞乾聲、門外微鈍化，不另加鎖門操作 |
| 11–16秒 | ECU；同角度match cut | 同一支完好筆懸在婚宴簽署席，現世婚紗頭紗進畫面邊緣 | 承川催簽可用上一聲線延續，知棠先不答；火聲切斷；室內宴會底聲與一口吸氣 |
| 16–20秒 | MCU；緩慢push-in | 知棠停筆，視線落到展示副本；原件在遠端完整可辨 | 無新解釋句；把拒簽決定留給動作；婚宴鋼琴減弱，筆尖未落紙 |
| 20–25秒 | CU insert；固定斜俯拍避免多手 | 先交代完整原件，再單獨拍撕開標示展示副本的頁；另一手按住原件 | 這字我不簽；字樣是道具內容不是燒錄字幕；單一撕紙聲，鋼琴停 |
| 25–30秒 | MCU；人物與完整原件同框 | 知棠抬眼面對承川，撕頁留桌；不在此提前拍完整副本交付 | 我母親的公司，不是嫁妝；拒簽先兌現；一句結束後留短室內底聲 |

## 角色造型與表演

本輪已完成characters[].shot_looks目錄及scene.data.character_looks逐鏡選擇的工具整合；下列完整外觀資料已可隨新製作bundle傳入工人。原始故事source保持不變，原有按集looks仍可並存。候選episodes不是整集覆寫命令；鏡頭照cue選造型，同一人物的臉與身份保持一致。工具與資料已具備，實際角色圖、動作、聲音及成片仍待驗收。

| 角色 / 候選ID | 涉及集 | 造型與切換條件 | 來源 |
| --- | --- | --- | --- |
| zhitang / zhitang-bride-veiled | E1 | East Asian woman, 28, oval face, straight shoulder-length black hair tucked behind the left ear, dark brown eyes, small silver rectangular watch; An ivory wedding gown and veil; veil remains on in every present-time shot of E1. 只限E1現世；同集前世需shot級variant，不可全episode覆蓋。 | [source.mjs:51](./source.mjs#L51)、[source.mjs:562](./source.mjs#L562) |
| zhitang / zhitang-bride-unveiled | E2、E3 | East Asian woman, 28, oval face, straight shoulder-length black hair tucked behind the left ear, dark brown eyes, small silver rectangular watch; An ivory wedding gown without a veil. E2第一鏡起無頭紗，E3仍未換裝。 | [source.mjs:51](./source.mjs#L51)、[source.mjs:620](./source.mjs#L620) |
| zhitang / zhitang-watch-off | E40 | East Asian woman, 28, oval face, straight shoulder-length black hair tucked behind the left ear, dark brown eyes, ivory tailored trouser suit. No watch on either wrist; the unique silver rectangular watch has been removed to the table. 只限E40落筆那一拍，原稿優先避腕構圖，仍防模型補回第二只錶。 | [source.mjs:51](./source.mjs#L51)、[source.mjs:2837](./source.mjs#L2837) |
| zhixia / zhixia-arm-dressed | E35 | East Asian woman, 23, round face, short black bob with one copper hair clip on the right, warm brown eyes, dark teal cardigan and cream shirt, plain canvas shoulder bag. A small clean dressing covers the left forearm after rescue; light smoke soiling, no visible wound. 救出後才有紗布；E35救出前不可先出現。 | [source.mjs:86](./source.mjs#L86)、[source.mjs:2555](./source.mjs#L2555) |
| zhixia / zhixia-healed | E39、E40 | East Asian woman, 23, round face, short black bob with one copper hair clip on the right, warm brown eyes, dark teal cardigan and cream shirt, plain canvas shoulder bag. A faint healed mark on the left forearm is only glimpsed at the sleeve edge; no dressing or fresh wound. 數月後已恢復，疤只在袖緣一閃不特寫。 | [source.mjs:86](./source.mjs#L86)、[source.mjs:2780](./source.mjs#L2780) |

## 道具與空間連戲

依[source.mjs:36](./source.mjs#L36)、[source.mjs:2943](./source.mjs#L2943)；特殊道具以獨立參考圖與交接鏡追蹤，列出的外觀差異屬美術選擇，不能改原有劇情因果。

| ID | 唯一性 | 狀態 | 持有人與拍法 |
| --- | --- | --- | --- |
| documents | 三份授權文件 | 展示副本E1撕；原件E2封；完整副本E3簽收 | 公證人保原件，許聞保另存副本；排版後製三種不同頁角標，不畫模型亂碼；同框可見未撕原件。 |
| watch | 母女共用的同一只銀方錶 | 母親舊影像→知棠常戴→E40桌上 | E40簽約時由知棠取下；桌上錶與腕上不可並存；手部鏡避腕或shot variant。 |
| rings | 新娘婚戒與男方婚戒是兩物 | E1退顧家女戒；E23出售她付款男戒 | 女戒回承川，男戒到E23前一直由知棠持有；兩戒盒色/形可作製作區分，不改所有權。 |
| fire-map | 老倉三出口與固定對講 | E11列項；E26實測；E33接通；E35改北口 | 淑雲安全側，知夏東側固定點；E30–35重疊時間用場景牌與相同煙濃度對位；移動後不續固定對講。 |
| evidence-box | 副本箱、舊案帳箱 | E29裝副本箱，E33顧攜出，E34舅收 | 原件從不進火場；箱角固定標記，不能把燒箱剪成唯一證據消失。 |

## 全40集攝製檢查

每集的完整cast、location、look候選、prop與CC檢查在JSON；下表只放該集獨有的主要拍法與最容易拍錯的地方。主鏡頭以一個主要動作為素材，其餘並列動作拆insert/反應。

| 集 | 主要鏡頭 | 風險 → 控制 | 來源 |
| --- | --- | --- | --- |
| 01 這次不簽 | 撕頁後讓完整原件仍留在畫面 | 同集前世褲裝與現世婚紗衝突 → 前世用zhitang--base、現世用zhitang-bride-veiled，match cut逐鏡綁定 | [source.mjs:562](./source.mjs#L562) |
| 02 替妳著想 | 讓承川親口讀授權對象，收據進知棠手 | 無台詞公證人被生成第四聲線 → 只拍封袋手與收據，三位cast說話 | [source.mjs:620](./source.mjs#L620) |
| 03 藏在附件裡 | 附件和舊委任各展一角，知棠把筆轉向通知 | 講授權過密且婚紗被換掉 → 同一天婚紗無頭紗；只露當下比對條款 | [source.mjs:677](./source.mjs#L677) |
| 04 先別趕人 | 知棠按住解僱通知，司機收回照片 | 照片地址或兒童資料搶戲 → 照片只見背面線索，住址遮罩 | [source.mjs:734](./source.mjs#L734) |
| 05 那筆錢 | 妹妹護住地址，插一個知棠視角火場背影 | 閃回把妹妹求救提前揭穿 → 不拍電話另一端、不加全知畫面 | [source.mjs:791](./source.mjs#L791) |
| 06 證人要走 | 空椅與知棠等電話形成失聯壓力 | 把顧書面變新角色旁白 → 知棠讀關鍵兩字後讓司機自述 | [source.mjs:849](./source.mjs#L849) |
| 07 多出的重量 | 空車欄與過磅數字兩個insert後回司機 | 一張紙被剪成定罪 → 只證明重量矛盾，不加縱火者畫面 | [source.mjs:907](./source.mjs#L907) |
| 08 限時大單 | 車位空缺與訂單期限同框 | 英雄蒙太奇抹掉損失 → 保留另一半運量被轉走通知 | [source.mjs:966](./source.mjs#L966) |
| 09 匯款的另一端 | 排車圖背面翻成遮罩收據 | 學費變條件交換 → 周主動證言，搬遷幫助不附訪談條件 | [source.mjs:1025](./source.mjs#L1025) |
| 10 關門的時間 | 禮袋落桌，錄音筆只播放受損片刻 | 提前播完整錄音破壞E19 → 斷片只提示，簽收封存後送備份修復 | [source.mjs:1083](./source.mjs#L1083) |
| 11 修過兩次的門 | 淑雲把兩工單指到同一門框 | 把列項拍成已修好 → 門仍不能當安全出口使用；對講未驗收 | [source.mjs:1154](./source.mjs#L1154) |
| 12 第一批到了 | 三次簽收各接一部車到場 | 看成全量訂單完成 → 台詞保留只交留下的一半 | [source.mjs:1212](./source.mjs#L1212) |
| 13 失控的人 | 剪輯婚宴畫面停住，知棠轉向資料 | 用勝利樂掩蓋名聲受挫 → 落點留在客戶暫停與權限凍結 | [source.mjs:1270](./source.mjs#L1270) |
| 14 第一次平反 | 三份款項指向同一車號 | 資訊太多觀眾記不住 → 每次只圈車號、收貨、重付各一欄 | [source.mjs:1325](./source.mjs#L1325) |
| 15 母親留下的空格 | 對應碼遞出後知棠重新想起手機背影 | 回憶長片搶掉現在合作 → 只加新觀察點，不重播E5全段 | [source.mjs:1384](./source.mjs#L1384) |
| 16 不能拿人填帳 | 知棠劃去自己支出保住工資 | 兩筆預算被混為同一 → 營運內核預算與許聞外部費不同色角標 | [source.mjs:1443](./source.mjs#L1443) |
| 17 讓他來拿 | 副本借閱欄填完才開查核日程 | 表現成無成本神計 → 保留私人費用受限與真正原件未動 | [source.mjs:1501](./source.mjs#L1501) |
| 18 他親手搬走 | 門禁簽收和搬箱清單接上同一時間 | 把找到搬移紀錄當追回紙本 → 空架和未追回三箱留到結尾 | [source.mjs:1559](./source.mjs#L1559) |
| 19 錄音不是答案 | 母親聲音出現，知棠停住而許聞分三欄 | 錄音剪成全知定罪 → 聲音與日期款項現場分段驗 | [source.mjs:1617](./source.mjs#L1617) |
| 20 私下處理 | 拒絕私了後把具名告發文件推向許聞 | 告發被拍成判決 → 只落已收件分案，無逮捕結局 | [source.mjs:1675](./source.mjs#L1675) |
| 21 明天提前來了 | 封門膠條擋在知棠面前 | 重生記憶仍被當準確導航 → 資料清理提前一日，主角只用既有清單追 | [source.mjs:1745](./source.mjs#L1745) |
| 22 沒錢的查核 | 把必要費用一格格留下 | 把兩次停資寫成重複事件 → 這次明說外部查核費，不是E16部門預算 | [source.mjs:1802](./source.mjs#L1802) |
| 23 賣掉那枚戒指 | 男方戒盒合上，收據取代戒指 | 與E1已退女戒混同 → 男戒外形不同且台詞點出自己購買 | [source.mjs:1857](./source.mjs#L1857) |
| 24 對不上的日期 | 四人把三條來源放成互相對得上的線 | 四角同鏡身份漂移 → 用桌面四組手與兩組雙人鏡 | [source.mjs:1912](./source.mjs#L1912) |
| 25 婚禮前的約定 | 姐妹推資料夾到桌中央 | 把今生約定當前世通話紀錄 → 不重演火場，讓知棠用表情重新理解 | [source.mjs:1971](./source.mjs#L1971) |
| 26 一起走一遍 | 知夏走完兩出口再測固定對講 | 東出口測通等於北線不用走 → 兩條分開驗，手機備案與固定點都交代 | [source.mjs:2028](./source.mjs#L2028) |
| 27 他要買一句原諒 | 顧的供述停在半頁，知棠不簽免責 | 反派道歉剪成洗白 → 停在保留供述與拒絕保證 | [source.mjs:2087](./source.mjs#L2087) |
| 28 不用他的命換 | 舅舅推交易，知棠把證據來源表推回 | 妹妹訊息被加聲線 → 知夏只文字，許聞可讀出所在地 | [source.mjs:2142](./source.mjs#L2142) |
| 29 最後的交接 | 手機封袋到排風燈熄的因果剪接 | 知棠誤入本集、四角同框過載 → 知棠不入鏡不出聲；舅先離倉再出煙 | [source.mjs:2201](./source.mjs#L2201) |
| 30 十八點零二分 | 知棠把要衝的腳停在外圍線 | 失聯人物被畫成即時定位 → 只讀最後名單，不加手機恢復通話 | [source.mjs:2259](./source.mjs#L2259) |
| 31 兩件事一起做 | 許聞通知保管人與消防接手交叉剪 | 時間回跳看成倒退或瞬移 → 18:05/18:10/18:25只作可選CC；必要時間可拍劇內手機、時鐘或收據原文，不加永久時地字卡 | [source.mjs:2328](./source.mjs#L2328) |
| 32 照著貨線走 | 點名筆停在三個空格 | 主角跟進火場 → 消防背影阻止，她留線外 | [source.mjs:2387](./source.mjs#L2387) |
| 33 他先走了 | 顧帶箱走，知夏反向找兩工人到固定點 | 顧離開後落物先後錯置 → 本集出口先可用，E35才出現阻礙 | [source.mjs:2442](./source.mjs#L2442) |
| 34 外圍那一箱 | 正式編號與副本箱同框 | 把舅收箱拍成進倉 → 只在安全外圍，顧交箱可畫外完成 | [source.mjs:2497](./source.mjs#L2497) |
| 35 對講那一頭 | 知夏離開固定對講後改走北線 | 固定對講變隨身無線 → 走前完成位置交接、消防引導 | [source.mjs:2555](./source.mjs#L2555) |
| 36 意外需要證據 | 舅在車內手碰啟動位置被要求留下 | 當夜鑑識立刻判定有罪 → 只保存、待比對、留下說明 | [source.mjs:2612](./source.mjs#L2612) |
| 37 不能再替你簽 | 舅要她代答，她把文件留桌抽回手 | 母親被抹黑又瞬間平反 → 留下新聞壓力到E39 | [source.mjs:2670](./source.mjs#L2670) |
| 38 原諒不是免責 | 合照收到箱底，完整供述仍留上層 | 情感拒绝蓋掉合作證據 → 有利不利供述一起交付 | [source.mjs:2725](./source.mjs#L2725) |
| 39 門上的名字 | 門牌恢復母親名字後切縮編路線圖 | 起訴被誤讀已定讞 → 明示數月後、待審、兩年無股利 | [source.mjs:2780](./source.mjs#L2780) |
| 40 桌上的錶 | 兩姊妹落筆，錶留兩份協議中央 | 生成桌上腕上兩只錶 → 先取錶動作再構圖避腕 | [source.mjs:2837](./source.mjs#L2837) |

## 聲音、四語與CC

以下voice沿用來源合適提案，未試聽未驗收。zh-TW用自然台灣國語，音量不替代表演；其他三語先按同一角色身份試錄，母語審聽後可調voice。外語人名是發音草案，日/韓字形不當正式譯名定案。

| 角色 | 聲線與表演 | zh-TW / ja / ko / en發音草案 |
| --- | --- | --- |
| 沈知棠 / zhitang | Kore；台灣國語；清晰沉著，受傷時降低音量，不變尖銳。 | shěn zhī táng / シェン・ジータン / 선 즈탕 / Shen Zhitang |
| 沈知夏 / zhixia | Aoede；台灣國語；年輕、克制，敢說真話後語速放穩。 | shěn zhī xià / シェン・ジーシア / 선 즈샤 / Shen Zhixia |
| 顧承川 / chengchuan | Puck；台灣國語；親和表面下帶算計，不以低吼演反派。 | gù chéng chuān / グー・チョンチュアン / 구 청촨 / Gu Chengchuan |
| 沈崇岳 / chongyue | Charon；台灣國語；低、緩、像在談家常；敗局才出現呼吸失序。 | shěn chóng yuè / シェン・チョンユエ / 선 충웨 / Shen Chongyue |
| 許聞 / xuwen | Orus；台灣國語；平穩中低音，數字咬字清楚。 | xǔ wén / シュー・ウェン / 쉬 원 / Xu Wen |
| 周啟德 / qide | Fenrir；台灣國語；粗啞但不誇張，關鍵時間慢說。 | zhōu qǐ dé / ジョウ・チードー / 저우 치더 / Zhou Qide |
| 杜淑雲 / shuyun | Sulafat；台灣國語；沉著、成熟，像可信的師傅。 | dù shū yún / ドゥー・シューユン / 두 수윈 / Du Shuyun |
| 沈雲禾 / yunhe | Vindemiatrix；台灣國語；溫和、先說人再談數字；舊錄音的質地由後製加上。 | shěn yún hé / シェン・ユンホー / 선 윈허 / Shen Yunhe |

- 撕紙斷琴是唯一開場強停；後續拒絕交易改用停筆與呼吸，避免每次都重複同招。
- 火場通訊優先；末集双音鋼琴只在簽完後回來。

- 舅舅=母親的兄長，不可日韓英譯成父系叔父；姐妹從母姓。
- 展示副本／完整未簽原件／另存完整副本三詞每語各唯一對照；起訴不譯conviction。
- 新娘婚戒與她買的男方婚戒必須不同名；授權/表決權不可概括成公司已轉讓。

旁白依來源[source.mjs:34](./source.mjs#L34)，不得跟本劇角色共用聲線。字幕出軌後逐條查說話者、標點、當地閱讀速度和轉場；翻譯要對每語音軌對時，不復制繁中CC時間碼。關鍵資訊不只靠左右聲道，必測mono與手機外放。

## 預告素材與留存

15–30秒預告只用E1停筆撕展示副本、E2附件追問、E3頁碼；不露E20幕後者、E25妹妹動機、E35生還或E39起訴。

E6–24每次證據段先給人的代價（失聯、半量訂單、凍結、追不回三箱），才給一項對照；E30–35在重疊視角開頭用已知物件定錨，避免觀眾以為消防時間重置。

先驗前5秒能聽懂衝突、30秒取得第一回報，再看30秒/1分鐘/3分鐘留存、換篇退出與實際點擊觀看的落差；不用空剪節奏或故意截斷已說一半的答案換點擊。百萬點閱是目標，沒有保證。

## 待完成驗收

- 婚紗／褲裝與E40錶離腕的造型資料和逐鏡選擇工具已備妥，待實際角色圖與切鏡驗收。 使用zhitang--base、zhitang-bride-veiled、zhitang-bride-unveiled及zhitang-watch-off；E1按前世/現世鏡頭切換，E2–3無頭紗。剩下要以生成畫面查同臉、服裝切點和全場只一只錶。（E1、E2、E3、E5、E15）
- 四語聲線與醫護／火場音效尚未試聽或成片驗收。 目前僅候選voice與敘事資料；20–30秒中文長句須TTS測時再精簡。（E1、E30、E31、E33、E35）

- 使用已備妥的逐鏡造型資料做角色圖與動畫小樣，查同臉、方向、道具接觸與交接後狀態。
- zh-TW實際TTS、開場30秒剪輯、40集聲音/CC/全片驗收；之後ja/ko/en母語聽校。
- source變更需重驗hash；工具完成不代表付費生成、正式匯入、核准或上架已執行。

## 供應商能力：未成年入鏡尚未驗證

目前Veo 3.1 Lite的首格I2V路徑使用allow_adult；依[官方Veo能力文件](https://ai.google.dev/gemini-api/docs/veo)，不能把它當成未成年入鏡已支援。本輪只新增限制與來源，不改人物年齡、劇情或現有配音。

本稿沒有確認需要標記的現時未成年命名角色。

沈知夏現時23歲。來源提到母親交錄音筆時她15歲（source.mjs:264、2960），但現稿只以錄音來源與保管史交代，未安排15歲本人入鏡；不能只因背景史就把現時成人ID全域標成未成年。若後續新增年少回望，須先獨立確認年齡、集/鏡與供應能力，不能沿用成年look冒拍。

character.video_constraints標記實際未成年人物；只有畫外聲不自動禁止中文配音。分鏡需區分說話者與畫面內人物，但不能靠背影、局部、卡通畫風或省略年齡宣稱繞過限制成功。必須保留原設年齡，先選手繪動畫或合法可支援相應年齡的供應商，做含該人物的pilot確認能力與效果再放量。此批不能宣稱已可直接全400集拍完；通過離線設計檢查也不代表供應商或成片已驗收。
