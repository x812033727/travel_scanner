---
id: 2026-10-25-produce-video-duckdb-agent-full-export
title: 製作 DuckDB 2.0 agent 模式完整跟進清單影片
status: in-progress
priority: P1
area: docs
owner: codex-duckdb-20261025
claimed_at: 2026-10-25T23:13:03Z
created_at: 2026-10-25T23:13:01Z
completed_at:
branch: codex/ai-tech-duckdb-20261025
depends_on: []
scope:
  - docs/videos/duckdb-agent-full-export
---

# 製作 DuckDB 2.0 agent 模式完整跟進清單影片

## Why

觀眾容易把表格列印預覽當成完整交付。以DuckDB 2.0的新agent輸出為近期入口，跟同一份原創1,200筆配送CSV寫完整條件、交出480筆嚴格晚到名單，並以改需求為`>=`的720筆實跑對照說清預覽、條件與全檔驗收。CSV／SQL／COPY／Parquet為既有能力，不把CLI印法當AI模型、效能或查詢正確性保證。

## Definition of done

- [x] 獨立worktree、精確scope、來源與資料包、正常後臺研究登記可讀回；查重覆蓋本機／遠端／PR／main及後臺分頁。
- [x] 正式brief／Jev原始實評、正常pending outline與有依據的委派local adopt綁同一SHA，未偽稱遠端或使用者UI點擊。
- [x] 同一案例六章正式稿、claims與資料／條件一致，原生事實／敘事／聽眾結果如實交付；兩讀者12/13 false與root採用取捨完整保留，不稱native narrative PASS。
- [ ] 繁中當前音檔／卡片／成片QA與至少480秒正文完成；en、ja、ko、es、pt、id、vi、th各metadata、CC與M4A實際交付後臺並讀回。

## Steps

- [x] 查四個既有worktrees、五個local branches、231 remote heads、30 open PR全文、open／done任務、base及origin/main。
- [x] 後臺先辨識200上限，再正常`limit,before`三頁查完423項；無同題。
- [x] 由明確授權DNS `6354ed3` 建立`codex/ai-tech-duckdb-20261025`，claim本episode；記錄與main分岔，不自行merge。
- [x] 正確保存第五題研究／企劃來源與小型資料、SQL、原始RUN輸出及授權；不搬大型CLI、壓縮包、外站全文或PDF。
- [x] 獨立標準函式庫核對全部480筆及改需求720筆；原480檔不覆寫；可攜路徑SQL明示未重跑。
- [x] 後臺正常PUT／GET研究登記：`duckdb-agent-full-export`、slides、ai-news；原生brief／stance／A/B/C解析檢查無問題。
- [x] 正常Jev outline分析、保存raw回覆與分數／失敗原因，送正常hand-pushed pending review後做委派local adopt。
- [x] 接收六章scratch並導入ca1e／64景111句；verify3當前21項CONFIRMED、視覺修正與完整raw/native歷史保存。
- [x] 根層verify-1/2/3精確copy供native facts；正常script pending、native本地採用與TTS dry-run實際收據落地。
- [x] EN、JA、KO與ES各111句targets／六章／metadata／縮圖詞經作者三輪、root獨立全量語義審查後正常i18n-merge；目前為文字4/8，沒有actual CC／M4A／後台交付。
- [ ] root解除provider hold後才啟動bounded付費TTS及當前音訊驗收；其後完整render／QA與八語交付。
- [x] 首commit／push／PR1861後root實際GET公開CSV／42-entry ZIP，各200且完整bytes／SHA相同；資料夾HTML未另GET。

## How to verify

`node tools/tasks.mjs check`；原生`checkBrief`、`stanceProblems`及`outlineOptions`純函式核對；data manifest逐檔SHA／size、完整CSV獨立predicate、全部本地Markdown／HTML交付連結；正常VideoTool GET讀回slug、stage及outline內容SHA／review status。後續音檢只採最新clip/hash的實際收據，文字估時不算音長驗收。

## Notes

Owner為`codex-duckdb-20261025`，同一協調代理團隊持續製作；目前仍in-progress，不能將「研究／登記完成」當整片done。採A依站主2026-10-25持續委派；不需要再問例行選題。正式docs見`docs/videos/duckdb-agent-full-export/production-start.md`。

Backend：`https://mokaair.com/admin/videos/duckdb-agent-full-export`；2026-10-25T23:22:43Z已GET讀回research，沒有伺服器outline／script核准。root後續明確授權正常Jev分析費用及local委派採用；TTS／其他media仍未授權本分工啟動。絕不建`auto.json`。

23:31:57Z正常Jev choice A／passed，P(A)=1.00、stance=.88、demo=.95、advice=.02；raw答覆未改。正常outline送審GET回讀pending `ebe65265-7f4d-4372-94ab-eaf0ade2b799`、stage outline。23:34:24Z原生local approve採A，brief SHA `08b1efe36fee8260b1837de9a4793921fe610ab0b498939102d1980a5240347b`；note明記本地委派、非remote/UI核准。Jev note提到auto核准，但真實hand-pushed review仍pending，不能混成一個事件。

Base `6354ed3ebcc82c1baefe57bcd1f8d436f183581a`與查核時`origin/main 76cc8aa1a3385f4176af3d7e588025d3ef6c8e15`分岔；新episode scope在兩邊均無歷史，沒有聲稱目前branch就是最新main。shared lexicon由其他三片持有，本task刻意不涵蓋。

原研究有一項命令敘述校正：舊license review／早期文字的`-init /dev/null`與十份真實argv不一致，正式採實際`-no-init`日誌；該舊receipt不搬入小型包。原始二進位、archive、資料與runlogs未重跑或修改。

root指定當前方案為六章（outro歸第六）。2026-10-26當前ca1e原生估時總628.2秒、保守扣開場／outro583.9秒，仍是計畫，不是媒體PASS；原七章／24秒與較早637.37秒估值保留於歷史，不作目前音長驗收。

歷史source導入分工當時不commit、push、開PR、merge或deploy；後續授權前維持本地工作與正常後臺研究／pending審核紀錄。原始碰撞大JSON及配對憑證不放進公開episode資料。

## 歷史ca1e source gates與paid TTS hold（metadata追加前）

當前source SHA `ca1ef60f4e9fd98f7c2e336a7fc8ab339c58b94f557ba0a7f6b8fb7cc279e1bf`、claims `cc38eeb8634eaa45c2a46c981bb1f7b0c9fca034158647437c1de0de8fd79191`、speechHash `38cf9292f6945199`。64state＋thumb native static0layout，root已實看全部64contacts／修卡／final thumb；獨立verify3的兩個fresh in-memory capture逐bytes等於frozen bitmap。111 full line objects／say／voice／SQL未改。

R2 reader5／6各12/13且passed=false，分別no_recap／no_detour；root明確接受必要輸入與減法、新聞版本脈絡兩項教學取捨。未改raw/native failed/problems或門檻，也沒有新fresh score。verify1原REVISE、verify2歷史7d PASS、verify3當前視覺delta PASS均完整保留；根層verify-1/2/3精確copy供nativefacts。

正常script review `dd47b9a0-6456-4651-9456-32b320909338` GET讀回pending，content_sha256綁生成的script.md `7aac2017419c82a4b81fb40050f067c9e021312600e5d66ec70846b58946107b`，不是video.json。Native本地script採用實際01:48:28.930Z，只是本地委派採用，非remote／UI批准。Raw server project_stage雖顯示narration synthesized，本地沒有已合成音訊證據。TTS dry-run111requests／111pending／2508估計字元，Gemini Sulafat；configuration ready與月餘6244644不是provider availability或帳單。

root依第四initial93/118 raws、一次resume仍settled busy，以及ForTy PT R1已知HTTP429／0新音訊，決定第五暫不啟動新paid TTS。本片目前TTS0／raw0，沒有M4A、全片QA或八語完成；不換provider／voice／全局設定，不查帳單或清journal。只完成source gates與dryrun準備。整片票仍in-progress，不done／release。

正式進度、目前收據、相對教材與公開URL待驗界線見docs/videos/duckdb-agent-full-export/result.md及receipts/index.json；新文件freeze另列，不覆寫原266檔historical manifest。本docs分工不commit、push、PR或backend操作，由root後續commit。

## root verify4當前metadata綁定與公開教材（2026-10-26T03:46:05.649960+00:00）

Root明確委派/root/formal_docs_commit沿用本票codex-duckdb-20261025 claim完成文件／收據及同分支scoped commit／push，沒有接管paid或媒體producer。首push410633ab與PR1861 draft／no-auto-merge已建立；root於02:39公開GET CSV／ZIP 200及SHA proof已落地，原資料與9條RUN命令不變。

當前40eb僅description追加兩個真實immutable URL；root獨立verify4 MD c1b7af46f33dbc6fdd3a36ca562c5531bbdfb53d4dcd2f5a25dbffabd6ac4080、JSON292e77789e9c79a4fd851daf96d574bdb953045c5ff01319c21edaca91bd7afa PASS。完整111line／64scene／claims／voice／speech38cf及生成script7aac全不變，21項為固定依賴連續性CONFIRMED，未冒稱新live全來源或fresh敘事。既有normal script pending／01:48本地採用仍綁7aac，沒有新server/UI/local核准。

首次verify4 invocation用錯estimateTimeline參數、在reports寫出前失敗；修正rerun才產生真實PASS，診斷另記，沒有製造raw stderr。prepared17檔與原freeze逐bytes封存，舊68reviews不動；當前progress／新source-gates／index／validation／freeze各記範圍。paid TTS0、R2兩讀者12/13 false、八語及overall仍未完成；官方5/21 v4素材已取得但第五尚未採用。不merge／deploy／YouTube上傳。


## EN文字本地採用（媒體仍0）

Root明確委派本docs分工採既有claim更新EN文字狀態。作者完整111source→English mapping與三輪檢查後，root獨立讀全111＋metadata，僅修標題明示complete follow-up list及第一句preview omits rows，111targets不變。正常i18n-merge真exit0，現i18n/en.json等於root nativepurepreview，六章／title／description／tags／縮圖詞current；EN文字1/8，actual CC／M4A／fit／meter／ASR／backend EN均未完成，繁中paid TTS0／raw0／actual timeline無。

Source40eb／claimscc38／speech38cf／script7aac／voice／lexicon／data與verify4／R2兩份12/13 false不改。329舊檔在docs變更前全hash相同；舊progress／README／result／receiptREADME／task／index與6eb等freeze先逐bytes封存。作者原26freeze、111mapping、首次native pass3的sheetTodo字串期望錯誤、兩項root metadata delta與真merge log均保留，不以文字或估時冒稱配音fit／音檢。此分工不改英文targets、不付費或寫後台；只在root獨立freeze審查PASS後精確stage／commit／push同branch，PR no-auto-merge，不merge/deploy/YT上傳，也不開topic6。


## JA文字本地採用與文件準備

Root另委派/root/formal_branded_main_peer為本輪唯一文件編輯，沿用既有claim／branch75d0，不接管任何paid／媒體producer。日文作者111句／六章／metadata完整三輪後，root獨立讀全部source→target與metadata PASS_TEXT_ONLY，未改任何target。正常CLI i18n-merge真exit0，actual i18n/ja.json SHA324c6f070993c1fc1b08f18d5f9131527eb24278e8ff4f200dfb63c6db4b83f2等於native pure preview；目前EN＋JA文字2/8，actual CC／配音／fit／meter／ASR／後台JA仍0，繁中master TTS0／raw0／actual timeline無。

完整作者21freeze＋root獨審／merge／初次validator錯誤收據已安全複本保存於localization/ja。作者URL分割假設、root sheetTodo型別與freeze.files結構假設三個錯誤各自保存原腳本／真工具診斷，均非音訊或native品質失敗，沒有改輸入或門檻來過。48／44字的文字建議提示保留，無max_chars或實際fit結論。

修改可變文件前，原325證據及EN35freeze／Git blobs全核相同，舊35份文件、freeze、進度／README／result／task／index已逐bytes封存。Source40eb／claimscc38／speech38cf／script7aac／111 source line objects／voice／lexicon／data及兩份敘事12/13 false全不改，EN／JA target不重寫。本分工只準備文件、檢查及freeze，未stage／commit／push；須root獨立review後才另行授權精確scoped commit／pushPR1861，保持no-auto-merge，不合併／部署／YouTube上傳、不開topic6。


## KO文字正常採用與增量文件準備

Root指定/root/branding_restore沿既有claim為本輪唯一FIFTH文件編輯。Root已全量獨立讀111組KO／六章／fullmetadata，僅修jd24、g738與description兩處白話用詞；109句及所有source/context不變。正常i18n-merge真exit0，actual KO6b1e等於root修文後nativepurepreview，不等同作者舊df020 preview。這是音訊前文字修訂，不重設native shorten／reword／retake回合。

現為EN＋JA＋KO文字3/8，master paid TTS0／raw0／actual timeline無；全部actual CC／M4A／fit／meter／ASR／後台交付仍0。作者21freeze＋root審查／delta／preview／merge／log安全複本保留；只封存五份實際可變docs/task及三份前輪描述檔，83舊JA檔與31／61／90／171索引原位核對，以Git0d885及重建identity復原全部舊88，沒有遞迴再複製history。

Source40eb／claimscc38／speech38cf／script7aac／voice／lexicon／data／ENJA與兩份敘事12/13 false固定。作者13保護輸入加root已採用KO共14檔核對，不改任何targets。只準備新KO index／驗證與精確freeze／path proposal；未stage／commit／push，須root獨立審查後另行授權，不開topic6或啟paid/media/API。


## ES文字正常採用與增量文件準備

Root指定/root/branding_restore沿既有claim為本輪唯一FIFTH文件編輯。Root全量讀111組ES／六章／fullmetadata，僅修jd24明示符合條件的完整跟進母體、description說清未量測token使用量與成本；其他110句與所有source/context不變。正常i18n-merge session69401真exit0，actual ES2e8511等於root修文後nativepurepreview，不等同作者舊preview。這是音訊前文字修訂，不重設native shorten／reword／retake回合。

現為EN＋JA＋KO＋ES文字4/8，master paid TTS0／raw0／actual timeline無；全部actual CC／M4A／fit／meter／ASR／後台交付仍0。作者31freeze＋root六份收據安全複本保留；只封存五份實際可變docs/task及三份前輪KO描述檔，50舊KO檔與221及更早索引原位核對，以Git be172及重建identity復原全部舊55，沒有遞迴再複製history。

Source40eb／claimscc38／speech38cf／script7aac／Sulafat voice／lexicon／data／ENJA KO ES與兩份敘事12/13 false固定；15保護輸入全SHA核對，不改任何targets。原生估時／字數建議不是配音fit，dry-run估計不是發票。只準備新ES index／驗證與精確freeze／path proposal，未stage／commit／push；須root獨立審查後另行授權，不開topic6或啟paid/media/auth/API。

ES native lint真exit0，保留37.5／36手機標題寬度建議（0 errors、1 warning）；初次docs checker誤期望0 warnings的exit1及原腳本／log另存，不改譯文／native門檻。
