# T27 日本垃圾桶調查：製作紀錄

2026-10-02 至 2026-10-03（Asia/Taipei）；站主在 T26 完成後指定「做下一個」，依第二季有效企劃製作本集〈日本垃圾桶少？旅客調查說了什麼〉。本集為原創插畫長片、台灣口音 Gemini Sulafat 旁白及可選繁中 CC。

## 定稿與獨立查核

137 句、六章、2,201 口語單位。另一位查核者完整讀取觀光廳公告、原始面訪方法與複選圖表、報道發表 PDF 及羽田名稱對照，13 項主張全部核對，沒有未解決事實。公布日為 2026-04-28；面訪收集時間為 2025-11-18 至 2026-01-13，對象是五座機場的 4,110 名離境外國旅客。17.2% 是最多被選的困難項目，43.7% 是沒有困難；多選題不能畫成互斥比例，也不能把「最多」說成「多數」。另外 2,000 則網路貼文不併入面訪分母，不推論全國垃圾桶數量、密度、單一歷史原因或隨機代表性。

十人卡片明示為原創假想例子：六人遇困難、七次困難勾選、四人無困難，合計十一個勾選；不是調查資料或真實訪談。所有比例圖共用 0–100 軸，跨年日期卡只表示順序。

正常 Jev 選大綱 A、自動核准，choice 0.99、stance 0.94、demo 0.86、advice 0.01；核准後 brief 未改。最後只有一處聽眾改寫：63kr／c1-s17 從「把兩個問題分開，第一名才不會越講越大。」改為「把兩個問題分開，就不會把第一名當成多數。」獨立覆核確認事實與數字未變，正常 rewrite 收據及舊稿／語音檢查快照均保留。

- video.json SHA256：`89d7d0fb16acfb196d5f19f6f9cc96a776b69b08234a492f1d3e8fd7078d494c`
- speech hash：`e763f5bdd108bfa1`
- fact-source-audit.json SHA256：`fff4ae7c5bdac4beaaf8ce6b56253527836ced4024bd6f9a52efbf0e25582eda`
- verify-1.md SHA256：`783cdf2689cb1c7f32b05681f900b820f99a3b6ca54a072584f569e87e4e0131`

2026-10-05 補記：倉庫是公開的，本紀錄與 `fact-source-audit.json` 內的本機使用者路徑已改為 `<home>`，其他內容不變；上列 fact-source-audit.json SHA256 因此改為遮蔽後的值（任務 2026-10-05-scrub-local-user-paths-from-the）。遮蔽前的檔案與原雜湊見 commit bc5f18db8（#1144）。

原始稿、assets 登記稿與單句改寫稿的雜湊保存在來源譜系，沒有以新稿覆蓋原始版本的證據。

## 語音與正文實測

正常 dry-run、額度及同題去重前檢後，首次 137 次 TTS 成功、2,477 計費字。每次收到的 WAV 回應與請求雜湊保存於 repo 外 `_requests/`。首次 check-audio 標 37 句，離線 Whisper 第二意見清除 23 句，其餘按正常有限重錄處理。

首批重錄完成 12 句後，s8yh 的第 13 次請求回 HTTP 502：request ID `1790948629363-cfcb89a4ed6e`，request SHA256 `cfcb89a4ed6eaa04c5ac16e7ffa00e77488b66057167996bbc02983d32464f01`。guard 停止自動重試，保留成功音檔及檢查。既有 SSH 連線設定無法非互動使用，沒有取得供應商／主機端產出或計費證據。後續先從已存音檔重建時間軸及正常檢查，再依新 dry-run 選出的四句做一次有界重錄；持續被標的 63kr 經上述一次聽眾改寫，單句重新合成。502 的供應商結果與費用仍不確定，不宣稱未計費或找回未知產出。

保存的成功語音 POST 合計 154 次、2,800 計費字，另有一次結果不確定的失敗 POST；此統計不是費用帳單。最終正常語音檢查 137/137 通過、零被標：60 exact、40 同音／語助、10 Jev、27 第二意見。正常 audio review-push／pull 於 2026-10-02T14:29:08.671Z 保存核准。

實際句音檔純講述合計 **533.270 秒（8:53.27）**，247.6419 口語單位／分。正常正文時間軸 **20,197 frames／673.233333 秒（11:13.23）**。獨立重建時間軸與原始旁白 PCM 雜湊相符；137 個連續畫面狀態最長 6.8 秒、平均 4.914112 秒，圖解佔正文 94.756647%。正文首句於 5.266667 秒完成，17.2% 答案於 15.2 秒完成；第一章總長 88.533333 秒的 lint 警告保留，lint 零錯誤。

純講述、正文與實際成片各超過 480 秒，沒有用片頭片尾、重複、慢播或長停頓補足。這些是實測，不是企劃目標。

## 原創畫面及書擋

130 個原創 SVG、93 種語義模式、相鄰重複零；正常 renderer 輸出 137 個畫面狀態。素材作者完成全圖前檢，另一位審稿者實看全部 137 張正常 PNG、23 頁聯絡表及重要畫面原尺寸。

三項發現已閉環：c2-s06 用「算一人」避免暗示保留身分資料；c4-s08 只勾選網路、垃圾桶不勾選，突出「其他困擾」；c5-s14 加上公里單位及密度公式。正常 renderer 重製三張、重用 134 張；審稿者重看三張原尺寸、相關聯絡表及縮圖。最後單句口播改寫不改畫面，正常 renderer 再全數重用。

- art manifest SHA256：`260ed6f4a37ce2199e8ef563fc0de0b4d92bd3368b67b89d5d4809927b538bda`
- frames manifest SHA256：`114792f08efeac08ec723ef8d6fa67808066ca6b243b76482559af50ac8e2462`

首次正常 assemble exit 0，正文 20,197 frames、-14 LUFS、true peak -0.9 dBFS，137/137 segments 編碼完成。該次沒有書擋，因本機 channel current registry 及舊安裝資產已不存在。無書擋版本及 checks、state、timeline、narration 按檔案與雜湊保存在 `_history/unbranded-first-assembly/`；其 final SHA256 `ee61d35e59cd381ca741749dc89c775859529deaaa14e2bc194b15874aa653f7`，不是最終交付版本。

已核對站主核准的 `mokaair-sothatswhy-bookends-v1` 實際位元組、幀數及完整音畫解碼：hash `047ff12a4888185d8fb1cb0cd520f7a2e23b9c3538fe3f2e8d4cb35afb0720bb`；intro 357 frames／11.9 秒、outro 90 frames／3 秒。片頭包括原有 Mokaair CC 提醒及系列片頭，沒有重複加原始五秒。系列段落依站主選用的固定版本穿插 14 個國家／地區的品牌字卡及聲音，最後落在「原來如此」；English／美國字卡是其中一張，不是本集配音或字幕語系標示，也沒有為本集重新合成額外語言。核准收據是系列素材選擇，不等於本集完整播放或上傳核准。

T27 為 slides，正常 series default 只匹配 drama explainer；本集使用 repo 外私有 work base 的 `_branding/current.json` 保存驗證後的絕對素材路徑，唯一 sothatswhy-t27 junction 經 realpath 核對指向真正的本集媒體。正常 `assemble --adopt-branding` 採用這個選擇，在檢查成功後才原子替換成片、正文、pin、checks。全域 registry、來源 format、T26 及其他影片沒有修改；原 work base STOP 檢查保留。全部 137 段正文畫面重用，正常工具重做音訊處理及封裝，沒有重合成 WAV；新 body 的雜湊按實際位元組獨立量測，不以首輪雜湊代替。

## 最終交付與後台讀回

含已核准系列書擋的正常成片已完成，實際解碼 20,644 frames；容器時長 688.200000 秒、video 688.200000 秒、audio 688.200000 秒（約 11:28）。1920×1080 H.264／AAC。正常 assemble、11 項 QA、4 項上架包檢查均通過；outline、audio、final、publish 四個正常關卡的核准均綁定當前檔案。

最終 final.mp4 SHA256：`3894c35e2cd5860d0b834c1ba02578986600c15e1e4ce53d59d0b95f1e993016`；upload metadata SHA256：`0b391df71413e3ea5ef4307b4984d332dd81174e43af5fc98b92e4ed0abe79d3`。正常字幕有 137 cues，SRT／VTT 與 current presentation timeline 逐位元組相符，正文字幕偏移 11.9 秒，章節重新計算並保留零秒第一章。正文與 final 的六個取樣波形比對全部 correlation >0.98，偏移誤差不超過 1/6000 秒；全部畫面狀態另按實際封包 PTS 核對，詳見 runtime-audit。

實際 final 解碼取樣 15 張（13 張正文含六章及重要圖解、片頭、片尾），由協調者及另一位視覺審稿者實看，零未解決發現。另一位覆核者完整解碼全部音畫，按實際 final 雜湊核對幀數與正常 QA／核准／上架包；不是只看 JSON 宣告。相關收據為 visual-review、runtime-audit、final-runtime-review。

正常 review-push／pull 已把本集 720p 預覽、完整成片及上架包送至同集後台，再以 GET 讀回。final review ID：`cab3a243-7d28-433e-bca1-a0a4de07e247`；publish review ID：`2922dac4-fd3a-438c-9614-128ddadd1cc2`；附件 final 的 SHA256 與本機完整成片相同。讀回時間 2026-10-02T15:52:00.323Z，sanitized receipt 保存在 delivery-proof.json。YouTube ID 仍 null、on_youtube=false，ready_to_upload=false；每集語言決定仍 pending，不宣稱可自動上傳或站主已完整播放。

後台：<https://mokaair.com/zh-TW/admin/videos?video=sothatswhy-t27>。實際媒體、字幕與 upload 目錄保存在上述 repo 外單集目錄；本次沒有上傳 YouTube。

## 驗證與權限界線

最後在本次製作使用的 bundled Node 24.19 執行 `npm run test:tools`，共 1,247 項：1,244 通過、3 skip、0 fail。最新 series branding main 更新後的 core／installer／assembly branding 三支測試另有 19 項全通過。系統 Node 24.13 的第一次 final tools run 發生檔案層級失敗；單獨重現 gemini.test.mjs 得到原生 exitCode 3221226505，改用 bundled Node 同支六項通過，再跑完整套件通過。原始失敗及成功日誌均保存，沒有為此修改來源、媒體或系統 Node。`check:tasks` 驗證 1,300 份票，僅既存其他票的 warning；最後 staged diff 另檢查。

來源位於 managed worktree sothatswhy-t27，branch codex/sothatswhy-t27-pilot，安全接到 main `acb935fb461e34ee110b725b742179cc22d67770`。Git 只收本集腳本、原創 SVG 與雜湊綁定的文字收據；媒體保存在 `<home>/mokaair-work/videos/sothatswhy-t27/`。完成實際媒體、正常核准及全部獨立覆核後才建立草稿 PR。

沒有修改全域語言、圖片、預算或 uploader 設定；沒有重啟 worker、合併、部署、上傳或公開。機械檢查、抽樣視覺覆核及後台附件可讀回，與站主實際聽音、完整播放、字幕播放器驗收及 YouTube 上架是不同證據。每集額外語言／只出繁中的選擇仍由站主決定；正常讀回的 locales 為空、決定時間為 null，沒有偽造勾選。
