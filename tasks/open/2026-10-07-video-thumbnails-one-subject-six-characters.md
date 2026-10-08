---
id: 2026-10-07-video-thumbnails-one-subject-six-characters
title: Video thumbnails: one subject, six characters, three rotating layouts, QA
status: in-progress
priority: P2
area: tools
owner: claude-fable
claimed_at: 2026-10-08T00:12:08Z
created_at: 2026-10-07T15:24:58Z
completed_at:
branch: claude/focused-hopper-t3zgz9
depends_on: []
scope:
  - tools/video/templates
  - tools/video/render
  - tools/video/qa/thumbnail.mjs
  - tools/video/qa/thumbnail.test.mjs
  - tools/video/compile/fixture.mjs
  - tools/video/core/fixtures/minimal/video.json
  - tools/video/qa/cli.mjs
  - .agents/skills/youtube-video/references/visuals.md
  - .claude/skills/youtube-video/references/visuals.md
  - .agents/skills/youtube-video/SKILL.md
  - .claude/skills/youtube-video/SKILL.md
  - docs/videos/README.md
  - docs/videos/ILLUSTRATED.md
---

# Video thumbnails: one subject, six characters, three rotating layouts, QA

## Why

頻道診斷（`docs/videos/channel-review-20261007/README.md` §2.1 D05）看過 18 張縮圖：09-27～09-30 上架的 11 張是 `theme.css` `.thumb-art` 的青綠圓環＋橘點同一版型只換字；10-04 後 7 張用關鍵影格鋪底，但主體是片中的比喻（咖啡店員、盆栽、雨傘、雜貨店收據），只有 2 張對得上題目。大字 11/18 超過 `visuals.md` 的 6 字上限（程式只擋 12 字：`compilation.mjs:29`、`plan.mjs:36`），11/18 與標題重複過半，兩張斷行拆詞（「一半的攻／擊」「建議日不／是生效日」）。三份規格互相矛盾：`docs/videos/README.md` §版型「一個標籤、一行大標、一行小字」（沒有主體）、`visuals.md` 第 57–58 行「≤6 字＋一個視覺主體、不重複標題」、`prompts.mjs` 第 204 行「≤10 字兩行」。沒有 CTR 數據前不能說縮圖壓低了點擊（觀看前四名全是同一版型），所以先做低成本的 QA 與規格統一，版型重做等 Studio 的曝光點閱率。

## Definition of done

- [x] `qa/thumbnail.mjs` 加三條：大字 ≤6 個 CJK 字（英文詞另計、最多 2 個）、兩行斷詞不拆詞（Node 22 `Intl.Segmenter` zh）、大字與標題前 10 字的最長共同片段 >50% 就警告；`thumbnail.test.mjs` 覆蓋。
- [x] `README.md`、`visuals.md`、`SKILL.md` 規矩 6、`ILLUSTRATED.md` 的縮圖規格改成同一套（≤6 字、一個主體、不重複標題、主體可用 screencast 截圖或關鍵影格、評論該產品時 logo／介面截圖可入鏡）；`prompts.mjs` 第 204 行由票 `2026-10-07-video-script-rules-outro-with-a` 改成同一組欄位（shot／capture）。
- [x] `templates.mjs` `thumbnailHtml` 與 `theme.css` `.thumb` 三套版型 A／B／C 輪替（文字欄左 40%、主體右 60%；沒有主體圖時是依 slug 輪流的單色底，圓環＋橘點刪掉）；聯絡表看過（見 Notes）。
- [x] 主體來源：`thumbnail.data.capture`（screencast 景的真實截圖，站主 2026-10-08 放行 logo／介面截圖）→ `thumbnail.data.shot`（關鍵影格裁右側）→ 單色底；撰稿規則那句在另一張票的 `prompts.mjs`。look 的 negative 不變。

## Steps

- [x] 先把 QA 三條與規格統一做完（hours），不等版型。
- [x] 版型：`thumbnailHtml` 做 A／B／C 三版；showcase 的 `thumbnail` 改成 ≤6 字並帶 B／C 變體；縮到 168px 寬確認大字可讀。
- [ ] 站主在 Studio 對 S88lbAsLz2E、UOgxCymxb1I、FYHFsj0SB7Q 各上一張 B 版做 Test & compare（桌機 Studio、兩週）；換縮圖前先給 `apps/api/app/video_youtube/sync.py` 的 `_thumbnail` 加「已換過就跳過」開關，否則同步會把原縮圖再送一次。

## How to verify

`npm run test:tools`；對 18 支現有的 `thumbnail` 資料跑新的 QA 應至少標出 11 支的大字超長與 4 支的照抄標題；聯絡表上三套版型在 168px 寬仍讀得到大字。

## Notes

`docs/videos/README.md` 只改 §版型的縮圖那一行與 §片頭與片尾（片尾改成約 15 秒、只求訂閱，素材由站主換），不動其他規格。版型重做是否優先，等 `docs/videos/channel-review-20261007/README.md` §6.3 的第 2 個數字（曝光 ≥1,000 後 CTR <2% 才是縮圖問題）。

### 2026-10-08 做了什麼（claude-fable，分支 `claude/focused-hopper-t3zgz9`）

- **版型**（`tools/video/templates/templates.mjs`、`theme.css`）：頻道縮圖改成 `.thumb.column`（左 40%，padding 56/24，大字 136px、兩行高 `max-height: 300px`、不用 `text-wrap: balance` 好讓 QA 算得準）＋ `.thumb-subject`（右 60%）。三套版型 `layout: a|b|c`：a 主體放內縮的圓角卡；b 主體鋪滿、左側遮罩；c 硬切、文字欄是色塊。四個色票 `tone: teal|plum|navy|forest`。沒寫 `layout`／`tone` 時 `thumbnailRotation(slug, offset)` 依 slug 雜湊（與 `slidesPresetFor` 同一個 FNV）輪流；B／C 變體 offset 1／2，所以三張一定不同版型。主體來源 `render/plan.mjs thumbnailSubject`：`capture`（`"<screencast 景 id>"` 或 `"<id>#n"` 取第 n 張，從 `screencast/<key>/manifest.json` 拿檔與 sha256，裁左上角）優先於 `shot`（關鍵影格，裁右側）；`renderProblems` 擋不存在的景與超出張數的 `#n`；`render --thumbnails-only` 用 `cachedManifest` 讀已拍的截圖。原來如此事務所（`series`）保留原本的整寬欄、遮罩與 left/right 鏡像，不套新版型（`thumbnails.md` 自己有規格）；只是沒關鍵影格時不再畫圓環。`.thumb-art` 從 theme.css 刪掉，theme hash 變了：既有影片下次 `render` 會重畫所有影格（本機免費）。
- **QA**（`qa/thumbnail.mjs`）：`HEADLINE` 改成欄寬 432、兩行 300；新增 `HEADLINE_SERIES`（舊的 868／460）給 `series`。`thumbnailChecks({ bytes, headline, title?, series? })`：≤6 字（`headlineCount`：CJK 各 1、英文詞／數字各 1、最多 2 個）與斷詞（估出的換行位置對 `Intl.Segmenter("zh")` 的詞）是 **fail**，標題前 10 字 LCS >50% 是 warning。斷行寫 `\n` 時 CJK 兩側不算字元（「攻\n擊」仍是「攻擊」），英數兩側算一個空白（「Gem\n11月」不是 Gem11）。
- **沒做、要別人做**：
  1. `tools/video/qa/cli.mjs` `thumbnailItem`（不在本票 scope；票 `2026-10-05-hold-lost-planner-and-jev-answers` 的 scope）要改成 `thumbnailChecks({ bytes, headline, title: doc.youtube?.title, series: thumbnailSeries(doc) })`（`thumbnailSeries` 在 `render/plan.mjs`）。沒改之前：標題重複的警告出不來；**原來如此事務所的縮圖會被當頻道規則判（>6 字就 fail）**——合併前要補這兩行。
  2. 因為 ≤6 字現在是 QA fail，fixture 的長大字讓 scope 外的 6 個測試紅：`tools/video/qa/qa.test.mjs`（5 個：minimal fixture 的「第一名不一定最好用」9 字；合集的「仙門風雲 全集」在 136px 會斷成「仙門風／雲」）與 `tools/video/review/sync.test.mjs:1787`（同一個合集 fixture）。修法：`tools/video/core/fixtures/minimal/video.json` 大字改 ≤6 字（例如 `**不一定**最好用`），`tools/video/compile/fixture.mjs:69` 改成 `仙門風雲\n全集`，`qa.test.mjs:146` 的「34 px」跟著 fixture 走。
  3. 「連續兩支不同色」需要跨影片狀態，沒做：同一色票的機率 1/4，站主看到撞色就在 video.json 寫 `tone`。
  4. 合集（BINGE）與漫劇的縮圖也走新版型與 ≤6 字；若站主要合集例外，再開票。
  5. `node tools/video/cli.mjs render --file …/showcase/video.json` 被 lint 的 8 分鐘下限擋住（showcase 只有 2.2 分鐘，HEAD 就如此），所以聯絡表是用 `openRenderer` ＋ `renderPlan`／`thumbnailHtml` 直接畫的 9 張（a／b／c × 無圖／關鍵影格／截圖），版面檢查零問題，縮到 168px 大字仍讀得出來。
  6. `.claude/skills/youtube-video/references/visuals.md` 不存在（`tools/skills.test.mjs` 規定 `.claude` 只放 SKILL.md），scope 裡那一行是空的。

### 2026-10-08 審稿後修正（claude-fable）

審稿對 6185128f 提了六條 should-fix，逐條處理如下（都在本票 scope 內；重跑 `node --test` 相關檔與整套 `npm run test:tools`）。

1. **版型 b × `capture` 把截圖的左上角（logo 與選單）藏在遮罩下**（`theme.css`）：`.thumb-subject.layout-b` 鋪滿整格、`from-capture` 又把截圖的左上角釘在 x=0。改成 `.thumb-subject.layout-b.from-capture img { width: 60%; margin-left: 40% }`，截圖留在右 60%，遮罩對 capture 改成在 40% 前淡出（`.layout-b.from-capture::after`），關鍵影格（`from-shot`）的 b 版不變。用 `openRenderer` 重畫 a／b／c × 截圖／關鍵影格／無圖 9 張並**看過圖**（假的 1280×800 頁面左上角放紅色 LOGO 塊）：改前 b-capture 的 LOGO 整個在遮罩下，改後三版都看得到；版面檢查零問題。
2. **企劃還允許 12 字、qa 卻擋 6 字**：`compilation.mjs`、`prompts.mjs`、`story.mjs`、`story-plans/plan.mjs` 都不在本票 scope，開票 `2026-10-08-video-planners-thumbnail-headline-six`（P1，依賴本票與 `2026-10-07-video-script-rules-outro-with-a`，後者還在 `prompts.mjs` 上）把五處限制改成 `THUMB_HEADLINE_MAX` 與 `headlineCount` 的算法，並讓 lint 先警告。**沒有**在 qa 對合集與漫劇開例外：站主定的是每張縮圖 ≤6 字，qa 不過時成片關卡不會自動核准（`final_qa_passed` 要 qa ok），卡片帶著「the headline counts 9 characters」停在後台等站主改字，不是悄悄放行 12 字的縮圖；企劃改好之前漫劇與合集會多這一步，所以那張票是 P1。合集大字本來就是系列名、必然撞標題前 10 字，`qa/cli.mjs` `thumbnailItem` 對 `isCompilation(doc)` 不再比對標題（`thumbnail.test.mjs` 覆蓋）。
3. **各語言縮圖被當中文判**（`qa/cli.mjs`）：`thumbnailChecks` 多 `locale`，不是 `zh-TW`（`CHANNEL_RULES_LOCALE`）時只檢查尺寸、位元組、手機上的字高與重複標題，不套 6 字、2 個英文詞與 zh 斷詞；`thumbnailItem` 對 `thumbnail_locales` 的每一張帶 `locale`。測試改用四個詞的「Not always the best」、「最高とは限らない」、「항상 최고는 아니다」都 ok 且零警告；`README.md` §版型補一句。
4. **價格與千分位被拆成兩個詞**：`templates.mjs` 匯出 `HEADLINE_WORD`（`(?:NT\$|US\$|[$€¥£￥])?[A-Za-z0-9][A-Za-z0-9.,'%+-]*`，`headlineCount` 去掉尾端逗號），`qa/thumbnail.mjs` `headlineTokens` 用同一個 token，所以「NT$270」是一個數字、行模型也不會在 `NT$|270` 斷行。「$50 vs $20」的訊息現在寫 `($50, vs, $20)`；`NT$270`、`1,000`、`US$20`、`€18`、`Yes,` 進測試。
5. **visuals.md 寫了「連續兩支不同底色」**：程式只依 slug 雜湊輪色、沒有跨影片狀態，改成「底色依 slug 在四色中輪流，撞色時站主寫 `thumbnail.data.tone`」，與 `README.md` 與 `templates.mjs` 的註解一致。
6. **DECISIONS.md 的「改 look 的 negative」沒做、也沒記**：`DECISIONS.md` 不在本票 scope，不能改；在 `ILLUSTRATED.md` 的 `thumbnail.data.shot`／`capture` 列記下這是有意不做的（AI 畫的 logo 既不準也不是合理引用，真 logo 只有截圖給得了），這裡也記一筆。**待站主**：請在 `docs/videos/channel-review-20261007/DECISIONS.md` 第一列的「接著做」補一句「negative 不改，logo 與介面只從 `capture` 來」，或說要改再開票。
