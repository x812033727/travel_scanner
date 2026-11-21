# 第 13 集真人版 fix-polish：上架前精修重拍（2026-11-21）

站主 2026-11-21 決定審片列 A、B 的鏡全部重拍。第 13 集在 `review-zt/consolidated/retakes.json` 有 A 一鏡（s16）、B 四鏡（s28、s14、s20、s08）；
s02、s34、s35 是 C，不在這批。原因照 `review-zt/reports/e013.txt` 第 1、2、4、5 項與畫格條 `review-zt/ep/e013/review/shots/sNN.jpg`、證據格 `x/s16_7950_c.jpg`。

- 種子 9139101、9139102；960×544 Ref2VA；5 鏡 10 支，共 72 秒。
- 鏡號：成片 s01–s10 = 分鏡 c01–c10，s12–s42 = c11–c41（s14 = c13、s16 = c15、s20 = c19、s28 = c27）。
- base：`_live-e913/…/picks.json` 每鏡 `draft` 所在的資料夾（d1、fix1）裡、同種子的 `prompts/ref-sNN-SEED.txt`（picks.json 沒有 `motion_from` 欄，用 `draft` 路徑判斷；s16 的兩個 d1 種子提示詞逐位元相同）。
- 產生：`python3 -I ../../_scripts/polish-build.py 13` → `~/mokaair-work/videos/zhong-tian-qu-qi-e913-dh/runpod/live/fixp/`。
- 台詞一字沒改，都是畫面上露嘴的原聲鏡（s14 無台詞）。參考圖全部沿用 base（三張許硯 l1 圖都是平臉、沒有在笑的圖）。
- 刨子在 s14、s16 用同一句寫死：全木中式刨，淺黃褐長木塊、約前臂長、手腕粗，前端一根橫穿的圓木把兩頭各露一截，中間一片木楔；不寫 metal／iron 之類的否定名詞。
  這個樣子從側面看就是 s15（保留）那把「木塊上突出一個圓木頭」，所以 s14→s15→s16 會比較接近；s19 的扁木板審片接受，不動。

| 鏡 | 審片問題（現在那支） | base | 改了哪些句子（舊 → 新） | 換圖 | 拿不準的 |
| --- | --- | --- | --- | --- | --- |
| s16（A） | 前景是一把現代鑄鐵台刨（前球把、後握把），佔前景約 3 秒；門在剪進來的段落已經開著 | `d1/…/ref-s16-9131102.txt`，8 秒 | 構圖：「one carpenter's wooden hand plane, a smooth rectangular block of pale wood in the left foreground」→ 手與刨子縮到畫左下角、平拿、上面那句全木中式刨。道具句：「the only tools … and a wooden plane; no knife, no sword, no axe, no scabbard and no weapon …」→「牆上只有一把平掛的手鋸；石木匠兩手空著」。動作：「yanks the door wide open, plants himself … jabs one thick finger」→「門第一秒已經在開，他一面說一面瞪畫外左的人、粗手指往畫左的巷子用力一戳、手臂打直」；前景的手不動照舊；不笑句照舊 | 不換 | 沒有刨子道具圖，只能靠文字；「carpenter's plane」這個詞本身仍可能把模型拉回現代台刨（d1 同一個詞 s14 畫成素木塊、s16 畫成鐵刨），挑片先看左下角 |
| s14（B） | 丟出來的是一塊素木塊，不像刨子 | `d1/…/ref-s14-9131101.txt`，6 秒 | 動作：「one carpenter's wooden hand plane, a smooth rectangular block of pale wood comes tumbling …; the shoes jerk back half a step」→ 第一秒同一句全木中式刨翻著從畫右上掉下、看得到橫把，平摔進刨花堆、刨花飛起，落地後把手兩頭與木楔朝上留到最後一格；拿掉鞋子退半步（一鏡一個動作）。補「The set picture fixes the place only, never the mood.」（這鏡沒有人，base 沒有這個分隔字串，refine-prep 需要；寫法照 e911 s18） | 不換 | 3 秒插鏡，翻滾中把手可能看不清楚，主要靠落地後那 2 秒；音效太輕是剪接的事（報告第 10 節），不在這批 |
| s20（B） | 說狠話時和氣地露齒笑；手只扶門把、沒有要關門，下一鏡「先別關」沒前因 | `d1/…/ref-s20-9131101.txt`，8 秒 | 構圖：「one hand on the edge of the door」→ 打開的門板在他畫右、左掌平貼門緣。表情：「scornful: … a cold sneer at one corner of his mouth, teeth barely showing」→ 冷臉逐部位寫（眼瞇成縫往旁斜看、眉壓下、下巴抬、嘴角用力往下、嘴唇薄而緊、鼻子短哼一聲），動作句後加整鏡不笑句。道具句同 s16 改成正面寫。動作：「starts pushing the door shut toward screen left; the young man … lowers the wooden plane」→ 他把重心壓在左掌、把厚木門板往畫左推過門洞，最後一格門擋住右半個門洞與他右半身、只剩臉和左肩在縫裡、門還在動；前景許硯不動、兩手垂在畫框下（拿掉第二個動作與刨子） | 不換 | 門板的方向是照 s21（唐小棠按住他畫右的門板）寫的，跟現在 s20 的門在他畫左相反；模型若照場景圖把門畫回左邊，推的方向會亂。冷臉可能被讀成平臉而非冷笑（分鏡允許冷笑，這裡選擇寧冷勿笑） |
| s28（B） | 舉的是淺色新板、潦草大葉，拿的是毛筆樣的筆；全程咧嘴笑到大笑 | `d1/…/ref-s28-9131101.txt`，8 秒 | 構圖：「holding up the long planed board … earnest and sure: brows level, eyes bright, … no smile」→ 左手舉一塊斜向陽光的舊木板，寫死成 s27 那塊：深褐、風化、木紋深、手臂長兩掌寬、細炭線方框裡一排密線、正中一片指頭大的柳葉；右手一根指頭長的黑炭條、拇指和兩指捏著；表情改成皺眉有一道細紋、眼睛專注瞇著盯石木匠、下顎緊、字間嘴抿平、嘴角平直不動（拿掉 bright、sure）。「the board is … not a screen and not a blind; … no weapon …」→「這塊深色木板就是工作台上那塊舊板；牆上只有一把平掛的手鋸」。動作：「tilts the board up … and taps the little leaf twice」→ 板從第一格就斜舉著，唯一動作是炭條在柳葉上點兩下、再把板穩住、眼睛回到石木匠；整鏡不笑照舊 | 不換 | base 已經寫了整鏡不笑仍然大笑，這次只多了具體的冷靜臉；若兩支還笑，照 WRITING 第十一節改鏡頭設計（例如側臉或收到手與板的近景），不再改字 |
| s08（B） | 石桌上帳冊一疊變並排兩疊、書口有一排像字的黑紋；外衣袖口白毛邊，跟 s02、s05、s10 的灰外衣不同 | `fix1/…/ref-s08-9131201.txt`，6 秒 | 構圖：「a tall stack of ten thread-bound account books」→「桌中央正好一疊十本、一整齊的堆，書口是素淡黃紙，其餘桌面空著」。外衣：「an old plain grey cloth outer coat」→「舊的薄單層灰布外衣敞著穿，直袖口是同一塊灰布反摺」（照 s10 畫格的樣子）。動作：「leans over … traces a square … in the air …; after the last word he taps the top book once …」→ 一面說一面走到石桌前、兩手平放在那疊旁邊的空石面上、往外滑開再收回比出竹簾大小，手停在桌面到最後一格、那疊書不動（兩拍改一拍） | 不換 | 審片改寫句要唐小棠在右前景，但真人版改動（script.md 第 204 行）已把 c08 改成許硯單人中景、她在畫外左，照分鏡不加人；「walk back」改成 steps up，因為 6 秒內走加比劃可能只做一個 |

## 三個檢查（2026-11-21）

- `polish-build.py 13`：0 錯，5 鏡 10 支 72 秒。第一次跑 s14 報 `'never the mood. ' occurs 0 times`（無人插鏡的 base 本來就沒有），補分隔句後通過。
- `preflight-prompts.py …/fixp/colab-jobs.json`：0 error、0 warning。
- `h3r.sh check --manifest …/fixp/colab-jobs.json`：0 error、0 warning。

## 挑片時看

- s16、s14：刨子是不是全木、有沒有橫把，左下角有沒有金屬亮面或前後兩個把手；s16 石木匠有沒有戳手指、有沒有笑。
- s20：整鏡有沒有露齒或嘴角上揚；門有沒有真的往他身前關、最後半掩；門板在他哪一邊（接 s21）。
- s28：板是不是深色舊板、線細；手上是炭條不是毛筆；逐格看有沒有笑（146–147 秒對應的段落）。
- s08：只有一疊、書口有沒有長字；袖口是不是灰布不是白毛邊。
