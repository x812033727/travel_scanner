---
id: 2026-10-20-brand-story-production-resume
title: Resume brand story production with verified local handoff and live readback requirements
status: in-progress
priority: P1
area: docs
owner: codex-gpt6-brand-resume
claimed_at: 2026-10-20T00:32:33Z
created_at: 2026-10-20T00:32:23Z
completed_at:
branch: codex/brand-story-resume-20261020
depends_on: []
scope:
  - docs/videos/brand-stories-resume-20261020
---

# Resume brand story production with verified local handoff and live readback requirements

## Why

站主要求繼續品牌故事系列，並授權使用影片工具裝置配對及完成工作後送 PR。新雲端 checkout 沒有正式主機媒體或影片權杖；須先辨識已開拍改編五集與 A01 r47 的現有進度，避免重複開拍或沿用失效收據。

## Definition of done

- [x] 驗證 A01 r47 編輯及六章包，不更改既有審稿內容。
- [x] 產生 52 句旁白與 50 場景逐鏡匯出，完整保留 54 筆 PENDING 主張關聯。
- [x] 由獨立審查者確認匯出一致性與待決發布差異。
- [ ] 影片工具完成站主裝置配對，唯讀核對正式工作進度與成本。
- [ ] 依可用的精確版本與預算關卡接續製作，記錄實際結果；仍需外部條件時明確交接。
- [ ] 提交 PR；製作未完成時保留此票，不把離線資料當成成片驗收。

## Steps

- [x] 讀 brand-story、youtube-video/story 與 task-board 規範；比對原試作及改編五集票。
- [x] r47 兩個 builder --check exit 0，新增匯出 builder --check exit 0。
- [x] 獨立審查發現並修正 12 項 metadata 差異漏報、TSV 主張對應遺漏，修正後 PASS。
- [x] HTTPS Git origin 可讀；GitHub GraphQL Forbidden，改以受支援的 REST 讀取 open PR 清單成功，沒有同一新增 scope 的工作。
- [x] 使用 main 的 home override 指向 checkout 外的私有目錄發起裝置配對，短碼不寫進 Git。
- [ ] 站主按允許後讀回並處理下一個真實阻塞。

## How to verify

```bash
node docs/videos/brand-stories-resume-20261020/build.mjs --check
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-editorial-candidate-20261019-r47/build.mjs --check
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-worker-handoff-r47-canonical-20261019/build.mjs --check
npm run check:tasks
```

## Notes

- 新交接在 docs/videos/brand-stories-resume-20261020。原 A01 試作票及其他持有者的票保持原樣。
- 站主明確回覆：「可以接影片工具權杖配對你自己做完傳PR」。沒有要求自動合併或跳過成片看片。
- 原 r47 兩位敘事讀者及 canonical conversion 均 PASS；54 個歷史主張仍 PENDING，實際音訊正文 420–480 秒未驗收。不得捏造 worker script-review 或已聆聽收據。
- curl 對 mokaair.com 曾 CONNECT 403；以既有 CLI 加 Node 環境代理支援後成功取得裝置配對，等待站主允許。環境草稿已另保存 mokaair.com、api.github.com 域名；草稿不代表已發布。
- 目前未匯入、未付費生成、未變更正式設定、未上傳。每片 US$25 所有項目合計上限保留。
