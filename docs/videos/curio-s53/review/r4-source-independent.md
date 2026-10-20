# S53 R4｜固定來源與書面畫面獨立覆核：兩處限縮 HOLD

2026-10-20 UTC。R4 的 **129 句口播、129 列主張之史實內容 PASS**，R3 指出的兩處直接來源問題已修；整份五檔來源／畫面包仍 **HOLD**，因 `research.md` 的 F07 保留一處過寬簡述，且 `s53021` 書面插圖與事件時序相反。本報告只審固定文字與畫面提示詞；不代表雙人盲讀、政策、生成插圖、配音或成片放行。

## 固定對象與重新開源

| R4 檔案 | 本次 SHA-256 |
| --- | --- |
| `brief.md` | `b029ee451bfad26fe9cd03463ccd8e4a6b2d6cf01d6248b9b6ae4b405051bbc8` |
| `research.md` | `048f181b8dd93705550c074c8e1cce5121b3af2f0b1a677767e01b7af4b20d84` |
| `claims.md` | `f8be9d38935c5e6512bc14ad19842ac9e6b9347570d05b6fa3e0cd60f05b91db` |
| `video.json` | `e271691db8c0dac4d70c4e5ef3aa5878c2f9ba2549975a7699134ea0bff70088` |
| `script.md` | `5783416b22cce59b8fa0acfbfe24fac1a539094c697e5ec67950077917ea9ba2` |

我從固定提交的 raw URL 重新下載兩份全文至 `/tmp/s53-r4-relief.txt`、`/tmp/s53-r4-calamity.txt`（僅本次暫存），核得 [R：1913 年救濟調查](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt) SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`、[C：1906 年新聞編書](https://github.com/GITenberg/The-San-Francisco-Calamity-by-Earthquake-and-Fire_1560/blob/7720f6008349283e7a5e72d2cd52ebfbd4b9b815/1560-0.txt) SHA-256 `4f001abb09f44aa630059d2325de55bd8f88d8304fa21ce97322d57e0fa3213c`，均與研究表相同。R 為 1913 年編纂調查、包含 1908 年訪查，不是 1907 年現場錄音；C 仍未作 R4 口播的獨立定量證據。`claims.md` 137 個連結均指向固定 R 全文，所列範圍未超出原檔行數。

## R3 退回點與 R4 史料結果

- `s53011` 現直接連 [R L4250–4264](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4250-L4264)：原文記地震後第一夜，人們在公共廣場、公園、空地暫住。旁白「許多失去住處的人，先在公園與廣場暫住」未超出此處。**修復 PASS。**
- `s53095` 現寫「帶孩子的寡婦，以及家中主要工作者失能的家庭」，主張列亦同；[R L5011–5016](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L5011-L5016) 正是 *widows with children* 與 *families having incapacitated breadwinners*，並記慈善機構替兩類家庭搬修小屋。該景只畫匿名援助者拿無字資料夾。**旁白／主張／書面畫面修復 PASS。**
- R4 新增的買地分期 `s53112a` 每月 8–25 美元、`s53114a` 有人月付幾乎只抵利息，均見 [R L11000–11013](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L11000-L11013)。它們只限 680 個較完整訪查家庭中買地者，不是小屋原擬租金。`s53116`→`s53117`→`s53129`→`s53130` 的地租問答把報告另知的 23 件扣屋放在 **457 個未取得完整紀錄地址**這邊，原文 [R L10502–10520](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10502-L10520) 明確區分 1,137／680／457 與那 23 件；R4 未把 23 當 680 樣本或全市比例。`s53038`–`s53043` 的 1907-03-19 完工與 08-17 暫用期限相隔不足五個月，見 [R L10450–10460](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10450-L10460) 和 [R L4934–4941](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4934-L4941)。
- 全稿仍分清 5,610 **各官方營地建成**、5,343 **搬出營地**、1,137 **試尋地址**、680 **較完整訪查**、457 **未得完整紀錄**、70／680 **買地**、7／70 **付清**與失訪部分已知的 23 **地租扣屋**；來源不明分母的 558／82% 未入旁白、卡片或說明欄。沒有把公園委員會的「不干預」寫成正式授權，也沒有憑來源補造搬屋機械。

## 兩處限縮 HOLD 與最小修法

1. `research.md` F07 寫「Associated Charities 曾替**寡婦**和失能家庭等搬修部分小屋」，仍省掉來源 [R L5011–5016](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L5011-L5016) 的 **with children**。雖然口播和 `claims.md` 已修，研究表的「目前可採主張」仍顯得包含所有寡婦。請改成「帶孩子的寡婦及主要工作者失能家庭」；不需改口播。
2. `s53021` 接在 `s53020` 的 **1906-08-01** 建屋計畫公布後、`s53028` 的 **09-10** 開工前；[R L4852–4865](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4852-L4865) 明定當時只是公布建屋計畫，09-10 才開工、09-16 漢密爾頓廣場首批 20 棟才完成。該景 prompt `at a public square after the 1906 fire ... before a row of plain cottages` 會把尚未蓋好的小屋排進 8 月場景，與來源時序相反。可只改成一位職員在帳棚旁看無字公地圖，例如 `Wide shot at a public square in August 1906, an anonymous clerk studies an unmarked land plan beside a plain canvas tent, mild overcast light`。不要在提示詞寫「before cottage construction」之類會反而叫模型畫小屋的字。旁白和主張不用改。

其餘逐景畫面是無字小屋、地塊、錢幣、文件或人員做單一可辨動作；沒有用可讀假通知、特定家庭個案、卡車／輪子／滑木等無據搬屋機械，也未把 5,610 全畫成金門公園一處。`video.json` 是七章、127 景（119 插圖、7 數字卡、1 片尾）；正文插圖比例 **119／126 = 94.44%**，卡片沒有連續超限。**129／129** 旁白與 `claims.md` 按 ID／文字／順序相同；`screenplay(doc)` 與 `script.md` 逐位元相同；16 條 `loops` 有效；`lint --slug curio-s53 --json` **0 errors／0 warnings**。作者快估開場 41.10–50.67 秒、正文最快 8:18.67，仍須以實際 TTS 驗證。企劃列明濃縮開場後 5 秒片頭、21 秒片尾及末 16 秒雙推薦與訂閱的位置，`video.json` 的說明欄有兩份固定原文和頻道 URL；本輪尚無相應媒體或 Studio 可點連結。

**下一步：**只修 F07 與 `s53021` prompt，固定新的五檔雜湊後換人核差分。若 129 句口播字串未變，R4 兩位新盲讀的劇本雜湊可沿用；在史料／書面畫面重新 PASS 前，不啟動政策、配音、插圖或成片。
