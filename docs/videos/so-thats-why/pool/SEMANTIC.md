# 語意近鄰：編輯輔助

`semantic.py` 只找待比較的問題，不判定重複，也不修改選入、退題或合併。編輯仍須比較答案、成立條件、觀眾新增理解與來源。

## 模型與資料

- 使用 [Xenova ONNX 轉換模型](https://huggingface.co/Xenova/paraphrase-multilingual-MiniLM-L12-v2)，上游是 [sentence-transformers 多語模型](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)，模型卡標示 Apache-2.0。
- 固定 revision `2c4055b12046f11709e9df2c122e59ffbdc2f900`。程式釘住 ONNX 權重與 tokenizer 的 SHA-256；不執行遠端模型程式。
- 權重約 118 MB、tokenizer 約 17 MB。僅明確執行 `--prepare` 才下載；平常推論在本機 CPU，沒有把候選文字送到代管嵌入服務。
- 輸入是題目加研究目標，最多 128 tokens；attention-mask mean pooling 加 L2，384 維。適用條件仍要人工閱讀，不能只靠向量。
- 執行環境實測為 numpy 2.5.2、onnxruntime 1.31.0、tokenizers 0.23.3。這是可選 Python 工具，不是新增 npm 或正式站相依；機械檢查及人工去重不要求下載模型。

## 使用

在已安裝上述可選套件的 Python 環境執行：

```powershell
python -X utf8 tools/video/so-thats-why/pool/semantic.py --prepare
node tools/video/so-thats-why/pool/cli.mjs preview
python -X utf8 tools/video/so-thats-why/pool/semantic.py --input docs/videos/so-thats-why/pool/.cache/draft.json --output docs/videos/so-thats-why/pool/.cache/semantic-neighbours.json
python -X utf8 tools/video/so-thats-why/pool/semantic_test.py
```

第六批 Node 使用 Codex 附帶 v24.22.1。快取、模型、完整近鄰報告均在忽略版控的 `.cache/`；正式審閱只保存版本、輸入雜湊、判斷與必要摘要。不要把快取列數當成素材數。

快取以文字和模型設定作鍵，矩陣與中繼資料成對驗證。新矩陣先寫成以內容雜湊命名的檔案，最後原子替換中繼資料；提交前中斷仍能讀舊快取。尚未提交的新推論工作可能需要重算。報告本身若寫入中斷須重生，不能視為完整報告。

## 本次量到的效果與界線

[已知配對檢查](reviews/wave3-semantic-baseline.json) 使用上一批人工合併的 50 組：詞面工具找到 11 組，本模型 top-10 找到 29 組，兩者聯集 31 組。這是非隨機、事先知道結果的集合；不是全庫召回率，也沒有用這組結果調門檻。21 組仍不在語意 top-10，必須繼續靠人工和其他檢索找漏合。

23 組原先保留不同的配對中，有 12 組也出現在語意近鄰。近鄰不是合併分類器，因此這不是誤判率；它正好說明相似不能取代機制判讀。新增批次的配對與理由另留在當批獨立審閱及集中處置。

首輪 2,293 原始紀錄完整建向量約 588 秒；之後依文字快取增量執行。長的歷史研究目標有 34 筆截斷，輸出只計本次新建向量的截斷量。沒有完成萬筆／十萬筆效能或獨立抽樣品質評估。現在相似度分塊計算仍為平方量級，不能假設擴到十萬筆可直接照跑。

獨立程式審閱與實際模型小樣見 [code review](reviews/wave3-life-code-review.json)。沒有以語意分數自動復活歷史退題、核准劇本或安排製作。

## 第四批實測

第四批完整原題集合為2790筆。新增129題的top5近鄰由各覆核者讀機制與條件；最後來源/措辭修正後另對最終pool雜湊重算。增量向量2筆、2.957秒，不是冷啟動建向量時間。

當批4個人工合併對，詞面找到1、語意top10找到3；集合太小且非隨機、已知答案，不能推全庫品質。12個尚未標示distinct的舊高分對經兩人讀題/答案/條件後全部保留不同核心；未因此宣稱重新讀其全部來源。細節見[當期收據](reviews/wave4-final-validation.json)、[舊配對](reviews/wave4-root-old-pairs.json)及[第二人覆核](reviews/wave4-science-reviews-home.json)。

## 第五批實測

最終輸入2895原題；當批105提案以問題／答案／條件及近鄰人工覆核，語意不自動合併。修訂後綁定最終pool的SHA重算，新建2向量、3.322秒、當次新增截斷0。歷史截斷限制不因本次0而消失。

當批4個人工合併對，詞面找到1、語意top10找到0。PNG／FLAC共享預測殘差、衣物交聯／舊形狀固定等由人工核心比較處置，不能靠相似字面；完整已知配對與實測見[第五批收據](reviews/wave5-final-validation.json)。樣本非隨機、事先知道答案，不代表全庫召回率，也未調門檻迎合本批。

## 第六批實測

最終輸入2959原題；當批64提案逐讀問題／答案／條件及近鄰，語意不自動合併。修訂後綁定最終pool的SHA重算，新建0向量、2.962秒、當次新增截斷0。歷史截斷限制仍保留。

本批沒有新增人工合併對，因此不計算本批已知合併命中率；53個方向在作者鎖定前已記為不另收錄，不能把它們當63個新核心之外的素材數。近似配對的保留理由在獨立覆核與去重紀錄，未為本批調門檻，也未證明全庫沒有漏合。見[第六批收據](reviews/wave6-final-validation.json)。

## 第七批實測

最終3017原題，新建0向量、2.341秒；新增截斷0，不覆蓋歷史截斷限制。新題的問題、答案、條件與近鄰由非作者逐題閱讀。本批無新增人工合併對，不計算已知合併命中率，也不因此宣稱全庫沒有漏合。

另8組尚未記distinct的舊高分對由兩人逐讀後保留不同條件，非隨機品質樣本。詳[第七批收據](reviews/wave7-final-validation.json)。
