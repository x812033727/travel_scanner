# B18 名稱移除：獨立差異審查請求

請以父候選 `sha256.json` `56d6602b844a5daa055c7a176ad7db739d5ee29150c22eacb89110006071c05a`、父版獨立審查 `bbb3782c57ec05c4ba0c58dfb766343e67f4ef4f890c051ed93c8552dd1508a1` 和本包 `sha256.json` 為精確版本界線。

1. 跑 `node build.mjs --check`、`node manifest.mjs --check`，獨立比較 JSON 物件：`B18.json:/names` 僅刪「朝日啤酒／アサヒビール／Asahi」；`series-adoption.json:/names` 與 `/plan/names` 同步，其他欄位不變。
2. 逐檔比對六章 `remapped-chapters/` 與父版、`claim-coverage.json` 雜湊，確認 65 筆 `UNCHECKED` 主張、來源、fact、全部旁白／景／loops 不變。離線 `composeStory` 可完全相同，但仍不可用來宣稱成片相同。
3. 檢查舊企劃中的啤酒公司名稱是否在旁白、圖像提示、標籤、`must_verify`、來源 `supports` 或 caveat 以事實語氣殘留；尤其要核對 `image_notes` 的無商標限制仍在。來源只支持「吹田一座啤酒工廠」時，不替它猜公司。
4. 確認[法院判決 PDF](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)的讀取限制與父審查所述的 1972／1978 差異仍明列，不要把前版離線 PASS 當成本版正式 hash 綁定 review 或 worker PASS。若極小差異安全，請給本版精確 SHA 的**差異審查**；之後才安排新的正式 `reviews/B18.json`、雙集匯入編譯與主機 dry-run。

任一非名稱欄位漂移，或發現未證實公司已進入故事／圖像，請標 HOLD 並指明檔案、欄位與來源段落。本請求不授權正式匯入、付費製作或上傳。
