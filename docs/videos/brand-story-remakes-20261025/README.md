# 後台品牌故事：新規則重製

依站主「參考1844、從C03開始、完成就接下一個、採推薦設定、預設八語」持續製作，並依追加指示套用 [PR1860](https://github.com/x812033727/travel_scanner/pull/1860) 的正式片頭片尾取得流程。**17題SOURCE／書面配鏡及原生敘事合併PASS；其中16題八語未定時文字TEXT_PASS，共14,600句／792章。行李箱R7來源PASS但native6 HOLD，不列17題；這些數字都不是成片數。實際故事音訊、插圖、配樂、影片及付費請求仍為0。** [逐項狀態](status.json)與[接續順序](execution-order.json)綁定各集當前檔案雜湊。

正式站全頻道 v4 套件 `mokaair-brand-package-v4-endscreen` 已下載並安裝，package SHA `416c8768d4d29f2e746a0c019d2d598ec367cbb66b0ff996841c523651a63e88`。兩檔均1080p30，實SHA、150／630格與完整影音解碼通過：**開場濃縮後5秒片頭、最後21秒片尾**。這是兩份重用製片素材，並非生成故事媒體。[正式取得、影音QA及操作指南](branding-pr1860/README.md)與[必要包規則](branding-pr1860/required-branding.json)已落地；[preflight](branding-pr1860/preflight.mjs)在缺檔、錯包、版本不符或無法比對正式站時停止。每次真正合成前須重跑；尚無逐集production pin、timeline或組片。

C03正式TTS曾執行，在供應商派送前被 `video_budget_preproduction_hold` 拒絕。影片工具權杖有效，不需重貼；精確新版帳戶存在與否仍待正式主機查證，各片US$25上限的受保護啟用、實際歷史帳本及全片報價仍待完成。站主已選由Claude執行只讀主機交接，目前等待安全JSON；本機探針獨立PASS，尚未host run，不能用CLI hold或網站未列slug推論帳戶不存在。正式branding取得已解阻，不能繼續把它列為製片阻塞。[C03入場交接](c03/production-entry.md)、[正式主機唯讀交接](c03/connection-and-budget-readback.md)與[目前停線](production-hold.json)保存具體待辦；沒有借原slug帳戶、改前綴或移除保護。

| 題目 | 當前來源／書面分鏡／敘事 | 後台與八語文字 |
| --- | --- | --- |
| [C03 Moleskine](c03/production-entry.md) | R3來源／書面配鏡及actual native3合併PASS | 企劃核准已匯入／劇本核准已匯入；1,144句TEXT_PASS；後台八語三部分全選 |
| [C04 泡泡紙](c04/production-entry.md) | R2來源／書面配鏡及actual native2合併PASS | 企劃核准已匯入／劇本核准已匯入；880句TEXT_PASS；後台八語三部分全選 |
| [C05 金鳥](c05/production-entry.md) | R13來源／書面配鏡及actual native12合併PASS | 企劃pending／劇本pending；872句TEXT_PASS，107句／語繼承原全量校對及2句／語獨立delta校對；後台八語三部分全選 |
| [C06 Play-Doh](c06/production-entry.md) | R3來源／書面配鏡及actual native3合併PASS | 企劃核准已匯入／劇本核准已匯入；1,304句TEXT_PASS；後台八語三部分全選 |
| [C07 Dr. Martens](c07/production-entry.md) | R10來源／書面配鏡及actual native9合併PASS | 企劃pending／劇本核准已匯入；672句TEXT_PASS；後台八語三部分全選 |
| [C08 龜甲萬](c08/production-entry.md) | R9來源／書面配鏡及actual native9合併PASS | 企劃核准已匯入／劇本核准已匯入；1,016句TEXT_PASS；後台locales={} |
| [C09 Patagonia](c09/production-entry.md) | R7來源／書面配鏡及actual native7合併PASS | 企劃核准已匯入／劇本核准已匯入；824句TEXT_PASS；後台八語三部分全選 |
| [C10 OXO](c10/production-entry.md) | R7來源／書面配鏡及actual native6合併PASS | 企劃核准已匯入／劇本核准已匯入；944句TEXT_PASS；後台locales={} |
| [C11 UCC](c11/production-entry.md) | R6來源／書面配鏡及actual native5合併PASS | 企劃pending／劇本pending；640句TEXT_PASS；後台locales={} |
| [C14 CamelBak](c14/production-entry.md) | R6來源／書面配鏡及actual native5合併PASS | 企劃pending／劇本pending；616句TEXT_PASS；後台locales={} |
| [C15 FriXion](c15/production-entry.md) | R5來源／書面配鏡及actual native3合併PASS | 企劃pending／劇本pending；632句TEXT_PASS；後台locales={} |
| [C19 Seven Bank](c19/preparation-completion-r8.json) | R8來源／書面配鏡及actual native8合併PASS | 企劃pending／劇本pending；904句TEXT_PASS；後台locales={} |
| [Seiko](seiko/production-entry-text-r4.md) | R4來源／書面配鏡及actual native4合併PASS | 企劃核准已匯入／劇本核准已匯入；1,160句TEXT_PASS；後台八語三部分全選 |
| [Garmin](garmin/production-entry-text-r4.md) | R4來源／書面配鏡及actual native3合併PASS | 企劃pending／劇本pending；1,080句TEXT_PASS；後台locales={} |
| [C20 Zippo](c20/production-entry-text-r8.md) | R8來源／書面配鏡及actual native8合併PASS | 企劃核准已匯入／劇本核准已匯入；864句TEXT_PASS；後台八語三部分全選 |
| [Dyson](dyson/production-entry-r5-prepared.md) | R5來源／書面配鏡及actual native2合併PASS；140句／7章／3,316 units，A單人one_line／no_recap保留 | free operator已凍結，企劃／劇本pending、locales={}；八語作者進行中，尚非TEXT_PASS；clean metadata獨立PASS |
| [行李箱](source-preparation-checkpoint-20261026.json) | history/r7凍結SOURCE／書面配鏡PASS；99句／2,330 units／25 loops，actual native6合併HOLD僅no_recap | R8作者進行中、未checkpoint；actual5是R6歷史，不沿用R4；無八語TEXT_PASS |
| [哆啦A夢](doraemon/production-entry-text-r6.md) | R6來源／書面配鏡及actual native5合併PASS；131句／6章／3,002 units，A單人no_recap保留 | 1,048句／48章八語TEXT_PASS，ID一處修正後獨立targeted PASS；兩卡pending、locales={}；clean metadata獨立PASS |

[原始全批共圖查核](opening-teaser-image-audit.md)保留發現缺口當時的快照；[當前逐稿核對](opening-teaser-plan-reconciliation.json)證明16集29個事件預告已有來源核對的書面共圖計畫。實際圖片尚未生成，不能稱實圖共用已驗收。正常回收圖先做一次，預告呼叫前只讀核對原生cache key與實檔SHA；缺cache停止，不觸發第二次付費生成。每對須獨立驗圖，最終manifest及檔案SHA仍須一致。

[本輪文字metadata收據](text-preparation-checkpoint-16.json)逐份核得14,600句／792章，為當前16集的未定時文字，排除舊基底、候選和未審草稿；各語metadata、章名、逐句文字與獨立校對鏈保存。C05 R13的16條新增譯句以獨立delta審查接續原107句／語全量校對，未冒稱重讀全部109句。純視覺換稿的語意校對以明列舊source SHA的rebind收據繼承，原始校對檔不改。這些均不是定時SRT、配音、語言輪或上傳資格。

原生兩讀者必要項只有兩位對同一項皆答no才失敗；單人保留意見完整保留。各輪HOLD、未審版本、raw答案、隔離輸入及來源SHA不覆寫。正式核准只適用其精確canonical劇本；視覺採用時的批准檔不變檢查與其後真實核准匯入分開留證。後台stage表示下一關，不能據此推定核准或媒體完成。C03／C04／C05使用合法legacy renderer卡片，後台分類仍story；官方report-only只為未分類卡填分類，實讀證明未覆寫既有owner選擇。

[原始盤點](batch.json)為22筆品牌故事、19筆未上YouTube、18題，非目前新增卡片後的後台總數。龜甲萬原版與short-v8為同題；[53份原稿SHA](original-preservation.json)未變。18題中16題已完成來源／原生合併及八語TEXT_PASS，其餘2題為Dyson及行李箱；Dyson R5已另外SOURCE／native PASS，合計17題，公開行李箱R7仍native6 HOLD。Seiko、Garmin、C20及哆啦A夢均已列入16份文字，不為C系列缺號發明集數。

製作目標13分鐘，**真實TTS正文720–840秒**，口徑含冷開場及有聲CTA，只排額外26秒片頭片尾。[原生計時口徑](duration-measurement-scope.json)區分規劃分項與全程計時。字數或估計時間線不是實聲通過；短稿不能靠慢播、沉默或重述填長。C07／C11／C14／C15刪除重述後的規劃長度風險保留，需來源與實聲再核對。

畫面採MiniMax image-01、唯一look `{"preset":"cute-mystery"}`，正文至少70%相關插畫、最多連續3張必要字卡；英語匿名prompt不含品牌、真人名、logo、可讀字及版權角色。台灣說書旁白、繁中燒錄及CC，layout d縮圖黃字黑邊主標／白副標。clean-master目前只有[衍生配方及metadata檢查](c09/variants/clean-master/README.md)，每個實際clean輸出仍須自己的完整QA及當前final核准。

[prepare-runtime.mjs](prepare-runtime.mjs)僅初始化明列集數的正常字典及官方劇本；已有批准的執行根不可覆寫。受控採用保留原核准、字典、語意校對及失敗回退鏈。[runtime-cli.mjs](runtime-cli.mjs)只交給官方工具，不解除付費保護。來源快取、公共研究影片與正式branding原件在倉庫外，Git只收文字證據。

[C07 R11範圍／容量研究](c07/candidate-scope-capacity-r11.json)已final，找到新決策與障礙材料，但自然13分鐘容量仍HOLD，尚未adopt；當前R10來源／native與672句八語文字不改。C11原容量研究亦保留，均不能用慢播、沉默或重述補時。Dora R6與Dyson R5已新增SOURCE／native PASS及凍結operator交接，clean metadata獨立PASS；Dora已全八語1,048句／48章獨立TEXT_PASS，加入16份完整文字；Dyson外部八語作者進行中，未列TEXT_PASS。行李箱以[history/r7](rolling-suitcase/history/r7/preservation-manifest.json)綁定source／native6 HOLD，R8工作稿排除。

[13集歷史checkpoint](text-preparation-checkpoint-13.json)與[14集歷史checkpoint](text-preparation-checkpoint-14.json)維持原bytes，對應reconciliation exact副本分別保存在[13集archive](history/opening-teaser-plan-reconciliation-13-20261026.json)與[14集archive](history/opening-teaser-plan-reconciliation-14-20261026.json)。[15集歷史checkpoint](text-preparation-checkpoint-15.json)記錄前輪原SHA、14集發布commit `f1cf3eae8727910162a996a28a344ca7539f7618` 與archive SHA，保留前後來源鏈。

[入場停線文件](production-hold.json)現列16個精確slug的本地文字ready清單，每片cap US$25；帳戶存在、歷史、餘額與啟用狀態均待正式主機證據。本輪變更前文件已[exact archive](history/production-hold-before-sixteen-text-20261026.json)，這次清單更新不授權支出或啟用帳戶。Claude只讀安全JSON仍待回，正式v4兩份重用素材尚未逐集assembly。

[已發布SOURCE進度收據](source-preparation-checkpoint-20261026.json)保留commit `7133137e6fb133dea6d8f9557e4d8b6916d97f3b` 當時17題SOURCE／native與15題文字的原bytes；[當前16題文字forward](text-preparation-checkpoint-16.json)新增Dora全八語結果，SOURCE／native仍17。正文實聲仍全部未知，Dora／Dyson／行李箱的字數及cut估時都不是720–840秒通過。

[正式後台安全GET報告](backend-current-status-20261026.md)核實15份文字稿的精確canonical：企劃approved8／pending7、劇本approved9／pending6；8題實選八語metadata／CC／dub，其餘locales={}。報告是匯入前觀測；其後[C07 script](c07/approval-import-current-20261026.json)、[Seiko兩關](seiko/approval-import-current-20261026.json)、[C20兩關](c20/approval-import-current-20261026.json)共5筆真owner決定已由官方review-pull匯入，舊freeze／status／entry保持歷史狀態。加入Dora凍結operator的兩張pending卡後，16題目前已知企劃approved8／pending8、劇本approved9／pending7，八語實選仍8題。語言全選仍不是實clean影片或配音資格。

[C03全片報價缺口稽核](c03/production-quote-gap-audit.md)與[當前製片入口](c03/production-entry.md)、[主機只讀交接](c03/connection-and-budget-readback.md)已對齊：現行保護在每次派送前核對已結算、保留／不確定額與下一操作上限；沒有新增「全部未來模型上限總和必須≤25」關卡。完整all-in quote與真host JSON／受保護啟用仍缺，generic USD200不代表授權。production-hold的activation用語已明列unknown_pending_protected_host_readback，變更前exact bytes另存[歷史快照](history/production-hold-before-explicit-unknown-20261026.json)。

[16題文字checkpoint](text-preparation-checkpoint-16.json)保留13／14／15與source17原bytes，並以[15題reconciliation exact archive](history/opening-teaser-plan-reconciliation-15-20261026.json)接續前輪來源鏈。Dora原operator空表README／prep的exact SHA吻合freeze後，才更新current文字說明及completion；原prepared entry／brief／source／native／freeze不改。當前hold變更前亦另存[15題exact快照](history/production-hold-before-sixteen-text-20261026.json)。

SOURCE17提交的[倉庫封裝收據](source-progress-repository-packaging-20261026.json)仍屬該已發布snapshot：一份primary MP3保留local、未commit，Dora history/r5/script.md的一條author-freeze-bound EOF空行例外保留。其7372 JSON／8970 text／582 files不是本輪16題尚未stage的驗證數字。Rolling R8 SOURCE PASS與fresh native7盲讀仍未published，當前只綁history/r7/native6 HOLD；不能提前計入18。
