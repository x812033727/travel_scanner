# 批次 4.8（每小時自動化漏掉的十則，五語）：對既有規格的差異

批次 4.8 沿用 4.1～4.3 的代理規格（`agents/`＝幣圈、`agents/tech/`＝科技、`agents/ai/`＝AI），
以及 [`DELTA-4-5.md`](DELTA-4-5.md)（五語批次）與 [`DELTA-4-7.md`](DELTA-4-7.md) 第 3、4、11–16 條。
以下兩處是「只做 zh-TW」的規則，**對本批不適用**：
- [`DELTA-4-6.md`](DELTA-4-6.md) 全文；
- DELTA-4-7 第 2 條，以及「不帶 `--full`」「研究紀錄沒有 `translations`」這些句子。

下面只寫不同或要再說一次的事。
**這份文件的規則優先於各垂直規格、DELTA-4-5、DELTA-4-6 與 DELTA-4-7 裡與它衝突的句子。**

1. **為什麼有這一批。**
   - 每小時的新聞自動化從 9 月 24 日起幾乎沒有產出。站主 2026-09-26 要求在重跑自動化擋下的舊候選之外，再手工寫一批十篇、五語，也當作練習。
   - 三位探索代理在 2026-09-26 掃到台北 21:03，候選清單原樣搬進 repo：
     [`../candidates-since-0922-ai.md`](../candidates-since-0922-ai.md)、
     [`../candidates-since-0922-tech.md`](../candidates-since-0922-tech.md)、
     [`../candidates-since-0922-crypto.md`](../candidates-since-0922-crypto.md)。
   - 十則都不在自動化的候選裡。它們的發布者（OpenAI、Anthropic、Qualcomm、WordPress.org、Synology、日本金融廳、台灣中央銀行、韓國金融委員會）都不在自動化的來源清單上，所以被漏掉。
   - **兩則是補寫件**：Synology（09-18）、中央銀行（09-17），事件日在窗口前。正文照事件日寫，不寫「最近」「本週」。

2. **五語。** 站主 2026-09-26 選了五語，這點與 4.6、4.7 不同、與 4.5 相同。
   - 內容包 `locales` 是 `zh-TW`、`en`、`ja`、`ko`、`zh-CN`。
   - 研究紀錄的 `translations`（四語的 `hero_label` 與 `diagram`）由翻譯代理補。
   - 流程是撰稿 → 兩輪查核 → 翻譯 → 逐語審稿。
     - 翻譯照 `agents/TRANSLATE.md`；AI、科技用 `agents/ai/`、`agents/tech/` 各自目錄下的版本。
     - 審稿照 `agents/REVIEW.md`；AI 另有 `agents/ai/REVIEW-GROUPS.md`。
   - 自檢：翻譯併入後跑 `check_article.py <slug> --full`，出圖後跑 `--full --assets`。
   - **五語文章只能連到五語都有的文章**，兩個結尾連結、正文裡的 `article` inline、`related` 都一樣。
     - 第 5 條的目標都已確認五語齊全（2026-09-26）。
     - 4.6、4.7 的文章只有 zh-TW，**不能連**，例如 `crypto-news-taiwan-deposit-token-pilot-20260922`、`tech-news-cisa-kev-linux-kernel-20260918`。
     - 要提到它們寫的事，就把能撐住那句話的官方頁放進本篇的 `sources[]`。

3. **研究紀錄由專責的 opus 研究代理寫**，同 DELTA-4-7 第 3 條。
   - 範例：`docs/ai-news-2026-09-late/research/ai-news-anthropic-pace-metrics-20260917.json`。範例含 `translations`，研究代理先不寫這一欄。
   - 候選清單裡每則的「容易寫錯的地方」「重疊檢查」是研究代理的**起手輸入**：要逐條重查，查實的寫進 `must_not_write`／`not_said`。
   - 研究紀錄一旦寫成，對撰稿與兩輪查核都有拘束力。
   - `corrections_applied` 寫 `[]`。

4. **`display_order` 與事件日照下表**，由 `check_article.py` 的 `RELATED`（`# 4.8` 區）順序決定，不要再動順序。
   4.4 的 29 個 slug 已經先佔在 `RELATED` 裡，所以本批從 AI **186**、科技 **337**、幣圈 **230** 起算。

   | 垂直 | slug | order | 事件日（台北） | 日期依據 |
   | --- | --- | --- | --- | --- |
   | AI | `ai-news-chatgpt-ads-taiwan-20260923` | 186 | 2026-09-23 | feed `pubDate` 02:00Z＝台北 10:00；頁首同日 |
   | AI | `ai-news-gpt-6-sol-luna-20260923` | 187 | 2026-09-23 | feed `pubDate` 9/22 18:00Z＝台北 9/23 02:00；頁面印 Sep 22 |
   | AI | `ai-news-claude-opus-55-20260922` | 188 | 2026-09-22 | 頁首只印日期、沒有時刻，照發布者日期 |
   | AI | `ai-news-google-vids-omni-free-20260924` | 189 | 2026-09-24 | JSON-LD `datePublished` 9/23 19:00Z＝台北 9/24 03:00；頁面印 Sep 23 |
   | 科技 | `tech-news-wordpress-712-20260922` | 337 | 2026-09-22 | 7.1.2 發布文 14:01Z＝台北 22:01 |
   | 科技 | `tech-news-synology-dsm-sa2613-20260918` | 338 | 2026-09-18 | 公告自印 Publish Time 16:17（UTC+8） |
   | 科技 | `tech-news-snapdragon-8-elite-gen6-20260922` | 339 | 2026-09-22 | 新聞稿電頭 MAUI、只有日期，照發布者日期 |
   | 幣圈 | `crypto-news-japan-onchain-finance-forum-20260925` | 230 | 2026-09-25 | 令和 8 年 9 月 25 日公表 |
   | 幣圈 | `crypto-news-taiwan-cbc-stablecoin-deposit-token-cbdc-20260917` | 231 | 2026-09-17 | 理監事會後記者會 |
   | 幣圈 | `crypto-news-korea-market-manipulation-referrals-20260923` | 232 | 2026-09-23 | 第 16 次定例會議議決、會後發布（KST，與台北同日） |

   協調者已裁定、不要重新推導的事：
   - **WordPress 的事件是 9/22 的 7.1.2 安全更新，不是 KEV。**
     - 探索代理提的 slug `tech-news-wordpress-712-kev-20260925` 不用。
     - CISA 把它列入「已遭利用」清單，寫成後續發展，正文寫「美國時間 9 月 25 日」。
       依據：CISA 公告日是美國時間 9 月 25 日；KEV 目錄的 `dateReleased` 是 18:58Z，台北已是 9/26 02:58。
     - 這是八天內第三篇碰到 KEV 的科技文。主軸是「WordPress 7.1.2 與怎麼確認自己的網站」，KEV 是什麼最多一句帶過。
   - **跨日的三篇（GPT-6、Google Vids、WordPress 的 KEV）正文兩個日期都寫**，例如「台北時間 9 月 23 日凌晨（美國時間 9 月 22 日）」。
     slug、`news_date`、第一段的台北日期三者一致。
   - **沒有時刻的兩篇（Claude Opus 5.5、Snapdragon）不換算。**
     - Snapdragon 照新聞稿印的「9 月 22 日」寫，可以帶電頭「茂宜島（Maui）」；新聞稿沒印時區，不寫「夏威夷時間」。
     - Opus 5.5 那篇的 9/24 Claude 部落格後續文可以進 `sources[]`，但它不是事件日。
   - **GPT-6 Sol／Luna 與 Claude Opus 5.5 分開寫。**
     - 兩篇不放同一張比較表。
     - 各自的評測比較一律寫成該公司的說法。
     - 內容不互相重講。互相提及時不連結，同批文章不當結尾連結。
   - **ChatGPT 廣告台灣是新事件，不是重寫舊文。**
     - 會因此過期的三頁另開維護票處理，本批不動：`ai-news-chatgpt-ads-20260505`、`ai-news-chatgpt-sponsored-agents-20260916`、`chatgpt-ads-status`。
     - 結尾連結照第 5 條指向 5 月那篇。
     - 正文可以寫「台灣先前不在名單上」，但只能根據本篇 `sources[]` 撐得住的內容。
   - **Snapdragon 只寫高通。**
     - 聯發科天璣 9600 Pro 沒有入選，不合併、不比較。
     - 高通的新聞稿沒寫代工廠，不可寫「台積電 2 奈米」。
   - **中央銀行那篇不可寫成與金管會 9/22 的存款代幣試辦是聯合行動。**
     那篇只有 zh-TW，不能連；要提金管會的試辦，就把金管會新聞稿放進本篇 `sources[]`。

5. **兩個結尾連結。**
   - 第一個是垂直索引，標題不改（同 DELTA-4-5 第 3 條）。
   - 第二個指向下表那篇**既有、五語都有**的已發布文章。
     - text 逐字照抄那個內容包現行的 zh-TW `title`。
     - 網址是 `https://mokaair.com/zh-TW/life/<目標 slug>`。
     - 兩篇資安文指向同一個目標是刻意的，`RELATED` 允許多對一。

   | 本批 slug | 第二個連結的目標 | text（逐字） |
   | --- | --- | --- |
   | `ai-news-chatgpt-ads-taiwan-20260923` | `ai-news-chatgpt-ads-20260505` | ChatGPT 廣告開放自助購買：OpenAI 5 月公告的工具、計費與鎖定機制 |
   | `ai-news-gpt-6-sol-luna-20260923` | `ai-news-gpt-6-astra-20260903` | GPT-6 Astra 發布：從回答問題到完成電腦工作 |
   | `ai-news-claude-opus-55-20260922` | `ai-news-claude-opus-5-20260724` | Claude Opus 5 推出：一般工作使用者值得注意哪些改變？ |
   | `ai-news-google-vids-omni-free-20260924` | `ai-news-gemini-omni-20260519` | Gemini Omni 在 I/O 亮相：用對話改影片，素材與連續性仍要自己把關 |
   | `tech-news-wordpress-712-20260922` | `tech-news-eu-cra-reporting-20260911` | 歐盟《網路韌性法》通報義務上路：9 月 11 日起，誰要多快通報 |
   | `tech-news-synology-dsm-sa2613-20260918` | `tech-news-eu-cra-reporting-20260911` | 歐盟《網路韌性法》通報義務上路：9 月 11 日起，誰要多快通報 |
   | `tech-news-snapdragon-8-elite-gen6-20260922` | `tech-news-nvidia-mediatek-20260831` | NVIDIA 投資聯發科技 35 億美元：合作深化公告與可轉債申報書各寫了什麼 |
   | `crypto-news-japan-onchain-finance-forum-20260925` | `crypto-news-jfsa-working-group-20260216` | 日本金融審議會報告：建議加密資產改依金融商品取引法，相關法案已成立、施行日未見 |
   | `crypto-news-taiwan-cbc-stablecoin-deposit-token-cbdc-20260917` | `crypto-news-taiwan-vasp-act-20260630` | 虛擬資產服務法三讀通過：七種服務商、穩定幣許可與仍未定的施行日 |
   | `crypto-news-korea-market-manipulation-referrals-20260923` | `crypto-news-fca-p2p-crypto-crackdown-20260917` | FCA 查緝倫敦非法點對點加密資產交易：行動日 9 月 10 日、公布日 9 月 17 日 |

6. **索引由協調者在同一個 PR 補，撰稿與翻譯代理都不要碰。**
   - 三個索引的標題不改。
   - 十個連結用 `update_index.py ai tech crypto` **五語一起**加進去，先跑 `--dry-run`。做法同 4.5：
     - 換掉 `EXPANDED_ON`；
     - 需要敘述時用 `INSERT` 表；
     - 不重跑 `build_*_index.py`；
     - `CITED` 維持空，除非五語同時加。

7. **活頁面，發布當天要重讀：**
   - OpenAI Help Center 的 Ads Manager 國家表（頁面自印更新時間）；
   - Anthropic 的方案用量說明；
   - Google Vids 的方案與地區；
   - 金融廳論壇 9/30 第一次會議後公開的議事概要；
   - 韓國金融委員會秋夕連假後可能補的英文版。

   研究紀錄的 `live_data_warnings` 要列出這些頁面，撰稿寫成「截至查核日」。

8. **網路請求**同 DELTA-4-7 第 11 條，再加本輪探索踩到的：
   - **Anthropic 的 Opus 5.5 公告在 `https://www.anthropic.com/claude-opus-5-5`**，不在 `/news/…`，也不在新聞頁的 `publishedOn` 清單。
     - 正文讀到的 `<article>` 沒有「哪些方案、哪些平台可用」那段。
     - 這段要從完整頁、system card 或 Claude 說明中心找。找不到就寫「官方未說明」，不可推論成「免費版不能用」。
   - **OpenAI〈Better prompt caching for GPT-6〉回 403。** 現場重試一次；還是讀不到就不進 `sources[]`，也不用 Wayback。
   - **Google Vids 文章裡的說明中心連結指向 Google 內部草稿網域** `support-content-draft.corp.google.com`。
     - 不能引用，也不能自己改寫成 `support.google.com/...`，那是猜網址。
     - 地區、語言、年齡、免費額度要找 `support.google.com` 上搜得到的真實頁面確認，查不到就寫「官方未說明」。
     - 頁面的「Read AI-generated summary」一律跳過。
   - **Qualcomm 新聞稿的 HTML 頁是空殼。**
     - 讀 `<link rel="alternate" type="text/markdown">` 指向的 `.md` 版；`sources[]` 放 `.md` 網址，研究紀錄寫明原因。
     - 新聞稿清單從 `sitemap.xml` 的 `<lastmod>` 找，`/news/rss` 是 404。
   - **KEV 的日期逐個 CVE 看，不看公告日。** CVE Program API 的 ADP `kev` 區塊有 `dateAdded`。
   - **日本金融廳、韓國金融委員會的英文新聞頁都落後**（分別停在 9/15、9/16），沒有這兩則。
     - 一律讀日文、韓文原文，引文照原文並附中文。
     - 日文版、韓文版譯文裡的機關名、會議名照原文，不從中文回譯。
   - **中央銀行 PDF 的頁碼與印刷頁碼差 1**：第七題在 PDF 第 44–47 頁、印刷頁 43–46。引用時寫清楚用的是哪一種。
   - `curl --compressed -w '%{size_download}'` 回報的是壓縮後的 bytes。研究紀錄的 `bytes` 記**落地檔案的大小**。

9. **查核報告進 repo**，同 4.7。
   - 每篇兩個檔：`factcheck-draft/<slug>-round1.md`、`<slug>-round2.md`。第二輪換人，逐句回一手來源。
   - 逐語審稿採用的修正與協調者對四個譯文的修訂，都由 `apply_corrections.py` 追加進既有的 `translation-corrections.json`（reason 以「協調者」開頭的是協調者的；工具只會追加，不會覆寫 4.5 的紀錄）。協調者對 zh-TW 原稿的修訂不經過那支工具，逐筆列在 HANDOVER §1h。

10. **每一篇都要有一張圖**，同 DELTA-4-7 第 15 條，畫在 `build_assets.py` 的 `# 4.8` 區。
    - 繪圖函式在兩輪查核之後，照定稿數字畫，五語各一份。
    - 圖上的數字不可以比正文強。
