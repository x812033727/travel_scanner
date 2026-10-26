---
id: 2026-10-26-curio-f-and-g-pilot-f01
title: Curio F and G pilot: F01 Cinderella, F14 Pandora, G01 Fox sisters, U17 told as a story
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-storyteller
claimed_at: 2026-10-26T23:50:45Z
created_at: 2026-10-26T13:43:57Z
completed_at:
branch: claude/clever-archimedes-4oqn4s
depends_on: []
scope:
  - docs/videos/curio-f01
  - docs/videos/curio-f14
  - docs/videos/curio-g01
  - docs/videos/curio-u17
  - docs/videos/history-curiosity/topic-checks/F01.md
  - docs/videos/history-curiosity/topic-checks/F14.md
  - docs/videos/history-curiosity/topic-checks/G01.md
  - docs/videos/history-curiosity/topic-checks/U17.md
---

# Curio F and G pilot: F01 Cinderella, F14 Pandora, G01 Fox sisters, U17 told as a story

## Why

奇聞檔案局 2026-10-26 加了 F 軸（童話、神話與怪談的原版）與 G 軸（靈異事件），並把「說書版」寫法（前三分之二說故事、後三分之一打開檔案）
用到 U 軸（`docs/videos/history-curiosity/README.md` §F 軸與 G 軸）。題材點閱量測（`docs/videos/storyteller-genres-20261026/README.md`）
量到童話神話與靈異是搜尋點閱最高的兩類，要用四集試片看在我們頻道上是不是也一樣。

## Definition of done

- [ ] 四集做到可以上架：F01 灰姑娘、F14 潘朵拉、G01 福克斯姊妹、U17 希爾夫婦（說書版）。
- [ ] 每集的題目查核與獨立覆核寫在 `docs/videos/history-curiosity/topic-checks/<id>.md`，查不到的事實拿掉。
- [ ] 上架兩週後記下曝光點閱率、前 30 秒留存、平均觀看時長，跟已上架的奇聞檔案局比，寫進這張票的 Notes。

## Steps

- [ ] 讀 `.agents/skills/curio-episode/SKILL.md` 與 `youtube-video`；新集走主機可愛解說路線（cute-mystery），主機還不認得 F、G 時，
      照 skill §選路線 走本機漫劇格式。
- [ ] 逐題查 `topics-fg.json` 的 `facts_to_verify`（U17 在 `topics.json`），第一手來源優先：格林初版與第二版書影、赫西俄德與伊拉斯謨、
      1888 年《New York World》、空軍藍皮書檔案。
- [ ] 稿子照 README §一集怎麼講（說書版）與 skill §稿子；F01 的示範開場在 README，查核後再改。
- [ ] 畫面守 README §版權與畫面：不畫迪士尼造型，切腳與啄眼不畫傷口。
- [ ] 上架選「不是為兒童打造」。

## How to verify

`node tools/video/cli.mjs lint --slug curio-f01`（其他三集同）沒有錯誤；四份 `topic-checks/*.md` 都有獨立覆核的結論。

## Notes

這張票由 `2026-10-26-curio-f-and-g-axes-fairy` 拆出來。U17 的題目卡在 `topics.json`（狀態 checked），F01、F14、G01 在 `topics-fg.json`。
