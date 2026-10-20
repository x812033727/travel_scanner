---
id: 2026-10-20-curio-s49-1835-moon-hoax-source
title: Curio S49 1835 Moon Hoax source-audited preproduction
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T15:07:01Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s49
---

# Curio S49 1835 Moon Hoax source-audited preproduction

## Why

站主要求持續做不重複的歷史長片，並採編輯推薦方向。原擬 1904 聖路易奧運馬拉松所需官方報告在此環境遭 egress `CONNECT 403`，不從記憶寫實；故選題庫 U30 的 1835 年《紐約太陽報》「月球大騙局」，S01–S48 沒有此題。以 1859 年 Locke 名下重印本及 Harold Jacoby 1902 天文評論寫一張報紙如何層層造出月面居民；把 1859 出版者宣傳與同時代新聞選錄分清。

## Definition of done

- [x] A／B 企劃推薦 A、固定來源 URL/SHA 與精確段落，標出重印本／後出分析界線。
- [x] 30–60 秒濃縮、原版 5 秒片頭位置、正文保守至少八分鐘的繁中逐句稿及 `video.json` 對應。
- [x] 逐句來源與書面畫面提示、lint 0 error／0 warning、作者自檢與未完成關卡交接。
- [x] R1 獨立覆核 HOLD 的來源錨點、旁白及書面畫面 R2 差分修復；作者收據記精確 SHA。

## Steps

- [x] 查 S01–S48 與題庫；確認不重複並留原馬拉松來源跟進票。
- [x] 固定下載 Locke 1859／Jacoby 1902 全文、記 SHA 與來源限制。
- [x] 生成 133 景、136 句／12 個 loops，重生 `script.md`，檢查同文與時間。
- [x] 執行 lint 與 task 檢查、記六份交付的精確 SHA 後釋出本票。
- [x] R2 對照 R1 逐項修復，重生劇本並重核 136 句逐字一致、保守正文八分鐘及畫面比例。
- [x] 另一位覆核者按 R2 精確雜湊重讀固定來源、逐句錨點與書面畫面，留下獨立結論。

## How to verify

在 repo 根目錄跑 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s49 --json`、`npm run check:tasks`；R2 作者收據見 [`docs/videos/curio-s49/verify-2.md`](../../docs/videos/curio-s49/verify-2.md)，獨立來源與書面畫面結論見 [`docs/videos/curio-s49/review/r2-source-independent.md`](../../docs/videos/curio-s49/review/r2-source-independent.md)。前製 lint 與獨立文字查核都不等於 TTS 或媒體實測。

## Notes

截至 2026-10-20，R1 獨立來源／書面畫面覆核曾為 **HOLD**；R2 精確版本已由另一人重核為**固定來源事實 PASS、書面畫面 PASS**。仍無兩位盲讀、網站 A／劇本關卡、TTS、圖像、配樂與成片。1859 重印本含出版社序與對 1835 報紙反應選錄；Jacoby 的報紙引句又取自該重印本，不構成對 1835 原紙的第二份獨立見證。六萬冊與發行量五倍只歸屬 1859 出版者。帶月面生物與巨鏡的畫面都是報導內容的卡通示意。R2 保守文字估正文 2,660 單位／325 單位每分約 8:11，須等實際音訊覆核；品牌片頭及 Studio 片尾框只有計畫。

2026-10-20 獨立來源與書面畫面覆核已落在 [`docs/videos/curio-s49/review/r1-source-independent.md`](../../docs/videos/curio-s49/review/r1-source-independent.md)，結論 **HOLD**：`moon083` 將原文「不像鳥」說反；`moon066` 與 `moon079` 書面提示分別指定無角動物、單隻翼人，與原文及當句旁白衝突；`moon123` 發行量數字連到錯的 `P13`，應改 `P02`。其餘需補的逐句錨點與用語見覆核；修正後重核，尚未生成或驗收圖片。

R2 作者修復對照 R1 全部發現，詳見 [`docs/videos/curio-s49/verify-2.md`](../../docs/videos/curio-s49/verify-2.md) 的差分、靜態檢查與 SHA。獨立重核收據是 [`docs/videos/curio-s49/review/r2-source-independent.md`](../../docs/videos/curio-s49/review/r2-source-independent.md)；**文字與書面分鏡 PASS 只對該文所列五個交付檔雜湊有效**，本站與媒體關卡均未放行。
