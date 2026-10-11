---
id: 2026-10-10-curio-topic-bank-checks
title: Curio topic bank: independent re-check of H02-H07, then H08 and the other four axes in small batches
status: in-progress
priority: P3
area: docs
owner: claude-fable-curio-topics
claimed_at: 2026-10-11T17:39:46Z
created_at: 2026-10-10T14:38:30Z
completed_at:
branch: claude/curio-topic-bank-second-batch
depends_on: []
scope:
  - docs/videos/history-curiosity/topic-checks
  - docs/videos/history-curiosity/topics.json
---

# Curio topic bank: independent re-check of H02-H07, then H08 and the other four axes in small batches

## Why

奇聞檔案局的題庫（`docs/videos/history-curiosity/topics.json`，40 題）只有拍成集的 H01、U02、L08 查核過。2026-10-10 第一次整批查核（每題一個研究代理加一個覆核代理）因帳號每週用量上限中斷：H02–H07 的研究寫完了（`topic-checks/H02.md`–`H07.md`），但沒有人重開來源覆核，`topics.json` 仍是 `candidate`；H08 與 M、P、U、L 四軸的 31 題還沒查。前三集每一集都在查核時改掉題目卡上的事實（H01 的熱飯菜、U02 的「否認 58 年」、L08 的年份），沒查過的題目卡不能直接拿來寫企劃。

## Definition of done

- [x] H02–H07 各有「## 獨立覆核」一節（另一個代理重開來源，逐列 UPHELD／REFUTED／UNOPENED），通過的題目在 `topics.json` 改成 `checked`，`note` 寫查核後的更正；被否決的寫明處置。（2026-10-10：六題都是 ADOPT_WITH_CHANGES，都改成 `checked`。）
- [ ] H08 研究加覆核。
- [ ] 第二批新題（2026-10-11 站主「增加題目並查核」「能開幾個題目就幾個，無上限」）：95 張新卡 H09–H28、M09–M26、P09–P25、U09–U29、L09–L27 寫進 `topics.json`（candidate，題庫共 135 題），每題一個研究代理加一個獨立覆核代理；通過的改 `checked` 並換上覆核後的 title／hook／finding，被否決的在 `note` 寫處置。
- [ ] M、P、U、L 四軸：站主或下一季的排程決定先做哪一軸；每批 4–8 個代理，批與批之間看一次用量。
- [ ] `topic-checks/README.md` 的狀態表與實際一致。

## Steps

- [x] 開票、認領；第一批只放三個覆核代理（H02–H04），量每個代理的用量。
- [x] H05–H07 的覆核。
- [x] 依覆核結果改 `topics.json`（只改通過獨立覆核的題目）與 README 狀態表。
- [ ] H08；其餘四軸分批。
- [x] 2026-10-11 起草 95 張新卡並 commit（候選，憑既有知識寫的；先 15 張、再 80 張）。
- [ ] 新題分批查核：每批 5 題、一軸一題、照代號順序（H09、M09、P10、U11、L09 → H10、M10、P09、U09、L10 → …），批與批之間看用量；每批研究寫完再派覆核。這個 session 能做幾批就做幾批，沒查到的留 candidate，下一個 session 從 `topic-checks/README.md` 的狀態表接著做。

## How to verify

`grep -L "## 獨立覆核" docs/videos/history-curiosity/topic-checks/H0*.md` 沒有輸出；`python -X utf8 -c "import json;d=json.load(open('docs/videos/history-curiosity/topics.json',encoding='utf-8'))"` 可解析，`checked` 的題目都有對應的覆核一節；`npm run test:tools` 的衛生測試沒有抓到本機路徑。

## Notes

- 2026-10-11 第二批進度（claude-fable-curio-topics）：題庫擴到 188 題（55→135→188，三次 commit）。查核已完成研究＋獨立覆核並改 `checked`：M09、P10、L09；覆核完成、題目卡三行待整理：H09、U09、P09；研究完成等覆核：H10、H11、M10、U11、L10、L11；研究中：H12、M11、M12、P11、P12、U10、U12、L12。中途一次撞到帳號的 session 用量上限（21:00 UTC 重置），16 個代理中斷：中斷的覆核代理有三個其實已把〈獨立覆核〉寫完只差回報，兩個研究代理留下半份草稿（U10、P11）由接手的代理續寫，其餘重派。教訓：同時跑 15 個代理約 4 到 5 小時就會撞上限，每個代理死在哪一步不一定；研究檔每寫完一節就存檔、覆核只改一個檔的做法讓中斷幾乎不損失工作。覆核代理一開始只把收緊寫成〈覆核再改〉註記、沒改 title／hook／finding 三行，brief 已改成要直接改那三行，先前六題由一個整理代理補做。
- 2026-10-11 第二批第一輪實測（claude-fable-curio-topics）：研究代理一題約 27 萬到 38 萬 token、34 到 40 分鐘、開 40 到 90 個網址；M09、L09、P10、U11 都是 ADOPT_WITH_CHANGES，每題都改掉原卡一到四處講滿的地方（U11 的「飛碟是記者寫出來的」不成立：1947 年當天報紙與他本人的報告都寫 saucer-like，「我說的是飛法」是 1950 年才說的；P10 的「預言落空反而更堅信」是書的詮釋，書自己的尾聲寫團體一個月內散掉，2025 年還有用解封檔案寫的反駁論文；M09 的「三十幾個齒輪」應為現存 30 個、「幾十年後 X 光才看出齒輪」講反了；L09 的 1935 年原報導沒開到，細節全靠轉述）。這個網路的限制：web.archive.org 的存檔頁對代理回「Blocked by egress policy」（只能用 availability API 確認有存檔），Commons API 回 429（改讀檔案頁 HTML），nytimes.com、Britannica、JSTOR、DTIC 回 403——只靠存檔的來源要在覆核時判 UNOPENED，下一個 session 若在別的網路可以補開。
- 2026-10-11（claude-fable-curio-topics）：站主說「增加題目並查核」。新卡的選題原則照 README §題材與 §內容守則：有「檔案感」（一個年份、一份文件、一個名字）、鉤子先丟反常識的斷言、一手來源找得到、避開醫療與選舉陰謀論、靈異儀式、在世人物的畫像與血腥。新題：H09 艾爾哈特失蹤、H10 富蘭克林探險隊、H11 伏尼契手稿；M09 安提基特拉機械、M10 馬爾法燈光、M11 1518 年舞蹈瘟疫；P09 聖經密碼與白鯨記、P10 1954 年飛碟預言與《當預言失敗》、P11 索斯科特的箱子；U09 LGM-1 脈衝星、U10 1897 年神祕飛船、U11 「飛碟」一詞的由來；L09 紐約下水道鱷魚、L10 萬聖節糖果傳說、L11 韓國電扇死。研究與覆核代理的指示沿用第一批的寫法（預設否決、引句要在頁面上找得到、打不開的頁不算數、圖片逐張看授權頁），另外兩件這個環境量到的事：Commons 的 API 對這個網路一律回 429，代理改讀檔案頁 HTML；Britannica、NYT 對機器回 403，走 Wayback。
- 2026-10-10 H02–H07 覆核完成（claude-opus-curio-topics）：六個代理各重開一題的全部來源，實測每個 25 萬到 39 萬 token、17 到 28 分鐘（合計約 179 萬 token）。六題都維持「改過後可採用」，沒有一題的主幹被推翻，但每題都有一到四列被否決或改判；最要緊的三件：H03「八千萬棵樹」是 1933 年的粗估（面積高估約四倍）、H07「鐵是伏爾泰 1751 年才寫的」不成立（1738 年的信已有）、H03 最有名的倒樹照片不是可靠的公有領域檔。逐題的改動與要站主決定的事在 `docs/videos/history-curiosity/topic-checks/README.md` 的表與各檔的〈獨立覆核〉。
- 題目卡怎麼寫回題庫：scratch 的小腳本從各檔〈題目卡（查核後）〉讀 `title`／`hook`／`finding` 與處置，沒有〈獨立覆核〉一節就拒絕；`photo_candidates` 改成指向該檔的圖片清單（原卡的候選圖有幾張覆核後不能用）。
- 覆核代理不准跑 git、只准改自己那一個檔；`topics.json` 與 README 由主線改。六個代理同時在一個 worktree 裡各改各的檔，沒有互相蓋到。
- 還沒做：H08 與 M、P、U、L 四軸的 31 題。照這次的量，一題研究加覆核約 50 萬到 70 萬 token；四軸全做約 1,500 萬到 2,000 萬，要分批、看用量，先做下一季要拍的那一軸。
- 2026-10-10：覆核代理的提示沿用第一次整批查核的寫法（預設否決、引句要在頁面上找得到、打不開的頁不算數、圖片逐張看授權頁）。一個做網路查核的代理約 15–30 萬 token，見票 `2026-10-10-history-curiosity-pilot`（已結案）的教訓：不要一次放幾十個。
