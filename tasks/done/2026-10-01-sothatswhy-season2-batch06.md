---
id: 2026-10-01-sothatswhy-season2-batch06
title: 原來如此第二季第六批：B44 S43 T43 A46 製作包與獨立審稿
status: done
priority: P2
area: docs
owner: codex-sothatswhy-batch06
claimed_at: 2026-10-01T07:46:16Z
created_at: 2026-10-01T07:46:05Z
completed_at: 2026-10-01T08:12:30Z
branch: codex/sothatswhy-season2-batch01
depends_on:
  - 2026-09-29-so-that-s-why-vet-the
scope:
  - docs/videos/so-thats-why/season2/B44.md
  - docs/videos/so-thats-why/season2/S43.md
  - docs/videos/so-thats-why/season2/T43.md
  - docs/videos/so-thats-why/season2/A46.md
  - docs/videos/so-thats-why/season2/reviews/batch06/
  - docs/videos/so-thats-why/season2/batch06-packaging.json
  - docs/videos/so-thats-why/season2/validate.mjs
---

# 原來如此第二季第六批：B44 S43 T43 A46 製作包與獨立審稿

## Why

接續使用者「繼續」，從其餘80題選米其林指南、星星閃爍、倫敦Knowledge及USB安全移除，補四份可追溯文字企劃，累計20到24題，沿用草稿#1075。已對第一季、第三季、品牌100及AI名詞標題去重，無同一問題；S43不改寫天空顏色，T43不重寫其他交通設備，A46不作硬體可靠性或資料救援教程。

## Definition of done

- [x] 四包有2026-10-01直接讀來源及限制、前提/備註4000/2000、六章480秒、每包兩支180–220單位Shorts、原創提示/AB及15組五語標題說明。
- [x] 不同作者獨審事實、聽眾文字及五語，修正閉合，報告與收據綁final byte SHA256。
- [x] 六批validator與漂移拒絕通過；前五批65份包/報告/收據/bundle byte不變，索引只改本四列且check/status/verdict保留。
- [x] README及母票記24/100、其餘76題待審選；本批在草稿結案，母票保持開放並釋出。

## Steps

- [x] 查worktree/branch/remote/PR、main範圍歷史及去重，claim兩票；母票只改索引，本票只改四包、審稿、本批bundle及validator映射。
- [x] 重讀一手來源、寫四包，修正原題的辨識保證、全倫敦/所有載客服務及隨時拔USB誤讀。
- [x] 交叉事實、聽眾文字及五語獨審；收據綁最終SHA。
- [x] 六批validator、漂移fixture、連結/字元/票務，提交本批並更新同草稿；staged whitespace作提交前最後檢查。

## How to verify

node docs/videos/so-thats-why/season2/validate.mjs（預設batch01及--batch=batch02至batch06）；npm run check:tasks；git diff --cached --check。來源、獨審與byte保留另驗；文字檢查不是媒體或站主驗收。

## Notes

- 六批validator PASS；isolated valid exit0，正文/報告/bundle漂移各exit1且原因正確，未知batch exit1。210本地Markdown連結、LF/單EOF、前五批65份byte保留通过。索引恰改B44/S43/T43/A46四列，其餘96列語義與所有原check/status/verdict保留；check:tasks驗1243票PASS，無關stale/scope警告未動。
- B44所有目的明歸屬官方，root獨讀三原頁；S43點源可見性及Short1日文may兩限定修正後全文/15語重審；T43的320/quarter mile收窄All London、不套所有Suburban，2022冊只作範圍提醒；A46兩listener拆句後全文/15語重審，政策與當前傳輸範圍不變。所有四報告和JSON收據綁final byte SHA256，沒有未閉合必要修正。

長片仍為六章大綱，無完整逐字稿。無付費生成、音訊人聽/圖片/成片QA、正式匯入、核准、部署或上架。原候選查核只作URL線索，新增主張由今日原文驗；更正舊topic-checks需要另開精確scope票。
