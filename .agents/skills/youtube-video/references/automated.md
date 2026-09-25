# 全自動路線：AI 撰稿、台灣口音旁白、自動做成片

這條路線的成品是一支投影片加旁白的影片。旁白由伺服器代為合成（頻道聲音是 Gemini 的 Sulafat；Azure 是另一個供應商，站主覺得它的聲音太平），畫面由 HTML 版型截圖，合成用 ffmpeg，CC 字幕五語系。站主只要在四個地方把關：

1. 選大綱
2. 聽旁白
3. 看成片、確認可以上架
4. 在 YouTube Studio 按公開

前三個都在網站後台的「影片審核」頁（`/admin/videos`）做：工具用 `review-push` 把該關的東西送上去（企劃與選項、旁白與 Jev 檢查、720p 成片與五語系標題、上傳檢查表），站主在頁面上核准或退回，工具再用 `review-pull` 讀回。核准綁定檔案雜湊，檔案改過就要重新送審。對話裡的提問只在後台頁用不了時當備援。

為什麼這樣設計、YouTube 與 Azure 的規則，寫在 `docs/videos/DESIGN.md`；頻道的版型、配色與聲音寫在 `docs/videos/README.md`。這份只寫**怎麼做**。

路徑寫法：`<ROOT>` 是 repo 根目錄；`<VIDEO_WORKDIR>` 是影片的工作資料夾，預設在使用者家目錄下，可以用 `--workdir` 或環境變數 `VIDEO_WORKDIR` 改；`<SLUG>` 是影片代號；`<VIDEO_DOCS>` 是這支影片在 repo 裡的資料夾 `docs/videos/<SLUG>/`，只放文字檔。音檔、畫面、mp4 只放在 `<VIDEO_WORKDIR>/<SLUG>/`，絕不進 git（repo 是公開的）。

## 一次性設定（站主做，代理不經手任何金鑰）

| 項目 | 怎麼做 | 沒做會怎樣 |
| --- | --- | --- |
| Gemini 語音（頻道聲音） | 不用新金鑰：伺服器用網站既有的 Gemini 金鑰（`hotspot_guide_gemini_api_key`，在「AI 供應商與金鑰」）。`video.json` 寫 `"voice": {"provider": "gemini", "name": "Sulafat", "style": "…"}`，模型預設 `gemini-3.8-flash-tts`。每月字數上限另計（預設 300,000 字），設在「Azure 語音（影片旁白）」卡片上 | `tts` 結束碼 3 |
| Azure 語音 | 只有選 Azure 聲音時才需要。Azure 入口網站建 Speech 資源（F0 免費層），金鑰與區域填在同一張「Azure 語音（影片旁白）」卡，按連線測試 | `tts` 結束碼 3 |
| 影片工具權杖 | 配對，不貼權杖（RFC 8628 裝置流程）：代理在背景跑 `node tools/video/cli.mjs login`，把它印出的連結（`/zh-TW/admin/settings?provider=azure_speech&video_pairing=…`，開到卡片的「配對本機工具」）交給站主；站主核對驗證碼和終端機上一樣，按「允許」。權杖直接寫進 `~/.mokaair/video-tool.json`，不會印出來。配對在 Redis 只活 10 分鐘，權杖在領取時才產生、只能領一次 | `tts` 結束碼 3，提示去 login |
| ffmpeg | Windows 執行 `winget install BtbN.FFmpeg.GPL`；Ubuntu 執行 `apt-get install ffmpeg`；也可以設 `FFMPEG_PATH` 指定位置 | `assemble` 結束碼 5 |
| 瀏覽器 | `npx playwright install chromium`；Windows ARM64 上建議用原生的 Edge：`render --channel msedge`，或設 `VIDEO_BROWSER_CHANNEL=msedge` | `render` 結束碼 5 |

## 主幹

| # | 階段 | 誰 | 產出 | 關卡 |
| --- | --- | --- | --- | --- |
| 0 | 認領票、開工作區 | 協調者 | — | 票已認領 |
| 1 | 企劃（提示 `.agents/skills/youtube-video/references/prompts/planner.md`） | 企劃代理（sonnet） | `<VIDEO_DOCS>/brief.md` | `review-push` 送企劃；站主在 `/admin/videos` 從 2–3 個大綱選一個；`review-pull` 記下核准 |
| 2 | 撰稿（提示 `.agents/skills/youtube-video/references/prompts/writer-video.md`） | 撰稿代理（sonnet） | `video.json`、`claims.md`、發音字典新增的詞 | `lint` 零錯誤 |
| 3 | 查核（提示 `.agents/skills/youtube-video/references/prompts/verifier-video.md`） | **另一個**代理（opus） | `verify-1.md` | 改超過 3 個事實，就換人再查一輪，寫 `verify-2.md` |
| 4 | 聽眾優先審稿：口語、句長、術語唸法、開場鉤子 | 審稿代理 | 修正清單 | 協調者套用後再跑 `lint` |
| 5 | `tts` | 工具 | 每句的音檔、`narration.wav`、`timeline.json` | 先跑 `--dry-run` 看字數與額度 |
| 6 | `check-audio`（Gemini 轉寫、Jev 判斷），再 `review-push` 送旁白 | 工具、站主 | `review/check-flags.json` | 被標的句子補字典或改措辭，`tts --redo review/check-flags.json` 只重錄那幾句；站主在 `/admin/videos` 核准旁白，`review-pull` 記下 |
| 7 | `render` | 工具 | `frames/`、`contact-sheet.png`、`thumbnail.jpg` | 看聯絡表；版面錯誤就縮短文字 |
| 8 | `assemble` | 工具 | `final.mp4`、`checks.json` | 自動檢查全過 |
| 9 | CC 翻譯：`i18n-sheet` 出底稿 → 每個語系一個翻譯代理（`prompts/caption-translate.md`，sonnet）填 → `i18n-merge` → 另一個審稿代理（`prompts/caption-review.md`，opus）只交修正清單 → 協調者改底稿再 merge → `captions` | 翻譯與審稿代理、工具 | `<VIDEO_DOCS>/i18n/<語系>.json`、`captions/*.srt` | `i18n-merge` 沒有列出問題；lint 沒有過期或缺漏的翻譯 |
| 10 | `review-push` 送成片（720p 預覽、聯絡表、縮圖、五語系標題說明） | 站主 | — | 站主在 `/admin/videos` 看完核准，`review-pull` 記下 |
| 11 | `package`，再 `review-push` 送上架確認 | 工具、站主 | `upload/`（含 `UPLOAD.md`） | 核准的成片必須和目前的 `final.mp4` 一致；站主按「確認可以上架」，`review-pull` 記下 |
| 12 | 站主照 `UPLOAD.md` 在 Studio 上傳成私人，檢查後自己按公開 | 站主 | YouTube 影片 | 影片 ID 寫回 `video.json` 的 `youtube.video_id` |

第 4 步聽眾審稿最常抓到的四種問題：代理替站主編經驗（「我都自己測過」）；台灣介面有中文名稱卻寫英文 UI 名；預測沒標成意見；引用站上已經過期的圖解。

隨時可以跑 `node tools/video/cli.mjs status --slug <SLUG>`，它會列出 12 步做到哪裡，並印出下一個該跑的指令。它判斷的依據是比對各檔案裡記下的雜湊，不看紀錄：腳本改過，舊的旁白就不算完成。

## 指令

```bash
node tools/video/cli.mjs status   --slug <SLUG>
node tools/video/cli.mjs lint     --slug <SLUG>              # 或 --file 指向範例
node tools/video/cli.mjs ids      --count 20 --slug <SLUG>   # 新句子的穩定 id
node tools/video/cli.mjs audition --text-file <FILE> [--voices a,b]   # 中文一律走檔案
node tools/video/cli.mjs tts      --slug <SLUG> [--dry-run] [--redo flags.json]
node tools/video/cli.mjs review   --slug <SLUG>
node tools/video/cli.mjs render   --slug <SLUG> [--channel msedge]
node tools/video/cli.mjs assemble --slug <SLUG>
node tools/video/cli.mjs i18n-sheet --slug <SLUG> [--locale en,ja]   # 翻譯底稿在 <VIDEO_WORKDIR>/<SLUG>/i18n/，只標出缺漏或過期的句子
node tools/video/cli.mjs i18n-merge --slug <SLUG> [--locale en,ja]   # 底稿寫回 i18n/<語系>.json，雜湊由工具算
node tools/video/cli.mjs captions --slug <SLUG>
node tools/video/cli.mjs review-push --slug <SLUG> [--gate outline|audio|final|publish]   # 送審到 /admin/videos
node tools/video/cli.mjs review-pull --slug <SLUG>              # 讀回站主的決定，核准才寫進 approvals.json
node tools/video/cli.mjs approve  --slug <SLUG> --gate outline|audio|final|publish --note "<站主怎麼回答的>"   # 後台頁不能用時的備援
node tools/video/cli.mjs package  --slug <SLUG>
node tools/video/assemble/smoke.mjs --workdir <DIR> [--channel msedge]   # 整條流程的冒煙測試
```

結束碼：0 成功；1 lint 或檢查沒過；2 用法錯誤或順序不對（例如還沒 tts 就 assemble）；3 需要站主（權杖、後台設定、核准）；4 外部服務或額度；5 工具沒裝。要中途停下來，在工作區或它的上一層放一個 `STOP` 檔：長的階段做完手上那一段就會停，下次從快取接著做。

## video.json 的重點

- 格式定義在 `tools/video/core/schema.mjs`。
- 最小範例：`tools/video/core/fixtures/minimal/video.json`。
- 每種版型各用一次的範例：`tools/video/templates/fixtures/showcase/video.json`。

寫作重點：

- **句子 id**：用 `ids` 產生，是穩定的短碼。插入新句子時不要重新編號，翻譯、快取和站主的唸錯標記都靠它對齊。
- **章節**：有 `chapter` 的場景會開一個 YouTube 章節。章節至少 3 個，每個至少 10 秒；lint 先用估計值檢查，`tts` 之後再用實際時間檢查一次。
- **版型**：共 11 種，資料欄位與可以逐條出現的數量定義在 `tools/video/templates/templates.mjs` 的 `TEMPLATE_SPECS`。`**文字**` 會變成強調色，`\n` 是手動斷行。
- **圖片與圖解**：只能用 `apps/web/public/` 或 `docs/videos/` 底下的檔案，並列在 `assets`，寫清楚來源與授權。
- **說明欄**：`youtube.description` 只寫本文。章節時間戳、站內文章連結（依 `source_guide` 自動加 UTM）、參考資料（`sources`），都由工具組進去。

## 發音與試聽

- 中文 TTS 最常唸錯英文縮寫和破音字。發音字典是 `docs/videos/` 底下的 `lexicon.json`，所有影片共用，第一支影片建立它。每個英文詞都要在字典裡，lint 才會過。
- 格式是 `{ "schema_version": 1, "terms": { … } }`。`terms` 的值有兩種：唸法（例如 `"LLM": "L L M"`，送出時變成 `<sub alias>`），或 `null`（表示照原字唸就對，要等試聽確認過）。
- zh-TW 的 `<phoneme>` 音標沒有官方文件，不要用。
- **Gemini 沒有 SSML**：字典的唸法直接換進文字裡送出（不是 `<sub alias>`），停頓換成 Gemini 的 `<long pause>`／`<short pause>` 標籤，但長度不像 Azure 的 break 那樣精準。語氣靠 `voice.style`，Gemini 聲音不能寫 `rate`。伺服器回 24 kHz，本機工具用視窗化 sinc 內插升到 48 kHz。
- **試聽只能經伺服器**：`audition --voices gemini:<聲音>`。站主的 Gemini 金鑰限了伺服器 IP，在 AI Studio 會 403；Cloud 的 Gemini-TTS 只收服務帳號。
- 內建瀏覽器放不了 repo 外 `file://` 路徑的音檔：試聽檔用 SendUserFile 直接給站主。試聽檔不要放在 scratchpad（代理會清掉）。
- **收斂旁白**：`check-audio` 先在本機比對，只差同音字（拼音連聲調相同）或語氣詞的句子不送 Jev；Jev 的每日次數在「AI 供應商與金鑰」卡片，和自動新聞、景點介紹共用。被標的句子 `tts --redo` 只重錄那幾句（快取按句）。一直被聽錯的句子就改措辭，例如句尾「答」→「回答」、「旗艦」→「旗艦模型」、「分三步走」→「分三個步驟」。`check-audio` 遇到轉寫失敗的句子會跳過，連續 3 句失敗才停；工具這邊的修改不用部署就生效。

## 成本

- Azure 每個中文字算兩個計費字元，SSML 標記也計費。一支 10 分鐘的影片約 8,000–9,000 計費字元，免費額度每月 50 萬，大約可以做 50 支。
- `tts --dry-run` 會印出這支影片的估計字數，以及伺服器回報的本月用量。
- 每月上限由站主在後台卡片設定。超過時伺服器以 429 拒絕，請求不會送到 Azure，所以不會產生費用。
- Gemini 以送出的文字字數計，和 Azure 分開算，預設每月 300,000 字（約一百支 10 分鐘影片）。
- 實測合成語速約每分鐘 300 字（48 kHz 單聲道），工具估計用 250，所以 `lint` 估的長度偏長；要 8–12 分鐘的成片，旁白字數要比估計多寫一些。

## 坑

- **中文參數一律寫進檔案**：PowerShell 5.1 會弄壞命令列上的非 ASCII 參數，所以 `audition` 只收 `--text-file`；`approve --note` 也盡量寫英文或短句。
- **`render` 回報版面錯誤**：代表縮小 40% 以後字還是放不下，或畫面裡有字型沒有的字（例如 emoji）。處理方式是縮短文字或換版型，不要改主題 CSS。
- **`assemble` 回報某一格「不像」預期的畫面**：代表畫面錯位了，先看 `checks.json` 是哪個場景的哪一格。門檻：44 dB 以上直接算對、35 以下算錯；中間（字很密的表格、比較卡，正確也只有 40 左右）要比同場景其他畫面高 3 dB，`checks.json` 會記下它和每個對手的分數。不要調低門檻。
- **`tts` 回報某一批改成逐句合成**：代表那一批的靜音切段和字數對不上。這通常不影響成品，只是多送幾次請求。如果同一批一直發生，把那個場景拆短一點。
- **代理不能碰權杖**：用上面的配對流程，權杖不能出現在對話裡、檔案裡或指令參數裡。替站主開一個終端機分頁讓他打權杖，會被分類器擋成 Credential Leakage。
- **ffmpeg（除錯 `assemble` 時用得到）**：PNG 的 concat 預設時基是 1/25 秒，每個檔案要加 `option framerate 30`；PNG 沒有色彩資訊，要 `setparams` 加 `-x264-params colorprim/transfer/colormatrix`；單聲道先正規化再轉立體聲會大 3 LU；抽格用場景片段上的 `select=eq(n,N)`，不要對串好的 mp4 用 `-ss`；Noto Sans CJK 單行會「溢出」零點幾個行高，所以版面檢查容許到 0.4 em。
- **本機環境**：
  - `winget install BtbN.FFmpeg.GPL`（原生 ARM64）之後，舊的 shell 的 PATH 沒有它：用完整路徑或 `FFMPEG_PATH`。
  - Playwright 要的 `chromium_headless_shell` 在 Windows ARM64 是 x64 模擬，很慢：用 `--channel msedge`（17 個投影片狀態約 75–90 秒）。
  - 沒有 `node_modules` 的 worktree 會解析到主 checkout 的（沒有字型套件）：在 worktree 裡跑 `npm ci --ignore-scripts`。
  - `uv sync` 失敗留下的壞 venv（`apps/api` 底下的 `.venv`，沒有 fastapi、os error 183）：刪掉重來。
  - npm 11.6.2 的 `--package-lock-only` 會拿掉 `libc` 欄位：lockfile 的條目要手補。
- **在過期的分支上跑新工具（toolrun）**：`git archive -o x.tar origin/main tools/video .agents/skills/youtube-video`，再**另一個指令** `tar -xf`（串在一起會被 worktree 守門擋）。在解開的目錄建一個指向 worktree `node_modules` 的 junction（它會消失，消失後 pinyin-pro 會失敗），並複製一份 docs；`--file`／`--slug` 相對於 toolrun 目錄。
- **worktree 隔離的 session**：含 `$(…)`、shell 迴圈、`MSYS_NO_PATHCONV=1 "/c/Program Files/…"`、jq 字串，甚至 `node -e` 裡出現「不進 git」字樣的指令，都可能被當成 git 操作擋下。改用 PowerShell、ccd_pr 工具、Edit，或 scratchpad 裡的 .mjs 腳本。`EnterWorktree` 也會把還在跑的背景代理鎖在外面（它們對舊 worktree 的寫檔、curl、node 都被拒）：等代理做完再切，或讓代理寫到 repo 外。
- **改工具或後台時的測試坑**：
  - `apps/api/tests/test_error_localization.py`：admin／deployments 以外的每個 `AppError(…, "code")` 都要四語系訊息，否則 CI 的 api 會紅（只跑單一檔案時看不到）。影片工具的錯誤在 `apps/api/app/video_speech/admin_api.py` 丟；其他模組丟自己的例外（例如 `checking.CheckUnavailable`）。
  - 新的後台頁要加進 `apps/web/e2e/admin-operations-full-stack.spec.ts` 寫死的導覽清單。
  - 改這個 skill：`tools/skills.test.mjs` 檢查路徑前會拿掉 `<X>/` 這種大寫佔位符，所以寫 `<VIDEO_DOCS>/brief.md`；還不存在的檔案要寫成「`docs/videos/` 底下的 `lexicon.json`」。

## 主機自動產線

設計在 `docs/videos/AUTOMATION.md`；這裡是維運。容器是 `docker-compose.prod.yml` 的 `video-worker`（compose profile `video`，部署腳本已帶 `--profile video`）。

- 看紀錄：`docker compose -f docker-compose.prod.yml logs --timestamps video-worker`；`top video-worker` 看它是不是在 `sleep 300`。
- 緊急停止：`docker compose -f docker-compose.prod.yml exec -T video-worker touch /var/lib/mokaair/video-work/STOP`，做完手上那一段就停；要恢復時刪掉這個檔。
- `video_docs` volume 只在第一次建立時從映像填入，之後映像裡的 `docs/videos` 更新不會進去。
- 工人只看得到自己的 volume，可能重做本機已經做過的題目：本機或分支上的影片用 `review-push --report-only` 登記到審核頁。
- 換新模型前先更新主機的 Claude CLI（`claude update`；2.1.259 對 Opus 5.5 回 400，要 2.1.280 以上）。
- 第一次配對碰上部署重啟的 502：重啟工人即可；驗證碼 10 分鐘過期，工人會自己重新要。
- 診斷時用 stdin 跑 `flow.mjs` 的 `step()` 會真的做一個單位的工作，不是唯讀。
