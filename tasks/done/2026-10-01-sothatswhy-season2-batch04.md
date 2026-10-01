---
id: 2026-10-01-sothatswhy-season2-batch04
title: 原來如此第二季第四批：B37 S31 T29 A41 製作包與獨立審稿
status: done
priority: P2
area: docs
owner: codex-sothatswhy-batch04
claimed_at: 2026-10-01T06:47:52Z
created_at: 2026-10-01T06:47:51Z
completed_at: 2026-10-01T07:07:19Z
branch: codex/sothatswhy-season2-batch01
depends_on:
  - 2026-09-29-so-that-s-why-vet-the
scope:
  - docs/videos/so-thats-why/season2/B37.md
  - docs/videos/so-thats-why/season2/S31.md
  - docs/videos/so-thats-why/season2/T29.md
  - docs/videos/so-thats-why/season2/A41.md
  - docs/videos/so-thats-why/season2/reviews/batch04/
  - docs/videos/so-thats-why/season2/batch04-packaging.json
  - docs/videos/so-thats-why/season2/validate.mjs
---

# 原來如此第二季第四批：B37 S31 T29 A41 製作包與獨立審稿

## Why

接續使用者「繼續」，從尚未製作88題選Amazon部門營業利益、高山沸點、日本街區住居表示與手套觸控；累計文字包由12到16，沿用草稿#1075。四題比對第一季/第三季/品牌100/AI名詞，無相同問題；B37不照搬Alphabet公司結構，S31不重寫S44昇華，T29不作所有日本地址通則，A41不作設備實測。

## Definition of done

- [x] 四包有今日直接讀原始來源與限制、後台4000/2000欄位、480秒六章、各兩支180–220單位Shorts、英文原創圖像/AB縮圖與15組五語標題說明。
- [x] 不同原作者獨審事實、聽眾文字與五語，修正閉合、報告和收據綁最終byte SHA256。
- [x] 四批validator及isolated drift拒絕通過，前三批正文/報告/收據/bundle byte不變；索引只改本批四列且原check/status/verdict保留。
- [x] 母票與README記16/100、其餘84題未決；批次票在草稿#1075結案，母票釋出保持開放。

## Steps

- [x] 比對分支/worktree/遠端/PR/main範圍歷史及既有題庫，claim窄scope與母票。
- [x] 今日重查一手來源並寫四包，刪未核歷史、共通保證或未讀數字。
- [x] 交叉事實/聽眾文字/五語獨審，修正閉合、最終SHA收據。
- [x] 四批validator、isolated fixture、連結、票務及staged whitespace；提交並更新草稿。

## How to verify

node docs/videos/so-thats-why/season2/validate.mjs；--batch=batch02、batch03、batch04；npm run check:tasks；git diff --cached --check。機械檢查不替代一手來源與獨審，也不代表媒體驗收。

## Notes

- 完成focused驗收：四批validator全部PASS；isolated positive exit0，正文/報告/bundle漂移各exit1，未知batch拒絕。176個本地連結、LF/單一EOF通過；前三批39個包/報告/收據/bundle byte與turn起點HEAD完全相同，其他96列候選題語義不變且原check/status/verdict保留。check:tasks驗1241票，只有既有無關scope警告。

- B37題名會限定FY2025/營業利益指標而非永久最賺；S31不沿用山峰沸點未重算值；T29只解市區街區方式與地番區別，不引用未核京都告示、韓國改革或全國占比；A41刪香腸故事與全部手機通用設定保證。
- 文字企劃包含長片大綱，無完整480秒逐字稿、付費生成、聽音/圖像/影片QA、正式匯入、核准、部署或上架。
