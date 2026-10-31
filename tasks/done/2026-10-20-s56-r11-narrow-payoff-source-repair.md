---
id: 2026-10-20-s56-r11-narrow-payoff-source-repair
title: S56 R11 move merger payoff and fix narrow source visuals
status: done
priority: P2
area: docs
owner: codex-gpt6-s56-r11-author
claimed_at: 2026-10-20T22:43:11Z
created_at: 2026-10-20T22:43:09Z
completed_at: 2026-10-20T22:45:02Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s56/video.json
  - docs/videos/curio-s56/claims.md
  - docs/videos/curio-s56/script.md
  - docs/videos/curio-s56/review/r11-author-fix.md
---

# S56 R11 move merger payoff and fix narrow source visuals

## Why

S56 R10 正式 OR 為 12／13 HOLD，兩位乾淨讀者都在必答 `no_recap` 指出 `s56079` 已說出 `s56174` 同一個兩岸火勢合流結論。R10 獨立來源／書面畫面另因 `s56112` 無據的「催車」和開場 `s56011`／`s56013` 太早畫出福斯特的隨身箱 HOLD。本票把合流答案留在片尾，只做這幾處窄幅修稿，再交新凍結稿獨立覆核。

## Definition of done

- [x] `s56079` 成為來源支持的近距離問句，由 `s56081` 煤氣設施回答；`s56174` 保留為全稿唯一火勢合流口說答案，消防分兵伏筆改在該處回收。
- [x] `s56112` 只說裝車後按約付款、坐車北行，未聲稱他催車；開場兩個 prompt 拿掉尚未收拾的箱子。
- [x] `video.json`、`claims.md`、重產 `script.md` 及 [R11 作者交接](../../docs/videos/curio-s56/review/r11-author-fix.md)精確對齊並保存五檔 SHA，其他史料／畫面界線維持。
- [x] 250 字元／分鐘估算開場 <=60 秒、正文 >=8 分鐘；shot 占比 >=70%；lint 0 errors／0 warnings。

## Steps

- [x] 等 R10 正式敘事 OR、來源 HOLD 與合併任務封存後，核對五檔原稿 SHA 及兩位盲讀者的相同 `no_recap` 引句。
- [x] 只改兩個口說、三個 prompt，改接舊伏筆並加煤氣設施短伏筆；從影片資料重產劇本及對齊主張表。
- [x] 記錄完整 R10→R11 差分、五檔 SHA、稿面時間與未決關卡；交下一位獨立來源／畫面覆核者，不代做盲評、政策或付費音訊。

## How to verify

`node tools/video/cli.mjs script --slug curio-s56` 重產；`node tools/video/cli.mjs lint --slug curio-s56 --json` 為 0 errors／0 warnings。程式比對 `script.md === screenplay(video.json)`、154 個唯一逐句 ID、`claims.md` 154 列 ID／全文一致、121 景（118 shot／3 big）、18 條伏筆前設先於回收。250 字元／分鐘估算開場 59.33 秒、正文 699.63 秒；325 字元／分鐘估算開場 48.33 秒、正文 566.87 秒。R10→R11 差分及五檔 SHA 見作者交接。`npm run check:tasks` 與 `git diff --check` 在完成前另跑。

`npm run check:tasks` exit 0（僅既有其他任務逾時、範圍重疊警告）；`git diff --check HEAD --` 本票涉及的已追蹤檔案 exit 0；新報告及任務沒有行末空白。逐場 JSON 比對確認只改 2 個口說、3 個 prompt、伏筆一筆改接一筆新增；`claims.md` 只有相應兩個口說格及導言時點改動。

## Notes

R11 `narrative_hash=7673b92858cdf86b`、`speech_hash=9ae33c04c1986d95`。R10 雙盲否票及來源 HOLD 不直接判定 R11；需重新做獨立來源／畫面、乾淨雙盲、正式 OR、政策與音訊關卡。`s56107` 的代詞精度是 R10 來源報告的非阻斷建議，本輪依窄幅任務沒有改它。作者沒有執行付費 TTS、獨立 PASS、乾淨盲評、政策分類或媒體製作。
