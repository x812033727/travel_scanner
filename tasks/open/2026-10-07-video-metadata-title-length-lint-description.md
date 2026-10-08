---
id: 2026-10-07-video-metadata-title-length-lint-description
title: Video metadata: title length lint, description first line, UTM and series hashtag
status: in-progress
priority: P2
area: tools
owner: claude-fable
claimed_at: 2026-10-08T00:12:09Z
created_at: 2026-10-07T15:24:58Z
completed_at:
branch: claude/focused-hopper-t3zgz9
depends_on: []
scope:
  - tools/video/core/metadata.mjs
  - tools/video/core/metadata.test.mjs
  - tools/video/core/compilation.mjs
  - tools/video/core/compilation.test.mjs
  - tools/video/package
  - .agents/skills/youtube-video/references/publish.md
  - .claude/skills/youtube-video/references/publish.md
---

# Video metadata: title length lint, description first line, UTM and series hashtag

## Why

頻道診斷（`docs/videos/channel-review-20261007/README.md` §2.2 D06、D13 留下的事實）：18 支標題中位 40 個全形字、最長 57，9 支超過 `publish.md` 自己寫的 40 字，而 `prompts.mjs` 只檢 100 字；只有 5/18 標題含數字且多是版本號；6 支用「是誰測的／怎麼讀／先分清」同一句型（參考頻道 150 支裡 0 支）。說明欄 15/18 第一行是網址（S88lbAsLz2E、UOgxCymxb1I、zxHRm5jnELc 同一網址出現 3 次）、鉤子句掉到第 3 行；10-04 後 6 支的站內連結沒帶 `utm_source=youtube`；旁白模板說「說明欄第一行」但 `composeDescription` 09-26 改成連結第一行後兩邊沒同步（cc09kA17Xsw 363s、xSrFAMk_udE 188s 指路錯）；18 支各 3 個 hashtag 全是題目詞，沒有系列 hashtag，說明欄互相連結 0 次。

## Definition of done

- [x] `metadata.mjs` 的 `youtubeWarnings` 對 `youtube.title` 檢查：≤36 個全形字等值（`titleWidth`：CJK 1、ASCII 0.5）、最多一個「？」、禁用詞（是誰說的、是誰測的、怎麼讀、怎麼看、先分清、先問）、「、」列舉三項以上、集數字樣（第 N 集／EP N／#N，`numbered: true` 放行漫劇）、標籤超過 10 個；全部是警告字串，格式同 `checkYoutubeFields`；`metadata.test.mjs` 覆蓋。「前 15 字內有產品名或主詞」沒做（判不出什麼是產品名，站主要的話另開）。lint.mjs 第 398／427 行已接（60cdbef1；本文與翻譯各一次，漫劇帶 `numbered: true`）。
- [x] `composeDescription` 固定：第一行本文第一句（鉤子）、第二行給誰看（本文第二行）、第三行起其餘（`bodyLayout`）；🔗 文章連結放本文之後、同一網址在整份說明欄只出現一次（本文 `dedupeLinks`、📚 `unlinkedSources`；「同一頁」是 `urlKey`：去 `utm_*`、`#`、尾斜線，其他 query 保留）；每個 mokaair.com 連結帶 UTM（`withUtm`／`tagMokaairLinks`，campaign 是 slug）；最後一行兩個題目 hashtag 加 `category` 對映的系列 hashtag（`SERIES_HASHTAGS`：ai-terms、tutorial、ai-news；沒對映就只有兩個）；各語系同順序。「第三行留言題」照 10-08 的指示改成「第三行起本文其餘」。
- [ ] 撰稿提示裡「說明欄第一行的文章」那句由 `2026-10-07-video-script-rules-outro-with-a` 改（prompts.mjs 不在本票 scope）；`package` 這邊已經把連結放到本文之後。
- [x] `publish.md` §標題、§說明欄、§標籤與「全自動路線的上架包」改成與程式一致。`.claude/skills/youtube-video/` 只鏡射 `SKILL.md`（`tools/skills.test.mjs` 明文禁止 references 有第二份），所以 scope 裡的 `.claude/.../references/publish.md` 不存在也不該建。`docs/videos/README.md` §說明欄不在 scope，沒改。

## Steps

- [x] 讀 `tools/video/core/metadata.mjs` 的 `composeDescription` 與標題檢查，列出現在實際的順序（改前：🔗 文章連結 → 本文 → 📌 章節 → 📚 參考資料 → 📷 圖片來源 → 前三個 tags 的 hashtag；標題只在 `checkYoutubeFields` 檢 100 字與角括號，lint.mjs 第 397 行把它的回傳全當 error）。
- [x] 加標題 lint 與說明欄組裝規則，補測試（`core/metadata.test.mjs`、`package/metadata.test.mjs`、`package/package.test.mjs`）。
- [x] 對 repo 裡全部 32 支 `video.json`（含 7 支漫劇、2 支原來如此）跑一次新規則，基準記在 Notes。

## How to verify

`npm run test:tools`；`node tools/video/cli.mjs lint --slug <任一已上架 slug>` 對 57 字的 UWYoO3JfOK0 標題給出警告；`package` 產出的說明欄第一行不是網址、所有 mokaair.com 連結帶 UTM、同一網址只出現一次。

## Notes

已公開的 18 支改標題與說明欄只能站主在 Studio 手改（`publish.md` 寫明網站不動已公開的影片）；候選的新標題在 `docs/videos/channel-review-20261007/README.md` §3 逐支表與 §5。手機列表到底顯示幾個全形字沒有量過（publish.md 寫 40、第三方只量拉丁字元），36 字是保守值。

### 2026-10-08 實作（claude-fable，分支 `claude/focused-hopper-t3zgz9`）

**誰在用哪份 `metadata.mjs`**：`core/metadata.mjs` 是真的在組說明欄的那份（`composeDescription`、`checkYoutubeFields`、`articleUrl`）；`package/metadata.mjs` 的 `composeMetadata` 只是每個語系各呼叫一次 core 的 `composeDescription`，再組 `metadata.json` 與 `UPLOAD.md`。lint.mjs 第 396–397 行、compilation.mjs `descriptionWithinBudget`、qa、review 都走 core。

**基準（改法之前的 32 支 video.json，`youtubeWarnings` 跑出來）**：28 個警告——寬度 >36 的 9 支（ai-real-jobs-chart 37、ai-term-context-window 36.5、ai-terms-prompt-to-graph-engineering 41、free-vs-paid-ai-plans-2026 40、google-vids-free-ai-video-omni-1-1 41.5、gpt6-vs-opus55-worth-paying 40、openai-agents-broke-in 38.5、rtx-spark-local-ai 38、why-openai-killed-sora 53）、「、」三項以上 6 支、兩個「？」2 支（ai-term-large-language-model、rtx-spark-local-ai）、標籤 >10 個 11 支（最多 18）、禁用詞 0 支（repo 裡的 32 支沒有那六個詞；有的是已公開而不在 repo 的那幾支）。7 支漫劇標題「第N集」以 `numbered: true` 放行，不放行會再多 7 個。說明欄：32 支本文第一行都不是網址（第一行是網址的 15 支是已公開影片在 Studio 上的版本，不是 repo 的 `youtube.description`）、6 支本文有站內連結、其中 1 個沒帶 utm；組完之後 0 支第一行是網址、0 個沒帶 utm、0 個同一頁出現兩次。19 支本文第二行不是「給…」開頭（漫劇、原來如此、幾支早期的），這些的第二行就是本文的第二句或第二段——規則是「本文第二行」，不是「找『給』字」，撰稿規則那張票把「第二行＝給誰看」寫進提示才會對齊。

**決定**：
- 警告不能塞進 `checkYoutubeFields` 的回傳（lint 把它全當 error），所以另開 `youtubeWarnings({ title, tags }, where, { numbered })`，回傳格式跟 `checkYoutubeFields` 一樣的字串。lint.mjs 第 398（本文）與 427（翻譯，`where` 用 locale）行已經呼叫它（60cdbef1 接的，漫劇帶 `numbered: drama`），所以 `cli.mjs lint --slug` 會印這些警告；`docs/videos` 裡沒有 UWYoO3JfOK0 那支的 video.json，「How to verify」那句要拿 repo 裡寬度超過 36 的任一支（例如 why-openai-killed-sora，53）看。
- 寬度算整個標題含「｜系列名」後綴（手機列表看到的就是整串）。
- 「沒有對映就不加第三個」照字面做：沒有系列對映只有兩個 hashtag。合集（compilation.mjs，不在 scope）沒傳 `category` 所以也只有兩個。
- 標籤：`uploadTags` 取 video.json 前 10 個（去重、500 字內）；翻譯語系的 tags 不再混進 `metadata.json` 的 `tags`（原本是 narration + 各語系合併到 500 字）。YouTube 的 localizations 本來就沒有 tags 欄位，翻譯的 tags 留在 `i18n/<語系>.json`。
- 本文裡只剩網址的行（文章本身、或同一頁在別行句子裡已經連過）會被拿掉；句子裡提到文章網址時不再另加 🔗 行；📚 不再列文章本身與本文已連的頁（一頁一次，見下面「審稿後修正」）。
- 系列 hashtag 各語系同一個（hashtag 是頻道層級的分組）。

**測試**：`node --test` core/metadata、package/metadata、package/package、variants、check、compilation、compilation-review、narration-locale、lint、qa/links、dubs/captions-package 全綠；`npm run test:tools`（實作時 2024 個、10 個失敗，其中 9 個是縮圖票進行中的 `captureRef` import；審稿後重跑見「審稿後修正」）。

**留給別人**：lint.mjs 第 396 與 425 行、compilation.mjs 第 361 行 `descriptionWithinBudget` 呼叫 `composeDescription` 時沒傳 `category: doc.category`、`series: doc.series`、`campaign: doc.slug`，所以 lint 算的說明欄比 package 少第三個 hashtag（ai-term-embedding、ai-term-large-language-model、ai-terms-prompt-to-graph-engineering 各 19 bytes、openai-devday-2026-recap 16 bytes），沒有 pack 時本文的站內連結也少了 `utm_campaign=<slug>`：貼近 5,000 bytes 的說明 lint 放行、package 才拒絕。兩個檔都不在本票 scope（lint.mjs 正被別張票改），接 lint 的人把這三個參數傳下去就對齊；`docs/videos/README.md` §說明欄仍是舊順序；撰稿提示（prompts.mjs）要寫「第一行鉤子、第二行給誰看、連結在本文之後」；`SERIES_HASHTAGS` 目前只有 ai-terms／tutorial／ai-news 三列，explainer（原來如此事務所）與 comparison 要不要各自的 hashtag由站主定。

### 2026-10-08 審稿後修正（claude-fable）

審稿人指出四點，三點改在 scope 內、一點 scope 外只記下來：

1. **📚 與 🔗 同一頁各出現一次**（should-fix，改了）。`dedupeLinks` 只看本文，`sources` 列到文章自己時（`docs/videos/ai-term-embedding/video.json` 最後一筆就是 `https://mokaair.com/zh-TW/life/ai-term-embedding`）🔗 與 📚 各一行同一頁。加 `unlinkedSources(sources, linked)`：`composeDescription` 組 📚 前先把文章連結與去重後本文裡每個連結的 `urlKey` 收成 `linked`，等於其中任一頁的來源、以及同一頁的第二筆都不列；全部都連過就沒有 📚 段。測試「a source that is the article, or a page the body links, is not listed again under 📚」。對 32 支 video.json 用 `urlKey` 重算：同一頁出現兩次 0 支（之前 1 支，ai-term-embedding）。
2. **`urlKey` 砍整個 query 太粗**（should-fix，改了）。站外很多頁只靠 query 分頁（ai-agent-vs-chatbot 的 sources 有 `ntm.gov.tw/cp.aspx?n=5444` 與 `?n=5445`），本文兩行各放一個時第二行會被 `dedupeLinks` 當重複拿掉。現在 `urlKey` 只刪 `utm_*` 參數（加 `#` 與尾斜線），其餘 query 原樣保留、順序不動；解析不了的字串走同樣規則。測試：`?ref=1&utm_source=…` → `?ref=1`、兩個 ntm 頁不相等、兩行只剩網址的 ntm 頁都留下。publish.md §說明欄第 4 點寫明「同一頁」的定義、第 6 點寫明 📚 不列哪些。
3. **lint 與 package 組出的位元組不同**（should-fix，scope 外，沒改）。見上面「留給別人」第一項：lint.mjs 第 396／425 行與 compilation.mjs 第 361 行要傳 `category`、`series`、`campaign`。本票 Notes 原本把「都走 core」當成等價，不對：core 的 `composeDescription` 一樣，但 lint 少傳三個參數。lint.mjs 現在是別張票的未提交改動，不能在這裡碰。
4. **票檔與程式不符**（should-fix，改了）。DoD 第一條、Notes「決定」第一點與「留給別人」第一項原本寫 lint.mjs 還沒接 `youtubeWarnings`，其實 60cdbef1 已在第 398／427 行接上；改成現況。測試數字更新：`npm run test:tools` 2026 個、只有本來就失敗的 1 個。

重跑：`node --test` core/metadata（11）、package/metadata、package/package、qa/links、compilation、compilation-review、lint、package/check、variants、qa/qa、qa/checks、narration-locale、cli、schema 共 171 個全綠；`npm run test:tools` 整套在交回時跑到 1,181／2026，只有本來就失敗的那 1 個（「the shipped independent duration review binds the current plans and implementation」），後半段沒等到結束，接手的人再跑一次確認；`cmp .agents/skills/youtube-video/SKILL.md .claude/skills/youtube-video/SKILL.md` 相同（`.claude` 下仍只有 SKILL.md）。
