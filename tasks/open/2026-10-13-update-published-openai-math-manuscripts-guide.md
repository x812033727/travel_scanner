---
id: 2026-10-13-update-published-openai-math-manuscripts-guide
title: Update published OpenAI math manuscripts guide with first-party corrections
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-13T07:39:48Z
completed_at:
branch: codex/news-hourly-review-20261013
depends_on: []
scope:
  - docs/openai-math-manuscripts-update-2026-10-13.md
---

# Update published OpenAI math manuscripts guide with first-party corrections

## Why

正式站已刊五語文章 `ai-news-openai-math-manuscripts-20261006` 報導 OpenAI 最初發布 722 份數學手稿。後續 TechCrunch 10/08 對數學界審查標準有更新角度，OpenAI 10/07 repo 修訂後現存 719 份。重複候選 `62a29197-da43-4d14-a30d-8a3f8aca341f` 已在 2026-10-13 退件，因其五語稿顛倒「已形式化」比例且事實查核未過；有價值的後續事實應審慎更新既刊稿，而非另發錯誤第二篇。

## Definition of done

- [ ] 既刊 Guide 五語保留最初 722 份發布時點，另外準確交代 10/07 撤回 3 份、現存 719 份與 14 份修補；不混為同一時間點。
- [ ] 對 OpenAI 官方 repo、公告、AGMAI 聲明與自然語言／Lean 證明原始論文逐句查核新增主張，清楚分開 OpenAI 自述、數學界保留意見及正式驗證結果；五語各更新、保存並走原有審稿／發布流程。
- [ ] 五語已發版本、稽核紀錄與五個公開頁的修正句逐一讀回；未過關不能稱已完成。

## Steps

- [ ] 記錄既刊五語目前版本、原句與來源快照，核 722／719／300、10 份 reasoning summaries 的單位及 Institute for Advanced Study 非 Princeton University 附屬關係。
- [ ] 比對 [OpenAI repo 修訂紀錄](https://github.com/openai/math/blob/main/history.md)、[OpenAI 公告](https://openai.com/index/sharing-ai-progress-in-mathematics/)、[AGMAI 聲明](https://agmai.org/)與 [Lean 落差研究](https://arxiv.org/abs/2610.08144)，僅納入可由一手來源支持的新增內容。
- [ ] 經管理介面修五語並重新查核，按每語已發版本／公開頁讀回；將執行證據寫入 `docs/openai-math-manuscripts-update-2026-10-13.md`。

## How to verify

從 `/zh-TW/admin/guides` 找到既刊 `ai-news-openai-math-manuscripts-20261006`，讀五語保存稿、版本與稽核；編輯後走現有審稿／發布；打開 `https://mokaair.com/{zh-TW,zh-CN,en,ja,ko}/life/ai-news-openai-math-manuscripts-20261006` 核發布修正句與正確來源、日期。初次 429 不能算通過，可限速重試。

## Notes

退件候選的五語預覽把「300/719 約 42% 已形式化」寫成 42% 未形式化，也把 10 份推理摘要寫成 10 份手稿附完整思考過程；這些錯句不可從退件草稿複製。TechCrunch 的評論有獨立更新價值，但單一評論不能取代一手驗證。此票涉及已發文章，不能從本地文件修改推論正式站已更新。
