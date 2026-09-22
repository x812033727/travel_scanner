---
id: 2026-09-22-diagram-text-clipped-offcanvas
title: 四張路線圖的文字被畫到畫布外，任何螢幕都看不到
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-22T00:34:24Z
created_at: 2026-09-22T02:20:00Z
completed_at: 2026-09-22T00:41:21Z
branch:
depends_on: []
scope:
  - apps/web/public/guides/incheon-airport-to-seoul
  - apps/web/public/guides/tokyo-5-day-itinerary
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

## 範圍縮小了（2026-09-22）

原本四張一起做，但認領被擋下來：另外兩張在別人的票的 scope 裡，都還是 `review`。

| 圖 | 誰佔著 | 狀態 |
|---|---|---|
| `incheon-airport-to-seoul` | 無 | **這張票做** |
| `tokyo-5-day-itinerary` | 無 | **這張票做** |
| `narita-haneda-to-tokyo` | `2026-09-20-localize-four-tokyo-first-trip-guides`（codex-batch007-source-pr） | 等它 |
| `kansai-airport-to-osaka-kyoto` | `2026-09-21-five-language-kansai-arrival-usj-batch`（codex-kansai-batch008） | 等它 |

`pack_ingest.py` 也被 `2026-09-17-commons-non-ascii-filename-ingest` 佔著，
所以「把這個檢查加進 `check_svg`」也留到那張票放掉之後再開。
缺陷的細節已經寫進那兩張 Codex 的票裡，給它們的擁有者看。

## Definition of done

- [x] 這張票的**兩張**圖沒有任何文字的 `getBBox()` 右緣超過 1600（或左緣小於 0）。
      實測最大右緣：仁川 1588、東京 1594。
- [x] 被救回來的字仍然讀得懂，班次與票價一字未減。
- [x] `check_svg` 兩張都回空陣列，最小字級：仁川 18、東京 15。

## Steps

- [x] 逐張決定救法，見下方「做法」。沒有動字級往下調。
- [x] 改完用瀏覽器重量過，溢出與重疊都是 0。
- [x] 不需要：我只動 `<text>`，沒有動 `<desc>`，兩個內容包的 `description` 比對後仍與 SVG 一致。
- [ ] 考慮把這個檢查加進 `pack_ingest.check_svg`。它現在檢查 viewBox、字級、
      禁用元素與外部參照，**但不檢查文字有沒有超出畫布**，所以這類缺陷一直沒被擋下來。
      **還不能做**：`pack_ingest.py` 在 `2026-09-17-commons-non-ascii-filename-ingest` 的 scope 裡。

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


## 做法（2026-09-22）

### `incheon-airport-to-seoul`

右側標籤起點在 x=1285，左邊就是 cx=1210／1250 的圓點，**往左移會撞到圓點**，
所以改成在分隔號處拆行，資訊一字不減：

| 原本 | 改成 |
|---|---|
| `直達 T1 43 分／T2 51 分 · 一般列車 約 60 分` | 兩行：`直達 T1 43 分／T2 51 分` ／ `一般列車 約 60 分` |
| `機場巴士 6001／6015 · 深夜 N6701 到首爾站約 60 分` | 兩行：`機場巴士 6001／6015` ／ `深夜 N6701 到首爾站約 60 分` |
| `서울역 首爾站 Seoul Station`（只超出 23） | `서울역 首爾站 Seoul Sta.` |

縮寫是跟著這張圖自己的體例：同一組裡本來就有 `홍대입구 弘大入口 Hongik Univ.`。

### `tokyo-5-day-itinerary`

`成田 Narita · N'EX、TYO-NRT 巴士 →` 改成 **`text-anchor="end"` 加 `x="1580"`**。
這樣右緣不再取決於字串長度，而且剛好貼齊箭頭終點 1560，比猜一個新的 `x` 穩。

順手修掉兩個既有問題：

- **一個重疊**（正式站原始檔就有，不是這次改出來的）：
  `最後採買後前往機場（成田走 N'EX／巴士，羽田走京急／單軌電車）` 撞到「Day 4」的圓角標籤。
  **括號裡的內容和圖上兩個機場箭頭旁的標籤完全重複**，拿掉括號同時解決重疊與重複。
- **兩個 13px 的字級**（屬於票 `2026-09-21-91-ci` 的 `svg_small_label` 那一組）：
  拉到 15px。`東京スカイツリー Skytree` 原本右緣就在 1598，放大會變 1621 撞出畫布，
  所以 `x` 一併從 1445 左移到 1418。那張票的清單可以少這一個檔。

### 量測結果

| 圖 | 文字數 | 溢出 | 重疊 | 最大右緣 | 最小字級 |
|---|---|---|---|---|---|
| `incheon-airport-to-seoul` | 21 | 0 | 0 | 1588 | 18 |
| `tokyo-5-day-itinerary` | 39 | 0 | 0 | 1594 | 15 |


## 2026-09-22 收尾：仁川那張被主線先修掉了

合併主線時 `incheon-airport-to-seoul/diagram-1.svg` 撞到衝突。
**#636「Localize Seoul airport and T-money guides」修的是同一個缺陷，只是做法不同**：
它把文字大幅縮短，而不是拆行。

| 這張票的做法 | #636 的做法 |
|---|---|
| `직達 T1 43 分／T2 51 分` ＋ `一般列車 約 60 分`（兩行） | `T1 43／T2 51 分 · 普通約 60 分`（一行） |
| `機場巴士 6001／6015` ＋ `深夜 N6701 到首爾站約 60 分`（兩行） | `6001/6015 · N6701首爾站60分(T1)`（一行，還多了航廈資訊） |
| `서울역 首爾站 Seoul Sta.` | `서울역 首爾站`（拿掉羅馬拼音） |

**採用主線的版本，撤掉我對這個檔的改動。** 理由：#636 同時產出了
`diagram-1-{en,ja,ko,zh-cn}.svg` 四個語系版本，維持同一套措辭才不會讓
繁中版和它的四個兄弟檔分岔；它也比較新，是那個批次刻意的決定。

五個語系版本都用瀏覽器量過，**全部零溢出、零重疊**：

| 檔 | 溢出 | 重疊 | 最大右緣 |
|---|---|---|---|
| `diagram-1.svg`（zh-TW） | 0 | 0 | 1576 |
| `diagram-1-en.svg` | 0 | 0 | 1585 |
| `diagram-1-ja.svg` | 0 | 0 | 1589 |
| `diagram-1-ko.svg` | 0 | 0 | 1592 |
| `diagram-1-zh-cn.svg` | 0 | 0 | 1594 |

所以這張票實際留下的修正**只有 `tokyo-5-day-itinerary`**。

**一個值得記的教訓**：我認領時 `incheon-airport-to-seoul` 不在任何進行中的票的 scope 裡，
但 #636 顯然涵蓋它。**scope 檢查擋得住已登記的重疊，擋不住還沒登記的平行工作**；
碰到這種共用檔案，合併前再看一次主線動過什麼比較保險。
