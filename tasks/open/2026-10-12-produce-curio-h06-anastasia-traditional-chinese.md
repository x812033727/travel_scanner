---
id: 2026-10-12-produce-curio-h06-anastasia-traditional-chinese
title: Produce Curio H06 Anastasia Traditional Chinese episode
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-curio-h06
claimed_at: 2026-10-12T13:51:16Z
created_at: 2026-10-12T13:51:10Z
completed_at:
branch: codex/curio-h06-production-20261012
depends_on: []
scope:
  - docs/videos/curio-h06
  - docs/videos/history-curiosity/topics.json
---

# Produce Curio H06 Anastasia Traditional Chinese episode

## Why

H06 是奇聞檔案局已查核題庫中、H05 之後的下一支影片。1920 年在柏林出現的安娜・安德森被認作可能倖存的俄國公主安娜塔西亞，但 1970 年法院判決、1995 年檢體比對與 2009 年兩座墓的研究回答的是不同問題。觀眾需要一支只出繁體中文、能看著原始文件分辨「沒有證明是公主」「DNA 排除皇室血緣」「五名子女都在兩座墓中」及各自界線的影片。H05 及五支舊片重製已有別的工作者，本票僅處理 H06。

## Definition of done

- [x] 站主或正式站依既有大綱流程選定一案，該選擇與任何人工核准有可讀回紀錄。
- [x] 繁體中文史料查核、口播稿、旁白、插圖／來源卡、可關閉 CC、成片及上傳包完成；正文和成片實測各至少 8 分鐘。
- [x] 1970 年判決沒有替安德森肯定指定另一身分；1995 年檢體研究的可讀證據限制；2009 年兩篇原始論文對全家與姊妹個別身分的不同結論，均有逐句來源與獨立覆核。
- [ ] 自動音畫、字幕、來源與權利檢查通過，真人播放／聽音與上傳、公開狀態分別留證；未完成者明記為未完成。

## Steps

- [x] 查 H05 與舊片重製的在途所有權，從已查核 H06 題卡接題，建立獨立工作樹與窄範圍認領。
- [x] 重新核對可直接讀取的 2009 年 PLOS ONE、PNAS 原論文與 1970 年判決索引，記錄法院轉錄 403、1995 年論文付費牆的證據限制。
- [x] 寫繁中 brief、三個不同敘事大綱及研究／主張清單，列出來源閱讀示範、插圖與照片權利邊界。
- [x] 讀回正式站頻道立場設定，將適用編號 2、4、6、7、9 與來源判讀示範寫進 brief。
- [x] 核對立場原文、跑大綱檢查與原生送審流程；選定方向後才進入撰稿與付費製作。
- [x] 寫完整口播稿，逐句核對來源並完成獨立史實與說書檢查；核定分鏡、時間軸、素材清單和可審成本。
- [x] 按已核定方案製作繁中音訊、畫面、字幕與成片；逐項核對實際檔案、播放、片長、授權和上傳包。
- [ ] 依站主對成片和發布的授權完成交付，回填 topics.json 與證據，不把本地 READY 當成已上傳或公開。

## How to verify

- 規劃階段：讀 `docs/videos/curio-h06/brief.md`、`research.md`、`claims.md`，比對 `docs/videos/history-curiosity/topic-checks/H06.md`、列出的原始論文和判決索引；執行 `git diff --check`、`npm run test:docs-videos`、`npm run check:tasks`。
- 製作階段：以既有 `youtube-video` 流程的 planner／script／verification 檢查和媒體 QA 輸出為準；對照旁白與 CC 的時間戳，驗證正文和成片片長。
- 交付階段：分別讀回實際媒體、字幕、來源授權、上傳狀態；站主聽音與播放紀錄應和自動檢查分開。

## Notes

2026-10-12：本票在 `codex/curio-h06-production-20261012`、`curio-h06-anastasia` 工作樹中認領。H05 D.B. Cooper 仍有獨立在途工作，五支已發影片重製亦有獨立範圍；勿改其檔案。

企劃先沿 H06 獨立覆核的 `ADOPT_WITH_CHANGES` 題卡。選項 A 是安德森人物線接法院與兩座墓；B 是傳說形成；C 是從第二墓倒敘兩種 DNA 問題。三案目前皆只是草案，沒有本集選案、旁白、圖片、成片或發布。只預設繁體中文，其他語言須另有站主選擇。

可直接讀全文的 PLOS ONE 2009 論文指出第二墓的一名女兒無法僅據其報告的 DNA 分為瑪麗亞或安娜塔西亞；PNAS 2009 論文支持五名子女皆已找到。1970 年 BGH 判決由第三方轉錄，2026-10-12 網頁讀取限制為 403，須標「判決轉錄」並在成片引用前核對。1995 年 Nature Genetics 全文受付費牆限制；不得把書目或二手說明當成親讀全文，更不得說百分之百個人鑑定。

安德森 1984 年去世，只用無臉背影／剪影，不用生圖重建其肖像。真人照候選要逐張核授權；拒用來源不明的 mugshot、伊帕切夫宅照和任何遺骸影像。2026-10-12 製作端讀到的正式站立場已填，auto_pick_outline=true 且啟用插圖投影片；brief 標示適用立場 2、4、6、7、9，正式送審前仍要讀回原文核對。沒有在本步觸發任何付費媒體或正式站狀態變更。

企劃檢查：`npm run check:tasks` 通過（只有既有票過期警告）；brief 的八個頂層章節與 planner 規定順序相符。`npm run test:docs-videos` 為 116／121 通過，五個其他系列測試因這個新工作樹尚未安裝 `pinyin-pro` 而無法載入，並非 H06 文字驗證失敗。為避免在 C 槽新建大體積 `node_modules`，企劃階段沒有執行 `npm ci`；正式製作前需在可用依賴環境重跑。

2026-10-12 製作更新：已在獨立工作樹接上現有依賴，以 bundled Node 24.19 跑 `test:docs-videos`，199／199 通過；`check:tasks` 通過。原判決掃描已取得並目視核對（訴請在 PDF 第 13 頁）；兩輪獨立史實覆核、聽眾修稿與最新稿 `lint` 均通過。正式站 Jev 選 A，立場 0.91、示範 0.83、建議 0.02，自動核准並由 `review-pull` 讀回。最新 `tts --dry-run` 預估 2,587 計費字元；`keyframes --dry-run` 為 76 張插圖、首輪約 US$1.03。繁中 TTS 已啟動，尚未記為完成。

2026-10-13：旁白 137 句已合成；兩輪目標修稿後，逐句檢查為 102 句逐字相符、34 句同音或語助詞差異，最後 1 句由獨立 Whisper 轉寫確認原稿實際有唸出。零旗標後，音訊關卡由正式站自動核准並讀回。畫面改成 71 張插圖、5 張具權利紀錄的歷史照片和 30 張原生卡。第一批圖的人工檢視抓到三個自動評分漏掉的問題（1920 場景出現秋葉與後來才有的地標、樣本盒畫成植物箱）；已停批、收窄提示詞後續跑，仍須檢查新圖和成片。影片說明中的四條 403 連結已改為可讀的原判決／NIH 論文全文／館藏鏡像入口，來源與授權標記保留。

2026-10-13 圖像續跑保存點：`mokaair-work/videos/curio-h06/STOP` 現存，第二輪新生成 27 張後停下；`keyframes/manifest.json` 已選到 `grave-map-table`，後面仍未完成。人工像素審查發現自動判分漏掉的假 EXIT、法庭旗幟、中央本應留白卻放卡、透明檢體盒、人偶木標和地圖假字。已只改這些鏡位的 `video.json` prompt，待 C 槽空間恢復時從 manifest 重用未變鏡位；`hospital-room-two-voices` 僅畫風評分未過、內容可用，之後按流程記錄是否保留。Windows 分頁檔擴張令 C 槽一度只剩約 2.7 GB，尚未渲染、合成、製字幕、製上傳包或上傳 YouTube。

2026-10-13 分鏡完成並送審：L08/H01 冗餘素材與五支重剪的重複本機封存檔經 VPS 逐檔驗證後精確清除，C 槽恢復可製片空間；`STOP` 已撤除。全片改為 65 個插畫鏡頭、5 張已核權歷史照片、36 張原生卡。新生成鏡位逐張人工審看；有假路牌、透明檢體、錯誤家譜或錯誤地圖的鏡位改用原生卡，僅留下語意安全且不誤示來源的圖。`hospital-room-two-voices`、`end-archive-desk`、`end-canal-return` 三張以 `keyframes --accept-best` 保留完整評語，強制成片人工審看。最新 `lint` 0 錯 0 警告；`review-push --gate storyboard` 已送正式站，`review-pull` 目前仍待站主核准，故尚未渲染、合成、製字幕或上傳。一般系統 Node 24.13 的 199 項測試有 1 項子程序無輸出崩潰；同一 44 項檔案測試在 bundled Node 24.19 為 44／44 通過，還要以 bundled Node 重跑全套。

2026-10-13 驗證補記：改用 bundled Node 24.19 重跑完整 `docs/videos/*.test.mjs` 與 `docs/videos/**/!(demo)/*.test.mjs`，199／199 通過；`git diff --check` 與 `npm run check:tasks` 也通過。正式站 `https://mokaair.com/zh-TW/admin/videos?video=curio-h06` 可讀回 65 鏡、3 鏡保留和「核准分鏡」待決定；沒有把送審當作核准。

2026-10-13 分鏡二次人工審圖：三頁聯絡表逐張複核後，`dna-hair-and-box` 把毛髮／組織畫得像昆蟲，`relatives-day-room` 把安德森的成年親屬畫成小孩，`berlin-staff-corridor` 出現近代護士制服與紅十字帽；三者都可能誤導史實，改用原生資料卡。原圖、判分與退役前的 manifest 留在工作目錄 `keyframes/`，特別是 `retired-shots-before-card-replacement-20261013.json`，不把自動評分當人工通過。

為維持有畫面解說的節奏，依既有旁白把 `relatives-disagreement`、`relatives-legal-question`、`grave-2007-path`、`grave-family-board` 四個低風險卡窗改成沒有臉、文字或史實標記的象徵插畫，逐張讀回像素；法庭資料夾初稿有假旗幟／肖像，重畫後才保留。`grave-data-overlap` 兩版畫錯資料件數、`grave-fragments-limit` 兩版盒子出現虛構標記／愛心，皆退回原生資料卡，失敗圖與判分 manifest 另存 `before-data-overlap-retirement-20261013.json`、`before-fragments-retirement-20261013.json`；不再為比例增加付費生成。最終 `video.json` 為 66 插畫、5 史照、35 原生卡。旁白時間軸 19,567 格內插畫覆蓋 9,888 格，即 50.5341%；正式 `pace` 用旁白正文時間軸，不把品牌片段加入分母。`lint` 0 錯 0 警告，`keyframes` 重綁時 66 張沿用評語、0 張新生圖，媒體帳本仍為 US$2.45；三張原有 `accept-best` 的人工待看標記保留。新分鏡尚待重新送審與站主核准，成片尚未製作。

2026-10-13 02:55（台灣）：新版 `review-push --gate storyboard` 成功送出正式站待審；隨後 `review-pull --gate storyboard` 讀回「waiting for the owner」，`status` 顯示 66 張關鍵影格已完成、分鏡仍未核准，未進行 render／assemble。新分鏡修改後 `test:docs-videos` 在 bundled Node 24.19 為 199／199，`check:tasks` 通過（只有其他票的既有逾期提醒），`git diff --check` 通過。舊分鏡審核答案不能套用新版。

2026-10-13 備份與關卡讀回：H06 工作目錄、`docs/videos/curio-h06` 與本任務檔的渲染前快照共 365 檔／173,473,550 B，已直接串流至 VPS `/var/backups/curio-video/20261013-h06-prerender/curio-h06-prerender.tar.gz`；壓縮檔、全部逐檔 SHA 與獨立讀回均通過，收據在 `mokaair-work/backup-receipts/h06-prerender-stream-verified-20261013.json`。來源保留供後續製片。三張 `accept-best` 選用圖再次以像素目視核對，未新增史實誤導點；成片仍須再看。最新正式站 `review-pull --gate storyboard` 仍回覆「waiting for the owner」，沒有渲染、合成、字幕、上傳包或 YouTube 上傳。

2026-10-13 成片待審：站主核准新版 66 張插畫分鏡，正式站讀回舊 65 鏡送審已被取代。渲染後 68 個原生／照片畫面狀態無排版或缺字問題；縮圖已改掉尾端孤字。兩處超過 8 秒的畫面經三句目標重錄修正，137／137 句音訊檢查零旗標，重新合成只重編 2／106 段。繁中成片 19,709 格、10:56.97、-14 LUFS、137 條可關閉字幕；自動品管 11／11 通過，聯絡表及四個實際成片時點已目視抽查。正式站 720p 預覽與品管報告已送達，但因 `hospital-room-two-voices`、`end-archive-desk`、`end-canal-return` 三張保留插圖，成片關卡仍為「待決定／需站主審看」。已向站主提供審核頁及 02:55、10:20、10:44 時點；尚無成片核准、上傳包、最終差量 VPS 備份或 YouTube 上傳。渲染前快照已備份；最終差量備份腳本備妥，待成片核准、上傳包及文件凍結後才執行。

2026-10-13 成片核准與上傳包：站主在正式站核准 66 張插畫的 10:57 繁中成片，並選「只出繁體中文」。最後 `final.mp4` SHA-256 為 `9a34efba5583956e76ad184aad244b991040d3eb31432f0e9e1528e6a941d8d3`；11／11 自動品管通過，137 條可關閉繁中 CC、5 張史照的授權與來源逐張核對。上傳包包含 MP4、縮圖、繁中說明與 SRT，4／4 檢查通過。片尾 10:44 保留圖看似實拍，故人工將上傳包 AI 合成內容申報改為「是」並寫明原因；QA 的原始自動判斷仍保留作歷史紀錄。舊申報為「否」的上傳包核准已由新版取代，正式站讀回新版 metadata SHA-256 `cfeff3eecb5dffc968fa5c1a80d8f0dcf0e714f483c090c59461b3b1c1ad0451` 已核准。沒有 H06 YouTube 影片 ID，也沒有上傳或公開紀錄；交付與備份的收據分別在工作目錄及 `mokaair-work/backup-receipts`。

2026-10-13 VPS 最終增量備份：將已核准成片、繁中上傳包、正式站審核紀錄、來源文件與本任務檔 44 個檔案（原始 387,515,852 B）串流至 `/var/backups/curio-video/20261013-h06-final/curio-h06-final-delta.tar.gz`，並以獨立讀回逐檔驗證；壓縮檔 SHA-256 `f17f2d20268b35a7dc34846f439d86c318d548a896d6ca08c5f2fbd7f42a2523`。本機收據為 `mokaair-work/backup-receipts/h06-final-delta-stream-verified-20261013.json`，依賴先前已驗證的渲染前快照。C 槽現役來源和上傳檔保留，未清除；H06 仍無 YouTube 上傳／公開證據，本票維持進行中。
