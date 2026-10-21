# S23 Short 1 第三版獨立史料預檢：PASS

- 查核日：2026-10-20 UTC
- 精確對象：`shorts.json` SHA-256 `d1a21eaf4fd28bf881d4fd06461a3874d505cdd9c64f4dec5b610402db9f9e9c`
- 結論：**史料與書面畫面 PASS**。這只核准腳本進入重建；新語音、成片與上架品管須另驗。

第三版只改 `turn` 旁白為「測試成績達標，哈里森仍沒當場拿到整筆獎金。」我直接對讀固定版 1765 年法案第 40 頁：第 49–55 行承認哈里森時計的航試偏差「did not lose its Longitude beyond ten Geographical Miles」，同頁列最高獎的三十地理英里級距；第 111–137 行把 £20,000 分兩半，首半仍取決於公開原理與移交時計，後半仍取決於同類時計製成並測試。因此「成績達標」指精度，「沒當場拿到整筆獎金」指新法案的分期條件，沒有聲稱議會已支付或未支付某一半的確切金額。`hs041` 的兩段不同長度絲帶只是抽象比較，無假數字或付款收據。

其餘六拍重核：hook 的「不超過十海里」符合 *beyond ten* 的包含邊界，說明欄保留原文地理英里；setup 的 £20,000／約三十海里為法案追述的最高級距；proof 的公開原理、交出時計及再製同類時計與第 57–67、93–137 行相符；payoff 的 1773 年法案第 111–117 行授權支付「not exceeding £8,750, as a further Reward」，旁白與字卡均用「授權」；loop 沒有從追加授權反推兩半原獎各付多少。六張選鏡只用無字法案、金幣、色帶、鐘錶匠、文件示意，不冒充 H4 機芯或原始公文。標題、說明與兩條固定法案連結仍與前版同義，沒有新增未查主張。

`from-episode --slug curio-s23 --workdir /workspace/.video-work --check` 退出碼 0：`1 Shorts valid; every keyframe matches its hash`。六拍依序且只產一支 Curio Short。本次未修改作者腳本，也未呼叫付費語音、影像或站台發布服務。

對讀材料：`/tmp/s23-1714-90.txt`（固定 1765 年法案第 40 頁）、`/tmp/s23-ruffhead-882.txt`（固定 1773 年法案第 882 頁）、本集 `research.md`、`claims.md`、`video.json`、前兩次獨立預檢與目前 `shorts.json`。
