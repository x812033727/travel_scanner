---
id: 2026-10-15-curio-u09-research-outline
title: Curio U09 research outline
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-u09-production
claimed_at: 2026-10-16T01:13:24Z
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
