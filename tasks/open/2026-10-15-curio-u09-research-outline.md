---
id: 2026-10-15-curio-u09-research-outline
title: Curio U09 research outline
status: in-progress
priority: P2
area: docs
owner: codex-curio-u09-script
claimed_at: 2026-10-15T23:53:06Z
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
- [ ] 正式稿獨立史料覆核、十三題盲評與站主劇本核准；媒體製作另按關卡接續。

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
- [ ] 補格式新版 brief 由主代理重新送審並讀回核准，再送劇本。

## How to verify

對照 research.md 的來源開啟狀態及 claims.md C01–C24。用獨立讀者檢查 1967 年初始記錄／快紀錄、LGM、1968 年振盪／旋轉的分界；核對 brief.md 有 A／B、7 章約 600 秒與三個開場 loops。`npm run check:tasks`；`git diff --check`。尚無正式稿，不執行媒體或 video.json lint。

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
