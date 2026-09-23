# 批次 4.4（次要新聞：AI／科技 8 月 1 日–9 月 15 日、幣圈 2026 全年，只做 zh-TW）：對既有規格的差異

批次 4.4 沿用 4.1～4.3 的代理規格（`agents/`＝幣圈、`agents/tech/`＝科技、`agents/ai/`＝AI）與
[`DELTA-4-5.md`](DELTA-4-5.md)、[`DELTA-4-6.md`](DELTA-4-6.md)、[`DELTA-4-7.md`](DELTA-4-7.md) 的全部規則
（4.7 的第 2、3、4、6、8、9、10、11、12、13、14、15、16 條原樣適用）；只有下面幾件事不同或要再說一次。
**這份文件的規則優先於各垂直規格與三份舊 DELTA 裡與它衝突的句子。**

1. **窗口與性質。** AI 與科技是 **2026-08-01 00:00 至 2026-09-15 23:59 台北**的「次要新聞」——具體、對一般讀者有用、
   當時沒排進頭條的官方公告；幣圈是 **2026 年全年**、只寫法規／技術／產業運作（`crypto.md`），不碰行情。
   候選清單在 [`../candidates-secondary-2026-ai.md`](../candidates-secondary-2026-ai.md)、
   [`../candidates-secondary-2026-tech.md`](../candidates-secondary-2026-tech.md)、
   [`../candidates-secondary-2026-crypto.md`](../candidates-secondary-2026-crypto.md)（探索代理 2026-09-22T23:01–00:01Z 掃完，原樣搬進 repo）。
   站主 2026-09-23 圈選：**三個垂直的候選清單全收，共 29 篇**（AI 9、科技 10、幣圈 10）。
   去重表 `../published-news-2026-09-23.md`（114 篇）是探索時的依據；研究代理仍要自己 grep `content/` 再列一次 `overlaps_existing_article`。

2. **事件日多半不是「最近」。** 這批是回頭整理 1–2 個月前（幣圈最早到 4 月）的公告，正文第一段照事件日寫，
   **不可寫「最近」「本週」「日前」**；要交代「為什麼現在才整理」時只准一句：「這一則在發布當時沒有排進本站的頭條批次，這一篇補上」。
   官方頁若在事件日之後有更新（Windows 26H2 的 8/31 更新、Notebook 等），正文可用，但要寫明更新日並歸因；slug 與 `news_date` 一律事件日。

3. **`display_order` 照下表**，由 `check_article.py` 的 `RELATED`（`# 4.4` 區塊）順序決定，**不要再動順序**：
   AI 接 **177** 起（9 篇）、科技接 **327** 起（10 篇）、幣圈接 **220** 起（10 篇）。順序＝候選清單的推薦順序（站主全收，未另排序）。
   **歐盟 DSA 指定 ChatGPT／Reddit／Roblox 只寫一篇、寫在科技垂直**（`tech-news-eu-dsa-designation-20260831`，站主裁定）；
   AI 候選清單提的 `ai-news-eu-dsa-chatgpt-vlose-20260831` **不寫**。

   | 垂直 | slug | display_order | 事件日（台北） | 事件日裁決 |
   | --- | --- | --- | --- | --- |
   | AI | `ai-news-gemini-student-offer-20260820` | 177 | 2026-08-20 | `datePublished` 08-19T19:00Z → 台北 08-20 03:00（真實時刻，換算） |
   | AI | `ai-news-meta-muse-agent-20260909` | 178 | 2026-09-09 | 09-08T19:00:51Z → 台北 09-09（換算） |
   | AI | `ai-news-openai-cursor-wind-down-20260828` | 179 | 2026-08-28 | 08-28T06:00Z → 台北同日 |
   | AI | `ai-news-claude-text-watermark-20260815` | 180 | 2026-08-15 | RSC `publishedOn` 08-14T19:16Z → 台北 08-15（換算） |
   | AI | `ai-news-openai-zero-data-retention-20260820` | 181 | 2026-08-20 | 08-19T19:00Z → 台北 08-20（換算） |
   | AI | `ai-news-openai-hugging-face-incident-20260826` | 182 | 2026-08-26 | `00:00Z` 佔位，不換算 |
   | AI | `ai-news-chatgpt-business-premium-seats-20260810` | 183 | 2026-08-10 | `00:00Z` 佔位，不換算 |
   | AI | `ai-news-anthropic-alignment-security-20260831` | 184 | 2026-08-31 | 08-31T15:00Z → 台北同日 23:00 |
   | AI | `ai-news-gemini-notebook-usage-limits-20260829` | 185 | 2026-08-29 | 08-28T17:00Z → 台北 08-29（換算） |
   | 科技 | `tech-news-apple-child-safety-ios27-20260914` | 327 | 2026-09-14 | Apple 頁面日期，無時刻 |
   | 科技 | `tech-news-eu-dsa-designation-20260831` | 328 | 2026-08-31 | 執委會 `Publication 31 August 2026`，無時刻 |
   | 科技 | `tech-news-windows-11-26h2-20260827` | 329 | 2026-08-27 | 8/31 有更新，正文交代 |
   | 科技 | `tech-news-high-na-euv-12inch-photomask-20260908` | 330 | 2026-09-08 | 三份官方稿同日 |
   | 科技 | `tech-news-apple-rosetta-end-20260901` | 331 | 2026-09-01 | 9/1 與 9/9 兩則說法不同，並陳 |
   | 科技 | `tech-news-tsmc-sony-image-sensor-jv-20260811` | 332 | 2026-08-11 | TSMC 與 Sony 同日 |
   | 科技 | `tech-news-edge-manifest-v2-sunset-20260807` | 333 | 2026-08-07 | 文件頁 9/15 為更新日 |
   | 科技 | `tech-news-windows-age-api-20260908` | 334 | 2026-09-08 | 兩篇姊妹文同日 |
   | 科技 | `tech-news-chromium-v8-kev-20260909` | 335 | 2026-09-09 | 兩個 CVE 分別 9/4、9/9 列入；slug 取後者，正文兩個日期都寫 |
   | 科技 | `tech-news-sign-in-with-apple-domain-20260824` | 336 | 2026-08-24 | Apple Developer 頁面日期 |
   | 幣圈 | `crypto-news-treasury-genius-issuance-20260818` | 220 | 2026-08-18 | 聯邦公報刊登日 |
   | 幣圈 | `crypto-news-taiwan-travel-rule-20260804` | 221 | 2026-08-04 | 金管會新聞稿日；公報 08-13 是預告刊登，正文交代 |
   | 幣圈 | `crypto-news-korea-tokenized-securities-20260904` | 222 | 2026-09-04 | FSC 新聞稿日 |
   | 幣圈 | `crypto-news-japan-crypto-fraud-measures-20260806` | 223 | 2026-08-06 | 金融庁公告日 |
   | 幣圈 | `crypto-news-taiwan-antifraud-rules-20260720` | 224 | 2026-07-20 | 公報發布日；05-28 是預告 |
   | 幣圈 | `crypto-news-sec-transfer-agent-dlt-20260904` | 225 | 2026-09-04 | SEC 提案發布日（HTML 可能 403，走聯邦公報／PDF） |
   | 幣圈 | `crypto-news-paxos-clearing-agency-20260529` | 226 | 2026-05-29 | Release 34-105562 日期 |
   | 幣圈 | `crypto-news-cftc-perpetual-contracts-20260603` | 227 | 2026-06-03 | 聯邦公報刊登日；05-29 是採納日，正文交代 |
   | 幣圈 | `crypto-news-stablecoin-cip-20260622` | 228 | 2026-06-22 | 五機關聯合提案刊登日 |
   | 幣圈 | `crypto-news-treasury-state-regime-20260403` | 229 | 2026-04-03 | 聯邦公報刊登日 |

4. **第二個結尾連結**照 `check_article.py` 的 `RELATED` 對照（協調者已填）；text 逐字抄目標內容包現行的 zh-TW `title`。
   目標全部是既有已發布文章，沒有同批互指。研究紀錄的 `second_link` 欄位要抄同一個目標並附該標題（研究代理核對目標存在）。

5. **同一事件兩篇的分工（協調者裁決，不再翻案）**：
   - `ai-news-openai-hugging-face-incident-20260826`（OpenAI 自家事後報告）與既有 `ai-news-nvidia-hugging-face-20260903`（NVIDIA 收購、Hugging Face 的說明）
     是不同發布者的不同文件；本篇只寫 OpenAI 報告的內容，收購案以一句連到既有篇。
   - `ai-news-anthropic-alignment-security-20260831` 與上面那篇各自成篇（兩篇都提到 METR 覆核，各寫各的，互相用 `article` inline 連）。
   - 三則「改維護票」不做：ChatGPT Ads 歐洲擴張與 8/11 更新（掛 `ai-news-chatgpt-ads-20260505`）、數發部 MyData 三則（掛 `tech-news-moda-mydata-student-loan-20260917`）、
     總統令公布虛擬資產服務法與 FDIC／OCC 的 PPSI 版本（掛 `crypto-news-taiwan-vasp-act-20260630`、`crypto-news-stablecoin-aml-20260410`）。

6. **網路規則**同 DELTA-4-7 第 11 條，再加本輪探索踩到的：MAS `/news` 是 853,817 bytes 的維護頁（大 body 不是命中）；
   FATF 兩條路徑都 403（6/19 那則沒有一手來源，本批不寫）；HK SFC、BIS、OCC 新聞索引 404；韓國 FSC 站內搜尋回 0 是無效的零（改翻分頁列表）；
   `digital-strategy.ec.europa.eu` 的 `news-redirect/rss.xml` 回 500（改走 `/en/news`）；Samsung newsroom 連線重設（三星說法只能引 ASML 聯合稿）；
   中華電信列表翻頁是帶 `__RequestVerificationToken` 的 POST，不猜端點；`blog.google` 的 sitemap `lastmod` 是 16:00Z 檔期值，不當事件時刻；
   Apple 官方有繁中版的頁（兒少安全）可引繁中原文，但英文版仍是主來源。

7. **研究紀錄**（4.7 第 3 條）放各垂直工作區的 `research/`；AI 的工作區仍是 `docs/ai-news-2026-09-late/`（display_order 177–185 的 manifest 與 sheet 由該工作區出）。
   科技 `docs/tech-news-2026/research/`、幣圈 `docs/crypto-news-2026/research/`。

8. **索引**同 4.7 第 8 條（協調者同 PR 用 `update_index.py --locale=zh-TW`），但 **AI 索引的連結依事件日插進月份群**（4.3 做法），不是接在最後；
   科技與幣圈依既有群組。`CITED` 維持全空。

9. **額度與波次**：研究、撰稿、查核各以 ≤6 位代理一波；5 小時窗超過 70% 或週額度超過 90% 就停到重置，未完成的篇留在票裡註明狀態，不硬趕。
