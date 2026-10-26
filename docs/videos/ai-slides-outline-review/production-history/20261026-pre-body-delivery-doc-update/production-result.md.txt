# 第四片製作進度快照

截至2026-10-25T23:30:48Z，原句兩輪重錄後仍標記的nm8j／h58h／j47b已作保義修詞，獨立[verify-5](verify-5.md) PASS。3個新request／67 billable chars的TTS已完成，100個高層request重用；**當前新take尚未完成ASR及嚴格音訊核驗，沒有成片QA或正式交付**。

| 項目 | 實際狀態 |
|---|---|
| 凍結版本 | source `296fa0c93be25c7074ec50259db650f5663aca2324a5e0a16da2118406757c2f`；claims `2c56550a6ffde77c8ee781f909554a8c94c9f7d787f877fc34b4c385160778f7`；speech `a8055d3edb90bcda`。 |
| 三句差異 | 只有3個line.text及3個claims quote；其餘115個完整line物件／全部非text欄位不變。131列全7欄、118口白／claim／scene對帳、defined＝used＝131。 |
| 原句音檢歷史 | 初次118 checked／111 accepted／7 flags；retake1為113 accepted／5 flags；retake2於23:18:43為115 accepted／3 flags／0 unchecked。這是舊speech0f1，不是新a805已通過。 |
| 最新TTS | 23:22:54原生stage完成3 requests、67 billable chars、100 reused、無fallback；103是118句的高層規劃request數，不是精確付費HTTP次數。 |
| 當前TTS時間 | 18106 frames／30＝603.5333秒；outro前591.3667秒；扣冷開及outro的正文566.1333秒。這是TTS時間，不是已驗收音訊或編碼片長。 |
| 已完成render | 舊source5c於23:16:47完成114 new states、477秒、exit0；114張圖SHA逐一等於真正看過的R2 preview。current visualHash同為1a6b602366198b99，三句text不改圖卡／transition／縮圖。 |
| 敘事 | R2兩raw及citation修復後native各12／13、passed=false，no_recap保留；本次僅知情三句差異核對，沒有新blind／新分數。 |
| 原生靜態檢查 | lint0 errors／2 warnings；current TTS timeline compose3129 bytes、6章、1 credit／272 bytes、problems[]。不是final package QA。 |

原verify-1 REVISE、verify-2 R1 PASS、verify-3欄位回歸REVISE及verify-4恢復PASS均保留原SHA；verify-5只綁當前三句與其固定依賴，不改歷史。數值／條件／作者示例／C6註記與五項採用值界線不變，沒有Notebook產品試用或UI導覽。

## 尚未完成

- 必須對新a805三個take完成正常ASR，再作全目標、原生WAV／cache／裁決／實際完成證據的嚴格唯讀核驗。既有3旗與未來新結果分開，不清旗或修改轉寫。
- strict helper僅CFG.source／speech兩值更新，其餘bytes等於原版；root已留14項self-test輸出。本次只驗差異、不執行actual audit，不宣稱current audio PASS。
- 114張已完成圖片及靜態visualHash相同不代表encoded film或QA完成；待音訊通過後才能合成／字幕／核心QA與正常後臺交付。
- 本producer仍缺合法官方品牌bookend package／素材；靜態outro不能當正式片頭尾已裝。追蹤ID `2026-10-25-local-first-build-without-branding` 位於第三片分支，此處不造跨分支相對連結。
- 八語metadata／CC／實際M4A與整包交付尚未完成，all_eight_ready及overall均false。沒有YouTube公開、合併或部署。

詳[機器可讀進度](production-progress.json)、[current TTS timing](narration-current-timing-snapshot.json)、[知情敘事差異](narrative-listener-reword1-informed-review.md)及[收據索引](production-receipt-index.json)。

## 23:44 UTC 後續音訊結果

當前 a805 原生複檢已實際 exit0：118／118 句接受、0 flags／unchecked（84 exact、15同音／語助、6 Jev、13第二轉寫）。[嚴格唯讀核驗](narration-listener-reword1-verification.json)綁定全部118個當前WAV、完整原文、spoken form、有效原生裁決、最新TTS及完成log，ready=true／problems=[]，正文566.1333秒。這項後續結果取代上方快照中的待音檢狀態，歷次旗標及原敘事false不變。

正常script／audio送審已pending，本機另依站主委派採用；詳[narration-backend-adoption.json](narration-backend-adoption.json)，不冒稱遠端批准。現正合成本體候選，仍缺官方片頭尾；未有實際MP4完成、核心QA或影片後台交付證據。八語已建立原生翻譯底稿，尚無已完成外語媒體。
