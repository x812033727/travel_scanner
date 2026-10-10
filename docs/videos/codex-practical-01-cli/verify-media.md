# CLI 01 靜態畫面查核

查核日期：2026-10-11（Asia/Taipei）。狀態：`static_visual_pass`。目前版本的總覽、繁中縮圖及八張代表完整字卡，未見文字裁切、遮擋或溢出；終端紀錄已明標「真實測試輸出摘錄／重新排版」。這份結論只涵蓋靜態畫面，不是完整媒體核准。

查核者 `codex_feasibility` 曾編寫本片稿件，因此不自稱獨立內容審稿者。未參與撰稿的 `media_readability` 另獨立檢視跟做命令、終端紀錄、作者參考版比較三張完整字卡，並重新檢視修正後的終端字卡，確認新標示清楚且無裁切；稿件的獨立事實與教學查核另見 [verify-1.md](verify-1.md)。

## 版本與產物綁定

來源：`docs/videos/codex-practical-01-cli/video.json`。外部媒體根目錄：`C:/Users/x8120/mokaair-work/codex-practical-series/media/codex-practical-01-cli`。下表媒體路徑均相對於該根目錄；本報告不要求將 PNG、音訊或成片提交到版本庫。

| 檔案 | SHA-256 |
| --- | --- |
| video.json | `4ff3c4981a53b42319b33045fa6df1cdfa4f19a3c60b0b55da54fd2ded00c93a` |
| frames/manifest.json | `394cf11d0e9152c771d942e7e436c77ca0aebbf673fecbe438112f611cae3b6c` |
| frames/cache.json | `1ecd85ca53d25edae645adb9664f37a4aab29bb217b75008b0676676b170eae9` |
| contact-sheet.png | `8d9ba968e3010a1c2de6e471b91a9a98b76212299e553eb07ca236d401edc20c` |
| thumbnail.jpg | `a6a7c8c79d4f49aaf8aacdcd06e2e5e09001246db1226baa4fc4b218dcf05c1f` |

以現有工具的純函式重算，來源 `visual_hash` 與 manifest 均為 `d2cfd740cf8615d8`；目前主題與 manifest 的 `theme_hash` 均為 `17fcf59dd1a1f4ac`。manifest 為 60 張卡、136 個狀態、1920×1080、30 fps；1445 個靜態圖與轉場圖引用均存在。cache 共 139 項，包含修正前的歷史快取；所有項目的 `problems` 皆為空。不能把 139 項說成現行 139 個畫面，也不能把自動檢查沒有問題說成人眼逐張驗收。

總覽原圖為 1920×10731，檢視工具顯示時縮為 1074×6000。已用它檢查 136 狀態的版面一致性、揭露順序及明顯遮擋；細字可讀性以完整 1920×1080 代表字卡判斷。

## 最終版本續查

最終旁白更新後，重新核對來源與 render 產物。前次來源 SHA-256 `a912a176d6981e4fcfc86097e96aa2f36d6ff3ca67290199fe3350455055fa17` 保留為歷史版本；目前來源以表列 `4ff3c498…c93a` 為準。視覺與主題雜湊不變；manifest、cache、總覽、縮圖及下列八張代表圖的 SHA-256 都與前次持久化報告相同，1445 個現行引用仍全部存在。

實際讀取 `C:/Users/x8120/mokaair-work/codex-practical-series/runs/pilot-render-finaltimeline.log`，內容為 `0 states drawn, 136 reused, in 13 s`，SHA-256 `7220474277d66eb34542fc67bf6f9d3ef4e45f93152c8998631ea6a7c2aab394`。這是渲染快取沿用證據；本次未重畫或擴大人眼檢視範圍。

前輪完整 136 張雜湊表只曾放在工具 session 記憶，沒有持久保存，跨回合後不可取得。因此不宣稱做過全 136 張前後逐位元組比對；前後 byte 比較限定原報告已保存的八張代表圖。為後續續查，已將本版 136 張 active still 的逐檔 SHA-256 保存為 `C:/Users/x8120/mokaair-work/codex-practical-series/runs/independent-media-visual-20261011/final-active-still-hashes.json`，收據 SHA-256 `087094d28b14ed39679631bc6bdf51be6243d978cd6af327c14bdc0e9c493756`。該收據同時保存來源、manifest、總覽、縮圖、渲染紀錄與八張比較結果，不提供音訊或成片核准。

## 實際檢視的完整字卡

八張現行代表 PNG 均存在於本版 manifest。其餘狀態沒有逐張以完整解析度閱讀。

| 字卡 | PNG | SHA-256 |
| --- | --- | --- |
| 真實測試輸出摘錄／重新排版 | frames/19c639c6de4ca7d7.png | `b063c1dc28fc2495094188bd3994276486bd33de6d588f51fe87f0390508add9` |
| 只讀提示 | frames/a6221531bcd3197a.png | `3773bcf866523e5ced38333fb562f3a6830612decfdaf3ce559edf1474affcee` |
| 五檔責任表 | frames/e34c73c2dc0ec1b5.png | `86f71559e8ca97194f3b944fc883602dbebf38fe4efa96ead0a5602768ddd6a7` |
| 換題練習步驟 | frames/68821b566e5e95bf.png | `24193e93d25a2fa1317f0148a62815b8a7f4c0978e7052eb24d8f461ba7f9ada` |
| HTTP 網址 | frames/3a76ddb50f62d24f.png | `3d098904d911fd0010c1cddb9a136b97a5cdf8c1d6815d5903e07d67557047d8` |
| 作者參考版比較 | frames/fcd14cdae8de9065.png | `9ba7577981d49f4e4f5ded4dce513685c7373bed399f1f517ac4178b5005de09` |
| 完成與未執行狀態 | frames/e00ed10bdc878a21.png | `9c380a97685ab2235f0560b69fafdce2abd0d5694abd298be8670c920b79d79b` |
| PowerShell 跟做命令 | frames/26e28a88ea5fc9fc.png | `31adb646f0acafff59d37e9e9f3745d628882857cc82c9df54ba9f0b1821d16a` |

觀察結果：

- 終端標題、命令與 3 tests／2 pass／1 fail 清楚可讀，內容留在面板內；修正後的來源標示排除了原生終端截圖的歧義。底部日期及版本字級較小、對比較低，屬於次要來源資訊，在完整圖可辨識。
- 五檔責任表及作者參考比較表的欄列清楚，沒有跨欄或遮擋。作者參考版標示與「本輪模型未改檔」狀態卡清楚區分來源，未把作者成果呈現為模型修補。
- 只讀提示與跟做命令沒有水平裁切；後者明標「不是錄製的完整原始 argv」。換題練習的三步驟換行自然，步驟箭頭沒有壓住文字。
- HTTP 網址完整可見，左右仍留安全邊距。代表字卡未見個人完整路徑、帳號或憑證。
- 繁中縮圖為 1280×720，「跑完 ≠ 做對」及「CODEX 實作 01 CLI」可讀，未見文字溢出。沒有另外模擬手機小尺寸縮圖。

## 修正與查核界線

首次看終端字卡時，測試結果雖為真實紀錄，終端視窗樣式可能讓觀眾以為是原生截圖。root 已只修改其視覺標題、重渲染三個狀態；修正版完整圖已重新檢視，標題清楚，結果數字保持一致。未因本項視覺修正重送模型或旁白。

英文、日文、韓文縮圖字詞仍列於 `thumbnail_locale_gaps`；本次查核限定繁中縮圖。若之後新增其他語系，須另渲染與檢視。

本次沒有播放成片、聆聽旁白、核對字幕同步、評估轉場動態或逐張停留時間，也沒有閱讀音訊／成片 QA 收據。Codex App 原生介面未錄製；本報告不提供 App 操作完成的證據。完整媒體 QA、站主播放與上架仍需各自的關卡。來源、主題或產物 hash 改變時，須重新綁定相應檢查。
