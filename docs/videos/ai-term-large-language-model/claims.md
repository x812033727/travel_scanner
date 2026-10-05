# 大型語言模型：逐條主張與來源

作者整理日：2026-10-04。這是待獨立查核的作者主張表；不代表已查核通過、核准或已生成媒體。

「原創」指本集作者的虛構故事、示意稿或可重跑的離線程式，不是其他模型的真實輸出。凡標「編輯方法」為站主立場 4、6、7 的具體操作建議，不是保證零錯誤的產品能力。所有 scene 的 `claims` 都對應下列編號。

| 編號 | 主張與支持範圍 | 來源 | 重查日 | 場景 |
| --- | --- | --- | --- | --- |
| c1 | 失物櫃台、人物、所有地點與生活比喻都是原創虛構示意；麵團、陶藝、集市不是模型內部實物。 | 原創：brief.md、build.mjs | 2026-10-04 | 場景預設 c1，fictional-label |
| c2 | 語言模型能生成看似通順的文字，但輸出仍可能有錯；文字完整與可信度不能等同。 | https://developers.google.com/machine-learning/crash-course/llm/transformers | 2026-10-04 | hook、counter-handoff、market-scoop、errors-chapter、garden-language、wrap |
| c3 | 本集離線程式只用標準函式庫，未呼叫網路、帳號或語言模型；輸出只驗資料與規則，不能代替模型能力評測。 | 原創：demo.py、demo-log.md | 2026-10-04 | fictional-label、evidence-terminal、demo-not-benchmark |
| c4 | L001 是雨傘，location=north_counter、status=unclaimed；紀錄沒有失主姓名或電話。 | 原創：demo.py RECORDS、demo.py evidence | 2026-10-04 | counter-hands、counter-empty-hook、first-three-jobs、evidence-terminal |
| c5 | 王先生、失主電話與「已領走」錯誤句由編輯刻意寫成，非實測輸出；這些內容與紀錄不符或無法支持。 | 原創：build.mjs first-three-jobs / invented-name；demo.py | 2026-10-04 | first-three-jobs、invented-name、kitchen-gap |
| c6 | 本示例的物件位置紀錄不能證明任一訪客所有權；不作真實失物領回規則或法律判定。 | 原創：demo.py 欄位範圍 | 2026-10-04 | counter-match、counter-dog |
| c7 | 一份回答可以同時含文字生成、資料查找與工具計數；模型可把外部結果組成文字，三欄是查依據／執行證據，非互斥分類。 | https://ai.google.dev/gemini-api/docs/function-calling | 2026-10-04 | counter-boxes、three-jobs-card、garden-language、three-column-card |
| c8 | 符合未領且為雨傘的紀錄是 L001、L003，共兩筆；不是所有六筆。 | 原創：demo.py count、demo-log.md | 2026-10-04 | counter-pair、count-terminal、demo-two-umbrellas、condition-stats |
| c9 | 模型提出函式／工具要求後，應用程式仍須處理呼叫並交回結果；要求不等於已執行。具體自動化與權限依產品而異。 | https://ai.google.dev/gemini-api/docs/function-calling | 2026-10-04 | tools-chapter、market-request、tool-three-steps、garden-tool |
| c10 | 常見因果式文字生成根據已有 token 預測下一個，生成内容參與後續步驟；不能看到尚未產生的 token。此說法不泛化為所有 LLM 架構。 | https://huggingface.co/docs/transformers/tasks/language_modeling ; https://huggingface.co/docs/transformers/llm_tutorial | 2026-10-04 | bakery-next-piece、bakery-row、generation-not-all |
| c11 | LLM 是 Large Language Model 的縮寫，大型語言模型經訓練學習語言模式與表示；不是單一聊天產品的名稱。 | https://developers.google.com/machine-learning/crash-course/llm ; https://developers.google.com/machine-learning/crash-course/llm/transformers | 2026-10-04 | generation-chapter、bakery-skill |
| c12 | token 可能是詞、子詞或字元，不能一概一中文字一 token；本集麵團比喻沒有實作 tokenizer 或給固定換算數值。 | https://developers.google.com/machine-learning/crash-course/llm | 2026-10-04 | bakery-pieces、bakery-uneven、token-card、garden-related-token |
| c13 | 文字生成的選擇受上下文與解碼方式影響；常見方式含貪婪選擇與抽樣。不說哪種保證正確。 | https://huggingface.co/docs/transformers/llm_tutorial | 2026-10-04 | bakery-selection |
| c14 | Transformer 可以有編碼器、解碼器或兩者；本稿因果式單向生成不代表所有語言模型一模一樣。 | https://developers.google.com/machine-learning/crash-course/llm/transformers ; https://huggingface.co/docs/transformers/tasks/language_modeling | 2026-10-04 | generation-not-all |
| c15 | 常見自注意力以數學方式處理 token 間的關係與重要性；代名詞例子是本集原創簡化示意。 | https://developers.google.com/machine-learning/crash-course/llm/transformers | 2026-10-04 | bakery-relations、bakery-carry、bakery-weigh |
| c16 | 注意力處理上下文，不保證永遠理解或找對所有指涉；這是來源能力範圍加上錯誤可能性的保守邊界。 | https://developers.google.com/machine-learning/crash-course/llm/transformers | 2026-10-04 | attention-boundary |
| c17 | 一般推論時貼入資料，是提供當次上下文；訓練／微調才是調整權重的不同程序。不否認產品另外保存或用資料訓練的政策。 | https://developers.google.com/machine-learning/crash-course/llm/tuning | 2026-10-04 | parameters-context、pottery-new-clay、pottery-brief、market-saved |
| c18 | 模型參數是訓練更新的數值，參與運算；不等於每個參數對應一筆可翻查的失物紀錄。 | https://developers.google.com/machine-learning/crash-course/llm/transformers | 2026-10-04 | pottery-adjust、pottery-many-pots、parameters-context |
| c19 | 本集「不是逐條失物簿」是機制比喻，不能推論模型從不記住訓練資料或無法檢索任何事實。 | 原創限定表述；https://developers.google.com/machine-learning/crash-course/llm/transformers | 2026-10-04 | pottery-many-pots |
| c20 | 後續對話是否仍可見材料取決於應用程式是否提供當次輸入；產品保存、再次檢索／提供與模型重訓需區分。 | https://huggingface.co/docs/transformers/llm_tutorial ; https://developers.google.com/machine-learning/crash-course/llm/tuning | 2026-10-04 | pottery-bare-table、market-key、memory-rule、garden-next-context |
| c21 | 指令指定表格等形式屬於調整輸入任務；不因此保證遵守或事實正確。 | https://developers.google.com/machine-learning/crash-course/llm/tuning | 2026-10-04 | pottery-instruction |
| c22 | 缺欄位卻填姓名、把未領寫成已領，是本集可直接對照的錯誤示意；格式完整不能證明新增內容。未聲稱實測到模型做此事。 | 原創：demo.py、invented-name 字卡 | 2026-10-04 | pottery-limit、kitchen-empty-jar、invented-name |
| c23 | 可要求只依資料、標來源、缺欄位寫未知並說缺什麼；是編輯操作建議，仍須檢查實際回答，非保證。 | 站主立場 4、6、7；原創操作示意 | 2026-10-04 | unknown-rule、check-lines、rewrite-request、garden-check-it |
| c24 | 生成機制不等同完整能力考試；是否完成任務應用任務結果與核對標準判斷。不宣稱永不能推理或像人一樣理解。 | https://developers.google.com/machine-learning/crash-course/llm ; 編輯方法 | 2026-10-04 | pottery-capability、pottery-uncertainty、kitchen-task |
| c25 | 六筆原創資料包含兩把雨傘、一水瓶、一圍巾、一帽子、一手套。完整行在 demo-log.md。 | 原創：demo.py data | 2026-10-04 | demo-six-objects、six-records-table |
| c26 | L002/L005 已領，共兩筆；未領 L001/L003/L004/L006，共四筆。全部六、未領四、未領傘兩各有不同條件。 | 原創：demo.py count | 2026-10-04 | six-records-table、demo-cap-out、count-terminal、condition-stats |
| c27 | L001 不含 owner_phone 欄位，demo.py missing 回 UNKNOWN / field_not_in_dataset；沒有到網路搜電話。 | 原創：demo.py missing、demo-log.md | 2026-10-04 | missing-terminal、demo-phone-gap |
| c28 | 資料缺電話只能說本資料無法回答，不能推出全世界不存在電話。 | 原創資料範圍與邏輯邊界 | 2026-10-04 | demo-empty-palm |
| c29 | 留條件、代號與實際結果可回查每一步；是本集檢查方法，不代表工具永遠不會算錯。 | 原創：demo.py count；站主立場 4、7 | 2026-10-04 | demo-trace、three-column-card、rewrite-request |
| c30 | Mokaair 已有 LLM 文章圖解；本集新製的六筆資料獨立完整附在說明本文與 demo-log，不把未上線 repo URL 當連結。 | apps/api/app/guides/content/what-is-a-large-language-model.json ; demo-log.md | 2026-10-04 | article-cta |
| c31 | 這次離線規則得到確定輸出，不證明任何模型永不犯錯，也不證明整類模型能力高低。 | 原創實驗範圍 | 2026-10-04 | demo-not-benchmark |
| c32 | 資料取得、工具執行與模型整理是不同階段；條件或資料可在任何實作階段出錯，需逐段核對，不只查數字。 | https://ai.google.dev/gemini-api/docs/function-calling ; 原創資料示例 | 2026-10-04 | market-scoop、tool-three-steps、kitchen-counterexample |
| c33 | 完整應用程式可準備輸入、提供外部工具並處理輸出；相同模型在不同整合裡能存取的資料／工具可以不同。不是每個產品都有每個功能。 | https://ai.google.dev/gemini-api/docs/function-calling ; https://huggingface.co/docs/transformers/llm_tutorial | 2026-10-04 | product-model、market-boundary、market-access |
| c34 | 重複相同文字不是新增獨立外部證據；兩個答案一致不能單獨證明真實性。本稿不給任何模型相關錯誤率。 | 邏輯與編輯方法；https://developers.google.com/machine-learning/crash-course/llm/transformers | 2026-10-04 | kitchen-repeat、kitchen-agree、kitchen-evidence |
| c35 | 找到來源後仍應對照支持範圍，不能因為有來源就接受任何延伸句子。 | 站主立場 4，編輯查核方法 | 2026-10-04 | kitchen-bias、garden-check-it |
| c36 | 檢索提供相關材料，工具執行指定處理；這是本集分工概述，不宣稱所有檢索都聯網、都回正確結果或改模型權重。 | https://ai.google.dev/gemini-api/docs/function-calling | 2026-10-04 | nearby-terms |

## 與企劃不同的地方

候選選項 A 寫成 11 秒冷開場與七個內容章，75 張原創 shot。2,929 口播單位，估約 13.84 分鐘，比 10 分鐘目標長；上緣不是上限，保留必要機制、三個可回查步驟與能力邊界，沒有慢播、空停頓或重複灌時。實際正文至少 8 分鐘仍須合成後驗證。沒有配樂與音效欄位，待確認授權素材或已有設定後再安排。

## 我懷疑但沒動的事

- Google 頁面同時講完整編碼器／解碼器與遮罩訓練，不能套到所有生成式 LLM；本稿另用 Hugging Face 因果生成來源收窄。
- 沒有測模型，不能填模型錯誤率或把兩個答案一致說成正確。
- 工具的條件與實作也可以錯；本次只對六筆離線資料驗證，不泛化為「工具一定正確」。
- 聊天產品的記憶與訓練政策因產品不同；本稿保留條件句，不對任一產品作功能承諾。

## 進度

完整旁白、75 插圖提示、字卡與離線程式已撰稿；官方頁重開、離線 demo 已跑。尚待獨立逐條查核、聽眾審稿、大綱核准、旁白、插圖、品管、語言選擇及上架。數字只是估算或此次離線資料輸出，不是成片時長、模型跑分或發布證據。
