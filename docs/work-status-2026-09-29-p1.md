# 2026-09-29：原 64 張 P1 任務稽核

本次範圍固定為主分支 `c1da5fad` 的 64 張 P1，不把後來的新票混入分母。站主要求仍有必要就執行、已無必要就刪除、無法判斷就詢問。逐票讀取接受條件、主分支實作、PR與驗收紀錄；程式合併、內容包完成、正式發布與現場驗收分別判斷。

## 第一輪判定

- 30 張已完成而漏結案。
- 2 張新加坡舊票被 2026-09-22 的獨立審查與正式發布證據取代。
- 13 張仍有可執行工作（含三项程式修正、四項產品驗收、六支影片獨立查核）。
- 14 張需站主決定、正式站基線或帳號/預算/驗收條件。
- 3 張已有其他 PR 承接或等待其修復。
- 2 張 Gemini 教學票經站主明示保留，這輪不做。

判定不是全數執行完成宣告；本輪實際結果與測試會記錄在下方及各票。正式站未經本輪具體批准不進行寫入。

## 本輪執行紀錄

- 代理憑證：新增正式 API 啟動必須至少32字元、開發環境未設憑證但信任轉送位址的啟動警告；新回歸在修正前 9 failed / 2 passed，修正後安全設定、公開讀取限流及API金鑰URL測試合計61 passed。Ruff和四檔mypy通過。主機成對設定仍是合併前門檻。
- 新聞長正文、逐篇發布暫停規則：正在修正與測試，完成結果將補入。
- 社群／網站外觀：正在補本機可用驗收；本機缺少真實服務時不宣稱完整服務驗收通過。
- Gemini 51–56、69–74：站主回覆「保留待辦，這輪先不做」。

## 逐票證據與剩餘工作

### 1. 2026-09-07-contextual-travel-services

**仍有缺口，待站主決定/條件** — Contextual travel services and affiliate catalog

- PR #336 MERGED 2026-09-07 as 885369588362edcb27bb7ae86e9a345d15214722; task records deployment separately.
- docs/travel-services.md release boundary and original task explicitly retain real six-city stock, live tracking, and enablement gates.
- No later task or matching open PR in the 2026-09-29 snapshot completes these gates; the old contextual worktree is prunable.

剩餘／處理：36 hotels, 18 tours, 12 transfers and nine country eSIM plans need current licensed/evidenced inventory, actual partner landing/tracking checks, and explicit production release. Hotel ordinary-booking work and destination-level Travelpayouts do not fulfil this product-level inventory scope.

待決事項：這個六城市旅遊商品目錄仍要照原規模推出，還是只保留目前飯店／目的地合作入口？若要继续，先核准一輪正式站唯讀現況盤點，再列具體匯入與啟用批次。

### 2. 2026-09-07-hotel-platform-options-and-quote-readiness

**仍有缺口，待站主決定/條件** — Hotel platform options and quote readiness

- PR #341 and historical data PRs through #367 all MERGED; #367 merged 1fb6e07b87d23d1cd24b96e6d6ecb0dcf5744857 on 2026-09-09.
- Latest task checkpoint is 60 identities, 30 approved products/30 pending and 100 approved options/260 pending; zero complete cities. These are historical counts only.
- docs/hotel-platforms/README.md explicitly warns pending JSON is not live sync truth; no later reviewed six-city completion record found.

剩餘／處理：Fresh current-state baseline; six cities each ten verified hotels, three areas, official plus two OTAs with all five OTA checks; complete maps/durable coordinates/links, then city release acceptance.

待決事項：要繼續完成六城市各10家、每家官方加2個OTA的原規格嗎？需要先同意正式站唯讀核對，再逐批呈現實際待審飯店和操作。

### 3. 2026-09-07-merchant-style-discovery

**仍有缺口，待站主決定/條件** — 網美與文青店家風格篩選、審核及首批來源資料

- PR #345 plus eight candidate batches through #361 MERGED; #361 merged a8adec5e4132e4392f20568708d043ac2292e7ea on 2026-09-09.
- Original task has one remaining DoD: exact maps/durable coordinates, administrator style review, then separate merchant publication.
- Recorded candidate import/replay evidence expressly preserves pending/inactive/unverified rows and is not public-style approval; no later full batch acceptance found.

剩餘／處理：Current candidate reconciliation and exact maps/durable coordinates, separate source-backed style approval and merchant publication via normal audited administration.

待決事項：是否繼續把這八批候選逐家完成地圖／座標／風格審核並發布？需要先核准正式站唯讀盤點；核准發布的名單另列給你。

### 4. 2026-09-07-mokaair-community-foundation

**仍必要，本輪執行可行部分** — Mokaair community foundation and account safety

- PR #340 MERGED 7f21d7eb2af223a561bc04519ce67021198b1068 with deployment recorded; PR #343 account-safety follow-up MERGED 2026-09-09.
- docs/community.md:197-212 still explicitly lists missing translation-failure/updated-original browser handling, five-locale/dark-mode journeys and worker/outage/capacity recovery.
- apps/web/e2e/community.spec.ts currently contains only three real-service journeys (publication/messages, pet rules, mail recovery/deletion); offline catch-up exists; no complete translation/outage/capacity browser matrix.

剩餘／處理：Implement/run missing isolated-service acceptance matrix; refresh outdated unchecked messaging/pet boxes from actual passed evidence. Production SMTP/S3/translation activation and public launch remain separate owner decisions.

待決事項：只有完成隔離驗收後才需決定是否公開啟用社群，以及正式寄信／物件儲存／翻譯與審核營運設定；目前本機測試工作可先做。

### 5. 2026-09-07-mokaair-community-web

**仍必要，本輪執行可行部分** — Mokaair community responsive web and five-language experience

- PR #340 MERGED and original task records all six desktop/mobile real community journeys passing at e096aeb; follow-up deadlock fixed before merge.
- docs/community.md:208-212 still lists five-locale and dark-mode community journeys plus translation failure/updated-original handling as open.
- apps/web/e2e/community.spec.ts has three base journeys; current file does not parameterize the complete five-locale/dark-mode matrix.

剩餘／處理：Run an explicit five-language/light-dark/responsive/accessibility/failure matrix on isolated services and fix actual failures; reconcile the many stale unchecked boxes with evidence rather than treating them all as unwritten code.

待決事項：無需先問即可做隔離驗收；公開啟用仍待站主另行決定。

### 6. 2026-09-08-continue-evidence-backed-remaining-hotspot-candidate

**仍有缺口，待站主決定/條件** — Continue evidence-backed remaining hotspot candidate review

- All bounded-batch checklist items are checked, but dated follow-up notes explicitly retain unresolved real queue work.
- Fourth batch historical result: 164 Korean rows blocked by exact Naver URL gate and nine non-Korean exceptions plus Taipei Sky Tower held pending by owner instruction.
- docs/hotspot-review-next-batch.md and ops/hotspot_review_next_batch.json contain receipts; task warns political/editorial value judgments need owner and old counts are not current.

剩餘／處理：Fresh live queue baseline; Naver exact URLs for Korea; individual source/map/coordinate blockers and owner editorial choices. Do not reject Taipei Sky Tower while the owner's opening hold applies.

待決事項：韓國景點要由你提供／人工查精準 Naver 網址後續做嗎？其餘有爭議紀念物與無独立地圖身分的例外，要先取最新清單讓你逐項裁決。

### 7. 2026-09-08-travelpayouts-live-destination-activation

**仍有缺口，待站主決定/條件** — Complete live Travelpayouts brand and destination offer verification

- PR #358 and #363 MERGED with recorded 2026-09-08 default/empty-state deployment.
- Task explicitly says destination_offer_count was zero; Klook landing 403, KKday unallowlisted invl.me hop and 403; browser acceptance never completed.
- PR #370 is direct Klook integration; task explicitly rejects treating that as Travelpayouts project approval.

剩餘／處理：Signed-in Project 570089 brand availability, 33-destination/module offer matrix, genuine final landing and tracking evidence, reviewed publication and real clickout analytics.

待決事項：Travelpayouts 的33目的地合作目錄要继续開通，還是保留直接 Klook 等現有渠道即可？若繼續，需可用的已登入品牌帳戶及逐批發布批准。

### 8. 2026-09-09-site-experience-settings

**仍必要，本輪執行可行部分** — Mokaair site experience palettes and managed information pages

- PR #380 MERGED 30a8e06ad003c177c46e487d2075cde09f496529 on 2026-09-09.
- docs/site-experience.md:43-45 records native same-document Back fixed on desktop/Pixel 7 and all twelve palette screenshots visually checked; automatic close/back regression is already implemented.
- Remaining named blocker is built-in-browser inspection on an isolated preview: six palettes, large text, nested modals/touch flows and public tools/community/pet/account. Earlier preview startup denial was environment-specific, not a permanent product requirement.

剩餘／處理：Create an isolated preview under current permissions and inspect the specified flows with CUA; retain owner visual acceptance separately if specifically required. No policy publication/deployment needed.

待決事項：可以先完成現有權限下的隔離預覽和內建瀏覽器查核；主觀外觀接受／正式發布再交站主決定。

### 9. 2026-09-11-deny-school-hospital-tram-stop-ward

**仍必要，本輪執行可行部分** — Deny school, hospital, tram stop, ward and military base types in hotspot discovery

- Original PR #403 MERGED/deployed, but later done task 2026-09-12-denylist-tombstones-real-attractions and #561 intentionally undo three of seven blanket denials.
- Current apps/api/app/hotspots/discovery.py:138-154 allows Q245016 military base, Q9842 primary school and Q16917 hospital back to human review; four remaining denied types and mixed-type regression exist in tests.
- The later done ticket still records owner production check owed for Q38278536, Q8669747, Q10911386, Q2410409; no outcome receipt found.

剩餘／處理：Correct this stale ticket's seven-type acceptance to four retained deny types plus protection/recovery verification for the three released types. Fresh read-only live discovery checks and four heritage-row status checks remain; do not reinstate reverted types.

待決事項：票面可先修正；正式站只讀查核四類與四筆歷史景點，之後如已誤退需再決定恢復操作。

### 10. 2026-09-12-food-merchant-enrichment

**仍有缺口，待站主決定/條件** — 反向用美食定位平台補齊待審店家資料（Gemini 補齊模式與瀏覽器批次匯入）

- PR #432 MERGED 50edf8555d633990f241bb4d4bac92378bdc0211 on 2026-09-12; task records A-D merged and deployed.
- apps/api/app/foods/data/enrichment/2026-09-12-pending-merchants.json still has records: []; docs/catalog-content-reviews/2026-09-12-pending-merchant-enrichment.md does not exist.
- Later #686 merchant_platform source tier and #688 CatchTable batch are a related route but do not establish this original 30-pending-merchant pilot acceptance; old JSON source rules are now historical.

剩餘／處理：Fresh production pending-merchant worklist, 30-row researched pilot under current source rules, dry-run/apply with unchanged coordinates/map/approval states, before/after counts and report.

待決事項：要繼續原本待審店家30家補齊試點嗎？若要，需要先核准正式站匯出唯讀工作清單；完成研究與 dry-run 後再核准具体寫入批次。

### 11. 2026-09-14-article-image-retry

**可依完成證據結案** — Article images recover from rate limits

- PR #470 MERGED d22c658ea23be72966e8f65098fb6dea71b9c649; original task records web code subsequently deployed.
- Later tasks/done/2026-09-19-edge-rate-limit-refuses-search-crawlers.md records actual production location / already using mokaair_content_pages, host application and reload 2026-09-19, and subsequent installer run twice changing only an eight-line comment.
- PR #568 MERGED; tasks/done/2026-09-12-nginx-deploy-checks-false-pass.md later takeover closes repository/host drift and records real nginx isolated validation: 120 image requests allowed, page budget preserved, seven non-image routes limited.
- Current prod-host-ops/references/nginx-edge.md:21-27 documents host's mokaair_content_pages and the article-image empty-key exemption.

剩餘／處理：No implementation/activation work remains supported by the historical evidence. The original 'host activation unknown' note predates later same-day verified host reconciliation.

### 12. 2026-09-14-article-sitemap-pagination

**可依完成證據結案** — Paginate article sitemap for all five languages

- PR #594 merged 2026-09-20.
- apps/api/app/guides/sitemap.py:entries has keyset cursor/next_cursor; apps/web/lib/guides.server.ts:loadGuideSitemap drains cursor pages.
- docs/article-localization/releases/batch030/README.md proves 2,256 sitemap entries over three pages were verified.

### 13. 2026-09-14-gemini-advanced-md

**站主指定保留，本輪不做** — Gemini 深入教學 69–74：MD 與 CLI 設定實驗

- PR #520 merged six authored lessons and real local CLI/fixture verification.
- Task and docs/gemini-series/advanced/content/md/verification retain unmet model-driven commands/skill execution/session-resume and shared release acceptance.

剩餘／處理：2026-09-29 owner explicitly said to retain the task and skip it this round. Existing acceptance requirements remain unmet.

### 14. 2026-09-14-gemini-advanced-platform

**可依完成證據結案** — Gemini 深入系列：可見篇章與發布批次支援

- PR #520 merged as a06afe22; main contains implementation and all original DoD/Steps checked.
- docs/gemini-series/advanced/platform/next-integration/verification.json records 160 unit cases, base/advanced 10 browser cases each, 272 article visits, build/typecheck/i18n/lint passed.
- Latest catalogue integration PR #947 builds on the same server projection; these platform-only tasks do not require publishing the advanced lessons.

剩餘／處理：Close completed implementation ticket; retain content/release acceptance separately.

### 15. 2026-09-14-gemini-advanced-visible-projection

**可依完成證據結案** — Gemini 深入系列：伺服器可見清單與投影驗證

- PR #520 merged as a06afe22; main contains implementation and all original DoD/Steps checked.
- docs/gemini-series/advanced/platform/next-integration/verification.json records 160 unit cases, base/advanced 10 browser cases each, 272 article visits, build/typecheck/i18n/lint passed.
- Latest catalogue integration PR #947 builds on the same server projection; these platform-only tasks do not require publishing the advanced lessons.

剩餘／處理：Close completed implementation ticket; retain content/release acceptance separately.

### 16. 2026-09-14-gemini-advanced-visible-ui

**可依完成證據結案** — Gemini 深入目錄：接收可見清單的介面與瀏覽器驗證

- PR #520 merged as a06afe22; main contains implementation and all original DoD/Steps checked.
- docs/gemini-series/advanced/platform/next-integration/verification.json records 160 unit cases, base/advanced 10 browser cases each, 272 article visits, build/typecheck/i18n/lint passed.
- Latest catalogue integration PR #947 builds on the same server projection; these platform-only tasks do not require publishing the advanced lessons.

剩餘／處理：Close completed implementation ticket; retain content/release acceptance separately.

### 17. 2026-09-14-gemini-advanced-work

**站主指定保留，本輪不做** — Gemini 深入教學 51–56：日常與工作流程

- PR #520 merged six drafts, lessons 52–54 revised packs, and actual Google Pro results.
- docs/gemini-series/advanced/content/work/verification/live-20260915/README.md explicitly leaves human assessment, iPhone Live, natural scheduled trigger and shared release open.
- The owner previously said to skip phone testing; do not silently reverse that instruction or invent a pass.

剩餘／處理：2026-09-29 owner explicitly said to retain the task and skip it this round. Existing acceptance requirements remain unmet.

### 18. 2026-09-19-api-keys-in-logged-urls

**仍有缺口，待站主決定/條件** — Google API keys ride in request URLs and the collector logs them

- PR #561 merged f521b902; header-based requests and regression tests exist.
- Task records 2026-09-19 deployment/log checks; owner key rotation explicitly unconfirmed.

剩餘／處理：Owner reports whether the exposed YouTube key was rotated and site setting updated; never read or copy secret values.

待決事項：已詢問：2026-09-19 後是否已輪替 YouTube API 金鑰並更新網站設定？

### 19. 2026-09-20-five-language-article-batch-003

**仍有缺口，待站主決定/條件** — Five-language article batch 003

- PR #592 merged four of five article translations; main has five locales on four packs but japan-onsen-ryokan-guide still only zh-TW.
- External batch003-live-ac860f38/browser-verification.json status=complete covers released subset.
- P2 2026-09-20-correct-hakone-and-noboribetsu-bathing-tax remains source-publication prerequisite; existing original claim/worktree present.

剩餘／處理：Finish guarded onsen zh-TW correction, re-pin live source, regenerate/review four translations, release; narrow old ticket to remaining onsen scope.

待決事項：是否將未完成的溫泉篇來源修正與四語翻譯接續執行，正式站修正另走逐步批准？

### 20. 2026-09-21-five-language-kansai-arrival-usj-batch

**可依完成證據結案** — Five-language Kansai arrival and USJ batch 008

- PR #629 merged 2026-09-21; both main packs contain five locales.
- Task DoD is reviewed content/PR with all checks ticked; external kansai-batch008-release/content-review-v8.json exists.

剩餘／處理：Content ticket complete; any new live release must use separate evidence.

### 21. 2026-09-21-localize-two-singapore-guides-in-batch

**可依完成證據結案** — Localize two Singapore guides in batch 010

- PR #635 merged.
- docs/article-localization/releases/2026-09-22/README.md and batch010-singapore/release-evidence.json record v6 approved source correction, 10 drafts/10 publications, 10 HTML and 20 browser cases.
- Main both packs contain all five locales.

### 22. 2026-09-21-taiwan-zh-tw-batch-004-taipei

**可依完成證據結案** — Taiwan zh-TW batch 004: Taipei viewpoints and where to stay

- PR #624 merged 2026-09-21.
- Both main packs have zh-TW and existing four locales; task explicitly only creates reviewed PR and prohibits merge/deploy/import itself; all DoD checked.

剩餘／處理：Publication is outside this PR-preparation ticket.

### 23. 2026-09-21-validate-equivalent-singapore-guide-numbers-and

**已過時，可刪除** — Validate equivalent Singapore guide numbers and food-directory links

- docs/article-localization/releases/2026-09-22/README.md explicitly supersedes #639 intermediate 112-warning findings: final 115/115 approved, zero blockers, two omitted SVG labels restored, durations reviewed, all five food-directory links localized.
- Final numeric-equivalence-review.json retained beside release evidence; batch010 fully published and browser-reviewed.

剩餘／處理：Remove obsolete queue ticket, preserve final evidence. Do not infer need for generic weakening of validator.

### 24. 2026-09-22-do-not-publish-the-two-batch010

**已過時，可刪除** — Do not publish the two batch010 Singapore guides until their review gate clears

- docs/article-localization/releases/2026-09-22/README.md explicitly says #647 assertions are superseded by the completed release and independent hash-bound receipts.
- Important: apps/api/app/guides/publish_holds.json still contains the stale two-Singapore hold reasons; removing a task must not silently imply modifying production holds.

剩餘／處理：Delete obsolete task; record stale hold-config reconciliation separately if not fixed in current scope.

### 25. 2026-09-22-document-batch-010-and-011-localization

**可依完成證據結案** — Document batch 010 and 011 localization release evidence

- PR #648 merged 2026-09-22; README and 15 small evidence/review JSON files are present in docs/article-localization/releases/2026-09-22.
- Record distinguishes zero GitHub reviews from independent hash-bound editorial review and resolves stale #639/#647 claims.

### 26. 2026-09-22-localize-jeju-car-rental-guide-in

**可依完成證據結案** — Localize Jeju car rental guide in five languages

- PR #643 merged 2026-09-22.
- Main five locales; docs/article-localization/releases/2026-09-22 records five drafts/five publications, five HTML and ten browser cases with independent LF SVG review.

### 27. 2026-09-22-localize-naver-map-and-kakao-t

**可依完成證據結案** — Localize Naver Map and Kakao T guide in five languages batch013

- PR #649 merged 2026-09-22; main five locales.
- External batch013/journal-production.json sha256 6caed8833f72e18fa4cd242797d5cb9c6d4784102b64a776cccc31764435c3d4 has four draft/four publish operations done and pending=null.
- batch013/public-qa-c54fd5ca/visual-review.json status PASS; 20 screenshots, 10 page cases, five expanded-source cases, all images/canonical/hreflang/overflow checks pass.

### 28. 2026-09-22-preserve-validated-variable-height-guide-diagrams

**可依完成證據結案** — Preserve validated variable-height guide diagrams

- PR #658 merged 2026-09-22.
- main pack_ingest.py has _body_svg_dimensions, staging/reuse dimensions, per-reference svg_dimensions_mismatch checks; all original DoD checked.

### 29. 2026-09-22-publish-reviewed-five-language-otaru-day

**可依完成證據結案** — Publish reviewed five-language Otaru day trip

- PR #646 merged 2026-09-22; exact committed review receipt says PASS_exact_committed_LF_blobs_and_visuals.
- External otaru-release/new-head/journal-production.json sha256 6e954b7f692cd977c48988b7e104d2b9bf41d3d2f71645fdd07d989b8e73def4 has five drafts/five published done and pending=null.
- public-qa-66fb5c57/visual-and-related-links.json status PASS sha256 7808fc9e95db5cc83ffc32f5ab0af6e84d3da48af0b12c27d06e1d617a09e089.

### 30. 2026-09-22-publish-reviewed-five-language-sapporo-itinerary

**可依完成證據結案** — Prepare reviewed five-language Sapporo itinerary PR

- PR #645 merged 2026-09-22.
- External sapporo-whitespace-committed-review/receipt.json PASS_exact_whitespace_only_PR_patch_and_identical_visuals binds final commit 1954d1bb2708b0c2ef5bc27aa19be83c01eb0c0c.
- sapporo-release-fixed/journal-production.json sha256 e5c352e7da839531bbf7771a4e5a472df109898d8f77467c78ddf7e4f0553865: five draft/five publish done, pending=null; public QA results also retained.

### 31. 2026-09-22-respect-per-slug-publish-holds-in

**仍必要，本輪執行可行部分** — Respect per-slug publish holds in localization bundle publisher

- main content_pack.py has load_publish_holds; docs/article-localization/publish_bundle.py has no hold guard and calls publish_locale directly.
- PR #652 is CLOSED, not merged; original remote branch remains but root checked no open PR modifies publisher.

剩餘／處理：Implement current-hold guard including dry run, newly-held phases, and lost-response reconciliation tests; root authorized this agent implementation.

### 32. 2026-09-23-internal-proxy-token-required-in-production

**仍必要，本輪執行可行部分** — Production accepts forwarded client addresses without the internal proxy token

- Current main validate_api_serving_security accepts empty proxy token; _from_our_proxy passes empty token.
- New regression before implementation: 9 failed, 2 passed; root is implementing startup requirement and safe development warning.
- No open PR files overlap the target; --force claim only bypasses merged #561 redis-migration infra.py scope.

剩餘／處理：Complete local tests; retain pre-merge production equality/presence check and paired-service rollout as explicit blocked acceptance.

待決事項：修正完成後，需核准正式站唯讀查核 API/web 代理憑證是否同值且至少32字元；只輸出判定，不顯示憑證。

### 33. 2026-09-26-video-dubs-worker

**現有PR工作或依賴，保留** — Video languages worker: the worker makes only the parts the owner chose (metadata, captions, dubs), packages them and sends the languages review

- PR #870 merged 2026-09-28T06:38:47Z; merge 79e26fcd is ancestor of current HEAD. All four required CI checks SUCCESS.
- tools/video/automation/flow.mjs:1573 has languages(); tools/video/core/stages.mjs:31/60 provides chosen-language state and captions.
- Task has one unchecked host acceptance: choose all three English parts and observe completion.
- Open draft PR #964 (efb9be7f) documents a real production languages-review 422 stopping the queue and implements recovery; its separate production acceptance task is in that branch, not main.

剩餘／處理：Retain ticket's host acceptance; coordinate with #964 and its queue-recovery verification. Code delivery alone and manually published dub tracks do not prove the chosen-parts worker flow.

待決事項：After #964 is merged and explicitly deployed, which approved video should be used for English metadata/captions/dub acceptance?

### 34. 2026-09-27-batch030-english-migration-diagram-fit

**可依完成證據結案** — Fit Batch030 English migration diagram labels

- PR #874 merged 2026-09-28; docs/article-localization/releases/batch030/README.md records exact corrected asset deployment, eight English desktop/mobile checks, four full-size SVGs, min margins 29–39, independent PASS and hold clearance.

### 35. 2026-09-27-correct-wordpress-migration-tag-links-batch030

**可依完成證據結案** — Correct WordPress migration tag links Batch030

- PR #855 merged; batch030 release README records exact two guarded inline corrections to zh-TW v6, verified backup, source journal SHA 818b89a6a7ed8c5293fe499fec4a96512158423be897a6b3d33221c601eabc79, independent source/public QA.

### 36. 2026-09-27-fix-batch028-english-page-builder-diagram

**可依完成證據結案** — Fix Batch028 English page builder diagram overflow

- PR #863 merged; batch028 release README records deployed SHA df4bee3246105b41378d09ef44e9c069f1a354b8c496b16f2c9d64833b6d4dc9 and minimum margin 15.42px.
- Final release QA included repaired English/Japanese diagrams, 40 page cases/20 mobile-right cases, all 20 card bounds pass, hold cleared.

### 37. 2026-09-27-fix-batch028-japanese-page-builder-diagram

**可依完成證據結案** — Fix Batch028 Japanese page builder diagram card padding

- PR #869 merged; batch028 release README records deployed SHA 017b9865991f441d0d48986378bcc4ca613b3bdbf121bcb65afb0f84f3cb7091 and margin 19.77px.
- Final independent acceptance SHA e4e4f872ae370a3bef8b1fc04f76eebbb3ea87b681e0997ae110c0a1111f3f26 includes both repaired diagrams.

### 38. 2026-09-27-news-evidence-excerpts-stop-at-8

**仍必要，本輪執行可行部分** — News evidence excerpts stop at 8,000 characters, so the checks never see the rest of the page

- PR #892 fixed HTML extraction but scanner still slices primary/linked text at 8000 and refresh does the same.

剩餘／處理：Agent implements bounded evidence preservation with long-source and pipeline-budget regressions.

### 39. 2026-09-27-video-drama-room-messages-api

**可依完成證據結案** — Video drama room API: a discussion thread on every series document and every episode's screenplay

- PR #870 merged; all required checks SUCCESS; task DoD/Steps all checked.
- apps/api/app/video_automation/messages.py:323 answer_message; admin_api.py:732 answer_video_series_message; migration 0108_video_drama_messages.py present.
- tools/video/automation/client.mjs:141 calls automation/series/messages/next.

剩餘／處理：Close open task with merged-PR and CI evidence; preserve history in tasks/done.

### 40. 2026-09-27-video-drama-room-one-off-series

**可依完成證據結案** — Video drama room: a one-off episode is a one-episode series with a single story bible document

- PR #870 merged; all required checks SUCCESS; all task checks complete.
- apps/api/app/video_automation/series.py:984 creates one-off series; models.py:450 includes one-off; migration 0107_video_one_off_series.py present.
- Current schemas.py:621 validates one-off form and series.py:1277 handles approved bible.

剩餘／處理：Close stale review task.

### 41. 2026-09-27-video-drama-room-web

**可依完成證據結案** — Video drama room web: the discussion thread on documents and screenplays, the one-off episode's page

- PR #870 merged; all required checks SUCCESS; all task checks complete.
- apps/web/components/admin-video-thread.tsx:44 implements DiscussionThread; admin-video-series.tsx:588 embeds document discussion; admin-video-reviews.tsx:288 embeds screenplay discussion.
- admin-video-thread.test.tsx and admin-video-series.test.tsx are present.

剩餘／處理：Close stale review task.

### 42. 2026-09-27-video-drama-room-worker

**可依完成證據結案** — Video drama room worker: the planner and the writer answer the owner's messages, every drama has a script gate, the brief comes from the approved document

- PR #870 merged; all required checks SUCCESS; all task checks complete.
- tools/video/automation/discuss.mjs:200 implements discussStep; client.mjs:141 provides message-next API.
- Task Notes and #870 describe one-off bible routing, script gate and re-verification after script edits.

剩餘／處理：Close stale review task.

### 43. 2026-09-27-video-languages-api

**可依完成證據結案** — Video languages API: each video's languages (metadata, captions, dub), the languages gate and ready-to-upload

- PR #870 merged; all required checks SUCCESS; all task checks complete.
- apps/api/app/video_reviews/admin_service.py:209 ready_to_upload; :861 preserves a recorded locale decision; :905 set_locales.
- apps/api/app/video_reviews/schemas.py:210 locales_decided_at and :212 ready_to_upload; migration 0106_video_locales.py present.

剩餘／處理：Close stale review task; do not confuse this implementation ticket with the dubs-worker runtime acceptance or #964 recovery.

### 44. 2026-09-27-video-languages-web

**可依完成證據結案** — Video languages web: the language panel after the final cut, the languages card, the publish card's five states

- PR #870 merged; all required checks SUCCESS; all task checks complete.
- apps/web/components/admin-video-reviews.tsx:115 LanguagePanel; admin-video-review-card.tsx:649 LanguagesBody; :134-164 derives publish states from ready_to_upload.
- Task documents five-language strings and panel/card/state tests as complete.

剩餘／處理：Close stale review task.

### 45. 2026-09-27-video-split-settings-api

**可依完成證據結案** — Video split settings API: the drama's own instructions, voice, rounds, gates, models and language defaults

- PR #870 merged; all required checks SUCCESS; all task checks complete.
- apps/api/app/video_automation/schemas.py:223 SettingsSave; migration 0105_video_split_settings.py and tests/test_migration_0105_video_split_settings.py present.
- Task Notes contain partial-save validation, independent drama models/voice, integration results; current test_video_automation_settings.py present.

剩餘／處理：Close stale review task.

### 46. 2026-09-27-video-split-settings-web

**可依完成證據結案** — Video split settings web: the settings tab splits into tutorial, drama and shared, each saved on its own

- PR #870 merged; all required checks SUCCESS; all task checks complete.
- Task Notes record owner-approved change: drama settings live on drama tab after #844, rather than third settings subtab.
- apps/web/components/admin-video-settings.tsx:27 defines tutorial/shared; :199/:204/:208 separate save bodies; :439 points to drama tab; admin-video-drama-settings.tsx wraps full drama settings.

剩餘／處理：Close stale review task; retain note explaining why the final location differs from original three-subtab DoD.

### 47. 2026-09-27-video-split-settings-worker

**可依完成證據結案** — Video split settings worker: a drama reads its own voice, standing instructions, rounds and language defaults

- PR #870 merged; all required checks SUCCESS; all task checks complete.
- tools/video/automation/flow.mjs:210 settingsFor; :247 settles chosen voice; :406 chosen instructions; :1398 verification rounds; :1433 retake rounds.
- Task Notes record fallback to tutorial on old sites plus unchanged tutorial behavior tests.

剩餘／處理：Close stale review task.

### 48. 2026-09-28-batch031-three-wordpress-target-locales

**可依完成證據結案** — Batch031 three WordPress target language drafts

- PR #879 merged 2026-09-28; main three packs have five locales; scoped evidence docs/article-localization/batch031-content-draft-evidence.md exists.
- Task explicitly covers 12 reviewed target documents +36 assets in draft PR; deployment/import/publication are excluded.

剩餘／處理：Do not call these live based on this closure; later release remains separate.

### 49. 2026-09-28-batch040-live-source-reconciliation

**仍有缺口，待站主決定/條件** — Reconcile Batch040 live zh-TW source revisions before locale release

- PR #930 repository source correction merged; PR #948 created separate live-source task.
- No release record exists; task explicitly requires isolated production-image rehearsal, verified backup and guarded three-slug live source writes; prior receipt only read-only baseline.

剩餘／處理：Fresh live conflict check, isolated rehearsal, exact approved guarded source publication for three slugs.

待決事項：是否核准準備 Batch040 三篇繁中來源修正的正式站發布方案，完成預檢/演練後再逐步批准寫入？

### 50. 2026-09-28-batch041-live-source-reconciliation

**仍有缺口，待站主決定/條件** — Reconcile Batch041 live zh-TW image SEO source revision before locale release

- PR #934 repository source correction merged; #948 separate live-source task.
- No release record; task says no nonproduction Docker environment and no mutation completed.

剩餘／處理：Fresh version/hash check, isolated rehearsal and guarded image-seo-workflow source publication.

待決事項：是否核准準備 Batch041 圖片 SEO 繁中來源修正的正式站發布方案，演練後再逐步批准寫入？

### 51. 2026-09-28-correct-measurement-guide-source-links-before

**仍有缺口，待站主決定/條件** — Correct measurement guide source links before localization

- PR #902 merged 2026-09-28; main four packs still only zh-TW and scoped evidence proves seven link-to-text corrections.
- docs/article-localization/batch036-measurement-source-links.md says must be followed by guarded zh-TW revision/publication before localization; no release evidence found.

剩餘／處理：Rebind published zh-TW source via guarded update for four measurement guides before translating; preserve task until live acceptance or split dedicated release ticket.

待決事項：是否接續這四篇 GA4/Search Console/UTM 的正式站來源修正，逐步批准後再翻譯？

### 52. 2026-09-28-localize-marketing-mix-and-brand-tone

**仍有缺口，待站主決定/條件** — Localize marketing mix and brand tone guides in Batch 036 Pair B

- PR #907 merged 2026-09-28; main both packs and all five locales present, scoped independent editorial GO documented.
- Unlike other content-only tickets, DoD explicitly includes import/publish and live-page verification; no release evidence found.

剩餘／處理：Guarded eight-locale publication and live browser QA; or move remaining release scope to separate ticket before closing content work.

待決事項：是否接續發布這兩篇已審稿的八份譯文（發布前會提出精確清單與預檢結果）？

### 53. 2026-09-28-localize-newsletter-content-guides-batch035-pair

**可依完成證據結案** — Localize Kit and content marketing guides (batch 035 pair B)

- PR #900 merged 2026-09-28; both main packs have five locales and scoped evidence record exists.
- DoD is reviewed complete drafts/24 assets and open reviewable PR; publication explicitly separate.

剩餘／處理：Live release remains separate and is not claimed.

### 54. 2026-09-28-localize-pestle-and-swot-tows-guides

**可依完成證據結案** — Localize PESTLE and SWOT/TOWS guides in five languages (Batch039 Pair B)

- PR #928 merged 2026-09-28; both main packs have five locales, scope evidence doc present.
- DoD covers draft content/24 assets/structural audit/editorial review; live release explicitly separate.

剩餘／處理：Live release remains separate and is not claimed.

### 55. 2026-09-28-video-1m-ai-agents

**仍必要，本輪執行可行部分** — Million-views batch 3: what an AI agent actually is, what one costs to run, and the setting that keeps it from spending your money

- PR #891 merged 2026-09-28T09:20:18Z; explicitly only stages 1-4, and verify-1.md is writer's own check.
- docs/videos/ai-agents-explained-what-they-cost contains brief.md, video.json, claims.md, verify-1.md; task explicitly lacks finished video/upload/English dub.
- No YouTube ID in checked video.json; no matching media folder at the two known local workdirs checked (this is not proof of global absence).

剩餘／處理：Independently recheck claims and mark the no-cache five-round bill as illustrative; then approved outline, narration, rendering, audio/final QA, languages and owner upload. Do not delete or close as if #891 delivered an MP4.

待決事項：For production continuation, confirm owner setup/paired tool access and whether to use existing option A; no paid generation or host setting change performed by audit.

### 56. 2026-09-28-video-1m-ai-price-war

**仍必要，本輪執行可行部分** — Million-views batch 1: GPT-6 Sol and Luna vs Claude Opus 5.5 price war, what your bill looks like now

- PR #891 merged; six packages are scripts and source checks only, not produced videos.
- docs/videos/ai-price-war-gpt-6-sol-vs-opus-5-5 has option-A script and fact claims; task reports dated 2026-09-28 checks but no independent verifier.
- Remaining owner setup in task: channel stance/outline, paired video-tool token and backend narration key. No verified finished media or upload receipt found in the checked sources.

剩餘／處理：Fresh independent official-price and worked-bill verification is actionable without credentials. Continue approved production only after setup and cost/host gates; retain task through upload and English dub.

待決事項：Confirm common six-video production setup and option-A outline choice if channel stance is not already configured.

### 57. 2026-09-28-video-1m-free-vs-paid

**仍必要，本輪執行可行部分** — Million-views batch 6: free vs paid AI plans 2026, is 20 dollars a month worth it, worked out

- PR #891 merged but explicitly leaves narration/render/upload undone and independent verifier outstanding.
- docs/videos/free-vs-paid-ai-plans-2026/claims.md:3/6/9 still marks OpenAI figures PENDING, including free uploads and Go/Plus prices.
- Task Notes explain source-environment 403 and require browser recheck before tts.

剩餘／處理：Independently verify currently pending OpenAI claims plus other pricing/limits; update script/claims consistently before narration. Then the same six-video production gates. This is genuinely unfinished, not obsolete.

待決事項：Use common six-video production setup decision; do not synthesize pending factual claims.

### 58. 2026-09-28-video-1m-google-vids-free

**仍必要，本輪執行可行部分** — Million-views batch 4: Google Vids makes AI video free with Gemini Omni 1.1, limits and a worked example

- PR #891 merged; only brief/script/writer fact-check delivered.
- docs/videos/google-vids-free-ai-video-omni-1-1 has script and sources. Task explicitly corrects Workspace Individual six-clip claim and references separate google-vids-quota-recheck article ticket.
- No finished media/upload/English dub acceptance in task or PR.

剩餘／處理：Independent official quota/account-type verification; retain both officially conflicting limits with correct account attribution if still present. Then approved production and owner upload.

待決事項：Use common six-video production setup decision; no need to ask whether a known factual recheck is useful.

### 59. 2026-09-28-video-1m-siri-ai

**仍必要，本輪執行可行部分** — Million-views batch 2: Siri AI on iOS 27, who gets it and how to turn it on

- PR #891 merged; package stages 1-4 only and all verify-1 files are writer checks.
- docs/videos/siri-ai-ios-27-how-to-get-it has option-A script; task :67 leaves outline, paired token, TTS and assembly outstanding.
- No finished video/English dub/upload acceptance found in the task/PR/current package.

剩餘／處理：Independent current Apple model/region/language availability check, then production gates. Preserve as needed unless owner changes topic strategy; not an obsolete ticket.

待決事項：Use common six-video production setup decision.

### 60. 2026-09-28-video-1m-vibe-coding

**仍必要，本輪執行可行部分** — Million-views batch 5: vibe coding your first website in 2026 with Claude, ChatGPT or Gemini, published free

- PR #891 merged; scripts and author checks only.
- docs/videos/vibe-coding-first-website-2026 contains brief/script/claims; task :59 says ChatGPT feature detail could not be read (403) and remaining production needs owner setup.
- No media/final QA/upload/English dub completion recorded.

剩餘／處理：Independent tool/hosting claims check and meaningful demonstration review; then approved narration/render/final QA/language pipeline and owner upload.

待決事項：Use common six-video production setup decision.

### 61. 2026-09-28-video-story-api-policy-languages

**現有PR工作或依賴，保留** — 故事版立場檢查、自動語系、釋放名額、媒體每小時上限與 Flash 單價

- Live PR #938 OPEN, non-draft, BEHIND, head d1aa02b13696af06b2d046fbfecf44719496bd5a; api/web/containers/full-stack-smoke SUCCESS on that head.
- Current main judge/admin_service/media files do not contain the PR's story policy/autolanguage flow; task still open because PR not merged.
- PR already owns the necessary implementation; don't reimplement in this audit.

剩餘／處理：Coordinate existing PR, update against current main and rerun required checks on new head before any separately authorized merge. Host pilot remains separate.

### 62. 2026-09-28-video-story-pilot

**仍有缺口，待站主決定/條件** — 試作兩支品牌故事並記錄數字

- Current docs/videos/STORY.md:287 trial record table remains placeholder for actual durations, costs, image quality and tokens.
- Dependencies story-worker #933 and story-policy #938 are still OPEN/BEHIND.
- Task explicitly requires two production-host videos A01 luggage/B18 conveyor sushi, owner final viewing, settings/limits and expenditure measurement; nothing in repository proves those occurred.

剩餘／處理：Keep pilot ticket. First land prerequisite implementations, then prepare explicit host deployment/config/import steps and selected two-video cost bound; owner watches completed cuts and chooses 1K vs 2K based on evidence.

待決事項：After dependencies are ready, approve a concrete production trial for A01 and B18 with the documented US$25 per-video ceiling, configured languages and host changes?

### 63. 2026-09-28-video-story-worker

**現有PR工作或依賴，保留** — 工人的故事流程：逐章撰稿、查核、審稿與提示詞

- Live PR #933 OPEN, non-draft, BEHIND, head 0cf33a304210bc8349e2a53246ca867e647bc9ed; api/web/containers/full-stack-smoke SUCCESS on that head.
- tools/video/automation/story.mjs does not exist on current main; PR implements it and describes mocked full-flow tests, fact-source extraction and narration-length checks.
- PR has a 2026-09-29 update and also implements story-page tidy follow-up; another active implementation exists.

剩餘／處理：Continue via existing PR owner/workflow, update to current main and verify new head rather than duplicating implementation. Real-media pilot is separate.

### 64. 2026-09-28-vps-youtube-studio-deployment-and-live

**仍有缺口，待站主決定/條件** — VPS YouTube Studio deployment and live private upload acceptance

- PR #893 merged 2026-09-28T06:55:22Z, but explicitly no production files/settings/containers changed, no Google login and no real upload.
- Task's host preflight is dated 2026-09-28 06:17-06:19 UTC and says to repeat before deployment.
- Synthetic DOM/container checks are documented, while owner exact version/steps/test-video/login and persistent private-video metadata/captions/thumbnail/translations/recovery acceptance are unchecked.

剩餘／處理：Retain. Prepare concrete deployment version/steps plus approved private test video; rerun preflight only in authorized production workflow, owner login/channel selection, and real persistent-state/resume validation.

待決事項：Which specific private test video and final deployment version should the owner approve for mokaair.com, and when can the owner perform Google login/channel confirmation?
