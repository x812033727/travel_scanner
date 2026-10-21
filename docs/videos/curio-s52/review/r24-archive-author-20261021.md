# S52 R24｜收到尋獲船舶消息的單景修正

2026-10-21 UTC。 [R23 非作者覆核](r23-lighting-independent-20261021.md)確認八景光線修正均符合 Cook 6 月 3 日晴朗日誌，但在全 113 景抽查發現未改的 `s52014` 把碼頭工人、貨箱和整艘船同時放進**室內檔案室**，因此仍 HOLD 擴畫。我只改 `s52014.data.prompt`：檔案室裡一名匿名文員把無字帆船素描放在密封消息旁的木講台上，示意**1768 年 4 月 3 日皇家學會得知找到船**，不畫船真的停在室內或當日碼頭裝貨。素描、講台、消息信函是概念道具，沒有宣稱是原件照片、原文信函或特定人的肖像。[Kippis 後出敘述 L598–624](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L598-L624)是該句旁白的來源層級。

[一葉結構化差分](r24-archive-structured-diff.json)證明把此新字串換回舊值即逐位元恢復 R23 `video.json` SHA-256 **`86f9b98339a6e29b73446709ebb923f323e77277076a698c718952df725acd81`**；R24 現檔 SHA-256 **`cf3211e99155afd7cd71c715f6c6fd6055c43975a3a20e199b4582dda6f13677`**，唯一 JSON 葉差是 `scenes[13].data.prompt`。brief／research／claims／script、115 句音檔、其他 112 景、R22 兩格已收原生圖均未改。`visualHash=7f8b312bafc0755a`、`speechHash=2af0a08f6e592b5d`；lint 0 errors／0 warnings。

私有 `STOP` 仍在，ledger **US$0.0675**（5 image、5 judge），既定 **US$4.46** 上限不變。請非作者對本句與固定來源、室內構圖及精確差分做獨立覆核；即使 PASS，也須由工具實際確認兩格舊圖可按逐景 request／judge 原樣沿用，再分批看新原生圖。此作者回條沒有買圖、核准整集分鏡或代替站主聽審。
