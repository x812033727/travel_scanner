# C08 short-v8 後台劇本入口與正式站交接

2026-10-24。此收據只準備非付費、非寫入的短版審稿入口；不代表正式站已重匯入、已審稿、已配音或可上架。

## 精確核准邊界

- 站主核准 PR #1811 的 36 句／36 鏡 C08 v8 短版。核准原件 `docs/videos/story-everyday-kikkoman-c08/reviews/v8-short-narration-candidate-20261024.md` SHA-256 為 `040d9a499ddb864f62ebf0edcc948cc58439ffa13d0dae0ce5a9475297ee5d69`；其檔內「候選／HOLD」為核准前的歷史狀態，後續站主核准另有對話紀錄。
- 頂層可匯入投影 `docs/videos/story-everyday-kikkoman-c08-short-v8/script.md` SHA-256 為 `07cc18d1d90e6eba679a699f0243d977717f896b924158ab251fb390a308c0b9`。核准原件、投影及同 slug `video.json` 的 36 個 ID／可見旁白逐一同序，0 差異；畫面原件 SHA-256 `0676e76a4c9d49b12ece74df1835a72ce264eabb24a3158635921f57244dd241`，原獨立來源／畫面覆核見舊專案 `reviews/v8-short-independent-review-20261024.md`。
- `approved-scripts.json` 只把 C08 的現行入口由舊 84 句切換到新 36 句。舊 `docs/videos/story-everyday-kikkoman-c08/`、原 SHA `b9e4c547ffa190609b433d48ff7e27a94b9c9df4322aeb48104a3163694b3376` 及後台既有審稿卡均不刪除。`script-intake.mjs` 僅為精確 C08 短版 slug、固定原件與投影 SHA、36 句及六章格式開例外；其他劇本維持舊規則。

## 正式站只讀讀回與執行順序

同工作輪由主協作者以既有本機 video-tool token 對正式站做唯讀 GET：系列為 `paused`；C08 第 8 列為舊 slug `story-everyday-kikkoman-c08`、`planned`，舊 project 有 approved script SHA `b9e4c547...`，新 `story-everyday-kikkoman-c08-short-v8` project 為 404。沒有正式站寫入。C20 與本票無關。

1. 本機 `node tools/video/review/script-intake.mjs --id C08` 只回 `dry-run-local-only`，36 句、投影 SHA `07cc18d1...`；**此命令不連後台**。
2. 正式站匯入前再讀 `paused` 系列、20 列及 C08 planned/舊 slug／無 request，也讀短 slug 是否衝突。以目前已獨立認證的 20 列 `stories.json` SHA-256 `2d30b13b5d15b9f9072f5c1ebc98ef64d34eb41d0e770954e31d291610d324c9` 執行正式站**只乾跑**，要求 `update=[C08]`、`create=[]`、零問題且其他 19 列無變動。此乾跑尚未進行。
3. 另行授權的同列 apply 必須保留第 8 列的資料庫 ID 與舊歷史 project。改成新 slug 後，進度查詢會依新 `(episode.number, episode.slug)` 找審稿卡，因此舊 84 句 approved 卡不會算在新列，`scripts_approved` 可能暫降 1。
4. 必須先讓新 slug 已是正式站同列現值，`script-intake --id C08 --apply` 才能通過 paused/planned/slug 預檢。此命令只建立新 slug 的**pending**手動劇本卡；後台另行審核新卡並讀回 SHA／36 句後才可計為 approved。任一步失敗均停止，不靠舊 84 句核准卡冒充新版。

本票沒有呼叫正式站 import apply、script-intake apply、TTS、圖片、配樂、上傳或發布。C08 繁中試片的 US$25 核准不解除獨立帳本、舊費用與供應商實價 HOLD。

## 本機驗證與獨立覆核

`node tools/video/review/script-intake.mjs --id C08` 回 `dry-run-local-only`、36 句與上述投影 SHA，未呼叫網路。`script-intake.test.mjs` 在補齊負測試後 11／11 PASS：包括被改的原件／投影／機器旁白、近似 slug、章序與破損條列、正式站仍為舊 slug 時 1 次 GET／0 寫入，以及新短版 pending 卡與舊 approved project 並存的本機模擬。後兩項只是注入 transport 的測試，不是正式站乾跑或後台卡。

非作者代理先以精確稿件與當時程式 diff 唯讀重核：核准原件、投影與 `video.json` 的 36／36 文字與 ID 相同，精確 C08 例外未放寬其他集數，原四項負測試及舊 slug 0 寫入測試 PASS。代理建議再拒絕章內破損 `-` 行並測新舊 project 共存；作者隨後新增這兩項守門及測試。主協作者 `/root` 於 2026-10-24 08:40 UTC 作第二次非作者唯讀覆核，對 PR #1823 最終 diff（包含這兩項補強）判無 blocker，並獨立重跑 11／11 測試、C08 本機 36 句乾跑與 `git diff --check`，均 PASS。這仍非正式站乾跑、整支影片或付費驗收。
