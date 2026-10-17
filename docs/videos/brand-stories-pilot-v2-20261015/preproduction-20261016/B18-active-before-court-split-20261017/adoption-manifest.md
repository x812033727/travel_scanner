# B18 法院 PDF 分源接入前備份

2026-10-17。本目錄保存接入新版來源審稿資料列前的本機原始位元組，不是正式機快照。

| 原本的本機檔案 | 備份檔案 | SHA-256 |
| --- | --- | --- |
| `episodes/B18.json` | `B18.json` | `209fb773139e96afd5a56f373b6f0843eca902f81b374c19bcd9bc8a4d78e3dd` |
| `episodes/reviews/B18.json` | `B18-review.json` | `124b4bea3e08a14e5402370c678b8d53d7f61c6180db5e80c6d4aeff52278114` |
| `stories.json` | `stories.json` | `07a71fc18c3aa12d426dcc1c9ecd30e59c150079a1e83d868b7024c09670c999` |

三個來源與備份檔各自的 SHA-256 在替換前逐一相同。新 B18 資料列 SHA-256 為 `9a8ceabd48c6970cd654c077ab33499d070fbbcf5eca4e078e5777a12f99dc9b`；獨立收據已正規化為 LF，SHA-256 為 `d61ff84d1f91a25787727d625e9c04cbbb31803b95f4658e2eb8669061d19b85`，只綁 canonical story SHA-256 `7a598d16c9efcd9014f3554531dfe5569408cbeb1f90fdfbff4b0975e5`。新版雙集 `stories.json` SHA-256 為 `ac1dbde239039f722c902e48dbde7b0ed0d1f628d3ba6b8f57afaef53248bd54`；編譯前後 A01 序列化資料列完全相同、兩列後端 `check_story_file` 零問題／拒絕／忽略。

作者隔離候選的 15 檔 manifest SHA-256 `87d9ee2fafe2b579dad9dd496391e31d5db585054abf89da380edfd345b959f4`；[獨立審查](../B18-court-pdf-split-candidate-20261017/independent-review-20261017.md)與新收據另存。新 B18 `must_verify[4]` 只引用法院 PDF，編譯列的 `reviewer_only` 僅此一筆；65 筆場景主張仍全部 `UNCHECKED`。本次只接入本機套件，沒有正式匯入、付費服務、配音、插畫或成片。
