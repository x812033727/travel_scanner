# 《喜宴未散，清算開始》開拍準備核對

更新日期：2026-10-02（Asia/Taipei）。**使用者最新指示是全部優化後，先做 E1／E2 繁中影片。** 40 集的最後優化指令已覆核；兩集完整台詞及繁中聲音預演已完成，E3–40 完整演出稿尚未寫完。動畫生成仍為 **0 秒**，未通過人工聽校、畫面或成片驗收。

最終交付仍為同一畫面主版、zh-TW／ja／ko／en 四種角色配音及各語可開關 CC。**先完成整部自然台灣口音繁中影片與 CC，交使用者本人確認後，才開始外語產線實作、台詞適配、試音、配音、混音與 CC。** 現有外語草稿僅留存，目前不平行執行、不花費；競賽主片公開前仍須四語全部驗收及掛載完成。

## 本輪實際產物與尚未驗收項目

| 項目 | E1 | E2 |
| --- | --- | --- |
| 繁中首輪台詞 | 33 句；前 11 句重用開場，後 22 句已新錄；另有 1 次同文補錄 | 34 句已新錄 |
| 聲音預演實測 | 約 2:25 | 約 2:39 |
| 畫面窗口 | 40；原 42 鏡中 S35→S34、S39→S38 合鏡，來源 ID 仍保留 | 41 |
| 無台詞動作窗口 | 10 個 | 7 個 |
| 繁中 CC | 已按實際聲音落點產出 SRT／VTT | 已按實際聲音落點產出 SRT／VTT |
| 尚待驗收 | 2 項辨字待查、人工聽校、畫面、混音及最終 CC | 2 項辨字待查、人工聽校、畫面、混音及最終 CC |

兩集合計約 **5:04**，精確秒數與採用版本以 [E1／E2 覆核](episodes/review.md)及各集 `timing-report.json` 為準。這些預演只有人聲及無聲動作窗口，**不是動畫，也不是 animatic**；音效、環境聲及配樂尚未製作。逐句 WAV 未裁字或拉伸，角色 stems、master 及字幕落點已做檔案／sample 層核對；這不等於台灣口音、情緒、呼吸、閱讀感受或畫面已通過人耳／人眼驗收。

E1「姐。」做過一次同文同聲補錄，ASR 仍有「這／借」差異，已停止反覆重試；另一項「棠棠／唐唐、妳／你」為待查同音差異，未因 ASR 再重錄。E2 剩餘「附件／復健、啊／他」差異也待實際聽校，不能以 ASR 一票認定發音錯誤。詳情與原始收據留在 [episodes/review.md](episodes/review.md)。

完整原始鏡頭為 42＋41＝83；實測後 E1 兩組合鏡成立，目前 81 個畫面窗口，原鏡頭與台詞映射均保留。無聲動作沒有塞入假旁白；`voice.video.json` 只供聲音執行，完整畫面依獨立 edit plan 與 `measured-edit.json` 執行。E1 前 51 秒沿用開場實測，後半接在 51 秒，不接舊規劃的 60 秒。

產物均在 repo 外，各集 `editorial-zh-TW/` 含 `master.wav`、stems、`zh-TW.srt`／`zh-TW.vtt`、`measured-edit.json`、`timing-report.json` 與 `original-shot-plan.json`：

- E1：`/workspace/mokaair-work/competition-20261002/media/wedding-reckoning-e01-voice-zh-tw/editorial-zh-TW/`
- E2：`/workspace/mokaair-work/competition-20261002/media/wedding-reckoning-e02-voice-zh-tw/editorial-zh-TW/`

原 [pilot 聲音收據](pilot/review.md)、[51 秒剪輯](pilot/measured-edit.json)及[測時](pilot/timing-report.json)保留為歷史，已納入 E1，不能用來表示本輪只有 11 句完成。

## 已有什麼、還缺什麼

| 部分 | 實際已有 | 開拍／交付缺口與證據 |
| --- | --- | --- |
| 原作與攝製資料 | 40 集來源、逐集攝製設計、命名造型、道具交接、音效方向；本輪 40 集最後優化指令與 E1／E2 完整文字已覆核 | E3–40 仍需寫完整演出稿與可執行分鏡。[profile](../production-20261001/profile.json) 的 `design-and-tooling-not-render-accepted`／`selected-not-auditioned` 是歷史狀態；文字覆核不能改寫成全角色聲音或全片驗收。 |
| 後台資料與核准 | 兩集完整劇本已送後台待審，共 83 個原始 scene、67 句真台詞，無聲 scene 保留 `lines: []` | **待審不是批准**，真實文件／劇本核准仍待完成。此次沒有修改 Series 或全域設定。[E1 後台](https://mokaair.com/zh-TW/admin/videos?video=wedding-reckoning-competition-e01)／[E2 後台](https://mokaair.com/zh-TW/admin/videos?video=wedding-reckoning-competition-e02)。 |
| 本作兩集受控執行器 | 已新增範圍限定的執行路徑，42 項離線測試通過，可按本作、集數與實測分鏡設計生成守門 | **尚未部署，執行 host 尚未配置，真實文件 reviews pending。** 離線測試不代表線上模型／支出守門或畫面已驗證。全域 `drama_enabled` 維持 OFF，只准本作 E1／E2，不啟用其他作品。 |
| Veo 3.1 Lite | API catalog/provider 與片段工具已有 `veo-3.1-lite-generate-preview`、1080p、8 秒與首尾幀路徑；不送 `referenceImages` | 動畫 0 秒；尚缺實際 keyframe、單鏡動作、身份、服裝與區域可用性樣片。核對 [`gemini_video.py`](../../../../apps/api/app/video_media/providers/gemini_video.py)、[`clips.mjs`](../../../../tools/video/media/clips.mjs)。Lite 原生音訊必開，成片另混角色人聲。 |
| 中文角色配音 | 兩集 67 個不重複台詞已錄；既有角色 voice／speaker／emotion 沿用，前 11 句重用快取 | 仍有辨字待查項目，人工聽校未完成。核對 [`requests.mjs`](../../../../tools/video/tts/requests.mjs)、[`voice-audit.mjs`](../../../../tools/video/production/voice-audit.mjs)。合成成功不等於聲線與表演已採用。 |
| 繁中 CC | 本輪 task-local 組裝器已依 WAV sample 落點產出兩集 SRT／VTT，保留 speaker 與原文 | 仍需聽校起尾音、閱讀速度及隨畫面確認；可開關，不燒錄。完整混音與成片尚不存在，不能宣稱影音同步驗收。 |
| ja／ko／en 角色配音與 CC | 只保留既有外語草稿；一般教學影片 dub 有部分可重用能力 | **漫劇產線未完成，依使用者指示延至完整繁中影片本人確認後才動工。** [`dubs/cli.mjs`](../../../../tools/video/dubs/cli.mjs) 拒絕 `isDrama(doc)`；後台 [`admin_service.py`](../../../../apps/api/app/video_reviews/admin_service.py) 回 `video_locales_dub_not_for_drama`。只刪阻擋不等於完成整合。 |
| 120 分鐘合集 | `compile` 可接已核准集數、對齊音訊、合併每集皆具備的各語 CC | [`compile/cli.mjs`](../../../../tools/video/compile/cli.mjs) 尚無完整三條外語角色音軌合集交付流程。各軌須共享同一剪輯、片頭片尾與總長；接縫及字幕偏移待驗。 |
| YouTube 發布 | 已有 metadata／CC 包裝及上傳相關工具 | 尚未操作上架，也未確認目標頻道多語音訊能力。站主上架前須驗播放器音軌切換、預設語言及 CC；本機有字幕不等於播放器已具四語。 |

《喜宴》沒有製作設計中已標記的未成年入鏡路徑障礙。其餘 Codex 五部中，《朕不是你們的替死鬼》也沒有；另外三部各有未成年角色或孩子入鏡，現有 Lite 首格 I2V 路徑未驗證。這是選片時的製作可行性差異，不代表成人樣片已通過。

## 執行與成本的真實邊界

聲音 CLI 使用 repo 外各集 runtime 目錄的 `video.json`、`brief.md`、`series.json`，以 `--file` 執行；這些是有聲 scene 文件，不能直接冒充包含無聲動作的整集動畫。完整畫面執行須讀取實測剪輯、來源綁定、角色／造型及原鏡映射，再經本作範圍守門。後台完整劇本與供 TTS 的有聲 scene 文件用途不同，不能因通用聲音流程不接受空台詞就刪掉動作或捏造旁白。實際步驟見[本作兩集執行手冊](episodes/scoped-production-runbook.md)。

以下仍是離線準備工具，不會生成媒體，也不能代替真實文件核准或畫面驗收：

```bash
node tools/video/cli.mjs production-check --slug wedding-reckoning
node tools/video/cli.mjs production-build --slug wedding-reckoning --out /workspace/mokaair-work/competition-20261002/review
```

工具配對已完成，網路 CLI 在此環境使用 `node --use-env-proxy`。`tts --dry-run` 不合成，會以配對憑證唯讀查聲音／額度；真實 `tts` 才發出語音請求。`clips --dry-run` 不送生成，但有時間軸、關鍵影格與分鏡核准等前提，不能拿 40 集細綱直接報精確成本。`audition` **沒有 `--dry-run`**，執行即會請求語音；外語 `dub` 仍拒絕漫劇，亦不在本輪範圍。

成本分開記錄：

- 兩集首輪 **67 個不重複台詞、898 計費字元**。前 11 句／118 字元重用；本輪新錄 56 句／780 字元。另有 E1 一次同文補錄、2 字元，歷次累計 **68 次成功 TTS 請求、900 字元**；快取重用不重複計費。檢查另依實際請求更新 [cost-ledger.csv](cost-ledger.csv)。
- API 未回傳實際 USD，待帳單核對。語音／檢查預留 **US$10，包含早期 US$5**，不能登成已付金額。
- Veo 尚無請求／花費。依 2026-10-02 官方價格 Lite 1080p **US$0.08／生成秒**，目前 81 個窗口各取一份 8 秒素材，首輪 **81 × 8＝648 秒，估 US$51.84**。剪掉的秒數仍計費；不默認每鏡兩次。必要重拍、角色圖／關鍵影格、TTS、音效／音樂及 judge 另計。
- **US$3,000 目標＋US$1,000 預備金**是先前完整長片加四語的保守授權上限，不是本兩集報價或花費目標。沿用 pilot 累計 US$100、早期製作累計 US$350 與總額守門；最新執行範圍僅 E1／E2，不因舊規劃列過前三集而自動追加 E3。

## 完成前兩集的次序

1. **鎖定可審版本。** 保留原 source、攝製設計、角色／造型與兩集演出稿的來源 hash，核對本次優化列、實測分鏡及已送審的後台文件；完成真實文件／劇本核准，不沿用其他版本的通過紀錄。
2. **處理聲音待查項目。** E1／E2 已有全句首輪 WAV，查辨字差異並完成台灣口音、角色區別、情緒與可懂度的人工聽校。若確認需補錄，再僅替換有問題的句子、重排量秒與 CC；不把 ASR 同音異字全部當成發音錯誤，也不把自動通過當成人工聽校。
3. **部署並配置本作範圍路徑。** 42 項離線測試只是程式證據；尚需部署、設定執行 host、核對真實文件核准與支出守門。全域維持 OFF，以本作 E1／E2 的受控路徑鎖 Lite 模型、8 秒來源素材及預算，不能擴大到其他作品或全域 queue。
4. **先驗角色／關鍵影格、一鏡及開場，再批次完成兩集。** 依實測聲音執行，包含雙人對話、同臉換裝、撕展示副本與完整原件保留。每鏡一項清楚動作；E1 合鏡保留主鏡畫面動作及全部台詞／來源映射。可見嘴部另驗口型，不宣稱已有自動 lip-sync；不靠靜畫或 freeze 補時。
5. **完成兩集混音與繁中 CC。** 記錄採用臉、造型、聲線、圖／聲來源、拒用及重試原因；加入已驗收音效／配樂後，核對全部台詞、前 5／30 秒回報、道具因果、字幕與片尾銜接。保存實際採用率與每分鐘成本，作為後續全片製作依據。
6. **後續完整繁中影片由使用者確認後，才開外語。** E3–40 尚需完成演出稿、核准與製作。整部繁中影片與 CC 完成並由使用者本人確認後，才實作 locale×speaker casting、外語適配／配音、獨立混音與 CC；四語全數驗收及掛載後才交競賽主片公開包。

## 歷史收據、連線與保留缺口

初輪離線核對沒有付費生成，`production-check` 曾驗 10 部／400 集資料零錯誤，驗的是資料契約。首次未配對的 status 曾回 401／exit 3，現已被成功配對取代；`speech/status`、`media-status` 已成功，Gemini 語音也已完成兩集首輪合成。無須重新配對或要求使用者貼 API 金鑰，本包不保存 token／一次性代碼。

先前唯讀媒體設定為 `drama_enabled=false`、全域 clip `gemini-omni-1.1-flash`／1080p／8 秒、單片上限 US$200；這是讀取快照，不是本案授權額度。現有通用請求沒有單作品 Lite／budget 覆寫；**新受控執行器解決的是本作範圍路徑，尚未部署，不能宣稱線上能力已改變，也不要求先啟用或切換全域設定。** 配對 token 不授予管理設定變更或文件核准；先前《喜宴》六份文件待審、0 集 ready／started 亦不得冒充新版本核准。最新兩集劇本已送審，並未核准、生成影片或更動 Series／全域設定。

- [十部後台同步票](../../../../tasks/open/2026-10-02-ten-drama-backend-production-sync.md)與[同步收據](../production-20261002-sync/README.md)保留；它們記錄先前十部待審資料，不是本輪媒體。
- [造型舊票](../../../../tasks/open/2026-10-01-owner-settles-the-looks-the-ten.md)的早期「需第二角色 ID」不應當作現行限制；本片[攝製覆核](../binge-five-20260928/wedding-reckoning/production-review.md)已有命名造型與逐鏡資料，仍缺實際角色圖與切鏡驗收。
- [漫劇 policy 題組票](../../../../tasks/open/2026-09-28-video-drama-policy-questions.md)涉及自動 QA 仍套教學題的風險；放量前需處理或採既有人工成片審核，不能假設自動核准必成。
- [既有漫劇 pilot 票](../../../../tasks/open/2026-09-26-video-drama-pilot.md)、[series pilot 票](../../../../tasks/open/2026-09-26-video-series-pilot.md)是其他題材的未完成端到端驗證，不是《喜宴》已驗收證據。
- [語言上傳同步票](../../../../tasks/open/2026-09-30-youtube-approved-languages-sync.md)與配音交接 PR #1132 的合入／部署狀態須於相應階段核對；多角色外語／合集音軌仍需實作，不得只把 `planned-not-implemented-for-drama` 改成 ready。

參考：[兩集實際覆核](episodes/review.md)、[本作兩集執行手冊](episodes/scoped-production-runbook.md)、[動畫製作流程](../../../../.agents/skills/youtube-video/references/animation-production.md)、[Veo 官方文件](https://ai.google.dev/gemini-api/docs/veo)、[官方價格](https://ai.google.dev/gemini-api/docs/pricing)。
