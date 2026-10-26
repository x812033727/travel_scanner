# DuckDB2.0：八語文字已採用，媒體尚未製作

繁中來源仍為[video.json](video.json)40eb，speech38cf、[script.md](script.md)7aac；八種外語的111句、六章、完整標題說明／tags與縮圖詞均經作者及root全量文字審查，再由正常原生`i18n-merge`採用。**這是8/8本地文字，不是八語CC／配音交付。** 繁中master paid TTS0／raw0／actual timeline無，M4A、fit／meter／ASR、全片與後台交付尚未完成。

| 語言 | 句／章 | 當前i18n SHA-256 | 證據 |
| --- | --- | --- | --- |
| en | 111／6 | `faf5cb2f1c7fd536e012cd2a8191062ee4069d42ef46b8b8fbf8f10543f2cf4b` | [採用收據](localization/en/actual-native-text-adoption.json) |
| ja | 111／6 | `324c6f070993c1fc1b08f18d5f9131527eb24278e8ff4f200dfb63c6db4b83f2` | [採用收據](localization/ja/actual-native-text-adoption.json) |
| ko | 111／6 | `6b1e38d9b3e868a5cf312a1cb0180f88b43d5741aad0bb1959f9e9d0f8738d0f` | [採用收據](localization/ko/actual-native-text-adoption.json) |
| es | 111／6 | `2e8511e2456cf75c6455f205fcf6105613a5b867995ccd6079490b0349afa60c` | [採用收據](localization/es/actual-native-text-adoption.json) |
| pt | 111／6 | `f0696f7449489eb4c8536a0501fd24afed155ae0b6531c46e15c3181b84d3b07` | [採用收據](localization/pt/actual-native-text-adoption.json) |
| id | 111／6 | `1eefbda5e5253f143c0a4d27b9eca3d08453e28464ea688705b1773d3e7c9988` | [採用收據](localization/id/actual-native-text-adoption.json) |
| vi | 111／6 | `e9a22e9d92c524a6c492f97088913b7285f3c6ce28467c12b2d8125fa1002428` | [採用收據](localization/vi/actual-native-text-adoption.json) |
| th | 111／6 | `0af06dff9045602f026526516e3d7d10c1c689effa9c06c1a5d57d8eb257d544` | [採用收據](localization/th/actual-native-text-adoption.json) |

[當前進度](production-progress.json)、[全八語文字摘要](localization/all8/actual-all8-text-adoption-summary.json)、[當前收據索引](receipts/all8-text-adoption-index.json)及[本輪檢查](receipts/all8-text-adoption-validation.json)分列範圍。PT／ID／TH的原採用批次當時只達文字7/8，保持原文；VI另有真實completion後才成立8/8。所有root review中的before-merge狀態與作者REVISE／validator錯誤也保持歷史，不倒改成功。

這支以1,200筆原創虛構配送資料，區分40列預覽／1,160列省略與明確條件選出的480筆完整交付；`>=`變式720筆包含240筆剛好準時。完整[可攜教材](public-run/README.md)、[SQL](public-run/demo/followup.sql)、[需求變式](public-run/demo/variant.sql)、[26,889B ZIP](duckdb-public-fixtures.zip)與[公開GET查核收據](receipts/fifth-public-artifacts-verification.json)保留。這是同一DuckDB2.0.0、確定性作者操作；不是AI模型／效能／token／成本評測。原創教材CC0-1.0、DuckDB MIT與官方來源權利分開。

[verify4](verify-4.md)只核metadata公開連結delta與既有21項固定證據連續性，不冒稱今日重新live查所有官方事實。兩份[敘事原始結果](narrative-r2/)仍各12/13 false，root教學取捨與[本地採用](reviews/script-local-adoption.json)不等同server批准。官方5秒片頭／21秒片尾素材已取得，但第五尚未套用成片；不把其他片的scoped recovery當成本片paid放行。

本輪只封存[五份可變文件與三份ES描述檔](history/before-all8-text-adoption-docs/identity.json)，舊ES68可由63份原位＋5份快照精確重建，以Git `a090b585a674db0f1e0f2ef12771363bfa7596eb` 保留全部556份舊檔；不遞迴複製history。原[ES284索引](receipts/es-text-adoption-index.json)與更早資料保持原文。新196份proof均有[exact copy identity](localization/all8/copy-identity.json)，PT正確閱讀入口為[corrected.md](localization/pt/author/source-target-complete-111.final.corrected.md)，舊錯標籤Markdown及inverse proof照存。

PR1861維持[no-auto-merge](https://github.com/x812033727/travel_scanner/pull/1861)。本輪不呼叫API／paid／ASR／媒體，不改source、claims、voice、lexicon、data或任何已採用target；只準備精確freeze供root審查，未stage／commit／push，不merge／deploy／上傳YouTube，也不開第六題。
