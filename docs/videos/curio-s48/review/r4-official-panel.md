# S48 R4 隔離旁白雙盲：正式敘事 FAIL

2026-10-20。兩位新讀者各只收到 `node tools/video/cli.mjs narrative --slug curio-s48 --json` 生成的旁白與固定 13 題，沒有讀企劃、來源、主張、畫面、舊評或彼此答案。輸入 JSON SHA-256 `f3532d6ef33c938fd691cb39b2bd2f2b672d7fe09f3e57ef84a5910c63f8c083`；對應 `brief.md` `875550d9b245012357c27a2360641f54202003a5e45bde638f19e1f5811ec8bf`、`script.md` `0794fe3217bf4aab22158135d4af4ebf834b2cfb37c845a898fad4c0873a7cc6`、`video.json` `a2f36c1dc2c6a3b1b609ea5630a2e9cf11c9e795bf272956901d6d054bec0501`、`claims.md` `baee71c3df9ded7d8128cf73a92855ec5743fb6f0981745ba060927672aa1183`。題規 SHA-256 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`。

原始答案分別存為 [A JSON](r4-official-panel-a.json) 與 [B JSON](r4-official-panel-b.json)，工具 `panelVerdict`、`mergePanelVerdicts` 的完整結果和雜湊在 [合併 JSON](r4-official-panel-merged.json)。A、B 各 **11／13**；兩人同時判必答 `payoffs`、`no_recap` **No**，合併 **FAIL**。這次讀者看到的內容符合 CLI 隔離說明；先前 [A 編輯首讀](r4-blind-a.md)和 [B 編輯首讀](r4-blind-b.md)各看過 brief 或 claims，保留為編輯意見，**不充當**本次官方盲評。

| 共同失敗題 | 可查的原句與修稿方向 |
| --- | --- |
| `payoffs` | `[atl026]` 問短暫訊號中斷「問題在哪裡」，`[atl027]` 說確切原因仍未知；這個問法承諾了文本不能提供的原因。B 還指出開場 `[atl005]` 問鉤上的是什麼，正文 `[atl054]` 卻只說甲板上沒看見線。應把問題收窄到後文能回答的「訊號能否再送／當時能否確認」。 |
| `no_recap` | A 指出 `[atl095]` 已說愛爾蘭端回訊，`[atl096]` 又說對岸能送訊；B 指出 `[atl050]` 先說只見索具與儀表，`[atl054]` 又說未目視舊線。刪重複或換成有新事實的下一步；編輯首讀另記 `[atl085→086]` 計數近重述，修稿可一起壓縮。 |

R4 已有獨立史料／書面畫面差分 PASS，**不代表敘事 PASS**。R5 要改稿並重凍結來源、畫面與旁白雜湊，再走獨立差分、兩位全新隔離讀者、政策與站台版本關卡；此刻不配音、不買圖、不組片。
