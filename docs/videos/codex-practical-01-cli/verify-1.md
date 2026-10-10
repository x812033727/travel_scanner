# CLI 01 獨立事實與教學查核

查核日期：2026-10-11（Asia/Taipei）。查核者：practice_design；未撰寫本片 video.json、script.md、claims.md 或 author-evidence.json 的教學內容；本次只遮罩 claims.md 的公開定位資訊。查核者曾編製課程材料，因此本報告是對影片稿件的獨立查核，不冒充完全不熟悉教材的新手學習驗收。

結論：本版稿件 20 項主張 PASS，沒有未修正的事實錯誤；CLI 稿件事實／教學關卡通過。C20 已改為全新 start/reference 的只讀比較與第 03 課交接，沒有提前教同名刪除或篩選實作。本結論不涵蓋 Codex App、TTS 聽感、合成影片、站主播放驗收或上架。

## 綁定的稿件版本

| 檔案 | SHA-256 |
| --- | --- |
| video.json | `aedaef1c2c4af4958f01a9522bfc23e949f92c3945be73c38998739f314d99d2` |
| claims.md | `a73120df8d9a55cb5ea736425ca9c5c4d41cc5dfd95061d976390e92b22882f7` |
| script.md | `c438eaa86823ccba156f840ebfbfeb9ea4d89fa614d12c704cafd51f87b37eb9` |
| author-evidence.json | `06cdbdc632d483182325e2afaf5d331ef602f78078c7fa2b6e51281943d4c52c` |

若上述來源改動，這份關卡需重新綁定及查核；不能把本結論套用到新版。

## 原始證據及重做方法

直接讀取 repo 外原始紀錄，而非只讀作者整理表：`<home>/mokaair-work/codex-practical-series/runs/lesson-01-cli` 下的 session-01/prompt.txt、invocation.json、events.jsonl、answer.md、receipt.json、source-hashes.json、reference-tests.log、test-receipt.json、browser/receipt.json，以及 start/reference 五份程式。

| 原始檔 | SHA-256 |
| --- | --- |
| session-01/receipt.json | `09265676823f4d7e4800ab128b058bfc4e24c195d858301d7143737e8384c9f0` |
| session-01/events.jsonl | `d0a9e83323a264c326aa46e8d48fdc1fab9071951ca682f825ae3f59312fcc89` |
| session-01/prompt.txt | `c351e426dea6f39dbfd9fd3346aeb2acf79c134c9c9bc9939c5bc05dd538c4a8` |
| session-01/answer.md | `076f2ea395a12da48a45d3604cb876e18f421bc5a61357f1b1dfc049f8b5badc` |
| reference-tests.log | `03ff6b5087c4466904dae7302aa030252d7c720dd62927900ef5b34dcb7b0a05` |
| browser/receipt.json | `862915e4fb5a45d522d0ceff699011f919e365cda7085dbffff0b62f5819ddf3` |

以 materializeLesson(1) 建立全新副本到 `<home>/mokaair-work/codex-practical-series/runs/independent-verify-01-cli-20261011`。這不是另一輪 Codex 生成；沒有重送模型、登入或付費請求。從各 snapshot 實際重跑 `node --test core.test.mjs`：start exit 1／3 tests／2 pass／1 fail；reference exit 0／3 pass／0 fail；challenge exit 1／2 pass／1 fail。另在錯誤目錄實跑同一命令，exit 1，回到 start 後取得上述基線。

五份 start 檔與原實跑 start 的逐 byte SHA-256 全數一致：app.js `001e6fc55774b50732e6878bb336d1d4346e4d4f49739f659d570cfab5e1cf3c`；core.mjs `547831a8cf66422104f88bd17a903579cc1a6fba5c3aaf53cc4f7d6573f68c12`；core.test.mjs `111187cc469b5d2bf551126d72b8584589f97ac7bab6816f899502c6b498ebc1`；index.html `5740079d2988294ef077375172d2b34845f5798d465c03dcea9f18d2c4e64a07`；style.css `8fa375135810ed68890ee1bae3a331cf78690dafcd8ef8d8e711df80e115327c`。上層 baseline-prompt.txt 亦與原提示逐 byte 同 hash。

另外真正執行 browser-check.mjs，於全新 Edge context 比較 file:// 與 loopback HTTP，並重做兩版的 13 項檢查。獨立副本 browser/receipt.json 的 hash 為 `78951dcb5d3996dbc35f14b83d87576bcdf7733b4d5ec295d6a01a39e8aa4824`，Edge 155.0.4283.45、Node v24.13.0。該輪 HTTP 由測試 harness 的 Node 靜態伺服器提供；沒有把它寫成 Python 命令的原始執行紀錄。Python 3.14.6 與命令語義另以本機版本和官方文件核對。

## 逐項判定

PASS 表示主張在稿件實際限定的範圍內成立；未執行的建議、條件式排錯，不能被解讀為已實跑。

| ID | 狀態 | 查核結果及界線 |
| --- | --- | --- |
| C01 | PASS | 原 receipt outer exit 0、24 events；原 item_7 實際 command 為 node --test core.test.mjs，exit 1，3/2/1。內外成功意義分開正確。 |
| C02 | PASS | 原五檔 unchanged receipt 與目前原五檔、獨立副本 hash 一致；原 answer 自述也一致。沒有只靠模型自述證明。 |
| C03 | PASS | 材料入口、五檔及各 snapshot 可獨立啟動已重做；01 交診斷和下一輪契約，03 才實作 filter/search。原模型回覆沒有修程式。 |
| C04 | PASS | reference 來源為作者預備的 expected；原模型無檔案修改，稿件多次明說作者實作。 |
| C05 | PASS | invocation/receipt/item_10 支持 CLI 0.162.0-alpha.17.2、Node v24.13.0；稿件限定為錄製版本而非最新版。 |
| C06 | PASS | 逐檔讀取原始碼，責任表及 code 卡片與實際呼叫對上；JSON 編碼和 localStorage 寫入分開。 |
| C07 | PASS | 原 HTML module 與 app import 對上；MDN 支持 HTTP 模組測試，原及獨立 Edge file:// 均實際取得兩個載入錯誤。 |
| C08 | PASS | 三測試沒有 DOM、焦點或版面操作；原 answer 與事件清楚沒有 browser run。網頁驗收另列作者來源。 |
| C09 | PASS | 原 app 使用專用 localStorage key、沒有遠端帳號／資料庫；MDN origin 規則支持 protocol/host/port 界線。 |
| C10 | PASS | 提示全文及五段卡片意思一致，獨立材料提示 hash 與原 prompt 完全一致。 |
| C11 | PASS | 本機 codex exec --help 實查 stdin、read-only、-C、skip-git-repo-check、output-last-message。卡片是較短跟做命令，沒有冒充錄製完整 argv。新模型 replay NOT RUN。 |
| C12 | PASS | 原 JSONL 的 item_3/5/7/10 與 answer 可直接核對節錄；畫面明標 log 重現，沒有稱原生 TUI 錄影。個人完整路徑與 stderr 未放入稿件卡片。 |
| C13 | PASS | item_7 堆疊定位第 17 行；讀第 13–21 行支持第 16 行通過、第 18–20 行未跑到；visibleTasks 原文忽略 filter。沒有把後段刪除斷言當通過。 |
| C14 | PASS | Python 官方文件支持 cwd 靜態服務及 loopback bind；py --version 實查為 3.14.6。HTTP 網頁已獨立重做，但 Python command 的新 browser 錄製 NOT RUN，來源沒有混寫。 |
| C15 | PASS | 原 browser receipt 正好 13 項，非 13 項全部表示功能成功：1 項 file:// 預期載入故障、start active 預期缺口，其餘 11 項 pass。独立 HTTP 重做同結果；start active 2、reference active 1。日期 UTC 對台北 2026-10-11 正確。 |
| C16 | PASS | 原 reference log 3 pass／0 fail／exit 0，独立重做同結果，仍標作者參考。 |
| C17 | PASS | 下一轮提示、空清單／順序／輸入不变／網頁篩選验收與原 answer 一致；稿件明說未執行，未提前聲稱修復。 |
| C18 | PASS | 條件式排錯合理；錯目錄及 file:// 已独立重做。port 占用例 NOT RUN，稿件沒有稱實測。 |
| C19 | PASS | 官方 troubleshooting 與原事件支持區分未執行和專案失敗；本次 auth／quota 故障模擬 NOT RUN，稿件為「如果」而非錄製事實。 |
| C20 | PASS | 已逐讀 transfer-task/transfer-what-to-look-for 與教材01契約；全新兩版2/1 vs3/0比較重做完成。只讀交03的函式範圍及驗收；challenge另為 Completed 缺口，沒有要求01修功能。 |

## 口語與教學卡片查核

逐讀全部 60 卡、162 句旁白及 code／terminal／table 內容。主線完整：先確定材料与目錄 → 建檔案責任地圖 → 送只讀契約 → 分清 inner/outer exit → 找實際失敗斷言 → 另做 HTTP 網頁 → 交下一輪範圍 → 排錯與變式。目的、操作、可觀察結果和交付物都有對應，沒有只列功能。

旁白用短句解释 origin、hash、斷言与退出碼，程式／參數由可停看的卡片承載；沒有把 code 或完整命令逼進口播。第 01 課保留 Active 故障與未執行後段斷言，reference 明標作者，提供了可解釋差異的失敗案例。C20 修正後能將方法遷移到新副本，而不是抄出本次模型報告。

`node tools/video/cli.mjs lint --slug codex-practical-01-cli` 實跑 exit 0：0 errors、0 warnings；估 14.3 min、162 lines、3174 spoken units。這是字數估計，不是實際可播放長度；TTS 聽感、字幕時間軸與合成後正文長度仍 NOT RUN。

卡片展示的是實際 CLI log 的重現及另行網頁來源，沒有原生 Codex App 截圖或操作證據。網頁自動化證明上述限定行為；最終剪輯截圖的可讀性、終端與網頁切換的節奏、音畫對齊仍需媒體階段驗收。不得將本稿件的 PASS 升級為 App 或成片通過。

## 未執行範圍

- 新一輪付費／模型提示重送、讀者首次登入及故障模擬：NOT RUN。
- Codex App 實跑、App UI 源圖與36支全系列成片：NOT RUN。
- 配音實際聽審、影片播放、字幕同步、實際片長、站主接受、YouTube 上架：NOT RUN。
- 全新 ZIP 壓縮／解壓後跟做由 root 的 package receipt 另綁定；本輪独立跟做以全新 materialized 01 為基準，不冒充 ZIP receipt。

查核用官方來源實際開啟日期均為 2026-10-11：[CLI reference](https://learn.chatgpt.com/docs/cli/reference)、[non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)、[best practices](https://learn.chatgpt.com/docs/learn/best-practices)、[troubleshooting](https://learn.chatgpt.com/docs/reference/troubleshooting)、[MDN modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)、[MDN localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)、[Python http.server](https://docs.python.org/3/library/http.server.html)。本輪沒有提出需改動的事實項，未觸發多項事實改稿後的第二輪規則。

2026-10-11 腳本來源重新綁定（rename_code_audit 獨立比對）：以 `git cat-file blob 4f34b813022876c2a9ccf7590f956b2ce080279f` 讀取先前暫存版本，逐 byte SHA-256 為原查核的 `7014d08f62a3076b0a4fef304700cabec9e6a1643dd393ae10116f24215169b0`，16,378 bytes。只將第 3 行「作者稿｜教學卡片重現真實 exec 檢查紀錄，未合成、未完成獨立事實審稿。」換成「作者來源稿｜教學卡片重現真實 exec 檢查紀錄；當前實測與驗收狀態見 PRODUCTION-STATE.md。」，再將檔尾兩個 LF 改為一個 LF，即與目前 16,394 bytes 的 script.md 完全相同；兩版原本均為 LF，沒有其他內容差異。

本次另逐 byte 重算 video.json、claims.md、author-evidence.json，三檔 SHA-256 均與上表原查核值一致；旁白 JSON、字幕來源、60 張卡片及既有 C01–C20 的內容未變，20 項 PASS 維持。這次只重新綁定腳本來源；PRODUCTION-STATE.md 的引用提供後續製作狀態入口，未新增配音、合成影片或播放驗收的查核結論。

2026-10-11 影片 JSON 來源重新綁定（practice_design 獨立比對）：以 `git show :docs/videos/codex-practical-01-cli/video.json` 讀取原查核版本，原 SHA-256 `0bdff9e7b8679fca51c7b21d2e8d4915c785b104828aaf5e6d147dab340051e6` 保留為歷史來源。解析兩版 JSON 後逐欄位比對，唯一差異為 `baseline-test.data.title` 新增「真實測試輸出摘錄／重新排版」（實際 JSON 路徑 `$.scenes.30.data.title`）；沒有刪除或修改其他欄位。這是非口播的畫面標籤；lines、命令、輸出、claims 全部未變。新版 SHA-256 `a912a176d6981e4fcfc86097e96aa2f36d6ff3ca67290199fe3350455055fa17` 已綁定於上表；script.md、claims.md、author-evidence.json 雜湊均與上次查核一致，因此既有 20 項 PASS 保留。本次只核對來源差異，沒有重新執行模型、瀏覽器、語音或影片驗收。

2026-10-11 聽辨用字增量獨立查核與來源重新綁定（practice_design；未撰寫替換句）：直接讀取 `media/codex-practical-01-cli/review/history/listener-rewrite-1` 保存的完整前版，video.json 原 hash `a912a176d6981e4fcfc86097e96aa2f36d6ff3ca67290199fe3350455055fa17`、script.md 原 hash `8892b61e1493f144bd6f59966db96296f58cb28e06057a808b8ac4e2ccfa4a04` 均與上次查核綁定一致。兩版 JSON 逐欄位比對只有 `$.scenes.9.lines.2.text` 一處改動，ID `346cca` 保留：「你跟做時也保留起點，別靠記憶猜原本的樣子。」改為「你練習時也保留起點，別靠記憶猜原本的樣子。」；script.md 亦恰好只替換同一句。這次只將「跟做」改為「練習」，保留起點的要求與語意一致，未新增事實、數字、專名、命令或實测結果，其他卡片、主張與行 ID 全部未變。新版 video.json `4ff3c4981a53b42319b33045fa6df1cdfa4f19a3c60b0b55da54fd2ded00c93a`、script.md `60ba0243a4b9375f6b86fa31d6d3e3203706fbde7b2f7e6e68eacf3126ffb427` 已綁定於上表；claims.md、author-evidence.json 及教材／錄製提示的保護雜湊未變，20 項主張 PASS 保留。替換句由 rename_code_audit 建議、root 套用，本查核者獨立核對增量；沒有把聽辨改字等同配音、整片或站主驗收通過。

公開定位說明：`<home>` 與 `<repo>` 是去識別佔位，不供直接執行。精確路徑與未遮罩原始收據保存在 repo 外；既有收據 SHA-256 仍綁定原始位元組。

2026-10-11 公開定位遮罩增量與 claims 來源重新綁定：practice_design 只將 claims.md 的私人使用者路徑換成 `<home>`，並加入不供執行的公開定位說明；原版 hash `04a833a864afd789162819623822b82ef647ea14eb92939c4ed8b4ac98c32137` 與完整前版仍保存於 repo 外。未編寫此次遮罩的 rename_code_audit 直接比對前後完整檔案，C01–C20 表格逐位元組相同，新版 claims.md hash `a73120df8d9a55cb5ea736425ca9c5c4d41cc5dfd95061d976390e92b22882f7` 已綁定於上表，20 項 PASS 保留。其獨立收據 `independent-locator-audit-final.json` hash 為 `bd4099c940b77a2fd695955793f119c645c7c9bb7f3d5167220612a2d7728644`；公開 evidence 中既有原始收據、製作來源與核准 hash 仍指向未遮罩的原始產物，不是目前公開副本的 hash。此次遮罩未修改影片旁白、卡片、教材程式或模型輸入。

2026-10-11 片尾畫面節奏增量獨立查核與影片來源重新綁定（practice_design；未編寫此畫面修改）：直接比對 repo 外 `media/codex-practical-01-cli/review/history/pace-fix-1` 的完整前版。前版 video.json `4ff3c4981a53b42319b33045fa6df1cdfa4f19a3c60b0b55da54fd2ded00c93a`、script.md `60ba0243a4b9375f6b86fa31d6d3e3203706fbde7b2f7e6e68eacf3126ffb427` 均與前次綁定一致；解析後只有 `$.scenes.59` 的八處畫面差異：template 由 outro 改為 bullets；刪除非口播 cta；三條原有 data.lines 原樣移至 data.items；新增畫面 source；三句各新增 reveal:1。全部 162 句的文字與 ID、60 張卡片的其他欄位及 claims 均完全相同。authoring.mjs 只修改片尾卡片宣告；script.md 只將片尾「畫面：outro」換成「畫面：bullets」。新版 video.json `aedaef1c2c4af4958f01a9522bfc23e949f92c3945be73c38998739f314d99d2`、script.md `c438eaa86823ccba156f840ebfbfeb9ea4d89fa614d12c704cafd51f87b37eb9` 已綁定於上表，20 項 PASS 保留。此項與公開定位遮罩是兩筆獨立增量；本次只查核來源，不代替新畫面目視、旁白、字幕、成片 QA 或站主播放驗收。
