---
id: 2026-10-01-sothatswhy-season2-batch02
title: 原來如此第二季第二批：B27 S27 T28 A33 製作包與獨立審稿
status: in-progress
priority: P2
area: docs
owner: codex-sothatswhy-batch02
claimed_at: 2026-10-01T05:43:43Z
created_at: 2026-10-01T05:43:41Z
completed_at:
branch: codex/sothatswhy-season2-batch01
depends_on:
  - 2026-09-29-so-that-s-why-vet-the
scope:
  - docs/videos/so-thats-why/season2/B27.md
  - docs/videos/so-thats-why/season2/S27.md
  - docs/videos/so-thats-why/season2/T28.md
  - docs/videos/so-thats-why/season2/A33.md
  - docs/videos/so-thats-why/season2/reviews/batch02/
  - docs/videos/so-thats-why/season2/batch02-packaging.json
  - docs/videos/so-thats-why/season2/validate.mjs
---

# 原來如此第二季第二批：B27 S27 T28 A33 製作包與獨立審稿

## Why

user「繼續」後接續第二季母票，從剩餘96題取B27/S27/T28/A33。首批四包與草稿PR#1075保持文字包狀態；第二批補今天的來源、完整企劃、兩支Shorts與五語，不付費生成或匯入。候選索引由已認領的母票更新。

## Definition of done

- [x] 四包包含逐條當日來源、4000/2000字元內後台欄位、480秒六章、各兩支180–220單位Shorts、五語長短片包裝、具體原創插畫與縮圖提示。
- [x] 每包不同作者／查核者的事實、聽眾文字與五語審稿；FIX已閉合，報告及JSON收據綁最終byte SHA256。
- [x] `batch02-packaging.json`與正文相符；現有檢查器支援兩批且首批包／收據不變。
- [x] 第二批以草稿PR#1075追加交接，母票8/100文字包進度與其餘92題未選狀態清楚。

## Steps

- [x] 核對worktree／遠端分支／PR與題庫去重；claim精確scope。
- [x] 四題撰稿與當日查核，刪未核故事與全球泛化。
- [x] 換人審稿、修正、最終雜湊收據。
- [x] 檢查兩批、票務、連結，更新既有草稿PR。

## How to verify

`node docs/videos/so-thats-why/season2/validate.mjs`與`--batch=batch02`、`npm run check:tasks`、`git diff --check`。只有本批四列候選題變動、首批包與收據雜湊不變、機械檢查能拒絕正文／報告／包裝變更。不宣稱實際音檔人聽、生成圖或成片QA。

## Notes

- 2026-10-01：PR#1073與#1075仍為草稿，後者CI在進行；沒有合併授權。本批在同分支更新#1075，維持依賴#1073，不新增堆疊第三層PR。
- B27不能說9必定賣更多；S27不用未核現行救護車法律當泛用說法；T28由目前官方收運說明切入，曲目歷史若無一手不採；A33不用「Hopper找到第一個bug」的迷思。

- 2026-10-01 驗收：四包交叉審稿PASS，B27 write_b26→root、S27 write_a31→write_t26、T28 root→write_b26、A33 write_t26→write_a31；只有1項FACT措辭／頁次澄清及來源日期更正，沒有>3 FACT改動。
- 兩批validator均PASS；isolated positive fixture通過，package／report hash drift、bundle drift與unknown batch都拒絕。140個本地Markdown連結可解析，原100id/status/check保存；僅本批四列更新，其餘96列包括首批不變，首批正文／審稿／bundle未變。check:tasks驗1238票與diff --check通過；既有過期claim與scope重疊僅警告。
- 第二批文字包及母票進度由同一草稿PR#1075交接，base為#1073分支。正式長片逐字稿、真實音訊／圖像及站主核准均未完成，不以TEXT_ONLY宣稱媒體可上架。
