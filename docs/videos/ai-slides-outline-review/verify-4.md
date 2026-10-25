# 第四片獨立事實核驗 4 — PASS

RESULT: PASS

查核日：2026-10-25 UTC。查核者：`news_verify`，未撰寫本片或本次claims修補。這份收據只驗claims表格的格式／可追溯性修復，承接verify-3對R2三句／兩卡已實核保義的部分，不是新增全篇外部事實審查、故事改寫輪次、敘事盲讀或媒體驗收。只寫本報告；未修改source、claims、brief、素材、音訊、後臺、git，未執行付費操作。

## 固定版本及結果

- 當前video SHA256：`5c762406b378be00cfad56936a634399954185aabce05d4b95287fb40e632490`，與verify-3的R2 source完全相同。
- 當前claims SHA256：`848a55932e1e62fb5dbaedb40e62823f764c83a1c3906efe398b0bd76e0f10df`。
- 修前壞claims完整備份：`/workspace/work/ai-tech-next/fourth-r2/claims-before-traceability-repair.md`，SHA256 `6f31b4ed577dc8f7523f4df4679e9958a602a88e008316a98d8fb228c26f0526`，與verify-3受審版本相同。
- R1基線claims：`/workspace/work/ai-tech-next/fourth-before-r2/claims.md`，SHA256 `ece95ef98c2cdf06d78b710cc6bb458edba94fd93a90cbb8cf1b0786f8ab1d93`。
- 修補者的完整proof：`/workspace/work/ai-tech-next/fourth-r2/claims-traceability-repair.json`，SHA256 `50c4d071b607cdabebecfb0ba0c10cafa1bfbe15a3974db54888ad576523b882`。本查核從實際檔案重新推導結果，並逐131項比對proof，不以proof自稱成功代替核驗。
- 原verify-3 **REVISE保持原bytes**，SHA256 `5a61023f187e10ddab5ca636c9742ac9e46e80488adf10114010737b3a0ca6d7`；原verify-1 REVISE `8861a2673576e025a569dd417fe8323d7c06e2fd8ecf1081b0ca0ba01d91f749`、verify-2 R1 PASS `976641249d5027774cc9e7cc11b87e146313fa7a9b6d63d71c83a9ade4dfc382`亦未變。

**PASS：verify-3唯一必修F1已真正修復，0待修。** 120列scene逐ID恢復為R1原值；11列恢復原查核日期，並以`—`明示未列獨立scene。全部131列現在都是7欄，查核日均為原本的`2026-10-25`。當前R2每列原已存在的所有cells（包含三句quote／evidence、全部URL、數字及限制）逐格逐字不變，非claim行亦逐行保留原bytes。這是日期／scene欄恢復，不是新增或改正131項外部事實。

## 本輪實際核驗表

| # | claim／where | before → current | evidence／URL | HTTP | verdict |
|---|---|---|---|---|---|
| 1 | 全131個claim ID與表格欄位 | 120列6格、11列5格 → 131列皆7格；ID順序／唯一性相同 | 實際修前備份、當前claims、R1基線，逐ID解析 | LOCAL | CONFIRMED。131個ID無新增、重複、刪除或換序；表頭7欄與資料相符。 |
| 2 | 120個遺失scene | 空缺 → 各列R1原末格 | R1 claims原bytes與當前末格逐字比較；完整表見下 | LOCAL | CONFIRMED。包括全部118句的正確scene，以及c121／c133原多場景欄。 |
| 3 | c122–c132共11列日期／scene | 缺日期及scene → 2026-10-25／— | R1原查核日期、當前第6／7格 | LOCAL | CONFIRMED。恢復日期，未捏造原本不存在的單一scene。這11項仍由既有claim ID被實際scene.claims引用。 |
| 4 | 所有原有前綴cells，尤其c8／c54／c114 | R2三句quote／evidence／URL → 全部逐字相同 | 當前claims與修前壞claims完整前綴；verify-3已核的R2來源 | LOCAL | CONFIRMED。只追加被丟欄位及11個明示佔位，不把R1舊旁白蓋回R2。 |
| 5 | 全部非claim行 | 修前 → 修後完全相同 | 逐行保留換行符比較；標題、來源索引、限制、敘事判定等 | LOCAL | CONFIRMED。沒有順便改來源／限制、移除REVISE歷史或改盲讀結果。 |
| 6 | 118個active spoken line的quote／claim／scene | 修前可由ID追溯 → 現可同時從實際scene欄追溯 | 當前video.json／claims.md逐條交叉驗證 | LOCAL | CONFIRMED。118/118皆唯一claim、quote精確、claim在正確scene.claims、scene cell精確相同。 |
| 7 | 全131個定義與實際引用 | 原定義集 → 同一131個ID，全部在scene.claims使用 | 全90場scene.claims集合與claims定義集雙向比較 | LOCAL | CONFIRMED。131/131被引用；未定義引用0、未使用定義0。 |
| 8 | R2 source及所有非claims依賴 | verify-3 source → bitwise相同 | 與fourth-r2/video.candidate.json全bytes比較＋完整source SHA | LOCAL | CONFIRMED。118句、90場、6章、metadata、assets、voice、subtitles等都沒改。 |
| 9 | 原創資料／新增資產bytes | verify-3與R1已核產物 → 同SHA | 20份copied data與4份R1新增SVG／PNG實際重算完整SHA | LOCAL | CONFIRMED。沒有以資料／素材改動迎合表格；未重畫未變圖片。 |
| 10 | 原生metadata／description／lint | 上輪6章3129 bytes → 本輪相同 | 實跑原生API及CLI；下列結果 | LOCAL | CONFIRMED。0 errors、2 warnings、problems[]；沒有媒體或敘事PASS推論。 |

本輪沒有新增網址或外部事實；官方6個primary URL、pinned公開包URL與原URL cells全部不變。verify-3所列同日正常UA HTTP200 raw／SHA收據仍適用於相同依賴；本輪未重發HTTP請求，沒有把LOCAL格式驗證冒稱新GET。

## 全131列可追溯性逐項結果

每列目前均7格，第1–5格及修前已存在的第6格均精確保留。下表列出實際當前date／scene；120個scene等於R1原值，c122–c132的`—`是明示未列單一scene，並非新增實測資料。

| # | claim ID | checked_on | current scene cell | verdict |
|---|---|---|---|---|
| 1 | c1 | 2026-10-25 | four-page-local-output | CONFIRMED |
| 2 | c2 | 2026-10-25 | sum-question | CONFIRMED |
| 3 | c3 | 2026-10-25 | two-to-four-question | CONFIRMED |
| 4 | c4 | 2026-10-25 | handoff-question | CONFIRMED |
| 5 | c5 | 2026-10-25 | dated-news-hook | CONFIRMED |
| 6 | c6 | 2026-10-25 | local-authored-scope | CONFIRMED |
| 7 | c7 | 2026-10-25 | source-record-start | CONFIRMED |
| 8 | c8 | 2026-10-25 | source-report | CONFIRMED |
| 9 | c9 | 2026-10-25 | sixty-source-pages | CONFIRMED |
| 10 | c10 | 2026-10-25 | briefing-audience-and-target | CONFIRMED |
| 11 | c12 | 2026-10-25 | briefing-audience-and-target | CONFIRMED |
| 12 | c13 | 2026-10-25 | report-and-data-year | CONFIRMED |
| 13 | c14 | 2026-10-25 | report-and-data-year | CONFIRMED |
| 14 | c15 | 2026-10-25 | year-label-consequence | CONFIRMED |
| 15 | c16 | 2026-10-25 | two-metric-question | CONFIRMED |
| 16 | c17 | 2026-10-25 | money-versus-respondents | CONFIRMED |
| 17 | c18 | 2026-10-25 | money-versus-respondents | CONFIRMED |
| 18 | c19 | 2026-10-25 | split-metric-record | CONFIRMED |
| 19 | c20 | 2026-10-25 | two-page-number-introduction | CONFIRMED |
| 20 | c21 | 2026-10-25 | two-page-number-fields | CONFIRMED |
| 21 | c22 | 2026-10-25 | two-page-number-fields | CONFIRMED |
| 22 | c23 | 2026-10-25 | locate-and-identify-figure | CONFIRMED |
| 23 | c24 | 2026-10-25 | locate-and-identify-figure | CONFIRMED |
| 24 | c25 | 2026-10-25 | prompt-field-question | CONFIRMED |
| 25 | c26 | 2026-10-25 | reusable-full-prompt | CONFIRMED |
| 26 | c27 | 2026-10-25 | prompt-card-one | CONFIRMED |
| 27 | c28 | 2026-10-25 | prompt-card-one | CONFIRMED |
| 28 | c29 | 2026-10-25 | prompt-card-one | CONFIRMED |
| 29 | c30 | 2026-10-25 | prompt-card-two | CONFIRMED |
| 30 | c31 | 2026-10-25 | prompt-card-two | CONFIRMED |
| 31 | c32 | 2026-10-25 | prompt-card-two | CONFIRMED |
| 32 | c33 | 2026-10-25 | prompt-card-two | CONFIRMED |
| 33 | c34 | 2026-10-25 | prompt-card-three | CONFIRMED |
| 34 | c35 | 2026-10-25 | prompt-card-three | CONFIRMED |
| 35 | c36 | 2026-10-25 | prompt-card-three | CONFIRMED |
| 36 | c37 | 2026-10-25 | prompt-card-three | CONFIRMED |
| 37 | c38 | 2026-10-25 | missing-year-question | CONFIRMED |
| 38 | c39 | 2026-10-25 | specific-field-feedback | CONFIRMED |
| 39 | c40 | 2026-10-25 | outline-usability-question | CONFIRMED |
| 40 | c41 | 2026-10-25 | author-initial-outline | CONFIRMED |
| 41 | c42 | 2026-10-25 | author-initial-outline | CONFIRMED |
| 42 | c43 | 2026-10-25 | same-material-both-pages | CONFIRMED |
| 43 | c44 | 2026-10-25 | material-list-not-page-question | CONFIRMED |
| 44 | c45 | 2026-10-25 | author-written-stages | CONFIRMED |
| 45 | c46 | 2026-10-25 | no-product-conversation | CONFIRMED |
| 46 | c47 | 2026-10-25 | what-decision-to-change | CONFIRMED |
| 47 | c48 | 2026-10-25 | change-page-question | CONFIRMED |
| 48 | c49 | 2026-10-25 | concentrated-feedback-a | CONFIRMED |
| 49 | c50 | 2026-10-25 | concentrated-feedback-a | CONFIRMED |
| 50 | c51 | 2026-10-25 | concentrated-feedback-a | CONFIRMED |
| 51 | c52 | 2026-10-25 | concentrated-feedback-b | CONFIRMED |
| 52 | c53 | 2026-10-25 | concentrated-feedback-b | CONFIRMED |
| 53 | c54 | 2026-10-25 | concentrated-feedback-b | CONFIRMED |
| 54 | c55 | 2026-10-25 | visible-change-question | CONFIRMED |
| 55 | c56 | 2026-10-25 | page-one-metric-separation | CONFIRMED |
| 56 | c57 | 2026-10-25 | page-one-metric-separation | CONFIRMED |
| 57 | c58 | 2026-10-25 | global-page-relationship | CONFIRMED |
| 58 | c59 | 2026-10-25 | global-corporate-value | CONFIRMED |
| 59 | c60 | 2026-10-25 | global-private-subset-value | CONFIRMED |
| 60 | c61 | 2026-10-25 | sum-question-payoff | CONFIRMED |
| 61 | c62 | 2026-10-25 | double-count-reason | CONFIRMED |
| 62 | c63 | 2026-10-25 | page-two-subset-output | CONFIRMED |
| 63 | c64 | 2026-10-25 | national-total-question | CONFIRMED |
| 64 | c65 | 2026-10-25 | regional-private-scope | CONFIRMED |
| 65 | c66 | 2026-10-25 | us-private-value | CONFIRMED |
| 66 | c67 | 2026-10-25 | china-private-value | CONFIRMED |
| 67 | c68 | 2026-10-25 | private-not-national-spend | CONFIRMED |
| 68 | c69 | 2026-10-25 | page-three-same-scope-output | CONFIRMED |
| 69 | c70 | 2026-10-25 | usage-page-new-unit | CONFIRMED |
| 70 | c71 | 2026-10-25 | survey-reported-ai-use | CONFIRMED |
| 71 | c72 | 2026-10-25 | survey-reported-ai-use | CONFIRMED |
| 72 | c73 | 2026-10-25 | survey-not-census | CONFIRMED |
| 73 | c74 | 2026-10-25 | unresolved-block-delivery-question | CONFIRMED |
| 74 | c75 | 2026-10-25 | two-source-observations | CONFIRMED |
| 75 | c76 | 2026-10-25 | wording-needs-alignment | CONFIRMED |
| 76 | c77 | 2026-10-25 | both-2025-unresolved | CONFIRMED |
| 77 | c78 | 2026-10-25 | do-not-adopt-either-rate | CONFIRMED |
| 78 | c79 | 2026-10-25 | page-four-annotation-output | CONFIRMED |
| 79 | c80 | 2026-10-25 | citation-record-connects-pages | CONFIRMED |
| 80 | c81 | 2026-10-25 | find-original-figure-question | CONFIRMED |
| 81 | c82 | 2026-10-25 | page-two-citation-filled | CONFIRMED |
| 82 | c83 | 2026-10-25 | page-two-citation-filled | CONFIRMED |
| 83 | c84 | 2026-10-25 | follow-the-citation | CONFIRMED |
| 84 | c85 | 2026-10-25 | follow-the-citation | CONFIRMED |
| 85 | c86 | 2026-10-25 | page-three-citation-filled | CONFIRMED |
| 86 | c87 | 2026-10-25 | page-three-citation-filled | CONFIRMED |
| 87 | c88 | 2026-10-25 | page-four-citation-filled | CONFIRMED |
| 88 | c89 | 2026-10-25 | annotation-source-position | CONFIRMED |
| 89 | c90 | 2026-10-25 | adopted-versus-annotation | CONFIRMED |
| 90 | c91 | 2026-10-25 | editable-handoff-question | CONFIRMED |
| 91 | c92 | 2026-10-25 | handoff-two-uses | CONFIRMED |
| 92 | c93 | 2026-10-25 | pdf-and-pptx-handoff | CONFIRMED |
| 93 | c94 | 2026-10-25 | pdf-and-pptx-handoff | CONFIRMED |
| 94 | c95 | 2026-10-25 | pptx-native-object-evidence | CONFIRMED |
| 95 | c96 | 2026-10-25 | editable-unit-text | CONFIRMED |
| 96 | c97 | 2026-10-25 | powerpoint-test-boundary | CONFIRMED |
| 97 | c98 | 2026-10-25 | before-presenting-in-your-app | CONFIRMED |
| 98 | c99 | 2026-10-25 | completed-delivery-package | CONFIRMED |
| 99 | c100 | 2026-10-25 | news-workflow-connection-question | CONFIRMED |
| 100 | c101 | 2026-10-25 | review-position-connection | CONFIRMED |
| 101 | c102 | 2026-10-25 | official-format-and-review | CONFIRMED |
| 102 | c103 | 2026-10-25 | official-review-objects | CONFIRMED |
| 103 | c104 | 2026-10-25 | official-feedback-then-proceed | CONFIRMED |
| 104 | c105 | 2026-10-25 | review-is-optional | CONFIRMED |
| 105 | c106 | 2026-10-25 | outline-lock-after-proceed | CONFIRMED |
| 106 | c107 | 2026-10-25 | review-this-deck-content | CONFIRMED |
| 107 | c108 | 2026-10-25 | account-availability-question | CONFIRMED |
| 108 | c109 | 2026-10-25 | announced-gradual-rollout | CONFIRMED |
| 109 | c110 | 2026-10-25 | announcement-versus-help | CONFIRMED |
| 110 | c111 | 2026-10-25 | no-account-result-to-resolve | CONFIRMED |
| 111 | c112 | 2026-10-25 | check-your-option | CONFIRMED |
| 112 | c114 | 2026-10-25 | goal-not-tied-to-menu | CONFIRMED |
| 113 | c115 | 2026-10-25 | adapt-the-same-brief | CONFIRMED |
| 114 | c116 | 2026-10-25 | adapt-the-same-brief | CONFIRMED |
| 115 | c117 | 2026-10-25 | adapt-the-same-brief | CONFIRMED |
| 116 | c118 | 2026-10-25 | write-your-first-page | CONFIRMED |
| 117 | c119 | 2026-10-25 | write-your-first-page | CONFIRMED |
| 118 | c120 | 2026-10-25 | write-your-first-page | CONFIRMED |
| 119 | c121 | 2026-10-25 | page-one-metric-separation、page-two-subset-output、page-three-same-scope-output、page-four-annotation-output、completed-delivery-package | CONFIRMED |
| 120 | c122 | 2026-10-25 | — | CONFIRMED |
| 121 | c123 | 2026-10-25 | — | CONFIRMED |
| 122 | c124 | 2026-10-25 | — | CONFIRMED |
| 123 | c125 | 2026-10-25 | — | CONFIRMED |
| 124 | c126 | 2026-10-25 | — | CONFIRMED |
| 125 | c127 | 2026-10-25 | — | CONFIRMED |
| 126 | c128 | 2026-10-25 | — | CONFIRMED |
| 127 | c129 | 2026-10-25 | — | CONFIRMED |
| 128 | c130 | 2026-10-25 | — | CONFIRMED |
| 129 | c131 | 2026-10-25 | — | CONFIRMED |
| 130 | c132 | 2026-10-25 | — | CONFIRMED |
| 131 | c133 | 2026-10-25 | completed-delivery-package／thumbnail | CONFIRMED |

## source、metadata與原生檢查

本輪重新確認當前source完整bytes等於verify-3所綁定R2 candidate。因整檔相同，三張完整prompt卡、三種交付、2026報告／2025資料區分、五項採用數值及單位／母體／子集限制、70／79未對齊政策、本地作者同次產出與未試用Notebook界線、帳號方案未解限制均沒有被這次表格修補改動。這是依賴保真核對，不冒稱重新對全部外部事實做了一輪獨立研究。

20份原data實際bytes／SHA皆與verify-3記錄吻合；新增四頁縮覽、縮圖的4個SVG／PNG亦逐完整SHA吻合。source中9筆assets的source／license與voice／style／metadata原封相同，沒有修改授權、資料或媒體。

以本repo原生`loadProject`、`estimateTimeline`、`composeMetadata`、`creditedAssets`與`creditBytes`重新執行唯讀計算：

- description：**3129 UTF-8 bytes**；SHA256 `68b24ac0e94060a585da3fba66ef1b459cc675407a6a05acc82f8eaff0c3b0ea`，與verify-3相同。
- metadata problems：`[]`。
- 實際輸出credit：**1筆／272 bytes**；9筆assets記錄不等同9筆可輸出credit，未刪原credit。
- 實際原生輸出：6章，完整三卡提示、6個官方來源URL、pinned資料包URL與原本地／未實測／未原生PowerPoint渲染限制完整保留。
- 估時658.2333秒（11.0分鐘）、118句、2323 spoken units；這是估時，未當作實際音長。

| estimated at | actual composed chapter |
|---|---|
| 00:00 | 我從公開報告寫下簡報需求 |
| 00:25 | 來源紀錄把金額與使用比例分開 |
| 02:10 | 完整需求交出後，作者初稿仍擠在兩頁 |
| 04:03 | 集中修改讓四頁各自有了任務 |
| 07:08 | 第二到第四頁接回原報告 |
| 09:13 | Google公告新增生成前的大綱審查 |

實跑`node /workspace/work/ai-tech-next/run-video-slides.mjs lint --slug ai-slides-outline-review`：exit 0，**0 errors、2 warnings**。warnings仍為約25秒冷開，以及immj／f6fw／cwpj的2025重現；未改成0 warnings。原生輸出中的章節時間仍是估時，沒有執行TTS／音檢或成片驗收。

## 限制與收尾

- verify-3 F1：**CLOSED**，以實際131列恢復結果確認；原verify-3 REVISE及壞claims備份保留。
- 當前source／新claims的窄範圍格式及可追溯性：**PASS，0待修**。本輪實質外部事實更正0項；沒有觸發「超過3項事實更正」再換人規則。
- R2三句／兩卡保義結論承接固定同一source的verify-3實核，沒有把claims-only修復當新增全篇事實審查。
- 未讀或修改新盲讀raw答案，不把敘事NO改成YES；本PASS不等同新敘事PASS，也不是另一輪故事改寫。
- 未做Notebook帳號試用、PowerPoint原生渲染、付費模型、TTS／ASR、音軌／M4A、成片、八語或發布操作。本收據不宣稱上述交付可用。
- PASS只綁source `5c7624…`／claims `848a55…`；不要覆寫歷史REVISE或套用其他SHA。

