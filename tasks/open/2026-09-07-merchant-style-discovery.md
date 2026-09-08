---
id: 2026-09-07-merchant-style-discovery
title: 網美與文青店家風格篩選、審核及首批來源資料
status: review
priority: P1
area: api
owner: codex
claimed_at: 2026-09-08T05:53:35Z
created_at: 2026-09-07T23:14:18Z
completed_at:
branch: codex/merchant-style-batch-07
depends_on: []
scope:
  - apps/api/app/models.py
  - apps/api/app/foods
  - apps/api/app/cli.py
  - apps/api/migrations/versions/0061_merchant_styles.py
  - apps/api/tests/test_merchant_styles.py
  - apps/api/tests/test_trend_import.py
  - apps/api/tests/test_schema.py
  - apps/web/components/food-browser.tsx
  - apps/web/components/food-browser.test.tsx
  - apps/web/components/food-merchant-card.tsx
  - apps/web/components/food-merchant-card.test.tsx
  - apps/web/components/admin-merchant-styles.tsx
  - apps/web/components/admin-merchant-styles.test.tsx
  - apps/web/lib/foods.ts
  - apps/web/lib/foods.test.ts
  - apps/web/messages
  - docs/merchant-styles.md
  - README.md
  - apps/web/e2e/community.spec.ts
  - apps/web/playwright.config.ts
---

# 網美與文青店家風格篩選、審核及首批來源資料

## Why

使用者要求網美／文青分類篩選，以及實際蒐集與審核店家。現有分類是料理種類，
不能將風格塞成主菜分類，也不能靠風格跳過店家發布條件。

## Definition of done

- [x] 獨立雙風格可與城市、商圈、料理及文字交叉篩選；僅核准標籤公開。
- [x] 管理員審核需來源、日期、理由，保留版本衝突檢查與稽核。
- [x] 五語系前台卡片、篩選與後台審核表單。
- [x] 首批 5 家來源查核（4 新候選、1 既有），可重跑匯入且不覆寫舊審核。
- [x] 新舊遷移、API/Web、桌面/Pixel 7 驗證；完整 CI 以 PR 最新 SHA 檢查為準。
- [x] PR #345 合併、部署及首批預覽／正式匯入／重播驗證。
- [x] 第二批 8 家官方來源查核及 9 個風格提案，備份後加入正式環境待審清單。
- [x] 第二批 PR #346 完成 CI、依「合併後繼續新增」授權合併，main CI 全綠。
- [x] 第三批7家官方來源查核、待審匯入、稽核與重播驗證。
- [x] 第三批 PR #347 完成 CI 與依本輪授權合併，post-merge CI 全綠。
- [x] 第四批5家新店＋1家既有補風格、6個提案完成來源查核、待審匯入、快照比對與重播驗證。
- [x] 第四批PR #350及第五批PR #354完成CI並依各輪授權合併。
- [ ] 第六批資料／測試／交接 PR 完成 CI 與合併（本輪合併授權針對 #354）。
- [ ] 逐家補齊地圖與永久座標、管理員風格審核，再另行發布店家。

## Steps

- [x] 從 main 的獨立工作目錄建立 codex/merchant-style-discovery；保留 #343。
- [x] 新增 0061、公開與管理 API、僅待審匯入路徑及稽核。
- [x] 獨立審核元件、草稿、錯誤狀態、五語系文字。
- [x] 完成程式驗證與 PR #345 交付；上架狀態不可描述成已完成。

## How to verify

API: Ruff、mypy、pytest；Windows 不支援 UnixStreamServer，完整 deployment_agent 測試由 Linux CI 執行。
Web: 單工 Vitest、TypeScript、lint、check:i18n、production build；merchant-styles.spec.ts 跑 desktop/Pixel 7。
匯入及人工查核記錄見 docs/merchant-styles.md。

## Notes

2026-09-08 跨工作區交接：已確認 `admin-food-merchants-panel.tsx` 無未提交或本分支待交付變更，後續店家來源／風格審核不再修改此檔，僅釋放這一個 scope 給 `codex/admin-domain-workspaces` 加入待審初始篩選。其餘 scope、店家資料、風格／地圖／平台審核功能及 PR 狀態均不變；本次交接不授權合併或部署。

2026-09-08 第二次窄幅交接：已確認 `.github/workflows/ci.yml` 與 `apps/api/app/i18n.py` 均無未提交或本分支待交付變更，從本任務釋放這兩個 scope 給 `codex/admin-domain-workspaces`，分別供既有 CI 加入後台 Playwright 測試，以及新增 `catalog_scope_invalid`、`catalog_scope_mismatch`、`provider_setting_conflict` 錯誤翻譯。本任務後續不再修改這兩檔；其他 scope、應用程式、資料及遠端 PR 不變，只提交本地任務 metadata，不 push、合併或部署。

2026-09-08 第三次窄幅交接：已確認 `apps/web/e2e/merchant-styles.spec.ts` 無未提交或本分支待交付變更，也沒有本任務進行中的修改，僅釋放此 scope 給 `codex/admin-domain-workspaces` 為 PR #369 補上新增唯讀 `/admin/provider-settings` 請求的有效空設定 fixture。本任務不代改 E2E、不再修改此檔；其他 scope、應用程式、資料及遠端 PR 不變，只提交本地任務 metadata，不 push、合併或部署。

新候選缺精準地圖與可永久保存座標時保持 pending/inactive/unverified，不用來源文字推造識別。
先完成原始來源審查，再於已部署的後台逐一記錄操作人及風格核准；資料檔不能偷帶 approved。
PR #345 已合併部署，第二／三批 PR #346、#347 已依授權合併；繼續新增仍只補正式待審候選，不代表核准發布。
未啟動付費模型或地圖批次；第五批PR #354已依本輪授權合併，第六批資料PR的合併仍需新授權。

## PR 與驗證交接

- PR: https://github.com/x812033727/travel_scanner/pull/345 ，base `main`。
- Linux CI（92ecde8）：API 1792 passed / 3 skipped，含 PostgreSQL、全套遷移及同時首次審核衝突測試；Ruff、mypy、containers、全端 smoke 通過。
- Web 全套 133 files / 785 tests 通過；TypeScript、lint、五語系檢查與 tools 27 tests 通過。
- 本機 production webpack build 通過；預設 Turbopack 的正式建置由 Linux CI 驗證。本機 node_modules junction 跨 root 不支援 Turbopack，不修改專案設定繞過。
- 最新 UI 的 merchant-styles.spec.ts：22 passed（五語系、深淺模式、desktop / Pixel 7、後台草稿及獨立儲存）；已檢查手機深色及審核成功截圖。此套為 API mock UI 證據，不是正式資料。
- 早期瀏覽器測試使用錯誤的按鈕／select label locator，已改用實際按鈕名稱及具名審核群組的 combobox；不是放寬驗證或延長 timeout。
- #345 合併為 `b3e49a325edcc41e167653e9fe13619403248507`，main CI `34171987990` 全綠，8 個應用服務部署同版本；資料庫 `0061_merchant_styles`。
- 首批正式匯入為 4 新候選＋1 既有店家補標籤，5 pending 風格；既有 FAbULOUS 狀態不變，重播零新增。

## 第二批交接（2026-09-08）

- PR: https://github.com/x812033727/travel_scanner/pull/346 ，base `main`；本次接獲明確合併授權後完成。
- 從上述最新 main 建立 `codex/merchant-style-batch-02`；未碰原 checkout 的 mobile-planner-app-ui 或 PR #343。
- 新增台中2家、京都2家、東京1家、新加坡2家、曼谷1家，9個標籤（網美5、文青4）。完整分店、來源及排除理由見 docs/merchant-styles.md。
- 正式環境比對名稱與地址零重複；JSON checksum 一致、取得兩個部署鎖、備份可讀後套用成功，8 家 pending/inactive/unverified，所有地圖／座標／商圈欄位留空。
- 稽核恰為建立8店及提案9風格各一筆，actor=NULL 系統匯入；再次預覽0店／0標籤。未呼叫管理核准 API。
- 正式伺服器受控批次目錄 `/root/mokaair-merchant-batch-02-ZJOQ5uHv` 保留來源、preview/applied/replay JSON、pre-import.dump 及索引；備份權限600，不刪除舊備份。
- 只匯入資料、不重建映像、不跑新遷移；/ready 正常、公開風格仍0、foods頁200。待審清單在 `/zh-TW/admin/foods`。
- 本機 API 40 passed / 1 skipped（PostgreSQL row-lock 專屬），涵蓋實際第二批 preview/apply/replay、欄位隔離、公開隱藏與稽核；Ruff 全套與 mypy 255 files 通過。
- 新測試初版误用了不存在的 naver_place_id，已按真實模型改為 naver_map_url 並重跑通過；沒有修改產品邏輯或放寬斷言。
- 無 Web 程式或資料庫結構變更；Linux PostgreSQL 與完整 CI 結果查看第二批 PR checks。

## 第三批交接（2026-09-08）

- #346 以 `--match-head-commit 49748e84c405485180aac86276cf32c68371ed7f` 合併為 `b06022771c90a834180ac2607c0fe223db79eadb`；確認 origin/main 與 post-merge CI `34175624475` 全綠後繼續。
- 從該最新 main 建立 `codex/merchant-style-batch-03`。未操作原 checkout 或 #343，不重建資料批次無需更動的應用映像。
- 7 家候選：青田七六、中央書局、kubrick油麻地、森の図書室、Onion安國、PS.Cafe One Fullerton、Jypsy One Fullerton；3網美、4文青。官方來源、搬遷／樓層與閉館排除依據見 docs/merchant-styles.md。
- 來源 JSON、SHA-256、正式環境名稱／地址查重及預覽完成；先備份再以既有 importer 加入待審，不核准風格、地圖或發布。
- 本機 API 43 passed / 1 PostgreSQL-only skipped；Ruff 全套、mypy 255 files 通過。將既有批次資料庫測試參數化覆蓋第二／三批，新增跨批次身分去重測試。
- 第三批正式作業目錄 `/root/mokaair-merchant-batch-03-JRTuNg2X`，保留來源、預覽／套用／重播結果及私人備份，不刪舊檔。
- 正式套用7店／7標籤、重播0／0；地圖／座標／商圈留空，店家pending/inactive/unverified，稽核2筆actor=NULL系統操作。三批共19新店＋1既有補風格、21個pending標籤，未公開。

## 第四批交接（2026-09-08）

- #347 鎖定head `744262e31b12ff48edda9fff02f03ea1ca6b1f4e` 合併為 `67234d9bd56a1a037b62daf6439275339e3ae1d3`，origin/main與post-merge CI `34179094453` 已核對全綠。
- 從最新main建立 `codex/merchant-style-batch-04`，不操作原mobile-planner checkout或其他PR。
- 新增神保町ブックセンター、梟書茶房、文喫福岡天神、Brown Hands百濟、TERAROSA水營；Walden Woods僅補缺少的網美提案。3文青／3網美，來源與判定界線見 docs/merchant-styles.md。
- 本機 API 46 passed / 1 PostgreSQL-only skipped；全套Ruff及mypy 255 files通過。資料測試納入第四批，新增既有approved店家完整欄位、來源及分類不被覆寫的SQLite／PostgreSQL回歸測試。
- 正式作業目錄 `/root/mokaair-merchant-batch-04-PnQ6qaZd` 保留JSON、preview/applied/replay、備份及Walden前後快照；備份7,060,901 bytes、權限600，不刪舊備份。
- 正式名稱／地址查重、checksum、部署鎖與備份完成後套用5新店／6風格；再預覽0／0。新店皆pending/inactive/unverified、地圖／座標／商圈空白。Walden店家／來源／分類前後快照完全一致，既有發布狀態不變。
- 新增稽核2筆actor=NULL系統操作，四批合計24新候選＋2既有補風格、27個pending標籤；公開風格仍0、/ready正常、foods頁200。未重建服務、遷移、核准或公開發布。
- PR: https://github.com/x812033727/travel_scanner/pull/350 。已無衝突同步main的大阪飯店資料PR #348，保留雙方內容；最終CI以PR最新head為準。
- CI紀錄（fe565e1）：PR run `34179853238` 全綠，API 1819 passed / 3 skipped、Web 785、isolated browser 230、旅遊與社群全端各6通過；push run `34179822859` 首次全端工作失敗。
- 失敗位置為 community.spec.ts:375，刪除帳號後的舊session GET `/api/travel/auth/me` 發生ECONNRESET，未收到HTTP狀態，並非已觀察到授權斷言錯誤。同次PostgreSQL輸出有 `uq_community_metric` 重複讀取計數，但不能據此認定是重設連線的原因。
- 此類問題已由 [既存社群併發待辦](2026-09-07-community-read-metric-concurrency.md)追蹤，本批未修改相關程式、未放寬斷言／timeout，也未在正式環境修復。已單獨重跑失敗工作，通過也不代表根因已解決；結果與最新head檢查記錄於PR，未複製token、私人信件或會員識別。

## 第五批交接（2026-09-08）

- 本輪「合併後繼續新增」授權已用於#350：先後無衝突同步#349店家預約連結與#352飯店資料，重跑相關測試，八項checks全綠後鎖定head `240178b6daff4607b8db1e4be027d4aefc70fcd3` squash合併為 `7b19c2f5717a1becdb6f93249bb0fc9d5c4ae598`，已fetch確認在main。
- #350最終PR run `34184379282`、push run `34184376555` 均通過；API 1847 passed / 3 skipped、mypy 257 files、Ruff，旅遊與社群全端各6項通過。先前偶發社群連線錯誤仍由既存待辦追蹤，本批未修復或放寬測試。
- 從上述最新main建立 `codex/merchant-style-batch-05`，保留原mobile-planner checkout與其他PR。合併後main CI為 `34184865496`，最終狀態與第五批完整CI結果記錄於PR。
- 5家全新候選：現流冊店、浮光書店、ONIBUS中目黒駅前店、Cafe Bibliotic Hello!、The Coastal Settlement；2網美／3文青。分店地址、來源年份、營運細節限制及未納入項目見 docs/merchant-styles.md。
- 增加第五批資料／真實preview-apply-replay測試，並逐欄驗證第二至五批店名、地址、風格證據與來源。首輪新增來源計數誤含fixture舊店，已限定至本批merchant IDs；未修改產品程式或降低驗證標準。
- 本機48 passed / 1 PostgreSQL-only skipped，全套Ruff及mypy 257 files通過；tools 27 tests、task board 176 files通過。Linux PostgreSQL與完整遷移／Web／五語系／瀏覽器由CI驗證。
- 正式環境先查重，確認已部署API為 `aaa33f008c82c56e5c541dede8205097102193e1`、schema `0062_merchant_platform_links`，不回退或重建服務。查重首查誤用JSON欄位address_local，read-only SQL遭拒，按模型address欄位重查零重複；沒有寫入副作用。
- 正式作業目錄 `/root/mokaair-merchant-batch-05-QcyRbvOC` 保留JSON、preview／locked-preview／applied／replay與備份索引；備份7,087,794 bytes、權限600，無刪除舊備份。兩部署鎖、三處checksum及鎖內預覽皆核對後套用。
- 正式新增5店／5標籤，重播預覽0／0；皆pending/inactive/unverified、未填地圖／座標／商圈，未指定審核人。兩筆系統稽核，五批合計29新候選＋2既有補風格、32個pending標籤；公開風格仍0、/ready正常、foods頁200。
- 第五批仍只交付來源資料及待審匯入，需在後台補精準地圖、耐久座標、商圈與獨立風格／發布審核；未完成整體任務，不標done。

## 第六批交接（2026-09-08）

- 本輪「合併後繼續新增」授權用於#354：先無衝突同步main的#353飯店資料，相關測試78 passed / 1 PostgreSQL-only skipped、Ruff與mypy通過。八項checks全綠、CLEAN／MERGEABLE後，以exact-head guard鎖定 `bab1e5af71652711237470cca49e4e39d66d20bc` 合併為 `88eb4b15b99619782d60e78c29ab12f5c9e35c68`，已fetch確認在main。
- #354最終PR run `34186127865`、push run `34186125849` 均通過，無需重跑失敗工作；post-merge main CI `34186647969` 的最終結果記錄於第六批PR。
- 從上述main建立 `codex/merchant-style-batch-06` 並重新claim原任務；沒有操作原mobile-planner checkout、#343或其他工作目錄。
- 新增三餘書店、森彦、喫茶七番、喫茶ニューポピー，共4家、3網美／1文青。全部使用實際閱讀的店家官方頁，分店、樓層、新建／老屋界線及暫不納入的來源見 docs/merchant-styles.md。
- 第六批納入既有資料證據驗證及真實preview／apply／replay參數化測試；精準驗證欄位、來源、稽核與公開隱藏，不修改產品程式。相關測試50 passed / 1 PostgreSQL-only skipped，所有foods／merchant／trend測試172 passed / 6 PostgreSQL-only skipped；Ruff全套與mypy 257 files通過。
- 正式環境映像仍為 `aaa33f008c82c56e5c541dede8205097102193e1`、schema `0062_merchant_platform_links`。名稱／地址零重複，雙部署鎖、三處checksum、鎖內預覽及備份驗證後套用成功。
- 作業目錄 `/root/mokaair-merchant-batch-06-GX1dnUMU` 保留JSON、preview／locked-preview／applied／replay、公開查詢前後收據、備份及索引；備份7,092,975 bytes、權限600，不刪除既有備份。
- 正式新增4店／4標籤，重播0／0；均pending/inactive/unverified且地圖／座標／商圈空白、無審核人。兩筆系統稽核，六批共33新候選＋2既有補風格、36個pending標籤（網美17／文青19）。公開查詢前後完全一致且仍為0，/ready正常、foods頁200。
- 未重建服務、執行遷移、呼叫付費模型／地圖或核准發布；本批PR尚需新合併授權，整體精準地圖與人工審核工作未完成，不標done。

## 第六批合併驗證補強（2026-09-08）

- 新一輪「合併後繼續新增」已授權#356，但8106651的push CI仍blocked：首次community建立旅程ECONNRESET；單次重跑為mobile full-stack.spec.ts:232等不到航班動態連結，150秒逾時。當次Next的runtime/public-config與trips/{id}有JSON解析500，社群則6項通過。未把不同失敗混稱同一根因。
- 查核現行CI確實以next dev啟動全端Web；既存待辦記有load-manifest.external.js讀取JSON清單失敗的明確堆疊。本輪在原scope內將全端CI改為先build、再next start，兩套Playwright均指定使用正式建置，消除此測試環境的請求時編譯；API、worker、PostgreSQL、Redis、S3、SMTP與原有桌面／Pixel 7案例、斷言、timeout保持不變。
- 此調整遵循專案既有isolated UI建置方式及[Next.js官方測試指南](https://nextjs.org/docs/app/guides/testing/playwright)。不改Next依賴、不宣稱修復開發伺服器自身或社群計數重複鍵；正式資料與服務完全不動。新head全套CI通過後才以SHA guard合併。
- 79266a2的正式建置與旅遊6項均通過，社群6項在admin登入後GET settings收到401。已定位安裝的Playwright Cookie.matches只對HTTP localhost（非127.0.0.1）容許Secure cookie；獨立合成Cookie本機實驗亦確認numeric loopback不回送、localhost正常回送。擴充本任務的兩個測試檔scope後重新claim，將全端站點、Playwright baseURL、Origin與MinIO CORS統一localhost；API／Redis等內部連線不变。保留production Secure、HttpOnly、SameSite及所有授權斷言，未注入登入token或繞過登入。

## 第七批交接（2026-09-08）

- #356已依新一輪授權合併：同步main #355後鎖定2984f82045ad5bcdb83d0dd7532527f78f5a180c，8項checks全綠、CLEAN／MERGEABLE，SHA-guard squash為f48e9a6e710779d7c8f53786e8d3fd5a492ee691，已fetch確認main。
- PR run 34190397145全綠；push run 34190395334初次desktop community GET /community/me仍ECONNRESET，Next有destination stream closed early，不能把正式build視為已修復所有transport reset。第一次在整體run未完時重跑請求遭拒；完成後僅重跑失敗job一次，attempt 2全綠。原失敗證據與界線保留於#356評論，不更改斷言、timeout、並行度或Cookie安全設定。
- 該head Linux API1859 passed／3 skipped，Ruff與mypy 257 files通過；Web133個元件測試檔、230個瀏覽器案例、五語系25 namespaces通過；本機合併後資料回歸83 passed／1 PostgreSQL-only skipped。Post-merge main CI 34191139080結果另記PR。
- 從該main建立codex/merchant-style-batch-07並claim本任務；保留原mobile-planner checkout及其他PR。
- 新增本屋B&B、RBL CAFE、文喫六本木與NOC Cityplaza，3文青／1網美；均讀取官方店址與風格來源。本屋B&B飲品頁圖片另以瀏覽器實際檢視確認咖啡及茶飲，不只因供應啤酒而歸為酒吧；未下載或複製圖片入庫。其他分店與舊活動的排除界線見docs/merchant-styles.md。
- 正式read-only初查誤用JSON的name_zh欄位，SQL拒絕且無寫入；按模型name重新查詢，僅找到不同城市的文喫福岡天神，四家無重複。映像仍aaa33f008c82c56e5c541dede8205097102193e1，readiness與schema0062正常。正式寫入前仍须雙鎖、checksum、鎖內預覽、備份及重播驗證。
- 第七批相關測試52 passed／1 PostgreSQL-only skipped，全部foods／merchant／trend 174 passed／6 PostgreSQL-only skipped；Ruff全套、mypy257 files、tools27 tests、五語系25 namespaces及task board176 files通過。新資料加入既有真實preview／apply／replay測試與跨批去重檢查，不改產品程式。
- 正式作業目錄 `/root/mokaair-merchant-batch-07-BqTXChhr` 保留JSON、preview／locked-preview／applied／replay／verified及公開查詢前後收據；備份7,097,706 bytes、mode600、restore目錄可讀。雙部署鎖、三處checksum及鎖內預覽皆通過後新增4店／4提案；重播0／0。
- 正式逐欄驗證店名、地址、來源、風格、證據、日期，4家皆pending/inactive/unverified、無地圖／座標／商圈／審核人；兩筆actor=NULL系統稽核保留count、target及提案items。七批37新候選＋2既有補風格、40個pending標籤（網美18／文青22）。公開payload前後一致且仍0，/ready正常、foods頁200。
- 未重建服務、執行遷移、付費模型／地圖呼叫、寵物規則推導或核准發布。第七批PR保持待審，需新一輪合併授權；完整精準地圖、耐久座標、商圈及人工審核仍未完成，不標done。

## 第七批合併與重新部署準備（2026-09-08）

- 使用者新授權「合併重新佈署後繼續新增」，目標為#359。先無衝突同步main的#357首爾飯店資料，相關API回歸88 passed／1 PostgreSQL-only skipped；重新取得完整CI後才用最新SHA guard合併。
- 正式預檢：10個既有服務正常，API／Web仍為aaa33f008c82c56e5c541dede8205097102193e1，schema0062，社群與公開註冊均關閉。資料volume、部署socket與canonical環境檔保持原狀；磁碟可用133G。
- 本次依明確授權重新部署合併版本，使用乾淨Git archive與獨立release目錄，不重設canonical checkout、不刪舊映像／volume／備份、不開啟社群或註冊。部署須雙鎖、映像核對、私有可讀備份、保留回退資訊及重複readiness驗證；完成結果交接於下一批。
