---
id: 2026-10-15-curio-h10-research-outline
title: Prepare Curio H10 Franklin source refresh and outline choices
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-h10-production
claimed_at: 2026-10-16T01:56:12Z
created_at: 2026-10-15T16:33:45Z
completed_at:
branch: codex/curio-next-five-20261016
depends_on: []
scope:
  - docs/videos/curio-h10
---

# Prepare Curio H10 Franklin source refresh and outline choices

## Why

使用者要求接續製作五集奇聞檔案局。H10 富蘭克林遠征需要更新來源、兩個可選的完整大綱及主張邊界，交站主與獨立審核員一起檢視；本任務只處理 H10 前製。

## Definition of done

- [x] research.md 登錄 2026-10-16 實際打開的來源與限制。
- [x] claims.md 可將兩案重要敘述對回來源，修正 4 月 25 日所記「明日 26 日」南行計畫。
- [x] brief.md 提供 A／B、可朗讀 30–60 秒開場、六章、3–5 轉折、loops 與結尾新資訊。
- [x] 獨立審核員讀回修正版；大綱層級通過，非正式劇本十三題通過。
- [x] 完成獨立覆核與手動 outline 送審交接，後台讀回 pending。
- [x] 原版與補格式版均讀回站主選 A；本集 US$6／本批 US$30 估算停手上限已核准。
- [x] 延伸完成本機 A 案 video.json、script.md、逐句來源、loops 與作者檢查。
- [x] 正式劇本通過獨立史料與十三題覆核後，交站主核准。

## Steps

- [x] 閱讀現行 curio-episode／youtube-video／script-writing，參考 H01-v2 前 30 景與 H09 brief。
- [x] 唯讀參考 949bb91fc 題庫，重開 Parks Canada、加拿大歷史博物館、Waterloo 與原始研究來源。
- [x] 補入 2024 Fitzjames 身分研究與 2024–2025 官方成果背景。
- [x] 按獨立覆核意見，把開場物件清單改成可朗讀場景和三個未揭曉行動時刻。
- [x] 大綱階段送審後曾釋出票；當時尚無 video.json、未啟動付費工人。

## How to verify

`git diff --check`；`npm run check:tasks`；逐一讀 research.md、claims.md、brief.md 的交叉引用、六章時長和 loops；核對開場朗讀量為 30–60 秒。正式稿增加 `node tools/video/cli.mjs lint --slug curio-h10 --json`、逐句映射／來源 ID／SHA 檢查；音訊與獨立敘事 QA 尚未通過。

## Notes — 大綱前階段歷史（目前狀態見下方正式稿交接）

工作樹為 curio-next-five，base a77a9416d。此 task 的 UTC 產生日期為 10/15，文件查核日採 Asia/Taipei 10/16。H10 九個採用來源均取得正文或指定專節；主線不加入血腥遺骸、食人畫面或死因排行榜。共同預算為每集 US$6／五集 US$30 估算停手提案，尚未授權；本任務實際外部付費 US$0，未啟動付費工人、未推送。獨立覆核者 curio_h12_m09_planning 已確認主要史實並讀回開場修訂，無剩餘阻擋項。凍結 brief SHA-256：725991c44d9129668377c291efd0aa8edfc9306635abe551c6fc2616397e45ff。git diff --check 與 check:tasks 通過（1895 票；既有長期認領／scope 警告保留）。

2026-10-16 01:01（Asia/Taipei），主代理完成五集手動 outline 送審並讀回 pending；H10 review ID：`72a82580-0901-476f-b0b6-e7ddfa30e7c5`，對應上述最新 brief SHA。獨立覆核與送審交接完成，釋出認領但不標 done。下一位接手者須先讀回站主 A／B 選擇及本批 US$30 明確授權；目前兩者均未核准。送審卡未啟動付費製作。已送審 brief 維持原樣，由主代理統一 commit／PR。

## 2026-10-16 正式稿交接（目前狀態）

原版及補格式版 A 均已核准，收據見 `docs/videos/curio-next-five-20261016/decision-20261016.json`、`format-decision-20261016.json`。本集 US$6／五集 US$30 已授權，本作者尚未付費。原 research-outline 任務延伸正式稿，owner 保持 `codex-curio-h10-h11-scripts`，保留 claim 供盲評修稿，不另開重疊票。

video SHA-256 `e11a22a7a29086a06a8261943cd3e78bea6775223705cb3eab9b8dbdffa1a559`；brief `ab081206f4055046c18b7a89016f05c9f885aa6bdd37ea3c2e2c661f2d74aa0d`。82 句，文字時間軸估算 9.75 分鐘；純口播估算 502.56 秒。lint 0 errors／2 warnings，詳見 `script-validation.json`。完整正文、逐句來源、loops、估時與作者十三題自檢均在本集目錄。

兩個提示詞 warning 為 historical／modern 時代描述；已記錄場景實際變化，不以同義字消除警告。待獨立正式稿覆核及站主劇本核准；未送劇本後台、未配音、未產圖、未發布。

本輪 `git diff --check`、逐句／來源／SHA 一致性檢查通過；`npm run check:tasks` 通過，驗證 1895 票，保留其他任務既有長期認領／重疊警告。作者收據並不充當盲評。

## 2026-10-16 第一輪敘事退修

獨立盲評未過：chapters_link, payoffs, no_detour。已完成第 1 輪結構修訂，原答案保留在 `narrative-round1.json`，逐項回應在 `narrative-revision-1.md`。新版 video SHA `58e37c2eb2bc8190ba16aa4b9dc5050397819a12e263b29cf3a0641dba7c306b`；80 句，估算 9.60 分。lint 0 errors／2 warnings；未標 narrative pass。提交後釋出認領，供獨立事實覆核接手。無後台劇本送審、無付費呼叫。

第 1 輪修訂驗證：逐句文字及時間軸句序、主張／來源 ID、video／brief SHA 一致；`git diff --check` 與 `npm run check:tasks` 通過（1895 票，只有其他既有認領警告）。

## 2026-10-16 獨立正式劇本史料查核

查核員 `codex-gpt6-h10-h11-fact` 對版號 SHA-256 `58E37C2EB2BC8190BA16AA4B9DC5050397819A12E263B29CF3A0641DBA7C306B` 完成逐句、逐景資料與上架文字查核；[verify-1.md](../../docs/videos/curio-h10/verify-1.md) 記錄全部 80 句／78 景、來源、存取限制及聽眾檢查。沒有史實修改或未解主張，lint 0 errors／2 視覺提示詞 warnings。嚴格敘事盲評仍指出 `h3369d03` 的搜尋位置問句缺少具體回收，因此**正式劇本尚不得送審**。此收據只覆核當前 SHA；修文後要重新綁定新 SHA 並至少定向重查變動句。未送後台、未付費。

## 2026-10-16 第二輪敘事退修

第二輪嚴格盲評 11／12 項必答通過，唯一未過 `payoffs`：`h3369d03` 把因紐特口述直接問成下一次海底搜尋位置，`h725fbb3` 卻說 2014 年岸上零件使隊伍改位。原評審答案保存於 `narrative-round2.json`；作者只做最後一輪定向修訂，詳見 `narrative-revision-2.md`。新版 video SHA-256 `236e94b49168e52e57f6c063c9cd377fdf2086cc91fb0907932a3d13fc3389ac`。兩句旁白改為把口述界定範圍與岸上物件導致改位分開，loop 由 `h725fbb3` 回收；80 句、估時 9.615 分，lint 0 errors／原有視覺警告 2。`script.md`、逐句主張與估時已跟版；未將作者修文當成盲評通過，舊 `verify-1.md` 仍綁舊 SHA，須獨立重查變動句並重做嚴格盲評。尚未送後台劇本、未付款。

## 2026-10-16 獨立史料第 2 輪與新鮮度 HOLD

獨立新查核員 `codex-gpt6-h10-fact-round2` 對 SHA-256 `236E94B49168E52E57F6C063C9CD377FDF2086CC91FB0907932A3D13FC3389AC` 完成兩句改稿與舊版 78 個已確認主張中固定種子抽樣 26 句（含兩句改稿）的直接原始頁複查，26／26 可支持、事實修文 0。完整來源、HTTP 200 讀回、逐句表與聽眾檢查見 [verify-2.md](../../docs/videos/curio-h10/verify-2.md)。

另找到 [University of Waterloo 2026-05-06 發布](https://uwaterloo.ca/news/media/dna-matches-identify-four-more-sailors-franklin-expedition)：再辨認四名船員，累計六名。現有結尾仍以 2024 Fitzjames 作最後新資訊；台詞沒有直接錯誤，但對 2026-10-16 的資料查核標示而言有近況缺口。**正式劇本史料關卡 HOLD，不送站主劇本核准。**本查核員只建議於 Fitzjames 回收後加很短的 2026 身分研究後記並同步來源／說明；不自行改稿。後續改字應綁新 SHA 重查事實與敘事盲評，必要時重走 brief 核准。本輪未付費、未送後台。

## 2026-10-16 身分研究後記修稿

作者 `codex-gpt6-h10-freshness-coda` 依獨立查核的新鮮度 HOLD，直接閱讀 Waterloo 2026-05-06 公告，於 2024 Fitzjames 紙條簽名回收之後加兩句短後記：2026 年五月再辨認四名船員、累計六名。原 A 案 brief 完全未動；原劇本 80 句未改字；完整變更與邊界見 [freshness-coda.md](../../docs/videos/curio-h10/freshness-coda.md)。

本版 `video.json` SHA-256 `4EF199C9FC35E0761004A64EF32434EEA483DFAF5B25AC4DB28D0C154C024680`；`script.md` SHA-256 `A4A64B02732D97C9DDB216B2CD42F789D95A0B0ADEB8AB3CE22B3C9CA679E596`。82 句、文字估時 9.829 分；lint 0 errors、2 個既有畫面警告，沒有付費呼叫。**第 2 輪 verify-2 的 HOLD 尚未解除**：須請新的獨立史料查核員做第 3 輪，並由獨立敘事盲評者針對新版劇本重新評分；兩者都通過才由主代理送站主正式劇本核准。本作者不送後台、不開始製作。

## 2026-10-16 新版雙重覆核

製作協調者未撰寫 H10 後記，對 `4EF199C9…` 的兩句新增台詞、數字卡、說明欄與原始 Waterloo 2026 發布重新核對；[verify-3.md](../../docs/videos/curio-h10/verify-3.md) 判史實 PASS，解除前版新鮮度 HOLD。未讀前版盲評的獨立讀者只看目前 `script.md`，十三題全部答是，含必答 12／12；答案在 `<home>/mokaair-work/videos/curio-next-five-20261016/review/blind-curio-h10-strict-r4.json`，主代理以 `narrative --answers` 匯入並讀回 passed。原有兩個畫面 lint warnings 仍在，不影響送審。下一步：執行 `script` 與 `review-push --gate script`，由站主審閱新版劇本；核准讀回前不得開始 H10 付費配音或產圖。

已執行 `script --slug curio-h10`，正式 `script.md` SHA-256 仍為 `A4A64B02732D97C9DDB216B2CD42F789D95A0B0ADEB8AB3CE22B3C9CA679E596`；`review-push --gate script` 成功，隨後 `review-pull --gate script` 讀回 **waiting for the owner**。目前等待站主在 `/admin/videos` 核准這份劇本或提出改字；H10 尚未付費製作。

## 2026-10-16 H10 已核准劇本與旁白 QA

站主核准 script.md，協調者以 review-pull --gate script 現場讀回 approval recorded。Gemini Sulafat 80 個 TTS 請求產生 82 句時間軸 WAV，2,397 計費字元、實測 588 秒；帳本 h10-tts-20261016-01 保守估額 US$0.20。check-audio 82／82、Jev 1 次、15 個品質旗標；帳本 h10-audio-qa-20261016-01 保守估額 US$0.50，工具沒有美元結算單。h62e41a7 的「2026 年」經離線 Whisper small 再確認。其餘 7 句需站主優先試聽；詳見 audio-qa-1.md。後台旁白審核與插畫仍待後續關卡。

## 2026-10-16 H10 旁白送審

逐句試聽頁與音訊 QA 收據已產生，review-push --gate audio 成功，review-pull 現場讀回 waiting for the owner。已請站主試聽 7 個重點旗標，核准讀回前不啟動 H10 插畫。

## 2026-10-16 H10 旁白核准與插畫製作

站主回覆已試聽並在後台核准；協調者以 `review-pull --gate audio` 現場讀回 `audio: approval recorded`。`keyframes --dry-run` 為 73 鏡、MiniMax image-01 1K、最多三 take 約 US$2.96；共用估算帳本 `h10-keyframes-20261016-01` 先預留 US$2.96，連同已用估額 US$0.70 為 US$3.66，低於本集 US$6。已啟動逐圖生成與 Gemini 圖像評審；尚未完成插畫驗收，也未送分鏡後台。

## 2026-10-16 H10 分鏡定向複核與送審

首次全頁目視發現八鏡與旁白場景、地點、道具或無字要求相反，詳見 [keyframes-qa-1.md](../../docs/videos/curio-h10/keyframes-qa-1.md)。僅重畫這八鏡，保留其餘已通過圖片；第二份 [keyframes-qa-2.md](../../docs/videos/curio-h10/keyframes-qa-2.md) 綁定新版 `video.json` 與 manifest 雜湊，記錄 73／73 評審通過、0 `needs_review`，並逐頁複看四頁聯絡表。劇本與旁白未改。H10 累計工具估算 US$2.519／US$6。已 `review-push --gate storyboard`，隨後 `review-pull` 讀回 **waiting for the owner**；站主核准前不製作成片。

## 2026-10-16 H10 繁中成片已送最終審核

站主在 `/admin/videos` 核准新版 73 張分鏡，協調者以 `review-pull --gate storyboard` 讀回 approval recorded。`render`、`clips`、`assemble` 與 `captions` 已完成；成片 10:14.17，正文 9:48.17，102 段繁中 CC，成片 SHA-256 `912F39E5DF15E0FEC7AADE44FE6872B28E8C6E5E9EDA63F60EEECB7E4949017C`。最終 QA 10／11，唯一未過為片尾同一卡 17.4 秒超出 15 秒；已用 `--manual-review` 送後台，`review-pull --gate final` 讀回 **waiting for the owner**。詳見 [final-qa-1.md](../../docs/videos/curio-h10/final-qa-1.md)。本輪一次 Jev 最終 QA 估算 US$0.05，批次協調者已結算至共用帳本，H10 累計估算 US$2.569／US$6。站主核准成片前不做上傳包，語言尚未選定，未上傳 YouTube。

## 2026-10-16 成片核准與三語授權

站主已在後台核准 H10 繁中成片；`review-pull --gate final` 現場讀回 `final: approval recorded`。後台 `locales_decided_at` 為 `2026-10-16T06:05:13.839762Z`，英、日、韓均選標題說明、字幕、配音；本機已同步 `languages.json` 並產出各 82 句含 `max_chars` 的工作表。站主另核准 H10 多語 US$2.00，H10 停手上限改為 US$8.00；連同 H11 多語 US$2.00，五集合計停手上限 US$34.00。詳見 [multilingual-authorization-1.md](../../docs/videos/curio-h10/multilingual-authorization-1.md)。三語尚未翻譯／審稿／配音，未製成多語上傳包，未上傳 YouTube。

## 2026-10-16 H10 英語配音三句定向修文

H10 英語工作表已完成翻譯及前兩輪獨立審稿。首版英語配音的八個自動旗標裡，`h5cac1f4`、`h72b4789`、`hb624337` 的 `addition` 被 Gemini/Jev 與離線 Whisper 反覆轉成 `edition`；為避免把同張紙的補記聽成另一版本，只改這三句英語，`i18n/en.json` 的其餘 79 句與繁中核准劇本均未改。獨立審稿 [i18n-review-en-3.md](../../docs/videos/curio-h10/i18n-review-en-3.md) 對工作表 SHA-256 `12D3DBF03A11AD6DB89D616EDFA21FF44E2D98FA74F1D7172DE3C4B3983CD3A4` 判 PASS，三句各為 78／84、81／85、77／81 字；4 月 25 日只記錄翌日出發計畫，未宣稱實際成行。下一步僅重錄這三句、定向音訊 QA，並按本集多語新增 US$2.00 停手額度逐筆結算；原英語音訊旗標及尚未製成的多語上傳包仍待處理。

## 2026-10-16 H10 英語三句重錄後 QA

三句定向重錄及新版 `check-audio` 已完成，82 句中 68 exact、8 Jev 接受、6 旗標；`addition`／`edition` 的兩句已解除旗標，4 月 25 日那句僅因 `25th` 保留旗標。共用帳本將三句 TTS 與差異 QA 核銷為保守估額 US$0.04，供應商實際帳單尚不可見。獨立離線 Whisper 複核三句新音訊，並將六旗標逐一分流，詳見 [i18n-audio-qa-en-2.md](../../docs/videos/curio-h10/i18n-audio-qa-en-2.md)。目前沒有確定需再付費重錄的語意錯誤；站主需特別試聽 `h3a137ee` 人名及 `hcc5d7ed` 句首是否多出 `thought`，再對這版英語音軌作人工判定。完整 82 句本機試聽頁在 `<home>/mokaair-work/videos/curio-h10/review/dub-en.html`。尚未讀回站主核准，未送多語上傳包，未上傳 YouTube。

## 2026-10-16 H10 日語配音 QA 分流

日語配音 82 句與 `check-audio` 完成：44 exact、14 Jev 接受、24 旗標。獨立離線 Whisper small 已逐句重聽全部 24 句並與核准日文對照，收據見 [i18n-audio-qa-ja-1.md](../../docs/videos/curio-h10/i18n-audio-qa-ja-1.md)。`h93d6e3d` 的核准稿及 Parks Canada 來源為 9 月 18 日，Gemini 和離線 Whisper 均辨成 10 月 18 日，是核准日語音軌前必聽的高風險日期；`hc9c15f2` 兩套把「北極の岸」辨成「北極の環境」，`h3e67f13` 兩套把「冒頭の隊」辨成「ボートの隊」，也需優先試聽。專名及確認用語另列於收據。已製作本機 82 句 `review/dub-ja.html`，預設顯示 24 旗標；尚未得到站主聽後判定，未改稿或付費重錄。H10 多語餘額需保留韓語；確有錯音時，先讀共用帳本，再按句定向處理。

## 2026-10-16 H10 英語試聽回覆與韓語配音 QA 分流

英語六句旗標送站主試聽後，站主回覆「英語旁白可以」；已補記於 [i18n-audio-qa-en-2.md](../../docs/videos/curio-h10/i18n-audio-qa-en-2.md)。這是英語音軌的人工聽感結論，不等於多語上傳包或發布核准。

韓語 82 句的首輪 `check-audio` 為 61 exact、5 Jev 接受、16 旗標。兩組離線 Whisper small 已覆核 16／16 旗標，逐句證據見 [i18n-audio-qa-ko-1.md](../../docs/videos/curio-h10/i18n-audio-qa-ko-1.md)；本機 `review/dub-ko.html` 可逐句聽全部 82 句，預設顯示 16 旗標。`ha4fd3dc` 的「口述」被兩套辨為「珠子」，列最高優先試聽；`h323f98d` 的「補記」兩套辨識都不穩。船名、人名也列於收據。韓語 `h93d6e3d` 的 9 月 18 日被兩套正確辨出，沒有日語版的日期疑慮。尚無站主對韓語的聽後判定，未改韓文稿或重錄。H10 多語估算帳本已用 US$1.99／US$2.00，這次離線工作 US$0；若有實際錯音，先核對追加額度，不能直接付費重錄或 QA。多語上傳包尚未送審／上傳。
