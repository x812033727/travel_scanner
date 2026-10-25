# 後台品牌故事：10/25 新規則重製交接

本批依站主「繼續完成後台未完成影片、用新規則重製，參考 [PR #1844](https://github.com/x812033727/travel_scanner/pull/1844)」的指示建立，原始碼基準為 `2b20c30d3`。目前完成的是新稿與審核準備，**尚未產生本批音訊、插圖、配樂或成片，沒有送出付費請求，也沒有成片核准**。

站主追加「從 C03 開始重製」後，當前製作順序改為 **C03 Moleskine 優先**，再按既有集數接續（見 [execution-order.json](execution-order.json)）。C03 舊版上架包正文約 8 分鐘且未燒字幕；[C03 r3新規則稿](c03/README.md)已通過來源與雙讀者合併、企劃／劇本均已核准並匯入；已完成的 C04／C05／C09 新稿及審核紀錄保留。舊 C03 付費素材位於另一台 Windows 工作機，本環境未取得原件；[現有證據](c03/existing-evidence/media-inventory.json)記下可用性與歷史收據差別，依站主後續「如果不行你就重新來吧」指示，新版改按從零製作預檢，舊素材取回不再是前置條件；原件及既有支出仍保留，不宣稱已沿用。

## 範圍與目前狀態

[盤點快照](batch.json)記錄 22 筆後台品牌故事，其中 19 筆沒有 YouTube ID 且未放棄，合計 18 個題目。龜甲萬原版與 `short-v8` 是同題兩版，兩筆舊紀錄均保留；不得當成兩個新題目重複製作。[原稿保全檢查](original-preservation.json)確認所引用的 53 份舊來源檔雜湊全數未變；這不是舊媒體驗收。

先前首批完成 C04、C05、C09 的新稿，現依追加指示先推進 C03；目前共四題已備新稿。其餘14題仍在原始[佇列快照](queue.csv)，執行狀態以 [execution-order.json](execution-order.json) 為準：Zippo、龜甲萬、Seven Bank、哆啦A夢、FriXion、CamelBak、UCC、OXO、Dr. Martens、Play-Doh、Seiko、Garmin、Dyson、輪子行李箱。

| 第一批 | 精確稿件的獨立審查 | 本機檢查 | 後台審稿卡 |
| --- | --- | --- | --- |
| [C03 Moleskine](c03/README.md) | [來源／書面配鏡 PASS](c03/reviews/source-r3-delta.json)；[雙讀者合併 PASS](c03/reviews/narrative-final.json) | [lint](c03/lint-final.json)：0 errors、31 warnings | [企劃與劇本核准已匯入](c03/backend-status.json)；[正式入場交接](c03/production-entry.md) |
| [C04 泡泡紙](c04/script.md) | [來源／書面配鏡 PASS](c04/reviews/source-r2-delta.json)；[兩位隔離讀者合併 PASS](c04/reviews/narrative-final.json) | [lint](c04/lint-final.json)：0 errors、6 個估計鏡頭時長警告 | [劇本核准已讀回並匯入](c04/backend-status.json)，review ID `4b59f286-1467-4548-b0da-95b5462f682f` |
| [C05 金鳥蚊香](c05/script.md) | [來源／書面配鏡 PASS](c05/reviews/source-r6-delta.json)；[兩位隔離讀者合併 PASS](c05/reviews/narrative-final.json) | [lint](c05/lint-final.json)：0 errors、0 warnings | [劇本核准已讀回並匯入](c05/backend-status.json)，review ID `398b6b93-0ce6-439a-925e-8ff72a1bc5fd` |
| [C09 Patagonia](c09/script.md) | [來源／書面配鏡 PASS](c09/reviews/source-r12-delta.json)；[兩位隔離讀者合併 PASS](c09/reviews/narrative-final.json) | [lint](c09/lint-final.json)：0 errors、18 warnings | [已核准並匯入](c09/backend-status.json)，review ID `5c822c92-3bb6-437e-8b8a-157737a71543` |

四支的來源／敘事 PASS 僅限收據綁定的文字與書面配鏡。C03、C04、C05、C09 的正式劇本核准已讀回並以官方 `review-pull` 匯入；C03企劃亦已核准。原始送審時的 pending 收據保留。均未通過成片關卡。兩位讀者依原生合併規則判定：必要題只在兩位都答 no 時失敗；各自答案、保留意見及歷史 HOLD 都保留。C09 一位讀者仍對公平質疑的回收有保留，兩位均提醒 079「同年」跨段距離較長，保留在審查紀錄，不改寫成一致同意。最新機器狀態見 [status.json](status.json)。

## 本批採用的規格

- 目標 13 分鐘，**實際旁白正文須量得 12–14 分鐘**；片頭片尾不補正文，字數、文字時間線及 dry-run 均不算量測。
- 開場依序為觀眾利害與有來源的數字、具體場景、至多兩個預告、點名題目與規模的承諾、全片問題；每章對觀眾說話並有旁白反應，正文每 30–45 秒有實質鉤子，至少 8 組有回收的伏筆。
- `kind: story`、`format: drama`；MiniMax `image-01`，`look` 僅為 `{"preset":"cute-mystery"}`。內容相關插畫占正文至少 70%，兩張插畫之間至多 3 張必要字卡；匿名示意人物與無商標物件，不把插畫當史料重建。
- 台灣口音說書旁白，目標約每秒 4.5 字；繁中燒錄字幕並保留 CC，其他語言仍做 CC，配音另依逐片選擇。
- 5 秒正式頻道片頭放在濃縮開場後，21 秒 v4 片尾；片尾不預告下一集。bold 縮圖採 layout d，滿版主體、黃字黑邊主標與白字副標，主標選最有利害的約 6 字、副標至多 12 字。

以上依[10/25 決定](../channel-review-20261025-story-series/README.md)、[品牌故事流程](../../../.agents/skills/brand-story/SKILL.md)與 #1844 執行，不沿用舊版 10 分鐘／不燒字幕設定。

## 製片入場仍被擋住

[準備檢查](readiness.json)記錄的 C 系列付費保護仍有效：這四個精確 remake slug 尚無已啟用、可派送的全片預算帳戶。既有單集 US$25 核准、來源 PASS 或建立新帳戶，均不能自行解除 hold；須先核對歷史費用、未結算請求、實際供應商價格及餘額，再完成符合現有硬停線的帳戶與啟用流程。不得換成其他 slug 前綴繞過保護。

目前可用的影片工具權杖可讀進度、建立新的 pending 劇本卡；可操作的管理員／正式主機連線仍未接通，無法據此執行原集重綁、drop／redo、設定啟用或取得正式工人素材。新卡沒有綁回原 episode，也沒有建立 `auto.json` 或自動續跑。

可讀到的一組 5 秒／21 秒品牌素材只標為候選，**尚未證明是站主選定的正式 v4**。檔案存在、雜湊與秒數相符，不等於畫面、聲音及身分已驗收；正式組片前仍須取得並核對正確素材。

[C04 關鍵影格 dry-run](c04/keyframes-dry-run.txt)為 92 張圖，單次約 US$1.24、每景最多 3 次約 US$3.73；[C05](c05/keyframes-dry-run.txt)為 94 張圖，單次約 US$1.27、最多 3 次約 US$3.81。這些是當時的**圖像階段估價**，不是包含文字、TTS、轉寫、Jev、配樂、重試與歷史費用的全片報價；工具顯示的 US$200 是站點泛上限，不是本批授權。[C09](c09/keyframes-dry-run.txt)為 92 張圖、最多 3 次約 US$3.73。三份 TTS dry-run 只證明可讀取句數與供應商設定，沒有合成音訊或測得時長。配樂 dry-run 因缺少真實 TTS timeline 正常停下，未造時間線換取估價；精確輸入與日誌雜湊見各集 `preflight-inputs.json`。

## 原始稿、審稿卡與隔離執行目錄

各集的 `video.json` 是機器稿來源；作者 `script.md` 與 `claims.md` 保留逐句來源及編輯背景。官方 `writeScreenplay` 會從機器稿另外產生執行目錄的 `script.md`，後台實際收到的文字快照存為各集 `backend-script.md`，其雜湊由 `backend-script-receipt.json` 綁定。不要把作者稿與後台投影的雜湊混用，也不要以產生劇本為由覆寫作者審查原件。

[prepare-runtime.mjs](prepare-runtime.mjs)可將指定候選複製到倉庫外的獨立執行根目錄，依正常流程初始化不可變發音字典，再產生官方劇本；它不呼叫模型、不建立核准、不複製原集 `auto.json`。產生的媒體另放在執行根目錄之外；遇到既有產物須先核對，不能當成全新專案覆寫。

三份候選凍結後，設定兩個位於倉庫外的絕對路徑，可用同一份官方 CLI 做精確檢查：

```sh
node docs/videos/brand-story-remakes-20261025/prepare-runtime.mjs "$REMAKE_RUNTIME_ROOT" "$REMAKE_MEDIA_BASE"
node docs/videos/brand-story-remakes-20261025/runtime-cli.mjs "$REMAKE_RUNTIME_ROOT" lint --slug story-everyday-bubble-wrap-c04-remake-20261025
```

[runtime-cli.mjs](runtime-cli.mjs)只把明列指令交給既有 CLI；它不解除付費保護，也不代替站主關卡。四支已有上表的新卡，後續先讀回同一筆 review ID／內容雜湊，避免重送或覆蓋。四份劇本均已匯入正式決定；不要再用準備程式覆寫已核准的執行目錄，程式遇到 `approvals.json` 會要求先核對。

接續順序為：凍結精確稿件與新審核 → 正式入場及全片報價核對 → TTS 實測與逐句聽檢 → 插圖及分鏡驗收 → 正式片頭片尾、配樂、組片、燒錄字幕與 CC → 完整解碼、QA、站主看片及上傳包。來源快取 `source-snapshots/` 由 `.gitignore` 排除；交接保留來源 URL、雜湊與獨立收據，不把原廠全文快取當交付內容。

目前任務仍未完成；尚無本批媒體 QA、實際時長、站主看片、上傳或發布成果。

## 本次驗證

`npm run test:docs-videos`：236 passed、0 failed、0 skipped；文件測試收集契約另 2 passed。任務檢查通過 2178 份（既有其他任務的 stale／overlap 警告保留），兩個交接 helper 通過語法檢查。四份精確稿 lint 均 0 errors；估計鏡頭時長、長句與用字警告仍依各集日誌保留，須在真實 TTS／圖像階段處理。

C03 從零製作採獨立runtime，明確選集以避免碰到既有核准：`node docs/videos/brand-story-remakes-20261025/prepare-runtime.mjs "$C03_RUNTIME_ROOT" "$C03_MEDIA_BASE" c03`。原生獨立查核檔若存在會核對video SHA後複製，仍不建立owner核准；有既有approval或媒體時會停下要求核對。

## 後續採用的八語設定

依站主「用推薦、不用問、預設八語」接續各集；本次C03也已從後台讀回八語metadata／CC／dub全部選取。英、日、韓、西、葡、印尼、越南、泰文的文字與metadata已完成獨立校對，共1,144句；[語言設定與真實決定來源](language-defaults.json)及[C03文字準備](c03/i18n/README.md)分開記錄選擇、文字與實際媒體就緒。配音仍待真正乾淨核准主片；保留繁中燒錄版，另採已驗一項metadata差分的clean主片配方，不假造QA或語言資格。
