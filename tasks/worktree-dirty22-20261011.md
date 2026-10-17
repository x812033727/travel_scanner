# 22 個 Codex dirty 工作目錄深入核對（2026-10-11）

核對 22 個目錄、4,454 個 status paths。已移除 4 個完成且 unused 的目錄及其本機 refs；保留 18 個，其中 5 個來源 scope 已完成但仍有依賴或使用狀態待釐清，13 個有整合、交付或材料對帳待辦。Claude 與《偶的江湖》不在本輪操作範圍。

逐檔比較基準 `9c46c14ed5c22388be68dec8301695667a226bee`；收尾 main `657d34790d1446d4f4b2784b4cf5261a22f2c5f6` 只新增獨立 Skills 製作票，未改本輪清理依據。

移除的 working files 邏輯大小共 113.64 MiB；新建 ZIP／增量 bundle 備份 19.36 MiB。這不是實體磁碟 free-space 實測差額。重用既有已驗證 482 MB baseline bundle。

## 已完成清理

| ID | 分支 | 未提交內容判讀 |
| --- | --- | --- |
| 54 | `codex/country-foods-map-links` | 17 個 Python 檔 AST 與 HEAD 相同，只有格式差異；產品已由 PR #56 取代合併。 |
| 56 | `codex/security-hardening` | 唯一 CI 修改的實質內容已在 PR #25；安全功能已在 PR #23。 |
| 57 | `codex/article-localization-batch016-llms` | 692 項全為舊 checkout 缺檔；現存 55 檔為 HEAD 內容、Git 指標及 1 個快取，產品已在 PR #654。 |
| 58 | `codex/article-localization-source-edit-preservation` | 2,507 項全為舊 checkout 缺檔；現存 57 檔為 HEAD 內容、Git 指標及 13 個快取，產品已在 PR #654。 |

每個候選均保存全部現存檔案、raw index、index-stage、status、SHA-256 與可恢復 Git 歷史；ZIP 實際讀回且復原儲存庫可讀全部候選 commit graph。清理前核對 HEAD、bytes、open PR、Codex owner/attachment、process command line、Windows Restart Manager 檔案占用。54 的 Git 刪除遭 OneDrive 唯讀目錄限制後，逐檔核對殘留、另存 gitdir 殘留，才以精確路徑完成清理；原失敗與補救收據均保留。其餘 3 個在精確目錄清除唯讀屬性後由 Git 移除，refs 使用預期 SHA compare-and-delete。

## 保留目錄與具體待辦

### 4 · codex/codex-practical-series-20261011

- 路徑：`C:/Users/x8120/.codex/worktrees/afd6/travel_scanㄐ`
- 判讀：1 個自動產生的環境設定；未完成的是 PR #1429 與 App 實錄／試製。
- 保留依據：原owner 2026-10-11 最後回覆明確「App 實際素材與試製仍未完成」；01 CLI13:27已試製、教材完成，不等於36支成片完成。
- [ ] 保留 local10cc468b，沿#1429整理未推送錄製準備差異及review，不另開重複課程票。
- [ ] 在原owner恢复原生擷取能力後，完成01 App實際操作及试製，再做03/05 App/CLI；首課跟做回饋、上傳/公開另驗收。

### 6 · codex/article-locales-release-20261007

- 路徑：`C:/Users/x8120/.codex/worktrees/4e16/travel_scanㄐ`
- 判讀：環境設定與 Decrypt 分類草稿；已發布 32 篇的收據仍待 PR #1373 合併。
- 保留依據：PR #1373 尚未合併；已發布的 32 篇收據與看板結案仍在分支。另有未入共享 main 的 Decrypt 混合主題分類問題票，不能把程式認得警語等同分類已修復。
- [ ] 保留 root、release 收據與 ignored localization staging／baseline／jobs；依現有 owner 合併 #1373，核對 4 張 release 結案與總表，不重發已發布內容。
- [ ] 保全本機 Decrypt 原票及兩個確切候選證據，與 main 既有 audited category correction 票逐一對帳；若未覆盖，只補 feed 分類／這兩候選的窄 scope，保持 HOLD、rewrite 計數及正常審稿。
- [ ] environment.toml 可視為生成設定另存；它的可清性不代表整個 workflow 完成。

### 7 · codex/stalled-videos-completion-20261008

- 路徑：`C:/Users/x8120/.codex/worktrees/2a98/travel_scanㄐ`
- 判讀：3 個舊刪除、環境設定、製作收據及原票；程式 PR #1387 與非 Mods 音軌交付未完。
- 保留依據：真正原owner最新最後回覆：23/54目標音軌已發布，31未完，Mods由使用者指定先跳過；zh-CN不补，費用US$2.49934/20。這是owner紀錄快照，不是本輪重新查正式站。
- [ ] 保留13 dirty/index与HEAD；在#1450恢復票中維護原id alias、檔案SHA和精確cohort。
- [ ] 沿#1387把7產品/測試檔兼容整合到main；不要覆蓋後續四語政策、STOP/lease與paid uncertainty guards。
- [ ] 原delivery owner接續非Mods31未完音軌的cached/QA/upload gates，Mods保持HOLD；本輪不啟動製作或付費。

### 9 · codex/news-recovery-20261010

- 路徑：`C:/Users/x8120/.codex/worktrees/6f71/travel_scanㄐ`
- 判讀：8 檔等同主幹；其餘為舊收據／claim、已結案舊票與環境設定。208 cohort 由原 owner 續作。
- 保留依據：舊 news-recovery 程式與工作副本已由 successor 接上；原 owner 的 208-cohort 恢復仍進行中，未證明舊 checkout 已釋出，故保留。
- [ ] 保留原owner與208恢復claim；實際繼續工作使用當時fresh Source/SQL/RQ/CAS/once-only receipts，從主線及successor最新紀錄續作，不能重播舊124publication或已done Save。
- [ ] 將舊docs/task副本標作歷史收據；保全13檔與external news-review/20261010-6f71STATE，不把舊open legacy-navigation搬回共享open。
- [ ] 沿PR1450已恢復的video-held-retry-status票追UI問題；此票與新聞恢復分開，不重複新增。
- [ ] 只有取得實際owner收尾／不再使用舊6f71目錄的證據後才重新判目錄清理；本輪保留不是dirty本身阻擋。

### 13 · codex/pr921-tidy-metadata-current

- 路徑：`C:/Users/x8120/.codex/worktrees/pr-merge-watch/travel_scanㄐ`
- 判讀：9 檔等同主幹，7 檔已有後續替代，1 張舊票；HEAD 的 missing-entry 保留 guard 仍缺。
- 保留依據：真正未完在committed HEAD：tools/video/automation/tidy.mjs有missing-entry hold；current main仍listed.get(slug)??null並使用舊local approval回退，latest200漏列不代表可清。#1450已恢復單一2026-10-11-restore-tidy-capped-list-retention-guard。
- [ ] 保全 staged17全patch/index，不reset、abort或重播舊Shorts整包。
- [ ] 只把missing-current-metadata保留guard與相容回歸接到#1450單一票；保持main現有共享素材、compilation與四語規則。
- [ ] 不在本輪執行任何正式tidy、媒體刪除或paid操作。

### 14 · codex/article-locales-wave6-release-20261010

- 路徑：`C:/Users/x8120/.codex/worktrees/article-locales-wave5-20261008/travel_scanㄐ`
- 判讀：兩份同正文結案 metadata；內容已合併，17 篇／68 語系發布仍未完。
- 保留依據：17 篇／68 語系內容已合併，但整個 wave6 root 的發佈交付仍未完成；兩個 dirty 檔是結案 metadata，不是未合翻譯內容。
- [ ] 保留 workflow 與 ignored bundle／baseline／jobs，不因 #1409 已合併而删除 root。
- [ ] 把本機 done 與 main review 的同正文票對帳為已完成 author/review 節點；發佈票維持未完。
- [ ] 由原 owner 按 17 篇／68 語系原 cohort 重新取得合法 source pins、备份／恢復與逐頁驗收，再执行现有 release 票；本次只讀核對未做正式站操作。

### 17 · codex/video-approved-final-languages-20261004

- 路徑：`C:/Users/x8120/.codex/worktrees/e82d/travel_scanㄐ`
- 判讀：9 檔等同主幹、3 張舊 open 已 done、環境設定；仍有 held 製作流程用途。
- 保留依據：具體尚未完成的owner scope：main bounded-video-media-followthrough仍由codex-video-stall-followthrough認領；DevDay known59 jobs的成功結果需source-bound native採用，Embedding序列gate尚無實際release；Argon/Skills/SEC圖像及三行JA有精確held receipts。沒有主owner釋出此operational checkout用途的證據。
- [ ] 不要以3張舊open再開bug；done證據直接連main同id。
- [ ] 沿main bounded-followthrough与DevDay既有票對照實際native採用、producer排除/序列release及可採用helper；保留unknown paid result與STOP。
- [ ] 若移轉operation用途，先把外部frozen helper/source/HEAD依賴與責任完整交接，再由root重新判unused；本輪不重啟或付費。

### 18 · codex/news-backlog-review-20261007

- 路徑：`C:/Users/x8120/.codex/worktrees/fe41/travel_scanㄐ`
- 判讀：2 份操作收據、5 張問題草稿、環境設定；520 cohort 尚未結案，須逐項去重與對帳。
- 保留依據：原520 news review尚未結案，兩份操作收據與5份問題草稿仍含未共享內容。
- [ ] 在原owner任務下保全2份receipt與external news-review/20261007-fe41 baseline/actions/intents；以精確520IDs先read-only對帳現有successor，不能盲目重播Save/normal judge或宣稱舊數量currentpending。
- [ ] 將same-host source selection草稿連同 current _source_index 無排序覆寫的正面code證據，對現有PR1450/共享票先去重後追踪deterministic selection及reordered-row tests；不接管原claim。
- [ ] 把navigation草稿拆清已完成#1411/#1444與現有rotating-source-widgets scope，只對仍缺source-aware admission/正文真正變更fixture追加窄驗證。
- [ ] 其餘3草稿先核current producer/deploy lock契約、source-verification/finalization順序與actual attribution payload；只在reproducer證明仍有缺口時補原ID或窄票，不將2026-10-07判斷直接移植。

### 27 · codex/stalled-production-resume-20261010

- 路徑：`C:/Users/x8120/.codex/worktrees/3603/travel_scanㄐ`
- 判讀：環境設定、14,616B 獨有收據及 2 張原票已保存至本次 cleanup PR；製作與 Whisper 相容性工作仍未完。
- 保留依據：Whisper permanent compatibility票claim曾被shared-language scope拒絕，私有shim不等於main永久修復；兩原票未出現在#1450 8a8 snapshot。
- [x] 持久保存14KBrecovery及兩原票到durable draft PR，保持原時間、scope、known result與lease/STOP序列。
- [ ] 沿原native receipt核對JA/EN V5 terminal與checks，不把four-clip兼容pilot當音訊核准。
- [ ] 原owner依已有五片英日韓metadata/CC/dub選擇接續各native gate，先解合法shared-whisper scope；本輪不重跑付費或外部官方endpoint。

### 31 · codex/gemini-advanced-platform

- 路徑：`C:/Users/x8120/.codex/worktrees/3281/travel_scanㄐ`
- 判讀：環境設定與測試用 workbook-inspector NDJSON；33 篇真實環境驗收與整套發布未完。
- 保留依據：平台及36篇作者材料已合併，33篇真實帳號／模型／裝置驗收與整套release仍未完成；不是2dirty造成產品未整合。
- [ ] 沿現有7張advanced author/release票續作，使用ACCEPTANCE的33篇逐實驗條件補真實帳號/模型/裝置證據；保留已完成Windows69–71範圍與所有failed/private receipts，不重做平台。
- [ ] 先保存NDJSON、private實驗exports及ignored browser outputs；不要把synthetic workbook、fixture或書面課綱宣稱Google實測完成。
- [ ] 整套39限定write-slug/87頁候選需重新source/version凍結與ready gate；Google環境和費用仍按原owner選擇，這輪不呼叫任何provider或正式站。

### 38 · codex/llm-selected-language-completion-20261007

- 路徑：`C:/Users/x8120/.codex/worktrees/23a9/travel_scanㄐ`
- 判讀：只有生成環境設定；PR #1368 與選定語言交付未完成。
- 保留依據：選定語言完成/已approved語言包和來源/metadata補件是本PR交付範圍；owner最新回覆AI修Bug已交到另一checkout，但未表示此LLM PR已merged或新答卷publication。
- [ ] 沿#1368保全四語translation worksheet、原source/currentmanifest/音訊receipts以及3張工具bug票；有後續四語policy變更時在review中明確處理舊zh-CN資料。
- [ ] 將PR的source integration、語言consumer readback与owner播放/YouTube upload/publication分别驗收；不從READY推論done。

### 39 · codex/renewed-finals-host-handoff-20261007

- 路徑：`C:/Users/x8120/.codex/worktrees/7392/travel_scanㄐ`
- 判讀：生成環境設定與 0-byte 意外暫存檔；PR #1359 及原生語言交付未完成。
- 保留依據：#1359 OPEN head d03c624b與本地exact同；committed runner/context/temp source-resubmission/portable receipt及7張工具draft仍未merge，main hand-off-owner-approved-renewed-finals仍open。
- [ ] 保全empty artifact和environment metadata但不把它們恢復成bug。
- [ ] 沿#1359處理verified native units-before-submission source及review；pending/unknown原答卷、source/choice/manifests和新backend送審consumer逐一驗收。
- [ ] owner/YouTube/公開交付仍獨立；不繼續生成或盲重送。

### 46 · codex/ai-series-continuation-20261004

- 路徑：`C:/Users/x8120/.codex/worktrees/b136/travel_scanㄐ`
- 判讀：只有生成環境設定；來源已完成，但 Embedding executor 仍驗證此目錄的凍結 helper 絕對路徑。
- 保留依據：真executor normal-audio-check-post-merge-v5-budget40.DRAFT.mjs:29會verifyPinned全部private_file_pins，:83每dispatch前checkLocal；沒有證據這個absolute pin已移轉。原e931 stopped不表示後續new resume已能脫離此helper；不得為cleanup replay/修改它。
- [ ] 保留checkout，實際原因是Embedding凍結helper依賴，不是environment或notLoaded。
- [ ] 窄ticket記錄 frozen helper migration：原manifest/entry不可改或重放；將same bytes helper與證據保全到穩定隔離位置/保留source git snapshot，再由合法successor在全新guard/manifest進行獨審與零provider驗證。原b136 path真正無依賴後root再做unused/CAS。
- [ ] LLM原1250媒體、G15驗證檔、2支Shorts/private聽感、原31+新增4ASR/未知第5預留全留原位；不把checkout清理當媒體刪除授權。

### 47 · codex/codex-learning-publication-receipt

- 路徑：`C:/Users/x8120/.codex/worktrees/fc2e/travel_scanㄐ`
- 判讀：32 個官方研究快照、失敗截圖、環境設定；305 語系文件發布已完成，pinned owner 用途未核實。
- 保留依據：Codex教學產品／發布已完成；34dirty僅研究和暫存證據可封存，但原聊天pinned且最後owner用途未能核實，本輪保留。
- [ ] 保全32官方research快照、failure PNG、environment及ignored frontend/build logs；將finalize-release與#585 receipt連為產品完成證據。
- [ ] 保留pinned原聊天及目錄；須有實際owner收尾或已不再依賴研究資料的證據才可判unused；不要為清理去解除pinned或接管owner。
- [ ] 不新增「完成Codex教學發布」票，不重發305locale documents；若需要整理broadblocked歷史清單，只以既有finalize-release正面證據對帳，不把舊0/60當currentpending。

### 48 · codex/batch034-source-task-close

- 路徑：`C:/Users/x8120/.codex/worktrees/batch006-final-close/travel_scanㄐ`
- 判讀：2 份重複完成 metadata；PR #887 已完成，但仍附在 pinned c5d9 聊天，使用狀態未釐清。
- 保留依據：#887 原 source-only 修正已完成；兩份 local 票只是重複完成收據。但目前仍有 111 個關聯且 managed worktree 附在 pinned c5d9 聊天，ownership 不明，本輪保留。
- [ ] 將两份 local task 原始 bytes／hash 保全成重复完成 metadata，记录 main done 的 source-only closure；不用重新开 source 修正或发布票。
- [ ] 本輪保留root及pinned c5d9 managed attachment；后续须得到具体owner交接／释放或可核验的unused证明，再讨论备份后清理。此行不是本輪remove候选。

### 50 · codex/korea-source-fact-corrections

- 路徑：`C:/Users/x8120/.codex/worktrees/korea-source-fact-corrections/travel_scanㄐ`
- 判讀：Jeju 2 檔已有較完整主幹版本；Nami JSON／SVG 公休日接駁例外尚未整合。
- 保留依據：Jeju 兩檔提案已被較完整的主線版本取代；Nami 週三公休日接駁例外的 JSON＋SVG 修正仍未整合。
- [ ] 保留 Nami JSON、SVG、原 owner 与 Batch008 HOLD 记录；只将 Jeju 两份旧提案标成主线已取代并备份，不再重开 Jeju。
- [ ] 与共享 Nami/Seoul 恢复票对账，独立查证 Gapyeong 周三公休日接驳例外，在 fresh main pin上仅移植这8处与图说明，保留后来的枫叶 interlink。
- [ ] 来源通过后再重绑四语候选、hash与独立审稿；此轮不查正式站、不付费、不发布，也不释放原claims。

### 53 · codex/article-five-language-completion

- 路徑：`C:/Users/x8120/.codex/worktrees/c5d9/travel_scanㄐ`
- 判讀：938 個非空 stage、81 個空暫存、15 個 pilot 包及程式／任務異版；84 歷史 jobs 尚需按版本對帳。
- 保留依據：1099個路徑含舊stage/包/失敗attempt、source/tool異版和歷史任務；4e16承接協調但未逐material證明完整successor，故保留。
- [ ] 由现有4e16協調票，先用84精確slug/locale的source/job/manifest/hash與後續release ledger逐項read-only對帳；16main已有target依版本標superseded或reuse，68main未見target查真實DB/後續包後才列currentpending。
- [ ] 保全15pilot bundle檔、938非empty stage、5rendered/3translated/4problem receipts、source/base/progress及provider unknown/STOP/locks；對Bangkok受保護token錯誤先修定稿再重審，blocked的已知限額不能盲重送。
- [ ] pilot-source與current-source不同時先明列source修訂與獨立review，未取得current-source正面完整proof前不install/publish舊pilot、不刪材料。
- [ ] series與sitemap已#947/#594完成，沿done successor對舊task過期清單收尾；23source/tool異版逐功能只挑尚無successor的窄hunk，禁止整體回放舊guards少的local code。
- [ ] 本輪保留c5d9；確認material逐項完成/封存承接及實際owner不用後才重評清理，不將1099dirty路徑全部當1099個未完工作。

### 55 · codex/article-localization-batch-011-korea

- 路徑：`C:/Users/x8120/.codex/worktrees/article-localization-batch-011-korea/travel_scanㄐ`
- 判讀：5 個 Jeju 檔等同主幹；12 個 Nami／Seoul 候選、來源修訂與 HOLD 記錄尚待完成。
- 保留依據：17 個 dirty 路徑中 5 個 Jeju 路徑已與 main 相同，另外 12 個仍是 Nami/Seoul 候選、來源差異及 HOLD 記錄。
- [ ] 保留12個未整合路径与原HOLD/owner/政策拒绝证据；已完成5個Jeju路径单列已整合，不重跑其翻译、审核或发布。
- [ ] 先与共享 Nami/Seoul 窄恢复票对账，在fresh main上核对Nami under36资格、13:30班次、取消50%、公休日接驳及Seoul T-Luggage中心/尺寸/机场条件；只依允许的独立审稿路线解除具体HOLD。
- [ ] 保留main新增interlink，重绑8份语系候选与8张图的source/hash/review证据；不得绕过blocked by policy、擅自释放原claim、付费或正式发布。

## 持久待辦與查核

- #27 兩張缺失原票已按原 ID 恢復；保留原時間、scope、owner／claim，沒有接管製作。14,616B 收據原樣另存 `tasks/evidence/worktree-cleanup/2026-10-10-production-resume.original.md`。
- 新增 `2026-10-11-migrate-frozen-embedding-helper-dependency`：僅追蹤 b136 的凍結 helper 依賴遷移；沒有更動原 manifest、HOLD、paid/provider 狀態。
- 其餘待辦優先沿既有 task/PR，不因舊 open 副本重新開已完成 bug。清理後用同一 snapshot 核對保留目錄的 HEAD、status、index-stage 及全部現存 dirty 檔案。

完整逐檔清單與備份：`C:/Users/x8120/.codex/scratch/codex-dirty22-deep-20261011/codex-dirty22-report.html`、`recovery/manifest.json` 與三份分類 audit JSON。

主幹／PR 合併、正式站發布、影片交付和 owner 播放驗收各自記錄；本輪没有執行產品待辦、付費生成、發布或其他 owner 的工作。
