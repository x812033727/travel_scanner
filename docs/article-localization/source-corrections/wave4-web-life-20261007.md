# 網站設計與 SEO 生活文章：來源修正與四語本機安裝紀錄

這一批十二篇既有公開 zh-TW 文章已完成 en、ja、ko、zh-CN 共 48 份獨立最終審稿，並由協調者執行官方 bundle 組裝、本機安裝及相同命令重播，三個實際程序均 exit 0。此紀錄涵蓋本機內容準備；尚未表示這一批已合併、部署、匯入或正式發布。

固定範圍為 `css-layout-basics`、`image-formats-compression`、`responsive-layout-basics`、`web-layout-hierarchy`、`website-color-system`、`website-information-architecture`、`website-cache-cdn`、`search-crawlers-explained`、`structured-data-basics`、`sitemap-website-submission`、`web-design-project-workflow`、`seo-content-cannibalization`。來源查證截點及既有 `checked_on`（2026-09-14）保留；本次不把重讀舊證據描述為重新取得官方網站事實。

六篇來源共有九個精確修正。八個 ArticleInline 將一般網站用語錯連至 AI 術語文章，修為同字 TextInline；另一處修正繁體字。修正不改其餘原文葉節點、文章 metadata、來源 URL／日期、其他既有語系、原始媒體或授權。

| 文章 | 精確來源 pointer | 已覆核修正 |
| --- | --- | --- |
| `website-color-system` | `/blocks/3/inlines/1` | ArticleInline `參數`（`ai-term-model-parameters`）→ 同字 TextInline |
| `website-color-system` | `/blocks/17/inlines/1` | ArticleInline `標記`（`ai-term-token`）→ 同字 TextInline |
| `website-information-architecture` | `/blocks/15/inlines/1` | ArticleInline `標記`（`ai-term-token`）→ 同字 TextInline |
| `search-crawlers-explained` | `/blocks/12/inlines/1` | ArticleInline `標記`（`ai-term-token`）→ 同字 TextInline |
| `structured-data-basics` | `/blocks/1/inlines/1` | ArticleInline `標記`（`ai-term-token`）→ 同字 TextInline |
| `structured-data-basics` | `/blocks/5/inlines/1` | ArticleInline `分詞`（`ai-term-tokenization`）→ 同字 TextInline |
| `sitemap-website-submission` | `/blocks/0/inlines/1` | ArticleInline `參數`（`ai-term-model-parameters`）→ 同字 TextInline |
| `seo-content-cannibalization` | `/blocks/24/inlines/1` | ArticleInline `標記`（`ai-term-token`）→ 同字 TextInline |
| `seo-content-cannibalization` | `/blocks/18/items/2` | `連贯` → `連貫`，其餘句子保留 |

來源提案／套用者與來源最終 reviewer 分離；下面為六份原始、未重新代寫的獨立來源修正收據 SHA-256。官方 `source_correction.verify_review` 重建精確 diff，確認原公開來源與資料庫版本／雜湊 guards、修後 normalized document 及未改其他葉節點。

| 文章 | 原始獨立 reviewer | 原始 review SHA-256 |
| --- | --- | --- |
| `website-color-system` | `news_gate_review` | `72dbb208142dc02ce6f161f068942de9bd6c38fc14c3124421a3fac8b5d370a2` |
| `website-information-architecture` | `news_gate_review` | `5e250cd1b9451422b19b5aa05a512ca56ff164d584bbc7499e10c1b93acb2985` |
| `search-crawlers-explained` | `localization_task_inventory` | `e1fd2dcde9a7bd798c249b50b2fac30c9b8ced907ee3ede1da485058ad879aad` |
| `structured-data-basics` | `localization_task_inventory` | `e7a54c4129c10ed20b79e9f9d3dfafcea6df841adcddffac3dc003dc26b73d9e` |
| `sitemap-website-submission` | `hk_target_final_review` | `f38e7022a81ac6cf786ef9a3074f988d15e94ba5aabf5abf9ac9e142b30b68e8` |
| `seo-content-cannibalization` | `hk_target_final_review` | `864b811e1aeb1e596a9ff55522e4b09f9e79925399ce71c5bd124acaa079d8a7` |

原正式站 baseline SHA-256 為 `19c0ff10e958055d59d71ac4fb2b8ef9291d77dbbc2d3917bb491661829b3eae`，保持原位元組。Authoring derived baseline SHA-256 為 `7194d18dc7f1880aa4b16e5e37adf14b411d1eacf4f8d0b85ee6c62cb363dced`；其六篇僅依已核准來源更改 `source_document`、`source_sha256`、`locale_documents.zh-TW`、`pack_sha256`。全部 1,204 列其餘欄位及原 DB guards 相同。Admission 收據 SHA-256 為 `6d293c3bd0f775abeecbbd8c759409ec4df7c195b9eda9d0c1d875afe4671b55`。此 derived baseline 是本機 authoring 輸入，未冒充下一次發布的新正式站快照。

四語原始 Codex CLI attempts 與 `thread.started` 證據保留，最終 reviewer 與真正翻譯者分離。逐篇審稿包含全文、標題與 description、來源標題、所有 SVG 文字與描述、實際 preview PNG、最終 hero JPG、字形、native 可見字級至少 15px、數字／URL／code、AI 圖片聲明及文章連結。下面記錄真正最終 reviewer，未把工具 exit 0 轉成新 editorial PASS。

| 語系 | 真正最終 reviewer | 篇數 |
| --- | --- | --- |
| `en` | `localization_existing_work` | 12 |
| `ja` | `hk_target_final_review` | 12 |
| `ko` | `Codex /root (4e16)` | 1 |
| `ko` | `localization_existing_work` | 11 |
| `zh-CN` | `news_gate_review` | 12 |

最終 48 份原 review 的獨立 SHA／artifact／document／producer／evidence 綁定收據 SHA-256 為 `f6e3e43769bfd50ca2fe504c066f3de914cb0bb5d42827d7a24bcbf031801139`。JA 最終 handoff SHA-256 為 `98aa263be0c16cb602fa6be4193f083a12ef7314a897a808a9b33a26e8c50e92`。KO 的 `structured-data-basics` 最後一筆修正將「지난 날짜나 허위 리뷰」改為「갱신되지 않은 날짜 정보나 허위 리뷰」，保留 numeric／URL tokens；官方 materialize/render 完成後，另一位 reviewer 重新親讀實際最終稿並出具當前審稿。其餘 47 份 artifact 與原固定 pins 相同；所有原始 attempts、失敗紀錄、修正前 backups 與 review 原字節保留。

組裝後的 manifest SHA-256 為 `a175e63ec2a7ef5b845e5416bd3b6f4f0a41ca8e2b90f9428ddb5cd8d6e2594c`，涵蓋十二個五語 pack、156 個資產及六份來源修正。實際 assembly 收據 SHA-256 為 `f9ac2b60debbc4994efac9cf74a1507c7755207d36fb534fb0e202bc0ad6677f`。本機 installation/replay 完成收據 SHA-256 為 `f9cd63964fc2da6faf6c4da836412ad75ea5bc1c3a5b24140d2bb0819df58ab1`；實際 journal SHA-256 為 `2651273e143a9725c256532c441e94f7e36c115e27d08c95a3f1ba291cd8f869`，status 為 installed，共 168 筆 pack／asset 操作。獨立唯讀交核確認每筆目前位元組、原／staged bundle 與 48 個 job 全檔一致，官方 bundle／deployed-content／reviewed-job contracts 接受。

協調票在寫入前包含 stage、`docs/article-localization/installations/.lock`、實際 manifest 前 16 碼目錄及十二個 per-slug receipts；backup 檔名使用 before SHA 前 24 碼。原計畫的 `.install.lock` 名稱以官方工具實際 `.lock` 為準。私人 stage 在複製前已有 `*` ignore 規則；外部原始 baseline、job、review 和 bundle 均保留。

重播前的實際 file-pin capture 有 193 筆資產與 journal／receipt 檔案，其位元組重播後相同，該 capture 沒有十二個 pack 檔。十二 pack 及全部 168 操作的目前 after SHA 均獨立驗證；兩次官方 installer 本身也驗證相同 operation after hashes。這是本次重播證據的精確範圍，不聲稱不存在的 pack 前後原始 capture。

原 wrapper 在兩次官方 exit 0 後把 bundle-relative pack path 用作 repository path，最後唯讀核對失敗；失敗完整保留，另用 baseline 的 repository pack path 完成唯讀核對，沒有重跑 installer。獨立技術交核 SHA-256 為 `374aec15a2e0e1ad266b7b5888c9e6b753485f338827a7a613c28e64111c9eaf`；錯誤 manifest、錯用原 baseline、外部安裝輸入、未核准來源、改動原 DB guard、少一筆來源 diff 的六個唯讀 negative probes 均實際拒絕。

後續發布需另走 release 任務、實際部署後新正式站 baseline、原六份來源修正 admission 及新的 publishing journal。預定 selected scope 是 48 個新 target locales 加六個修正 zh-TW 來源，共 54 個 selected locale operations；不得改原審稿／attempt bytes，或以這份本機紀錄宣稱已公開補齊。

開 PR 前另比對全部十三篇 ArticlePack：分類值與其餘 metadata 值保留，topics 的序列化順序採正式站快照釘住的順序，沒有改動 topic 成員。既有 schema 的預設欄位會由官方 assembler 寫出，原始檔案位元組與 normalized model 的比較範圍分開。日本入境文章的來源修正與四語審稿另有專屬紀錄。
