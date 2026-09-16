# 查核紀錄：ai-news-deepseek-v41-flash-20260910

- 查核日：2026-09-15（獨立查核編輯，草稿視為未查證）
- 取得方式：curl，User-Agent `Mokaair-editorial`，不帶任何個人資料
- 讀過的一手頁面（皆為查核當天內容）：
  - https://api-docs.deepseek.com/news/news260910 （英文發布公告）
  - https://api-docs.deepseek.com/zh-cn/news/news260910 （簡中發布公告）
  - https://api-docs.deepseek.com/updates 、https://api-docs.deepseek.com/zh-cn/updates （更新日誌）
  - https://api-docs.deepseek.com/quick_start/pricing 、https://api-docs.deepseek.com/zh-cn/quick_start/pricing （模型與價格）
  - https://api-docs.deepseek.com/api/list-models （模型列表 API 說明）
  - https://api-docs.deepseek.com/sitemap.xml （新聞列表，最新一則仍是 news260910）
  - https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash （模型卡 README、LICENSE、inference/README.md、models API 的 `license:mit` 標籤）
  - https://github.com/deepseek-ai （近期更新的儲存庫，沒有另外的 V4.1 模型庫或 V4-Pro 說明）

## 結果總覽

共拆出 **91 條**可查主張（description 4、title 1、開頭兩段 10、五節正文 58、表格 13（含 caption）、callout 4、sources 4）。

| 分類 | 條數 |
|---|---|
| 正確 | 80 |
| 需要改寫（過度肯定、歸因不清、暗示推定） | 8 |
| 錯誤 | 1 |
| 查無出處 | 2 |

另為把正文壓回 3,000 字上限，刪了三句非事實性的收尾句、刪兩處贅字（見第 12–15 項）。修改後 `check_article.py`：`OK … zh-TW paragraphs 2995`。

逐項核對後確認正確、未改動的重點：9/10 發布日；「新架構系列中最小」「原生視覺理解」；模型名 deepseek-flash；V4-Flash 與 V4-Flash-Vision-Exp 退役、兩個舊名暫時導向 V4.1-Flash；552B MoE、Causal Encoder-Decoder、輸入 8B／輸出 16B（公告原文「8B active parameters for input, 16B for output」，模型卡「8B parameters per token during prefill and 16B during decode」，文章歸因給 DeepSeek）；KV 快取 HBM 1/4、SSD 1/8（相對上一代）；MIT 授權（模型卡「This repository and the model weights are licensed under the MIT License」，LICENSE 檔為 MIT）；1M 上下文、圖文輸入文字輸出；推論範例 MP=8；公告「9 月 14 日 04:00 UTC 起 deepseek-v4-pro 導向 V4.1-Flash、按 V4.1-Flash 價格計費、直到 V4.1-Pro 推出」（簡中寫北京時間 12:00，與台灣時間同）；英文與簡中公告頁查核時都仍保留這段；更新日誌與價格頁註 (2)「9 月 14 日之後繼續提供 V4 Pro、計費方式不變、有變動另行通知」；價格頁 deepseek-v4-pro 版本 DeepSeek-V4-Pro-0813；表格 4 列 12 格；WorkBuddy（含 CodeBuddy）與 OpenCode；4/24 條目 deepseek-chat／deepseek-reasoner 指向 v4-flash 非思考／思考模式、預告 7/24 停用；價格 0.3／1.2、1.32／3.96 美元（英文價格頁，美元）、離峰半價、尖峰 UTC 01:00–04:00 與 06:00–10:00（＝台灣 9–12 點、14–18 點）、新價 9/10 04:00 UTC 生效；Vision 一列 flash 支援、v4-pro 不支援。文中沒有任何評測分數。

## 逐條改動

1. **description**（錯誤＋需要改寫）
   - 原文：「原定 9 月 14 日併入的 V4-Pro，後來改為繼續提供。本文依官方頁面整理兩則公告的先後」
   - 改後：「發布公告寫 V4-Pro 自 9 月 14 日起改導向，更新日誌與價格頁則寫 9 月 14 日之後繼續提供。本文依官方頁面整理兩種說法的先後」
   - 理由：官方用語是 route（導向），不是「併入」；「繼續提供」不是另一則公告，而是更新日誌與價格頁上的文字。
   - 依據：https://api-docs.deepseek.com/news/news260910 、https://api-docs.deepseek.com/updates 、https://api-docs.deepseek.com/quick_start/pricing

2. **開頭第一段**（錯誤）
   - 原文：「公告原本也寫 V4-Pro 將在 9 月 14 日併入 V4.1-Flash，官方更新日誌與價格頁之後改為繼續提供。」
   - 改後：「公告也寫 V4-Pro 的請求將自 9 月 14 日起改導向 V4.1-Flash，但查核時官方更新日誌與價格頁寫的是 9 月 14 日之後繼續提供 V4-Pro。」
   - 理由：「原本」暗示公告已改，但查核當天英文與簡中公告頁都仍是導向的文字；「之後改為」推定了更新日誌被改寫的時序，沒有一手證據。
   - 依據：同上三頁，另 https://api-docs.deepseek.com/zh-cn/news/news260910

3. **第 1 節第 1 段**（需要改寫：只轉述廠商優勢，缺平衡）
   - 原文：「這些是廠商公布的成績，本站沒有重測。」
   - 改後：「這是廠商說法，模型卡對照表也有它落後其他廠商模型的項目，本站沒有重測。」
   - 理由：「超過包括 V4-Pro 在內的旗艦模型」容易被讀成全面領先；模型卡的前沿模型對照表中，GPQA Diamond、HLE、Terminal-Bench 3.0／4.0、ProgramBench、NL2Repo-Bench 等項目都有其他廠商模型較高。依規格不寫分數。
   - 依據：https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash

4. **第 1 節第 3 段**（需要改寫：把合作邀請寫成像硬體門檻）
   - 原文：「官方的推論範例以 8 路模型平行的設定執行，發布公告更寫著歡迎具備兩千張 GPU 與儲存叢集的大規模部署需求者聯絡。」
   - 改後：「模型卡連結的推論範例以 8 路模型平行的設定執行。發布公告另外邀請規劃以兩千張 GPU 加儲存叢集大規模部署的單位聯絡 DeepSeek。」
   - 理由：原文「更寫著」接在「一般電腦跑不動」之後，會讓讀者以為兩千張 GPU 是執行條件；公告原文是「Planning a large-scale deployment with 2,000 GPUs + a storage cluster? Let's talk.」。推論範例的出處也改成明確的「模型卡連結的」。
   - 依據：https://api-docs.deepseek.com/news/news260910 、https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/main/inference/README.md

5. **第 2 節標題**（需要改寫）
   - 原文：「舊模型名改導向、V4-Pro 去留：兩則公告的先後」
   - 改後：「舊模型名改導向、V4-Pro 去留：兩種說法的先後」
   - 理由：API 文件新聞列表只有一則 9/10 公告；「繼續提供」是更新日誌與價格頁的文字。
   - 依據：https://api-docs.deepseek.com/sitemap.xml 、https://api-docs.deepseek.com/updates

6. **第 2 節第 1 段開頭**（配合第 5 項）
   - 原文：「第一則是 9 月 10 日的發布公告。」 → 改後：「第一種說法來自 9 月 10 日的發布公告。」

7. **第 2 節第 2 段開頭**（查無出處）
   - 原文：「第二則是之後的改寫。查核當天，更新日誌 9 月 10 日那一條與價格頁的註解都已變成：」
   - 改後：「第二種說法在更新日誌與價格頁。查核當天，更新日誌 9 月 10 日那一條與價格頁的註解寫著：」
   - 理由：研究紀錄的存檔快照只涉及簡中價格頁，且存檔站不是一手來源；更新日誌那一條是否曾寫過導向文字，查無一手證據（Internet Archive 查核當天暫停服務，也無法複核）。只寫查核當天看得到的文字。
   - 依據：https://api-docs.deepseek.com/updates 、https://api-docs.deepseek.com/quick_start/pricing

8. **第 2 節第 2 段結尾**（查無出處＋補上時序的依據）
   - 原文：「官方沒有另發新聞稿，頁面也未標示修改日期。」
   - 改後：「從「決定繼續提供」的措辭看是導向計畫之後的決定，但頁面未標示日期，API 文件新聞列表也沒有另發公告。」
   - 理由：只查了 API 文件的新聞列表，沒查 X、微信公眾號等管道，「官方沒有另發新聞稿」說過頭；章節標題寫「先後」，所以補上先後的判斷依據（原文「In response to user demand, we have decided to continue…」），同時不推定日期。
   - 依據：https://api-docs.deepseek.com/sitemap.xml 、https://api-docs.deepseek.com/updates

9. **第 2 節第 3 段**（需要改寫：把官方說法寫成本站確認的現況）
   - 原文：「要特別留意的是，9 月 15 日查核時，…依更新日誌與價格頁的現況，deepseek-v4-pro 仍在服務，V4-Flash 的兩個舊名則照舊由 V4.1-Flash 服務」
   - 改後：「9 月 15 日查核時，…依更新日誌與價格頁的說明，deepseek-v4-pro 在 9 月 14 日之後繼續提供，V4-Flash 的兩個舊名則由 V4.1-Flash 服務」
   - 理由：本站沒有呼叫 API，「仍在服務」是推定；改成轉述頁面說明。開頭贅字刪除以控制字數。
   - 依據：https://api-docs.deepseek.com/updates 、https://api-docs.deepseek.com/quick_start/pricing

10. **第 4 節第 3 段**（需要改寫：暗示 DeepSeek 可指定固定版本、過度肯定可預期性）
    - 原文：「讓同樣的輸入有可預期的行為。DeepSeek 價格頁把模型名稱與實際版本分開列出，從這次經驗看，名稱相同不保證背後版本相同。」
    - 改後：「讓行為比較可預期。DeepSeek 價格頁把模型名稱與實際版本分開列出，但沒有說明能否用帶日期的版本名呼叫；8 月 13 日的更新日誌也寫，沿用 deepseek-v4-pro 這個名稱就會用到最新版本。」
    - 理由：價格頁與 Lists Models 範例只給 deepseek-flash、deepseek-v4-pro 兩個 id，沒有說明可呼叫 DeepSeek-V4-Pro-0813 這類版本名；原文讓人以為能在 DeepSeek 固定版本。「名稱相同版本會換」改用官方原文佐證（8/13：「simply set the model name to deepseek-v4-pro to use the latest version」）。
    - 依據：https://api-docs.deepseek.com/quick_start/pricing 、https://api-docs.deepseek.com/api/list-models 、https://api-docs.deepseek.com/updates

11. **callout**（需要改寫）
    - 原文：「deepseek-v4-pro 在 9 月 14 日之後繼續提供，計費方式不變。發布公告頁仍是原本的文字，現況請以更新日誌與價格頁為準。」
    - 改後：「更新日誌與價格頁寫 deepseek-v4-pro 在 9 月 14 日之後繼續提供，計費方式不變。發布公告頁仍保留 9 月 14 日起改導向的原文，官方未標示繼續提供這段說明的日期，串接前請再看這兩頁的最新內容。」
    - 理由：官方沒有說哪一頁為準；把繼續提供歸因到頁面，並提醒讀者自行再看最新內容。
    - 依據：同第 9 項，另 https://api-docs.deepseek.com/news/news260910

12. **第 3 節第 2 段**（字數）：刪除收尾句「模型名稱比較像一個入口，後面接的是哪個版本，要看服務商當下的公告。」（與第 10 項改寫後的內容重複）
13. **第 4 節第 3 段**（字數）：刪除「；一般使用者則留意工具的更新紀錄是否提到換模型」（第 3 節情境與圖解已涵蓋）
14. **第 5 節第 3 段**（字數）：刪除「對一般使用者，最實際的仍是弄清楚工具接的是誰、條款寫了什麼。」（與第 2 段重複）
15. **第 4 節第 1 段**（字數）：「API 價格這裡只簡單帶過」→「API 價格只簡單帶過」

## 研究紀錄同步

`docs/ai-news-2026-09-mid/research/ai-news-deepseek-v41-flash-20260910.json`：
- verified_facts 新增：模型卡 prefill／decode 原文與對照表有落後項目；簡中價格頁為人民幣、英文頁為美元；Lists Models 範例只列兩個 id、未說明可用版本名呼叫；8/13 更新日誌「沿用名稱即用最新版本」；更新日誌 9/10 條目查核時只有繼續提供那段、新聞列表最新仍是 news260910。
- verified_facts 修正：兩千張 GPU 改記原文並註明是部署合作邀請；inference README 補「reference implementation」與未列最低硬體需求。
- unverified_or_excluded 新增：更新日誌是否曾被改寫無一手證據；社群帳號未查；V4-Pro 9/14 後實際可否呼叫未測；存檔站查核當天無法複核。

## 讀者角度檢查

- 隱私：第 5 節只寫「請閱讀 DeepSeek 官方隱私政策與服務條款，本文不代為解讀」，並寫明不論廠商國別都要先看內部資料規範；沒有未查證的資料安全指控。未改。
- 實測暗示：開頭第二段與第 1 節都寫明本站沒有呼叫或重測；上班族摘要情境標明為編輯設計。未發現「我們試用」類文字。
- 與 `ai-news-qwen-35-20260216` 的重疊：Qwen 篇談開放權重下載、硬體門檻、託管與自建取捨；本篇只在第 5 節最後一段一句帶過並指向該篇，主軸是模型名導向與 V4-Pro 去留，不重複。
- 與既有 `deepseek-privacy-and-data-flow`、`deepseek-chat-and-reasoner` 指南：本篇沒有重講隱私或推理模式內容。

## 仍不確定的點

1. 「9 月 14 日之後繼續提供 V4-Pro」這段文字是哪一天加上的，官方沒有標示；更新日誌 9/10 條目是否曾寫過導向文字也無一手證據。文章只寫查核當天的文字與措辭上的先後。
2. 發布公告頁（英、簡中）至今沒有更正；DeepSeek 之後若改公告或改價格頁，表格與 callout 需要重查。
3. V4-Pro 在 9/14 04:00 UTC 之後實際是否仍由 DeepSeek-V4-Pro-0813 回應，本站未呼叫 API 驗證。
4. DeepSeek App 與網頁版目前的模型：9/10 的公告與更新日誌都沒寫（對照 8/13 條目有明寫 APP／Web），文章維持「官方這幾頁沒有交代」。
5. DeepSeek 在 X、微信公眾號等管道是否另有說明未查。
6. 更新日誌 NL2Repo-Bench 65.4 與模型卡 64.0 不一致（文章不寫分數，不受影響）。
7. 「開放下載不代表一般電腦跑得動」是編輯判斷，官方沒有列最低硬體需求；依據是 552B 參數規模與官方推論範例用 8 個 tensor-parallel rank。
