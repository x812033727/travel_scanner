# 批次 4.9（GPT-6.1 Sol，一篇，五語）：對既有規格的差異

批次 4.9 沿用 4.1～4.3 的 AI 代理規格（`agents/ai/`）、[`DELTA-4-5.md`](DELTA-4-5.md)（五語批次），
以及 [`DELTA-4-7.md`](DELTA-4-7.md) 第 3、4、11–15 條與 [`DELTA-4-8.md`](DELTA-4-8.md) 第 2、3、7–10 條。
以下是「只做 zh-TW」的規則，**對本批不適用**：
- [`DELTA-4-6.md`](DELTA-4-6.md) 全文；
- DELTA-4-7 第 2 條，以及「不帶 `--full`」「研究紀錄沒有 `translations`」這些句子。

下面只寫不同或要再說一次的事。
**這份文件的規則優先於各垂直規格、DELTA-4-5、DELTA-4-7 與 DELTA-4-8 裡與它衝突的句子。**

1. **為什麼有這一批。**
   - OpenAI 在 2026-09-29 10:00Z（台北 18:00）發了〈Introducing GPT-6.1 Sol〉。這一則就在每小時新聞自動化掃的 `openai.com/news/rss.xml` 裡。
   - 同一天其他中文媒體都報了；到 9/30 台北下午，正式站的 sitemap 仍然沒有這一則，但自動化同一天出的其他 9/29 新聞都有上線。
   - 站主 2026-09-30 要求照 4.8 的做法手寫五語。自動化那筆候選卡在哪一關，要在 `/admin/news` 查，不在本批範圍。
   - 事件日與 `display_order`：

     | slug | order | 事件日（台北） | 日期依據 |
     | --- | --- | --- | --- |
     | `ai-news-gpt-61-sol-20260929` | 190 | 2026-09-29 | feed `pubDate` 9/29 10:00Z＝台北 9/29 18:00 |

     `display_order` 由 `check_article.py` 的 `RELATED`（`# 4.9` 區）決定。

2. **本批的路徑（Linux 容器，不是 Windows）。** 規格裡的 Windows 路徑一律換成下列路徑：
   - ROOT＝`/home/user/travel_scanner`；
   - python＝`ROOT/apps/api/.venv/bin/python`；
   - 抽 PDF 用協調者給的 `pypdf` venv（系統 python 的 `pypdf` 壞掉）；
   - Chromium＝`/opt/pw-browsers/chromium`；
   - 工作區＝`/root/news49`：代理的暫存檔放 `/root/news49/agents/<角色>/`。

3. **來源只用 OpenAI 自己的頁面。**
   - `openai.com/index/introducing-gpt-6-1-sol` 與 `openai.com/index/devday-2026-recap` 對 curl 回 403（Cloudflare「Enable JavaScript and cookies」挑戰頁，約 9.8 KB）。這是**讀不到**，不是沒有。
     現場各重試一次；仍讀不到，就不進 `sources[]`，也不用 Wayback。
   - 協調者 2026-09-30 實測讀得到正文、而且有 GPT-6.1 Sol 的一手頁面：
     - `https://developers.openai.com/api/docs/models/gpt-6.1-sol`；
     - `https://developers.openai.com/api/docs/pricing`；
     - `https://developers.openai.com/changelog`；
     - 官方 RSS `https://openai.com/news/rss.xml`：`<item>` 的 `description` 有一句官方摘要，可以撐那一句。
   - System card 若在 `cdn.openai.com` 找得到 PDF 就讀；找不到就寫「官方未說明」，不要猜網址。
   - 下列頁面只能當線索，**不能**當來源，正文也不可以轉述它們獨有的數字或說法：
     - `aiposthub.com`、`maplefeather.com`、`myclaw.ai`、`hao.cnyes.com`，以及任何媒體與整合站；
     - 使用者實測心得；
     - 「45 頁 system card」「思維鏈遵循率 44.8% 對 16.1%」「循環模型架構」這類在一手頁讀不到的說法。

4. **和 9/23 那篇分工。**
   - `ai-news-gpt-6-sol-luna-20260923` 寫的是 GPT-6 Sol 與 Luna 首發；本篇寫 **GPT-6.1 Sol** 這個新版本。
   - 開頭一段就交代它和 GPT-6 Sol 的關係：是新模型還是改版、API 名稱、舊版怎麼處理。只寫官方頁有寫的。
   - 不重講 9/23 那篇的 Luna 與 ChatGPT 方案內容。
   - **價格比較**只放官方定價頁印出來的牌價：GPT-6.1 Sol、GPT-6 Sol、GPT-6 Astra 的輸入、快取輸入、輸出單價，每百萬 tokens、美元。
     - 「五分之一」「降 95%」這類倍數與百分比，官方頁有印才寫，並歸因；自己算的要明寫「編輯換算」，而且不進標題、摘要和圖。
   - 評測數字一律寫成「OpenAI 公布的評測」，並寫明不代表讀者自己的任務。
   - 不做「該不該換模型」的購買建議。
   - 在哪些 ChatGPT 方案、Codex、API 能用，照官方頁逐字寫。讀不到就寫「官方未說明」，**不可**推論成某方案不能用。

5. **兩個結尾連結。**
   - 第一個：AI 索引，標題不改：`2026 年 AI 新聞總整理：1 月至 9 月的重點與生活應用`。
   - 第二個：`ai-news-gpt-6-sol-luna-20260923`，text 逐字為 `GPT-6 Sol 與 Luna 推出：API 降價、Codex 可用，ChatGPT 對話裡還沒有`，網址 `https://mokaair.com/zh-TW/life/ai-news-gpt-6-sol-luna-20260923`。這篇五語齊全。
   - `related` 同樣放 `ai-news-gpt-6-sol-luna-20260923`。

6. **索引由協調者在同一個 PR 補**，用 `update_index.py ai`，五語一起加，先跑 `--dry-run`。撰稿與翻譯代理都不要碰索引。

7. **活頁面**：定價頁、模型頁、changelog 與 ChatGPT 方案頁，研究紀錄的 `live_data_warnings` 要列出來，正文寫「截至查核日」。發布當天由協調者重讀。

8. **查核報告**：`factcheck-draft/ai-news-gpt-61-sol-20260929-round1.md`、`-round2.md`。兩輪由不同的 opus 代理做，第二輪逐句回一手來源。
