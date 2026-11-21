# 第 6 集真人版 fix-polish：上架前精修重拍（2026-11-21）

範圍：`consolidated/retakes.json` 裡 e006 tier A／B 的四鏡（全是 B：s25、s30、s35、s39）。C 級的 s09、s34 不在這裡（審片寫「接受」或「不花錢的模糊做法」）。
種子 9069101、9069102，960×544 Ref2VA，每鏡兩支，共 8 支、56 秒草稿。產出在 `~/mokaair-work/videos/zhong-tian-qu-qi-e906-dh/runpod/live/fixp/`。
base 從 `_live-e906/.../picks.json` 的 `draft` 路徑找（picks 沒有 `motion_from` 欄，用 draft 所在的資料夾判斷）。

| 鏡 | 審片問題 | base | 改了哪些句子（舊 → 新） | 換圖 | 拿不準 |
| --- | --- | --- | --- | --- | --- |
| s25 | 許硯肩上多一條灰披布、斜紅布變小紅繩結、背景換成院子加晾衣架 | `fix2/prompts/ref-s25-9061201.txt`（8 秒） | 「patched robe… one strip of red cloth tied diagonally」→ 袍子「lying smooth and close over both shoulders」、紅布「一掌寬、從左肩直直平貼到右胯」；「behind him only the vermilion gate」→ 寫死灰磚牆、一根紅柱、紅門、紅架大鼓「exactly as in <Picture 4>」；低頭看籃子時補「眉頭皺、眼睛累」，愣住後「眉毛揚起、眼睛睜大發亮」。台詞與拿三塊皂不變 | `set-xianya-l1` → `set-xianya-steps-l2`（同一個縣衙門口的左半，README 說右邊那排紅木架像兵器架、已裁掉；晾衣架就是從那排架子長出來的） | 披布是不是從「patched」或衣服皺褶長出來的不確定，只能靠正面寫「貼肩」；拿出的皂仍沒包葉（之前已接受） |
| s30 | 三人排排站對鏡頭；唐小棠胸前金鍊大算盤、髮型不同；趙捕頭手上的紅紙包像紅卡片；銅印有字紋 | `d1/prompts/ref-s30-9061101.txt`（6 秒） | 構圖改成「沿著台階頂看」：趙在右三分之一、四分之三側面朝左對許硯；許硯在左三分之一、靠近鏡頭一步、四分之三側面朝右；唐小棠在畫左緣、許硯肩後半身被擋。紅紙包「palm-sized parcels」→「每包是一塊掌心大、一指厚的白皂包著素紅紙」；銅印 → 「拳頭大的黃銅方塊、上有短圓鈕、四面光素」（照 s31 實拍的樣子）；「the abacus at her chest」→「右手在腰間拿著掌心大的小金算盤」，動作改成「掛上腰帶」；唐小棠補「兩個丸子頭粉緞帶」與精明表情；趙補「瞇眼、字間嘴平」；許硯補「嘴閉、看著趙」；婚書改成「平放在趙攤開的掌心上」；結尾加「三人臉都朝彼此」 | 沿用 base | 趙一人有塞紙包、轉身拿印、轉回伸手三拍，6 秒可能做不完（稿子原樣，沒刪）；唐小棠也有一個動作，三人同時動 |
| s35 | 「整條街被封」不成立：後景攤販在整理貨、攤子有桌有貨；唐小棠笑；c5.3 起四人排排站 | `fix2/prompts/ref-s35-9061201.txt`（8 秒） | 街 → 「the same street as in <Picture 8>：兩排兩層木樓，每間門面從檻到楣是豎排門板、外面兩條灰木板釘成大 X，石板從牆到牆空著」；拿掉一串「no table, no goods, no vegetables…」否定名詞；人 → 「三人單行從畫左往畫右走過畫面中間，身體側面對鏡頭」：許硯、秦霜（挎籃）、唐小棠；路人改成街尾兩個；唐小棠 → 停步、眼睛在左右兩排門板間跳、再轉四分之三側臉向許硯：眉壓低皺緊、眉間深紋、眼睛睜大、字間嘴抿成硬線、下顎繃；結尾「三人前後錯開、各自半轉向彼此」。台詞不變 | `set-shiji-l1`（滿街菜攤，就是攤子有貨的來源）→ `set-xianjie-l1`（空街、兩邊木門板全關）；拿掉 `aling-portrait-l1` | **阿令移出這一鏡**（稿子 c35 寫她走最後）：四個有名字的人會分身／排排站（preflight `four`、e906 s01 秦霜分身）；s34 她已先走下石階，s36 起本來就不入鏡。`set-xianjie-l1` 是藍天，s36、s38、s40 是灰白天，天色可能接不上（稿子寫晴）；右邊那棟掛著紅綢，可能被畫進來 |
| s39 | 街兩邊攤子擺滿蔬果像在營業；許硯背上沒有斜紅布（現片也看不到籃子） | `fix5/prompts/ref-s39-9061502.txt`（6 秒） | 街 → 同 s35 的豎板加 X 釘板、空石板街「the same street as in <Picture 7>」，拿掉「awnings and signboards」；許硯 → 「一掌寬深紅布從左肩斜過背到右胯，從背後看得清楚」、「竹籃裝白皂掛在右手、在畫面下緣」；動作「sets the basket down」→「放到右腳邊的石板上」。錢員外在二樓欄杆往左下看、許硯仰頭不變；許硯背對、台詞用錄音，提示詞照舊不寫台詞 | `set-shiji-l1` → `set-xianjie-l1`（與 s35 同一張） | 圖上沒有二樓欄杆陽台，茶樓陽台只靠文字（fix5 用 shiji 時也是文字畫出來的）；天色同 s35 |

## 檢查（2026-11-21）

- `polish-build.py 6`：4 鏡、8 支、56 秒，0 錯
- `preflight-prompts.py fixp/colab-jobs.json`：0 error、0 warning
- `h3r.sh check --manifest fixp/colab-jobs.json`：0 error、0 warning

沒有送出任何 Colab／RunPod 工作，沒有 commit。
