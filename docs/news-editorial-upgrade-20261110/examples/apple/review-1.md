# Apple 小樣獨立覆核 1

結論：**PASS — 內容示範可供站主審閱，無阻擋修正。** 這是文稿與官方來源覆核，不是 App 實測、採購、匯入或發布驗收。

覆核者：`layout_review`，非作者。日期：2026-11-10（台灣）。覆核範圍為 `article.md`、`draft.json`、`sources.md`，並與原 `ai-news-apple-intelligence-usage-packs-20261109.json` 比較。

## 固定文稿

- `article.md` SHA-256：`577dad5e6deb463ec8acee1713762313491d986ac61640c072cfc75ccafdb527`
- `draft.json` SHA-256：`2bcf5f224a9850026bf8a9187d6718aad1bbb8651b7388a22c14aec5276dd9a3`
- 前述 PASS 限定這兩個版本；若改動事實句、標題或導讀，需重新核對。
- JSON 解析成功；逐一比對 title、description、所有小標、段落與表格列，全部出現在 Markdown 對應內容，沒有遺漏或差異。

## 我實際讀取的證據

瀏覽工具對 Apple 頁面回傳不可取得／429，沒有將此視為通過。隨後以 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 重新直接 HTTP 取得三個官方頁面，均為 200；抽取並親讀實際正文，沒有依賴作者保存檔或只看狀態碼。

| 官方頁面 | 本次獨立讀到的內容 | 本次 HTTP 內容 SHA-256 |
| --- | --- | --- |
| [Creator Studio 智慧功能](https://support.apple.com/en-us/127888) | 有效訂閱、購買國家、用量包先後扣除、每月重置、12 個月到期、一次性購買、iCloud 購買帳號、不可家人共享、Logic Pro 的查看／History／購買路徑、Apple 晶片／macOS 27／iCloud／美式英文／beta 條件。頁面發布日 2026-11-05 | `7c03dd4b342e30c3571e14faaf2934227defd30c0bc6f8cf28efb76cfe85b42a` |
| [媒體服務適用地區](https://support.apple.com/en-us/118205) | Taiwan 區塊確實列 Apple Creator Studio；相鄰國家段落已區分，沒有把其他地區的條目誤歸台灣 | `fc5efd2ebd7ec23aff72fec485c2476a7315a9365d8d582c7df4899570bd4dce` |
| [Apple Intelligence Usage Terms](https://support.apple.com/en-us/148587) | 第 1 節支持特定功能達限後暫停或受限、等待重置、其他裝置功能仍可使用；第 5 節只說部分功能可能有依地區不同的年齡限制，未列固定年齡。頁面發布日 2026-09-09 | `dc6e8857b94fd4f018b34d01b69894b253978f730ae85c705c1e1cfb16876975` |

未獨立重新讀取作者「未採用」的 The Verge 與 Apple 127901；它們不是本稿現行主張的證據。沒有登入 Apple 帳號、打開 Logic Pro、取得按鈕畫面或購買。稿件標為官方路徑，未冒稱本站實測。

## 主張與編輯判定

- **價格：PASS。** 沒有把舊稿的 49.99 美元寫成官方或台灣售價，也沒有擅自換算、填入台灣上市日、宣稱每包固定可問幾次。正文清楚限制到已核對官方頁面未列台灣價格／日期。
- **地區與方案：PASS。** 八個用量包購買國家與有效 Creator Studio 訂閱條件正確；台灣訂閱可用和加購名單分開，不誤導成台灣完全無法使用智慧功能。
- **入口與條件：PASS。** Show Usage、History、Buy More Usage 的關係與 Mac 條件一致；作者已依前置建議補入 beta。未宣稱上述為適用所有 Apple Intelligence 的單一門檻，也未虛構年齡數字。
- **額度：PASS。** 每月原有額度先用、加購逐月保留至購買後 12 個月、一次性購買、不可家人共享，皆有正文支持。
- **標題與導讀：PASS。** 標題提出 Logic Pro 使用者的實際問題，也承諾回答台灣範圍；正文確實回答。沒有以全面收費或恐慌語句誇大。導讀較長但資訊明確，無必須修正的誤導。
- **新增有效資訊：PASS。** 相較舊稿，新增購買地區／訂閱資格、台灣服務區分、先後扣額、History 查看、助理系統／語言／beta 條件；都有目前官方證據。移除其他 App 本月上線預測與外媒價格反覆 FAQ，內容增益不是單純換標題。

## 精確修正清單

**無待修阻擋事項。** 前置建議的 beta 狀態已出現在 `article.md` 第 17 行及 JSON 對應段落。沒有對流量、點擊率或收入改善作保證。
