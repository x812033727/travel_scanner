---
id: 2026-11-01-curio-topic-pool
title: Curio topic pool: dedup, sources, merge thin topics, themes
status: in-progress
priority: P2
area: docs
owner: claude-opus-curio-pool
claimed_at: 2026-11-01T14:56:04Z
created_at: 2026-11-01T14:56:03Z
completed_at:
branch: claude/curio-topic-pool
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - tools/video/curio/pool
  - docs/videos/history-curiosity/topics.json
  - docs/videos/history-curiosity/topics-fg.json
  - docs/videos/history-curiosity/README.md
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
---

# Curio topic pool: dedup, sources, merge thin topics, themes

## Why

站主 2026-11-01：照原來如此事務所的素材池（PR x812033727/travel_scanner#1971）幫奇聞檔案局也建一個自己的池，用來增加題目。要求一樣：
- 做好去重與來源整理；
- 太薄或無聊的題合併或淘汰；
- 影片不要為了片長硬湊。

片長站主定為「≥8 分鐘都可以」（不必硬撐 13 分鐘）。

題庫原本散在幾個地方：
- `topics.json`（224 題）與 `topics-fg.json`（61 題）；
- 已製作的 `curio-*` 目錄；
- S37–S63 只在 `origin/codex/curio-*` 分支上；
- W 軸 19 支只寫在 migration 文件裡。

這些地方都沒有工具讀，來源只在各題的 topic-check 表格裡；`topics.json` 也跟實際成片脫節。

## Definition of done

- [x] `docs/videos/history-curiosity/pool/` 能 build 出：
  - 去重後的核心題；
  - 每個原 ID 的合併、淘汰、轉出或 Shorts 理由；
  - 來源反查；
  - 8–13 分鐘的題案；
  - 可搜尋的頁面。
- [x] 已製作或製作中的題鎖定：只當去重對象，不能被併掉或淘汰。
- [x] 第一批約 40 題新題，每題至少兩個可讀來源，經非作者覆核。
- [x] `node --test tools/video/curio/pool/pool.test.mjs` 與 `cli.mjs check` 通過。
- [x] 142 題候補的篩選研究與覆核、處置寫回題庫、片長規則同步（站主要求併在 #1986）。

## Steps

- [x] 工具：照 PR 1971 的 core/history/render/store/cli/semantic 改成 curio 版。
- [x] 抽出分支上的 S 軸集數、W 軸清單、原來如此池的核心題（跨系列查重）。
- [x] 第一輪編輯處置（作者）。
- [x] 非作者覆核編輯處置。
- [x] 第一批新題研究（6 個研究代理）與非作者覆核。
- [x] 題案、selection、build、頁面實看、PR（x812033727/travel_scanner#1986）。

## How to verify

```bash
node --test tools/video/curio/pool/pool.test.mjs
node tools/video/curio/pool/cli.mjs check
node tools/video/curio/pool/cli.mjs index && node tools/video/curio/pool/cli.mjs index   # 第二次 0 writes
```

## Notes

- 2026-11-01 站主：「不用另外開票，一起在 1986 就好」。原本要在合併後另開票的三件事都併進這張票：
  - 片長規則同步到 curio-episode skill 與系列 README；
  - 142 題候補的篩選研究與覆核；
  - 處置寫回 `topics.json`／`topics-fg.json`。

  scope 因此加上題庫兩檔、系列 README 與 skill。
  - `topics.json` 也在 `2026-10-18-curio-s-axis-pilot-s01-red` 的 scope 裡，但那張的認領是 2026-10-18，已超過 24 小時（stale），分支 `claude/curio-s01` 已不在遠端；
  - `2026-10-26-merge-curio-f-and-g-topics` 與 `2026-10-10-curio-topic-bank-checks` 沒人認領。

  寫回只加 `pool` 欄位、改正已製作題的 `status`，不合併兩個檔、不把篩選研究當成 `checked`（`checked` 仍是 topic-checks 的完整查核加獨立覆核）。
- lint 沒有寫死 13 分鐘：`tools/video/automation/explainer-series.mjs` 本來就照 `series.target_minutes` 寫稿、下限 8 分鐘。所以片長規則只改 skill 與 README 的文字，沒改程式。

- PR 1971 的 `sectionFor` 會把 `/topic-checks/` 當成多題共用檔，對 curio 一題一檔的格式會回傳空字串、默默丟掉所有網址。curio 版改成整檔讀。
- 詞面相似對 curio 的標題幾乎抓不到真重複：L04／M01 只有 0.30，跟雜訊同分。本機語意近鄰（PR 1971 釘版的 MiniLM）才找得到，例如 U30 與 S49 同一題、M02 與原來如此的 X2020 同一題。語意分數只是給編輯讀的候選，不會自動合併。
- 2026-11-01 結果：
  - 原始紀錄 392、核心題 376、入選 97（新題 55）；
  - 已製作 95、候補 142；
  - Shorts 20、淘汰 14、轉出 7；
  - 35 個題案。

  入選新題的數字是 61 題新題裡，扣掉降為待查的 3 題與轉 Shorts 的 3 題。
- 舊題處置的非作者覆核推翻了 22 條，最常見的錯是把同一類別當成同一個答案（例如紅衣小女孩與魔神仔）；之後的批次照 README 的合併判準先自查。
- 研究代理每題約 2–3 萬 token、6 個並行約 30 分鐘；覆核代理每人約 30 題、約 25–30 萬 token。這個環境擋 web.archive.org，FBI、NSA、JSTOR、ADS 也常回 403 或 405。
- 2026-11-01 第二輪（舊卡篩選研究）結果：
  - 範圍：12 個研究代理、142 題（139 張舊題目卡加 3 題待查新題）；五位非作者覆核，照收 68、改過後收 51、待查 10、否決 5。
  - 素材池現在入選 204、Shorts 33、淘汰或轉出 26、候補 15、暫緩 3。
  - 共 38 個題案，其中 32 組的題都已入選。
  - 寫回題庫：285 題加 `pool` 欄位、43 題改 scripted。
- 教訓：覆核者的修改欄位要明寫「給改好的完整文字，不要寫修改指示」。這次約四成寫成「把『X』改成『Y』」，整合時照字面貼進去，事後要逐條重套；下一輪的覆核說明要先寫清楚。
- 隱私事件：研究代理 L9 曾把站主 email 放進一次 fr.wikisource API 請求的 User-Agent（對方回 429）。之後所有代理的指示都加了禁止在請求中放個人資料。
- 站主 2026-11-01 決定：F15 梅杜莎轉 Shorts（只講珊瑚或笛聲），U31 薇拉事件選入長片（不點名國家）。素材池 revision 2026-11-01-curio-pool-205：入選 205、Shorts 34、暫緩 1（P18）。
- 2026-11-02 第三輪（站主：「幫我把 P18 重跑跟 15 題候補補來源」）：
  - 工具加 `rechecks`：後一批替已篩選的待查題附加來源，不覆蓋；欄位以修改指示開頭的退回。
  - 4 個研究代理換管道（HathiTrust、Internet Archive `/stream/`、loc.gov `?fo=json`、Delpher 等），2 位非作者覆核：照收 2、改過後收 9、待查 4；P22、L01、L27 研究代理自判補不到。
  - 升為入選 11 題（P18、G01、G02、G19、F12、F26、F33、G23、M20、M34、N106）；T10「屋主前一年出版鬼故事書」改正為同一年（1936）。
  - 研究代理會引用前一輪的來源編號，`intake` 只認本批來源：整合腳本把重查題的舊編號拿掉（本來就掛在題上），第一次篩選的舊卡複製前一輪的讀取並標「沿用、未重開」。
- 2026-11-02 第四批新題（站主：「繼續擴充池」）：6 個研究代理、3 位非作者覆核，53 題進批次（照收 10、改過後收 38、待查 5），入選 46。可成片清單頁也改成 build 產生（`PRODUCIBLE.html`）。
- 站主 2026-11-02 決定：M34 跟 N386 排成一組（T45，N386 待查所以暫不算可成片）；N350 源義經先不收（暫緩）；其他照排（T46 史書名場面、T47 華盛頓、T48 名人的一招與一句；N409 轉 Shorts）。
- 素材池 revision 2026-11-02-curio-pool-262：原始紀錄 445、入選 262、候補 10、暫緩 1、Shorts 35、題案 42（40 組可成片）、單集 163。
- 覆核說明明寫「只給改好的完整文字」之後，五位覆核者交回的欄位沒有一個被退回。loc.gov 在第四批覆核時連續回機器驗證，兩題因此降為待查；沒有繞過。
- 2026-11-02 第五批（站主：「繼續擴充池」「八語言國家的都可以提高」「東南亞的題另外開一組補」）：
  - 7 個研究代理（含東南亞補充組）、約 72 個點子；4 位非作者覆核：照收 6、改過後收 49、待查 5、否決 1。60 題進批次，入選 53、候補 5、Shorts 2。
  - 弱軸補上：G 21→29、P 24→30、S 23→34。入選地區：日本 10、韓國 3、印尼 7、越南 3、泰國 2、西語與葡語世界 10、中國 5、英語圈與歐洲其他 13。
  - 東南亞第一輪多半卡在來源，第二組靠 Delpher 的殖民時期報紙（jsru.kb.nl SRU＋resolver.kb.nl OCR）與 Vajirayana 才補到；印尼期刊庫 garuda.kemdikbud.go.id 不在環境允許的網域。
  - 新題案 T49–T57；N191 燒餅歌因為有了同核心的 N549，從 Shorts 移回長片（T56）。
  - 素材池 revision 2026-11-02-curio-pool-316：原始紀錄 505、入選 316、候補 15、Shorts 36、題案 51（49 組可成片）、單集 199。
  - 一位覆核者曾把下載檔誤存到 repo 工作目錄，自己搬走了；我確認 `git status` 乾淨。之後的說明檔明寫「下載檔只存在自己的 scratchpad」。
- 還沒做：
  - 15 題候補的來源（N386、N387 在 loc.gov；U36 要塔斯社原電訊；N447 在韓國論文庫；其餘寫在各題 notes）；
  - 題案的實際試讀。
