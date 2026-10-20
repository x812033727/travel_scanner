# S49 R6｜巨鏡運輸轉折與虛構火災畫面：作者凍結

2026-10-20 UTC。這是**作者修稿及機械自查**，尚非 R6 獨立史料／書面畫面 PASS 或正式敘事雙盲 PASS。[R5 獨立來源覆核](review/r5-source-independent.md)確認 136 句旁白事實可用，但 `moon103` 書面畫面把虛構火災放在 `real modest observatory`，故畫面 HOLD。[R5 兩位只讀劇本的新讀者](review/r5-fresh-panel-b.md)對 `moon049–051` 都指出重述；B 的 `payoffs` 也否決。A 額外讀通用指引而揭露隔離限制，不能把 R5 評語當 R6 關卡票。

R6 僅改 `moon049–051` 三景的旁白與提示詞，以及 `moon103` 一景提示詞，並同步 `claims.md`、重生 `script.md`。`moon049` 把鏡片完成後還需顯微鏡與轉動架的報導下一步交代清楚；`moon050` 問器材如何跨海，`moon051` 以文章聲稱的一行人出航、鏡片與支架到高地**直接回答**。不再於數字之後重問數字來源、又重說沒有器材清冊。新增研究錨點 P05a，固定 [1859 重印本 L501–568](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L501-L568) 記鏡片運至首都、另造顯微鏡與架子，並在**文章自己的敘事**中讓一行人從倫敦出航、到岸後把鏡片和支架送往高地。L565–568 另記牛隊登坡；研究表明示原文沒有指定牛隊是運鏡片的唯一工具。新三景的畫面均是無可辨原件的卡通想像，沒有把這些寫成真正 Herschel 器材史。

`moon103` 台詞仍是「這是虛構報導裡的火，不是赫歇爾真實觀測站的火災紀錄。」畫面改成 1830 年代讀者合上一張無字虛構火災報紙，旁放普通天文台示意圖；**不畫火焰、真站點或 Herschel 本人肖像**。其餘 129 個編號景、其他 133 句口播、全部 `loops`、企劃選案、來源固定版、頻道／來源 URL、縮圖及片頭片尾計畫不變。

| 內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `eb622b1471461f61a213a66c2bf646274e0e4887c82e102bea83ef2aa4aaea0e` |
| `research.md`（新增 P05a） | `73eb8e6f49f10ac4a0f275511913ccfff5c3f18eec6958cc6b25595eb20506d2` |
| `claims.md` | `a9f13314a1ab2776de217423b8cfc537ca5739ea09535f4d241a2d9791fc95ff` |
| `script.md`（CLI 重生） | `dfc5ae984d4720f4c104edaf23cf1d7ff6bca5b05793b51fe32fdd59995fb8f8` |
| `video.json` | `5dc1602b0aeb254ea1c2b3d45ab9fbff15450fe73f80e06c202059cd6f3934b4` |

`script --slug curio-s49` 重生，敘事短碼 `fefeaa74c94c3449`；`lint --slug curio-s49 --json` 為 **0 errors／0 warnings**。JSON 與劇本 **136/136** 台詞逐字同序，133 個編號景在 claims 中同 ID／同台詞／同書面畫面提示，全部 ID 唯一。開場前八景 176 spoken units，以 325 CPM 估 **32.49 秒**；正文 2,706 units，以同速估 **499.57 秒（8:19.57）**。這些是保守文字估時，未有 TTS 實長。`git diff --check`、`npm run check:tasks` 均通過；後者為 2,123 票，既存 stale／scope overlap 提醒不影響退出碼。

下一步須由未參與 R6 作者修補者重開固定 L／J，核對四景書面提示、三句新旁白與 P05a 來源；再由**兩位真正新的、只讀 R6 `script.md` 和固定十三題規則**的讀者作正式雙盲。前版來源／敘事票不能移作 R6 PASS。獨立來源及故事皆通過後才能送站台劇本卡、跑正確類別政策判讀、實際 TTS 和後續圖像；目前沒有付費媒體、配樂、成片、上傳或可點 Studio 片尾元素。
