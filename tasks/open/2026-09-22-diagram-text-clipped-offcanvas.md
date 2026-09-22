---
id: 2026-09-22-diagram-text-clipped-offcanvas
title: 四張路線圖的文字被畫到畫布外，任何螢幕都看不到
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-22T02:20:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/public/guides/narita-haneda-to-tokyo
  - apps/web/public/guides/incheon-airport-to-seoul
  - apps/web/public/guides/kansai-airport-to-osaka-kyoto
  - apps/web/public/guides/tokyo-5-day-itinerary
  - apps/api/app/guides/pack_ingest.py
---

# 四張路線圖的文字被畫到畫布外，任何螢幕都看不到

## Why

圖的畫布是 `viewBox="0 0 1600 900"`，超出這個範圍的內容**會被裁掉**。
2026-09-22 用瀏覽器實測（`getBBox()`）發現四張路線圖有文字的右緣超過 1600：

| slug | 超出的文字數 | 最遠右緣 | 例子 |
|---|---|---|---|
| `narita-haneda-to-tokyo` | 3 | 1696 | 「N'EX 最快 53 分 · TYO-NRT 巴士 最快 65 分」 |
| `incheon-airport-to-seoul` | 3 | 1718 | 「機場巴士 6001／6015 · 深夜 N6701 到首爾站約 60 分」 |
| `kansai-airport-to-osaka-kyoto` | 3 | 1703 | 「関空快速 約 70 分 · はるか 約 45 分 · 巴士 約 60 分」 |
| `tokyo-5-day-itinerary` | 1 | 1705 | 「成田 Narita · N'EX、TYO-NRT 巴士 →」 |

**這和手機的捲動無關。** 捲動只是決定一次看得到多少，
這些字是被 `viewBox` 裁掉的，**桌機 1280px 以上整張圖完整顯示時一樣看不到**。
被切掉的還都是班次、時間與票價這類讀者真正要的資訊。

四張都是同一個版型：右側的目的地標籤起點在 x=1285 到 1460 之間，
後面接一串長的中日文說明，於是撞出畫布。

## Definition of done

- [ ] 這四張圖沒有任何文字的 `getBBox()` 右緣超過 1600（或左緣小於 0）。
- [ ] 被救回來的字仍然讀得懂，沒有為了塞進去而砍掉班次或票價。
- [ ] `check_svg` 仍然過，字級沒有降到 15 以下。

## Steps

- [ ] 逐張決定救法：把右側那一組標籤整體左移、縮短文字、或改成兩行。
      **不要單純縮小字級**，15px 是下限，降下去在手機上又讀不到了。
- [ ] 改完用瀏覽器重量一次（見下方指令），不要只靠算的。
- [ ] 圖改了就重跑 `tools/lift-diagram-descriptions.py --slug <slug>`
      讓內容包的 `description` 跟上，並把內容包從 CRLF 轉回 LF。
- [ ] 考慮把這個檢查加進 `pack_ingest.check_svg`。它現在檢查 viewBox、字級、
      禁用元素與外部參照，**但不檢查文字有沒有超出畫布**，所以這類缺陷一直沒被擋下來。

## How to verify

在瀏覽器開圖檔本身，跑這段：

```js
const s=document.querySelector('svg'); const o=[];
for (const t of s.querySelectorAll('text')) {
  const b=t.getBBox();
  if (b.x+b.width > 1600.5 || b.x < -0.5) o.push(Math.round(b.x+b.width)+' '+t.textContent.trim());
}
JSON.stringify({over:o.length, items:o});
```

`over` 要是 0。

## Notes

- **純算的會出錯，兩個方向都會。** 我先用 Python 依字元寬度估算掃完 1,546 個 SVG，
  標出 7 張；瀏覽器實測後**只有 4 張是真的**，
  `everland-lotte-world-guide/diagram-1-en.svg`、`fukuoka-airport-to-hakata-tenjin`、
  `singapore-entry-2026-sg-arrival-card` 三張是誤判（模型高估拉丁字母的寬度）。
  反過來也可能有漏網的，**所以要全站確定，得用瀏覽器量過 1,546 個檔**，不能只信估算。
- 同一次全站掃描也確認了：**1,546 個 SVG 的 viewBox 全部是 `0 0 1600 900`**，
  1,845 個圖塊的尺寸全部是 1600x900，沒有比例特例。
- 另有 **10 個檔案字級低於 15**（13 或 14px），在 1180px 寬時是 9.6 到 10.3px。
  那是另一張票 `2026-09-21-91-ci` 的 `svg_small_label` 範圍，不在這裡處理。
- 標題與頁尾那種橫跨整張畫布的長句在手機上要滑兩次才讀完，**那不是缺陷**，
  是 1600px 畫布的必然結果；這張票只處理真的被裁掉的字。
