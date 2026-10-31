# C06 R3 EN / JA 文字翻譯自查

範圍：已通過中文文字來源與敘事審核之 C06 R3 的英語、日語工作表。這是譯者自查，不是獨立 `TEXT_PASS`，未執行 native merge、語言輪、TTS、計時字幕或配音。

中文稿綁定：`45057c33f3c6efa3510c5c27f1f9c03172ba7ebbea5a2914ac0b01e0693e0a13`。

| Locale | 工作表 | 句數 | 章數 | 標題字元 | SHA256 |
|---|---|---:|---:|---:|---|
| en | `media/story-everyday-play-doh-c06-remake-20261025/i18n/en.todo.json` | 163 | 6 | 63 | `78f93bacd82e2810f9359618b95d8a1a8b00753012cedcbaab616e848c6a930d` |
| ja | `media/story-everyday-play-doh-c06-remake-20261025/i18n/ja.todo.json` | 163 | 6 | 40 | `fe3a9ac7306826b7bef51fb052dd40f3972c1874b5967a1d5a2fb39996b18837` |

兩份皆填滿 163 句、6 章，以及 title、description、tags、thumbnail 的 text。僅修改 text 欄位；以遞迴移除 text 後的完整資料結構，逐份比對 `translation-source-sheets/{en,ja}.json`，完全相同。所有原始 URL 順序與字元逐字保持，兩份標題皆少於 100 字元；EN/JA thumbnail 副標分別 11/9 字元。未改來源 hash、id、scene、todo、glossary、boundaries、parts，未寫其他語言或 repo 檔案。

逐句自查包括：

- 2024 年為 Hasbro 說法時間，數字仍是「年出貨逾 5 億罐」，不是孩子人數、零售銷售或收入。
- 1933 年清潔訂單、1949 年接手、1950 年代衰退、1955 年用途提案、1956 年子公司／品牌回顧、1957 年顏色、1960 年工具與專利申請、1965 年核發、2026 年成人產品，沒有混併。
- Kay Zufall 與 Joseph 的關係保留中文「姻親」範圍；英語用 related by marriage，未收窄成 sister-in-law。日語用「姻戚」。英文 Cleo McVicker、Noah、Joseph 與 Kay Zufall，日語對應クレオ・マクヴィッカー、ノア、ジョセフ、ケイ・ズフォール，全篇保持一致。
- 專利的可塑與保形並存、慢乾與反覆改形、optional 黏結成分、作者對包覆／糊化的解釋、密閉保存「文本聲稱最長三年」、乾硬後不能練回等條件保留。未改成 1933 年配方或現代產品保證。
- 2026 年成人系列「公司稱首次」、噴霧保存結構數月為 Hasbro 說法，未獨立保證結果。未把現代套件工序倒寫早期歷史。
- 你／我視角、假設／想像動作、問句及來源歸因保留；日語適度省略可自然承接的第二人稱，沒有改成一段摘要。

待獨立校對／媒體階段處理：

- 英文縮圖副標為 `2024: >500M`，以保持短標；罐數單位與年出貨／公司歸因完整保留在片頭文字，獨立審閱可評估縮圖是否應再明寫單位。這不是對呈現效果的批准。
- 人名日語表記已一致；未作獨立發音查核，仍需後續字典／實聲聽檢。
- 沒有真實聲音或時間軸，因此未判斷 dub time-fit、12–14 分鐘、字幕切分、縮圖實際可讀性或媒體 QA。

無 provider、後台、付費、Git 或核准動作。
