---
id: 2026-09-17-commons-non-ascii-filename-ingest
title: 非 ASCII 檔名的 Commons 圖片 ingest 不進來：UnicodeEncodeError
status: blocked
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-17T00:56:16Z
completed_at:
branch: codex/guide-diagram-dimensions
depends_on: []
scope:
  - tasks/open/2026-09-17-commons-non-ascii-filename-ingest.md
---

# 非 ASCII 檔名的 Commons 圖片 ingest 不進來：UnicodeEncodeError

## 2026-09-22 remaining validation handoff

The implementation and regression tests merged in PR #561 on 2026-09-19,
commit `f521b9023e5d0ea154b74ebc6f84c2bcf2f47913`. A normal stale-claim
takeover (without force) was used to preserve this task as the unfinished
validation record and release its obsolete implementation scopes.

Still unverified: a real Commons `pack_cli ingest --dry-run` and the original
preferred Sendai/Zuihoden photograph, whose exact filename was not recorded.
The historical 429 observations below are not a claim of a current outage.
The original photo identification and live validation evidence remain the
handoff blocker; this task is not marked complete. Its current scope is its
own record because the remaining work is validation and disposition. A new
implementation defect, if found, must receive a separately claimed code scope.

## Why

`pack_ingest` 透過 Commons API 抓圖時，檔名含非 ASCII 字元（日文、韓文、泰文、越南文）的圖片會丟
`UnicodeEncodeError`，整個 ingest 失敗。第六批有一位撰稿者回報過，當時的查核者重現不出來所以沒追；
第七批寫仙台松島篇時再次撞到，而且這次知道是怎麼回事：**Commons 的回應標頭帶非 ASCII 內容**，
httpx 或底層的 urllib 在處理時炸掉。

實際代價是選圖被限縮：那位撰稿者說構圖最好的瑞鳳殿照片檔名含日文，只能改用純 ASCII 檔名的同主題照片。
日本、韓國、泰國、越南的景點在 Commons 上很多是當地文字檔名，這個限制會一直咬。

## Definition of done

- [x] 用一個檔名含日文的 Commons 圖片重現（例如 `File:瑞鳳殿…jpg` 這類），寫成一個會紅的測試。
- [x] 修掉：抓圖與讀 metadata 的路徑都要能處理非 ASCII 的檔名與回應標頭。
- [x] 測試轉綠，`uv run pytest tests/test_guides_content_pack.py -q` 全綠。
- [x] 在 `docs/travel-guides.md` 的內容包那一節拿掉（或修正）任何「檔名用 ASCII」的暗示，如果有的話。
      （查過：沒有這種暗示，不用改。）

## Steps

- [x] 先重現：`app/guides/pack_ingest.py` 的 `commons_file_info` 與 `fetch_image` 兩條路徑都試。
- [x] 看是 httpx 的 header 解碼、還是 URL 編碼沒做。工具本來就有一個 `UrllibTransport`（票
      `2026-09-13-life-ai-series-tooling` 提到 httpx 的連線被 Wikimedia 擋 403 才改走 urllib），
      問題可能在那一層。
- [ ] 修完用第七批仙台松島篇原本想用的那張瑞鳳殿照片實測一次。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_pack_ingest.py tests/test_guides_content_pack.py -q
```

會紅／轉綠的那兩個測試在 `tests/test_guides_pack_ingest.py`（`-k "japanese or non_ascii_location"`）。

再用一個非 ASCII 檔名的 Commons 圖跑一次 `pack_cli ingest --dry-run`，要能通過。

## Notes

- 第七批因此換過照片的是 `sendai-matsushima-2-day-itinerary`；修好之後可以回頭換成構圖較好的那張。
- 這不影響已上線的文章，只影響之後的撰稿。

### 2026-09-19 修法（claude-fable-5-1）

- **根因不在 URL 編碼，在回應標頭。** httpx 在 URL 進到 urllib 之前就把路徑與查詢字串照
  UTF-8 百分比編碼（本機測試伺服器看到的是 `GET /%E7%91%9E%E9%B3%B3%E6%AE%BF.jpg` 與
  `titles=File%3A%E7%91%9E…`），所以 `commons_file_info` 的 API 查詢與 `fetch_image` 的下載
  請求本來就送得出去。炸的是 `UrllibTransport.handle_request` 收回應那一步：`http.client` 把
  每個回應標頭當 ISO-8859-1 解成 `str`，程式再把 `dict(answer.headers.items())` 交給
  `httpx.Response`，而 httpx 把 `str` 標頭值以 ASCII 重新編碼
  （`httpx/_models.py:82 _normalize_header_value`）——只要任一標頭有位元組 ≥ 0x80 就是
  `UnicodeEncodeError: 'ascii' codec can't encode characters`。3xx 分支（`error.headers`）同樣寫法，
  所以帶非 ASCII 的 `Location` 也會炸。
- **修法**：新增 `_header_bytes(message)`，把 urllib 給的標頭以 latin-1 反向編回原始位元組（無損），
  用 `(bytes, bytes)` 配對交給 httpx，由 httpx 自己挑編碼（ASCII → UTF-8 → ISO-8859-1）；
  `response.headers[...]` 讀回的就是 UTF-8 原文，帶這種位元組的 `Location` 也跟得下去，重複的標頭
  （`Vary`、`Set-Cookie`）不再被 dict 吃掉。ASCII URL、轉址交還 httpx、scheme 檢查、403 迴避的
  User-Agent 全都沒動；`_known_topics` 沒碰。
- **測試**放在 `apps/api/tests/test_guides_pack_ingest.py`（Commons transport 的既有測試與本機
  `HTTPServer` 夾具都在這裡，票原本列的 `test_guides_content_pack.py` 沒有；scope 因此加了這個檔）：
  - `test_a_japanese_file_name_survives_the_metadata_call_and_the_download`：本機伺服器仿 Commons 回
    `File:瑞鳳殿.jpg` 的 imageinfo（百分比編碼的 `url`／`thumburl`／`descriptionurl`、utm 查詢字串、
    `1920px-` 檔名，照下面實測到的形狀），圖片回應帶 raw UTF-8 的
    `Content-Disposition: inline;filename="瑞鳳殿.jpg"`；走 `commons_client()`（真的 `UrllibTransport`）
    跑 `commons_file_info` + `fetch_image`。修前紅（上述 UnicodeEncodeError），修後綠。
  - `test_a_redirect_to_a_non_ascii_location_is_followed`：`Location` 帶 raw UTF-8 的 302，修前同樣炸，
    修後跟到 `/%E7%91%9E%E9%B3%B3%E6%AE%BF.jpg`。
- **實際 Commons 回什麼**（2026-09-19，UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，
  限額 4 次請求，全部用完；cookie 與 client-IP 值沒記）：
  1. `api.php` 第一次 → **429**（`x-envoy-ratelimited: true`、`retry-after: 7`；共用出口 IP 被限流）。
  2. 等 75 秒後 `action=query&generator=search&gsrsearch=intitle:瑞鳳殿&gsrnamespace=6&prop=imageinfo&iiprop=url|size|mime|extmetadata&iiurlwidth=1600&format=json`
     → 200，走修後的 transport。回應標頭全 ASCII（`content-type: application/json; charset=utf-8`、
     `content-disposition: inline; filename=api-result.json`、`vary: Accept-Encoding,X-Subdomain,…,User-Agent`）。
     現在的 URL 形狀：`url` 在 `https://upload.wikimedia.org/wikipedia/commons/7/72/%E7%91%9E%E9%B3%B3%E6%AE%BF_2009_%283684054474%29.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original`；
     `thumburl` 已改在 **`thumb.wikimedia.org`**（`/wikipedia/commons/thumb/7/72/<encoded>/1920px-<encoded>?utm_source=…&utm_content=thumbnail`）：
     要 1600 給的是 1920px，API 卻仍回報 `thumbwidth` 1600（`CommonsInfo.width/height` 對不上實際位元組，
     但 staging 用的是 `fit_bytes` 的實際尺寸，無影響）；`descriptionurl` 是
     `https://commons.wikimedia.org/wiki/File:%E7%91%9E%E9%B3%B3%E6%AE%BF_2009_(3684054474).jpg`。
     可用的日文檔名：`File:Zuihouden(瑞鳳殿) - panoramio.jpg`（CC BY 3.0）、
     `File:瑞鳳殿 2009 (3684054474).jpg`（CC BY 2.0）、
     `File:瑞鳳殿 (Zuiho-den in midwinter) 14 Jan, 2013 - panoramio.jpg`（CC BY-SA 3.0）。
  3. GET 第一個的 `thumburl` → 200：`content-type: image/jpeg`、
     `content-disposition: inline;filename*=UTF-8''Zuihouden%28%E7%91%9E%E9%B3%B3%E6%AE%BF%29_-_panoramio.jpg`
     （RFC 5987，純 ASCII）、`etag`、`last-modified`、`content-length: 1161961`、`server: envoy`、
     `x-ratelimit-limit: 600000, 600000;w=60`、`access-control-expose-headers`、`x-cache`、`server-timing`、
     `report-to`、`nel`、`content-security-policy-report-only`……**沒有任何非 ASCII 位元組**，也沒有轉址；
     修後的 transport 讀回 JPEG 1920×1440。
  4. HEAD `upload.wikimedia.org` 原檔 → **429**（`server: Varnish`、`x-cache-status: int-front`、`retry-after: 600`）。
- **沒重現到的**：撰稿者當天是哪個標頭帶了非 ASCII，今天看不到（thumb 的回應全 ASCII）；候選是
  轉址 `Location`、舊的 upload.wikimedia.org 縮圖堆疊、或 `Set-Cookie: GeoIP=…` 帶城市名。修法不挑
  標頭，任何 ≥ 0x80 的位元組都不再炸，所以不必知道是哪一個。
- **沒做到**：用真 Commons 圖跑 `pack_cli ingest --dry-run`（限額與 429），以及第七批那張特定瑞鳳殿
  照片（票沒寫檔名）；`sendai-matsushima-2-day-itinerary` 換圖仍待下一位——上面第 2 點列了三張可選。
- 驗證：`cd apps/api && uv run pytest tests/test_guides_pack_ingest.py tests/test_guides_content_pack.py -q`
  全綠；`uv run ruff check app/guides/pack_ingest.py tests/` 與 `uv run mypy app` 通過。
