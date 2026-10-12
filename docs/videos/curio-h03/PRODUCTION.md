# H03 製作紀錄

更新：2026-10-12（Asia/Taipei）。本集問題是「通古斯大爆炸：森林倒了，為什麼沒有隕石坑？」；製作路線為插圖投影片，沿用奇聞檔案局第 3 版畫風與 Sulafat 旁白。

## 最新進度：繁中上傳包已核准（2026-10-12）

站主已回覆「核准本版分鏡與成片」，範圍為 11 分 34.3 秒版本及五張保留圖。
正式站於 `2026-10-12T04:02:50.168388Z` 記錄分鏡核准，
於 `2026-10-12T04:03:20.672188Z` 記錄成片核准；兩筆 review ID 與內容 SHA 均沿用下列現版。
原本的「只出繁體中文」授權於 `2026-10-12T04:03:36.920100Z` 保存至正式站，
locales 為空物件，表示不加其他語言；沒有重問語言或重製媒體。

原生 `review-pull` 已記錄當前核准，exit 0；舊音訊 SHA 的歷史提示不影響最新音訊核准。
`package` exit 0，產出繁中上傳包，原生檢查 4／4 通過。
獨立檔案消費端核對通過：成片、縮圖、SRT 與原件 SHA 相同，只有 zh-TW；
139 cue、7 個實際章節、13 筆研究來源、2 張照片署名及 AI 旁白／畫面揭露完整。
說明欄 3,584 bytes，教育類別 `category_id=27`。

只在生成的上傳指引修正分類名稱與站主需確認的 Studio 欄位，並在 metadata 的
`disclosure_reason` 移除未使用配樂的泛用描述；`contains_synthetic_media=false` 保留為自動分類，
實際擬真重建的 Studio 揭露仍由站主於上傳時確認。來源、所有媒體及標題說明未變。
metadata SHA：`3a87c11795acfc0973521593b9930979173dc2a6bfd9d64731f4e81b6fcdc982`；
UPLOAD.md SHA：`46ba0dbe59002ecae3ed6a32be062d5e54bf2d28248cece06462b8e89f6a8a54`。
共享模板問題記入 [上傳指引任務](../../../tasks/open/2026-10-12-derive-video-upload-guide-category-and.md)。

原生上傳包審核已核准並回讀：publish `31f7d43a-0bd5-4c77-a9f4-e7f186feb9e4`（2026-10-12T04:31:11.914678Z）。
正式站 `ready_to_upload=true`，瀏覽器顯示「可以上架」。
正式主機使用 READ ONLY transaction 執行 `read_approved_package(..., verify_files=True)` 通過，
確認已核准成片、繁中 SRT、縮圖、metadata 與站主選擇一致。
只有繁中時，原生 `review-push --gate languages` 明確回報沒有額外語言批次可送（exit 3）；
原文上傳包直接供應繁中 metadata／字幕，consumer 的 `approval_pin.languages=null` 正常。
沒有強制建立空語言批次或冒稱語言 manifest 已核准。

本機交付：`C:/Users/x8120/mokaair-work/videos/curio-h03/upload/UPLOAD.md`。
完整證據在同目錄上一層的 `_audit/delivery-proof.json`、`upload-consumer-review.md/json`、
`backend-consumer-readback.json`；原始品管 10／11 與播放器 CC NOT_RUN 均保留。

站主核准不擴大為完整播放、聽音或播放器 CC 的已驗證聲明。
YouTube 上傳、公開發布、PR 合併及部署尚未執行。

第一次送上傳包於 04:18:41Z 因 API 無回應 exit 4。唯讀查得 27 個完整分段
（113,246,208 bytes），逐片 SHA 對回核准成片後只補剩餘 20 片；伺服器確認完整
檔案 SHA／大小，再由原生流程送審。未重新生成媒體。原生續傳改進另記
[分段續傳任務](../../../tasks/open/2026-10-12-resume-review-file-transfers-from-server.md)。
語言在 04:08:32Z 被同一登入身分改成英日韓全選，來源無法歸因至特定人或對話；
依本次明確繁中指示於 04:19:45Z 恢復空選擇並回讀。主工人未收編 H03，
查無新增語言製作持久紀錄；最後核准及 consumer 再次驗證只有繁中。

## 成片送審時的證據（2026-10-12，以下為核准前快照）

81 張最終插圖均有相同檔案 SHA 的實際觀看紀錄，沒有缺漏或過期紀錄。
五張經 native `--accept-best` 保留的圖片仍保有原始評分、takes 與評語；這不等於站主接受。
分鏡 review `da0651b4-5904-4232-81ec-d71928e3e551` 仍 pending：48 張 native 通過的普通鏡頭
仍帶細節評語，後端要求該欄為空。最低分 7.18 已達門檻 7，81 張 coverage 完整；
沒有竄改評語或分數以取得核准。待辦見
[判定契約任務](../../../tasks/open/2026-10-12-reconcile-passing-storyboard-verdicts-with-nonempty.md)。

新時間軸只因面積示意改為原生「8,000 km² ÷ 2,000 km² ≈ 4」字卡而更新。
139 段 WAV 與旁白總檔全部保持已審 SHA；音訊 review
`d91b4953-eb3f-4329-ae68-5f1dea60c8c0` 於 `2026-10-12T02:53:47.354894Z` 自動核准，
正式站 GET 與本機 approval 已回讀一致。最新 timeline SHA：
`d256ebfe5e46cafadf85fc48f136a6c8ef725aafa4a87a5973db39bd9eb6ec12`。

原生 render 已 exit 0：34 個非 shot 場景、56 個畫面狀態、376 秒完成，沒有版面錯誤。
本機文件／影片規格測試 199 項通過、0 失敗。
assemble 於 `2026-10-12T03:26:35.756Z` exit 0：115 景全部編碼，成片 20,829 幀／694.3 秒
（11 分 34.3 秒），響度 -14 LUFS、true peak -1 dBFS；checks.ok=true、problems=[]。
139 段繁中 CC 與本機 audio/final review 頁均已產生。最終成片 SHA-256：
`e786669f5a392fde7f281c617c28f885d25df8b13535b4a37f9e2ae6eaea304e`。
成片 review `385728b4-7bc8-4798-89fb-a5ea16102df8` 已送審並 GET 回讀 pending；
站主尚未核准 H03 的分鏡或成片，尚未產生可核准的上傳包。

QA 10／11：唯一未過為 JPL 來源對原生抓取回 HTTP 403；獨立 web 開啟已讀到官方文章內容，
原生失敗結果仍保留。Commons 照片來源 URL 內括號被檢查器截斷的假 404 已以百分比編碼修正，
完整網址原生 GET 200；共用 parser 問題另立任務
[`2026-10-12-preserve-balanced-parentheses-when-extracting-video`](../../../tasks/open/2026-10-12-preserve-balanced-parentheses-when-extracting-video.md)。
最後這項只改 `/assets/1/url`，新來源 SHA
`a7e17af3914bedfbf1327219ef646a59a1625a26ac537914e1ea6d2a509afed6`；四項媒體 hash 全不變。

獨立 CC/branding 核對 PASS：139 cue 文字、WAV hash、起訖與成片音軌吻合，
加 5 秒位移後每句最佳 lag 均為 0 ms、最低相關 0.999931；片頭／片尾實際畫素與指定素材相符。
SRT SHA：`4cf72b2f0d02fe8ff88ff777cc8777e2d2a3f4864ea742949a699fde6e521c59`。
只有 zh-TW；7 個實測章節、AI 旁白／圖片揭露及兩張照片的署名均完整。
720p 正式站播放器已確認播放至 67.22 秒後暫停，duration=694.3、readyState=4；
該播放器沒有 CC track，不能把這段播放紀錄當成字幕顯示或完整聽音驗收。
另備妥本機 `review/with-cc.html`，但 loopback 服務啟動遭執行政策拒絕（只回
`blocked by policy`，沒有更詳細理由），未改用其他啟動方法；播放器 CC 實看保持 NOT_RUN。
可交付的字幕檔為 `captions/zh-TW.srt` 與 `zh-TW.vtt`。
共用審片播放器缺少字幕軌的問題已記入
[`2026-10-12-load-subtitle-tracks-in-local-and`](../../../tasks/open/2026-10-12-load-subtitle-tracks-in-local-and.md)。

56 個原生字卡／照片狀態已逐張實看並綁定 PNG SHA，兩組各涵蓋 17 個場景。
第一組 26 狀態 PASS_WITH_MINOR：報紙來源字覆蓋少量原圖下緣，仍可辨識原件與來源；
第二組 30 狀態 PASS。面積約四倍、不同能量模型及切科湖爭議的文字均與旁白相符。
這項紀錄不等於全片播放、動態轉場或聽音驗收。

成片另抽 15 場的首／中／尾共 45 格，兩名代理已完成實看，沒有新增阻擋：
五張保留圖均使用正確的 selected SHA，主體沒有因合成新增裁斷，約四倍字卡、照片署名及正文均完整。
少量裝飾頂線被推到畫框上緣、片尾左留白縮窄，列為 minor。
51 筆原生字卡 PSNR、98 筆 motion 證據及獨立 ffprobe 已核對；成片抽取前後 SHA 不變。
這是畫格抽樣與媒體證據核對，仍不是完整動態觀看、站主聽音或播放器字幕驗收。
審片問題已送出，2026-10-12T03:48:18Z 回讀的分鏡及成片均 pending；只出繁中不需重問。

URL 修正前來源 SHA `c7be5e8032fbf0775976a642bc558f408e1453f0b6b36a688decbfe0e7b8790b`。
該次只補報紙來源作者及 AI 旁白揭露；speech `cba1834e2d1021c3`、visual `f81bccf24595cb3b`、
look `635987294f938929`、pictures `128a0fe78ded537f` 全部不變。
`checks.pictures_hash=5f52a91843b05416` 是實際選圖 SHA 序列的原生 `keyframesHash`，
和提示詞的 `picturesHash` 定義不同；已重算吻合，81 張檔案均未過期。
圖片與圖片 judge 帳本估值合計 US$2.6935，沒有待收的 provider request 或 reservation；
這不是完整供應商帳單，TTS 實付總價未取得，不將估價當實付。
以下為分階段的歷史紀錄；較早版本的「最新」只指該次記錄時點。

## 站主範圍

站主本次指示：「繼續製作奇聞檔案局下一支影片，一樣只出繁體中文。」

製作繁中旁白、標題說明及可開關 CC。這項指示不等於任何未完成媒體的審看紀錄；YouTube 上傳、公開發布、PR 合併與部署尚未執行。

## 目前證據

- 企劃：站主已選 A「跟庫利克找坑，從倒樹解開空爆，再查八千萬棵與切科湖」。Jev 原選 A（0.88），立場 0.90、示範 0.10、建議 0.01；示範分數未達 0.60，後由站主明確核准。
- 大綱 review：`8c9554c5-ceb3-48b7-ab66-fd713e681f45`，2026-10-11T23:08:38.855460Z 核准、選項 A，正式站已回讀 approved。`brief.md` SHA-256：`98e2a3a28c529714bef64d4c42bd76aca5e08ab1cb9318df5c897d7f8cb0bdfc`；送審後不再改企劃。
- 原始題庫已完成前期覆核，本次另查 2025 年八千萬棵估算評論、2023 年切科湖正反研究、2024 年可能碎片模型及 2026 年幾何模型。研究刷新不是完整稿核准。
- 正式站初查 `/api/video/reviews/curio-h03` 回 404，確認沒有既有 H03 製作供接續。
- 插圖路線啟用，有效模型為 MiniMax `image-01`，每支上限 US$80；Gemini Sulafat 已配置。這是前置狀態，實際付費前仍跑 native dry-run。
- 外部 `languages.json` 已設定沒有附加語言。聊天訊息沒有精確時間戳，因此未冒填成正式站的選擇時間；來源另存語言授權收據。
- 完整稿 115 景、82 張插圖、2 張原件照片、139 句。字卡對拍、氣動壓力條件、沉積定年與來源書目均已修正；第一輪完整事實查核及第二輪獨立覆核通過，沒有未解問題。聽眾審稿及說書表演指令通過；尚不是音訊或成片驗收。
- 來源補強後、時間修正前 `video.json` SHA-256：`08b8fc80c9b9720ee30cf1ccf73f8f0d540a03e8b3ec6ef77166dde43237dca2`。該次只在 sources 與 c21 追加 Icarus 2019 傷亡研究，去掉 sources 後的 JSON 與聽眾審過的版本完全相同；未更動旁白、表演或分鏡。原刊搜尋回傳內容已讀，直接 DOI／原刊 GET 403；不冒稱付費全文已讀。
- 原生 dry-run：Sulafat 可用；82 張 MiniMax image-01 插圖每張一次預估 US$1.11、每張三次上限估 US$3.32，低於有效 US$80 本集上限。這是估價，尚未支出。
- 139 句旁白已合成及檢查通過。初版正文 20,618 幀／687.2667 秒；片尾時間修正後只重錄 `bikj`、`ze2w` 兩句（40 計費字元），137 段原音的 SHA 保持相同。最新正文 20,589 幀／686.3 秒，speech hash `cba1834e2d1021c3`，timeline SHA `132a6d97d67b7f4cc5f354c5c4b9dd57a1fe56646464b9dd90eb23c74bf753e7`。
- 音訊檢查：109 句字面相符、16 句同音／語助詞差異、3 句 Jev 通過、11 句由不看原稿的 Whisper 第二次轉寫排除疑慮、0 句待處理。音訊 review `4d67cd87-0db6-49b4-ade2-60b1b2b12cc8` 於 `2026-10-12T00:35:23.833237Z` 自動核准，已 GET 回讀及 review-pull；這不是站主完整試聽紀錄。
- 開場三張插圖小樣經兩次提示詞修正後已實看，可用；自動通過但實際是帶葉活樹的版本沒有採用。其餘插圖製作中，尚未生成成片或執行最終媒體 QA。詳見 [視覺製作檢查](visual-review.md)。
- 2026-10-12T00:04Z 最終 TTS dry-run：139 句／139 次待合成、約 2,735 計費字元，Gemini Sulafat ready；當月餘額 9,313,446 字元。原生命令 exit 0，dry-run 沒有合成費用。
- 初次 TTS 在 `jbd7` 已收到音訊後，Windows 將 confirmed journal 暫存檔改名時出現 EPERM（exit 1）。保存的 confirmed 暫存紀錄、WAV 及當前請求 SHA 全部吻合；已備份原件，再原文恢復該紀錄。原生 journal 回放以會丟錯的 send stub 驗證 `reused: true`、0 新請求、0 新增計費，獨立代理唯讀覆核通過。該句 WAV SHA `38ce5a9648c9648615e8165a31db49e6588dfdc844b0227edd11c2ec94e542f3`，4.880 秒。沒有刪除不確定請求或重買該句；後續 TTS 從剩餘句子繼續。平台問題已在既有 [Windows speech journal rename task](../../../tasks/open/2026-10-09-windows-speech-journal-rename-failures.md) 追蹤，本集未修改共用程式。
- 實测片尾由 8.4 秒修為 7.9 秒：只縮 `wg93` 句後停頓至 100ms、`njit` 至 0ms，保留問句後 300ms 及片尾固定 1500ms。`tts --refresh-evidence` 0 新請求／0 計費／139 段沿用，另逐一核對 139 段 WAV SHA 相同；後續兩句重錄另記。最新 `video.json` SHA `ce7418c4415cf9c8ce8c1afe9b024e562b4bc600307022ce4483d7ad5d87b590`。最新時間軸 137 狀態、最長 7.9 秒、平均 5 秒、插圖 61.33%，cadenceProblems 為空；文字、聲線及圖片提示未變。

## 外部檔案

製作目錄：`C:/Users/x8120/mokaair-work/videos/curio-h03`；CLI 的 `--workdir` 使用上一層 `C:/Users/x8120/mokaair-work/videos`。

- `_audit/research-refresh-agent.md`：當日來源、事實界線與素材授權研究。
- `_audit/preflight-*.json`：正式站初始查詢與有效設定。
- `_audit/language-authorization.json`：站主繁中限定的原文與記錄時間。
- `_audit/run-stage.mjs`：本集原生命令執行器，留下 stdout、PID、結束碼及時間收據。
- `_audit/assets-receipt.json`：1908 年報紙剪報及 2024 年 Landsat 原圖的來源、授權、雜湊與逐張檢視紀錄。

視覺修正最新來源 SHA `39699a32346ad389a58bfbbe771a63dc2ec00e1985b5a9c62e85ee0dfc6c17f0`。背景回到站主選定第 3 版的柔和 cel 陰影，保留 2D、粗線及條件式大頭人物；全片插圖依新 look 重新綁定，不冒用舊圖核准。只變更畫風敘述及特定插圖提示，旁白、聲線、已測時間軸及 speech hash 均未變；音訊核准保持有效。原始圖片、評分與來源各自保存於 `_audit/pilot-v1`、`pilot-v2`、`summer-v1`、`cel-background-v1`、`cel-pilot-v2`，沒有把失敗評分改成通過。

本機文件／影片規格測試：199 項通過、0 失敗；記錄 `_audit/docs-video-tests.log`。此測試不取代圖片實查、成片 QA 或站主審片。

所有音訊、影像、成片和收據保留在 repo 外；既有 H02 成片及核准未修改。

2026-10-12T01:22Z 圖片提示更新：前二十景實看後，沿用十四景、修正六景，另簡化 59 個尚未生成的提示為正向有限物件列舉。最新來源 SHA `09a6de779cd2975d0a13ca1329328c46b889c431a54b7e77a4d9116d84a75e15`，look 保持 `635987294f938929`，pictures `8467939604a71642`，speech 保持 `cba1834e2d1021c3`。聲音、字幕文字、字卡、事實與時間未動。圖片仍在生產，詳見視覺檢查及外部 `_audit/positive-prompt-revision.json`；尚未完成成片。

獨立差異與保全稽核 `_audit/positive-prompt-audit.md/json` 通過：恰為 65 個 `data.prompt` 變動，所有非 prompt 欄位逐項相同；20 個場景原圖、63 筆快取與 124 筆帳目均保全，備份時沒有未結請求。另一名代理完成 `_audit/pre-render-text-review.md/json`：115 景、139 句、139 個預計繁中 CC 無缺句或重疊，最多兩行、每行 16 寬字、最高 5.22 字／秒；日期、數字、来源名稱與口播一致，139 段 WAV 均匹配時間軸。此預檢不冒稱已看最終播放器字幕。

2026-10-12T02:29Z：82 張均已生成並由三名代理分段實看與核對 SHA，十七個內容／素材問題集中窄修。最新來源 SHA `a32373b5b8f791bb053d04eed102d917b670037d4bab468aa5b8a410be8f38ac`，pictures `f7abfe2c72ada894`；只改十七個 prompt，look、speech、旁白、字卡、時間、claims 及 camera 不變。原生續跑沿用 65／82 圖；原批完整保存於 `_audit/material-fixes-v1`。少數純風格或小構圖偏差保留原判讀，將另列成片審看，未改 judge 或冒記通過。尚無合成成片。

2026-10-12T02:46Z：集中修後只剩碎片散布、日間火球、計數框三張窄修；面積圖改為既有 native `big` 算式字卡，避開不準確的生成比例。最新來源 SHA `27d8f51b6460578ae1ac0fe60653cd5a77a024910d2009b429dc667bb01e428e`，pictures `128a0fe78ded537f`，look／speech 不變。最終規格為 115 景、81 張插圖、2 張授權原件照片、139 句繁中旁白；插圖占比約 60.66%，節奏檢查無問題。`tts --refresh-evidence` 139 段沿用、0 請求／計費；尚需完成圖片及字卡渲染、分鏡與成片審核。
