---
id: 2026-10-08-video-planners-thumbnail-headline-six
title: Video planners: thumbnail headline limit 12 to the channel's six (compilation, drama, brand story)
status: done
priority: P1
area: tools
owner: claude-fable
claimed_at: 2026-10-08T02:36:58Z
created_at: 2026-10-08T03:40:00Z
completed_at: 2026-10-08T04:27:44Z
branch: claude/focused-hopper-t3zgz9
depends_on:
  - 2026-10-07-video-thumbnails-one-subject-six-characters
  - 2026-10-07-video-script-rules-outro-with-a
scope:
  - tools/video/automation/compilation.mjs
  - tools/video/automation/compilation.test.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - tools/video/automation/story.mjs
  - tools/video/automation/story.test.mjs
  - tools/video/story-plans/plan.mjs
  - tools/video/story-plans/plan.test.mjs
  - tools/video/story-plans/validate.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/core/fixtures/drama/video.json
  - tools/video/core/fixtures/illustrated/video.json
  - tools/video/templates/terminal/fixtures/claude-code/video.json
---

# Video planners: thumbnail headline limit 12 to the channel's six (compilation, drama, brand story)

## Why

票 `2026-10-07-video-thumbnails-one-subject-six-characters` 把 `qa` 的 thumbnail 項改成頻道規則：大字
最多 6 個字（`templates.mjs` `THUMB_HEADLINE_MAX`，`headlineCount`：CJK 各 1、英文詞或數字各 1、最多 2 個），
超過是 **fail**。但全自動路線替站主寫大字的企劃還允許 12 個字：`automation/compilation.mjs:29`
`HEADLINE_MAX_CHARS = 12`（第 144 行驗、第 249 行交給工人）、`automation/prompts.mjs:574` 漫劇
`headline ≤ 12 chars`、`prompts.mjs:1275` 合集 `≤ 12 characters`、`automation/story.mjs:709` 品牌故事
`clip(…, 12)`、`story-plans/plan.mjs:36` `LIMITS.headline: 12`。一支工人企劃的合集或漫劇寫了 7–12 字的大字，
lint 與 render 都過，到 `qa` 才 fail：成片關卡不會自動核准（`final_qa_passed` 要 qa ok），卡片停在後台等
站主改 `video.json`（BINGE.md §43、§46 本來是 qa → 成片自動核准）。審稿 2026-10-08 指出這個落差；本票不在
原票 scope，所以另開。

## Definition of done

- [x] `HEADLINE_MAX_CHARS`、`LIMITS.headline`、`story.mjs` 的 `clip(…, 12)` 改成 `THUMB_HEADLINE_MAX` 與
      `headlineCount` 的算法（字數是 `headlineCount(headline).count`，不是 `.length`；英文詞或數字最多
      `THUMB_HEADLINE_WORDS_MAX`），`validate.mjs` 跟著。
- [x] `prompts.mjs` 漫劇（第 574 行附近）與合集（第 1275 行附近）的大字規則改成「≤ 6 個字、一個英文詞或數字算
      1、最多 2 個、`\n` 只放在詞的邊界、不重複標題前 10 字」，與 `.agents/skills/youtube-video/references/visuals.md`
      §縮圖同一套字。
- [x] `core/lint.mjs` 對非系列（`thumbnailSeries(doc)` 是 null）的縮圖大字做同一條檢查當 **警告**（qa 才 fail），
      讓撰稿階段就看得到，不要等到成片關卡。
- [x] 企劃的回答超過 6 字時重問一次（`compilation.mjs` 的 `ANSWER_ATTEMPTS` 機制已有），仍超過就把大字截到詞邊界
      而不是硬切。
- [x] 各自的測試覆蓋；`npm run test:tools`（只剩本來就紅的「the shipped independent duration review binds
      the current plans and implementation」）。

## Steps

- [x] 先讀 `tools/video/qa/thumbnail.mjs` `thumbnailChecks` 與 `templates.mjs` `headlineCount`，規則以它們為準。
- [x] 票 `2026-10-07-video-script-rules-outro-with-a` 還在 `prompts.mjs` 上，等它結案再 claim。

## How to verify

`cd /home/user/travel_scanner && node -e 'import("./tools/video/qa/thumbnail.mjs").then(async m=>{const {jpegBytes}=await import("./tools/video/qa/test-images.mjs");console.log(m.thumbnailChecks({bytes:jpegBytes(1280,720,2000),headline:"仙門風雲第一部全集"}))})'`
現在是 `ok: false`，而 `compilation.mjs:144` 接受這 9 個字；做完後企劃不可能交出 qa 會擋的大字。

## Notes

- 合集的大字本來就是系列名（「仙門風雲 全集」對標題「仙門風雲 全集：第一部完整版」），所以 `qa/cli.mjs`
  `thumbnailItem` 對合集不做重複標題的警告（2026-10-08 審稿後改的）；這張票不用再碰那一條。
- 各語言自己的縮圖（`thumbnail_locales`）不套中文字數與斷詞規則（`thumbnailChecks` 的 `locale`），企劃給翻譯的
  大字規則不在本票。
- 實作（2026-10-08，claude-fable）：共用的規則與截字放在 `story-plans/plan.mjs`：`headlineProblem(headline)`
  （count ≤ `THUMB_HEADLINE_MAX`、英文詞或數字 ≤ `THUMB_HEADLINE_WORDS_MAX`、`\n` 與瀏覽器的斷行都不落在詞中間，
  後者用 `qa/thumbnail.mjs` 的 `headlineSplitWords`）與 `clipHeadline(headline)`（`Intl.Segmenter` zh 逐詞累加到
  六字；收尾若是 `DANGLING` 裡的虛詞（的、沒、第…）就丟掉，至少留三字；四字以上的詞會被欄位切開時補一個 `\n`；
  已合規的大字原樣回傳，含 `**` 與 `\n`）。`compilation.mjs`（`metadataProblem` 用 `headlineProblem`，最後一次
  重問仍超過就 `clipHeadline`）與 `story.mjs`（品牌故事 `clipHeadline(plan.thumbnail.headline)`）都從這裡拿；
  真正的家應該是 `templates.mjs` 或 `qa/thumbnail.mjs`，不在本票 scope，要搬另開票。
- `plan.mjs` 的 `LIMITS.headline` 是 `THUMB_HEADLINE_MAX`，但 `storyProblems` 的硬上限留在 `LIMITS.headlineDraft`
  （12，改用 `headlineCount` 算）：`brand-stories-100` 一百個故事有 58 個大字超過 6 字（T01「一元官司，沒判誰發明」
  等），另有 12 個四到六字的大字在欄位三字一行時會切在詞中間；這些都在本票 scope 之外，所以超過六字是
  `storyWarnings` 的**警告**，`validate.mjs` 印成 `WARNING <id>: … the builder cuts it to 「…」` 且 exit 0
  （現在是 `0 problems, 70 warnings`），成片由 `story.mjs` 截到詞邊界。要讓作者自己寫六字的話，另開票改那
  70 個故事檔，再把 `headlineDraft` 拿掉。
- 三個 scope 外的 fixture 大字被 `lint` 的新警告打到，而 `drama.test.mjs`、`terminal.test.mjs` 斷言它們 lint
  乾淨，所以一起改：`core/fixtures/drama/video.json`「精衛為什麼填海」→「填不完的海」、`core/fixtures/illustrated/video.json`
  「第一名\n**不一定**最好用」→「**不一定**\n最好用」、`templates/terminal/fixtures/claude-code/video.json`
  「先在終端機**確認版本**」→「**一行**\n就知道」。這三個也是交給工人的範例，範例本來就不該違規。
- `qa` 的斷詞規則比想像嚴：欄位一行三字，所以「她磨好了刀」（她／磨／好了／刀）會在「好了」中間斷而 fail，
  企劃與 lint 都照這條擋；`compilation.test.mjs` 的範例大字因此改成「她的刀\n磨好了」。
- 合集提示詞不寫「不重複標題前 10 字」：合集大字本來就是系列名（Notes 第一條），改寫成「the series' name is the
  promise a compilation makes, so it may open the title」；漫劇提示詞有這一條。
- `prompts.mjs` 第 256 行（slides writer）與第 1449 行附近在 template literal 裡寫 `\n`，模型看到的是真的換行
  而不是「\n」兩個字；本票新加的兩處用 `\\n`。那兩處是別票的字，沒動。
- `.agents/skills/youtube-video/references/prompts/planner-compilation.md` 第 11、19 行仍寫 `thumbnail_headline_max (12)`
  與 `≤ 12 characters`（`.claude/skills` 的同名副本也是），不在 scope，要同步再開票；payload 現在多給
  `thumbnail_headline_words_max`。
- 審稿後修正（2026-10-08，claude-fable）：
  - `clipHeadline` 截完補 `\n` 之後再用 `headlineProblem` 驗一次；仍過不了（第二行還是會被欄位切在詞中間，
    「Nike\n曾是代理商」「200億\n判決，後來」）就丟掉最後一個詞再排一次，最少留三字，所以 `story.mjs` 寫進
    video.json 的大字一定是 qa 會過的。最多只補一個 `\n`（visuals.md §縮圖「一到兩行」），不靠第三行過關。
    作者自己把 `\n` 寫在詞中間的（「名字沒註\n冊的辣椒醬」）會先把那個 `\n` 拿掉再排。沒丟掉任何詞的大字
    收尾不動（「廉航怎麼賺？」留問號）。`brand-stories-100` 一百個只有 B24「Nike曾是」、C11「200億判決」改了，
    截完 100 個企劃與 qa 全過；`plan.test.mjs`「the repository's plan is complete, sound and compiled」多一條
    性質測試：每個故事 `headlineProblem(clipHeadline(headline))` 是 null。
  - `headlineProblem`（企劃）與 `thumbnailHeadlineProblems`（lint）補上 `thumbnailChecks` 的第四條：大字縮到
    320 寬至少 `MIN_HEADLINE_PX_AT_PHONE`（24 px），與 qa 同一句話。8 字母以上的單一英文詞（「Anthropic」
    「Perplexity 來了」「Microsoft\n買了」）企劃、`metadataProblem`、lint 三處都擋；`clipHeadline` 救不了它（怎麼
    截都 21 px），回傳最長的那個截法，`storyWarnings` 改口「the builder cannot cut it to the rule（…still …）」
    而不是承諾一個 qa 會擋的字串。沒有把它升成 `storyProblems` 的硬錯誤：`apps/api/app/video_automation/stories.py`
    `check_story_file` 鏡射 `storyProblems`（「change both together」），不在本票 scope；真實企劃由上面那條性質
    測試守住（現在 0 個）。順帶發現 stories.py 的 `LIMITS["headline"] = 12` 用 `len` 算，本票把 JS 端改成
    `headlineCount` 之後兩邊已經分岔（「Anthropic 推出」JS 算 3、Python 算 13），要另開票同步。
  - 三個 scope 外的 fixture（上一條 Notes）補進 frontmatter 的 scope，不再只是 Notes 裡的例外。`check:tasks`
    因此多一條「與 2026-10-07-video-thumbnails-one-subject-six-characters 都覆蓋 tools/video/templates」的警告：
    那張票與本票同一個 owner、同一條分支（claude/focused-hopper-t3zgz9），不是撞車；它結案後警告自己消失。
