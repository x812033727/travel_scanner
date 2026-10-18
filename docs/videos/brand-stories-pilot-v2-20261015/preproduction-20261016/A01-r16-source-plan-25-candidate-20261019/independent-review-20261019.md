# A01 r16 來源企劃元資料獨立複核：離線 PASS，正式製作 HOLD

日期：2026-10-19。審查對象限於 `manifest.json` SHA-256 **`61257B4687F232FA8A963332F4C8FAB988A83565CE4F08615C5E0CEEAC7D449A`** 的來源企劃候選。結論：本次機械與出版者元資料檢查 **P0 = 0、P1 = 0、P2 = 0**；這不是 78 筆主張的正式事實審查，也不是主機採用或付費製作核准。

## 精確差異與來源歸屬

`node build.mjs --check` 退出碼 0。建置器釘選 r12 六章橋接與 r16 稿件的雜湊，從橋接 `candidate/series.json` 唯一一次把零起算索引 23 的 `publisher` 由「Plath 2024 年校友刊自述（第 17 頁）」改為「West Seattle High School Alumni Association《Chinook》」，再把該欄改回並對原企劃做完整物件比對；其餘欄位、來源 URL、順序、`must_verify` 及索引 24 均相同。出版者與作者分開是合理的：[校友會官方期刊索引](https://wshsalumniassociation.org/chinook-archived-issues/)將《Chinook》列為 West Seattle High School Alumni Association 的期刊；Plath 的自述歸屬仍留在索引 23 的 `supports` 與 `t7b` 主張。

檢查器重算 23 筆 r16 編輯企劃來源、25 筆補足後的內部企劃來源、18 筆公開引用來源及 78 筆仍為 `PENDING` 的主張 URL 對照；`t7b` 對應企劃索引 23／公開索引 16，`n14` 對應 24／17。另有 7 筆內部研究來源不屬於公開引用。對樓梯的有限陳述有 [Travelpro 官方比較文章](https://travelpro.com/blogs/the-travelpro-blog/bring-this-not-that-duffel-bags-versus-rolling-suitcases)支持，但不能擴張為所有旅客或所有輪箱的通則。候選原五檔共 55,462 bytes，沒有符號連結；針對憑證、私有本機擷取路徑、主機連線資訊和常見個資格式的掃描無命中。

## 未重驗的史料與後續關卡

本次網頁讀取器無法取得約 33 MB 的《Chinook》PDF，**沒有重新查證第 17 頁的 1988 年自述文字，也沒有驗證 SL8 與校友會鏡像 PDF 的位元組相同**。本審查只確認官方期刊索引支持出版者欄位的歸屬，並保留候選稿對 Travelpro 1987 年說法與 Plath 晚年自述差異的未定論。正式事實審查仍須針對可取得的原始頁面與正式保存稿另行完成。

本候選 **HOLD**：不能直接把 25 筆內部來源當成公開來源匯入；A01 的公開來源過濾、正式六章／主張 ID 重編、verifier、listener、兩名獨立敘事讀者及綁定正式檔案雜湊的 `story/reviews/script-review.json` 均未由本審查完成。本檔不授權正式機寫入、解除 STOP、付費圖片或配音、合成及上傳。
