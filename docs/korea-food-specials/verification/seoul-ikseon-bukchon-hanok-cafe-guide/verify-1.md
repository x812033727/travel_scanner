# 益善洞／北村咖啡：第一輪獨立審稿

查核日期：2026-09-20。審稿者與撰稿模型不同；重新對官方可見頁、Commons 頁、pack 段落與圖解核對。本輪仍須由另一模型作第二輪查核。

## 修正

- 原稿總表列七店，卻將 `차 마시는 뜰／이채 카페`、`서울커피／레인리포트／하이웨이스트` 合併成兩個「入選依據」段落，intake 只辨識四店，正文 2693 字。已拆為七個獨立段落，各留官方頁與 Naver 連結，補入逐店地址辨認與空間差異。重新 intake：**7 店、3916 字**，無警告。
- Visit Seoul 韓屋專題與 Highwaist 的原 URL 使用不正規路徑，在 web 工具遭防火牆擋下；改成站內可見的 canonical URL：`/editorspicks/SeoulHanokCafes/31659` 與 `/PalaceArea/CafeHighwaistIkseon/ENP038783`，並同步 sources 與逐店段落。
- 官方對 `이채 카페` 強調從窗邊看韓屋村；對 `서울커피 익선점` 僅明說位在韓屋村；`차 마시는 뜰` 是傳統茶坊及庭院描述。依本系列「建物本身是韓屋」的門檻，三家總表與 SVG 去掉「韓屋」標籤，保留可由官方空間文字支持的「網美」。Osulloc 官方明寫 `60년대의 양옥`，維持不標韓屋。
- `images.json` 原來使用 `images` 陣列、但 ingest 需要 `hero.title`，且工作目錄沒有 hero 檔。重新核對 Commons 原圖頁的作者、CC BY-SA 4.0 與 6404×4269 原圖，補正 manifest。實際 hero 已目視：北村韓屋街於藍調時段，alt 相符。

## 官方證據

| 店家 | 官方可見頁與核對項目 |
|---|---|
| 어니언 안국 | [VISITKOREA](https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=191156)：安國分店、1920 年代韓屋、`계동길 5`、平日／週末時間、招牌品項。 |
| 오설록 티하우스 북촌점 | [品牌分店頁](https://www.osulloc.com/kr/ko/store-introduction/312)：北村店、`60년대의 양옥`、`북촌로 45`、分日時間。 |
| 차 마시는 뜰、이채 카페 | [Visit Seoul 韓屋咖啡專題](https://english.visitseoul.net/editorspicks/SeoulHanokCafes/31659)：兩店各自標題與門牌 `북촌로11나길 26`、`북촌로 20-21`，茶桌／庭院與窗邊韓屋村景分別屬於不同店。 |
| 서울커피 익선점 | [Visit Seoul 分店頁](https://english.visitseoul.net/area/Seoul-Coffee-Ikseon-Branch/ENP039310)：益善分店、33-3 Supyo-ro 28-gil、11:00–22:00、最後點餐 21:40。 |
| 레인리포트 레인보우 | [Visit Seoul 分店頁](https://english.visitseoul.net/PalaceArea/rainreport/ENP933ykf)：33-7 Supyo-ro 28-gil、韓屋空間、Cloud Pavlova、10:30–20:30。 |
| 카페 하이웨이스트 익선점 | [Visit Seoul 分店頁](https://english.visitseoul.net/PalaceArea/CafeHighwaistIkseon/ENP038783)：18 Donhwamun-ro 11da-gil、白牆與韓屋建物、司康、09:00–22:00。 |

## 收件結果與待查

- `intake_check.py`：7 店，3916 字；`pack_cli ingest --dry-run` 成功；已 ingest 至隔離 repo。hero JPEG 經匯入器壓縮後 205991 bytes，略高於 200000 byte 指引，低於硬上限；此為現存警告。
- SVG 原始文字已與七店表格重核，並通過 ingest 的 SVG 檢查；尚未做 SVG 像素級渲染目視。營業時間是 2026 年 9 月官方頁快照，出發日仍須重查。
