# 第 17 集真人版 fix-polish：上架前精修重拍（2026-11-21）

審片來源：`/root/mokaair-work/review-zt/consolidated/retakes.json`（e017，tier A 2 鏡、B 5 鏡）與 `reports/e017.txt`。
種子 9179101／9179102，960×544 Ref2VA。7 鏡 14 支、共 96 秒（每種子 48 秒）。只寫提示詞與 spec，沒有送出。
base 一律是 `picks.json` 現在用的那支的提示詞；picks.json 沒有 `motion_from` 欄，從 `draft` 路徑判斷七鏡都出自 `d1/`，兩個種子的 d1 提示詞逐字相同（cmp 確認）。

**參考圖要注意**：`d1/retake.json` 寫的院子圖是 `set-xujia-yuan-l3`，但實際送 Colab 的 `d1/colab-jobs.json`（與 detached.json）是 `set-xujia-yuan-huo-l1`（起火版）。
`polish-build.py` 先讀 retake.json，所以 s02、s06、s14 在 spec 裡明寫 `pictures`，沿用實際用過的起火版。

## 燈籠骨架（s39、s40，嚴重）

d1 三鏡（s35、s39、s40）用的是同一句「a ring of blackened bamboo strips the size of two hands」，模型夜裡畫成圓球籠（s35），白天畫成一個斷開的圈（s39、s40）——「ring」被照字面畫了。
新道具句照 s35（與 s26）實際畫出來的樣子寫：頭那麼寬的圓球籠、八根往外弓的焦黑竹骨上下收攏、腰上兩道細圈、骨間全空、站在掌寬的深色圓木底座上，底座**正面**嵌一片拇指甲大的圓銅片（一圈凸起素環圍著方孔）。
不寫 paper、ring of strips、characters。這一句在 s39、s40 **逐字相同**（647 字元，已比對）。兩鏡都再加「the lantern stays dark and unlit」。

## 每鏡

| 鏡 | tier | 審片問題 | base | 改了哪些句子（舊→新） | 換圖 | 拿不準 |
| --- | --- | --- | --- | --- | --- | --- |
| s39 | A | 燈籠變斷開的黑圈掛銅片；背景是竹棚 | `d1/prompts/ref-s39-9171101.txt` | 道具句→上面的固定句；「in his right hand at the bottom of the frame」→ 整個燈籠舉在下巴高、畫右、全在框內，眼看底座銅片；表情逐部位（眉壓低皺緊、眼瞇、咬牙、嘴抿成線）；背景「only the pale pine frame」→ 虛焦的一根平滑剝皮淺黃松木圓柱、土牆、天；動作「手一緊＋側瞄一眼再收回」→ 只剩手指慢慢收緊到指節發白、眼睛一直在銅片上 | 照 base（angle-a、angle-b、`set-zhifang-gujia-chen-l1`） | 審片建議送一格 s35 當道具參考圖，但 refs-live 沒有燈籠圖、本次不能動 refs-live，只能靠文字；若兩支仍不像，下一步是從 s35 截一格做 `prop-` 圖再重抽。場景圖本身有綠樹與紫花（s36/s37/s40 也有），沒寫否定句去掉 |
| s40 | A | 舉到眼前的圈認不出是燈籠、銅片像螺旋沒方孔；透過圈直視鏡頭 | `d1/prompts/ref-s40-9171101.txt` | 道具句同 s39；起始：燈籠在胸前、身體右側（畫右），身體與臉四分之三朝畫右；動作「舉到眼前＋盯銅片＋握拳」→ 慢慢舉到臉旁眼高（畫右）停住，臉四分之三側向燈籠，眼盯底座銅片到最後一格（握拳拿掉，已在 s39 做） | 照 base（portrait、angle-a、angle-b、`set-zhifang-gujia-chen-l1`） | 審片句寫銅片「under the base」，那樣看不到，改成底座正面 |
| s18 | B | 唐小棠說完「全沒了」卻乾淨帶笑；竹簾變長席＋葉子 | `d1/prompts/ref-s18-9171102.txt` | 錨句拿掉「her resting face composed」；她「knees drawn up, drained: eyes lowered」→ 雙臂抱膝、袖上灰、右頰一抹灰、低頭，眉心上提擠緊、眼紅含淚、嘴抿嘴角下拉、下巴繃著抖；竹簾「flat rectangular mat … willow-leaf」→ s13／s26 畫出的方形硬竹簾、木邊、中間深色菱形，第一格已立在她膝前、他兩手扶上角；許硯「steady/level」→ 眉低而定、眼盯她臉、下顎緊；動作「立簾子再轉頭」→ 只說話、在「石叔」轉頭朝畫右；她只抬一下眼、嘴角仍下拉到最後一格；說完抿嘴等 | 照 base | 全片沒有任何 smile 字（照 fix3／e910 做法）。竹簾的「柳葉」改成「菱形」是照前後鏡多數畫出來的樣子（審片中等 9 的建議）；s32 膝上的簾子不一樣這次不處理。提示詞 970 字，接近 1000 字上限 |
| s14 | B | 被抓的手臂伸向畫右，卻回頭看畫左 | `d1/prompts/ref-s14-9171102.txt` | 錨句與構圖的髮型換成 s13 fix2 的散髮句；構圖加：身體朝畫右的火、頭從左肩轉回臉四分之三朝畫左；左臂往畫左緣拉直，畫左緣一隻灰藍袖的手第一格已握住她左前臂（接 s13 fix2 的「his right hand already holding A-ling's left forearm」），人數句改成「只多一隻手」；動作「回頭看＋左臂沉出畫」→ 只剩肩膀放鬆、拉直的左臂放鬆下沉，手仍鬆鬆握著；嘴閉著（系統聲錄音） | `aling-angle-a-l1` → `aling-loose-angle-a-l1`（散髮版，s13 fix2 同一張）；院子照實際的 `set-xujia-yuan-huo-l1` | 畫左緣的手可能被畫成牽手或多一個人；審片說不能水平翻轉，所以沒翻 |
| s25 | B | 前景背影換衣服、有鬍子、插簪；韓伯沒橫杖攔 | `d1/prompts/ref-s25-9171101.txt` | 加二牛錨句（照 s24，寫 smooth-shaven、頭頂一個素圓髻）並點名；背影改寫成褐色交領短打捲袖布帶、扁擔在右肩、前端掛一隻空木桶、面朝畫左；韓伯竹杖寫成淺黃褐、跟他一樣高，起始直握在右手；動作「杖一直橫在胸前」→ 第一秒把竹杖橫過來兩手平舉在二牛胸口高度攔住、到最後一格；表情改成眉壓低、眼盯二牛、下顎繃；說完抿成硬線看著二牛 | 加 `erniu-angle-b-l1`（側臉朝畫左，正好接背影朝畫左；不送正面圖，免得轉過臉來） | preflight 的 `prop`（carrying pole）warning 不改：扁擔寫在構圖裡、不在外貌錨句，是這鏡要的道具，base 也有同一個字。仍可能看到二牛側臉 |
| s02 | B | 竹竿平舉對鏡頭像端槍、對鏡頭嘶喊 | `d1/prompts/ref-s02-9171102.txt` | 構圖加：半背對鏡頭、身體朝畫右的牆與火，竹竿高舉、從手陡斜往畫面右上伸進牆外著火的草頂與煙、近端在胯邊，頭從左肩轉回、側臉朝畫左；動作「先捅再轉頭喊」→ 朝畫左喊的同時往上捅一下，竿頭一直指著右上的火；說完下顎繃住；運鏡慢推→固定鏡頭（審片句） | 院子照實際的 `set-xujia-yuan-huo-l1` | 台詞是錄音 a01，但畫面上他照 base 開口喊（全景，對嘴容錯大），剪接照舊鋪錄音 |
| s06 | B | 三個村民同臉同衣排排站帶笑、小禾張臂擺拍、秦霜手臂指錯邊 | `d1/prompts/ref-s06-9171101.txt` | 拿掉小禾的錨句、構圖與「不說話」句，屋門口寫成空著；秦霜一腳踩井沿、半背對鏡頭、身體朝畫右，右臂直伸向畫面右上的火，頭從左肩轉回側臉朝院門喊；三村民「站著不動」→ 第一格已從院門彎腰提桶趕向井，逐一寫不同（灰鬍瘦老翁灰衣、深藍包頭壯婦褐衣、比較矮的瘦少年補丁黃褐衣），臉側面、眉皺眼睜嘴緊；動作「手臂從井掃向火」→ 手臂一直伸著朝院門喊，村民繼續趕路 | 拿掉 `xiaohe-portrait-l1`；院子照實際的 `set-xujia-yuan-huo-l1` | 拿掉小禾是照審片句「No child in the doorway」；分鏡原本有她在門口，請協調者確認可以。三個沒參考圖的人仍可能長得像 |

## 檢查（2026-11-21）

- `python3 -I _scripts/polish-build.py 17`：7 鏡、14 支、96 秒，0 錯誤
- `preflight-prompts.py …/fixp/colab-jobs.json`：0 error(s)、2 warning(s)（s25 兩支的 `prop` carrying pole，理由見上表）
- `h3r.sh check --manifest …/fixp/colab-jobs.json`：0 error(s)、0 warning(s)

輸出在 `~/mokaair-work/videos/zhong-tian-qu-qi-e917-dh/runpod/live/fixp/`（`colab-jobs.json`、`retake.json`、`prompts/ref-sNN-917910{1,2}.txt`）。
