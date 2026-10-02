# 朕不是你們的替死鬼｜製作覆核與攝製設計

2026-10-01。本輪逐集核對40集的衝突、轉折、結尾、人物/道具狀態，並對照設定、opening_30_seconds、continuity_notes與上一輪修訂；未發現新增可確定的劇情矛盾。以下是可實作的攝製設計與風險控制，並非渲染、試聽、母語翻譯或正式站驗收。

來源绑定：`399f468d18158a3938450d95d1cc9b615756cfa686d93c9c3e8afc7bcf34dc28`（SHA-256 of JSON.stringify(source)）。完整機器可讀資料在 [production-design.json](./production-design.json)，共40集、11名角色、6個開場鏡頭。

## 交付與核准邊界

先完成zh-TW台灣口音版；ja/ko/en先做名詞與發音預備，中文版鎖定後各自TTS與CC。所有字幕為可開關CC，沒有繁中或外語燒錄字幕。劇內文件、鐘與標示是物件；關閉CC時仍需由鏡頭和原稿台詞理解。現有README或舊setting中燒錄／五語CC描述依此次新授權改為共享 [profile](../../production-20261001/profile.json)，不讓過期規格回流。

採Gemini veo-3.1-lite-generate-preview，1080p/24fps每次8秒素材；主要行為一鏡一動作，剪取3–6秒，餘反應/插入另片。沒有referenceImages或extension；不可freeze補時。此批正片採clips-only：紙證與觀察也有可信的手部、視線或環境動作；重要文字先核對再合成到動態插鏡。仍圖只供前製animatic，不能混稱完成動畫。原生模型音訊不用作台詞主軌，後製分角色人聲、音效、環境、配樂。

## 拍攝語言

宮廷糧政懸疑；金冠與粗糧的質地差建立权力距離，明暗可讀的暖土色，公文不浮在空中當解說卡。

城北河運／北倉與北門，南三州經南橋關；東公糧倉臨東南河，仍受南關控制。每次糧流只用一張固定朝向地圖。

葉穗從先救眼前到承擔程序責任，拒絕喊口號；裴定衡慢、精確、把威脅包成公事；何靜讀數有節奏但不是旁白機器。

Day1到Day30逐日粮食因果；E29末摘冠到E39無冠，E40先簽自己姓名才重新戴冠。三種印、兩種通行牌、兩份身世材料不可合併。

## 開場0–30秒

來源：[source.mjs:590](./source.mjs#L590)、[source.mjs:626](./source.mjs#L626)。以下秒數是剪輯目標，實際TTS與成片尚未量測；每格內若列反打/插入，拆成單動作素材後剪接，不能要求模型一次完成整段蒙太奇。

| 時間 | 機位 | 畫面行為 | 對白意圖與聲音 |
| --- | --- | --- | --- |
| 0–5秒 | 特寫；冠自上進框、桌面短反打 | 冠落下；觀眾在印盒邊看見第30日處決日期，姓名仍被遮住。 | 葉穗只問宮外是否有人吃飯，不知道自己的日期。；冠珠輕響，遠處空碗敲擊。 |
| 5–12秒 | 中景；何靜入桌邊停下 | 何靜放下一碗賑粥。 | 問這是否今日宮外所得。；瓷碗落桌，關掉誇張肚餓音效。 |
| 12–17秒 | 手部近景；側面固定 | 葉穗把自己面前御膳撤到一旁。 | 只撤自己的飯，不清全桌。；盤沿短摩擦。 |
| 17–22秒 | 近景；眼平固定 | 葉穗先喝一口賑粥。 | 以實際嚐味代替演說。；吞嚥與小停頓。 |
| 22–26秒 | 桌面雙人；沿桌低位 | 同一碗粥推到裴定衡面前。 | 不逼吞、不互換新碗。；碗滑動止住。 |
| 26–30秒 | 手與臉兩切；裴的筷停著再見配額紙 | 裴定衡不動筷，只推出可用糧額。 | 明日一萬碗的要求引出真正資源問題。；紙落桌取代勝利配樂。 |

## 角色造型與表演

本輪已完成characters[].shot_looks目錄及scene.data.character_looks逐鏡選擇的工具整合；下列完整外觀資料已可隨新製作bundle傳入工人。原始故事source保持不變，原有按集looks仍可並存。候選episodes不是整集覆寫命令；鏡頭照cue選造型，同一人物的臉與身份保持一致。工具與資料已具備，實際角色圖、動作、聲音及成片仍待驗收。

| 角色 / 候選ID | 涉及集 | 造型與切換條件 | 來源 |
| --- | --- | --- | --- |
| ye-sui / ye-sui-crowned | E1、E2、E3、E4、E5、E6、E7、E8、E9、E10、E11、E12、E13、E14、E15、E16、E17、E18、E19、E20、E21、E22、E23、E24、E25、E26、E27、E28、E29 | A 24-year-old East Asian woman with an oval face, focused dark eyes and straight black hair secured in one compact high knot. A narrow bronze hairpin shaped like a rice leaf never changes. She wears a plain deep teal court robe with restrained antique-gold edging, practical dark boots and a short brown counting cord at her waist. Slim, upright silhouette; no heavy makeup or ornamental weapon. A plain gold crown around the unchanged hair knot; the bronze rice-leaf hairpin remains. E29羅杏摘冠前；E1同集戴冠動作需空冠位前態。 | [source.mjs:60](./source.mjs#L60)、[source.mjs:626](./source.mjs#L626) |
| ye-sui / ye-sui-uncrowned | E29、E30、E31、E32、E33、E34、E35、E36、E37、E38、E39、E40 | A 24-year-old East Asian woman with an oval face, focused dark eyes and straight black hair secured in one compact high knot. A narrow bronze hairpin shaped like a rice leaf never changes. She wears a plain deep teal court robe with restrained antique-gold edging, practical dark boots and a short brown counting cord at her waist. Slim, upright silhouette; no heavy makeup or ornamental weapon. No gold crown. Keep the bronze rice-leaf hairpin and the original hair knot. E29末摘下後至E40先簽名；不得每集重生金冠。 | [source.mjs:60](./source.mjs#L60)、[source.mjs:2332](./source.mjs#L2332) |
| ye-sui / ye-sui-recrowned | E40 | A 24-year-old East Asian woman with an oval face, focused dark eyes and straight black hair secured in one compact high knot. A narrow bronze hairpin shaped like a rice leaf never changes. She wears a plain deep teal court robe with restrained antique-gold edging, practical dark boots and a short brown counting cord at her waist. Slim, upright silhouette; no heavy makeup or ornamental weapon. The same gold crown is worn again only after the signature; keep the rice-leaf hairpin. 只E40簽名後鏡頭。 | [source.mjs:60](./source.mjs#L60)、[source.mjs:2455](./source.mjs#L2455) |
| han-rui / han-rui-transfer-mark | E18 | A 20-year-old East Asian woman with a heart-shaped face and straight dark hair in two simple low braids. She wears a pale grey-blue short jacket, a navy skirt and a small embroidered yellow pouch at her waist. A faint pale restraint mark circles her right wrist. No court ornaments. Only a faint pale mark at the right wrist; no open wound or blood. E18轉移患者群中可見；後續若無本人就不造反應鏡。 | [source.mjs:315](./source.mjs#L315)、[source.mjs:1664](./source.mjs#L1664) |

## 道具與空間連戲

依[source.mjs:45](./source.mjs#L45)、[source.mjs:3106](./source.mjs#L3106)；特殊道具以獨立參考圖與交接鏡追蹤，列出的外觀差異屬美術選擇，不能改原有劇情因果。

| ID | 唯一性 | 狀態 | 持有人與拍法 |
| --- | --- | --- | --- |
| crown | 同一金冠與常在的稻葉銅髮簪 | E1戴→E29末羅杏摘→E30–39無→E40簽後重戴 | 葉穗戴；羅杏摘時保管，鏡頭不暗示冠被毀；金冠是條件地位道具，不把無冠畫成換臉。 |
| soup | E1唯一賑粥碗與葉自己的御膳 | 何靜端來→葉先喝→推裴；其他桌膳保持 | E1桌上連續追蹤，不由罗杏端來；碗缺口與湯量同一；E40不重拍虛构換粥結局。 |
| three-seals | 南關左稅桌印、右借桌印、內廷副印是三枚 | E6/E9對兩張同貨重收證；E17醫票右桌印；內廷副印屬另一條 | 稅與借兩桌有各自印人；不把內廷印挪去關口；取不同輪廓和案桌方位，逐鏡保留印泥/紙張先後。 |
| grain-account | 糧、現金、借款、專屬採購與欠糧分欄 | E15部分供糧；E23供18–19；E24回糧供20–21；E26預付供22–23；E28新船供24–26；E32續入 | 每次由各責任人具名，不女帝一簽無限生糧；實際袋數按劇情比例與批次，入倉≠已分發，糧食不變銀票。 |
| permits | 父親舊失效通行牌與E39葉峻新合法牌 | E7舊牌出現→E13知失效→E25扣→E26不返；E39新牌另造 | 葉峻舊牌被公家扣證；新牌依法核發；新牌材質/編號清楚不同，不能只把舊牌翻面再發。 |
| identity-papers | 身世原件、裴的預寫副本、何靜縫合抄件 | E19原件葉讀，裴帶走COPY；E20原件羅杏封／何靜抄；E30原件公開 | 羅杏保原件；抄件不能憑空變原件；封袋繩與縫合邊不同，讀錯日期才是線索不靠魔法消字。 |
| public-case | 第30日處決文／罪責文／公開糧務契約／刑枷證物 | E1日期但姓名隱；E10本人知道；E34改同日晨；E37枷當證物；E40簽名先於冠 | 何靜/聯署人按程序管理；沈巧E33盒在場本人不在；日期用場內紙文與口述，CC關閉也不漏關键。 |

## 全40集攝製檢查

每集的完整cast、location、look候選、prop與CC檢查在JSON；下表只放該集獨有的主要拍法與最容易拍錯的地方。主鏡頭以一個主要動作為素材，其餘並列動作拆insert/反應。

| 集 | 主要鏡頭 | 風險 → 控制 | 來源 |
| --- | --- | --- | --- |
| 01 萬歲先喝這碗粥 | 一碗粥推到不動筷的人前 | 日期資訊偷渡成女主先知 → 只給觀眾日期且遮姓名，葉尚未知 | [source.mjs:626](./source.mjs#L626) |
| 02 先削我的宮宴 | 一日宴食配額改成賑糧 | 一晚削宴解決全季糧荒 → 只一天份，交單缺內廷副印仍懸而未決 | [source.mjs:684](./source.mjs#L684) |
| 03 滿帳空倉 | 雙層麻袋露縫與半倉 | 空鏡袋數未減仍報半倉 → 同尺度標示實收，拒簽全額 | [source.mjs:742](./source.mjs#L742) |
| 04 秤砣也會說謊 | 標準砝碼在兩秤得到不同結果 | 秤自己飄動成法術 → 同一校驗砝碼移位，官驗在場 | [source.mjs:802](./source.mjs#L802) |
| 05 只護這一趟 | 韓鐸交出有限護糧許可 | 掌軍許可等於全軍歸女主 → 只此趟糧隊與指定路，妹妹威脅紙另拍 | [source.mjs:862](./source.mjs#L862) |
| 06 把大車拆成小車 | 小船繩取代巨車出關線 | 改運路即免所有關税 → 仍遭同貨兩票，抵押不是皇印 | [source.mjs:923](./source.mjs#L923) |
| 07 有粥，也要有人看病 | 沈巧按名單把小車分到戶 | 饑民群聲擠入未登錄對白 → 群眾只環境聲，羅杏看舊收條另鏡 | [source.mjs:981](./source.mjs#L981) |
| 08 讓命令走出門 | 賈勳簽下實際交付量 | 簽收等於內廷副印到手 → 問題仍問印權，皇族紙批次是另證據 | [source.mjs:1042](./source.mjs#L1042) |
| 09 同一袋糧收兩次 | 同一車貨兩張徵收票並置 | 稅與借款翻成同一費目 → 兩欄讀清，三車仍被扣作代價 | [source.mjs:1104](./source.mjs#L1104) |
| 10 祭天名冊上的人 | 葉終於讀到自己處決姓名 | E1已知道卻再演驚訝 → 此刻第一次讀完整原文，未簽未表態 | [source.mjs:1166](./source.mjs#L1166) |
| 11 照你們的日子祭天 | 五州進度變成祭典附件 | 五州全經南門地理錯亂 → 南三州與北兩州分路，只准查一關 | [source.mjs:1238](./source.mjs#L1238) |
| 12 關卡不是誰的錢袋 | 無軍令號的路障被撤 | 英雄砍關口或取回當天新糧 → 三車晚一天放行，無合法軍令才撤 | [source.mjs:1298](./source.mjs#L1298) |
| 13 讓車替命令作證 | 公開車單讓首車先付 | 後續偽證罪失去知情鋪垫 → 葉明确知道失效並叫停，未上報留下責任 | [source.mjs:1360](./source.mjs#L1360) |
| 14 誰欠誰的糧 | 同車號與撕紙邊對上 | 一件假借款消所有欠款 → 限定這批偽造部分，真債另列 | [source.mjs:1420](./source.mjs#L1420) |
| 15 糧商不收空頭萬歲 | 唐敏只把可付批次推過來 | 商人突然無限供糧 → 支付/存糧上限具體可見，北路專約另揭 | [source.mjs:1482](./source.mjs#L1482) |
| 16 先把欠的餉送到手 | 軍屬糧單與商款清單分流 | 糧發軍戶被譯成銀子付商 → 两个物理欄；妹妹明日轉院時間另記 | [source.mjs:1543](./source.mjs#L1543) |
| 17 統領收到的那封信 | 醫療緩轉申請得到一天批示 | 韓鐸帶兵闖醫院或醫票印錯 → 無軍隊入內，只一天暫緩且右借桌印 | [source.mjs:1605](./source.mjs#L1605) |
| 18 換診的那一天 | 全體病患按公開名單轉移 | 只救妹妹破平等承諾 → 鏡頭先多名患者再她的右腕淡痕 | [source.mjs:1664](./source.mjs#L1664) |
| 19 養母沒有燒掉的紙 | 原件被讀，預寫副本被帶走 | 裴拿走唯一原件導致後面復生 → COPY在裴手，原件仍留可封存 | [source.mjs:1723](./source.mjs#L1723) |
| 20 把三份日期放在一起 | 三個日期來源合成認定 | 真姓名也被翻成假名 → 葉穗姓名真、皇族血统假，原件封袋可見 | [source.mjs:1782](./source.mjs#L1782) |
| 21 有糧的皇族 | 兩車卸貨後其餘二十八車停住 | 北線専約一揭就變強搶軍糧 → 尊重合法文件，未滿足條件車仍停 | [source.mjs:1853](./source.mjs#L1853) |
| 22 讓受災的人自己說 | 抱怨聲寫成請願原話 | 群眾忽然全都感恩 → 保留不信任與權源疑問 | [source.mjs:1913](./source.mjs#L1913) |
| 23 鎖住的不是空倉 | 官署配額再縮一格 | Day18–19庫糧被演成供整月 → 仅剩兩日，零買補缺不解專约 | [source.mjs:1975](./source.mjs#L1975) |
| 24 被扣住的軍糧 | 雙收糧沿原單退回 | 退稅被拍成現金發工資 → 是糧供Day20–21，工钱仍未解 | [source.mjs:2035](./source.mjs#L2035) |
| 25 被抓的運糧人 | 舊通行牌放上罪證桌 | 葉之前不知造牌卻被逼認 → 承接Day8知失效未報，不認莫須有搶劫 | [source.mjs:2095](./source.mjs#L2095) |
| 26 親人也不能免帳 | 三張獨立證詞分別確認 | 證人同聲串供或舊牌立刻返還 → 各自來源；牌扣證不返，新糧只供22–23 | [source.mjs:2155](./source.mjs#L2155) |
| 27 不是誰的私印 | 自己責任與未付糧款同頁 | 承錯後責任只剩反派 → 葉先簽自己的部分，裴拒自己的款 | [source.mjs:2213](./source.mjs#L2213) |
| 28 一場婚姻，一顆人頭 | 私談婚約威脅完畢才讓唐進 | 唐敏偷聽到不该知道血统秘密 → 先完成私談，唐只帶24–26糧批 | [source.mjs:2273](./source.mjs#L2273) |
| 29 留給她的最後一頁 | 錯誤與血統知情日期寫完再摘冠 | Day14知道被误成Day15才初知 → 區分初知與次日驗證，冠從此離頭 | [source.mjs:2332](./source.mjs#L2332) |
| 30 朕有話要說 | 身世原封公開，觀眾有不同反應 | 公開立即全體擁戴 → 混合反應，裴停糧的代價落地 | [source.mjs:2393](./source.mjs#L2393) |
| 31 有人留下，有人轉身 | 三人共同签而不是再次加冕 | 無冠章節又生成金冠 → 固定無冠look，當天是最後配給日 | [source.mjs:2465](./source.mjs#L2465) |
| 32 刀守的是哪條路 | 小糧車通過依法守住的路 | 韓恢復舊君絕對命令 → 用保城本權，不用女主血統號令 | [source.mjs:2527](./source.mjs#L2527) |
| 33 三張桌拼成一本帳 | 三份文件封在共同箱 | 沈巧因道具箱在場變第五人 → 盒代表既有證據，沈巧無臉無新聲 | [source.mjs:2585](./source.mjs#L2585) |
| 34 午間送到的調兵令 | 同交付號暴露假軍令 | 祭典提前變成Day29處決 → 只Day30午→晨，何靜被帶問話 | [source.mjs:2643](./source.mjs#L2643) |
| 35 同一張約，兩個主人 | 無何靜的桌上比兩份敵方附件 | 何靜被押仍遠程神解题 → 靠已在手文件，蕭決定自己的私糧封契 | [source.mjs:2702](./source.mjs#L2702) |
| 36 祭天臺上的核帳桌 | 何靜先獲釋再上公開台 | 何在台上瞬移或裴突然自愿認罪 → 先建立釋放，蕭封契與欠款链逼出簽字 | [source.mjs:2760](./source.mjs#L2760) |
| 37 交出那枚調兵印 | 韓只收威脅武器，枷成證物 | 女主直接公開處死反派 → 依法羈押查款，葉也簽知情審查 | [source.mjs:2818](./source.mjs#L2818) |
| 38 讓下一道命令也能被問 | 各地回函有支持也有限制 | Day31–40被剪成瞬間大團圓 → 保留欠款、過失及共同權限制 | [source.mjs:2874](./source.mjs#L2874) |
| 39 第一批新糧 | 新糧與新合法牌在春光同框 | 把被扣舊牌拿回當赦免 → 新编號新核发，Day120且追款未完 | [source.mjs:2935](./source.mjs#L2935) |
| 40 先看帳，再叫萬歲 | 先簽葉穗，再戴金冠 | E40又換粥或先加冕再簽 → 沈巧問糧、何靜答账，不重造E1對話 | [source.mjs:2455](./source.mjs#L2455) |

## 聲音、四語與CC

以下voice沿用來源合適提案，未試聽未驗收。zh-TW用自然台灣國語，音量不替代表演；其他三語先按同一角色身份試錄，母語審聽後可調voice。外語人名是發音草案，日/韓字形不當正式譯名定案。

| 角色 | 聲線與表演 | zh-TW / ja / ko / en發音草案 |
| --- | --- | --- |
| 葉穗 / ye-sui | Kore；臺灣國語；年輕女聲、低而清楚，憤怒時降低音量，未試聽。 | Yè Suì / イエ・スイ / 예 쑤이 / Ye Sui |
| 裴定衡 / pei-dingheng | Charon；臺灣國語；成熟低男聲，字間留白，少吼叫，未試聽。 | Péi Dìng-héng / ペイ・ディンホン / 페이 딩헝 / Pei Dingheng |
| 韓鐸 / han-duo | Orus；臺灣國語；中低男聲，短句沉穩、救援時加快而不咆哮，未試聽。 | Hán Duó / ハン・ドゥオ / 한 둬 / Han Duo |
| 羅杏 / luo-xing | Vindemiatrix；臺灣國語；帶些沙質的成熟女聲，溫和、短促口語，未試聽。 | Luó Xìng / ルオ・シン / 뤄 싱 / Luo Xing |
| 葉峻 / ye-jun | Puck；臺灣國語；明亮青年男聲，急但不油滑，未試聽。 | Yè Jùn / イエ・ジュン / 예 쥔 / Ye Jun |
| 何靜 / he-jing | Aoede；臺灣國語；清晰中音女聲，數字與停頓分明，未試聽。 | Hé Jìng / ホー・ジン / 허 징 / He Jing |
| 唐敏 / tang-min | Pulcherrima；臺灣國語；較低、較厚的中年女聲，談價直接不拖泥帶水，未試聽。 | Táng Mǐn / タン・ミン / 탕 민 / Tang Min |
| 賈勳 / jia-xun | Fenrir；臺灣國語；粗中音男聲，官腔刻意、語速偏快，未試聽。 | Jiǎ Xūn / ジア・シュン / 자 쉰 / Jia Xun |
| 蕭承越 / xiao-chengyue | Algieba；臺灣國語；平穩清亮男聲，禮貌的壓力勝於嘶喊，未試聽。 | Xiāo Chéng-yuè / シャオ・チョンユエ / 샤오 청웨 / Xiao Chengyue |
| 韓芮 / han-rui | Leda；臺灣國語；較輕柔的青年女聲，句尾堅定，未試聽。 | Hán Ruì / ハン・ルイ / 한 루이 / Han Rui |
| 沈巧 / shen-qiao | Gacrux；臺灣國語；低沉年長女聲，氣息稍慢、語意清楚，未試聽。 | Shěn Qiǎo / シェン・チャオ / 선 차오 / Shen Qiao |

- 冠珠是權力條件音：E1壓頭、E29離開、E40簽後返回，無冠段不在配樂偷偷重現加冕聲。
- 糧袋、秤、算珠、印章各有可辨短音；內廷副印不與南關雙印共享聲標。
- 公文段用一個讀數接一個反應，禁止人聲/旁白/配樂三層同時爭理解。

- 粥/御膳是食物，賦稅/借糧/官欠/預付/糧額分開；古風敬稱不能把條件責任譯成絕對赦免。
- Day14知情和Day15驗證、Day30午改晨，日期用四語一致事件表，不能字面本地曆法換算。
- 葉穗是真姓名而非皇族假名；借位女帝/血統不實不等於她所有敕令自動作廢。

旁白依來源[source.mjs:39](./source.mjs#L39)，不得跟本劇角色共用聲線。字幕出軌後逐條查說話者、標點、當地閱讀速度和轉場；翻譯要對每語音軌對時，不復制繁中CC時間碼。關鍵資訊不只靠左右聲道，必測mono與手機外放。

## 預告素材與留存

E1日期遮名、E3雙袋縫、E10讀到姓名，至「第30日」停；不要用E20血統結論、E29摘冠、E36簽供或E40再加冕。

每段糧政對話配一個能被看懂的量變：少半倉、兩秤、同車雙票、兩車卸二十八車停。Day23–30以配給剩幾天與紙面責任串起，避免重複宣言抵消倒數。

先驗前5秒能聽懂衝突、30秒取得第一回報，再看30秒/1分鐘/3分鐘留存、換篇退出與實際點擊觀看的落差；不用空剪節奏或故意截斷已說一半的答案換點擊。百萬點閱是目標，沒有保證。

## 待完成驗收

- 金冠戴／摘／重戴的命名造型與逐鏡工具已備妥，待實際切鏡與人物圖驗收。 E29摘冠前crowned、摘後uncrowned；E40簽名前uncrowned、簽後recrowned，髮簪保留。需要驗證生成畫面確實按順序切換，毋須再開發造型工具。（E1、E29、E40）
- 糧批、三枚印與原件／副本的連戲規則已列入prop_rules，待美術素材和動態插鏡驗收。 按已定的印章輪廓、票據欄位、封袋/縫合邊與各批供應日期製作；剩下核對實際道具文字、唯一性及持有人，不再等待另一份規劃裁定。（E6、E9、E17、E19、E20、E24、E26、E28、E34）
- 四語敬稱與制度術語尚未母語配音聽校。 稱謂可壓縮但責任與條件不可減省。（E10、E27、E36、E40）

- 使用已備妥的逐鏡造型資料做角色圖與動畫小樣，查同臉、方向、道具接觸與交接後狀態。
- zh-TW實際TTS、開場30秒剪輯、40集聲音/CC/全片驗收；之後ja/ko/en母語聽校。
- source變更需重驗hash；工具完成不代表付費生成、正式匯入、核准或上架已執行。

## 供應商能力：未成年入鏡尚未驗證

目前Veo 3.1 Lite的首格I2V路徑使用allow_adult；依[官方Veo能力文件](https://ai.google.dev/gemini-api/docs/veo)，不能把它當成未成年入鏡已支援。本輪只新增限制與來源，不改人物年齡、劇情或現有配音。

本稿沒有確認需要標記的現時未成年命名角色。

本劇登記角色年齡皆為20歲以上，現稿未確認任何未成年命名造型或必拍年少回望。因此不推測新增minor旗標；背景群眾若後續安排兒童，仍需在分鏡前明列並驗證該製作路徑。

character.video_constraints標記實際未成年人物；只有畫外聲不自動禁止中文配音。分鏡需區分說話者與畫面內人物，但不能靠背影、局部、卡通畫風或省略年齡宣稱繞過限制成功。必須保留原設年齡，先選手繪動畫或合法可支援相應年齡的供應商，做含該人物的pilot確認能力與效果再放量。此批不能宣稱已可直接全400集拍完；通過離線設計檢查也不代表供應商或成片已驗收。
