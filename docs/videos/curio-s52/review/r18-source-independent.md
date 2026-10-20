# S52 R18｜獨立史料與書面畫面覆核

2026-10-20 UTC。**史料 PASS；116／116 主張與口播對齊 PASS；書面畫面 PASS。**此裁決只綁下列 R18 五檔。兩名 R18 新讀者、語音及實際生成插圖須另行驗收。

| 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `3463fced92403975e91bb624216370f9e56ac603348336c037929f4084efc5df` |
| `research.md` | `644adc7e538ca85fe1e1b6e274293b7cc39c54c8bd94b0e8decb5466072b038a` |
| `claims.md` | `edd53a0d74cf3508308211d5cdc272c5f6050c16f9fcbf49a92b734daf233a1a` |
| `video.json` | `43dcfe719f5b0a30f743d6b93d42bfb4447ad85072b4685398567c37948c5906` |
| `script.md` | `1a5d07020b2f15555f3359d31ecf6d90c6f8cb4780c8d3159e4c7cc2544d6857` |

## 固定原文重新對讀

直接重讀 `/tmp/curio-s52-sources/` 的固定全文並重新算 SHA-256：[庫克日誌的 1893 年轉錄](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt) `c00d08c12188eaf17d8f631e22e5b36882af8f5f6ee0bfe469e8601d9b8cf536`、[Kippis 後出庫克傳記](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt) `c723fd1d180efb3c55e783fc156018741cb9bc7b1402c3a490f50a65b31f9956`、[1771 年皇家學會原報的 OCR 轉錄](https://github.com/markjhill/2025-helsinki_cascade/blob/2ac861600a431e8cb2e2eae3b1cdcd33b7350207/data/rsc/Royal_Society_Corpus_open_v6.0_texts_txt/Royal_Society_Corpus_open_v6.0_text_106113.txt) `d7b32ca98aadd3a652748091eabc1c1ff329ed5e6df51498fbb5d20ff6b21a74`。庫克正文是當事人視角但經後編，Kippis 是後出敘述，原報此份是 OCR；未把三份誤當三次獨立觀測或用損壞的數字欄算秒差。

| R18 差分 | 原文與判定 |
| --- | --- |
| `s52005` | [Kippis L598–624](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L598-L624)明載皇家學會呈請國王派船，讓選定觀測者去看 1769 年凌日；[Cook 編者前言 L790–803](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L790-L803)把目的解釋為改善日地距離估算。新問句只問「為什麼派船追這一刻」，後文有此答案；不再要求稿中未提供的南太平洋選址獨有理由。**PASS**。 |
| 刪 `s52109` | [庫克 6 月 3 日日誌 L5963–5975](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5963-L5975)同時說完整看見凌日、暗影干擾接觸讀時與三人差距。保留的 `s52084`、`s52102–07` 分別承載這兩層事實；刪重述沒有刪去必要史實或導致下一個倍率問題無據。**PASS**。 |
| 刪 `s52306` | [Kippis L1165–1182](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1165-L1182)的四格表明指 Green；[原報 L140–163](https://github.com/markjhill/2025-helsinki_cascade/blob/2ac861600a431e8cb2e2eae3b1cdcd33b7350207/data/rsc/Royal_Society_Corpus_open_v6.0_texts_txt/Royal_Society_Corpus_open_v6.0_text_106113.txt#L140-L163)仍分列 Cook 與 Solander。保留的 `s52118` 說明傳記表的界限，`s52121–22` 直接查原報並給新資料；刪「傳記未轉錄全部記錄」沒有掩蓋原報存在。**PASS**。 |
| 刪 `s52324` | [原報 L150–163](https://github.com/markjhill/2025-helsinki_cascade/blob/2ac861600a431e8cb2e2eae3b1cdcd33b7350207/data/rsc/Royal_Society_Corpus_open_v6.0_texts_txt/Royal_Society_Corpus_open_v6.0_text_106113.txt#L150-L163)對亮線漸斷、幾秒不確定及離開時邊緣難辨有明確敘述；保留的 `s52320–23` 逐項說出，刪掉概括性末句後，`s52123` 自然轉去外派兩隊。**PASS**。 |
| `s52127–28` | [庫克 6 月 4 日日誌 L5977–5982](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5977-L5982)只記觀測者當晚「帶著成功返回」，不列逐人接觸時刻；1771 原報 OCR 的 342 行中，Green／Cook／Solander 本站觀測各有一段，外派觀測者只在 L160 概述，未見兩隊逐人的四次接觸表。新 `s52128` 分開說這兩份文字各缺什麼，限縮範圍，沒有說其他全部史料不存在；`s52127` 保持 R17 的清晰口語。**PASS**。 |

## 差分、畫面與長度

以目前 `video.json` 逆改 `s52005`／`s52128`、從已追蹤舊檔按原順序補回三景，再把 `s52306`／`s52324` 換成 R16 凍結新句，重算的 JSON SHA-256 **恰為 R17 `ba6896e5a95caf1dee4e653702b036c0bc14340857dcb93ad08e97510b7e757c`**。因此 R17→R18 的 `video.json` 差分確實只有作者所列兩句與三個刪景，沒有暗改提示詞、運鏡、章名、21 組伏筆或片尾。留下的 111 個 `shot`、2 個 `big` 卡和 1 個 `outro` 仍沿用已核的書面畫面；特別覆核 `s52005` 空白請願書概念圖與新問句相符、`s52128` 兩欄空白外派記時圖沒有假造具體數字。這是**提示詞**檢查，不代表圖片已生成、通過評審或可以當史料照片。

逐字比較 `screenplay(video.json)` 與 `script.md`：完全相同。`video.json` 的 116 個 `lines[].id/text` 依序與 `claims.md` 的 116 列逐字相符；ID 唯一。`lint --slug curio-s52 --json`：0 errors、0 warnings。按 `estimateTimeline(..., 325)` 重算，第一章開場 **35.63 秒**、正文第二章至片尾前 **488.93 秒＝8:08.93**；這是最快文字估時，R18 語音長度與對時仍未驗證。

**剩餘關卡：**兩名新隔離讀者與正式敘事 OR；通過後才合成新版或刪句後的音訊，跑全篇 `check-audio`。R16／R17 舊 WAV 與時間軸不可代替 R18 結果。圖片評審與配樂的網站本月額度亦未恢復，沒有實際圖片或成片。
