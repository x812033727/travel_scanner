# 八種外語交付結果與正式批次狀態

2026-10-25。en、ja、ko、es、pt、id、vi、th 八種外語的標題說明、CC、M4A 配音及本地化縮圖已完成，並經 `final`／`publish` 路由交付後臺、讀回檔案大小與 SHA-256。八語各 80/80 句實際音檢通過，共 640 句；這是繁中原版之外的八語，沿用同一支繁中字卡成片。

可供 PR 審查的公開收據為 [delivery-verification.json](delivery-verification.json)，包含八語音檢、47 個後臺檔案角色讀回、八張縮圖、M4A evidence aliases、pending 狀態及 QA／字幕提示；完整工作收據仍留 repo 外。

**正式 `languages` 批次仍未完成。** 本輪原生送出實際以 exit 3 停止，原因是遠端來源 `final` 審核仍為 `pending`。檔案已交付不等於正式語言批次已綁定，後臺三項語言狀態目前仍為 `working`；不改寫成核准或發布。

站主於 2026-10-25T11:26:16.864834Z 儲存八語三項選擇，本機於 11:28:25 UTC 讀回，`languages.json` 保存同一選擇與時間。可重用 AI／科技技能已記錄繁中原版加八外語，八語各含 metadata、CC、配音；兩份技能鏡像內容相同，本次沒有修改技能或聲音。

## 配音與本地檔案

依 `language-delivery-verification.json`（2026-10-25T16:10:53.139Z），八語均對應目前翻譯、80 個實際 take 與當前 M4A；`all_eight_ready=true`、各語 `ok=true`、`problems=[]`。旗標及未檢查項目均已經原生檢查收斂，沒有手動清除旗標來冒充通過。

| 語言 | 音檢 | M4A 秒數 | LUFS | 解碼後 dBTP | 實際音檢完成 UTC | M4A SHA-256 前 12 碼 |
| --- | --- | ---: | ---: | ---: | --- | --- |
| en | 80/80 PASS | 500.6 | -14.0 | -2.9 | 15:08:34.827 | `5cf6c30562ce` |
| ja | 80/80 PASS | 500.6 | -14.0 | -2.9 | 15:15:55.954 | `7c125e717693` |
| ko | 80/80 PASS | 500.6 | -14.0 | -2.8 | 15:50:34.574 | `d9892bb2d7ba` |
| es | 80/80 PASS | 500.6 | -14.0 | -2.8 | 14:24:14.565 | `f6f3fb19706d` |
| pt | 80/80 PASS | 500.6 | -14.0 | -2.9 | 15:19:46.714 | `2cd6acdb52cf` |
| id | 80/80 PASS | 500.6 | -14.0 | -2.8 | 13:19:03.647 | `1a9d6c65325c` |
| vi | 80/80 PASS | 500.6 | -14.0 | -2.9 | 15:44:38.378 | `efff6ed7da29` |
| th | 80/80 PASS | 500.6 | -14.1 | -2.8 | 16:06:17.787 | `299606e37bf4` |

日文最大視窗調速 1.12 倍，泰文 1.09 倍，其餘各語最大值為 1 倍。配音沿用本片既有 `dub-with-peak-guard.mjs` 的 AAC headroom；上述數字為最終編碼檔的實測值，不是預估可容納的字數。完整 bytes、雜湊、翻譯雜湊與各次量測時間保留於收據。

韓文先前一個 34 字請求曾回 HTTP 502，沒有可用音檔，原請求是否計費仍無法查明。原收據及一次有界替代決定保持原狀；後續成功與本表 PASS 不表示原請求未計費。先前無效的第二轉寫、各輪旗標及舊 take 也保留歷史，不當成本輪通過證據。

## 後臺檔案與下載位置

`backend-delivery-verification.json` 於 2026-10-25T16:44:51.430Z 以正常 project readback 核對伺服器已驗證的大小與 SHA-256，`ok=true`、`problems=[]`：

後臺入口：[OpenAI DNS containment](https://mokaair.com/zh-TW/admin/videos?video=openai-dns-containment)。

- `final` 收到八個 `dub_{locale}`，以及八個同檔的 `evidence_{locale}_m4a`。後臺該片「成片 → 原始證據」有這八個 M4A 下載項；各 evidence alias 與對應 M4A 的 bytes／SHA 相同，見 `backend-audio-downloads.json`。
- `publish` 收到繁中加八語共九份 CC、九語說明與完整 metadata、八張本地化縮圖、繁中三張縮圖變體及原成片。metadata SHA-256 為 `50db2164febff5232de9b028f929da7cb31396023cf9a8c3114ea9debea937b9`。
- 八張外語縮圖最後檢查均 `ok=true`、無警告，為 1280×720 JPEG；手機寬度 320px 時大字約 24–34px，見 `thumbnail-final-checks.json`。早期縮圖檢查警告保留於原 QA 收據，沒有以新結果刪除歷史。

此處的遠端核對是已儲存 blob 的伺服器驗證結果與 project metadata 讀回；沒有冒稱使用管理員專用路由重新下載二進位。檔案已提供下載，也不等於遠端審核已批准。

原繁中成片保持不變：SHA-256 `32dc8fc9e7de880011ab257dc3e774ddf23e4203dc1138a6d1f1bac88ca50dd6`，正文 500.6 秒；沒有重做原版 TTS、畫面或組片。YouTube video ID 仍為 null，未上傳或公開到 YouTube。

## 仍保留的 QA 結果

最新原生 `review/qa.json` 為 **10/11**，不是全數通過。唯一未通過項為 policy：Jev 立場 0.73、示範 **0.48**、建議 0.01、業配 0.03；示範低於 0.6 門檻。早期繁中原版 `review/qa-original-zh-TW.json` 的示範 **0.46** 保留為歷史，不拿它取代最新 0.48，也不把站主委派的採用決定寫成工具通過。

九語 CC 檢查為通過並帶 **35 項速度 advisory**：es 5、pt 1、id 4、vi 25，均保留在最新 QA。它們是超過每秒 17 字元的閱讀速度提示，不能寫成「字幕零警告」。配音 640 句音檢 PASS 也不會消除這些字幕提示或 policy 未過項。

## 正式批次的外部依賴

`backend-delivery-verification.json` 讀回遠端 `final=pending`、`publish=pending`；八語 metadata／captions／dub 仍為 `working`。因此包含正式批次綁定的任務保留 `blocked`，不勾選完成。

已存在有界後續監看，沒有另外啟動第二個工人：`formal-language-binding-watch.json` 記錄 2026-10-25T16:44:44.829Z 開始，至 2026-10-26T16:44:44.829Z，間隔 300 秒。本次文件核對時讀回為 2026-10-25T16:49:47.685Z，狀態 `waiting_for_genuine_source_approval`。

等待期間只讀遠端狀態；只有真實來源成片審核變成 `approved`，且成片／package 雜湊、站主選擇與本地媒體仍吻合，才再驗證媒體並正常呼叫一次原生 `review-push --gate languages`。監看不作審核決定，不建立假核准；來源、選擇改變或拒絕時停止，24 小時到期也停止。若送出成功，仍須依新收據記錄批次狀態，不能把送出當成批准。

全部媒體與上述收據在 repo 外：`/workspace/work/videos/openai-dns-containment/`、`/workspace/work/ai-tech-dns-containment/`。本文件只更新交付事實與未完成依賴，未改 voice、技能、UI 或審核結果。
