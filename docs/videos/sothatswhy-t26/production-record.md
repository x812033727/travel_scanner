# T26 單集製作交付

製作日期：2026-10-02。題目：〈為什麼日本常端飯碗，韓國卻常放桌上？〉，原來如此事務所第二季。站主指定先製作一集，採正常 SLIDES／原創 SVG 圖解、台灣口音 Gemini Sulafat 旁白與繁中可選 CC。

本集成片及上架包已完成。正常成片 QA 11／11、上架包檢查 4／4 通過；後台成片預覽已保存並自動核准。這些是工具與後台關卡結果；站主完整播放、人工聽審與上架由站主接續。尚未上傳 YouTube，沒有 YouTube ID。

## 成品與量測

| 項目 | 實際結果 |
| --- | --- |
| 畫面／編碼 | 1920×1080、H.264、30 fps 名義影格率；169 景、26,941 個成片影格 |
| 純旁白 WAV | 180 clips，714.020000 秒（11:54.02）；48 kHz／16-bit／mono |
| 正文 | 26,701 影格；名義 890.033333 秒，ffprobe 容器 890.100 秒（14:50.10） |
| 成片 | ffprobe 容器及串流 898.100 秒（14:58.10）；影格名義時間 898.033333 秒 |
| 品牌 | `mokaair-brand-package-v2-cc`；片頭 150 影格、片尾 90 影格 |
| 插畫／狀態 | 157 張原創 SVG；180 視覺狀態，最長 7.666667 秒、平均 4.944630 秒，圖解占正文 87.962998% |
| 聲音 | 正常合成檢查 -14 LUFS、true peak -0.9 dBFS；未加音樂 |
| 字幕 | zh-TW SRT、VTT 各 180 cues，正文偏移正常品牌片頭 5 秒；沒有燒入畫面 |
| 上架資料 | 縮圖、繁中標題／說明、6 章實際時間、SRT、private metadata 與 `UPLOAD.md` |

純旁白、正文及成片各超過八分鐘；正文不靠品牌片頭片尾補時，也未慢播或重複稿子。實際 PTS 存在既有合成的微小量化／AAC 尾端差異：正文 96 個場間界累積約 -48.503 ms，片尾起於 895.100 秒，比影格網格晚 66.667 ms，正文末影格 hold 約 148.503 ms。不能稱成片平均影格率精確等於 `30/1`；正常編碼／聲音關卡通過，逐 packet 取證與限制記在 `verify-runtime.md`、`verify-visual.md`，沒有修改驗收門檻或字幕去掩蓋差異。

## 檔案與來源綁定

影片工作區：`<home>/mokaair-work/videos/sothatswhy-t26/`。媒體及付費輸出保留於 repo 外，公開 Git 只存主稿、事實與驗收文件、原創 SVG 及必要工具修正。

- `final.mp4`：完整 1080p 成片；`upload/final.mp4` 為核准成片的 byte-identical 複本。
- `upload/`：上架包；操作流程依 `upload/UPLOAD.md`。
- `captions/zh-TW.srt`、`captions/zh-TW.vtt`：可選字幕，非燒錄字幕。
- `checks.json`、`review/qa.json`、`approvals.json`：正常工具證據；核准由正常 `review-push`／`review-pull` 建立。

| 檔案／綁定 | SHA256 |
| --- | --- |
| 主稿 `video.json` | `90975caf8b5f719d6f7f49fd0da4c80a8058cd376df74fc8db6242dd8b044f25` |
| 事實 `claims.md` | `ec889a4246d9190deff7693347d33e1a97735f7c97fd3356151b80529e7fd523` |
| 大綱 `brief.md` | `a3700f660d9ca4a8dd21db5c9587b28e90819606e8eb1b15ebe2836f107fea6d` |
| 原創素材 manifest | `11cd8be93dace7a2775e2b586294c111cb9ece036db0153033c30d27cd36b3a5` |
| 時間軸 | `e2baf37ca8c14e675cd250c8a5a4deb1cf05d17cb726ba38c89b4843f72c5e57` |
| 正文 `build/body.mp4` | `58dcc7961454be07c983bcc19e15e9e7c4e7a125757bf241ee2cc5af1fb144c2` |
| 成片 `final.mp4` | `8aa8ad5b2fb7f89ecddf3a020d048e158bdc70195386f100c27e52cee9cc67b3` |
| 品牌 package hash | `a27622022d8d9e2f56221a81a1d7443ab241c40a37a515925784511f0416dcdd` |

正常 speech hash 為 `ce1ab16b0fde5fad`、visual hash 為 `9e8853bd4d25fbd3`。修改主稿、圖像、時間軸或媒體後必須重新走相應關卡，不能沿用本次核准。

## 已完成的驗證

- 五個一手來源與口語稿經獨立查核，範圍限定指南介紹的常見吃法；沒有採用法律、全民習慣或唯一歷史起因等未支持主張。詳細 claims 與來源見 `verify-1.md`。
- 音訊 180／180 current，正常轉寫／Jev 檢查零旗標；音訊核准綁定目前時間軸。這不是人工完整聽審。
- 180 renderer still 的 32 頁聯絡表已實看；兩項圖文矛盾修正後，重看兩張 renderer 圖及兩頁，核對其餘 178 張 bytes 與 current renderPlan。
- 正常 full force render 180 drawn／0 problems；修圖後正常增量 render 2 drawn／178 reused／0 problems。合成 507 個取樣影格均吻合。
- 從實際 final 解碼並真正查看 13 distinct frames／4 頁，其中 10 格另看原尺寸；兩項修圖、餐具擺位與品牌片頭片尾抽樣無必修。100 格擷取中的其餘 87 格未宣稱親自看過。
- 正常最終 QA 11 項通過，涵蓋合成、renderer、旁白核准、節奏、字幕、metadata、事實、來源連結、縮圖、policy 與 disclosure；正常 package 4 項通過。
- 成片字幕、frame／packet count、實際時長、WAV 重建、資產與既有核准的獨立綁定覆核見 `verify-runtime.md`。沒有將 PNG 雜湊或模型 PASS 寫成完整播放、全部動畫或平台上架驗收。

必要 renderer 修正另以任務 `2026-10-02-video-render-settled-layout` 管理：原 layout 檢查誤量進場中的 `translateY(28px)`；移到既有 settled seek 後執行原檢查，保留真正 overflow、字型、圖片、文字 fit 與進場影格。實際 Edge 回歸 6／6 通過；scoped tests 47 passed／1 opt-in skipped；完整 tools tests 1,206 passed／3 skipped／0 failed。沒有修改主題 CSS 或門檻。

開 PR 前已更新至 `origin/main` 的 `dedcf15d107032c5d561c2ac0e25cb6963aa20b2`；新主線未改本集 scope。重新核對主稿、art manifest 及兩個 renderer 檔案 SHA 均未變。更新後完整 `npm run test:tools` **1,221 passed／3 skipped／0 failed**，exit 0（198.81 秒）；`check:tasks` 驗證 **1,295** 檔，exit 0，保留既有 stale-claim／scope warnings；主稿 lint 仍 0 errors／0 warnings，`git diff --check` 通過。測試 log 保存在 repo 外 `t26-post-rebase-full-tools.log`、`t26-post-rebase-tasks.log`。

## 後台與交付狀態

[本集影片審核頁](https://mokaair.com/zh-TW/admin/videos?video=sothatswhy-t26)。正常 final review `e7710905-a3b8-4a13-a231-29de14bd22b1` 為 approved，綁定上述成片 SHA256；preview、contact sheet 及 thumbnail 皆有已保存的附件 SHA。音訊 review `2f27e1b4-cf19-48b3-a8fb-b7d33064e3dc`、現行 outline review `6da52b1d-3980-455b-bafe-4d3061d7c8d1` 亦為 approved。

正常 publish review `3e729749-4dfa-4088-9dfe-119bb9806edb` 為 approved，綁定 `upload/metadata.json` SHA256 `e5d220cd3056cfaeda78dd6636d0e6c2c6f3f9d1385b648eb955a10ac5edfe66`。其 final 附件 SHA 等於本次完整成片；字幕附件 `captions_zh-TW` SHA 為 `6cc731996e19d455b35dbed040d5020f7f0a0446c13f1bebb7ad22516e16416b`。這個 gate 是上架包確認，不代表 YouTube 上架。2026-10-02T12:11:11.062Z 的正常 live GET 確認 `on_youtube=false`、YouTube ID 為 null，所有製作 checklist 已完成。

該 live GET 亦確認後台 `locales_decided_at=null`、`ready_to_upload=false`、`download_available=false`；前兩者是尚未保存站主每集語言確認，後者是合集下載欄位，不代表正常 publish 的成片附件不存在。本集完整 final、metadata、thumbnail、繁中 SRT 及 description 均已列於核准的 publish review 附件。去除憑證及非必要欄位的 live 收據保存在 repo 外 `t26-remote-delivery-2026-10-02T12-11-11-062Z.json`，SHA256 `bcaeef5d0f936d7249df7f055e599f4228484d7958ce57affdf65a6c7f15cb47`。

完成正常 publish pull／report-only 並更新主線後，2026-10-02T12:22:20.264Z 再用正常 GET 刷新同集；上述核准、影片／metadata／附件 SHA、YouTube ID null 及待站主語言確認皆未變。刷新收據 `t26-remote-delivery-2026-10-02T12-22-20-264Z.json` 的 SHA256 為 `df7f2b21f54053687e17f9069a34b9b7e1d624da13c66d797619e09aab93d7a8`。

這集本機製作僅繁中，`languages.json` 為空追加語言選擇，不做額外翻譯、配音或 Shorts。後台每支影片的站主語言確認是另一筆 owner 記錄，不能用本機 choice 假稱它已保存；最後 live receipt 另記錄實際 `locales_decided_at`／`ready_to_upload`。沒有變更全站語言或圖片開關、沒有啟用 uploader、沒有暫停或重啟 worker。沒有部署本次工具修正，也沒有上傳或公開影片。
