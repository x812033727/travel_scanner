# 四語字幕與包裝文字獨立覆核

檢查日：2026-10-07。覆核者未撰寫 `ag018`、`ag097` 的八句譯文。英文／簡中由 `preflight_consumer` 完整讀取，日文／韓文由 `inline_recovery_review` 完整讀取；均對照目前繁中來源、claims、示範紀錄、既有查核及共用 lexicon。

**目前文字、五語 CC 草稿與未核准 metadata draft 的覆核完成。** 四語各 142 句，共 568 個譯文 entry，另有每語標題、說明、標籤及六章標題共 36 組 metadata，已完成內容覆核。實際 719 個 cue 的時間、CPS、切分及來源 ID 已核對；一項日文跨 cue 拆詞問題已透過正常 native worksheet／merge／captions 流程修正並實際重驗。成片、音訊、站主語言選擇與正式 upload package 的核准不在這個結論內。

## 獨立收據與目前檔案

`<operation-root>` 代表站主保留的 `ai-agent-continuation-20261007` 私有操作資料夾。以下收據均在其 `caption-review/`，不包含憑證；完整檔案 SHA-256 綁定讀取版本，review ID 是本次獨立文字覆核 ID，不是 production approval。

| 覆核範圍／ID | 收據 | SHA-256 |
| --- | --- | --- |
| 英文／簡中 284 句；`ac818520-7107-4f47-80c4-7ffe1892c548` | `en-zh-CN-current-content.review.json` | `8c29b6aaf397145251f0732b7cdb1c53600d2420d15d84508ea70b5c1dac9819` |
| 日文／韓文 284 句；`ai-agent-ja-ko-current-content-20261007T112217892Z` | `ja-ko-initial.review.json` | `ddadbdf6155660bf2cde448f589c21ed7a49b517c5c700dc7f78f178a2fff4ae` |
| 彙整；`ai-agent-caption-content-20261007T112605Z-v2` | `current-content-review.pending.v2.json` | `1434bfc9ea2de3f47ff58adf40db22bda99a56f597406e223adeb68f7b85c73e` |
| 實際 JA／KO 293 cues 的初次覆核；`ai-agent-ja-ko-actual-captions-20261007T114206827Z`，記錄拆詞問題 | `ja-ko-actual-captions.review.json` | `6b4d01bfdba7e6b856f4165e09a0359ea9cd3c7d957784a9b9b9c8635d93262c` |
| 單逗號候選的獨立覆核；`ai-agent-ja-ag080-punctuation-independent-20261007T114425316Z` | `ja-ag080-punctuation-candidate.review.json` | `46a0b6a1a4926fbad8b3647e937e3a4cac6bad89e3925ef2279ae437abeb11f2` |
| 目前五語 SRT／metadata draft 實際檔案覆核；`ai-agent-actual-caption-bindings-2026-10-07T115100363Z` | `actual-captions.bindings.final.json` | `f6f7a33376991115510e1098a44913965b8921f8a9b16e72549578080f355f5f` |

初次文字彙整 observed UTC：`2026-10-07T11:26:10.792015+00:00`；目前實際 CC／metadata 覆核 observed UTC：`2026-10-07T11:51:00.365Z`。四語均為 142 個唯一 ID、與來源場景順序相同、無空白／缺漏／多餘／stale entry，568 個 native `source_hash` 均對應目前來源文字。初次合併每語只有 `ag018`、`ag097` 的 text／source_hash 更新；將兩個 entry 還原後，整份翻譯與 `original-<locale>.json` 快照深度相等。其後日文只另在 `ag080` 加一個逗號，其他 141 個 entry 與 metadata 均精確保留，詳見下方 before／after 證明。原 pending 收據保留為當時階段證據。

| 目前已讀檔案 | Bytes | SHA-256 |
| --- | ---: | --- |
| `video.json`，目前 visual 版 | 36751 | `905ac35021688b7ca80264f12afd6f8973b959317438538e2199bdb4536a058c` |
| `i18n/en.json` | 19784 | `6698e7fb1c3ea61feecf19c50d9b54fb66c57d06761125214f3773ad06244ecf` |
| `i18n/ja.json`，含 `ag080` 逗號修正 | 22423 | `fbe6477c4964b164e3c4352a4d950f39e11de7f3616d5af5ccde8e1e0769cd19` |
| `i18n/ko.json` | 21600 | `2de7749c394238599128daaabd2368604439d00652603a8c1f883b993f3e5044` |
| `i18n/zh-CN.json` | 19921 | `bdf27a6bb64f542e6421659b486f2ac5a9de7f59e3a1e6377c0c02ed1b5906da` |

初次文字版 source SHA 為 `96b1e5fc9c31c9be0f87fefa214cedd54cab00233140d7d6a5498ae1725a3b48`。目前 visual 版僅改 visuals／reveals；本次逐 ID 比對確認 142 行的 text／say／pause／voice／順序保留，native speech hash 仍為 `80b70c13bcc03e34`，visual hash 為 `b9ae256bfd4c2369`。這不是重新合成或購買配音的證明。

八句待改稿提案的 `applied:false` 是原提案狀態；本覆核依 native merge 通知及上述實際 current bytes 核實套用，沒有修改提案或人工改寫雜湊。

## 內容與歷史界線

| 語系／ID | 目前文字 | 判定 |
| --- | --- | --- |
| en／`ag018` | Historical example: checked Sept 27, 2026, for a Sept 28 plan. | 保留歷史查詢日與隔日行程日，順序正確。 |
| ja／`ag018` | 過去の例です。2026年9月27日に、翌28日の計画を調べました。 | 保留過去示範、年份及兩個不同日期。 |
| ko／`ag018` | 과거 사례입니다. 2026년 9월 27일, 다음 날 28일 계획을 확인했습니다. | 保留歷史案例與「隔日」關係。44 codepoints 的 cue 可讀性待實際 timing。 |
| zh-CN／`ag018` | 这是历史示范：二〇二六年九月二十七日查询，规划九月二十八日。 | 保留完整歷史與查詢／規劃界線。 |
| en／`ag097` | The museum gives walking advice; we did not test it or check weather. | 館方建議與未實測／未查天氣分開，未杜撰分鐘數。 |
| ja／`ag097` | 館の徒歩案内はありますが、実測も天気の確認もしていません。 | 保留已有步行案內及兩項未做事項。 |
| ko／`ag097` | 박물관의 도보 안내는 있지만, 실측도 날씨 확인도 하지 않았습니다. | 保留館方建議與未驗證的範圍。 |
| zh-CN／`ag097` | 馆方有步行建议，但我们未实测，也没查天气。 | 不再把已有館方建議誤寫成完全無來源。 |

完整譯文保留平常週一休館與 2026-09-28 教師節特例，沒有推廣成每個週一開館；說明欄保留 2026-09-27 示範日期及出發前重查館方公告。台北車站附近 → 臺博館本館 → 二二八和平公園仍是草案，不聲稱已實地導航、實測步行、查天氣、預訂、付款或登入旅客帳號。`ag006`、`ag119`–`ag122` 的教學示意與實際編輯查詢邊界仍在，沒有把自行排版的表格稱為產品錄影或真實模型逐字對話。固定流程也能使用工具、依回饋調整的代理架構，以及人工授權點均保留。

## Metadata 與來源標籤

每語 title／description／tags／六章標題的九個 metadata hashes 全部 current；metadata 值與原快照相同。四語 title 均非空、未超過 100 字且無 `<`／`>`。目前來源與四份 native worksheet glossary 的四個標籤逐字一致：

| 來源標籤 | 來源 URL |
| --- | --- |
| Anthropic：Building effective agents | `https://www.anthropic.com/engineering/building-effective-agents` |
| 國立臺灣博物館：開放時間與票價 | `https://www.ntm.gov.tw/cp.aspx?Create=1&n=5444` |
| 國立臺灣博物館：2026 年節日開閉館公告 | `https://www.ntm.gov.tw/en/News_Content.aspx?n=5713&s=251424` |
| 國立臺灣博物館：本館交通資訊與地址 | `https://www.ntm.gov.tw/cp.aspx?n=5445` |

這裡核對來源命名、對應關係與譯文保留的限制，不代表本覆核者於當日重新開啟官方頁。既有 `verify-1.md` 的查核日為 2026-09-27；current source 的 `checked_on=2026-10-07` 與 fresh primary-source 查核應由其獨立收據驗證，不能由這份翻譯審稿代替。

## 實際五語字幕與切分

已讀 canonical 的實際五份 SRT。繁中／英文／簡中 426 cues 由 `preflight_consumer` 審讀，日文／韓文 293 cues 由 `inline_recovery_review` 審讀。每份 SRT 和 VTT 均與目前 source／translations／timeline 的純 native `buildCues` → serializer 重建結果逐 byte 相同；再解析實際 SRT 重驗其時間和數值限制，沒有只採 manifest 的空 problems 當作通過證據。

Timeline：30 fps、19,182 frames、639.4 秒、36 scenes／84 states；142 source IDs／scene／順序精確相符。`timeline.json` SHA `dd814aca675fe70a819917c1139dd8d80add41075cc99a2a81483f3b78f112f0`（48,788 B）；`captions/manifest.json` SHA `9af56e1900229039cdabc0f529a8221bfdf4086a1284b9b94ec6c41ec07caf0d`（540 B）。所有 cue 在其來源行窗口內，無時間倒置／重疊／缺行，最短 cue 仍大於 native 900 ms；日期、否定、條件、已做／未做及授權限制的句內順序保留。

| SRT | Cues | 最大 CPS／native 上限 | 最短 ms | 最大行寬／上限 | SHA-256 |
| --- | ---: | ---: | ---: | ---: | --- |
| `captions/zh-TW.srt` | 142 | 5.2945／9 | 2567 | 16／16 | `ca9c50884e56a9511b808d6382f1776c21885d3e2840cf85df44d101049386e4` |
| `captions/en.srt` | 142 | 18.7477／20 | 2567 | 42／42 | `78cd1d4d78963fd693ed69748f45f4192b0ea9b36cec7ce71f3b383cae839a38` |
| `captions/ja.srt` | 145 | 7.6923／8 | 1918 | 16／16 | `73850a8d6282e340c4024eeac51d1484216549f7dccb22fea15a20d1634015dc` |
| `captions/ko.srt` | 148 | 10.1286／12 | 1845 | 18／18 | `cc605e96a1257963815566d3c4743ec6dd34e51140ef300c831f7e79f46d4107` |
| `captions/zh-CN.srt` | 142 | 6.4480／9 | 2567 | 16／16 | `16e8d26e8aa8236dece5cfbd305da5eeb64aacf775533017ea4b616e7c73b079` |

全 719 cues 的逐 ID／scene／source／translation／實際時間／CPS 清單在 `actual-captions.cue-ledger.final.json`（307,928 B），SHA `fe7d3b409a7c5d1512809c6faf3017533dc2a416e0bdcbb225a5d3df4eae159a`。CJK 行寬與 CPS 使用 native 顯示寬度單位，英文／韓文使用 native codepoint 計數。

### 已修正的日文拆詞問題

初次實際 JA SRT SHA `93404ba0b1113338aa3edf9be9ce1f59e5468f0543958f30a469de3d7783e754` 的 `ag080` 在 cue 14／15 將「プログラム」切成「プログラ｜ム」；雖然 native 數值檢查為零，人工審讀仍列為必要修正。原 SRT、初次收據、候選和獨立覆核均保留。

唯一改動：`決まった条件で報告書を出すプログラムの方が安定するかもしれません。` → `決まった条件で報告書を出すプログラムの方が、安定するかもしれません。`。只在長比較主語後插一個 `、`，原字及語序、來源條件與「可能」的不確定性完全保留。候選 SHA `d50925ec107041284d4a8c9754edb0e88fba08310f1081d7752b7e5a1b800b90`，獨立 reviewer 與候選作者不同。

正常 native worksheet／merge／captions 重產後，**實際** cue 14 為 64.033–69.549 秒，完整含「プログラムの方が」；cue 15 為 69.549–72.500 秒「安定するかもしれません」，CPS 分別 3.8071／3.7275。實際結果與獨立覆核的 native 候選完全相同；僅這兩個 cue 改變，其餘 717 個 cue records 相同。將逗號反轉並按 native JSON 編碼後，整份 JA SHA 精確回到 `9407daff215d92c96b388bce5b34a27125c4a81998eef06c66db0cc2475ba9ef`，證明其他 141 個 entries 和 metadata 未被改寫。不是手改 SRT 或沿用原切分時間。

## 實際 metadata draft

已完整讀取 `review/metadata-draft/metadata-draft.json`，SHA `0fc96d1dc3bcd9e0a3b0f6d48098509c13222ddaf7230eeba7db021d2cc07463`（9,022 B），purpose 明列 `UNAPPROVED_METADATA_DRAFT`；這是草稿而非正式 native upload package。其七個 source bindings（source、lexicon、文章及四份 i18n）和 timeline SHA 均重新讀檔精確核驗；純 native `composeMetadata` 重建整個 metadata 物件深度相同，五語 title／description／tags 預算無問題。六個 chapter clocks 為 `00:00`、`00:15`、`02:17`、`03:29`、`07:08`、`09:11`，對應目前 timeline 與各語章節名稱。

每語描述保留四個上述來源標籤及其 exact URL 各一次，歷史示範日期、出發前重查及草案界線保留。metadata description 第一行含文章 CTA；繁中實際首行為：

`🔗 完整文章：https://mokaair.com/zh-TW/life/ai-agents-explained?utm_source=youtube&utm_medium=video&utm_campaign=ai-agent-vs-chatbot`

五語 CTA 目前均使用該繁中文章 URL，不宣稱文章已具備四語翻譯。`description.<locale>.txt` 是展示稿，首行是 title，第三行才是上述 CTA；已逐檔確認它等於 `title + 空行 + metadata.description + 換行`，沒有把展示 TXT 首行誤當 API description 首行。

| 展示稿 | Bytes | SHA-256 |
| --- | ---: | --- |
| `description.zh-TW.txt` | 1123 | `e4d7a27e47b8c66c99070f8c9a5f257829d6c9b5b028d0e4856a16f634f48e8e` |
| `description.en.txt` | 1124 | `35a80f469b740eba4f251e9b7113cd0ffef078db5ae9bb66916a187f0fc3020c` |
| `description.ja.txt` | 1230 | `723234097f7153bf5a8f804fe353d9be745ba85ed33deb30ed5e097646e6dd94` |
| `description.ko.txt` | 1133 | `0f1605f8b03c919a454dc2c6ccd048510872af01f5e71341476ca766d0723a4e` |
| `description.zh-CN.txt` | 1147 | `24b57647a25e3764cc6df52e7bc5b59832cab1be27347b46efc91642571ad84b` |

共用 lexicon SHA `862d277aaf4359e9e07b5f3281f59eabb240f5ea3227c174f692cf2d0237f675`；source article `apps/api/app/guides/content/ai-agents-explained.json` SHA `fbb59011402f61d75ec8d3ce221fda10751d15b0d79014208eba36e4f18aad14`。草稿欄位、來源清單和精確私有檔案 binding 全部收錄於 final JSON。

## 驗證界線

- 五份字幕 timing 均是繁中 narration 的行窗口，沒有 dub timing。translated splits 是 native 在同一來源行內按文字 spoken-weight 分時；timeline 沒有逐字 measured char timing。本覆核核對 source ID、窗口與語意順序，未進行逐詞音訊聽驗或聲稱精確跨語音訊對齊。
- 四語既有檔案沒有 localized thumbnail words；保留 native zh-TW fallback 行為，沒有不存在的語系縮圖文字或手機字卡 fit 驗收。
- 站主未核准成片語言、`locales={}` 是 parent 所回報的既有狀態；本覆核沒有呼叫 API 或新增選擇。五語免費草稿存在，不代表站主選了這些 delivery locales。沒有生成或審核 dubs，也沒有 dub fit verdict。
- 原文字收據的 timing pending 是當時階段；目前數值與切分結論僅適用上述實際 full SHA。後續 source／translation／timeline／branding 或 metadata 重產改變時須重新綁定，不涵蓋未來成片、字幕 overlay、整段播放器觀看、音訊驗收或 owner acceptance。

本 reviewer 只新增／更新本獨立審稿文件及 private receipts；日文候選由 root 的正常 native 流程套用。本 reviewer 沒有 source／translation／media／cache／journal／approval 修改，沒有 provider 或 production request，也沒有發布或 owner acceptance 宣稱。

## 最終音訊版本追加覆核（2026-10-07）

本追加段的 mechanical readback UTC `2026-10-07T13:22:31.244Z`，split／ag125 文字讀取收工 UTC `2026-10-07T13:29:24.353585+00:00`。前面的 14,301 B V1 收據完整保留，prefix SHA 仍為 `a3d3e6dac05a53593f9e2220218a8357487898e5082e4c2f70f5def1b5ee0a4e`；V1 的 639.4 秒、舊 cue 數、章節與檔案 SHA 是當時證據，不冒充本版。

**本版 source-bound 免費 caption 與未核准 metadata draft 範圍可用。** 新 timeline 是 18,895 frames／30 fps＝629.833333 秒，36 場景、84 states、142 個來源行；speech hash `ef2d1ce1ef5e5ea2`。ag125 同義改詞的獨立來源查核另在 `verify-3.md`。沒有由此判定重組裝後的 movie、actual overlay、全片播放器或 owner 聽音通過；沒有產出 dubs 或更改 `locales={}`。

新的 binding 為 `<home>/mokaair-work/ai-agent-continuation-20261007/caption-review/actual-captions.bindings.final-audio.json`，review ID `ai-agent-final-audio-caption-bindings-2026-10-07T132231235Z`，SHA `fe9144d9dd30167e6b1381aa456ac17415abe118ec7139607e2802322f98991f`（79,349 B）。全 718 cues 的 `actual-captions.cue-ledger.final-audio.json` SHA `8f24717235af18183c4e9bee284e1bca51b321ccb7bd4668dd2f5849b3e387a2`（307,618 B）；本次八組 split／16 cues 與五語 ag125 的讀取收據 `actual-captions.final-audio.read-review.json` SHA `8ea70515b1610a9da3bf8a2ad41f117f13f4500f1674a1f18e4d08306b8540df`（5,777 B）。全部是新檔，V1 closure／binding／cue ledger 未被覆寫。

### Current source、音訊與 i18n lineage

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `video.json` | 36757 | `6b9bb4db44c6199254c7c84e411e84618c4eeeed77e22469ed1fcb8f44c99235` |
| `timeline.json` | 48782 | `31b39a0b6968fe0a3b65cc621805b23c20a1e3ff370631cd263378c64c80e0fe` |
| `narration.wav` | 60464044 | `29582a770d65215d8b899b808ee34ae35c602be82989a94489edec7df9b202f5` |
| `captions/manifest.json` | 540 | `f5aa547deedb56255a67207a7641c8ae8b752b1d32b353c24228e1ae76ba26e0` |
| `local approvals.json` | 641 | `b41354f5a0280dc13ed9f56091373c383a22493e1c4195b3755c288ea5f428f6` |

本次重新讀取 142 個 raw WAV：完整 SHA 與 timeline 相符；實際 WAV 是 48kHz／mono／16-bit，逐檔 measured sample count 亦匹配 audio_samples。142 個 current QA records 的 clip16、scene、intended text 對上實際 raw SHA 與 current source。最新 native check row UTC `2026-10-07T13:08:38.219Z` 是 142 lines、114 exact、17 alike、11 judged（其中 10 second-opinion cleared）、0 flagged、unchecked 0、1 transcribed、0 new Jev calls。沒有把 matched exact／sound 的 noul:null 當成未匹配句的合格分數。

local audio approval 的 file 是 timeline.json，SHA 精確等於本版 `31b39a0b6968fe0a3b65cc621805b23c20a1e3ff370631cd263378c64c80e0fe`。本機紀錄 UTC `2026-10-07T13:12:48.280Z`，note 指向 admin UTC `2026-10-07T13:11:24.096518Z` 的設定式自動核准；不是 owner 完整聽音。root 回報遠端 audio review ID `832222e7-e54b-4bb2-96ee-dfa682331af1`；本 reviewer 沒有另呼叫 API 查詢或核准。

四語 568 個 source_hash 全部以 current zh-TW text 的 pure native textHash 逐項驗證。同一 ID／scene 順序完整覆蓋。將各語 ag125 整個 entry 反轉為保存的 merge 前 entry 後，整份 parsed translation 深度相同：其他 141 entries、metadata、陣列順序不變。EN／簡中只更新 ag125.source_hash、text 沿用；JA／KO 加上已独立審過的「只寫」。作者的實際 audit `listener-rewrite1/actual-i18n-audit.json` SHA `a4d3647c76e5c196b61c204781dd8aae6e787dc6521d06bc6c96050a3840e0ab` 另存；本輪自行重做 full-object inverse 與 source_hash 驗證，沒有只信作者宣告。

| Current i18n | Bytes | SHA-256 |
| --- | ---: | --- |
| `en.json` | 19784 | `80ab0f62a861538d06776fdf7301508f08280f816ea3110b3868c31a42b2545f` |
| `ja.json` | 22432 | `cd1cca8082fd883172fdc9c547051757ffb3ff09ffa948a2aafa1cb60c6696d1` |
| `ko.json` | 21597 | `6eb812ed9183e605f0c2a73b1602c946475e773774f6f352eeebd9b221c785fd` |
| `zh-CN.json` | 19921 | `9300210c9bbbb4e8cef3f6cb3ebd8463755b0b5bc112d48da4a020821733c61b` |

### 五份實際字幕與自然切分

五份 SRT 與五份 VTT 逐位元匹配 pure native buildCues／toSrt／toVtt；actual parse 與 built cues 相同。全 718 cues 的 CPS、line width、duration、overlap、來源行窗口問題為 0；每語 142 IDs 覆蓋完整，各行 joined 字母／數字序列保持 source／翻譯原順序。translated timing 仍在繁中旁白行窗口按 spoken-weight 分配，沒有逐詞外語實測或 dub fit 宣稱。

| SRT | Cues | 最大 CPS／上限 | 最大 width／上限 | 最短 ms | Bytes | SHA-256 |
| --- | ---: | --- | --- | ---: | ---: | --- |
| `zh-TW.srt` | 142 | 5.2945／9 | 16／16 | 2566 | 12458 | `6990e788ed9a8ddfabcdb6f89a561a330812b999abcaeb6e978a0aceec02fc7a` |
| `en.srt` | 142 | 18.7547／20 | 42／42 | 2566 | 12873 | `d870c1f2ccdf002019b38238521b7d8dbb6ae0cfaec170e2873a35caf3c23672` |
| `ja.srt` | 145 | 7.6923／8 | 16／16 | 1918 | 15240 | `3769b73d3df8d230bc9e4fe8f503fb61de497159d98be17c37d903ae57cbbc90` |
| `ko.srt` | 147 | 10.1325／12 | 18／18 | 1950 | 14854 | `3846248d95bedf2c6066b2fcc3192ed518e4cf7a578fecbcff715a1c3e398847` |
| `zh-CN.srt` | 142 | 6.4498／9 | 16／16 | 2566 | 12682 | `3f57a9295a327cfb5cd230555f053bc3baae8b57298c454206b9ad4801ab833f` |

本版 KO 為 147 cues，V1 為 148，總數由 719 改為 718。實際讀取八組 split（JA ag006／ag080／ag111；KO ag111／ag018／ag027／ag097／ag107）與五語 ag125，沒有必要文字／切分修正。JA ag080 cue 14 在 55.467–60.983 秒完整顯示「プログラムの方が」，cue 15 在 60.983–63.933 秒保留「安定するかもしれません」；原跨 cue 斷詞未復發。JA ag111 的「告／知」是同一 cue 內兩行 wrap，沒有跨 cue 延遲或刪字。

五語 ag125 均在 312.000–317.700 秒的同一來源行窗口。JA「とだけ書きません」、KO「만 쓰지 않습니다」、EN not just、簡中「不能只说」保留否定範圍，沒有變成所有週一可參觀。歷史 9/27 查詢／9/28 規劃、館方有建議但我們未實測／未查天氣、外部指令不擴權等原義保留。

### Current metadata draft 與六章節

Metadata draft SHA `68ba754e51e18f85320c1ecef4cacd579d28c7a6dd693e2ec98823faea0a7f71`（9,022 B）仍標 UNAPPROVED_METADATA_DRAFT。七個 source bindings 及 current timeline 全部重讀精確符合；pure composeMetadata 整個結果 deep-equal，五語 title／description／tags budgets 與 chapter 問題為 0。六個 clocks 是 `00:00`、`00:15`、`02:09`、`03:20`、`06:59`、`09:01`，對應實際 frames 0／472／3872／6014／12576／16248，未沿用 V1 clocks。

每語 description 保留四個 official label／exact URL 各一次，首行仍為本文 CTA；五語目前都使用 `https://mokaair.com/zh-TW/life/ai-agents-explained?utm_source=youtube&utm_medium=video&utm_campaign=ai-agent-vs-chatbot`，不宣稱四語文章已翻譯。description.<locale>.txt 的 title 首行／CTA 第三行格式也逐檔符合重建。

| Current display description | Bytes | SHA-256 |
| --- | ---: | --- |
| `description.zh-TW.txt` | 1123 | `e9428acf158bb4a46a7ae83373e302835792b4f5fe10ddbff52a71cff4de825e` |
| `description.en.txt` | 1124 | `91af0e2a1ffc3f83c1767e0d5b49fee5af1ad8ccaee96e97925f0f8a98838d40` |
| `description.ja.txt` | 1230 | `3a403486ad6d4f19538fae660d932cea2b7e69edf1fef4d01fd667133f28cd5d` |
| `description.ko.txt` | 1133 | `70f5dce9f32624cd5038850a9b2320342618a19328c07c226d48d184d8adb9a9` |
| `description.zh-CN.txt` | 1147 | `a3adae6a80b9d17ca1708f93e715b2e7a7cbd5411facbb36da652f9509941472` |

本追加只審 current 免費字幕與 unapproved metadata draft，沒有 final movie assembly／actual overlay／全片播放器或外語音訊聽驗結論。沒有 owner 語言選擇、dubs、final／upload approval 或 YouTube upload／publication；root 回報的 locales={} 沒有因免費五語草稿而改變。其他 citation ci037 未知 sent／STOP 及 Embedding hold 未被操作；source／media／cache／journal／approval 未由本 reviewer 修改。
