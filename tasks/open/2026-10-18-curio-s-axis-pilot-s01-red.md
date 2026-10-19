---
id: 2026-10-18-curio-s-axis-pilot-s01-red
title: Curio S axis pilot: S01 Red Cliffs, S09 Okehazama, S18 Napoleon
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-history-stories
claimed_at: 2026-10-18T23:59:48Z
created_at: 2026-10-18T23:11:24Z
completed_at:
branch: claude/curio-s01
depends_on: []
scope:
  - docs/videos/curio-s01
  - docs/videos/curio-s09
  - docs/videos/curio-s18
  - docs/videos/history-curiosity/topic-checks/S01.md
  - docs/videos/history-curiosity/topic-checks/S09.md
  - docs/videos/history-curiosity/topic-checks/S18.md
  - docs/videos/history-curiosity/topics.json
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
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

- 2026-10-19（claude-opus-5-5-history-stories）：S01 大綱草稿 `docs/videos/curio-s01/brief.md`（A 案「曹操的兩封信」建議、
  B 案「黃蓋的那封信」、不採用的 C 案），等站主選。查核清單 `topic-checks/S01.md` 18 列，**全部 UNOPENED**：
  這個雲端環境的網路政策擋掉 ctext.org、zh.wikisource.org、zh.wikipedia.org，原文開不了，表裡的引文是憑記憶寫的。
  下一步：在能開這些網站的環境（或站主把網域加進允許清單後）逐列開《三國志》與裴注原文，再找另一個代理做獨立覆核；
  第 9 列（吳主傳「公燒其餘船引退」）與第 14 列（江表傳曹操給孫權的信）是主線的骨架，被推翻就重寫大綱。
- 2026-10-19（同上）：站主選 A 案。S01 稿子寫完：`docs/videos/curio-s01/video.json`、`script.md`、`NOTES.md`；
  lint 0 錯誤（警告：8.7 分鐘、sources 故意空著）；盲評七輪，第七輪 13／13 通過。查核清單擴到 32 列，仍全部 UNOPENED，
  網路政策照舊擋著原文網站。下一步是查核，不是生圖。
- 2026-10-19（同上）：S09 大綱草稿 `docs/videos/curio-s09/brief.md`（A 案「信長的那一夜與那一場雨」建議、B 案「今川義元的最後一天」、
  不採用的 C 案「一把刀的四百年」），等站主選。查核清單 `topic-checks/S09.md` 24 列，全部 UNOPENED：網路政策也擋掉
  ja.wikisource.org、dl.ndl.go.jp、www.aozora.gr.jp、ja.wikipedia.org。結檔「存檔」或「未結」要等第 18 列（正面攻擊說的學界狀態）查完。
- 2026-10-19（同上）：站主選 S09 A 案。稿子寫完：`docs/videos/curio-s09/video.json`、`script.md`、`NOTES.md`；
  lint 0 錯誤（警告：8.1 分鐘、sources 故意空著）；盲評六輪，第六輪 13／13。查核清單擴到 35 列，仍全部 UNOPENED。
  結檔暫定「未結」，等第 18 列。
- 2026-10-19（同上）：S18 大綱草稿 `docs/videos/curio-s18/brief.md`（A 案「一個數字的旅程」建議、B 案「小下士的一生」、
  不採用的 C 案「拿破崙情結的科學」），等站主選。查核清單 `topic-checks/S18.md` 17 列，全部 UNOPENED：網路政策也擋掉
  en.wikisource.org、gallica.bnf.fr、www.napoleon-series.org、archive.org、www.britishmuseum.org。
- 2026-10-19（同上）：站主選 S18 A 案。稿子寫完：`docs/videos/curio-s18/video.json`、`script.md`、`NOTES.md`；
  lint 0 錯誤（警告：8.2 分鐘、sources 故意空著）；盲評九輪，第九輪 13／13。查核清單擴到 34 列，仍全部 UNOPENED。
  三集的稿子都寫完了；這張票剩下的是三集的查核（要開放原文網站）與之後的旁白、插圖、成片、實測。
- 2026-10-19（同上，分支 `claude/curio-s01-check`）：S01 查核完成並經獨立覆核，用 GitHub 上的四庫本《三國志》轉錄
  （殆知閣 v2.0、Kanripo KR2a0012）代替被擋的 ctext／維基文庫。主線成立；旁白依查核改七處，`sources` 與 `claims.md` 補齊。改稿後盲評第八輪 12／13（重述），
  再改兩處後第九輪 13／13；lint 0 錯誤 0 警告、9.0 分鐘。
  剩：中華書局本核對兩處異文（S01.md 第 4、13 列）。S09、S18 的查核還沒做：日文與英法文來源仍被擋，
  可以先找 GitHub 上有沒有《信長公記》或拿破崙驗屍報告的公開文本。
- 2026-10-19（同上，分支 `claude/curio-s09-check`）：站主開放網域後，S09 查核完成並經獨立覆核（35 列，24 維持、10 加但書、
  0 推翻）。來源：維基文庫《信長公記》我自刊我書本、國會圖書館的甫庵《信長記》古活字版與參謀本部《日本戰史 桶狹間役》、
  文化廳國指定文化財 DB。第 3 章照公記重排、四處誤譯改正、刀銘加上「尾張守／上總介」的疑問；盲評第十輪 13／13，lint 0 錯誤、9.0 分鐘。
  剩：陽明本、天理本沒開；S18 的查核還沒做。
- 2026-10-19（同上，分支 `claude/curio-s18-check`）：S18 查核 34 列完成（安托馬爾基驗屍紀錄、康斯坦、Komlos 2003、國會圖書館的吉爾雷版畫、
  1802–03 年外交文件、Maitland、韋氏字典等）。主線成立；157 公分改成假設語氣，1812 年日常用呎的不確定寫進說明欄；
  「拿破崙情結」的來歷、近衛擲彈兵下限、法國抗議的對象改正。獨立覆核 1 列推翻（「小下士」是拉斯卡斯的敘述）、8 列加但書，
  照改；結論卡改「他不矮，是被畫小了」。盲評第十三輪 13／13，lint 0 錯誤、8.8 分鐘。三集的稿子與查核都完成。
- 2026-10-19（同上，分支 `claude/curio-s01-narration`，雲端容器）：三集旁白站主聽過（「三集都沒問題」）；插圖站主授權上限
  US$9.64，三集一起畫完，全部過評審：S01 84 張 US$1.73（八景改提示詞重畫）、S09 80 張 US$1.74（六景）、
  S18 74 張 US$1.85（十一景），合計 US$5.32，沒有換圖或改成卡片。改提示詞都照「一個人做一件事」。
  雲端怎麼做旁白與插圖寫進 `curio-episode` skill 新的一節。下一步：`review-push --gate storyboard` 給站主看分鏡、成片、品管、上架包。
- 2026-10-19（同上）：站主要把雲端做法寫進 `curio-episode` skill，scope 加上兩份 skill。另外三張票的 scope 也有這份 skill
  （`2026-10-19-curio-keeps-the-brand-stories-hook` 狀態 review、#1577 已合併；`2026-10-14-curio-episodes-keep-the-series-look` #1500
  與 `2026-10-14-ai-and-tech-videos-tell-one` #1504 也已合併），沒有人還在改它；這次只在〈交接〉前加一節，跟 main 合併沒有衝突。S09 刀銘卡補「意思是：討取義元」，
  因為旁白為了唸對改成白話，跟卡上的原文不一樣。
