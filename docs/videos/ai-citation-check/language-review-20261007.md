# 四語文字與來源獨立審稿

**結論：en、ja、ko、zh-CN 均 ready after fixes；8 項全文建議已由主操作者套用並獨立核對，現行文字無待修正項。** 另三處先前字幕速度修正亦已覆核，見 `caption-review-20261007.md`。這是來源綁定的本機文字審稿，不是原生 language gate、站主選語、配音、音訊 QA、最終影片或上架核准；未知 ASR 與 STOP 仍保留。

覆核者 `language_review_contract` 未撰寫原翻譯，未修改翻譯、繁中源稿、hash 欄位、音訊或字幕產物。依 `caption-review.md` 讀取繁中 36 場／143 句、各語 143 句（共 572 個翻譯 entry）、各語標題／說明／四個 tags／六個章名，並讀 `claims.md`、`demo-log.md`、兩輪查核、lexicon 及實際字幕。原作者自審沒有作為通過理由。沒有執行 Git、付費 API 或 review API。

全文翻譯覆核釘選讀取於 `2026-10-07T09:40:01.853Z`；後續視覺修訂與重新產生的 metadata draft 另於 `09:47:27.355Z` 獨立重綁。來源與完整機械 metadata 詳見同名 JSON；SHA-256 均為實際 bytes，不是沿用舊檔案名推定。

## 可驗證來源與日期

| 來源 | 本輪實際存取與身分 | 支持範圍／限制 |
| --- | --- | --- |
| S1：[Anthropic Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations) | 官方原頁；公開 GET 於 `09:38:03.581Z`，HTTP 200，無跳轉。頁名 `Reduce hallucinations - Claude Platform Docs`；361,732 bytes，SHA `0a9c390223bc10bd76b8e94141f35f3f1e1b64c7581abb409ce3aec33e07b070`。另以 web 工具讀取正文。 | 原頁把引用用於逐項可查核性、找不到支持就撤回；允許不確定可減少錯誤，不能消除錯誤，關鍵資訊仍要驗證。支持 C1／C2／C3／C5；沒有支持「附引用便免人工查核」。本輪未見可核對的發布或更新日，HTTP Last-Modified 亦空。 |
| S2：[Mokaair 提示詞入門](https://mokaair.com/zh-TW/life/ai-chat-prompt-basics) | 自有文章原頁；公開 GET 於 `09:38:07.222Z`，HTTP 200，無跳轉。514,970 bytes，SHA `424c9083bcd5fb4562449e6c99e3570d62d88c85547fadaf9428797f174a6b6d`。web 工具先回不可存取；後續直接公開 GET 確認正確題名與內容，另讀 repo 文章包。 | 入門內容確實教要求來源、列出缺少資訊與允許說不知道，支持 `ci068`–`ci071` 的 CTA 說明與 C4／C5 編輯脈絡。不是模型正確性保證；本輪沒有把頁面內容日期當成經驗證的最後更新日。 |

原稿的 `checked_on=2026-09-27` 與四語說明中的 2026 年 9 月 27 日保持歷史查閱語義。本輪讀到該日留存紀錄，但不能獨立重演當日 HTTP 回應；2026-10-07 是本輪重查日，兩者均不是文件更新日。C4、三步法與「先停一分鐘」屬編輯提供的習慣，沒有被翻成成功率、實測耗時或保證完成查核。

## 八項全文修正及實際套用

| 語系／ID | 問題與原譯 | 已套用且重新讀取的文字 | 原生 CPS |
| --- | --- | --- | ---: |
| en `ci117`（meaning） | 原文是影響決策「也」可能造成損失；`Start with the claim most likely to affect a decision or cause harm.` 用 or 擴大選取條件。 | `Start with the claim most likely to affect decisions and cause loss.` | 13.40 |
| en `ci062`（meaning） | `If it cannot find a supporting passage, have it say so.` 未明說原文的「不知道」。 | `If no passage supports it, have it say 'I don't know'.` | 13.95 |
| en `ci068`（meaning） | `The first link below is a beginner's guide to prompting.` 沒保留「說明欄第一行」的位置。 | `The description's first line links to a beginner's prompting guide.` | 15.00 |
| en `ci098`（readability） | `And drop unsupported claims cannot become no need to check.` 未標示兩個被比較的說法，閱讀易混淆。 | `'Drop unsupported claims' cannot mean 'no need to check.'` | 10.84 |
| ja `ci091`（meaning） | `見つからないなら、引用先が違う可能性もあります。` 漏掉「不是你讀得不夠快」的對比。 | `見つからないのは読む速さでなく、誤引用のせいかもしれません。` | 6.64 |
| ja `ci105`（meaning） | `古い記事は過去の説明には使えても、今の判断には不十分です。` 把「不一定」加強成一定不足。 | `古い記事は過去を説明できても、今の判断に使えるとは限りません。` | 4.35 |
| ko `ci105`（meaning） | `오래된 글은 과거 설명엔 좋아도 오늘 결정엔 부족합니다.` 同樣把可能不適用變成定論。 | `옛글은 과거를 설명해도 오늘 결정엔 안 맞을 수 있습니다.` | 4.49 |
| zh-CN `ci141`（facts） | `页面更新得再新，也未必支持每一项主张。` 將原文「頁面日期」改成「更新」日期。 | `页面日期再新，也未必支持每一项主张。` | 3.95 |

主操作者採用了英文引號內／外句點的排法；本覆核讀的是表中的實際值。標點沒有改變不確定性、否定或引文範圍，沒有為了表面完全相同而要求再改。

各語其餘全部 entry 亦對照繁中核過。`ci004`／`ci005`／`ci077` 保留編輯刻意寫錯的示意與「不是真實模型輸出」；`ci045`／`ci046`／`ci050` 保留降低不等於消除；`ci033`／`ci058`／`ci073` 保留引用不是正確保證；`ci034`／`ci038`／`ci062`／`ci107`／`ci135` 保留撤回未支持主張與不確定；`ci055` 保留查閱日，沒有當成更新日。數字三步、一分鐘與歷史年月日沒有改變；沒有加入真實產品事故、價格或模型實測結果。

英文自然直接，日文以ですます體結句，韓文保留自然有禮的教學口吻，簡中為可讀的簡體表述；沒有必要為填滿修正表而更換同義詞。未見數字或名稱跨 cue 移位造成相反意義。硬性 dub max_chars 不適用：本任務沒有已選 dub worksheet，不能用旁白字幕速度推定配音可以合格。

## 當前實際檔案與原生文字綁定

| 語系 | entry／最大字元 | 標題字元／章數 | 實際翻譯檔 SHA-256 |
| --- | --- | --- | --- |
| en | 143／80 | 59／6 | `d3fa6fe0ec97cec0b13ed2ac381c78796e7ad57fb1010df964ac5d0c670abd24`（20,037 bytes） |
| ja | 143／36 | 28／6 | `b4e506bdac60e6d60e75b3df42e0cf1c5fdde4c0fc122260dec3b6ccf2ab816e`（22,187 bytes） |
| ko | 143／38 | 32／6 | `becbc66517ff02bdc13b006af231a4dc45a3b53c731f9eac7ebb055c7d94af0d`（21,688 bytes） |
| zh-CN | 143／25 | 20／6 | `b3064a01e966e7b6cd2cae7e40894046445e89bb1ef5a97bb71fa010cbeafe0f`（19,477 bytes） |

相對首次釘選，實際 text 改動只有英文六句（兩個速度＋四個全文修正）、日文三句（一個速度＋兩個全文修正）、韓文一句與簡中一句，共 11 句。所有 572 個既存 source_hash 與各語非 line 欄位完全不變；逐一重算原生繁中 textHash，缺句、stale hash 及孤立 ID 都是零。四語 title／description／tags／六章的 source_hashes 都 current，原生 `checkYoutubeFields` 零問題。

現行 `video.json` SHA `ba96bc7d5d1cc5d6fd20172064baefabd2bb319b00ba67387b02b4e90c5e3423`（24,643 bytes）與視覺修訂前 `a9b9eb260a2d61a6f430fdb74e2193a6327fb3267aa7c430b39105235f8d3cd2` 不同；獨立比對確認所有 143 個繁中 ID／順序／文字／原生 source_hash、YouTube 欄位、sources 及縮圖文字相同。原生 `speech_hash=399237f659e75fc5`，實際 draft timeline SHA `3ef9c3e53d35f4192ca8207220ce2b4f0809e10cada127c20ac8a68665d841b5`。

收尾的檔案釘選檢查實際偵測到 `c1e01a5a…` 已變為上述 `ba96bc7d…`，因此沒有把舊快照繼續標成 current。`09:46:10.103Z` 與 `09:47:27.355Z` 的獨立差異檢查確認最新變動只有 `link-vs-proof`／`not-found` 兩個既存 verdict 字串移到 title 第二行；沒有新增或刪除主張，voice／章節／metadata／sources／縮圖／所有 143 個原生 source_hash 與文字不變。metadata draft 已由主操作者重建後再綁定。本段核對文字與依賴，不代表實際渲染安全區或畫面已獲批准，也沒有把視覺整檔變更說成整檔未變。

## 字幕與說明欄的實際 draft evidence

實際 `20261007T093841Z-draft-captions.exit.json` 記錄 `09:38:41.628248Z` 開始、`09:38:44.360071Z` exit 0。日誌與 manifest 為繁中 143、英文 143、日文 144、韓文 148、簡中 143 cues，五語問題空陣列、timing 均為 narration。獨立以原生 `parseSrt`／`checkCues` 再讀 SRT，並由現行 text＋同一 timeline 呼叫 `buildCues`：每個 cue 的文字、開始與結束時間全數精確相同，問題均為零。這證明本次字幕檔的文字與讀取速度，不證明配音或旁白已獲音訊 QA。

主操作者依最後視覺稿實際重建的 metadata draft 於 `09:47:03.472Z` 生成，7,823 bytes，SHA `014459f94b52a86e2e40a122fe65640fa539a7b70c00903b7e4e532aa6d98b22`。本覆核讀到其全部來源 SHA 仍 current、六個章節及零 field problems。繁中實際第一行為：

`🔗 完整文章：https://mokaair.com/zh-TW/life/ai-chat-prompt-basics?utm_source=youtube&utm_medium=video&utm_campaign=ai-citation-check`

英／日／韓／簡中也在第一行放相同實際文章 URL，配各語的 Full article／記事全文／전체 글／完整文章 標籤。連到繁中入門文章的實際路徑符合現行 draft，不據此宣稱文章已有四語版本。說明仍保留官方來源與歷史查閱日。這是 `review/metadata-draft` 的未核准本機產物，尚非原生 `upload/metadata.json` 或正式上傳包。

四語都沒有 `thumbnail` 翻譯文字，原生狀態為 missing；本輪只核對源稿縮圖與教學示意一致，沒有審不存在的翻譯縮圖或宣稱多語縮圖完成。此選用項不是本輪現有字幕與已填 metadata 的待修正文字。

統計：全文 meaning 6、facts 1、readability 1，其餘分類 0；8 項均已套用，另三處速度修正保持通過，現行待修正 0。後續任何 text／source／metadata 變更都需重新釘選。原生語言選擇、manifest、音訊、成片、正式產包及上架關卡仍由正常流程處理，本紀錄不改動那些狀態。
