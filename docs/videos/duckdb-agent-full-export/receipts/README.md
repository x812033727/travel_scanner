# 公開安全收據索引

[index.json](index.json)只列實際存在的source／查核／靜態樣本／授權摘要與其bytes、SHA，不代表伺服器核准或媒體完成。個別收據的source與scope優先；歷史verify1的REVISE及raw/native答案保持原文。

索引不收錄自己、production-progress.json、result.md、validation.json或documentation-freeze.json，避免循環雜湊。最終documentation-freeze.json另列這批文件身份並排除自己。原episode-source-manifest.json維持266檔歷史source freeze，不覆寫成目前整棵樹的manifest。

[current-source-gates.json](current-source-gates.json)只在讀到root實際normal pending、native local approve及TTS dry-run收據後更新。後臺pending不是遠端核准，本地採用不是使用者UI點擊，dry-run不是付費合成。

[tts-deferral.json](tts-deferral.json)是root的排程暫緩與跨片既有證據安全摘要；不含raw transport／pairing／憑證，也不聲稱已獨查provider帳單。第五目前TTS0，不更換provider／voice或全局設定。

[native-description-compose.json](native-description-compose.json)保留補連結前原生metadata純組字結果：工具沒有自動產生本片GitHub教材URL。首push後root已GET公開CSV／ZIP，本次才手動追加兩條immutable教材URL；新的檢查另列下方，舊收據未改。

## 已公開教材的metadata追加

[fifth-public-artifacts-verification.json](fifth-public-artifacts-verification.json)是root於首push後實際unauthenticated streamed GET的安全proof：CSV與42-entry ZIP均200，bytes／SHA逐一匹配本地；不是音訊／影片下載proof，也未單獨GET資料夾頁。

[metadata-public-links-delta.json](metadata-public-links-delta.json)、[原生metadata檢查](metadata-public-links-native-checks.json)、[新索引](metadata-public-links-index.json)與[新freeze](metadata-public-links-freeze.json)記這次唯一description追加。舊index／compose／gate／validation／freeze收據保持原文與當時source身份；新source等待root獨立verify4與重新綁定。script重新生成SHA仍7aac…107b，不能宣稱新server核准。

## root獨立verify4後的當前綁定

[verify4報告](../verify-4.md)及[完整JSON](../reviews/fifth-verify-4.json)為root實際獨立PASS，綁source40eb與21項不變依賴連續性；新[current-source-gates.verify4.json](current-source-gates.verify4.json)保留原pending readback與local adoption的時刻／script SHA，沒有新核准。舊[current-source-gates.json](current-source-gates.json)、metadata index／freeze不覆寫。

prepared17檔及author freeze的[逐bytes封存](../history/before-root-verify4-adoption/identity.json)另列身份，原68份reviews保持SHA。[當前索引](root-verify4-adoption-index.json)不收自己／mutable progress／validation／freeze以免循環；[文件驗證](root-verify4-adoption-validation.json)和[新freeze](root-verify4-adoption-freeze.json)各自明列範圍。

[首次呼叫診斷](root-verify4-initial-invocation-diagnostic.json)記root先用錯estimateTimeline參數，在寫報告前失敗；原stderr保留tool session，不捏造raw檔。修正後的真實報告才是PASS；本輪沒有重新live GET、付費TTS／ASR、媒體或server核准。


## 英文文字採用索引

EN文字採用時使用[en-text-adoption-index.json](en-text-adoption-index.json)，原[verify4索引](root-verify4-adoption-index.json)、[metadata準備freeze](metadata-public-links-freeze.json)與所有舊紀錄不改。新增[EN實際native採用](../localization/en/actual-native-text-adoption.json)只涵蓋111targets／六章／metadata／縮圖詞的本地文字；不是CC檔、M4A、fit、ASR或後台交付。作者原26freeze、第一個pass3期望錯誤、root獨立逐句審查與真native merge log各自保留範圍；原生估時文字限制不代表音訊PASS。更新前doc／task／index及兩個舊freeze在[archive](../history/before-EN-text-adoption-docs/identity.json)有精確bytes／SHA。


## 當前EN＋JA文字2/8

當前使用[ja-text-adoption-index.json](ja-text-adoption-index.json)。[JA真實採用](../localization/ja/actual-native-text-adoption.json)綁root逐句獨審、正常merge exit0與actual JA file SHA；[當前驗證](ja-text-adoption-validation.json)核對原325檔、前一輪35檔及其[精確封存](../history/before-JA-text-adoption-docs/identity.json)。舊EN index／freeze與所有舊審查保持原文。

JA作者初次URL抽取錯誤、root sheetTodo型別與freeze結構錯誤的診斷和原腳本各自保存，不混作ASR、音訊或native品質關卡失敗；JA作者純merge／compose無時間軸，root正常CLI merge才構成當前文字採用。文字2/8不是actual CC／M4A／fit／ASR／後台交付，繁中paid TTS及raw仍0。


## KO正常文字採用後：EN＋JA＋KO 3/8

當前另用[ko-text-adoption-index.json](ko-text-adoption-index.json)，舊JA171及更早31／61／90索引原位不改。[KO實際採用](../localization/ko/actual-native-text-adoption.json)綁root全111獨審、兩行／description白話修訂、真正常merge exit0與actual KO6b1e；[root完整delta](../localization/ko/root/root-wording-delta.json)不改109句或source/context，不是音訊重寫回合。作者21freeze＋root收據都有[exact copy proof](../localization/ko/copy-identity.json)，作者舊preview與root已採用版本分開保存。

[五檔增量封存及舊88重建](../history/before-KO-text-adoption-docs/identity.json)使用0d885 Git anchor，83未變舊檔留原位，沒有再複製遞迴history。[當前驗證](ko-text-adoption-validation.json)記source／glossary／native lint／tasks／連結與hash。文字3/8不是實際字幕、M4A、fit或後台交付；master paid TTS0／raw0／actual timeline無，兩份敘事12/13 false保持原文。新freeze另列精確proposal，未stage／commit／push。
