# 解說雙系列（原來如此事務所／奇聞檔案局）Google Flow 動畫化長片新規則

- **版本日期**：2026-11-25（依首支試作長片《原來如此事務所》P02 `sothatswhy-p02-cloud-rain-flow` 實戰定案，並納入《奇聞檔案局》共用標準與「去 GitHub 化」雲端單一權威規範）
- **適用系列**：《原來如此事務所》（`sothatswhy`）、《奇聞檔案局》（`curio`）
- **沿用基準**：保留 2026-11-14 V2 畫風（劇場級動畫光影 × 厚塗水粉；雙系列頭身比與人物嚴格分家）、2026-11-24 腳本與封面規格（`intro_at: "none"`、0 秒直接進鉤子、`heimao-left` 縮圖、`lint` 0 error / 0 warning、全片零燒錄字幕）。

---

## 一、去 GitHub 化：雲端硬碟單一權威原則（2026-11-25 起強制）

1. **新集 0 GitHub Commit**：
   - 成片經獨立盲審通過後，**定稿腳本、分鏡表、多語翻譯、盲審報告與製作檔一律直接存 Google 雲端硬碟，不再推入 GitHub**。
   - GitHub 僅保留網站與工具程式碼（`apps/`、`tools/video/`、`ops/`）與極小共用設定（`lexicon.json`、`theme.css`）。
2. **單集雲端標準結構**（`G:\我的雲端硬碟\AI\備份\AI劇\<系列>\<分類>\<代碼>\製作檔\<slug>\`）：
   - `腳本定稿/`：`video.json`、`script.md`、`brief.md`、`flow-shot-list.json`、`PLAN-*.md`、`i18n/*.json`、`timeline.json`
   - `review/`：`full-review-result.json`、`opening-review.json`、`audience-review.md`、`master-qa.json`、`qa-master-12frames.jpg`、`qa-thumbnails-9langs.jpg`
   - `flow-clips/`（720p 原片＋1080p30 升頻片＋4 格 QA 表＋`manifest.json`）
   - `stills/`（1376×768 靜態厚塗插畫）
   - `audio_raw/`、`dubs/`（8 語 MiniMax 配音 `.m4a`、逐句原始 WAV、對時 `.srt`、`description.<l>.txt`、`dub-qa-summary.json`）
   - `thumbnails/`（9 語系 `heimao-left` 封面）
   - `import_pkg/`（可直接重送 `cli.mjs import` 的完整上架包）與 `SHA256SUMS`（0 差異校驗清單）。
3. **新規則存放**：規則正本同步存於各系列 `_共用\製作檔\規則與規範\`（不受 `rules-sync` 單向同步覆蓋）與 `_規則與教訓\規則\`。

---

## 二、方案 B 動靜混剪與點數控管

| 項目 | 《原來如此事務所》（`sothatswhy`） | 《奇聞檔案局》（`curio`） |
| :--- | :--- | :--- |
| **目標片長** | 6–8 分鐘（16:9 寬螢幕） | 8–10 分鐘（16:9 寬螢幕） |
| **Flow 動態鏡頭數** | 35–40 支（動態佔比 **≥ 45%**，P02 實測 52.4%） | 40–48 支（動態佔比 **≥ 40%–45%**） |
| **單集 Flow 點數上限** | **≤ 500 點**（P02 實測 468 點、0 重拍） | **≤ 550–600 點** |
| **靜態場景數** | 35–45 張 `1376×768` 厚塗插畫（`beat-motion-v5`） | 55–85 張 `1376×768` 厚塗插畫（`beat-motion-v5`） |
| **下載與升頻規格** | 統一用 `Omni 1.2 Flash`（4s 24fps 12 點/支），**0 額外點數下載 720p 原檔** → `ffmpeg` Lanczos 升 1080p30、`bt709`、`-an` 抽離模型原聲 | 同左 |
| **共用片尾封存** | 1 支無文字紅章片尾（`_shared/stamp-outro-1080p30.mp4`），每集省 12 點 | 封存 2 支無文字檔案章片尾（結案章／未解章），每集省 12 點 |

---

## 三、開拍前「全片」三視角獨立盲審

1. 不再只審前 300 秒：須由三名未參與撰寫的獨立讀者（`newcomer` 新手、`scroller` 速滑族、`stickler` 較真派）審閱**完整 `00:00` 至片尾**腳本與縮圖兌現承諾。
2. 硬性過關條件：三份皆 **≥ 8.5 分**、`would_stay_300: true`、`would_stay_full: true`、`swipe_at: null`、`thumbnail_payoff_ok: true`、`problems: []`，且 `cli.mjs lint --file <local video.json>` 達 **0 error / 0 warning** 才准開拍。

---

## 四、Google Flow 0 點數前置把關與防雷規則

1. **雙專案嚴格隔離**：
   - **有角色專案**：只上傳鎖定角色設定圖與固定場景底圖（原來如此：`chief-canon-v2.png` + `kid-canon-v2.png`；奇聞：`ada-canon-v2.png` + 過世滿 70 年之單集 3.5 頭身歷史角）。
   - **無人科普／歷史空景專案**：**零角色參考圖**，專責物理圖解、雲層微距、古地圖、器物、無人船隻與建築，杜絕角色特徵污染純畫面（兩系列無人鏡佔比皆維持 45%–65%）。
2. **先 0 點數 `Nano Banana 2.1` 生圖 QA，全過才花 12 點生片**：
   - 所有 Flow 首格／尾格與靜態插畫皆先用 `Nano Banana 2.1`（0 點數）出 `16:9`（`1376×768`），逐張確認構圖、五指、角色特徵、科學／時代細節無誤後，才進 `Omni 1.2 Flash` 生片。
3. **16:9 比例靜默重置防雷**：
   - 從 Video 切回 Image 模式時 Flow 常自動重設為 `1:1`（`□`），每次生圖必確認寬銀幕（`▭` / `16:9`），下載後以程式驗 `1376×768`。
4. **安全過濾詞避雷**：
   - **原來如此（小問）**：影片提示詞禁寫 `"8-year-old"`、`"girl"`、`"child"`、`"bare face"`、`"thrusts"`，一律改寫 `"the cute 2D cartoon mascot character in a navy coat with yellow hood"`。
   - **奇聞（H／G／F 軸懸案怪談）**：禁寫血腥、屍體、暴力直擊、武器傷害等詞，改以懸疑冷暖光影、剪影、物證道具特寫與 `Ada` 驚訝反應呈現；若涉及兒童歷史角色同樣套用中性卡通描述。
5. **0 點數生圖必檢構圖地雷**：
   - 角色不可站立於書桌或陽台護欄頂端（須安全站於欄杆內側或地面）。
   - 嚴禁任何亂碼文字、街道招牌字或刻度數字；所長必露耳無耳筆、小問必無眼鏡、Ada 必維持 3.5 頭身修長比例與暗酒紅細圓框眼鏡；科學細節（如水壺壺嘴透明水蒸氣間隙）與時代道具（無現代穿越物）須 100% 精準。

---

## 五、多鏡位剪輯與留存節奏規則

1. **依故事拍（Unique Story Beats）切鏡**：不依自動拆分的零碎子句反覆切反應鏡，讓每支 4 秒 Flow 完整跑完動作弧線。
2. **長 Flow 鏡（> 7.5 秒）自動多鏡位**：全景原速播完（~4.2s）→ 切 `1.24x` 關鍵動作高潮慢放特寫（~3.6–4.4s）→ 尾格 `beat-motion-v5` 平順收尾，絕不單格死停。
3. **長靜圖自動切段運鏡**：`6.5–9.5s` 切 2 段、`> 9.5s` 切 3 段交替 `beat-motion-v5`（`push-in / pan-right / pull-out / pan-left / tilt-up`）。
4. **章節留存新紅線（P03+ 與奇聞 Flow 全面適用）**：
   - 單一章節**不可連續出現超過 3 顆靜圖**。
   - 單張靜圖時長規劃上限壓在 **≤ 8 秒**。

---

## 六、配音、CPS 自動巡檢與雙引擎 `-14 LUFS` 混音

1. **聲線配置**：
   - **原來如此**：中文 Gemini `Sulafat`（所長）＋`Leda`（小問）；8 語外語（`en, ja, ko, es, pt, id, vi, th`）走官方 `DUB_MINIMAX_VOICES` 雙聲線（越文小問依 `DUBS.md` 沿用 Gemini `Leda`）。
   - **奇聞檔案局**：單人說書，中文 Gemini `Sulafat`；8 語外語全走 `DUB_MINIMAX_VOICES` 第一聲線（全 8 語純 MiniMax）。
   - **Ultra 冷卻備援**：主機 Ultra 槽位冷卻中，經站主授權可改走網站 `SITE` 金鑰完成中文合成，不阻塞產線。
2. **逐句 CPS 異常自動巡檢（必跑）**：
   - 全片合成後自動掃描每句字速，凡 `cps < 3.5` 或 `cps > 7.0` 必抽聽音檔，即時攔截雙重朗讀或截斷（P02 成功攔截並修剪 `p088`）。
3. **多語對時與雙引擎響度驗收**：
   - 短鏡（`< 1.8s`）於翻譯工作表強制壓縮字元上限。
   - 全音軌（含 8 語 `.m4a`）採 `sothatswhy/curio` 背景配樂（`-23 dB` 側鏈壓低）＋蓋章音效 → 雙階段線性 `loudnorm`（目標 `I=-14, TP=-1.5` 預留 AAC 編碼裕度），**同時通過 `loudnorm` 與 `ebur128` 雙驗證**（`-14.0 ± 1.0 LUFS`、`TP ≤ -0.8 dBTP`、音畫時長差 `< 0.1s`）。

---

## 七、零燒錄文字、`heimao-left` 字體鎖定與驗收上架

1. **全片零燒錄文字**：影片、圖解、蓋章片尾皆無燒錄文字，9 語系共用同一支 1080p 影像母帶；外掛 `.srt` 超過 22–24 字之長句補手動換行。
2. **9 語 `heimao-left` 封面字體鎖定**：使用 `templates.mjs` 渲染封面時，將 `https://video.local/...` 改指本機 `@fontsource-variable/noto-sans-*`（TC/JP/KR/Thai）與 `theme.css`，確保粗黑無襯線字體正確套用，並輸出 3×3 九語總覽圖肉眼逐張驗收。
   - **奇聞專屬封面規定**：左上第一行（九語皆然）必點名具體人物／事件／品牌／器物（禁代名詞），左下放 3.5 頭身 `Ada` 誇張反應，右半幅放去文字特徵物／紋章／禁制章 `✕`。
3. **成片獨立盲審 → SHA-256 雲端備份 → `cli.mjs import` 上後台**：
   - 未參與製作之獨立代理進行 6 維度盲審（單項 ≥ 7.5、平均 ≥ 8.0、0 Blocker），修完微瑕才封版。
   - 先完成 Google 雲端硬碟完整備份＋SHA-256 0 差異核對，再透過 `cli.mjs import --from` → 站主後台核准與勾選語言 → `--languages` → `--publish --clips --recordings` 正式上架。
