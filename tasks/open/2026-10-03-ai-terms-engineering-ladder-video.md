---
id: 2026-10-03-ai-terms-engineering-ladder-video
title: AI 名詞影片：從提示詞工程到圖形工程，五個名詞一集
status: in-progress
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-10-03T14:14:11Z
created_at: 2026-10-03T14:10:32Z
completed_at:
branch: claude/compassionate-sagan-kmhqx8
depends_on: []
scope:
  - docs/videos/ai-terms-prompt-to-graph-engineering
---

# AI 名詞影片：從提示詞工程到圖形工程，五個名詞一集

## Why

站主 2026-10-03 要一集介紹五個 AI 工程名詞：提示詞工程（單次對話的指令與輸出）、上下文工程（把對的資料、可見資訊與記憶傳給模型）、駕馭工程（Harness Engineering：任務邊界、工具權限、出錯攔截、監控；Agent = Model + Harness）、迴圈工程（觀察–執行–檢查–重試的自動循環）、圖形工程（把多個代理與迴圈排成有向圖／狀態機，追蹤進度、成本與輸出）。「AI 名詞十分鐘」系列是一集一個名詞，但這五個詞總是一起出現、互相定義，觀眾的問題是「名詞一直換，該追哪一個」，所以這集是一張地圖，單一名詞的深講仍留給各自那一集。

## Definition of done

- [x] `docs/videos/ai-terms-prompt-to-graph-engineering/` 有 `brief.md`（8 節、3 個大綱選項、站主觀點提案、示範）、`video.json`（lint 0 錯誤，估計 11.8–12.3 分）、`claims.md`、`shorts.json`（兩支精華）、`demo-log.md`（示範的逐字證據）。
- [x] `verify-1.md`：多代理獨立查核第一輪（329 條判定、29 個修正投票通過並套用、撰稿者再修 17 處）；事實改動 21 個 > 3，所以要第二輪。
- [x] `verify-2.md`：另一組代理重查改過的 40 個欄位、第一輪 CONFIRMED 的三分之一（81 條）與整支稿的一致性：131 條判定、7 處收緊、不需第三輪。
- [ ] 站主在 `/admin/videos` 挑大綱（頻道立場仍空白，Jev 不會自動挑）→ 後續照 `automated.md` 由工人或 session 接手 `tts` 以後的步驟。
- [ ] 名詞庫登記：`docs/videos/ai-terms/terms.json` 與系列 README 補上這一集（那個資料夾在票 `2026-09-29-ai-terms-video-pilot` 的 scope 裡，這張票不碰）。

## Steps

- [x] 讀 skill `youtube-video`、`automated.md`、系列規格 `docs/videos/ai-terms/README.md`、三集試片的 brief 與 video.json；四篇站上文章；一手來源（Anthropic ×2、LangChain ×2、Hashimoto、Osmani、Karpathy README、Simmons、arXiv 2608.21156、LangGraph 文件、Google Cloud 指南、Claude 文件、Thoughtworks）。
- [x] 企劃 `brief.md`：配方 D「先地圖」，三個選項，示範是我們自己的產線（lint 擋稿、三個常數、核准綁雜湊、status 的 14 步）。
- [x] 撰稿 `video.json`：91 景（63 shot、28 卡）、120 句、2,550 單位；每個英文名詞只在字卡，旁白全中文（不動共用的 `lexicon.json`）；`look: riso-forest`（工人輪替規則對這個 slug 的結果）。
- [x] lint 到零錯誤（稿子本身 3 次，另 2 次故意放英文詞的測試、1 次改字覆核；見 `demo-log.md`）。
- [x] `claims.md`（27 條）、`shorts.json`、`demo-log.md`。
- [x] 查核第一輪（多代理：七組查核＋反證＋兩面投票＋完整性）→ lint 第 10 次 0 錯誤。
- [x] 查核第二輪 → lint 第 11 次 0 錯誤；說明欄組合後 4,928／5,000 位元組。
- [ ] 提 PR、合併；之後 `review-push --gate outline`（頻道立場仍空白，大綱由站主在 /admin/videos 挑）。

## How to verify

```bash
node tools/video/cli.mjs lint --slug ai-terms-prompt-to-graph-engineering    # 0 errors（唯一的警告是估計 11.9 分、目標 9–11：系列規格說留著，成片約 10 分）
node tools/video/cli.mjs status --slug ai-terms-prompt-to-graph-engineering  # [x] brief、[x] script passes lint
npm run check:tasks
```

## Notes

- 2026-10-03（claude-fable-5-1）：名詞的中文——站上文章把 Harness Engineering 譯「代理執行環境工程」，站主需求與坊間用「駕馭工程」；旁白用駕馭工程，字卡標英文與站上譯名，`cta`／`outro` 說明。Graph Engineering 旁白用「圖形工程」。
- 各家樓層排法不同（Simmons 的階梯沒有駕馭層；Osmani 把迴圈放在馬具上一層；數位時代說沒有共識）：影片明說「各家排法不一樣，這集照今年夏天一份學術綜述（arXiv 2608.21156）排」。
- 不講的數字：LangChain 2026-02 的分數與模型名（跑分）、OpenAI 2026-02〈Harness engineering〉的團隊人數與程式行數（頁面對我們的 UA 回 403，Wayback 也連不上）、李宏毅課堂的 80 字實驗（只有新聞轉述，沒有一手來源）。
- `sources` 裡有三個 `raw.githubusercontent.com` 連結（repo 的常數與 HANDS-OFF.md）：`github.com` 對工具的 UA 回 403，`links` 品管會擋，所以用 raw；站主不喜歡可以拿掉，證據在 `demo-log.md`。
- 示範不呼叫模型（本機沒金鑰），示範的是這條產線本身；旁白沒有「我測過」任何產品。
- 任務板的 `claim` 第一次被拒：`docs/videos/lexicon.json` 在三張進行中的票的 scope 裡；照 `2026-09-28-video-1m-ai-agents` 的做法把 scope 縮成自己的資料夾，並讓旁白不含英文詞，所以不必動字典。
- 2026-10-03 查核第一輪後：組合後的說明欄 4,946／5,000 位元組，只剩 54 位元組；之後改說明欄本文或來源標題要先量（`composeDescription`），超了 lint 會擋。四個字「觀察、執行、檢查、重試」查核判定不在任何一手來源（只在數位時代與站主需求），稿子改成 Osmani／站上文章的「找工作、檢查結果、記進度、再跑一圈」；站主若堅持原用語，要在字卡標成站主的歸納。Simmons 的頁面其實有日期 2026-07-04。原定由工作流最後一位代理套用修正並寫報告，那一步被模型安全機制擋下（提示太長），改由撰稿者依投票結果用腳本套用；下次把紀錄寫檔再讓代理讀，不要塞進提示。
- 撰稿用的產生腳本在 session 的 scratchpad（`_tools/build_video.py`），不進 repo；`video.json` 是定稿，之後改稿直接改 JSON。
