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
  - tools/video/package
  - .agents/skills/youtube-video/references/publish.md
  - .claude/skills/youtube-video/references/publish.md
---

# Video metadata: title length lint, description first line, UTM and series hashtag

## Why

頻道診斷（`docs/videos/channel-review-20261007/README.md` §2.2 D06、D13 留下的事實）：18 支標題中位 40 個全形字、最長 57，9 支超過 `publish.md` 自己寫的 40 字，而 `prompts.mjs` 只檢 100 字；只有 5/18 標題含數字且多是版本號；6 支用「是誰測的／怎麼讀／先分清」同一句型（參考頻道 150 支裡 0 支）。說明欄 15/18 第一行是網址（S88lbAsLz2E、UOgxCymxb1I、zxHRm5jnELc 同一網址出現 3 次）、鉤子句掉到第 3 行；10-04 後 6 支的站內連結沒帶 `utm_source=youtube`；旁白模板說「說明欄第一行」但 `composeDescription` 09-26 改成連結第一行後兩邊沒同步（cc09kA17Xsw 363s、xSrFAMk_udE 188s 指路錯）；18 支各 3 個 hashtag 全是題目詞，沒有系列 hashtag，說明欄互相連結 0 次。

## Definition of done

- [ ] `lint` 對 `youtube.title` 檢查：≤36 個全形字（警告）、前 15 字內有產品名或主詞、最多一個「？」、禁用詞清單（是誰說的、是誰測的、怎麼讀、先分清、先問）命中就警告；`metadata.test.mjs` 覆蓋。
- [ ] `composeDescription` 固定：第一行一句鉤子（結論或反轉）、第二行給誰看、第三行留言題，文章連結放第四行以後且同一網址只出現一次；每個站內連結都帶 UTM；第三個 hashtag 由 `category`／系列決定（例如 #AI名詞十分鐘、#AI月費算盤）。
- [ ] 撰稿提示裡「說明欄第一行的文章」改成「說明欄的文章」，或讓 `package` 真的把連結放第一行之後——兩邊一致即可。
- [ ] `publish.md`（兩份）§標題、§說明欄改成與程式一致的順序，`docs/videos/README.md` §說明欄不在這張票的 scope，改它另開票或併進縮圖票。

## Steps

- [ ] 讀 `tools/video/core/metadata.mjs` 的 `composeDescription` 與標題檢查，列出現在實際的順序。
- [ ] 加標題 lint 與說明欄組裝規則，補測試。
- [ ] 對 18 支現有 `video.json` 跑一次新 lint，把警告數記進 Notes 當基準。

## How to verify

`npm run test:tools`；`node tools/video/cli.mjs lint --slug <任一已上架 slug>` 對 57 字的 UWYoO3JfOK0 標題給出警告；`package` 產出的說明欄第一行不是網址、所有 mokaair.com 連結帶 UTM、同一網址只出現一次。

## Notes

已公開的 18 支改標題與說明欄只能站主在 Studio 手改（`publish.md` 寫明網站不動已公開的影片）；候選的新標題在 `docs/videos/channel-review-20261007/README.md` §3 逐支表與 §5。手機列表到底顯示幾個全形字沒有量過（publish.md 寫 40、第三方只量拉丁字元），36 字是保守值。
