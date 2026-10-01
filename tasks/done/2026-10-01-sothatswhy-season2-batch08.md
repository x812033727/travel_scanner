---
id: 2026-10-01-sothatswhy-season2-batch08
title: 原來如此第二季第八批：B50 S36 T45 A39 製作包與獨立審稿
status: done
priority: P2
area: docs
owner: codex-sothatswhy-batch08
claimed_at: 2026-10-01T10:14:22Z
created_at: 2026-10-01T10:13:59Z
completed_at: 2026-10-01T10:41:49Z
branch: codex/sothatswhy-season2-batch08
depends_on:
  - 2026-09-29-so-that-s-why-vet-the
scope:
  - docs/videos/so-thats-why/season2/B50.md
  - docs/videos/so-thats-why/season2/S36.md
  - docs/videos/so-thats-why/season2/T45.md
  - docs/videos/so-thats-why/season2/A39.md
  - docs/videos/so-thats-why/season2/reviews/batch08/
  - docs/videos/so-thats-why/season2/batch08-packaging.json
  - docs/videos/so-thats-why/season2/validate.mjs
---

# 原來如此第二季第八批：B50 S36 T45 A39 製作包與獨立審稿

## Why

接續使用者「繼續」，從剩餘72題選B50 KFC聖誕商品、S36乾燥情境靜電門把、T45日本計程車自動門、A39兩步複製貼上，補四份文字企劃，累計28到32題。已對第一季、第三季、品牌100及AI名詞完整題庫比對核心問題與例子。母票持有索引，本票限定四包及本批審稿、bundle、validator映射；第七批PR#1079外部轉待審後，本批另開分支與草稿，前七批原包不改。

## Definition of done

- [x] 四包有2026-10-01直接讀來源與限制、前提/備註4000/2000、六章480秒、每包兩支180–220單位Shorts、18個原創提示與15組五語標題說明。
- [x] 不同作者獨審事實、聽眾文字與五語；修正閉合，報告和收據綁final byte SHA256。
- [x] 八批validator及漂移拒絕通過；前七批91份包/報告/收據/bundle byte不變，索引只改本四列並保存原check/status/verdict。
- [x] README及母票記32/100、剩餘68題待審選；本批在草稿結案，母票保持開放並釋出。

## Steps

- [x] 核對worktree/branch/remote/PR及main範圍歷史、去重，claim兩票並分配作者。
- [x] 重讀一手來源、寫四包；歷史商品、車款及編輯故事保留日期與來源範圍。
- [x] 交叉事實、聽眾文字及15組五語獨審，修正後重讀，收據綁最終SHA。
- [x] 八批validator、漂移fixture、本地連結/字元、票務及staged whitespace通過，提交並開第八批草稿。

## How to verify

node docs/videos/so-thats-why/season2/validate.mjs（預設batch01及--batch=batch02至batch08）；npm run check:tasks；git diff --cached --check。來源、獨審、原包byte保留與索引四列另驗；文字檢查不是媒體或站主驗收。

## Notes

- 四份獨審均FACT0；S36一處來源段落定位、T45一處簡中字形、A39三項非FACT（四處）修正均作者閉合、審稿全文/15語重讀後綁final byte。B50無待修項。純旁白最長含句內標點均≤40字元；A39 C/V/Mac的字母與詞彙發音仍待真實音訊、人聽。
- 八批validator PASS，isolated valid exit0、正文/報告/bundle漂移各exit1且原因正確，未知batch exit1；243個本地Markdown連結、LF與單EOF通過。前七批91檔逐byte保留，索引只有B50/S36/T45/A39四列變更，其他96列與原100 IDs/check/status/verdict保存。窄化及換角度原因寫回100題入口，不將原問題的未核部分當已回答。
- 提交前再次核對：#1079仍OPEN非draft、head d6180df4，母PR#1073 OPEN/head7c31e842。第八批從前者HEAD獨立草稿，base使用codex/sothatswhy-season2-batch07；沒有推動/合併第七批或母PR。票務及staged whitespace為提交前最後檢查。
- Windows tasks done已寫done副本但留下open副本、exit1。已驗證兩個絕對路徑在workspace內，done狀態/完成時間有效，兩副本除status及completed_at外全文相同，才刪精確舊open檔；done完整保留。母票release成功，status open且owner/claimed_at空白。
- 歸檔及release後check:tasks exit0，Validated 1245 task files；既有不相干stale/scope警告未更動。

2026-10-01開工：#1079仍OPEN draft，head d6180df4/base codex/knowledge-story-backlog；母PR#1073 OPEN，母分支7c31e842，前六批#1075已併母分支但尚非main。origin/main更新b03e938e，scope歷史無新落地；沒有其他active task/遠端branch/worktree/PR佔用本scope。保留使用者未追蹤.codex/environments/。

開工後再核對#1079已由外部改為非draft、autoMergeRequest為null，head仍d6180df4。不覆寫其審查範圍或狀態；本批從此HEAD切codex/sothatswhy-season2-batch08，既有未提交內容完整保留。提交前再次核對母分支及#1079，以當下已驗證狀態選草稿base。

B50只採品牌官方1974活動/1985商品資料，不選起源逸事或2026預訂；S36限定材料與乾燥條件，不把臺灣冬季普說乾燥。T45以協會與JNTO今日乘客指引及Toyota有日期車款例子，刪未一手證明的1959/1964/1967起源及90%市占。A39講兩步編輯，Gypsy專用鍵不當Ctrl+C/V發明；刪字母形狀與鄰鍵動機。

長片仍為六章企劃，完整逐字稿另作。無付費生成、人聽/圖片/成片QA、正式匯入、核准、部署或上架。原topic-checks保存，需更正另開精確scope票。
