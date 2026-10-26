# 公開安全收據索引

[index.json](index.json)只列實際存在的source／查核／靜態樣本／授權摘要與其bytes、SHA，不代表伺服器核准或媒體完成。個別收據的source與scope優先；歷史verify1的REVISE及raw/native答案保持原文。

索引不收錄自己、production-progress.json、result.md、validation.json或documentation-freeze.json，避免循環雜湊。最終documentation-freeze.json另列這批文件身份並排除自己。原episode-source-manifest.json維持266檔歷史source freeze，不覆寫成目前整棵樹的manifest。

[current-source-gates.json](current-source-gates.json)只在讀到root實際normal pending、native local approve及TTS dry-run收據後更新。後臺pending不是遠端核准，本地採用不是使用者UI點擊，dry-run不是付費合成。

[tts-deferral.json](tts-deferral.json)是root的排程暫緩與跨片既有證據安全摘要；不含raw transport／pairing／憑證，也不聲稱已獨查provider帳單。第五目前TTS0，不更換provider／voice或全局設定。

[native-description-compose.json](native-description-compose.json)記錄原生metadata純組字結果：沒有自動產生本片GitHub教材URL。相對教材檔案可在checkout開啟；公開URL需root首commit／push／PR後另GET驗證，不先填入source。
