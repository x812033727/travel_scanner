# 製作筆記：`curio-w27-marugame-seimen`（丸龜製麵，題目池 `N9105`，總分 9.55）

## 來源與查核紀錄
- 獨立查核兩輪完成（`verify-1.md` → 修訂營收／獲利口徑、倫敦 2021 時間軸、母集團海外店數、日圓單位與長輩員工分母 → `verify-2.md` **VERDICT: PASS**）。
- 16 份一次官方／法人來源全數核實：東利多控股 FY2026/3 IFRS 決算短信（合併營收 2,787.15 億日圓、日本丸龜 1,371.93 億日圓／事業利益 219.55 億日圓／利益率 16.0%／全直營 887 店）、吉野家控股 FY2026/2 花丸事業（營收 329.91 億日圓／利益 24.27 億日圓，丸龜獲利達 9.05 倍）、一橋商學院第 20 屆波特獎報告、第 3 屆日本服務大賞官方案例、丸龜製麵 2024 年 3 月全門市 100% 麵職人配置（1,632 名）與 2026 年 2 月維持 100%、FY2019 經濟產業大臣賞自動控溫大釜（省電 31.3%／省水 47.6%）、丸龜官網香川門市清單（全香川僅高松 1 店、丸龜市 0 店）、2022 年 4 月協定、逾 1 億日圓故鄉納稅與 2025 年 11 月零自售烏龍麵祭典。
- 1956 紅線：零在世或 1956 年後過世人物入名或入畫。

## 腳本與觀眾／敘事雙審（v15 定稿）
- `lint`：**0 errors, 0 warnings**（9.5 min、120 句、2,329 spoken units、7 章節、全 9 語系通過）。
- 前 300 秒獨立三審（`opening-review --check` 通過，`opening_hash: 72bb5713dbb3790a433303e0756534489f687295d4944fa430e462ef2e7325aa`）：
  - `newcomer`: **9.1**（`would_stay_300: true`, `problems: []`）
  - `scroller`: **9.0**（`would_stay_300: true`, `problems: []`）
  - `stickler`: **9.2**（`would_stay_300: true`, `problems: []`）
- 敘事雙審（`narrative.json` 通過，`narrative: 86cb84e3d8ae4f88`）：Reader 1（14/14 YES）＋ Reader 2（14/14 YES）＝ **28/28 ALL YES**。

## 視覺資產（60 鏡關鍵影格＋9 語系縮圖）
- `nobody: true` 占比：**39/60（65.0%）**；5 鏡規範 Ada（`s05`, `s18`, `s31`, `s46`, `s60`，綁定 `ada-canon-v2.png`）。
- 零 MiniMax 生圖：14 張（5 張 Ada＋9 張重畫）使用內建 `generate_image`（`$0`），46 張使用 `gemini-3.1-flash-image`（`2K`, `16:9`）。
- 獨立 2× 放大四象限審圖（共 5 輪，Round 1: 34/60 → Round 2: 50/60 → Round 3: 57/60 → Round 4: 59/60 → Round 5: **60/60 = 100% PASS**，`Border flags: 0`）。
- 主圖與 9 語系縮圖：`heimao-left` 全出血版型，全 9 語系標題皆明寫主角名稱並已逐張肉眼檢核通過。
- 後台審核關卡：`script` 與 `storyboard` 皆已推上 `/admin/videos`（`pending`）。

## 八語系翻譯與審校
- `en/ja/ko/th/es/pt/id/vi` 四路平行翻譯＋獨立 8 語系審校，修畢泰文 `m086`（空運機器誤譯修正）、`m096`（破冰成語修正）、韓文 `m062`（`말렸지만` → `권했지만`）、葡文引號與印尼文 `perajin`，縮短 8 語標題寬度至 36 全形字內並合入 `i18n/*.json`，全 9 語系 `lint` **0 errors, 0 warnings**。

## 待續（Gemini TTS 每日配額重置後）
- 尚待完成：`tts`（`Sulafat` 120 句）→ `check-audio` → `music` → 8 語 MiniMax `dub` → `render` → `clips` → `assemble` → `captions` → `qa`（11/11）→ 獨立代理一般觀眾成片評分挑刺（`review/audience-review.md`）修完重過 `qa` → `package`（4/4）→ Google Drive 零差異備份更新 → `review-push --gate final`。
