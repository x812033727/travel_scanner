# A01／B18 品牌故事新版試作｜奇聞檔案局規格

> 2026-10-18 A01 片長決定：站主選擇 A01 正文約 7–8 分鐘、保留緊湊有鉤子的故事；[r9 離線候選](preproduction-20261016/A01-duration-decision-20261018-r9/README.md)只把該集 `target_minutes` 改為 `[7, 8]`，保留 r8 凍結稿及其獨立增量審查。B18 與後五集仍約 10 分鐘，試作系列仍為 10 分鐘。r9 也繼承 r8 `video.json.sources` 不完整且含無關來源的 **P1／HOLD**，不能匯入。文字估時不是 TTS 實測；正式工人九至十一分鐘關卡尚未作 A01 限定調整，六章、實稿、音檔及成片審核都未因此通過。以下 10/17 段落是當時快照，當前正式機狀態須重新讀回。

> 2026-10-17 當時實況：#1548 已合併部署；A01 歷史發音表固定（80→81）及 round22 六章採用（81→82）已在正式機提交並完成讀回。來源收據見 [81／82 採用與驗證](preproduction-20261016/A01-pinned-lexicon-transition-candidate-20261017/README.md)。六章真正工人查核與 listener 已完成；整體 narrative 第10輪只剩 one_line 未過，單句修訂待重審，獨立 script-review 尚未通過，也尚無配音、MiniMax 圖片或成片。B18 與後五支的付費製作未啟動。

2026-10-17 較早的狀態快照（A01 寫回資訊由上方實況取代）。**A01 已匯入正式站，但整片敘事第 9 輪仍有三項未通過，尚未進入配音、插畫或成片。後續來源與敘事修正仍是隔離的離線候選，尚未寫回正式機。B18 的 85 景企劃資料列、獨立來源審稿收據與雙集匯入檔已接入本機套件；65 筆逐景主張仍是 `UNCHECKED`，沒有正式匯入或啟動付費製作。** 這次本機採用的[備份及讀回收據](preproduction-20261016/B18-active-before-attribution-flow-20261017/adoption-manifest.md)綁定 canonical story `d0a9e19d311def1130c50cf6ba83a9ffb7f58c435e7c2460901abb211fe03648`。[新版說書節奏完整稿](preproduction-20261016/B18-spoken-source-cadence-candidate-20261017/README.md)已取得僅限離線文字的獨立事實與敘事 PASS；它還須與 85 景正式章稿對齊、查核 65 筆主張並測 TTS，不能視為成片或正式工人收據。[逐景對齊方案](preproduction-20261016/B18-fullscript-route-b-plan-20261017/README.md)及[符合十項事實上限的後繼 Row10b](preproduction-20261016/B18-route-b-row10b-candidate-20261017/README.md)仍只是隔離設計，未改現用企劃或工人章稿。企劃審查不代替主機實稿或成片驗收。部署與主機證據見 [A01／B18 試作票](../../../tasks/open/2026-09-28-video-story-pilot.md)。舊 100 題庫及其審稿維持原樣。

站主已選定品牌故事改成奇聞檔案局新版規格：MiniMax `image-01`、精確 `look: {"preset":"cute-mystery"}`；A01 正文單獨改為 7–8 分鐘，B18 與後五集正文仍約 10 分鐘。先完成 A01／B18 試作及站主看片，再做[已選的五支](../brand-stories-five-20261014/README.md)。**目前只有 A01 獲明確授權，所有付費項目合計最多 US$25。** [最新報價 v3](../brand-stories-five-20261014/drafts-20261016/cost-proposal/B18-five-production-cost-proposal-v3.md)提議 B18 與後五集每集最多 US$5、六集共 US$30，仍待站主答覆；正式機也要先具備相符的逐片限額。站主已免除訂閱／供應商餘額證明，不再要求帳務截圖。既有全片帳本、預留／結算與未確認支出仍須核對。

B18 的既有全文、收據、工人輸入與剩餘差距已做[準備度核對](readiness-20261016/B18-readiness.md)。該報告固定在 `e15df0219` 的檔案版本，17 個來源檔案已逐一對照 Git 內容雜湊；本頁的狀態與費用文字在其後更新。

較早的 [B18 分鏡與開場候選](preproduction-20261016/README.md)保存 103 鏡、三組同圖預告／回收與各自獨立覆核；它是歷史備料。本機輸入已改採下述 85 景候選，這項接入沒有改動主機或媒體。

A01 已保留[第九輪實際全文與獨立診斷](script-review-20261016/README.md)，可直接閱讀三項退回各自對應的段落與規則差異。[開場到起源的單句銜接候選](readiness-20261016/A01-hook-origin-candidate/README.md)另存原檔、候選與完整 SHA；未寫入正式機，未建立新的通過收據或啟動第十輪。

2026-10-17 的[第 19 輪離線候選](preproduction-20261016/A01-round19-origin-year-repeat-candidate/README.md)在第 14 輪來源修正後，逐輪保存起源企劃、逐句來源及重複年份的窄修；每輪有獨立 manifest。[精確來源差異](preproduction-20261016/A01-round19-origin-year-repeat-candidate/independent-review-20261017.md)及[108 句整稿人工閱讀](preproduction-20261016/A01-round19-origin-year-repeat-candidate/independent-full-script-review-20261017.md)已各自完成離線覆核，沒有找到新的確定旁白阻擋。[第 20 輪](preproduction-20261016/A01-round20-i17-fact-index-candidate/README.md)只補一筆來源表事實索引；[獨立差異複核](preproduction-20261016/A01-round20-i17-fact-index-candidate/independent-review-20261017.md)已通過，108 句旁白未變。正式工人的 verifier、listener、盲讀敘事審核與實稿收據仍未完成；這不是第九輪失敗的覆寫，也不是配音、MiniMax 圖像或成片完成。

[A01 的 80→81 詞典稽核唯讀閘門](preproduction-20261016/A01-host-transition-export-candidate/README.md)與[獨立程式審查](preproduction-20261016/A01-host-transition-export-candidate/independent-review-20261017.md)已完成離線範圍；聚焦測試 6／6 通過。第 81 筆只會處理既有稿與共用詞典的來源綁定，**不會安裝第 20 輪六章**；既有章稿還需要另一筆受審的修訂與正式機排他寫入、前後讀回。2026-10-17 後台唯讀顯示 A01 仍因第九輪說故事審查停住，英／日／韓配音勾選已儲存但須等無燒錄字幕中文版與可關閉繁中 CC 成片過審才製作。

B18 較早的 103 鏡分鏡保留為歷史備料；[單線敘事與逐景主張候選](preproduction-20261016/B18-claim-granularity-candidate-20261017/README.md)為 **85 景、88 句、66 景插畫、65 筆正式狀態 `UNCHECKED`**，靜態正文估算 560.97 秒，沒有 TTS 實測。後繼的[法院 PDF 分源候選](preproduction-20261016/B18-court-pdf-split-candidate-20261017/README.md)及[獨立審查](preproduction-20261016/B18-court-pdf-split-candidate-20261017/independent-review-20261017.md)修正一行旁白與兩個畫面提示，法院對第 579776 號的 1972 年認定僅引用 PDF 並由人工核讀；其他來源的 1978 年說法只保留為分歧註記，本片不口播。1971／1974 年給茶設備分歧也只留於查核註記。新版工人輸入資料列的獨立審查與本機雙集重編已完成；正式 verifier、listener、narrative、語音、圖像、CC、成片與站主看片仍待完成。

| 順序 | 新版作品 slug | 觀眾追的問題 | 新版企劃 |
| --- | --- | --- | --- |
| A01 | `story-rolling-suitcase-v2` | 輪子箱早有前案，為何直到 1970 年才進百貨公司？後來如何更順手？ | [輪子行李箱](A01-rolling-suitcase.md) |
| B18 | `story-conveyor-belt-sushi-v2` | 一間缺人的壽司店如何把啤酒工廠輸送帶變成新吃法？ | [迴轉壽司](B18-conveyor-belt-sushi.md) |

本包的 [`series.json`](series.json) 是**兩集獨立新系列** `brand-stories-curio-pilot-v2`，第 1、2 集依序安排中午時段。工人真正讀的是資料庫中的六章 `beats`；[`episodes/A01.json`](episodes/A01.json) 與 [`episodes/B18.json`](episodes/B18.json) 才是供新版審稿與將來編譯的輸入。每支保留母企劃的十項必查事實與來源索引，重寫了標題、問題、六章因果與開場伏筆；母企劃原檔與審稿在 [`brand-stories-100`](../story-plans/brand-stories-100/README.md)。新版 slug 與系列隔開舊排程，也避免把舊版媒體或批准誤當新版結果。**本包的完整 `scripts/*.md` 不會隨 `stories.json` 匯入；工人會依六章 `beats` 另寫 `story/chapters/*.json`，再合併成 `video.json`／`script.md`。**

## 試作匯入的精確批次

`kind: story` 會挑最早的 `ready` 集數啟動，**不受 `series_auto_continue=false` 阻止**。A01 已在正式站匯入；目前本機重編的 [`stories.json`](stories.json) SHA-256 為 `c02fa490725c169c5cb84c0bf05ae9afa1a0c9bac65d8e17d7c602aafed9871b`，其中 A01 資料列與接入前的編譯檔逐位元組相同，B18 換成最後獨立覆核的來源歸屬、轉角故障敘述與新收據。**這不是當初 A01 匯入檔的相同 SHA，不能依舊的 `--limit 1 --apply` 步驟重跑。**

待 A01 的實際帳本、旁白、成片與站主看片都通過，再用這份當時重新核對 SHA 的雙集輸入以 `video-story-import --series brand-stories-curio-pilot-v2 --limit 2` 唯讀試跑；必須確認 A01 在正式站維持不變、只有 B18 待新增，且沒有 `rows.update`、額外 `rows.create`、`problems` 或 slug 衝突。屆時重新做正式機、佇列和預算前檢，取得 B18 付費核准後才可考慮 `--apply`。每日集數或關閉自動接續都不能當成 B18 尚未入列的證據；關掉 `drama_auto_approve_final` 是留給站主看成片的另一道關卡，不能代替精確匯入。

## 每支影片的觀看順序

1. 第 1 秒進入具體場景。旁白開場 30–60 秒，只預告後續三個有年份的轉折，在結果前停住；預告要按事件順序，正文逐一回收。
2. 第一章後接頻道 **5 秒動畫片頭**。第二章從人物和困境出發，之後每章由上一章的結果引出下一個問題，不念章節目錄，也不重播已說過的答案。
3. 六章合計目標旁白正文 **約 10:00**，實際秒數由 TTS timeline 與 `ffprobe` 量。正文至少 8 分鐘；材料不足就縮短或退回企劃，不能用沉默、慢播或片頭片尾充數。只用台灣口音單人旁白；繁中字幕跟音訊。
4. 正文末三句回答開場、留一題與故事相關的留言問題、給有理由的訂閱邀請。接 **21 秒動畫片尾**；YouTube Studio 在最後 16 秒設「最符合觀眾喜好」影片、訂閱與「最新上傳」影片，實際上傳後逐項點擊驗證。MP4 卡位本身不可點。

畫面以 MiniMax 可愛卡通**靜態插畫**說故事。`look` 只能是 `{"preset":"cute-mystery"}`，不加 `style` 或 `negative`；不生成商標、名人肖像、真實文件內文。全部正文鏡頭用 `visual: "still"` 與後製緩慢運鏡，**生成影片 clip 鏡頭數為零**；片頭片尾沿用頻道既有 v4 動畫素材。配樂與重試都須計入該片獲准的全項上限。繁中字幕使用可關閉 CC；英／日／韓配音可由站主先勾選，但須等無燒錄字幕的繁中成片與可關閉繁中 CC 通過審核後才開始製作。提示詞逐鏡只寫時地、景別、**一個一般化人物做一件事**、焦點與柔和／陰天／檯燈等中性光線；物件或風景鏡頭也要有該人物的動作，避免晴朗正午與飽和綠色植物。正文至少 70% 是插畫 `shot`，連續卡片最多三張；卡片只放必要的數字、名字、短引文或來源。插畫是故事示意，不聲稱重建歷史現場。預估 75–120 張只是排程假設，付費前需依定稿分鏡估全片張數、重畫、judge、TTS、文字模型、轉錄與合成的上限。

## 審稿與交付關卡

- 本包的 `episodes/*.json` 已重排敘事，**母企劃審稿的 hash 不再適用**。另一位查核者須打開來源、逐章比對新版敘述、為每支另寫 `episodes/reviews/<ID>.json`，並以新版 `story_sha256` 綁定；尤其核對 A01 的 1970 年接受、1928 年箱子的製作年界線、Samsonite 1997／2000 年表及 Travelpro 競爭者說法，B18 的轉彎靈感兩種來源、20／50 日圓、實用新案與多重擴張因素。不得把本機結構檢查當獨立查核。
- 目前企劃 canonical hash：A01 `c247eba081af44e183549d26f34bcdd0d9d98c3e9205672641c8a58b9ebd424d`；B18 `d0a9e19d311def1130c50cf6ba83a9ffb7f58c435e7c2460901abb211fe03648`。兩份[獨立審稿](episodes/reviews)各自綁定現有資料列；B18 的最近前版與更早版本原始檔、收據及匯入檔分別保存在[最新接入前備份](preproduction-20261016/B18-active-before-attribution-flow-20261017/backup.json)、[可讀登記前備份](preproduction-20261016/B18-active-before-readable-registration-20261017/backup.json)和[更早備份](preproduction-20261016/B18-active-before-row-adoption-20261017/adoption-manifest.md)，舊收據不再適用。這只核准企劃資料列的來源敘述，不能代替逐字稿、逐景主張或成片審查；若 JSON 任一字更動須重新計算並重審。
- `node docs/videos/brand-stories-pilot-v2-20261015/build.mjs --draft` 驗證結構後，兩份新版審稿讓 `--write` 編出本機 [`stories.json`](stories.json)；Python `check_story_file` 回傳兩支、零問題／拒絕／忽略。正式環境 exact slug／佇列／媒體／鎖與版本仍須唯讀查驗，才可評估匯入。
- 匯入後先核對工人實際產出的六章 `story/chapters/*.json`、`video.json` 與 `script.md`。逐章與本包已審的完整旁白比對開場伏筆、年份、因果、來源限定與結尾回收；若要採用本包逐字稿，須依工人的章檔格式逐章接入並重新跑 lint、事實查核與聽眾審稿，不能只覆寫下一輪會被章檔重建的 `video.json`。若採用工人新稿，須另做逐句事實查核與完整敘事盲評，並以**實際稿件的 hash** 留下審稿收據。本包手稿的 PASS 不自動核准工人新稿。兩個 `-v2` slug 在正式 worker 的 `script` 關卡會因缺少 `<VIDEO_WORKDIR>/<slug>/story/reviews/script-review.json` 而停住；獨立審查者依[操作欄位](../../../tasks/open/2026-10-14-support-10-minute-minimax-cute-brand.md)比對實稿並寫入 hash 綁定的 PASS 收據，站主才可明確重試。若章稿或合併稿改動，舊收據失效並再次停住。依實稿重排逐鏡表、預估配音長度與整集成本後，才能進入 TTS 與圖像生成。批准付費後記錄每項實際支出、鏡頭與音訊 hash。`video.json`、TTS、圖像、片尾可點元素和站主看過成片，各要各自的證據。

A01 的完整編輯稿與獨立收據在 [`scripts/`](scripts/)：[稿件](scripts/A01.md)／[審查](scripts/reviews/A01.md)，但它們不會隨 `stories.json` 匯入。B18 的[第三版完整說書稿](preproduction-20261016/B18-spoken-source-cadence-candidate-20261017/B18.md)及[獨立全文文字審稿](preproduction-20261016/B18-spoken-source-cadence-candidate-20261017/review-candidate.md)保留在隔離候選，口播檔 SHA `7b286566…` 的離線文字審查 PASS；**它仍不能當正式 worker `script-review.json` 或逐景 verifier PASS**。曾短暫將第三版接入本機 `scripts/B18.md` 的[歷史採用收據](preproduction-20261016/B18-script-before-spoken-source-cadence-20261017/adoption-manifest.md)仍保留，後續 GitHub CI 發現此舉違反 worker 的舊稿參考 SHA gate，現已從逐位元組備份還原 `scripts/B18.md`／`scripts/reviews/B18.md` 至 `5326bd66…`／`1583b363…`，與現行 worker 相符；第三版須待章稿、來源與程式參考更新並重審後才能採用。舊稿面估值 A01 約 9:02、B18 約 9:06 使用每分鐘 300 字，不能當成實錄；第三版 B18 粗估正文 8:53、含片頭片尾 9:19，同樣要以正式 TTS 量測。兩集舊分章畫面與全項成本假設見 [A01](A01-shot-plan.md)、[B18](B18-shot-plan.md)，其中 B18 的 US$25、餘額證明與舊完成狀態已由本頁及最新報價取代。正式逐鏡清單、實錄與全項帳本仍須逐一驗證；舊版 100 題每日排程不因這兩筆新版 draft 自動更改。

## 2026-10-17 離線採用與報價續查

- A01 的[第 20 輪既有章稿修訂模型](preproduction-20261016/A01-round20-existing-revision-offline-candidate/README.md)把共用詞典 80→81 轉換與章稿 81→82 修訂分開，保留第九輪真實 FAIL 與舊輪數稽核；六章重新從本次第 1 輪查核。[獨立修正審查](preproduction-20261016/A01-round20-existing-revision-offline-candidate/independent-fix-review-20261017.md)只通過此離線差異。乾淨 PR 工作樹的合成交易與真實 worker 上限探針共 8／8 通過；正式機適配器、寫入鎖、即時捕捉和新一輪 worker 結果仍缺，A01 仍是第九輪說故事審查 FAIL。
- [A01 唯讀匯出提案閘門](preproduction-20261016/A01-round20-host-export-plan-candidate/README.md)串接 80→81 匯出檢查與 81→82 修訂計畫，合成資料的 5／5 定向測試、語法檢查和獨立程式複核通過。它不連主機、不寫資料，也沒有正式 apply；尚無新鮮完整的主機捕捉或所有寫入者共用的排他鎖，結果一律維持 `HOLD`。
- B18 的[新資料列與來源覆核](preproduction-20261016/B18-worker-input-adoption-candidate-20261017/independent-review-20261017.md)保留 85 景、88 句與 65 筆 `UNCHECKED` 逐景主張；[後繼版](preproduction-20261016/B18-worker-input-name-trim-candidate-20261017/README.md)移除來源未證實的啤酒公司名稱。獨立審稿者以新故事 SHA `3c43dc0c0eccdb063cc1e62d756c48ce2a476c5bfe1a70b74799c8f3cfc475f1` 簽了只限企劃資料列的[精簡收據](preproduction-20261016/B18-review-short-20261017/README.md)；原收據和 821／800 字拒絕診斷另存。已將此版接入本機 [`episodes/B18.json`](episodes/B18.json)、[`episodes/reviews/B18.json`](episodes/reviews/B18.json) 並重編雙集 `stories.json`；兩次編譯 SHA-256 均為 `07a71fc18c3aa12d426dcc1c9ecd30e59c150079a1e83d868b7024c09670c999`，A01 列與接入前相同。原始檔與雜湊見[接入前備份](preproduction-20261016/B18-active-before-row-adoption-20261017/adoption-manifest.md)。此為本機套件接入，主機未匯入。
- B18 更後繼的[法院 PDF 分源資料列](preproduction-20261016/B18-court-pdf-split-candidate-20261017/README.md)經[第二位獨立審稿人](preproduction-20261016/B18-court-pdf-split-candidate-20261017/independent-review-20261017.md)核讀官方判決；新收據只對 canonical SHA `7a598d16c9efcd9014f3554531dfe5569408cb1542cbeb1f90fdfbff4b0975e5` 有效，且只把法院專屬的 fact 4 設為 `reviewer_only`。已接入本機 row／review 並重編雙集，SHA-256 `ac1dbde239039f722c902e48dbde7b0ed0d1f628d3ba6b8f57afaef53248bd54`；A01 編譯列未變。前版原始檔與雜湊見[本次備份](preproduction-20261016/B18-active-before-court-split-20261017/adoption-manifest.md)。這不是 B18 正式匯入或逐章、逐景查核；65 筆場景主張仍 `UNCHECKED`。
- B18 當時的[可讀登記事實分源候選](preproduction-20261016/B18-readable-registration-candidate-20261017/README.md)把 1962 年白石名義登記與名稱的 `e6/e7` 直接交給可讀的發明協會來源 S2 核對，法院專屬 fact 4 只保留第 579776 號 1972 年期滿與後續業者的認定。[獨立審查](preproduction-20261016/B18-readable-registration-candidate-20261017/independent-review-20261017.md)核准 canonical SHA `da692f3833f3d5448e3ec7603f0549a4f9b1afe2828c00aa8ee657618584a5e1` 的企劃資料列，`reviewer_only:[4]` 不變。已先[備份舊 row／review／雙集檔](preproduction-20261016/B18-active-before-readable-registration-20261017/backup.json)，再接入本機；當時 `stories.json` SHA-256 `16e314adf3c94953ac17ea5f15e9cc9f96b2e51ab5489be524c16b762cfaa055`，編譯 A01 列逐欄相同，API `check_story_file` 為兩支、零問題／拒絕／忽略。後來的來源歸屬與轉角修訂已另行審查並接入本機，目前 SHA 見本頁上方。85 景、88 句與 65 筆 `UNCHECKED` 不變；正式 verifier、主機匯入、配音、插畫與成片仍未進行。
- [B18 全片費用刷新](preproduction-20261016/B18-cost-refresh-candidate-20261017/README.md)以 66 張插畫及正常重試估算 US$2.08798 稅前；[獨立審查](preproduction-20261016/B18-cost-refresh-candidate-20261017/independent-review-addendum-20261017.md)確認計算與 102 次產圖、另 102 次規劃審圖的說法。B18 加後五支各 US$5、六支總上限 US$30 仍只是未核准提案；正式機須完成 0133 migration 並讀回六個原始帳戶和未結操作，摘要顯示有效 US$5 不能單獨證明已升級。A01 的 US$25 授權不延伸到其他六支。
- 五支新片仍按 A29 樂高、A16 Costco、A37 Adidas／Puma、B14 味之素 ABF、A21 品客順序，在 A01／B18 實際成片與站主看片後製作。五集目前只有本機稿件、工人輸入及分鏡，沒有正式 TTS、MiniMax 圖像、CC、MP4 或上架。#1510 保持草稿及 `no-auto-merge`；此處 PASS 均只限離線範圍。
