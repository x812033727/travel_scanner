---
id: 2026-10-01-b37-fy2025-evidence-rounding
title: B37 原題查核摘要：修正 FY2025 AWS 億美元約數
status: done
priority: P3
area: docs
owner: codex-b37-evidence
claimed_at: 2026-10-01T07:00:11Z
created_at: 2026-10-01T07:00:10Z
completed_at: 2026-10-01T07:07:23Z
branch: codex/sothatswhy-season2-batch01
depends_on: []
scope:
  - docs/videos/so-thats-why/topic-checks/s2-B26-B38.md
---

# B37 原題查核摘要：修正 FY2025 AWS 億美元約數

## Why

第四批製作發現原B37答案寫457億美元，與同節原表456.06億不一致。新包採正確原值；原查核入口也要修正以免下一位續用。

## Definition of done

- [x] 重讀FY2025 SEC Note10及官方2026-02-05全年業績，45,606百萬美元=456.06億，整億約數456。
- [x] 只改B37答案約數並留本日更正/未重查範圍，其他B26–B38題及原表不改。
- [x] 不同作者覆核單位與原表，連結、票務、whitespace檢查通過，與第四批草稿同PR結案。

## Steps

- [x] 查分支/遠端/PR/main，who-is-on-it顯示該scope無active task或open PR，claim精確單檔scope。
- [x] 精確摘要更正及製作包入口；2026H1和起源段不充作本日已核。
- [x] 獨立數字覆核，check:tasks與staged diff通過，done並推草稿#1075。

## How to verify

原SEC https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm Note10的2025 AWS operating income45606（millions）；公告 https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Fourth-Quarter-Results/ Full Year2025 $45.6b。diff僅B37答案457→約456及一條有日期補註；npm run check:tasks；git diff --cached --check。

## Notes

- 完成focused驗收：四批validator全部PASS；isolated positive exit0，正文/報告/bundle漂移各exit1，未知batch拒絕。176個本地連結、LF/單一EOF通過；前三批39個包/報告/收據/bundle byte與turn起點HEAD完全相同，其他96列候選題語義不變且原check/status/verdict保留。check:tasks驗1241票，只有既有無關scope警告。

- 2026-10-01 write_b26只讀覆核兩處PASS：原10-K45606百萬美元÷100=456.06億，整億四捨五入456；datednote明確未重核H1/起源，新包只採FY2025。覆核者未修改本檔。

- 公開文字證據修正，沒有發佈/正式匯入或投資建議。原始checked/check歷史來源保留；非全份題庫再驗。
