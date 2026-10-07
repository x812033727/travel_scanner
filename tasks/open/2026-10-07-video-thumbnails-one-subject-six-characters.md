---
id: 2026-10-07-video-thumbnails-one-subject-six-characters
title: Video thumbnails: one subject, six characters, three rotating layouts, QA
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-07T15:24:58Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/templates
  - tools/video/qa/thumbnail.mjs
  - tools/video/qa/thumbnail.test.mjs
  - .agents/skills/youtube-video/references/visuals.md
  - .claude/skills/youtube-video/references/visuals.md
  - docs/videos/README.md
---

# Video thumbnails: one subject, six characters, three rotating layouts, QA

## Why

頻道診斷（`docs/videos/channel-review-20261007/README.md` §2.1 D05）看過 18 張縮圖：09-27～09-30 上架的 11 張是 `theme.css` `.thumb-art` 的青綠圓環＋橘點同一版型只換字；10-04 後 7 張用關鍵影格鋪底，但主體是片中的比喻（咖啡店員、盆栽、雨傘、雜貨店收據），只有 2 張對得上題目。大字 11/18 超過 `visuals.md` 的 6 字上限（程式只擋 12 字：`compilation.mjs:29`、`plan.mjs:36`），11/18 與標題重複過半，兩張斷行拆詞（「一半的攻／擊」「建議日不／是生效日」）。三份規格互相矛盾：`docs/videos/README.md` §版型「一個標籤、一行大標、一行小字」（沒有主體）、`visuals.md` 第 57–58 行「≤6 字＋一個視覺主體、不重複標題」、`prompts.mjs` 第 204 行「≤10 字兩行」。沒有 CTR 數據前不能說縮圖壓低了點擊（觀看前四名全是同一版型），所以先做低成本的 QA 與規格統一，版型重做等 Studio 的曝光點閱率。

## Definition of done

- [ ] `qa/thumbnail.mjs` 加三條：大字 ≤6 個 CJK 字（英文詞另計）、兩行斷詞不拆詞（Node 22 `Intl.Segmenter`）、大字與標題前 10 字的最長共同片段 >50% 就警告；`thumbnail.test.mjs` 覆蓋。
- [ ] `README.md`、`visuals.md`（兩份）、`prompts.mjs` 第 204 行的縮圖規格改成同一套（≤6 字、一個主體、不重複標題、底色由主體決定）。
- [ ] `templates.mjs` `thumbnailHtml` 與 `theme.css` `.thumb` 至少三套版型輪替（文字欄左 40%、主體右 60%；沒有主體圖時不再畫圓環＋橘點），`render` 的聯絡表看過。
- [ ] 主體來源寫進撰稿規則：為縮圖多畫一張「鉤子段落的主體物件」shot（主體在右三分之一、畫具體物件不畫比喻）；產品 logo／介面截圖仍不放（SKILL.md 規矩 6、ILLUSTRATED.md negative 擋 logo），要放得站主先改規矩。

## Steps

- [ ] 先把 QA 三條與規格統一做完（hours），不等版型。
- [ ] 版型：複製 `thumbnailHtml` 做 A／B／C 三版，`node tools/video/cli.mjs render --file tools/video/templates/fixtures/showcase/video.json` 看聯絡表；縮到 168px 寬確認大字可讀。
- [ ] 站主在 Studio 對 S88lbAsLz2E、UOgxCymxb1I、FYHFsj0SB7Q 各上一張 B 版做 Test & compare（桌機 Studio、兩週）；換縮圖前先給 `apps/api/app/video_youtube/sync.py` 的 `_thumbnail` 加「已換過就跳過」開關，否則同步會把原縮圖再送一次。

## How to verify

`npm run test:tools`；對 18 支現有的 `thumbnail` 資料跑新的 QA 應至少標出 11 支的大字超長與 4 支的照抄標題；聯絡表上三套版型在 168px 寬仍讀得到大字。

## Notes

`docs/videos/README.md` 只改 §版型的縮圖那一行與資料夾表，不動其他規格。版型重做是否優先，等 `docs/videos/channel-review-20261007/README.md` §6.3 的第 2 個數字（曝光 ≥1,000 後 CTR <2% 才是縮圖問題）。
