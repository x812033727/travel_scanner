# CLI 01 靜態畫面查核

查核日期：2026-10-11（Asia/Taipei）。狀態：`static_visual_pass`。目前版本的總覽、繁中縮圖、八張既有代表完整字卡及三張新結尾字卡，未見文字裁切、遮擋或溢出；終端紀錄已明標「真實測試輸出摘錄／重新排版」。這份結論只涵蓋靜態畫面，不是完整媒體核准。

查核者 `codex_feasibility` 曾編寫本片稿件，因此不自稱獨立內容審稿者。未參與撰稿的 `media_readability` 另獨立檢視跟做命令、終端紀錄、作者參考版比較三張完整字卡，並重新檢視修正後的終端字卡，確認新標示清楚且無裁切；稿件的獨立事實與教學查核另見 [verify-1.md](verify-1.md)。

## 版本與產物綁定

來源：`docs/videos/codex-practical-01-cli/video.json`。外部媒體根目錄：`<home>/mokaair-work/codex-practical-series/media/codex-practical-01-cli`。下表媒體路徑均相對於該根目錄；本報告不要求將 PNG、音訊或成片提交到版本庫。

| 檔案 | SHA-256 |
| --- | --- |
| video.json | `aedaef1c2c4af4958f01a9522bfc23e949f92c3945be73c38998739f314d99d2` |
| frames/manifest.json | `c2dce8eb308fbf4341f88444049aebf5493e1071a302886d9c6234bafe06d951` |
| frames/cache.json | `29829a4bac12fc12c46011f982f67116bd60dff22ec3031171df90ce47366db4` |
| contact-sheet.png | `c3ba304e2158aa3b8e805bd9ca4524744cba10f5100284f2c30b8bafe8fa97da` |
| thumbnail.jpg | `a6a7c8c79d4f49aaf8aacdcd06e2e5e09001246db1226baa4fc4b218dcf05c1f` |

以現有工具的純函式重算，來源 `visual_hash` 與 manifest 均為 `1d1dcaaba9d0661b`；目前主題與 manifest 的 `theme_hash` 均為 `17fcf59dd1a1f4ac`。manifest 為 60 張卡、138 個狀態、1920×1080、30 fps；1458 個靜態圖與轉場圖引用均存在。cache 共 142 項，包含修正前的歷史快取；所有項目的 `problems` 皆為空。不能把 142 項說成現行 142 個畫面，也不能把自動檢查沒有問題說成人眼逐張驗收。

現行總覽原圖為 1920×11043，檢視工具顯示時縮為 1043×6000。已重新檢視 138 狀態總覽，確認新結尾的三個揭露狀態及版面一致性；細字可讀性以完整 1920×1080 代表字卡判斷。

## 136 狀態版本的歷史續查

上一輪旁白更新後，曾重新核對來源與 render 產物。該輪來源 SHA-256 為 `4ff3c4981a53b42319b33045fa6df1cdfa4f19a3c60b0b55da54fd2ded00c93a`，更早的來源為 `a912a176d6981e4fcfc86097e96aa2f36d6ff3ca67290199fe3350455055fa17`；兩者均保留為歷史版本。該輪視覺與主題雜湊不變；manifest、cache、總覽、縮圖及下列八張代表圖的 SHA-256 都與前次持久化報告相同，當時 1445 個引用全部存在。

實際讀取 `<home>/mokaair-work/codex-practical-series/runs/pilot-render-finaltimeline.log`，內容為 `0 states drawn, 136 reused, in 13 s`，SHA-256 `7220474277d66eb34542fc67bf6f9d3ef4e45f93152c8998631ea6a7c2aab394`。這是該輪渲染快取沿用證據；該輪未重畫或擴大人眼檢視範圍。

最初完整 136 張雜湊表只曾放在工具 session 記憶，沒有持久保存，跨回合後不可取得。因此該輪不宣稱做過全 136 張前後逐位元組比對；當時 byte 比較限定原報告已保存的八張代表圖。後來已將 136 狀態版的全部 active still SHA-256 保存為 `<home>/mokaair-work/codex-practical-series/runs/independent-media-visual-20261011/final-active-still-hashes.json`，收據 SHA-256 `087094d28b14ed39679631bc6bdf51be6243d978cd6af327c14bdc0e9c493756`。這是以下結尾修正的完整持久化比較基準，不提供音訊或成片核准。

## 結尾漸進揭露修正：現行 138 狀態

root 將一張結尾改為三項逐步揭露的 bullets 字卡。本查核者未撰寫這項視覺修正，已獨立以完整尺寸檢視三張新圖：標題、已揭露的重點、編號與頁尾都清楚，沒有裁切、重疊或溢出，留白充足。先前 `media_readability` 的查核範圍沒有擴張到這三張新結尾圖。

以完整持久化的 136 狀態基準逐檔 SHA-256 比較，135 張保留圖的位元組完全一致；移除的只有舊 `outro` reveal=0，新增的只有 `outro` reveal=1／2／3，沒有其他狀態變更。另直接比較封存的 `<home>/mokaair-work/codex-practical-series/media/codex-practical-01-cli/review/history/pace-fix-1/video.json` 與現行來源：162 句旁白文字與 ID、非結尾場景、所有場景的 claims 陣列完全一致。

現行 138 張完整逐檔 hash、135 張比較結果、新增／移除狀態、來源、manifest、cache、總覽及縮圖綁定，已保存於 `<home>/mokaair-work/codex-practical-series/runs/independent-media-visual-20261011/outro-pace-fix-1-active-still-hashes.json`，收據 SHA-256 `c82e806aea1ec08a535cfd6e0dd25f3c05ebe592ca810e056705e23ba682d07d`。本次未評估成片秒數或動態節奏，不能以靜態圖結論代替完整成片 QA。

## 實際檢視的完整字卡

八張既有代表 PNG 及三張新結尾 PNG 均存在於本版 manifest。其餘狀態沒有逐張以完整解析度閱讀。

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
| 結尾：第一項 | frames/2e954f0e38ff2018.png | `4744d924d8f8a94e81b2d5b11be599f3d9305f4130e6a7ebcc251e63ae10fb3c` |
| 結尾：前兩項 | frames/e712829838ed339d.png | `b50033bfcb9794dcde64a07c8896ea125c295f69a410581cd7fedc67f0fa8df5` |
| 結尾：完整三項 | frames/a68687531ee119fa.png | `fe8bdac2a9e736dbb87ad230e6f120cd13efc328e01e8bf105b78e5986c81152` |

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

公開定位說明：`<home>` 與 `<repo>` 是去識別佔位，不供直接執行。精確路徑與未遮罩原始收據保存在 repo 外；既有收據 SHA-256 仍綁定原始位元組。
