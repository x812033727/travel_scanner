# 批次 4.10（Claude Sonnet 5.5，一篇，五語）：對既有規格的差異

批次 4.10 照 [`DELTA-4-9.md`](DELTA-4-9.md) 的做法走：沿用它引用的所有規則，路徑、代理分工、查核報告的格式也都一樣。
下面只寫不同的地方。**這份文件的規則優先於 DELTA-4-9 與它引用的各份規格裡與它衝突的句子。**

1. **為什麼有這一批。**
   - Anthropic 在 2026-09-28 發表 Claude Sonnet 5.5，公告頁是 `https://www.anthropic.com/claude-sonnet-5-5`。
   - 每小時的自動化沒看到這則：Anthropic 來源原本只收 `/news/` 底下的連結，模型發表頁卻放在網站根目錄。這個缺口在同一個 PR 修了。
   - 站主 2026-09-30 要求手寫五語。

   | slug | order | 事件日（台北） | 日期依據 |
   | --- | --- | --- | --- |
   | `ai-news-claude-sonnet-55-20260928` | 191 | 2026-09-28 | 公告頁只印日期（Sep 28, 2026），沒有時刻。照 Opus 5.5 的判例（DELTA-4-8 第 4 條）照印、不換算；研究代理若在一手頁找到時刻，照 DELTA-4-5 第 6 條換算台北時間並回報 |

   `display_order` 由 `check_article.py` 的 `RELATED`（`# 4.10` 區）決定。

2. **來源只用 Anthropic 自己的頁面。**
   - 可用的頁面：
     - 公告頁；
     - Claude 開發者文件的模型總覽、定價與版本說明（`platform.claude.com/docs/...`，2026-09-30 協調者實測讀得到；版本說明 9/28 那一則寫了 Sonnet 5.5 上 API 與三家雲端）；
     - system card（從公告頁或 Anthropic 網站上的連結取得，不猜網址）；
     - Claude 說明中心。
   - 媒體與整合站只能當線索。
   - 同一天有 GPT-6.1 Sol 那篇。兩篇**不放同一張比較表、不互相比較評測**，照 DELTA-4-8 第 4 條「GPT-6 與 Opus 5.5 分開寫」的判例。

3. **和既有文章分工。**
   - `ai-news-claude-sonnet-5-20260630` 寫的是 Sonnet 5。本篇寫 5.5 這一版：
     - 和 Sonnet 5 的關係（新模型、API 名稱、舊版怎麼處理）；
     - 價格與可用範圍（API、Claude 應用的哪些方案、三家雲端）；
     - Anthropic 公布的評測，一律寫成「Anthropic 公布」，並寫明不代表讀者自己的任務；
     - system card 的安全分級（照原文、歸因）。
   - `ai-news-claude-opus-55-20260922` 寫的是 Opus 5.5。可以一句話提到同系列，但不重講它的內容。
   - 價格只寫 Anthropic 印出來的牌價。倍數、百分比來源沒印就不寫；要寫就明寫「編輯換算」，而且不進標題、摘要和圖。
   - 不做「該不該換模型」的建議。
   - 方案可用性照官方頁逐字寫。讀不到就寫「官方未說明」，**不可**推論成某方案不能用。

4. **兩個結尾連結。**
   - 第一個：AI 索引，同 4.9。
   - 第二個：`ai-news-claude-sonnet-5-20260630`，text 逐字為 `Claude Sonnet 5：能力與成本之間，怎麼找日常工作的平衡？`。
   - `related` 放 `ai-news-claude-sonnet-5-20260630` 與 `ai-news-claude-opus-55-20260922`，兩篇都五語齊全。

5. **索引**：`update_index.py ai`。連結放在 9 月那組、Google Vids（9/24）之後，也就是 GPT-6.1 Sol（9/29）之前，照事件日排。
   - 索引的日期句在 4.9 已經是「事件到 2026-09-29、最後增補 2026-09-30」，本篇的事件日比 9/29 早，所以日期句不動。

6. **查核報告**：`factcheck-draft/ai-news-claude-sonnet-55-20260928-round1.md`、`-round2.md`。兩輪由不同的 opus 代理做。

7. **工作區**：`/root/news49/s55/`（代理暫存放 `/root/news49/s55/agents/<角色>/`）。
