# S62 R10｜最後一輪兩句澄清提案

2026-10-22 UTC。**只提案，未套用或重錄；全片 listener 改詞第 2／2 輪。**R9 改詞的新音訊已處理完其餘旗標，當前僅 `s62041`、`s62097` 仍被 Jev 標記；這兩句此前只用原措辭初錄及兩次重錄，尚未改詞。本票不另開更多輪數，不宣稱我聽過原音，也不把含義相同的轉寫說成已證實唸錯。

| ID | 原句 → 唯一候選 | 理由及保留界線 |
| --- | --- | --- |
| `s62041` | 回到開場那夜：他想核對木星是否真的走錯，卻拿不到九日的新位置。下次會是什麼隊形？<br>→ **開場那個夜晚，他想核對木星是否真的走錯，卻因滿天雲層，無法觀測九日的新位置。下次會是什麼隊形？** | 當前 heard 只加「一」成「那一夜」，其餘意義完整，屬非實質差異，不能因此宣稱發音錯誤。協調者要求為發表清晰度改寫，故直接指明開場那個夜晚，將既有雲遮、無觀測位置的關係說清楚；保留明確開場回呼、九日、木星與隊形問句，不改成當晚實際測得新位置。 |
| `s62097` | 二月二十八日，一夜裡仍有小點在木星近旁出現。<br>→ **二月二十八日當晚，仍有小點在木星近旁出現。** | 現在 heard 為「二月二十八日，翌夜裡仍……」，翌夜可能被理解為下一晚。當晚把觀測綁回同一日期；不改二月二十八日、木星、近旁光點或其數量未在本句列出的狀態，也不宣稱整晚持續看見。 |

## 固定原文核對

直接重開 `/tmp/curio-s62-sidereal.txt`，SHA-256 `74fc9b817b64bc33415c6a44100c30f48952bc531d380682e5f4f1a26cc56fb5`，即 GITenberg commit `6672b6c62a0f30e9bb9b84410ef48c6698c37ea5` 的 Carlos 1880 英譯。候選不把編者說明當觀測者原話。

- `s62041` 的 claims [G04 L1294–1309](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt#L1294-L1309)：一月八日觀測位置換邊後，他疑木星走得不合天文學家計算，急等下一夜，但 `the sky was covered with clouds in every direction`。這支持九日雲遮而無法核對新位置；候選只明示原本既有的阻擋原因。開場回呼是稿件結構提示，後半問句仍停在下一次隊形未知，不加結果。
- `s62097` 的 claims [G12 L1727–1765](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt#L1727-L1765)：L1758 起為 `Feb. 28: 1 h.`，L1763 又記同條目的第五時辰新點。是二月二十八日當晚的觀測，不是二十九日晚；當晚不把它誤移一天。

提案快照：video SHA-256 `a82374eb8b6762908e847730895db6c960b04eef0e6ef6652b24bb967f629131`，script `572bbb5066df994cf3ad36a567f76c97095aff47066cf43babefaf929edd5198`，claims `6b9a942e57ab35406024b1278f82fbbebed935c73381c46515aedb33d209afe0`；旗標 `708b61e86fd86dd1aad5920130724d8cc54aade6ac8dae33f62a30af07173f3b`，check `a01ce38265de6389ae549fe346a49dffdb668684f2d4f1933b41c8b6da84d290`。雜湊只記讀到的版次，不是稿件或音訊核准。

若採用，協調者應同步兩列 claims／script、重跑 lint、新來源差分覆核與敘事盲讀，再在目前第 2／2 輪內只重錄這兩個 ID、跑 check-audio，並重算正文時間軸。仍有旗標就保留給音訊審核，不透過另取 R11 名稱重設輪數。沒有 video/script/claims、媒體或 Git 操作。
