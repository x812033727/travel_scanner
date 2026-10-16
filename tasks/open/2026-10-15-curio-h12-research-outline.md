---
id: 2026-10-15-curio-h12-research-outline
title: Curio H12 research and outline
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-15T16:34:42Z
completed_at:
branch: codex/curio-next-five-20261016
depends_on: []
scope:
  - docs/videos/curio-h12
---

# Curio H12 research and outline

## Why

站主要求繼續製作五集奇聞檔案局；本票負責 H12 弗蘭南燈塔的本次來源查核與可選大綱，避免把後世文學場景當作當年現場。

## Definition of done

- [x] 保存本次重開來源的 research.md、逐項 claims.md 與可供選擇的 A/B brief.md。
- [x] 另一位查核員覆核事實與大綱，修正有依據的問題。
- [x] 協調者完成原大綱的站主選綱交接。
- [x] 2026-10-16 續作核准 A 的完整正式稿、逐景提示、claims、loops 與兩支 Shorts 稿。
- [x] schema／lint 與 Shorts 結構檢查通過，作者本機驗證收據落地。
- [ ] 正式稿由另一位查核員與盲評者覆核，協調者套用修正後送站主。

## Steps

- [x] 閱讀 curio-episode、youtube-video、故事主線／開場／十三題及 H01-v2 前 30 景。
- [x] 唯讀承接題庫 H12，重開 NLB 當年文件、Gibson 原詩及 NRS 2026 展覽公告。
- [x] 寫兩個約 10 分鐘大綱、各至少三個開場鉤子與回收預案。
- [x] 獨立覆核。
- [x] 依站主核准 A 寫完整稿；「獨立覆核」的已勾項只指原大綱，不涵蓋這次正式稿。
- [ ] 完成正式稿的獨立查核、聽眾審稿與十三題盲評。
- [x] 回應初輪獨立退修：夜間畫面、信件主線、刪除旁枝；重跑機械檢查並交新查核／盲評。

## How to verify

檢查三份文件的來源 ID 與 claims 對應，兩案時間各 600 秒；人工確認詩中餐桌沒有被當成最初現場。協調者統一執行 `git diff --check` 與 `npm run check:tasks`，避免平行改動時重複驗證。

## Notes

- 本次查核日期為 2026-10-16（Asia/Taipei）；任務工具以 UTC 產生 2026-10-15 的票號，未改票 ID。
- 題庫來源提交 `949bb91fc85d41a53633d056062b27d87651e9d5`；沒有修改共享題庫。
- 1929 神祕日誌的傳播鏈本次未重讀原刊，不放進推薦案的具體斷言。已重讀的 1912 詩只證明文學文本存在，不主張詩是所有傳說的唯一源頭。
- 110 英尺是器材箱位置，不是量得的浪高；海浪說標為 Muirhead 的最可能解釋。
- 2026-10-16 01:01（Asia/Taipei），協調者完成手動大綱送審並讀回 `pending`；review ID：`d5fae6fa-4eb7-412e-973b-5713ea63e14b`，對應 brief SHA-256：`FF4AF2F817BD382943EA3EEF63AAD97962DB04C8B0D8FEBAC1373C81952E80EB`。送審版 brief 未再修改。
- 交接完成，釋出本票認領；仍待站主選 A／B 大綱，以及本批 US$30.00 估算停手上限授權（尚未核准）。正式生產尚未開始，沒有付費請求或 worker 啟動；本票未標 done，整集尚未完成，由協調者統一 commit／PR。
- 2026-10-16 獨立覆核由另一集作者完成，協調者轉交意見；已明確分開 ARCHTOR 15 日午夜過船通報與岸上 Return Book，避免混成同一觀察。研究／大綱版已凍結供站主選擇，不代表正式稿十三題已通過。

### 2026-10-16 正式稿續作

- 協調者讀回原 review `d5fae6fa-4eb7-412e-973b-5713ea63e14b` 已核准 A；五集本批每集 US$6／總 US$30 已授權，紀錄在 `docs/videos/curio-next-five-20261016/decision-20261016.json`。本票重新以 `codex-curio-h12-m09-scripts` 認領。
- 原核准 brief SHA：`ff4af2f817bd382943ea3eef63aad97962db04c8b0d8febac1373c81952e80eb`。現行 lint 要求「問題／一句答案／站主觀點」，host 要求「大綱」；協調者授權補欄位並更新選項外核准／預算狀態。A／B 正文到文末逐字比對原版一致；新 SHA：`155eb4940fdfacf015266a5670d7f70a67ced26beab0981bec8f0feb790ab778`。新版由協調者重送，不能沿用舊 hash 當新核准。
- `video.json`、`script.md`、`loops.md`、`shorts.json` 完整落地。98 景／100 句、93 插圖景，七章，估約 9.2 分鐘；不是合成後實測。NLB 原始文件再讀，新增救生圈綁繩、風向比較與後續處置的 C18–C19。
- 本機 `lint` 零錯誤；3 個位置關鍵詞頻率警告保留，因故事固定在同一燈塔，鏡頭已跨船、屋內、紀錄室、西側與展廳。三個開場鉤子與回收景 prompt 完全相同，來源 claim ID 完整；兩支 Shorts schema 與母片 shot 引用均通過。詳見 `script-validation.json`。
- 待正式稿獨立查核與十三題盲評、補格式大綱重核准、正式劇本核准。作者未發付費請求、未送後台、未啟動 worker，未新增發音字典詞。僅提交本票及 H12/M09 文件範圍，保留進行中供覆核修訂。
- `npm run check:tasks` 通過（1895 票，既有過期認領及其他 scope 重疊警告保留）；本次文件 `git diff --check` 通過。正式稿 SHA-256：`c4cf11d72124ac99c617ef6e7fff0bce3930f432f07332bdaf0d777ebef718c6`。

### 2026-10-16 初輪退修回應與獨立重驗交接

- 補格式新版 brief 已讀回 `approved / A`，review `d1594b9a-25a2-48de-bfa7-5916ace5e5b9`；讀回見批次 `format-decision-20261016.json`。brief SHA 仍為 `155eb4940fdfacf015266a5670d7f70a67ced26beab0981bec8f0feb790ab778`，本輪未改。
- `passing-ship` x5ik 改為 ARCHTOR 15 日午夜普通過船，`relight-night` bkys 改為 26 日晚點燈。NLB 信與報告相關段再次實讀。
- 以同一封穆爾信作全片可持續追蹤的物件，章間轉場直接連到信中搜索、西側、衣物，再對讀調查和詩作；不虛構信件遞送。刪除 usc4、9vpq、um28 三段旁枝。全部改句／畫面與刪句 ID 見 `revision-1.json`。
- 修稿 SHA-256：`429edd65822936cd682593be8c89fe0903f2186fc0cd7549ac392685807689a9`。95 景／97 句、90 插圖景，估 09:03（未合成）；schema／lint 0 error，3 個已說明的地點詞頻提示，Shorts 引用、主張表、開場同圖回收均通過。收據 `script-validation.json` 為作者機械驗證，不是獨立通過。
- 下一位獨立查核者接手本 scope 寫 `verify-1.md`，另需新十三題盲評。初輪結果曾退修，本輪作者不自判通過。尚未正式劇本送審或付費：paid calls = 0、worker starts = 0；每集 US$6／整批 US$30 授權仍有效，但不跳過劇本核准。此票保留 open 待覆核，不 done。

### 2026-10-16 正式稿獨立事實覆核第 1 輪

- `docs/videos/curio-h12/verify-1.md` 逐列檢查 207 個旁白、畫面文字／提示及上架文字項目；綁定 `video.json` SHA-256 `429edd65822936cd682593be8c89fe0903f2186fc0cd7549ac392685807689a9`。一手史料已重新讀取，ARCHTOR 午夜十五日過船、二十六日晚點燈與 110 英尺器材位置的初輪退修已通過。
- **事實 HOLD：** `exhibit-new` 句 `6fu8` 的「人們仍能回到那張紙面前」會讓 2026-10-16 聽眾以為原信現仍可到場觀看，但蘇格蘭國家檔案館公告的展期已於九月結束。待作者改成明確過去式，再以新版 SHA 複核；查核者沒有修改正式稿。獨立 lint 0 error、3 個地點詞頻 warning；票仍 open 供敘事退修、重新盲評與站主劇本核准。
