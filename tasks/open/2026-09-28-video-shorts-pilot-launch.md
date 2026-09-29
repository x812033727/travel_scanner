---
id: 2026-09-28-video-shorts-pilot-launch
title: Video shorts P1: the three pilots through the Shorts tab, the first uploads and the first numbers
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-28T03:35:00Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-shorts-tools-push
  - 2026-09-28-video-shorts-web-routes
  - 2026-09-28-video-shorts-admin-tab
  - 2026-09-28-video-shorts-youtube-auto
scope:
  - docs/videos/SHORTS.md
---

# Video shorts P1: the three pilots through the Shorts tab, the first uploads and the first numbers

## Why

第一期的四張票做完之後，要在正式站走完一次：三支試片（PR #871）從這台電腦送上站、自動品管、排進時段、站主上傳到 Studio、網站認領並排程、公開、讀到第一批數字。設計裡有幾件事只有真的頻道回答得了（`2026-09-28-video-shorts-youtube-auto` 的 Notes 列了五項），門檻常數也要對照實際結果調。

這張票取代 `2026-09-27-ai-shorts-owner-review-studio-launch` 裡「站主用命令列追蹤」的那幾步：排程、成效、花費改在 Shorts 分頁做；那張票的其餘項目（頻道基準匯出、90 天的每週選題）仍然有效。

設計全文在 `docs/videos/SHORTS.md`。

## Definition of done

- [ ] 前四張票已合併並部署（部署走 skill `deploy`，要站主同意）；遷移在 head、Shorts 分頁打得開、工人的 `tick` 有在回報。
- [ ] 站主做完一次性的四件事（`SHORTS.md` §站主要做的事 第 1–4 項）：頻道立場、連結頻道、帳號權限、自動上架授權與開跑日期。
- [ ] 三支試片用頻道聲音重做（`build --speech server`），`check-audio`、`qa`、`package`、`push` 都過，出現在片庫並自動排進前三個時段。
- [ ] 站主下載這一批、拖進 Studio、按「我上傳好了」；三支都被認領，標題、說明、字幕、揭露、排程時間在 Studio 核對無誤。
- [ ] 三支在排定的時間公開；第 1、3、7 天的數字出現在成效區。
- [ ] 五項實測（草稿讀不讀得到、`fileDetails.fileName`、取消排程、相關影片、未稽核專案的字幕與排程）的結果寫進 `docs/videos/SHORTS.md`，取代「實測後決定」的說法；結果跟程式的假設不同的另開票。
- [ ] 實際的花費、每支的機器時間、品管沒過的項目與原因寫進 `docs/videos/SHORTS.md`；門檻要不要調，寫下決定。

## Steps

- [ ] 部署前唯讀預檢；部署；驗證。
- [ ] 先用一支私人的測試影片走一次認領、排程、撤回，確認不會動到頻道上其他影片。
- [ ] 三支試片重做並送上站。
- [ ] 站主上傳與授權；觀察第一週。
- [ ] 把數字與實測結果寫回文件。

## How to verify

- `/admin/videos?tab=shorts`：月曆上三個時段是「已公開」，成效區三列各有第 1、3、7 天的數字與來源。
- YouTube Studio：三支影片的瀏覽權限、排程時間、字幕語言、「變造或合成內容」。
- `docs/videos/SHORTS.md` 沒有留下「實測後決定」的句子。

## Notes

- 這張票不是上架的授權：公開哪一天由站主在 Shorts 設定選；授權卡由站主自己按。
- 試片的腳本（`docs/videos/ai-shorts/pilots/*.json`）不要改：`core.test.mjs` 綁著它們的雜湊。換聲音是 `build` 的參數，不是腳本的欄位。
- PR #880 的 12 支 Shorts 要不要一起接進來，等那個 PR 的去向決定；接的話用 `import`。
- **2026-09-29（站主問「有些影片還是 Shorts 沒出現在後台」）**：原因是這些影片從沒送上站，後台只列資料庫裡的影片。
  站主選了：三支試片用頻道聲音重做再送、#880 的 12 支 Shorts 原樣匯入當審片、#880 的 6 支長片寫匯入工具一起送
  （票 `2026-09-28-video-tool-import-a-finished-long`）。當天做完，21 支都在正式站、各有一筆成片審核在等站主：
  - 三支試片：`build --speech server`，旁白檢查被標的句子重錄兩輪。`shorts-poster-blind` 0 句；`shorts-receipt-total`
    剩第 4 句（「我給同一個人工智慧兩種問法」聽成「…，有兩種問法」）；`shorts-prompt-check` 剩第 6 句（「直接問的這組」
    聽成「直接問了這組」），意思都沒變。第一輪把「答案確實對」聽成「答案卻是對」，重錄後已過。qa 沒全過（頻道立場空白，
    policy 一定不過），所以沒有自動核准、也還沒排進時段；這張票的第三項要等站主核准後才算完成。
  - 12 支 #880 Shorts：`ai-real-world-0N-<集>-short-1|2`，內容線 `cut`，來源是同名長片。原檔 24 fps，先轉成 Shorts
    規格（30 fps、48 kHz、兩段式 −14 LUFS）才匯入得了（另開票 `2026-09-29-shorts-import-a-cut-that-is`）。
    旁白是 Windows Hanhan，沒跑旁白檢查（省全站共用的 Jev 額度）；說明欄的「完整影片」連結要等長片上 YouTube 才補得上。
