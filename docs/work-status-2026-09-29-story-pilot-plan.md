# 2026-09-29：兩支品牌故事試作方案

本次完成站主要求的「依賴就緒後準備試作方案」，沒有正式連線、設定、匯入、建立工作、生成、上傳或發布。原[試作票](../tasks/open/2026-09-28-video-story-pilot.md)仍保留；本文件的步驟與金額是待確認方案，不是已執行紀錄。

## 版本與指定試作件

[PR #933](https://github.com/x812033727/travel_scanner/pull/933) 已於 **2026-09-29 02:49:56 UTC** 合併，merge／本次查詢 main 為 `157cca889a169ebf9f0af4f609be69388b8f6d2e`；final head `345d8e9926d79b107e23db560b4fdf8cc96db2e0` 的 api、web、containers、full-stack-smoke 全部 SUCCESS。GitHub compare 證明此 main 在 #938 merge `0cfcfdc126db3a6f4ed3f3fc2136816ba8045761` 之後（ahead 1、behind 0），故同時包含工人與政策／語系依賴。#909 的 backlog 也已在此提交中。

這是**製備基準**，不是已核准部署 SHA。正式執行前選定包含上述依賴及必要修正的提交、API／worker image digest，核對當次 CI、live revision 與 migration。若選定版本含 #966 startup token guard，須先完成經批准的 API/web 配對配置；本輪快照兩者 token 均未設定，不能直接部署該修正。只記錄 presence／長度／一致性結果，不輸出值。

兩件同屬 `brand-stories`，不是兩個作品；影片格式 `drama`、作品種類 `story`。目標13分鐘、16:9、Flash 1K、全靜態卡通圖加運鏡、只有旁白、不做合集、不加多語配音。

| 順序 | 企劃／影片 slug | 暫定題目 | 原排程欄位 |
| --- | --- | --- | --- |
| 1 | A01／`story-rolling-suitcase` | 人類先登上月球，輪子行李箱才賣得起來 | day 1、12:00 |
| 2 | B18／`story-conveyor-belt-sushi` | 啤酒工廠的輸送帶，轉出了迴轉壽司 | day 1、20:00 |

原排程僅是企劃資料，不授權當日自動上架。製作每日最多一件，以 Asia/Taipei 日期計；A01經站主看完並核帳後才加入B18，必要時隔日製作。

## 已固定的本機輸入

根目錄為 [brand-stories-100](videos/story-plans/brand-stories-100/README.md)。下列 SHA-256 為 **Git 提交中的原始 LF 位元組**，已與本機逐檔相等；匯入時再核對部署檔案，不能只比名稱。

| 相對檔案 | SHA-256 |
| --- | --- |
| `stories.json`（1,414,653 bytes） | `6f1e4619c7bf5847b1b67a21b5e97dd015ccef939fbf19c098c33178840dce26` |
| `series.json` | `8dfc3e57399dd034733b418cdca88ac528fd4a3f0a6b5ddacc8fd2c8a65f2da7` |
| `schedule.json` | `a9fc56847c70c433084c34b377cd384d1ec42282e4925a0fd8baa4348ada3fae` |
| `stories/A01.json` | `d4f8fd5b3dbf21bac4949a12e32f3538fdd71b328c7951b9a536e0664235cf7f` |
| `stories/B18.json` | `5c2221ac9b03e3ef4d040df36a31d0d1f8756b492dc7d3229f93771978ee3aa9` |
| `reviews/A01.json` | `7b0333f9abf7b58f364c2d5b2cb677db928084cd7bfd07c8094e94d8d78ac963` |
| `reviews/B18.json` | `8e3c99abf90f28fb10953eb5c33b545b7f57945a96350e67af05252eae2fe71b` |

Node 24.21.0 執行 `node tools/video/story-plans/validate.mjs`：100 stories、50 days、**0 problems，exit 0**。只驗本機企劃與審稿綁定，未重抓來源或呼叫模型；正式寫稿前針對 A01/B18 重讀來源及 caveats，新增事實另行查核。可先在本機執行 `validate.mjs --only A01,B18 --fetch --report <PRIVATE_EVIDENCE>/source-read.json` 留來源讀取證據，這不是成片查核。

## 啟動前設定與門檻

設定名稱以 [settings schema](../apps/api/app/video_automation/schemas.py)、[故事工人操作](../.agents/skills/youtube-video/references/story.md) 與 [STORY.md](videos/STORY.md) 為準；這些是擬採值，沒有改正式設定。

| 項目 | 試作要求／停止條件 |
| --- | --- |
| 站主與權限 | 在後台確認 AI 漫劇啟用、頻道立場、常設指示、旁白聲音、核准的訂閱帳號／媒體供應商及 `content.manage`；登入、金鑰與同意由站主處理。不得切到未批准的付費 API |
| 作品欄位 | `brand-stories`、`kind=story`、`target_minutes=13`、`hands_off=true`、`visual_tier=stills`、`compilation=false`、`image_model=gemini-3.1-flash-image`；look沿用固定series檔，無吉祥物。改2K另由站主決定 |
| 節流 | `episodes_per_day=1`、automation的 `drama.series_max_in_flight=1`；前者只在新建作品時由import覆寫。既有作品須先核其值與其他ready/started工作，不能靠再次import改設定或排除舊工作；若已有其他故事，先另行安排可隔離的核准時段 |
| 預算 | **全片接受上限每支US$25，兩支最多US$50**。`drama.max_usd_per_video` 是media估算上限，0表示不限制；建議試作設20並為旁白／Jev／judge等另留最多5美元，須按當日價目、重做上限與未結算請求核實餘額，不能把這個配置當總額硬保證 |
| 已知預算缺口 | [image-model-pricing票](../tasks/open/2026-09-28-video-story-image-model-pricing.md)仍open：工人估價／快取模型可能與作品實際模型不同；付費前完成修正及回歸。media ledger也未涵蓋TTS／文字模型全部成本，judge記帳不逐次呼叫spend；若無法證明保守預留及下一階段最壞花費仍在25內，停在dry-run，先補控制及排演，不能調高25來通過 |
| 其他上限 | 逐項核對圖片與judge月額度、`drama.series_episodes_per_month`、旁白月字数、Jev每日次數、審核檔案大小，以及既有工作已用／已預留量；只申請本試作所需增量，不套用每日兩支／每月60支的rollout值 |
| 真人關卡 | `drama.drama_auto_approve_final=false`，兩支都由站主播放／核准；hands_off不繞過此設定。保留既有旁白品質門檻，不以自動QA取代人審 |
| 語系與公開狀態 | `drama_caption_locales` 只填 `en, ja, ko, zh-CN`；zh-TW基礎字幕自動包含，不能把zh-TW填進此設定。合計符合原規格五語字幕及標題／說明翻譯，無配音。先前已決定的語系不由伺服器覆寫；逐片核對持久化決定。停在可以上架，不上傳、不公開、不排程 |
| 保留與共用影響 | 未上傳前保留媒體、chapters、auto/state及成本證據；啟用清理前只做已批准的tidy dry-run。上述drama設定會影響其他作品，先記原值並確認沒有衝突，不暫停或重啟其他工作來騰空 |

## 經站主逐步同意後的執行順序

1. **預檢與備份**：按[deploy技能](../.agents/skills/deploy/SKILL.md)與[release hold規則](../ops/release/README.md)核對四鎖、hold、其他release、資源、live SHA、映像、migration、worker連線與磁碟；在第一筆寫入前留備份SHA並通過 `pg_restore --list`。不清他人的hold。選定版本必要時先部署、驗健康；這份方案沒有授權部署。
2. **資料與能力核對**：確認既有 `brand-stories`、兩個slug及集數狀態；已開始／已完成者不得重建或改slug。讀來源、model routing與設定只回非敏感結果；實際媒體供應商和全靜態clips依賴均須可用。CLI從stdin匯入不經nginx；若選後台匯入，先核實host body limit大於1,414,653 bytes及JSON envelope，不能只信repo範例。
3. **試跑兩件**：於核准host repo根目錄，以固定 `stories.json` 跑下方無apply命令。預期只列A01/B18、無refused/problems，確認create/update/unchanged及每日1；已有其他episode或結果不同即停，保存完整去識別報告。
4. **先做A01**：確認上表預算與設定後，僅apply `--limit 1`。新作品建立即active、集數ready，工人可能立即開始，因此設定／預算必須先完成。既有作品的設定不會被import覆寫。驗資料只有批准的一件新工作；重跑dry-run可為unchanged或已啟動的started/leave_alone，只要沒有新create/update/refused、沒有problems且原ID不變。禁止匯入全100件。
5. **逐階段觀察**：brief/series → 六章writer → 獨立verifier → listener → script核准 → 有cast才look → TTS／長度／音訊 → keyframes／分鏡 → render／clips manifest／music／assemble／五語CC → QA／package。保留每次stage時間、重做及費用；一章事實改超過3項依工人再查，NOT FOUND不得留稿。來源失效、預算不足、quota或帳號阻擋即停。
6. **A01驗收後再做B18**：站主看完A01、帳本總額不超25、所有接受條件通過後，再批准同一輸入 `--limit 2 --apply`，預期A01保留、只新增B18。每日1可能等下一個台北日，不臨時調2。此分兩次匯入落實原票前兩件，避免A01技術done後B18在真人確認前自動啟動。
7. **收尾**：B18同樣驗收並保留上傳包。把下表實測填回STORY.md試作紀錄與原票；兩支完成不授權七天rollout、每日兩支或YouTube操作。需要暫停作品／恢復共用設定時也確認既有工作及核准時段。

以下只是未執行命令；工作目錄、檔案與部署映像均須先核對：

```bash
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli video-story-import --series brand-stories --limit 2 --episodes-per-day 1 < docs/videos/story-plans/brand-stories-100/stories.json
# A01已批准的第一階段：
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli video-story-import --series brand-stories --limit 1 --episodes-per-day 1 --apply < docs/videos/story-plans/brand-stories-100/stories.json
# A01真人驗收後，重新dry-run limit2；另獲批准才以同命令limit2 --apply補B18。
```

`node tools/video/cli.mjs auto --once`只做一個stage，不代表完成一支影片。不要為了排演呼叫會領取或start工作的API；本機準備只讀檔與離線測試。

## 接受證據與失敗續跑

| 每支必填證據 | 通過條件 |
| --- | --- |
| 版本／輸入／狀態 | UTC、deploy SHA、API/worker digest、上表輸入hash、series/episode/slug、開始／完成狀態與核准人；私人ID保留私人收據 |
| 成片格式 | ffprobe：1920×1080、30fps、**720–900秒**。工人自動旁白容許11:30–15:30較寬，不取代原票12–15分鐘成片驗收 |
| 品質／畫面 | `review/qa.json` 全PASS、逐鏡 `checks.json` 均motion；所有聯絡表／logo/真人長相/無文字檢查、音訊與字幕同步；站主實看1K放大品質並決定維持1K或另批2K差額 |
| 事實與語系 | claims/verify、六章改稿紀錄、來源時間、聽審與五語CC／標題說明審查；旁白只有narrator，畫面prompt不含企劃names |
| 實測／成本 | 長度、鏡數、圖片數與重做率、逐階段秒數；合併media帳本與其他供應商／用量收據核帳，每支全費用≤25；另列文字/TTS/Jev/judge及訂閱token，不把訂閱用量換算成已付API費；記待結算量 |
| 上傳包／人審 | final.mp4大小和SHA-256、字幕／縮圖／metadata及package hash、持久化可以上架狀態、站主播放結果；沒有YouTube ID也是本試作的正常結果 |

失敗保留 `auto.json`、`story/chapters/`、已知job、素材hash和帳本，不刪工作區／不按放棄以換新slug；同ID續跑並先核對既有已花費與in-flight請求。修章時從chapters改起，重新查核／聽審／TTS／字幕，不直接改會被覆蓋的video.json。長度兩輪仍失敗、`no_more`、額度耗盡或來源不足交站主；不盲重試、不切付費API、不放寬原接受值。既有redo-dropped限制仍需原票追蹤。

正式收據與MP4/WAV、頁面全文、帳號紀錄存repo外；repo只回填去識別數字、hash、PASS/FAIL/BLOCKED與待辦。本輪驗證只完成依賴／Git祖先、本機企劃0問題、七檔Git位元組一致及設定原始碼核對，沒有聲稱媒體或主機已驗收。
