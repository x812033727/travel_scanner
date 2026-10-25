# 第四片獨立事實核驗 5 — PASS

RESULT: PASS

查核日：2026-10-25 UTC。查核者：news_verify，未撰寫原片或套用本次修改。本輪只驗原句兩輪重錄後的三句聽感修詞、對應claims及固定依賴；**不是當前音訊、敘事盲讀、成片或八語PASS**。沒有修改source／claims／lexicon／assets／media，沒有付費、後臺、git或實際音訊audit執行。

## 固定版本與結論

- 當前video SHA：`296fa0c93be25c7074ec50259db650f5663aca2324a5e0a16da2118406757c2f`。
- 當前claims SHA：`2c56550a6ffde77c8ee781f909554a8c94c9f7d787f877fc34b4c385160778f7`。
- 原生speechHash：`a8055d3edb90bcda`。
- 實際完整修前archive：`/workspace/work/ai-tech-next/fourth-audio-archives/before-listener-reword1`；video `5c762406b378be00cfad56936a634399954185aabce05d4b95287fb40e632490`／claims `848a55932e1e62fb5dbaedb40e62823f764c83a1c3906efe398b0bd76e0f10df`。

**PASS，三句保義及差異依賴0待修。** 真正兩版JSON逐葉比較只有nm8j、h58h、j47b三個line.text改動，118個ID及順序相同、其他115個完整line物件與所有非text欄位相同。當前claims各回復這三句舊quote後，**完整bytes精確等於修前claims**；沒有其他字、欄位、來源或日期變動。全131列皆7欄，原日期／scene修補未回歸，118句quote／claim／scene全吻合，defined＝used＝131，無未定義／未使用主張。

## 三句完整核驗表

本輪無新增外部事實或URL，證據為原本已核的本地原創示例、完整上下文及其固定manifest；LOCAL不冒稱新HTTP GET。

| # | line／scene／claim | before → current | evidence／URL | HTTP | verdict及理由 |
|---|---|---|---|---|---|
| 1 | nm8j／missing-year-question／c38 | 如果大綱少填資料年，這時要改哪裡？→大綱如果漏了資料年份，要在哪裡補上？ | data/input-brief.json；完整三卡；下一句9h68；https://github.com/x812033727/travel_scanner/tree/c8308b78321ad3ebc23bf516d1828203d07a40a8/docs/videos/ai-slides-outline-review/data | LOCAL | CONFIRMED。明示如果、資料年、補欄位的問題均保留，非報告年份／發布日，未改成產品已發生漏欄位或新增UI導覽。9h68仍回答該頁資料年欄。18字，guard[]、未知Latin[]。 |
| 2 | h58h／author-written-stages／c45、c129 | 我把自己寫的初稿和集中修改，一起留在範例紀錄裡。→我自己寫的初稿和整批修改要求，都留在範例紀錄裡。 | data/outline-before-review.json、review-feedback.json、build_demo.py；同一pinned資料包；下一句z84y | LOCAL | CONFIRMED。保留作者自己編寫初稿與一批feedback要求，沒有把修改要求改成模型回應或修訂成品；同一紀錄／集中一次修改不變。z84y同次產出、無真實停等仍完整。24字，guard[]、未知Latin[]。 |
| 3 | j47b／adopted-versus-annotation／c90、c128 | 它留在註記欄，沒有混進已採用的五項數值主張。→這個差異只放在註記欄，不列入已採用的五項數值主張。 | data/page-citation-manifest.json；實際s4.svg；前句m5bu；C1–C5採用、C6 annotation_only_not_adopted_rate | LOCAL | CONFIRMED。差異回指C6兩處來源觀察，前文cwpj／iek7仍限定問法／分母未對齊、不判報告錯誤；只作註記、不列入五項的否定及中文五字完整。不是五頁／五樣本或已確認採用率。25字，guard[]、未知Latin[]。 |

純函式rewriteProblems會保護阿拉伯數字、Latin及字典term次數，不會保護中文五、語義或條件；本輪另外核對這些部分。三句未新增／刪除數字、日期、產品名或字典詞，無say／say_for變更；字典不需改動。五值581.69／344.66／285.88／12.41／88及各自範圍、2026報告／2025資料、70／79未解政策，均在未變的原句及資料中保留，未重做或改寫原研究結果。

## 原旗標、精確subset與歷史收據

完整archive的check-flags.json speech仍為0f1e427877b23e0e，旗標精確為nm8j／h58h／j47b，與套用3個ID完全相等；8gv2／gy6e未被順便改動。實讀actual-check.log末段及原旗標：nm8j聽成「資料呢」、h58h聽成「幾次修改」、j47b聽成「實質主張」，有效原生裁決仍各有旗。23:18:43.205Z原句retake2的118 checked／115 accepted／3 flags／0 unchecked與exit1由root實際完成回報及application保存；本輪沒有把旗標清除，也不把ASR近音直接宣稱為主觀聽到的錄音錯字。

條件式預備審稿當時的eligible IDs=null狀態保持歷史效力；後來這份已完成原句R2證據才支持精確subset套用。`listener-reword1-application.json`不預寫音訊PASS。本輪只確認文字與當前claims，三個新take仍須完成正常ASR／全目標核驗。

| 舊收據 | 完整SHA，均保持原bytes |
|---|---|
| verify-1 REVISE | 8861a2673576e025a569dd417fe8323d7c06e2fd8ecf1081b0ca0ba01d91f749 |
| verify-2 R1 PASS | 976641249d5027774cc9e7cc11b87e146313fa7a9b6d63d71c83a9ade4dfc382 |
| verify-3 R2 claims回歸REVISE | 5a61023f187e10ddab5ca636c9742ac9e46e80488adf10114010737b3a0ca6d7 |
| verify-4 欄位修補PASS | 8d87f739f2af241cde9a35b5f0eef6b31d0ac9523c417841e4a49f1df4c592e9 |

## 素材、畫面及嚴格auditor設定

全部scene.data／asset記錄／thumbnail／metadata／voice／style／subtitles／loops／章名均與修前完整相同。本輪重算9個asset檔及20份原copied data的fullSHA，皆吻合先前獨審記錄；沒有以改資料迎合新旁白。

root的完整render已exit0、114 new states、477秒；`fourth-render-still-binding.json`明示綁舊source5c。本輪逐114檔實際重算PNG SHA，全部等於該收據及原已看R2 preview SHA；原生純函式visualHash修前／修後同為`1a6b602366198b99`。因此三句詞彙不改任何stills／transition／thumbnail，沒有重畫必要；**這不是新speech時間軸、完整encoded film或QA驗收**，也不是本查核者重新看完114張圖片。

新strict helper `/workspace/work/ai-tech-next/verify-slides-narration.listener-reword1.mjs` SHA `504fe71404cb73a3e19c3830aaab71b7dae564ff3e90b672ff8268ab1decc966`，與原helper SHA `4921dbf39faa304de8965de6f45478e2e9b2f8430ab84a0985f8444259c932a1`逐bytes反替換相等：只有CFG.source 5c→296f、CFG.speech 0f1→a805兩個值。其餘matcher、全目標長度、confidence、WAV綁定及寫入限制等所有bytes相同。root先前14項self-test輸出已保存，本輪只讀並記SHA，不重跑self-tests或actual audio audit，也沒有重跑既有236工具測試。

完整證據及114 PNG hash、9 asset hash、helper兩CFG反替換核對在`listener-reword1-independent-delta.json`。

## 原生lint與compose

本輪唯讀native lint exit0：**0 errors、2 warnings**，仍為短冷開與immj／f6fw／cwpj的2025必要重現。未改成0 warnings。

23:23:36讀到的actual timeline已是current speech a805、18106 frames／30＝603.5333秒；這只表示當時TTS時間軸，**不表示當前take已音檢PASS**。用當前source＋該current TTS timeline原生compose：3129 UTF-8 bytes、problems[]、6章、1筆實際credit／272 bytes；description SHA `c0908b397e916efe7752db0db1d952c6a98691b7424b31b824cbf8769bc7fe25`。若後續重錄改時間，須依更新timeline再組成。

| current TTS at | chapter |
|---|---|
| 00:00 | 我從公開報告寫下簡報需求 |
| 00:25 | 來源紀錄把金額與使用比例分開 |
| 01:58 | 完整需求交出後，作者初稿仍擠在兩頁 |
| 03:37 | 集中修改讓四頁各自有了任務 |
| 06:29 | 第二到第四頁接回原報告 |
| 08:29 | Google公告新增生成前的大綱審查 |

另外的estimateTimeline為659.2333秒，僅估時，不混為實際TTS。兩種compose都有3129 bytes但時間戳／SHA不同，完整結果在`listener-reword1-native-static.json`。

## 知情敘事差異及收尾

重新讀R2兩份原始回答、citation修復及各自native結果：原raw回答均12／13；原生未帶line ID的advisory格式記錄曾為11／13，補足引用後兩份仍**12／13、exit1、passed=false**，必要NO均是no_recap。原始與格式修復檔完整保留，未把它們合併成13／13。

本輪是知情的三句lexical差異核對：nm8j仍是同一條件問題，h58h仍交代作者初稿／集中修改紀錄，j47b仍是C6排除於五項主張。沒有新增／移動／刪除章、掛鉤或回收；原no_recap證據rrvd／r3y9及jzkh／frra都沒改。故未發現這三句帶來新的敘事語義問題，但原NO與教學取捨保持，不重算分數、未做新blind，也不把舊文字面板的90秒估算當新實際音訊驗收。

新增外部事實更正0項，0待修，未觸發超過3項實質事實更正的第二人規則。此PASS只綁296f／2c56的三句與上述固定依賴；音訊、成片QA、正式品牌片頭尾、八語與後臺交付仍各需自己的實際收據。
