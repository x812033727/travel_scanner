# S57 R3｜獨立史料與書面畫面覆核

2026-10-20 UTC。**HOLD：二月補給段的事件先後顛倒。**本報只審下表固定 R3 五檔的史料、逐句主張、書面畫面與前後時序；未參與作者修稿，未把 [R2 的來源 PASS](r2-source-independent.md)沿用為 R3 判定。敘事雙盲、政策、實際插圖、語音、配樂及成片各有後續關卡；本次沒有呼叫付費媒體服務，也沒有改創作檔。

| 固定檔 | SHA-256 |
| --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `7a68ed10261086ba13dbf1a85a87932eb8ad8a81723874c6abeb0df8490fe657` |
| `claims.md` | `0f7e8278ac3482b79bd9013d29c187940f99869794f1fe7c241071511459c262` |
| `video.json` | `698b29027e4b57523d62e7bda8210e5f2dfc5910a6a1b2507f156fdd3b6088a0` |
| `script.md` | `afc30e64b439c4d3ea783ab6a47b57f63b8c73c34ece00e85b3a4b46281c71f7` |

## 固定版本與逐句覆核

重新從固定 commit 取得 [S：史丹利《How I Found Livingstone》電子節錄本](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt)與 [L：Waller 1874 年身後編刊《最後日記》第二卷](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt)。原始文字 SHA-256 分別重算為 S `de84c2eb2089e18c8e080fe24ecac95c44c1cc993be355987cdd3221036d158f`、L `e6658569be045054c89e59c2aac9819a430a9a84fbdbed289a2ba0fa27750962`。S 書名頁明示 *Abridged*；L 是身後編刊文字而非已校勘親筆手稿；下列 L/S 行號均為固定電子檔行號。

[R3 作者完整差異](r3-author-diff.patch)涵蓋 **24 個景 ID**：`s57001` 是只改章名；其餘 **23 句**改口播與主張列，其中 **14 景**另改 prompt；一個 `loops` 的 payoff 指向新章首。逐一讀完五檔並核對這些差異：`video.json` 有 189 個唯一景 ID，`claims.md` 與 `script.md` 各 189 列／句，**189／189 口播逐字一致**。`claims.md` 的 217 個固定來源連結涵蓋 45 個不同檔名、commit、行號範圍組合，均指向上述兩份原文且落在原文行數內。連結形式與存在不代替事件時序判讀。

## 阻擋點：布包找回被放到較早的補給之前

| 口播與企劃位置 | 固定原文 | 判讀 |
| --- | --- | --- |
| `s57137`「幾天後，日記記：追問下有人拿出一包藏起的布。」畫面是已找回的布包；`s57139` 才說「新的援助終於交到李文斯頓手上」；`s57142` 再說藥箱在「隔天」收到。[brief.md](../brief.md)第七章亦按「找回一包布 → 新的援助」敘述。 | L 在 [5783–5794](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5783-L5794) 先記失貨及有人「想起」可能藏起的布；**2 月 18 日**已記史丹利給新物資 [L5796–5804](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5796-L5804)；**2 月 19 日**收藥箱與藥品 [L5806–5810](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5806-L5810)；直到**2 月 20 日**追問後才記有人拿出藏在 Thani 貨中的布包 [L5812–5818](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5812-L5818)。 | **HOLD。** `s57137` 的「拿出」與已找回布包畫面對應 20 日，不能以前段 18 日的「想起」當作它早已被拿出的證據。接著把 18 日新援助寫成「終於交到」的後續，又讓 19 日藥箱變成那之後的「隔天」，使觀眾按倒序理解。應按 18→19→20 日重新排事件，或在口播清楚標明回溯，並同步修 brief、claims、prompt 與 loops 後另凍結。 |

## 其餘 R3 差異的史料與畫面結果

- `s57004` 的開場問句與五道封印可由 [L5873–5881](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5873-L5881) 支持，未提前口播選擇的答案。`s57094` 說**打算**次日往盧辛加，與 [L5317–5335](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5317-L5335) 的未來式相符；新的村路 prompt 不畫成已抵達。
- `s57134` 問布包能否找回、`s57137` 歸屬於日記記述，均未替失貨指控定罪；兩景的倉庫／布包為可愛插圖示意。`s57139–s57150` 單句所說援助、布、船、藥箱、等待史丹利從海岸送非奴隸人手，見 [L5796–5810](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5796-L5810)；`s57140` 把船與未完成水路計畫相連是已在 claims 標明的詮釋，計畫本身見 [L5769–5777](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5769-L5777)，沒有說路線已走完。這些單句來源成立，**不消除上述排法造成的日期錯置**。
- `s57163–s57165` 把章尾問題接到 3 月 13 日完成給 Bennett 的信；[L5864–5881](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5864-L5881) 明記 13 日信件、公文及 14 日託交封好的日記。改後問題／章首答案有直接時序和文書對應，新的寫信／折信 prompt 不冒充可讀原件。`loops` 的 `s57164 → s57165` 亦對得上。
- `s57169–s57173` 的行李、早餐與 5 點／8 點，由 [S14360–14373](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L14360-L14373) 支持。史丹利說自己心事重吃不下，只說同行者**似乎**沒胃口；R3 保留此觀察視角，早餐碗及人物 prompt 沒替李文斯頓添加心理原因。這些細節仍只有 S 的出版回憶，`s57173` 也作了歸屬。
- 14 個改動的 prompt 均為原創示意且未引入可讀假文書、精確未走路線或只由兩位歐洲人完成的隊伍；**`s57137` 的已找回布包畫面須隨上述時序修訂一同重看**。系列實際生成圖的畫風與事實一致性未在書面階段宣稱通過。

未改的核心史料界線仍成立：[S9305–9307](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L9305-L9307) 稱相遇為 11 月 10 日，[L5252–5260](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5252-L5260) 有斜體圓括號 10 月 28 日，片中只稱「1871 年晚秋」；著名招呼只歸屬 S；勸歸和選擇續行兩本皆述，但完整對白只在 S；尼羅河源是李文斯頓當時的信念；1873 年死亡消息是卷尾追述與編者整理，不冒稱本人最後日記。這些界線不能因 R2 PASS 或 lint 綠燈略去。

## 檢查與交接

`node tools/video/cli.mjs lint --slug curio-s57 --json`：**0 errors／0 warnings**，189 句、14.58 分鐘估算。`npm run test:docs-videos`：**236 pass／0 fail**。`npm run check:tasks`：exit 0，僅印既有無關 stale／scope 警告。這些檢查不判斷歷史時序。修好二月段並重新凍結五檔後，應對新 SHA 重新作獨立來源／書面畫面覆核；本 R3 HOLD 不作媒體放行。
