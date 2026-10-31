---
id: 2026-10-31-b01-shimano-b02-lonely-planet-b03
title: 奇聞檔案局品牌三集：山葉 B01、Shimano B02、Lonely Planet B03（研究、稿子、查核、盲評，付費前報價）
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-curio-brand-b
claimed_at: 2026-10-31T14:58:22Z
created_at: 2026-10-31T14:58:19Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-b01
  - docs/videos/curio-b02
  - docs/videos/curio-b03
  - docs/videos/history-curiosity/topic-checks/B01.md
  - docs/videos/history-curiosity/topic-checks/B02.md
  - docs/videos/history-curiosity/topic-checks/B03.md
  - docs/videos/lexicon.json
---

# 奇聞檔案局品牌三集：山葉 B01、Shimano B02、Lonely Planet B03（研究、稿子、查核、盲評，付費前報價）

## Why

站主 2026-10-31 要三個黑猫研究院式的品牌題目，選了：山葉（做鋼琴的公司為什麼機車也叫山葉）、Shimano（不賣整車卻收全世界腳踏車的錢）、
Lonely Planet（BBC 買下又折價賣出的旅遊書）。站主說這類現在算奇聞檔案局系列，並說「開始做吧」。
所以照 `curio-episode` skill 做成 `curio-` slug（B 是暫定的「品牌」編號，`topics.json` 的六個主軸沒有這一類，要不要正式開 B 軸由站主決定）。

## Definition of done

- [ ] 三集各有 topic-check（逐列一手來源）、`brief.md`、`claims.md`、`video.json`（13 分鐘、開場五步、loops ≥ 8、插圖 ≥ 70%、配樂）
- [ ] 另一個代理獨立查核寫 `verify-1.md`；盲評兩位讀者沒有同否的題，存 `panel/`
- [ ] `node tools/video/cli.mjs lint --slug curio-b0N` 0 錯誤
- [ ] 旁白與插圖的張數與上限金額三集一次報給站主，核准後才跑付費步驟

## Steps

- [x] 研究：三集 topic-check（B01 70 列、B02 72 列、B03 76 列）
- [x] 撰稿：brief、claims、video.json（三集 lint 0／0；B01 13.2 分、B02 13.4 分、B03 13.3 分估計）
- [x] 獨立查核 verify-1.md（每集查核代理逐句，盲評改稿後再查改動句；B01 兩輪、B02 兩輪、B03 三輪）
- [ ] 盲評 panel
- [ ] lint 0 錯誤、報價給站主
- [ ] （站主核准後）tts → check-audio → keyframes → music → render/clips/assemble → captions → qa → review-push

## How to verify

`node tools/video/cli.mjs lint --slug curio-b01`（b02、b03 同）；`node tools/video/cli.mjs narrative --slug ...`。

## Notes

- 人物：山葉寅楠 1916 卒可畫；島野庄三郎 1958 卒未滿 70 年、不畫本人；Wheeler 夫婦在世、不畫。商標與可讀文字一律不畫。
- 容器有 2026-10-25 配對的影音權杖（`~/.mokaair/video-tool.json`），10-31 用 GET media/status 驗過有效。
- 2026-10-31 長度：skill 寫的「13 分鐘約 3,500 字（4.5 字／秒）」實際太長。lint 的估計是準的（H24 lint 12.2 分、實際旁白 12:10，約 3.5 字／秒）；
  第一版 B01 3,362 字 lint 估 16.1 分。三集改成正文約 2,700–2,800 字，lint 估 13.2–13.4 分。
- 2026-10-31 發音字典加 BBC（B B C）、Lonely、Shimano、TripAdvisor（null，待試聽）。B01 旁白沒有拉丁字母詞。
- 撰稿用的產生器在 session 暫存目錄，不進 repo；之後改稿直接改 video.json，再跑 `script --slug`。
- 2026-10-31 B01 盲評第 4 輪通過（兩位讀者 13/13）；`panel/reader-1.json`、`reader-2.json` 存檔，合併規則同主機（兩位都否才算否）。
  `narrative --answers` 要每題 evidence 以 `[tNNN]` 開頭，否則判 FAIL（不是內容問題）；合併腳本在 session 暫存，做法：取答「是」且有 id 的那份。
- 盲評前三輪三集都卡在同一處：開場預告超過兩個、講掉後面章節的結果。原因之一是 lint 要開場至少 3 個 loops setup（H24 NOTES 記過）；
  做法：利害句算一個 setup，加兩個停在結果之前的預告。其次是時間倒跳（另起一條持股或台灣的平行線）與片尾重述數字——片尾答案句只放第一次出現的數字或點名回呼。
- 人物：在世或過世未滿 70 年的人，旁白講到他時畫面不能有代表他的臉（職業＋性別也算指認）；只放手、物件或明顯無關的路人。三集查核共抓到約 40 張。
