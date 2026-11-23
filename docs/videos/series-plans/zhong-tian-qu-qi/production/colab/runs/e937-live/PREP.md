# 第 37 集重製版 r2（e037-r2，內部 937）真人版開拍前置

- 2026-11-23，第 37 集前置代理。**沒送任何生成**（Colab、RunPod 都沒開，`zt-live2`、`zt-live3` 都沒碰）、**沒有付費圖**、沒 commit、沒改第 33–36 集的檔
  （唯一碰到的共用檔：`writer-tools/e001-r2/build-r2.py` 的 `EN` 加一個鍵 `diaoqi`，舊集逐位元重建不變；refs-live README 加一段）。
  **獨立審稿已套用**（§7；改前的檔在 scratchpad `e937prep/*-before-review.*`）。**站台 TTS 錄音 39／39 錄齊、核對完**（協調者准，§4）。
- 依據：第 36 集前置全套（`writer-tools/e036-r2/{r2.py,review.md,review-independent.md}`、`colab/runs/e936-live/{mkspec.py,spec.json,PREP.md}`（§7 獨立審稿怎麼套、§8 開門圖）、
  `colab/runs/e936/extras.json`、scratchpad `tools/{build936.sh,prep936.sh,rec936-slow.sh,rec936-check.sh,mkhints936.py,fw936.py,f0y936.py,span936.sh,heads936.py}`、`e936d1.sh`）、
  `colab/runs/e935-live/PREP.md` §8（cinema camera）、`r2-bible-e031-e040.md`（拍法 1–43、〈接點〉36→37、〈道具〉〈人物〉〈小角色〉〈場景〉〈原版必修〉第 37 集）、
  任務檔最後幾條教訓、站主 2026-11-21～23 規則（§0）。稿子 `docs/videos/zhong-tian-qu-qi-e037-r2/script.md`（40 鏡）。
- **接點 36→37 照第 36 集定版成片寫**：`/root/mokaair-work/videos/_live-e936/zhong-tian-qu-qi-e936-dh/cut/e936-live.mp4`（200.84 秒）最後 15 秒與 s31–s34 每秒抽一格
  （scratchpad `e937prep/tail/sheet.jpg`、`sheet2.jpg`）：s35 秦霜在後牆頭回頭；s36 從牆頭望遠山，**滿月**、山上一串小火光；s37 阿令在屋門口；
  s38 許硯在畫左（舊灰外衣、左手陶油燈、側臉朝右上望）、唐小棠背影在正中抓他袖子，背景木桶、樹、院門、滿月；s31 **草蓆在樹與井之間的院子中段**。
  圖上的**院門本來就半開：門扇掛在右門柱、往內半開、門洞左半空著**（聖經〈接點〉36→37 的備案一：照圖寫；初稿寫「靠左柱」是反的，獨立審稿必改 1）。s01：二牛從後牆中間的院門朝鏡頭衝進來、樹旁四個流民從蓆上坐起。
- scratchpad = `/tmp/claude-0/-home-user-travel-scanner/31162243-7ed2-5899-b9c2-443c1f2a5c1a/scratchpad`；進度 `e937prep/PROGRESS.md`。

## 0. 站主 11-21～23 規則（PR #2217，`production/OWNER-CHECK-20261122.md`、`tasks/open/2026-11-21-1-30-a-b-140.md` Notes；協調者 2026-11-23 轉達）

| 規則 | 本集怎麼照做 |
| --- | --- |
| 品質優先、該花錢重拍就重拍；能自己決定的自己決定，最後只列站主要決定的事 | 本前置照這個寫：§6 只列要協調者／站主決定的事 |
| 人群聲一律用本集錄音倒放（`colab/runs/_scripts/crowd-murmur.py`；Pixabay 人群床有可辨識的英文字，不用） | s35 壯丁歡呼、s17–s21 流寇的喊殺、s31 巷子：剪接時 `python3 -I crowd-murmur.py 37 <秒>`（39 句錄齊後才能做；本集錄音在 `zhong-tian-qu-qi-e937-dh/audio/`） |
| 音效用真實音效庫 `zhongtian-music-library/_sfx-zhongtian-real-20261121/`（Pixabay＋通過檢查的 Flow）；Flow 提示要寫 sound effect only, no music | 剪接照 script.md〈音樂與音效〉從這個庫挑；庫裡沒有的（石灰煙炸開、刀鞘敲手腕、槍挑刀）列給站主用 Flow 做，提示照寫 `sound effect only, no music` |
| 唐小棠背影鏡附髮型參考圖 `refs-live/tangxiaotang-back-shuangji-e929-w3.png`；跪姿要拍到膝蓋 | 她的五個背影鏡（s07、s09、s32、s34、s35）都由 `spec.json` 的 `append_pictures` 加送這張、一句「只定髮型、不定地方與光」；s28 刁七跪、s39 許硯單膝跪都寫全身（Wide），s40 寫成蹲 |
| 柴刀固定句「a long narrow iron blade with a slightly hooked tip」會被畫成劍 | 本集柴刀不寫（拍法 5），`prep937.sh` 擋 `slightly hooked tip`、`chopper`、`sword`；之後若要寫柴刀改短而寬的方頭厚柴刀 |

## 1. 分鏡（`writer-tools/e037-r2/r2.py`，43 鏡＝c01–c40＋三個拆鏡；下面是寫稿時的紀錄，獨立審稿後的改動見 §7）

- build：scratchpad `tools/build937.sh`（`build-r2.py` → `docs/videos/zhong-tian-qu-qi-e037-r2/{video.json,overlays.json,storyboard.md}`、`hailuo/{ff,clips}-dh-e937.json`）；
  `storyboard-check.py` 稿子 40 鏡 199.5 秒；`shot_reading` 7 個 `cast.speaker`（s03、s16、s37、s38 系統；s08 唐小棠插鏡錄音；s23 二牛插鏡錄音；s33 二牛遠處喊：`OFFSCREEN_SPEECH = False` 的刻意寫法），其他陷阱 0。台詞 39 句逐字照稿。
- **拆鏡**：**s09b**（c09 後半：許硯與六個扛鋤頭的流民走出院門，2026-11-06 審稿補的那句；s09 只留塞油燈）、**s16b**（c16 系統＋心裡話約 9.5 秒加停頓：心裡話拆出來，握拳又鬆開）。
- **集長**：BUY 一個種子 261 秒（5 秒 5、6 秒 30、8 秒 7）；稿子估 199.5 秒；剪接以錄音人聲為準，預估成片約 3 分 20 秒–3 分 40 秒（第 36 集稿子 194.5 秒、BUY 260 秒、成片 200.84 秒）。
- 照聖經與第 36 集審稿、成片審查的教訓改稿子的地方（各鏡 zh 有寫）：
  | 稿子 | 真人版 | 為什麼 |
  | --- | --- | --- |
  | 院子：井在左前、院門在右、東牆下一排草蓆 | 院門在後牆中間（門扇推開靠左柱）、井在前右、草蓆在樹與井之間；二牛朝鏡頭衝進來、秦霜從後牆右段跳下 | 拍法 29、42；第 36 集成片 |
  | c01 肩膀撞開門板、門板撞籬笆彈回 | 第一格已經衝進門（門扇照圖推開） | 一鏡一個動作；任務檔『門要明寫』 |
  | 唐小棠 c08 近景說話、c32 c34 c35 說話、c07 c09 聽 | c08 兩手抓袖口的插鏡＋錄音；c32 c34 c35 從背後；c07 c09 不點名的背影；全部加送雙丸子背影圖；**沒有正臉** | 拍法 3、4、40；站主 2026-11-22 |
  | 秦霜 c05 手按柴刀柄、c13 解下柴刀交給壯丁 | 不寫；她空手排陣 | 拍法 5、〈道具〉 |
  | c14 秦霜肩後拍許硯（她在前景說話） | 許硯肩後拍她（她在畫左朝乾地說、肘往後一頂） | 她的嘴要在畫面上；軸線（秦霜左、許硯右） |
  | 新渠渠頭：一人深的渠、一道三步寬的土埂、閘板、山 | 圖上：約膝深的乾渠往深處、**左岸那道新土堆＝土埂**、渠上一塊木板（台詞的閘板）、遠處松樹（山腳）；守的人在土埂上面向左、淺坑挖在前面的乾地 | 拍法 29（圖說了算）；平木板會長字 |
  | 薄月偏西 | 不寫月亮，只寫冷月光（圖上的細月塗掉） | 第 36 集是滿月 |
  | 約二十人、約六十人、四百人、約四十個婦孺 | 看得見的三到九人（每人衣色年紀）；四百人＝遠處一長串小火光與六個奔跑的黑影；婦孺＝小禾與兩個婦人 | 拍法 34、37 |
  | c17 一長串火把衝下山 | `a long thin line of small orange flames streaming out of the pines, far away` | 拍法 37（圖上沒有山坡） |
  | c21 石灰煙 | `thick white powdery smoke`（不寫 fog） | 拍法 37 |
  | 流寇『舉刀』（c31 c33） | 素木棍；刀只有刁七一把 | 〈小角色〉、拍法 5 |
  | c33 短匕柄敲手腕、c31 短匕在指間翻 | 刀不出鞘、刀鞘的一端敲手腕；不翻 | 拍法 22 |
  | 刁七 `cast.json` 的皮甲 | 破布短褐、繩腰帶、黑綁腿；疤在左（extras） | 原版必修、〈人物〉 |
  | c27 刀在空中翻一圈插進土埂 | 刀被挑出畫面上方；s28 前景插在土裡 | 一鏡一個動作 |
  | c28 刁七跪下（中景） | 全身（Wide）、兩膝著地 | 站主 2026-11-22 |
  | c35 起袍子下半截沾石灰白粉 | `pale white lime powder dusted over the lower half of the robe` | 不寫泥（第 32 集 fix3） |
  | c37 臉被淡藍光照亮 | 不寫 | 拍法 11 |
  | c40 許硯咧嘴笑（原版） | 不笑、眉頭擠緊、眼睛睜大；蹲（不是跪） | 原版必修 |
- 自審（`writer-tools/e037-r2/review.md`，不是獨立審稿）；給獨立審查者的提示 scratchpad `e937prep/review-prompt.md`，由協調者派。

## 2. 新圖（全部免費，寫進 `assets/refs-live/README.md`，`prep937.sh` 每次逐位元重建比對 20 張）

| 圖 | 怎麼來 | 鏡 |
| --- | --- | --- |
| `set-shanjiao-qu-ye2-l1` | `shanjiao_qu_ye_clean.py`：付費夜景 `-ye`（第五輪 37046）照第 36 集的清理塗掉護欄、直立平木板（改細樁）、地平線方塊，**再塗掉細月** | s10 s13 |
| `-ye2-geng`／`-zhuo`／`-tian`／`-cao`／`-kong` | `shanjiao_qu_ye_e937.sh`：土埂與乾草堆／乾地與遠處松樹／渠、木板與暗秧田／乾草堆近景／松樹頂上的夜空 | s12 s24 s26–s28／s11 s14 s17 s18 s21 s22 s25／s15 s16 s16b s19／s23（插鏡）／s20 |
| `set-shanjiao-qu-chen-l1` 與 `-chen-geng`／`-zhuo`／`-tian` | 同上：清理後的夜景提亮成天快亮的灰藍、松樹上方一條灰白 | s35／s39 s40／s37／s36 s38 |
| `set-xujia-houmen-ye-men-l1`、`-xiang-l1` | `xujia_houmen_e937.sh`：後門圖（試鏡第一輪 37038）的半開門與柴堆／從門口看出去的巷子 | s29 s30／s32 s33 s34 |
| `set-xujia-yuan-ye-dong2-shu-l1`、`-di-l1` | `xujia_yuan_ye_e937.sh`：夜院子的樹枝映夜空／院子的地 | s02 s03／s08（插鏡） |

沿用：第 31 集的 `set-xujia-yuan-ye-dong2-l1`（s09b）、第 36 集的 `-zhong`（s01）、`-qiang`（s04 s05）、`-chai`（s06 s09）、`-wu`（s07）；後門整張 `set-xujia-houmen-ye-l1`（s31）。
加在最後一張的：`tangxiaotang-back-shuangji-e929-w3.png`（s07 s09 s32 s34 s35）、`prop-changqiang-l1.png`（s26 s27 s36）。

## 3. d1（種子 9371101／9371102）

| 檔 | 內容 |
| --- | --- |
| `colab/runs/e937/extras.json` | 乾淨畫面句；秦霜身分句拿掉柴刀；阿令不寫紅唇；二牛拿掉 `empty-handed`、`an honest open face`；小禾的草兔子塞在腰間；**刁七的皮甲換成破布短褐、繩腰帶，疤寫在左邊** |
| `colab/runs/e937-live/mkspec.py` → `spec.json` | 42 鏡全部有改：唐小棠背影三鏡拿掉三張臉部圖與身分句、s32 s34 地點句開頭大寫；她的五個背影加送雙丸子背影圖（`append_pictures`）；拿槍三鏡加送長槍道具圖；許硯 angle-b 不送、全景 s04 s09b s10 s35 s39 只送 l1、近景 s03 s15 s16 s37 s38 先 l1 後 angle-a；二牛 s02 的 angle-a 換成 l1、全景 s01 s28 只送 l1；阿令 angle-b 不送、s31 只送 l1；插鏡 s08 s23 拿掉地點句、一張裁切只當地面與光；s17 s21 沒有人；渠（s10–s28、s35–s40）拿掉 `below the deep pool`；only 句點名不具名的人（寫兩次）；鞋句（秦霜皮靴、不具名的人草鞋）；clear-and-still 句逐鏡換（夜氣、油燈、火把、石灰粉、熱水的蒸氣、天快亮的冷空氣）；視線句；大寫 |
| scratchpad `tools/prep937.sh` | 照 `prep936.sh` 的順序與檢查，改成本集：`append_pictures`（加在最後一張、句子放在場景句後、重編表頭）；唐小棠的名字與臉部圖全集沒有、五個背影都有髮型圖；院門推開、後門半開；沒有細月；草蓆在樹與井之間；兵器字只在劇情要的鏡；煙只有石灰的；跪的鏡是全身；渠沒有潭字、沒有 causeway；沒有 cinema camera、stubble、chopper、sword、armour、tassel。log `tools/prep937.log` |
| scratchpad `e937d1.sh` | （審稿後 86 支 528 秒，§7）84 支 522 秒，G4、session `zt-live3`（**先確認沒有別的集在跑**）、兩輪補缺、跑完釋放 VM。**沒有執行**（`DRY=1` 0 錯） |

**檢查結果（2026-11-23）**：`build937.sh` 42 鏡、storyboard-check 199.5 秒、shot_reading 7 個 `cast.speaker`（刻意）；免費圖 20 張逐位元重建相同；
`set-xujia-yuan-ye`（l2）、`-ye-dong2`、`set-xujia-houmen-ye`、`set-shanjiao-qu-ye`、`-ye2`、`-chen`（l1）最新版；st1 DRY `check_manifest` 0／0、st1 preflight 0 錯 0 警告；
**84 支、522 秒**（5 秒 10、6 秒 60、8 秒 14）；分隔句每支各一次；精修句漏進 d1 0；`prompt_sha256` 與兩種子一致；送圖、點名、場景、光線逐鏡相符；
**preflight 0 錯 0 警告**；`check_manifest.py`、`h3r.sh check` 0／0；否定名詞、會長字的名詞、掛著的東西、open、點名畫外人、插鏡地點字、泥／金箔、潭字、唐小棠被點名、cinema camera，全 0。
`e937d1.sh` `DRY=1` 0 錯。

**估價**：照第 36 集（80 支 520 秒，估 22–26 CU）與第 32 集實跑（78 支 518 秒約 2.4 小時），本集 84 支 522 秒約 **2.4–2.7 小時、23–27 CU（約 US$2.3–2.7）**。
Colab 餘額以跑之前的數字為準（第 36 集收尾記約 220 CU）；**剩約 100 CU 時先問站主**。

## 4. 錄音（`tools/rec937-slow.sh`）與錄音後核對

- 協調者准用站台 TTS。`rec937-slow.sh` 照 `rec936-slow.sh`：一句一呼叫、**間隔 ≥ 12 秒**、失敗（429 `video_speech_upstream_busy`）等 90 秒重試、每句最多 20 次；已錄的檔跳過，重跑就續錄。
  提示 `tools/e937-tts-hints.json`（`mkhints937.py`，9 句多音字：數 shǔ a01 a33、得 děi a04 a05 a09 a15、著 zhe a15 a35、著 zháo a22、倒 dǎo a29）；聲調聽寫看不出，要人耳聽過。
- 錄音後跑 `tools/rec937-check.sh`（聽寫 `fw937all.sh` 兩種、YIN 音高 `f0y937.py`、人聲長度 `span937.sh` 對 BUY → `tools/{fw937.txt,f0y937.txt,span937.txt,span937-buy.txt}`）。
- **結果（2026-11-23 01:18–01:48 UTC）**：**39／39 錄齊**（a02 遇到站台 429 `video_speech_upstream_busy` 五次、約 11 分鐘後恢復，其他一次過）；`rec937-check.sh` 跑完、**重錄 4 句**（`tools/rec937-retake.sh`，第一次的檔在 `audio/take1/`），變調 7 句。
  全文 `~/mokaair-work/videos/zhong-tian-qu-qi-e937-dh/audio/README-retakes.txt`；聽寫 `tools/fw937.txt`（重錄 `fw937-retake.txt`、變調 `fw937-shifted.txt`）、音高 `f0y937.txt`（`-retake`、`-shifted`）、人聲長度 `span937.txt`／`span937-buy.txt`（`span937-retake.txt`）。
  - **人聲長度對 BUY：39 句都放得下，BUY 不改**。最緊：s01 a01 5.08／6、s02 a02 4.68／6、s37 a35＋a36 5.20／8、s05 a05 重錄約 5.2／8、s24 a23 重錄約 4.6／8、s14 a14 4.06／6、s36 a34 4.13／6。
  - **聽寫**：帶上下文 38 句 r1.00（a04 0.97、a21 0.95、a32 0.95 只差標點或漏一字）；不帶上下文聽錯的都是同音或專名（渠→曲、刁七→貂妻／標旗、陣→鎮／正、小禾→小河、閂→關），照前幾集接受。
    **a20 秦霜「扔！」兩次都聽不出**（第一次「哼，真」、重錄「就」；一個字的短喊 whisper 解不出）：**要人耳聽**；s20 她在畫面上張嘴喊（`nospeak`），片中原聲也可以用。
  - **重錄**：a05 秦霜 329→248 Hz（用重錄）、a18 刁七 286→211 Hz 再降 `a18-p80` 170（用）、a23 二牛 317→247 Hz（用重錄）、a20（見上）。
  - **音高**（拍法 43，≥ 3 半音）：變調 `a19-p130`（秦霜耳語 158→210，接 s18 刁七 170：3.7）、`a25-p125`（秦霜 177→228，接 s28 二牛 180：4.1）、`a12-p80`（許硯 182→147）、`a08-p88`（唐小棠 306→272）、
    後門 `a28-p88`（阿令 211→185）與 `a30-p115`（唐小棠 204→238）：同場阿令 185／166 對唐小棠 238／234 ≥ 4 半音。不變調：a31 二牛遠處喊 289（< 290，對 a32 唐小棠 234 有 3.7）、a39 許硯 202（慌，喊聲範圍）、a34 秦霜 166（放輕，前後 258／114）。
    相鄰說話者全部 ≥ 3 半音（最小 a18-p80 170→a19-p130 210 3.7、a33 唐小棠 258→a34 秦霜 166 7.6）。
  - **刁七（Fenrir）第一次量**：a21 149、a24 177、a18-p80 170 Hz，已補進聖經〈人物〉。
  - **剪接用哪個檔**：a05、a23 用重錄；a18、a19、a25、a12、a08、a28、a30 用 `-pNN`；其他用原檔。人群聲（s35 歡呼、流寇喊殺）照站主規則用 `crowd-murmur.py 37`（39 句已齊，可以做）。

39 句、7 個聲音加系統：

| 鏡 | id | 角色 | 句子 | BUY |
| --- | --- | --- | --- | --- |
| s01 | zq937a01 | 二牛 | 四百人！山上下來四百人，火把數都數不完！ | 6 |
| s02 | zq937a02 | 二牛 | 咱們連流民裡肯拿鋤頭的，才六十個。 | 6 |
| s03 | zq937a03 | 系統 | 叮。守村任務：婦孺一個不能少。 | 6 |
| s04 | zq937a04 | 許硯 | 不守村口。下山的路，最後都得走渠頭那道土埂。 | 8 |
| s05 | zq937a05 | 秦霜 | 四百人，也得一個一個走那道土埂。陣我來排。 | 8 |
| s06 | zq937a06 | 許硯 | 陣妳排，怎麼打我照妳的，一個字都不改。 | 8 |
| s07 | zq937a07 | 許硯 | 小棠，婦孺都進屋，妳跟阿令守後門。 | 6 |
| s08 | zq937a08 | 唐小棠（插鏡，錄音） | 那你呢？你一個書生，打算站在哪裡？ | 6 |
| s09 | zq937a09 | 許硯 | 我站渠頭。石灰是我的主意，我得在那裡。 | 8 |
| s10 | zq937a10 | 許硯 | 糖坊剩的石灰，三步埋一袋，袋口朝上。 | 6 |
| s11 | zq937a11 | 二牛 | 坑才挖到膝蓋，這麼淺有什麼用？ | 6 |
| s12 | zq937a12 | 許硯 | 不用深，夜裡衝過來的人，絆一跤就夠了。 | 6 |
| s13 | zq937a13 | 秦霜 | 前排蹲下，我不喊，誰都不准動。 | 6 |
| s14 | zq937a14 | 秦霜 | 你下去，站到後頭，這裡會死人。 | 6 |
| s15 | zq937a15 | 許硯 | 我說過照妳的陣打，可我得看著它打完。 | 6 |
| s16 | zq937a16 | 系統 | 宿主不會打架，站在前排的用處是當靶子。 | 6 |
| s16b | zq937a17 | 許硯（心裡話） | 當靶子也好，至少她不用回頭找我。 | 6 |
| s18 | zq937a18 | 刁七 | 衝過去！柳溪的糧，全是咱們的！ | 6 |
| s19 | zq937a19 | 秦霜 | 等，讓他們踩上坑，再等三步。 | 6 |
| s20 | zq937a20 | 秦霜（短喊） | 扔！ | 5 |
| s22 | zq937a21 | 刁七 | 什麼鬼東西！眼睛睜不開了！ | 6 |
| s23 | zq937a22 | 二牛（插鏡，畫外） | 渠頭的草著了！差點燒到閘板！ | 6 |
| s24 | zq937a23 | 二牛 | 火把全滅了！衝在前頭的，全掉進坑裡了！ | 8 |
| s25 | zq937a24 | 刁七 | 我刁七爺的刀，不砍書生，給我讓開！ | 6 |
| s27 | zq937a25 | 秦霜 | 刀放下了。再動一下，槍頭就進你喉嚨。 | 8 |
| s28 | zq937a26 | 二牛 | 綁了！把刁七押去穀倉關起來！ | 6 |
| s29 | zq937a27 | 小禾 | 哥哥呢？哥哥是不是在外面打仗？ | 6 |
| s30 | zq937a28 | 阿令 | 哥哥在渠頭。妳進去，把門閂上。 | 6 |
| s31 | zq937a29 | 阿令 | 進來一個，我就放倒一個。 | 6 |
| s32 | zq937a30 | 唐小棠（背影） | 滾出去！許家的門，你們進不來！ | 6 |
| s33 | zq937a31 | 二牛（畫外，很遠） | 刁七綁了！你們的頭子綁了！ | 6 |
| s34 | zq937a32 | 唐小棠（背影） | 他們跑了……一個都沒進來。 | 6 |
| s35 | zq937a33 | 唐小棠（背影） | 婦孺都在，一個不少，我數了兩遍。 | 6 |
| s36 | zq937a34 | 秦霜 | 你一個字都沒改我的陣，也一步都沒退。 | 6 |
| s37 | zq937a35 | 許硯 | 陣是妳排的，我只負責站著別跑。 | 8 |
| s37 | zq937a36 | 系統 | 叮。秦霜好感，加七。 | （同鏡） |
| s38 | zq937a37 | 系統 | 叮。任務完成。 | 6 |
| s39 | zq937a38 | 小禾（短喊） | 哥哥！ | 5 |
| s40 | zq937a39 | 許硯 | 小禾？小禾！妳的臉怎麼燙成這樣？ | 6 |

沒有台詞的鏡：s09b、s17、s21（5 秒）、s26（6 秒，奪槍）。
錄音後要注意：**刁七（Fenrir）第一次量**、補進聖經〈人物〉；同場聲音差 ≥ 3 個半音（拍法 43）：第一場二牛（170–230）對許硯（88–145）、秦霜（195–240）；
第二場二牛對刁七、秦霜對二牛；第三場後門阿令（第 31–35 集 170–197）對小禾（300–360）、唐小棠（中位約 252）；天快亮唐小棠 a33 對秦霜 a34（相鄰）。

## 5. 還缺、要付費才補得上的（都不擋 d1；建議，不自己跑）

1. **渠的夜景偏 CG、溝底裂土像磚**（第 36 集就記過；`-ye` 是同一張改光）：二十五鏡。草稿 CG 感太重才考慮灰底重畫（約 1.5–2 CU）；**建議先看 d1**。
2. **後門圖偏 3D**（試鏡第一輪 37038；門裡暖光、石牆）：六鏡，同上先看 d1。
3. **婦孺沒有一鏡全景**：s35 用唐小棠背影＋錄音交代；審稿或成片審查覺得不夠，可以加一鏡無台詞全景（5 秒兩支，約 0.5 CU）。

## 6. 還擋著開拍的事（要協調者／站主決定）

1. ~~獨立分鏡審查~~（2026-11-23 做完、已套用，§7）。
2. ~~錄音~~：39 句錄齊、核對、重錄 4 句、變調 7 句、BUY 不改（§4）。**a20「扔！」要人耳聽**。
3. **花錢**：`e937d1.sh`（86 支 528 秒）約 23–27 CU，等協調者；先確認 `zt-live3` 上沒有別的集在跑。

**fix／retake 的提醒（照第 36 集 §6）**：渠的潭字是 `mkspec.py` 拿掉的；**s10–s28、s35–s40 的每個 fix／retake spec 都要帶 `[R2.POOLMARK, ""]`**（插鏡 s23 另外要帶拿掉整句地點句的替換）；
fix 也要帶 `mkspec.py` 的唐小棠背影替換（身分句、三張臉部圖、`only` 句）與 `append_pictures`（髮型圖、長槍圖：`retake.py` 不會加圖，要照 `prep937.sh` 的做法加在最後一張）、clear-air 逐鏡替換與鞋句。

## 7. 獨立審稿怎麼套（2026-11-23，`writer-tools/e037-r2/review-independent.md`；協調者的決定）

改前的檔在 scratchpad `e937prep/*-before-review.*`（`r2`、`mkspec`、`spec`、`PREP`、`extras`、`prep937`、`e937d1`、`shanjiao_qu_ye_e937`、`bible`、`refs-README`）。
改完重跑 `build937.sh`（**43 鏡**、shot_reading 7 個刻意的 `cast.speaker`、其他陷阱 0）、`prep937.sh`（rc=0：**86 支、528 秒**（5 秒 12、6 秒 62、8 秒 12）、st1 與 d1 preflight 0／0、
`check_manifest`／`h3r` 0／0、所有掃描 0、免費圖 30 張逐位元相同，加了下表每項的斷言）、`DRY=1 e937d1.sh` 0 錯、`node tools/video/drama-admin/bundle.mjs build`。
**錄音不用重錄**：s27b 用原本的 a25（`a25-p125`，4.3 秒／6 秒），台詞編號不變（s27 無台詞）；39 句仍全部放得下 BUY（`tools/span937-buy.txt` 重算）。

| 項目 | 怎麼處理 |
| --- | --- |
| 必改 1：院門的門扇寫反 | `YARD`、s01：`the slatted plank gate leaf hinged on the right gate post standing half swung back inward …, the left half of the gateway clear`，二牛從門洞左半衝進來；zh、§1、聖經〈接點〉36→37 一起改（`open`、`hung` 是掃描擋的字，寫成 `swung back`、`hinged`） |
| 必改 2：s28 槍頭從左進 | 改從**右**緣伸進來（秦霜在 s26、s27 都在右）；mkspec 的 only 句一起改 |
| 必改 3：s21 掉坑是進行中的動作 | 第一格兩個黑影已經陷在坑裡到腰、斷草圍腰、火把在地上；動作只留煙吞火把 |
| 必改 4：s26、s27 長桿第一格沒分開 | s26 `its spearhead still an arm's length short of her in the first frame`；s27 `its spearhead pointing low at the ground a step short of him, well apart from his saber` |
| 必改 5：s10 跪著的壯丁 | 改蹲：`already crouching low on his heels` |
| 必改 6：`-ye2` 護欄清理的亮直條 | `shanjiao_qu_ye_clean3.py`（上下內插、x 480–520 淡入）→ 新 id `set-shanjiao-qu-ye3-l1`、`-ye3-zhuo`、`-ye3-kong`、`-ye3-cao`；`-ye2-geng`、`-ye2-tian` 照送 |
| 必改 7：s37 圖文不一致、`-chen` 滿天星 | `destar_e937.py` 去星 → `set-shanjiao-qu-chen2-l1` 一族，s37 改送新裁切 `-chen2-kong`（松樹頂上的灰白天），s35 送去星的 `-chen2` |
| 建議 1：雙丸子背影圖是白天（協調者同意做夜版） | `tangxiaotang_back_ye.py` → `tangxiaotang-back-shuangji-e929-w3-ye.png`（原檔不動）；s07、s09、s32、s34 夜裡與 s35 天快亮的背影鏡都送夜版（天快亮仍偏暗冷，白天的藍天與屋子更不合） |
| 建議 2：刁七的刀會變劍 | `SABER` = `one long single-edged saber with a broad, gently curved back, widening toward the tip, a plain round iron disc at the hilt`（`blade`、`guard` 掃描或人數判斷會出事：`guard` 讓 ref2manifest 以為多一個人） |
| 建議 3：s27 一上一下兩段（協調者定拆鏡） | **s27**（5 秒、無台詞：刀第一格舉到肩高正往下劈，槍頭一挑把刀挑出畫面上方）＋**s27b**（6 秒、中近景：槍尖第一格已經停在喉前一掌、他兩手空著，秦霜說 a25）；兩支都加送長槍道具圖。兩種子多 6 秒、約 0.3 CU |
| 建議 4：s28 舉手又繞繩 | 刁七兩手第一格已經扭到背後、繩子繞胸口與上臂 |
| 建議 5：「只有一條路」（免費做法） | s17 六個黑影 `running one behind another in a single file along one narrow beaten footpath across the field toward the ridge`（`track` 是掃描擋的運鏡字） |
| 建議 6：`-chen` 地面太亮 | 併在必改 7：gamma 1.55 → 1.35、灰白只加在 30–47% 的天空、以藍度加權（松樹不變白） |
| 建議 7：木板後的拉絲矩形 | 先看 d1（協調者定） |
| 建議 8：s35 長槍道具圖 | 加送（最後一張） |
| 建議 9：刁七的疤 | 照定妝照寫 `a short pale old scar on his left cheekbone`（r2.py 與 extras）；s28 臉低著略朝畫左 |
| 建議 10：後門屋簷的空白木板 | 先看 d1 s31（協調者定） |
| 建議 11：BUY 可省 | 不改（品質優先） |

**估價**（審稿後）：86 支 528 秒，約 2.4–2.7 小時、**23–27 CU**（比審稿前多 6 秒，約 0.3 CU）。
