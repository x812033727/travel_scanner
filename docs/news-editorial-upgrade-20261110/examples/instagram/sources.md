# Instagram 樣稿來源與編輯紀錄

狀態：作者完成，待獨立查核；未發布、未匯入 repo。

查讀日期：2026-11-10（台灣）。所有外部請求使用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，`curl -L` 跟隨轉址。原始 HTML、移除註解／script／style 後的文字、大小與 SHA-256 保存在 `evidence/`。

## 實際讀取

| 來源 | 結果與採用範圍 |
| --- | --- |
| https://edits.instagram.com/blog/introducing-effect-builder/ | HTTP 200、201168 bytes，讀到完整公告與日期 Nov 9, 2026。標題 Introducing Effect Builder: Turn your idea into an Instagram Stories effect。唯一用於本文產品事實的官方來源 |
| https://help.instagram.com/2290747514829899/ | HTTP 200、346248 bytes，但移除 script／style 後僅剩 Help Center。Meta title 是 About Effect Builder，不能代替本文；未用來補功能、地區、規定，也未列為文章來源 |

沒有把 shell 頁、來源數量或 HTTP 200 本身當成事實驗證。這篇只需要一份完整官方公告即可支持已寫內容，不湊第二個來源。

## 主張對照

- 開放資格、費用：公告末段明寫 available in the US for people over 18，以及 free to create and publish effects。樣稿保留「超過 18 歲」的原文含義；沒有把它擅自改為精確的年滿 18 歲。台灣不在該次公告的製作工具範圍內，未見台灣開放日期。
- 功能形式：首段 web-based tool、No design or coding experience needed；文字提示產生效果，使用自己的照片預覽。
- 構想例子：第一步官方直接舉 warm vintage film grain、dreamy pastel watercolor、bold comic-book contrast。樣稿依序譯成復古底片顆粒、粉彩水彩、漫畫風格，未加生成成功率。
- 構想與測試：Ideas for your first effect 問讀者想要的濾鏡、內容的視覺世界與社群希望分享的東西。樣稿把它整理成先想氛圍與使用情境的讀者建議；不聲稱有特定編輯控制介面。
- 安全審查：How to create and publish 第 2 步。所有效果都要通過安全審查，核准後才加入 Stories effects browser；原文未列審查耗時或通過率。按活動日期預留等待的提醒是依此流程提出的編輯建議，不是官方時程。
- 作者連結與分享：第 3 步明載 Instagram handle、tap through to profile、Try it、My effects，以及可先在自己的限動套用分享。
- 台灣套用效果的限制：公告沒有逐國列出已發布效果的觀看／套用資格，因此樣稿不把製作工具的美國限制擴張成「台灣完全不能用任何效果」，也不保證台灣帳號一定能看見全部已核准效果。

## 相對原公開稿的調整

1. 以官方開放資格與台灣讀者能否動手做開場，移除重複的「據 The Verge」句型。
2. 以讀者操作階段組織：構想、預覽、審查、他人使用與作者入口。保留限制，沒有假裝已實測。
3. 不沿用只有外媒報導、未在完整官方公告找到的風格參考圖上傳、AI 改寫提示詞、後續聊天指令等介面細節。
4. 不把外媒記者一次漫畫提示詞結果寫成工具品質定論。
5. 不聲稱增加觸及、粉絲或收益。官方提到被發現的機會，樣稿只確定描述可點回作者頁的機制。
6. 不捏造台灣售價、推出日期、審查天數或通過率。

## 格式與待辦

`draft.json` 含 title、description、4 個 sections、1 個實讀官方 source。`article.md` 與 JSON 內容一致，每節附官方公告連結。正文含 description、段落與小標共 750 個 CJK 字元（不含來源連結），未硬填 FAQ 或表格。依獨立查核者初步意見，導讀已直接說明美國／年齡資格與台灣尚未列入，不讓資格限制成為懸念。

下一關是另一位代理逐項查核並對定稿檔雜湊出具 review。本檔是作者的來源紀錄，不等於獨立查核通過。
