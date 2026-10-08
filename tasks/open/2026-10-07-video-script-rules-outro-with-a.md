---
id: 2026-10-07-video-script-rules-outro-with-a
title: Video script rules: outro with a subscribe reason, numbers said out loud
status: in-progress
priority: P2
area: tools
owner: claude-fable
claimed_at: 2026-10-08T00:12:08Z
created_at: 2026-10-07T15:24:57Z
completed_at:
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

- [ ] 新片的 `outro` 場景固定三句旁白：回答開場的問題、一個觀眾答得出的留言題、一句有理由的訂閱邀請（系列集點名下一集；單篇新聞片用頻道層的固定承諾或指向播放清單，不自動編造下一支題目）。
- [ ] 官方頁抓得到的數字講出口並在字卡用既有的 `stats.source`／`quote.source` 標「官網 YYYY-MM-DD」；官方頁抓不到（例如 OpenAI 全家對工人 UA 回 403）但自家已查核文章（帶 checked_on）有的，允許引用並標文章查證日；免責只留說明欄一句。
- [ ] `lint` 對「以官網為準／公告沒寫／不代表／我不唸」片語家族計數並 warn（不是硬錯誤，否則撰稿的 lint_errors 迴圈只會換同義句）；每支旁白超過一次就警告。
- [ ] `script-writing.md`（`.agents` 與 `.claude` 兩份同步）§開場、§句子、§結尾改成同一套說法，`npm run test:tools` 過。

## Steps

- [ ] 改 `prompts.mjs` COMMON 第 44–45 行與 verifier 第 250 行；確認 NOT FOUND 的處理仍是「drop the number or the sentence」（第 254 行）。
- [ ] 改 `prompts.mjs` outro 規則（第 82 行附近）與 cta 規則（第 80 行：片中已推過一次文章，結尾不再第二次）。
- [ ] `tools/video/core/lint.mjs` 加片語計數的 warn()，`lint.test.mjs` 補案例。
- [ ] 用 `tools/video/core/fixtures` 的 showcase 與 illustrated 範例跑一次 `lint`，確認既有範例不會被新規則打成錯誤。

## How to verify

`npm run test:tools`；`node tools/video/cli.mjs lint --file tools/video/core/fixtures/illustrated/video.json` 零錯誤；下一支由產線寫出的 `video.json` 的 outro 有三句、旁白全文「以官網為準」≤1 次、至少一個標了日期的數字字卡。

## Notes

不要改 `docs/videos/HANDS-OFF.md` 的立場草稿來達成這件事：正式站的立場是 10 條、存在 `channel_stance` 設定，改文件改不到正式站。片尾卡（3 秒按讚／分享／小鈴鐺，沒有「訂閱」）換成只求訂閱的新 `outro.mp4` 是站主用 `branding --install` 換素材包的事，見 `docs/videos/channel-review-20261007/README.md` §2.1 D03；已公開的 18 支只能由站主在 Studio 補結束畫面與置頂留言。
