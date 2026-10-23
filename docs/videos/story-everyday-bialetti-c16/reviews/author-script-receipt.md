# C16 Bialetti｜作者劇本與逐鏡修訂收據

日期：2026-10-23（台北時間）。作者 `codex-c16-script` 依兩位獨立、只讀旁白的盲讀 HOLD 修訂此稿。**目前新稿沒有獨立來源／配鏡 PASS，也沒有新版兩位盲讀 PASS。**舊稿的 85/85 獨立 PASS 是精確舊雜湊的歷史證據；不可套用於以下新稿。站主劇本核准、整支付費核准、真實配音、媒體生成、匯入、上傳與發布均未完成。

## 已採用企劃綁定

| 檔案／狀態 | SHA-256 |
| --- | --- |
| 已採用 `treatment.md` | `1B82057CE1CA064C84829F64F2D5B4679CC2E9CCA74F14F24964650636282EEE` |
| 已核 `source-matrix.md` | `3705477A06ED4395C44D57882951349B0D8D16DAF8D946DC86CECEC9ADF1D713` |
| 站主採用 Treatment 收據 | `37F28906D4B29CD9DAF133E73BAFB9C321CFC4D3AD0DE1DED5CCC5F27CC07DE0` |
| 分支起點／Treatment PR #1698 head | `e32a2b5f05b38e4fe25ba7db5738e5b2e48aa2f4` |

## 新版四份 Git blob bytes

| 檔案 | SHA-256 |
| --- | --- |
| `script.md` | `398029F77DAEA0AC861C34184D89F42B5233544853B76562E6F1D3FFCE0376A1` |
| `script-source-notes.md` | `EAB56335270C22055F4450BCA95BEEB2223ABE21FA471EAA2DCDE227D89A77C0` |
| `visual-plan.md` | `08C9592BFD9E9079C6101DC280B8CFD304C0AFA1EC91F5A067CA849397F9BF33` |
| `visual-plan.json` | `4B76CFF72832BCA2527CB59D126DDC4512C9EDC35B5DAAE3C4D8287C7047604F` |

以上是暫存索引 `git show :path` 實際 bytes 的 SHA-256，與作者收據自身 SHA 無關。任一四檔再修改須重算並重核。

## 舊版審查與這次修訂

[舊版獨立逐句／配鏡收據](independent-script-source-visual-review.md)綁 `script.md` `1F92C7016D71488D4553E9D3AF246A41B2CC8435CC1A19468BED0106212CE22F`、`script-source-notes.md` `A650E4B7A4A7BA0FBCE2C279242C7B447DC5ED6C656168C98045EE96E7978C0A`、`visual-plan.md` `F625C5EF9873D7D5D72CF4ED4DF6B174040B0D24A8A22953A45686F0FC770C1B`、`visual-plan.json` `47B7720D7F4408927CDFCF7B3FA42E8A35E6F06AE30EE2284A1E5D9AE170E664`，判舊版 85/85 來源與 85/85 配鏡 PASS。此前作者按同一審查者要求，先修了七鏡錯誤的展場海報／同場館藏想像，再修鄰鏡 `c160607` 的雜誌頁；這些證據仍留在獨立收據中。

兩位互不接觸的盲讀者只看上述**舊版**旁白，分別在 [PR #1713](https://github.com/x812033727/travel_scanner/pull/1713) 及 [PR #1714](https://github.com/x812033727/travel_scanner/pull/1714) 判 HOLD。共同問題是 `no_spoiler`、`one_line`、`no_toc`、`no_recap`、`no_detour`；第二位另指出 `opening_hooks`、`one_thread`。作者沒有要求舊讀者按舊稿重判，也沒有自行宣稱修好後 PASS。

新版開場 c160103、c160104、c160106 留下鋁材、三張紙、印刷雜誌三個未揭答案的具體場景；c160107 收束線索，c160108 的具體問句是濃縮開場最後一句；1933 僅在 c160301 作回顧式設計起點，1950／1951 的可見實用新型只在 c160506–507 揭露及定性。早期家庭煮法、成品結構、水路、戰後製造、印刷與電視宣傳按時間推進；刪去館藏物件年份與膠囊產品支線，片尾只接「看見壺」與「留在爐邊」的問題。旁白從 85 句收為 81 句，逐鏡跟著旁白改為 72 張候選原創插圖、9 張後製字卡。5 秒片頭在 c160108 後，21 秒 v4 片尾與連結在 c160610 後。M16 角色身分及 M17 發明／權屬／訴訟繼續 HOLD，不當定論或畫面事實。

## 作者預檢及時長界線

- 機械檢查：81 個唯一旁白 ID 與 Markdown／JSON 81 鏡順序一對一；72 `shot`、9 `stats`，最長連卡 2；`look` 精確為 `{"preset":"cute-mystery"}`；圖片 prompt 無品牌、產品、畫家或歷史人物姓名。無可讀文字、歷史廣告重畫、受保護小鬍子角色或真實人物肖像。
- 每個事實句有 M01–M18 來源錨或明標概念／留言／訂閱性質；作者另重開國立 Museo Omero〈Moka〉的零件與持續生產段，以及 Bialetti 上市公開說明書。ADI 圖錄與 Fiera 原頁本輪連線逾時，依既有已核來源矩陣與舊版獨立收據寫作，仍需新版獨立審者直接覆核。作者不自行簽來源 PASS。
- 開場 228 字元及標點，正文 2,236 字元及標點；用每分鐘 250 字元**紙上估算**，約 55 秒加 537 秒，加 5 秒片頭與 21 秒片尾約 10 分 18 秒。沒有真實 TTS；正文是否達 480 秒與插圖時間是否達 70% 均待後續量測。不得用字數或鏡數代替。
- `git diff --check` exit 0、機械一對一與提示詞檢查 PASS、`npm run check:tasks` exit 0（驗 2,081 票；輸出的既存逾期／重疊警告與本稿無關）。

## 下一關

請作者以外的審查者對新版四份精確雜湊做來源／逐鏡差異重核，再交**兩位新讀者**只拿新版純旁白重做盲讀。只有這些關卡通過，才交站主審新版劇本與逐鏡；另有整支張數、嘗試次數與費用的付費核准。這張作者收據不授權任何付費生成、匯入、上傳、發布或合併。
