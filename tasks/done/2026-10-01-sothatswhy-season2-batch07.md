---
id: 2026-10-01-sothatswhy-season2-batch07
title: 原來如此第二季第七批：B47 S48 T48 A44 製作包與獨立審稿
status: done
priority: P2
area: docs
owner: codex-sothatswhy-batch07
claimed_at: 2026-10-01T08:37:38Z
created_at: 2026-10-01T08:37:36Z
completed_at: 2026-10-01T09:04:29Z
branch: codex/sothatswhy-season2-batch07
depends_on:
  - 2026-09-29-so-that-s-why-vet-the
scope:
  - docs/videos/so-thats-why/season2/B47.md
  - docs/videos/so-thats-why/season2/S48.md
  - docs/videos/so-thats-why/season2/T48.md
  - docs/videos/so-thats-why/season2/A44.md
  - docs/videos/so-thats-why/season2/reviews/batch07/
  - docs/videos/so-thats-why/season2/batch07-packaging.json
  - docs/videos/so-thats-why/season2/validate.mjs
---

# 原來如此第二季第七批：B47 S48 T48 A44 製作包與獨立審稿

## Why

接續使用者「繼續」，從剩餘76題選KitKat考生贈禮、火焰形狀、北海道愛努語地名及雙胞胎臉部解鎖，補四份可追溯文字企劃，累計24到28題，以第七批單獨草稿交接。企劃母分支#1073已含前六批24包。已對第一季、第三季、品牌100及AI名詞完整題庫比對核心問題與例子；相近背景不構成同題。母票只持有索引，本票限定四包及本批審稿、bundle、validator映射。

## Definition of done

- [x] 四包有2026-10-01直接讀來源與限制、前提/備註4000/2000、六章480秒、每包兩支180–220單位Shorts、18個原創提示與15組五語標題說明。
- [x] 不同作者獨審事實、聽眾文字與五語；修正閉合，報告和收據綁final byte SHA256。
- [x] 七批validator及漂移拒絕通過；前六批78份包/報告/收據/bundle byte不變，索引只改本四列並保存原check/status/verdict。
- [x] README及母票記28/100、剩餘72題待審選；本批在草稿結案，母票保持開放並釋出。

## Steps

- [x] 核對worktree/branch/remote/PR及main範圍歷史、去重，claim兩票並分配作者。
- [x] 重讀一手來源、寫四包；窄化歷史商品、外加氣流/微重力、地名多說及相似臉風險的適用條件。
- [x] 交叉事實、聽眾文字及15組五語獨審，修正後重讀，收據綁最終SHA。
- [x] 七批validator、漂移fixture、本地連結/字元；提交本批並開第七批草稿，票務及staged whitespace作提交前最後檢查。

## How to verify

node docs/videos/so-thats-why/season2/validate.mjs（預設batch01及--batch=batch02至batch07）；npm run check:tasks；git diff --cached --check。來源、獨審、原包byte保留與索引四列另驗；文字檢查不是媒體或站主驗收。

## Notes

- 2026-10-01提交前新核對：#1075已於08:55:06Z併入codex/knowledge-story-backlog（7c31e842）；#1073尚開啟、未併main。新母分支與開工HEAD 00ea84的完整tree相同，故保留全部未提交內容，改以codex/sothatswhy-season2-batch07從更新後母分支另開草稿，沒有重播前六批或合併/推動母PR。
- check:tasks已驗1244票PASS；原有不相干stale/scope警告未動。Windows done留下open duplicate時，確認done副本僅status及completed_at有預期差異後，刪精確舊open檔，done內容保留。
- 七批validator PASS；isolated valid exit0，正文/報告/bundle漂移各exit1且原因正確，未知batch exit1。227個本地Markdown連結及LF/單EOF通過，前六批78份包/報告/收據/bundle byte保留。索引只改B47/S48/T48/A44四列，其餘96列語義及所有原check/status/verdict保存。
- 四份不同作者報告均0項FACT修正。S48三處繁中/日文措辭及「未自行取得實驗數據」界線已作者修正，獨審全文及15語重讀後綁0876最終byte。其他三包沒有待修項；四包的純旁白含句內標點最長均≤40字元，口語單位與字元統計分開，發音和實際音訊仍待媒體階段。
- B47的2018桔梗屋公告及2009願望卡展示都限定公告內容，不推今天服務或成效；官方地方頁UA403但web原正文可讀。S48原PDF作者web403、UA200且實讀，獨審自己的最後web也可讀；不同取得結果分開紀錄。T48官方歷史背景與兩說/未明限定全語保留；A44不把Face ID單一外觀/隨機人基準推給Pixel或全部群體。

2026-10-01開工：原查核報告只作題目/URL線索，新增主張以今日一手原文核。B47不推2009商品今日可寄或在售、不採累計口味數；S48限定普通地面蠟燭和微重力低動量條件；T48不用單一字義定論/80%或北海道命名逸事，不仿造愛努紋樣；A44不把隨機他人統計推給孿生/相似手足或全部裝置。

長片仍為六章企劃，完整逐字稿另作。無付費生成、人聽/圖片/成片QA、正式匯入、核准、部署或上架。原topic-checks保存，需更正另開精確scope票。
