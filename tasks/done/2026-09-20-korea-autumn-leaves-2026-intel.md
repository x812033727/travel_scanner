---
id: 2026-09-20-korea-autumn-leaves-2026-intel
title: 韓國賞楓 2026 時效情報：10 月上旬山林廳預測地圖發布後再寫（第八批規劃時官方來源還沒開張）
status: done
priority: P2
area: docs
owner: claude-opus-5-5-korea-autumn-leaves
claimed_at: 2026-10-05T07:35:44Z
created_at: 2026-09-20T00:24:20Z
completed_at: 2026-10-05T08:51:46Z
branch: claude/korea-autumn-leaves
depends_on: []
scope:
  - apps/api/app/guides/content/korea-autumn-leaves-2026.json
  - apps/web/public/guides/korea-autumn-leaves-2026
  - apps/api/app/guides/content/nami-island-petite-france-day-trip.json
  - apps/api/app/guides/content/seoul-4-day-itinerary.json
  - apps/api/app/guides/content/korea-ktx-srt-ticket-guide.json
---

# 韓國賞楓 2026 時效情報：10 月上旬山林廳預測地圖發布後再寫

## Why

站上有 `japan-autumn-leaves-2026`、`korea-winter-events-2026`、`korea-ski-resorts-2026-2027`，就是沒有韓國的秋天。
第八批規劃（2026-09-20）時兩個官方來源都還沒開張：山林廳「산림단풍 예측지도」尚未發布（forest.go.kr 首頁是 1.6 KB 的殼，
보도자료 列表讀得到但還沒有今年那一則），氣象廳的單楓現況頁也還沒有 2026 年資料，所以這題被 drop，不是題目不好。

## Definition of done

- [x] 10 月上旬重讀山林廳보도자료（`https://www.forest.go.kr/kfsweb/cop/bbs/selectBoardList.do?bbsId=BBSMSTR_1036&mn=NKFS_04_02_01`）與氣象廳單楓頁；
      讀得到各山的預測高峰日才寫，讀不到就再延後並記下試過的網址。
- [x] intel、zh-TW、800–1,500 字、`valid_until` 約 2026-11-30；互連 `seoul-4-day-itinerary`、`nami-island-petite-france-day-trip`、`korea-ktx-srt-ticket-guide`。
- [ ] 過期處理：`valid_until` 隔天拿掉其他文章連過來的連結（照第七批 README 的時效規則）。→ 日期未到，拆成 `2026-10-05-korea-autumn-leaves-links-expire-2026`。

## Steps

- [x] 重讀官方來源（2026-10-05）
- [x] 規格（寫在工作區，沒有批次 docs 目錄：單篇）
- [x] 撰稿
- [x] 查核（另開一輪，逐一重抓來源比對，見 Notes）
- [x] 出圖與照片
- [x] PR
- [ ] 匯入：publish after merge (coordinator, owner consent)

## How to verify

`pack_cli lint --kind intel --slug korea-autumn-leaves-2026`；正式站頁面 200、可索引。

## Notes

- 對外請求 UA 一律 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，不得帶任何人的 email 或個人資料。
- **官方來源 2026-10-05 的狀態。** 山林廳 2026-09-22 就發了「2026년 한반도 단풍절정 예측지도」（보도자료 nttId=3224451，
  附件是楓樹類、橡樹類、銀杏三張地圖與 PDF），比票預期的「10 月上旬」早；列表要用 `searchWrd=단풍` 搜才找得到。
  本文只有四座山（설악산 10/20、속리산 10/28、내장산 11/4、한라산 11/6）與全國樹種別日期（楓樹類、橡樹類 10/31、銀杏 10/30），
  其餘三十幾個點只在附件地圖（`getImage.do?atchFileId=CTGRY_00000000412261&fileSn=1`／`3`，1463×2070 與 1628×2303 的 JPG），
  要切格放大讀；PDF 是兩頁，pdftotext 抽不出韓文（字型編碼），用看圖讀。
  同系列還有 09-17（點鳳山 9/14 第一片楓紅）與 09-29（國立樹木園的地址查詢服務，50% 的高峰定義）兩則。
- **氣象廳。** `weather.go.kr/w/forecast/life/seasonal-observation/autumn-leaves.do` 的內容是 JS 載入的：資料在
  `https://www.kma.go.kr/kma/theme/maple_photojs.jsp?treeType=4&obsPlace=<山名>`（JSONP，21 座名山的 단풍전／첫단풍／절정 與照片日期）。
  10-05 只有설악산（9/28）與오대산（10/1）是첫단풍。頁上沒寫判定比例，所以正文不寫氣象廳的百分比。
- **讀不到的：** 國立樹木園的「한반도 단풍절정 검색서비스」`knpn.nature.go.kr` https 與 http 都連線逾時（可能擋海外），正文沒有叫讀者去用。
- **查核。** 這個 session 沒有開子代理的工具，查核由同一個代理在草稿寫完後另開一輪：30 條主張逐條重抓來源（全部 200）、兩張地圖逐格重讀。
  改了 4 處：「雪嶽山最先／最早」（화악산、소백산 同為 10/20，금원산 的銀杏 10/16 更早）改成「從雪嶽山開始」；「全國平均」改成「以全國來看」
  （原文是全國的樹種別預測，沒說是平均）；photo-1 圖說「比首爾近郊晚一週」改成「比春川晚一週」（首爾植物園只差 2 天）；
  callout 裡沒有來源的「還在楓前就往後挪」改成中性的建議。PR 的 review 階段是第二雙眼睛。
- **intake_check 擋掉的：** `destination_id` 是 null 的文章不能有 offer（第八批 README 第 2 條與 intake_check）；
  `japan-autumn-leaves-2026` 有兩個 offer 是較早的批次，這篇不放。
- **互連的做法。** 這篇用 article inline 連三篇 howto；三篇各加一行只有 article inline 的 `rich_paragraph` 連回來
  （南怡島在冬季活動那行之後、首爾四天三夜在 Day 3 方案 A 之後、KTX 在延伸閱讀最後）。
  只有連結的段落不算字數，目標沒發布或過期時網站畫成純文字（`content-blocks.tsx`），所以先匯入哪一篇都不會壞連結。
  scope 因此加了這三個檔。2026-12-01 起要刪掉它們，拆成 `2026-10-05-korea-autumn-leaves-links-expire-2026`。
- **hero** 是 Commons `File:Seoraksan in the Fall 1- 설악산 단풍.jpg`（CC BY-SA 3.0），ingest 在品質下限壓到 246,850 bytes，
  依第七批 ERRATA 在 ingest 之後重壓到 200 KB 以下；photo-1 是 `File:Naejangsan Pavilion 2.jpg`（CC BY-SA 3.0）。
- **匯入（publish after merge, coordinator, owner consent）：** 四個 slug 一起：`korea-autumn-leaves-2026`（create）與
  `nami-island-petite-france-day-trip`、`seoul-4-day-itinerary`、`korea-ktx-srt-ticket-guide`（update，各多一行連結）。
  之後跑 `guides-links-rebuild`、`guides-links-check --locale zh-TW`，確認頁面 200、可索引。
