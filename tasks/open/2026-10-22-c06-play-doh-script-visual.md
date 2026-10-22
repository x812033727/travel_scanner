---
id: 2026-10-22-c06-play-doh-script-visual
title: Write and independently check C06 Play-Doh script and visual plan
status: review
priority: P2
area: docs
owner: codex-gpt6-c06-script
claimed_at: 2026-10-22T03:50:34Z
created_at: 2026-10-22T03:50:28Z
completed_at:
branch: codex/brand-story-play-doh-c06-script
depends_on: []
scope:
  - docs/videos/story-everyday-play-doh-c06/script.md
  - docs/videos/story-everyday-play-doh-c06/script-evidence.md
  - docs/videos/story-everyday-play-doh-c06/visual-plan.md
  - docs/videos/story-everyday-play-doh-c06/visual-plan.tsv
  - docs/videos/story-everyday-play-doh-c06/build-local.mjs
  - docs/videos/story-everyday-play-doh-c06/series.json
  - docs/videos/story-everyday-play-doh-c06/brief.md
  - docs/videos/story-everyday-play-doh-c06/video.json
  - docs/videos/story-everyday-play-doh-c06/reviews/script-review.md
  - docs/videos/story-everyday-play-doh-c06/reviews/blind-reader-1.md
  - docs/videos/story-everyday-play-doh-c06/reviews/blind-reader-2.md
  - docs/videos/story-everyday-play-doh-c06/reviews/visual-preflight.md
  - docs/videos/story-everyday-play-doh-c06/production-quote.md
---

# Write and independently check C06 Play-Doh script and visual plan

## Why

C06 的企劃已由站主採用，仍缺可審的逐字稿、逐句證據、奇聞檔案局畫面計畫與整支試片報價。C03／C04 的劇本和付費核准不轉移到本集。

## Definition of done

- [x] 94 句逐字稿能逐句追到來源或標為編輯歸納；不把公司與博物館回顧冒充同時期原件。
- [x] 兩位獨立盲讀和另一位獨立來源查核留下雜湊綁定的審閱紀錄，擋下未修正的實質問題。
- [x] `video.json` 的旁白 ID 全數且只出現一次，插圖至少七成、連續資料卡不超過三張，畫風是 `cute-mystery`。
- [x] 逐鏡和整片成本停線可供站主審核；在站主核准劇本及付費額度前不生成付費媒體。

## Steps

- [x] 讀回 C06 已核准企劃與來源矩陣，建立逐字稿初稿。
- [x] 逐句獨立來源查核、修訂、兩位盲讀。
- [x] 製作逐鏡 JSON、視覺預檢與整支報價，執行必要 lint。
- [x] 建立草稿 PR 供站主審劇本與逐鏡方向；維持 review 狀態，不在草稿時 `done`。

## How to verify

`npm run test:docs-videos`、`npm run check:tasks`、影片結構 lint、逐句來源審閱及兩份盲讀紀錄；逐鏡 ID／畫面比例由腳本讀回，不以 Treatment 時長目標當 TTS 實測。

## Notes

- 2026-10-22：站主僅核准 Treatment 方向，逐字稿、鏡位、付款、上傳與發布均需各自關卡。
- 收藏機構記述 1955 年教室試用與正式推出、1956 年子公司向學校行銷；這是不同里程碑。沒有首筆訂單原件，腳本不定首次成交年份。
- 1960 申請／1965 核准的兒童造型材料專利不能倒推早年壁紙清潔膏配方，也不能證明今天市售配方。
- 第一版稿為 94 句，正文純語音仍待合成後實測；不能把片頭片尾動畫加進八分鐘門檻。
- 2026-10-22：script SHA256 `80671FCE0CC1D03E46B68361173FB547B156C255F1AF10468E3011389E08232F`、video SHA256 `666CD45A5E126D7F17DD95CCE1CACE213B07EAA2597340D3661D5CC3C3C4CBFA`；來源 94／94 PASS、兩位盲讀 PASS、獨立視覺預檢 PASS。80 張插圖、14 張字卡；`lint` 0 errors／0 warnings，`check:tasks` 通過。整支本機試片 US$25 仍只是提案。
- `npm run test:docs-videos` 235／236 通過；既有 Windows `imported-long-languages/runner.test.mjs:679` 子程序以 3221226505 崩潰、無 stdout/stderr（C05 分支同樣重現）。`tts --dry-run` 因本集尚無可證明的故事工作目錄而回 `STORY_LEXICON_MIGRATION_REQUIRED`；沒有嘗試付費配音。
- 2026-10-22：草稿 PR [#1676](https://github.com/x812033727/travel_scanner/pull/1676) 疊在 Treatment PR #1674 上，已加 `no-auto-merge`。票維持 review；等站主分別核准稿件及 C06 本集整支付費試片額度。
