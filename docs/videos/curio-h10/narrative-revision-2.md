# H10 敘事修訂 2：搜尋位置的因果與回收

- 舊稿 `video.json` SHA-256：`58e37c2eb2bc8190ba16aa4b9dc5050397819a12e263b29cf3a0641dba7c306b`。
- 新稿 `video.json` SHA-256：`236e94b49168e52e57f6c063c9cd377fdf2086cc91fb0907932a3d13fc3389ac`。
- `brief.md` SHA-256：`ab081206f4055046c18b7a89016f05c9f885aa6bdd37ea3c2e2c661f2d74aa0d`，未修改核准的大綱。
- [第二輪嚴格盲評原文](narrative-round2.json)：12 項必答過 11 項，章名建議題通過；唯一未過 `payoffs`。本次是第二個、最後一個作者修訂回合，新版須交新讀者盲評，不以本筆作者記錄充當通過。

## 只改兩句旁白

| 句 ID | 原句 | 現句 | 理由 |
| --- | --- | --- | --- |
| `h3369d03` | 一句沉船的描述，怎麼變成下一次海底搜尋的位置？ | 因紐特見聞先畫出搜尋範圍。後來是哪條現場線索，讓水下搜尋改了位置？ | 舊問題要求口述直接產生下一個海底座標，後文沒有此因果。新問題要求找出使 2014 年水下搜尋改位的現場線索；`h3630626` 說明金屬件的船圖比對，`h725fbb3` 補出木製塞件與實際改位，具體回收。 |
| `hc2e7f24` | 於是搜索不只往水下看，岸上有沒有遠征留下的物件，也成了重要問題。 | 搜索隊不只往水下看，也留意岸上有沒有遠征留下的物件。 | 移除「於是」暗示口述必然導致此岸上調查的因果。 |

史料界線：[Parks Canada 因紐特知識](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/inuit/qaujimajatuqangit)說傳統知識界定搜尋區，陸上與水下考古方法協助搜尋；[Parks Canada 幽冥號發現經過](https://parks.canada.ca/lhn-nhs/nu/epaveswrecks/culture/archeologie-archeology/decouvertes-discoveries/erebus)記錄 2014 年 9 月 1 日岸上發現吊艇裝置金屬件及木製塞件，Ryan Harris 隔天據此調整搜尋區後以聲納發現沉船。新稿沒有把 1869 年的標圖說成現代精確座標，也沒有把兩條線索寫成同一個決定。

`video.json` 的 loop 已改指向 `h725fbb3`，`line-claims.json` 跟隨兩句文字；`script.md` 由 `node tools/video/cli.mjs script --slug curio-h10` 從新版 `video.json` 重新產生。`script-timing.json` 只保存重新計算的**估時**，不是音訊實測；`loops.md` 時間隨之更新。`node tools/video/cli.mjs lint --slug curio-h10 --json` 為 0 errors、2 個既有的 historical／modern 插畫提示詞警告，80 句、估時 9.615 分。未送後台劇本、未呼叫付費服務；舊版獨立史料查核 [verify-1.md](verify-1.md) 綁舊 SHA，新版尚待獨立者對變動句重新核對並綁新 SHA。
