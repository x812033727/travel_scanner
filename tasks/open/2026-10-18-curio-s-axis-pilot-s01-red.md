---
id: 2026-10-18-curio-s-axis-pilot-s01-red
title: Curio S axis pilot: S01 Red Cliffs, S09 Okehazama, S18 Napoleon
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-18T23:11:24Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s01
  - docs/videos/curio-s09
  - docs/videos/curio-s18
  - docs/videos/history-curiosity/topic-checks/S01.md
  - docs/videos/history-curiosity/topic-checks/S09.md
  - docs/videos/history-curiosity/topic-checks/S18.md
  - docs/videos/history-curiosity/topics.json
---

# Curio S axis pilot: S01 Red Cliffs, S09 Okehazama, S18 Napoleon

## Why

奇聞檔案局的 S 軸（歷史人物與名場面，`docs/videos/history-curiosity/README.md` §S 軸）要先做三集試片，
看三個地區哪一個的留存最好：S01「為什麼曹操說，赤壁的船是他自己燒的？」（中國）、S09「兩千人打兩萬五千，
信長真的是繞路奇襲嗎？」（日本）、S18「拿破崙其實不矮？」（歐洲）。三題的題目卡都是 `candidate`，事實沒有開過來源。

## Definition of done

- [ ] S01、S09、S18 各有 `topic-checks/<id>.md`（研究加獨立覆核，照 `2026-10-10-curio-topic-bank-checks` 的格式），通過的題目在 `topics.json` 改 `checked`。
- [ ] 三集照 `curio-episode` skill 做完：大綱站主選、稿子有 `loops` 表、lint 0 錯誤、旁白站主聽過、插圖整集一次報價一次畫、成片過品管、上架包。
- [ ] 每集的實測（插圖張數與重畫、花費、旁白長度、品管分數）寫回 README §成本與產能。

## Steps

- [ ] 三題的研究與獨立覆核；改掉題目卡上錯的事實（特別是赤壁的曹操信出處、桶狹間的兵力數字、拿破崙驗屍紀錄的換算）。
- [ ] 讀 `curio-episode` skill；新的一集走主機可愛解說路線（`cute-mystery`）。主機路線還沒認得 S 主軸時（票 `2026-10-18-curio-host-route-knows-the-s`），縮圖標籤與「主軸：」要人工改成 S。
- [ ] S01 → S09 → S18，一集一個 PR 或一集一次交接。

## How to verify

`node tools/video/cli.mjs lint --slug curio-s01`（及 s09、s18）0 錯誤；`topics.json` 的 S01、S09、S18 是 `checked` 以上。

## Notes

示範開場（S01）在 README §S 軸，可以直接當稿子的起點，但查核後可能要改。
