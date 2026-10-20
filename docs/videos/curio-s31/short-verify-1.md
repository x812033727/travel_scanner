# S31 單支 Short：京師是終點，來路仍缺

2026-10-20 零付費前製。長片的精確 `script.md`／`video.json`／`claims.md` SHA-256 分別是 `8bad325d15b9ab6ba512330c8f9e8e4f3c14c64550730a16020f27fac332c623`、`0b5e8dcc054c880127e49efd0ec0dd58f86f77c0a50530f2e094b2b8d0fbe762`、`ddbdd532bdc1b688c7b0ce432213021021120c84c9bc6cc652321622097948f1`。本集 [shorts.json](shorts.json) SHA-256 `d42b7fdcc8d0803f36e903ef209955b1eeabaa555697c9357cc901e23cd8e3f9`，只含 `curio-s31-short-1` 一支 `from-episode` 候選。文稿由本次撰寫者對照已核長片及固定原文自查；**不是獨立來源審查或已完成的 Short**。

| 短片景 | 長片插圖鏡位 | 來源與界線 |
| --- | --- | --- |
| hook、loop | `ly004` | 杜牧《過華清宮絕句》的一騎是詩的畫面，不當作確定驛路或同一匹馬跑完全程。 |
| setup | `ly031` | 將杜牧詩與**另一本**《新唐書·楊貴妃傳》分開；後者記 `騎傳送`。 |
| turn、proof | `ly034`、`ly037` | 貴妃傳寫 `走數千里，味未變已至京師`，沒列接力站、出發果園或逐日路程。 |
| proof | `ly049` | 《新唐書·禮樂志》生日新曲只記 `南方進荔枝`，未把這批果子接到傳記的騎傳。插圖畫樂廳，不假造果籃。 |
| proof | `ly083` | 白居易描述巴峽荔枝是另一時代、另一段文字，不能指定為貴妃那一籃。 |
| payoff | `ly093` | 研究桌上的空白路線只標京師這個已述到達點，不畫不知的來源線。 |

固定數位轉錄與本地重開全文雜湊：杜牧 [原詩](https://github.com/garychowcmu/daizhigev20/blob/4a6d6f2088825f132521d848c2ea86cf9c9a7620/%E9%9B%86%E8%97%8F/%E5%9B%9B%E5%BA%93%E5%88%AB%E9%9B%86/%E6%A8%8A%E5%B7%9D%E6%96%87%E9%9B%86.txt#L257-L263) `/tmp/curio-s31-fanchuan.txt` SHA-256 `f6a2c78a1da55168b03e7556ac4a57c7c7f64c74b63ffe4af2d56558cceb42d1`；《新唐書》[貴妃傳](https://github.com/garychowcmu/daizhigev20/blob/4a6d6f2088825f132521d848c2ea86cf9c9a7620/%E5%8F%B2%E8%97%8F/%E6%AD%A3%E5%8F%B2/%E6%96%B0%E5%94%90%E4%B9%A6.txt#L10103)及[禮樂志](https://github.com/garychowcmu/daizhigev20/blob/4a6d6f2088825f132521d848c2ea86cf9c9a7620/%E5%8F%B2%E8%97%8F/%E6%AD%A3%E5%8F%B2/%E6%96%B0%E5%94%90%E4%B9%A6.txt#L1015) `/tmp/curio-s31-newtang.txt` SHA-256 `c9b7a46b1f4f1c3950c40a5e4b30f3ccb3bfd19acd2d638d38359d0db7f5f559`；白居易[原序](https://github.com/garychowcmu/daizhigev20/blob/4a6d6f2088825f132521d848c2ea86cf9c9a7620/%E9%9B%86%E8%97%8F/%E5%9B%9B%E5%BA%93%E5%88%AB%E9%9B%86/%E7%99%BD%E6%B0%8F%E9%95%BF%E5%BA%86%E9%9B%86.txt#L6047-L6048) `/tmp/curio-s31-baiji.txt` SHA-256 `6074f3b5cc14e45b4c1c18edfddd7ec814709038f8351bb7cbcde17b66ddbb81`。轉錄不等於原件掃描；詩、後出史書、後來植物描寫也不是一張共同貨單。

格式預檢：Short `validate`、Curio 單支 `episodeShortsProblems`、六拍 `scriptGrammarProblems` 均 **0 問題**；8 景、8 句、136 個含標點字元，第一張 headline 7 字，最長一句 19 字。估約 34–42 秒，正式須以頻道聲線實測 25–55 秒。無來源影片 YouTube ID，Short 說明欄未填占位連結；離線 metadata 只報「長片尚無網址」，其他字數／標籤檢查通過。

`from-episode --check` 目前以 `no keyframes/manifest.json` 停止：S31 尚未購買插圖，故沒有選定影格或 9:16 實際裁切可審。待長片音訊／圖片與成片關卡完成後，用**最新選圖雜湊**重跑、檢視原尺寸與直式安全區，再製作旁白、字幕、QA 與上傳包。此草稿沒有呼叫 TTS、生圖、配樂、網站送審或 YouTube 上傳。
