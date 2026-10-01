---
id: 2026-10-01-sothatswhy-season2-batch09
title: 原來如此第二季第九批：B42 S35 T35 A37 製作包與獨立審稿
status: done
priority: P2
area: docs
owner: codex-sothatswhy-batch09
claimed_at: 2026-10-01T11:29:02Z
created_at: 2026-10-01T11:29:00Z
completed_at: 2026-10-01T11:53:17Z
branch: codex/sothatswhy-season2-batch09
depends_on:
  - 2026-09-29-so-that-s-why-vet-the
scope:
  - docs/videos/so-thats-why/season2/B42.md
  - docs/videos/so-thats-why/season2/S35.md
  - docs/videos/so-thats-why/season2/T35.md
  - docs/videos/so-thats-why/season2/A37.md
  - docs/videos/so-thats-why/season2/reviews/batch09/
  - docs/videos/so-thats-why/season2/batch09-packaging.json
  - docs/videos/so-thats-why/season2/validate.mjs
---

# 原來如此第二季第九批：B42 S35 T35 A37 製作包與獨立審稿

## Why

接續使用者「繼續」，從剩餘68題選B42 Sega家用主機轉型、S35秋葉紅色生成、T35年越蕎麥文化寓意與A37電源轉換的縮小條件，補四份文字企劃，累計32到36題。已對第一季、第三季、品牌100及AI名詞完整題庫比核心問題與例子。母票持有索引，本票限定四包與本批審稿、bundle及validator映射；第八批PR#1080外部轉待審後另開第九批分支草稿，前八批原包不改。

## Definition of done

- [x] 四包有2026-10-01來源正文與限制、前提/備註4000/2000、六章480秒、每包兩支180–220單位Shorts、18個原創提示與15組五語標題說明。
- [x] 不同作者獨審事實、聽眾文字及五語；修正閉合，報告與收據綁final byte SHA256。
- [x] 九批validator及漂移拒絕通過；前八批104份包/報告/收據/bundle byte不變，索引只改四列並保存原check/status/verdict。
- [x] README與母票記36/100、剩餘64題待審選；本批在草稿結案，母票保持開放並釋出。

## Steps

- [x] 核worktree/branch/remote/PR與main範圍歷史、去重，claim兩票再分作者。
- [x] 今日來源親讀、寫四包，記錄來源取得限制與收窄理由。
- [x] 不同作者交叉事實、聽眾文字、15組五語審稿，修正後全文重讀並綁雜湊。
- [x] 九批validator、漂移fixture、本地連結/字元、票務及staged whitespace通過，提交第九批草稿。

## How to verify

node docs/videos/so-thats-why/season2/validate.mjs（預設batch01與--batch=batch02至batch09）；npm run check:tasks；git diff --cached --check。另核來源、獨審、原包byte保留及索引四列。文字檢查不是媒體或站主驗收。

## Notes

- 歸檔及母票release後check:tasks exit0，Validated 1246 task files。staged whitelist為本批18檔，git diff --cached --check exit0；既有不相干stale/scope警告未更動。提交前再核#1080/#1079/#1073均OPEN，08遠端head仍2ea7929d，第九批遠端尚不存在。

- Windows tasks done已寫done副本但舊open仍在、exit1；已核兩個絕對路徑在workspace、done狀態/時間有效，除status/completed_at外全文相同，才刪精確舊open。done完整保留。母票release成功，status open、owner及claimed_at空白。
- 額外不同代理唯讀整合核對PASS：README36/72/540/64、四列original_title/check/status/verdict、四包全部metadata與bundle、審稿路由/雜湊/false媒體旗標一致，無需修正。

- 四份獨審PASS；B42/S35/T35 FACT0且無必修OTHER。A37 FACT1英文過度斷言、KO三標題品牌及縮圖規格由作者修正後，獨審全文/15語重讀閉合並綁新SHA。四包的報告與收據均綁最終byte雜湊；無音訊或媒體驗收。
- 九批validator PASS；isolated valid exit0，正文/報告/bundle漂移及未知batch各exit1、原因正確，fixture driver最終exit0。261本地Markdown連結與LF/singleEOF、前八批104檔逐byte保存通過。索引僅B42/S35/T35/A37變更、其他96列及原100 ID/check/status/verdict保留；README36/72/540與剩餘64一致。
- Shorts單位B42 200/199、S35 204/217、T35 201/195、A37 198/201；真句長連句尾符號也≤40，無Latin拼讀。句尾符號與split/trim的計數口徑分開記，實際口速仍待音訊。
- 原本未安裝本worktree依賴，tools/skills.test.mjs因js-yaml缺失未啟動；依鎖檔npm ci --ignore-scripts補543套件（無改鎖檔），用bundled Node24.19.0重跑tasks與skills共25測試PASS。初次default Node24.13的engine提示不當測試失敗根因；沒有跑無關全web/API或聲稱全test:tools完成。
- 提交前scope collision重查只有本兩票及既有PR鏈；#1080 OPEN非draft/head2ea7929d，八項CI SUCCESS；#1079與#1073仍OPEN。第九批獨立草稿base選08，不改既有ready PR或合併。

2026-10-01開工核對：#1080 OPEN非draft，head2ea7929d/base codex/sothatswhy-season2-batch07；#1079 OPEN非draft/head d6180df4/base codex/knowledge-story-backlog，母PR#1073 OPEN/head7c31e842/base main。origin/main更新3b297d52，相關scope歷史無新落地；無其他active task/branch/worktree/PR佔本次新增scope。保留使用者未追蹤.codex/environments/。從08 HEAD另切codex/sothatswhy-season2-batch09，不修改第八批審查狀態。

B42以品牌回顧描述2001轉型，原年報PDF未讀不採；S35講部分秋葉花青素生成，不推所有紅葉或唯一用途。T35文化寓意與據傳廣傳分開，刪六成未溯源數字和午夜規範；A37以DOE工程條件，不把換晶片當每款小冷安全的保證，不採GaN藍光LED品牌故事。

長片仍為六章企劃，完整逐字稿另作。無付費生成、人聽/圖片/成片QA、正式匯入、核准、部署或上架。原topic-checks保存，需更正另開精確scope票。
