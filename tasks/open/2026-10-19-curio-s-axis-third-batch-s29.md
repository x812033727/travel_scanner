---
id: 2026-10-19-curio-s-axis-third-batch-s29
title: Curio S axis third batch: S29 Cao Chong weighs the elephant, S14 Musashi at Ganryujima, S26 let them eat cake
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-history-stories
claimed_at: 2026-10-19T22:13:18Z
created_at: 2026-10-19T22:13:17Z
completed_at:
branch: claude/curio-s-batch2
depends_on: []
scope:
  - docs/videos/curio-s29
  - docs/videos/curio-s14
  - docs/videos/curio-s26
  - docs/videos/history-curiosity/topic-checks/S29.md
  - docs/videos/history-curiosity/topic-checks/S14.md
  - docs/videos/history-curiosity/topic-checks/S26.md
---

# Curio S axis third batch: S29 Cao Chong weighs the elephant, S14 Musashi at Ganryujima, S26 let them eat cake

## Why

站主 2026-10-19：「繼續新集數，用推薦的選擇就好不用問我，有額度就一直做下去吧」。第二批（S03、S11、S34，票
`2026-10-19-curio-s-axis-second-batch-s03`）稿子已合併、旁白與插圖已送站主。第三批照樣一區一集：S29「曹沖稱象，可能來自
一部佛經？」（中國）、S14「宮本武藏在巖流島真的故意遲到？」（日本）、S26「『沒有麵包就吃蛋糕』，瑪麗皇后真的說過嗎？」（歐洲）。
選題理由：原文開得到（《三國志》鄧哀王沖傳在殆知閣、《雜寶藏經》在 CBETA、《二天記》《五輪書》在國會圖書館或青空文庫、
盧梭《懺悔錄》在 Project Gutenberg）。

## Definition of done

- [x] 三題各有 `topic-checks/<id>.md`（研究加獨立覆核）。
- [x] 三集稿子選 A 案、`loops` 至少 8 個、盲評全過、lint 0 錯誤、`claims.md`、`verify-1.md`，開 PR。
- [x] 旁白、配樂、插圖做完並 `review-push` 給站主。

## Steps

- [x] 查核先做（研究代理＋獨立覆核代理），再寫稿。
- [ ] 每完成一段就開 PR（站主：額度用完前記得開 PR）。

## How to verify

`node tools/video/cli.mjs lint --slug curio-s29`（及 s14、s26）0 錯誤；`status --slug` 看關卡。

## Notes

- 同一集的 tts、check-audio、keyframes 不能同時跑（skill〈在雲端環境做旁白與插圖〉）。
- 盲評輪數（每輪換一位只讀 `narrative` 輸出的新讀者）：S29 四輪（10→11→12→13），S14 三輪（11→12→13），S26 三輪（10→12→13）。
  最常卡的是 chapters_link（章首第一句要直接回答上一章最後的問題）、no_recap（同一件事講兩次）與 payoffs（問了「是誰」卻只答得出「查不到」——
  改成問查得到的「最早寫在哪裡」）。各集細節在各自 `NOTES.md` 的盲評表。
- 2026-10-20 狀態：三集旁白、插圖、配樂都做完，`review-push --gate audio` 與 `--gate storyboard` 都已送站主（待審）。
  花費（插圖＋配樂）：S29 US$1.32、S26 US$2.00、S14 US$1.51。旁白：S29 9:52、S26 9:28、S14 10:36。
- 念錯的字用 `say`／`say_for` 修（共用的 `docs/videos/lexicon.json` 只收拉丁字母詞，中文詞放進去 lint 報錯）：
  S29「何焯」念成 chāo，改 `say` 為「何卓」；S14「沼田」改 `say` 為「找田」。builder 遇到該詞自動加這兩欄。
  check-audio 剩下的都是同音字（陳壽／承受、碑上／悲傷、武藏／五臟、書裡／蘇利）。
- 插圖：三集同時跑 keyframes 會被主機擋「請求過於頻繁」，一次跑一集；502 直接重跑。評審三次不過的景改成
  「一個人做一件事」、去掉招牌／石板／黑板（會被畫上字）；S26 十二歲的瑪麗．安東尼觸發 PROHIBITED_CONTENT，
  改成不畫小孩（地球儀、宮廷保姆、譯者）。S29 builder 會依出現順序輪換時段字（`_TIME`），改提示詞時別新增
  「in the afternoon」這類鍵，否則後面二十幾張都會換字重畫。
- **成片前要先裝品牌素材包**（`intro.mp4`、`outro.mp4`、`manifest.json`，見 `docs/videos/BRANDING.md`）：雲端容器沒有
  `_branding`，S01／S09／S18 的雲端成片因此沒有片頭與片尾（成片長度等於旁白）。已請站主提供素材包；裝好後三集用
  `assemble --adopt-branding` 重做再送審，S29／S26／S14 成片時就會自動接上。
- 下一步：站主核准旁白與分鏡後 `review-pull`，裝好品牌包再 render → clips → assemble → captions → qa → `review-push --gate final`。
