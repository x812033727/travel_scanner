---
id: 2026-10-18-curio-s-axis-history-figures-and
title: Curio S axis: history figures and famous scenes, plan and topic bank
status: done
priority: P2
area: docs
owner: claude-opus-5-5-history-stories
claimed_at: 2026-10-18T23:07:31Z
created_at: 2026-10-18T23:07:06Z
completed_at: 2026-10-18T23:16:51Z
branch: claude/history-stories-axis
depends_on: []
scope:
  - docs/videos/history-curiosity/README.md
  - docs/videos/history-curiosity/topics.json
---

# Curio S axis: history figures and famous scenes, plan and topic bank

## Why

站主 2026-10-18 想做講歷史人物、歷史事件的小故事系列（國家不限、不碰爭議，例如三國、織田信長的時代），
標題要讓人想點，點進來後要一直有鉤子。企劃建議把它做成奇聞檔案局的第六軸 S（歷史人物與名場面），
因為「演義／軍記物 vs 正史」剛好對上系列的三段（流傳的版本 → 紀錄 → 現在怎麼看），畫風、路線、評審、
lint 與預算可以全部沿用。站主看完企劃說「用你建議的」。

## Definition of done

- [x] `docs/videos/history-curiosity/README.md` 有 §S 軸：為什麼放在奇聞檔案局、六種鉤子、一集怎麼講、
      示範開場、題庫與順序、試片三集、不收的題目、畫面注意事項，以及主機路線還沒認得 S 的說明。
- [x] `topics.json` 有 S01–S36（`candidate`），`series.axes` 有 S，`note` 寫明第三批的來歷。
- [x] 主機路線的 S 主軸與試片三集各有自己的票。

## Steps

- [x] 跟既有 188 題比對，拿掉重複的鄭和寶船（H28）、秦始皇陵（H26）、圖坦卡門（H24）、倫敦大火（P17）。
- [x] 寫 README §S 軸、§題材的表、§選定紀錄、§票。
- [x] 開 `2026-10-18-curio-host-route-knows-the-s` 與 `2026-10-18-curio-s-axis-pilot-s01-red`。

## How to verify

`python3 -c "import json;d=json.load(open('docs/videos/history-curiosity/topics.json'));print(sum(t['axis']=='S' for t in d['topics']))"`
印出 36；`npm run check:tasks` 過。

## Notes

- 題目卡上的事實是憑既有知識寫的，沒有開來源；查核走 `2026-10-10-curio-topic-bank-checks` 的做法（研究加獨立覆核），
  試片三集在試片票裡查。
- 原本要在這張票順手把 S 加進 `explainer-series.mjs`，但那些提示詞的雜湊被 `explainer-series.test.mjs` 釘住，
  而那個測試檔在 `2026-10-14-ai-and-tech-videos-tell-one`（進行中）的 scope 裡；改提示詞也會讓進行中的奇聞檔案局
  journal 重問一次。所以拆成另一張票。
