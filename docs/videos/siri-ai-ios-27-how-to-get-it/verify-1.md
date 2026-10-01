# 查核報告 第 1 輪（2026-09-30，選項 C 重寫稿）

獨立驗證者，非撰稿者。舊稿的 `verify-1.md`、`verify-p1-20260929.md` 只當作「以前錯在哪」的線索；本表每一條都在 2026-09-30 重新開啟官方頁。抓取的頁面與抽出的說法清單在 `mokaair-work/videos/siri-ai-ios-27-how-to-get-it/_tools/verify-r1/`（`dump.txt`）。

網址：N＝https://www.apple.com/newsroom/2026/09/siri-ai-a-profoundly-more-capable-and-personal-assistant-is-here/（200，UPDATE September 14, 2026）　S＝https://support.apple.com/en-us/127893（200，Published Date: September 22, 2026）　UG＝https://support.apple.com/guide/iphone/turn-on-and-activate-siri-iph83aad8922/ios（200，iOS 27 版）　O1＝https://help.openai.com/en/articles/11487775-connected-apps-in-chatgpt（200，Updated: 11 hours ago）　O2＝https://help.openai.com/en/articles/8357869-how-to-change-your-language-setting-in-chatgpt（200，Updated: 2 months ago）　G1＝https://support.google.com/gemini/answer/13695044?hl=en（200）　G2＝https://support.google.com/gemini/answer/14579026?hl=en（200）

| # | 說法 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Siri AI 9/14 起以 beta、英文推出 | hook、language-gap、language-region | N、S | 200 | CONFIRMED | |
| 2 | Apple 說它理解你的個人情境 | ne2s、dtqw、vypt、recap | N、S | 200 | CONFIRMED（「直接」是撰稿用語，Apple 原文為 understands personal context） | |
| 3 | 個人資料來源：訊息、郵件、行事曆、備忘錄、提醒事項（支援頁列五個加 and more） | five-sources、what-it-reads | S | 200 | CONFIRMED | |
| 4 | 表格 Siri AI 列：系統直接理解訊息、郵件／系統層級 App 動作／目前只有英文 | three-assistants.rows[0] | N、S | 200 | CONFIRMED | |
| 5 | 表格 ChatGPT 列：你自己連接帳號／連接後做支援的動作／支援中文 | three-assistants.rows[1]、fg87 | O1、O2 | 200 | CONFIRMED（O1：choose an app, connect an account if prompted；Take supported actions；O2 語言清單列 Chinese，未分繁簡） | |
| 6 | 表格 Gemini 列：你自己選要連哪些／同意後可編輯 App／含繁體中文 | three-assistants.rows[2]、swab | G1、G2 | 200 | CONFIRMED（G1：Choose which apps Gemini connects to；With your permission … editing and managing your content in other apps；G2：Chinese (Simplified / Traditional)） | |
| 7 | 連好以後都能替你做事，能連什麼看方案、地區和裝置 | 6trj | O1、G1 | 200 | CONFIRMED（O1：plan, region…interface；G1：Gemini app, device, country） | |
| 8 | ChatGPT 和 Gemini 現在就能用中文 | language-gap、m823、chinese-users | O2、G2 | 200 | CONFIRMED | |
| 9 | 四種能力：個人情境、世界知識（上網）、螢幕感知、系統層級 App 動作 | four-abilities | N、S | 200 | CONFIRMED | |
| 10 | App 動作例：傳訊息、建立行程 | ni9m | S | 200 | CONFIRMED | |
| 11 | 家傳食譜示範（訊息→郵件→提醒事項購物清單），標明是 Apple 的例子 | recipe-demo | N | 200 | CONFIRMED | |
| 12 | 螢幕感知例：看球隊網站，把主場比賽加進行事曆 | onscreen-example | N | 200 | CONFIRMED | |
| 13 | 獨立 Siri App，用 iCloud 同步對話，手機開頭可在別的裝置接著問 | siri-app | N、S | 200 | CONFIRMED | |
| 14 | 三種喚醒：Hey Siri、長按側邊按鈕、動態島下滑 | invoke-ways | N、UG | 200 | CONFIRMED（「長按」N 未寫，UG：Press and hold the side button） | |
| 15 | Siri AI 系統層級入口；ChatGPT、Gemini 各自的 App 只能找你連接過的服務 | two-homes.right.points[1]、jep2 | O1、G1 | 200 | CHANGED | 「只能找你連接過的服務」→ 畫面「找你的資料靠連接的服務」、旁白「找你的資料要靠連接的服務」。G1：部分 Connected Apps designed to automatically work with Gemini，且 Gemini 自動使用 Google 搜尋等服務的公開資訊，「只能」與「你連接過的」都說過頭 |
| 16 | iPhone：15 Pro 系列、16 系列以後、iPhone Air | devices.rows[0]、zvte | S | 200 | CONFIRMED（N 的機型段未單列 iPhone Air，S 有） | |
| 17 | iPad mini A17 Pro、M1 以後 iPad | devices.rows[1]、rq8n | S、N | 200 | CONFIRMED | |
| 18 | Mac：M1 以後、MacBook Neo | devices.rows[2] | S、N | 200 | CONFIRMED | |
| 19 | Apple Watch：Series 9、Ultra 2、SE 3 以後，須搭配已開 Siri AI 的 iPhone | devices.rows[3]、mer4 | S | 200 | CONFIRMED（S 原文 Series 9 or later、Ultra 2 or later、SE 3；見「懷疑但沒動」） | |
| 20 | Vision Pro 所有機型 | devices.rows[4]、rt3s | S | 200 | CONFIRMED | |
| 21 | 不在清單的舊機型不會有 Siri AI | n4yd | S | 200 | CONFIRMED | |
| 22 | 法、日、韓、葡、西「十月」加入；旁白「Apple 九月十四號說十月加入」 | language-region.stats[1]、af4g | N | 200 | CONFIRMED（推論：N 發布日 2026-09-14，原文 next month；S 9/22 版只寫 currently available in English） | |
| 23 | 未滿 13 歲不提供 | language-region.stats[2]、6jei | N | 200 | CONFIRMED（註腳 Siri AI is not available for users under 13） | |
| 24 | 歐盟：iOS、iPadOS、watchOS 不提供；Mac 與 Vision Pro 英文可用 | eu-china.left、4xkv | S | 200 | CONFIRMED | |
| 25 | 中國大陸帳號地區目前無法運作 | eu-china.right、3ssf | S | 200 | CONFIRMED | |
| 26 | 帳號須在符合資格的地區，支援頁沒列清單、沒提台灣 | eligible-region | S | 200 | CONFIRMED | |
| 27 | 裝置語言與 Siri 語言須一致，現在要整台改英文 | language-tradeoff、v485 | S | 200 | CONFIRMED | |
| 28 | 中文訊息能否處理、繁中時程 Apple 沒說 | a8gr、f9ab、jvk4 | N、S | 200 | CONFIRMED（兩頁都沒寫） | |
| 29 | 開通五步：更新 iOS 27 → 設定 → Siri（關著先打開）→ Try Siri AI (Beta) → 選聲音、語音登錄 → 檢視隱私設定 | how-to-enable | S | 200 | CONFIRMED | |
| 30 | 加入等候名單，等待時間不一，輪到才自動下載 | waitlist、rape | S | 200 | CONFIRMED | |
| 31 | 螢幕內容它也看得到 | riw5 | N、S | 200 | CONFIRMED | |
| 32 | 裝置端加私密雲端運算；處理時個人資料不儲存、Apple 無法存取；外部專家可隨時驗證 | private-cloud | N | 200 | CONFIRMED | |
| 33 | 新模型與 Google 及其 Gemini 一起打造 | h83z | N | 200 | CONFIRMED（Apple Foundation Models … in collaboration with Google and its Gemini models） | |
| 34 | ChatGPT、Gemini 自己選要連哪些帳號、隨時能中斷 | privacy-switches.right、u8jx | O1、G1 | 200 | CONFIRMED（O1：disconnect apps from Settings > Plugins；G1：anytime） | |
| 35 | 仰賴伺服器的功能有每日上限，Siri AI 在其中；之後付費提供更多用量 | daily-limits、4bj2、fa3w | N、UG | 200 | CONFIRMED | |
| 36 | beta 回答可能出錯、規則之後會改 | daily-limits.items[2]、9gfn | N | 200 | CONFIRMED（泛稱 beta；N 寫 daily limits vary by … system policies；「會出錯」官方未明寫，見懷疑） | |
| 37 | 結尾文章〈三大助手日常比較〉存在 | wrap、w3v9、description | repo `apps/api/app/guides/content/gemini-vs-chatgpt-vs-claude-daily.json` | — | CONFIRMED（zh-TW 標題「三大助手日常比較：同題操作與評分方法」；官方功能比較與同題練習，明說不是實測排行；只有 zh-TW，未提 Siri） | |
| 38 | 說明欄第一行的站內文章（source_guide） | 96fq | repo `ai-news-siri-ai-ios-27-20260914.json` | — | CONFIRMED（存在） | |
| 39 | 標題、縮圖（New Siri. Can you get it?）、說明、標籤 | youtube、thumbnail | — | — | CONFIRMED（無數字；內容與上列一致） | |
| 40 | 語言選擇是台灣使用者最大的取捨；它住在系統裡是最大的不同 | jedh、a2rk | — | — | OUT OF SCOPE（判斷句，見看法） | |

## 摘要

- 查了 40 條：CONFIRMED 38、CHANGED 1（#15）、NOT FOUND 0、OUT OF SCOPE 1。另在 `claims.md` 更正證據文字：c18 的選單名稱現為 Settings > Plugins；c22 補上 Gemini 有預設連動的 App 與自動使用公開資訊。
- 會過期：#22「十月」與「目前只有英文」——N 2026-09-14 寫 next month，S 2026-09-22 只寫 currently available in English；10 月語言上線後 language-region、language-gap、recap、chinese-users 都要改。O1 頁「Updated: 11 hours ago」，選單名稱常改；每日上限之後會有付費方案（N 未給日期）。
- 看法對照 brief §站主觀點：32wr「比起誰比較聰明，更該看它讀你多少、你能不能自己決定」一致。d2h9「連得越少、越清楚，用起來越安心」是延伸（站主觀點講「讀多少、自己決定」，沒講少連），不矛盾，有標記。7qte 以「我的答案是」標記，「不是因為它比較聰明」與觀點一致。jedh「最大的取捨」、a2rk「最大的不同」是未標記的判斷句，報告不改。
- 聽眾檢查：超過 40 字 mer4（45）、4xkv（43）、unw2（41）；沒有「經查證／根據官方文件／本影片」、括號或網址；Latin 詞都在 lexicon（逐字）。
- lint：0 errors、0 warnings，8.8 分鐘、108 句。
- 懷疑但沒動：Apple Watch「SE 3 以後」——S 原文只寫 SE 3（沒有 or later），目前沒有更新的 SE，不算錯；「beta 回答可能出錯」是一般說法，官方沒寫；「直接理解」的「直接」是撰稿用語；S 另寫開通後出國仍可用（稿中沒提，舊報告說已刪，其實官方有寫）。
- 第二輪：不需要（FACT 修改 1 條，未超過 3 條）。
