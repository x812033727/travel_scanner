# 查核指令（第二批，每篇一位查核者，查核者不是撰稿者）

你查核**一篇**已寫好的 AI 名詞文章：`docs/ai-terms-series/batch-03/staging/<slug>/pack.json`。
先讀 `docs/ai-terms-series/batch-03/brief.md` 與 `catalogue.json` 裡這個 slug 的指派，知道撰稿者被要求什麼。

## 你要做的

1. **逐條查事實。** 把正文、表格、callout、圖解 `<desc>` 與圖上文字拆成可查主張。凡是「某論文說」「某官方文件寫」「某年某事」
   「某機制如何運作」的句子，都要在 `sources` 的一手來源裡**今天親自打開**找到依據。論文的數字要對到論文自己的設定。
   User-Agent 一律 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，不帶任何人的 email 或個資。
2. **查來源本身。** 每筆 `sources` 的網址打得開（`curl -sSL`，看狀態碼）、標題對、確實支持文中用到它的主張、`checked_on` 合理。
   新聞、部落格、內容農場要換成一手來源或刪掉主張。
3. **查本系列的規矩**：沒有型號、價格、截止日期、排行榜分數；假設案例標了「示例」且沒有寫成觀察結果；推論＝inference、推理＝reasoning
   用得對；定義有分歧的詞兩邊都寫了並說明採用誰的；沒有「用了就不會⋯⋯」這類保證；台灣用語；圖上每個數字正文都有。
4. **直接修。** 在 `pack.json`（必要時 `diagram-1.svg`）裡改掉錯誤，保持字數在 1,800–3,000、結構不變（≥5 H2、恰好一個表、≥1 callout、
   指派的站內連結都在）。改完跑 dry-run：
   `cd apps/api && .venv/bin/python -m app.guides.pack_cli ingest --from ../../docs/ai-terms-series/batch-03/staging --slug <slug> --dry-run`
5. **寫 `verify-1.md`** 在同一目錄：每一處修改一行 `原句（節錄）→ 改成 ｜ 理由 ｜ 依據網址`；再列「查過、沒問題的主要主張」與
   「我懷疑但沒改的事」。最後一行寫 `facts_changed: N`（只算事實性修改，不算措辭）。

## 不准

- 不碰 `apps/`、別人的目錄、`catalogue.json`、任務票；不跑 git；不跑不帶 `--dry-run` 的 ingest。
- 不重寫整篇，不改 slug，不加指派以外的站內連結。

可以（2026-10-03 起）：改完 `pack.json` 後，同步更新同目錄的 `notes.md` 與 `research.json`（換掉的來源、`running_text_characters` 用 `app.guides.pack_ingest._body_length` 實算）。

最後回報一行：`facts_changed`、dry-run 結果、你懷疑但沒改的事。

## 第三批另加

- 不跑任何 git 指令，連唯讀的也不要。暫存檔放 `staging/<slug>/_tools/`，不要用共用 scratchpad。
- 一併檢查 `brief.md`「和第二批不同的地方」：topics 含 `ai-terms`、「本文／這篇」最多一次、正文沒有查證過程、台灣用語。
