# 原來如此事務所：教訓

只跟原來如此事務所有關的教訓。所有 AI 劇都會遇到的寫在 `shared.md`，奇聞和原來如此都會遇到的寫在 `explainer.md`。

寫法：一條一段，最新的放最上面。開頭寫日期、哪一集（slug）、誰發現的，接著寫發生什麼、為什麼、下次怎麼做。
已經變成正式規則的，搬進規則檔，這裡留一行「已升為規則：<檔案>」。

這份會自動同步到雲端硬碟 `AI劇/原來如此事務所/_規則與教訓/教訓/教訓.md`（docs/videos/rules-sync）。

- **2026-11-11，站主決定：稿子不用硬寫，8 分鐘下限保留。** 「稿子不用硬寫，品質為主，流暢的內容才重要」；同一天也說「8 分鐘下限也幫我留著好了」（PR #2069）。兩句一起讀：內容講完、講順就停，不灌水；素材撐不到 8 分鐘、要硬補的題目不開拍，放後備（`docs/videos/so-thats-why/material-20261111/README.md`）。P06 為了 2,050 字下限，盲評時刪了 120 度的岔題又得補字，就是要避免的情況。已升為規則：dialogue-pilot README §9「長度」。
- **2026-11-11，sothatswhy-p06-bubble-film，站主決定：語速調快。** 規則是 ≥ 4.5 字／秒，P06 只有 3.74；Gemini 配音沒有語速參數，style 寫「一秒四到五個字」講不到。
  用 P06 全稿只換 style 實測三種：3.74、4.39、4.95；站主聽過選 4.39 那種（「像節目主持人，一秒五個字以上，句與句緊接、不拖長尾音」），原來如此的門檻改成 4.3。
  寫法在 dialogue-pilot README §4；`tts` 結尾會印語速。style 要寫得比目標快（寫「一秒五個字以上」才講到 4.4），模型會打折扣。
- **2026-11-11，sothatswhy-p06-bubble-film，站主發現：縮圖的人被字擋住。** 系列縮圖 `subject: "right"` 只取插圖正中約 38% 寬放在右邊；
  `kid-wand` 的小問偏左，九語縮圖都只看得到欄杆和一隻手。換成 `kid-square-q`（人和方框都在中間）。下次挑縮圖鏡頭前，先用 PIL 把候選圖裁中間 38% 看一次。
  換 `thumbnail.data.shot` 會改到 visual_hash，插圖、分鏡、組裝都變「過期」：`keyframes --shot <那一景>`（不畫新圖）→ 用累積的 `pins.json` 再 `repin`
  → 重新核准分鏡 → `clips` → `assemble`，成片位元不變，成片核准仍有效。上架包已核准時，`review-push --gate publish` 不會把新縮圖送上站
  （票 `2026-11-10-review-push-a-changed-thumbnail-never`），新縮圖要直接交給站主。
- **2026-11-10，sothatswhy-p06-bubble-film，接手 session：插圖提示詞的三個坑。** (1) 代理寫的重畫提示詞常含 `no text`，`build_scenes.py` 的 `BANNED` 會擋，
  改成正面描述（clean empty corners、plain unmarked bottle、plain bare ears）；每條 ≤ 840 字，所長鏡頭要以 Waist-up／Head-and-shoulders 開頭。
  (2) 小問鏡頭寫「台灣公寓客廳」容易畫成真人照片；畫風字放最前面、背景寫 plain flat pale cream background，再用 `--seed-offset` 換種子。
  (3) 不要修圖蓋假字（會弄壞輪廓線），換種子重畫比較快。所長的黑髮是刻意的（灰髮那句會畫成灰色頭套），代理建議加回灰髮時不要採用。
- **2026-11-10，sothatswhy-p06-bubble-film，接手 session：`pins.json` 要指 `-trim.jpg`。** 插圖有紙邊時，工具的 `file` 指向 `<景>-<take>-trim.jpg`（P06 有 89 景）；
  pins 寫成原圖會用到有紙邊的版本。repin 後把跟檔案對不上的 `margins` 拿掉。
- **2026-11-10，sothatswhy-p06-bubble-film，接手 session：新容器缺的東西。** 換容器後 `tts` 沒有沿用舊錄音（153 句全部重錄，費用很少，但 check-audio 要重跑、旁白要重新核准）；
  系列設定圖要先從 `docs/videos/so-thats-why/series-sheets/characters` 還原到工作目錄的 `_series/sothatswhy/characters/`，`look` 才會沿用；
  配樂 `sothatswhy-bed-r2.m4a` 從雲端硬碟 `原來如此事務所/_共用/製作檔/sothatswhy-shared/_music/` 取回放到 `_music/`（核對 sha256）；
  repo 的 Playwright 若比容器內建的新，`render` 找不到瀏覽器，把 `/opt/pw-browsers/chromium_headless_shell-<內建版>` 連結成 repo 要的版本號，不要另外安裝。
- **2026-11-10，sothatswhy-p06-bubble-film，接手 session：長時間的步驟會被背景時限停掉。** 背景指令預設 30 分鐘、最多 2 小時；116 景 × 3 take 的插圖約 4.5 小時。
  用 `setsid nohup … & disown` 脫離 shell 跑，再用 until 迴圈等完成檔；`keyframes` 重跑會保留已畫的景。雲端硬碟備份不要跟 render／assemble 同時跑（會出現 differences），等寫檔的步驟結束再傳。
