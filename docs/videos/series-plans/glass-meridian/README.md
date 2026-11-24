# 玻璃地平線（Glass Meridian）｜十季歐美 AI 影集企劃包

在人類最後一座 200 層全透明垂直穹頂城「子午線一號（Meridian One）」裡，30 歲中籤者搭上金色電梯前往陽光普照的日冠後便音訊全無。外牆維修工程師 **Clara Vance（克拉拉・范斯）** 在暴風雪中從**穹頂外側**撬出五年前「墜亡」丈夫留下的黃銅工牌——上面留有不到 48 小時的新鮮指紋與三道刻痕，進而一步步掀開十二座玻璃巨塔、250 年地磁災變「灰潮」與軌道方舟 `Meridian Zero` 長達兩百年的生存騙局。

本包依 2026-11-24 站主核准之規格整理：**真人寫實電影感（`live-action-cinematic`）**、**10 季 × 每季 12 集＝全劇 120 集（封閉終局）**、**YouTube／串流高密度版（每集約 7–9 分鐘、目標 8 分鐘；單季 12 集可無縫接成約 95 分鐘單季大電影合集）**、**英文原音為主（鎖定歐美全球市場，同步繁中＋7 語共 9 語字幕／配音）**。

## 閱讀順序

1. [設定集](setting.md)：垂直玻璃城結構、五大硬規則（含「無紙無私網」AI 防亂碼設計）、五大勢力、12 位人物真人視覺與口音基準、12 條跨季長線伏筆與不可逆代價。
2. [十季總綱](outline.md)：由單塔裂縫到跨塔內戰、軌道反擊與拆牆終局的升級曲線。
3. 分季細綱：全劇 120 集逐集冷開場鉤子、兩段高張力節拍、交替集末懸念（相鄰兩集懸念型絕不重複）與連貫狀態。
4. [連貫性與伏筆帳](continuity.md)、[逐集狀態 CSV](continuity.csv)。

| 季 | 季名（中／英） | 集數 | 細綱 |
| ---: | --- | --- | --- |
| 1 | 外牆裂縫 / *The Seam* | E001–E012 | [season-01.md](season-01.md) |
| 2 | 盲區四分鐘 / *Four Minutes of Frost* | E013–E024 | [season-02.md](season-02.md) |
| 3 | 第二座塔 / *Meridian Two* | E025–E036 | [season-03.md](season-03.md) |
| 4 | 十二種牢籠 / *Twelve Cages* | E037–E048 | [season-04.md](season-04.md) |
| 5 | 零號中樞 / *The Pivot* | E049–E060 | [season-05.md](season-05.md) |
| 6 | 白紙醫生 / *Tabula Rasa* | E061–E072 | [season-06.md](season-06.md) |
| 7 | 玻璃內戰 / *Shattered Glass* | E073–E084 | [season-07.md](season-07.md) |
| 8 | 第十三子午線 / *Meridian Zero* | E085–E096 | [season-08.md](season-08.md) |
| 9 | 七十二小時灰潮 / *The Ash Tide* | E097–E108 | [season-09.md](season-09.md) |
| 10 | 沒有玻璃的天空 / *Open Horizon* | E109–E120 | [season-10.md](season-10.md) |

## AI 真人寫實製作防呆設計

- **無紙無私網禁令（The Clear-Line Act）**：全劇鏡頭內零紙本可讀文字、零手機或螢幕文字；所有情報改由無字金屬工牌（顏色＋凹槽刻度）、玻璃音柱語音與人物微表情交付，根絕 AI 影片文字亂碼。
- **六主角強區分防撞臉**：六位核心主角在族裔、性別、年齡、髮型、服裝主色（深橘灰／深藏青／象牙白＋酒紅／橄欖綠／深卡其／深黑＋三圈紅膠帶）與英文口音（US／UK London／東歐／微西語美式／北美／北歐）全面拉開。
- **物理時間窗驅動鉤子**：外牆 180 秒失溫倒數、每日凌晨 03:00 四分鐘全城霧化除霜盲區、S9 全季 72 小時即時倒數，讓每集自帶高壓節奏。
- **開拍前關卡**：目前 `ready_for_import` 為 `false`；付任何點數或進入 S1 製作前，須依 `animation-preproduction` 與 [WRITING.md](../../drama/WRITING.md) 先鎖定 6 位核心角色定妝圖、4 個第一季母場景圖與 S1E01 開場連續 3 鏡小樣（Pilot）。

## 本機重建與驗證

在倉庫根目錄執行（完全離線、不花費任何模型或生成費用）：

```bash
node docs/videos/series-plans/glass-meridian/build.mjs
node docs/videos/series-plans/glass-meridian/build.mjs --check
node docs/videos/series-plans/glass-meridian/validate.mjs
node --test docs/videos/series-plans/glass-meridian/validate.test.mjs
npm run check:tasks
```
