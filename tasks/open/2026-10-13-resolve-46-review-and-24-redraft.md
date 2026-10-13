---
id: 2026-10-13-resolve-46-review-and-24-redraft
title: Resolve 46 review and 24 redraft hourly news backlog
status: in-progress
priority: P1
area: ops
owner: codex-news-hourly-backlog
claimed_at: 2026-10-13T05:49:41Z
created_at: 2026-10-13T05:49:35Z
completed_at:
branch: codex/news-hourly-review-20261013
depends_on: []
scope:
  - docs/news-hourly-backlog-2026-10-13.md
---

# Resolve 46 review and 24 redraft hourly news backlog

## Why

正式站 AI 每小時新聞在 2026-10-13 13:46（Asia/Taipei）有 46 筆待審查、24 筆需重寫／失敗；來源漂移、查證與翻譯錯誤、舊稿重複及 provider 故障混在同一佇列。站主明確授權處理這 70 筆，也要求沿用既有 draft PR #1480。逐篇判斷及稽核證據記在 [`docs/news-hourly-backlog-2026-10-13.md`](../../docs/news-hourly-backlog-2026-10-13.md)。

## Definition of done

- [ ] 70 個基線候選各有可核實的終態（發布／退件）或明確的原因、持有人與可執行的後續票；沒有把新候選、未完成 judge、待查來源或舊 worktree 狀態混算。
- [ ] 發布的每篇經候選／run／稽核及公開語系讀回；保留審查與 redraft 不靠整批 retry 或無旗標 backfill 跳過關卡。
- [ ] 本名冊與既有 draft PR #1480 同步，票在 PR 內完成；未經站主同意不把 draft PR 合併／部署當作任務完成。

## Steps

- [x] 固定 2026-10-13 13:46 的 46／24 基線及 70 個候選 ID，區分 `manual_review`／`shadow_review`、`needs_redraft`／`failed` 與來源障礙。
- [x] 人工退件十個有明確重複／過時／證據不足原因的候選：Sonnet 5.5、Morning Minute／Drake、XRP Ledger 延期、Ledger／CryptoBilis、Google Vids、Gemini coworker agent、OpenAI／澳洲舊稿，以及 Evernorth、Pleterski、澳洲聽證三筆舊預告；逐筆讀回候選及稽核。
- [x] 修 Drake `b0825fb1…` 與 XRP Ledger `5186a9c9…` 的指定三語錯句／表格；各送一次重新查核，後台已發布清單讀回，公開頁讀回範圍見名冊。
- [x] Falcon ASR `6384736e…` 五語各補官方來源表格並送一次重新查核；後台已發布，四語公開表格讀回，ja 429 待補驗。
- [x] Kalshi `cf07bd04…` 五語修正過度陳述並重查；目前回到待審，卡 CoinDesk 正文／作者頁差異及不可讀的 `/markets` 導覽頁。
- [x] Flock `7bea807c…` 五語補當事公司回應並重新查核；候選已發布，五語公開 H1／公司回應讀回。
- [x] NVIDIA Astra `e69d8fbc…` 唯一官方來源刷新、繁中標點修正，候選已發布，五語公開 H1／8 倍主張讀回。
- [x] Citrix `dcc3116c…` 日文指定錯句已修、單篇重查並刷新唯一 Google Cloud 正文；新事實、五語及 Jev 審查通過，候選已發布，五語 H1／規則包名／DTLS／UDP 443 讀回。EvoLib `c5912455…` 同一 Microsoft 正文刷新後仍反覆顯示來源變更，不盲目重送。
- [x] AEMA `e0e959d9…` 核唯一 NVIDIA 官方正文與既刊 DSX 不重複，留稽核原因後單次刷新來源；候選已發布，四語公開 H1 讀回、ko 429 待補驗。
- [x] Google Genesis `6cbc274d…` 的 7 月舊公告與 Project Suncatcher `f8830a55…` 的同日已刊發射／來源數字更正，逐筆以具體理由退件並在「已退件」清單讀回；固定基線此時 7 發布、12 退件、51 尚待終態。
- [x] EvoLib `c5912455…` 本地用原生解析器重現 `msr-promo` 推廣卡輪替造成假正文漂移，精確排除後兩次 body hash 穩定；交既有動態 widget 修復票，不再盲刷來源。
- [x] Meta Connect 直播稿 `89156804…` 與同批固定總覽高度重複，且混入導覽／作者頁及未通過事實查核；填具體稽核原因退件、讀回「已退件」。固定總覽候選仍須補官方一手證據及修五語。
- [x] Anthropic ART `2cb24617…` 五語 FAQ／提示框去除超出 9/23 一手來源的現在式斷言，各存草稿並單篇重新查核；後台讀回 AI 代審「發布」與候選已發布，Guide 韓文已發版本 6、五語公開 H1／開頭／重點摘要讀回。
- [x] Apollo 存款推論 `d266ad56…` 查出 1 萬美元按 3.3%–5% 年息應是 330–500 美元，唯一來源及五語稿卻都寫 100 美元；Orchard `77a835d1…` 為 8/03 舊公告、Decrypt 監管回顧 `2c3e35f7…` 為 9/26 舊分析且後有 10/05 CFTC ANPRM。三筆各留稽核理由退件並讀回。
- [ ] 補已發稿的終態 run、稽核、已發版本及尚缺的公開全文證據；釐清 Kalshi 導覽頁與 EvoLib 動態來源障礙。
- [ ] 分批處理剩餘的明確翻譯／事實問題、來源變更與固定基線尚存 15 筆 redraft／failed，將每次人工決定及其讀回更新名冊。
- [ ] 對無法安全完成的來源抓取、provider 未知結果或程式障礙建立精確後續票並標出持有人，再核對最新佇列與基線 70 筆逐一結案。

## How to verify

在正式站 `/zh-TW/admin/news` 依名冊候選 ID 開詳情，核候選狀態、原因、人工決定及 run 結果；對發布候選從詳情逐一開五語前台連結，核 H1、修正句與 Guide 版本。用當次查到的正式站數字和固定 70 ID 名冊比較，不從計數差推導逐筆成果。本地 `npm run check:tasks` 驗票格式；PR #1480 的 CI／merge／deploy 狀態需另外讀回。

## Notes

此票僅 claim `docs/news-hourly-backlog-2026-10-13.md` 的 repo 內容範圍；舊 worktree／舊票仍由他人持有，不動它們。正式站 SSH `plink` 被本次環境的自動審核阻擋，沒有改用其他通道重送；後台 UI 的「重新查核」是非終態，Anthropic 已另作終態讀回。`retry` 可能重起付費撰稿並清掉人工決定；French OAuth 失敗的實際付費結果未明，先核 run／RQ／供應商收據。2026-10-13 14:53 的全站 UI 為待審 31、需重寫 15、已發布 604、已退件 955，佇列流動，不能直接用差額結案；固定 70 ID 名冊是 8 發布、16 退件、46 未有終態。名冊逐項寫了來源 URL 導覽頁、CFTC 官方 HTTP、翻譯失敗、重複及 AI judge handback 的不同處理方案。
