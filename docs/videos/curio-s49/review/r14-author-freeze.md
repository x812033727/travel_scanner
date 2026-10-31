# S49 R14｜章末問題直接落到下一章的報紙反應

2026-10-20 UTC。R13 來源／書面畫面獨立覆核 PASS，正式雙人敘事合併 12/13 HOLD：兩名讀者都認為 `[moon111]`「編輯反應真的只有相信嗎？」到下一章首句 `[moon112]` 未直接回答，直至第二句才舉例。R14 只改 `moon112` 旁白和主張錨點，並在研究表補一句新錨點；`moon082/083` 的相鄰相似性只有讀者 B 提出，正式 `no_recap` 仍通過，故本輪不擴張修改。

`moon112` 由「翻開先前那本重印書的後段，當年各報的反應被排在一起。」改成：

> 不是。先前那本重印書收的《費城詢問報》摘錄說，是真是假，讓讀者自己判斷。

這直接回答 `moon111`，交出與盲信不同的具體編輯反應，又不提前重說 `moon115` 的《商業日報》質疑或 `moon119` 的《晚郵報》反諷。固定 1859 重印本 [L 2157–2161](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L2157-L2161) 的 *Philadelphia Inquirer* 原句說 `truth or falsity` 讓讀者 `decide for themselves`。旁白限定為**重印書所收摘錄**，不宣稱已核對 1835 原報頁。書面鏡頭仍是一名讀者翻開 1859 小書；原書影像不得偽裝成 1835 年報紙。

| R14 固定檔 | SHA-256 |
| --- | --- |
| `brief.md` | `b9658ef9df619b6c92ba440ff395065a7702206690a72be863da24bcf098e8e9` |
| `research.md` | `f5da15ac571478389b9b9920832f79434f83af0d312cb84747dcdb680a667750` |
| `claims.md` | `6429496dad004e2e4c1d6b1def31e1c9631a08bad4b2ae0529240ba12f12d91d` |
| `script.md` | `0903ccc03e433c44d7f41f9ebf2325a6c051d7be50622bba5209a87d1802d2e1` |
| `video.json` | `8297aff2b6ebafec29bb192e7070ebaa9913ed6f321ff4bcdb2ac53827b4f95a` |

`script --slug curio-s49` 重生劇本，narrative `6d9e2d55fcbfb72d`、speech `dcd0542b4c6c64c3`。130/130 編號景與 claims 的 ID／順序／旁白相合；另有三句片尾，合計 133 唯一 line ID。124 shot、6 big、11 loop 及所有畫面／卡片／音樂／片頭片尾設定沿用。`lint --slug curio-s49 --json` **0 errors／0 warnings**，全片文字估 13.92 分鐘，第七章估從 11:13 起；R12 正文實測 12:26.53 只屬舊稿，不移轉為 R14 實測。`npm run test:docs-videos` **236/236 PASS**，`npm run check:tasks` **2125 票驗證成功**，`git diff --check -- docs/videos/curio-s49` 通過。

R14 必須重做獨立來源與書面畫面覆核，並由兩位新讀者盲讀這版全部旁白、正式合併；之後按精確新稿重做政策和音檢。R13 的敘事 HOLD、R12 的政策與舊音檔均不算新版放行。網站與站主審核狀態照實記錄；音訊零旗標前不進插圖、配樂或成片。
