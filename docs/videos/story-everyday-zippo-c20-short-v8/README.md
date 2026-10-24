# C20 Zippo｜v8 短版非付費機器專案

此資料夾從站主核准的 **36 句／36 鏡**短版建置。舊 `../story-everyday-zippo-c20/` 根目錄的 42 句 `script.md`、`visual-plan.md/json` 是歷史版，沒有改寫。新專案用獨立 `story-everyday-zippo-c20-short-v8` 影片 slug，仍指向作品 `brand-stories-everyday-reversals` 第 20 集；**尚未核定後台如何避免同集重複匯入，不得直接送正式匯入**。

## 鎖定輸入與核准

`build.mjs` 在讀取舊專案 `reviews/` 的三份 v8 檔案時，先核對原始 UTF-8 SHA-256，再逐 ID 比對劇本表、只讀旁白投影和 JSON 分鏡的旁白及來源註記。任一字元改動都拒絕重建。輸出六個機器與說明檔，`--check` 只讀比較輸出，不覆寫。

| 鎖定輸入 | SHA-256 |
| --- | --- |
| `reviews/v8-short-script-candidate-20261024.md` | `8BF33F7F733D5ACB8C7AC64186B5932C43E6BB06867A6FFBF2ECC6BF0E68D82D` |
| `reviews/v8-short-blind-plain-20261024.txt` | `358000A1EBA0DEF8D2C3FBE0C7DDB8276BBACAB74F82C534750BBBEAC40814E5` |
| `reviews/v8-short-visual-plan-candidate-20261024.json` | `D30CBE9F9E92BF8339D82671879EF465538D1691885B5161CA85D7E10D571419` |

獨立來源及相鄰畫面覆核為 36／36 PASS；兩位只讀旁白盲讀各 12／12 Yes。站主對此版劇本與分鏡的核准在 `../story-everyday-zippo-c20/reviews/owner-v8-short-script-approval-20261024.md`；整支本機試片最多 US$25 的另次核准在 `../story-everyday-zippo-c20/reviews/owner-v8-paid-pilot-approval-20261024.md`。報價及嘗試上限見 `../story-everyday-zippo-c20/production-quote-v8.md`。本資料夾只是轉檔，沒有重新取得內容核准。

## 產物與操作

```text
node docs/videos/story-everyday-zippo-c20-short-v8/build.mjs --check
node docs/videos/story-everyday-zippo-c20-short-v8/preflight.mjs
node tools/video/cli.mjs lint --file docs/videos/story-everyday-zippo-c20-short-v8/video.json
```

影片資料是六章一對一的 36 個 scene：**33 個 `shot`** 和 **3 個本機 `big` 字卡**（`c200207`、`c200302`、`c200511`）。品牌名只在旁白、後製縮圖和文字卡；33 個圖片提示詞取自核准 JSON，MiniMax 只能用 `image-01` 和精確 `look: {"preset":"cute-mystery"}`。不得畫商標、可讀字、實物專利重建、真人肖像、火焰、吸菸或點火步驟。片頭排在 `c200107` 後 5 秒，片尾在 `c200610` 後 21 秒，字幕只用可關閉的繁中 CC。

`preflight.mjs` 已確認 schema 及奇聞視覺靜態限制零錯誤。紙上時間軸 9,995 正文影格＝333.167 秒，插圖 9,105 影格＝約 91.10%；再加既有 26 秒片頭片尾約 5:59。這些**不是實際配音或成片量測**。

## 明確停線

`c200102` 的顯示逐字稿保持「Zippo」；僅配音用的 `say` 暫按 [Zippo 中國官網所用「之宝」名稱](https://china.zippo.com.cn/cn/about/whole-journey.html)寫為「之寶」，`say_for` 綁原句雜湊。這是非付費讀法預排，仍須獨立逐字比對及實際人耳聽驗，不能以 lint 通過宣稱配音合格。

現行通用 lint 仍有兩個錯誤：短版 `target_minutes: [5,7]`、估時正文未通過通用八分鐘關卡。需要 C20 精確稿件綁定的短版**實測**時間政策，不能靠片頭片尾填補正文，也不能降低其他集的八分鐘門檻。圖片提示詞的近景／中景／俯視用中文，現行英文關鍵字檢查另給 33 個景別警告；部分紙上鏡頭估時超過十秒，須在實測聲音與片格階段審視，不能因此擅改核准分鏡。

付費前另須讀回 C20 單集可歸因預算路由、供應商實價、已花與未結請求，鎖住整支最壞情形不超過 US$25；先量 36 句實際聲音，再決定購圖。沒有本機 final.mp4、後台匯入、上傳或發布。任何改旁白、卡片文字或圖像方向都須新查核與站主精確核稿。
