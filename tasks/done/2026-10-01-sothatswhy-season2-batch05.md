---
id: 2026-10-01-sothatswhy-season2-batch05
title: 原來如此第二季第五批：B46 S32 T41 A40 製作包與獨立審稿
status: done
priority: P2
area: docs
owner: codex-sothatswhy-batch05
claimed_at: 2026-10-01T07:15:45Z
created_at: 2026-10-01T07:15:42Z
completed_at: 2026-10-01T07:36:24Z
branch: codex/sothatswhy-season2-batch01
depends_on:
  - 2026-09-29-so-that-s-why-vet-the
scope:
  - docs/videos/so-thats-why/season2/B46.md
  - docs/videos/so-thats-why/season2/S32.md
  - docs/videos/so-thats-why/season2/T41.md
  - docs/videos/so-thats-why/season2/A40.md
  - docs/videos/so-thats-why/season2/reviews/batch05/
  - docs/videos/so-thats-why/season2/batch05-packaging.json
  - docs/videos/so-thats-why/season2/validate.mjs
---

# 原來如此第二季第五批：B46 S32 T41 A40 製作包與獨立審稿

## Why

接續使用者「繼續」，從其餘84題選便利貼、海水鹽分、飛機菸灰缸與網址www，補四份可追溯的文字企劃，累計16到20題；沿用草稿#1075。已比對第一季、第三季、品牌100與AI名詞，無相同問題。S32不是第一季杜拜淡化水題；T41不重寫遮光板或禁菸歷史；A40不改寫HTTPS或網域後綴故事。

## Definition of done

- [x] 四包有2026-10-01直接讀原來源與限制、前提/備註4000/2000欄位、六章480秒、各兩支180–220單位Shorts、原創提示/AB縮圖及15組五語標題說明。
- [x] 不同原作者獨審事實、聽眾文字與五語，修正閉合，報告及收據綁final byte SHA256。
- [x] 五批validator和漂移拒絕通過；前四批52個包/報告/收據/bundle byte不變，索引只改本四列並保存check/status/verdict。
- [x] README和母票記20/100、其餘80題未決；批次票在草稿結案，母票保持開放並釋出。

## Steps

- [x] 查分支/worktree/遠端/PR及main範圍歷史，去重並claim母票與本批窄scope。
- [x] 今日重讀一手來源並寫四包，刪未核數字/歷史/全球通則。
- [x] 交叉事實、聽眾文字與五語獨審，重綁最終SHA收據。
- [x] 五批validator、漂移fixture、連結/字元/票務/staged whitespace；提交並更新同一草稿。

## How to verify

node docs/videos/so-thats-why/season2/validate.mjs（預設batch01及--batch=batch02至batch05）；npm run check:tasks；git diff --cached --check。機械檢查不替代原始來源及獨審，不代表媒體或站主驗收。

## Notes

- 完成focused驗收：五批validator PASS；isolated valid exit0，正文/報告/bundle漂移均exit1且有對應拒絕原因，未知batch exit1。192個本地連結、LF及單EOF通過；前四批52份包/報告/收據/bundle與本turn起始HEAD byte相同，其他96列候選題語義未改、原check/status/verdict保留。check:tasks驗1242票通過，現存無關stale/scope警告未動。
- B46 root獨讀NIHF三原頁及可讀的品牌英國官方歷史；作者美國品牌頁web可讀，root重取逾時與英國旁證界線寫進報告，黃色故事仍明標品牌歸屬。S32無必要修正；T41繁體錯字已閉合重讀、無FACT變動；A40無必要修正。
- 長片只有六章大綱，無完整逐字稿。無付費生成、實驗、人聽/圖像/成片QA、正式匯入、核准、部署或上架。原候選查核索引不當本日證據；若須更正舊報告另開票。
