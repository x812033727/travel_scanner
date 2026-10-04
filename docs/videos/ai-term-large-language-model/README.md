# 大型語言模型：文字包交接

長片交付日：2026-10-05。繁體中文長片長 14 分 3.1 秒，正文 13 分 55.1 秒、實際口播 11 分 48.1 秒；成片 11 項品管與上架包 4 項檢查全過，獨立成片／字幕審查完成。正常 final 與 publish 流程均已核准、讀回，後台五個附件的完整 SHA-256 與大小逐一相符。站主只選繁體中文，字幕與文字只有 zh-TW，沒有新增配音。G 槽備份、1,250 檔完整還原與雲端同步驗證均已通過；兩支 Shorts 尚未完成並共用素材，全部本機媒體保留，刪除零檔。YouTube ID 仍為空，未上傳或發布。

目前成片 SHA-256：`aec91b1ffb5d5e18a8348432bbc9ab7cd4bad98459d3349b4c5e24cde850685b`，363,549,695 bytes；上架 metadata SHA-256：`0420dd643a2f855d97682f90032098b7bfe93ba074285e90a1d113fb78b28797`。final 核准時間為 2026-10-04T17:12:39.581633Z，publish 為 17:18:41.446916Z，正常 publish-pull 於 17:24:53.9557909Z 完成。五個後台附件為成片、metadata、縮圖、繁中說明與繁中 CC；UPLOAD.md 留作本機操作說明。後台的「on YouTube」與 CLI 的「owner confirmed the upload」是既有概括文字，不能當成實際上傳或站主接受的證據。

以下保留作者階段及逐次續跑歷史；以以上交付狀態和私人 RUN 最後 checkpoint 為準。67 張分鏡的 60 條原始 judge 警告、失敗圖及重畫收據均保留，沒有刪問題取得核准。

備份批次為 `20261004T172900751Z-llm-d6e2ea2352cb43b6954f38d46dcf182f`，位於 `G:/我的雲端硬碟/Backup/Mokaair/ai-series-continuation-20261004/`。兩個內容尋址分卷保存目前完整工作目錄的 1,250 檔、2,411,346,068 bytes；安全路徑、逐檔 SHA-256、完整 ZIP 驗證及實際還原通過。第一次還原目錄造成 291 字元長路徑而失敗，原收據與部分還原保留；改用新的短目錄、最長 219 字元後才完整成功，沒有改原件、分卷或系統設定。原 11 個封存／支援檔及另存的四個驗證／零刪除收據均完成 DriveFS cloudID、MD5、大小、operations=0 的兩次穩定核對；這是 G 回讀與同步 metadata 證據，未宣稱獨立雲端下載 SHA。兩支 Shorts 的七張共用圖及保守保留條件仍存在，未執行 deletion-plan 或 tidy。

- `brief.md`：三個可比較大綱；選項 A 已由 `review-push --gate outline` 送審，`review-pull` 讀回自動核准。站主立場 4、6、7 依當日設定抄入。
- `build.mjs`、`line-ids.txt`：本次作者的旁白、場景與素材來源。執行 `node docs/videos/ai-term-large-language-model/build.mjs` 只重建本資料夾的 `video.json` 與估算 `draft-metrics.json`；不買素材、不跑合成、不送審。後續若修 `video.json`，也要同步作者來源，避免重建退回舊稿。句子 id 來自影片 CLI，插句時新增，不能重編既有 id。
- `video.json`：冷開場約 11 秒、七個內容章，108 場景、67 張原創插圖提示、138 句、2,930 口播單位。目標 10 分鐘；估 13.84 分不是成片。正文與成片各至少 8 分鐘，實測達標後才算。
- `claims.md`：36 項作者主張及來源／示意界線；`verify-1.md` 已獨立全讀長片、場景、metadata、示範及兩支 Shorts，三項範圍修正均已套用，沒有未解決事實。
- `demo.py`、`demo-log.md`：六筆純虛構失物資料，無網路或模型呼叫；位置有據、失主電話未知、依條件數出全部六／未領四／未領雨傘兩。可離線重跑。
- `shorts.json`：兩支切片文字與重用圖；第二支的六筆開場使用正常文字卡、兩把雨傘使用附完整 SHA-256 的既有全圖卡，避免中央直式裁切切掉手柄。口播未改、schema 通過；已實看全圖卡的雙柄及雙手，實際播放、25–55 秒與 QA 仍須在正常流程量測。沒有長片公開網址，不能填虛構連結。

最初作者驗證的估算與歷史凍結保留於獨立審查附錄。最新來源 lint 零錯誤、一個警告，把 37/73 張提示的「central」構圖指令當重複場景；七個內容場景地點仍不同。demo 三種結果與斷言通過，兩支 Shorts schema 無問題。來源與靜態版面檢查不代表實際成片 QA。

作者階段沒有新增或修改共享名詞庫、字典、正式站設定與其他影片資料夾，也沒有付費服務呼叫。後續產線已送審大綱並開始實際 TTS；沒有上傳或發布。音樂／音效未指派。原創資料與結果已寫進說明本文，沒有依賴尚未合併的 GitHub URL。

九卡修正前的產線記錄：video SHA-256 為 `9f25b680fe634f7023f88e3f91fd50ceabd29d687592ef2ff1be35312d7a957c`，brief SHA-256 為 `b23f074132fe526115f9908c49d430881f028272b0b064375d64376c3f7c8ca9`。大綱核准讀回時間 `2026-10-04T10:50:23.673Z`。兩處實測句尾停頓先以零重錄修好；後續轉寫核對排除 14 個誤認，只局部重錄四句，最後將一處含糊措辭改成「清單沒寫物品主人」。數字、王先生、事實、聲音及 138 個句子代號均保留；獨立附錄與 `review/rewrites.json` 留有記錄。

後續實看修正 26 張圖片提示並完整保留原件；三鏡小樣產生五張圖，程序 exit 0 但只有 52/75 張，且高分仍有真實錯誤，不能視為完整成功。六件圖缺少兩把傘、木杓交接變成木碗和攪棒，因此改為既有六筆明細與要求／執行／回傳正式卡。原六筆逐列卡改成前三句各揭示一對、後三句揭示原有條件與資料限制；六個實際渲染狀態均實看，與原句一致、無溢出。第一版雙行表曾高出 53px，失敗及原件保留；單行分隔版本才通過。花園三籃全幅可辨，兩人變一人等原判決及直式裁切限制仍保留。其他重畫需再次實看，未修改任何 judge.problems。現有全部 73 鏡的場景＋Style＋Camera＋Avoid 完整長度最多 1,381 字元，低於服務的 1,500 上限，沒有截斷；模型與預算未變。

九卡修正前真實口播 708.1 秒、正文時間軸 835.1 秒，八章均過；改卡後實測插圖佔比 54.60%、最長畫面八秒、平均約六秒，無節奏問題。138/138 句通過當前檢查、零旗標；每個 WAV 的完整雜湊及 PCM 都由另一位代理獨立核對。正常 `tts --refresh-evidence` 以零合成、零計費、108 次快取復用更新兩景模板資料，音檔完全未變。音訊重新依設定自動核准，讀回時間 `2026-10-04T13:44:44.344Z`，綁最新 timeline SHA-256 `086c5b2c46fb0cc306896d22b708ea31cbf4741a7097601338ec523148306a83`；後台 GET 確認同一雜湊。這不是站主實聽或成片完成；插圖仍需分鏡關卡，成片另需 QA。媒體、逐關證據及續跑說明在私有 `<home>/mokaair-work/ai-series-continuation-20261004/RUN.md`；完成後先驗 G 槽備份再清理，缺少本機媒體時先查封存收據，不直接重買。

最新續跑：23 張重畫已於 2026-10-04T14:06:10.353Z 結束，exit 1，本輪 36 張新圖、累計 US$2.187；獨立逐張實看仍有七個真實錯誤，未把 passed:true 當成像素核准。四景 pottery-brief、pottery-limit、demo-one-umbrella、kitchen-repeat 改為有據字卡／真離線輸出；另五卡修正當句不可見的資料與三欄呈現。九卡共 16 個狀態均有獨立語義核對，四新卡與前五卡共 16 張 normal-renderer PNG 已實看且無溢出。原件、所有 takes、judge.problems 與失敗版均保留。

當前來源為 `eafefe5847d332e4b1566a81a9a1e6c24463c037c75297364781df281187eb6c`，69 shots；九卡來源 1ad01d 的窄審與最新三 prompt 的獨立審核均通過。其餘 66 個 shot 完整不變；138 句／IDs／停頓／reveal、108 TTS requests／138 keys、voice/look 均不變。插圖實測仍佔 51.6625%，正文 835.1 秒、口播 708.1 秒、最長八秒、平均六秒，沒有增停頓補時。正常 refresh 仍零合成／零計費／108 次復用，timeline 只改八個模板欄位，新 SHA `4e1864fba7fabae05367977ca0d38b784757d26b533e3743dbe96e348b3c8925`；audio 自動核准於 14:23:50.220422Z，正常讀回 14:24:18.798Z 及後台 GET 同 SHA。138 實檔 WAV／PCM／check 未變、零旗標；這不是站主實聽。

三景 demo-cap-out、kitchen-agree、garden-follow-up 分別去除瓶蓋誤認、背景假字及兩籃代三籃。完整 MiniMax payload 為 1,353／1,301／1,336 字元，全部 69 鏡最多 1,381，沒有截斷。正常小樣收據 `llm-three-failure-pilot-2030.log`／exit JSON 在私人續跑目錄；新圖及 Short 實際裁切仍須核對，不能把小樣 exit 0 當成完整成功。PR 1207 因其他程序再次開啟自動合併，已關閉並設回草稿／no-auto-merge，以遵守本輪禁止合併。Embedding 的下一集文字另存 draft PR 1211，20 項 exact-head CI 通過；尚未購買它的 TTS／圖。沒有新完成成片、G 備份批次或本機媒體刪除。

最新23:10交接：長片 `2a9bfa4e99d17d1805891f70c56e78416101bc94255c330e96ee62555e14408a`，67shots；Shorts `b70535ce3c920a88c451cbc589ed63f9a9e16168a9c15d9806828fb8915a06a0`，全部20句未改。三鏡小樣終止exit1，新六圖USD0.081，帽圖仍多瓶／花園仍兩籃，原件和判決保留；最後兩景已改真實已領資料表與三欄核對卡。實測插圖50.1577%／body835.1秒／voice708.1秒／138states／8秒最長，沒有加停頓或降低門檻。正常0synthrefresh的新audio timeline `3b57a6f54b78cd5267c6a6b2898bd87e5650121a7da8dbceb78d81f03b6f7e02` 自動核准並exact讀回，138實際PCM／check未變。正常67圖整理0新生成、全部原判不變，累計USD2.268。

當前67分鏡manifest `b008c55cf9bf913d010870c66ae5cfe06db0d823a34cf09bf9f52066bfe50c31` 已交付三張完整contact sheets。最初15:03:01Z讀回為 **pending**；後台於15:03:33.257946Z作出 **approved** 決定，15:23:41Z的GET核對同一雜湊，正常`review-pull --gate storyboard`於15:25:55.071Z記錄本機核准。51圖的60條原警告仍完整保留，沒有刪問題或代批准；實際review決定才是依據。Short1首束傘／三籃與Short2雙傘改為有完整SHA證據的contained assets，真實兩個isolated ffmpeg首格與標準字幕都已實看；原圖人物／束帶警告保留，完整Short媒體及播放仍待。

本機fullfilm render及一次性的後續assemble/captions/QA/package只製作可看片待審包，收據 `llm-review-draft-*-2030` 与 `llm-review-draft-continuation-2030.json` 在私人RUN目錄。它不送final/publish、不上傳發布或清媒體；使用者取消／episode STOP／source改動會停下。後續heartbeat先核目前process與terminal收據，不能重開同slug。PR1207維持draft/no-auto-merge；Embedding下一集source另在draftPR1211、20項CI通過，未購素材。尚無完成交付＋已選語言的合格G清理項，全部媒體與shared assets保留。

23:30續跑：正常render於15:17:48.512655Z結束exit0，71個正式卡片狀態及完整frames manifest已落地；正常assemble仍在執行，沒有重開同slug。後台語言欄仍為`locales:{}`、`locales_decided_at:null`，已逐欄真實同步本機mirror，保留null：只先做必要繁中基底，沒有宣稱站主已選「只出繁中」，沒有新增翻譯／配音。成片QA及正常final核准必須先於package；package若因缺final核准exit3，是正常關卡等待。兩支Shorts正常`from-episode --check`通過，但20句與長片沒有逐字相同的錄音，不假冒既有音訊或Windows聲音。所有成片與語言交付條件完成前，仍保留原媒體。

23:45最新狀態：使用者已直接選擇本集「只出繁體中文」。瀏覽器工具初始化失敗後，透過既有主機的正常`admin_service.set_locales`與管理員驗證／`video_locales_set`稽核，只記錄本集空的附加語言選擇；後台決定時間`2026-10-04T15:36:31.277219Z`，15:37:05Z的GET與本機mirror一致。現在必要字幕與metadata只有zh-TW，沒有配音／翻譯或需送審的語言批次；不是代人核准其他關卡。獨立正常render實看完成41張卡的71狀態，108場／138句揭項相符，804正式图片檔完整，71版面／72字型檢查零錯，原51圖警告及三個Short共用圖不變。完整成片與字幕同步仍待正常合成和QA；沒有G封存或刪媒體。
