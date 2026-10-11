# H02 旁白改寫與 pilot 提示詞差異覆核

日期：2026-10-12（Asia/Taipei）。覆核者：`h02_verify2`，未撰寫這五句候選改寫。

**PASS / SCRIPT DIFFERENCE REVIEW**：五句旁白維持原意、人名、數字與證據限制；兩個提示詞修正使示意畫面符合原稿，沒有新增史實主張。此 PASS 適用於下列來源版本的七處差異，旁白重錄、插圖生成與成片仍需另行驗證。

- 當前 `video.json` SHA-256：`aa6a6155da421683bdb9a2bf16532d1460e78d15a17cd5505d14748efa9c917e`
- `claims.md` SHA-256：`6db38c75194a57b3361ee9eaab058b46da1f76fa0bab47ac48ea70de187be3a3`
- 基準版本為 [verify-2.md](verify-2.md) 覆核的 `7b8d066cbb42ad7ee621171fcaedcda7c5eeafb9acf9bf8dc6c7d287b08c482d`；保留該報告的歷史來源綁定。

## 讀回證據

獨立讀取工作區 `_audit/rewrite-1-receipt.json`、`_audit/audio-before-rewrite-1/video-before.json`、當前完整 `video.json` 與 `claims.md`。備份與當前 JSON 的 SHA-256 分別符合收據的 before／after hash。遞迴比較解析後的完整 JSON，**恰有五個 line.text 與兩個 data.prompt 差異**；其餘欄位相同。claims 的完整 hash 維持原覆核版本。

以 bundled Node 24.19.0 執行官方 `loadProject`／`lintProject`：0 errors；3 項既有提示詞重複用字 warnings。未發送供應商請求、核准 gate、變更媒體或原稿；僅新增本報告。

## 五句旁白

| Scene／line ID | 套用後文字 | 差異判定 |
|---|---|---|
| hook-place-not-verdict／abb7999e | 讀到刻下的文字，就知道應該去哪裡找。 | 保留留言提供搜尋去處的意思；接句仍交代人的下落未知。沒有宣稱已找到殖民者或確認全員抵達。對應 c8／c15。 |
| farewell-uneasy-colonist／069ea2a2 | 克羅托安人曾遭英格蘭人誤襲，雙方也有過嫌隙。 | 改為被動語序；「克羅托安」「英格蘭」字形與事件方向相同。對應 c6。 |
| return-opened-chest／c11d2375 | 在舊壕溝的盡頭，有五只箱子，原本藏起來，又被挖開了。 | 保留「五」、發現位置與藏起後被挖開的順序；沒有新增箱子內容、持有人或破壞者認定。對應 c13。 |
| return-message-rule／369cdc7d | 搬走時，刻下地名；遇難時，加十字，這是約好的讀法。 | 加「時」與停頓拆開易誤聽連音；「十字」完整保留，仍是約定的記號讀法。對應 c8／c15。 |
| h02-history-rumour-distance／4f036f32 | 史崔奇的記載是轉述，沒有他親眼看到屠殺的紀錄。 | 「史崔奇」完整保留；仍限定為缺乏親見紀錄，沒有擴大成確定未曾目擊或屠殺已證實。對應 h02e2。 |

逐句符合 listener-rewrite 的原意／專名／數字保留規則；沒有新日期、數量、拉丁字、人名或事件。這五處為措辭修正，沒有五項新的事實修正。

## 兩個 pilot 提示詞

| Scene | 已讀回的修正 | 差異判定 |
|---|---|---|
| hook-white-happy | 明確指定 coastal timber palisade、plain pointed vertical wooden stakes；排除 stonework、battlements、castle。帽子在頭上，手位在畫面下方，以臉為主體。 | 修正生成圖錯畫石製堡壘的風險，符合已覆核的懷特返航木柵記述（c11）。1590、日出、懷特高興的表情與 c15 讀法相同；帽位、手位與背景構圖為復原示意編排，沒有新增傳記或建築史主張。 |
| farewell-deer-melon | 鹿 lowered neck、muzzle at leafy melon vine、visibly nibbling a leaf；瓜留在藤上；intact roof 保留。 | 讓原本的鹿吃瓜植物情節確實出現在示意畫面（c5）。完整屋頂原提示詞已存在；葉片與藤上果實是動作呈現，沒有把所吃部位新增為懷特明確辨認的史料細節。 |

旁白五句使 speech hash 與音訊下游重新綁定；兩個提示詞使 pictures hash 與相關圖片／分鏡下游重新綁定。後續應在當前來源版本完成重錄查核、圖片實看、重新渲染與成片 QA。本報告不提供旁白、圖片、成片或上傳核准。

## 第二輪 pilot 提示詞差異追加覆核

日期：2026-10-12（Asia/Taipei）。**PASS / PROMPT DIFFERENCE REVIEW**：`farewell-deer-melon` 的單一 `data.prompt` 修正只調整卡通配色、畫風與較近的動作構圖，沒有新增史實；旁白及 claims 未變更。前述七處差異覆核與 verify-2 的歷史綁定保留。

- 修正前完整 JSON／`_audit/pilot-v2/video-before.json` SHA-256：`aa6a6155da421683bdb9a2bf16532d1460e78d15a17cd5505d14748efa9c917e`
- 修正後完整 `video.json` SHA-256：`64c95e39f9021c4dbe2793b758df4ee5c72a4668b787a833de5d52346d032910`
- 未變更的 `claims.md` SHA-256：`6db38c75194a57b3361ee9eaab058b46da1f76fa0bab47ac48ea70de187be3a3`
- `_audit/pilot-prompt-2-receipt.json` SHA-256：`4d21d927c91026931caa43b74c0a7966fa50387bb567cea3c14cb5cb59942ec7`

獨立讀回收據、修正前備份、修正後完整 JSON 及 claims，遞迴比較恰有 `scenes.10.data.prompt` 一處差異；其 before／after 文字與收據相同，其他欄位完全一致。`cb08d4da` 仍為「舊屋已經長滿了瓜，懷特還看見鹿走進去吃。」，對應 c5。木屋、完整屋頂、鹿低頭吃瓜藤葉及藤上果實均保留。新提示詞指定 medium close、嘴部與葉片居中、扁平卡通、羊皮紙黃／深藍／灰綠配色；這些是示意畫面的呈現方式，沒有把葉片等編排提升為懷特明確辨認的史料細節。

官方函式讀回：speech hash 前後皆為 `20d0bfc523979b9f`，look hash 前後皆為 `e77cf823ca0ea548`；pictures hash 從 `a623337d7a540ad3` 變為 `7fbe6e9de60ddcb8`。此差異不使既有旁白文字及音訊綁定失效，相關圖片、分鏡與渲染下游須綁定新 pictures hash。此 PASS 僅覆核差異；新的圖片實看、judge、分鏡 gate、成片 QA、後台狀態及交付仍須各自驗證。

以 bundled Node 24.19.0 再跑官方 `lintProject`：0 errors、4 warnings；其中 3 項為原有提示詞重複用字，另 1 項為鹿提示詞重述 look 的 teal 配色。該提示已保留在讀回證據；本輪差異覆核不把 lint warning 視為圖片已通過。

## 歷史服裝、靜物與刻字卡片差異追加覆核

日期：2026-10-12（Asia/Taipei）。**PASS / VISUAL DIFFERENCE REVIEW**：本輪實際差異為 31 個 `data.prompt` 修正，加上 `return-tree-cro` 的 template／data 改為既有 quote 卡片。逐項比對原稿、claims 與原覆核結論，沒有新增史實主張或剩餘事實必修項。服裝、年齡一致性、道具與手部景別屬復原示意的編排，不宣稱史料記錄了每個人的具體衣著。

- 修正前完整 JSON／`_audit/visual-correction-1/video-before.json` SHA-256：`64c95e39f9021c4dbe2793b758df4ee5c72a4668b787a833de5d52346d032910`
- 修正後完整 `video.json` SHA-256：`c9269e0e278a150b3de585a5e57ebf66e69fcb72cf74165429623a7614b9a663`
- 未變更的 `claims.md` SHA-256：`6db38c75194a57b3361ee9eaab058b46da1f76fa0bab47ac48ea70de187be3a3`
- `_audit/visual-correction-1-receipt.json` SHA-256：`ef4385d10c41ff79a53be7279010e110a6c318a697f34143078c75b6f6de43ef`
- 獨立時碼證明 `_audit/visual-correction-1-timing-proof.json` SHA-256：`99d1e2c3eb65b34f0815ff53ec5435dfb47683bc0eb3ed34b1826ce11c413d64`

### 逐項差異範圍

完整 JSON 遞迴比較共有 38 個葉欄位差異：31 個 prompt 的替換；tree 場景的 1 個 template 替換、3 個原 shot data 欄位移除與 3 個 quote data 欄位新增。收據逐筆 before／after 重播後與完整當前 JSON 完全一致。所有 134 個 line 物件（包含 ID、文字、停頓及表演 cue）、各 scene claims、其他 data 欄位、metadata、look 與 assets 不變。

| 已檢查的 scene IDs | 判定 |
|---|---|
| farewell-northern-bay、farewell-repair-wall、farewell-uneasy-colonist、farewell-grandfather、farewell-reluctant-governor、farewell-mark-agreement、farewell-inland-plan | 1587 場景指定成年英格蘭人與十六世紀末衣著；航海分規及無標籤示意圖、木材修屋符合原情境。內陸圖另明示假設遷移，沒有把計畫寫成已確認旅程。 |
| hook-empty-track、farewell-three-years-question、return-white-inference、return-hope-has-limit、route-governor-ready、route-england-return、h02-close-white-did-not-meet、h02-close-grandfather-unfinished | 保持懷特為同一個復原示意人物、1590 年衣著及原道具；沒有把開門、期待或推測改成找到倖存者。布袋限制排除現代登山背包。 |
| return-trumpet-dark、return-creek-search、route-captain-decision、return-walk-ashore、farewell-england-wait、return-one-witness、farewell-distress-knife | 水手／船長／懷特及下肢／手部視角維持原文；限定十六世紀末衣著，排除現代海軍服裝。臨別刻字圖仍要求木材空白，十字與字母由卡片呈現。 |
| h02-history-lawson-book、h02-history-record-not-witness、h02-history-ancestor-memory | 十八世紀初旅行者及哈特拉斯人物衣著，沒有把 1709 年出版改成指定談話年。哈特拉斯人物不加平原族群戰冠。 |
| h02-history-killing-rumour、h02-history-rumour-distance | 十七世紀初記錄者衣著；旁白仍把史崔奇內容限定為轉述，沒有新增目擊或屠殺已證實的畫面。 |
| h02-find-trade-route、h02-find-origin-not-carrier | 保留十六世紀末假設交易與局部手部／器物示意，不新增持有人或實際交易事件認定。 |
| farewell-trade-hand | 改為乾魚、草蓆與沙地靜物，明示象徵交換道具而非目擊事件；移除手、人物及頭部，沒有新增交易細節。 |
| hook-island-home | 原稿已限定住屋、蘆葦、沙丘與海岸；再明確排除門口人物、動物或吉祥物，沒有新增島上人口或聚落命運主張。 |
| return-tree-cro | quote 卡片為 `kicker: 樹幹上的三字母`、`quote: CRO`、`source: 懷特1590年返航記述｜NPS 1590航程`。保留 c10、line `6abe644b` 與原文，沒有 translation／reveal；沒有把樹上三字母合併為入口木樁上的 CROATOAN，也沒有新增人物。 |

### 實際時碼與音訊讀回

本段依據獨立 timing proof，**沒有採用原 apply helper 對不存在的 start／end 欄位的比較**。讀取本輪備份的完整 measured timeline，以官方 `buildTimeline` 與每句實際 `audio_samples` 重建前後兩版。先驗證全部 line 的 `start_frame`／`end_frame`／`audio_samples`，以及所有 scene／state 的 `start_frame`／`end_frame`／`reveal` 都是存在的整數；再完整比對 134 行、109 景、128 個 states。

修正前重建結果與 measured timeline 的全部核心欄位完全一致；前後所有 line 時碼、scene 起訖與 states 完全相同，唯一 timeline 差異是 `scenes.31.template` 從 shot 改為 quote。`return-tree-cro` 仍為 frame 5655–5827、單一 reveal 0 state。總長維持 20175 frames／30 fps＝672.5 秒；全部 TTS request 物件及 keys 相同。

speech hash 維持 `20d0bfc523979b9f`；look hash 維持 `e77cf823ca0ea548`；pictures hash 變為 `d003bcdacd87fb7a`，shot 數從 91 變為 90。當時實際 `narration.wav` SHA-256 為 `d94e49a3f8bc79c2676c2a7082d865c0a8c7e9c1ae66e8d94c03fc96961c9b20`，官方 `audioEvidenceProblems` 無問題。

官方 `lintProject`：0 errors、5 warnings；包含原有配色／用字提示，以及 `farewell-trade-hand` 的 still-life close-up 未被景別字表識別的提示。此差異 PASS 不核准未生成或未實看的圖片。quote 的 template 會使 timeline 完整檔案 hash 改變，後續應用 `tts --refresh-evidence` 的零新合成路徑重建並刷新 audio review；圖片及分鏡須綁定新 pictures hash，render、成片 QA、後台與交付仍待另驗。既有收據與前述覆核版本全部保留。


## 本批畫面修正已套用，當時待獨立覆核

這是工具在套用後留下的歷史待審紀錄。來源由 `c9269e0e278a150b3de585a5e57ebf66e69fcb72cf74165429623a7614b9a663` 變為 `294227a3e6ee357312f0c9faa2b23f9cbc22e72bad7e2e1edb3fa8e188eb62c2`；claims 維持 `6db38c75194a57b3361ee9eaab058b46da1f76fa0bab47ac48ea70de187be3a3`。套用收據為 `_audit/post-batch-source-delta-2026-10-11T19-49-15-115Z/source-delta-receipt.json`，SHA-256 `9b25b28dc6f7a1aab5a45adc3a9116193e2249b76e5b4320ef7ffd4d205b74e8`。當時僅確認來源已寫入、旁白與時碼不變，沒有宣稱媒體、後台或獨立覆核通過。

## 本批46處畫面修正的實際差異覆核

PASS / POST-BATCH VISUAL DIFFERENCE REVIEW

覆核日期：2026-10-12（臺灣）；獨立讀回時間：2026-10-11T19:50:24.917Z。此次核對實際落地完整檔案、不可變收據及快照，不以候選預檢取代實際覆核。原候選 SHA-256 為 `9482a99f35f0a9b405a0f627daac2354d40d3fbbe6ad5567a3c8cef82e6d3294`；授權副本為 `1284b2ee74cb49482149b42f0c5c3ef116b01d41b8a796ccfa33988effb97d69`。副本只有授權狀態與其紀錄不同，46處內容相同。

完整來源鏈保留：`7b8d066cbb42ad7ee621171fcaedcda7c5eeafb9acf9bf8dc6c7d287b08c482d` → `aa6a6155da421683bdb9a2bf16532d1460e78d15a17cd5505d14748efa9c917e` → `64c95e39f9021c4dbe2793b758df4ee5c72a4668b787a833de5d52346d032910` → `c9269e0e278a150b3de585a5e57ebf66e69fcb72cf74165429623a7614b9a663` → `294227a3e6ee357312f0c9faa2b23f9cbc22e72bad7e2e1edb3fa8e188eb62c2`。claims 全程維持 `6db38c75194a57b3361ee9eaab058b46da1f76fa0bab47ac48ea70de187be3a3`。

46處均與完整備份逐項比對：四個 shot 改為已有史料支持的 quote 卡；其餘36個未選定純物件鏡頭只追加排除人物、臉部、吉祥物、擬人化及額外動物的限制，六個未選定手部鏡頭只追加排除臉部、全身與其他人物的限制。42處還原完全相同的附加句後，整景與備份相同；原 subject、camera、lighting、示意或假設限定均保留，沒有增加史實。

| Scene／line | 卡片內容與史料界線 | 保留的影格區間 |
| --- | --- | --- |
| farewell-northern-bay／7d3976ee | 北方預定目的地為乞沙比克灣，沿用c4及懷特1587／NPS 1587；名稱卡未新增精確地圖。 | 1125–1271 |
| farewell-armada／5a4ea7a7 | 1588年英格蘭防守背景與西班牙無敵艦隊，沿用c9。卡片明示事件名稱、非逐字引述；2026-10-12重新開啟NPS〈1590 Rescue Voyage〉支持。 | 4455–4614 |
| return-landing-date／53923c71 | 日期整理為1590年8月18日，沿用c2及懷特1590／NPS 1590；原中文年份旁白、chapter與缺省emotion皆保留。 | 5181–5342 |
| return-post-croatoan／8697084e | 柵欄入口木樁上的CROATOAN，沿用c10及懷特1590／NPS 1590；沒有把它與樹上的CRO合併。 | 5827–5970 |

獨立實際證明：`_audit/post-batch-source-delta-2026-10-11T19-49-15-115Z/independent-readback-proof.json`，SHA-256 `f9258494519dbb6b8c4dfdb3eef60a5a948e0c255392b723b3252aa03b8ab40e`。18項檢查全部通過，包含226個快照檔案逐檔SHA與bytes（合計138151252 bytes）、完整來源JSON重播，以及134句旁白物件、claim、TTS requests與cache keys不變。快照inventory SHA-256為 `71c35495c0553308c1953e254f0151577a06da0df7ac064cb1d48364a2c75431`；舊音訊、所有原圖／take、cache、ledger、jobs、review與owned STOP收據均保留。

時碼檢查直接使用快照中的measured timeline（SHA-256 `5ad5408f37ca1811492b00a2aa3b352a35dfe761cb762af27255a8b2cf4d9504`）及官方buildTimeline。全部134行的start_frame、end_frame、audio_samples與109景／128states的start_frame、end_frame、reveal均為存在的整數；前版重建等於快照全部核心欄位，前後完整句時碼、景起訖、states及chapters相同，只有表內四景template改變。沒有使用不存在的start／end欄位，也沒有採用舊helper的錯誤undefined比較。

speech hash `20d0bfc523979b9f`、look hash `e77cf823ca0ea548`及總長20175 frames／30 fps＝672.5秒不變；pictures hash實際為 `b8190ace38a5bd14`，本版shot總數為86。134個WAV與旁白主檔逐bytes雜湊保持；narration SHA-256為 `d94e49a3f8bc79c2676c2a7082d865c0a8c7e9c1ae66e8d94c03fc96961c9b20`。官方lint為0 errors、5 warnings。依現有MiniMax image-01的官方1500字元上限，以官方composeShotPrompt靜態檢查86鏡：沒有超限或裁字，最小餘裕451字元；這項檢查沒有provider或credentials操作。

此次PASS僅涵蓋實際來源差異、保存與時碼／音訊沿用條件。quote template使完整timeline內容改變；後續須零新TTS的refresh-evidence、audio review刷新、圖片及分鏡重新綁定，然後另驗render、成片、字幕、QA、後台與交付。未生成或未實看的媒體仍待驗，本次沒有付費、native stage、再次套用或修改canonical MEDIA／timeline。


## 最終十八張來源卡的實際套用差異覆核

PASS / FINAL NATIVE CARD DIFFERENCE REVIEW

覆核日期：2026-10-12（臺灣）；實際獨立讀回時間：`2026-10-11T20:50:18.434Z`。此次核對實際套用後的完整來源、授權候選、不可變快照及套用收據，未以候選預檢代替实际覆核。僅18景的 `template`／`data` 改為既有 quote 卡片；全部134個旁白物件、ID、文字、emotion、cue、claims、章節及其餘來源欄位原樣保留，沒有新增史實。

- 前版完整來源及快照 `docs/video.json` SHA-256：`294227a3e6ee357312f0c9faa2b23f9cbc22e72bad7e2e1edb3fa8e188eb62c2`
- 實際當前完整來源 SHA-256：`4dfe4d73dd458323949542ba5c22cd68a7838cbdc237b36543b07ea18620322e`
- 未變更的 claims SHA-256：`6db38c75194a57b3361ee9eaab058b46da1f76fa0bab47ac48ea70de187be3a3`
- 最終 frozen18 候選 SHA-256：`cea7541ad5909406ba9fb52b7bdefa4c72609cadc14c0dbb5fed18617689ca28`
- Root授權副本 SHA-256：`b1899bfce634c97f25601961d7ddce5fd996929cf86a1616fb8be7dc5dd53462`
- 不可變 snapshot-receipt SHA-256：`b2b961e9a3cb7395219ca21c0ac4c916925c12bf09e6875ee6507581dc9ed30f`
- 不可變 applied-receipt SHA-256：`27c81da47d907ef3c1f659a389745df1e78ad5ad7c7ae818dce6f3173b6c2069`
- 獨立實際讀回證明 SHA-256：`913ae5039b8b14167311a46537ec666e4d2dc8e787a8facad63a94f001a1d1ee`

以上收據與證明保存在外部 `_audit/final-native-card-delta-2026-10-11T20-46-08-231Z/`。舊版 `294227a3…` 及前四次差異來源鏈、歷史收據與 proof 全部保留，沒有把舊 proof 改綁新版 `4dfe4d73…`。

完整十八卡已由兩名獨立視覺覆核者逐讀 before／after／claims。Early frozen18 獨立差異證據 SHA-256：`457dd65e988270baaad7c87683bd6059bdc7b83507a85960a73d9fd74093360d`；Late 來源卡覆核收據 SHA-256：`c45b8fb758d48829311dea1d8a03df260bf1ed9f1aa25833277ec4a36fc164cc`。這些是語意與來源差異覆核，不能當成站主已播放成片或正式 QA 的核准。

| Scene／line | 卡片文字及史料層級標示 | 原樣保留的影格區間 |
| --- | --- | --- |
| return-creek-search／86b291b5 | 船艇與小炮；搜尋對象摘要｜懷特1590年返航記述 | 6749–6930 |
| return-hope-has-limit／e3138e28 | 有去處，未定下落；本集判讀｜懷特1590年返航記述 | 8562–8706 |
| route-croatoan-place／f842d461 | 克羅托安；名稱用法摘要｜NCpedia／NPS | 9007–9152 |
| route-broken-cable／ebd0c9ba | 斷纜、失錨；事件摘要｜懷特1590年返航記述 | 9927–10091 |
| route-captain-decision／7de7ba3d | 停泊與安全；本集判讀｜懷特1590年返航記述 | 10416–10565 |
| route-storm-sail／89cdc105 | 天氣阻住了去路；事件摘要｜懷特1590年返航記述／NPS | 11171–11331 |
| route-third-birthday／adeea438 | 維吉尼亞．戴爾的三歲生日；日期對照，未證實當時仍在世｜懷特記述 | 11480–11632 |
| h02-history-late-story／72d80a5e | 祖先故事；傳聞摘要｜勞森1709年出版著作 | 11779–11962 |
| h02-history-survival-pressure／dd29a13e | 可能增加生存壓力；推論摘要，未解人員去向｜1998年Virginia樹輪研究 | 13398–13616 |
| h02-find-brass-analysis／21a67841 | 銅與鋅：黃銅；材料分析摘要，未認出主人｜ECU／Smithsonian，2017 | 14890–15055 |
| h02-find-dating-first／14d603d3 | 年代跨至十八世紀初；附近器物脈絡，非戒指定年｜Smithsonian，2017 | 15429–15601 |
| h02-find-context-question／15e3784d | 器物年代／原本出土地層；本集判讀方法，非新發掘成果｜NPS／既有報導 | 15936–16108 |
| h02-find-trade-route／515ebefd | 可能透過交易進入村落；可能路徑摘要，非定居判定｜NPS／Smithsonian | 16279–16435 |
| h02-find-inference-step／a2a221f7 | 仍需獨立檢驗；本集判讀方法，非新結果｜FCF主張／NPS較早評估 | 17888–18042 |
| h02-close-link-life／6aaa024d | 器物 ↔ 可確認的生活現場；本集條件式判讀，非已找到原屋｜NPS較早評估 | 18358–18518 |
| h02-close-identified-house／c33bbeea | 器物才多了生活脈絡；本集條件式例子，非已出土房屋｜NPS較早評估 | 18518–18698 |
| h02-close-persons-unknown／f08503c5 | 仍無法認出每個人的結局；本集判讀｜NPS較早評估與既有器物個案 | 19417–19583 |
| h02-close-unclosed-file／bf77b9cc | 航程未完成，實際去向未確認；本集判讀｜懷特1590記述／NPS | 19758–19935 |

史料界線逐項保留：生日卡是日期對照，未證實戴爾返島時仍在世；1709是勞森著作出版年，不指定談話年；乾旱只表示區域資料的可能生存壓力，不能解答去向；黃銅材質不能指認主人；附近器物年代不是戒指本身定年；交易是可能路徑，不能藉此認定定居；出土位置、地層及房屋身分卡是本集判讀方法或條件式例子，不是新發掘結果。NPS較早評估不寫成對2026宣告的事後回應，也沒有宣稱全球不存在獨立檢驗。結尾保留線索可讀、航程未完成與實際去向未確認，沒有真的蓋章結案。

實際讀回共394項檢查全部通過：357個快照檔案的完整SHA／bytes合計170264017 bytes，inventory SHA-256為 `376c6c8b361552991d9b14ae2cfcb2b8da4459a98b5347d7550bf134389e2580`；完整來源重播只含確定的十八景。全部實際 `start_frame`／`end_frame`／`audio_samples`／`reveal` 均存在且為整數；官方 buildTimeline 重建的134行、109景、128個states與chapters保留，總長20175 frames／30 fps＝672.5秒。未使用不存在的 start／end 欄位或undefined比較。

官方完整TTS requests前後相同：120個request、134個line cache keys。134個WAV及narration均逐檔完整SHA讀回且與快照、cache、timeline相同；官方音訊格式／sample evidence無問題。speech hash仍為 `20d0bfc523979b9f`，look hash仍為 `e77cf823ca0ea548`，narration SHA-256仍為 `d94e49a3f8bc79c2676c2a7082d865c0a8c7e9c1ae66e8d94c03fc96961c9b20`。pictures hash從 `b8190ace38a5bd14` 改為 `fa7e4b12363d155e`；shot數86→68。插圖按實際影格為11064／20175＝54.8401%（368.8／672.5秒），符合至少50%的門檻；不是按鏡頭數估算。

原批86張選定圖片亦逐檔full SHA讀回，所有舊take、media/cache、jobs、ledger、audio、review與owned STOP保持。jobs嚴格物件格式及ledger entries陣列均成立；以官方totalsOf(entries)重算全部totals，與保存值相同，reserved及reservations均為0。此讀回不修改收據、STOP、媒體或付費階段。

本次PASS只涵蓋實際來源差異與保存／沿用條件。讀回當下完整timeline仍是前版template結構，尚須零新TTS的refresh-evidence與audio review刷新。新版pictures／storyboard綁定、保留圖片的站主final gate、render、字幕、成片QA、後台審核、上架包及站主播放仍需各自驗證。來源URL均保留；工具GET403與瀏覽器正文可讀的結果分開記錄，不刪除正確citation，也不因本次差異PASS更改既有QA verdict。
