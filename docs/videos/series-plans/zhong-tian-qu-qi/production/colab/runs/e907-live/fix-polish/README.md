# 第 7 集真人版 fix-polish：上架前精修重拍（s20、s08、s07）

2026-11-21 寫好，**還沒送出**。依 `/root/mokaair-work/review-zt/RETAKE-BRIEF.md`。來源：`review-zt/consolidated/retakes.json` 裡 e007 的 tier B 三鏡（本集沒有 A；三筆的英文改寫句都是「待補」）。
`reports/e007.md` 是濃縮版，`ep/e007/review/REPORT.md` 不存在，所以照中文描述、畫格條 `ep/e007/review/shots/s07|s08|s20.jpg`、證據格 `x/m_s07.jpg`、`x/s20_124.jpg`，
加上本集前幾輪的挑片紀錄（`fix1`、`fix2`、`fix3/review-picks.tsv`、`pick-review.md`、`cut-review*.md`）自己寫。
種子 9079101／9079102，960×544 Ref2VA，每鏡兩支、各 6 秒，共 6 支、36 秒草稿。參考圖三鏡都照 base（`pictures: null`）。

base：`picks.json` 沒有 `motion_from` 欄，照 `draft` 路徑認：s07 是 `d1/out/s07-9071102.mp4` → `d1/prompts/ref-s07-9071102.txt`；
s08、s20 是 fix3 → `fix3/prompts/ref-s08-9071402.txt`、`fix3/prompts/ref-s20-9071401.txt`。

| 鏡 | 審片問題 | base | 改了哪些句子（舊→新） | 換圖 | 拿不準的 |
| --- | --- | --- | --- | --- | --- |
| s20 | 轉折句「爛手？那我現在就洗給大家看，看清楚了。」整鏡拍唐小棠後腦勺（錄音 a18，比她原聲小 2–4 dB）；正面五位小姐同一張臉直視鏡頭；推袖讀成捏衣領，而且 s21、s22 袖子又垂回手腕 | `fix3/prompts/ref-s20-9071401.txt`，6 秒 | ① 構圖：背後過肩、她臉出畫 → **視線高度的中近景推到近景，鏡頭在她左側，清楚的側臉朝畫右看人群**，頭頂留空、丸子頭緞帶入鏡。② 人群：前景右邊五位、臉朝她 → **只留三位、在中景遠處虛焦、人小**，寫成三個不同的人（年長長臉、圓臉微胖、瘦小年輕），臉朝她、嘴閉、皺眉懷疑。③ 表情：`no smile at any moment…` → 冷臉逐部位寫：眉往下往中間壓、眼睛瞇成硬的一條線盯著她們、嘴角往下、字間嘴抿薄、下顎咬緊、下巴微抬，最後一字後嘴抿回一條線；說話「冷、脆、嘴動作小」。④ 台詞：背對不出聲 → **露臉說原聲**（稿子原句＋面向對方的系列句）。⑤ 動作：先推右袖再推左袖（兩個動作）→ **一個動作：右手把那塊小白皂（接 s19 遞皂停在半空）從腰舉到下巴高、朝人群、離臉一前臂遠，停住**。白皂寫死比手掌小、一指厚 | 無（側面角度圖 `tangxiaotang-angle-b-l1` 正好是她側臉，留著） | **改成原聲**：剪接表要把 s20 從錄音（a18）改成片段原聲（`clip_voice`），a18 不用 +3 dB 了；挑片要聽寫逐字核對。**拿掉推袖**是有意的：接 s21、s22 袖子在腕上（上一輪 cut-review-2 第 3 項）；代價是少了「捲袖子要洗」的那一拍，靠台詞與 s21 交代。唐小棠露臉不笑是這集最難的（fix1、fix2 兩輪四支全都笑或正對鏡頭），這次靠嚴格側臉＋逐部位冷臉，仍可能笑；兩支都笑就 KEEP 現在的 9071401 |
| s08 | 「不算買，算試洗。洗一次，不香不要錢。」沒有臉只有手插鏡（錄音 a08）；白皂比手大一倍 | `fix3/prompts/ref-s08-9071402.txt`，6 秒 | ① 構圖：高角度背後過肩、臉出畫、竹筐佔下半 → **視線高度的中近景，鏡頭在她右側，清楚的側臉朝畫左看畫外的秦霜**，胸上、頭頂留空。② 白皂：「palm-sized」→ **小白皂、捏在拇指與手指間、不比四指併攏寬、比手掌小、一指厚、綠葉包著**，動作結尾再寫一次「仍比手小」。③ 表情：逐部位寫冷靜（眉平不動、眼神平穩、眼皮放鬆、嘴角平、字間嘴收成直線、下顎穩、下巴平），拿掉 `no smile at any moment…` 與 `her face stays turned away`。④ 台詞：背對不出聲 → **露臉說原聲**（稿子原句）。⑤ 動作：舉皂晃一下＋平放回筐＋拍筐沿（三拍）→ **一個動作：從腰舉到肩高、朝秦霜、離臉一前臂遠，頂端晃一下停住**；鏡頭固定 → 稿子的慢推 | 無 | **改成原聲**（retakes 的 note 本來就要「重拍改原聲」）：剪接表 s08 改用片段原聲，a08 不用了。拿掉「放回竹筐、拍一拍」：一鏡一個動作；s09 接推車出發，竹筐不在這一鏡也接得上。唐小棠露臉不笑同 s20 的風險（fix1 兩支 2.4 秒起都在笑） |
| s07 | 秦霜拿鋸齒長彎刀、光刃插在腰帶正前、坐在推車把上、帶笑（稿子：柴刀插腰右、站柴堆邊、不笑） | `d1/prompts/ref-s07-9071102.txt`，6 秒 | ① 站位：`low-angle medium shot from beside the handcart wheel of Qin Shuang by the woodpile` → **膝高低角度，她兩腳站在柴堆前的泥地上、重心平均**；場景句拿掉推車在中間與院門（推車不入構圖，免得她坐上去）。② 柴刀：`long narrow iron blade with a slightly hooked tip … held blade-down in her right hand` → **第一格就已插在腰帶右邊：一前臂長的短直刃、暗灰、一條平直刃口、方鈍刀頭，刃朝下貼右大腿外側，纏黑布的木柄立在右胯骨旁**。③ 拿掉否定名詞 `no rolls and no cylinders on the ground`、`no second copy of anyone appears`（改成 `appears exactly once and is the only person`）。④ 表情：`no smile at any moment…` → 逐部位冷臉（眉低平微皺、眼瞇、眼皮沉、目光硬、字間嘴抿成薄直線、嘴角往下、下顎繃、下巴平），台詞說得平、嘴動作小。⑤ 動作：插刀＋扛筐（兩個）→ **一個動作：屈膝雙手抓筐沿，一下甩上右肩，站直、右手扶筐，刀仍在右胯** | 無 | 拿掉「把刀插回去」這一拍（稿子 c07 的動作）：插刀正是上次畫錯的地方（光刃插到腰帶正前），而且一鏡兩動作只會做一個；刀改成開場就插好。刀沒寫刀鞘（稿子「整集不出鞘」但又寫刃口發亮），可能仍是光刃，但位置在右胯、刃朝下。竹筐扛到肩上時頭可能被擋或出畫（d1 有一格擋到） |

## 寫法的決定

- 三鏡都從 base **複製後只改 `Initial composition:` 到 `One continuous shot.` 之間**；header、角色外貌錨句、`never the mood. `、`One continuous shot.`、乾淨畫面句與尾段照舊（兩個分隔字串各一次，`polish-build.py` 已查）。
- 照 e930 fix3 與 e903 fix-polish：只用正面描述、正文沒有 smile 字（唐小棠錨句裡的 `composed and unsmiling` 是 base 原有的，保留）、冷臉逐部位寫、一鏡一個動作（`her one movement:`）、說話面向對方、道具寫死樣子與跟手的大小比。
- 唐小棠兩鏡都用**嚴格側臉**（鏡頭在她側面、臉的高度）：本集紀錄裡她不笑成功的幾鏡都是側臉朝對方；正面或四分之三時兩輪都笑、也會對鏡頭。
- 兩鏡唐小棠的手與臉之間寫「一前臂遠，臉保持清楚」，免得舉起的白皂擋臉。

## 檢查（2026-11-21）

- `polish-build.py 7`：`e907: 3 shots, 6 drafts, 36 s`，0 錯。
- `preflight-prompts.py …/fixp/colab-jobs.json`：第一次 2 個 warning（s08 兩支 `unpictured Qin Shuang`：動作句寫了 `toward Qin Shuang on screen left`，被當成她在畫面裡）；改成 `off screen left` 後 **0 error(s)、0 warning(s)**。
- `h3r.sh check --manifest …/fixp/colab-jobs.json`：0 error(s)、0 warning(s)。

`polish-build.py` 仍有 e903、e909 回報過的兩個毛病（沒改原檔）：`REPO = HERE.parents[6]` 要 `parents[7]`；失敗後重跑會被自己寫出的 `fixp/prompts/ref-*` 判成「seed already used」。
這次用 scratchpad 的副本跑（只改 `REPO` 那一行、`HERE` 釘在原本的 `_scripts`），重跑前先刪 `fixp/prompts/ref-s*-907910*.txt`。

輸出：`~/mokaair-work/videos/zhong-tian-qu-qi-e907-dh/runpod/live/fixp/`（`retake.json`、`colab-jobs.json`、`prompts/ref-s07|s08|s20-907910{1,2}.txt`），片子會出在 `fixp/out/`。

## 拍完要看

- s20、s08：唐小棠逐格看嘴角有沒有上揚、有沒有對鏡頭；臉是不是側臉；白皂有沒有比手大、有沒有擋臉；原聲聽寫逐字對稿。s20 背景三位小姐是不是同一張臉、有沒有看鏡頭、有沒有人穿桃粉。
- s07：刀的形狀（直、短、鈍頭、沒有鋸齒）與位置（右胯、刃朝下）；她是站著不是坐；嘴角有沒有上揚；扛筐時頭在不在畫內。
- 換上新片段後：剪接表 s08、s20 從錄音改原聲（a08、a18 不再用），重量剪點與字幕時間。
