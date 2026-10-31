# S50 R4｜研究統計界線獨立差分覆核

2026-10-20 UTC。**研究註解窄修 PASS；[R4 來源覆核](r4-source-independent.md)唯一的研究欄 HOLD 可解除。**我未參與 R4 改稿或這次研究句子修正，直接重讀固定 1667 年刊本 A，再比對原本及現行 `research.md`。此裁決只覆核這一行的文本歸屬，不將尚不可直連的 Gazette／London Museum 升為原頁查核，也不代替劇本雙盲、生成圖驗收或網站關卡。

固定 A `/tmp/curio-s50-A63385/A63385.xml` SHA-256 `0a4b379b932fc331c9ff10bd217e6d8b2cc513388a3fd73d7f64f0b35447595e`，與研究檔所釘版本一致。[A L153–164](https://github.com/textcreationpartnership/A63385/blob/4ac29739d661a1c7f2a34f51ffb8a1811176f146/A63385.xml#L153-L164) 同段明列城牆內燒毀 373 acres、城牆外燒毀 63 acres 3 roods、**城牆內未燒 75 acres 3 roods**，及燒毀房屋 13,200 棟。因此舊句「未計沒有燒到的城區」與原文矛盾；新句「測量員同段列出燒毀房屋數、燒損面積及城牆內未燒面積；13,200 不是全倫敦房屋總數」同時守住三種統計量與房屋數界線，**PASS**。刊本說數字如測量員印出，這裡的「同段列出」是指刊本的同一段，不推論測量的現場路線或時間。

我以 Git 基線與現行檔案逐行比較：`research.md` **恰有一個邊界段落的一句替換**，前半句（Pepys、Farriner、Vincent 來源層級）完全相同，其餘檔案不因本次修正而變。原 `research.md` SHA-256 `109557d74963733a6b8b3715739d49ec1d68648f5f34a7c9e10d52a9f940e6c7`；現版如下。

| 凍結內容 | SHA-256 |
| --- | --- |
| `brief.md` | `60040a61dcf7b2b4b62bba30773537d4c559104724a7f6d83926082211d983e1` |
| `research.md`（差分 PASS） | `27f9df563ab8376d2f6ee10837772821534515fd29b86b7e83e259eb56023a95` |
| `claims.md` | `41ebfffe54f72c0fda9f1fd563d90613efb2dbb6757e2d49a8f2e832558b4805` |
| `script.md` | `81766925948a74b1915ae86754e1ca01db1c187c3cdd092d73970e2137435e23` |
| `video.json` | `0fa7b40caee68e8d475827ca551d14b15eac14d7f85fec68c0497cd4f80d7a1f` |

R4 三句旁白與書面畫面已有獨立 PASS；本次只解除來源包中這一個研究註解的 HOLD。`fire037` 與 `fire108` 仍只按倉庫 P17 已有查核標層級，當前代理對 Gazette／Museum 原頁仍為 CONNECT 403。R4 的新 **script-only** 雙盲敘事尚待完成；沒有 TTS、插圖、配樂或成片可宣稱通過。
