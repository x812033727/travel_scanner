# 五支品牌故事｜製作前檢查收據

本機核對日期：2026-10-14（Asia/Taipei）。範圍是本機 repo、預設影片工作目錄及 Google 公開價目；**未連正式主機、未讀正式資料庫／後台、未匯入、未執行付費模型，也沒有五支成片**。本文件供安排五集製作時逐項回讀，不能把表格的「本機不存在」推論成主機不存在。

## 1. 本機輸入與空白工作區

依 [影片工具的路徑實作](../../../tools/video/core/paths.mjs)，逐集文字檔位置為 `docs/videos/<slug>/video.json`，媒體位於 `<VIDEO_WORKDIR>/<slug>/`；本機沒有設定 `VIDEO_WORKDIR`，故使用 `C:\Users\x8120\mokaair-work\videos`。五個 slug 從[原 100 題已編譯清單](../story-plans/brand-stories-100/stories.json)回讀；該檔目前 1,414,653 bytes，SHA-256 為 `6f1e4619c7bf5847b1b67a21b5e97dd015ccef939fbf19c098c33178840dce26`。下表的兩項 `否` 是 `Test-Path -LiteralPath` 的本機結果。

| 題號 | slug | 原 100 題序號 | `video.json` | 工作目錄 |
| --- | --- | ---: | --- | --- |
| A29 樂高 | `story-lego-sold-legoland-to-survive` | 33 | 否 | 否 |
| A16 Costco | `story-costco-hot-dog` | 3 | 否 | 否 |
| A37 Adidas／Puma | `story-adidas-puma-brothers` | 47 | 否 | 否 |
| B14 味之素 | `story-ajinomoto-chip-film` | 8 | 否 | 否 |
| A21 品客 | `story-pringles-vat-case` | 9 | 否 | 否 |

對應的[五份 treatment 與觀看承諾](README.md)是編輯輸入；各題仍以原 `stories/<ID>.json`、`reviews/<ID>.json` 為已查核事實基礎。執行 `node tools/video/story-plans/validate.mjs --only A29,A16,A37,B14,A21` 得 `100 stories`、`0 problems`、`4 warnings`（A16、A21、A29、A37 的原縮圖字數或斷行）。這只檢查企劃結構與原 review 綁定，不代表五份新 treatment 的完整逐字稿已通過獨立查核。製作前須將新敘事逐句連回來源，對新增或改寫的事實再查核。

## 2. v4 品牌素材與本機工具

從 `C:\Users\x8120\mokaair-work\videos\_branding\current.json` 讀到的 index 與實檔：

| 項目 | 本機回讀值 |
| --- | --- |
| package ID／pin | `mokaair-brand-package-v4-endscreen`／`416c8768d4d29f2e746a0c019d2d598ec367cbb66b0ff996841c523651a63e88` |
| `current.json` 檔案 SHA-256 | `d9567db21cc08f0055707754242636f3e63f91474413871f530aaf33cbdb9454` |
| 片頭 `intro.mp4` SHA-256 | `50a53efa54fe5158a166390c7f46518c052be1af005f99a5f3c57e530b0bb67d`；與 index 相符 |
| 片尾 `outro.mp4` SHA-256 | `00eb9ccc8449fa8b47de0aab290b8aa7d55b09962c12a127e0f0c9c5f7834396`；與 index 相符 |
| `ffprobe` | 兩者皆 1920×1080、30 fps；片頭 150 格／5.000 秒，片尾 630 格／21.000 秒 |
| `branding --json` | 2026-10-14 在安裝依賴後讀回上述 index／檔案 SHA；`series: null`、`installed: false`，尚未對五集任何一集安裝素材 |

實檔在 `_branding/<pin>/`，SHA 由 `Get-FileHash -Algorithm SHA256` 算出。這只證明**本機** v4 來源一致；實際合成前應在執行環境再回讀 index、檔案 SHA 並把 pin 與成片一起記錄。此 v4 片尾可點元素依[時間修正票](../../../tasks/open/2026-10-12-correct-v4-youtube-end-screen-timing.md)放在**最後 16 秒**；MP4 的卡位不等於 YouTube Studio 連結，實際上傳後須在 Studio 放兩個影片元素與訂閱元素並點擊驗證。

本機可找到系統 Node `v24.13.0`、`npm`、`uv 0.12.4`、FFmpeg 與 FFprobe `N-125875-g5d4d3bdc61-20260731`，並可找到 `tools/video/cli.mjs`、`tools/video/automation/story.mjs`、`tools/video/story-plans/validate.mjs`、`apps/api/app/video_automation/story_cli.py`。`python` 指向 WindowsApps shim，未驗證為可執行的 Python 環境。首次唯讀嘗試 `node tools/video/cli.mjs branding --json` 因本 checkout 缺 `pinyin-pro` 以 `ERR_MODULE_NOT_FOUND` 退出；其後在 repo 根目錄 `npm ci`（exit 0），改用本機已驗證的 bundled Node `v24.19.0` 執行同一 CLI（exit 0），得到上表所列 index 與 `installed: false`。這只證明本機工具已能讀取品牌素材，**沒有任何五集 `video.json` 或媒體工作區**，更不是主機製作狀態。

`npm run test:docs-videos` 第一次在缺依賴時 131／137 通過；安裝依賴後用系統 Node 24.13.0 為 214／215，剩餘案例的子程序以 `3221226505` 退出。這是[既有 Windows Unicode 路徑遞迴複製問題](../../../tasks/done/2026-09-28-investigate-windows-native-crash-in-video.md)的同一症狀；依 [dev-and-ci 環境指示](../../../.agents/skills/dev-and-ci/references/local-env.md)只對本次命令改用 bundled Node 24.19.0，**215／215 通過，exit 0**，沒有修改或略過測試。`npm run check:tasks` 為 exit 0、只列其他工作的過期認領警告。

## 3. 五份 treatment 尚未接進 story worker

[故事工作流程](../../../.agents/skills/youtube-video/references/story.md)與[工人實作](../../../tools/video/automation/story.mjs)顯示：工人向 `GET /video/automation/series/next` 取資料庫 episode `beats`，以六個固定 key `hook/origin/idea/engine/turn/now` 逐章撰稿；**不讀本資料夾的 Markdown**。目前 [CLI 匯入器](../../../apps/api/app/video_automation/story_cli.py)只讀完整編譯 JSON 的 stdin；[校驗／匯入規則](../../../apps/api/app/video_automation/stories.py)要求故事連號 `1..N`，`--limit N` 只取前 N 題，不能用 `--limit` 選 A29、A16、A37、B14、A21。因此把現有 100 題 `stories.json` 交給工人，既不能只做這五題，也不會採用本資料夾新增的開場、因果轉場和三句結尾。

**下一個必要變更**：先選定不動原 100 題清單及排程的五集接線方案。可另製一份經審核的五題編譯輸入與獨立 `kind=story` 作品，映射新 treatment 為有效的六章 `beats`、重排連號與不衝突的時段；這份輸入尚未建立或驗證。匯入器會查跨作品 episode 與影片 slug 衝突：若正式站已匯入原 100 題，同 slug 的第二作品會被拒絕。屆時必須先查 live ID／slug／狀態，設計保留既有 episode 的接法或經審核的新 slug；不得直接覆寫已開始的故事、改原排程或假設 dry-run 一定會通過。新增事實、章節要點與 CTA 的來源及 review 也需重驗。現有 writer 的 `now-outro` 提示詞只要求回答與一個下一步；本企劃要求的「回答、故事相關留言、訂閱」三句及片尾 16 秒 Studio 元素，還須在逐字稿、工人提示詞／組裝與實片 QA 中逐項核對，不能因原 worker 有說書提示就視為完成。

只有在五題輸入、slug 接法、主機狀態及站主決定都落定後，才可在**已核准的主機環境**用下列形式作唯讀匯入試跑；此處未執行，也沒有 `--apply`：

```bash
# <approved-five.json> 必須是另外審核的完整編譯輸入，不是 README 或 treatment。
# 檔案從主機 shell 的 stdin 餵給 api；先核對其 series.slug 與 --series 相同。
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli video-story-import \
  --series <approved-five-series-slug> < <approved-five.json>
```

記錄 dry-run 的 `create/update/leave_alone/refused/problems`、既有作品差異、五個 slug 與相同 ID 的所有在製工作；有任何衝突就停止設計修正。`--episodes-per-day` 只在新建作品時生效，已存在作品須在後台確認。匯入後 `node tools/video/cli.mjs auto --once` 也只推進一個工作單元，不能當作一支成片的命令。

## 4. 主機、站主與實際生產關卡

[A01／B18 試作票](../../../tasks/open/2026-09-28-video-story-pilot.md)目前仍為 `open`，其勾選項要求：先在正式主機讓 A01、B18 到「可以上架」，站主看過；回填時長、張數、重做率、階段秒數、實際帳本、1K 清晰度與 token 用量。票明載正式站操作須站主同意，且部署、上限、頻道立場、字幕語系、權限、主機 nginx／worker 狀態須逐項核對。此前的[試作執行方案](../../work-status-2026-09-29-story-pilot-plan.md)也只是一份未執行的方案，不能當作 live 收據。本輪沒有查正式主機、沒有改它的設定或驗帳；五集另需安排，不自動跳過 A01／B18 關卡，也不觸發每日兩支 rollout。

在接線完成且取得該階段的站主決定後，五題每支按同一張收據走：

1. **主機前檢**：核 live SHA、API／worker 版本與映像、release hold、資料庫備份／migration、既有 `brand-stories` 與五個 ID／slug／狀態；查帳號、`content.manage`、AI 漫劇開關、頻道立場、常設指示、繁中聲音、字幕語系、模型路由、TTS／judge／圖片額度、每日與同時進行上限。保留去識別讀取證據，不把本機結果當主機結果。
2. **鎖稿與成本**：將五份 treatment 轉成 worker 可讀、獨立查核的六章企劃；逐章核來源、畫面句、片頭 40–50 秒懸念、約 13 分鐘正文、5 秒品牌片頭、21 秒品牌片尾；核付費餘額、重試上限與整支成本上限。每支先做少量連續畫面試看，再批量產圖。
3. **只在無衝突且獲批時啟動**：先做上述 import dry-run、留 JSON／狀態回讀，然後才決定 apply 的明確批次。工人依序 `brief/series` → 六章 writer、verifier、listener → `video.json`／claims／lint → TTS／長度／check-audio → keyframes／分鏡 → render／靜圖運鏡／music／assemble／captions → QA／package。遇來源不足、額度不足、事實改動或品質退回，保留同 slug 的章稿、`auto.json`、費用與失敗收據，不換號重買。
4. **真人驗收與上架**：量旁白與成片各自時長、FFprobe 格式、字幕同步、畫風一致、v4 pin、來源主張、全片播放；留下 `qa.json`、成片 SHA、實際花費與重做率。站主看完成片之後，私密上傳、Studio 可點結束畫面、公開／排程與站主接受都各留獨立證據。

## 5. 圖像基本成本假設

[Google 官方 Gemini API 價目表](https://ai.google.dev/gemini-api/docs/pricing)現列 **Gemini 3.1 Flash Image 標準付費輸出 1K：US$0.067／張**（1,120 輸出 token；不是 0.5K 的 US$0.045，也不是 Batch 價）。[原故事規格](../STORY.md)選這個模型，按[工人每章配額](../../../tools/video/automation/story.mjs)估約 89 鏡／集。僅以每鏡一張成功輸出的基本費計：`89 × 5 × 0.067 = US$29.815`，顯示為 **五支約 US$29.82**，每支約 US$5.96；若每支產出 120 張含重做，則 `120 × 5 × 0.067 = US$40.20`。89 與 120 都是估算，不是生成紀錄。

此數**不包含**輸入文字／參考圖 token、文字／thinking 輸出、查核與聽眾 judge、TTS／音訊檢查、配樂、縮圖／畫面變體、失敗或額外重試、改 2K 的差額、平台稅費及匯率。每支 US$25 的原試作上限是**整支實支費用**上限，不能拿圖像小計證明達標；製作前須依當時價目、配置、待結算請求和實際帳本重新估價並停在可控制的批次。
