# H02 靜圖視覺覆核

審查日期：2026-10-12。審查者：h02_review；末兩張選用圖、未選用木樁 take 3 與 46 項修正候選由 h02_visual_finish 接續獨立覆核（未參與圖片生成）。

目前實際源稿：`4dfe4d73dd458323949542ba5c22cd68a7838cbdc237b36543b07ea18620322e`，109 scenes／134 lines／68 shots。十八景來源卡差異已由 root 套用，獨立 actual readback 證據為 `<VIDEO_WORKDIR>/_audit/final-native-card-delta-2026-10-11T20-46-08-231Z/independent-readback-proof.json`，SHA-256 `913ae5039b8b14167311a46537ec666e4d2dc8e787a8facad63a94f001a1d1ee`，394 checks 全 true；本審查者另讀回 canonical source／claims 完整 SHA 與該證據相符。source 差異與末段的實際 rendered 靜圖顯示各有證據；完整成片播放、音訊及 CC 整合未由本代理驗證。

第一批局部快照：本批審查用源稿 SHA-256 為 `c9269e0e278a150b3de585a5e57ebf66e69fcb72cf74165429623a7614b9a663`，有 **90 個 shot**；manifest 快照 `b2bfe4969656da13de0ade0a8600f63f6a0baeb69af49dcfa398ba819728f042` 中 **25 張 selected 均有實看紀錄及完整 SHA-256**。建議 20 張保留、祖父／新生兒 2 張沿正常人工 accept-best 路徑處理、北灣主道具／軍艦巨大頭像／登岸船圖人物 3 張必修。未選用的木樁 take 3 另有兩個額外動物頭。四張原生字卡加 42 項未選用 prompt 的預防修正候選已完成獨立預檢，詳見後文；沒有把候選預檢當作已套用或成片通過。`return-tree-cro` 在此源稿為 CRO 引文卡，舊版樹圖不再作為 current shot。下列初版 91 張規劃與先前圖片觀察保留作歷史紀錄，不代表目前版本已完成全套覆核。

十八卡修正前的增量覆核綁源稿 `294227a3e6ee357312f0c9faa2b23f9cbc22e72bad7e2e1edb3fa8e188eb62c2`（86 shots），本審查範圍 36 張新 selected 均有逐張原圖紀錄；其中 27 張可留、9 張由協調者另行實看確認必修。加 22 張未變沿用圖片，累計 58 張有 SHA 綁定的目視證據；其中九張現已改來源卡，舊圖觀察與完整 SHA 保留為修正收據。其餘 49 景已在末段對回更新後 manifest 的實際 selected／take／完整 SHA，均與既有目視證據相同；不能把舊 58 張計數說成 current 68 張都已由本代理實看。十八替換卡、原 CRO／CROATOAN 卡、三 PD framed 圖與縮圖共 24 張 actual render 另已逐一實看、綁定正式 frames manifest，無阻塞顯示問題。歷史快照、來源卡靜圖與完整成片各有邊界，詳見末段。

初版三張 pilot 結論：三張靜圖的關鍵道具與旁白可以配合使用，未見石造城堡、塌頂舊屋、錯誤 CROATOAN 文字或求救十字。當時 `return-tree-cro` 增加年輕人物，有身份與連戲歧義；此項現已由改成引文卡處理，不再要求修正舊圖。

## 本次實際查看的範圍

實看下列三個本機 JPG，並讀回 `video.json` 的對應 prompt、旁白與 `return-two-carvings` 字卡；對照 `claims.md` 的 c5、c10、c15 及首輪查核紀錄。沒有修改稿件或媒體，也沒有執行生成。

當次 `video.json` SHA-256：`64c95e39f9021c4dbe2793b758df4ee5c72a4668b787a833de5d52346d032910`。

圖片檔位於 `<VIDEO_WORKDIR>/keyframes/`：

| scene／檔名 | SHA-256 |
| --- | --- |
| `hook-white-happy`／`hook-white-happy-1.jpg` | `e0c3506520ee15e77c77922a9332bf04e20e7e6e0280648bd37f7d6b927792a6` |
| `farewell-deer-melon`／`farewell-deer-melon-3-trim.jpg` | `eb75c298091ef6ec1d11b87530a6cdace8e64c2f57889be2cbf3051cff93b630` |
| `return-tree-cro`／`return-tree-cro-1.jpg` | `10178533fd1ec1451f2d38e13e4fb9bb0bbf31731e33ea09d946dbbf29ebba1f` |

## 逐圖觀察

### hook-white-happy

可辨識的灰白鬍鬚人物戴單頂帽子、挑眉微笑，旁邊是尖頂直立木柵與海面。沒有石牆、城堡垛口、團聚家人或現身的倖存者，足以配合「懷特卻寫自己很高興」，未把他的判斷畫成全員平安的證據。

人物雙手仍在畫面下緣，與 prompt 的 hands below frame 有偏差；這不影響本鏡史實或閱讀，不列為必修。人物造型屬卡通示意，不可把它稱為懷特的考證肖像。

### farewell-deer-melon

可見木屋內部、上方橫梁與封閉的屋頂結構，日光由門口進入；地面有瓜藤與瓜果，鹿嘴叼著葉子。畫面確實有吃植物的動作線索，不是僅把鹿放在瓜旁邊。沒有塌頂或現代整齊田畦，與 1587 年仍立著的舊屋及鹿在其中覓食的記述相容。

景別比 prompt 的 medium close shot 更寬，鹿的頭也沒有明顯壓低，但鹿嘴葉子與地上瓜蔓仍可辨，足以支持此句旁白，不要求動作或風格細節完全逐字符合 prompt。瓜種、鹿種與屋內細節屬示意，不據此提出考古判定。

### return-tree-cro

樹幹與樹皮清楚，中央有大面積光滑留白；沒有生成文字、完整 CROATOAN 或十字。來源規格本就要求圖面空白，由後續 `return-two-carvings` 對照卡呈現「樹幹 CRO／柵欄入口木樁 CROATOAN」，因此這張空白圖本身不是刻字內容的證據。成片仍須確認對照卡正確出現且可讀。

實圖比 close-up 更寬，右側多出一位無鬍鬚、外觀比開場懷特年輕的人物；prompt 只要求樹旁一隻手。這帶來身份與連戲歧義：旁白沒有指定他是誰，不能在剪輯或標示中把他當作懷特、已找到的殖民者或倖存兒童。建議優先以既有圖較近的樹幹取景避開人物身份歧義；本次不改圖，也不要求付費重生成。

## 本次判定的限制與後續檢查

- 本次是三張靜圖的獨立目視核對，沒有觀看運鏡、字幕、配音同步或完整成片，也未實測手機版裁切；不能稱為完整影片 QA 或站主接受。
- 三張的色彩、光線與材質細緻程度並非完全一致，但仍可讀作卡通示意。本次不以風格細節未完全一致為拒收理由。
- 三張 pilot 未涵蓋海上風暴、遠景地理、夜景或考古段落，不能代表其餘 88 張已通過。全 91 張的重複構圖、人物連戲與章節變化，須在 contact sheets 完成後另作整體審查。

## 全套聯絡表覆核方法（已準備，尚未執行完）

全套生成完成後，先以凍結的 `keyframes/manifest.json` 對回該版本 `video.json` 的所有 shot scene（目前 90 個；初版 91 個）：只審 manifest 選用圖，逐張列 scene ID、檔名與 SHA-256；確認沒有缺圖、誤用淘汰 take 或同圖冒充不同景。聯絡表按劇本順序分章，保留 scene ID 標籤。尚在寫入的 manifest 與舊聯絡表不能當作全套完成證據。

每張先在聯絡表看主體與章節脈絡，再對回該景旁白、prompt、claim；有疑點就開原圖確認，避免把縮圖模糊猜成文字、人物或史料。逐張記「可接受／最小必修／成片待查」，問題一定附 scene ID、具體可見內容及最小處理範圍。

| 檢查面向 | 逐張判準 |
| --- | --- |
| 史實與證據層級 | 1587 年仍立著的舊屋不能畫成 1590 年拆屋現場；傳聞、人物推測及現代團隊宣告不能畫成已證實的屠殺、全員平安或解案。AI 示意圖不充作現場史料。 |
| 木柵與刻字位置 | 懷特返航的木柵不是石造城堡。樹幹只對應 CRO，入口去皮木樁才對應 CROATOAN；不合併位置、不生成求救十字。圖面空白可以接受，實際拼字須由正確的對照卡承擔。 |
| 人物與年代 | 額外人物不得使觀眾誤以為找到殖民者或倖存兒童。承接「懷特／他」的人物需避免突然變成現代遊客；卡通外貌不要求考證肖像，但明顯現代服裝或角色身份跳換須處理。現代研究段落可以有現代研究人員。 |
| 地圖與地點 | 無標籤海圖只能作概念示意，不當作考證地圖或精確航線。乞沙比克灣在北、羅阿諾克停留地在南；1587 年往內陸搬的計畫與約五十英里南方的克羅托安是兩件事。不能用任意地圖形狀替代這些方位。 |
| 畫面文字與異物 | 找生成文字、錯字、簽名、浮水印、旗幟符號及無來源的角色。細小疑點需看原圖，不能僅憑 judge 分數定案。空白書頁、樹面與地圖不要求為了有字重畫。 |
| 可讀性與連續觀看 | 以章節總表看近景／遠景、人物／物件／環境與觀看重點是否變化；一張圖至少有可辨的主體。中央安全區本身可接受；景別比 prompt 稍寬、日光顏色或材質細節不同，不單獨列為必修。字幕安全區與實際運鏡仍待成片檢查。 |

修正優先順序是排除史實誤導、無來源角色／文字與明顯身份錯置；優先指出可用既有 take、裁切或後期排除問題的範圍。這份審查不自動授權重生成，也不為風格細節不完全一致要求付費返工。

## 生成中局部覆核：第一章與兩張航程示意

2026-10-12 讀取時 manifest 只有 8 個 selected entries，仍在生成；本段以實看檔案的 SHA-256 綁定，沒有把當時的 manifest 當成全套凍結版本。第一章四張 selected 均已實看：`hook-white-happy` 沿用前述 pilot 觀察，另三張如下。另加看 `farewell-landfall`、`farewell-northern-bay`，不據此宣布第二章完成。

| scene／選用圖 | SHA-256 | 實際觀察與局部判定 |
| --- | --- | --- |
| `hook-blank-post`／`hook-blank-post-1.jpg` | `44d8c1877c21723a0b2c8ccdb66dfdf7c65eaf16b748c98dccc2b626a04b5aeb` | 無文字、十字、人物或石堡。景別更寬，木柱底部像扎根樹幹，也未呈現入口定位；可作開場無字木質線索，不把它當作入口木樁的考證圖。後續 CRO／CROATOAN 位置仍以對照卡釐清。 |
| `hook-island-home`／`hook-island-home-3.jpg` | `c3f3fc5f453980d25bf2aebab83c09103a2174f5b623b84efe5f1a1405077185` | **最小必修：屋門口有清楚的粉紅色怪鳥／角色，source 沒有這個角色。** 海岸木屋本身可讀；不要只為明亮配色重買，但需以既有候選圖或後期排除門口異物，才作正常住處示意。manifest 也標 `needs_review: true`，但本項判定來自實際目視。 |
| `hook-empty-track`／`hook-empty-track-1-trim.jpg` | `92c646e81a8b2fe7feca5b4a85199deed3e3c4f36e957b5c0da6222babff57b6` | **最小必修：眼鏡、背包、短褲與現代登山客造型，承接「那他為什麼還是沒找到人」時容易被當作懷特。** 需排除現代人物或換既有可用圖，避免敘事年代與身份錯置。左手棕色塊與沒有明確岔路是次要偏差，不為它們單獨要求重生成。 |
| `farewell-landfall`／`farewell-landfall-2-trim.jpg` | `395ad8db0da71834094c767348eadb2f1b4b619aded34b5ecc0df0ed7b2cb927` | 可見一艘帆船，沒有生成字或現代機動船。單船示意可配合「船隊」旁白，不等於宣稱當時只有一艘；缺海岸線不列為史實必修。船在畫面中較小，成片可讀性待查，必要時用既有圖取近景。 |
| `farewell-northern-bay`／`farewell-northern-bay-2.jpg` | `fa675cf27b7c9a839f0e381a83eb431fa08b53e429b487a608af71a00c6112ff` | 航海工作台、無標籤地圖與量測工具可辨。地圖形狀不能當作羅阿諾克／乞沙比克的真實海圖；人物戴白水手帽與海軍式服裝，屬現代水手符號，不作十六世紀服飾考證。只在概念示意的用途下接受，真正南北關係由後續 `farewell-destination-compare` 承擔；若成片把本圖演成當年水手的具體現場，需排除人物／地圖身份歧義。 |

目前局部最小必修為 `hook-island-home` 的門口異物、`hook-empty-track` 的現代人物；先前 `return-tree-cro` 的年輕人物仍是成片身份檢查項。已看圖中木柵沒有石造城堡，木質留白沒有生成錯字或十字。未看全套 91 張、章節聯絡表或成片，**尚不給全套或全片通過結論**。

## 修正後的新選用圖：兩項必修已消除

2026-10-12 依 current `keyframes/manifest.json` 的 selected 路徑重新開啟兩張原圖，核對 SHA-256 與 manifest 相符，再對回 source `c9269e0e278a150b3de585a5e57ebf66e69fcb72cf74165429623a7614b9a663` 的 prompt 與旁白。此段取代前述同 scene 的局部必修判定；不是依 judge 分數宣布通過。

| scene／current 選用圖 | 實際 SHA-256（與 manifest 相符） | 獨立目視觀察與判定 |
| --- | --- | --- |
| `hook-island-home`／`hook-island-home-1-trim.jpg` | `d4b2914250225a9a5deea8346fcce1d4fdbb4a7440c5d95918ce103a1a9aa737` | 海岸草頂住處、沙地與植被可辨，沒有門口怪鳥、人物、動物、生成文字或浮水印。**舊版門口異物必修已消除。** 門板關閉，與 prompt 的空門口有偏差；無角色的關門仍能作地名／住處示意，不列新必修。此圖是通用住處示意，不是克羅托安建築的考證圖。 |
| `hook-empty-track`／`hook-empty-track-1-trim.jpg` | `c34225a587da4a9f6b3c44954d4cb66cf4df84b3900d8fa8bc169e63052296eb` | 灰白鬍鬚的年長男子、布帽、斗篷、襯衣、短馬褲與靴子可辨；沒有現代登山背包、牛仔褲、休閒短褲或運動鞋，人物可讀為同一類懷特卡通示意。**舊版現代旅客必修已消除。** 畫成全身站立、雙腳著地而非抬起一靴；這是次要姿勢與景別偏差，不影響「他為何沒找到人」的問題，不列新必修。服飾與臉部仍屬示意，不據此宣稱懷特肖像或具體隨身物件已獲考證。 |

另已讀回 `return-tree-cro` 的 current template 是 `quote`，文字為 `CRO`，對應樹幹三字母；因此舊年輕人物樹圖不再作 current shot，也不再要求裁該舊圖。引文卡的實際渲染、可讀性與後續 CROATOAN 對照仍待成片檢查。

當次兩張新圖局部判定：兩項原圖必修均已消除，沒有新增必修。其他三張修正 pilot 在當次尚未覆核；其後北灣、修屋的觀察見下一段。沒有呼叫 native stage、生成或修改媒體，**不給 current 全套／全片 QA 通過結論**。

## 修正後的北灣與修屋：服裝改善，量測工具待處理

2026-10-12 接續依 current manifest 重新開原圖；兩張的實際 SHA-256 均與 manifest 相符，源稿仍是上述 `c9269e…`。北灣檔名雖與早期相同，圖片內容與 SHA 已更新，不能沿用早期 `fa675cf…` 的結論或雜湊。

| scene／current 選用圖 | 實際 SHA-256 | 獨立目視觀察與判定 |
| --- | --- | --- |
| `farewell-northern-bay`／`farewell-northern-bay-2.jpg` | `e0604faf33891ee65d796d43032c81768a382a807498a9b3a92c08007ef74be0` | 白色現代水手帽／海軍制服已換成布帽、襯衣與古式上衣，**原現代制服問題已消除**。棕色背袋有翻蓋、扣帶外形，沒有清楚的拉鍊、現代品牌或尼龍特徵；雖違反 no backpacks 的字面要求，不單憑這個泛用背袋判為年代錯誤，也不為它要求付費重買。**中央金色工具仍需處理：看不到可辨識的兩腳分規，外形有單一長刃與護手，較像劍。** 這影響導航場景的主體讀法，不是只要配色更像就能解決。無標籤圖只能作概念海圖，不代表實際羅阿諾克／乞沙比克海圖。 |
| `farewell-repair-wall`／`farewell-repair-wall-1.jpg` | `eec01293b1949830223aa9254c74bc250810804c5040ea06fd84c81e9bd0c4e7` | 木板、木樑、支撐木與端面木紋清楚，沒有先前土石塊牆的讀法；人物衣著是布帽、襯衣、寬鬆馬褲與靴子，未見現代牛仔褲、運動鞋或工作帽。**原現代服裝與牆體問題已消除，可作修屋示意。** 人物仍有 chibi 幼態比例，單憑卡通頭身不能認定描畫童工，不列新必修；不要求每個服裝字詞或配色逐字實現。 |

北灣最小處理範圍：用既有可用 take 的分規畫面，或以現有圖裁成不含人物與工具的概念海圖；後者仍由後續對照卡呈現南北目的地。這是具體剪輯建議，不自動要求或授權付費重生成。判定來自實看圖片，沒有把 judge 9.29／10 當成獨立視覺證明。

魚與草蓆圖、current 全套 90 張聯絡表、實際裁切／運鏡、字幕與完整成片仍待覆核。本次沒有修改源稿或媒體、沒有呼叫 native stage，尚不給全套或全片 QA 通過結論。

## 持續生成中的增量覆核：17 個 current selected 已實看

2026-10-12，此批 source 仍為 `c9269e…`、90 個 shot。當次 manifest 可對回 17 個 current selected；8 張已在前文實看，另逐一開啟下列 9 張原圖，實際 SHA-256 均與選用記錄相符。本段的 retain／accept-best 是審查建議，未改 needs_review、未執行人工核准，也不是全套或成片通過。

以下路徑均為 `<VIDEO_WORKDIR>/` 下的具體選用檔案：

| scene／選用路徑 | SHA-256 | 建議與實際觀察 |
| --- | --- | --- |
| `farewell-old-dwelling`／`keyframes/farewell-old-dwelling-2-trim.jpg` | `7c926feeb6813fb71f85b9a704ee0bf2eb87ce386af17b9980ef89ecdf858974` | **RETAIN**：屋頂完整、木牆與空門口可辨，沒有角色、文字、浮水印或現代設備。地面多幾塊石頭是佈景偏差，不是石造住宅，不列必修。 |
| `farewell-manteo`／`keyframes/farewell-manteo-1.jpg` | `4f8fbea9a585de9758b30dec14eaa2ff4546bd6b708c8e115e9117ff2d1fcb07` | **RETAIN**：短髮、裸頭、獸皮樣衣物及說話表情可讀，沒有額外人物或羽冠。抬手指形略僵硬，屬次要繪畫偏差；不把卡通臉／服飾稱為曼提歐肖像考證。 |
| `farewell-trade-hand`／`keyframes/farewell-trade-hand-1.jpg` | `a06ec399b3a044f7b0faae0532698452265dcfe6fede851db342cd3cc594ddbd` | **RETAIN**：草蓆與魚清楚，無角色、包裝、字樣或浮水印。魚較像鮮魚且沒有手，與 prompt 的乾魚／遞物動作不同；旁白不宣稱魚種或製法，仍可作交換物示意，不列史實必修。 |
| `farewell-uneasy-colonist`／`keyframes/farewell-uneasy-colonist-1.jpg` | `2e2341ee62a5de086465e2bce6041add00c8c64778c5d2d28023b7f5f9195a82` | **RETAIN**：有鬍鬚人物的擔憂表情、布帽與古式衣著可辨，沒有現代拉鍊／品牌、傷者或攻擊場面。坐姿全身、泛用皮袋與 close-up 規格有偏差，不影響關係有嫌隙的旁白。 |
| `farewell-thin-food`／`keyframes/farewell-thin-food-1.jpg` | `b6a5586d9f98eaa3d68d0cacb6b9bf3d9f5f8ba0211e37b33bee50df82c3868e` | **RETAIN_WITH_EDIT_NOTE**：木碗與食物可辨，沒有文字、角色或現代設備。碗看來接近盛滿、背景有家具，不呈現 prompt 的少量散粒與 top-down 構圖；可作食物示意，不能把它當作當年實際存糧量的證據。旁白仍須清楚交代食物不穩。 |
| `farewell-grandfather`／`keyframes/farewell-grandfather-1-trim.jpg` | `dc8e70cdeeac46016292116732585ca64767726ae41ff77678c1fd3f845d749c` | **RECOMMEND_HUMAN_ACCEPT_BEST**：年長灰白鬍鬚者俯身看木製搖籃，木屋、布衣與光線可讀，沒有額外人物、生成字、浮水印或現代醫療／嬰兒設備。選用 take 1 的主要差異是半寫實動畫畫風，適合批次結束後人工 accept-best；不為畫風單獨再買。眼鏡等細節屬示意，不能當作懷特本人隨身物件考證。 |
| `farewell-newborn`／`keyframes/farewell-newborn-1.jpg` | `7b92ded709eac3cf2439f37ad09cc33db2bd40db9da952c931eebddbb1cda0a5` | **RECOMMEND_HUMAN_ACCEPT_BEST**：選用 take 1 實際閉眼睡眠，布包裹與木製搖籃可辨，無額外角色、文字、浮水印或現代塑膠／電動設備。主要差異是暖色動畫畫風；適合批次結束後人工 accept-best，不需要為其他 take 的睜眼或色調再買。 |
| `farewell-reluctant-governor`／`keyframes/farewell-reluctant-governor-2.jpg` | `abe3d2b8ffd9d0888f7277a0da6a7296cf341bf48437833b4652a0900fc416f0` | **RETAIN**：灰白鬍鬚人物與空白紙張可辨，沒有假文件文字、現代背包或額外人物。紙張攤開與寬簷帽屬次要偏差；單憑寬簷帽不判成現代帽。仍可作帶著請求離開的示意，不充作原件文件。 |
| `farewell-mark-agreement`／`keyframes/farewell-mark-agreement-1-trim.jpg` | `d17f275d21381589336b0e29e8dada0313c72227e480a499c4318f61168d8352` | **RETAIN**：刀具接近木樁去皮留白，木柵清楚；沒有 CROATOAN、十字、生成文字或石堡。刀刃偏長、刀尖不在正中央是比例／構圖偏差，不列史實必修，也不把此示意當作實際刻字現場。 |

此批沒有新增必修的史實／文字／額外角色／浮水印問題。`farewell-northern-bay` 的 `e0604faf33891ee65d796d43032c81768a382a807498a9b3a92c08007ef74be0` 長刃／護手工具問題仍保留，不能因其他圖片可留而抹掉。祖父與新生兒兩張的三次 take 已耗盡，只建議批次結束後人工接受上表各自的選用 take 1 及所列 SHA，不包含未實看的其他 take；本次沒有核准、重新生成、改稿、改媒體、呼叫 native stage 或寫 STOP。

## 持續生成中的增量覆核：20 個 current selected 已實看

接續開啟下列三張原圖，source 仍為 `c9269e…`，實際 SHA 均與當次 manifest 相符。路徑仍以 `<VIDEO_WORKDIR>/` 為根；此段只增加局部圖片審查，不代表 current 90 shots 已完成。

| scene／選用路徑 | SHA-256 | 建議與實際觀察 |
| --- | --- | --- |
| `farewell-inland-plan`／`keyframes/farewell-inland-plan-1.jpg` | `19e7f5e9c1b21583befaee1d925845945ed28f2dae86574702b3631a44dce5bd` | **RETAIN**：單一人物、林間路徑與布帽、古式衣著可讀，沒有現代背包、運動鞋、字樣或浮水印。chibi 幼態比例不單獨當作兒童史實；配合「搬遷計畫」的旁白作假設示意，不能演成已證實的一次旅程，也不能由任意林路推導五十英里的方向。 |
| `farewell-distress-knife`／`keyframes/farewell-distress-knife-3-trim.jpg` | `4261681a6ac76ffbea00d0fc534c163ffa5f98e805a936919ee733cb534c5dcd` | **RETAIN**：一手、素色袖口與無字木面可辨，沒有十字、錯字、額外人物或浮水印。刀偏長且握法僵硬，仍可讀為刀具；配合條件式危險記號說明可留，不宣稱已刻出求救十字。 |
| `farewell-england-wait`／`keyframes/farewell-england-wait-2.jpg` | `70b360a2268a6e458d96c007fe98f58302ad076430e6bdba3c92e5addd47a7e3` | **RETAIN**：灰白鬍鬚男子、布帽、馬褲、靴子與傳統帆船可辨，無現代制服、品牌、文字或浮水印。桶口開啟、看向觀眾而非水面是次要道具／姿勢差異，旁白不主張該桶的封存狀態，不列必修。 |

本組三張沒有新增必修，北灣主道具仍待處理；祖父／新生兒仍僅對前表所列選用 take 提出人工接受建議。實際裁切、字幕、片段動態與完整成片未在此處檢查。

## 持續生成中的增量覆核：22 個 current selected 已實看

接續兩張原圖的實際 SHA-256 與 current manifest 相符，source 仍為 `c9269e…`。本次發現一項即使 judge 通過仍須處理的額外角色問題。

| scene／選用路徑 | SHA-256 | 建議與實際觀察 |
| --- | --- | --- |
| `farewell-armada`／`keyframes/farewell-armada-1.jpg` | `673f9f9e823f5d5372e53b2b1375e6ab013cede81cee5fdc823f9cbad893cb49` | **FIX_REQUIRED**：船中央長出一顆巨大男性頭像，比例遠大於正常甲板人物，會讀成船型角色或怪船；source 只描述傳統武裝帆船，沒有此角色。manifest 的 `needs_review: false` 不抵銷這個實看問題。最小處理是改用既有可用 take，或以既有圖裁切／後期完整排除頭像而仍保有可讀帆船；純港口角度與配色不必返工。 |
| `farewell-three-years-question`／`keyframes/farewell-three-years-question-2.jpg` | `4a7b691d0823f926c85031f27d5be7e924a63a6721b93a3a3f34d83e6a4f42e1` | **RETAIN**：年長灰白鬍鬚者扶木欄、古式布衣與帆船索具可辨，沒有額外人物、文字、浮水印或現代裝備。手的位置較右、畫風與開場略異是次要偏差；能承接懷特回航的不確定感，不宣稱本圖為實際肖像。 |

目前實看 22 張，待處理兩項為北灣的劍狀主道具與軍艦的巨大人頭。未改 source／媒體／核准，也未呼叫 native stage；其餘尚未生成或未實看的 shot、完整成片都仍未給通過結論。

## 持續生成中的增量覆核：23 個 current selected 已實看

| scene／選用路徑 | SHA-256 | 建議與實際觀察 |
| --- | --- | --- |
| `return-landing-date`／`keyframes/return-landing-date-1-trim.jpg` | `f51ab24bfb76104ca1ac2db4a6d47b23506e07eb8628a6e631f824b555e14207` | **FIX_REQUIRED：人物身分／年代讀法。** 小艇中央有兩名 source 未描述的人物；一人紅色短筒帽，另一人頂髻與綠色交領樣衣著，整體較像泛東亞古裝人物，無法讀成同一位年長灰鬍鬚懷特或十六世紀英國船員。旁白正說懷特回到羅阿諾克，不能直接用這兩名角色代替他的身分。這不是僅由 chibi 幼態比例判成孩童，也不宣稱帽型／髮型可考證特定民族。最小處理可排除人物、保留木艇靠岸示意，或用既有可用 take；船形和巨大太陽的風格差異不單獨要求返工。沒有文字或浮水印。 |

本圖實際 SHA 與當次 manifest 相符，source 仍為 `c9269e…`；judge 無問題記錄仍不抵銷上述人物讀法。當前三項必修為北灣主道具、軍艦巨大頭像與上岸船圖人物；未給全套或全片通過結論。

## 批次關閉後補完：25 個 selected 覆核紀錄齊全

接續審查者 h02_visual_finish 依上述源稿與 manifest 快照，逐一開啟最後兩張 selected 原圖及未選用的木樁 take 3。下列 SHA-256 均由實檔重算；前兩張與 manifest 相符，木樁 take 3 在該 manifest **沒有 selected 路徑**。累計覆蓋是前文 23 張加本段 2 張選用圖；本段不把未選用候選混入 25 張的計數。

| scene／實看路徑 | SHA-256 | 建議與實際觀察 |
| --- | --- | --- |
| `return-trumpet-dark`／`keyframes/return-trumpet-dark-1-trim.jpg` | `37c75824b49b6f934a78de87c8a5997ae34b6904ffdfdb76d1b57093d79fdc30` | **RETAIN**：單一船員在木艇上舉起銅色號角，深色岸線與夜色可辨，沒有額外人物、生成字、浮水印、白色現代水手帽或海軍制服。柔軟布帽、布衣與泛用肩帶可以作古式船員卡通示意；chibi 幼態比例不單獨判成兒童史實。號角尚未貼到嘴邊，屬舉號角的示意姿勢，不把此靜圖稱為實際吹奏動作已驗證，也不因此要求重買。 |
| `return-walk-ashore`／`keyframes/return-walk-ashore-1-trim.jpg` | `3a97d4b0cbcac9a39034b800177417b64c0bd207ae34d1ab462428e6b1441692` | **RETAIN_WITH_EDIT_NOTE**：襪、皮靴、沙地、海岸與晨光清楚，沒有臉、現代運動鞋、額外人物、文字或浮水印。畫面露出膝上衣擺、兩腳站定，左腿前另有細長棕色物／帶狀細節，與只看單腿踏步的 prompt 不完全一致；其確切道具身分不作猜測。仍可作登岸示意，不影響當年上岸與時間先後的旁白；不為景別／姿勢偏差付費重買。成片可讀性及運鏡是否凸顯多餘細節仍待檢查。 |
| `return-post-croatoan`／**未選用** `keyframes/return-post-croatoan-3.jpg` | `7302d50bcdda5921c5e925f3e4ef7cd6be5b4cea2c2412be5a1c488ba528fd4e` | **DO_NOT_SELECT／FIX_REQUIRED**：木柱上清楚附著兩個無身體的貓／兔樣角色頭，source 沒有這些角色，會干擾木樁刻字線索。木柵與留白本身可讀，未見生成文字或浮水印；不因無字而要求重畫。支持改用來源綁定的 CROATOAN 字卡，保留「柵欄入口木樁」定位，沒有再買圖片的必要。 |

此快照 25 個 selected 的實際檔案 SHA-256 全部與 manifest 相符，且逐圖紀錄均含對應完整 SHA；沒有以舊 SHA 覆核同名新內容。這只完成該批靜圖的累計目視紀錄，尚非全 90 shots／運鏡／聲畫／完整成片／站主接受的通過證據。

## 四張字卡與未選用物件／手部 prompt：46 項候選獨立預檢

審查候選為 `<VIDEO_WORKDIR>/_audit/object-prevention-final-candidate.json`，實檔 SHA-256 `9482a99f35f0a9b405a0f627daac2354d40d3fbbe6ad5567a3c8cef82e6d3294`。此紀錄是 **候選預檢 PASS**：未由審查者套用 source、改核准、呼叫生成或 native stage。

- 全部 46 個 `before` 與上述 `c9269e…` 源稿中的 scene 精確一致，46 個 ID 不重複；全部旁白、line ID、emotion、claims 與章節欄位不變。源稿 109 scenes／134 lines 的內容完整保留，不據此宣稱實際渲染或對時檢查已完成。
- 4 張來源字卡對應 `farewell-northern-bay`、`farewell-armada`、`return-landing-date`、`return-post-croatoan`；除了 template／data，其他欄位精確不變。北方預定地名、1588 年防守背景、1590 年8月18日與入口木樁 CROATOAN 均承接原 claims，不新增已找到殖民者或解案的說法。軍艦卡保留「事件名稱，非逐字引述」以說明 quote 版型的引號；日期卡標「日期整理」。CROATOAN 不充作新取得的木樁照片；樹幹 CRO 與入口木樁 CROATOAN 的分別仍須在成片可讀。
- 36 張物件／環境景和 6 張指定手部景均尚未有 selected 檔案。逐讀所有原 prompt，分類合理：物件、海岸、船具、考古器物、空白檔案與假設住宅沒有必要的人物／動物被排除；六張手部景仍保留指定的手及器物。原本的示意地圖、假設重建、空白表面、現代研究／歷史交易限制均保留。
- 36 張只附加 `Object-only illustration: no people, human faces, character mascots, personified objects or extra animals.`；6 張只附加 `Only the specified hand and object; no face, full body or other characters.`。移除這些精確尾句後，整個 scene 與 `before` 相同；主體、camera、光源、旁白及 claims 沒有其他改動。

預防尾句與四張字卡能針對已觀察到的額外角色、主道具與年代讀法問題，沒有可見的來源事實衝突或必須阻止套用的顯示問題。這是有邊界的修正建議；尾句尚未經後續生成驗證，字卡的實際引號、字體、來源行、停留時間與前後銜接仍待渲染及成片覆核。

## 套用修正後：86 shots 的增量原圖覆核

本節開始改綁源稿 `294227a3e6ee357312f0c9faa2b23f9cbc22e72bad7e2e1edb3fa8e188eb62c2`，共 109 scenes／134 lines／86 shots。上節 46 項候選已由協調者套用；本節只記審查者 h02_visual_finish 實開的新選用圖，審查範圍為 `return-dismantled-houses` 至 `h02-history-artifact-question`。原 25 張 selected 中有 3 張必修改為字卡，22 張未變圖片沿用既有 SHA 所綁的目視紀錄；舊 25 張快照不混作本版 25 張覆蓋。

### 新版第 1 組：1 張新選用圖

本次讀取的 manifest SHA-256 為 `13732e8ef6f453dc0c189b8de25bc7e37171a1742955a29d4e059431c4090fa7`，23 張 selected（22 張沿用、1 張新選用），仍在生成。下列原圖已實開，SHA 與該快照相符；未完成鏡頭不計入通過。

| scene／選用路徑 | SHA-256 | 建議與實際觀察 |
| --- | --- | --- |
| `return-dismantled-houses`／`keyframes/return-dismantled-houses-1.jpg` | `53e88ff3fdf7737ac7ae2eefcfc88be9379063ab588aa2b309cc664f34baed68` | **RETAIN_WITH_EDIT_NOTE**：矩形空地／坑狀地面與拆下木板清楚，沒有完整留存房屋、人物、文字或浮水印，能作拆屋後遺留地面的示意，不當作當年基址的考古實證。前景左右各有小型紅黑瓢蟲樣裝飾，未完全符合 no extra animals；它們不承接殖民者身分，也未畫成找到倖存者。保留這項可見偏差，成片檢查不讓它們搶走拆屋重點；不單為前景小裝飾或坑的景別付費重買。 |

本組新增 1 張目視紀錄，新版累計有 23 張 selected 的已看證據；尚未給其餘 63 shots、字卡渲染、運鏡或完整成片通過結論。沒有更改源稿、媒體、manifest、judge、核准、native stage 或 STOP。

### 新版第 2 組：5 張新選用圖，沿溪船員有年代必修

本組源稿仍為 `294227a3e6ee357312f0c9faa2b23f9cbc22e72bad7e2e1edb3fa8e188eb62c2`。接續逐張開原圖，重算下列實檔 SHA 與 selected 相符；讀取時 manifest 已有 28 張 selected，快照 SHA `cf3b365f4c0c1111b7d3d4f1cf4bc22c7d09c1dcfa0a9d5d7df2c2d69542d0f2`。判斷來自原圖目視，沒有只靠 judge 的 passed 欄位。

| scene／選用路徑 | SHA-256 | 建議與實際觀察 |
| --- | --- | --- |
| `return-defensive-palisade`／`keyframes/return-defensive-palisade-3.jpg` | `53f487f4f6ee8185d475a603b692b6483f6320b971b7364e5a2fcb330ac4a1e9` | **RETAIN**：高大木質立柱圍牆、樹木與內側道路可辨，沒有石堡、人物、擬人頭像、文字或浮水印。中央是內縮轉角而非向觀眾凸出的角；仍能交代樹幹圍起的防守住處，不為轉角方向或柱頂形狀要求重買。 |
| `return-heavy-metal`／`keyframes/return-heavy-metal-2.jpg` | `3bfdcb38688095a8e70ae21d022f968c050b340a6de102be72061c07dc67044e` | **RETAIN_WITH_EDIT_NOTE**：灰色長方重物被草遮住，沒有人物、額外角色、文字或浮水印。表面裂紋與粗糙邊緣使材質較像石條，並非明確金屬光澤；保留這個材質讀法偏差，不把畫面當作鐵條／鉛的材質證據。以旁白說明遺留重物的示意可留，不單憑光澤或 extreme close-up 未落實要求重買。 |
| `return-creek-search`／`keyframes/return-creek-search-1.jpg` | `db2d02682bd6f31d8e98f012f28b7733b1ec294123a3b9ad34d99bebe5d3e068` | **FIX_REQUIRED：帽型／軍裝的年代讀法。** 岸邊船員戴清楚的雙角帽，白色上緣、金色叉形徽記，藍色外衣有金邊，整體讀成後世軍裝或海盜角色；與本景 1590 年英國船員、素色布帽及 no naval uniform／pirate costume 的限制不合。這不是由 chibi 幼態比例判成兒童，也不以未遮眼的姿勢列必修。沒有額外人物、生成字或浮水印；建議批次後用既有可用 take 或來源字卡消除年代讀法，不在審查中開新付費請求。 |
| `return-empty-mooring`／`keyframes/return-empty-mooring-1.jpg` | `52d69706dd7d10a9ca5d4d440f75d563760290fede272b5201537a3c52209e1b` | **RETAIN_WITH_EDIT_NOTE**：無船的水面、單一木柱與岸邊蘆葦可辨，木面是樹皮樣深色紋理，沒有明確角色臉、刻字、浮水印或找到船艇的畫面。柱在水中央而非岸邊，屬停泊示意的位置偏差，不能用來考證實際碼頭；旁白沒有把空柱當作搬走船艇者的證據，不列史實必修。 |
| `return-opened-chest`／`keyframes/return-opened-chest-1.jpg` | `b58eed6ffbcb7a87906e147b7df1c503e6ffb8a46ee9745b15cba4b2b48fb927` | **RETAIN_WITH_EDIT_NOTE**：地坑中有打開的木箱、古式金屬環與把手，沒有角色、文字、現代設備或浮水印。箱蓋完整、仍附在箱體，與 broken lid 有偏差；可作挖開箱子的代表性示意，不把單箱說成當年只有一只，也不把完整箱蓋當作損毀細節證據。後續受損物件鏡與旁白仍須釐清損毀不等於聚落遭襲，不為箱蓋姿態要求重買。 |

本組 4 張可留、1 張年代必修。新版新增圖片累計 6 張實看，加 22 張未變沿用圖片，共 28 張有目視證據；`return-creek-search` 的帽型／軍裝必修保留，不被 judge 通過抵銷。仍未給尚未生成／未實看鏡頭、字卡或完整成片通過結論，未改源稿或媒體。

### 新版第 3 組：5 張新選用圖，留言判斷場景有石堡必修

本組仍綁上述 `294227a3…` 源稿，逐張開啟下列原圖。讀取時 manifest 已有 33 張 selected，快照 SHA `193bed03f60c6ed6b981aa457a1ef7bbf60f3ba7a5457da442e2987d8e7e605e`；每張實檔 SHA 與該 selected 記錄一致。

| scene／選用路徑 | SHA-256 | 建議與實際觀察 |
| --- | --- | --- |
| `return-ruined-frame`／`keyframes/return-ruined-frame-1.jpg` | `a195e98a43d46991a5cbb6ee496c2ddb287acc611d0ad3d042024eae36014824` | **RETAIN**：開箱內的木框頂邊及角落有裂損，中央留白，沒有生成畫像、文字、額外角色或浮水印。裂損點較上方、不是正中央，屬構圖偏差；仍能配合受損物件的示意，不把木框損壞本身當作聚落遭襲的證據。 |
| `return-white-inference`／`keyframes/return-white-inference-1-trim.jpg` | `f2d78d8444273e7b4a6738f47ca3743a4580e2f38e9708847c8d6fea3a5feecd` | **RETAIN**：灰白鬍鬚年長男子、素色布帽、古式布衣與土坑內木箱可辨，沒有現代背包、制服、額外人物、文字或浮水印。眼鏡、腰旁小物及全身景別屬示意，不把它們當作懷特的考證肖像或隨身物件，也不為臉部 close-up 未落實要求重買。旁白已把敵人說法標成他的推測，本圖沒有新增攻擊現場。 |
| `return-hope-has-limit`／`keyframes/return-hope-has-limit-1.jpg` | `be526f51721f1e00e6868e579ca1281bd5f09931d16ee80b9d5ab16efccb52b3` | **FIX_REQUIRED：木質圍柵被畫成石堡。** 門框、拱門兩側厚柱與大面積牆面有清楚的分塊石造讀法，雖上緣另有木柵，仍不是本景應有的木質圍柵。這使返島現場的主建物材料誤導，不能只把 judge 的杯／袋差異當作本圖唯一問題。人物年長鬍鬚可讀，拿杯而非布袋、未朝向門口是次要偏差；沒有文字或浮水印。建議在批次後以來源字卡或既有可用素材排除石堡，不在審查中重買。 |
| `return-one-witness`／`keyframes/return-one-witness-1.jpg` | `d766f5b99017f0ea981440e06cf11f2cf91be84678be5b45dbcec51b05d91f1c` | **RETAIN**：灰白鬍鬚年長寫作者、羽毛筆、木桌與空白紙頁清楚，沒有假史料文字、現代文具、額外人物或浮水印。正面景別取代過肩鏡，眼睛／表情與前圖不同是卡通示意偏差，仍能交代留下記述的目擊者，不為此重買；不把空白頁稱為懷特原件。 |
| `return-next-step`／`keyframes/return-next-step-1-trim.jpg` | `b93ea7ce15207209660b8475afcf34f22e10552c6157036471584ebabaf8878d` | **RETAIN_WITH_EDIT_NOTE**：沿岸小船、淺灘與空水面可辨，沒有角色、文字或浮水印。船上是簡化矩形欄／棚框與單色紅旗，沒有可見引擎、螺旋槳或國家徽記；帆並未出現，不能據此主張帆船構造或具體航行能力已驗證。可作還須渡海的小舟示意，海岸輪廓不當作精確航線，不為缺帆或遠景構圖單獨重買。 |

本組 4 張可留、1 張石堡必修。新版新增圖片累計 11 張實看，連同 22 張未變沿用圖片，33 張有已看證據；本審查範圍當前兩項必修為 `return-creek-search` 船員年代讀法及 `return-hope-has-limit` 石造城門。另記協調者已確認沿溪搜尋在本批結束後改成來源字卡：kicker「沿溪搜索」、quote「船艇與小炮」、source「懷特1590年返航記述｜NPS 1590」；保留 c14 與原旁白全文，由後續 `return-empty-mooring` 繼續交代沒有找到。這是待套用決策，不表示已改 source、已渲染或已核准。

### 新版第 4 組：5 張新選用圖，近代住處與額外吉祥物必修

本組仍綁 `294227a3…`，原圖逐一實看；快照 manifest SHA `32383495a88fad4e4519368c2383bf33bfa67f2ee38f136ab241446f3fbd201b` 有 38 張 selected。下列完整 SHA 均對回該選用內容，不把概念海岸或圖中羅盤當作經考證的地圖資料。

| scene／選用路徑 | SHA-256 | 建議與實際觀察 |
| --- | --- | --- |
| `route-croatoan-place`／`keyframes/route-croatoan-place-1-trim.jpg` | `e9866399f71c08104f17986234c56530b9566c3f815e219fe5658d90b9959e35` | **FIX_REQUIRED：住處年代／類型讀法。** 島上小屋有規整白色牆面、方格玻璃窗、直板門與橘色屋面，讀成近代海邊小屋，並非此歷史段的原住民蘆葦頂住處。這是主體的時代／類型偏差，不能只把它當作配色差異。沒有角色、文字、異物或浮水印。協調者另行實看確認後，選擇批次後改來源字卡，以地名與族名本身交代，不再買小屋圖片。 |
| `route-hatteras-coast`／`keyframes/route-hatteras-coast-2.jpg` | `852c23d346b34035e336d3824bddf5275aaea5a364eaeb0afd709b98f500267e` | **RETAIN_WITH_EDIT_NOTE**：沙岸、兩側水色與俯視海岸示意清楚，沒有角色、文字、浮水印或精確地圖標記。畫成尖端沙地／半島樣輪廓而非完整長條屏障島，不當作哈特拉斯島真實形狀、五十英里距離、南北方向或具體航線的考證；旁白以「大致」交代地點，方位仍由既有對照卡承擔，不為未標籤輪廓重買。 |
| `route-diverging-directions`／`keyframes/route-diverging-directions-1.jpg` | `887b249220373b8f57e14463aaa75afeba80d042bb0ed2676a72097d48db8986` | **RETAIN_WITH_EDIT_NOTE**：一名泛用旅行者、銅色圓盤羅盤與岔枝可辨，沒有額外人物、生成字、浮水印或已抵達殖民者的畫面。羅盤面有放射線紋，非完全留白；不把它當作實測指向或航線。人物不是旁白中的特定懷特肖像，chibi 幼態不單獨當作孩童史實；布衣、棕色肩帶與鞋沒有明確現代品牌／拉鍊／運動鞋特徵，不列年代必修。 |
| `route-governor-ready`／`keyframes/route-governor-ready-1.jpg` | `6dcf487c8f6b266f469cb63ff5238f38f3ffa653e5321a537bb377672858957b` | **RETAIN_WITH_EDIT_NOTE**：灰白鬍鬚年長男子、布帽、布衣、帆船甲板與帶扣旅行包清楚，沒有額外人物、文字、浮水印或現代制服。除了身前包，背後另有矩形行囊／捲物，且人在甲板而非梯上；保留這個多包與景別偏差。包沒有可見尼龍、現代品牌或拉鍊，不單憑背負方式判成現代登山裝備，也不把這些隨身物件當作懷特的考證資料。 |
| `route-broken-cable`／`keyframes/route-broken-cable-2.jpg` | `2cd9c665896ec59156c0889d8798988a0812dc233e2ffb11b81d8c3ed38d0e3c` | **FIX_REQUIRED：額外吉祥物。** 船首欄後有清楚的黃頭、藍色護目鏡、橘色身體角色，讀成吉祥物／機器人樣人物，source 此物件鏡明確沒有角色。這不是纜繩或木紋可疑點，而是可辨的額外主體；不能以 judge 通過抵銷。纜繩的鬆纖維可讀，並非中央特寫；建議批次後來源字卡或既有素材排除角色，沒有文字／浮水印，不在審查中開付費請求。 |

本組 3 張可留、2 張必修；新版新選用圖累計 16 張實看，加原 22 張未變圖片，共 38 張有目視紀錄。本審查範圍累計四項必修為沿溪船員、石造城門、近代小屋及船首吉祥物，均待批次後集中處理。

另記協調者確認的兩張待套用字卡：`return-hope-has-limit` 用 kicker「讀懂留言之後」、quote「有去處，未定下落」、source「本集判讀｜懷特1590年返航記述」，避免把本集的判讀偽裝成懷特逐字引文；`route-croatoan-place` 用 kicker「族名，也是地名」、quote「克羅托安」、source「懷特1590年返航記述｜NPS 1590」。兩者均保留原旁白／claims／emotion；本段不代表修正已套用或渲染已通過。

### 新版第 5 組：5 張新選用圖，船長帽與擬人船具必修

本組仍綁 `294227a3…`，快照 manifest SHA `ad7c7f469958fe23a0b5274a9929ec250e9b8724458bee0a9228fae91508f463` 已有 43 張 selected。下列五張均開啟實際原圖，完整 SHA 對回 selected；最後兩張的額外角色分別按具體可見程度記錄，沒有因負面提示詞未逐字實現就一律要求重買。

| scene／選用路徑 | SHA-256 | 建議與實際觀察 |
| --- | --- | --- |
| `route-last-anchor`／`keyframes/route-last-anchor-1.jpg` | `6c13c15e3d8bfb9f3d8bfba0e264bc9a6072856cff40037ad555b0b4b96a7375` | **RETAIN**：單一鐵色錨、粗麻纜、木質帆船甲板與海面清楚，沒有人物、擬人臉、文字或浮水印。錨型屬泛用卡通道具，不宣稱具體鑄造構造已考證；單錨可承接「最後只剩一套」，不因畫風較細緻或照明不同要求重買。 |
| `route-water-left-ashore`／`keyframes/route-water-left-ashore-1-trim.jpg` | `0226d5e6b82563f689ffb64586261361a6512a872d6c3d9ff8b38ea6c6137d53` | **RETAIN**：封閉木桶橫躺沙岸，浪邊靠近，沒有角色、擬人臉、字樣、浮水印或現代塑膠設備。可作岸上留下淡水桶的示意，不用桶數或水線主張具體實物數量與當時水位；較簡單平面風格不列必修。 |
| `route-captain-decision`／`keyframes/route-captain-decision-1.jpg` | `62d5b1a31cbcd97ed0995f8a8c9a06dfa943387397db8a9e27d247d417d6df3a` | **FIX_REQUIRED：後世船長／海盜帽型。** 人物戴巨大、硬挺、金邊的 cocked／雙角帽樣造型，搭配外衣與領巾，讀成後世船長或海盜；與 1590 年素色布帽及 no pirate costume 限制不合。這與前述沿溪船員採相同年代判準，並非泛用寬簷軟帽的細微差異。緊張表情與木欄可讀，沒有額外人物、文字或浮水印；建議批次後最小來源字卡修正，不在此重買。 |
| `route-southward-plan`／`keyframes/route-southward-plan-1-trim.jpg` | `629b66ad316236b64f402d3db02df5b14d36f2eafa549295066c0dbfd1226f73` | **RETAIN_WITH_EDIT_NOTE**：帆船、海面與近岸島景本身可讀，沒有文字或浮水印；右後甲板欄旁另有紅帽、圓黃臉的小頭像，未完全符合物件鏡的 no characters。它很小，可讀成泛用船員，沒有巨大頭像、明確機器人結構或現代物件；協調者另行實看後確認保留，與巨型擬人船具採不同處理。保留這個匿名船員偏差，不把圖稱為無人甲板、精確航向或特定船員肖像，不為此付費返工。 |
| `route-storm-sail`／`keyframes/route-storm-sail-2.jpg` | `64c081c02b67d007af8cd71f544a575b0ebd93e328cebd67bee91ab0ceb8aa65` | **FIX_REQUIRED：船具擬人。** 左側兩個甲板柱／機械構件有完整笑臉、腮紅與嘴，形成明確擬人道具，與此物件景 no faces／personified objects 不合，不能解釋成泛用小船員或木紋。帆、索具、風浪本身清楚，沒有生成字或浮水印。最小處理可取既有畫面的右側帆與海面，完整排除兩張臉；或批次後改來源字卡。實際裁切尚未執行／驗證，不等同已修好，不為此開新購買。 |

本組 3 張可留、2 張明確必修。新版新選用圖累計 21 張實看，加 22 張未變沿用圖片，共 43 張有目視紀錄；本範圍明確必修累計 6 項。協調者另行原圖覆核確認船首吉祥物、船長帽型與擬人船具須在批次後改來源字卡，`route-southward-plan` 的小船員保留，無第 7 項必修。所有判定仍保留來源、原旁白與 claims，未修改 source、媒體、核准或 STOP。

### 新版第 6 組：4 張新選用圖，熊臉抱枕與祖先故事住處必修

仍綁源稿 `294227a3…`。本組逐一實開原圖並核對完整 SHA；快照 manifest `827b0467187279c8ce553b6150e2fa5083f6f93b346bf2116bed99a62149d10e` 有 47 張 selected。

| scene／選用路徑 | SHA-256 | 建議與實際觀察 |
| --- | --- | --- |
| `route-england-return`／`keyframes/route-england-return-2.jpg` | `04311a1fbeae5326dcc840d7e078055e0e85b25da0b2215d42be4bb6419cecdd` | **RETAIN_WITH_EDIT_NOTE**：灰白鬍鬚年長男子、軟帽、布衣、帆船與英格蘭港口示意可辨，沒有額外人物、文字或浮水印。背上多一個有帶扣／隔袋的棕色行囊，與單一布製旅行包有偏差；未見現代品牌、尼龍或拉鍊，不單憑背負方式判成現代裝備，不把包形當作懷特的考證隨身物。石鋪港口在英格蘭段可以作一般背景，與返島木柵被畫成石堡的問題不同；本圖沒有演成到達克羅托安。 |
| `route-third-birthday`／`keyframes/route-third-birthday-1-trim.jpg` | `78c66ae201e672f6af7f1cfdf8afd0c2a0f0defe5672960ba2b671b73fc8ae60` | **FIX_REQUIRED：熊臉抱枕／近代嬰兒房讀法。** 空木搖籃旁有占主要區域的熊臉造型抱枕／玩偶，兩耳、眼鼻口完整，與此物件鏡僅有搖籃／亞麻布及 no mascots 不合，也使歷史住處讀成近代嬰兒房。不是微小木紋或路旁裝飾。沒有倖存兒童或生成字，搖籃本身可讀；協調者另行原圖確認後決定第 7 項必修改生日事件摘要卡，保留 c2／c7 與原旁白，零新購。 |
| `route-later-clues-question`／`keyframes/route-later-clues-question-1.jpg` | `878ebadee60341552b7ec973ed0b35e710d48ff3b8437836d5a3819939c77ad9` | **RETAIN_WITH_EDIT_NOTE**：沙地路徑、兩側植物與遠端日光清楚，沒有明確人物、生成字或浮水印。路旁兩個小棕色莢／塊狀物有暗斑，可能被讀成小裝飾，但沒有足以確認完整角色身分的臉／身體構造；不把它們當作殖民者留下的實物線索。植物種類、莢狀小物與路幅偏差只留觀察註，不擴成付費返工或新必修。 |
| `h02-history-late-story`／`keyframes/h02-history-late-story-1-trim.jpg` | `05ad524bfb9e38d974914198cd439a54d0619e1e6c65d9f38f634da2d0fb3f9f` | **FIX_REQUIRED：沿海住處的建物類型。** 遠處建物有分塊磚／石牆、中央拱門、兩側紅色拱窗及尖亭塔式屋頂，讀成異域塔亭／門樓，並非此段 source 的沿海蘆葦頂住處。這與前述小屋採同一主體類型判準，不單為道路較寬較直列必修，也不依此指定某一民族建築。海岸／道路沒有角色、文字或浮水印；建議批次後摘要卡承接一百多年後的祖先故事，不再買住處圖。此項已送協調者另行原圖確認。 |

本組 2 張可留、2 張必修觀察。新版新圖累計 25 張實看，加原 22 張未變圖片，共 47 張有目視證據；八項必修均由協調者另行原圖確認，祖先故事塔亭建物改晚期祖先傳聞摘要卡，原候選保留、零新購。未改源稿、媒體、judge、核准或 STOP，尚未給完整成片通過結論。

### 新版第 7 組：5 張記述／傳聞圖可留

本組仍綁 `294227a3…`，snapshot manifest SHA `95308f5a75c2fca3118bd8ab54d6e273230aba04ea76458e158d421b5bcb64a8` 有 52 張 selected。依每景原有世紀審查衣著：勞森段為十八世紀初，史崔奇傳聞段為十七世紀初；不套用 1590 年船員的帽型限制。逐張原圖 SHA 與 selected 相符。

| scene／選用路徑 | SHA-256 | 建議與實際觀察 |
| --- | --- | --- |
| `h02-history-lawson-book`／`keyframes/h02-history-lawson-book-2-trim.jpg` | `5b3afc41cc6cbf01c7b16fe402cf0a139c352bb529df5e96841b2b9d993d4675` | **RETAIN_WITH_EDIT_NOTE**：單一人物、十八世紀式外衣／背心／白領巾、木桌與空白書頁清楚，沒有現代設備、假書名、文字或浮水印。書是打開而非關閉，人物坐著而非放下書，屬姿勢／開合偏差；仍可交代後來出版的記述，不把空白書當作勞森原本或封面考證。chibi 幼態比例不單獨判成孩童。 |
| `h02-history-ancestor-memory`／`keyframes/h02-history-ancestor-memory-2-trim.jpg` | `6e0b94e8c1623a023ebcd4d795d8be46a0ebfbaed7ab1eb0a6cc251dfd966ce6` | **RETAIN_WITH_EDIT_NOTE**：灰髮長者在木質住處門旁手掌向海，沒有額外人物、生成字、浮水印或現代設備；帽上是單羽毛，沒有 Plains 式全羽冠。布袍／軟帽是泛用歷史人物示意，不把它們當作哈特拉斯民族服裝考證，也不用膚色或卡通臉部猜定族群肖像。坐姿、全身與位置偏差不影響轉述祖先故事，不要求人物 close-up 逐字實現。 |
| `h02-history-record-not-witness`／`keyframes/h02-history-record-not-witness-1.jpg` | `3246a01e90ecf482d9824c3f2d57c9d2693d8fa9959a886c8c09e956203077d8` | **RETAIN_WITH_EDIT_NOTE**：單一寫作者、羽毛筆、空白紙、外衣／背心／領巾與羽飾三角帽可辨，沒有假記述文字、額外人物或浮水印。按十八世紀初的情境，這頂帽不是 1590 年船員的同一年代問題；背後泛用行囊與正面鏡頭屬偏差，沒有品牌／尼龍／拉鍊特徵，不單憑它們要求重買。旁白保留「不是1587年現場紀錄」的證據層級，不把此示意當原件。 |
| `h02-history-killing-rumour`／`keyframes/h02-history-killing-rumour-1-trim.jpg` | `5522808983dfdffc5d30e6a30e6c636d6c28d6fe58deb74fe3fb802bb9eec80d` | **RETAIN**：單一文書人物翻開空白紙封包，布衣與木桌可辨，沒有額外角色、假文字、現代設備或浮水印。衣著是泛用早期歷史文書人物示意，不作特定服飾考證；圖中沒有攻擊、被害者或屠殺現場，能承接「另一個故事」而未把傳聞畫成已證實命運。 |
| `h02-history-rumour-distance`／`keyframes/h02-history-rumour-distance-1-trim.jpg` | `1ddda0f4ce6ae3c84e8d4022fd74a513f7ca46b3fe84946e31b076079edfdf81` | **RETAIN_WITH_EDIT_NOTE**：有鬍鬚人物、疑惑眼神與素色書本清楚，沒有假文字、額外角色、現代設備或浮水印。書打開而非關閉，衣著與髮型屬泛用文書人物示意，不當作史崔奇考證肖像。畫面沒有親見屠殺或受害者，旁白仍明確說是轉述，不以書的開合偏差要求重買。 |

本組 5 張可留，沒有新增必修。新版新增圖片累計 30 張實看，加 22 張未變沿用圖片，共 52 張有目視證據；八項必修與其待批次後字卡處理仍保留。實際書卡字體、聲畫、CC、運鏡和完整成片均未在本次驗證。

### 新版第 8 組：6 張研究／器物示意，現代電線桿必修

本組仍綁源稿 `294227a3e6ee357312f0c9faa2b23f9cbc22e72bad7e2e1edb3fa8e188eb62c2`。六張均逐一實開原圖；最後兩張讀取時 manifest SHA `802d3e14737aec4555e1ce231559bacd6a7cd51f9d33f5d536f3d2d645e081a6` 有 58 張 selected。以下完整 SHA 對回實檔及該 selected；判定不以 judge 分數取代原圖觀察。

| scene／選用路徑 | SHA-256 | 建議與實際觀察 |
| --- | --- | --- |
| `h02-history-tree-rings`／`keyframes/h02-history-tree-rings-1.jpg` | `e811eaa0db0f7ca8d76e76f6c14f856faedf4c8ec6c9809c13dbde1db6d18f2c` | **RETAIN_WITH_EDIT_NOTE**：同心年輪、放射裂痕與木質斷面清楚，沒有角色、生成字或浮水印。畫成填滿畫面的整段樹幹橫切面，並非研究桌上的細長木芯；可以作年輪概念示意，不稱為維吉尼亞實際樣本、取樣方法或乾旱測量數據，也不按畫出的圈數推定年代。不為橫切面／木芯的構圖偏差重買。 |
| `h02-history-survival-pressure`／`keyframes/h02-history-survival-pressure-1-trim.jpg` | `c2f726605c97a3ec48500cf4b3bb26295e7f85b672bbba26b07237d48b22ddef` | **FIX_REQUIRED：歷史生存場景出現現代電線設備。** 枯萎玉米、乾地與左側小屋可辨，但清楚有兩組電線桿及架空導線，使歷史生存壓力畫面讀成近代農村。這是明確現代設備，不是玉米位置或色彩差異。沒有角色、生成字或浮水印；協調者另行原圖確認第 9 項必修，採乾旱推論來源卡，保留「可能增加生存壓力」與仍無法回答去向的邊界，零新購。 |
| `h02-history-romantic-book`／`keyframes/h02-history-romantic-book-1-trim.jpg` | `7d582745c81bf3e92d649396a832139e73b5402726515f69c971f7dba6db1b16` | **RETAIN_WITH_EDIT_NOTE**：匿名讀者、書房、素色布衣／領巾與空白書頁清楚，沒有假書名、額外人物或浮水印。書是打開而非關閉，桌上杯及眼鏡樣小物屬次要物件；沒有足以辨認電腦、滑鼠或其他現代電子設備的特徵。按十九世紀閱讀情境可作泛用示意，不稱為特定作者肖像或作品封面，不為書的開合重買。 |
| `h02-history-stones-appear`／`keyframes/h02-history-stones-appear-1-trim.jpg` | `caa0fe27333123b61640dceb904cabd36d6bcb6bd3abb1bbd8fdb06d2d103b8c` | **RETAIN_WITH_EDIT_NOTE**：木桌／架上單一粗糙石塊表面留白，沒有假刻文、人物、擬人臉或浮水印，可以承接號稱刻字石的器物示意，不稱此圖為真實刻字石照片。左上牆面有小型展示標牌，含白色短字形及黃色橫線樣偽文字，無可確認的真實內容；不杜撰其字義或稱為館藏證據。協調者確認先保留觀察註，等實際 renderer 裁切／顯示範圍再判斷小標牌是否干擾，不為此提前重購。 |
| `h02-history-stone-inspection`／`keyframes/h02-history-stone-inspection-2.jpg` | `27911b7dd90ddb5251461fa611e5ebe9096946a88d1d91981daa9ea67997c22e` | **RETAIN_WITH_EDIT_NOTE**：單一戴手套的手握圓形放大鏡，沒有額外手、身體、臉、假檢驗文字或浮水印。鏡片沒有柄，手指夾住鏡緣，桌面沒有石塊／可辨石面，與原 prompt 有偏差；鏡內白色弧線／點讀為反光，不是完整吉祥物臉。可保留為泛用檢視示意，不能當作對特定石頭的檢驗操作或結果證據；旁白已區分多數偽造與首塊未定論，圖中沒有捏造結果。judge 的 7.18／passed／needs_review false 只作狀態記錄，本判定來自實看；不為無柄、握法或未見石面重買。 |
| `h02-history-artifact-question`／`keyframes/h02-history-artifact-question-1.jpg` | `3a58064e68d3cce26d08706ac02b9f9fdcb2b82cb71a61a1b10cbacc234125d0` | **RETAIN_WITH_EDIT_NOTE**：匿名灰髮年長讀者、素色深外衣／襯衫／領帶、圖書室與空白書頁可辨，沒有假書名、現代電子設備、額外人物或浮水印。原 prompt 已指定十九世紀 reading room，廣義正式衣著可作該段示意，不套用 1590 年船員服飾限制，也不當作特定歷史人物肖像。書本、杯及表情細微差異不改變器物判讀問句，不列必修。 |

本組 5 張可留、1 張必修。本範圍 36 張新增 selected 全數完成實際原圖覆核，27 張可留（含偏差／成片觀察註）、9 張必修。加 22 張未變圖片沿用既有完整 SHA 的紀錄，累計 58 張有目視證據。後段另外 28 shots 由其他審查範圍接續；本節不給它們通過結論，也未實看來源卡渲染、運鏡、CC、聲畫或完整成片。

### 本範圍集中必修清單：9 張，待整批後改來源卡

以下每項均先由本審查者實看，並經協調者另行原圖確認；完整 SHA 為被指出問題的原 selected 圖片。協調者決定以來源／事件／推論摘要卡集中修正，保留原候選，不追加圖片購買。此清單仍綁 `294227a3…` 的圖片覆核，**不表示新來源卡已套用、渲染、核准或完成成片覆核**。

| scene | 原 selected SHA-256 | 必修及後續處理邊界 |
| --- | --- | --- |
| `return-creek-search` | `db2d02682bd6f31d8e98f012f28b7733b1ec294123a3b9ad34d99bebe5d3e068` | 後世雙角帽／金邊軍裝；來源卡「沿溪搜索／船艇與小炮」，保留 c14 及原搜索旁白，下一鏡繼續交代沒有找到。 |
| `return-hope-has-limit` | `be526f51721f1e00e6868e579ca1281bd5f09931d16ee80b9d5ab16efccb52b3` | 木柵變石造城門；卡「讀懂留言之後／有去處，未定下落」，來源明標「本集判讀」，不冒充懷特逐字引文。 |
| `route-croatoan-place` | `e9866399f71c08104f17986234c56530b9566c3f815e219fe5658d90b9959e35` | 原住民住處變近代白牆玻璃窗小屋；卡「族名，也是地名／克羅托安」，不新增精確海岸形狀主張。 |
| `route-broken-cable` | `2cd9c665896ec59156c0889d8798988a0812dc233e2ffb11b81d8c3ed38d0e3c` | 船首黃頭護目鏡機器吉祥物；改來源卡，保留原 c18 及纜繩／返航條件敘事。 |
| `route-captain-decision` | `62d5b1a31cbcd97ed0995f8a8c9a06dfa943387397db8a9e27d247d417d6df3a` | 1590 年人物戴後世硬挺金邊船長帽；改來源卡，保留 c18 與船長決定的原旁白。 |
| `route-storm-sail` | `64c081c02b67d007af8cd71f544a575b0ebd93e328cebd67bee91ab0ceb8aa65` | 兩個甲板器物長出大笑臉；改來源卡，保留 c18 及天候／返航敘事，不新增怪船角色。 |
| `route-third-birthday` | `78c66ae201e672f6af7f1cfdf8afd0c2a0f0defe5672960ba2b671b73fc8ae60` | 搖籃旁大型熊臉抱枕／玩偶；生日事件摘要卡保留 c2／c7，不畫成已知生還嬰兒或近代嬰兒房。 |
| `h02-history-late-story` | `05ad524bfb9e38d974914198cd439a54d0619e1e6c65d9f38f634da2d0fb3f9f` | 蘆葦頂沿海住處變磚石拱門塔亭；晚期祖先傳聞摘要卡保留 h02e1 及「一百多年後」的記錄時距，未定命運。 |
| `h02-history-survival-pressure` | `c2f726605c97a3ec48500cf4b3bb26295e7f85b672bbba26b07237d48b22ddef` | 現代電線桿／導線；乾旱推論卡保留 h02e3 與「可能增加生存壓力」邊界，不以乾旱解案。 |

本審查者僅更新本報告；未改源稿、媒體、manifest、judge、核准、native stage、LEASE 或 STOP。純風格、微小道具、姿勢及無明確現代特徵的行囊不擴成必修；實際成片再檢查小展牌、前景裝飾及相關偏差是否遮蔽旁白重點。

## 十八張來源卡：獨立候選覆核與實際套用收據

本節將上面各組「待整批後修正」的歷史狀態更新為實際 source 收據；逐張原圖觀察、原 selected 完整 SHA、judge／人工接受建議與已看範圍不被覆寫。

獨立候選階段只寫外部 `_audit`：十八卡逐張語意／完整差異報告 `final-native-cards-preview-18-independent-review.md` SHA-256 `d4faa1cfeb9070593f5862d69dd99f307344b7227980e33f4e8f77b136aac9b2`；frozen 語意／控制檔／86 張實檔雜湊報告 `final-native-cards-frozen-18-independent-review.md` SHA-256 `60584f657a3c003420214249c86b4b1a16bd98646c5771c9949cc8e5a64266a6`。frozen 候選 SHA `cea7541ad5909406ba9fb52b7bdefa4c72609cadc14c0dbb5fed18617689ca28` 已經本審查者 185 checks 獨立通過，含全部原 86 selected bytes 的兩次完整 SHA readback、strict ledger 297 筆 totals 重算、零 jobs／reservations、root owned STOP 與無 LEASE。這些是當時 freeze 的證據，不描述後續控制檔當前狀態，也沒有把 full SHA 重算說成重新目視後段 28 圖。

root 後續把同十八景 source 差異實際套用；實際變更收據的獨立 proof 狀態為 `INDEPENDENT_ACTUAL_SOURCE_DELTA_PASS_MEDIA_DELIVERY_PENDING`，checked_at `2026-10-11T20:50:18.434Z`（UTC），SHA `913ae5039b8b14167311a46537ec666e4d2dc8e787a8facad63a94f001a1d1ee`。本審查者已重新讀回這個 proof，394 項 checks 全 true，並核對 actual source 為 `4dfe4d73dd458323949542ba5c22cd68a7838cbdc237b36543b07ea18620322e`、claims 仍為 `6db38c75194a57b3361ee9eaab058b46da1f76fa0bab47ac48ea70de187be3a3`。

實際 delta 僅十八景 template／data 改成來源卡：`return-creek-search`、`return-hope-has-limit`、`route-croatoan-place`、`route-broken-cable`、`route-captain-decision`、`route-storm-sail`、`route-third-birthday`、`h02-history-late-story`、`h02-history-survival-pressure`、`h02-find-brass-analysis`、`h02-find-dating-first`、`h02-find-context-question`、`h02-find-trade-route`、`h02-find-inference-step`、`h02-close-link-life`、`h02-close-identified-house`、`h02-close-persons-unknown`、`h02-close-unclosed-file`。前九景是本報告的早段必修原圖，後九景的問題由 root／後段原圖審查者確認；本代理負責全部十八張卡的語意及完整差異，不重宣稱目視後九張原圖。

109 scenes、134 個完整 line 物件及 claims／cue／emotion／chapters／reveal／integer geometry 全保留，actual 128 states／20175 frames、120 TTS requests，speech `20d0bfc523979b9f`、look `e77cf823ca0ea548` 不變，pictures 由修正前改為實際 `fa7e4b12363d155e`。actual weighted 插圖比例 11064／20175＝54.8401%，高於 0.5；source 現為 68 shots。上述為候選及 actual source proof 的重播結果，沒有把時碼不變當成字卡實際顯示已通過。

另已讀回 root 控制收據 `_audit/stop-released-final-native-cards.json`：root 於 `2026-10-11T20:51:10.262Z`（UTC）只釋放 owned STOP，原 STOP SHA `68a9091138c1e7b5ad5256f6b9b9f6bfdeb5c5babecc5a8810c4206dd8dff7e3`，global_stop_removed false；本審查者沒有操作 STOP。TTS evidence 刷新 receipt／log `_audit/tts-2026-10-11T20-51-12-261Z.receipt.json` 及同名 `.log` 顯示成功、0 requests synthesized／0 billable characters／120 reused。這只確認既有旁白重用刷新，不替代聽音、成片、上架或站主接受。

### 原圖與人工建議仍有 take 邊界

早段 58 張紀錄仍綁當時 `294227a3…` 原圖：22 張沿用圖片與本代理實看 36 張新增 selected。九張改卡後，不再把它們當成 current shot 的保留建議；另外 49 景要對回新 manifest 的實際 selected 路徑及完整 SHA 才能沿用同內容觀察。祖父 `farewell-grandfather-1-trim.jpg` SHA `dc8e70cdeeac46016292116732585ca64767726ae41ff77678c1fd3f845d749c` 與新生兒 `farewell-newborn-1.jpg` SHA `7b92ded709eac3cf2439f37ad09cc33db2bd40db9da952c931eebddbb1cda0a5` 的人工保留建議只對這兩個 take，未修改 judge 或 `needs_review`，未執行 accept-best／owner approval。`h02-history-stone-inspection-2.jpg` 無柄／未見石面的泛用示意限制與 `h02-history-stones-appear-1-trim.jpg` 的小展牌註記仍保留，不能用 judge 分數抹除觀察，也不為次要偏差擴成重購。

### render 顯示覆核計畫（生成前紀錄）

預定實開十八張已改來源卡的實際 rendered frame、三張 PD 圖的實際 framed 結果與縮圖，逐檔記錄完整 SHA、source／render 版本和可見結論。卡片需驗證文字／日期／摘要或推論／傳聞／非戒指定年／較早 NPS 評估等標籤、引號、折行、字級、來源行與留白是否實際可讀；不把 quote 版型引號誤作新取得的逐字引文。

三張 PD 圖分別為 `farewell-arrival-print`（1590 de Bry 後世版畫，非 1587 抵達實拍）、`farewell-baptism-print`（1876 Sheppard 受洗想像圖，非當年現場紀錄）、`h02-history-ruins-picture`（1893 John Parker Davis 後世想像，刻字位置與目擊記述不同）。覆核時確認實際 caption／credit 與圖像裁切／傾斜沒有藏掉這些限制；原 stock SHA／授權另有素材收據，不冒充本代理已看 final frame。

縮圖 source 預期顯示「不是咒語／歷史懸案／他知道去處，卻沒找到人」，使用 `hook-white-happy`；要驗證重點與這個未解命運的邊界、角色、文字折行與手機尺寸可讀性。當前尚未取得 root 交付的新 manifest／render 完整 SHA／實際縮圖，不給它們 PASS，不宣稱完整成片、CC、聲畫、backend review、owner playback 或上架完成。本代理未執行 native stage、API、媒體或 source 修改。

外部 `_audit/final18-render-qc-plan.json` 已依實際 source 列出十八卡／三 PD 圖／縮圖預期內容，SHA-256 `f109fe7e2c0967918a50eeb0d1f822166ed4dd80ff969781dd1d956a593b98ee`；全部 viewed false、render／manifest pins 留空，等待 root 實際產物。預期 geometry 的依據僅為 immutable actual-source proof timing_after，不把計畫當成已渲染證據。

## 正式 render：24 張實際靜圖覆核

本節更新上面的生成前計畫；原計畫、候選、原圖問題與歷史 hash 仍保留。本代理逐一以 `view_image` 實開 **18 張替換卡、2 張原 CRO／CROATOAN 卡、3 張 PD framed 圖與縮圖，共 24 張**。沒有阻塞顯示問題；縮圖副句的跨行保留排版註記。這是所列靜圖的顯示覆核，不是整部成片、動畫 transition、音訊或字幕整合通過。

綁定的 current keyframes manifest SHA-256：`92961cfc19a1109001fdc82e1f2b4cde66042580d41eb898c67930acdfc67055`，完整 68 selected，pictures `fa7e4b12363d155e`。正式 `frames/manifest.json` SHA-256：`fbcee7b24a321044e189eeee34f2e6f4dd6d3c3f1ea0deaa9afa1d3e43f5edc0`，visual `75becb74ee2f79c7`、theme `17fcf59dd1a1f4ac`，109 scenes／60 native still states、1920×1080／30fps。上述 manifest、actual source `4dfe4d73…` 及所看檔案都再讀回完整 SHA，穩定且相符；沒有用正在生成的 cache 或聯絡表替代 final manifest。

current timeline SHA-256：`4c9de49bf9536d6d645b6aa3cd40a7301a809bd1149365223910922cbb8ff4c3`。TTS 刷新後增加 134 個逐 line `audio_sha256` 證據欄；只排除這些音訊雜湊 metadata，所有其餘 scene／line／chapter integer geometry 均與 immutable actual-source proof `timing_after` 完整相同，仍為 20175 frames、30fps／48000Hz。沒有把 geometry 相同當作聽音或成片播放證據。

外部完整逐檔覆核：`_audit/final-render-24-actual-image-qc.json` SHA-256 `78db8e6806989d14f1972661b9010850b34a8941a051372dcf0616d3b971c969`；人讀報告 `final-render-24-actual-image-qc.md` SHA-256 `7b6f596c78daf214408a527cc47a769576e8ac6f432375c955029f02c3e109a2`。495 項唯讀 checks 全 true，含官方純 `renderPlan` 的所有 scene／state key 對映、正式 manifest 檔名／reveal、60 張 PNG 尺寸／完整 SHA、transition 檔案存在、24 張所看圖的 post-view 完整 SHA、current source／claims／manifest 再讀。24 張實看中有 23 張 native still states 與 1 張縮圖，因此其他 **37 張 native still states** 僅有檔案／對映檢查，**不宣稱實看**。原外部 QC 的 prose 寫成 36 張為計數筆誤；原檔與 SHA 保留，更正另見 `_audit/final-render-24-qc-count-correction.json`，不更動實看清單或判定。

下列路徑均相對 `<VIDEO_WORKDIR>`；每行是實際開啟的最終圖，已對回 final frames manifest。

| scene／實際檔案 | 完整 SHA-256 | 可見結論 |
| --- | --- | --- |
| `return-creek-search`／`frames/001c4a0d41d420bd.png` | `3a55397480e7a9895f78ec185fac2cfa8313754427d5b6b78a9f9ee1d164b681` | 「沿溪搜索／船艇與小炮／搜尋對象摘要」完整可讀，表示搜索對象，不是發現結果。 |
| `return-hope-has-limit`／`frames/39b8ed7fbd37f4fa.png` | `6dd3e00005622ddeac7a6bec885f051a7ed82cec72bfe4bf342eb8aad2430b39` | 「有去處，未定下落」及「本集判讀」完整可讀；摘要引號沒有冒充懷特逐字引文。 |
| `route-croatoan-place`／`frames/f9a940676a7ec392.png` | `570404f580db6efda92b2fca72c4181479a9ed74f7c4befcd4f1fc73fd43aeef` | 「族名，也是地名／克羅托安／名稱用法摘要」完整可讀，沒有新增精確地理外形主張。 |
| `route-broken-cable`／`frames/0ebab1bbab6300bf.png` | `99e9501f716612b0c3142c2bfeaf50db82f2ffa05bee0d2712c6ec1826a4ae0b` | 「航程受阻／斷纜、失錨／事件摘要」完整可讀，原護目鏡吉祥物不再顯示。 |
| `route-captain-decision`／`frames/fc4a117b3258655a.png` | `14f8c2adbc64d9e2442670464e164fd9de1ad688987524d1d7e70b19f043076e` | 「先讓船停得住／停泊與安全／本集判讀」完整可讀，原錯年代帽不再顯示。 |
| `route-storm-sail`／`frames/34cb1e7f47044069.png` | `a7cc9db5505996c651ae62cbd358e1aae446977c29cdd7b70f2bf8f79775a6a2` | 「未完成的尋人航程／天氣阻住了去路／事件摘要」完整可讀，沒有器物笑臉或已抵達暗示。 |
| `route-third-birthday`／`frames/27bc0b9fbbe9aee6.png` | `1d6fdc0ca03c109577b0f1e859fca7d28429b1bbde8a46ee34074fd26c988868` | 1590 年 8 月 18 日及三歲生日完整可讀，明標「未證實當時仍在世」，沒有畫成已知生還。 |
| `h02-history-late-story`／`frames/76df037f1b8837f2.png` | `2368951b85c5349dbb1959c37a2b9c395a7368e007e45e872c4d330d471ca2e3` | 一百多年後的祖先故事及「傳聞摘要｜勞森1709年出版著作」完整可讀。 |
| `h02-history-survival-pressure`／`frames/955cc18b51a99594.png` | `daf0be6063fd191fe890e4bed4f537ab3f29f0185ac18c96e3afde4174a299b0` | 區域乾旱、可能增加生存壓力及「推論摘要，未解人員去向」完整可讀。 |
| `h02-find-brass-analysis`／`frames/b025736f719045c5.png` | `025f21e24ef04b3b387e5d973679e9bc802897e47d62e6d789a8f02f774d1e46` | 銅與鋅：黃銅／ECU／Smithsonian，2017完整可讀；材料分析摘要明標未認出主人。 |
| `h02-find-dating-first`／`frames/bfd245ea0d165199.png` | `014ba0adec915377b8baac76d2c65fd53f660fb20864647de41a7330aea5f0fa` | 戒指附近器物年代跨至十八世紀初，完整顯示「附近器物脈絡，非戒指定年」。 |
| `h02-find-context-question`／`frames/35cb167ed746fe14.png` | `01ca4ff2444b696cae9b84b45801dd5b2baaf405e7b2c7ddbc59cfdc1aae7257` | 器物年代／原本出土地層及「本集判讀方法，非新發掘成果」完整可讀。 |
| `h02-find-trade-route`／`frames/e75f9e9db2ea90a5.png` | `54f2a23abbd86b531f0b5751c6e627f80a0ce5970a4c269a7daefbc9a8348332` | 可能透過交易進入村落及「可能路徑摘要，非定居判定」完整可讀。 |
| `h02-find-inference-step`／`frames/ae8daf00eafa7543.png` | `57dc0d81702d3a56b87642958e1e10c91e11911e2f5830dd225398d2545bb4a4` | 器物位置→聚落推論／仍需獨立檢驗，完整標「非新結果／NPS較早評估」。 |
| `h02-close-link-life`／`frames/d3cb96ed81ca376e.png` | `1325222f7db450e39ad3a28a45b39c42269b18eb3e27624aa89d589e9486a1fb` | 器物↔可確認的生活現場，完整標「本集條件式判讀，非已找到原屋」。 |
| `h02-close-identified-house`／`frames/19fa997c85d6caa3.png` | `9e7ab5eb75d753a0b3038a7a5b65fea609ec0efeb84d7e2c722c08a9d3485911` | 如果房屋能確定屬於他們／器物才多了生活脈絡，完整標「非已出土房屋」。 |
| `h02-close-persons-unknown`／`frames/aad899dbdbbb8103.png` | `587e9e618f11689a2697ec4a5fdb6fe8f26c1ba5a9b088db3b625057cc880dfb` | 目前器物資料仍無法認出每個人結局及 NPS 較早評估完整可讀，沒有多餘角色或假字。 |
| `h02-close-unclosed-file`／`frames/618b964eb309ffe4.png` | `cadb87ba20f1e122894400e4218cd5af2600a8bc6253a6d6e870280737ee3415` | 去處留下線索／航程未完成、實際去向未確認完整可讀，沒有貓印章／假字或全員抵達暗示。 |
| `return-tree-cro`／`frames/142cd9aa4a8591e5.png` | `d59d49c95924845f57462e4928c701d0be1017476d2457497949711fe66d42a1` | 「樹幹上的三字母／CRO」及來源完整可讀。 |
| `return-post-croatoan`／`frames/c609bce7b1561941.png` | `60e012db1b152c2eeb68a9f6e6942f281e254e616d0de9e297ec6fe87f9fa1e7` | 「柵欄入口的木樁／CROATOAN」及來源完整可讀，與樹幹三字母分開。 |
| `farewell-arrival-print`／`frames/ac69208a60e302a7.png` | `b6cfbf2a5fb4cf25e9c8fb8a4c7b76e033214bdc9cf071e95aa8d8673d2e9007` | de Bry 後世版畫、1590／非1587抵達實拍及國會圖書館公有領域credit完整可讀。 |
| `farewell-baptism-print`／`frames/bb4cbb80cb3586f8.png` | `b956a7207be83ebb4f0269ae08c9f630b6b4ccfacb3cbd889cb0e368d3c6af09` | 1876 受洗想像圖／非當年現場紀錄與 Sheppard 公有領域credit完整可讀。 |
| `h02-history-ruins-picture`／`frames/5d1537f6ede45b90.png` | `4d15443a0cb1c996871365ca4d24c5ef4f5ea8df48b7f9708b2a00e0a1012598` | 1893 後人想像／刻字位置與目擊記述不同與 John Parker Davis 公有領域credit完整可讀。 |
| `thumbnail`／`thumbnail.jpg` | `93427f863a7eb0a42504aa333c46265b3a8e4970cf3a01045a499a38d1f74b25` | 1280×720，主標「不是咒語」清楚，沒有 Markdown 星號；副句完整但「找到人」跨行，保留排版註記，未宣稱已解案。 |

十八張替換卡均有明確事件摘要、本集判讀、傳聞、推論或條件式標籤；版型引號與標籤一起閱讀，不冒充新取得的逐字引文。三 PD 圖保留完整 caption／credit，畫面裁切與傾斜沒有藏掉後世想像的證據限制。縮圖主標、角色及副句符合「知道去處，未確認命運」的本集承諾；本代理未用手機播放 UI 做實測，也未給上架或站主接受結論。

### 49 張早段原圖：current selected take 對回

正式 keyframes manifest 中 49 景的實際檔名／seed／完整 SHA 均與本報告先前目視紀錄完全相同，並重新算實檔 SHA 對回 manifest。可沿用各圖既有 RETAIN／偏差註記；九張改卡原圖不再列為 current shot。完整 49 筆對映在上述 JSON 的 `retained_early_raw_scope.entries`，沒有把已淘汰 take 的觀察套到新圖。祖父 `farewell-grandfather-1-trim.jpg`、新生兒 `farewell-newborn-1.jpg` 及檢石 take 2 的實際選用內容維持原 SHA；原人工建議與 judge 意見仍各有邊界，本代理沒有替它們改 judge、人工核准或 accept-best。

本代理另重新計算全部 68 selected 實檔 SHA 與 current manifest 一致，這是內容完整性讀回，**不是全 68 圖重新目視**。小展牌及無柄放大鏡的既有示意限制仍保留；本次 24 張 rendered 卡／照片／縮圖不包括它們在完整成片中的裁切結果。沒有對 assembly、完整 MP4 播放、CC 整合、音訊、backend review、owner playback、上傳或公開發布給通過結論；本代理未執行 native stage、API、paid、source／媒體／manifest、LEASE 或 STOP 修改。

## 成片抽樣：16 個正文點與 4 個品牌界線

在 root 提供正式 assemble exit 0 收據後，本代理依原計畫，使用指定 Winget ARM64 FFmpeg（decoder 2／filter 1／PNG encoder 1 threads）從完成的 `final.mp4` 擷取並逐張以 `view_image` original 實看。**16 個正文點＋4 個品牌界線共用最後正文格，合計 19 張唯一 PNG**；所列抽樣未見阻塞版面或主體問題。這是成片抽樣通過，不是整部影片聽看、全部動態或 CC 播放器驗證。

actual `final.mp4` SHA-256：`d86471c94a661023f697f2261bab8c8a61a8bf203a1a1c09b9f3ace28eb1c5a6`，204325624 bytes，1920×1080／30fps、20415 frames、680.5 秒；抽圖後及最終 QC 再讀回仍完全一致。actual body SHA-256：`a061ad4c1a6b2ce6cdfa745da88afc8d0bf57a3e6e2c67f656bb1cc173654806`。applied branding hash `a27622022d8d9e2f56221a81a1d7443ab241c40a37a515925784511f0416dcdd`，intro 150／body 20175／outro 90 frames，正文 offset 5 秒。來源 `4dfe4d73dd458323949542ba5c22cd68a7838cbdc237b36543b07ea18620322e`、claims `6db38c75194a57b3361ee9eaab058b46da1f76fa0bab47ac48ea70de187be3a3`、timeline `4c9de49bf9536d6d645b6aa3cd40a7301a809bd1149365223910922cbb8ff4c3`、frames manifest `fbcee7b24a321044e189eeee34f2e6f4dd6d3c3f1ea0deaa9afa1d3e43f5edc0` 及 keyframes manifest `92961cfc19a1109001fdc82e1f2b4cde66042580d41eb898c67930acdfc67055` 全部重新讀回原 pins。

新證據位於 `<VIDEO_WORKDIR>/_audit/final-cut-visual-samples-2026-10-11T21-27-48-651Z/`：`final-cut-sampled-visual-qc.json` SHA-256 `76ba8578e8374404bdb719f97220d49812dfbecf589af6260d24681acfdb82b4`；人讀報告 `.md` SHA-256 `6874cf75b09b7df4571a76fe5424cf000b2de05af4c1ea160dc8423a79a22b85`。175 項唯讀 checks 全 true，含逐圖 post-view 完整 SHA、實際 PNG 尺寸、16 點 scene／完整 data／claims、reveal／integer interval／指定 take 或 still reference、4 界線及 source／media 完整 bytes 再讀。每張唯一 PNG 的完整 SHA 與實看註記均在新報告，不覆寫原計畫或 495 checks 靜圖證據。

下表時間為成片抽出格子的實際 PTS；frame 為零起算解碼索引。每列均已實看，不包含未抽樣時段。

| scene／reveal | final frame／實際秒數 | 可見結論 |
| --- | --- | --- |
| `hook-white-happy`／0 | 180／6.000000 | 老年懷特、帽、木柵與海面清楚，沿用已知手部偏差。 |
| `hook-place-not-verdict`／1 | 754／25.132682 | 只顯示左框「知道去處／CROATOAN：克羅托安」，右框未提前出現。 |
| `hook-place-not-verdict`／2 | 894／29.799349 | 右框才顯示「未確定下落／不能證明每個人的命運」，左框保留。 |
| `farewell-grandfather`／0 | 3125／104.162435 | 原 1-trim take 的祖父、木搖籃與晨光完整，保留既有風格註記。 |
| `farewell-newborn`／0 | 3284／109.461784 | 原 take 1 的閉眼新生兒、素布與木搖籃清楚，保留既有風格註記。 |
| `return-tree-cro`／0 | 5890／196.327148 | 樹幹三字母 CRO 及來源完整可讀。 |
| `return-post-croatoan`／0 | 6048／201.593490 | 柵欄入口木樁 CROATOAN 及來源完整可讀，與樹幹分開。 |
| `return-two-carvings`／1 | 6196／206.526172 | 只顯示左框樹幹 CRO。 |
| `return-two-carvings`／2 | 6351／211.692839 | 右框新增木樁 CROATOAN／離地5英尺、約1.5公尺；左框保留。 |
| `route-third-birthday`／0 | 11705／390.152995 | 1590年8月18日、三歲生日及「未證實當時仍在世」完整。 |
| `h02-find-dating-first`／0 | 15664／522.113802 | 附近器物年代與「非戒指定年」完整，沒有冒充戒指本身定年。 |
| `h02-close-link-life`／0 | 18587／619.544206 | 器物↔可確認生活現場、條件式、非已找到原屋與 NPS 較早評估完整。 |
| `h02-close-identified-house`／0 | 18757／625.210547 | 如果／才及「非已出土房屋」限制完整，沒有冒充找到原屋。 |
| `h02-close-unclosed-file`／0 | 19996／666.508594 | 航程未完成、實際去向未確認完整，沒有舊圖貓章或假字。 |
| `h02-close-outro`／0 | 20121／670.675260 | 正文「未結／mokaair.com」完整。 |
| `h02-close-outro`／0 | 20324／677.441927 | 最後正文格仍是未結卡，未被品牌提前覆蓋；與下列界線共用。 |

四個品牌界線均已實看：intro 最後格 frame 149／PTS 4.966667 為 Mokaair 與「開啟 CC 字幕」提示；frame 150／PTS 5.000000 才進入懷特正文。frame 20324 仍為未結卡；frame 20325／PTS 677.500000 才進入淺色 Mokaair 品牌 outro。兩對相鄰格無空白、錯內容或提前覆蓋；僅對這些格子給結論，不延伸為完整動態與聲音銜接通過。

原擷取 helper 在 FFmpeg 成功產出 19 圖後，因 1ms 容差比較 actual PTS 與 `n/30` 而回報驗證失敗。新 `extraction-recovery-receipt.json` SHA-256 `1385bd833d59369ee1544f7ea5746f9b071560611fc09bfecc61d4224bae583c` 保存這個失敗邊界，重新核對精確 `select=n` 索引、19 輸出順序、geometry 與全部來源／媒體 pins；最大抽樣 PTS 差 24.74ms，小於一個 30fps 格。新報告分列實際 PTS 與名義 frame 時間，沒有重抽、修改成片或掩蓋原 helper exit 1；不據此宣稱全片聲畫同步已驗證。

raw 正文沒有燒錄 CC，符合 source `burn_in=false`；品牌的 CC 提示不是播放器已開啟字幕的證據。兩組比較卡的來源行靠近下緣，外掛 CC 的顯示及重疊尚須播放器另驗，其餘抽樣卡主文與來源下方可見留白。前節 23／60 native still＋1 縮圖及另外 37 未看是該獨立靜圖 cohort；本次成片抽樣不改其原計數，也不合稱全 60 靜圖已看。本代理沒有聽音、完整播放、站主接受、上傳／公開發布結論，未改 API、native stage、paid、source／canonical media／manifest、LEASE 或 STOP。
