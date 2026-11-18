# 第 32 集真人版 fix3：s21、s26、s26b 泥的重拍計畫（未送出）

2026-11-18 寫。重拍 s21、s26、s26b 三鏡：許硯臉上和袍子上的泥（s26／s26b 連扛他的人的背上也有）被畫成一片片會反光的金箔色楓葉狀貼片，
REVIEW 3 的調色（`gold.py` 遮罩）改得了顏色、改不了形狀（`../review3-plan.md` 第 0、4 節；對照圖 `e932r3/img/gold_s21a.jpg`、
`gold_s26.jpg`、`gold_s26b.jpg`）。站主：品質為主、該修就修。**只寫好、跑過免費檢查，沒有送出任何生成**（Colab、RunPod 都沒開，
沒用站台 TTS，沒 commit）。

依據：`../fix1/`、`../fix2/` 的寫法；`../picks-merged.tsv` 與 `../review3-trims.tsv` 這三鏡的種子與剪點；`../review3-plan.md` 第 0 節；
`writer-tools/e032-r2/r2.py` 的 `XU_MUD` 與 s21／s26／s26b；稿子 `docs/videos/zhong-tian-qu-qi-e032-r2/script.md` c21、c25–c26；
`hailuo/edit-dh-e932-live.json` 這三鏡的 `clip_af`、`vf`、`panel_*`；聖經 `r2-bible-e031-e040.md`〈人物〉許硯列「泥寫在袍子與臉頰一大片，不寫小點」；
route-a.md 最後幾十條；任務檔的歷集教訓。

## d1 為什麼長出貼片

d1 這三鏡的提示詞**沒有** spots／patches／flecks／smears 這類字，貼片來自 r2.py 共用的 `XU_MUD` 跟光線句：

| d1 的字 | 為什麼畫成貼片 |
|---|---|
| `the robe, his arms and his face caked with wet yellow mud` | `caked` 是乾掉結成的一層殼，模型畫成會裂開、一片片翹起的硬塊；`yellow mud` 是黃色 |
| `low orange evening sun from the left, long shadows ...`（地點句）、`in the low orange light`、`the low orange evening light stays unchanged` | 黃色的泥被橘色斜陽正面打亮，就成了金色、帶高光的箔片 |
| s26／s26b `his muddy cheek against the dark brown cloth of a jacket's back` | 「沾泥的臉頰貼著背」讓泥也印到扛他的人背上（gold_s26b 背上的貼片） |

r2.py 那行的註解寫了「large patches」——`patches` 沒進提示詞，但聖經要的是一大片，不是一塊塊。

## 三鏡共同的改法

| 改什麼 | 新寫法（英文原句在 `mkspec.py`） |
|---|---|
| **泥：一大片濕深褐泥糊，均勻、霧面** | `one broad even coat of wet dark-brown mud paste over his forehead, cheeks and jaw, smooth and matte like the soil of the field and darker than his skin, his eyes, nose and lips left clean` |
| **衣服上的泥：大片深褐濕痕** | `the whole front of his robe and both sleeves soaked through with one wide wet dark-brown mud stain, the cloth dark and heavy with it, his hair matted with the same dark-brown mud` |
| **光：泥在陰影側，暖光只在背景** | 太陽仍在左邊低處（跟這場其他鏡同一個方向），但許硯在柔和均勻的陰影裡；結尾句 `the low orange evening light stays unchanged` 改成 `the soft even shade on his face stays the same to the last frame.` |
| 拿掉的字 | `caked`、`yellow mud`、`low orange`（三處）、`his muddy cheek`；任何 `gold／golden` 都不寫；也不寫否定名詞（不寫 no flakes／no gold／no glitter，審查建議裡的那串否定改成上面的正面描述） |
| 不笑 | 三鏡都加本季 NOSMILE（d1 s26 1101 嘴角放大看微微上揚） |
| 不動的 | 圖（xuyan-portrait-l1、angles/xuyan-angle-a-l1、場景裁切）、台詞與錄音安排、動作句、慢推、秒數都照 d1；基底是 d1 9321101 實際送出的提示詞與工作 |

## 各鏡

| 鏡 | 秒數 × 支、種子 | 構圖與動作（照 d1 選定那支） | fix3 另外改的 |
|---|---|---|---|
| s21 | 8 × 2：9321401／9321402 | 俯拍近景、仰躺在坑邊裂土上、胸以上；嘴唇乾白、眼睛半閉、臉朝天；片中原聲「沒……沒水。再往下一丈，也許就有……」說完頭往一邊歪（d1 選 9321101 0.500–8.000，原聲 0.90–7.02，`clip_af` 升 1.08） | 地點句的光改成 `the low evening sun far at the left behind the earth heap, the long cool shadow of the heap lying over the near side of the pit`；`cracked dry yellow furrows ... in the low orange evening light` 改成 `cracked dry furrows ... all of him and the earth around him in the same soft even shade light`。畫面裡沒有暖光。 |
| s26 | 8 × 2：9321403／9321404 | 近景、許硯側臉靠在扛他的人肩背上、眼皮撐開一條縫看著面前的空氣、嘴閉（d1 選 1101：側趴，不是稿子的倒掛；剪到 6.5 秒，鋪系統 a25 與兩行面板） | **扛法照 s25（fix1 9321202：橫在兩肩、頭與手臂垂在畫右）寫死**：`lying limp across the shoulders of the one who carries him, his body crosswise behind her neck, his legs beyond the left edge of the frame, his head and one limp arm down past her shoulder in the right half of the frame, his face turned sideways to us, his cheek resting on the dark brown cloth of her jacket's shoulder, her jacket plain even dark brown cloth all over`；d1 的 `slung head down over a shoulder ... his face upside down` 拿掉（選定那支本來就不是倒掛）。人數：`his is the only face in the frame, exactly one head and one face, his` ＋ d1 的「只露扛他的人深褐短衣的背」。背景：`the long drooping branches of a willow, the warm low sun only on the willow and the sky far behind him; his face, his robe and the mud on them in soft even shade.`（`hanging` 改 `drooping`，`yellowed` 拿掉） |
| s26b | 6 × 2：9321405／9321406 | 近景、同一姿勢、眼睛一條縫、眉頭微收、嘴閉不笑（d1 選 1102；剪到 5.833，鋪心裡話 a26） | 跟 s26 **同一句扛法**，兩鏡與 s25 接得上；d1 另一支 1101 同一畫面兩張許硯的臉，所以同樣寫死 `exactly one head and one face`；背景與光同 s26 |

## 檔案與指令（2026-11-18，全部免費的本機檢查）

- `mkspec.py` → `spec.json`：三鏡的 fix3 replace（每句先 assert 在 d1 提示詞裡剛好一次）、各自的兩顆種子、秒數。
- `mkjobs.py <live>/fix3` → `<live>/fix3/prompts/ref-sNN-SEED.txt`、`retake.json`、`colab-jobs.json`。不用 `retake.py`：它一次只吃一組種子，這次三鏡各有自己的種子；
  基底取 d1 的 9321101 工作與提示詞（d1 的 drop_pictures／swap／replace 已經在裡面），圖的路徑從 `/home/user/zt-work`（symlink）改成這個 checkout 的絕對路徑。

```
python3 -I mkspec.py                                    # 3 shots -> spec.json
python3 -I mkjobs.py <live>/fix3                        # 掃描 0 命中；colab-jobs.json 6 支、44 秒
python3 -I ../../_scripts/preflight-prompts.py <live>/fix3/colab-jobs.json            # 0 error(s), 0 warning(s)
python3 -I .agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix3/colab-jobs.json   # 0 error(s), 0 warning(s)
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest <live>/fix3/colab-jobs.json  # 0 error(s), 0 warning(s)
```

`<live>` = `/root/mokaair-work/videos/zhong-tian-qu-qi-e932-dh/runpod/live`；輸出會放 `<live>/fix3/out/sNN-93214xx.mp4`。

mkjobs 的掃描（命中就 exit 1）：
- 沿用 fix1／fix2：否定名詞 0、兵器字 0、`never the mood. `／`One continuous shot.` 各一次、會長字的字（含 open）0、掛著／鎖／攤位的字 0（所以垂柳寫 drooping）、
  `not smiling` 與 NOSMILE 以外的笑字 0、點名不在畫面的人 0、標頭與 `<Picture N>` 對得上、路徑都是絕對路徑且檔案存在。
- **fix3 的泥**：會長小片泥的字 0（spots、patches、flecks、flakes、specks、smears、smudges、streaks、splashes、splatters、blotches、dots、daubs、dabs、clumps、crumbs、
  chunks、crust、caked、leaf／leaves、petals、drops；只放過袍子的 `scholar's robe patched at one elbow`，身分句與構圖各一次）；反光字 0（glitter、sparkle、shiny、
  glossy、glint、gleam、shimmer、metallic、foil、reflect、sheen）；`gold／golden` 全文 0；`yellow／orange／amber／honey／sunlit／sunlight／ochre／bronze／copper`
  跟 `mud` 同一個子句（以 `.` `;` `:` 切）0；大片泥句剛好一次；d1 的 `caked`、`yellow mud`、`low orange`、`slung head down`、`upside down`、`hanging branches`、
  `his muddy cheek` 都不在；s26／s26b 有 s25 的扛法與 `exactly one head and one face`；d1 的台詞、動作句、慢推、圖、秒數都在；種子 9321401–9321406。
- 拿 d1 的 s26 提示詞試過這個掃描：抓到 `caked`，以及 `yellow` 跟泥同一子句——就是這次要拿掉的字。

**預估**：6 支、44 秒（s21 16、s26 16、s26b 12）。照第 31 集實測（556 秒 ≈ 2.59 小時、約 26 CU）按秒數約 0.2 小時、約 2 CU，
加 Colab 冷啟動共約 0.35 小時、**3–4 CU**（約 US$0.3–0.4）。選定之後還要精修這三鏡（refine，1312×736、σ0.5、10 步），照 fix1／fix2 的精修另計。
要省可以先各跑第一顆（9321401、9321403、9321405，22 秒）看泥。

**跑在哪個 session**：Colab session **`zt-live3`**（協調者指定）。manifest 本身不綁 session，送出時在指令帶 `--session zt-live3`；
同一個 session 一次只跑一件事（route-a 2026-11-09），送之前先確認 zt-live3 上沒有別的工作在跑（第 32 集精修若還在跑就排在它的行程號後面，
`while kill -0 <PID>; do sleep 30; done`）。背景執行帶 `timeout: 7200000`，並掛一個 run_in_background 的等待。

## 送出後挑片要看的

- **泥**（第一優先）：放大原尺寸逐 0.5 秒看，臉頰、額頭、下巴是**一整片**均勻的深褐濕泥，袍子前襟與兩袖是**一大片**濕掉變深的痕；
  沒有一片片邊緣鋸齒的楓葉狀／箔片狀貼片、沒有金色或亮橘的高光；扛他的人背上乾淨、同一種深褐。濕泥若有一點自然的濕光可以接受，像金屬箔就不行。
- **臉**：陰影裡仍認得出是許硯（定妝照的眉眼）；眼、鼻、嘴沒被泥蓋住；三鏡都不笑（s26 嘴角特別看）。
- **s21**：片中原聲整句在、對嘴；說完頭往一邊歪在框內；能用的長度要包住原聲（d1 是 0.90–7.02）。暖光沒了，跟 s20、s22 的金色斜陽比會冷一點——剪接看接不接得上，
  不行就只在調色把整鏡往暖拉一點（整鏡均勻的暖不會再長出貼片）。
- **s26／s26b**：扛法跟 s25 fix1 9321202 一樣（橫在兩肩、頭與一條手臂垂在畫右）、兩鏡彼此接得上；**畫面裡只有一張臉、一顆頭**（放大看邊緣有沒有第二張許硯或扛他的人的臉）；
  s26 眼皮撐開一條縫，s26b 眉頭微收；能用的長度 s26 至少 6.5 秒（a25 c1.00–4.59、面板 c0.90 起 5.6 秒、開箱聲 c4.75）、s26b 至少 5.833 秒（a26 c0.60–5.13）。
- **選定後剪接要跟著改**：`hailuo/edit-dh-e932-live.json` 的 `vf` s21／s26／s26b 是 REVIEW 3 的金色泥遮罩，框是照 d1 的畫面手讀的，換片段後要**拿掉**（套在新片上會吃到皮膚與袍子）；
  s26 的 `panel_y`／`panel_from` 與開箱音效 c4.75／c4.85 照新片重核；s21 的 `clip_af` 升調照原聲重量；`picks-merged.tsv` 與 `review3-trims.tsv` 這三列換成新種子與剪點。
- 三鏡都不行時：picks-merged.tsv 留著 d1 的選擇（s21 9321101、s26 9321101、s26b 9321102）加 REVIEW 3 的遮罩。再下一步就是照第 15 集「改字兩次不成就換做法」：
  泥只寫在袍子上、臉寫成乾淨蒼白（稿子「滿臉泥」改由袍子交代），或先畫一張滿臉泥的許硯定妝照當參考圖。
