# 五支品牌故事｜製作前檢查收據

本機核對日期：2026-10-14；規格複核：2026-10-15（Asia/Taipei）。五支的範圍是本機 repo 與預設影片工作目錄；**未核對它們在正式站的資料庫狀態、未匯入、未執行付費模型，也沒有成片**。A01／B18 另有部分後台 UI 觀察，詳見[原試作票](../../../tasks/open/2026-09-28-video-story-pilot.md)，不可推論五支或試作的精確 live 狀態。站主已指定五支採 MiniMax `image-01`、`cute-mystery`、約 10 分鐘，並在 A01／B18 原規格試作完成後才做。本文件供安排五集製作時回讀，不能把表格的「本機不存在」推論成主機不存在。

## 1. 本機輸入與空白工作區

依 [影片工具的路徑實作](../../../tools/video/core/paths.mjs)，逐集文字檔位置為 `docs/videos/<slug>/video.json`，媒體位於 `<VIDEO_WORKDIR>/<slug>/`；本機沒有設定 `VIDEO_WORKDIR`，故使用 `<home>\mokaair-work\videos`。五個 slug 從[原 100 題已編譯清單](../story-plans/brand-stories-100/stories.json)回讀；A21 更正後重新編譯，該檔 1,415,413 bytes，SHA-256 為 `c8fb18102634459c62f556022139e0bdc733ef432321c412ff810faed0ac0194`。下表的兩項 `否` 是 `Test-Path -LiteralPath` 的本機結果。

| 題號 | slug | 原 100 題序號 | `video.json` | 工作目錄 |
| --- | --- | ---: | --- | --- |
| A29 樂高 | `story-lego-sold-legoland-to-survive` | 33 | 否 | 否 |
| A16 Costco | `story-costco-hot-dog` | 3 | 否 | 否 |
| A37 Adidas／Puma | `story-adidas-puma-brothers` | 47 | 否 | 否 |
| B14 味之素 | `story-ajinomoto-chip-film` | 8 | 否 | 否 |
| A21 品客 | `story-pringles-vat-case` | 9 | 否 | 否 |

對應的[五份 treatment 與觀看承諾](README.md)是編輯輸入；各題仍以原 `stories/<ID>.json`、`reviews/<ID>.json` 為已查核事實基礎。執行 `node tools/video/story-plans/validate.mjs --only A29,A16,A37,B14,A21` 得 `100 stories`、`0 problems`、`4 warnings`（A16、A21、A29、A37 的原縮圖字數或斷行）。這只檢查企劃結構與原 review 綁定，不代表五份新 treatment 的完整逐字稿已通過獨立查核。製作前須將新敘事逐句連回來源，對新增或改寫的事實再查核。

## 2. v4 品牌素材與本機工具

從 `<home>\mokaair-work\videos\_branding\current.json` 讀到的 index 與實檔：

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

`npm run test:docs-videos` 第一次在缺依賴時 131／137 通過；安裝依賴後用系統 Node 24.13.0 為 214／215，剩餘案例的子程序以 `3221226505` 退出。這是[既有 Windows Unicode 路徑遞迴複製問題](../../../tasks/done/2026-09-28-investigate-windows-native-crash-in-video.md)的同一症狀；依 [dev-and-ci 環境指示](../../../.agents/skills/dev-and-ci/references/local-env.md)只對本次命令改用 bundled Node 24.19.0，**215／215 通過，exit 0**，沒有修改或略過測試。當時 `npm run check:tasks` 為 exit 0；2026-10-15 本工作樹因 A21 已完成票同時留在 `tasks/open/` 與未追蹤的 `tasks/done/` 而失敗，這份重複完成票未提交。

## 3. 五份 treatment 與 story worker 的接線

[故事工作流程](../../../.agents/skills/youtube-video/references/story.md)與[工人實作](../../../tools/video/automation/story.mjs)顯示：工人向 `GET /video/automation/series/next` 取資料庫 episode `beats`，以六個固定 key `hook/origin/idea/engine/turn/now` 逐章撰稿；**不讀本資料夾的 Markdown**。目前 [CLI 匯入器](../../../apps/api/app/video_automation/story_cli.py)只讀完整編譯 JSON 的 stdin；[校驗／匯入規則](../../../apps/api/app/video_automation/stories.py)要求故事連號 `1..N`，`--limit N` 只取前 N 題，不能用 `--limit` 選 A29、A16、A37、B14、A21。因此把現有 100 題 `stories.json` 交給工人，既不能只做這五題，也不會採用本資料夾新增的開場、因果轉場和三句結尾。

**已完成的本機接線**：在不動原 100 題與 A01／B18 的前提下，另建[五集系列](series.json)、五份六章 row 與各自的新[獨立審稿](episodes/reviews)，由 [`build.mjs`](build.mjs) 編成 [`stories.json`](stories.json)。五題連號、各用 `story-five-*` slug、分列五天中午；`reviewProblems` 與 Python `check_story_file` 對完整輸入均為零問題。這些是**本機驗證**，正式站仍須唯讀 dry-run、查 live ID／slug／既有製作狀態，不能覆寫已開始的故事。新版 writer 已加入可愛畫風的「回答、故事相關留言、訂閱」三句與一人一動作插畫指示；它仍須在實際逐字稿、片尾 16 秒 Studio 元素及全片 QA 中逐項核對。

原 story 產線要求 12–15 分鐘、非空 `look.style`／`look.negative`，工人把 `video.json` 設為 `preset:custom`。本工作樹的[窄範圍修正](../../../tasks/open/2026-10-14-support-10-minute-minimax-cute-brand.md)已讓**另立的五集系列**採 10 分鐘、MiniMax `image-01` 與精確 `{"preset":"cute-mystery"}`，原 13 分鐘 Gemini 自訂畫風路線仍通過回歸測試。本機含角色的 A29 小樣之 `validateVideo`、`lintVideo` 無錯誤；這是合成小樣，**不是正式 A29 逐字稿或成片**。`curio-*` 專屬 lint 不自動套用 `story-*`，五支實片仍要另驗插畫 ≥70%、連續卡片 ≤3、單鏡提示詞和畫風。

五題本機輸入與 slug 接法已驗；A01／B18 試作及主機狀態仍待驗。在**已核准的主機環境**核對輸入 SHA 與 live 狀態後，才可用下列形式作唯讀匯入試跑；此處未執行，也沒有 `--apply`：

```bash
# <approved-five.json> 指本資料夾 stories.json 經主機端 SHA 回讀的完整編譯輸入，不是 README 或 treatment。
# 檔案從主機 shell 的 stdin 餵給 api；先核對其 series.slug 與 --series 相同。
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli video-story-import \
  --series <approved-five-series-slug> < <approved-five.json>
```

記錄 dry-run 的 `create/update/leave_alone/refused/problems`、既有作品差異、五個 slug 與相同 ID 的所有在製工作；有任何衝突就停止設計修正。`--episodes-per-day` 只在新建作品時生效，已存在作品須在後台確認。匯入後 `node tools/video/cli.mjs auto --once` 也只推進一個工作單元，不能當作一支成片的命令。

## 4. 主機、站主與實際生產關卡

[A01／B18 試作票](../../../tasks/open/2026-09-28-video-story-pilot.md)目前為 `blocked`，其勾選項要求：先在正式主機讓 A01、B18 到「可以上架」，站主看過；回填時長、張數、重做率、階段秒數、實際帳本、1K 清晰度與 token 用量。站主於 2026-10-15 明確決定這兩支先完成，五支新版接著做。原試作維持原規格，票明載正式站操作須站主同意，部署、上限、頻道立場、字幕語系、權限與主機狀態均須逐項核對。此前的[試作執行方案](../../work-status-2026-09-29-story-pilot-plan.md)也只是一份未執行的方案，不能當作 live 收據。五支尚無正式站逐集狀態回讀；A01／B18 只有試作票記錄的部分後台 UI 觀察，未核實 live 版本、餘額或帳本。沒有改正式設定或驗帳；不自動觸發五支或每日兩支 rollout。

在接線完成且取得該階段的站主決定後，五題每支按同一張收據走：

1. **主機前檢**：核 live SHA、API／worker 版本與映像、release hold、資料庫備份／migration、既有 `brand-stories` 與五個 ID／slug／狀態；查帳號、`content.manage`、AI 漫劇開關、頻道立場、常設指示、繁中聲音、字幕語系、模型路由、TTS／judge／圖片額度、每日與同時進行上限。保留去識別讀取證據，不把本機結果當主機結果。
2. **鎖稿與成本**：將五份 treatment 轉成 worker 可讀、獨立查核的六章企劃；逐章核來源、畫面句、片頭 40–50 秒懸念、約 10 分鐘正文、5 秒品牌片頭、21 秒品牌片尾。核 MiniMax `image-01` 實際單價、餘額、重試與整支成本上限，按整集一次核定；已定畫風不為選風格再買樣張。需要驗分鏡連貫性時用連續鏡頭試看，再批量產圖。
3. **只在無衝突且獲批時啟動**：先做上述 import dry-run、留 JSON／狀態回讀，然後才決定 apply 的明確批次。工人依序 `brief/series` → 六章 writer、verifier、listener → `video.json`／claims／lint → TTS／長度／check-audio → keyframes／分鏡 → render／靜圖運鏡／music／assemble／captions → QA／package。遇來源不足、額度不足、事實改動或品質退回，保留同 slug 的章稿、`auto.json`、費用與失敗收據，不換號重買。
4. **真人驗收與上架**：量旁白與成片各自時長、FFprobe 格式、字幕同步、畫風一致、v4 pin、來源主張、全片播放；留下 `qa.json`、成片 SHA、實際花費與重做率。站主看完成片之後，私密上傳、Studio 可點結束畫面、公開／排程與站主接受都各留獨立證據。

## 5. 新畫面路線的基本成本假設

[原故事規格](../STORY.md)選 Gemini 3.1 Flash Image，但那是 A01／B18 和原 100 題規格，**不再用來估這五支**。[奇聞檔案局 skill](../../../.agents/skills/curio-episode/SKILL.md)依 H01、L08 收據記載 MiniMax 插畫連 judge 約 US$0.0135／張，整集約 75–120 張、畫面約 US$1.5–3。照相同路線粗估，五支畫面約 **US$7.5–15**；品牌故事實際張數與重畫率未測，故這只是過往集數的預算參考，並非站主授權、供應商當前報價或已支出。

此數**不包含**文字／thinking 輸出、逐章查核與聽眾 judge、TTS／音訊檢查、配樂、縮圖、額外重試、稅費及匯率。A01／B18 的每支 US$25 上限是**原試作整支實支費用**上限，不能拿五支的畫面小計代替；五支開始前也須按當時模型價目、完整流水線與站主核定的整支上限重新估價，完成後對帳。
