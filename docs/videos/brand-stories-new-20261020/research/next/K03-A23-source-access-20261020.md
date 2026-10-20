# 下一批 K03／A23 來源連線紀錄（未完成查核）

2026-10-20 在目前雲端執行環境測試。已套用的 restricted HTTP 網路政策只有預設開發網域，未包含下列新聞、品牌或法院網域。這份紀錄是查核障礙與待辦，**不是**對舊題庫敘述的新查核收據；不能據此編譯或匯入第 6–10 集。

| 候選 | 原題庫來源 | 本次結果 | 恢復連線後首先要核對 |
| --- | --- | --- | --- |
| K03 賓格瑞香蕉牛奶 | [賓格瑞 2024 年官方故事](https://www.bing.co.kr/news/news_story_view?sto_idx=23) | `curl: (56) CONNECT tunnel failed, response 403` | 1974 年上市、瓶型、市占率與外銷包裝等官方自述；數字保留出處與年份。 |
| K03 | [賓格瑞官方沿革](https://www.bing.co.kr/company/history) | 同一網域受限，未重新開頁 | 公司更名時間、工廠與產品推出順序。 |
| K03 | [The Korea Herald 2024 年報導](https://www.koreaherald.com/article/3850843) | `curl: (56) CONNECT tunnel failed, response 403` | 「申請文化遺產」究竟只是籌備、正式提出，還是獲登錄；不要把 2024 年籌備寫成 2026 年已完成。 |
| A23 Huy Fong 是拉差 | [California Courts 上訴判決 B303096](https://www4.courts.ca.gov/opinions/archive/B303096.PDF) | `curl: (56) CONNECT tunnel failed, response 403` | Underwood Ranches 供椒關係、訴訟時序與判決結果；以法院文件定稿。 |
| A23 | [Fortune 2024 年報導](https://fortune.com/2024/01/30/sriracha-shortage-huy-fong-foods-tabasco-underwood-ranches/) | 網域未在已套用網路政策，未重新開頁 | 供應中斷、市占與家戶數據的年份及資料來源；不能泛稱為今日現況。 |

以上網址與待查問題來自本機舊題庫 `docs/videos/story-plans/brand-stories-100/stories/K03.json`、`A23.json`，不表示本輪已打開網頁。K03「香蕉是奢侈品」原題庫自述佐證偏弱，A23「不打廣告」和「沒註冊 Sriracha 字樣」也須按原始資料限定語意；若新查核仍不充分，改選另一題。環境網路設定草稿須正式發布並套用後，再開來源、記逐條證據、重寫六章企劃並交獨立查核。
