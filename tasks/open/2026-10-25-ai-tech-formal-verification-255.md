---
id: 2026-10-25-ai-tech-formal-verification-255
title: AI tech formal verification 255
status: in-progress
priority: P2
area: docs
owner: codex-ai-tech-news
claimed_at: 2026-10-25T18:54:39Z
created_at: 2026-10-25T18:54:29Z
completed_at:
branch: codex/ai-tech-formal-20261025
depends_on: []
scope:
  - docs/videos/claude-formal-verification-255
  - docs/videos/lexicon.json
---

# AI tech formal verification 255

## Why

跟進2026-10-22 Claude／Theorem程式形式驗證研究，以本片原創255邊界值和兩個完整有限域例子，讓一般科技觀眾能寫清接受／拒絕／返回條件，改對程式後讀懂保證範圍。依站主持續委派完成繁中加八外語，直接交後臺並續做下一支。

## Definition of done

- [ ] 正式稿、每項主張、完整RUN產物與原創圖互相對應；Jev／敘事／事實結果如實保存。
- [ ] 繁中主片及正文均至少八分鐘，自然旁白每句音檢、畫面與成片QA完成。
- [ ] en、ja、ko、es、pt、id、vi、th各有標題說明、CC、真正完成音檢與實測的可下載M4A；後臺讀回驗證。
- [ ] 交接未完成項與後臺實際核准狀態，沒有YouTube公開、合併或部署。

## Steps

- [x] 檢查本地／遠端／open PR／既有片及後臺登記候選，建立隔離worktree與窄範圍claim。
- [x] 六官方來源、七項YT文字參考及兩個真實GCC／SAT／有限控制圖例子落地。
- [x] 登記後臺並用正常Jev選大綱，依站主委派採用與記錄。
- [x] 正式稿／claims與獨立事實verify-2 PASS、原創圖及14張樣卡觀看；兩份新敘事各9/13未過，教學採用理由與NO保留。
- [ ] 正常TTS／音檢／渲染／合成／字幕／成片QA。
- [ ] 八語翻譯獨立審查、逐語合成與音檢、上架包及後臺檔案讀回。

## How to verify

`node /workspace/work/ai-tech-next/run-video-formal.mjs lint --slug claude-formal-verification-255 --json`、原生音檢與QA、`npm run test:docs-videos`及`npm run check:tasks`。資料以data/manifest.json及loop-manifest.json核對原始SHA，原生媒體收據綁最新來源與WAV雜湊；後臺正常工具讀回角色、大小與SHA，核准狀態另記。

## Notes

2026-10-25 18:54–18:55 UTC，who-is-on-it查本機worktree、遠端heads、open PR和main history無同scope競爭者；正式PR前重查。父分支DNS已含站主八語、推薦自主與完成續作規則，ForTy另由唯一producer製作，不交叉改動。有效頻道立場已正常GET讀回，套用2／3／4／6／7。

官方研究239入口／123庫，公開release60／25，本地兩個獨立案例各256輸入始終分列。未跑Rocq或vendor checker，guard不寫buffer；uint8窄化與循環有限圖模型範圍必須講清。0.25秒timeout只是一筆觀察。八語僅文字不稱完成。不建立假auto.json或伺服器核准；PR必貼no-auto-merge。


字典窄範圍例外（2026-10-25 19:11 UTC）：正常who-is-on-it再次核對lexicon.json。MCP教學舊claim已342小時，無本機／遠端／PR工作蹤跡；不釋放或改動他人票。唯一相關open PR #1851是同一協調者的ForTy，字典三個null新增已完成並推送a2a79e495，當前唯一producer只做既定八語I18N／音訊，不再改字典。第三片在635父的獨立worktree以原生mergeSharedLexicon及原生writer lease，只追加C／SAT／Rocq／RISC-V四個null原文詞，不更換任何既有發音值、不改ForTy或原repo字典。此為同一站主授權製作所需的例行發音處理，按明示範圍碰撞例外執行；不強制接手舊MCP任務。


20:07實際繁中TTS完成100 requests／105句／2423 billable chars。新speech c6d33c74584faac1，timeline16800/30=560.0s；片尾前547.7s、再排開場後522.7333s，都超過8分鐘。ASR初檢根session13610正在執行，沒有把完成TTS當音檢PASS或影片完成；最新nativecheck及強WAV對帳後再做定向修正。
