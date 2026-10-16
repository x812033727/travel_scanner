---
id: 2026-10-15-curio-h11-research-outline
title: Prepare Curio H11 Voynich source refresh and outline choices
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-h11-audio-production
claimed_at: 2026-10-16T01:19:13Z
created_at: 2026-10-15T16:34:00Z
completed_at:
branch: codex/curio-next-five-20261016
depends_on: []
scope:
  - docs/videos/curio-h11
---

# Prepare Curio H11 Voynich source refresh and outline choices

## Why

使用者要求接續製作五集奇聞檔案局。H11 伏尼契手稿需要把新研究與仍未知的內容分清，產出可讓站主直接選 A／B 的大綱包；本任務只處理 H11 前製。

## Definition of done

- [x] research.md 列實際取得、僅摘要與無法開啟的來源。
- [x] claims.md 分清材料定年、文字統計、頁邊註記及全文解讀。
- [x] brief.md 提供 A／B、可朗讀 30–60 秒開場、六章、3–5 轉折、loops 與結尾新資訊。
- [x] 獨立審核員讀回修正版；大綱層級通過，非正式劇本十三題通過。
- [x] 完成獨立覆核與手動 outline 送審交接，後台讀回 pending。
- [x] 原版與補格式版均讀回站主選 A；本集 US$6／本批 US$30 估算停手上限已核准。
- [x] 延伸完成本機 A 案 video.json、script.md、逐句來源、loops 與作者檢查。
- [x] 正式劇本通過獨立史料與十三題覆核後，交站主核准。

## Steps

- [x] 閱讀現行系列規則及腳本故事、開場、結尾和十三題規則。
- [x] 唯讀參考 949bb91fc 題庫，重開館方、原始論文、校方聲明及研究者來源。
- [x] 納入 2024 多光譜、2025 Yale 筆跡介紹及 Naibbe 作者 README 的有限結論。
- [x] 按獨立覆核意見修正「2009 年定年工作」、開場不先揭露撤下新聞，以及模型圖僅為提案示意。
- [x] 大綱階段送審後曾釋出票；當時尚無 video.json、未啟動付費工人。

## How to verify

`git diff --check`；`npm run check:tasks`；逐讀三份文件，確認每個大綱主張有來源、每案六章時長與 loops、開場文字可朗讀 30–60 秒。Naibbe 完整論文、原始 Yale 掃描與 NSA PDF 本輪未取得，不可宣稱已讀。

## Notes — 大綱前階段歷史（目前狀態見下方正式稿交接）

工作樹 curio-next-five，base a77a9416d；查核日 2026-10-16 Asia/Taipei。Arizona 原站 404，以大學供稿的 Phys.org 刊載版替代並明示；Naibbe 論文正文 403，但 raw README 已讀。多光譜筆跡歸屬是研究者判讀，不是解密完成。共同預算每集 US$6／五集 US$30 仍是尚未授權提案。本任務付費 US$0，未啟動付費工人、未推送。獨立覆核者 curio_h12_m09_planning 重開八個可讀來源，讀回定年、開場及模型示意修訂後無剩餘阻擋項。凍結 brief SHA-256：4cc10a9506a997a0beca7f102e277fdcd6b45edfa488b204fcc39b3e61b50b6d。git diff --check 與 check:tasks 通過（1895 票；既有長期認領／scope 警告保留）。

2026-10-16 01:01（Asia/Taipei），主代理完成五集手動 outline 送審並讀回 pending；H11 review ID：`83bac5e3-c59b-417e-8060-0b14b4381f60`，對應上述最新 brief SHA。獨立覆核與送審交接完成，釋出認領但不標 done。下一位接手者須先讀回站主 A／B 選擇及本批 US$30 明確授權；目前兩者均未核准。送審卡未啟動付費製作。已送審 brief 維持原樣，由主代理統一 commit／PR。

## 2026-10-16 正式稿交接（目前狀態）

原版及補格式版 A 均已核准，收據見 `docs/videos/curio-next-five-20261016/decision-20261016.json`、`format-decision-20261016.json`。本集 US$6／五集 US$30 已授權，本作者尚未付費。原 research-outline 任務延伸正式稿，owner 保持 `codex-curio-h10-h11-scripts`，保留 claim 供盲評修稿，不另開重疊票。

video SHA-256 `560e1e84f82768a440480a9ab39d8c8b394fe0c88d608b9818fc457dda6e8134`；brief `a82c6e996fbe316e5e0acb27396cc278f94dcbb9278e3b5f9baa33384a28f564`。75 句，文字時間軸估算 9.41 分鐘；純口播估算 489.12 秒。lint 0 errors／0 warnings，詳見 `script-validation.json`。完整正文、逐句來源、loops、估時與作者十三題自檢均在本集目錄。

H11 將材料定年、字詞分布、新聞稿撤下、背面透字、筆跡推測及 Naibbe 作者模型分層；沒有聲稱全文破解或實測模型。待獨立正式稿覆核及站主劇本核准；未送劇本後台、未配音、未產圖、未發布。

本輪 `git diff --check`、逐句／來源／SHA 一致性檢查通過；`npm run check:tasks` 通過，驗證 1895 票，保留其他任務既有長期認領／重疊警告。作者收據並不充當盲評。

## 2026-10-16 第一輪敘事退修

獨立盲評未過：chapters_link, payoffs, no_recap, chapters_are_events, no_detour。已完成第 1 輪結構修訂，原答案保留在 `narrative-round1.json`，逐項回應在 `narrative-revision-1.md`。新版 video SHA `fc9b6b1ff2f94ab75ea1aa2d4e6753ad1d001b0de82ce693a1d3fd89f8e801a4`；75 句，估算 9.57 分。lint 0 errors／0 warnings；未標 narrative pass。提交後釋出認領，供獨立事實覆核接手。無後台劇本送審、無付費呼叫。

第 1 輪修訂驗證：逐句文字及時間軸句序、主張／來源 ID、video／brief SHA 一致；`git diff --check` 與 `npm run check:tasks` 通過（1895 票，只有其他既有認領警告）。

## 2026-10-16 獨立正式劇本史料查核

查核員 `codex-gpt6-h10-h11-fact` 對版號 SHA-256 `FC9B6B1FF2F94AB75EA1AA2D4E6753AD1D001B0DE82CE693A1D3FD89F8E801A4` 完成逐句、逐景資料與上架文字查核；[verify-1.md](../../docs/videos/curio-h11/verify-1.md) 記錄全部 75 句／73 景、來源、存取限制及聽眾檢查。沒有史實修改或未解主張，lint 0 errors／0 warnings。`v6856059` 一句 41 字，配音時注意停頓；期刊 Naibbe 全文未取得，正式稿只使用作者 README 能支持的範圍。此收據只覆核當前 SHA；若劇本改字要重新核對及重新綁定。獨立嚴格敘事盲評十三題全過，但站主正式劇本審核仍未完成。未送後台、未付費。

主代理匯入新的 script-only 盲評答案，`narrative` 工具 exit 0（13/13 yes）。`script --slug curio-h11` 重新生成稿件，SHA-256 `484436B7CA89D3D2F0E372D87768F0533B319B72ED40FCFE4413ADB26FE8E108`；`review-push --gate script` 成功，`review-pull --gate script` 讀回 `waiting for the owner`。正式劇本已在 `/admin/videos` 等待站主核准；尚未配音／產圖。

## 2026-10-16 繁中旁白製作與 QA（進行中）

站主已在後台核准本版劇本，`status --slug curio-h11` 現場讀回 `script approved`。`video.json` SHA-256 仍是 `FC9B6B1FF2F94AB75EA1AA2D4E6753AD1D001B0DE82CE693A1D3FD89F8E801A4`，`script.md` SHA-256 仍是 `484436B7CA89D3D2F0E372D87768F0533B319B72ED40FCFE4413ADB26FE8E108`。保留核准版本，未修改正文。

`tts --dry-run` 為 Gemini Sulafat 73 請求、2,346 計費字元；`keyframes --dry-run` 為 MiniMax image-01 70 景，首輪約 US$0.94、最多三 take 約 US$2.83。共用停手帳本 `<home>/mokaair-work/videos/curio-next-five-20261016/review/spend-ledger.json` 先保留 H11 TTS US$0.20，再實際合成 73/73 請求、75 句 WAV，實測旁白 09:08.2、2,346 計費字元；日誌無 hold，帳本按 US$0.20 保守估算結算，非供應商美元帳單。

音訊 QA 另先保留 US$0.50，`check-audio` 完成 75/75 轉寫、1 次 Jev 判讀：48 句逐字相符、13 句同音／語助詞、4 句 Jev 接受，另有 10 句旗標（`v2405e28`, `v0e564e3`, `v16d9e2d`, `va919cc7`, `v470a2c5`, `v1df5834`, `v439465f`, `v2ebbd0d`, `vd56bdd7`, `v75e1ebb`）。QA US$0.50 以請求數保守估算結算；H11 累計估算 US$0.70，無供應商最終美元帳單。`review/audio.html` 已建立。本機 Whisper small 不看稿獨立轉寫完 10 句，逐句判讀見 `docs/videos/curio-h11/audio-qa-1.md`：0 句足以直接重錄、6 句支持辨識漂移、4 句仍需站主試聽（`v0e564e3`、`v1df5834`、`v2ebbd0d`、`vd56bdd7`）。**旁白尚未核准、未送分鏡、未產圖。**先把音訊與報告送後台；站主聽後若指出確定錯字，再定向重錄並重新核准。

`timeline.json` SHA-256 `FF66A71BAC562CAE9A3013BFC7F72DD50A5F06107D4843F6A8421BD062AEFCA4`。`review-push --gate audio` 已成功送出 H11 旁白預覽；`review-pull --gate audio` 讀回 `waiting for the owner`。下一步等站主試聽並在後台核准，或指出句 ID／錯字。不可把本機第二轉寫當成站主核准。

## 2026-10-16 旁白核准與插畫製作（最新狀態）

站主已試聽 H11 旁白並在後台核准；`review-pull --slug curio-h11 --gate audio` 現場讀回 `audio: approval recorded`，`status` 顯示 `narration approved`。上述 10 句自動旗標仍保留於 QA 收據，未自行重錄。劇本正文與時間軸未改。

`keyframes --dry-run --slug curio-h11 --takes 3` 顯示 70 景，MiniMax image-01 1K，首輪約 US$0.94、三 take 上限約 US$2.83。付費前已在共用停手帳本預留 H11 插畫 US$2.83；原有音訊估算 US$0.70，預留後本集 US$3.53，未逾本集 US$6、本批 US$30。正使用 `keyframes --slug curio-h11 --takes 3` 製作與 Gemini 逐圖評審，逐鏡保存通過的快取。`strange-writing` 三 take 均出現可辨漢字，評審 text 0；整批結束後需定向修提示詞，不能把失敗 take 當成通過插畫。完成後依實際帳本結算、修明確問題，再送分鏡供站主核准。未送分鏡、未製成片、未上傳。

## 2026-10-16 插畫 QA 完成（最新狀態）

第一輪 70 鏡中 67 鏡通過，`strange-writing`、`paper-published`、`story-removed` 三鏡三 take 仍未過。已定向改這三鏡提示詞，第二輪只產生 5 張圖；其餘 67 鏡沿用快取與評審結果。最終 `video.json` SHA-256 `FE86AE2B1795834CA23FC2E032A3DD8AD5C2DF72840AA13116898319C2FB3624`，已核准的 `script.md` SHA-256 `484436B7CA89D3D2F0E372D87768F0533B319B72ED40FCFE4413ADB26FE8E108` 未變。`lint` 為 0 errors／0 warnings；`status` 讀回 script approved、narration approved、keyframes drawn。

最終 70／70 鏡評審通過，0 `needs_review`；manifest SHA-256 `30B7D6CEB8CD441A1D85DC8BDA684C90E959753B954ECD1216FE362C96EFFC99`。三頁聯絡表已逐頁目視，無新增史實矛盾；詳細缺陷、修法與三頁 SHA 見 `docs/videos/curio-h11/keyframes-qa-1.md`。本機媒體帳本工具估算 US$1.458、108 張 image-01 圖片／108 次 Gemini 評審，無 held／unknown／failed；主代理已將修圖預留按 US$0.0675 結算，共用帳本本集與音訊 US$0.70 合計 US$2.158、無未結預留，低於本集 US$6。未製成片或上傳。

`review-push --slug curio-h11 --gate storyboard` 已送出並回報 pending；`review-pull --slug curio-h11 --gate storyboard` 現場讀回 `storyboard: waiting for the owner`。三頁聯絡表已交站主查看；需站主在 `/admin/videos` 核准本版分鏡才可進成片。未製成片、未上傳。

## 2026-10-16 分鏡核准與成片製作中

站主回覆已看過三頁聯絡表並核准 H11 分鏡；`review-pull --gate storyboard` 和 `status --slug curio-h11` 現場讀回 `storyboard approved`，綁定既有 70／70 通過的 manifest。`render` 已完成（3 個需畫的卡片狀態），`clips` 乾跑與實跑均確認 70 張 still、0 個付費片段，沒有新圖或影片生成費用。`assemble` 正在本機編碼；尚未完成最終 QA、成片送審或上傳。

## 2026-10-16 成片已送人工審核（最新狀態）

`assemble` 已完成 9:34.2 成片，繁中字幕 104 cue。最終 QA **10／11**，唯一未過為片尾同一卡片停留 22 秒（規則上限 15 秒）；已在送審時標記 `--manual-review`，不把它說成全過。失效的 Phys.org 轉載連結已換成原始亞利桑那大學實驗報告的可開 PDF；語言檔 `decided_at: null` 明確保留站主尚未選語言。本次只做繁中成片，劇本 75 句、已核准旁白與 70 張分鏡均未改。

`review-push --gate final --manual-review` 成功送出 720p 預覽，`review-pull --gate final` 現場讀回 `final: waiting for the owner`。成片 SHA-256 `060B86C335008868EA93CC1977417A64EBE0A63D7F2994762671D7BBF27D3A15`。完整 11 項、來源修復、預覽與字幕雜湊及停手帳本見 [final-qa-1.md](../../docs/videos/curio-h11/final-qa-1.md)。H11 累計保守估算 US$2.208／US$6；尚未核准成片、未製作上傳包、未上傳 YouTube。

## 2026-10-16 H11 成片核准與繁中基礎包

站主在後台核准成片，`review-pull --gate final` 讀回 `approval recorded`。`package --slug curio-h11` 建出繁中基礎包，四項檢查全過，詳見 [upload-qa-1.md](../../docs/videos/curio-h11/upload-qa-1.md)；`review-push --gate publish` 已送審，`review-pull` 讀回 `publish: waiting for the owner`。後台語言選項尚未保存（`decided_at: null`）；站主表示要另選外語部件，選定後需按其設定製作並重新打包。未上傳或發布。

## 2026-10-16 三語選擇與取樣單位修正

後台已保存英、日、韓各語的標題說明、字幕與配音，`locales_decided_at=2026-10-16T05:22:29.664767Z`；站主另核准 H11 多語 US$2.00，H11 估算停手上限 US$8.00。加上 H10 同額增額，五集目前合計 US$34.00；見 [multilingual-authorization-1.md](../../docs/videos/curio-h11/multilingual-authorization-1.md)。三語工作表已填，但未合併或配音。

英文獨立審稿查到已核准繁中第 `v0e564e3` 句的「四頁」與 Hodgins 2009 原始定年報告的四「葉」不符，已在同一 H11 任務認領內將唯一這句改為「四葉」，同步主張表及來源登錄；原始樣本分別出自第 8、26、47、68 葉。新版 `script.md` SHA-256 `7000C074516D3A30484E794D9D490DFF9412E8A869AD4743D81915CDAC7D6238`，獨立史料及十三題敘事複核全過，lint 0／0；見 [修正收據](../../docs/videos/curio-h11/source-correction-1.md)及[複核收據](../../docs/videos/curio-h11/source-recheck-1.md)。已 `review-push --gate script` 送新版後台，`review-pull` 讀回等待站主；**舊劇本、旁白、成片及上傳包核准不得沿用**。先等新版劇本核准，再重建並送審後續媒體。英、日獨立翻譯審稿的 HOLD 及修項見各語 `i18n-review-*-1.md`；三語未付費合成、未上傳。

## 2026-10-16 修正版旁白核准與新成片待站主

站主已核准 `7000C074…D6238` 劇本與只重錄 `v0e564e3`「四葉」的新旁白；`review-pull` 分別讀回 script/audio approval recorded。重錄一個請求、25 計費字元，其餘舊 take 快取沿用；新版時間軸 SHA-256 `CCFF7C2723920387883243FC131FDFD1B6B8D57606DE39EF1A33587B96E36905`。重新合成的 9:34.3 成片 SHA-256 `54EFA17859D4359B84A9266799108B3C0DE0597DDFAAA2F1B4B3F556801FF1BC`，四語字幕已按新版繁中時間軸產出。完整媒體與 QA 收據見 [final-qa-2.md](../../docs/videos/curio-h11/final-qa-2.md)。

`review-push --gate final --manual-review` 已送新版 720p 預覽；`review-pull` 讀回 **waiting for the owner**。QA 為 10／11，只有片尾同一卡停留 22 秒未過節奏門檻，已請站主審看新版。舊成片與上傳包核准不能沿用。H11 共用帳本目前保守估算 US$2.348／US$8，三語付費配音尚未開始，YouTube 未上傳。
