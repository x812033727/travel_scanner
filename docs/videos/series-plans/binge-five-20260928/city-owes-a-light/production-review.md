# 這座城欠他一盞燈｜製作覆核與攝製設計

2026-10-01。本輪逐集核對40集的衝突、轉折、結尾、人物/道具狀態，並對照設定、opening_30_seconds、continuity_notes與上一輪修訂；未發現新增可確定的劇情矛盾。以下是可實作的攝製設計與風險控制，並非渲染、試聽、母語翻譯或正式站驗收。

來源绑定：`dce3acd2cbeb70c34feb1e1062d6a8d917930f92261f0e3dcb7b9634e894ba43`（SHA-256 of JSON.stringify(source)）。完整機器可讀資料在 [production-design.json](./production-design.json)，共40集、9名角色、6個開場鏡頭。

## 交付與核准邊界

先完成zh-TW台灣口音版；ja/ko/en先做名詞與發音預備，中文版鎖定後各自TTS與CC。所有字幕為可開關CC，沒有繁中或外語燒錄字幕。劇內文件、鐘與標示是物件；關閉CC時仍需由鏡頭和原稿台詞理解。現有README或舊setting中燒錄／五語CC描述依此次新授權改為共享 [profile](../../production-20261001/profile.json)，不讓過期規格回流。

採Gemini veo-3.1-lite-generate-preview，1080p/24fps每次8秒素材；主要行為一鏡一動作，剪取3–6秒，餘反應/插入另片。沒有referenceImages或extension；不可freeze補時。此批正片採clips-only：紙證與觀察也有可信的手部、視線或環境動作；重要文字先核對再合成到動態插鏡。仍圖只供前製animatic，不能混稱完成動畫。原生模型音訊不用作台詞主軌，後製分角色人聲、音效、環境、配樂。

## 拍攝語言

暴雨停電災難程序劇；冷青背景保留膚色，關鍵紅色只給許可／禁入，燈亮不等於安全。

醫院北、轉運站南、控制室西、排水口東；每次換隊用同張地理板與時間，未確認的路段不畫綠線。

林既明說話省力、承認舊錯不雄辯；鄭茵每次核實再下令；吳雅靠報數傳達急迫，避免全員哭喊。

只從已授權角色視角知道情況；供電／地圖／許可由專業人員確認。21:10到05:45的時刻、積水深度與濕衣程度遞增；半年／一年後另立日光造型。

## 開場0–30秒

來源：[source.mjs:511](./source.mjs#L511)、[source.mjs:550](./source.mjs#L550)。以下秒數是剪輯目標，實際TTS與成片尚未量測；每格內若列反打/插入，拆成單動作素材後剪接，不能要求模型一次完成整段蒙太奇。

| 時間 | 機位 | 畫面行為 | 對白意圖與聲音 |
| --- | --- | --- | --- |
| 0–5秒 | 低位近景；固定於安全線外 | 送餐袋停在線外，遠處燈熄滅，林既明伸手制止重啟。 | 先確認裡面的人。；局部斷電聲、雨音，無爆炸。 |
| 5–10秒 | 雙證據插入；顯示器與擔架輪各一短切 | 空載顯示與裡面擔架輪聲互相矛盾。 | 吳雅只報已核實初步人數。；輪軸聲由對講機傳來，不新造護士台詞。 |
| 10–16秒 | 中近景；林既明到消防員視線軸 | 林既明指向異常指示燈，要求消防再次核實。 | 不是操作設備，是請求查證。；話尾留半秒讓消防接收。 |
| 16–20秒 | 手部特寫；固定 | 獲令的操作手撤離重啟控制。 | 不教授開關步驟。；按鈕不落下、機械聲停。 |
| 20–26秒 | 近景；吳雅單人固定 | 吳雅聽見裡面回應後確認兩名病人與一名醫護。 | 由已有角色讀出核實人數。；未登錄醫護以敲擊／環境回應處理，不加第五聲線。 |
| 26–30秒 | 全景；安全線內外清楚分層 | 消防把警戒線拉好，林既明仍站在外側。 | 先救人、後查設備。；拉帶聲接第一集後續，不用大勝音樂。 |

## 角色造型與表演

本輪已完成characters[].shot_looks目錄及scene.data.character_looks逐鏡選擇的工具整合；下列完整外觀資料已可隨新製作bundle傳入工人。原始故事source保持不變，原有按集looks仍可並存。候選episodes不是整集覆寫命令；鏡頭照cue選造型，同一人物的臉與身份保持一致。工具與資料已具備，實際角色圖、動作、聲音及成片仍待驗收。

| 角色 / 候選ID | 涉及集 | 造型與切換條件 | 來源 |
| --- | --- | --- | --- |
| lin-jiming / lin-jiming-entry | E34、E36、E37 | Taiwanese man, 39, lean strong frame, weathered rectangular face, short black hair with slight grey at temples, stubble, faded orange unbranded delivery jacket over a charcoal shirt, navy work trousers, black rain boots, steel pencil clipped inside left pocket. An authorized rescue vest over the delivery jacket and a safety helmet; he remains a civilian technical adviser. E34獲正式許可才穿；E35無本人鏡頭；E37撤出前保持。 | [source.mjs:52](./source.mjs#L52)、[source.mjs:2573](./source.mjs#L2573) |
| lin-jiming / lin-jiming-bed | E38 | Taiwanese man, 39, lean strong frame, weathered rectangular face, short black hair with slight grey at temples, stubble, a charcoal shirt, resting in a hospital bed; lower body under a blanket, leg injury dressed. No rescue vest, safety helmet or visible rain boots. 傷在E37撤離，不能提前瘸行。 | [source.mjs:52](./source.mjs#L52)、[source.mjs:2816](./source.mjs#L2816) |
| lin-jiming / lin-jiming-recovery | E39、E40 | Taiwanese man, 39, lean strong frame, weathered rectangular face, short black hair with slight grey at temples, stubble, a clean practical orange work jacket over a charcoal shirt, navy work trousers and ordinary work shoes. Recovered from the leg injury; no rescue vest or helmet. 時間跳接以場景與可開關CC說明。 | [source.mjs:52](./source.mjs#L52)、[source.mjs:2875](./source.mjs#L2875) |
| lin-anan / lin-anan-raincoat | E9、E17 | Taiwanese girl, 16, slim build, chin-length black bob with a small blue hair clip, cream school shirt, dark school trousers, white sneakers, yellow canvas tote with a hand-stitched lamp patch. Natural teenage styling, no glamour makeup. A loose pale green raincoat over her school clothes; the yellow lamp-patch tote remains. E17交給朵朵前，之後不可再穿。 | [source.mjs:83](./source.mjs#L83)、[source.mjs:1018](./source.mjs#L1018) |
| lin-anan / lin-anan-wet | E17、E26、E31 | Taiwanese girl, 16, slim build, chin-length black bob with a small blue hair clip, cream school shirt, dark school trousers, white sneakers, yellow canvas tote with a hand-stitched lamp patch. Natural teenage styling, no glamour makeup. Wet cold school clothing; no pale green raincoat because she has given it away. No extra flashlight. E17交衣後至救出。 | [source.mjs:83](./source.mjs#L83)、[source.mjs:1518](./source.mjs#L1518) |
| lai-liang / lai-liang-helmet | E34、E37 | Taiwanese man, 58, stocky build, short salt-and-pepper hair, thick brows, faded olive work coat, dark trousers, brown safety boots. Slight limp visible but stable; no acrobatic movements. A yellow safety helmet with one white stripe. Preserve his stable pre-existing limp. 不可提前出現在E32集結點。 | [source.mjs:218](./source.mjs#L218)、[source.mjs:2573](./source.mjs#L2573) |
| duo-duo / duo-duo-borrowed-coat | E17、E26 | Taiwanese girl, 8, round face, two low black pigtails, pale pink rain poncho over a navy sweater, grey leggings, purple rubber boots, small orange stuffed fox held close. Natural child proportions; no glamour styling or sensational injury. A loose pale green borrowed raincoat over the original pink poncho, oversized sleeves; keep the orange fox. E17取得，未有歸還情節不得自行消失。 | [source.mjs:268](./source.mjs#L268)、[source.mjs:1518](./source.mjs#L1518) |

## 道具與空間連戲

依[source.mjs:36](./source.mjs#L36)、[source.mjs:3040](./source.mjs#L3040)；特殊道具以獨立參考圖與交接鏡追蹤，列出的外觀差異屬美術選擇，不能改原有劇情因果。

| ID | 唯一性 | 狀態 | 持有人與拍法 |
| --- | --- | --- | --- |
| route-map | 北醫院／南站250m／西控制400m／東排水700m，同一1.2km區域 | 逐段待查、已核實、禁行；不得一段查明就全路安全 | 鄭茵／陳勳各管本隊路線，林只提供舊知；每次改路同一朝向，註明南支與東支，地圖文字做實物資訊非字幕。 |
| delivery-kit | 送餐袋及白色外送頭盔，不是救援安全帽 | 袋E1–3→吳雅；頭盔E1–8後留場；不得穿越到東側作業 | E3袋由吳雅接手，E8頭盔留置；切手部交接建立唯一性，E34救援帽用不同色型。 |
| two-girls | 淡綠借衣、單支手電、橙狐、黃色燈補丁袋 | E17雨衣安安→朵朵，手電仍由安安控制；E26不逆轉 | 安安與朵朵沿站務員指示，同樓層平台待援；不剪成孩子涉水自救或父親250m即能跑到。 |
| evidence | 值班簿／維修簿／離線資料盒／附件原件盒四種證據 | 值班簿E12；維修簿E23複本E34原件交出；離線盒E24；附件盒E35 | 周禾及鄭茵按正式程序封存；林不得私收原件；標籤和封條色不同；E35三件公務證物同框逐項點收，避免兩盒變一盒。 |
| entry-permit | 救援許可、安全帽背心、乾燥隔離廊道與銘牌 | E33隔離／排水／測試完成；E34正式許可；E37双人比對 | 消防管入場，兩人只比對銘牌，周禾遠端控制；只呈核准結果，不特寫可照做的帶電維修或開關操作。 |
| timestamp | 事件時計與紙面日期 | E1 21:10→E38 05:45；E39半年；E40一年 | 控制室共同核對，跳年不混入當夜；以場內鐘／文件與短口語同時傳達關鍵時刻，字幕關閉仍能懂。 |

## 全40集攝製檢查

每集的完整cast、location、look候選、prop與CC檢查在JSON；下表只放該集獨有的主要拍法與最容易拍錯的地方。主鏡頭以一個主要動作為素材，其餘並列動作拆insert/反應。

| 集 | 主要鏡頭 | 風險 → 控制 | 來源 |
| --- | --- | --- | --- |
| 01 餐還沒送到 | 禁止重啟的手停在安全線外 | 空載圖示被當安全 → 同時給矛盾聲音且由消防核實 | [source.mjs:550](./source.mjs#L550) |
| 02 先把病床帶出來 | 擔架逐人出線而非林闖機房 | 主角越權救援 → 主角只交情報，不碰控制 | [source.mjs:607](./source.mjs#L607) |
| 03 我看過你修過這裡 | 吳雅接下送餐袋再報傷員 | 袋之後跟主角瞬移 → 清楚拍接手，女兒簡訊不等於路已安全 | [source.mjs:665](./source.mjs#L665) |
| 04 新圖少了一條路 | 新舊地圖三位置疊合 | 安全路線尚未查卻變綠 → 北廊標待查，南與東支分開 | [source.mjs:726](./source.mjs#L726) |
| 05 這個名字沒有權限 | 周禾以自己帳號查紀錄 | 主角被停權仍能登入 → 顯示周禾操作與停權紀錄不同欄 | [source.mjs:784](./source.mjs#L784) |
| 06 先保留這一頁 | 掛斷私人電話留下正式申請 | 公司口頭同意變成准操作 → 僅拿唯讀資料與封存要求 | [source.mjs:841](./source.mjs#L841) |
| 07 先亮起這一小區 | 一盞備援燈照到床路 | 局部燈亮剪成全院復電 → 遠背景仍暗，中央控制不變 | [source.mjs:897](./source.mjs#L897) |
| 08 七年前那個人 | 送達時間與停權時間並排 | 外送頭盔跟進後段機房 → E8後頭盔留置，文書證實停權 | [source.mjs:957](./source.mjs#L957) |
| 09 隔著兩百五十公尺 | 父女隔著電話各守原位置 | 250m誤讀可跑過去 → 暴雨阻隔和B1辦公室定位同時建立 | [source.mjs:1018](./source.mjs#L1018) |
| 10 配置單上的那一欄 | 災前停權記錄抵住甩鍋公文 | 宋書面說法變新增出場台詞 → 由在場角色讀文書，維持登記cast | [source.mjs:1079](./source.mjs#L1079) |
| 11 先複誦位置 | 救援車十分鐘轉場 | 一剪瞬移破時間軸 → 21:55至22:10有可見交接時間 | [source.mjs:1152](./source.mjs#L1152) |
| 12 紙上還留著那條通道 | 值班簿記載廊道存在 | 存在等於可以通行 → 畫面仍留未核實區段 | [source.mjs:1215](./source.mjs#L1215) |
| 13 只確認這一段 | 接力查第一段北廊 | 受困值班員變新聲線 → 只出文字/既有聲音轉述 | [source.mjs:1274](./source.mjs#L1274) |
| 14 不是你家的控制站 | 諮詢桌與控制台保持物理距離 | 主角擅進控制台 → 明示只可提供意見，原件不交他 | [source.mjs:1334](./source.mjs#L1334) |
| 15 讓現場把話說完 | 周禾以自己名義簽異常 | 林代簽周禾的判斷 → 一次簽名一責任，不交換手部 | [source.mjs:1396](./source.mjs#L1396) |
| 16 把值班的人接出來 | 救出值班員後傳出手寫紙 | 一人獲救代表全廊安全 → 另一段仍待查，消防報進度 | [source.mjs:1458](./source.mjs#L1458) |
| 17 我等她一起走 | 安安把淡綠雨衣披到朵朵外面 | 借衣逆轉或孩子冒險涉水 → 同樓層平台跟站務引導，手電只一支 | [source.mjs:1518](./source.mjs#L1518) |
| 18 救援不是封口費 | 私人車承諾被放回桌角 | 拒絕與失去資源無代價 → 留下已無私人車的空欄 | [source.mjs:1578](./source.mjs#L1578) |
| 19 這個字是誰簽的 | 舊簽名在投影上放大 | 揭露簽名就等於全部造假 → 承認真簽名，尚要完整附件 | [source.mjs:1637](./source.mjs#L1637) |
| 20 每一項都交簽核 | 主角承認未測就簽 | 用被陷害抹掉真失職 → 鏡頭留周禾獨立核准空欄 | [source.mjs:1699](./source.mjs#L1699) |
| 21 這段也照樣記下來 | 真實失職寫進當晚紀錄 | 簽認變恢復資格 → 以未獲准操作的站位收尾 | [source.mjs:1772](./source.mjs#L1772) |
| 22 三張表，不再一人扛 | 三張責任表各自交到功能位置 | 周禾未在cast卻新增手臉聲線 → 工程表只做已簽文件/場外收件，不造第五角色 | [source.mjs:1833](./source.mjs#L1833) |
| 23 老工頭開出的條件 | 電話另一端只傳維修簿複本 | E23原件提前到場 → 只複本，原簿留到E34 | [source.mjs:1896](./source.mjs#L1896) |
| 24 離線日誌上的日期 | 離線盒資料與停權時間對齊 | 林違反唯讀限制接手原件 → 周禾保管與比對，宋帳號事件可見 | [source.mjs:1955](./source.mjs#L1955) |
| 25 這一欄我不簽正常 | 周禾遞出自己異常表 | 新表被誤剪成舊維修簿 → 表頭與簽名位置不同 | [source.mjs:2016](./source.mjs#L2016) |
| 26 終於有人告訴他們往哪裡等 | 平台局部播音恢復 | 恢復廣播等於全站復電 → 只此區播音，淡綠借衣仍在朵朵 | [source.mjs:2076](./source.mjs#L2076) |
| 27 留給搬床的時間 | 吳雅把轉床期限寫上表 | 把轉床期限演成全院同秒死亡 → 每15分鐘重估，不誇大單一倒數 | [source.mjs:2137](./source.mjs#L2137) |
| 28 派遣單上的目的地 | 調度圖資源由總部移到醫院 | 救女兒插隊成正當英雄 → 公開醫療優先，女兒按站救援隊序 | [source.mjs:2198](./source.mjs#L2198) |
| 29 那個女孩是我女兒 | 賴良在電話中答應同行 | 隱瞞女兒關係再爆一次 → 承接既已知關係，只補具體位置編號 | [source.mjs:2258](./source.mjs#L2258) |
| 30 最後一項得去現場看 | 乾燥廊道方案停在待許可欄 | 展示帶電作業教學 → 禁止直接操作指令，待隔離驗證 | [source.mjs:2318](./source.mjs#L2318) |
| 31 把她交給你們 | 安安平台圖交陳勳後林赴東隊 | 主角一人兼兩處救援 → 南隊救女兒、東隊查排水明確分工 | [source.mjs:2392](./source.mjs#L2392) |
| 32 回報到了才算接上 | 東側集結點保留賴良空位 | 賴良提前到達 → 只電話或報時，正面登場留E34 | [source.mjs:2452](./source.mjs#L2452) |
| 33 先把需要的人送出去 | 第一張病床在兩點前轉出 | 備援亮燈先剪成工程已完成 → 同步乾燥隔離測試結論，等待正式許可 | [source.mjs:2512](./source.mjs#L2512) |
| 34 舊入口前的那一步 | 賴良先把帽拿手再等許可 | 原維修簿與安全帽提前出現 → E34首次本人抵東；原簿交出後只留副本 | [source.mjs:2573](./source.mjs#L2573) |
| 35 紀錄間的交接單 | 兩盒一簿在控制室封條逐一落下 | 主角不在卻插反應或盒子合併 → 只周禾鄭茵宋；附件盒與離線盒形狀不同 | [source.mjs:2635](./source.mjs#L2635) |
| 36 每一頁終於接得上 | 鄭茵承認舊警告而救出訊息抵達 | 同刻女孩出東側廊道 → 女孩消息不切實體救出，林仍東側 | [source.mjs:2694](./source.mjs#L2694) |
| 37 兩塊一樣的銘牌 | 兩人各自讀銘牌後撤離 | 合成同時比對受傷操作的大動作 → 分拆確認/遠控/撤出；腿傷只在撤出後 | [source.mjs:2756](./source.mjs#L2756) |
| 38 天亮以前，一盞一盞 | 病床父女分食仍見腿包紮 | 傷好太快或雨靴上床 → 床上look，夜→天慢亮，服務逐步恢復 | [source.mjs:2816](./source.mjs#L2816) |
| 39 六個月後的那封通知 | 半年後處分結果與工作界線同框 | 調查洗清全部失職 → 陷害和真過失分別呈現，無全資格回復 | [source.mjs:2875](./source.mjs#L2875) |
| 40 第一盞燈，留給後來的人 | 學員指未檢欄，普通燈最後才亮 | 把工程培訓拍成危險接線教程 → 不拍可複現接線；以檢查先於通電作回環 | [source.mjs:2933](./source.mjs#L2933) |

## 聲音、四語與CC

以下voice沿用來源合適提案，未試聽未驗收。zh-TW用自然台灣國語，音量不替代表演；其他三語先按同一角色身份試錄，母語審聽後可調voice。外語人名是發音草案，日/韓字形不當正式譯名定案。

| 角色 | 聲線與表演 | zh-TW / ja / ko / en發音草案 |
| --- | --- | --- |
| 林既明 / lin-jiming | Iapetus；台灣國語；中低音、疲憊但清楚，少用高聲宣言；不與旁白（Charon）或同場男角共用聲音；擬定 casting，未試聽，開拍前核對主機聲音池。 | Lín Jì-míng / リン・ジーミン / 린 지밍 / Lin Jiming |
| 林安安 / lin-anan | Zephyr；台灣國語；清亮自然、不幼態，疲弱段保留同一聲線；擬定 casting，未試聽，開拍前核對主機聲音池。 | Lín Ān-ān / リン・アンアン / 린 안안 / Lin Anan |
| 鄭茵 / zheng-yin | Kore；台灣國語；穩定中低女聲、短句有時間感；擬定 casting，未試聽，開拍前核對主機聲音池。 | Zhèng Yīn / ジョン・イン / 정 인 / Zheng Yin |
| 周禾 / zhou-he | Puck；台灣國語；青年中音、清晰而稍急，後段減少搶話；擬定 casting，未試聽，開拍前核對主機聲音池。 | Zhōu Hé / ジョウ・ホー / 저우 허 / Zhou He |
| 宋振南 / song-zhennan | Orus；台灣國語；低音、體面、控制停頓，不一直咆哮；擬定 casting，未試聽，開拍前核對主機聲音池。 | Sòng Zhèn-nán / ソン・ジェンナン / 쑹 전난 / Song Zhennan |
| 陳勳 / chen-xun | Fenrir；台灣國語；結實有力、不吼叫，無線電語句簡短；擬定 casting，未試聽，開拍前核對主機聲音池。 | Chén Xūn / チェン・シュン / 천 쉰 / Chen Xun |
| 賴良 / lai-liang | Algenib；台灣國語；年長沙啞、比主角慢半拍，與主角（Iapetus）、旁白（Charon）分開；擬定 casting，未試聽，開拍前核對主機聲音池。 | Lài Liáng / ライ・リャン / 라이 량 / Lai Liang |
| 吳雅 / wu-ya | Aoede；台灣國語；清楚中高女聲，柔和但能打斷無效爭論；擬定 casting，未試聽，開拍前核對主機聲音池。 | Wú Yǎ / ウー・ヤー / 우 야 / Wu Ya |
| 朵朵 / duo-duo | Sulafat；台灣國語；輕柔兒童口吻、少量台詞，不尖叫與不幼態誇飾；擬定 casting，未試聽，開拍前核對主機聲音池。 | Duǒ-duǒ / ドゥオドゥオ / 둬둬 / Duoduo |

- 斷電不是全靜音：雨、輪軸、對講殘響維持空間；每項核實留短靜默讓觀眾辨識。
- 林既明只一條克制主聲；實際電話保留不同空間底噪，E31讀訊不做接通聲或即時電話透視，mono仍可懂。
- E38降雨牆和脈衝配樂，E40用普通燈按鍵與自然室內聲結束。

- 全劇檢查、核實、許可、唯讀、操作五詞分開，翻譯不可把諮詢譯成控制。
- 21:10—05:45屬同夜跨日；半年與一年明確改日期，時間關鍵用現場鐘與口語。
- 北廊主線／南支／東支不得混譯；女孩是在同樓層安全平台待援，不是自行穿水。

旁白依來源[source.mjs:34](./source.mjs#L34)，不得跟本劇角色共用聲線。字幕出軌後逐條查說話者、標點、當地閱讀速度和轉場；翻譯要對每語音軌對時，不復制繁中CC時間碼。關鍵資訊不只靠左右聲道，必測mono與手機外放。

## 預告素材與留存

取E1空載顯示對擔架輪聲、E9父女電話、E19真簽名；到「他真的簽過」停。避開E35封存、E36救出、E37操作與E39調查結果。

每集只讓一項核實改變一個實際行動；地圖段落維持固定北向並跟隨紙/車/人，不連續念地名。E17借衣、E22三表、E35三證物形成可辨認物理回報。

先驗前5秒能聽懂衝突、30秒取得第一回報，再看30秒/1分鐘/3分鐘留存、換篇退出與實際點擊觀看的落差；不用空剪節奏或故意截斷已說一半的答案換點擊。百萬點閱是目標，沒有保證。

## 待完成驗收

- 借衣、救援裝備與傷後造型已具完整目錄及逐鏡工具，待可用製作路徑與畫面驗收。 依現有lin-anan/duo-duo借衣、lin-jiming-entry/bed/recovery及lai-liang-helmet逐鏡選用；核對同臉、交衣後原持有人不再穿、許可後才戴帽。未成年人製作能力限制仍獨立保留。（E17、E26、E34、E37、E38、E39、E40）
- 暴雨、人聲與醫療訊號的手機外放可懂度待實際混音。 文字能分辨的核實資訊可能在成片被雨聲蓋掉。（E1、E2、E27、E37）
- 林安安（lin-anan）明確16歲，Veo Lite I2V未驗證可生成其入鏡畫面。 目前首格I2V的allow_adult能力不代表允許未成年人顯影；不能把角色改為成年人，也不能以背影、局部、卡通風格或不提年齡當可保證捷徑。需經核可的手繪動畫或合法支援該年齡的供應商先做pilot、確認能力與交付再排量。僅畫外配音不因此自動受阻，逐鏡按實際可見人物判斷。（E9、E17、E26、E31、E38、E39、E40）
- 朵朵（duo-duo）明確8歲，Veo Lite I2V未驗證可生成其入鏡畫面。 目前首格I2V的allow_adult能力不代表允許未成年人顯影；不能把角色改為成年人，也不能以背影、局部、卡通風格或不提年齡當可保證捷徑。需經核可的手繪動畫或合法支援該年齡的供應商先做pilot、確認能力與交付再排量。僅畫外配音不因此自動受阻，逐鏡按實際可見人物判斷。（E17、E26）

- 使用已備妥的逐鏡造型資料做角色圖與動畫小樣，查同臉、方向、道具接觸與交接後狀態。
- zh-TW實際TTS、開場30秒剪輯、40集聲音/CC/全片驗收；之後ja/ko/en母語聽校。
- source變更需重驗hash；工具完成不代表付費生成、正式匯入、核准或上架已執行。

## 供應商能力：未成年入鏡尚未驗證

目前Veo 3.1 Lite的首格I2V路徑使用allow_adult；依[官方Veo能力文件](https://ai.google.dev/gemini-api/docs/veo)，不能把它當成未成年入鏡已支援。本輪只新增限制與來源，不改人物年齡、劇情或現有配音。

| 角色 ID | 明確視覺年齡 | 登記出場集（非每鏡都入鏡） | 年齡來源 |
| --- | --- | --- | --- |
| 林安安 / lin-anan | 16歲 | E9、E17、E26、E31、E38、E39、E40 | [source.mjs:86](./source.mjs#L86)、[source.mjs:87](./source.mjs#L87) |
| 朵朵 / duo-duo | 8歲 | E17、E26 | [source.mjs:271](./source.mjs#L271)、[source.mjs:272](./source.mjs#L272) |

安安在半年/一年後仍未滿18歲；不得因尾聲制服或成年聲線而假設已成年。雨衣轉手、病床或玩偶的近鏡只改構圖，不保證供應商接受未成年人物。

character.video_constraints標記實際未成年人物；只有畫外聲不自動禁止中文配音。分鏡需區分說話者與畫面內人物，但不能靠背影、局部、卡通畫風或省略年齡宣稱繞過限制成功。必須保留原設年齡，先選手繪動畫或合法可支援相應年齡的供應商，做含該人物的pilot確認能力與效果再放量。此批不能宣稱已可直接全400集拍完；通過離線設計檢查也不代表供應商或成片已驗收。

## 2026-10-02 配音與聲音細節覆核

本輪只有來源文字與製作設計覆核，沒有實際TTS、試音、SFX音檔或成片驗收。新增performance_states、audio_cues、audition_scenes每筆均為proposed，綁定集數與來源。source_excerpt只供語境，不能整段念成台詞；line_samples僅逐字引用已有原台詞，其餘試音段落待本集定稿取樣。

- E31為父女非同步訊息，回訊保留鎖定畫面，不是即時电话。
- E37林既明核實時尚未腿傷；操作回報後撤離才受傷、接受幫助。
- 安安16歲、朵朵8歲的冷與怕需試音，不用幼兒化、改年齡或聲線名稱冒稱驗收。

### 角色表演狀態

| 角色 / state | 集數 | 演出重點 | 來源 |
| --- | --- | --- | --- |
| lin-jiming / jiming-withdrawal-injury | E37 | 先核實，撤離途中才受腿傷；觀察時正常疲倦，撤出受傷後才短呼吸和接受救援；顧問不能演成自行操作的人。 | [source.mjs:2807](./source.mjs#L2807) |
| lin-jiming / jiming-morning | E38 | 腿部包紮，承認正在好轉；臥床音量與慢起句但句尾清楚；不宣告全城復原或演到不能回答。 | [source.mjs:2866](./source.mjs#L2866) |
| lin-anan / anan-cold-conscious | E17、E26 | 16歲，清醒受冷，在同層高處平台待援；短句帶恐懼但能安撫，不演成人救援專家；不加重傷喘叫或提早脫險的輕鬆語氣。 | [source.mjs:1569](./source.mjs#L1569)、[source.mjs:2128](./source.mjs#L2128) |
| zhou-he / zhou-authorized | E37 | 安全控制站待兩項核實後依授權處置；先接收後確認，不能讓剪接或聲音暗示林既明自行操作。 | [source.mjs:2761](./source.mjs#L2761) |
| chen-xun / chen-coordinates | E31、E37 | 要求分工、撤出接手救援；短句明確，不用威嚇腔；按角色完成再推進，不添設備教學。 | [source.mjs:2397](./source.mjs#L2397)、[source.mjs:2761](./source.mjs#L2761) |
| lai-liang / lai-check | E37 | 58歲老工頭獨立複核；看圖再答，與林既明不齊念；不越界成操作員。 | [source.mjs:2760](./source.mjs#L2760) |
| duo-duo / duoduo-afraid | E17、E26 | 8歲，怕黑、清醒仍在平台；以遲疑和確認眼前事物演怕黑，不尖嗓幼兒化或說成人道理。 Sulafat僅casting提案，必須聽校能否可信演8歲，不合就另記casting，不能宣稱已過。 | [source.mjs:1569](./source.mjs#L1569)、[source.mjs:2128](./source.mjs#L2128) |

### 聲音提示

- **city-e17-comms（E17；dialogue）**：通訊斷續只在非關鍵音節間，路線仍是同層高處，不新增下水指令；哭聲不能蓋位置。 來源：[source.mjs:1523](./source.mjs#L1523)。
- **city-e26-waiting（E26；dialogue）**：提示限已核對等待區；林由調度得知，不变亲眼看見平台，也未救出女兒。 來源：[source.mjs:2081](./source.mjs#L2081)。
- **city-e31-text-message（E31；message-read）**：先父親送短訊，再女兒回訊；若角色讀訊，只讀定稿，無接通聲、電話頻帶或即時重疊。 女兒回訊留鎖屏；鏡內手機是劇內道具，CC仍可關，無永久翻譯字卡。 來源：[source.mjs:2400](./source.mjs#L2400)。
- **city-e37-verifications（E37；dialogue）**：林／賴核實在先，周依授權操作在後；對講mono也能分角色，底噪不盖銘牌／原圖。 來源：[source.mjs:2761](./source.mjs#L2761)。
- **city-e37-accepts-help（E37；dialogue）**：排水回報後才有撤離碎片傷；讀女兒訊息的反應後才接受同行，碰撞不壓「好，我跟你們走」。 來源：[source.mjs:2764](./source.mjs#L2764)。
- **city-e38-lamp（E38；dialogue）**：近身病房與按燈聲取代雨牆；最後一句保留呼吸，不加全城勝利旁白。 來源：[source.mjs:2824](./source.mjs#L2824)。

### 待實作的試音段落

- **city-platform／E17**：lin-anan、duo-duo、zheng-yin。定稿挑清醒待援、怕黑及遠端確認三人段，乾聲先驗16／8／42歲，再加通訊。 驗收要聽：不看畫面能分安安與朵朵，不能靠不合年齡的成人低音／幼兒尖叫。 mono與手機位置清楚，沒有新傷或下水自救。 來源：[source.mjs:1523](./source.mjs#L1523)。
- **city-four-men／E37**：lin-jiming、lai-liang、chen-xun、zhou-he。定稿挑核實到撤出的相接段，Iapetus／Algenib／Fenrir／Puck不全壓成同一低音。 驗收要聽：閉眼可分觀察、複核、指揮、控制站；授權因果不亂。 傷後氣息只在撤離，最後改口清楚。 來源：[source.mjs:2761](./source.mjs#L2761)。

先完成zh-TW台灣口音乾聲與多人辨識，再做通訊／環境／音樂處理、mono與手機外放。不同voice_name或文字規則不能代替試聽。逐鏡聲音、造型、道具須和實際演出對上，CC只作獨立可開關軌；ja/ko/en在中文版定案後各自配音、重新配時及母語聽校。本輪沒有修改來源、歷史版本或正式站，不代表新增設計已同步後台。

## 2026-10-02 第二輪聲音交接修正

E13 的 hero_shot.sound 與 voice_notes 已改為「短信到中繼點後由陳勳回報」。依 [source.mjs:3056](./source.mjs#L3056)，值班員不出聲，E13 的求救短信傳到中繼點後由當集出場的陳勳回報；E13 出場清單只有林既明、周禾、陳勳，不新增鄭茵聲線。E14–15 訊息傳到調度席後才由鄭茵複誦，兩集原設保持。

這是來源與製作設計的文字一致性修正，source 未改，沒有試音、實際 SFX、CC 或成片驗收，也不代表後台版本已同步。
