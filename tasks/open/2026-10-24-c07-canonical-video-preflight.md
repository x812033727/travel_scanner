---
id: 2026-10-24-c07-canonical-video-preflight
title: Prepare C07 canonical video project without paid calls
status: in-progress
priority: P1
area: docs
owner: codex-c-series-integration
claimed_at: 2026-10-24T02:25:08Z
created_at: 2026-10-24T02:24:44Z
completed_at:
branch: codex/c07-canonical-video-preflight-20261024
depends_on: []
scope:
  - docs/videos/story-everyday-dr-martens-c07/video.json
  - docs/videos/story-everyday-dr-martens-c07/series.json
  - docs/videos/story-everyday-dr-martens-c07/brief.md
  - docs/videos/story-everyday-dr-martens-c07/claims.md
  - docs/videos/story-everyday-dr-martens-c07/verify-1.md
  - docs/videos/story-everyday-dr-martens-c07/reviews/canonical-video-preflight-20261024.md
---

# Prepare C07 canonical video project without paid calls

## Why

C07 已有站主核准的 73 句逐字稿與 73 鏡文字方向，但尚無後台影片工具讀取的 canonical video project。建立機器檔時必須保留原核准雜湊、來源審查與付費停線，不能把紙上時長或費用核准當作已能製作的證據。

## Definition of done

- [x] 新增可供影片工具讀取的 C07 video.json、series.json、brief.md、claims.md 與既有查核的 QA 對接檔。
- [x] 73 句核准原文可從機器檔的場景逐字還原；原 script.md、visual-plan.md、production-quote.md SHA-256 不變。
- [x] 非付費 lint 零錯誤；留下具體警告、估時和付費停線收據。
- [ ] 單集可歸因預算路由、實際配音／圖片／成片驗收由後續製作任務處理，不在本票啟動。

## Steps

- [x] 對 73 句與 73 鏡配對；四句紙上超過單鏡上限、一句需保留核准鏡頭硬切，只在標點分段，核對串回後的文字與原句一致。
- [x] 按 current schema 建立 78 個場景、68 張規劃插圖與 10 張後製字卡；來源和圖像提示詞保留事實界線。
- [x] 把既有 v12／v11 來源 PASS 映射到 QA 可讀檔，不冒稱新的獨立審查。
- [x] 明列 73 句原報價與 78 個 TTS 製作片段的費用對帳缺口。

## How to verify

- `node tools/video/cli.mjs lint --slug story-everyday-dr-martens-c07`：0 errors；原稿與紙上鏡頭仍有 24 warnings，詳見前製收據。
- 逐 ID 將 video.json 的 text 串回 script.md：73／73 相同；16 個 say_for 雜湊有效。
- `Get-FileHash` 核對三份受核准綁定的原件雜湊；`git diff --check`。
- `npm run check:tasks`：exit 0，僅列出原看板中過期 claim／重疊 scope 警告。核心 schema／lint／story／curio 的 81 項目標測試全過；完整 `npm run test:docs-videos` 進入與本集無關、每例耗時數十秒的多語音軌測試後中止，不宣稱全套通過。
- `factsChecks` 讀取本集 `verify-1.md`：PASS，沒有仍被場景引用的 NOT FOUND 主張。

## Notes

- `category: story` 加 `cute-mystery` 時，現行 core/drama.mjs 不允許 stats 字卡；與 C03 相同，C07 以 `category: explainer` 保持字卡 schema 有效，系列身分由 series.json 的 `kind: story` 保留。後台正式匯入時應讀回分類顯示及系列關聯。
- 五句分段使機器場景和 TTS 片段由原報價 73 增為 78；任何付費請求前需重新核價、部署可歸因預算路由、核對既有費用，並實測片頭後正文純語音至少 480 秒。圖片及成片另外驗收插圖時間至少 70%。
- `reviews/canonical-video-preflight-20261024.md` 是詳細非付費收據；本票不授權匯入、上傳或發布。
