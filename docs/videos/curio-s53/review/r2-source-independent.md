# S53 R2｜逐句史料與書面畫面獨立覆核

2026-10-20 UTC。**HOLD：作者凍結的 R2 稿尚不能進入媒體製作。** 本次獨立重開兩份固定文字，逐句讀過 135 句、125 張插圖提示詞、7 張數字卡及片尾；主要統計與樣本界線正確，但開場訪查時間、建屋因果、結語地租及兩張畫面的年代需要修正。這是固定稿的史料／書面畫面審核，不是盲讀、站主核准或成片驗收。

## 固定對象與方法

| 對象 | 本次獨立核對 SHA-256 |
| --- | --- |
| [brief.md](../brief.md) | `b029ee451bfad26fe9cd03463ccd8e4a6b2d6cf01d6248b9b6ae4b405051bbc8` |
| [research.md](../research.md) | `048f181b8dd93705550c074c8e1cce5121b3af2f0b1a677767e01b7af4b20d84` |
| [claims.md](../claims.md) | `f0a96554ec6da45b96c6c4521c8cbb2d0823d94e2d6182c9d31037cd4dc89de1` |
| [video.json](../video.json) | `80d7ac1c1c156691634bdd0a492d234e5ca169a4a3825959d97bc5bdb9c25f9c` |
| [script.md](../script.md) | `b8fba10ed2e143eb677aaf389bb2c4d088cf7ecda8e376386788afe198852df4` |
| [R：1913 年救濟調查固定全文](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt) | `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72` |
| [C：1906 年新聞編書固定全文](https://github.com/GITenberg/The-San-Francisco-Calamity-by-Earthquake-and-Fire_1560/blob/7720f6008349283e7a5e72d2cd52ebfbd4b9b815/1560-0.txt) | `4f001abb09f44aa630059d2325de55bd8f88d8304fa21ce97322d57e0fa3213c` |

R、C 均從上述固定提交的 raw URL 另行下載（HTTP 200），不是以作者摘錄或原有暫存 clone 代讀。R 是參與救濟者編纂的 1913 年調查，住房篇採 1908 年訪查及機構紀錄；C 的金門公園段是編書所收匿名敘述，僅能有歸屬地使用。`claims.md` 的 135 行 ID／文字與 `video.json` 135 句逐字相符，CLI 生成的 `script.md` 135 句亦相符；135 句中只有頻道邀請 `s53999` 無史料連結，合理。全部史料連結均指向上述兩個固定提交。

## 必修項

1. **`s53008` 開場時間錯置，並連帶修畫面。** 開場從「一九〇七年六月」接「**幾個月後**，訪查員……」，但訪查直到 **1908 年 8 月**才開始，距 1907 年 6 月約 14 個月；見 [R L10185–10200](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10185-L10200)。改為「隔年八月」或「一年多後」。該景 prompt 仍標 `public square in 1907`，卻畫訪查員；作為未來預告，請把畫面標成 1908 年訪查場景。
2. **`s53027`→`s53028` 暗示未證成的施工先後與因果。** R 說木材與刨木廠不足，另說 1906 年 9 月 10 日動工；沒有說「先建好兩座刨木廠，工程才真正開動」。見 [R L10244–10260](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10244-L10260)及 [R L4848–4870](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4848-L4870)。保留供料困難和開工日期，但不要把兩者剪成「等刨木廠建好才開工」。
3. **`s53997` 結語把地租說成搬屋必然後果。** R 說許多住戶須付地租，也說 680 個受訪家庭中有 70 戶買地；見 [R L10497–10505](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10497-L10505)及 [R L10997–11021](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10997-L11021)。「新地租卻會按月再來」宜改成「若搬到租地，仍要按月付地租」；`outro.data.lines` 的「土地仍要付」也宜按同一界線收窄。
4. **兩張提示詞的時間／場所互相矛盾。** `s53070` 一面寫 `public square in 1907`，一面畫研究員在檔案室翻 **1913 年報告**；可直接改成 1913 年檔案室的概念畫面。`s53082` 旁白是 Lobos Square **1908 年 6 月 30 日**才結束，prompt 卻寫 `public square in 1907` 並安排關閉營地大門。改成 1908 年的示意景；[R L4983–4997](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4983-L4997)沒有記載一扇大門，可用空出的營地位置替代。

## 同輪應收窄的主張及提示詞

- `s53002` 在開場首次講清場要求時直接當作當年原件敘述，約五分鐘後的 `s53070` 才交代「1913 年調查記載」。目前只有 R 這份後編調查可重開；首次提及就加簡短歸屬，避免畫面或口播使人以為已核對公園委員會原件。[R L4983–4990](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4983-L4990)。
- `s53054` 的「後來」使原擬 4／6 美元租金聽似在早期租約之後才提出；R 只提供原擬租金和後來法律形式改為買賣契約，沒有這個細分順序。`s53058` 的「文件換了名字」又把實質買賣義務說得過輕。可說「原擬二房每月四美元、三房六美元；市有地收租受阻後，改用分期買賣小屋契約」。[R L4899–4932](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4899-L4932)、[R L10482–10500](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10482-L10500)。
- `s53095` 應精確說「家中主要工作者失能的家庭」，對齊 R 的 *incapacitated breadwinners*，不要說成整戶都失去工作能力。[R L5010–5024](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L5010-L5024)。`s53099`「隔年的訪查員」緊接 1908 年 6 月營地結束與跨年慈善工作，也容易聽成 1909 年；改稱「一九〇八年的訪查員」。
- `claims.md` 的 `s53019` 只引建屋日期段，沒有給材料／工人困難的直接證據；補引 [R L10244–10260](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10244-L10260)。`s53093`–`s53094` 只引搬家費段，買地／地主問題應補引 [R L10997–11021](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10997-L11021)。
- `s53033` 的「交鑰匙牌」、`s53123` 的「乾的室內水龍頭」都不是 R 所記載的分配或缺水形態。前者可畫營地管理員對照空白分配表，後者可畫室外水栓與未接管的小屋，避免暗示未證成的道具細節。R 只說小屋由營地管理員分配，及約四成受訪小屋接水管、其餘從附近水栓取水：[R L4887–4897](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4887-L4897)、[R L10915–10930](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10915-L10930)。

## 其餘逐句結果與製作條件

| 範圍 | 核對結果 |
| --- | --- |
| `s53001`–`s53009` | 1907 清場與購屋懸念可由 R 支持；`s53008` 日期錯誤、`s53002` 歸屬待補。 |
| `s53010`–`s53047` | 災後、C 的有歸屬尋人告示、建屋物料、9 月動工、5,610 棟及二／三房數可支持；`s53027` 因果及 `s53019` 引證待修。C 的「九成帳棚」與「數千」未進口播。 |
| `s53048`–`s53083` | 早期租約／最後買賣契約、公園委員會無正式准許權、1907 年清場要求、延遲與少數驅離、Lobos Square 1908 年結束均與 R 符合；`s53054`／`s53058` 用語及 `s53070`／`s53082` 畫面待修。 |
| `s53084`–`s53109` | 5,343 是搬出小屋；12.50–25 美元是搬家公司常見費用，不是機械方法；1,137 是嘗試尋訪的搬屋地址，680 是較完整紀錄，457 未得完整紀錄。`s53095`、`s53099` 及兩行引證待收窄。 |
| `s53110`–`s53132` | 70／680 買地、7／70 付清、約七成共地、約四成接水管等都限於訪查樣本。23 起地主取屋緊接在 **457 個未得完整紀錄**的敘述後，卡片標「失訪部分已知」且旁白 `s53130`–`s53132` 明講界線；沒有把 23 算入 680 或外推發生率。`s53123` 道具待修。原文有歧義的 558／82% 未進口播、卡片或片尾。 |
| `s53997`–`s53999` | 無下集點名；結尾可收在土地與費用，但 `s53997` 須加租地條件。 |

125 張 `shot` 的提示詞都有內容；絕大多數是無名人物、空白文件及停放小屋的原創概念畫，未發明搬屋用的車輪、滑木、卡車或起重設備，也沒有可讀假契約或具名家庭。七張數字卡的 5,610、5,343、680、457、70／680、7／70、23 各有清楚標籤；125／132 張正文畫面為插圖，最長連續數字卡一張。

獨立執行 `node tools/video/cli.mjs lint --slug curio-s53 --json`：**0 errors／0 warnings**。按工具估值，開場 250／325 CPM 分別 **47.77／38.87 秒**，符合 30–60 秒；第一章後到 `outro` 前正文 **625.70／510.60 秒**，快估仍逾 8 分鐘。這是文字估值，還沒有 TTS 實測。`youtube.description` 含 R、C 固定全文與頻道 URL；R、C 可下載，但本環境連 YouTube 頻道時得到 CONNECT 403，故不能從本機證明頻道頁可開。

本機候選片頭／片尾的 SHA-256 分別為 `a5ae205fcf6fa7c92998ac4991225e54206fff482cf03493a60cfb2519e8fcef`、`275475470f1b7b5d93a2948f561d6e300d0406f9a5b2ab17cfb0dfe4bb3f34ee`；`ffprobe` 分別見 1920×1080／30 fps／150 格 5 秒與 630 格 21 秒。抽看片尾第 10 秒，有兩個推薦影片框與訂閱圓框；最後 16 秒的可點元件仍須私人上傳後在 Studio 安裝、儲存及點測。`video.json` 尚無成片或影片 ID，不能把候選素材視為本集已合成。

**下一關：**作者修改後重做五檔 exact-hash 凍結；另一位工作者核改動行和提示詞、重跑 lint 與開場估時，再進兩位新讀者盲評。此輪 HOLD 不核准付費 TTS、插圖、配樂或站台／YouTube 動作。任務票的 scope 只有 `docs/videos/curio-s53`，本覆核未改票、作者稿或 `video.json`。
