# 第 30 集真人版 fix-polish：上架前精修重拍（s01、s08、s17、s30）

2026-11-21 寫。只寫提示詞與 spec，未送出。依據：`review-zt/consolidated/retakes.json`（e030 的 A 級四鏡，本集沒有 B 級）、`review-zt/reports/e030.txt` 中等 2–5、畫格條 `ep/e030/review/shots/sNN.jpg`。
四鏡現在用的草稿都是 d1（`_live-e930/.../picks.json`：s01、s08、s30 是 9301102，s17 是 9301101）；d1 兩個種子的提示詞逐位元相同（cmp），base 一律寫 `d1/prompts/ref-sNN-9301102.txt`。
種子 9309101／9309102（d1 9301101/2、fix1 9301201/2、fix2 9301301/2、fix3 9301401/2 都沒重複，`polish-build.py` 已檢查）。

| 鏡 | 審片問題 | base | 改了哪些句子（舊→新） | 換圖 | 拿不準的 |
| --- | --- | --- | --- | --- | --- |
| s01 | 整集第一格唐萬金咧嘴大笑約兩秒才轉哭相（接第 29 集「哭著奔來」） | d1 `ref-s01-9301102.txt`，6 秒 | 表情句 `tearful and out of breath, not smiling: wet red eyes … brows pulled up` → `crying and out of breath from the first frame:` 眼紅含淚、淚流下圓臉、眉內端緊皺上提、嘴角用力往下、下巴皺著發抖、喘著抽泣說話；動作句後補「每個字眉都皺著、眼濕、嘴角往下；說完嘴抿成發抖的下彎線、吸一下鼻子」與 `no smile at any moment, not even in the first frame, until the last frame`。台詞、放下手臂（唯一動作）、朝畫左不變 | 無（定妝照是平臉） | d1 也寫了 not smiling 仍笑；這次靠逐部位哭相，挑片看第 0–2 秒 |
| s08 | 唐小棠背影左右肩各冒出一疊紙（兩本帳本） | d1 `ref-s08-9301102.txt`，6 秒 | `one thick stack … held against her chest in her right arm` → `exactly one ledger, a single thin bundle … about as long as her forearm and two fingers thick, tucked under her right arm and pressed flat against her right side … only one narrow cream edge of it showing below her right elbow`，加 `above her shoulders only the nape of her neck and her two buns`；動作 `tugs once at the sleeve … only her arm moving` → `gives one small tug at the dark brown sleeve …, only her left arm moving, her right arm staying pressed to her side over the one ledger`；秦霜加 `listening calmly: brows level, eyes steady on the young woman` | 無 | 審片稿寫「左臂抱帳本、右手拉袖」，但秦霜在畫左三分之一（接 s07），用離她近的左手拉、帳本夾右臂下，維持 base 的左右；稿子「秦霜退開半步」照一鏡一動作不拍 |
| s17 | 帳本特寫每頁都是全白紙，畫外在念「一筆都不漏」；頁面還折成三角 | d1 `ref-s17-9301102.txt`，5 秒 | 構圖 `insert close-up seen from slightly above, looking down … its top sheet blank and pale` → `extreme close-up from a very low side angle, the lens level with the paper's edge` 闔著的縫線帳本（兩掌寬、三指厚、棕線縫脊）側看：書口一層層米色紙邊朝鏡頭、縫脊在左、封面只剩上緣一細條；動作 `The right hand turns the blank pages over …` → `The right thumb riffles quickly down the stacked page edges … flicking back down … the ledger staying closed and level … with only its edges toward us`。拿掉 blank pages／sheets 的字樣，沒寫 nothing written 這類否定句 | 無（仍送 `-di-l1` 黃土地） | 背景圖是俯看的土地，平視時背景透視不一定對，只寫虛焦；拇指撥書口模型可能還是翻開一頁，挑片看有沒有攤平的白頁 |
| s30 | 魏少卿臉朝畫右（前後鏡都朝左）；背景是近乎天黑的落日與禿枝，夾在明亮的 s29、s31 中間 | d1 `ref-s30-9301102.txt`，8 秒 | 場景句 `the bare branches of a tree against the glowing evening sky, the low golden sun behind them at the right: low-angle` → `before the low mud-and-stone wall of the yard with the golden field beyond it, warm golden low evening sun from the right, the same bright warm light as the rest of the yard: slightly low-angle`；站位 `standing, … fan in his right hand …, sheet … raised high in his left hand …; that side … bare branches and the glowing evening sky` → 站畫右三分之一、身臉轉四分之三朝畫左、髮髻後腦朝畫右、眼盯畫左外，婚書（手掌大、只見紙背）右手舉在肩高，扇子合著低放在左手腰邊，左三分之二只有牆頭與金田；表情拿掉 `not smiling`，加眉壓低、鼻翼張、下顎咬緊；動作補「整句下顎咬著、嘴角往下，說完嘴抿成硬直線」與 NOSMILE 句 | `set-xujia-yuan-dong-shu-l1`（禿樹映晚天）→ `set-xujia-yuan-dong-qiang-l1`（泥牆、金田，院子右半近景 s18、s23–s29 用的同一張） | 低角度仰拍時背景容易拍到天，改成 `slightly low-angle`；牆與田的圖放大 4.6 倍偏軟；s31 第一格婚書已在唐萬金手上的不連戲不在這次範圍 |

## 檢查（2026-11-21）

- `python3 -I _scripts/polish-build.py 30`：4 鏡、8 支、50 秒，0 錯
- `preflight-prompts.py …/fixp/colab-jobs.json`：0 error(s)、0 warning(s)
- `h3r.sh check --manifest …/fixp/colab-jobs.json`：0 error(s)、0 warning(s)
- 字詞掃描：剩下的 `blank` 都是收尾句的 `blank expression`；`nothing` 是 s08 base 原有的 `Qin Shuang says nothing in this shot`；`smile` 只在 s01、s30 的 NOSMILE 句。

輸出：`~/mokaair-work/videos/zhong-tian-qu-qi-e930-dh/runpod/live/fixp/`（`prompts/ref-sNN-930910{1,2}.txt`、`retake.json`、`colab-jobs.json`）。
