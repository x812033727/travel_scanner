# Instagram 小樣獨立覆核 1

結論：**PASS — 內容示範可供站主審閱，無阻擋修正。** 僅驗證文稿與可讀官方公告，沒有登入、操作生成工具、送審或驗證台灣帳號。

覆核者：`layout_review`，非作者。日期：2026-11-10（台灣）。已讀作者三檔，並與原 `ai-news-instagram-effect-builder-20261109.json` 比較。

## 固定文稿

- `article.md` SHA-256：`21c418c45a0bc88b4b48d43e7d1011e35c2379f598a6a5ecac1fbbbf528f6fd8`
- `draft.json` SHA-256：`357b5c77b119689d6abf0156b802206cf136cf5c95447529da89e63da041f44c`
- JSON 可解析；title、description、所有小標與段落逐項比對 Markdown，全部相符。PASS 限定上述版本。

## 我實際讀取的證據與受阻範圍

瀏覽工具無法取得官方公告與 The Verge；隨後以 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 直接 HTTP 取得正文並親讀，沒有拿作者收據當作自己的閱讀紀錄。

| 頁面 | 本次獨立讀取結果 |
| --- | --- |
| [Instagram 官方完整公告](https://edits.instagram.com/blog/introducing-effect-builder/) | HTTP 200，201180 bytes；讀到標題、2026-11-09 日期、三步流程、構想建議與末段地區／年齡／免費條件。SHA-256 `fae27970701c1601cb160ae761681aefe2301cf345c0281b3b8c3946f31d5ee7`。這是本稿產品事實的唯一完整官方來源 |
| [官方短入口](https://edits.com/effectbuilder) | 跟隨轉址到 `edits.instagram.com/login/`，next 指向 `/app/effects`，HTTP 200。只證明官方入口及登入轉址，沒有進入編輯介面。SHA-256 `20541fecbd3c925ae153fd69daf41df2f208d598b70d5b614790edd4d172dc22` |
| [Instagram Help Center](https://help.instagram.com/2290747514829899/) | HTTP 200，345962 bytes；抽取可讀正文只得 Help Center。不能算第二份內容證據，沒有藉此補年齡、地區、額度或政策。SHA-256 `f8e52268d524d1cf1313a7ed908d25c125b640043f70e76914b4a071680e257a` |
| [原稿 The Verge 報導](https://www.theverge.com/tech/1030061/instagram-ai-effect-builder-filters) | HTTP 200，讀到完整正文及 2026-11-09 日期。對照舊稿用；不是本稿新增產品條件的證據。SHA-256 `b04479db729f1eeaeea4b10827bc3601dc6c5d6dbddb8195d31e794f13d12c3e` |

## 主張判定

- **價格／方案：PASS。** 官方末段支持免費製作與發布；稿件沒有引申所有 Meta 產品都免費，沒有編造方案、用量或付費後權益。
- **年齡：PASS，僅保留公告措辭。** 官方原文為 `people over 18`，稿件譯作「超過 18 歲」。這不是已驗證平台按生日如何判定，也不據此自行宣稱「年滿 18 一定符合」或「必須滿 19」。若未來要作精確資格操作指南，仍需能讀到的完整規則或帳號驗證。
- **地區：PASS。** 公告目前列美國，未列台灣推出日期；稿件把製作資格與已核准效果的套用範圍分開，不誤稱台灣完全不能使用任何效果，也未保證台灣帳號能看到所有效果。
- **入口／流程：PASS。** 網頁工具、文字描述、自己的照片預覽、提交安全審查、核准後進 Stories 效果瀏覽器，均在官方三步流程。入口也實際轉向對應工具登入頁。未登入，所以不把這次讀取寫成實測。
- **作者曝光機制：PASS。** Instagram handle 可點進個人檔案、Try it、My effects 與自己的限動分享都有官方明文；沒有推定一定增加觸及或收入。
- **未提供的數字：PASS。** 未填審查天數、通過率、台灣開放日期或生成成功率。活動應留意審查的句子屬清楚可辨的編輯建議。

## 標題、導讀與新增有效資訊

標題以誰能用與怎麼分享為承諾，正文確實回答。定稿導讀已直接寫美國、年齡與台灣尚未列入，沒有以「看清楚範圍」保留懸念；不構成誇張的全面開放宣稱。

相較舊稿，新增官方確認的免費條件、官方短入口、My effects 與 Try it、製作與套用範圍區別。移除單次記者實驗所衍生的品質暗示，不再把未從官方讀到的參考圖上傳與 AI 改寫介面細節當主幹。資訊增益可由本次官方正文支持，沒有把字數或更多來源連結當作品質證明。

## 精確修正清單

**無待修阻擋事項。** 前置建議已完成：年齡保留 `over 18` 含義、導讀直接揭示目前資格。來源頁／資格若改動，需更新查核；本次 PASS 不代表帳號可用、功能實測或發布授權。
