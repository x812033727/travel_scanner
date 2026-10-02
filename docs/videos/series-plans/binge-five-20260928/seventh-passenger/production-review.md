# 末班車上的第七個活人｜製作覆核與攝製設計

2026-10-01。本輪逐集核對40集的衝突、轉折、結尾、人物/道具狀態，並對照設定、opening_30_seconds、continuity_notes與上一輪修訂；未發現新增可確定的劇情矛盾。以下是可實作的攝製設計與風險控制，並非渲染、試聽、母語翻譯或正式站驗收。

來源绑定：`8da292c58ddf96e4fe4b7ba7af625bcffc8322795afd64b3945c09b874e5701c`（SHA-256 of JSON.stringify(source)）。完整機器可讀資料在 [production-design.json](./production-design.json)，共40集、10名角色、7個開場鏡頭。

## 交付與核准邊界

先完成zh-TW台灣口音版；ja/ko/en先做名詞與發音預備，中文版鎖定後各自TTS與CC。所有字幕為可開關CC，沒有繁中或外語燒錄字幕。劇內文件、鐘與標示是物件；關閉CC時仍需由鏡頭和原稿台詞理解。現有README或舊setting中燒錄／五語CC描述依此次新授權改為共享 [profile](../../production-20261001/profile.json)，不讓過期規格回流。

採Gemini veo-3.1-lite-generate-preview，1080p/24fps每次8秒素材；主要行為一鏡一動作，剪取3–6秒，餘反應/插入另片。沒有referenceImages或extension；不可freeze補時。此批正片採clips-only：紙證與觀察也有可信的手部、視線或環境動作；重要文字先核對再合成到動態插鏡。仍圖只供前製animatic，不能混稱完成動畫。原生模型音訊不用作台詞主軌，後製分角色人聲、音效、環境、配樂。

## 拍攝語言

窄車廂綠灰、原始機械乳白、覆寫紅光；紅色不等於每句是假。固定一扇門重用，不生成每站新場景。

程望通常在門內畫左，假月台畫右；門底鋼印下、電子牌上，兩層資訊各有insert。六席布局與售票隔間位置全片固定。

不以鬼叫演恐怖；相信→核對→選擇看得見。小滿咳嗽逐漸增加，後段不可突然跑跳；母親真偽使用同音色，聲音不能洩露答案。

七名活人、三位亡者；票和白燈不回現實，何照制服E27中段脫下，E38四人是病人服；E34後真母親不再靈異發聲。

## 開場0–30秒

來源：[source.mjs:528](./source.mjs#L528)、[source.mjs:566](./source.mjs#L566)。以下秒數是剪輯目標，實際TTS與成片尚未量測；每格內若列反打/插入，拆成單動作素材後剪接，不能要求模型一次完成整段蒙太奇。

| 時間 | 機位 | 畫面行為 | 對白意圖與聲音 |
| --- | --- | --- | --- |
| 0–5秒 | CU；門框側面固定 | 程望指節扣門框，門外母親伸手；人物不先跨門 | 我媽死了七年，卻叫我下車；第一句近乾聲，列車輪聲在底 |
| 5–8秒 | insert；上方電子牌固定 | 電子牌亮家字，不能當真月台號 | 母親聲音到家了從紅廣播出；同一母親聲音，不加邪惡變調 |
| 8–10秒 | ECU；向下切而非長掃 | 實體04鋼印出現在門底 | 無新增台詞；車輪聲不中斷，輕金屬聲 |
| 10–16秒 | MCU；門內側平視 | 小滿抓住程望衣角，另一手展示他的17原票 | 你的票，跟這裡不一樣；衣料受力、短句清楚 |
| 16–20秒 | ECU；固定雙物件比較 | 17原票貼近04實體印，數字在同一清晰焦面 | 留讀取時間，不再加規則講解；低頻暫退，只有票紙與輪聲 |
| 20–25秒 | MCU；回到原門內軸線 | 程望收回腳，母親笑容停住但不變怪物 | 先別開門；聲線維持人性，禁尖銳jump scare |
| 25–30秒 | wide；門內固定 | 門正常合起，把母親隔在外；先證明一次拒絕有效 | 不加結果旁白或片頭卡；只留車輪聲，門鎖輕響 |

## 角色造型與表演

本輪已完成characters[].shot_looks目錄及scene.data.character_looks逐鏡選擇的工具整合；下列完整外觀資料已可隨新製作bundle傳入工人。原始故事source保持不變，原有按集looks仍可並存。候選episodes不是整集覆寫命令；鏡頭照cue選造型，同一人物的臉與身份保持一致。工具與資料已具備，實際角色圖、動作、聲音及成片仍待驗收。

| 角色 / 候選ID | 涉及集 | 造型與切換條件 | 來源 |
| --- | --- | --- | --- |
| cheng-wang / cheng-wang-patient | E38 | Taiwanese man, 27, lean rectangular face, short black hair with a fixed left part, tired dark eyes, narrow old scar across right thumb. Plain hospital patient clothing, resting in a hospital bed. No travel jacket, raincoat, hoodie, necktie, staff badge, ticket or lantern. 院內本人，不沿用旅途外套；右掌敷料與拇指舊疤保留。 | [source.mjs:53](./source.mjs#L53)、[source.mjs:2816](./source.mjs#L2816) |
| cheng-wang / cheng-wang-age20 | E15 | Taiwanese adult man, 20, lean rectangular face, short black hair with the same fixed left part, dark eyes and recognizable adult facial proportions. Charcoal work jacket over a faded grey shirt, dark utility trousers and brown work shoes; narrow old scar across the right thumb. Less facial fatigue than the present-day 27-year-old, no childlike styling. No supernatural ticket, employee badge or guide lantern. 僅E15七年前事故的非連續短閃回；現時讀事故條的鏡頭仍選27歲base。由現時27歲減七年為20歲，直接採用已授權成年造型設計；不另造人物ID或變更聲線。 | [source.mjs:56](./source.mjs#L56)、[source.mjs:1414](./source.mjs#L1414) |
| lin-xiaoman / lin-xiaoman-patient | E38 | Taiwanese girl, 17, petite wiry build, blunt chin-length black bob tucked behind the right ear, alert eyes, red elastic band on left wrist. No glamour styling. Plain hospital patient clothing, resting in a hospital bed. No travel jacket, raincoat, hoodie, necktie, staff badge, ticket or lantern. 院內本人，不沿用旅途外套；右掌敷料與拇指舊疤保留。 | [source.mjs:84](./source.mjs#L84)、[source.mjs:2816](./source.mjs#L2816) |
| qiao-ning / qiao-ning-patient | E38 | Taiwanese woman, 34, average build, oval face, black hair in a neat low bun, plain silver stud earrings. Capable restrained gestures. Plain hospital patient clothing, resting in a hospital bed. No travel jacket, raincoat, hoodie, necktie, staff badge, ticket or lantern. 院內本人，不沿用旅途外套；右掌敷料與拇指舊疤保留。 | [source.mjs:138](./source.mjs#L138)、[source.mjs:2816](./source.mjs#L2816) |
| he-zhao / he-zhao-coated | E4、E6、E10、E12、E18、E20、E21、E26、E27 | Taiwanese man, 24, slight build, pale narrow face, short uneven black fringe, plain white shirt, loose maroon tie, dark trousers, worn trainers, bandage on right palm. An oversized navy conductor coat over the shirt, crooked brass employee badge on the coat, maroon tie. The right-palm bandage remains. E27中段前才穿；分鏡脫衣後用base，episode override不能整集覆蓋。 | [source.mjs:219](./source.mjs#L219)、[source.mjs:742](./source.mjs#L742) |
| he-zhao / he-zhao-patient | E38 | Taiwanese man, 24, slight build, pale narrow face, short uneven black fringe, a clean dressing on the right palm. Plain hospital patient clothing, resting in a hospital bed. No travel jacket, raincoat, hoodie, necktie, staff badge, ticket or lantern. 院內本人，不沿用旅途外套；右掌敷料與拇指舊疤保留。 | [source.mjs:219](./source.mjs#L219)、[source.mjs:2816](./source.mjs#L2816) |

## 道具與空間連戲

依[source.mjs:36](./source.mjs#L36)、[source.mjs:3034](./source.mjs#L3034)；特殊道具以獨立參考圖與交接鏡追蹤，列出的外觀差異屬美術選擇，不能改原有劇情因果。

| ID | 唯一性 | 狀態 | 持有人與拍法 |
| --- | --- | --- | --- |
| ticket-system | 七張原票與陸安亡票 | 程望00:31，小滿00:17，其餘各異；票孔跟原主心跳 | 每人本人持；何照E27取回；小滿E29由老人扶穩但仍在本人衣袋；可讀字用後製平面，七組光/嗒不同但不把聲音當醫療教學。 |
| platform | 電子牌、實體月台鋼印、機械箭頭 | E1 04；E3 06；E31電子17但實體09；E37三項吻合17 | 環境固定物；三層分鏡，不把電子17作放行證據。 |
| lights | 工作手電與黃銅白燈兩物 | 手電E31交徐浩；白燈E34交程望 | E32無徐浩，借檢票座白燈；跨門後兩物都不在現實鏡頭；形狀和光源不同，不能把早期手電拍成引導權限。 |
| bags | 小滿藍背包與顧永布購物袋 | 小滿包E29交顧；布袋E40由程望代提 | 每物僅一個；交接前後不能複製；顧固定外觀內袋子需構圖/shot override處理。 |
| whistle | 裂木鳥哨與幻景完好哨 | E14陳列盒裂哨對照；E35交陸循 | 真哨E35後陸循右手；亡票仍歸陸循；不修好哨子、不拍女兒新行動暗示復活。 |
| belt | 長安全帶 | E17取得卷收程望衣內；E27再用 | 程望保管；與購物袋短帶不可混換。 |

## 全40集攝製檢查

每集的完整cast、location、look候選、prop與CC檢查在JSON；下表只放該集獨有的主要拍法與最容易拍錯的地方。主鏡頭以一個主要動作為素材，其餘並列動作拆insert/反應。

| 集 | 主要鏡頭 | 風險 → 控制 | 來源 |
| --- | --- | --- | --- |
| 01 她在月台等我 | 17票與04鋼印同焦後收腳 | 三名全身同鏡導致多手拉扯 → 拉衣、貼票、收腳拆鏡，每鏡只一動作 | [source.mjs:566](./source.mjs#L566) |
| 02 還沒到的死期 | 六票節拍後移到隔間弱第七拍 | 配樂遮住第七聲或畫第七人 → 一拍一票對位，隔間只暗示不露人 | [source.mjs:624](./source.mjs#L624) |
| 03 這次換我拉住妳 | 原票固定扶手後讓小滿自己鬆手 | 被拍成程望推小滿出門 → 方向固定向車內，最後腳落內側 | [source.mjs:683](./source.mjs#L683) |
| 04 紅字底下有白字 | 紅漆沾手套與底下返字 | 新紅字直接變唯一真假判定 → 返只露一字、資料尚不完整 | [source.mjs:742](./source.mjs#L742) |
| 05 借來的名字 | 換回票後小名仍想不起 | 把失憶錯誤歸給換票 → 原壓痕在換票前存在，後面再驗 | [source.mjs:799](./source.mjs#L799) |
| 06 窗上那天不是今晚 | 收據車組號與牌底同號 | 日期或停錶直接當死亡證據 → 五月二十七日只月日，不畫當夜同日期 | [source.mjs:859](./source.mjs#L859) |
| 07 媽媽以前這樣敲門 | 白燈口聲音引向鉚釘 | 暗號被配成可信母愛theme → 此時不建立正確答案音樂；手機不拿出 | [source.mjs:920](./source.mjs#L920) |
| 08 票跟著誰的心跳 | 交換手後票光仍跟同一人 | 光跟持票人而非原主走 → 記錄每票節拍對應主人，換手保持 | [source.mjs:979](./source.mjs#L979) |
| 09 把老人帶回座位 | 購物袋受拉但老人腳留車內 | 老人危機被誇成受傷墜落 → 只動袋帶、腳步退回，無新傷 | [source.mjs:1042](./source.mjs#L1042) |
| 10 覆漆底下那條線 | 揭紅覆片，拓下白線到17 | 揭太多文字提前完結謎團 → 只返程線，留置完整條文E22才露 | [source.mjs:1103](./source.mjs#L1103) |
| 11 只寫驗過的事 | 已驗/待驗兩欄各擺一物 | 所有紅字皆假被配音講真理 → 喬寧當場糾正，列已驗證據 | [source.mjs:1177](./source.mjs#L1177) |
| 12 售票人在怕什麼 | 員工牌無姓名，鏡頭停在上鎖抽屜 | 誤拍何照不知道全名 → 他是恐懼不敢報，不是失憶 | [source.mjs:1237](./source.mjs#L1237) |
| 13 兩個一樣的敲門聲 | 同一敲門節奏從兩方向響 | 靠變聲提前判真偽 → 畫面標聲道，內容仍須E19核對 | [source.mjs:1296](./source.mjs#L1296) |
| 14 每一站都問同一句 | 女孩同句與完好哨三次重播 | 生成三版台詞失去重複證據 → 同語系同一take重用，裂哨倒影非持在手 | [source.mjs:1356](./source.mjs#L1356) |
| 15 玻璃後的事故條 | 事故條與短客觀片段對位 | E15同集20歲客觀回望與27歲現時調查混用造型，或把短閃回演成新記憶恢復。 → 短閃回鏡用cheng-wang-age20；現時玻璃前查證回cheng-wang--base。先顯母親推到救援端的原稿動作，再回已有事故條，不另加童年情節。 | [source.mjs:1414](./source.mjs#L1414) |
| 16 團聚的收據 | 三步壓痕依序對照唐綺敘述 | 把被摸票也算交易 → 選段、答應、按票需三步完整 | [source.mjs:1474](./source.mjs#L1474) |
| 17 急救櫃要一段回憶 | 長帶拉老人到實地後程望想不起味道 | 救援只剩動作爽點忽略代價 → 停留程望尋詞失敗，不演已失記憶新回放 | [source.mjs:1534](./source.mjs#L1534) |
| 18 他不肯亮出自己的票 | 程望先亮己票，何照揭玻璃遮紙 | 檔案解說沒有行動代價 → 原票冒被扣風險、兩分鐘確實失去 | [source.mjs:1594](./source.mjs#L1594) |
| 19 白燈那頭是誰 | 程望核對編號與票印方向後才低聲叫媽；唐綺只記錄 | 聲音溫柔就等於真母親 → 編號與票印方向兩證明都入鏡 | [source.mjs:1655](./source.mjs#L1655) |
| 20 紅拉桿壓住了什麼 | 紅桿與走紙錯路互相對照 | 給母親新控制紅桿能力 → 她只白燈口聲音，元凶紅桿遮擋有因果 | [source.mjs:1714](./source.mjs#L1714) |
| 21 地圖上的十七號 | 普通17月台圖被遮前拓兩份 | 陸循遠端回話增加第五聲線 → 只有遮板落下不配陸循聲 | [source.mjs:1787](./source.mjs#L1787) |
| 22 壓在白牌上的表框 | 空表推回，卸表框露完整規則 | 原文畫成七人湊齊魔法 → 只寫時限內皆可，名單是管理工具 | [source.mjs:1851](./source.mjs#L1851) |
| 23 他要加進清單的票 | 亡女票截止早已過去再現飯桌 | 一瞬無光等同不可救 → 先日期/時限比對，亡女不登場 | [source.mjs:1909](./source.mjs#L1909) |
| 24 飯桌又擺上來了 | 程望能看湯卻說不出味道 | 新生成回答會破坏幻景限制 → 新問題後留原句重播，不能回答 | [source.mjs:1969](./source.mjs#L1969) |
| 25 兩張票換一頓飯 | 拉下遮光簾轉身向活人 | 跨門被拍成溫柔團聚 → 決定留現實，沒有跨過假門 | [source.mjs:2029](./source.mjs#L2029) |
| 26 不把誰劃掉 | 七行清單不刪人，何照去後槽 | 何照突然穿牆取票 → 建立後側機械扣和門關上 | [source.mjs:2089](./source.mjs#L2089) |
| 27 夾在門縫裡的名字 | 票先滑出，再脫外套出門縫 | episode look把脫衣後仍畫制服 → 同集前後兩look、牌落地後不回身 | [source.mjs:2150](./source.mjs#L2150) |
| 28 紅廣播一直改站名 | 四步表隨原走紙逐格畫出 | 長講解壓垮節奏 → 一格配一個已見實物，最後停未完成欄 | [source.mjs:2209](./source.mjs#L2209) |
| 29 她的票快不亮了 | 小滿票固定衣袋，老人接背包 | 看似已死又復活 → 不宣告死亡，保留截止未到台詞 | [source.mjs:2269](./source.mjs#L2269) |
| 30 最後一趟，不會再等 | 母親指鐘，何照拿自己副本核對 | 錯拿程望收藏的另一份副本 → 何照取自己保留的一份，不從主角口袋拿 | [source.mjs:2329](./source.mjs#L2329) |
| 31 電子牌提前亮了 | 電子17切實體09，再交工作燈 | 兩個17被當核對完成 → 必須等E37實體17和箭頭同符 | [source.mjs:2401](./source.mjs#L2401) |
| 32 每個人守一件事 | 三人各守一位置穩住箭頭 | 多人同框身份與手交疊 → 每鏡最多三cast；顧永膝傷不跑 | [source.mjs:2463](./source.mjs#L2463) |
| 33 窗外還有好多個家 | 徐浩親手關掉像家的普通門景 | 偷造徐浩女兒新影像 → 只泛化舊站務門，情緒靠徐浩 | [source.mjs:2524](./source.mjs#L2524) |
| 34 檢票座上的那盞燈 | 貼原票後握燈柄，母影離開 | 母親在下一集再指路 → 白光倒影永久消失、燈仍亮 | [source.mjs:2585](./source.mjs#L2585) |
| 35 陳列盒裡的木哨 | 裂哨從盒到父親右手 | 同時左手松桿導致提前通關 → 右手拿哨左手壓桿到E36 | [source.mjs:2642](./source.mjs#L2642) |
| 36 最後一根拉桿 | 亡票與活票並排後陸循放桿 | 拍父女重逢獎勵反派 → 女孩不現身，亡票哨留他手 | [source.mjs:2701](./source.mjs#L2701) |
| 37 門外傳來站聲 | 三條件核對後清單先三後四 | 時限兩秒被看成現實操作時長 → 主觀延時不偷改鐘；先核驗才過門 | [source.mjs:2757](./source.mjs#L2757) |
| 38 監視器還在響 | 七人穩定名單與四張病人面孔 | 旅途外套和靈界物品混入 → 四人病人look，原票白燈清零 | [source.mjs:2816](./source.mjs#L2816) |
| 39 那則沒聽過的留言 | 新晚餐上桌再播放舊留言 | 回放等於取回共餐記憶 → 留他依然想不起的反應，這餐是新的 | [source.mjs:2872](./source.mjs#L2872) |
| 40 這一站是今天 | 扶門與第一集扣門框同角度 | 再加恐怖尾音暗示新循環 → 不加鬼影；日常交通票代原票 | [source.mjs:2929](./source.mjs#L2929) |

## 聲音、四語與CC

以下voice沿用來源合適提案，未試聽未驗收。zh-TW用自然台灣國語，音量不替代表演；其他三語先按同一角色身份試錄，母語審聽後可調voice。外語人名是發音草案，日/韓字形不當正式譯名定案。

| 角色 | 聲線與表演 | zh-TW / ja / ko / en發音草案 |
| --- | --- | --- |
| 程望 / cheng-wang | Schedar；台灣國語；中低音、節奏穩、壓住恐懼，哭戲保留呼吸；擬定 casting 未試聽。 | chéng wàng / チョン・ワン / 청 왕 / Cheng Wang |
| 林小滿 / lin-xiaoman | Zephyr；台灣國語；年輕清亮、帶氣但不幼態，疲弱段維持同一音色；擬定 casting。 | lín xiǎo mǎn / リン・シャオマン / 린 샤오만 / Lin Xiaoman |
| 顧永 / gu-yong | Algenib；台灣國語；年長柔厚、略沙啞、清楚不拖拍；擬定 casting。 | gù yǒng / グー・ヨン / 구 융 / Gu Yong |
| 喬寧 / qiao-ning | Kore；台灣國語；沉穩、清晰、安撫但不刻板播報；擬定 casting。 | qiáo níng / チャオ・ニン / 차오 닝 / Qiao Ning |
| 徐浩 / xu-hao | Fenrir；台灣國語；粗亮、急句但不吼滿全場，後段放低聲量；擬定 casting。 | xú hào / シュー・ハオ / 쉬 하오 / Xu Hao |
| 唐綺 / tang-qi | Aoede；台灣國語；乾淨柔亮、控制顫音，不唱台詞；擬定 casting。 | táng qǐ / タン・チー / 탕 치 / Tang Qi |
| 何照 / he-zhao | Puck；台灣國語；青年中音、前段虛浮吞尾，取回身分後穩定；擬定 casting。 | hé zhào / ホー・ジャオ / 허 자오 / He Zhao |
| 陸循 / lu-xun | Orus；台灣國語；低沉、整齊停頓，與顧永的鬆軟高齡聲分開；面對遺物時才破句；擬定 casting。 | lù xún / ルー・シュン / 루 쉰 / Lu Xun |
| 溫蘭音 / wen-lanyin | Sulafat；台灣國語；溫暖中低女聲、近距離少混響；假廣播可以完全相同，真偽靠規則判斷；擬定 casting。 | wēn lán yīn / ウェン・ランイン / 원 란인 / Wen Lanyin |
| 陸安 / lu-an | Leda；台灣國語；兒童記憶片段，少量自然台詞，不尖叫、不誘惑；聲音與小滿不同；擬定 casting。 | lù ān / ルー・アン / 루 안 / Lu An |

- 票孔嗒聲與輪聲分頻；七節奏先分組呈現，不要求觀眾從混音中精算七個心跳。
- 三短一長的真假是同素材重用；陸安每語系只一個固定句take，三次播出停頓完全相同。
- E34交燈撤低頻，E39舊錄音不使用靈異混響，E40自然日光與站聲結束。

- 17/04/06/09需每語系讀作編號而非時間；00:17/00:31才是時刻。
- 死亡時間欄保留角色初期誤解；E30才確認是各人搶救截止，翻譯不可提前解答。
- 記不得小名≠不知全名，何照知道姓名只是受脅迫不敢說；返程不譯成亡者回家。

旁白依來源[source.mjs:34](./source.mjs#L34)，不得跟本劇角色共用聲線。字幕出軌後逐條查說話者、標點、當地閱讀速度和轉場；翻譯要對每語音軌對時，不復制繁中CC時間碼。關鍵資訊不只靠左右聲道，必測mono與手機外放。

## 預告素材與留存

E1亡母招手、17對04、收腳；E2只給六票第七響。禁用何照原票姓名、E18亡者名冊、E20真用途、E34告別與E38七人生還。

E11–23把每份文件對照配一個物理行動與代價：遮板、讓票靠近陸循、丟兩分鐘、推回表格；避免連續六分鐘純口頭規則。E31回用E1鋼印構圖建立觀眾能自行解题的回報。

先驗前5秒能聽懂衝突、30秒取得第一回報，再看30秒/1分鐘/3分鐘留存、換篇退出與實際點擊觀看的落差；不用空剪節奏或故意截斷已說一半的答案換點擊。百萬點閱是目標，沒有保證。

## 待完成驗收

- 何照E27脫車掌外套與E38四人病人服已具完整命名造型及逐鏡工具，待畫面驗收。 E27轉折前選he-zhao-coated，脫下後回he-zhao--base；E38用四人的patient造型。需在實際畫面確認員工牌不重生、病人服無旅途配件。（E27、E38）
- 程望E15的20歲回望造型已加入目錄，待同一人物的成年年齡連戲驗收。 cheng-wang-age20僅用七年前短閃回；現時鏡仍用27歲base。20歲為27減7，屬成年造型；不增加新角色、不改小滿/陸安年齡。（E15）
- 七節拍、真假母聲及四語重複句仍待實際mono/耳機/手機試聽。 文字規則通過不代表觀眾聽得到關鍵證據。（E2、E8、E13、E14、E19）
- 林小滿（lin-xiaoman）明確17歲，Veo Lite I2V未驗證可生成其入鏡畫面。 目前首格I2V的allow_adult能力不代表允許未成年人顯影；不能把角色改為成年人，也不能以背影、局部、卡通風格或不提年齡當可保證捷徑。需經核可的手繪動畫或合法支援該年齡的供應商先做pilot、確認能力與交付再排量。僅畫外配音不因此自動受阻，逐鏡按實際可見人物判斷。（E1、E3、E7、E9、E10、E12、E14、E17、E21、E29、E37、E38、E40）
- 陸安（lu-an）明確9歲，Veo Lite I2V未驗證可生成其入鏡畫面。 目前首格I2V的allow_adult能力不代表允許未成年人顯影；不能把角色改為成年人，也不能以背影、局部、卡通風格或不提年齡當可保證捷徑。需經核可的手繪動畫或合法支援該年齡的供應商先做pilot、確認能力與交付再排量。僅畫外配音不因此自動受阻，逐鏡按實際可見人物判斷。（E14）

- 使用已備妥的逐鏡造型資料做角色圖與動畫小樣，查同臉、方向、道具接觸與交接後狀態。
- zh-TW實際TTS、開場30秒剪輯、40集聲音/CC/全片驗收；之後ja/ko/en母語聽校。
- source變更需重驗hash；工具完成不代表付費生成、正式匯入、核准或上架已執行。

## 供應商能力：未成年入鏡尚未驗證

目前Veo 3.1 Lite的首格I2V路徑使用allow_adult；依[官方Veo能力文件](https://ai.google.dev/gemini-api/docs/veo)，不能把它當成未成年入鏡已支援。本輪只新增限制與來源，不改人物年齡、劇情或現有配音。

| 角色 ID | 明確視覺年齡 | 登記出場集（非每鏡都入鏡） | 年齡來源 |
| --- | --- | --- | --- |
| 林小滿 / lin-xiaoman | 17歲 | E1、E3、E7、E9、E10、E12、E14、E17、E21、E29、E37、E38、E40 | [source.mjs:87](./source.mjs#L87)、[source.mjs:88](./source.mjs#L88) |
| 陸安 / lu-an | 9歲 | E14 | [source.mjs:299](./source.mjs#L299)、[source.mjs:300](./source.mjs#L300) |

程望27歲，E15事故回望在七年前，算得當時20歲，不能把「年少回望」字眼誤標為未成年；已補cheng-wang-age20完整造型，僅用E15短閃回，現時鏡仍27歲。陸安是「顯影9歲」，亡者或記憶影像身份不改變視覺年齡限制。

character.video_constraints標記實際未成年人物；只有畫外聲不自動禁止中文配音。分鏡需區分說話者與畫面內人物，但不能靠背影、局部、卡通畫風或省略年齡宣稱繞過限制成功。必須保留原設年齡，先選手繪動畫或合法可支援相應年齡的供應商，做含該人物的pilot確認能力與效果再放量。此批不能宣稱已可直接全400集拍完；通過離線設計檢查也不代表供應商或成片已驗收。

## 2026-10-02 配音與聲音細節覆核

本輪只有來源文字與製作設計覆核，沒有實際TTS、試音、SFX音檔或成片驗收。新增performance_states、audio_cues、audition_scenes每筆均為proposed，綁定集數與來源。source_excerpt只供語境，不能整段念成台詞；line_samples僅逐字引用已有原台詞，其餘試音段落待本集定稿取樣。

- E13紅廣播催前門、白燈口報編號同聲線但不同台詞take；只共用三短一長節奏，不能複製不同內容。
- E14陸安三次同句才是同一take重播，和E13分開。
- E19是程望查證後叫媽；E34後不新增靈異母聲，E39為另一時刻普通生前留言。

### 角色表演狀態

| 角色 / state | 集數 | 演出重點 | 來源 |
| --- | --- | --- | --- |
| cheng-wang / cheng-proof-then-mom | E19 | 兩項證據核對後才叫媽；查證前觀察節奏，確認後低音量放下防備；叫媽主體只能程望，唐綺只記錄。 | [source.mjs:1744](./source.mjs#L1744) |
| lin-xiaoman / xiaoman-cough | E14 | 17歲，咳嗽加重但清醒；咳在句間，仍能判斷重複句；不演已瀕死昏迷。 | [source.mjs:1444](./source.mjs#L1444) |
| lin-xiaoman / xiaoman-intermittent | E29 | 意識時斷時續，尚未截止；短氣息與少量反應依定稿，不長篇流暢獨白、持續慘叫或死亡音效。 | [source.mjs:2359](./source.mjs#L2359) |
| he-zhao / he-fears-name | E12 | 記得全名，只因威脅不敢報；吞嚥和避開姓名，不演真的失憶；保持24歲Puck。 | [source.mjs:1281](./source.mjs#L1281) |
| he-zhao / he-reclaimed-name | E27 | 拿票、報名並承認洩密；起句完整但氣息仍緊，不突然換成無畏人格或抹掉責任。 | [source.mjs:2194](./source.mjs#L2194) |
| wen-lanyin / mother-same-identity | E13、E19 | 真假通道同音色，靠證據確認；同一Sulafat與基本溫度，不能邪惡降調或善良耳語先判真假；E13兩內容分錄take。 | [source.mjs:1386](./source.mjs#L1386)、[source.mjs:1744](./source.mjs#L1744) |
| wen-lanyin / mother-release | E34 | 确认程望握燈後結束迴路；簡短平常，不擴成新告別演說；迴路斷後无新低語或呼名。 | [source.mjs:2672](./source.mjs#L2672) |
| wen-lanyin / mother-voicemail | E39 | 生前另一時刻的普通晚歸留言；同聲線平常口吻，非E34告別；手機透視後製無靈異混響，也不恢復失去的共餐記憶。 | [source.mjs:2959](./source.mjs#L2959) |

### 聲音提示

- **train-e13-red-content（E13；dialogue）**：紅廣播只錄本集催前門內容；同聲線但與白燈編號不同take，遮板位置對應空間。 不反派變聲；母親仿聲限E1／E13，其餘紅廣播仍陸循。 來源：[source.mjs:1339](./source.mjs#L1339)。
- **train-e13-white-content（E13；dialogue）**：白燈提供不完整編號，是独立台詞take，不能重播催門或提前說完E19證據。 紅遮板關後白燈仍響，不只靠立體聲理解。 來源：[source.mjs:1339](./source.mjs#L1339)。
- **train-e13-knock-pattern（E13；foley）**：三短一長同基礎pattern分聲源處理；遮板關後另一側持續，不與編號關鍵音節撞。 來源：[source.mjs:1340](./source.mjs#L1340)。
- **train-e14-exact-repeat（E14；recording）**：各語定稿後只錄一份「爸，這次到家了嗎」，三次重用同take含停頓，非三次獨立TTS。 尚無音檔或audio_ref，runtime需保存實際引用；顯影9歲與未成年影像限制不變。 來源：[source.mjs:1400](./source.mjs#L1400)。
- **train-e19-speaker（E19；dialogue）**：母親報號、唐綺筆聲、程望核對依序，程望才低聲叫媽；不可由唐綺說。 兩證據吻合才放鬆，母聲溫柔不能代替查證或恢復記憶。 來源：[source.mjs:1699](./source.mjs#L1699)。
- **train-e27-name（E27；dialogue）**：原票與本人全名對上，完整報名而無變聲；員工牌落地聲錯開姓名。 來源：[source.mjs:2194](./source.mjs#L2194)。
- **train-e34-final-guide（E34；dialogue）**：驗名接燈→確認握穩→迴路終止，之後不生成幽靈母聲；撤低頻仍保留列車環境。 來源：[source.mjs:2629](./source.mjs#L2629)。
- **train-e39-archive（E39；recording）**：普通晚歸留言與最後共餐不同時，不重用E34告別當留言；手機小喇叭透視無鬼聲。 程望唐綺是現場餐桌，不為錄音新增來回答話。 來源：[source.mjs:2916](./source.mjs#L2916)。

### 待實作的試音段落

- **train-mother-channels／E13**：cheng-wang、tang-qi、wen-lanyin。取定稿兩內容與程望查證段，同聲線不同take，乾聲後才加紅／白空間。 驗收要聽：證據未給前不能靠音色判真。 mono可聽紅遮板關後白敲擊仍響，不能把不同台詞重用成一句。 來源：[source.mjs:1340](./source.mjs#L1340)。
- **train-repeated-child／E14**：lin-xiaoman、tang-qi、xu-hao、lu-an。同一陸安句take三播，再接定稿辨認段；小滿咳在句間，唐綺非全知。 驗收要聽：實際音檔三次連停頓一致，不能只寫提示詞。 女孩和年輕女性可分，輪聲／咳聲不蓋爸爸線索。 來源：[source.mjs:1400](./source.mjs#L1400)。
- **train-proof-before-mom／E19**：cheng-wang、tang-qi、wen-lanyin。先編號／票印核對，才程望叫媽；唐綺只用定稿提醒與記錄。 驗收要聽：盲聽可分報號、提醒、母子確認的說話者。 情緒不早於證據，無恢復記憶或提前真相。 來源：[source.mjs:1699](./source.mjs#L1699)。

先完成zh-TW台灣口音乾聲與多人辨識，再做通訊／環境／音樂處理、mono與手機外放。不同voice_name或文字規則不能代替試聽。逐鏡聲音、造型、道具須和實際演出對上，CC只作獨立可開關軌；ja/ko/en在中文版定案後各自配音、重新配時及母語聽校。本輪沒有修改來源、歷史版本或正式站，不代表新增設計已同步後台。
