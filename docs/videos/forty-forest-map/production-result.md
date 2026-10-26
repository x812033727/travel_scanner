# ForTy 製作結果快照

文件觀測時間 2026-10-26T07:29:19.902839+00:00。本片正式官方 v4 主片及四種已驗外語 M4A 已送達[後臺影片頁](https://mokaair.com/zh-TW/admin/videos?video=forty-forest-map)；繁中、EN、JA、KO、VI 的實際時間軸 SRT／VTT、完整標題說明也已交付並讀回，共37個角色。已交付外語三部件為4／8，尚未完成 ES、PT、ID、TH。新版原生 QA **false、10／11**，final **pending**；35項閱讀速度提示（已交語言17項）與 ES／PT 各一 stale hard error 全保留，沒有宣稱八語或全部新規則完成。

## 正式官方新版與原版

| 項目 | 真實結果 |
| --- | --- |
| 來源／旁白 | source `450bd6ad82146cfa1110abfe133cf9124980095a22402e72bfe0c693a743394a`；speech `c6d70ecaef91a15d`；MASTER `51287e2d03921fe5da488590f23180257323c85b048c2f11cf35afe14f1773d7`。92句完整 intended／current WAV／ASR cache／原生裁決重新核對，0 flags／unchecked。 |
| 新主片 | SHA `564812bd2a172daab0782b95a8c19ab44e5ac0d567304767eeaa2f6aee46c40a`，47,603,425 bytes，1920×1080 H264／30fps；16163影格＝538.766667秒。AAC 48kHz雙聲道／container538.810秒，實測尾差0.043333秒，沒有將container長度稱作video長度。 |
| 官方 bookends | 5秒／150影格 intro 在第一章後 body frame682插入；21秒／630影格 outro。官方 package `416c8768d4d29f2e746a0c019d2d598ec367cbb66b0ff996841c523651a63e88`，正常 placed hash `39d34ab0d563aff4143d88518e178fe57e769747772084c7e9b05f42f6aeda64`。兩者用途不同，並非應該相同。 |
| 保留的原版 | 原 BODY `b293282ddfefdf7fb6d20e88bfef46b281c1ecac31807ac0ecc13ee4eb193d18`／41,255,462 bytes，與新copy的 build/body.mp4 全 SHA 相同。舊 final `56c69b8f-3ee1-4c8d-9050-a507fe972185` 真實 **approved**、12角色、QA11／11與原決策完整保留；沒有把它寫成仍pending。 |
| 新版 QA | `b14466b19eb9beb3f96ae84b08a538235a6763dcef29a356fd26d2629e2760d2`，false10／11；唯一失敗為 captions 的 ES／PT stale track。Jev 立場.83／示範.95／建議.01／業配.04。原生inline QA function return1；外層正常手動review-push OS exit0，兩者沒有混為一談。 |
| 新版審核 | `95bd4a89-2f84-4b44-8c54-9d98e1b4676d`，pending／manual candidate，ready_to_publish=false。沒有伺服器核准、language batch、YouTube發布、merge或deploy。 |

原始資料仍是2020年模型輸出，兩個台灣ROI及73項資料斷言的獨立覆核保留；B像素刻意選低分／同分，不是精度抽樣。沒有新增實地真值、重訓、官方App親測或2017–2025年度變化測量。敘事關卡仍9／13、passed:false，四項教學取捨NO保留。來源連結曾遇DOI403，後來固定v1官方API GET200、plain DOI及六筆CC BY4.0署名均保留。

## 實際外語與字幕交付

| 語言 | 目前品牌版 M4A full SHA-256 | bytes | 音訊核對 | CC cues／CPS提示 |
| --- | --- | --- | --- | --- |
| en | a127795f881fcb74adc5d096df71e4d62df5f32c0addd4133fa85e6e701bb277 | 14389761 | 92／92、0 flags／unchecked | 98／0 |
| ja | 00b4ff60773a15b9714b6f13bb85cfb4a657c4d74abc7c2c269f9afd3e7f6c03 | 15639130 | 92／92、0 flags／unchecked | 121／0 |
| ko | 5221939a899018fbdfd6e80fce6dded4d294a88148e97fb158995e264d5e879d | 13617826 | 92／92、0 flags／unchecked | 114／1 |
| vi | 9eb888015cbf0b710950c1ea741a8a8f9b3caf790ce342c9acf4bdf8b3b98817 | 12998465 | 92／92、0 flags／unchecked | 101／16 |

四語各92句、89fit窗，無skip／keep-fitted；EN／JA／KO／VI最高tempo依序1.21／1.19／1.14／1.10。四軌均538.810秒／AAC48k雙聲道／−14.1 LUFS，TP依序−2.8／−2.9／−2.5／−2.9。新官方presentation以原來已驗body raw／cache零TTS重封裝；正常cached check真exit0，完整368句與原始裁決、fit／meter及 current M4A 綁定獨立覆核。沒有新ASR／Jev呼叫或全檔人工聽完的宣稱。

繁中97cues／0提示；EN98／0、JA121／0、KO114／1、VI101／16。全部各完整92個來源ID，外語四軌採自己的current dub timing，繁中採旁白；native presentation位移只做一次，無跨官方bookend。完整標題含原生CC標籤，TXT為title＋空行＋完整description＋LF，與已在新final的native metadata逐項一致。實際章節為 `00:00 / 00:27 / 02:05 / 02:57 / 04:38 / 07:03 / 08:26`。

05:24:15.249Z主片＋四M4A真交付，receipt SHA `de3f67369239428ba714b8ff16d7d2bd4ee4ba78bc6e94bee2e87b9416e45268`。06:02:27.467Z再以15個text blobs／25新增角色、一次same-pending POST交付五語SRT／VTT／標題說明，receipt SHA `f9b12728187f34f6efbc55c3ea90471376a3d2704cb448237f8284ffdbb3f981`；原12current角色與payload、QA、owner choices、舊approved12均保留。37角色及每個 full SHA／bytes 見[實際交付摘要](receipts/official-v4-20261026/actual-delivery-and-37-download-roles.summary.json)。

核驗範圍是正常server分段組裝SHA／大小加authenticated role metadata讀回；沒有遠端binary下載再重算SHA。普通POST沒有CAS，freshGET可檢出前段競爭，不能冒稱提供原子compare-and-swap。未回寫標準dub ready或伺服器approval。正式八語package／language batch仍未完成。

## PT與ES的未知結果必須保留

PT v3唯一原生process258624於06:50:04.672149Z開始、06:50:36.418431Z真exit3。**本地92 raw WAV SHA變更0，沒有完成native stage／fit／新meter／音檢；上游計費總額及音訊結果UNKNOWN。** 原生失敗文字與journal回報Mokaair HTTP502，不能推成provider也回502或零收費。原driver270e中「未暴露final HTTP」的欄位範圍誤判由root [正式更正](receipts/official-v4-20261026/forty-pt-branded-R1-v3.root-unknown-outcome-review.json)，原driver收據未改寫。

只新增的held request body為 `3cc1ce6b7a4c1026cc52686be17962a255277ad86f795c46c88378068c0ee456`，journal fullSHA `b9d12c0e77dc02ec913bf8f23b82089e5172ae93675b24f39dea14a31203f75d`。原文retake1／shorten2／reword0原計數保持，舊known429零成功及本次未知不是同一個結論。系列hold現SHA `ad19fab46b2044ba5ea34ffd14a2d980d195f363007e456cdb3a02694661c384`，舊hold E8ac已封存。即使07:50:36.418431Z到了，也必須先取得真實per-request上游usage／結果或可恢復回覆，不能replay、forget、手動清journal或稱零計費。

較早ES request9a36／journal3935是另一個尚未解決的held未知結果，保留其原完整日誌與失敗，不以PT或成功GET代替解決。ES／PT stale captions仍在真QA內；ID／TH只有已審文字，沒有已驗M4A。接續完成八語仍依正常音訊／fit／字幕品質關卡，不能降門檻、清旗或夾送未驗fitted dub。

## 文件與來源時點

更新前已完整核對並封存74來源、329core、2wrapper、2132canonical檔案；舊可變文件與Git979c版本見[歷史封存](history/before-official-v4-doc-refresh-20261026/README.md)。當前source video、speech、voice、lexicon、data、四個accepted target及WAV均未變。此輪只改文件；原來來源74中的四份文件合法更新後，舊delivery proof仍是交付當時的歷史稽核，不冒稱剛重跑或全74目前仍同hash。

原始dirty i18n/es.json、pt.json保持bytes且不stage；[完整SHA索引](receipts/official-v4-20261026/README.md)使用清楚標示的production source snapshots，並分開列Git HEAD舊hash，不宣稱GitHEAD路徑等於實際製作來源。未複製token、auth、rawjournal、完整後臺快照或媒體。兩張未實作gap票（旁白pending進度區分及普通TTS收據恢復）仍open；本輪無任何功能修正。詳見[逐語進度](localization-review.md)與[機器進度](production-progress.json)。
