---
id: 2026-10-01-sothatswhy-season3-production-packages
title: 原來如此第三季：把已查核候選題整理成製作包
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-01T04:54:17Z
completed_at:
branch:
depends_on:
  - 2026-09-29-so-that-s-why-vet-the
scope:
  - docs/videos/so-thats-why/season3/
  - docs/videos/so-thats-why/season3-topics.json
---

# 原來如此第三季：把已查核候選題整理成製作包

## Why

`docs/videos/so-thats-why/season3-topics.json` 保存 B/S/T/A 51–75 共 100 個第三季候選題，題目查核已完成。但沒有第一季那種逐集完整製作包，亦沒有獨立接續票。這張票把舊企劃留下的文字工作排回隊列，P3 保留在試片與第二季準備之後的優先序；第二季未完成不妨礙獨立題目的文字整理，故不加不必要的相依。

## Definition of done

- [ ] `season3/README.md` 記 100 題的原 id、查核報告、採用／延後／換角度／不採用處置與理由、批次及包入口；沒有未決處置才結案。
- [ ] 採用的題目各有 `season3/<id>.md`，格式與第一季完整包一致：來源及確認日期、主張限制、7–9 分鐘章節大綱、畫面／縮圖注意事項、兩支 35–55 秒 Shorts 稿、長短片標題／說明、可貼進後台的前提與備註。
- [ ] 五語包裝與 proposed 排序單獨存在 `season3/`；不沿用第二季發布日期，不改前兩季題號或第一季排程。
- [ ] 跨季重複有明確處理、不同代理完成查核與聽眾審稿；新增事實重新找一手來源，候選題的 `check` 入口與包／審稿收據可追溯。
- [ ] `season3-topics.json` 回寫包入口／處置，保留原查核；延後題清楚列出重新評估條件。沒有實際媒體與平台驗收時維持文字包狀態。

## Steps

- [ ] 查 collision 後 claim；讀 youtube-video 技能、題庫的 `check` 與第一季完整包。
- [ ] 對第一季、第二季、品牌故事、AI 名詞去重；特別記 S55/S50、A70/A29/A30、A58/A38，與第二季採用紀錄核對。
- [ ] 先記題目處置與小批次 id；逐批補大綱、兩支 Shorts、五語包裝與貼用文字，不一次留下大量未落地稿。
- [ ] 新增或漂移的主張重新查核；不同代理審稿，保留內容雜湊與修正紀錄。需要改 `topic-checks` 時另開精確 scope 票。
- [ ] 審核所有題目處置、包完整性與長度，回寫 README／題庫入口；發布日與成片製作留給實際批准的後續批次。

## How to verify

`npm run check:tasks`；題庫 JSON 可解析、100 個原 id 完整且無重複；逐一驗包與原查核路徑、五語包裝、前提／備註符合 `DramaRequestIn` 當前上限（舊規格 4,000／2,000 字元）、兩支 Shorts 稿與審稿收據。查不到來源的說法不能進稿；候選題 `checked` 不改成 `published`。

## Notes

- 2026-10-01 補票，依據已完成的 `2026-09-29-so-that-s-why-vet-the`。本次只恢復待辦，未查核新主張或生成影片。
- 原查核留下的易錯點（例如日本快門聲屬業界慣例、Pepsi 海軍傳說）由各題 `check` 報告承接，不把查核前版本帶回稿子。
- 選題處置與完整包是本票成果；付費生成、正式設定／匯入、排程、上架須有對應具體授權。
