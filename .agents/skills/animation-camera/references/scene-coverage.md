# 一場戲的空間，與同一場戲的兩種寫法

前半是空間規則（軸線、畫面側、視線、進出），沒有任何程式檢查它們；後半把一場 12 鏡的對話戲寫兩次：第一次照這份 skill 寫，附 `shot_reading.mjs` 的實際輸出、craft 的列與三條路線的估價；第二次照試拍的習慣寫，逐鏡標出錯在哪、哪個讀者或模型會怎麼讀錯、要花多少錢才會發現。五種鏡位的用途在 `.agents/skills/youtube-video/references/drama-craft.md` 第二節，這裡不重複。

## 一、先定空間（人的事，程式不檢查）

1. **軸線**：兩個人之間畫一條線（對桌戲就是桌沿），整場戲攝影機留在線的同一側。這樣 A 永遠在畫面左、B 永遠在畫面右，觀眾不用重新找人。要越軸，先給一個全景（兩人都在畫面裡）再越，或在角色移動的鏡頭裡越。
2. **畫面側寫進每一鏡的 prompt**：`Ayu on screen left, facing right`、`Chen off screen right`。圖片模型只看這一鏡的文字，不知道上一鏡誰在哪；試拍用 `on screen left`／`off screen to the right` 這種寫法，S09 的過肩才把桌子軸線保住。
3. **視線**：反打的兩個近景，說話的人看畫外右、聽的人看畫外左，眼睛高度一樣（坐著對坐著、站著對站著）。眼睛看鏡頭只在設計好的時候。`prompt` 寫 `eyes on Chen off screen right`，不寫「看向鏡頭外」。
4. **過肩**：寫清楚從誰的肩後、肩在畫框哪一邊、肩占多少（`from behind Ayu's right shoulder at frame left onto Chen`）；兩個人的 id 都列進 `characters`（≤ 3），兩張設定圖都會當參考，judge 兩個人都問 identity。
5. **插鏡**：拍東西不拍人；prompt 寫 `Chen speaks off screen`，`speaker` 仍是 Chen（反應鏡與插鏡放的是畫外那個人正在說的那一句，drama-craft.md 第四節）。手要入鏡就寫哪隻手、袖口、腕上的東西，不寫臉。`characters` 列不列（這裡建議留空，`visual-quality.md` 第二節要留資料綁定，兩種都沒驗穩）在 `SKILL.md` 的「寫 prompt」插鏡條，一場戲裡只用一種。
6. **進出**：從軸線的同一側進場（畫外左進就從畫面左邊進），離場朝同一邊出；一個進場要自己一支素材（8 秒內走完），不要塞進別人的反應鏡。
7. **重新交代**：移動、進出、新的節拍開始之後給一個全景或多人鏡，約兩秒（craft `size.reestablish`：最多連 9 鏡沒有全景或多人鏡；`size.wide` 5–30%，都是編輯判斷）。
8. **連戲帳**：一張關鍵影格通過後，把真圖裡的腕側、袖長、髮長、道具數、門的狀態抄進後面每一鏡的 prompt。沒有欄位放它，寫在這一集的回報或 review 筆記裡，每張通過的關鍵影格一行，後面每一鏡照抄；試拍的 S04 R02 就是沒抄而被退（`model-misreads.md` 第一節），來源從沒寫過左右腕。樣子：

   ```
   s04 take 2 通過：錶在右腕、袖口挽到肘、借據摺著在左手、燈在右上、門關著 → s05 到 s12 的 prompt 照抄這五件
   ```

## 二、示範場（可接受版）：魚攤還債，12 鏡

空間：攤位的櫃檯從左到右橫過畫面，攝影機留在顧客這一側；阿玉（`ayu`）在畫面左、面朝右，老陳（`chen`）在櫃檯後、畫面右、面朝左；道具是一張摺好的借據、一只錢袋、一座黃銅秤。借據整場都是摺著的（連戲帳第一條）。`look.preset: "anime-2d"`，`look.negative` 保留 preset 的值（Lite adapter 會把它接成 `Avoid: …`，不必為 Lite 清空；`error-catalogue.md` #23），`look.motion: ""`（鎖定機位為主：`shot_reading` 對任何非空的 `look.motion` 配鎖定鏡頭都報 `look.motion`），`subtitles.burn_in: false`。

| 鏡 | `camera` | `prompt`（要點） | `motion` | 台詞／`characters` | 註 |
| --- | --- | --- | --- | --- | --- |
| s01 | `Wide shot, locked` | 全景：櫃檯橫過畫面，阿玉停在近側畫面左面朝右，老陳在櫃檯後畫面右面朝左，秤與刀在前，一盞燈 | `Chen sets a fish on the scale pan.` | chen「阿玉，這麼早？」／`[ayu, chen]` | 開場就在事件裡；全景交代軸線 |
| s02 | `Medium shot, slow push in` | 中景：阿玉近側畫面左，面朝畫外右的老陳，右手拿著摺好的借據懸在秤盤上方，燈光打右臉 | `Ayu lays the folded note on the scale pan.` | ayu「我哥的借據。」／`[ayu]` | 第一格是動作之前（紙還在手上） |
| s03 | `Insert of the note on the scale pan, locked` | 插鏡：秤盤上一張摺好的借據，盤還抬著，阿玉戴紅繩的右手剛從畫面左縮回；老陳在畫外說話 | `The pan dips under the note.` | chen「這張，三萬。」／`[]` | 畫外說話者不列；手只寫手與腕飾 |
| s04 | `Medium close-up, locked` | `Medium close-up of Chen behind the counter on screen right`, 面朝畫外左，右手往下伸向畫框底的秤盤，燈光從右 | `Chen lifts the folded note off the pan.` | chen「三萬，一毛都不能少。」／`[chen]` | 這個鏡位後面回來一次 |
| s05 | `Medium close-up, locked` | `Medium close-up of Ayu on screen left`, 面朝畫外右，左手一只布錢袋懸在櫃檯上方 | `Ayu sets the coin bag down on the counter.` | ayu「這裡兩萬。」／`[ayu]` | 反打：視線方向相反、高度相同 |
| s06 | `Over-the-shoulder from behind Ayu on Chen, locked` | 從阿玉右肩後（肩在畫框左）拍畫面右的老陳，錢袋在兩人之間，摺好的借據在他左手，右手已按在袋上 | `Chen pushes the coin bag back across the counter toward Ayu.` | chen 兩句「少一萬，借據就留在我這。」「妳哥的事，我不管。」／`[ayu, chen]` | 兩句掛一鏡：揭露前的停留；兩個 id 都列 |
| s07 | `Close-up, slow push in` | 阿玉的臉，畫面左，眼睛看畫外右的老陳，燈光在右臉，櫃檯邊緣虛在畫框底 | `Her jaw tightens.` | ayu「老陳。」／`[ayu]` | 反應鏡（look-only），兩字短鏡 |
| s08 | `Medium close-up, locked` | `Medium close-up of Chen behind the counter on screen right`, 摺好的借據在抬起的右手，眼睛抬向畫外左 | `He looks up from the note at Ayu.` | chen「叫我也沒用。」／`[chen]`；`source: { shot: "s04", from_s: 1.5 }` | 回到 s04 的鏡位：`camera` 整行與 prompt 第一個子句照抄，不畫圖不買素材。`from_s` 看來源買到的秒數：s04 約 2.93 s，伺服器預設的 Omni（與 H3）照 `clipSeconds` 只買 4 s，1.5 ＋ 2.2 ＝ 3.7 放得下，重播 s04 的 1.5–2.93 s；Lite 1080p 買 8 s 才切得到 s04 用過的尾巴之後（`from_s: 4`） |
| s09 | `Two-shot, locked` | 從顧客側的雙人鏡：阿玉畫面左，錢袋回到她面前、右手在抽繩上；老陳畫面右看著她；秤在中間 | `Ayu pulls the drawstring of the coin bag open.` | 無台詞：場景層 `"action_seconds": 2`、`"lines": []`（不在 `data` 裡）／`[ayu, chen]` | 新節拍（她升級）用多人鏡重新交代；無聲動作鏡 |
| s10 | `Overhead insert of the scale pan, locked` | 俯拍插鏡：秤盤，打開的錢袋在阿玉雙手裡傾向盤上（手在畫框左），第一批硬幣在袋口；老陳在畫外說話 | `Coins pour from the bag onto the scale pan.` | chen「阿玉！」／`[]` | 俯拍是角度，craft 把它當修飾詞跳過，圖片模型讀得到 |
| s11 | `Medium close-up, slow push in` | `Medium close-up of Chen behind the counter on screen right`, 面朝左，右手停在盤上方的空中，眼睛看著硬幣，摺好的借據還在左手 | `He stares at the coins.` | chen「……算了，兩萬就兩萬。」／`[chen]`；`visual: "still"` | 反應停留用靜圖：0.134 一張；推近的第 0 格是整張關鍵影格，會驗 PSNR；寫 `locked` 會被問是不是設計好的 hold |
| s12 | `Wide shot, slow pull out` | 全景，跟開場同一側：阿玉畫面左伸手越過櫃檯去拿老陳左手裡摺好的借據，硬幣堆在秤盤，燈在上 | `Ayu takes the note from his hand.` | ayu「借據，我拿走了。」chen「下次別來了。」／`[ayu, chen]` | 收場重新交代；拉遠的第 0 格不驗 PSNR |

### `shot_reading.mjs` 的實際輸出（2026-10-03，檔名改成占位）

```
<VIDEO_DOCS>/video.json: 12 個鏡頭（10 clip、1 still、1 cut）；look anime-2d，沒有 look.motion；production profile no

[s01] clip · 約 2.2 s · 1 lines（chen） · characters: ayu, chen
  景別  craft shotSize: ws（全景或多人，family wide），讀自 camera
  運鏡  craft cameraMove: locked | slides cameraMove: locked | assemble motionMove（still 時）: locked（第 0 格驗 PSNR: yes）
  動作  isLookOnly: no | 關鍵影格 prompt 819/4000 字

[s02] clip · 約 2.2 s · 1 lines（ayu） · characters: ayu
  景別  craft shotSize: ms（中景，family ms），讀自 camera
  運鏡  craft cameraMove: push | slides cameraMove: push in | assemble motionMove（still 時）: push-in（第 0 格驗 PSNR: yes）
  動作  isLookOnly: no | 關鍵影格 prompt 617/4000 字

[s03] clip · 約 1.97 s · 1 lines（chen） · characters: -
  景別  craft shotSize: insert（插鏡，family insert），讀自 camera
  運鏡  craft cameraMove: locked | slides cameraMove: locked | assemble motionMove（still 時）: locked（第 0 格驗 PSNR: yes）
  動作  isLookOnly: no | 關鍵影格 prompt 414/4000 字

[s04] clip · 約 2.93 s · 1 lines（chen） · characters: chen
  景別  craft shotSize: mcu（臉，family face），讀自 camera
  運鏡  craft cameraMove: locked | slides cameraMove: locked | assemble motionMove（still 時）: locked（第 0 格驗 PSNR: yes）
  動作  isLookOnly: no | 關鍵影格 prompt 559/4000 字

[s05] clip · 約 1.97 s · 1 lines（ayu） · characters: ayu
  景別  craft shotSize: mcu（臉，family face），讀自 camera
  運鏡  craft cameraMove: locked | slides cameraMove: locked | assemble motionMove（still 時）: locked（第 0 格驗 PSNR: yes）
  動作  isLookOnly: no | 關鍵影格 prompt 530/4000 字

[s06] clip · 約 5.4 s · 2 lines（chen） · characters: ayu, chen
  景別  craft shotSize: ots（臉，family face），讀自 camera
  運鏡  craft cameraMove: locked | slides cameraMove: locked | assemble motionMove（still 時）: locked（第 0 格驗 PSNR: yes）
  動作  isLookOnly: no | 關鍵影格 prompt 757/4000 字

[s07] clip · 約 1.5 s · 1 lines（ayu） · characters: ayu
  景別  craft shotSize: cu（臉，family face），讀自 camera
  運鏡  craft cameraMove: push | slides cameraMove: push in | assemble motionMove（still 時）: push-in（第 0 格驗 PSNR: yes）
  動作  isLookOnly: yes | 關鍵影格 prompt 540/4000 字

[s08] cut from s04@1.5s · 約 2.2 s · 1 lines（chen） · characters: chen
  景別  craft shotSize: mcu（臉，family face），讀自 camera
  運鏡  craft cameraMove: locked | slides cameraMove: locked | assemble motionMove（still 時）: locked（第 0 格驗 PSNR: yes）
  動作  isLookOnly: yes | 關鍵影格 prompt 499/4000 字

[s09] clip · 約 2 s · 0 lines（-） · characters: ayu, chen
  景別  craft shotSize: group（全景或多人，family wide），讀自 camera
  運鏡  craft cameraMove: locked | slides cameraMove: locked | assemble motionMove（still 時）: locked（第 0 格驗 PSNR: yes）
  動作  isLookOnly: no | 關鍵影格 prompt 720/4000 字

[s10] clip · 約 1.5 s · 1 lines（chen） · characters: -
  景別  craft shotSize: insert（插鏡，family insert），讀自 camera
  運鏡  craft cameraMove: locked | slides cameraMove: locked | assemble motionMove（still 時）: locked（第 0 格驗 PSNR: yes）
  動作  isLookOnly: no | 關鍵影格 prompt 393/4000 字

[s11] still · 約 2.7 s · 1 lines（chen） · characters: chen
  景別  craft shotSize: mcu（臉，family face），讀自 camera
  運鏡  craft cameraMove: push | slides cameraMove: push in | assemble motionMove（still 時）: push-in（第 0 格驗 PSNR: yes）
  動作  isLookOnly: yes | 關鍵影格 prompt 548/4000 字

[s12] clip · 約 4.77 s · 2 lines（ayu, chen） · characters: ayu, chen
  景別  craft shotSize: ws（全景或多人，family wide），讀自 camera
  運鏡  craft cameraMove: pull | slides cameraMove: pull out | assemble motionMove（still 時）: pull-out（第 0 格驗 PSNR: no）
  動作  isLookOnly: no | 關鍵影格 prompt 737/4000 字

讀了 12 個鏡頭，沒有陷阱：三個讀法讀到的就是寫的；畫面好不好仍要看小樣
```

（秒數是 lint 的估法：每字 0.24 秒、每句 0.3 秒、每鏡 0.7 秒，`tools/video/core/timeline.mjs`；旁白量過之後用 timeline 的格數。s08 的 PSNR 是 `assemble` 拿第 0 格對 s04 素材第 1.5 秒那一格，`sourceFrameProblem`。s08 若寫 `from_s: 4`，這裡會多一條 `source.bought`：s04 在 Omni／H3 下只買 4 s，4 ＋ 2.2 超過它，lint 的 10 秒放行、`clips` 要到 s04 買下之後才 `needs_review`。）

### craft 的列（`drama_craft_check.mjs`，24 列全過）

中位數 2.2 秒、第 90 百分位 3.9 秒、最長 5.4 秒、長短差 2.7；前 10 秒 5 鏡、前 30 秒 12 鏡、第一句角色台詞 0.0 秒；台詞中位數 5 字、旁白 0%；景別都有名、`camera` 與 `prompt` 沒有分歧；臉 50%、插鏡 17%、全景或多人 25%、最長 7 鏡沒有全景、同景別同人連 1；只有眼神 25%（s07、s08、s11），連 2；開場三鏡有事發生；同一運鏡連 1；鎖定 8 之 12，最長連 4；鏡位 1 個用了兩次（s04、s08），10 個用一次；沒有「and／then」的雙動作；溶接 0。`lint` 的鏡頭規則也過（剩下的錯是 `brief.md` 與章節數，屬整集文件，不屬鏡頭）。

### 錢（價目：`apps/api/app/video_media/catalog.py` 2026-09-26 讀；judge `JUDGE_USD_PER_CALL = 0.01`；每項都是手算，`animation-production` 的 `episode_estimate.mjs` 做同一件事）

| 路線 | 關鍵影格（11 張：s08 不畫） | 片段（10 支：s08 切素材、s11 靜圖） | 一次成功合計 | 上限用滿（圖 ×3、片段 ×2） |
| --- | --- | --- | --- | --- |
| Veo 3.1 Lite 1080p（固定 8 秒，US$0.08/s） | 11 × (0.134 + 0.01) = 1.58 | 10 × (0.64 + 0.01) = 6.50 | **8.08** | 4.75 + 13.00 = 17.75 |
| 同上，s08 不切素材、自己買一支 | 12 × 0.144 = 1.73 | 11 × 0.65 = 7.15 | 8.88（切素材省 0.79） | 19.49 |
| Gemini Omni 1.1 Flash（4–10 秒，US$0.15/s；10 支要 43 秒） | 1.58 | 43 × 0.15 + 0.10 = 6.55 | 8.13 | — |
| MiniMax H3 2K API（US$0.13/s；43 秒） | 1.58 | 43 × 0.13 + 0.10 = 5.69 | 7.27 | — |
| Hailuo 網頁 Pro 的 credits（H3 768P 7 點／秒、2K 12 點／秒；**年繳**頁面價 US$0.047／0.081 per s，月繳攤是 0.086／0.147；片段不經 judge） | 1.58（圖仍由產線畫） | 年繳 43 × 0.047 ≈ 2.02（768P）／≈ 3.48（2K）；月繳 ≈ 3.70／6.32 | 年繳 ≈ 3.6／5.1；月繳 ≈ 5.3／7.9 | 方案月額 4,500 credits，`animation-production` 算占比；網頁可照鏡長買，`animation-preproduction` 的 `shot_plan.mjs` 逐鏡算 |

Lite 買 80 秒、用到 26.4 秒：利用率 33%（這場戲的估算；成片剪多少秒還要看旁白實測）。這就是切素材與靜圖的價值：s08 與 s11 兩鏡 0.144 加 0 對 1.44。

## 三、同一場戲的試拍式寫法：每鏡標錯

同樣的故事，用《喜宴未散》兩集 81 鏡的習慣寫一遍。每一行是真會寫出來的句子，右邊是哪個讀者或模型會怎麼讀、哪一關抓到（或抓不到）、要花多少錢才知道。

| 鏡 | 寫法 | 錯在哪 | 誰讀錯、哪關抓、代價 |
| --- | --- | --- | --- |
| s01 | `camera: "Locked view of the stall."` | 沒有景別（view 不是修飾詞也不是景別） | craft `size.named`；`shot_reading` `size.none`；圖片模型自己決定多遠 |
| s02 | `camera: "Locked medium close-up."`；`prompt` 以 `Locked medium close-up. Frame for this one action: Ayu lays the note…` 開頭，結尾再貼一段每鏡共用的「Same approved setting and table axis…」 | prompt 逐字重抄 camera 整行，加共用段 | `shot_reading` `prompt.camera`；lint `promptSimilarity ≥ 0.8` 警告相鄰鏡頭幾乎相同；`setupKey` 把不同鏡位黏成同一個，`size.setups` 算錯；圖片模型看到兩次同樣的話，沒有多拿到任何畫面資訊 |
| s03 | `camera: "Locked hand close-up."`；`prompt` 寫 `Ayu, 26, straight black hair tied back, dark grey rain jacket…, her hand on the pan`；`characters: ["ayu"]` | 插鏡寫了整個人 | 試拍 S04 R01：畫成上半身廣鏡；judge 問 identity 一張沒臉的圖；一張 0.144，人看了才知道 |
| s04 | `camera: "Locked medium close-up."`；`prompt: "…the folded note already in his hand"`；`motion: "Chen lifts the folded note off the pan."` | 第一格的狀態已經在動作之後 | 片段從拿好的狀態開始，動作無處可做；E2 S34 讀稿抓到，沒抓到就是 0.65 一支 |
| s05 | `camera: "Locked medium close-up."`；`prompt: "Medium shot of Ayu…"` | `camera` 與 `prompt` 景別不同家 | craft `size.agree`；`shot_reading` `size.disagree`；圖片模型兩種都看到，畫哪種看運氣 |
| s06 | `camera: "Locked over-the-shoulder reaction shot."`；`characters: ["chen"]`；`speaker: "chen"` 三句 | 過肩只列一人；三句掛一鏡 7 秒 | 新娘的肩膀沒有參考圖，judge 不問她；8 秒素材剪 7 秒剩不到 1 秒餘裕（profile 每鏡 ≤ 8 秒含停頓，lint 錯誤超過才擋） |
| s07 | `camera: "Locked close-up."`；`motion: "Her fingers tighten once around the note."` | 微顫交給片段模型 | craft 算 look-only（對）；試拍 S01 R03／S03 R01：多出手、錶、筆，兩次重拍 US$1.28 歸零；這裡該是靜圖或一個看得見的動作 |
| s08 | `camera: "Locked medium close-up."`（prompt 第一個子句與 s04 不同）；`source: { shot: "s04", from_s: 5 }`，台詞 4 秒 | 回鏡位沒照抄；5 ＋ 4 ＞ 8，更超過 s04 在 Omni／H3 下買到的 4 秒 | `setupKey` 不同，`size.setups` 看不出回鏡位；lint（production profile）錯誤 `a cut from another shot's clip must end inside them`；`shot_reading` `source.length`；沒有 profile 時 10 秒內 lint 放行，`shot_reading` 的 `source.bought` 先報，不然 `clips` 要到 s04 買下之後才 `needs_review` |
| s09 | `camera: "Locked medium close-up."`，第三個連續的 MCU 拍同一個人 | 連三個同景別同人 | craft `size.stall`（≤ 2）；畫面像簡報 |
| s10 | `camera: "Locked overhead insert; Chen speaks."`；`characters: ["chen"]` | 畫外說話者列進 characters | `shot_reading` `cast.offscreen`；judge 問 identity_chen 一張只有手的圖；craft `size.listeners` 少算一個反應 |
| s11 | `visual: "still"`，`camera: "Locked medium close-up."`，`look.motion` 留 preset 的 `gentle camera move…` | 靜圖整格不動像定格；同一份 `look.motion` 接在前面每一支 clip 的 `locked` 後面 | `shot_reading` `still.locked`（問這是不是設計好的 hold）與每一支鎖定 clip 的 `look.motion`；試拍自己覆寫了 `look.motion`，沒文件說要 |
| s12 | `camera: "Locked wide shot; she rises and the camera pans left to follow"` | 一行裡三件事：locked、rises、pan left | 三個讀者都讀 `locked`（craft 的 locked 不受位置限制；slides 與 assemble 的順序是 drift → locked，在 push、pan、tilt 之前），`rises` 與 `pans left` 都沒用到；`shot_reading` `camera.person`；片段模型收到互相矛盾的原文。寫 `Wide shot, pan left` 就好，想要畫面往左跑要寫 `pan right` |

整場 12 鏡全部 `Locked`、沒有一個全景：craft 另外會報 `size.wide` 0%、`size.reestablish` 12、`motion.locked` 12 之 12，這正是試拍 E1 的讀數（量到的：鎖定 40 之 40、全景 0%、前三鏡全是反應）。
