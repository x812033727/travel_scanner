# S53 R5｜固定史料與書面畫面獨立覆核：PASS／PASS

2026-10-20 UTC。本輪只審 R5 五檔的史實、逐句主張與尚未生成的畫面提示詞。**來源 PASS、書面畫面 PASS**；不等於雙人盲讀、政策、實際插圖、配音、成片或 YouTube 審核通過。

## 固定對象與原文

| R5 檔案 | 本次 SHA-256 |
| --- | --- |
| `brief.md` | `8e44f47693dd75ad0a7509ab0f495c06adcc2e614b8c8bc09a51559d7202a27c` |
| `research.md` | `2e61530c650852281402476041175154ee69c414daf7431d6aa0db352e7c3d22` |
| `claims.md` | `6a0a1f315fb21baeec5665d0996a97be17b62239b1f72abe5ca93a3b26dab5a5` |
| `video.json` | `2d9e0036e03712028890b4c9af01d776f13394baabefb7cb389b8bb6b6c28f1d` |
| `script.md` | `5f944532562e9e6072efe08cd8d1e3c4caa64f380d4497adccf276df50f3a07d` |

我重新開啟固定 Git 提交 `dabb1ee570c9d5d5992d7eda7aafe215ce025567` 的 [1913 年 *San Francisco Relief Survey*](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt)，其全文 SHA-256 為 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`；另核固定提交 `7720f6008349283e7a5e72d2cd52ebfbd4b9b815` 的 [1906 年新聞編書](https://github.com/GITenberg/The-San-Francisco-Calamity-by-Earthquake-and-Fire_1560/blob/7720f6008349283e7a5e72d2cd52ebfbd4b9b815/1560-0.txt)，全文 SHA-256 `4f001abb09f44aa630059d2325de55bd8f88d8304fa21ce97322d57e0fa3213c`。兩份與 `research.md` 的固定檔雜湊相符。R 是事後編纂調查，C 未被拿來證明本版口播的數字。

## R4 HOLD 兩處及 R5 差分

| 項目 | 原文與 R5 檢查 | 結論 |
| --- | --- | --- |
| F07／`s53095` | R [L5011–5016](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L5011-L5016) 的 *widows with children*、*families having incapacitated breadwinners*；研究 F07 現寫「帶孩子的寡婦及家中主要工作者失能的家庭」，與仍未改動的旁白、主張同範圍。 | **PASS** |
| `s53021` 插圖 | R [L4852–4865](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4852-L4865) 記 1906-08-01 只公布建屋計畫、09-10 才開工；現提示詞為八月廣場旁的帳棚與職員查看**無字土地圖**，不再畫尚未建成的小屋。 | **PASS** |
| `s53004`／`s53006` | R [L10482–10500](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10482-L10500) 的月繳款與契約，及 [L4972–4994](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4972-L4994) 的遷屋困難，容許概括有住戶仍未找到安放小屋之處；新版用疑問句留待 `s53057`–`s53059` 才交代分期買賣契約。無具名家庭或私人當日心聲。 | **PASS** |
| `s53009`、`s53025` | R [L4250–4264](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4250-L4264) 記第一夜居民在廣場、公園等暫住；[L4934–4941](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4934-L4941) 明說公園委員會無正式授權權限，只同意不干預一年。R5 沒有寫成正式准許。 | **PASS** |
| `s53033`、`s53069`–`s53071` | R [L4887–4897](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4887-L4897) 先把小屋分給官方營地住戶；[L4972–4994](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4972-L4994) 記先證明買／租到新地才准自費搬屋、1907 年六月要求八月清空及 Lobos Square 延到 1908 年。新的開章答句、各處公園廣場與未如期清空均在此範圍；無字分屋、地圖、契約示意未冒充原件。 | **PASS** |

刪除的 `s53026`、`s53072` 已不在 `video.json`、`claims.md` 或 `script.md`；其餘提示詞仍是匿名成人、無字文件、普通小屋與地塊，不補造搬屋機械。各數字母體仍分開：5,610 建屋、5,343 遷屋、1,137 嘗試地址、680 較完整記錄、457 未取得、70／680 買地、7／70 付清、另知 23 起地租扣屋；未將 23 放入 680，也未在正片使用原文分母不明的 558／82%。

## 機械一致性與邊界

`video.json` 有 125 景：117 個插圖 `shot`、7 個 `stats` 卡、1 個 `outro`；**127／127** 口播與 `claims.md` 逐 ID、字串、順序相同，`screenplay(doc)` 與 `script.md` 逐位元相同。`claims.md` 的 134 個固定原文連結全指向該 R 提交、檔名及有效行範圍；16 條 `loops` 保留；`lint --slug curio-s53 --json` 為 **0 errors／0 warnings**。企劃與說明欄保留濃縮開場、5 秒片頭、21 秒片尾／末 16 秒雙推薦及訂閱位置、固定來源和頻道連結。這些僅為文字規劃，實際時長與可點連結仍待製作及 Studio 驗收。

非阻斷編輯註記：`s53004` 的 `claims.md` 一列僅列月繳款所依的 K 段；到期後安放小屋的不確定性由同一固定原文 H 段補足。後續整理逐句索引時可把 H 段也列在該列，不需改口播。`research.md` 底部仍留 R2「135 句」舊交接文字，R5 的當前準確數字由本報告與凍結檔的 127 句表示。

**後續關卡：**兩位未讀 R5 稿的讀者只看同一版 `script.md` 各自完成 13 題盲評並依系列規則合併；其後再跑政策／站台腳本、真實 TTS ≥8 分鐘與圖、動畫、成片驗收。本輪沒有付費或發布。
