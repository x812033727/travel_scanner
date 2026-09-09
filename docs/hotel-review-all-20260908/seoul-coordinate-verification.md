# 首爾五館行政許可座標獨立覆核

查核時間：2026-09-08 15:41:56 UTC。僅研究，沒有正式資料寫入。

五館皆從重新取得的首爾市原始 CSV 重現現有座標，與 `checks-before.json` **小數七位完全一致**。每個許可碼在原檔唯一，營業狀態均為 `01 / 영업/정상`。本覆核不等於完成飯店與平台全部核准；精確 Naver 身分由主代理另行核對。

## 官方來源與授權

[首爾市住宿業許可資料 OA-16044](https://data.seoul.go.kr/dataList/OA-16044/S/1/datasetView.do) 現場讀取確認：資料提供者／著作權人為首爾市，提供部門為 시민건강국 보건의료정책과，無第三方權利人；更新日 2026-09-08，明列 **EPSG:5174**，不直接提供經緯度。網站說明資料有約三日延遲，不能將許可狀態宣稱為即時營運保證。

資料集明列 [KOGL Type 1](https://www.kogl.or.kr/info/licenseType1.do)，允許標示出處後商用及衍生修改。需保留來源、年份、提供者、可用時的來源連結，且不得暗示政府背書。五館現有 `source_credits` 已包含來源／授權連結、2026 年份、許可碼、投影轉換及不代表推薦說明；應維持公開顯示。

## 逐館核對

| 飯店 | 原始許可码 | 官方許可門牌 | WGS84 緯度、經度 | 結果 |
| --- | --- | --- | --- | --- |
| InterContinental Grand Seoul Parnas | 3220000-201-1988-00099 | 서울특별시 강남구 테헤란로 521 (삼성동) | 37.5090478, 127.0608928 | 唯一有效許可、完全一致 |
| L7 GANGNAM by LOTTE HOTELS | 3220000-201-2017-00005 | 서울특별시 강남구 테헤란로 415, 1층,9층~27층 (삼성동, L7 HOTELS 강남타워) | 37.5057019, 127.0515507 | 唯一有效許可、完全一致 |
| Park Hyatt Seoul | 3220000-201-2005-00001 | 서울특별시 강남구 테헤란로 606 (대치동,지상3층~21.23층) | 37.5085668, 127.0641469 | 唯一有效許可、完全一致 |
| Solaria Nishitetsu Hotel Seoul Myeongdong | 3010000-201-2015-00030 | 서울특별시 중구 명동8길 27, 7층~22층 (명동2가) | 37.5624998, 126.9851617 | 唯一有效許可、完全一致 |
| The Westin Josun Seoul | 3010000-201-1970-00188 | 서울특별시 중구 소공로 106 (소공동) | 37.5644382, 126.9800992 | 唯一有效許可、完全一致 |

各館官方身分佐證：

- [InterContinental Grand Seoul Parnas](https://www.ihg.com/intercontinental/hotels/us/en/seoul/seoha/hoteldetail)：521 Teheran-ro, Gangnam-gu, Seoul。live_official_name_and_address_match。
- [L7 GANGNAM by LOTTE HOTELS](https://www.lottehotel.com/prerendered/gangnam-l7/en/about/information/index.html)：415 Teheran-ro, Gangnam-gu, Seoul。official_search_index_name_address_match_live_url_bot_interstitial。
- [Park Hyatt Seoul](https://www.hyatt.com/park-hyatt/en-US/selph-park-hyatt-seoul/hotel-info)：606 Teheran-ro, Gangnam-gu, Seoul。live_official_name_and_address_match。
- [Solaria Nishitetsu Hotel Seoul Myeongdong](https://solaria-seoul.nnr-h.com/news/I7Ey-8Bs)：27 Myeongdong 8-gil, Jung-gu, Seoul。official_search_index_name_address_match_room_page_empty_live；Official July 10 notice concerns Busan's future closure on 2026-12-29 and explicitly says Seoul Myeongdong continues operating. Do not misapply the Busan closure to this permit.。
- [The Westin Josun Seoul](https://www.marriott.com/en-us/hotels/selwi-the-westin-josun-seoul/overview/)：106 Sogong-ro, Jung-gu, Seoul。live_official_name_operator_and_address_match；Municipal permit is under the corporate name Josun Hotels & Resorts; Marriott's hotel footer independently identifies The Westin Josun Seoul, JOSUN HOTELS & RESORTS, and the same 106 Sogong-ro premises.。

L7 官網本次直接讀取遇機器人頁，Solaria 房型頁直接讀取空白；其官方搜尋索引可核對門牌。這些限制已與 municipal CSV 的成功重現分別記錄，沒有偽稱內建瀏覽器驗證。Westin 許可名稱為營運公司，官方 Marriott 頁尾同時標示品牌、JOSUN HOTELS & RESORTS 與相同 106 Sogong-ro 門牌。Solaria 官網的釜山未來閉館公告不能誤套用首爾明洞館。

## 可重現方法與精度限制

使用資料集公開 Sheet CSV POST 表單（無登入、無 API key）：[官方 CSV 下載端點](https://datafile.seoul.go.kr/bigfile/iot/sheet/csv/download.do)，參數為 `infId=OA-16044`、`srvType=S`、`serviceKind=1`、`pageNo=1`、`ssUserId=SAMPLE_VIEW`、空的 `strWhere` 與 `strOrderby`。讀取 CP949，僅保留選定公開許可欄位；原檔 SHA-256：`8fd4660e70d3d50c2008b32ef4eddf4a5290cf8cdfe43201a00f6de5a1248cce`。完整 CSV 未落地保存。

```powershell
uv run --no-project --with httpx --with pyproj==3.7.2 python docs/hotel-platforms/inspect_seoul_source.py
```

另以獨立選取五個許可碼的程序重新下載核对，使用 pyproj 3.7.2 / PROJ 9.5.1、`Transformer.from_crs("EPSG:5174", "EPSG:4326", always_xy=True)`，輸入原始 X、Y，輸出經度、緯度並取七位。投影操作為 Korea Modified Central Belt 的反投影及 Korean 1985 to WGS 84 (1)。PROJ 報告轉換精度 1 公尺，**不代表原始許可點位的測量精度**，也不代表飯店入口；禁止把七位小數解讀為公分級現勘資料。

[JSON 逐筆紀錄](seoul-coordinate-verification.json) 保存原始 X/Y、許可名稱／門牌／狀態、個別資料更新時間、WGS84 結果、來源授權與比較結論。未使用 OTA、Naver 或 Google 座標。
