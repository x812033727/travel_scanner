# 第 33 集重製版 r2（e033-r2，內部 933）真人版開拍前置

- 2026-11-19，前置代理。**沒送任何生成**（Colab、RunPod 都沒開）、**沒用站台 TTS**、沒 commit。只跑免費檢查。
- **2026-11-19 收尾**（前置收尾代理，站主常設授權 2026-11-18）：錄音 41 句已由協調者錄好，做完錄音後核對（§4）；**獨立審查**（`writer-tools/e033-r2/review-independent.md`，必改 8、建議 15）全部套用，只有建議 14 沒做（§1）；
  必改 1 水車葉板**選 A**：Colab `zt-live3` 跑 Qwen-Image-Edit 兩輪 8 支，**花 2.12 CU**（480.10 → 477.98），挑 `set-shentan-l2`，其餘全部免費（§2）。沒送 d1、沒 commit、沒跑 TTS（重錄 a19 的腳本寫好沒跑）。
- 依據：第 32 集的前置全套（`writer-tools/e032-r2/r2.py`、`colab/runs/e932/extras.json`、`colab/runs/e932-live/{mkspec.py,spec.json,PREP.md}`、scratchpad `tools/prep932.sh`、`rec932.sh`、`e932d1.sh`）、第 31 集同一套（唐小棠背影鏡：`e931-live/mkspec.py`）、`r2-bible-e031-e040.md`、任務檔第 32 集教訓、第 32 集成片最後 15 秒（`e932-live.mp4` 203–218 秒）。
- scratchpad = `/tmp/claude-0/-home-user-travel-scanner/31162243-7ed2-5899-b9c2-443c1f2a5c1a/scratchpad`。

## 1. 分鏡（`writer-tools/e033-r2/r2.py`，40 鏡＝c01–c40）

- build：scratchpad `tools/build933.sh`（`build-r2.py` → `video.json`、`overlays.json`、`storyboard.md`、`hailuo/{ff,clips}-dh-e933.json`）；`storyboard-check.py` 40 鏡 222.5 秒；`shot_reading` 6 個 `cast.speaker`（系統、心裡話、畫外錄音：`OFFSCREEN_SPEECH = False` 的刻意寫法）。台詞 41 句逐字照稿。
- **s01 照第 32 集 s36–s37 實拍改寫**：s36 胸口高全景、門左、韓伯跪在中間回頭、八個村民跪在右半臉朝門；s37 許硯在門口、圖卷橫在腰前右手、淡出 → s01 同機位（送 `set-citang-huang-l1`），第一格許硯已跨進門檻一步、圖卷橫在腰前，往右穿過跪著的人；韓伯竹杖靠在供桌邊。
- 照聖經改稿子的地方：風水先生小角色（不畫定妝照、不點名、只遠景側面、錢員外在前；聲音 Charon 寫在 `MINOR`）；秦霜竹竿不綁旗、柴刀不寫；唐小棠 s17 背影說話、s19 只露後腦；白鬚老漢村民改布包頭短灰鬚；水車只送 `set-shentan-l3`／`-gongdi-l2` 一族（原版必修；審稿必改 1 後的有葉板版）；s34 轉半圈固定鏡、結果先寫（第 32 集 fix2）；全集沒有泥（fix3）。
- 自審（不是獨立審稿，見 `writer-tools/e033-r2/review.md`）抓到的兩個必改已改：s06 越軸、s21 風水先生在錢員外身後（右緣）。
- **獨立審稿套用**（`r2.py` 用 `edit_r2*.py` 逐句替換，每句斷言只出現一次；`mkspec.py`；`prep933.sh` 加對應檢查）：
  | 項 | 怎麼改 |
  | --- | --- |
  | 必改 1 水車沒葉板 | **A**：`set-shentan-l2`（Qwen 只加十二片平木葉板）→ 免費 `set-shentan-l3` 與全部正午、清晨裁切重做；`WHEEL` 的「twelve flat wooden paddles」、s30 s35 s38 手按葉板、s34 水打最下面的葉板都照圖成立 |
  | 必改 2 s30 s35 右緣沒輪子 | 新框 `-bian-l3`／`-chen-bian-l3`（`560:315:60:250`：左邊石邊、右邊約四成五是輪緣與葉板）；許硯寫在左半、手按「on the rim of the wheel at the right」、背景改「beside him at the right, the near rim, spokes and paddles」；`-lun-l3` 只給 s38 |
  | 必改 3 s25 錯肩 | comp 與 `GAZE_REFINE` 都改 right shoulder，zh 改右肩 |
  | 必改 4 素牆有梁 | `citang_ye_crops.sh` 加 `set-citang-ye2-qiang-l1`（`400:225:895:92`，沒有梁），s07 s11 改送 |
  | 必改 5 場景麻繩 | `shentan_clean.py` 塗掉矮木架的麻繩、影子與橫繩 → `-an-l3`／`-chen-an-l3`（s29 s31–s33 s36 s37） |
  | 必改 6 s34 布鞋句 | `mkspec.py` 對 s34 拿掉「Every person in the frame wears dark cloth shoes」；`prep933.sh` 斷言 |
  | 必改 7 溝底的潭 | `D0`／`E0`／`E1` 改「on the flat dry fields」、`gd_g`／`nn_g` 改「beyond the pool」；掃描 `gully` 0 |
  | 必改 8 crowd | s12 改「standing about here and there on the sand」；掃描 `crowd` 0 |
  | 建議 1 s25 風水先生換邊 | 改 `FENG_EDGE_R`（右緣、已轉身往右）；mkspec 的 only 句改 right |
  | 建議 2 s22 | 二牛側臉朝畫右看右後方兩個壯丁、左手掌心朝上一攤；木料「held low behind them, well apart from the staff」 |
  | 建議 3 s13 竹竿 | 竹竿豎著、竿腳拄在大石上、竿頭在天空裡從左到右一劃 |
  | 建議 4 s15 竹竿消失 | 加 `BAMBOO` 豎在右手（遠側）、竿頭出畫面上緣；`prep933.sh` 斷言 s12 s13 s15 都有竹竿 |
  | 建議 5 s29 拍背 | 改拍肩（zh 註明稿子「拍在背上」改肩） |
  | 建議 6 s05 木梯、s07 梁 | 木梯「just beyond the right end of the altar table and clear of it」；s07 加「the long dark beam slanting up from his shoulder out of the upper right corner」、扛梁兩人改「a step along the beam」 |
  | 建議 7 s33 s36 那側有輪子 | 新常數 `SIDE_STONE_RIM`（石邊、綠水與畫緣停著的輪緣） |
  | 建議 8 夜版門洞 | `LOC["ye"]`、`["ye_men"]`、s06、s10 改「a dark passage and another lattice door, blue-black with the night」 |
  | 建議 9 s34 半圈看不出 | 有葉板了（必改 1 A），轉半圈看得出；文字不動 |
  | 建議 10 電塔與細桿 | `shentan_clean.py` 塗掉左邊地平線的小電塔、右邊地平線露出天空的細豎桿；工地版 `set-shentan-gongdi-l2` 一族同樣塗 |
  | 建議 11 s01 | 村民「their hands resting on their knees」；韓伯「kneeling in the middle of the floor in front of them」 |
  | 建議 12 s19 | 錢員外與風水先生「standing in the gap between the middle and right posts of the tall frame」 |
  | 建議 13 s17 | 唐小棠「standing on the stone edge of the pond」 |
  | 建議 14 角度圖 | **沒做**：`retake.py` 的 spec 只能換圖（swap）或拿掉圖（drop），不能加圖；要加得改共用工具與檢查，風險大於收益。FOOT 改寫成「秦霜、小禾每鏡只送 l1」與原因 |
  | 建議 15 聖經 33→34 | 〈接點〉33→34 照圖改（水車中間偏左、錢員外在高木架右邊遠處田邊、第 34 集第一鏡送 `-bian-l3`）；〈道具〉水車列、〈場景〉深潭列改成 `set-shentan-l3` 一族 |

## 2. 新圖（寫進 `assets/refs-live/README.md`，`prep933.sh` 每次逐位元重建比對）

| 圖 | 怎麼來 | 鏡 |
| --- | --- | --- |
| `set-citang-ye2-l1` | `citang_ye_clean.py`：`set-citang-ye-l1` 主梁裂紋照 `citang_huang.py` (b) 塗掉 | s05 |
| `-ye2-men`／`-ye2-tang`／**`-ye2-qiang`**（`-ye2-liang`、`-ye2-zuo` 備用） | `citang_ye_crops.sh`；`-ye2-qiang` 是審稿後加的沒有梁的素牆 | s06 s08 s10／s09／s07 s11 |
| **`set-shentan-l2`（付費）** | Qwen-Image-Edit 只在 `set-shentan-l1` 的輪緣加十二片平木葉板（`shentan-l2/`，第二輪種子 9331205，2.12 CU） | 只當底圖 |
| `set-shentan-l3` | `shentan_l3.sh`＋`shentan_clean.py`：`-l2` 塗掉麻繩、電塔、地平線細桿 | s34 |
| `-an-l3`／`-bian-l3`／`-lun-l3`／`-geng-l3`／`-tian-l3` | 同上，裁切（`-bian` 新框 `560:315:60:250`） | s31 s32 s33 s36 s37／s35／s38／s39／s40 |
| `-chen-l3`／`-chen-an-l3`／`-chen-bian-l3` | 同上，灰金清晨調色（同 `shentan_crops.sh` 的濾鏡） | s28／s29／s30 |
| `set-shentan-gongdi-l2` 與 `-an-l2`／`-mu-l2`／`-tian-l2`／`-geng-l2` | `set-shentan-gongdi-l1` 塗掉電塔與細桿、裁切 | s12；s14 s16 s22 s24 s26／s13 s17 s18／s15 s23 s27（插鏡只當天色）／s19 s20 s21 s25 |

沿用：`set-citang-huang-l1`（s01）、`-huang-zuo2`（s02）、`-huang-liang`（s03）、`-huang-zuo`（s04）。不再送：`-huang-qiang`（左上角有梁）、`set-shentan-l1`／`-l2` 與 `shentan_crops.sh` 的 l1 裁切。
**風水先生照聖經不畫**；稿子建議的水車道具圖 `prop-shuiche-t1` 由聖經改成兩張場景圖每鏡送。**圖上沒有、靠文字的**：閘門與石槽（寫在左邊石階那段石邊缺口）、木梯、木板桌、高起的田埂（用遠處田邊）。

## 3. d1（種子 9331101／9331102）

| 檔 | 內容 |
| --- | --- |
| `colab/runs/e933/extras.json` | 乾淨畫面句；秦霜柴刀拿掉；二牛 guileless、不 empty-handed；石木匠淺褐、沒有木屑老繭；小禾草兔塞腰帶；錢員外錦袍 medallions（不寫 pattern） |
| `colab/runs/e933-live/mkspec.py` → `spec.json` | 40 鏡全部有改：唐小棠 s17 拿掉三張臉與身分句；許硯 angle-b 不送、全景 s01 s28 只送 l1、近景 s02 s08 s30 s35 先 l1 後 angle-a；二牛 s14 換 l1、全景 s05 s24 只送 l1；錢員外不送 angle-b、全景 s19 s39 只送 l1；韓伯 s01 s04 跪著沒有竹杖；s20 s27 s34 沒有人；s27 插鏡拿掉地點句、天空圖只當顏色；only 句、皮靴句、視線句、大寫 |
| scratchpad `tools/prep933.sh` | 照 `prep932.sh` 的順序與檢查，加泥／金箔、兵器字、長東西分開、白鬚老漢、風水先生不點名的檢查。log `tools/prep933.log` |
| scratchpad `e933d1.sh` | 80 支，G4、session `zt-live3`、兩輪補缺、跑完釋放 VM。**沒有執行**（`DRY=1` 0 錯） |

**檢查結果（最後一次 2026-11-19 收尾，審稿套用後）**：`build933.sh` 40 鏡 222.5 秒、shot_reading 6 個 `cast.speaker`（同前）；免費圖 25 張逐位元重建相同、`set-shentan` 最新版是 l3；st1 DRY `check_manifest` 0／0、preflight 0 錯（4＋7 警告，d1 前的 angle-b 等）；**80 支、582 秒**（5 秒 2、6 秒 32、8 秒 40、10 秒 6）；分隔句每支各一次；精修句漏進 d1 0；`prompt_sha256` 與兩種子一致；送圖、點名、場景、光線逐鏡相符；**preflight 0 錯、6 警告**（s21、s37 headroom「leans forward」、s32 shout）；`check_manifest.py`、`h3r.sh check` 0／0；否定名詞、會長字的名詞、掛著的東西、open、點名畫外人、插鏡地點字、兵器字、泥／金箔、`gully`／`crowd` 全 0；s34 沒有「Every person」、s25 是 right shoulder、s30 s35 手在右緣的輪緣葉板、s33 s36 那一側寫到輪緣、s12 s13 s15 都有竹竿（審稿後加的斷言）。`e933d1.sh` `DRY=1` 0 錯。

**估價**：照第 32 集實跑（78 支 518 秒約 2.4 小時）與第 31 集（86 支 556 秒 2.59 小時、約 26 CU），本集約 **2.6–3.0 小時、26–30 CU（約 US$2.6–3.0）**（審稿後支數、秒數不變：80 支 582 秒）。餘額 477.98 CU（2026-11-19 收尾後）；近 400 CU 先問站主。

## 4. 錄音（`tools/rec933.sh`，協調者 2026-11-19 錄好 41 句；核對見 `audio/README-retakes.txt`）

41 句、9 個聲音（許硯 Umbriel、韓伯 Enceladus、石木匠 Schedar、二牛 Sadachbia、秦霜 Autonoe、唐小棠 Laomedeia、小禾 Leda、錢員外 Algenib、風水先生 Charon〔第一次〕、系統 Callirrhoe）。
TTS 拼音提示（`tools/mkhints933.py` 從 video.json 產生 `tools/e933-tts-hints.json`，字幕不動）：a02 還 huán、a08 得 děi、a19／a38／a39 釘 dìng、a27／a28／a30／a36／a40 轉 zhuàn。
**錄音後核對（2026-11-19，scratchpad `tools/fw933.py`、`fw933all.sh`、`f0y933.py`、`span933.sh`；結果在 `audio/{fw933.txt,f0y933.txt,span933.txt,README-retakes.txt}`）**：
- 聽寫（faster-whisper medium，單句與帶上下文）：帶上下文 41 句除 a05（r0.97，刪節號）、a06（上下文 r0.82、單句 r1.00，錄對）、a19 外全 r1.00；單句只有同音字；沒有一句把拼音念成字母。
- **要重錄：a19 一句**（石木匠 s18「好釘。釘十二片葉板，還有剩。」：兩種聽寫都只聽到一個「釘」，第二個動詞 dìng 被吞掉）。腳本 scratchpad **`tools/rec933-retake.sh`**（沒跑；一次站台 TTS；把拼音提示換成同音字「定」、舊檔移到 `audio/take1/`、錄完自動量音高、長度、聽寫）。
- 音高（YIN）：韓伯約 120 Hz（a03 103、a33 123、a37 117）；石木匠正午 a35 133、a39 140，跟韓伯只差 1.8–2.7 個半音 → 照第 32 集做 **`zq933a35-p119.wav` 163 Hz、`zq933a39-p119.wav` 168 Hz**（差 5.3–5.8 個半音，帶上下文聽寫 r1.00）；清晨 a29 93、a30 105（沙啞，韓伯不在清晨鏡，留）。**小禾（Leda）第一次量 a24 339、a27 326 → 聖經 300–360 Hz；風水先生（Charon）a21 276 → 聖經喊聲 250–300 Hz**，都已寫進聖經〈人物〉〈小角色〉。許硯 a28（s27 插鏡、放錄音）172 Hz 在半個範圍邊上、YIN 雙峰，留原檔、備 `-p85`；a34 短喊 277 Hz 在畫面上、留原檔、備 `-p80`。都還沒人耳聽過。
- **BUY 不改**：人聲長度（silencedetect）每句都放得下（6 秒鏡 5.9、8 秒 7.3、10 秒 9.3）；最緊 s20 7.21／8、s40 7.20／8、s30 兩句 8.06＋間隔／10。下表最後一欄是量到的人聲長度與音高中位數。

| 鏡 | id | 角色 | 句子 | 字 | 語氣 | BUY | 人聲／音高 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| s02 | zq933a01 | 許硯 | 列位祖宗，晚生許硯，向柳溪借這根梁。 | 15 | 一字一頓 | 8 | 4.54 秒／160 Hz |
| s03 | zq933a02 | 許硯 | 水車造成，三年之內，我還柳溪一座新梁。 | 16 | 很穩 | 8 | 4.09 秒／121 Hz |
| s04 | zq933a03 | 韓伯 | 祖宗要怪，就怪我老頭子，別怪孩子們。 | 15 | 慢，篤定 | 8 | 5.52 秒／103 Hz |
| s05 | zq933a04 | 石木匠 | 繩套好了！都站開，梁要下來了！ | 12 | 吼 | 6 | 3.73 秒／145 Hz |
| s06 | zq933a05 | 王二牛 | 好沉的梁……許大哥，你那頭撐得住嗎？ | 14 | 咬牙 | 8 | 5.35 秒／232 Hz |
| s07 | zq933a06 | 許硯 | 撐得住！慢慢放，別砸了供桌！ | 11 | 咬牙 | 6 | 3.32 秒／159 Hz |
| s08 | zq933a07 | 系統 | 叮。旱災任務，剩七日。 | 8 | 冷，宣布 | 10 | 2.18 秒／175 Hz |
| s08 | zq933a08 | 許硯 | 石師傅，這水車得在七天之內立起來。 | 15 | 喘，篤定 | （同鏡） | 3.73 秒／150 Hz |
| s09 | zq933a09 | 石木匠 | 七天？兩丈高的輪子，十二片葉板，做不出來。 | 17 | 不信 | 8 | 6.05 秒／149 Hz |
| s10 | zq933a10 | 許硯 | 做得出來。你帶人做木工，我畫一片，你做一片。 | 18 | 很穩 | 8 | 4.44 秒／127 Hz |
| s11 | zq933a11 | 石木匠 | 好。做砸了，這根梁的帳，算在你頭上。 | 14 | 瞇眼 | 8 | 4.53 秒／123 Hz |
| s12 | zq933a12 | 秦霜 | 全村壯丁聽好，從今天起，分三班！ | 13 | 嗓門亮 | 6 | 4.05 秒／192 Hz |
| s13 | zq933a13 | 秦霜 | 一班做，兩班睡，輪著來，木頭不許停。 | 14 | 俐落 | 6 | 3.98 秒／205 Hz |
| s14 | zq933a14 | 王二牛 | 秦姑娘，這分班的法子，妳從哪學來的？ | 15 | 好奇 | 6 | 4.18 秒／212 Hz |
| s15 | zq933a15 | 秦霜 | 他寫的冊子。寫得囉嗦，法子倒是對的。 | 15 | 淡淡地，嘴硬 | 6 | 3.98 秒／192 Hz |
| s16 | zq933a16 | 系統 | 宿主寫的冊子，總算有人看完了。 | 13 | 冷 | 10 | 2.51 秒／130 Hz |
| s16 | zq933a17 | 許硯 | 嫌囉嗦也好，至少她從頭看到了尾。 | 14 | 內心獨白，嘴閉著，心裡話，錄得近、輕 | （同鏡） | 3.48 秒／111 Hz |
| s17 | zq933a18 | 唐小棠 | 糖坊的糖，換了三十斤鐵釘，夠不夠？ | 14 | 得意 | 6 | 3.20 秒／251 Hz |
| s18 | zq933a19 | 石木匠 | 好釘。釘十二片葉板，還有剩。 | 11 | 難得滿意 | 6 | 3.12 秒／200 Hz |
| s19 | zq933a20 | 唐小棠 | 田埂上穿黃袍的，是錢員外請來的風水先生。 | 18 | 畫外，小聲 | 8 | 3.76 秒／224 Hz |
| s20 | zq933a21 | 風水先生 | 拆祠堂的梁，動了龍脈，要遭天譴！ | 13 | 畫外，尖著嗓子，拖長音 | 8 | 7.21 秒／276 Hz |
| s21 | zq933a22 | 錢員外 | 祖宗都不要了，柳溪這一村，要絕後嘍。 | 15 | 油滑，拖長音 | 8 | 5.77 秒／172 Hz |
| s22 | zq933a23 | 王二牛 | 天譴……大家說，這梁還要接著做嗎？ | 13 | 發毛 | 6 | 4.33 秒／183 Hz |
| s23 | zq933a24 | 許小禾 | 祖宗也口渴！水來了，祖宗先喝！ | 12 | 叉腰，大聲 | 6 | 3.64 秒／339 Hz |
| s24 | zq933a25 | 王二牛 | 對，祖宗先喝！大家接著做，別停！ | 12 | 笑彎了腰 | 6 | 4.02 秒／203 Hz |
| s25 | zq933a26 | 錢員外 | 笑吧。十日一到，看你們誰哭。 | 11 | 陰 | 6 | 4.39 秒／139 Hz |
| s26 | zq933a27 | 許小禾 | 哥，你看！我用你的白紙，也做了一個會轉的。 | 17 | 奶聲奶氣 | 8 | 4.77 秒／326 Hz |
| s27 | zq933a28 | 許硯 | 做得好。等水車轉起來，妳的風車也一起轉。 | 17 | 畫外，微笑 | 8 | 3.49 秒／172 Hz |
| s28 | zq933a29 | 石木匠 | 最後一根木栓。架子，立起來了。 | 12 | 沙啞，七天沒睡好 | 8 | 4.22 秒／93 Hz |
| s29 | zq933a30 | 石木匠 | 轉不轉，就看中午開閘了。 | 10 | 沙啞，鬆一口氣 | 6 | 3.34 秒／105 Hz |
| s30 | zq933a31 | 系統 | 叮。旱災任務，今日到期。 | 9 | 冷，宣布 | 10 | 2.49 秒／179 Hz |
| s30 | zq933a32 | 許硯 | 知道了。七天，梁拆了，人也熬了，就賭今天。 | 16 | 內心獨白，嘴閉著，心裡話，錄得近、輕 | （同鏡） | 5.57 秒／98 Hz |
| s31 | zq933a33 | 韓伯 | 時辰到了。開閘，給柳溪的田放水！ | 13 | 慢，篤定 | 8 | 6.13 秒／123 Hz |
| s32 | zq933a34 | 許硯 | 石師傅，拉！ | 4 | 手一落，短喊 | 5 | 1.32 秒／277 Hz |
| s33 | zq933a35 | 石木匠 | 閘開了！水往輪子底下衝過去了！ | 13 | 吃力 | 8 | 3.83 秒／133 Hz |
| s35 | zq933a36 | 許硯 | 轉啊……水明明打在葉板上，它卻不轉。 | 14 | 不敢相信 | 8 | 3.52 秒／186 Hz |
| s36 | zq933a37 | 韓伯 | 停了……七天的工，祖宗的梁啊。 | 11 | 聲音發抖 | 8 | 5.50 秒／117 Hz |
| s37 | zq933a38 | 秦霜 | 石師傅，是不是哪一根釘錯了？ | 12 | 皺眉 | 6 | 2.57 秒／225 Hz |
| s38 | zq933a39 | 石木匠 | 釘得死緊，一根都沒錯。是水推不動它。 | 15 | 粗啞 | 8 | 4.64 秒／140 Hz |
| s39 | zq933a40 | 錢員外 | 哈哈！七天拆一根梁，就轉半圈！ | 12 | 放聲大笑 | 8 | 4.79 秒／100 Hz |
| s40 | zq933a41 | 錢員外 | 許秀才，連老天都不幫你，還想跟天搶水？ | 16 | 笑到岔氣 | 8 | 7.20 秒／207 Hz |

沒有台詞的鏡：s01（6 秒）、s34（6 秒）。

## 5. 還擋著開拍的事

1. 花錢：`e933d1.sh` 約 26–30 CU（80 支 582 秒，`DRY=1` 0 錯）；a19 重錄 `tools/rec933-retake.sh`（站台 TTS 一次）。都等協調者／站主。
2. 人耳聽：a35-p119、a39-p119 對韓伯 a33／a37，a28 對 a28-p85，a34，a19 重錄。
3. 挑片時看：`-an-l3` 左岸麻繩塗掉的地方（約 x 150–330、y 300–440）有沒有被畫回一條繩；s34 輪子的葉板轉半圈、停住後兩秒不再動；遠景的地平線沒有長出電線桿。
