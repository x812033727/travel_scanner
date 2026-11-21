# 第 8 集真人版 fix-polish：上架前精修重拍（2026-11-21）

依據：`review-zt/consolidated/retakes.json`（e008 的 A、B 共 7 鏡）與獨立審片報告 `review-zt/reports/e008.txt`。報告開頭說明 `ep/e008/work/final.log` 與畫格條左上角的時間是試組（293.08 秒）的舊檔，下面的秒數一律照報告量的成片剪點。
只寫提示詞與 spec，沒有送出任何工作。種子 9089101、9089102；每鏡 2 支草稿，960×544 Ref2VA。

base 的來源：`_live-e908/.../picks.json` 沒有 `motion_from` 欄，改從 `draft` 路徑判斷（`d1/out/…` 或 `fix2/out/…`），提示詞取同一個資料夾 `prompts/ref-sNN-SEED.txt`。兩個種子的 d1 提示詞都用 cmp 比過，逐字相同。

| 鏡 | tier | 審片問題（成片秒數） | base | 改了哪些句子（舊 → 新） | 圖 | 拿不準的 |
| --- | --- | --- | --- | --- | --- | --- |
| s08 | A | 木箱是淺色新松木箱，s06／s09／s13 是深褐舊箱（46.84–54.84） | `d1/prompts/ref-s08-9081102.txt`，8 秒 | 原因就在 base：`one plain wooden crate of pale raw wood … no marks or writing` → `one old wooden crate of dark weathered brown planks, the wood darkened and worn with age, two flat dark wooden battens nailed across its closed lid, about two feet long`（照 s13 成片的木條蓋子寫，沒照審片句寫鐵護角：前後鏡看不到鐵角）；`Xu Yan behind the small table` → `standing on his feet behind the small dark wooden table`，動作句加 `on his feet the whole time, bends at the waist … straightens his back`（現片他像坐著）；場景句 `small plain wooden table` → `small dark wooden table` | 照 base | 審片句寫 iron corner fittings，我沒用；s06 桌是深色、s08 現片桌是淺色，寫 dark 可能讓桌與箱同色混在一起 |
| s10 | A | 秦霜肩上是白淨新松木箱（69.38–77.38） | `d1/prompts/ref-s10-9081102.txt`，8 秒 | 木箱句換成跟 s08 同一句的深褐舊箱；拿皂句加 `palm-sized and one finger thick`（同 s13 的皂）與 `her face turned toward the broad back of the escort chief` | 照 base | base 原有的 `no blade, no knife and no weapon…` 是否定名詞，但 d1 這鏡沒有長出兵器，屬於有效的舊句，保留不動 |
| s22 | A | 許硯正對鏡頭喊片名句；門房在他背後、深藍袍露臉，跟 s21／s24／s25 的灰袍背影不同人（157.31–165.31） | `d1/prompts/ref-s22-9081101.txt`，8 秒 | 構圖 `medium close-up of Xu Yan … toward the gatekeeper … off screen right` → 從台階頂、門房身後過肩往下拍：門房灰藍交領長衫、只露背與後腦，占畫右三分之一，`his face never seen`；許硯在下兩階、身體與臉朝上看著門房、眼睛鎖在他臉上，表情逐部位寫（眉壓、眼瞇、鼻翼張、胸起伏、一字一字）；背景兩女縮小虛焦、臉朝馬；動作 `comes up three steps … flings his right arm …` → 站在台階上，最後幾個字時右臂一甩指向畫左的紅太陽、停一拍、再轉回門房（一鏡一個動作）；人數句改成「許硯與門房的背影之外只有馬邊兩女」；運鏡 tracking → 慢推 | 照 base（門房沒有參考圖，只拍背影） | 畫面上 3 個有名字的人加門房背影共 4 人，preflight 沒報 four，但仍可能分身；s23 接點（他指太陽時正前方是大門、門口沒人）要挑片時一起看 |
| s25 | B | 拔出的是細長直刃像劍，還舉到頭邊（176.9–178.3） | `d1/prompts/ref-s25-9081102.txt`，6 秒 | 原因在 base：`a long narrow iron blade with a slightly hooked tip` → `a short heavy chopping blade of dark iron as broad as her palm and as long as her forearm, widening to a squared, slightly hooked tip, on a short plain wooden handle wrapped in black cloth`（照 s25b／s26／s30 成片的寬柴刀）；拔刀改成 `sliding it out low and straight down past her hip in one smooth motion … hang point-down along her right thigh, her right arm straight at her side until the last frame`；構圖補刀柄在腰帶右邊；冷臉補 `lips pressed into a flat line, jaw set` | 照 base | s25b、s26、s30 的提示詞仍寫 long narrow blade（已拍、成片是寬刀），這次不動；刀形只能靠文字，沒有柴刀道具圖 |
| s32 | B | 錢員外的臉停格 2.5 秒、許硯的收尾句蓋在停格上；沒有捶桌（229.56–240.06） | `d1/prompts/ref-s32-9081101.txt`，8 → **10 秒** | 原因在 base：`pounds his fist down on the table below the frame`（拳頭在畫外）→ 景別 `close-up … from the chest up` 改成坐在紅木桌後的腰上近景，桌面前緣橫在畫面下緣，上面七八顆小碎銀（接 s31），右拳先放在桌上；動作改成舉右拳捶在畫內的桌面、碎銀跳散；台詞後 `presses his lips into a tight line and keeps them shut, breathing hard through his nose, nostrils flaring, jaw muscles working, chest heaving, his eyes following someone walking away toward screen left, alive and moving until the last frame` | 照 base | 買 10 秒（審片建議；兩句台詞約 10 秒，base 8 秒才會停格）。許硯那句是錄音畫外，提示詞照 base 不寫 |
| s33 | A | 唐小棠變單一後髻，前後鏡是雙丸子頭（240.06–246.61） | `fix2/prompts/ref-s33-9081301.txt`，6 秒 | 髮型 `her two looped buns knocked a little askew` → `her hair exactly as in <Picture 2>: two round looped buns, one on each side of the crown, both clearly seen, each tied with a long pink silk ribbon hanging down past her shoulder, the left bun tilted a little and one pearl pin slanting`；`wide shot … everyone small` → `medium wide shot … framed from the knees up`，唐小棠在離鏡頭最近的位置，頭看得清楚 | **拿掉 `tangxiaotang-angle-b-l1`**（側後角度，兩個髻前後疊成一個，最像成片的單髻），8 → 7 張，header 與 `<Picture N>` 重編 | 換圖是推測：s30、s37 送了同一張 angle-b 仍是雙髻。base 的 `no sword, no knife…` 是 fix2 刻意加的（d1 有兵器問題），保留 |
| s39 | A | 同 s33，唐小棠單髻（277.57–285.57） | `d1/prompts/ref-s39-9081102.txt`，8 秒 | 只改髮型句（同 s33）；擦汗、上馬、秦霜抖韁 base 已拍對，不動 | 同 s33 拿掉 angle-b，7 張 | 一鏡三個動作（擦汗→上馬、抖韁）違反一鏡一動作，但 base 這樣寫已拍成，劇本需要，保留 |

## 檢查（2026-11-21）

- `polish-build.py 8`：7 鏡、14 支草稿、108 秒 → `~/mokaair-work/videos/zhong-tian-qu-qi-e908-dh/runpod/live/fixp/colab-jobs.json`
- `preflight-prompts.py`：0 error(s)、0 warning(s)
- `h3r.sh check --manifest`：0 error(s)、0 warning(s)

產生方式：從 base 逐句 `replace`（每句必須在 base 裡剛好出現一次），header、角色外貌錨句、`never the mood. `、`One continuous shot.` 與台詞句沒動。

## 挑片時要看的

- s08／s10：箱子是深褐舊箱、每格同色；s08 許硯是站著；箱面沒有字或牌子。
- s22：說話時臉朝門房、不朝鏡頭；門房只有背影、灰藍長衫、沒有露臉；兩女有沒有分身或看鏡頭；指太陽的方向在畫左；聽寫核對「太陽還沒落」原聲。
- s25：刀從頭到尾是寬柴刀、垂在腿邊沒有舉起。
- s32：有捶桌、碎銀跳；台詞後到片尾臉還在動（喘、下顎、眼睛），沒有笑。
- s33／s39：唐小棠兩個圓髻、兩條粉緞帶，逐格放大看側臉與背面。
