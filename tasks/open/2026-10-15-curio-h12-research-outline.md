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
- [x] 正式稿由另一位查核員與盲評者覆核，協調者套用修正後送站主。

## Steps

- [x] 閱讀 curio-episode、youtube-video、故事主線／開場／十三題及 H01-v2 前 30 景。
- [x] 唯讀承接題庫 H12，重開 NLB 當年文件、Gibson 原詩及 NRS 2026 展覽公告。
- [x] 寫兩個約 10 分鐘大綱、各至少三個開場鉤子與回收預案。
- [x] 獨立覆核。
- [x] 依站主核准 A 寫完整稿；「獨立覆核」的已勾項只指原大綱，不涵蓋這次正式稿。
- [x] 完成正式稿的獨立查核、聽眾審稿與十三題盲評。
- [x] 回應初輪獨立退修：夜間畫面、信件主線、刪除旁枝；重跑機械檢查並交新查核／盲評。
- [x] 回應第二輪獨立事實 HOLD 與嚴格盲評退修，完成定向改稿與零錯誤 lint；備妥新版供不同查核者與盲評者重驗。

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

### 2026-10-16 第二輪定向改稿

- 嚴格盲評在上一版指出 `no_spoiler`、`one_line`、`no_toc`、`no_recap`、`opening_hooks` 未過。新版開場只預告後來文字中的飯菜與倒椅，保留作者身分到詩章；穆爾信中的衣物觀察移到登島段，監督報告往後連續推進；刪除重複的 `no-loose-coil`，消除「讀哪份文件」式轉場。
- `6fu8` 改成「在那場展覽裡，人們曾親眼看見這封信」，館方展期已結束的時態問題已在作者稿件修正。NLB 原始信／報告與 NRS 展覽公告於本輪重讀；沒有加上未證實的事發畫面。
- 依原始 Muirhead 報告補兩個具體調查動作：停鐘不能單憑鐘面定失蹤日期；監督向實際瞭望的兩名少年詢問，再核對岸上逐夜記錄。這兩句緊貼「怎麼縮小時間／怎麼判斷沒看到燈」的主線，不重播原有結論；新場景與來源對應見 `claims.md` H12-C20、C14。
- 目前 `video.json` SHA-256 `5e46ddf2c3de77641a5ff17c9520255d5f3b003429a64ee1c1cb8c9cde39e859`；`script.md` SHA-256 `c8eb9a64ad6a24b170897a0d04b58684762aa8c9998d53f7cf2507ea4af40eea`。96 景／98 句、91 插圖景、七章，三個開場預告畫面與各自回收畫面完全相同，lint 0 error；估 09:06，已回到 9–11 分鐘目標，實際音訊時長未測。三項地點詞頻 warning 留給協調者判斷；沒有靠重述補時。逐項改動見 `revision-2.json`。
- 新版事實重驗與新一輪十三題盲評都**未完成**，不能拿上一版收據或盲評當通過；正式劇本未送後台、未合成旁白或插圖，付費呼叫 0。此票留 open 給下一位查核員與協調者。

### 2026-10-16 第二輪獨立事實覆核與敘事關卡

- 不同於第一輪的查核者重開 NLB 電報／穆爾信／繆爾黑德報告、吉布森 1912 年詩集及 NRS 2026 展覽公告，三站均用指定 editorial User-Agent 讀回 HTTP 200。對 `video.json` SHA-256 `5e46ddf2c3de77641a5ff17c9520255d5f3b003429a64ee1c1cb8c9cde39e859` 覆核全部 24 個第二輪改句及相關畫面，再以固定種子抽查 194 個現行場景文字／畫面資料中的 65 個。逐列證據與界線見 `verify-2.md`。
- 事實 **HOLD 一句 `i9ud`**：「一九一二年，吉布森寫下一首」把詩集出版年寫成創作年；一手書籍只證明 1912 年出版及收錄該詩，且說部分作品曾重刊。宜改「一九一二年出版的吉布森詩集，收錄了一首關於這座燈塔的詩」之類的出版／收錄說法，保留句 ID；查核者未改劇本。`6fu8` 展覽過去式、`s4hn` 停鐘、`k8sw` 兩名岸上瞭望少年都獲一手來源支持；沒有第二個事實阻礙。新版改字後須重新綁 SHA 查核。
- 新版十三題盲評另有 **`payoffs`、`no_recap` 兩題未過**，與事實覆核分開；關卡不能因事實修好而視為通過。已兩輪退修，協調者正向站主取得是否允許再作一次定向修正的決定。此票持續 open；正式劇本未送後台，付費呼叫 0。本查核者沒有改劇本、沒有提交後台或支付請求。

## 2026-10-16 站主授權的第三次定向去重

站主先後核准三處史實／回收修訂、刪除三個重複鏡頭，並在新版嚴格盲評 no_recap 仍未過後，另行核准一次限縮刪改。前兩次收據為 revision-3.json、revision-4.json；本次 revision-5.json 綁定當前 video.json SHA-256 4509E8B2C7B8E21001C2D738A877C71256BB13A557522408A3BB2F833C929ECF、script.md SHA-256 A51B99F496214712B21965D5F34BAA6DF93254D89C8D2ADBDCE224B6A5F2FEFF。本輪刪 3 鏡、改 7 句及一個畫面副標，移除 fbx9 → ecsy 的冗餘 loop；其餘 loop 保留。lint 0 errors／4 warnings，92 句、85 插畫景、估 8.6 分鐘。**目前仍待對此 SHA 的獨立事實查核及全新十三題盲評；劇本未送後台、未付費。**

## 2026-10-16 H12 第七版獨立複核

verify-4.md 的獨立事實與連貫性核對對 video.json DF094247…、script.md B07AE4FF… 判 PASS：NLB／Gibson 1912／NRS 原始來源重新讀回，90 景／92 句與 11 組實際回收吻合。與此分開，未讀前輪答案的嚴格 script-only 盲評對同一 script SHA 判 11／12 必答題；唯一未過 no_recap 在第 86 鏡 two-mysteries，重述前文已交代的失蹤上限與餐桌來源。站主已被問及是否只刪此鏡並把片尾第一句改成未結範圍的結論；未取得回覆前不改、不送後台、不付費。

## 2026-10-16 H12 第八版核對與待決去重

站主另行核准只刪 `two-mysteries`、把 `qv4y` 改為「『未結』只留給三人最後的遭遇，不代表後來每個細節都無從核對」。改動及兩個畫面提示的史實修正詳見 `revision-8.json`；現行 video.json SHA-256 F95964A7…、script.md E56C6322…、claims.md 4BD8C6EF…，89 景／91 句、84 插圖景，lint 0 errors／4 warnings、估 8.5 分鐘。獨立查核者重開 NLB、Gibson 1912、NRS 2026 一手來源，核實 11 組線索回收並對最終畫面提示雜湊確認 **史實／連貫性 PASS**。全新 script-only 盲評 **HOLD**：必答 `no_recap` 仍見門關著／反鎖、外套疑問、詩出版年份在近鄰鏡頭重述；其餘必答題過關。已向站主請示再一次限縮去重，回覆前不再改旁白、不送正式劇本後台、不付費。

## 2026-10-16 H12 第九版送正式劇本審核

站主核准將門的反鎖界線、外套疑問併到首次出現的句子，刪除重複鏡頭，保留文件比較畫面而不再重念年份。隨後刪去兩個不增加事實的角色修飾詞，將詩段橋句改為只往後走。獨立查核者對 `script.md` SHA-256 `3B9FCEA7933E0F6A2B2C680A8EADA40288C15E754042C4624DD81117D1FA6ED1` 判史實 PASS；新一位只讀劇本的盲評者判 13／13 PASS。三處畫面場景位置修正後，查核者另對 `video.json` SHA-256 `1AD357BBCB923FF8EA94444680BB931DBFC5874D7872E0CD636EFB7AAD94E21F` 判畫面 PASS。完整改動及哈希見 `revision-9.json`。

87 景／89 句、82 插畫景，`lint` 0 errors／4 warnings，估 8.4 分鐘（尚未合成實測）。`review-push --gate script` 已送 `/admin/videos`，exit 0；即時 `review-pull` 顯示 `script: waiting for the owner`。未合成旁白／插圖，H12 付費呼叫仍為零。後續要以後台讀回此版劇本核准後，才開始本集繁中製作；舊版審核或其他四集的核准不代替本版。

## 2026-10-16 劇本核准與繁中旁白製作中

站主回覆已在後台核准第九版劇本；`review-pull --gate script` 現場讀回 `script: approval recorded`，`status --slug curio-h12` 顯示 `script approved`。合成前 `tts --dry-run` 核對 89 請求、1,925 計費字元、Gemini Sulafat 可用。共用停手帳本已預留 TTS US$0.20、後續 Gemini 轉寫與 TypeSafe Jev 音訊 QA US$0.50，低於 H12 US$6 與五集 US$30 上限；TTS 正在逐句執行，尚未完成實測時長與音訊 QA，尚未送旁白後台。

TTS 已完成 89 請求、1,925 計費字元，正文時間軸 `14168/30 = 472.267` 秒；扣除 `ending-outro` 的 14.4 秒後，正文約 457.867 秒，未達 480 秒硬下限。US$0.20 在共用帳本以保守估額結算，並非供應商最終發票。此版旁白不送站主音訊審核，也暫不執行付費 `check-audio`；先增補約 35–45 秒有一手來源的新調查內容，完成獨立事實查核與十三題新盲評，改稿後重新送劇本審核，再只合成新增／改動的句子。原 89 句音檔保留供快取使用。

## 2026-10-16 H12 時長修稿暫停於盲評

保留第九版的 89 段既有音檔；尚未重錄、跑音訊 QA、產圖或送新版劇本。時長修稿草案在西側證據與事故推論增六景，並對既有 `wave-hypothesis` 改一行，現為 93 景／95 句、88 插畫景。`lint` 0 error／4 warning，估時 8.9 分鐘；這只是估算，仍要用新 TTS 驗正文是否達 480 秒。獨立史料複核 `verify-5.md` 與定向補查 `verify-6.md` 對現版 `script.md` SHA-256 `0A5D1B67B61D91B908B9592C2721D7A7F9A19CE4349790B7F6515E4112C744EF`、`video.json` SHA-256 `83BBB97BA70E38E387C0309073C996134F2E43D0B86DF33F7FBE5E1F033802C4` 均 PASS；`claims.md` SHA-256 `1A274FB94171014BA7110938D24E6A4246E027742A1C8B3326521E0CE4374725`。

新 script-only 盲評 `narrative-r14-answers.json` 對上述 script 只通過 11／13；`no_spoiler`、`opening_hooks` 因開場 `poem-tease` 提前說出飯菜與倒椅未過。之前兩次時長修稿盲評亦未全過；依 youtube-video/script-writing 的兩輪上限，本集停在這份未送審草案，已向站主請示是否另授權只修這一句並重新獨立查核與盲評。站主第九版核准不套用到本版，未獲新核准前不重錄或付費產圖。共用帳本 H12 累計保守估算 TTS US$0.20，音訊 QA 的 US$0.50 仍為未執行預留。

## 2026-10-16 H12 第十版送審與精確核准狀態

站主授權在新增六景後只改 `poem-tease`、`sequence-unknown`、`coiled-rope`、`document-card`、`letter-reader` 五句，刪除重複的 `letter-fate` 一鏡，並使開場畫面提示避開飯菜與倒椅。修改及雜湊詳見 `revision-10.json`；現行 92 景／94 句、87 插畫景，`script.md` SHA-256 `F423202B4FB6856FE39FA1CA9BC01473B4923555FE5823768AAFE108BB209AE7`。獨立史料查核 `verify-8.md` 對同版劇本／畫面／主張表判 PASS，全新 script-only 十三題盲評 13／13 PASS，CLI 匯入後判 storytelling panel passed。`lint` 0 errors／5 warnings、估 8.9 分鐘；這仍不是合成後時長。

最新版已送 `/admin/videos`，審核卡 `48a2ba6e-4da7-4234-83da-60617ad1f369`（2026-10-16 05:44:22 UTC）仍為 `pending`。站主回覆「已核准 H12 劇本」後再讀，後台實際已核准的是上一版 SHA `3B9FCEA7…` 的卡片，不能沿用到第十版。已請站主確認並核准 `F423202B…` 的卡片；在讀回該版核准前，不補錄、不跑付費 QA、不產圖。H12 已估 TTS US$0.20，音訊 QA US$0.50 仍僅預留；89 段舊音檔保留快取。正文八分鐘硬門檻仍待合成實測。

## 2026-10-16 H12 第十版旁白已送站主試聽

- 站主另行核准第十版；`approvals.json` 已讀回 `script.md` SHA-256 `F423202B4FB6856FE39FA1CA9BC01473B4923555FE5823768AAFE108BB209AE7` 的劇本核准，後台審核卡 `48a2ba6e-4da7-4234-83da-60617ad1f369` 也以唯讀 GET 確認 `approved`，決定時間 `2026-10-16T06:05:25.538745Z`。上節的 pending 是當時快照，不是現況。
- Gemini Sulafat 依核准稿完成 94 句時間軸旁白；本輪只新合成 12 句、沿用 82 句快取，新增 295 計費字元。`timeline.json` 的 `speech_hash` 為 `94b607cde96975de`，總長 15,049／30 = **501.633 秒（08:21.633）**；片尾前正文 14,617／30 = **487.233 秒（08:07.233）**，比 480 秒門檻多 7.233 秒。這是旁白實測，成片片長仍待日後 QA。
- `check-audio` 完成 94／94 句 Gemini 轉寫及一次 TypeSafe Jev 差異判讀：55 exact、10 sound、6 經 Jev 接受、23 句留旗標。另一套無稿 faster-whisper small 已逐句複核全部 23 旗標及六句未列旗標的原始差異；精確雜湊、分類及優先試聽句 `874p`、`wdik`、`3ncp`、`3w38` 見 `docs/videos/curio-h12/audio-qa-1.md`。兩套 ASR 不能代替站主聽感，尚未定向重錄。
- 音訊試聽頁已在 `<home>/mokaair-work/videos/curio-h12/review/audio.html`。`review-push --gate audio` 送出的音訊審核卡為 `a4eb23a3-3422-4523-ab42-a18caa4f5755`，綁定 `timeline.json` SHA-256 `EA4FB643E12F8077F9538D68D52614F8A1051A85FBD06AFD4A2922BF0E643465`；後台唯讀 GET 於本次交接仍見 `pending`（建立 `2026-10-16T07:54:59.668841Z`），`status --slug curio-h12` 同時顯示 narration not approved。**下一步等站主試聽並核准或指出需重錄的句 ID；在後台讀回對應雜湊核准前，不開始 H12 插畫。**
- 共用停手帳本對 H12 的保守費用估額為 **US$0.75／本集 US$6.00 上限**（首輪 TTS 0.20、音訊 QA 0.50、定向 TTS 0.05）；三筆均已列入估額結算，沒有仍佔用的 active reservation。這不是供應商最終美元帳單；其餘多語授權把五集合計上限提高到 US$34，不會改變 H12 本集 US$6 上限。

## 2026-10-16 新敘事題目下的 z4u3 定向修訂

- 站主同意只修 `z4u3`，並明確同意將已結束任務 `codex-gpt6-h12-targeted-revision` 的 H12 範圍認領移交；現由 `codex-gpt6-h12-final` 認領。不得把此授權擴大為其他句子或付費重錄。
- `z4u3` 只將提問「為什麼沒穿上就出門？」改成「外套能告訴我們誰先離站嗎？」；`3w38` 原句仍回答文件無法排出先後。`video.json` SHA-256 `4E1A03D2C79A642C1DB1E1BD03455626F78CAC704F75B2A8C7E561F40DC62409`，由工具再生的 `script.md` SHA-256 `D0CB64E23DB5CC45A88AB49A8E7B556BE6DEA6DB0D050924CFE39DEA41477C5D`。原始旁白與已核准音訊均屬舊版雜湊。
- 機械檢查 `lint` 0 errors／5 warnings、94 句；`npm run check:tasks` 與 `git diff --check` 通過。已重開 NLB 所載穆爾原信：衣物段記錄外套觀察，不能由此得知三人離站先後。**獨立史料查核與全新十三題盲評仍待完成；未送新版劇本後台、未重錄或產圖。**

### 追加授權：刪除 d4uq 重述鏡頭

- 站主另行同意只刪 `letter-reader` 一景／`d4uq` 一句，保留 `exhibit-first`／`3ncp`。已從 `video.json` 刪除整景，從 `claims.md` 的 H12-C03、H12-C16 場景映射移除，並以 CLI 重新產生 `script.md`。`loops.md` 及 Shorts 無該景引用，不需改。
- 最新 `video.json` SHA-256 `9C13AF1222552BCABCFBA4B0BE2D5BC8C3EA912F0A8CB2C93104DD8AC7B39E50`、`script.md` SHA-256 `8E7AF54E37406E9C16705CA074BA5628B8EC5B749ED8B98114AD178B2A5FEADF`、`claims.md` SHA-256 `A74A8BBB6952B6B78F9FCA6DFEF839F26D4BF2B792EC4F391145B13C9BCF9F02`。93 句／86 插畫景；`lint` 0 errors／5 warnings，估時 8.8 分鐘，`tts --dry-run` 僅 `z4u3` 一句待重錄，沒有付費呼叫。
- 依舊音訊時間軸，原正文 14,617 幀／30 fps；`d4uq` 佔 191 幀，純刪後正文暫估 14,426 幀＝**480.867 秒**，只比 8 分鐘下限多 0.867 秒。`z4u3` 新句尚未合成，實際正文長度必須在劇本核准後重錄並重新量測；此估算不能當最終合格證明。獨立史料與全新十三題盲評仍待此最終雜湊重驗，未送審、未重錄、未產圖。

### 追加授權：ds8v 明示史料歸屬，最新版送審準備

- NLB 轉錄的繆爾黑德報告稱船舶通報在失蹤消息發表後才送達；NLB 另一官方簡史則寫 12 月 18 日。站主同意只把 `ds8v` 改為「但繆爾黑德在報告裡說，這則消息是在失蹤被發現後，才傳到燈塔局。」`claims.md` 明列來源衝突，未將兩頁硬合併成一個日期。
- 最新 `video.json` SHA-256 `D16413FCD54ED2AA5FCFD12B88054FCF8B211AA96110C1514184467615AD3BF1`、工具再生 `script.md` SHA-256 `408E3C8BAAFC0063B0B53410B579D14BA09D650753DB466A409E59470F9A620B`。93 句、86 插畫景；`lint` 0 errors／5 warnings。另一位獨立審稿員先讀劇本，十三題全是，再查 NLB 當年紀錄與官方衝突；答案 `review/narrative-after-attribution-independent.json`，事實收據 `docs/videos/curio-h12/verify-after-attribution.md`。敘事結果已匯入且顯示 passed。
- 尚未對此新版付費重錄；舊時間軸對純刪的 480.867 秒只作估算，補錄 `z4u3`、`ds8v` 後必須再量測正文是否達 480 秒。
- `review-push --gate script` 已送最新版劇本至 `/admin/videos`；立即 `review-pull --gate script` 讀回「等待站主」，舊版核准對新版雜湊無效。下一步是站主核准 `408E3C8B…9A620B` 後再定向補錄。
- 站主明確核准 `408E3C8B…9A620B`；後台頁核對為最新 91 場／93 句卡，完成核准後 `review-pull --gate script` 讀回 `approval recorded`。`tts --dry-run` 僅 `z4u3`、`ds8v` 兩句需新合成，約 67 計費字元；在 H12 及全批額度內預留後才執行。

### 2026-10-16 最新音訊 QA 送審

- 兩句定向補錄後，`timeline.json` SHA-256 `792DC6C9D010FA7EE94884F7631CD3362D1496AF600A2BF7A14381A0D767F699`，`speech_hash` `6839b804e36ff7c7`；93 句總長 08:18.600，片尾前正文 08:04.200，實測超過 8 分鐘下限 4.2 秒。93 個 WAV 雜湊均與時間軸一致，只有 `z4u3`、`ds8v` 晚於舊版音訊核准時刻。
- `check-audio`：55 exact、10 sound、7 差異判讀接受、21 旗標；21 句都在舊版已試聽的 23 句旗標中，且都是原 WAV。`z4u3` 新句轉寫逐字吻合；`ds8v` 的「繆爾黑德」被 Gemini 辨成「繆爾赫德」，需要站主聽感判定。詳見 `docs/videos/curio-h12/audio-qa-2.md`；逐句頁已更新。
- `review-push --gate audio` 已送新版音訊，`review-pull` 讀回「現行版等待站主、舊版核准失效」。下一步請站主聽新錄的 `z4u3`、`ds8v` 並在 `/admin/videos` 核准最新時間軸，或指出實際錯讀；在該 SHA 核准前不開始 H12 插畫。本輪 QA 分流／送審未新增付費呼叫、未改共用費用帳本。

- 後台其後已核准最新版 `timeline.json` SHA `792DC6C9…F699`，`review-pull --gate audio` 讀回 `approval recorded`、`status` 顯示 narration approved。`keyframes --dry-run` 為 86 張 1K 插畫，每鏡先試一張估算 US$1.161；共用估算帳本先預留 US$1.25，才開始首輪 `--takes 1`。本輪尚在執行，已有少數圖評退件；須完成全輪、核對工具實際出圖／評審數與帳本後，再決定只修哪幾鏡及是否送分鏡後台。

## 2026-10-17 H12 分鏡送站主審核

- 六輪定向產圖後以同章已核准圖處理兩張退件：`slate-later` 明記回用 `slate-entry-3.jpg`（原退件保留），`extinguish-time` 用 `work-date-inference-1-trim.jpg` 快取圖並取得自己的 PASS 判讀；其餘選圖未重畫。選圖 manifest SHA-256 `F61238CD938140C8467501B376183A1865DC20D18DFCCC2FFA91504C26A475AB`，86／86 檔案雜湊正確、判讀通過，四頁聯絡表已重建；獨立逐圖覆核未見直接反向史實，但相近重圖和高度／位置表達較弱的鏡頭已列入 `docs/videos/curio-h12/keyframe-audit-3.md`。
- `lint` 0 errors；`status` 已標 keyframes drawn。共用停手帳本此時 H12 估算 US$4.185／6、五集 US$25.0295／39，實際供應商發票不可讀。`review-push --gate storyboard` exit 0，立即 `review-pull` 讀回 `storyboard: waiting for the owner`；**下一步等站主核准上述 manifest SHA 的新版分鏡，未讀回前不 render 或 assemble**。
- 站主已看過四頁聯絡表並核准這版分鏡；後台最新且唯一的 storyboard 卡 `bc2fce73-4e73-4105-8e58-bf4f41c5fb2a`，SHA 完全等於 `F61238CD…6A475AB`，核准時間 `2026-10-16T16:37:09.847333Z`。稍後 `review-pull --gate storyboard` exit 0 並記錄 `approval recorded`，`status` 已顯示 storyboard approved。可以接續本機 render／assemble；此核准不等於最終成片核准。

## 2026-10-17 H12 繁中成片送審

- 91／91 段成片及 97 cue 繁中字幕完成；8:44.6、`final.mp4` SHA-256 `2B24B5DF98A459CD587364C24D80FB0A7AFADFF4519DE86001B4A7D0E11D047D`。獨立抽看與合成收據無解碼、黑畫面或削波問題；詳細資料見 `docs/videos/curio-h12/final-qa-1.md`。
- 最終 QA 9／11：語言尚未選定時的英／日／韓字幕缺件，及 TypeSafe Jev「業配」0.36 超過 0.30。後台 final 卡 `9abacb14-5708-43c1-9f15-310908f4e6e3` 綁同一成片 SHA，唯讀 GET 與 `review-pull` 均確認 `pending`。已送站主人工審核，未核准前不製作上傳包。
- 此次 Jev 一次呼叫以 US$0.05 保守估額結算；H12 累計 US$4.235／6、五集累計 US$26.2295／39。供應商最終帳單未取得。

## 2026-10-17 H12 四語交接與聽感關卡

- 站主已核准同一繁中成片 `final.mp4` SHA-256 `2B24B5DF98A459CD587364C24D80FB0A7AFADFF4519DE86001B4A7D0E11D047D`，且後台選定 en／ja／ko 三語各自的標題說明、字幕與配音。站主另核准 H12 多語估算停手額度 US$2.50，使本集上限 US$8.50、五集上限 US$41.50；與原繁中授權分開記帳。三語 93 句文稿及 7 章已完成獨立複核，見 `i18n-translation-1.md`。
- 英、日、韓各 93／93 句配音成音，均 0 句超時間槽；四語字幕與三語標題說明、縮圖本機預檢見 `i18n-local-preflight-20261017.md`。未改已核准的繁中成片，沒有建立上傳包或上傳 YouTube。
- 三語 `check-audio` 均完成 93／93：英 12、日 27、韓 20 句自動旗標。英語 Gemini／離線兩套均疑第 `9jra` 句 them／him，待站主回答；日語優先 `cuxc`、`ds8v`、`dvmg`、`2d4b`、`cbd8`／`i3cg`、`wpvq`，待站主試聽。韓語 20 旗標的逐句頁與離線複核已整理，站主對韓語 93 句試聽問題回覆原文「OK」，記為韓語聽感接受、不重錄；原旗標仍保留。完整分流見 `i18n-audio-qa-en-1.md`、`i18n-audio-qa-ja-held.md`、`i18n-audio-qa-ja-1.md`、`i18n-audio-qa-ko-1.md`。
- 日語前次 `s4hn` 轉寫回應不明，後來按站主逐筆授權受控續跑，`s4hn`／`fgbf`／`ey9a` 各一次成功、journal 已清空；可能重複計費按最壞情況 US$0.20 保守計入。外部共享帳本在本次交接時 H12 估算 US$6.435／8.50，其中新增多語 US$2.20／2.50；五集估算 US$28.4295／41.50。供應商發票仍不可見；後續定向重錄及 QA 必須先核餘額。
- 下一步先讀站主英、日兩語逐句聽感；只對確定有問題的句子定向修文、重錄、重跑 QA／字幕。英、日聽感未定前不送 `publish`／`languages` 上傳包卡，也不把三語成音或韓語「OK」當成 Studio 上傳、後台核准或公開發布。

## 2026-10-17 H12 四語上傳包送審

- 站主對英語 `9jra` 回覆「聽到 them，英語旁白可以」，對日語回覆「日語旁白可以」；韓語先前回覆「OK」。三語音軌接受試聽、未重錄；12／27／20 句原始 QA 旗標保留在收據。沒有付費呼叫。
- 四語字幕重建完成，`package` 4／4 通過；繁中成片與三語配音 SHA 未變。上傳包 `metadata.json` SHA `6DDB8856…BEEE9`；詳細檔案及費用讀回見 `docs/videos/curio-h12/delivery-package-20261017.md`。
- 最新 `publish` 卡 `9ccad952-cb3b-45f6-8f8b-8ae71f0fda8d` 綁上傳包 SHA，後台已自動核准且 `review-pull` 記錄。最新 `languages` 卡 `abeb9cc0-20e8-409b-b972-c379072fcfcb` 綁 manifest SHA `8E5DD6E0…74B61F`，後台仍 **pending**；站主須審閱該卡。`status` 顯示 package 完成、on YouTube 未完成。
- H12 共用估算帳本 US$6.435／8.50、五集 US$28.4295／41.50，無 active reservation。此票待站主處理語言卡及 Studio 私人上傳；本次交接後釋出認領，不能標成全部完成。

## 2026-10-17 H12 語言卡核准讀回

- 站主回覆已核准最新版語言卡。唯讀後台 GET 確認最新 `languages` 卡 `abeb9cc0-20e8-409b-b972-c379072fcfcb` 為 **approved**，manifest SHA-256 `8E5DD6E09FDC943F0AB6A4FB8A04F0859D8A885144CF044F698CCA5FAF74B61F`，核准時間 `2026-10-17T03:37:04.574729Z`；最新 `publish` 卡 `9ccad952-cb3b-45f6-8f8b-8ae71f0fda8d` 仍為 approved。
- 本機 `review/languages.json` SHA 與後台相同，`review-pull --gate languages` exit 0，`approvals.json` 已記錄。`status` 仍顯示 `[ ] on YouTube`；不可把語言卡核准或 CLI 成功訊息當作 Studio 音軌已上傳／試播。仍待站主私人上傳成片與英／日／韓配音、字幕、專屬縮圖，填回影片 ID 並試播後讀回。
