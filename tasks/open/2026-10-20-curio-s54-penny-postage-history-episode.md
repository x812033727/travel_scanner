---
id: 2026-10-20-curio-s54-penny-postage-history-episode
title: Curio S54 penny postage history episode
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T19:00:53Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s54
---

# Curio S54 penny postage history episode

## Why

站主委託持續製作新的奇聞檔案局歷史影片。S54 用 1839–1840 英國一便士郵資改革，回答「費率先開始、郵票卻數月後才可用」；必須區分法律授權、實際費率、郵票開賣及准用日期。

## Definition of done

- [x] 不重複既有 `curio-s*` 集數與目前任務的 A／B 企劃，固定三份可重開史料、SHA-256 及具體行號。
- [x] 另一位工作者獨立重開三份全文，重算雜湊並判研究表 P01–P12 題材可行 PASS/HOLD；見 `source-feasibility-2.md`。
- [ ] 作者據通過的研究寫 8–15 分鐘逐句劇本、主張、分鏡、Shorts，經獨立逐句史料／書面畫面覆核及兩位新讀者盲評。
- [ ] 旁白、畫面、配樂與成片、濃縮開場、5 秒片頭、21 秒片尾及可點結尾連結經工具與站台關卡驗收；實際 YouTube 網址只用上架後取得的 ID。

## Steps

- [x] 查原始任務與 `main` 題目，讀系列 skill；選 A 案並明列 B 案的來源弱點。
- [x] 在本雲端取回 1839 年法案、1880 年希爾／姪子編刊回憶錄、1848 年美國倡議書固定版本；寫 [research.md](../../docs/videos/curio-s54/research.md) 與 [brief.md](../../docs/videos/curio-s54/brief.md)。
- [x] 獨立題材覆核 PASS；作者不可把自己蒐證當獨立 PASS。
- [x] 通過後寫 7 章完整劇本、逐句主張及書面分鏡，精確雜湊見 `author-freeze-1.md`。
- [ ] 由不同工作者逐句審核、新讀者雙盲，再做後續媒體及實測時長關卡。

## How to verify

`gh api repos/Anterotesis/statutes/git/blobs/433e7fa217b90a06f21b491788fb4b08b0ecd487` 可重開 1839 年法案印本 OCR，`git clone` 兩份 GITenberg 固定提交；`sha256sum` 對 [research.md](../../docs/videos/curio-s54/research.md) 三筆全文雜湊。`npm run check:tasks` 驗票格式，`git diff --check` 驗空白。題材可行覆核另需人工核對 P01–P12 原文行號。

## Notes

1839 年法案 *2 & 3 Vict. c.52* 序言寫一便士改革目標、內文授權財政部後續命令及三種預付載體，不能說立法當天已開賣 Penny Black。希爾 1880 年姪子編刊回憶錄含 1840 年日記摘錄；其敘述有當事人辯護角度，112,000 封是他於 1 月 11 日日記所記的**前一晚郵局寄件數**，所引段落未明言該局所在地，不能當全國總數。1848 年 Joshua Leavitt 的廉價郵資倡議書在 L4144 獨立分開列 1840-01-10 費率與 05-06 郵票使用。希爾記郵票 05-01 **開售**、05-06 **可用**；不能混作一天。原創可愛插圖只示意，不能重建可讀法案、實際郵票圖案或遺失的指示信。

搜尋時找到 1840 年 Vaughan 與 Pears 的「late Post Office agitation」小冊子，實際談**星期日郵局職員工作**，不是一便士郵資改革，故不列本集證據。另一份獨立當年法案已足以支持制度框架；如寫退款、實付總額、精確全國每日件數，需要新來源，不可從希爾日記外推。

2026-10-20：題材獨立覆核已 PASS，第一版 [完整劇本](../../docs/videos/curio-s54/script.md)、[逐句主張](../../docs/videos/curio-s54/claims.md) 與 [作者凍結](../../docs/videos/curio-s54/author-freeze-1.md) 已落地。仍**無新版逐句獨立 PASS、雙盲、網站核准或付費媒體**。不同工作者應以作者凍結的精確雜湊重新讀原文；不要把前一輪題材可行性 PASS 當全稿 PASS。

作者本地檢查：`npm run check:tasks` 驗證 2125 票、`npm run test:docs-videos` 236／236、`git diff --check` 通過；這些工具檢查不代替人工史料覆核。

2026-10-20 R9：R8 兩位隔離盲讀正式 OR 合併為 12/13 Yes，僅 `no_recap` FAIL，證據與 CLI 收據見 [合併報告](../../docs/videos/curio-s54/review/r8-isolated-merge.md)。作者依指摘刪除 1 月付款及收件人利益重述，以希爾當日日記的估計、翌日實數作連續場景；銷票段落縮短。五檔精確雜湊見 [R9 作者凍結](../../docs/videos/curio-s54/author-freeze-9.md)。正文以 325 漢字／分為 8.04 分鐘，`lint` 0 錯誤／0 警告；尚待**不同工作者**對 R9 重新做逐句史料／書面畫面與兩位新讀者盲評，R8 PASS 不可直接搬用。未製作付費媒體。

2026-10-20 R10：R9 [獨立來源／書面畫面](../../docs/videos/curio-s54/review/r9-source-independent.md) PASS，但[兩位新讀者正式合併](../../docs/videos/curio-s54/review/r9-isolated-merge.md) 為 11/13 Yes，`one_line` 和 `no_recap` FAIL。作者重排一月十日報紙記載與十一日日記／收款混亂的先後，刪去「回到」及片末重述，改以 1848 年夾郵票預付回信的原文實例收尾。R10 五檔雜湊見 [作者凍結](../../docs/videos/curio-s54/author-freeze-10.md)：正文以最快 325 漢字／分估 8.10 分鐘，`lint` 0 錯誤／0 警告，147 行主張／場景逐句對齊。**R10 仍待全新獨立來源與雙盲覆核**；沒有付費媒體。

2026-10-20 R11：R10 [雙盲正式合併](../../docs/videos/curio-s54/review/r10-isolated-merge.md) 已 13/13 PASS，[獨立來源／畫面報告](../../docs/videos/curio-s54/review/r10-source-independent.md) 只 HOLD `s54109` 的四月決策畫在五月收件所。作者只改該場提示詞為四月政府規劃室；旁白、研究、企劃、主張及重產稿的雜湊維持 R10 值，唯 `video.json` 新雜湊見 [R11 單景作者凍結](../../docs/videos/curio-s54/review/r11-author-visual-fix.md)。`lint` 0 錯誤／0 警告。下一步由不同工作者重核 R11 書面畫面及綁定，不把作者修改自認為獨立 PASS；尚未合成語音或付費繪圖。

2026-10-20 R14 WIP 前製交接：現稿 [獨立來源／書面畫面](../../docs/videos/curio-s54/review/r14-source-independent.md) PASS；兩位無先前對話背景讀者各 13/13，正式合併及同版 Jev 政策 PASS，精確雜湊與回條見 [R14 合併與政策摘要](../../docs/videos/curio-s54/review/r14-merge-policy/summary.md)。旁白 TTS／逐句音檢由另一個進行中的關卡處理，本次交接**未取得音訊 PASS**；分鏡、配樂、成片與網站站主審核亦未完成。此 WIP 只保留穩定前製證據，不包含正在寫入的音訊日誌或私有媒體。
