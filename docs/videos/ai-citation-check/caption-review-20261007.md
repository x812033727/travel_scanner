# 三處字幕縮短的獨立覆核

覆核者：`language_review_contract`，沒有撰寫原翻譯，也沒有套用本次縮短。實際檔案讀取與原生純函式覆核時間：`2026-10-07T09:32:28.884Z`。本紀錄只核對英文兩句、日文一句及其字幕時間，不代表完整四語審核、配音、成片或上架核准。後續四語全文覆核另見 `language-review-20261007.json/md`。

原件來自另一工作區的既存檔案；其 SHA 與主操作者 `OP/source-pins.json` 保存的首次來源釘選完全相同。未使用 Git，也未修改翻譯、來源、音訊或字幕產物。

| 語系／句子 | 繁中原意與原件 | 實際縮短後文字 | 覆核 |
| --- | --- | --- | --- |
| en `ci025` | `但還不能證明範例回答的結論正確。`；原譯 `But that does not prove the conclusion of the example answer is correct.` | `But this does not prove the example's conclusion is right.`（58 字元） | PASS。保留「尚不能證明」的否定、範例與結論；沒有改成已證明錯誤。原 `source_hash=88168f8c5bdd` 完全不變。 |
| en `ci113` | `先挑最影響別人決定的那一句。`；原譯 `Pick the sentence that could most affect someone else's decision.` | `Start with the claim that most affects others' decisions.`（57 字元） | PASS。保留優先選取、對他人決策的影響與最高優先級。以 claim 表達可查核的一句主張符合上下文。原 `source_hash=72c74e4e8bc9` 完全不變。 |
| ja `ci055` | `這次示範以我們開啟頁面的日期為準。`；原譯 `この例は、私たちがページを開いた日を基準にしています。` | `今回は、私たちがページを開いた日が基準です。`（22 字元） | PASS。自然ですます體；維持本次示範與「我們開啟頁面之日」，没有稱為文件更新日或今日。原 `source_hash=ddfad4729082` 完全不變。 |

原生實際首次字幕輸出 `20261007T092434Z-draft-captions.log` 報 en `ci025` 20.6 CPS、en `ci113` 21.2 CPS（上限 20），ja `ci055` 8.6 CPS（上限 8）。主操作者套用後的 `20261007T092539Z-draft-captions.exit.json` 記錄 `09:25:39.047636Z` 開始、`09:25:39.985675Z` exit 0；日誌列出 zh-TW/en/ja/ko/zh-CN，沒有速度問題。這是未核准的本機 draft 工作目錄，字幕使用原旁白時間，不是翻譯配音時間。

本覆核另獨立讀取實際 SRT，呼叫原生 `parseSrt` 與 `checkCues`：en 143、ja 144、ko 148、zh-CN 143 cues，四語問題均為空陣列。原生字幕 manifest 亦記錄繁中 143 cues、五語零問題。沒有執行重製字幕、付費請求或音訊檢查。

| 檔案 | 原件 SHA-256 | 三處縮短後、全文修正前 SHA-256 |
| --- | --- | --- |
| `i18n/en.json` | `1379e0965bdbb7462d745c3a45ade6e36606c1d3a5c281517e0ab8f2d3491601` | `dcae6f1038cc661eff31629bb7a934a39c71b9a53629ebdfbbd6df6f049731af`（20,029 bytes） |
| `i18n/ja.json` | `bb09d2efea494ce1b2404b06acff45c700e21a7621ba879efcf3a4635adcb3bc` | `d986eadfed3e899946e9b0c13c9c709b716d71c1e636351e5b479f092ca94c5a`（22,163 bytes） |
| `captions/en.srt`（draft） | — | `8921e94fabbb70caff91057d3cb5ea4bf2ff3543db7d1ce6ddba848234a0b85b` |
| `captions/ja.srt`（draft） | — | `85eeed3227ba5a58e05c622330150b27d635736bad6f11e16b1d1a77fb738781` |

逐物件比對確認英文只有 `ci025`、`ci113` 的 text 改變，日文只有 `ci055` 的 text 改變；所有 source_hash、標題、說明、tags、章節與其他欄位完全相同。另兩語原件完全相同。143 個各語 source_hash 都與現行繁中原生 textHash 相符，無缺句或孤立 ID。

現行 `video.json` SHA 為 `c1e01a5a8797445bd147606ad8ae87427c9adb9aa0f57a959474d30a01b968b0`（24,669 bytes）。它因先前視覺編排而異於首次整檔 SHA；這三處字幕修正未改繁中來源文字或任何來源 hash，不將視覺整檔變更描述成來源整檔未變。未核准的字幕 manifest `speech_hash=399237f659e75fc5`。後續全文修正後的實際翻譯檔 SHA 由另份完整審稿釘選；上表保留三處修正當時的歷史證據。

**結論：這三處字幕縮短 ready，0 項需修正。** 本結論只屬該三句，不給予全語言、翻譯縮圖、dub、音訊、最終影片、owner language selection 或 API language-gate approval。

## 全文修正後的三句再核對

`2026-10-07T09:40:01.853Z` 再讀現行檔案，確認上述三句及 source_hash 完全不變。另八處全文修正已由主操作者套用，其內容與釘選由完整審稿另記。三句當前原生 CPS 為 en `ci025` 16.29、en `ci113` 18.26、ja `ci055` 6.84；均在各語上限內。現行 SRT 全文與原生純函式重建的文字、開始及結束時間逐 cue 相同，五語零問題。

現行 en 檔 SHA 為 `d3fa6fe0ec97cec0b13ed2ac381c78796e7ad57fb1010df964ac5d0c670abd24`（20,037 bytes），ja 為 `b4e506bdac60e6d60e75b3df42e0cf1c5fdde4c0fc122260dec3b6ccf2ab816e`（22,187 bytes）；現行 en SRT SHA 為 `91455c8a0e23fc611679fd513581c617192ebd0188981c27bf219fdf1cfecd06`，ja SRT 為 `0b587a8d12323ddb5d07cd8aa9048b0c6699ac15207efe335a3736db70bcd00c`。這些是全文修正後的檔案身分，不覆寫上表的歷史釘選。

`09:47:27.355Z` 最後重綁時，源稿整檔因兩個 verdict 移入 title 第二行而為 `ba96bc7d5d1cc5d6fd20172064baefabd2bb319b00ba67387b02b4e90c5e3423`。獨立確認 143 個繁中文字／source_hash 及 voice／chapters／metadata／sources／縮圖不變，三句翻譯與字幕亦不變。最新 source＋metadata draft 的完整釘選見四語審稿；三句 ready 的限定範圍保持不變。
