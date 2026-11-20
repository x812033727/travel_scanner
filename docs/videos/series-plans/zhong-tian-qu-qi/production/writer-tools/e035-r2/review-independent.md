# 第 35 集重製版 r2（e035-r2，內部 935）獨立審稿：真人版分鏡與 d1 提示詞

- 審稿：沒參與寫稿的獨立代理，2026-11-20，開拍前（d1 還沒跑；錄音只有 3／36 句）。只寫這一個檔；沒改 `r2.py` 或別的檔、沒開 Colab／RunPod（沒碰 `zt-live2`、`zt-live3`）、
  沒用站台 TTS、沒付費圖、沒 commit。沒讀前置代理的自審 `writer-tools/e035-r2/review.md` 與 scratchpad 的 `e935prep/PROGRESS.md`。
- 審的對象：`writer-tools/e035-r2/r2.py`、`docs/videos/zhong-tian-qu-qi-e035-r2/{script.md,storyboard.md,video.json,overlays.json}`、
  d1 提示詞 `~/mokaair-work/videos/zhong-tian-qu-qi-e935-dh/runpod/live/d1/prompts/*.txt`（80 支）與 `colab-jobs.json`、`colab/runs/e935-live/{mkspec.py,PREP.md}`、
  `colab/runs/e935/extras.json`、`hailuo/clips-dh-e935.json`、`live-action/free-e031-e040/{xujia_wu_ye_crops.sh,hantian_yang.sh,hantian_yang_clean.py,cunkou_crops.sh}`。
- 對照：`r2-bible-e031-e040.md`（拍法 1–43、〈接點〉34→35 與 35→36、〈道具〉、〈人物〉〈小角色〉、〈場景〉、〈原版必修〉第 35 集）、第 33、34 集的獨立審稿通則、
  第 36 集 r2 稿 `docs/videos/zhong-tian-qu-qi-e036-r2/script.md` 的 c01–c03（接點 35→36）。
- 參考圖全尺寸打開看過：`set-xujia-wu-ye-l1`、`-table`、`-chuang`、`-qiang`、`-zhuo`、`-di`；`set-hantian-yang-l1`、`-zong`、`-zong-liu`、`-zong-an`、`-zong-tian`、`-zong-geng`、
  `-zong-shui`、`-xi`、`-chen`、`-chen-liu`、`-chen-an`、`-chen-shui`；`set-cunkou-l1`、`-men`、`-zha`、`-ding`、`-kong`、`-dao`。在 scratchpad `e935rev/` 放大看了田的地平線
  （四張調色）與 `-chen` 的遠樹，試裁了一張村口（必改 3）。
- 語速：PREP §4 只錄到 3 句，BUY 用第 30–34 集**已錄**的人聲長度（各集 `audio/span93N.txt`）照角色實測重估，見〈接受〉的 BUY 列與必改 5。

## 機械檢查（都通過的）

| 項目 | 結果 |
| --- | --- |
| 台詞 | `video.json` 36 句都能在 `script.md` 原文裡逐字找到，id 不重複；40 鏡＝c01–c35 加 s02b、s11b、s12b、s17b、s20b |
| 面板 | `overlays.json` 只有 s01「兌換：鴨群治蝗法」、s11「唐小棠 好感 +3 → 45」、s27「蝗災擋下，柳溪的田保住」、s30「天下歸心，百分之一到百分之二」，跟系統念的一字不差 |
| d1 清單 | 80 支、516 秒（每種子 258 秒：5 秒 4、6 秒 26、8 秒 9、10 秒 1），跟 `r2.py` 的 `BUY` 與 `colab-jobs.json` 逐鏡相符；兩種子的提示詞去掉種子後一樣 |
| 唐小棠的名字與圖 | `Tang Xiaotang` 只出現在 s11 的兩支；她的三張圖只在 s11 送（portrait＋angle-a）；s11 身分句沒有金算盤（只剩 `a small gold ornament`）；全部 80 支沒有 `stand-up collar`、`apricot`、`gold abacus`；`outer coat` 只在許硯的夜裡外衣 |
| 送圖 | 許硯 angle-b 全集沒送；s26、s34 只送 l1；阿令全景只送 l1；錢員外 s22 只送 l1；插鏡 s07、s21、s35 與 s12、s17b、s29 不送人；場景圖逐鏡照 `PLACE` |
| 潭字、泥、會長字 | 0 個 `pool`、`pond`、`mud`、` open`、`crowd`、`villager`、`hundreds`、`blossom`、`smoke`、`fog`、`candle`、`lantern`、兵器字 |
| clear-and-still 替換 | s14 `a dry wind blowing`、s20–s25 晨霧、s26 晚風；其他鏡照舊（見建議 4） |
| 布鞋句 | 只在全景 s12、s16、s19、s20、s22、s26、s34；s29 換成草鞋；近景沒有（許硯身分句裡的 `cloth shoes` 是定妝照句，同第 34 集） |
| 人數 | s12 四人、s16 兩人、s22 三人、s26 兩人、s29 十二人（十個流民含被牽著的小男孩＋婦人＋懷裡的孩子）、s32 四人、s34 五人，都寫 `exactly N` 且跟描述對得上；有名字的臉每鏡最多一到兩張 |
| 笑 | 寫了笑的只有 s11 最後、s20b、s22 冷笑、s25 最後；其他有臉的鏡寫 `not smiling`（**沒寫表情的鏡見必改 4**） |
| 精修文字 | `clips-dh-e935.json` 40 筆：背影鏡沒有唐小棠的名字、沒有立領句；s11 保留名字；`GAZE_REFINE` 的方向句都換進去；s04、s08、s18、s33 保留通用說話視線（聽的人就是前景背影，在畫裡，可以）；開頭 `3D CG` 是管線的事，同第 33、34 集 |

## 寫稿者沒把握的地方：逐一判斷

| 問題 | 判斷 | 見 |
| --- | --- | --- |
| (1) 田的左右照圖反過來 | **合理，而且是唯一照圖的寫法**。`set-hantian-yang-l1` 前景整片是水田，田埂後是犁過的褐土，遠山小屋在左，金黃垂柳在右、柳樹腳下一道窄的土田埂斜到右下。人、竹籠在右邊田埂、白線往左推，s12–s25 逐鏡的視線方向都一致（鴨子在左、阿令在右；s17b 鴨子轉向右邊田埂；錢員外在右邊大樹下朝左）。代價是田埂很窄、在圖上是一條斜帶：近景的人站在哪裡要照圖寫（必改 2、建議 6） | 必改 2、建議 6 |
| (2) 五個拆鏡 | **都合理**。s02／s02b（心裡話閉嘴→開口）、s11／s11b（正臉不說話→背影說話，近景→中景，拍法 40）、s12／s12b（出籠→報帳）、s17／s17b（近景看不到身後鴨子回頭）、s20／s20b（遠景數不出數）都是一鏡一個動作。s17b 補出了稿子的鉤子「幾隻鴨子同時回頭」，比原稿好讀 | 接受 |
| (3) c07 改算盤插鏡、帳冊不寫 | **合理**。聖經拍法 20、35 本來就列了「第 35 集算盤」插鏡；她的話放畫外錄音，不用露嘴。`-zhuo` 是整張小桌與那朵火，插鏡只當桌面與光，`INSERT_CLAUSE` 已寫明 | 接受 |
| (4) 村口沒有門樓、沒有籬笆：錢員外站土台、流民在柵門外 | **本集的寫法合理**：s31 低角度、`-ding` 的瓦頂當背景，看不到土台也不穿幫。**但這張圖的問題比門樓大**：柵門是一整片固定的木柵板（沒有兩扇門、沒有開口），那根「橫木」是釘死在柱上、斜撐壓在上面的結構木，不是能抬起的門閂；兩邊沒有籬笆，人可以從旁邊繞過去。本集只要手按著橫木不拉（s35）還讀得通；第 36 集 c01「兩手把門閂從托架上抬起」、c02「各拉開一扇柵門、流民走進來」在這張圖上拍不出來。若第 36 集再改圖，第 35 集 s26、s28、s29、s32、s34、s35 六鏡就跟它接不上 | 建議 1 |
| (5) c13、c15 不寫泥 | **合理**（第 32 集 fix3、第 34 集決定）。髮髻撞歪、幾縷頭髮垂額，跌坐的狼狽讀得出來 | 接受 |
| (6) 屋內 13 鏡送 e922 的夜圖與裁切（偏 CG） | **可以先拍，看 d1 再說**。全圖是明顯的 3D 算圖（磚塊圓角、窗外藍色霧景）；四張裁切都是 2.3–2.7 倍放大，偏軟；`-qiang` 幾乎全黑，只剩磚縫。好處是格局清楚（窗在左牆、小桌在牆角偏右、地上乾草），軸線一致。小問題：窗外是**深藍的霧景**，文字寫 `black with night`（建議 5）；`-di` 的機位跟稿子要的低角度相反（必改 1）。重畫約 1.5–2 CU，同意 PREP：先看 d1 | 必改 1、建議 5 |
| (7) 21 張免費圖 | **`-xi` 像傍晚**（橘、天頂轉青）。**`-chen` 讀得出清晨薄霧**，但霧是整張蓋一層（screen 45%），對比很低、偏插畫；而且遠處那棵紅樹被洗成鮭魚粉、黃樹變乳白，**小尺寸看像開花的樹**（原版必修第 35 集，建議 2）。**`-zong` 不太像「棕色半明半暗」**：讀起來是橄欖綠／青色的復古濾鏡，右上角偏青，亮度只降一點、垂柳仍然亮金黃，看不出天上壓著東西（建議 3）。地平線三根小竿塗得乾淨（放大 4 倍看四種調色都沒有竿、沒有方塊；房子右邊殘一道很淡的弧線，不像物件，接受）。裁切：`-zong-liu`、`-zong-geng`、`-zong-tian`、`-chen-an`、`-dao`、`-ding`、`-kong` 的取景給得出各鏡要的背景；**`-zong-an`（s13）六成是水**（必改 2）、**`-men`（s29）柵門佔三分之二**（必改 3）、`-di`（s05）是從上往下看整張桌（必改 1）；`-zong-shui`、`-chen-shui` 是俯看水面，s17b「貼水面」、s21「水面高度」寫法跟圖相反（建議 8，可接受） | 必改 1–3、建議 2、3、8 |
| 接點 34→35 | 第 34 集成片 `e934-live.mp4` **現在是 233.3 秒**（檔案 05:03 更新；PREP 寫的 244.6 秒是舊版），最後 15 秒抽 15 格看過：s38 阿令、s39 許硯肩上小禾（藍灰袍、袖子捲起、沒有外衣、髮髻）、s40 三個背影望著遠山上散成滿天小黑點的褐黑帶子，灰暗，最後全黑。**s01 接得上**：同一夜換到屋內，人只有許硯；外衣是回家後披上的（聖經：夜裡加外衣），袍子與髮髻一樣；光從灰暗田邊轉成一朵火的夜，中間隔集的斷點；s14 遠山的蝗群寫法跟成片一致（帶子＋散開的小黑點）。PREP 的秒數要改，s01 不用改（建議 9） | 建議 9 |
| 接點 35→36 | s32、s34、s35 的站位（許硯朝柵門、唐小棠在他右後、阿令身後半步、兩個守門的人在橫木兩頭、許硯右手按橫木）跟第 36 集 c01 一致；**能不能「抬起門閂」是圖的問題**（逐一判斷 (4)、建議 1） | 建議 1 |

## 必改

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 35 | s05 | **低角度「在桌子底下」跟送的圖相反**。`cam="Low-angle medium shot"`、comp `low-angle medium shot at a small child's height under the small dark square table … crouching … beneath the tabletop … the underside of the tabletop and its two dark legs around her`；送的 `set-xujia-wu-ye-di-l1` 是**站立高度往下看**整張小桌（看得到桌面與那朵火），而且桌腳之間下段有一圈橫撐，八歲小孩蹲不進桌底。模型只能照圖把她擺到桌邊，或把桌子改掉 | 第 33 集獨立審稿必改 7、第 34 集必改 3（位置與機位照圖）；拍法 29、42 | `cam="Medium shot, slow push in"`；comp 改成 `medium shot from a little above, like the picture: {XIAOHE}, crouching on the straw-strewn floor close beside the near left leg of the small dark square table, half tucked under the edge of its top, framed from the waist up, her left hand gripping the table leg, her face three-quarter to screen left toward the small window beyond the left edge of the frame, …`（其餘照舊；`the underside of the tabletop and its two dark legs around her` 拿掉）；motion 的 `shrinks back under the table` → `shrinks closer against the table leg`；zh 的「低角度中景（小禾的高度）」改「略高往下（照圖）」 |
| 35 | s13（鉤子） | **跌坐的位置沒寫在畫面哪裡，送的 `-zong-an` 六成是水**：圖上只有右上一條從樹幹斜到右下的窄土田埂，左與下全是插秧的水面。comp 只寫 `sitting down hard on the grass at the edge of the paddy`，腰以上的框會把他擺在畫面中下——就是水裡 | 第 34 集必改 2（s10 許硯站的地方是水）；拍法 29 | comp 改成 `… already sitting down hard on the low earthen bank in the right half of the frame, where it runs from the trunk of the big old tree down to the lower right as in the picture, the flooded paddy below him at the left, framed from the waist up, …`；`a few white ducks rushing past him along the bank` 照舊 |
| 35 | s29 | **送的 `-men` 柵門佔畫面三分之二，十二個全身的人沒地方站**。comp 寫 `its upright logs soft and out of focus along the left edge of the frame: beyond it, on the dirt road and the dry ground by the willow`；`-men` 是 720×405 的柵門正面，右三分之一才有柳樹與石溝，人只能縮小或擠到柵門前面（＝門內）。另外流民整群**沒有表情**（拍法 14），哭著求一口飯的戲最怕有人在笑 | 拍法 29、14、35；第 33 集必改 7 | **免費**：`cunkou_crops.sh` 加 `c set-cunkou-wai-l1 720:405:360:220`（我在 scratchpad 試裁過：柵門右段與斜撐只在左緣約兩成、中間垂柳、前景石溝與木板橋、溝後一片乾地、右邊兩間屋），新 id，`mkspec.py` 的 `PLACE` 把 s29 改送它，README 記一行。comp 的位置句改成 `beyond the stone-lined ditch and its plank bridge, on the dry ground round the willow, framed full figure, {REFUGEES}`；`REFUGEES` 後加 `their faces gaunt and pleading, eyes wet, not smiling` |
| 35 | s12、s19、s20、s34 | **沒寫表情**（拍法 14：每鏡寫表情；預設不笑要寫出來）。s12 四個開籠的村民、s19 與 s20 的阿令（全景、小）、s34 兩個守門的人（側身、看得到臉）都只有 `lips closed` 或什麼都沒有；s12 是亂糟糟的喜劇段，村民跟著鴨子笑出來的機率高 | 拍法 14；第 31 集原版必修（不該笑的鏡笑） | s12 `MEN4` 後加 `busy and harried, not smiling`；s19 `ALING_DUCK` 後加 `calm and intent, not smiling`；s20 加 `intent and still, not smiling`；s34 `GUARDS` 後加 `grave, not smiling`（s26、s34 的背影不用） |
| 35 | s31、s22（BUY） | **錢員外的兩句最可能放不下**。第 31、33、34 集錢員外（Algenib）實測 9 句都在 **2.2–2.9 字／秒**（中位 2.5；`span931`–`span934`），比許硯（中位 4.0）慢很多。s31「關門！糧不夠！誰敢開門，全村一起餓！」14 字、三個驚嘆停頓，估 **4.8–6.3 秒**，買 6 秒（放得下約 5.9 秒）；s22「鴨子治蝗？許秀才，你這是要笑死全縣的人。」17 字、冷笑拖長音，估 **5.9–7.7 秒**（第 31 集 s34 同樣「拖長音」16 字量到 6.73 秒），買 8 秒（約 7.3 秒） | 聖經〈每集鏡數〉（6 秒放 5.9 秒、8 秒放 7.3 秒）；拍法 43 | `BUY` 改 `"s31": 8`、`"s22": 10`（每種子多 6 秒，兩種子約多 0.5 CU）。不改的話，錄音後 s22 多半要剪掉拖音、s31 要剪停頓 |
| 35 | s25 | **長竿與哨繩第一格沒寫分開**。`r2.py` docstring 說 s17、s25 都寫了「the pole and the whistle cord」不相連，實際只有 s17 寫了；s25 是 `the small bamboo whistle … resting on its cord at her chest … {POLE} upright in her right hand`，竿子從胸前直上出框，最容易跟胸前的哨繩黏成一條 | 第 32 集 fix2（長東西第一格不相連）；第 33、34 集通則 | `{POLE} upright in her right hand` → `{POLE} held upright out at her right side, well apart from the whistle's cord` |

## 建議

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 35、36 | `set-cunkou-l1`（s26、s28、s29、s32、s34、s35；第 36 集第一場） | 見逐一判斷 (4)：一整片固定木柵板、橫木是結構木、沒有兩扇門、兩邊沒有籬笆。第 36 集 c01「抬起門閂」、c02「推開兩扇柵門、流民走進來」拍不出來；PREP §5.1 建議第 36 集前置時再決定，但**同一刻的六鏡在第 35 集**，第 36 集才改圖兩集就接不上 | 拍法 19、29；聖經〈道具〉村口柵門列（兩扇、門閂）；〈接點〉35→36 | **建議 d1 前決定**：Qwen 只改一件事「the palisade becomes a pair of gate leaves of upright logs set in a short log fence that runs off to both sides, one thick loose crossbar resting in two iron brackets across both leaves」，新 id `set-cunkou-zha2-l1` 再免費重裁，約 **1.5–2 CU**（一次不行再一次，上限約 4 CU）。不做就照本集寫法拍，第 36 集 c01–c02 改寫成「橫木抬不起、改從柵門旁讓人進來」 |
| 35 | s20（`set-hantian-yang-chen-l1`） | 晨霧調色把遠處那棵紅樹洗成鮭魚粉、黃樹變乳白，960×544 的小尺寸看起來像開花的桃樹與梨樹——正好是原版必修第 35 集要避開的「背景開花的果樹」。`-chen-liu` 左緣也有一小團粉色 | 原版必修第 35 集；拍法 18（不寫否定名詞，所以要靠圖） | **免費**：`hantian_yang.sh` 在調 `-chen` 前，對地平線那排樹（約 y 340–390）做局部降飽和、壓暗紅色（同 `hantian_yang_clean.py` 的遮罩做法），新 id；或先看 d1：s20 兩支背景樹看起來開花就重做 |
| 35 | s12–s18（`-zong` 一族） | `-zong` 讀起來是橄欖綠／青的復古濾鏡，不是「蝗群壓在天上的棕色半明半暗」：天偏青、亮度只降一點、垂柳仍是亮金黃；文字又寫 `the sun a pale disc high in a dull brown sky`，圖上沒有太陽。加上 extras 句 `the air is clear and still` 叫空氣乾淨，三樣疊起來 d1 多半是晴天濾鏡 | 第 34 集必改 1（clear 句跟劇情要的空氣打架）；逐一判斷 (7) | 免費重調：`colorbalance` 的 `gs`／`gm` 降到 0、`bs`／`bh` 再降、`brightness` 再壓一些、加一點暗角，新 id；`mkspec.py` 把 s12–s18（含 s12b、s17b）的 `CLEAR` 換成 `"the air dim and dusty under the dull brown sky, a clean natural film image"` |
| 35 | s29–s35（村口有火把的鏡） | 這幾鏡都寫火把的橘光 `wavering`，結尾又是 `the air is clear and still`；不至於把火熄掉，但會壓住晃動 | 第 34 集必改 1 | `mkspec.py` 對 s29、s30、s32、s34、s35 把 `CLEAR` 換成 `"the warm evening air, the torch flames flickering, a clean natural film image"`；s28、s31、s33 可一起換成 s26 的 `BREEZE` |
| 35 | s01–s11（屋內） | `NIGHT` 與構圖寫 `the small window black with night`，送的圖窗外是**深藍的霧景與山影** | 拍法 29（圖說了算） | `NIGHT`、`ROOM_BACK` 等的 `black with night` → `dark blue with night` |
| 35 | s12b、s16 | `-zong-liu` 的田埂是從樹腳斜到右下的窄帶，左半是水與犁過的地。s16 寫兩人「at the left … at the right」站在田埂上，阿令「在左」會落在水裡或乾地；s12b 許硯「左三分之一、站在田埂上」同理（腰以上，風險較小） | 拍法 29；必改 2 同一件事 | s16：`at the left {ALING_DUCK}` → `further along the bank toward the tree, {ALING_DUCK}`；拿竹竿的人 `who stands nearer us at the lower right of the bank`。s12b 可不改 |
| 35 | s01–s11 | 許硯的位置前後說法不一：s01、s03 坐在桌的 **left side**，s04、s08、s09、s11b 站在桌的 **far side**；唐小棠 s03 在 **right side**，s09、s11b 在 **near side**。過肩與背影鏡切換時模型會各自理解，桌子在牆角，far side 只有很窄一條 | 接戲；拍法 42 | 全場統一成「許硯在桌的左側、唐小棠在桌的右前側」：s04、s08、s09、s11b 的 `at the far side of the small dark square table` → `at the left side of the small dark square table`；s09、s11b 的 `standing at the near side of the table` → `standing at the right side of the table` |
| 35 | s17b、s21 | 構圖寫「貼水面」「水面高度」，送的 `-zong-shui`、`-chen-shui` 是**俯看**一片水與秧 | 拍法 29 | 可接受（插鏡、背景只當水面）；要一致就寫 `close-up from a little above the water` |
| 35 | PREP.md 開頭與 §1 | 第 34 集成片已更新為 233.3 秒（05:03），PREP 仍寫 244.6 秒；最後 15 秒的內容沒變，s01 不受影響 | 接點核對要記實際版本 | PREP 改成 233.3 秒並註明「05:03 版，s38–s40 不變」；第 34 集定版後照舊再核一次 |
| 35 | s14 | 唐小棠左手按住「一條被風吹亂的短緞帶」，但 `TBACK` 寫緞帶是 `short … wrapped around each bun`，纏在髻上的短緞帶吹不起來；按頭的手又會蓋住一顆丸子 | 拍法 40（剛好兩顆丸子） | `holding down one short pink ribbon tossing in the wind` → `the loose tail of one pink ribbon fluttering in the wind beside her fingers, both buns still clear`；或乾脆拿掉左手這一拍（右手指遠山就夠） |
| 35 | s31 | 動作寫 `thrusts it toward the gate's crossbar`，低角度框裡只有瓦頂與天，橫木不在畫裡 | 拍法 31（看的、指的地方寫成畫裡看得到的實物） | → `thrusts it down toward the gate below him` |
| 35 | 錄音後 | 除必改 5 兩鏡外，最緊的是 s24（錢員外 18 字、邊走邊說，估 6.2–8.1 秒／8 秒）、s30（系統 14 字＋心裡話 16 字帶刪節號，估 7.6–9.5 秒／10 秒）、s12b（唐小棠 21 字「喘」，估 6.1–6.9 秒／8 秒）、s20b（小禾一個一個數「一、二、三……」，估 4.5–5.5 秒／6 秒） | 聖經〈每集鏡數〉 | 錄完照 `span935.sh` 重核這四鏡；s24 超過 7.3 秒就改買 10 秒 |

## 接受（看過、不用改）

| 項目 | 為什麼 |
| --- | --- |
| 唐小棠（拍法 3、4、40） | 說話的九鏡（s03、s09、s11b、s12b、s14、s23、s26、s28、s32）都從背後、畫面正中、頭不動、剛好兩顆丸子，`HEADSTILL` 每鏡都在動作句裡，沒有轉頭的動詞；她的動作只寫手臂。正臉只有 s11（近景、嘴閉著、最後小笑），s11b 是中景背影，不同景別。s07 插鏡與 s17b 鴨子放她的畫外錄音：s07 有她的手、s17b 是她「看傻了」的反應對象，都合理。不寫淡杏外衣、高立領、金算盤 |
| 屋內軸線 | 許硯在左、唐小棠在右、窗在左牆、小禾在桌邊；s03／s04、s08／s09、s10／s11 的過肩、背影、反打一左一右接得上（s11 背景送桌右的暗牆，是 s10 的反方向） |
| 田的軸線 | s12–s25 鴨子都在畫左水面、人在右邊田埂；s17b 鴨子轉向右邊田埂（阿令那側）；s22／s23／s24 錢員外在右朝左、s24 往右走從右肩回頭（同第 33、34 集必改） |
| 村口軸線 | 柵門與流民在左、村道與小屋在右；s27、s30、s32 許硯朝左、s31 錢員外朝右下、s33 阿令從右邊村道來朝左看他的背；s32／s33／s34 接得上，s34 的站位交給第 36 集 c01 |
| 鉤子 | s13 鴨子站在頭上（加必改 2 的位置）、s17b 六隻同時轉頭（近景，五到八隻）、s20 白線第一格已經湧進水田、s21 鴨嘴啄蝗蟲（插鏡、第一格就是主體）、s31 低角度大喊、s35 手指一根根收緊、`the bar not moving`：都讀得出 |
| 鴨群的寫法 | 近景五到八隻、遠景「a long unbroken white line」、不寫數字；s19 的 `a loose flock` 是唯一的集合名詞，指的就是那一群鴨子，接受 |
| 原版必修第 35 集 | `FIELD` 寫「only this one paddy is green, the fields beyond the ridge dry and bare」，圖上田埂後是褐土、四周沒有水田；開花的樹只有 `-chen` 調色的風險（建議 2） |
| 錢員外、家丁、流民婦人 | 胸前素面（`the front of the robe plain brocade`）；家丁只在 s22 全景、空手；婦人只拍背影、孩子臉埋在肩上 |
| 系統與心裡話（s01、s02、s11、s27、s30、s35） | 嘴閉著、不寫淡藍光、面板交給剪接；已錄的 a01＋a02 共 4.7 秒、a03 3.45 秒，放得下 |
| BUY（其他鏡） | 用第 30–34 集實測重估：唐小棠（Laomedeia）11 句**中位 3.4 字／秒**（PREP 照稿子估 4，偏快），本集她最長的 s12b 21 字約 6.1–6.9 秒、s23 20 字約 5.8–6.5 秒，在 8 秒內；6 秒鏡最長的 s26 16 字約 4.7–5.2 秒。許硯中位 4.0、小禾 3.3、阿令 3.4（12 字約 3.5–4.2 秒）、系統 4.3：其餘說話鏡都在 5.9 秒內。流民婦人（Erinome）沒量過，14 字哭腔照 2.5–3 字／秒估 4.7–5.6 秒，8 秒夠 |

## 小結

- **必改 6 項**，都是改字或免費重裁，不花錢（BUY 兩鏡多約 0.5 CU）：(1) s05 拿掉「低角度在桌底下」，照圖改成蹲在桌腳邊；(2) s13 寫出跌坐在右半邊的土田埂上（圖上六成是水）；
  (3) s29 換一張柵門只在左緣的免費裁切 `set-cunkou-wai-l1`、流民站在石溝後柳樹邊、加不笑的表情；(4) s12、s19、s20、s34 補表情；(5) BUY：s31 改 8 秒、s22 改 10 秒（錢員外實測只有 2.2–2.9 字／秒）；(6) s25 竹竿與哨繩寫分開。
- **建議 12 項**；要付費的只有村口柵門改成兩扇門加門閂與籬笆（約 1.5–2 CU，**建議 d1 前決定**，不然第 36 集第一場拍不出「抬門閂、開門」）。
- 七個寫稿決定：田照圖反過來、五個拆鏡、c07 算盤插鏡、不寫泥都合理；錢員外站土台在本集可行，但村口圖本身的問題要在第 36 集前處理；屋內 CG 圖先看 d1；21 張免費圖 `-xi` 可以、`-chen` 要防開花的樹、`-zong` 不像棕色半明半暗。
- **最可能放不下的句子**：s22（錢員外 17 字拖長音／8 秒）、s31（錢員外 14 字大喊／6 秒），其次 s24、s30、s12b、s20b。
- 改完 `r2.py`、`mkspec.py`（與 `cunkou_crops.sh`、必要時 `hantian_yang.sh`）後重跑 `build935.sh`、`prep935.sh`；錄音補完後照 `span935.sh` 重核 BUY；PREP 的第 34 集秒數改成 233.3。
