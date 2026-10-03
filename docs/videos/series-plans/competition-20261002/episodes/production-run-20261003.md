# E1／E2 製作紀錄：2026-10-03

本輪已完成文件／劇本正常核准、沈知棠前世褲裝 B 與顧承川 A 選圖、S01＋S03 累積 storyboard 核准，以及 E2 S34 視覺 metadata 修正。S01 R04 已做既有配音的五秒預覽，但正常 judge 為 6.72／failed，owner 尚未決定保留或重拍，pilot 未接受。S03 兩版動畫及 S04 兩版首格均因具體連貫／動作問題退回；本輪已停止新的付費操作，E1／E2 工作未完成，等待品質決定後接續，沒有兩集成片或整批放行。

## 本輪範圍與狀態

- 使用者指示「先做個兩集」，本輪僅 `wedding-reckoning-competition-e01`、`wedding-reckoning-competition-e02`，語言為 zh-TW，先單鏡 pilot 再逐段推進。
- 2026-10-03 02:32:15–16（Asia/Taipei；UTC 2026-10-02 18:32:15–16）經正常管理流程核准三份既有 v3 文件與兩份已送審劇本。作品由 `setting` 變為 `active`。
- chapter 1 核准按正常章節流程將第 1–10 集標為 `ready`，第 11–40 集仍為 `planned`。這個資料庫狀態不擴大本輪製作授權；本輪 runner manifest 仍固定 E1／E2。
- 核准及歷次 runner 收據均記錄 `global_drama_enabled=false`。每次 runner 僅提交一筆或查詢一筆，未啟動全域 worker；各次執行前後設定雜湊均相同。
- 沿用取回的既有錄音與快取；本輪這些動作沒有新增 TTS，也未授予聽校、最終影片、外語或發布驗收。

固定 source object SHA-256 為 `37328fa1c643e0edfcd1d138a158410653b36d6e02739ce7a9c555b26bc5bb9c`；source.mjs bytes SHA-256 為 `ef8b5993221a3c065850eb326e7259ea7688457267188b31c2a725aedd2d29f3`。獨立審閱實際讀取 setting、40 集 outline 與 chapter 1 全文；三份 `body_md` 與固定來源重建逐字相同，`body_json` 遞迴差異為 0，未發現阻擋 E1／E2 的敘事問題。該審閱收據本身不授予核准。

## 正常核准的文件與劇本

以下五筆在 `approval-receipt.json` 均為 `approved` 且有 `decided_at`。

| 項目 | 正常審核 ID | 核准內容 SHA-256 |
| --- | --- | --- |
| setting v3 | `9d133427-503f-45d9-8326-5249ee76ce20` | `07559d4f445a465ea357ae095e6f41f794c9f3e0fb1138104708d599017c7488` |
| outline v3 | `455497ab-6fac-4a3f-ae21-c970be3d1565` | `cb7c379f2dd202ee729c7f0874678eb959f0431ca28515618b8157f546c39ed3` |
| chapter 1 v3 | `249e2729-03e7-4633-b2b0-651cf8e22c0d` | `a85f93948078e336c8785423bcef5f59dfe61778d45645ef4c885cd8b54930c5` |
| E1 script | `b909e8f3-0cfd-4488-b323-1d81dbaa0dce` | `82352b248e66810bd217092b6284ea13c0ec688dbb410e6f791107e13781c429` |
| E2 script | `e0c54172-1349-40fa-b29f-0da3422e84cb` | `3e1d8461cd7013ea646dd517e1f7bc35b960e191f9ac005df039c112e1468bdd` |

## 角色圖與 selected look

沈知棠兩張候選圖均由 `gemini-3-pro-image` 產生，job 收據為 `ready`、`attempts=1`、`error_code=null`。A 的手錶呈圓／橢圓形，不符來源的小型銀色矩形錶；第二筆使用明確 `retake_of` 與原因，要求三視圖保持矩形錶、左耳露出與原有角色設計。

| 候選 | Job ID | 圖片 SHA-256 | 視覺與選圖結果 |
| --- | --- | --- | --- |
| A | `ab6389c1-e19f-4804-8187-f33bab3d9caf` | `b4c710868d44b0039ff3351425a5c280833151535b1b30a50d925c05471364bb` | 因手錶形狀不符退回；保留成功生成紀錄與成本預留 |
| B／R02 | `87ad66e6-de69-4e56-bc0a-c30117e163ab` | `300d23b6db5ede7f921a07c00f071de6a7b408e91b841032cc2c0ca15fe5b25c` | 獨立查看實際圖像通過；矩形銀錶、左耳露出、成人臉部／褲裝／手部一致，後經正常流程選定 |

Look review：`67d3d104-95da-4363-9f38-1bf7e99e24d1`，gate `look`、subject `zhitang`、status `approved`、choice `B`；`decided_at=2026-10-02T18:43:30.031558+00:00`。核准的角色 manifest 內容 SHA-256 是 `d8da6622583dbd25c4e45c4cc0a663acfb36450927791d0599b0a357c2ab6988`。B 對應 option index 2、file role `candidate_b`，附件雜湊與本機圖片實際 bytes 相符。

送審時 `judge.overall=null`、`suggested=null`，沒有捏造付費 judge 分數或自動推薦。`submitted-review-readback.json` 保留較早的 `pending` 快照，後續 `look-approval-receipt.json` 才記錄明確核准與 B 選擇。這個 look 僅是沈知棠前世褲裝。

顧承川另生成單一候選 A，job `558bfb56-1b2f-4bd4-b4b1-51b305435581`、圖片 SHA-256 `3d9436102a09582e5271b71f403ee5e509b593e1a80269f273880308461df6a4`，實際 JPEG、448,228 bytes。root 與獨立圖像 QC 通過；正常 judge 為 `overall=7`、`passed=true`，保留正面與側面暖色輪廓光稍不一致的問題及完整 notes，沒有隱藏差異。

正常 look review `da447d14-1310-4ca2-81dd-8a8eabde6b28` 的內容 SHA-256 為 `67cb6317f3df600a3e8c7fd99a165a577f1556d53dbd813105e3c31cf4d0890f`。送審包只有真實 A 圖，附原 judge 證據，控制自動核准的 `judge.overall` 與 `suggested` 仍為 `null`。早期 `submitted-review-readback.json` 保留 `pending`；後取回的 `chengchuan-look-approval.json` 明確記錄 `approved`、choice `A`、`decided_at=2026-10-02T19:25:21.368378+00:00`，兩份收據依時間並存。

## wr-e01-s01 首格與單鏡 storyboard

兩張首格均由 `gemini-3-pro-image` 回傳 `ready`，但生成完成與視覺驗收分開判斷。

| 首格 | Job ID | 圖片 SHA-256 | 實際視覺覆核 |
| --- | --- | --- | --- |
| R01 | `934b13de-8205-445a-9b7a-fbc2df2d2757` | `272b78da401e79270aa96a6bf73ad7d13f30e5d2ce5e78eb078d8c35faeca98f` | `failed`：人物後方看似開啟的倉庫門與通道，不符既定已關門狀態；保留原圖，不送為通過分鏡 |
| R02 | `7b14ffea-1908-4b34-9075-69cfb4faadb8` | `24d92892ee48b22a90a1450ed0e66f01354f0fb1d19200f2fc8c17af77d9d149` | `passed`：連續不透光鋼門與封閉中縫清楚，完整成人臉部、褲裝、持筆手及反射火光符合單鏡需求 |

R02 的實際圖像覆核於 `2026-10-02T18:50:13.9488779Z` 完成；鏡幅稍寬至腰部，且錶腕方向與角色圖 B 不同，已在 QC 明列為這次孤立 pilot 可接受差異。動作過程不得換持筆手或錶腕；S02 手部銜接與整集連貫仍須另驗，不能把首格通過擴大成全片驗收。

正常 storyboard review：`4c831ccd-cfe8-457e-a210-896391c588fd`，subject `null`、status `approved`，`decided_at=2026-10-03T02:52:39.827966+08:00`。核准內容 SHA-256：`3a69b4802ffdc4101bbbd04efbb7b0d0cc407774e2073e02672fbf939d4ebec6`，只包含 `wr-e01-s01` 的 R02 首格，`needs_review=false`、`incomplete=false`；該核准不是整集分鏡、動畫或嘴型驗收。

## S03 重拍與累積分鏡 checkpoint

S03 的 R01（圖 SHA-256 `0f692107c296f442d149a3b793b1f7f6de34819ef761403425af3662846d988a`）把火焰與餘燼帶入現世婚禮，筆色也錯，已退回。R02（`fd985be5bd710ec639ee62e420ab32367f945762d8205aa3fb999c86284ba881`）清掉火場，但原件上出現簽名筆畫、筆尖與紙面間隙不明且有生成英文標籤，獨立 QC 退回。

R03 job `c53d2181-83e7-4890-b43b-79ca7632ff9e`、圖 SHA-256 `533ac41699d5d66c09571b5756b0fc69b8ce167a14f5fea680d09b16725bf188` 通過首格圖像 QC：完整未簽原件與附近薄展示紙分開，銀筆明確懸空，單一矩形錶、婚紗頭紗，沒有火場或可讀生成字。實際為長蕾絲袖，後續現世鏡頭須保持此造型；僅接受這張首格，未接受動畫、聲音或整集。

保留已核准 S01 R02，加入 S03 R03 的正常累積 storyboard review 為 `4ab00bce-395d-4ba9-94d3-89339e1fa3d4`，內容 SHA-256 `2ccc8aef0b0d8ab60a7a08e9edd77b97e66fd483853709723b8e824704abe0a0`。初次 readback 是 `pending`；`storyboard-s01-s03-approval.json` 後續記錄 `approved`、`decided_at=2026-10-02T19:27:10.006733+00:00`。舊 S01 核准保留，此次只核准這兩張首格，不等於 S03 clip 或 pilot 已驗收。

S04 R01 job `38ae5d88-cb55-45fe-b062-35e06c09f6cc` 已 `ready`，圖片 SHA-256 `77b55bdc66f3409f2855e8eb7af7f5de3bd32f4a25aaa50589c2851db15698dc`；root 實看後退回：上半身廣鏡不符手與原件 insert，婚紗盤髮也偏離已接受的及肩髮身份。

S04 R02 後來確實 execute 並回傳 `ready`，不能繼續把早期 preview 當最後狀態。Job `11ecc10d-958d-410a-bab7-2c19ecdf612e`、圖 SHA-256 `1e829a0fc8ebad001b2b9c733eb1d7558ac70397ca8100db88b45fdfbb763fb2`；鏡幅已修為手與文件，但手錶轉到指頁手，與已接受 S03 首格的持筆手戴錶不連貫，root QC 退回。這是實際圖片之間的連貫問題；原文只指定矩形銀錶，沒有指定左右腕。兩張都未送為通過分鏡，S04 沒有 clip；受控同鏡參考圖修正方案仍屬設計，未修改共享 provider 或繞過 runner。

## 動畫請求、確定原因與相容 payload

`pilot-e01-s01-clip` 使用 `veo-3.1-lite-generate-preview`、1080p／8 秒、16:9、`personGeneration=allow_adult` 及上述核准首格。Job `061183d5-a672-4ae0-ae41-09df30a31752` 終態為 `failed`，`attempts=1`、無 vendor operation、無 output file，app error code 為 `video_media_rejected`、detail 為 `Gemini refused the request`。共同 provider helper 的 HTTP 400 分支會映射成這個泛化訊息；此訊息本身不能判斷是參數、內容安全或其他拒絕原因。

`veo-readonly-diagnostic.json` 記錄單純 GET 模型 metadata 回傳 HTTP 200、支援 `predictLongRunning`，並核對送出 body 的 image/jpeg、`prompt`／`image` instance 與參數摘要。該 GET 沒有提交付費生成，也不證明生成參數相容或影片能成功。失敗 job 的本機 `usd_estimate` 已是 `0.0000`，但不等於供應商實際帳單已證明為零，保守 reservation 仍保留。

`pilot-e01-s01-clip-diagnostic-r02` 先 preview，後來另行 execute；不能再把早期 preview 當作其最後狀態。Job `fc63bb73-174e-49ee-96c1-23a1289541fa` 終態同為 `failed`、`attempts=1`、無 operation／file。`diagnostic-r02/transport.jsonl` 在 `2026-10-02T19:00:57.717918+00:00` 保留已遮罩的原始回應：HTTP 400、`INVALID_ARGUMENT`，明確指出 `negativePrompt` 不受該模型支援。這次診斷確認的是參數相容問題，沒有證據支持把它歸為內容安全拒絕。

R03 新 manifest 移除不支援的 `negative_prompt` 欄位，把原本全部 avoidance 指令附入主要 prompt；保留同一核准首格、Lite 模型、1080p／8 秒、adult 限制與 seed，並以 R02 job 作 `retake_of`。沒有改共享 provider code、全域設定、審核與重試保護。`diagnostic-r03/transport.jsonl` 回報 HTTP 200；execute 先記錄 `submitted` 與 vendor operation，`s01-clip-compatible-r03-poll01.json` 再記錄 `ready`，poll 沒有重新提交或新增 reservation。

R03 job：`340951d1-4f13-43fb-91fe-c6f42c40f032`，`attempts=1`；manifest SHA-256：`2a0e713ef4b95726f108b84f6454c02aa92ae21f0fc3ff9b9c1ad86e121486f4`。本機 `wr-e01-s01-clip-r03.mp4` 共 6,233,051 bytes，SHA-256 `e3a5ca3bee3a324fcc24b549b9cba376b8914386d420b7987e18081e2721bb0d`，與 job output 相同。收到檔案並不等於手部動作、錶腕／門的連貫、五秒剪用窗或完整影音驗收已通過；原生音軌也不是最後配音。

R03 後續經 root 與獨立 QA 均退回：0.5 秒起多出第二只圓錶，左臂抬起加入持筆動作，違反原本僅持筆手收緊一次的要求。原檔與兩份拒絕收據均保留。

R04 job `d1214a5f-859b-4df3-8012-6ffc6c71ed04` 已 `ready`、`attempts=1`；manifest SHA-256 `83b71367aa3a017e591dcdc35345cf9deabbf5f089308cfaa1b8c18d5e9ef93d`，影片 SHA-256 `57f40d5094bbd1f980a9177286e0f22cb9f5e81154e1978fa211f45a069932b0`，6,918,973 bytes、1920×1080、24 fps、8 秒。獨立 QA 全部解碼 192 幀，實際視覺檢查 48 個不重複取樣幀，認為前 0–5 秒可供既定鏡窗剪輯；這不是全速播放、聲音或 owner 驗收。原生音軌不沿用，預覽使用既有旁白 0.2–4.61 秒；`s01-with-existing-voice-preview.mp4` SHA-256 為 `65128501affa7a25c9b8accb73d6a6dbf8f9ea825074ee977451b70882c6dd96`。

正常 clip judge 的原始結果為 **6.72／failed**（門檻 7），指出片頭眼睛張開的額外動作。獨立逐幀檢查第 0–36 幀（0–1.5 秒）發現起始已睜眼，約 0.375–0.583 秒是一次自然眨眼；這是對具體問題的視覺解讀，不能證明其他低分會消失，也沒有改分、降門檻或把 failed 改成 passed。協調者已將真實五秒預覽交 owner 選擇保留試拍或重拍；截至本 checkpoint 尚未收到決定，**pilot 未接受**，不得據此宣告整批動畫通過。

S03 R01 job `dcaa8750-7e9a-4151-b1d5-6ce0efb48eef` 回傳 `ready`，影片 SHA-256 `72af39654833a7e96d64c251fe5312ed1999a2008d563b42d1e71b6f7316ee54`。root 檢查全段取樣聯絡表後退回：額外手部帶入第二支筆、第二只錶，原手／筆關係轉移且矩形錶變圓；紙面保持未簽也不能抵銷這些缺陷。

S03 R02 job `7d697602-0883-4b8a-9722-5bc2bd8c86d0` 回傳 `ready`，`wr-e01-s03-clip-r02.mp4` SHA-256 `1bf6147f03a1330edd75074dfd288cf7188cffbfc0a3653937240c0c04543c5e`，8,346,621 bytes、1920×1080、24 fps、8 秒。root 與獨立 QA 均退回：前約 0.75–1.75 秒持筆手將筆從斜直抬近水平再轉回，超出原定「微顫後穩住、不得碰紙」的動作。獨立 QA 全部解碼 192 幀、實看 45 個不重複取樣幀，沒有全速播放或聽音驗收；單手、單筆、矩形錶穩定且未碰紙／生成字，不能抵銷主要動作不符，完整 0–4.5 秒預定剪窗未通過。沒有為此再送第三次 judge，也沒有以縮短鏡窗、改稿或換配音把失敗改稱通過。

另存 `s03-motion-rejected-review-preview.mp4`（4.5 秒，SHA-256 `09450b91cc7a49142ae961e650ca684e9ac45f75df089fcacf276e61b93ebb86`）只供檢視被退回的動作：影片取 0–4.5 秒，沿用原 voice master 的 9–13.5 秒，丟棄 vendor 音軌，字幕是可切換 `mov_text`。收據明列 `quality_accepted=false`、`episode_complete=false`，不是通過樣片。

診斷與相容問題分為兩張未認領 P1 票：[保留安全遮罩後的拒絕細節](../../../../../tasks/open/2026-10-02-preserve-sanitized-video-provider-rejection-details.md)、[Veo Lite negativePrompt 相容](../../../../../tasks/open/2026-10-02-honor-veo-lite-negativeprompt-compatibility.md)。兩票只宣告 provider 與既有 test 路徑；本輪尚未修改共享 provider、guardrails 或重試流程。

## 保守預留與實際帳單

截至本輪收尾，共十張靜態圖（知棠 2、顧承川 1、S01 首格 2、S03 首格 3、S04 首格 2）每張預留 USD 0.134，共 USD 1.340；六筆 clip execute（S01 四筆、S03 兩筆）各 USD 0.64，共 USD 3.840；加原 manual reserve USD 10，pilot／batch exposure 為 **USD 15.180**。歷史 checkpoint 為首筆 clip 失敗後 USD 11.176、R02 失敗後 USD 11.816、R03 提交後 USD 12.456、R04 後 USD 13.096、S04 R01 後 USD 13.766、S04 R02 後 USD 13.900、S03 R01 後 USD 14.540；poll 不新增預留。

實際完成兩筆正常 judge（顧承川 look 與 S01 R04 clip），API 估計各 USD 0.01，合計 USD 0.02 已包含在 manual reserve USD 10 內，不能再與 USD 15.180 重複相加。更早 R04 judge attempt 在 Windows 唯讀 descriptor 的 fsync 階段失敗；保存的原程式、journal 與離線實驗明確證明尚未進入 POST transport。其後只有一次原請求不變的顯式 recovery POST；原失敗證據與新結果都保留，不能把預先寫入 journal 的 `post_count=1` 當成舊請求已送出，也不能推廣為不明付費請求的一般重試許可。

以上不是供應商實際扣款，`actual_billed_usd=null`，仍待帳單核對；被退回的成功圖片及兩筆失敗 clip reservation 均保留。第一筆失敗 job 的 `usd_estimate=0.0000` 不抵銷這份保守 exposure。

Pilot cap 為 USD 100，本輪 E1／E2 batch cap 為 USD 350。每個後續 execute 必須另據收據累加；只做 preview 的預估 exposure 不能當作已執行金額。

[成本明細](../cost-ledger.csv) 的新列逐筆保留十張圖、六筆 clip 與兩次實際 judge；generation 列的 timestamp 是本次收據盤點時間，並非供應商提交時間。影像的 `estimated_usd` 是保守 reservation，judge 的估計列明已包含於 manual reserve；所有 `actual_usd` 留空。manual reserve 不另冒充一筆支出列，不能把明細 estimate 小計當供應商帳單或直接再加 USD 10。

收尾唯讀稽核於 `2026-10-02T19:42:44.894824+00:00` 記錄 16 筆 job：14 `ready`、2 `failed`、0 nonterminal，全部只屬 E1 production slug；E2 目前只有已核准劇本與既有配音／metadata，沒有生成影像。全域仍 OFF，設定 SHA-256 `7fbbe241ff8ad931b6ab414e2ed0438ad5f052a5a450b9cbb7d36031b35acd71` 與預期完全相同；兩集劇本、兩個 look 與 storyboard 正常核准相符，沒有 final／publish review。`ready` 數量不代表 QC 接受數量。

## E2 S34 視覺 metadata 修正

原首格已把封存信封放進保管提袋，卻又要求執行入袋動作。現改為既有成年無聲見證人員的手，在鏡頭開始時把封存信封拿在開口提袋外，接續原有入袋動作。未新增人物、道具、台詞或敘事；S35 以後已在袋內的狀態保留。

僅改 dialogue 的 S34 `prompt`／`runtime_prompt`、measured edit 的相應 `data.prompt` 及來源／衍生檔案雜湊。`voice.video.json` 沒有無聲 S34 scene，故未改 voice runtime、原劇本、series source 或 `build-audio-preview.py`。E2 仍為 41 鏡、34 句、159.05 秒，S34 仍是 133.71–136.71 秒；所有動作、camera、來源 ID、配音位置與字幕保持原樣。

[視覺 metadata revision 收據](./episode-02-s34-visual-metadata-revision-20261003.json) SHA-256：`f01e7508be7052f80b5e33d3ebd80e8b39c8646bb35e4b654ebb822191f59d99`。目前 E2 measured edit SHA-256：`eca4d156b1879fb566e48131a24492efd13b59b4a7a3f3d7d4985dbe69b407a5`。新版 metadata 已另存，原取回素材與歷史收據保留；先前已提交的 manifests 仍保留原 bytes 供查詢／稽核，後續 manifests 要綁目前 E2 edit。

驗證通過：精確語義差異白名單、23 份來源／voice／劇本／歷史文件 bytes 不變、取回 `media/` 下全部 136 個檔案雜湊不變、E2 音訊／字幕 artifact hashes 相符；`git diff --check` 通過，既有音訊剪輯測試 `19 passed, 24 subtests passed`。原完整交接包的 147 檔核對仍保留在先前 transfer 收據，兩個數量的目錄範圍不同。

## 本機證據與接續位置

完整收據與素材保存在 repo 外的 `competition-20261002/production-20261003/`；本文不含私密主機資訊或憑證。角色圖片為 `zhitang-character-sheet.png`、`zhitang-character-sheet-r02.png`（原始檔 bytes 與 SHA 保留；正常審查附件的 MIME 為 `image/jpeg`），首格為 `wr-e01-s01-keyframe.jpg`、`wr-e01-s01-keyframe-r02.jpg`。角色 manifest 在 `bundle-v2/reviews/e01/looks/zhitang.json`，單鏡 storyboard 在 `bundle-v3/reviews/e01/storyboard-s01.json`；S34 新版 metadata 在 `s34-proposed-version/`，機械驗證在 `s34-applied-verification.json`。

| 本機相對收據路徑 | SHA-256 |
| --- | --- |
| `approval-receipt.json` | `8384d46ca314ee31fb7d55b3ad3cd89225b6cbc77b61e617b1568eef5740d1cc` |
| `independent-v3-e01-e02-review.json` | `a6765568a2b5e08c6674a794e5efbbb8cd66a4f410e2ec68cb7f647132c4fa4e` |
| `first-image-execute.json` | `ea5f9c3958aa2a197d73daea2530762dbaf15894b6716ce50b2333ee2aba60fd` |
| `look-r02-execute.json` | `feee896b40454e54071a04107654af17ab250ed84814d6eedbf44c7e969edf68` |
| `look-zhitang-r02-review/submitted-review-readback.json` | `d9abc972253d69e0f88da3c851dcfb5d78c23e52870b3e63e8f5cc798de3fd05` |
| `look-approval-receipt.json` | `b7e29faf5d52ad0488b51970b64b617d48145b32c7be5a2fab66872428f7e00e` |
| `s01-keyframe-execute.json` | `bc59a1d6367123d34462f4098e0ee0a38e98b477ef228914a0486ce2e3fd2964` |
| `s01-keyframe-r02-execute.json` | `448a4461e910619f70c1d863a04691d7a24ca3810e1e3beefc6bc9de5c671ca5` |
| `s01-keyframe-visual-qc.json` | `de1fe03baeb9011f514663324c58092871f1e2169e817098c2c8046765fc2889` |
| `s01-keyframe-r02-visual-qc.json` | `959f4ec3a04df2db58e82d4a8cf1e5a6054b71cab5623ef850bd38afba223793` |
| `storyboard-s01-approval.json` | `6c743743639a5dca376e6f8a799b9e45046385e1239dd06747f92fea0da8db19` |
| `s01-clip-execute.json` | `671090cc507ce0ca60bdc03ce2ec5688dcb61b1ac89b29c64f593c999b2b80b8` |
| `veo-readonly-diagnostic.json` | `f87c32ec0e5cda4adf428de44d77a0e750021082fdd3a994a14690631b3a59cb` |
| `s01-clip-diagnostic-r02-execute.json` | `5369244a679aad43871bf202aabac201b2ef1492a07b6e9ab201b235250db28f` |
| `diagnostic-r02/transport.jsonl` | `0111f51712753cb8ed6578b248b82317a3b2d0c2b85f571b04ab663b84f16f47` |
| `s01-clip-compatible-r03-execute.json` | `0c096f0beb93184fdd06ddde2cb96a6daf56edb9cbcd3ef1a1cffd2e74697c29` |
| `s01-clip-compatible-r03-poll01.json` | `3f40d2bf922bb9da4fa08209949e31ed3fb4a28efbc16129d43247381bd342d4` |
| `diagnostic-r03/transport.jsonl` | `3b24d7859fa89081a5a41b8a71406eeb458e146fbc8054bde19d24529e317d99` |

新增 checkpoint 收據如下；上表保留較早執行與核准的原始證據。

| 本機相對收據路徑 | SHA-256 |
| --- | --- |
| `s01-clip-r03-root-qc.json` | `5ca9e62737d363abecf88621837479646c791fa54db0eea041b441a8ef01001d` |
| `s01-clip-r03-independent-qa/independent-clip-qa.json` | `a32dc72ec019c8e5e8de79a24f2d37dceecc5a39c4eb12af0473f1a21d9e371e` |
| `s01-clip-motion-r04-poll02.json` | `82073ea3f9d6680e15975f4ddd7a8c992c465f5980c665e6a2d30bc6e65f3457` |
| `s01-clip-r04-independent-qa/independent-clip-qa.json` | `fcd79145522c9a6fc521c2db30fdc37db7692afef5ea029c9d6024a8c8afc6ab` |
| `judge-clip-s01-r04-recovery-01/result.json` | `24cdc514ec4f714f199026484bfa99421b7d167ac50a21ddb90d87d4273d427c` |
| `s01-r04-eye-opening-audit/eye-opening-audit.json` | `710f4e4c83eec24e5d9cab9a4b76f1977c58225aea64360b301baa9e24e31e30` |
| `judge-pretransport-recovery-20261003/proof.json` | `098885a02273e3605942e8c0f187d39efb7b2ee48e1816908a4ad144551b04e9` |
| `chengchuan-look-execute.json` | `7adde1fd81a80e4c89ad306451fba3304900f05c6738abe380238ebc55d01f1b` |
| `judge-look-chengchuan-preflight/result.json` | `ebe970d14fab00093c2d3ef3fa2da70d3dcf109a427bce11b77d55659fbd96f4` |
| `chengchuan-look-approval.json` | `c31390a3bf33c9cd69d039b846f8b68b03aa3407dd1b9ee943d50d01f5629476` |
| `s03-keyframe-r01-root-qc.json` | `1759776c6b38e793cf45db4ff2627a166da8dabd297124c8a972bbc33e966234` |
| `s03-keyframe-r02-independent-qc.json` | `a0e3bae7220770c4b49c38d1ae5904cd868948c6a2a33224ef53922281bbd997` |
| `s03-keyframe-r03-execute.json` | `188bb372b164192375cbab3009fe3348515601ae61282576d901381e75e73301` |
| `s03-keyframe-r03-independent-qc.json` | `96ec29a07d8aec804aa581c590337b1ef5efc46e27f2906f8fe30f2c994df632` |
| `storyboard-s01-s03-approval.json` | `1e4e11ad772dab7cae17a67013c805db33c83453bfd0f2cb5bd62bae29f38681` |
| `s04-keyframe-execute.json` | `4fd13c0ee692bb4b6f8594a10ea56917740e5e1c48ff5e35a84f9cb1f6ec78f0` |
| `s04-keyframe-root-qc.json` | `6422a3a7b1b900965d931c668a7bed3080a47eef749a1f23190071da40374432` |

收尾新增收據：

| 本機相對收據路徑 | SHA-256 |
| --- | --- |
| `s04-keyframe-r02-execute.json` | `c4becfc6c94fb7e6febaa5119afcc98f9970801155d51e6e907d1b381f980477` |
| `s04-keyframe-r02-root-qc.json` | `d93fc23abc760b6fce2f951847bbf93b278399a60657dadf56dfb4d5e5a63118` |
| `s03-clip-poll01.json` | `cb1c606e6e125ee3c1e6e4763c716b8481f2c28b74871f262a6a19e3c62551be` |
| `s03-clip-r01-root-qc.json` | `7917803df573708cee55b4dd32541ccaea544a76b8ddecfd12e69df90ffc9d8a` |
| `s03-clip-r02-poll01.json` | `067db48ec39120e01610c903b66a4b57e9e331e5a3c280064a36615e2678b2d2` |
| `s03-clip-r02-root-qc.json` | `0dd76a537770fcd57ce90bb08db44a877e8e0e76b624b5e442fc8a2eecd348c4` |
| `s03-clip-r02-independent-qa/independent-clip-qa.json` | `15a3d600233ebc20205016a4b55dd2d244e3311bfd4d12adcb2b16b3c132f894` |
| `s03-review-preview-receipt.json` | `4cba51299d12a6cfe884a886a0231d9580a9090a316975432f987eb5c71db8c7` |
| `final-live-audit.json` | `13f9d8ddda76028e4803b2caabe54107a3e703b4b40bb0944c26484abcee5da3` |

## 已驗證的 VPS 接續封存

於 `2026-10-02T19:48:41.344911+00:00` 確認 VPS 檔案 `/root/mokaair-work/competition-20261002/transfer/wedding-e01-e02-production-checkpoint-20261003.tar.gz` 已上傳並逐一核對所有 member hashes，權限 `0600`。共 188,576,365 bytes、415 個 payload files，加 `CHECKPOINT-INVENTORY` 共 416 members；archive SHA-256 為 `9ce2b61d6e45af86756ad80d89c3b9fd1db871750b6ea3baf14487cd0933f4e0`，inventory SHA-256 為 `e5faa31ec8099ef2ae61bb8e21eaf02e17938b458cc608c96123b8d483e33543`。

本輪 production 目錄 411 個檔案已全部封存；原先約 75 MB 的完整音檔交接包也保留於 archive 的 `original-audio-transfer/`。協調者於封存前完成 credential value／pattern 及內嵌 tar 掃描，沒有憑證。驗證收據在本機 `competition-20261002/transfer/production-checkpoint-vps-verification.json`，SHA-256 `fa9f3b11dade0c864d9b3492b3b54c815cb73dd19b6b8e3f786e941e302a936c`，明列 `episode_complete=false`、`pilot_accepted=false`。封存後 production 私有目錄維持凍結；此備份紀錄僅追加於 Git 文件，不回寫進已封存的 inventory 或驗證檔。

接續前先記錄 owner 對 S01 R04 的真實決定，釐清 S03 動作修正與 S04 參考圖連貫方案，再依新的真實關卡逐鏡推進；本輪不再追加付費請求或整批執行。兩集工作未完成，任務已釋出為 `open`，等待品質決定；四項聲音聽校旗標、E2 S06 嘴型同步與各鏡品質仍待各自驗收。原 [VPS 預檢](./vps-handoff-preflight-20261003.md)、聲音檢查及早期 pending 紀錄保留其歷史語義；`handoff.json.current_production_run` 指向本文 checkpoint，不改寫先前收據。
