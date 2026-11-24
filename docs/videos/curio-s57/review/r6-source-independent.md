# S57 R6｜獨立史料與書面畫面覆核

2026-10-20 UTC。**史料／逐句主張 PASS；書面畫面 HOLD 一景（`s57150`）。** 本結論只涵蓋下列五檔 R6 凍結稿。我沒有參與 R6 撰寫，沒有更動創作檔、產圖、合成語音、送站台審核或代替站主核准。R5 的[來源書面覆核](r5-source-independent.md)曾 PASS，但不移轉到 R6；本次重查 R5→R6 [逐行差異](r6-author-diff.patch)、全部 R6 場景／主張表與兩份固定版原文。

| 檔案 | R6 SHA-256 |
| --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `48f287375b22a77929130046c15c55079c78d9376996a033709dc7a1d625b933` |
| `claims.md` | `71b0f3405bd254e7be0d464d34d81c98fb78b08951e046b331ec79a34af03919` |
| `video.json` | `e766dbe4ac40932abfa5bea1a89713604b2fbb64158bf3523376bde0aa0131cc` |
| `script.md` | `f2d8c42f6b71698121199d7c3c26ddde958eddf1d25be96783356c8ef404ef87` |

## 固定原文與新句

重新下載 [S：史丹利《How I Found Livingstone》出版節錄本](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt)，原文 SHA-256 `de84c2eb2089e18c8e080fe24ecac95c44c1cc993be355987cdd3221036d158f`；[L：Waller 1874 身後編刊《最後日記》第二卷](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt)，原文 SHA-256 `e6658569be045054c89e59c2aac9819a430a9a84fbdbed289a2ba0fa27750962`。S 的編本註明節錄，L 的末段死訊經編者整理；行號是這兩個固定電子文字的行號，不能當手稿頁碼。

| R6 位置 | 獨立查核 |
| --- | --- |
| `s57101`、`s57104`、`s57106` | [L5420–5430](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5420-L5430)依次記 1871 年 12 月 13 日史丹利在烏吉吉收到美國領事 Webb 的信、亞丁電報至 4 月 29 日、15 日李文斯頓準備向東取貨。[S12363–12384](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L12363-L12384)另記領事在尚吉巴、信內有電報；兩本對電報起點／截至日期的描述不同。口播採 L 的亞丁與四月概稱，不混寫成兩份原文共證的精確電報內容；「從海岸」有 S 的尚吉巴位置支持。三句按 13→15 日順序，並保留李沒有自己的同類信件這一情境。 |
| 刪 `s57082`、`s57119`、`s57152`、`s57158` | 刪句不增史實。前後文仍維持早期勸歸、東行、李的舊箱和史丹利的新援助為不同階段；刪掉 `s57119` 也避開原稿「4 日日記回述前夜獨木舟離開」容易被畫成 4 日當下啟航的風險。[L5482–5499](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5482-L5499)仍支持立旗與人員到齊的相鄰橋接。 |
| `s57149`、`s57150`、`s57151` | [L5796–5804](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5796-L5804)明列史丹利新給的布、船等補給；李文斯頓說要等**史丹利從海岸派來非奴隸人手**才繼續工作。新三句分別說明貨已到而人未到、由誰安排、非奴隸限制；沒有把計畫說成已派到。這是當事人日記中的用詞，畫面不能由此推定任何被畫人物的身份。 |
| `s57189` | [L5741–5769](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5741-L5769)同時記他拒絕返家、先完成水源考察的判斷及其當時的尼羅河水源假說。[L5873–5881](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5873-L5881)記 1872 年 3 月 14 日把封好的日記交史丹利。R6 結句明指「回看」開場，不把地理假說當今日定論，也不再重述人與日記分路。 |

全稿的高風險順序再核：[L5783–5818](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5783-L5818)在 **2 月 18 日**先列史丹利新援助、**19 日**列藥箱與藥品、**20 日**才記有人拿出先前藏起的布包；拿出後仍缺 **436½ 碼**。`s57137–s57144` 維持這個次序和新舊兩批貨的區別，沒有將失貨指控獨立判罪。[S9305–9307](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L9305-L9307)與 [L5252–5263](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5252-L5263)仍對精確相遇日有分歧，片中只用季節／年份。1873 年去世時間仍以[L 身後編刊的早五月及編者推斷](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L10254-L10275)表述，不硬定五月一日。

機械對齊：**167** 個唯一 scene、**167** 個 claims 列、**167** 個 script 標記按 ID 與旁白文字逐一相同；`claims.md` 有 **192** 個指向 S／L 固定提交的來源連結，擷取的行範圍均有效。這個對齊檢查不能代替上面的語義覆核。

## 書面畫面停點

**`s57150` HOLD。** 新 prompt 是 `Two shot, elderly traveler discusses transport for helpers with young reporter beside blank luggage tags, Unyanyembe supply camp, no readable text`。它要求兩個人在同一畫面互動，與 [Curio 既定提示詞規格](../../../../.agents/skills/curio-episode/SKILL.md)和[系列畫面指南](../../history-curiosity/look.md)的「一個主體做一個動作」直接相反；MiniMax 對多人互動曾有錯主體與多餘人物的實測問題。單論史料，它沒有錯置日期或宣稱人手已到，但不能當通過系列書面畫面門檻的同版 prompt。作者可只改這一景，改為單一人物的一個動作，仍示意史丹利準備從海岸安排人手，而不畫出人手已抵達；例如一位年輕記者在營地把一個**素面**行李包合上。這只是修法界線，不代作者採入或核准新 `visualHash`。改後須以新五檔雜湊和新畫面雜湊做窄幅獨立差分；若旁白不變，來源判定可按不變文字核對。

其餘新 prompt 沒有已知的來源反證。`s57104` 用信旁一張折起的電報單示意，不得生成可讀、仿原件文字或暗示已核過那份實物；`s57149` 的 `several empty travel positions` 是抽象物件，日後原生圖須確認觀眾讀得到「人未到」而非畫出已到人員；`s57151` 的名冊須保持素面，不能讓模型憑空填出姓名或標定人物身份。插圖是概念示意，這些是實際原圖 KEEP／REJECT 的檢查點，不表示已有圖通過。

## 檢查與限制

`node tools/video/cli.mjs lint --slug curio-s57 --json`：**0 error／0 warning、167 句、估時 13.845 分**，開場 00:45；149／167 鏡是 `shot`，15 條 loops。`npm run test:docs-videos`：**236／236 pass**；`npm run check:tasks`：exit 0，僅有其他舊票的持有時間與範圍警告。**來源可供敘事盲評；書面畫面仍停在 `s57150`，付費插圖與分鏡不放行。** 敘事、政策、語音、網站真人審核、原圖、配樂、組片和發布均須各自完成。
