# B18 迴轉壽司｜正式製作前準備

審查證據的本機路徑已依 [2026-10-16 路徑遮蔽紀錄](evidence-path-redaction-20261016.md)處理；原始與公開版 SHA 分列，不變更 A01/B18 旁白或原審查結論。

這裡保存免費完成的分鏡與工人企劃候選，尚未匯入或產生配音、插畫、成片。

## 分鏡

[完整分鏡](B18-storyboard/storyboard.md)有 103 鏡：87 個插畫位置、16 張數字或來源卡，預計使用 82 個不同圖片。獨立覆核讀過全部鏡頭，並從文字切片逐字重建凍結稿的 24 段、2,729 計數單位。三組片頭提問與正文回收的 prompt、camera、asset key 相同；尾聲三句規劃共用一張已驗收圖片。真正生成後的檔案雜湊仍待綁定。

[獨立分鏡覆核](B18-storyboard/independent-review.json)確認編輯準備可繼續。作者原始檔案與雜湊原樣保存，包含當時「待獨立覆核」的文字；最新結果以這份獨立覆核為準。

## 開場企劃候選

[B18 候選](B18-worker-hook-candidate/B18.json)僅變更第一章 `point`，把三個提問對齊凍結稿 H02。原 row、原收據與[新獨立收據](B18-worker-hook-candidate/reviews/B18.json)分開保存；官方 `storyProblems` 和 `reviewProblems` 均為零。雜湊依正式 builder 的 `STORY_KEYS` 投影計算，完整 episode row 的 hash 不能代替這個審稿綁定。

原 worker row 候選尚未替換 `episodes/B18.json`、重編 `stories.json` 或變更主機 A01；它的其餘五章仍是企劃摘要。另有隔離的六章作者候選如下，兩者不可混成已匯入狀態。

[B18 約 10 分鐘離線口播縮稿候選 v1](B18-10min-narration-candidate/README.md)將凍結稿 2,729 units 縮為 2,293 units；獨立審查指出 O01 年份指代與 T01 排他措辭需修。[隔離的 v2](B18-10min-narration-candidate-v2/README.md)僅改這兩段，獨立文字複審已通過；TTS、正式 worker 章稿與整片敘事審稿仍待完成。

[B18 六章轉換計畫](B18-worker-conversion-plan/README.md)將 v2 的 24 段對到舊 103 鏡及 65 個待查子主張，列明卡片、來源疊字、共圖和作者章稿採用入口的缺口。[隔離的六章作者候選](B18-authored-chapters-candidate/README.md)現已完整寫出 99 句、96 鏡；獨立[離線覆核](B18-authored-independent-review-20261016.md)對 37 個檔案與段落、claim、原卡片的結構核對為有限 PASS。65 項主張仍全部未查，真敘事、worker 採用與媒體均為 HOLD。[草稿 PR #1518 的唯讀審查](B18-author-adoption-independent-review-20261016.md)另找到採用後 series 漂移可進付費查核、空 claim 可被視為查完、共圖未綁定實際圖片及 title 來源卡可在 checker patch 後消失；該 PR 為 HOLD。正式採用須由既有認領者修復並重審，不能把一般企劃匯入當成保留這份縮稿。

[B18 原生字卡手機尺寸前檢](B18-authored-mobile-card-qa-20261016.md)實際輸出全部 19 張：渲染錯誤為零，但 `idea-s027` 的三行來源副標在 320×180 過小。[隔離單卡修訂候選](B18-mobile-card-revision-candidate/README.md)已將重複來源的副標收成一行，保留主標／徽章中的兩個來源名並重新渲染；[獨立審查](B18-mobile-card-revision-candidate/independent-review-20261016.md)對該張靜態卡給予限定 PASS，正式採用與整片播放仍待辦。

[A01 第十輪離線候選與畫面稽核](A01-round10-candidate/README.md)保存第九輪真實 FAIL、兩句加一項 claim 的可逆修稿。[獨立審查](A01-round10-independent-review/README.md)只肯定限定史實與局部銜接，整體為 HOLD；四處聲畫錯位仍 FAIL，尚未有新一輪正式敘事 PASS。

[A01 第十一輪隔離畫面候選](A01-round11-candidate/README.md)只改六個鏡頭提示詞；[獨立文字覆核](A01-round11-independent-review/README.md)確認新描述對上旁白和相鄰動作。尚無 MiniMax 圖像驗收或正式敘事 PASS，不能將提示詞覆核當成成片通過。

[A01 第十一輪離線安裝交易候選](A01-round11-offline-install/README.md)以六章原檔、九處精確差異、專屬 STOP、狀態及帳本證據做本機 fixture 故障測試。它不是正式主機適配程式或上線核准；第九輪真實 FAIL 與付費媒體禁行仍在。

## 下一步與限制

- 把隔離作者候選接到受審的 worker 採用路徑；逐章查核、順稿及整片敘事審查都要在正式輸出重做。
- 目前六章候選的工具預設估時是正文 647.4 秒，加 26 秒片頭片尾為 11:13.4；尚未實錄，須以真實聲音與編輯判斷確認約 10 分鐘目標，不靠空白或強制變速湊長度。
- 產圖後確認共圖檔案、後製來源標示、片頭片尾資產，以及可關閉繁中 CC。
- 先完成 A01 試作看片；B18 付費製作仍待整片上限核准與相符的逐片預算約束。原 v3 報價仍以 91 張圖保守估計，未因本次 82 個計畫圖片而變更報價或授權。
- 成片播放、站主驗收、外語勾選與上傳分別處理。

所有整合檔案的原始位元組與雜湊列於 [integration.json](integration.json)。
