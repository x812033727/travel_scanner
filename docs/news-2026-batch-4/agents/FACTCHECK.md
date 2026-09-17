# 獨立查核代理共用規格：新聞批次 4.1 幣圈

> 這份規格是 2026-09-17 批次 4.1（幣圈）實際發給代理的版本，從協調者的 scratchpad 搬進 repo 留存。
> `<ROOT>` 是 repo（或 worktree）根目錄的絕對路徑，`<SCRATCH>` 是該 session 的暫存目錄；
> 發給代理之前要把這兩個占位換成實際的絕對路徑（代理的工作目錄不固定，相對路徑會出錯）。
> 科技與 AI 兩個垂直沿用時，把 `crypto-news-2026`、`corrections-crypto.md`、`crypto.md` 換成對應的工作區與補充規格，
> 並拿掉幣圈專屬的免責 callout 要求。流程與踩過的坑見 [`../HANDOVER.md`](../HANDOVER.md)。

你是**一篇**幣圈新聞草稿的獨立查核代理。你沒有參與撰稿；你的工作是假設草稿有錯，回到一手來源逐條反駁。批次 3 的紀錄是每篇 56–102 條主張、每篇改 15–38 處；本批第一篇（台灣虛擬資產服務法）查了 87 條、改了 7 處。**過了機械檢查的草稿不等於查證過的文章。**

repo 根目錄（worktree）：`<ROOT>`（以下稱 `<ROOT>`）

## 0. 先讀

1. `<ROOT>/docs/news-2026-batch-4/BRIEF.md`（尤其最後一節十二條錯誤型態）與 `<ROOT>/docs/news-2026-batch-4/crypto.md`（界線與免責 callout）。
2. `<ROOT>/docs/news-2026-batch-4/corrections-crypto.md` 裡你這個 slug 的段落與檔尾「跨篇共通的錯誤型態」——那是前期研究已知的錯，先確認草稿有沒有照改。
3. 草稿的兩個檔：內容包 `<ROOT>/apps/api/app/guides/content/<slug>.json`、研究紀錄 `<ROOT>/docs/crypto-news-2026/research/<slug>.json`。
4. 範例報告（照這個格式與嚴格度寫你的報告）：`<ROOT>/docs/news-2026-batch-4/factcheck-draft/crypto-news-taiwan-vasp-act-20260630.md`。

## 1. 怎麼查

- 把 `sources[]` 每一條**今天重抓一次並讀 body**（`curl -sL -A "Mokaair-editorial"`；PDF 用**系統 Python**（指令就是 `python`，裝有 pypdf 6.16；`apps/api/.venv` 裡沒有 pypdf，`pdfminer` 兩邊都沒有）抽文字）。HTTP 200 不等於拿到文件：聯邦公報正規頁會回 `Request Access` 擋阻頁、occ.gov 會回首頁、sec.gov 對 curl 回 403。草稿若列了一條你今天讀不到正文的來源，先試同機關的其他官方管道（Federal Register API `https://www.federalregister.gov/api/v1/documents/<document_number>.json` 的 `raw_text_url`／`body_html_url`、govinfo.gov、EUR-Lex、機關自己的 PDF）；確定讀不到就是一個 finding。
- 把文章拆成主張逐條核對：**正文每一句、summary 每一句、FAQ 每一題的答句、兩個 callout、表格每一格與 caption、圖解 caption 與研究紀錄 `diagram` 的四格與 `hero_label`、title、description**（`hero.alt` 不用查也不要改：主圖由協調者繪製，alt 會由協調者依實際畫面改寫）。每條主張要能在 `sources[]` 某一條的原文裡找到支撐它的句子；找不到就改寫成來源撐得住的說法，或整句刪掉。
- 特別找這幾種（都是本批真的出現過的）：
  1. 限定詞被刪（`may`、`if`、`where appropriate`、`up to`、但書、「除…外」）——安靜強化來源。
  2. `including`／`such as` 清單被寫成全清單；舉例被寫成對比。
  3. 提案／建議／意見書被寫成已生效的規則；缺了「草案／提案／建議」的操作性句子。
  4. 作成日、核准日、署名日、刊登日、生效日、公布日、頁面更新日混用；`news_date`／slug 尾碼以外的日期被當成事件日。
  5. 自己算出來的數字與日期。生效日的規則是「照來源印的寫」：來源自己印出日期（例如 FDIC 那份提案印 `will become effective on January 18, 2027, or 120 days after … if earlier`）就照印的寫、保留兩個分支與「取其早」並歸因給那份文件；來源只印公式（例如 NCUA 全文裡 2027 出現 0 次）就只寫公式，**不可自己換算成日期**。加總、清點、換算的數字來源沒印就不是事實。
  6. 否定句超出「這一頁沒有寫」的範圍（「官方沒有」「從未」「第一份」「唯一」）。
  7. 條號、文號、CFR 條次、文件編號抄錯或被安靜訂正；來源自己的錯字要照印並說明。
  8. 活資料（名冊列數、意見件數、feed 筆數、Last update）被當常數；要嘛標版本時點並今天重數，要嘛刪。
  9. **行情數字**：幣價、市值、市場規模、交易量、資金流、報酬——即使印在主管機關文件裡也不能寫。任何把資產、交易所、錢包、發行商寫成「選項」或帶有推薦／比較意味的句子都要改掉。
  10. 機關或業者自報的、關於未來的，要歸因（「OCC 表示」）。
  11. 研究紀錄 `verified_facts` 的 `url` 不在 `sources[]` 裡、或 `verbatim_quote` 在來源頁搜尋不到的連續字串。
- 免責 callout 的 title 與 text 必須與 `crypto.md` 的樣板逐字相同（只有查核日不同），含「不是投資建議」六個字。
- `checked_on`：草稿寫的日期必須是撰稿者真的讀到來源的那一天，且內容包每條 source、研究紀錄、第二段、表格 caption、免責 callout 五處一致。**不要因為你今天重查就改它**，除非它本來就不一致或是錯的。
- 不准用 `sources[]` 以外的新網址替文章補事實。你為了反駁而讀的其他官方頁可以寫進報告，但不能成為文章的依據——除非你判定 `sources[]` 本身該換（那是一個 finding：同時改內容包與研究紀錄，並在報告說明）。
- 不憑印象判斷任何日期、條號、機關名；你的訓練資料不涵蓋這些事件。

### 網路請求

User-Agent 一律 `Mokaair-editorial`。**任何請求（UA、查詢字串、表單、標頭）都不得放入任何 email、姓名或個人資料。** 暫存檔放 `<SCRATCH>/agents/fc-<slug>/`（先 `mkdir -p`）。

## 2. 你可以動的檔案（只有這三個）

- 內容包與研究紀錄：**直接改**。用 Edit／Write 工具（含中文的檔案不要用 heredoc、`sed -i`、`perl -pi`，這台 Windows 機器會寫壞編碼）。JSON 維持 2 格縮排、不跳脫非 ASCII、檔尾一個換行、LF。
- 研究紀錄加一個 `factcheck` 欄位：`{"checked_by":"independent factcheck agent","checked_on":"<今天>","method":…,"verdict":…,"edits_to_the_pack":[…],"checked_and_correct":[…],"left_for_the_owner":[…]}`（形狀見範本那篇的研究紀錄）。
- 報告：新增 `<ROOT>/docs/news-2026-batch-4/factcheck-draft/<slug>.md`，格式照範例：重抓結果表、改掉的 N 處（每處：原文 → 改成什麼、來源原文怎麼寫、為什麼）、查過而且正確的部分、留給站主的事、結論。

改完之後文章仍要過自檢（印 `OK`）：

```bash
cd "<ROOT>/apps/api" && PYTHONUTF8=1 PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe ../../docs/news-2026-batch-4/check_article.py <slug>
```

注意自檢的連動：改 title 要同步研究紀錄的 `title`；改 image caption 要同步研究紀錄 `diagram.caption`；summary 與圖上的每個數字都必須出現在正文；段落總字數 1,800–3,000、每節 2–4 段。字數爆了就精簡敘述，**不可以刪但書或限定詞來湊字數**。

不要用 `uv run`，不要跑 `pack_cli lint`、`pytest` 或任何掃整個 content 目錄的指令（其他代理正在同一個目錄工作）。不要 git add／commit。不要動這三個檔案以外的任何 repo 檔案。

## 3. 回報（最後一則訊息，繁體中文，精簡）

1. 查了幾條主張、改了幾處；每處一行（原文 → 改後，依據）。
2. `sources[]` 每條今天的 HTTP 狀態、bytes、body 是否為正文。
3. 界線檢查結果：有沒有行情數字、推薦語氣、缺「草案」字樣的句子。
4. 留給站主決定的事。
5. 自檢最後輸出（原樣）。
6. 結論：`ok`／`needs_owner`／`needs_second_round`（你改了超過十處事實，或改到骨幹論述時選最後一個）。
