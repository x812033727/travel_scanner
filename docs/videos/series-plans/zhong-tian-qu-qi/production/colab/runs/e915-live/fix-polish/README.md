# 第 15 集（e915）上架前精修重拍：s21、s25、s42

2026-11-21。審片 `review-zt/reports/e015.txt` 第 1–3 項、`consolidated/retakes.json` 的 tier B 三鏡（本集沒有 A）。種子 9159101／9159102，
每鏡兩支 960×544 Ref2VA。`python3 -I ../../_scripts/polish-build.py 15` 寫出 `runpod/live/fixp/`（6 支、44 秒）。只寫提示詞，沒送出任何工作。

**s21、s25 的犁是同一句**（站主 2026-11-21：兩鏡要同一個樣子）。兩支提示詞裡這一段一字不差，兩鏡也都送 `prop-quyuanli-l1`
（s21 是 `<Picture 4>`，s25 是 `<Picture 2>`；指向圖的那句另外寫，所以描述本身不帶圖號）：

> one curved-beam plough of dark weathered matte brown wood, about as long as a man is tall: a short flat wooden sole lying along the ground, one small pointed share of dull black iron no bigger than a man's hand fitted on the sole's front tip, the only metal on the whole plough, and one long wooden beam that rises from the back of the sole and bows backward in one smooth deep arc like a drawn bow up to waist height, its top end worn smooth and polished as the handle

形狀照道具圖（一根從短犁床後端往上彎的轅、頂端當犁把、前端一個小鐵犁頭），不另寫橫的犁把（s27 鏡尾出過 T 字把）。

| 鏡 | 審片問題 | base | 改了哪些句子（舊 → 新） | 圖 | 拿不準的 |
| --- | --- | --- | --- | --- | --- |
| s21 | 二牛肩上的犁頭是比上半身還大的斧頭形鐵刃，像斬首大斧；跟 s22、s25、s26 不同 | `fix2/prompts/ref-s21-9151302.txt`（8 秒） | fix1 寫字、fix2 加道具圖，兩輪犁頭都在肩上變大斧，照 WRITING 第十一節「改字只改一次」改**鏡頭設計**：舊「兩人各把一頭扛在左肩、犁頭那端在二牛肩上」→ 新「犁斜著抬：石木匠在後把磨亮的轅頂扛在左肩，彎轅往前往下到犁床；二牛在前左手往後提著犁床在左胯邊，小鐵犁頭在胯的高度朝畫左」。犁的描述換成上面那句。舊「從田埂走下來」→ 新「已經在田埂腳下的田裡，由右往左走」（少一拍）。舊「從肩上卸下、立在身旁」→ 新「二牛把犁床放到土上、石木匠把轅從肩上拿下，犁側面立在土上、他左手搭在轅頂」。`nothing else in their hands` → `the plough the only thing in their hands`。台詞、二牛笑、石木匠閉嘴不變 | 沿用 base（二牛兩張、石木匠、`prop-quyuanli-l1`） | 稿子寫「扛」，現在是一個肩扛、一個手提的「抬」；犁頭離地近、在畫面下半，應該不會再讀成斧頭，但斜抬的姿勢模型可能畫不穩（犁床從二牛手上滑開）。a21 錄音照舊，二牛嘴照樣動 |
| s25 | 片名那一鏡：犁幾乎沒前進、秦霜走在犁旁邊原地踏步、犁前面已有一道溝；犁是直桿＋藍鋼斧頭；屋後像電線桿；臉較成熟、手臂是黑護腕 | `fix1/prompts/ref-s25-9151201.txt`（8 秒） | 舊「鏡頭在田邊跟著她走（tracking）」→ 新「低機位固定（`The camera holds a static shot.`），她從畫右三分之一出發，推到畫左三分之一」，所以前進看得見；舊「前方田是平的」→ 新「從犁頭到畫左緣是整片沒翻過的稻茬，從畫右緣到她靴子是一道新溝」。舊犁的那串描述 → 上面那句，並寫「整架犁在她身前、她走在溝裡、兩手握轅頂」；推的句子加 `one weighted step after another`、「人跟犁一起從右三分之一走到左三分之一」。背景舊「low tiled farmhouses」→ 新「草頂與瓦頂的矮屋在柳樹間、屋頂上方的淡天空開闊空曠」。袖子那句加「前臂從手肘到手腕露出皮膚」、臉加「二十一歲的年輕臉」 | **加 `prop-quyuanli-l1`**（`<Picture 2>`，header 改成兩張） | 固定機位對全景走路是新寫法，可能走得慢；電線桿只能靠背景改寫減少，若還出現就在精修時加柔化（審片給的座標 x 1090–1130、y 170–300 會不一樣，要重量）。審片英文句的 `no poles, no wires`、`She does not smile` 沒有照抄（否定名詞會被畫出來）；封面要換成新的一格 |
| s42 | 結尾鏡：紙是糊白片（蓋假字的柔化）；賴三站到橫木這一側、貼在許硯與唐小棠中間；臉比 s38、s40 老；紙捆變圓麻袋；接不上第 16 集 | `d1/prompts/ref-s42-9151102.txt`（6 秒） | 舊「past the oilcloth bundle…on screen right behind the log Lai San」→ 新「左下前景一輛獨輪車，車上一捆扁方油布紙捆（十字捆繩、方角、跟車同寬、一拃厚）；橫木從畫面中間橫到右緣，後面全是遠側；賴三在畫右、橫木遠側，年輕光滑的二十八歲臉」。家丁「更後面、小、虛焦、臉在陰影裡」。許硯舊「左手搭紙捆、右手垂著、在車頭靠近橫木」→ 新「站在車把後、兩手握兩根車把」（稿子 c42）；冷臉加眉壓低、嘴抿成一條、嘴角往下。唐小棠舊「在兩人之間的車旁」→ 新「畫面最左、緊貼許硯左肩後半步，許硯在她與橫木之間」。紙舊「對摺的白紙、空白背面朝我們」→ 新「摺兩次、手指長的粗黃小紙條，平滑的摺面朝我們，小小地夾在指間」，賴三「整鏡在橫木遠側，探身把紙條伸到紙捆前端上方停住」 | 沿用 base（賴三、許硯兩張、唐小棠兩張、`set-shiqiao-l2`） | 紙條仍可能長字（小、黃、摺起來是減少面積，不保證）；三個有名字的人加兩個家丁，家丁寫成虛焦。賴三臉變老若是光線造成，字救不太到。第 16 集 s01 是反打（賴三背對、在畫右前景），左右站位本來就跟這鏡對不齊，沒有為它改 |

## 檢查（2026-11-21）

- `polish-build.py 15`：3 鏡、6 支、44 秒
- `preflight-prompts.py …/fixp/colab-jobs.json`：0 error(s)、0 warning(s)
- `h3r.sh check --manifest …/fixp/colab-jobs.json`：0 error(s)、0 warning(s)

字數：s21 1029、s25 950、s42 1161 字（第 14 集 polish 的 s40 是 1179，preflight 沒有擋）。
