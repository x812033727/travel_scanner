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

### 進度（2026-10-27）

- 站主 2026-10-26 的決定：大綱用推薦的、不用問；四集插圖加配樂上限 US$15；U17 結檔蓋「存檔」；稿子 PR 綠了就自動合併。
- 查核：F01 研究與獨立覆核完成（ADOPT_WITH_CHANGES，覆核 18 列同意、0 改判）；G01 研究完成（ADOPT_WITH_CHANGES），獨立覆核進行中；
  F14 研究進行中（容器重啟後接續）；U17 沿用 2026-10-12 的查核。
- 稿子：U17、F01 撰稿中（各一個撰稿代理，只寫自己的資料夾，lint 0 錯誤後交回）；G01、F14 等覆核完成再開。
- 網站登入：2026-10-26 第一次的配對碼過期沒人按，等稿子寫完再重開。
- 稿子（2026-10-27）：四集都 lint 0 錯誤 0 警告、盲評通過（兩位只讀旁白的新讀者，兩位都答否才算沒過）：
  F01 第 2 輪、U17 第 3 輪、F14 第 4 輪、G01 第 4 輪；最後一輪的讀者答案存在各集 `panel/`。估計長度 F01 13.2、
  F14 12.3、G01 13.3、U17 13.3 分鐘（不含片頭片尾）。
- 盲評學到的（下一批照做）：
  - **「先說故事、再開檔案」會被判 one_line 不過**：檔案那段一定回頭重講同一晚。U17、G01 改成**單一時間線**，
    每份紀錄在它出現的年份打開，才過；F01、F14 本來就照時間走。README 的「前三分之二說故事、後三分之一打開檔案」
    要改成「照時間走，紀錄在它出現的那一刻打開」（README 不在這張的 scope，跟示範開場一起改）。
  - 開場最多兩個預告，而且不能講出結果（F14 第一版開場就說「大罐子」）；重複的數字或事實一律只講一次，
    回頭要用「還記得…」並補新東西。
  - 跟主題無關的段落（F14 的希望爭論、神譜裡對女人的那段）兩輪都被判岔題，直接刪比改寫快。
  - 撰稿代理照原文補的情節，要另外逐句對查核表（F01 補了 #19–#60，改了八句說過頭的）。
- 要站主決定的（不擋旁白）：F14、G01 沒有照片卡（目前格式只收文字卡；1508 年印本書頁、Currier 石版畫要不要放）；
  U17、F14 的「說故事／開檔案」比例沒到三分之二（照時間走之後這個比例不再適用）。
- **要另外修**：`docs/videos/history-curiosity/README.md` §F 軸與 G 軸 的 F01 示範開場有三處跟查核相反（初版的鞋是金的不是玻璃；
  「當了王后就不用走路」是 1819 年第二版的句子；榛樹 1819 年才出現）。README 不在這張票的 scope，交給
  `2026-10-26-merge-curio-f-and-g-topics`（那張要動 README 的引用）一起改，或另開小票。
