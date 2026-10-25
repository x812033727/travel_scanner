# C03 Moleskine｜新規則從零重製

站主先指定「從 C03 開始重製」，再指示「如果不行你就重新來吧」。本版採全新製作，舊 C03 原稿、上架包與支出保留；取回舊音訊和圖片不再是前置條件。**目前完成新稿、文字分鏡、獨立審查與後台送審，尚未生成任何付費素材或成片。**

## 精確版本與後台

- 機器稿：`video.json` SHA-256 `65ca1b602a5048e4f6af7c721bf1bd15abf152616c07d179f6ff5b6350c02005`。
- 作者稿：[script.md](script.md)；逐句來源：[claims.md](claims.md)。143句、110景，其中100個插畫鏡頭、9張必要字卡與片尾；規劃比例按景數約91.74%，實際時間占比待TTS量測。
- [來源／書面配鏡 r3 PASS](reviews/source-r3-delta.json)，由另一代理實核，接鏈r1真實HOLD→r2修正→r3新規劃資料。原生查核檔 [verify-1.md](verify-1.md) 已複製至canonical執行目錄。
- [兩位隔離讀者原生合併 PASS](reviews/narrative-final.json)：讀者一13 yes，讀者二12 yes、no_recap為no。依原生規則同題兩位都no才失敗；未改成一致同意，原答案與資訊密度等保留意見完整保存。
- [後台 C03 新版](https://mokaair.com/zh-TW/admin/videos?tab=drama&video=story-everyday-moleskine-c03-remake-20261025)：企劃 `3b0480b5-0ca4-4337-b743-0db04dfb4106`、劇本 `c90d3492-7efe-4385-bdcc-ccd6664205d1`，最新讀回為企劃 pending、劇本 pending。送審canonical劇本 SHA `4fbe37211a5beda9f309156f736a4bab1e2f52eb044d97ccfb6ffad3e3cf289f`；[送審原文](backend-script.md)與作者附來源稿分開，不能混用雜湊。

## 新規則與預檢

13分鐘目標、五步開場、每章對觀眾說話與旁白反應；正文每30–45秒有實質鉤子。繁中燒錄字幕與CC、MiniMax image-01及精確cute-mystery preset、bold layout d縮圖、濃縮開場後5秒正式片頭與21秒v4片尾。**實際旁白正文12–14分鐘尚未量測**；字數、估計時間戳與lint都不代替音訊。

[精確預檢](preflight-inputs.json)：lint 0 errors／31 warnings，0敘事警告；保留的長鏡頭估值、提示詞近似等仍須在真實聲音與圖片階段檢查。TTS dry-run為120請求、4194計費字元，Sulafat可用；關鍵影格dry-run為100景，含首次每景最多3次，圖像與評審目錄估價最高約US$4.05。配樂原生dry-run因缺真實timeline正常停下。以上均無付費請求。

[費用與入場](pricing-and-entry.json)分開列圖像目錄估價、TTS/ASR保守單次預留與未完成的全片報價；US$4.05只屬圖像階段，站點US$200泛上限不是本片授權。現行整片US$25停線未提高，新的精確slug仍有preproduction hold；不能借舊C03只為收尾而啟用的帳戶或改前綴繞過。

## 接續

有正式連線的操作方見 [production-entry.md](production-entry.md)。先處理精確新版的企劃／劇本決定、受保護預算帳戶與價格／費用讀回，以及正式v4素材；再依官方流程實際TTS、逐句聽檢、插畫、組片、字幕、完整解碼QA與站主看片。舊付費圖片可取回作歷史證據，[提示詞相容表](reuse-eligibility.json)只是一份書面對照，沒有宣稱已重用媒體。

236項影片文件測試全過，0 skipped；兩個runtime helper、panel builder語法與作者Python builder解析通過；53份舊稿雜湊仍未改。未上傳或發布YouTube。
