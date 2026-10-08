---
id: 2026-10-07-video-script-rules-outro-with-a
title: Video script rules: outro with a subscribe reason, numbers said out loud
status: done
priority: P2
area: tools
owner: claude-fable
claimed_at: 2026-10-08T00:12:08Z
created_at: 2026-10-07T15:24:57Z
completed_at: 2026-10-08T04:27:43Z
branch: claude/focused-hopper-t3zgz9
depends_on: []
scope:
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - .agents/skills/youtube-video/references/script-writing.md
  - .claude/skills/youtube-video/references/script-writing.md
---

# Video script rules: outro with a subscribe reason, numbers said out loud

## Why

頻道診斷（`docs/videos/channel-review-20261007/README.md` §2.1 D03、D04）核對 18 支 zh-TW CC：沒有一支結尾請觀眾訂閱頻道（「訂閱」命中的全是產品訂閱），唯一反覆出現的行動是「說明欄的文章」把人送出 YouTube；14 支把標題承諾的數字（價格、降幅、日期、額度）改成「以官網為準／我不唸」，而那些數字就寫在說明欄連結的自家文章裡（cc09kA17Xsw 旁白 5 次加 5 組字卡；UOgxCymxb1I 字卡 `cut = None`）。兩者都是規格照寫出來的：`tools/video/automation/prompts.mjs` COMMON「Numbers … come only from an official page in sources … or 以官網為準 on the slide」、第 250 行「Third-party pages never confirm a number」把自家已查核文章也排除；outro 規則只寫「The last scene」，`script-writing.md` §結尾「挑一個」。站主點名的黑貓研究院與 Gary Chen 抽查 4 支，結尾全是留言題＋按讚訂閱＋下期見。

## Definition of done

- [x] 新片的 `outro` 場景固定三句旁白：回答開場的問題、一個觀眾答得出的留言題、一句有理由的訂閱邀請（系列集點名下一集；單篇新聞片用頻道層的固定承諾或指向播放清單，不自動編造下一支題目）。
- [x] 官方頁抓得到的數字講出口並在字卡用既有的 `stats.source`／`quote.source` 標「官網 YYYY-MM-DD」；官方頁抓不到（例如 OpenAI 全家對工人 UA 回 403）但自家已查核文章（帶 checked_on）有的，允許引用並標文章查證日；免責只留說明欄一句。
- [x] `lint` 對「以官網為準／公告沒寫／不代表／我不唸」片語家族計數並 warn（不是硬錯誤，否則撰稿的 lint_errors 迴圈只會換同義句）；每支旁白超過一次就警告。
- [x] `script-writing.md`（只有 `.agents` 那份：`tools/skills.test.mjs` 規定 references 只存在 `.agents` 底下，`.claude` 只放 SKILL.md，多放一份會讓 `npm run test:tools` 紅）§開場、§句子、§結尾改成同一套說法，`npm run test:tools` 過。

## Steps

- [x] 改 `prompts.mjs` COMMON 第 44–45 行與 verifier 第 250 行；確認 NOT FOUND 的處理仍是「drop the number or the sentence」（第 254 行）。
- [x] 改 `prompts.mjs` outro 規則（第 82 行附近）與 cta 規則（第 80 行：片中已推過一次文章，結尾不再第二次）。
- [x] `tools/video/core/lint.mjs` 加片語計數的 warn()，`lint.test.mjs` 補案例。
- [x] 用 `tools/video/core/fixtures` 的 showcase 與 illustrated 範例跑一次 `lint`，確認既有範例不會被新規則打成錯誤。

## How to verify

`npm run test:tools`；`node tools/video/cli.mjs lint --file tools/video/core/fixtures/illustrated/video.json` 零錯誤；下一支由產線寫出的 `video.json` 的 outro 有三句、旁白全文「以官網為準」≤1 次、至少一個標了日期的數字字卡。

## Notes

不要改 `docs/videos/HANDS-OFF.md` 的立場草稿來達成這件事：正式站的立場是 10 條、存在 `channel_stance` 設定，改文件改不到正式站。片尾卡（3 秒按讚／分享／小鈴鐺，沒有「訂閱」）換成只求訂閱的新 `outro.mp4` 是站主用 `branding --install` 換素材包的事，見 `docs/videos/channel-review-20261007/README.md` §2.1 D03；已公開的 18 支只能由站主在 Studio 補結束畫面與置頂留言。

### 2026-10-08 做了什麼（claude-fable，分支 claude/focused-hopper-t3zgz9）

照 `docs/videos/channel-review-20261007/DECISIONS.md` 的拍板做：

- **`prompts.mjs`**：`COMMON` 拆成 `RULES_HEAD`＋數字規則＋`RULES_TAIL` 兩個版本。翻譯類階段（translator、caption_reviewer、配音的 shorten／reword）仍讀 `COMMON`，位元組跟以前一模一樣——`tools/video/automation/automation.test.mjs` 的 `ZH_TW_PROMPT_SHA256` 釘住它們的 SHA-256（不在本票 scope），改了就紅。撰稿類階段（planner、writer、verifier、listener）改讀 `WRITING_COMMON`：數字說出口、字卡 `stats.source`／`quote.source` 標「官網 YYYY-MM-DD」、官方頁抓不到（payload 的 `sources` 標 failed）而 mokaair.com 的已查核文章有時標「Mokaair 文章 查證 YYYY-MM-DD」、免責只留說明欄、「以官網為準」每支最多一次；放行人設（名字、口頭禪、固定收尾句照後台常設指示，不自己編；第一句仍是鉤子）。verifier 同步：第三方頁仍不確認數字，自家已查核文章只在官方頁 failed 時確認，NOT FOUND 仍是 drop the number or the sentence，CONFIRMED 的數字不准換成「以官網為準」。outro 固定三句（答案帶數字、觀眾答得出的留言題、有理由的訂閱邀請；下一集只在企劃／payload／常設指示有給時點名，不編題目）；cta 卡仍是片中唯一推文章的景，說「說明欄的文章」不說「第一行」。開場：前 20 秒要有具體數字／日期／專有名詞、禁目錄式開場、「你以為…其實」每支一次。第 103 行解禁 `screencast`：對 `sources` 裡每個抓得到的官方頁至少一景，步驟格式照 `tools/video/screencast/steps.mjs`（goto→wait→capture focus+zoom、click／fill／mask 的限制、N 張截圖 reveal N−1 次、第一句不 reveal）；**版型（`screencast/scene.mjs`）只畫 `title` 與 `caption`，角落沒有來源與日期戳**，所以提示詞要撰稿把「來源名稱＋抓取日」寫進 `caption`。登入後介面只說一次「選單以你登入後看到的為準」。diagram 仍不用。縮圖：大字 ≤6 字、兩行在詞的邊界斷、不重複標題前 10 字、`data.shot`（鉤子段落的具體物件）或 `data.capture`（screencast 景 id）二選一當主體（欄位名照縮圖票；`schema.mjs` 不檢 `thumbnail.data` 的鍵，所以在版型做好前不會被 lint 擋）。
- **`lint.mjs`**：新 `episodeScriptProblems(doc, timeline)`（全是 warn）：片語家族 `HEDGE_FAMILY`（以官網為準／以官方為準／公告沒寫／公告沒有寫／不代表／我不唸／不在這裡唸／不替你填）全片合計 >1 就警告並列出每個片語的次數；前 40 秒（估計時間軸）出現「接下來分三段」「看完你會知道」或「第一，…第二，…最後」三個都在就警告；`outro` 旁白沒有「訂閱」、或不到三句，各一條警告。**閘門**：只對非漫劇、zh-TW 旁白、估計長度 ≥ `MIN_EPISODE_MINUTES`（常數 8，不是測試可放寬的 `minEpisodeMinutes()`）的稿子跑。理由：既有 fixture（minimal、illustrated、terminal、explainer、story）的 outro 都沒有「訂閱」，而 `drama.test.mjs`、`terminal.test.mjs`、`explainer.test.mjs`、`story.test.mjs`（都不在本票 scope）斷言它們 lint 零警告；fixture 只有幾十秒，是版型的範例不是稿子；正式稿不到 8 分鐘本來就是錯誤會被退回重寫，所以每支交出來的稿都會過這層。
- **測試**：`lint.test.mjs` 加三個案例（拉長到 8.5 分鐘的 minimal 只剩 outro 兩條警告、補三句後零警告、片語家族一次不警告兩次警告並列數、三種目錄句型與開場之後的「第一第二最後」不算）；`prompts.test.mjs` 加一個案例鎖住撰稿與查核的新文字，並從 `steps.mjs` 讀 `ACTIONS`／`MAX_STEPS`／`MAX_ZOOM`／`MAX_WAIT_MS` 確認提示詞描述的格式跟 schema 一致。
- **跑過**：`node --test tools/video/core/lint.test.mjs tools/video/automation/prompts.test.mjs` 60/60；`node tools/video/cli.mjs lint --file` 對 illustrated、showcase、screencast tutorial 三個範例，輸出跟改前逐行相同（都只有本來就在的 8 分鐘下限兩個 ERROR——票的「零錯誤」驗收在 CLI 下本來就不成立，只有測試環境放寬下限才零錯誤）。`npm run test:tools` 2013 個測試 2009 過、1 紅（本來就紅的「the shipped independent duration review binds the current plans and implementation」；基準另一個「API compiler and publication join run with the provisioned API runtime」這次沒紅）。

沒做／留給別人：

- `.claude/skills/youtube-video/references/script-writing.md` 沒有建：那個目錄不存在，`tools/skills.test.mjs` 明文只允許 `.claude/skills/<name>/SKILL.md`，references 只存在 `.agents` 一份。票的 scope 這一行是過時的。
- 「說明欄第一行的文章」不在 `prompts.mjs`，在 `tools/video/templates/fixtures/showcase/video.json`（sa25 旁白與 cta 卡的 `sub`，不在 scope）；撰稿是照 showcase 抄的，要連 minimal、illustrated、showcase 三個 fixture 的 outro（都沒有「訂閱」、不到三句）一起改才會真的帶動新稿——建議另開票改 fixture（改了要同步 `lint.test.mjs`「lints clean」的斷言與 `drama.test.mjs:901`）。
- 翻譯類階段的 `COMMON` 仍寫舊的「None there: … 以官網為準 on the slide」，因為 `automation.test.mjs` 釘 SHA-256；下次有人動那個測試檔時把四個雜湊更新並讓所有階段共用 `WRITING_COMMON`。
- `register.mjs` 的 `REGISTER_RULES`（不在 scope）仍寫「Later chapters may turn the same way」，與站主「你以為…其實每支一次」略衝突；提示詞裡我用「once in the video, in the first chapter」蓋過，lint 沒有計「你以為」。
- payload 的 `sources` 沒有「這是 Mokaair 文章」的旗標（`flow.mjs` 的 `siteSources` 只是把 `source_guide` 的網址排第一）；提示詞用最保守的判準：mokaair.com 的頁、頁面文字看得到查證日，才算「已查核文章」。站上文章頁有沒有把查證日印出來我沒驗證（apps/web 不在 scope），沒印的話這條放行等於沒放行，要在文章頁或 payload 補旗標。
- 縮圖的 `data.capture` 要等縮圖票把版型與 render 做進去才有畫面；`qa/thumbnail.mjs` 的 ≤6 字、LCS、斷詞檢查也在那張票。
- `automated.md` 第 102 行關於 screencast 的段落沒改（不在 scope，而且它描述的是格式，沒有「不准用」的字）。

### 2026-10-08 審稿後修正（claude-fable，同一分支）

審稿人對 60cdbef1 提了 1 個 must-fix、3 個 should-fix，四條都改了，全在 scope 內：

- **must-fix：翻譯標題的頻道規則警告擋了 QA。** `lint.mjs` 把 `youtubeWarnings`（寬度 >36、問號 >1、頓號清單、集數）對翻譯標題的警告放在 `i18n/<locale>.json` 路徑下，而 `tools/video/qa/checks.mjs` 的 `captionsItem` 把每一條 `i18n/` 開頭的 lint 警告都當成 captions 項的**失敗**（只有孤兒章節標題那句留警告），所以 why-openai-killed-sora 等 12 支已上線的稿子在 QA 會紅、`qa` CLI 以 EXIT.lint 結束。改法：那一行改成 `warn(\`youtube/${locale}\`, problem)`；`checkYoutubeFields` 的「(package refuses it)」那行不動（那是上傳包真的會拒絕的）。`lint.test.mjs` 新案例：39 格寬、不到 100 字的英文標題只產生 `youtube/en` 一條警告，`captionsItem` 仍 ok；`a<b>` 這種上傳包會拒的仍在 `i18n/en.json` 且 `captionsItem` 失敗。審稿人給的驗證指令現在印 `true caption files for zh-TW, ja, en, every translation current`。
- **should-fix：單獨的「不代表」誤報。** 已上線稿子裡 18 句「不代表」沒有一句在替數字打馬虎眼（「字數少，不代表 token 少」「有聊天框，不代表背後只會聊天」）。改成：`HEDGE_FAMILY` 拿掉「不代表」；新 `HEDGE_AFTER_UNWRITTEN = ["不代表", "不等於"]` 只在同一句含 `UNWRITTEN`（沒寫／沒有寫／沒列／沒提／沒說…）時才計（「公告沒寫，不代表沒有」仍算 2 次）。沒照審稿建議直接列「不代表沒有」當片語，因為審稿人自己舉的反例「免費不代表沒有上限」就含那四個字。重跑 docs/videos：ai-agent-vs-chatbot、ai-agents-explained、ai-citation-check、ai-term-token 不再警告；google-vids 從 5 降到 3（公告沒有寫 ×1、公告沒寫 ×2，都是真的）；openai-devday（以官網為準 ×6）、siri、sora 照舊。`prompts.mjs` `NUMBERS_RULE_WRITING` 與 `script-writing.md` §句子 同步改寫。
- **should-fix：目錄式開場抓不到已上線稿子的寫法。** 改 `OPENING_TOC`：「看完」句型 這支／影片 各自可選；「接下來」句型允許 我、加 告訴你／帶你（看）；新 `FIRST_NEXT_LAST`（句首 先／再／最後 三個都在前 40 秒）；新 `announcesList()`：含 這集／這支／這部／接下來／帶你／跟我／我分 的句子，加下一句，清單記號（、、還有／以及、句首 再／最後、三步／五件 這種計數、「、…與／和」）≥2 就算。對 16 支 zh-TW 非漫劇稿直接呼叫 `episodeScriptProblems`：ai-price-war、ai-real-jobs-chart、openai-agents-broke-in、ai-bug-fix-pr-review、ai-citation-check、rtx-spark（審稿人列的六支）加 always-on-agent、free-vs-paid、openai-devday、why-openai-killed-sora 會警告，共 10/16；ai-coding-tools、gpt6、google-vids、siri、ai-term-*、sothatswhy 不會。注意 ai-real-jobs-chart（7.3 分）、always-on-agent（7.1 分）、gpt6（7.2 分）估計長度不到 8 分鐘，`lintVideo` 的閘門不會對它們跑這層，CLI 看不到；測試用拉長的 fixture 把這些開場當第一句驗。`lint.test.mjs` 以上面八個已上線開場為正例、四個為反例。
- **should-fix：撰稿提示沒有標題與標籤規則。** `prompts.mjs` 撰稿段把「youtube.title at most 100 characters … tags at most 500 characters」換成從 `core/metadata.mjs` 讀常數的三條：標題 ≤ `TITLE_WARN_WIDTH`（36）格含「｜系列名」後綴、不編集數、最多一個「？」、不用頓號列三項、不用 `TITLE_BANNED` 六個句型，100 字與尖括號是上傳包的底線不是目標；標籤 ≤ `TAGS_MAX_COUNT`（10）、繁中詞與英文產品名放前面；說明欄那段原文不動。`prompts.test.mjs` 釘住。翻譯階段的 `COMMON` 與 translator 指示仍被 `automation.test.mjs` 的 SHA-256 釘住，沒動（同之前的 Notes）。
- 跑過：`node --test tools/video/core/lint.test.mjs tools/video/automation/prompts.test.mjs` 63/63；`node --test tools/video/core/metadata.test.mjs tools/video/qa/checks.test.mjs tools/skills.test.mjs tools/video/automation/automation.test.mjs` 195/195；`cmp` 兩份 SKILL.md 相同；`npm run test:tools` 結果見下方／回傳。工作樹同時有另一個代理在改縮圖票的檔（qa/thumbnail、templates、visuals.md 等），那些不是本票的，沒碰。
