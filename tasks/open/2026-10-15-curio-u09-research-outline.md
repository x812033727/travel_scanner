---
id: 2026-10-15-curio-u09-research-outline
title: Curio U09 research outline
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-u09-final
claimed_at: 2026-10-16T09:51:47Z
created_at: 2026-10-15T16:35:08Z
completed_at:
branch: codex/curio-next-five-20261016
depends_on: []
scope:
  - docs/videos/curio-u09
---

# Curio U09 research outline

## Why

使用者要求接續製作五集奇聞檔案局，U09 為其中一集。將既有題庫線索重新查核成可以讓站主選擇的獨立大綱，避免把 LGM 玩笑代稱寫成外星宣告，或將 1968 年兩階段解釋混成一次定案。

## Definition of done

- [x] 研究、主張界線與 A／B 大綱落地在 docs/videos/curio-u09。
- [x] 主要第一手資料重新開啟，記錄成功與受限來源。
- [x] 未參與撰稿者獨立覆核後可供站主選大綱。
- [x] 站主選擇 A／B 並完成本批費用授權後，交接後續正式稿製作。
- [x] 依核准 A 案完成正式稿、video.json、逐句證據與 loops，通過本機 lint。
- [x] 正式稿獨立史料覆核、十三題盲評與站主劇本核准；媒體製作另按關卡接續。

## Steps

- [x] 讀系列 skill、故事／開場／十三題規則及 H01-v2 前 30 景。
- [x] 查任務／分支／PR scope 無碰撞後認領。
- [x] 重讀 Bell 訪談、Hewish Nobel 演講與首篇 Nature 原件。
- [x] 寫 research.md、claims.md、brief.md，將三個開場鉤子對應後文回收。
- [x] 接收獨立覆核並修正開場長度與來源讀取範圍。
- [x] 協調者手動送審 outline 並讀回 pending；記錄 review ID 與 brief 雜湊。
- [x] 主代理讀回站主已選原案 A，且每集 US$6／五集 US$30 上限已獲授權。
- [x] 再認領原票展開正式稿，未新建重疊 scope；102 句與 14 loops 已建立。
- [x] 修正分鏡多樣性與情緒 cue；本機 lint 0 errors／0 warnings。
- [x] 補格式新版 brief 由主代理重新送審並讀回核准，再送劇本。

## How to verify

對照 research.md 的來源開啟狀態及 claims.md C01–C31。用獨立讀者檢查 1967 年初始記錄／快紀錄、LGM、1968 年振盪／旋轉的分界；核對 brief.md 有 A／B、7 章約 600 秒與三個開場 loops。正式稿另跑 `node tools/video/cli.mjs lint --slug curio-u09`，檢查 script.md 與 screenplay(video.json) 一致；`npm run check:tasks`、`git diff --check`。每輪退修後由未讀過該稿的新盲評者重讀，不自行標記通過。

## Notes

- 2026-10-16（Asia/Taipei）：舊題庫分支只讀；本集 scope 獨立，未改共享檔。
- Cambridge／Churchill／Nobel 網頁瀏覽工具有 403；規定 UA 直接 GET 讀到正式原頁／PDF，已清楚記錄。Nature 出版頁回登入中轉，不當成功；Hewish/Bell 1968 原件由 Cornell 學術鏡像取得並逐頁查看相關頁。
- 初稿階段原撰稿者只取得 Gold 1968 出版方索引摘要。獨立覆核者其後親自視讀 UBC 學術鏡像印頁 731–732；research S06 已補網址、讀取者、頁數與 SHA-256，claims 同步來源範圍，主張不變。
- 推薦 A 集中在訊號來源調查，B 集中在紙帶辨認；兩案均不岔進 Nobel 爭議。
- 近代人物不生成本人容貌；未建立正式劇本／video.json，未呼叫付費服務。本代理未 commit／push；由主代理統一整理 commit／PR。
- 本輪檢查：`npm run check:tasks` 通過（1895 個任務檔；既存過期／重疊警告）；`git diff --check` 通過。內容為新檔，正式稿 lint／盲評均未跑，不能以此視為故事關卡已過。
- 協調者初讀後，A／B 最後一章各從前章挪入 15 秒，保留 60 秒解釋旋轉波束及結尾；候選模型不另開定義段。費用段已連共同提案 US$6／集、五集 US$30（未授權）。
- 獨立覆核者 `curio_five_inventory` 重開 Cambridge、Bell 重刊、Nobel，視讀 2 月原論文 p.709／713 與 Gold 5 月原文 p.731–732，確認 LGM 玩笑代稱、振盪／自轉兩階段界線。開場修為 A 170 字元／150 中文字、B 163／145，約 38／36 秒正文加停頓預算 45 秒；A 欄與分段表相符、三事件保留結果。讀回後給予大綱層級通過，無剩餘阻擋項；不是正式劇本十三題盲評通過。
- 2026-10-16 01:01（Asia/Taipei），主代理回報 U09 outline 手動送審成功並讀回 `pending`；review ID `31269f8b-3ca6-4d62-987e-62acedc34e3b`，對應 brief SHA-256 `E268DE743CECA8CDB0EF6846AC893D8F2F0422C1F4E30CE6A6200003B8149D79`。已送審 brief 保持不變；未啟動付費或 worker 製作。
- 交接完成後釋出認領，任務保留 open：待站主選 A／B，並另行核准共同提案每集 US$6、五集 US$30 的估算停手上限。費用尚未授權，不是供應商硬上限，不沿用 H09 額度；核准後才按正式稿與媒體關卡繼續。

### 正式稿續作：2026-10-16

- 以上是先前送審交接快照。站主其後已核准五集 A 與每集 US$6／整批 US$30 上限，主代理已讀回原 outline review 的核准與 exact brief SHA。
- 以 owner `codex-curio-u09-script` 重新 claim 同票，正式稿落在 `video.json`、`script.md`、`script-evidence.md`、`loops.md`；研究與 claims 同步新增的 C25–C31。
- 101 景、91 插圖、9 內容卡、1 outro；102 句，2,067 口播單位；正文預估 605.57 秒，開場 45.93 秒。均為文字估時，未合成音訊。
- `node tools/video/cli.mjs lint --slug curio-u09` 通過：0 errors／0 warnings。情緒 cue、圖面變化與開場／回收 prompt 已整理，沒有更動共享程式或規則。
- 已核准 brief 缺現行 lint 要求的三個精確節標；依主代理指示，只在大綱前從既有內容提取問題／一句答案／站主觀點。A／B 選項正文未改。原 SHA `E268DE743CECA8CDB0EF6846AC893D8F2F0422C1F4E30CE6A6200003B8149D79`；新 SHA `0C6A058D0ED1BB5A8C2B42275275523F3A5BB19FE53C78E82B7F499F4B82C6D2`。由主代理重新送新版大綱，核准後才可送劇本／付費。
- 本輪沒有付費呼叫、媒體生成、後台送稿或 push。正式稿的獨立史料覆核、十三題盲評仍待執行；詳見 `docs/videos/curio-u09/script-status.md`。
- 本輪 schema／逐句索引／script 同步檢查均通過；`check:tasks` 通過 1895 份，僅既存過期／重疊警告。依主代理要求，只將本集 docs 與本票作本機 commit，認領維持供修訂接續。
- 主代理補充指示後，brief 選項外的舊狀態改為原案 A 已核准、每集 US$6 已授權，並連至批次 `decision-20261016.json`。A／B 主文保持原字；最終送審用 brief SHA 為 `6C4C27F3DB3EFF2106241AF15A7C69499E6070436D4061150530481F1BFBBEC9`，取代上一則只補三節時的中間 hash；lint 仍為 0 errors／0 warnings。
- 獨立十三題首輪必答 11／12，第 7 題退回兩個未兌現問題。僅修 `05002227` 為問快紀錄器能否捕捉、`7a031219` 為問是否還有更多同類；答案 `718638d1`／`9410e2e4` 的史實未改，沒有編造先前未捕捉原因。video／script／claims／逐句索引／loops 已同步，估時 604.60 秒、2,063 口播單位，lint 0 errors／0 warnings。新 video SHA `F5E73534B79611735B95D5C464D6FF367FEE7DD99C3422ED5531B9760A6C2625`；script SHA `D11BFC548632769AE8E42122712A3F882A997C4D6704C48531AB111C1BAF22AD`。待獨立讀回，不視為已通過。
- 第二位盲評者仍判第 7 題未過；本輪僅改 `2a37c45e`，明確回扣 `f58aba8f` 的「會不會有人發射」，以後續證據支持自轉中子星／波束掃過地球作答案。完整 loop 從中段 `742fe66c` 移到此句，中段限制假說的原文保留；C22／C23、稿件、loops、逐句索引同步。2,076 口播單位、估時 607.73 秒；lint 0 errors／0 warnings。video SHA `CCD845B56DAE53A5828DFD1B93881D273E8BDA963D74B61327F074ACAC9FE50D`；script SHA `A6EBACD14E9986B8422316ABAEC6178FF039D063F31FE33A1A01D14233AF3F5A`。brief 未改，無付費／後台／push；須由未讀過此稿的新盲評者重讀，任務持續認領。
- 2026-10-16 獨立重讀交接：主代理回報第二輪修訂版通過嚴格的 script-only 新盲評，必答 12／12、全部 13／13 yes，綁定 video SHA `CCD845B56DAE53A5828DFD1B93881D273E8BDA963D74B61327F074ACAC9FE50D`。答案檔已讀取：`<home>/mokaair-work/videos/curio-next-five-20261016/review/blind-curio-u09-strict.json`；第 7 題明列 `f58aba8f` 由 `2a37c45e` 回收。這是敘事盲評通過，不代替史料查核或站主劇本核准。
- 依主代理指示釋出作者認領，任務維持 open，交由獨立史料查核者認領並撰寫 `docs/videos/curio-u09/verify-1.md`。本次只更新任務交接，不改任何稿件、brief 或媒體；沒有付費／後台／push。
- 2026-10-16 獨立史料覆核讀回：正式稿仍綁定 `video.json` SHA `CCD845B56DAE53A5828DFD1B93881D273E8BDA963D74B61327F074ACAC9FE50D`；`verify-1.md` 對 C01–C31、所有內容卡、縮圖與後台文案逐項核查，31 項主張確認、0 項事實改動／阻斷。原 1968 年 2 月 Nature 論文印頁 709、713 本輪重新視讀，Gold 原文及 Bell／Hewish 回憶也已核對。現版 lint 0 errors／0 warnings；`narrative --answers` 收據 13 題全過。仍待劇本送後台及站主核准；沒有付費製作。
- 主代理隨後執行 `script --slug curio-u09`，生成稿 SHA `A6EBACD14E9986B8422316ABAEC6178FF039D063F31FE33A1A01D14233AF3F5A`；`review-push --gate script` 成功，`review-pull --gate script` 讀回 `waiting for the owner`。正式劇本已送後台待站主核准，未啟動任何付費媒體製作。

### 繁中旁白續作：2026-10-16

- 站主在後台核准正式劇本，主代理以 `review-pull --gate script` 讀回 `approval recorded` 後才啟動付費製作。先以 `tts --dry-run` 核對 101 次 Gemini Sulafat 合成請求／2,332 計費字元、`keyframes --dry-run` 核對 91 張 image-01 插圖；圖像尚未生成。
- 外部估算停手帳本先預留 US$0.20 再合成繁中旁白；實得 102 句 WAV、正文 590 秒（9:50）、2,332 計費字元，無供應商 hold。此 US$0.20 為保守估算，不是供應商最終美元發票。
- 再預留 US$0.50 執行 `check-audio`：102／102 句完成 Gemini 轉寫，1 次 TypeSafe Jev 差異判讀；58 句逐字吻合、25 句同音／語助詞、2 句 Jev 接受、17 句品質旗標。工具因旗標 exit 1，並非服務失敗。估算支出合計 US$0.70，仍在本集 US$6 上限內；帳本位於 `<home>/mokaair-work/videos/curio-next-five-20261016/review/spend-ledger.json`。
- 17 句旗標詳見 `<home>/mokaair-work/videos/curio-u09/review/check-flags.json`；已委託獨立離線 Whisper 盲聽交叉判讀，不再次送付費轉寫。待確定誤讀範圍後僅定向重錄有依據的句子，其餘送站主逐句試聽與音訊核准。旁白尚未核准、插圖與成片未開始。

### 插畫定向補圖與交接：2026-10-16

- 以上旁白待審描述為較早快照；站主其後已核准劇本與旁白，本輪 `status` 讀回兩關均核准。劇本 SHA `A6EBACD1…AF3F5A`、時間軸 SHA `D1D2C509…7F2EC` 未改。
- 按 [定向修復計畫](../../docs/videos/curio-u09/keyframes-repair-plan-1.md) 對 37 鏡執行一次 `--takes 3` 補圖；詳細費用、雜湊、待修圖和目視證據見 [本輪 QA 收據](../../docs/videos/curio-u09/keyframes-qa-2.md)。更新後 91／91 有選圖、84／91 評審通過、7 張評審待修；另有 2 張評審通過但與旁白明確矛盾，均未送分鏡後台。
- 本輪本機媒體帳本估算新增 US$0.874，低於已預留的 US$1.4985；主代理負責共享帳本核銷。沒有追加付費、合成成片或發布。

### 九鏡提示詞修復：2026-10-16

- 前輪 7 張評審待修，另有 `missed-session`、`beam-away` 兩張評審通過但畫面與旁白明確矛盾。本輪僅改這 9 個 `shot.data.prompt`，沒有改已核准的劇本、旁白、系列畫風或其他 82 鏡；詳細對應見 [第二輪修復計畫](../../docs/videos/curio-u09/keyframes-repair-plan-2.md)。
- 新 `video.json` SHA-256 `E9C4173F6A808A820C3563C13FC3E751344AD5694A117D0BF878D515CAC9E03E`；`script.md` SHA 仍 `A6EBACD1…AF3F5A`。`lint` 為 0 errors／0 warnings。九鏡 `keyframes --takes 3 --dry-run` 通過，MiniMax image-01 1K，保守最多 US$0.3645；沒有付費產圖或後台送審。
- 待主代理完成共享帳本上輪核銷與本輪預留後，限這九鏡重畫、評審、人工核對；91 鏡全過才送站主看聯絡表。

### 九鏡補圖後全尺寸驗收：2026-10-16

- 主代理已限額跑九鏡一批，圖評帳本增加 18 圖／18 評審、估算 US$0.2430；本集共享帳本讀回估算 US$4.129／US$6，已核銷這批。新 manifest SHA `44A280F3…99AB5C`，91／91 有圖、89／91 自動評審通過，仍有 `brief-window`、`beam-away` 兩張未過。
- 獨立全尺寸目視另退兩張雖過評審卻與旁白相反的圖：`more-marks` 把同一卷紙畫成三張分離紙；`line-of-sight` 的波束沒有掃到地球。其他五張依系列的可愛插畫驗收標準暫收。細節、九張選圖 SHA 與同章候選退路見 [第三輪 QA 收據](../../docs/videos/curio-u09/keyframes-qa-3.md)。
- 此輪未動已核准劇本、`video.json`、媒體選圖或後台；四個阻擋鏡頭仍要有合格圖或合規卡片才可送站主分鏡。不得把 89／91 的自動過線當 91／91 可用，也不得未預留共享帳本就讓退路觸發新的 Gemini 圖評。

### 四鏡提示詞定向準備：2026-10-16

- 逐一比對同章已過圖、目標鏡頭的運鏡及畫面與旁白關係；沒有四鏡都可安全複用、且在只改 prompt 時命中圖片快取的退路。只改 `brief-window`、`more-marks`、`line-of-sight`、`beam-away` 四個 `shot.data.prompt`；劇本、旁白、camera、`look` 不動。新 `video.json` SHA `529A13FA…B739E`，細節見 [第三份修圖計畫](../../docs/videos/curio-u09/keyframes-repair-plan-3.md)。
- `lint` 0 errors／0 warnings；四鏡 `keyframes --takes 3 --dry-run` 通過，保守三輪上限 US$0.1620。沒有新付費呼叫、媒體選圖或後台送審。既有 manifest 仍綁舊提示詞，四鏡仍阻擋；主代理先依系列重畫輪數規則與共享帳本決定後續，不得把乾跑當成驗收。

### 補圖後修稿與新版送審：2026-10-16

- 四鏡最後一批實做 7 圖／7 評審、估算 US$0.0945，已依共享帳本核銷；`brief-window`、`line-of-sight` 收下，`more-marks`、`beam-away` 停止付費重試、改來源卡。[第四份逐圖收據](../../docs/videos/curio-u09/keyframes-qa-4.md)記錄選圖 SHA、退回理由、插畫占比與舊 manifest。整集估算已用 US$4.2235／US$6。
- [新版差異史料複核](../../docs/videos/curio-u09/verify-2.md)解除首篇論文的誤導句；現版 `video.json` SHA `A54C8962…7F`。第 `57dd9251` 句依站主授權收窄未解之處。全新十三題盲評 13／13 yes，`narrative --answers` 通過；`script.md` SHA `2EE64BCE…3FC33`。詳見 [劇本狀態](../../docs/videos/curio-u09/script-status.md)。
- `review-push --gate script` 已送新版後台；`review-pull` 讀回前版核准失效、**新版等待站主**。在新版核准前不重錄，也不把舊音訊／分鏡當成新版交付。

### 接上 main 新規則：2026-10-16

- main 新敘事題目使上一版收據失效；新盲評抓到 `1dfdcacf` 對接收器結論的相鄰重述。僅改這句為「那串脈衝究竟來自多遠？」；獨立事實差異複核與另一位全新盲評者 13／13 均通過，詳見 [現行劇本狀態](../../docs/videos/curio-u09/script-status.md)。
- 現行 `video.json` SHA `719CFEA7…17E17`、生成稿 SHA `9D29AB19…B56D8`，已重新送劇本後台，讀回仍等待站主。沒有本輪付費重錄／圖像／成片；現有旁白時間軸及舊分鏡均不可當作新版核准。

### 現行劇本核准後的旁白重錄：2026-10-16

- 後台已讀回現行劇本 SHA `9D29AB19…B56D8` 核准；15 個變動請求定向重錄、86 個快取沿用，新時間軸 SHA `CC8A4E3F…2EDA38`，旁白 9:54。`check-audio` 檢查 102／102 句，15 個新轉寫與 1 次 Jev 判讀留下 17 旗標，其中 16 句沿用已試聽的舊 WAV，唯一新增 `1dfdcacf` 等站主判讀實際讀音。詳細雜湊、成本及差異見[新版音訊 QA 收據](../../docs/videos/curio-u09/audio-qa-2.md)。
- `review-push --gate audio` 已送新版後台、回應 pending；須核對站主對 `1dfdcacf` 的聽感與後台核准，才可沿用 89 張已驗收插畫重綁新 manifest。共用帳本保守估算 U09 US$4.7735／6，尚無新版分鏡或成片。

- 站主試聽 `1dfdcacf` 回覆實際聽到正確的「那串脈衝」、旁白可用；又明確核准 `CC8A4E3F…2EDA38` 時間軸。後台頁面核對為 09:54、102 句、17 旗標的最新卡，完成核准後 `review-pull --gate audio` 讀回 `approval recorded`。下一步只重綁當前 89 張已驗收圖，檢查 manifest／聯絡表後送新版分鏡；不把舊版分鏡核准沿用。

### 新版分鏡重綁與待審：2026-10-16

- `keyframes --shot august-desk --takes 1` 只重綁新版劇本目前需要的 89 張已驗收選圖與評審結果，實際新增圖片／評審均為 0；共享帳本 US$0.02 預留已以零成本釋放，U09 估算累計維持 US$4.7735／6。
- 現行 manifest SHA-256 `CFB01AE25347CBF7DB94C414956058EEECB5ADDD99ECCF4FA4882D4DB33BBE19`，89 鏡均有圖且沒有 `needs_review`；四頁聯絡表已重新產生。`review-push --gate storyboard` 已送新版後台，`review-pull` 讀回 `waiting for the owner`。待站主核准此 manifest 才製作成片；舊分鏡核准不適用。

### 現行分鏡核准後的本機成片：2026-10-16

- 站主在後台核准現行 manifest SHA-256 `CFB01AE25347CBF7DB94C414956058EEECB5ADDD99ECCF4FA4882D4DB33BBE19`，`review-pull --gate storyboard` 讀回 `approval recorded`；本機 `approvals.json` 與 manifest SHA 完全一致。
- `render` 已完成 12 種卡片狀態與縮圖；`clips --dry-run` 和實跑均證實 89 鏡全是已核准關鍵影格的 still 運鏡，新增付費片段 0 支、0 clip 秒。`assemble` 完成 101／101 段，`checks.json` 為 `ok: true`、`problems: []`，89 個 still 鏡頭通過本機檢查，聲音 -14 LUFS／true peak -1 dBFS。
- `final.mp4` SHA-256 `78FAAD29FB5B6556CAF18ACD21063250797F55DA4029638A6EA20349D6156C18`，176,667,919 bytes，1920×1080／30fps，實測 620.5 秒（10:20.5）；品牌片頭置於第一章後，品牌片尾為 v4-endscreen。旁白正文到 `subscribe` 前為 17,606／30 = 586.87 秒，超過八分鐘門檻。
- `captions` 產生繁中 SRT/VTT 共 105 cues，manifest `problems: []`；`review` 產生 `<home>/mokaair-work/videos/curio-u09/review/final.html` 試看頁。尚未執行付費最終 QA、送後台成片審核、製作上傳包或上傳；這些由主代理按共用帳本及站主關卡接續。
- 另從完成片於 00:25、05:00、09:50 抽取畫面目視，三處插畫、浮水印及框架正常，沒有黑畫面或燒錄字幕；抽看圖留在 `review/spot-*.png`。這是三點抽看，不能取代整片的站主審核。

### 成片核准與三語工作表：2026-10-16

- `qa` 與手動成片送審完成；最終 QA 為 10／11，唯一未過是當時站主尚未選語言，因此沒有英／日／韓字幕。繁中字幕、史料、畫面、音訊與政策等其他項目均通過。站主看過成片並在後台核准；後台最新 `final` review `09638ac5-1613-42af-82da-c43ead149d23` 讀回 `approved`，SHA-256 `78FAAD29FB5B6556CAF18ACD21063250797F55DA4029638A6EA20349D6156C18`，本機 `approvals.json` 相同。
- 後台語言面板於 `2026-10-16T13:55:04.341942Z` 儲存 en／ja／ko，三語均勾標題說明、字幕、配音。站主另授權 U09 多語新增 US$2.50 估算停手上限，使 U09 上限 US$8.50、五集合計 US$39.00；範圍與限制見 [多語授權收據](../../docs/videos/curio-u09/multilingual-authorization-1.md)。本機 `languages.json` 已按後台選擇落地。
- `i18n-sheet` 與 `i18n-merge` 已離線完成英、日、韓第一輪文稿：每語 102／102 句、7／7 章、標題、說明、標籤與縮圖文字；重新生成工作表皆顯示 0 待譯／過期，逐句均未超過配音用 `max_chars`。目前檔案 SHA-256：en `3B326B0E26439BF7C1A86497838C0261423C04E62C13E784E8FCFA2361174D26`、ja `822D4E141973B8527795E23F23371E92568F5700045787BB49C32AC83FF401FF`、ko `851FAC954DDD2B93DD1F56E921307DC932FD612CC5E77112B2A364C51DA4CFEA`。這是翻譯者第一輪，尚未通過獨立審稿。
- `dub --dry-run` 只讀估算：三語各 101 次合成請求；en 6,308、ja 2,798、ko 2,873 計費字元。英文 3／101、韓文 6／101 個時槽預計需加速；三語皆 0 個時槽超出 1.15 倍可容納上限。乾跑未送 Gemini、未產出三語音軌或付費 QA。待獨立審稿、逐語預留與帳本核對後才開始付費製作；任務維持 open，尚無三語 QA、語言包、Studio 上傳或發布。
- 本機 `captions` 產出草稿：zh-TW 105、en 104、ja 108、ko 109 cues；首次日語 `1dfdcacf` 一張字幕讀速超標，已只縮該句後重產，四語皆無字幕警告。這些外語字幕目前按繁中旁白時間軸排，配音完成後仍須按各語音軌重產。

### 三語獨立審稿後定向修訂：2026-10-16

- [第一輪獨立審閱](../../docs/videos/curio-u09/i18n-review-1.md) 對 en／ja／ko 分別列出 3 處、4 組、8 組缺點，狀態均為 HOLD。只依具體意見修英語 3 句、日語 4 句加說明欄、韓語 8 句加說明欄；原譯與新譯 SHA、修訂項目、乾跑與字幕數量見[定向修訂收據](../../docs/videos/curio-u09/i18n-revision-1.md)。新 SHA：en `2F5A696F…CFBEA`、ja `09256F9F…827EE`、ko `113A00E2…1B473`。
- `i18n-sheet` 三語 0 待譯／過期，句 ID 均與現行繁中稿 102／102 對應，逐句未超 `max_chars`。`dub --dry-run` 三語各 101 次請求，沒有不可容納時槽；字幕草稿 en 104、ja 109、ko 110 cues，工具無警告。未做付費呼叫，待獨立重審 PASS 後再與主協調者預留共享帳本，逐語製作配音與 QA。
### 韓語第二輪定向修訂：2026-10-16

- 第二輪獨立覆核判 en／ja PASS，ko 只留 `acc6618c`「天空另一區域通過」未明示；依覆核建議只修該句並順修 `fe66ab8a` 天空區域用詞。韓語舊 SHA `113A00E2…1B473`、新 SHA `3BFEFC99…313FB`，完整文字與乾跑見[韓語修訂收據](../../docs/videos/curio-u09/i18n-revision-2.md)。
- 韓語 102／102 句 ID、0 超時槽字數；`dub --dry-run` 101 次請求、0 不可容納時槽；字幕草稿 109 cues，無工具警告。新雜湊仍待獨立複核 PASS；未做付費呼叫。

### 三語獨立複核 PASS、英語配音與 QA：2026-10-16

- 第二輪獨立審稿已對 en／ja／ko 全數 PASS：文稿 SHA 分別 `2F5A696F…CFBEA`、`09256F9F…827EE`、`3BFEFC99…313FB`；後台仍選三語的標題說明、字幕與配音。
- 英語完成 101 次 Gemini 合成、102 句時間軸、620.5 秒音軌，0 句超時槽；Gemini 102／102 句轉寫與 Jev 一次判讀留下 10 句旗標。英語 TTS／QA 已依共享帳本各核銷保守估算 US$0.15／US$0.50，U09 累計估算 US$5.5235／US$8.50。詳細雜湊、離線 small 10 句與 medium 2 句分流見[英語音訊 QA 收據](../../docs/videos/curio-u09/i18n-audio-qa-en-1.md)。
- 接上 main 新漏字規則後，快取重跑 `check-audio --locale en` 為 0 新轉寫／0 新 Jev 呼叫，`3d181765` 顯示 `thought` 漏字疑點；兩套本機 Whisper 均未聽到。`049813c5` 兩套 Whisper 加 Gemini 均聽成 `published`（稿為 `publish`），待站主定向試聽；其餘旗標主要是人名或同音拼寫。102 句本機試聽頁在 `<home>/mokaair-work/videos/curio-u09/review/dub-en.html`，尚未得到站主英語聽感核准。
- 尚需逐語完成日／韓配音與 QA、站主試聽判讀、按配音時間軸重產字幕及語言上傳包；沒有上傳或發布。

### 日語第 101 次合成請求停手：2026-10-16

- 已按 U09 多語額度預留 JA TTS US$0.15、QA US$0.50；前 100／101 次合成請求成功，101／102 句 WAV 有快取。最後 `259da0ce` 的 33 個計費字元在 HTTP 502 後沒有可用回應，journal SHA `7c12c540…a930` 狀態 `held`；沒有完整 JA 音軌、時間軸或 QA。詳見[日語未明計費停手收據](../../docs/videos/curio-u09/i18n-ja-speech-hold-1.md)。
- 站內月額讀回只扣 2,764／原估 2,797 字，剛好未計最後 33 字；這不是 Gemini 官方用量收據，供應商是否計費仍未知。依既有「帳單不明即停」授權與 `docs/videos/DUBS.md`，未清 journal hold、未重送、未核銷預留，也未啟動 JA QA 或 KO 製作。待站主確認該筆用量或明確允許將它視作可能已付費並定向重試後續接。

### 日語定向恢復與新音軌 QA：2026-10-17

- 站主後續明確授權 `259da0ce` 一句 33 字重送、接受可能重複計費；只清該筆 journal hold，恰 1 新請求完成，先前 100 個已付費請求沿用。原 502 的供應商計費狀態仍未知，詳見[停手與定向恢復收據](../../docs/videos/curio-u09/i18n-ja-speech-hold-1.md)。
- 首次完整 fit 只有開場兩句約超 0.8 秒；獨立日語覆核通過後只縮 `96e528ee`、`8748fb3d`。新譯稿 SHA `5A77E028…C52FAB`，只新增一個 45 字 grouped 請求，完整音軌時槽全過；見[日語開場修訂](../../docs/videos/curio-u09/i18n-ja-fit-revision-1.md)。
- 第一輪完整日語音訊 QA 為 102／102 轉寫、1 次 Jev、22 旗標；本機 Whisper small 全 22 句與 medium 重點五句複核後，僅依證據定向修 `07ceb40b`、`724570c6`、`3ecfc37e` 三句。獨立日語覆核通過，現行 `ja.json` SHA `D53FC69F…38FBE`；逆替三句可恢復上一版雜湊，其餘 99 句未變。三句 TTS US$0.03、定向 QA US$0.15 已預留；實跑恰 3 新請求／93 字、98 快取沿用。完整 JA 音軌 SHA `066EA9CB…784D9`，620.5 秒、102 句、101 時槽、0 超時槽。
- 新一輪 `check-audio --locale ja` **只完成 101／102 個現行 WAV**：2 新句轉寫與 1 次 Jev，70 逐字一致、12 Jev 接受、19 旗標。`724570c6` 的 Gemini 轉寫返回 `502 AI 拒絕回應（OTHER）`，新 WAV 無 transcript；`check.ja.json` 裡該 ID 的舊快取與新 WAV 雜湊不符，不能把 JSON 102 個鍵當成全過。journal 無 hold，但供應商是否計費未知，因此沒有重送拒答的轉寫；後續核銷見下一筆紀錄。本機 Whisper small／medium 對新句都聽成「検査された」，核准稿是「確認された」；當時待站主定向試聽。完整狀態與 SHA 見[日語音訊 QA 收據](../../docs/videos/curio-u09/i18n-audio-qa-ja-1.md)，逐句試聽頁位於 `<home>/mokaair-work/videos/curio-u09/review/dub-ja.html`（19 旗標加 1 未驗句）。
- 2026-10-17，站主試聽現行 `724570c6.wav` 後確定聽到核准稿的「確認された」，不需重錄；此人工判讀不會補上新版 clip 缺少的機械轉寫。JA TTS US$0.03（3 成功請求／93 字）及 QA US$0.15（2 成功轉寫／1 Jev／1 計費不明拒答）已按全額保守核銷，當時 shared ledger SHA `11E13614…03211D`、U09 累計 US$6.3835／8.50。須另取得該一句轉寫重送授權，才可完成 JA 102／102 機械檢查；19 旗標仍須站主聽感判定，不能將日語音軌標為 ready。
- KO 譯稿 SHA `3BFEFC99…313FB` 已通過獨立審閱；乾跑 101 grouped requests／2,863 字、0 超時槽。韓語 TTS US$0.15 及音訊 QA US$0.50 已在共享帳本預留，SHA `9AB30450…B19754A`；須待 `dub` 成功完成 102 句與音軌、時間軸，才啟動已預留的付費 QA。韓語字幕、試聽頁與語言上傳包尚未完成。
- 站主另行授權日語 `724570c6` 只重送一次 Gemini 轉寫，接受可能重複計費。這次新增 1 成功轉寫與 1 Jev，現行音檔已 **102／102** 轉寫、20 旗標；該句新轉寫仍聽成「検査された」，但站主對同一 WAV 確認是「確認された」，因此保留音檔。其餘 19 旗標尚無站主整軌試聽核准。更新後試聽頁 102 音訊連結、20 旗標、0 未驗句，SHA `D8E6C6A8…B543E1E`；詳見[日語音訊 QA 收據](../../docs/videos/curio-u09/i18n-audio-qa-ja-1.md)。
- KO `dub` 成功完成 101 grouped 請求／2,863 計費字元，102 WAV、620.5 秒音軌、102 句時間軸、0 超時槽。音軌 SHA `775DE106…77E42E9`、時間軸 `886287B3…0F661BF`、fit `EE9B309C…CCF809E`。KO TTS US$0.15 與 JA 單句 QA US$0.15 已全額保守核銷，當時 shared ledger SHA `2385CDEE…ED38A4`、U09 累計 US$6.6835／8.50；韓語 QA US$0.50 仍預留，現正逐句轉寫。韓語試聽與字幕尚待 QA 後更新。
- 英語仍有 10 個旗標待站主試聽，英語字幕另有 `fcd9695d` 一句 21.3 字／秒超過 20 的讀速門檻；日語現行音軌重錄後須按配音時間軸再產字幕。韓語文稿已獨立審稿 PASS，但尚未配音或做付費 QA。四語上傳包、後台語言審核、Studio 上傳和公開都未完成；本票維持 open。

### 三語試聽核准與現行字幕：2026-10-17

- 站主已試聽 U09 英／日／韓三語逐句頁，回覆「三語旁白都可以」，包含新錄 KO `b6d2d02b`；稍早亦對現行 JA `724570c6` 明確聽出核准稿的 `確認された`。這是人工聽感接受，**不改寫** `check-audio` 的 EN 10、JA 20、KO 24 個機械旗標。三語均無未轉寫的現行 WAV，皆為 102／102；字幕與後台語言審核是後續關卡。各語現行音訊收據：[英語](../../docs/videos/curio-u09/i18n-audio-qa-en-1.md)、[日語](../../docs/videos/curio-u09/i18n-audio-qa-ja-1.md)、[韓語](../../docs/videos/curio-u09/i18n-audio-qa-ko-1.md)。
- KO 獨立文字複核發現 `b6d2d02b` 將「還可以靠旋轉」過度確定為「就是旋轉」；只修這一句，初稿譯文 SHA `3BFEFC99…313FB` → 現行 `E8AEAF6D…63BBB3`，獨立再審 PASS。定向新增 TTS 1 grouped 請求／50 字、QA 1 Gemini 轉寫／1 Jev，其餘 100 請求與 101 句轉寫沿用快取。現行 KO 音軌 SHA `9239141A…3B44`、時間軸 `15E00CC4…E1DD`、0 超時槽；現行試聽頁有 102 WAV、24 旗標、0 未驗句。KO 首輪 US$0.15 TTS＋US$0.50 QA、定向 US$0.02 TTS＋US$0.15 QA 均已保守核銷。U09 全集估算累計 US$7.3535／8.50，當時全批含 H12 final QA 預留 US$26.2295／39.00；後續使用帳本前須重讀現況。
- 四語字幕已依現行時間軸重產：zh-TW 105、EN 104、JA 109、KO 109 cue。EN 第 91 cue `fcd9695d` 從 21.3 CPS 的 2.110 秒延至 2.367 秒，修正版 SRT／VTT 精確同文同時、18.6 可見 CPS、離下句 2.5 秒；四語 manifest 問題皆空。修正只影響英文字幕，未改已核准繁中成片、英語譯稿或配音，詳見[字幕定向修正收據](../../docs/videos/curio-u09/i18n-caption-en-cue91-fix-1.md)。再次跑 `captions` 會覆蓋 EN 修正，必須重套並核對。
- U09 任務仍 open；語言上傳包與後台語言審核尚需以現行字幕、三語音軌和正式成片完成，Studio 音軌由站主自行操作。

### 四語上傳包與最新版後台卡：2026-10-17

- 初次 package 已 4／4，但獨立稽核發現三語縮圖字雖已審齊，舊 `frames/manifest.json` 的缺漏紀錄使包未帶分語縮圖。只執行 `render --thumbnails-only`，新增 en／ja／ko 三張 1280×720 縮圖；原 `thumbnail.jpg` 與聯絡表雜湊未變，已核准繁中 `final.mp4` SHA 仍 `78FAAD29…56C18`。三張目視沒有裁字；新版 package 重建後 4／4，四語說明／字幕、三語配音與三語縮圖齊全，十份來源與包內副本逐檔 SHA 相同。[上傳包收據](../../docs/videos/curio-u09/i18n-package-1.md)記錄精確 SHA 與字幕讀速檢查。
- 最新 `upload/metadata.json` SHA `4CEACE32B226D9B42783CC456B6C6CD7C7CEB30B20A163A9F7D7B351053E14D7`；publish 審核卡 `febf304b-511e-4a06-ac47-9d84eb439b7b` 已送並讀回 `pending`，等站主核准。最新 languages 審核卡 `4b526710-8719-43a4-a433-c9d5ded8d310`、manifest SHA `E170FA4BB6194114D0294377B28FD1E77B6E7D9733101C5D826DC78432F6C1B5` 也讀回 `pending`，待站主之後在 Studio 自行傳三語配音並於後台確認。第一輪無分語縮圖的兩張卡已自動標 `superseded`，不可核准舊版。尚無 Studio 音軌上傳、排程或發布；本票維持 open。
