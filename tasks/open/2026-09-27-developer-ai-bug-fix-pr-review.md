---
id: 2026-09-27-developer-ai-bug-fix-pr-review
title: Developer AI bug fix PR review video
status: in-progress
priority: P2
area: docs
owner: codex-video-bug-fix-continuation
claimed_at: 2026-10-08T00:18:55Z
created_at: 2026-09-27T15:26:33Z
completed_at:
branch: codex/ai-bug-fix-review-20261008
depends_on: []
scope:
  - docs/videos/ai-bug-fix-pr-review
---

# Developer AI bug fix PR review video

## Why

開發者篇第二支以同一份真實修補示範：舊測試全綠仍漏了非整除案例，AI 修補須依需求、實際差異與回歸驗收三關審查。

## Definition of done

- [x] `docs/videos/ai-bug-fix-pr-review/` 有企劃、完整口播與畫面資料、主張表，且示範與同題修補的實際差異和測試相符。
- [ ] 獨立查核通過，完成合成旁白、五語字幕、縮圖、成片與待上架包。

## Steps

- [x] 用舊碼與保留的本地修補，建立可重跑的三關審查示範；歷史 Claude 作者歸因不當作已驗證證據。
- [x] `video.json` 避免把本地示範說成正式站事故或已合併的 PR；`lint` 零錯誤零警告。
- [ ] 獨立查核後跑後續媒體管線與品檢。

## How to verify

`node tools/video/cli.mjs lint --slug ai-bug-fix-pr-review`；交叉核對 `../ai-coding-tools-same-task/demo/claude.patch` 與 `acceptance.test.mjs`。

## Notes

2026-09-27：起始程式 2 個舊測試全過，但 100 分分三人只得 99；事後四類驗收在起始碼 1/4、修補後 4/4。片中單位統一為「分」。遠端審核及 TTS 尚未執行。
2026-09-28：獨立 verify-1.md 與兩支工具的原始修補、測試輸出已交叉核對；五語字幕經獨立交叉審稿，28 張字卡與縮圖已目視檢查。TTS、成片、品管、審核及上架包仍待完成。
2026-09-28：Gemini Sulafat 旁白完成，`check-audio` 133/133 句、零標記；改寫的七句已同步五語字幕並經獨立覆核，`lint` 零錯誤零警告，最終成片重組中。站主大綱核准、正式站審核、11 項品管與待上架包尚待完成。
2026-09-28：新版 1080p `final.mp4` 完成，18,255 影格、約 10:08、-14 LUFS；`checks.json` 全過且無問題。五語字幕已按最終時間軸重產。待站主大綱核准及正式站各審核關卡。
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by codex-video-review (since 2026-09-27T16:32:36Z) was stale and is released so it stops locking its scope. Landed: #868. Still open: Independent check passed; synthesized narration, five-language subtitles, thumbnail, final cut and upload pack; Run the rest of the media pipeline and QC after the independent check.

2026-10-08：從未被其他 worktree／open PR 持有的既有佇列續作。舊稿與四語對 #868 的完整 bytes 相同，133 IDs／28 場景；原稿及語言 snapshot 保留在 repo 外。第二輪全稿 261 項發現七處 Claude 歷史歸因 NOT FOUND，原 CLI 命令、JSON 與退出紀錄仍未找到，沒有重新呼叫工具來製造歷史證據。

2026-10-08：現稿修正五句旁白、四處字卡及官方來源確認日期；第三輪換新覆核者全查 261 項，零 unresolved current facts，source SHA256 `7cddf570305b4afa8d87833aec8fac92ab3469648674fd6d17d085fd0dffe0d4`。本地 demo 再次重現起始 2/2、事後驗收 1/4 expected red、保留 patch 後 13/13。en／ja／ko／zh-CN 用原生 sheet／merge 同步五句，獨立 delta 20/20 通過，每語 133/133 source current、128 whole entries 及 metadata 完整保留。報告與來源清單見 `verify-2-20261008.md`、`verify-3-20261008.md`、`caption-delta-review-20261008.md`。

2026-10-08：最終 `lint` 0 errors／0 warnings，估計 10.2 分鐘。免費 render 28 張 1080p 字卡、contact sheet、縮圖與轉場完成並目視檢查。四語縮圖文字未新增，沿用主縮圖 fallback。這不是音訊／timed CC／成片驗收。

2026-10-08：9/28 成片完成筆記保留。預設影片路徑、已知工作目錄及 G 槽交付索引有限查找未找到原媒體，不能推論從未付費或已刪除。最終原生 TTS dry-run 實際為 28 requests／28 pending、4041 characters、gemini:Sulafat ready，只有 readiness GET、沒有 synthesis POST。已請站主提供舊媒體路徑；重買授權尚未取得。完整媒體 DOD 保持未完成，後續依 `CONTINUATION-20261008.md` 驗證找回媒體或取得重做授權後再續跑，禁止盲目重試不確定請求。沒有合併、部署、上傳或發布。

2026-10-08 10:09（台北）：站主在上述具體預檢後再次要求「繼續」，已授權本片新版主旁白與後續品檢製作；未釋出其他影片的 hold。新版 133 句音檔已合成，兩筆 Windows 本地寫入失敗均從完整已回答 bytes 恢復，沒有重送已回答或未知請求。畫面節奏修整為 47 場景／88 狀態，原生時間軸 17,881 frames／596.033 秒，零計費 refresh 與 canonical render 均 exit 0，最長靜態狀態 13 秒。現稿 SHA256 `4608bffb664b8d5a99667daae019184750b73fdaefe32256b08c0494f88c6cca`；新的獨立 `verify-4.md` 全查 350 項、零 unresolved，保留 dated 前輪原報告與來源 metadata。

2026-10-08 10:09（台北）：主轉寫 133/133 完成，98 exact／18 same-sound 或 filler／4 Jev pass／13 flags。第二套離線盲轉寫在 36 分鐘逾時，保留實際完成的八句結果，並核對及補查其餘五句；尚未通過旁白品檢。普通重錄 dry-run 最多 13 句／12 requests／256 billable characters，未執行這批重錄。成片、timed CC、待上架包及音訊／成片核准均仍未完成；正式站本片語言選擇仍未決定，不把四語文字草稿當成已核准配音或字幕。Draft PR #1375，沒有合併、部署、上傳或發布。實際階段與私有收據見 `CONTINUATION-20261008.md`。
