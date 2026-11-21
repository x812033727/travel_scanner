# 第 23 集真人版 fix-polish（上架前精修重拍，2026-11-21）

只寫提示詞與 spec，沒有送出。三鏡都是 A 級（`review-zt/consolidated/retakes.json`，審片報告 `review-zt/reports/e023.txt` 中等 1–3）；B 級沒有。
C 級（s40、s31、s23、s27、s28）交站主決定，這裡不寫。種子 9239101、9239102；台詞一字沒改；參考圖全部照 base。
三支 base 在 d1 的兩個種子提示詞逐位元相同（`cmp`），所以 base 寫的是挑中的那支（`picks.json` 的 seed）。

| 鏡 | 審片問題 | base | 改了哪些句子（舊 → 新） | 換圖 | 拿不準的 |
| --- | --- | --- | --- | --- | --- |
| s33 | 唐小棠 a31 錄音還沒講完，近景的魏少卿 c2.0 起開口、露齒動嘴 1.7 秒（中等 1）；桌上多一盤食物 | `d1/prompts/ref-s33-9231102.txt`，6 秒 | 構圖：扇子「held upright … like a short slim stick」→ 加「扇頭抵在下巴、下唇下方」；「testing her: eyes narrowed, lips closed」→「聽、掂量：嘴抿成一條不動的細線、下巴靠在扇上」；加「畫面底緣只有空的深紅桌面、一把陶壺兩個小陶杯」。動作：「says nothing … no talking, no mouthing words; his eyes widen a little, then narrow again」→「整鏡只聽：嘴貼著扇頭抿成一條線、下顎與臉頰不動；唯一的動作在眼睛：慢慢瞇起、左眉微挑」（只用正面描述，拿掉 no talking 這類否定） | 不換（`weishaoqing-portrait-l1`） | 上一版也寫了嘴閉，模型照樣讓唯一露臉的人去講那句不存在的話；這次用扇頭在唇下當物理上的理由，賭得是兩個種子至少一支整鏡閉嘴。扇頭可能擋到嘴、或被畫成打開的扇子（打開會長假字，第 21 集） |
| s37 | 五人在屏風前排成一排面向鏡頭；賭約變成垂到桌前緣的大皺白紙；三老看鏡頭、沒有點頭（中等 2） | `d1/prompts/ref-s37-9231101.txt`，6 秒 | 構圖：「wide shot across the room, one sheet of thick smooth cream paper … on the near edge … at the very bottom edge of the frame」→「從方桌近側拍、桌面在畫面中下，三方隔桌相對；陶壺旁一張巴掌大對摺白紙，素面朝上平放在桌面」；魏少卿加「身體朝畫右、朝後面的屏風」；唐小棠「side by side … face in profile」→「右前景、離鏡頭最近，身體與臉都轉向畫左看魏少卿」；許硯「close at her right shoulder」→「在她右肩後半步，身體與臉轉向畫左看魏少卿，眉頭皺起」；三老「seen side-on」→「在桌後屏風前、畫面裡小、虛焦，身體與臉側向畫左朝魏少卿，手攏在袖裡」。動作：「points the closed fan … glance at one another and nod together once」→「抬起合著的扇子隔桌指向三老；三老仍側身朝他，一齊點頭一次」（拿掉互看，一人一個動作） | 不換（魏 l1、唐 l1＋angle-a、許 l1＋angle-a、`set-kezhan-pm-l1`） | 許硯的灰外衣：審片指出 s36 沒穿、s37 穿；但外貌錨句與參考圖都有外衣，s40（不重拍）也穿著，所以照錨句留外衣，s36→s37 的外衣差別仍在。唐小棠正臉的髮型（單髻、長緞帶）是參考圖帶來的，上一輪已接受。s37 坐變站：s36 她在桌邊看不出是坐是站，s40 是站，這裡維持站。整句原聲重拍，魏少卿的聲音會換成新草稿的原聲，s37 與 s38 音高要重量 |
| s06 | 濕的大手接著粉袖、小手從藍灰袖那邊來；兩手疊在木頭上 2.5 秒沒有抓住往上拉（中等 3） | `d1/prompts/ref-s06-9231101.txt`，5 秒 | 構圖：「a small hand in … peach-pink … already gripping a man's wet wrist … above the dark wooden edge」→「從船側看、濕船舷橫過畫面中間；年輕女子的手臂從上緣下來（小手、乾、桃粉不透織錦袖口，粉袖留在船舷上方），年輕男子的手臂從下緣黑水裡上來（大手、濕、藍灰濕袖、滴水）；第一格她已握緊他手腕；粉袖只屬於上面那隻、藍灰袖只屬於下面那隻」。動作：「pulls hard upward, and the man's other hand slaps onto the wooden edge and heaves … warm glow of the one bow lantern」→「她往畫面上方直直用力拉，他的手腕、前臂、手肘跟著出水越過船舷，水從藍灰袖流下」，拿掉他另一隻手（一鏡一個動作）與船頭燈籠（上一版背後長出石燈籠與拱門，靠 1.36 倍裁切遮掉） | 不換（`set-chuan-ye-wu-l1`） | 兩隻手不點名（點名沒有參考圖會被畫成人臉，preflight 的 unpictured）。手握手腕有變成牽手的風險，但這鏡本來就要握住，靠「上下兩緣分開進來、往上拉」讀出方向。5 秒照 base；剪接只用約 2.5 秒 |

## 檢查（2026-11-21）

- `python3 -I _scripts/polish-build.py 23`：e923: 3 shots, 6 drafts, 34 s
- `preflight-prompts.py …/fixp/colab-jobs.json`：0 error(s)、0 warning(s)
- `h3r.sh check --manifest …/fixp/colab-jobs.json`：0 error(s)、0 warning(s)

## 拍完之後要看的

- s33：逐格看 c0–6 嘴有沒有開（上次第 6–7 格起開口）；扇子是否一直合著；桌上有沒有長出食物。
- s37：五人是否還排成一排面向鏡頭；三老是否側身、有點頭；紙是否平放在桌面、巴掌大；魏少卿的原聲是不是稿子原句（whisper），音高對 s38。
- s06：粉袖是否只在上面那隻手；是否真的往上拉、前臂出水；背後是否只有霧。
