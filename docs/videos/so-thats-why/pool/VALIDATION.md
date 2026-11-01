# 第三批素材池驗證：2,328 筆檢查點

日期：2026-11-01；Node v24.19.0。前批封存：[1,000 筆](VALIDATION-1000.md)、[2,000 筆](VALIDATION-2000.md)。本頁只報實際完成範圍。

## 資料與編輯

- [當期資料與索引收據](reviews/wave3-final-validation.json)：2,661 原始紀錄、2,548 核心、2,387 可選、2,328 入選、113 別名、59 候補。0 個未處理高相似警示不是全庫沒有語意重複的證明。
- 第三批 368 筆原題由非作者逐題編輯覆核，外站風險抽查：生命 93、化學材料 91、地球觀測 89、資訊系統 95。27 組新題合併、8 題暫緩後，新增 333 核心；另舊題 4 合併、1 暫緩，淨增 328。
- 1,224 與 2,293 個已封存舊 raw 均未改寫。首批退休／合併 L042、L293、P150、L177，以及第二批 E2106 都有當期聲明；原始問法與來源保留。
- 當批 171 個不同來源 URL；首次加入全庫 165 個。全庫 3,710 URL，其中三批研究來源 741；入選使用 1,972 URL、3,640 題來源關係。包含歷史引用，不能說這些頁面本次都重讀。
- 必要修正已由原覆核者讀回：Fernet 建立時間、ROWID 識別碼、構象平衡與能障、裂長/載荷/韌性門檻、ATP 旋轉描述、GA 胚來源與存糧來源的分工。見 [集中處置及修正入口](reviews/wave3-editorial-integration.json)。
- 地球來源部分 web 工具取得失敗，改讀作者重新取得的原始副本，沒有假稱 reviewer 網頁讀通；URL、hash 與獨立讀取範圍在來源副本及審閱收據。副本留在忽略版控暫存，不搬進正式素材。

## 影片長度

共 38 組影片候選，新 12 組正文預算 225–600 秒。正文包括解說開場與收束，不包含固定品牌片頭片尾；這不是試讀或成片實測。

G28 由 580 收到 415 秒；G29 結尾縮短至全片 520 秒，刪 70 秒再生章時剩 450 秒；G32 不採尚缺例證的 165 秒 FRET 延伸，先用 225 秒版本；G37 移出動畫時基支線剩 295 秒；G38 依段落可用內容收至 435 秒。每組保留無聊風險、刪除條件及證據缺口，不以題目數乘固定分鐘。

## 語意工具及程式

[已知配對評估](reviews/wave3-semantic-baseline.json)：上一批 50 組人工合併，語意 top-10 找到 29、詞面 11、聯集 31。這不是隨機樣本或全庫召回率。另 23 組不同核心中 12 組也在近鄰，不把近鄰當合併判決。新批和 12 組舊配對由人工看機制及條件，沒有自動分數淘汰。

[獨立程式審閱](reviews/wave3-life-code-review.json) 驗過實際模型 3 題的遮罩平均/L2，與獨立計算最大差約 2.98e-8；模型檔 hash、快取損毀及提交前中斷保護通過。兩個發現已修：缺 checkpoint 不可靜默略過，新題不可省 editorial。

```powershell
node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs tools/repo-hygiene.test.mjs tools/json-duplicate-keys.test.mjs tools/docs-videos-tests.test.mjs
python -X utf8 tools/video/so-thats-why/pool/semantic_test.py
node tools/video/so-thats-why/pool/cli.mjs check
node tools/video/so-thats-why/cli.mjs check
node tools/video/long-form/cli.mjs check
node tools/tasks.mjs check
```

範圍相關 Node **32/32**、Python 快取 **2/2** 通過，0 失敗/略過/取消。涵蓋兩份歷史快照、退休理由、新欄位、合併與退題、來源追溯、SQLite 交易回復/冪等/過期保護、HTML 跳脫；未宣稱本機整個 tools/docs-videos 套件皆已跑完。473 支既有長片與 2,287 個 task 格式檢查通過，既有無關警告未代改。

## 真實資料實測

實際本機 SQLite 同快照第二次匯入為 **UNCHANGED / 0 writes**。L042→L041、O3068→P049、H3062→LEG-T07、I3090→I3089 可查回；L177、V3016、I3032、O3069 不入選。GIA 來源反查包含 G34，未做外站監控。

| 動作 | 當次結果 |
| --- | --- |
| 詞面近似候選生成 | 16913.5 ms |
| 更新本機索引 | 8017.4 ms |
| 同快照再匯入 | 165.8 ms |
| 資料／螢光／細胞搜尋 | 3.6 / 6.0 / 3.5 ms |
| SQLite 大小 | 33,370,112 bytes |
| 程序 RSS 快照 | 349,937,664 bytes |

僅一次測量，受當下機器、檔案快取及其他工作影響，不是延遲分位數或併發壓測。本次最後語意重跑 2,661 raw，只有 4 筆文字需新增向量，35.037 秒；不能當作從零建立向量的耗時。

## 輸出與限制

[瀏覽器收據](reviews/wave3-browser-qa.json)：2,328 標示、50→100 分頁、新舊別名、G37 篩選、修正題名、段落秒數、畫面/新增理解和來源定位皆通過；桌面與 390px 手機截圖已人工查看，零頁面 JavaScript 錯誤、無水平溢出。初次測試錯把關鍵字 ID 視為只能回傳一筆；L042 也正確出現在 V3078 範圍引用，後改驗期望核心及其來源卡，沒有改應用程式。

243 個 manifest 輸入與 Git index blob SHA-256 一致。 本機連結及最後 staged 核對結果另附同一驗證收據。

10,000/100,000 真實資料規模、獨立語意品質樣本、完整 treatment、逐主張查核、試讀與觀眾成效仍未完成。沒有正式資料寫入、部署、媒體製作或發布；本次不是背景自動擴庫。
