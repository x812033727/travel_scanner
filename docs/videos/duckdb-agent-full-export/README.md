# DuckDB2.0：視覺元件與22份附件已驗證，音訊及正式成片待完成

截至2026-10-27T09:56:16.602807+00:00，64張原生圖卡與繁中加八語共9張JPEG縮圖已實際製作並逐張驗收；同一待審SCRIPT已附22份視覺元件，正常完整下載及獨立bytes／SHA查核完成。[當前進度](production-progress.json)、[實際元件索引](receipts/visual-components/index.json)與[完整下載證據](receipts/visual-components/normal_full22_proof.json)分列範圍。

22份為9張縮圖、聯絡表、9份完整原始標題說明草稿TXT、原生frames manifest、誠實元件報告及128秒無旁白視覺樣片。64張真實圖卡依稿件順序各停2秒，這是檢閱速度，並非實測旁白或章節時間；沒有把樣片當成正式成片，也沒有ZIP或64張PNG後台交付宣稱。

繁中paid TTS0／raw0，actual audio timeline與CC尚無；八語已驗M4A仍0/8，fit／meter／ASR、正式語言包、至少480秒正文、正式成片及完整QA仍待完成。原生靜態字標不等於官方5秒片頭／21秒片尾，本片尚未套用動畫bookends。

當前來源[video.json](video.json)SHA `1c475c928a02a6f584dd224ecfed1c5fafd53aa4bf1795c7a3758699692a12c8`；只刪除4張卡片被裁切的可選重複title，相同文字保留於key。正常快取render重用60張並重畫4張，原64張實看中的4項裁切失敗、4張替換圖的真實複審，以及初次native0／outer1縮圖失敗均完整保留。[視覺delta](receipts/visual-components/source-visual-delta.json)也記錄ES／PT／ID／VI四個縮圖短標的正常metadata merge；111句完整line objects、全部八語targets與完整metadata不變。

[script.md](script.md)仍為7aac，既有SCRIPT `dd47b9a0-6456-4651-9456-32b320909338`仍pending；新增附件不構成server／UI批准。40eb的verify4及source-gates保持原來源綁定；兩份原生敘事結果仍各12/13 false，教學取捨不改raw失敗或門檻。

| 語言 | 當前i18n SHA-256 | 範圍 |
| --- | --- | --- |
| en | `faf5cb2f1c7fd536e012cd2a8191062ee4069d42ef46b8b8fbf8f10543f2cf4b` | 111句／六章／完整metadata；CC及M4A未完成 |
| ja | `324c6f070993c1fc1b08f18d5f9131527eb24278e8ff4f200dfb63c6db4b83f2` | 111句／六章／完整metadata；CC及M4A未完成 |
| ko | `6b1e38d9b3e868a5cf312a1cb0180f88b43d5741aad0bb1959f9e9d0f8738d0f` | 111句／六章／完整metadata；CC及M4A未完成 |
| es | `61cf0a0077d9cf9fd3b93d8117bf3975dc162a982acc981213af6789e1889b9c` | 111句／六章／完整metadata；CC及M4A未完成 |
| pt | `43dc7e4434394fb72def2921db8a4201d32d0b66bac73a8deaab146407b5db6e` | 111句／六章／完整metadata；CC及M4A未完成 |
| id | `a71014a6452b76e081f276bd6cf628015c1d4a1cfbc9e04bda6ebc4975ce262a` | 111句／六章／完整metadata；CC及M4A未完成 |
| vi | `198c81025f5164c9c8e2d2e9ff821743674342f14a90a0c10691485967b68623` | 111句／六章／完整metadata；CC及M4A未完成 |
| th | `0af06dff9045602f026526516e3d7d10c1c689effa9c06c1a5d57d8eb257d544` | 111句／六章／完整metadata；CC及M4A未完成 |

原創1,200筆配送教材、480筆完整條件交付與720筆需求變式，見[可攜教材](public-run/README.md)；公開CSV／ZIP的既有200／SHA證據保持。

五份原始摘要已[逐bytes封存](history/before-visual-components-docs/identity.json)，舊索引／freeze保持原位，未遞迴複製history。本次公開proof只含明確審查過的文字／JSON／真實log，不含媒體、私有project、credentials、profile或release。PR1861維持no-auto-merge；本票尚未done，責任與原branch／PR1861延續；未merge／deploy／上傳YouTube。
