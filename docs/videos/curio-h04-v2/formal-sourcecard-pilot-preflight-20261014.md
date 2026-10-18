# H04 v2｜來源圖卡正式接入與兩鏡小樣預檢（2026-10-14）

> 這是付費前的歷史快照。後續已完成新版敘事盲審、時間軸重綁與兩張小樣；現行狀態及當時預估的訂正見[兩鏡小樣後檢](./authorized-six-pilot-postflight-20261014.md)。下方的「尚未生成／尚未送審」僅指本預檢當時。

**狀態：正式分鏡已改，兩張新增 `shot` 尚未生成；未送審、未成片。**前一份[離線有聲草剪](./opening-sourcecards-roughcut-20261014.md)保留為當時的預覽紀錄。本輪依站主接受的方向，把兩張來源 SVG 接入正式 `video.json`，並將 `tent-opening-question`、`model-paper-card` 改為待試做的 MiniMax 插畫鏡頭。台詞、句序、章節、旁白 WAV 與現行核准紀錄均未改動；沒有呼叫付費圖片、判圖、TTS、轉錄或後台審核。

## 正式變更與來源邊界

| 場景與舊模板 | 新模板及時窗 | 來源與畫面限制 |
| --- | --- | --- |
| `opening-inside`，`shot` | `diagram`，219–419 格，200 格 | [原生 SVG](./diagrams/opening-inside-source-card.svg) 明示「帳內未見隊員」及「非帳篷內部或搜救動作復原」。依 [S4 斯洛博佐夫證詞](https://dyatlovpass.com/case-files-298-300)，不是當年照片或逐物還原。 |
| `opening-gear`，`shot` | `diagram`，419–621 格，202 格 | [原生 SVG](./diagrams/opening-gear-source-card.svg) 明示留物與往山下的足跡，並說明圖標不代表件數、款式、擺放或實際路線。依 [S1 結案書](https://dyatlovpass.com/case-files-384-387-ru)。 |
| `tent-opening-question`，`big` | `shot`，2665–2808 格，143 格 | 近看匿名帳布上方向不明的小裂口，以提問接後文；[S2 鑑定](https://dyatlovpass.com/case-files-303-304-ru)才是由內側判定的來源。小樣不得看成證物復原或畫出下刀者。 |
| `model-paper-card`，`big` | `shot`，8365–8596 格，231 格 | 小型雪板的**模型概念插畫**。Gaume、Puzrin 2021 年的[原論文](https://www.nature.com/articles/s43247-020-00081-8)提出局部雪板、弱層、風吹雪逐漸加載與延遲釋放的可行機制；畫面不能冒稱 1959 年現場實測、原始論文頁或已確認事故原因。 |

兩個新提示詞以正向可見構圖為主，避開長串排除物；完整提示詞及不含歷次判圖結果的獨立覆核資料見 [blind payload](./formal-sourcecard-pilot-blind-20261014.json)。`model-paper-card` 保留舊 ID 以維持 `h4v048` 綁定，畫面不再是論文紙頁。

## 可重現的免費檢查

- 正式 `video.json` SHA-256：`6c7cd3d3a48c7fa03ba01122fb72601548867eb0faa09fc2ecde0dc507fa34dd`；改前檔 `77cc48df04e88fc35caa57fbfe7328ea984c63c296875912d32128a911429eed` 已複製至工作目錄的 `review/formal-sourcecard-adoption-20261014/before/`。兩張 SVG 的 SHA-256 分別是 `91993b66c17d004297f763068d885cf65e6531884716958a322cd091022898f8`、`2c77fc6ee9d5eddfe2f6f89c19e4e97d50f37e3dee5291ab06db5cf6e3c8c0a1`。
- 正式 renderer 分別抽出兩張 1920×1080 的原生圖卡影格：`native-render-opening-inside.png` SHA-256 `b78b7076fe76aac16b0cd6a5a43557b842898a509d945ebf5ce48147f735ca67`、`native-render-opening-gear.png` SHA-256 `3a901be54383bbd8d888e7107a5d847371641a2ccf47088f72bc7d9c81c6e427`，兩張 `layoutProblems=[]`。人工目視確認來源行可讀、字在字幕安全區上方；實際字幕／播放器字型仍待整片驗證。
- `node tools/video/cli.mjs lint --slug curio-h04-v2`：0 errors、4 warnings。三項是既存場景詞重複；一項是 `model-paper-card` **估計**停留 8.2 秒。用核准旁白的實際時碼計算，100 狀態、平均 5.3 秒、最長 **7.7 秒**、`cadenceProblems=[]`。
- 既有核准時間軸 15,827 格。正式分鏡依當前時窗計算，`shot` 7,935 格，`illustrationShare=50.1358438%`；整數門檻 7,914 格，只餘 **21 格**。兩張新圖若有一張退件或要改回非 `shot`，這個 50% 方案即不成立，不能用未生成圖或泛雪景充數。
- 乾跑 `keyframes --slug curio-h04-v2 --shot tent-opening-question,model-paper-card --takes 1 --dry-run`：MiniMax `image-01` ready，1K、無 style plate／參考圖／end frame，提示詞為 468／455 字元，分別低於 1181 字元預算；兩圖各一次正常 judge 的站端**估價合計約 US$0.03**。這只是估價，非付款收據；本輪實際新增花費 US$0。
- 正式圖片綁定 `picturesHash=615be7c0e501c98c`，舊 manifest 綁定為 `6a7fd19a5206d9bd`，已過期。舊 manifest SHA-256 `1e4f2001198c93afe78cefb3461634b4f2be43e4993bf94bfb384fb7cd1e1fcc`、ledger SHA-256 `3360f754379d1c33d1c89f6f4043d72e44934e4d80f9847a3b694de1cc3fa3fd` 均未動；ledger 為 US$2.879、215 images、213 judge calls、reserved 0。`STOP`、`LEASE` 於 repo、H04 工作目錄與其上兩層均不存在。

## 核准與採用限制

`speechHash` 仍為 `939e267cecc8f2cb`，100 句與現有 WAV 相同。預檢當時因台詞未動而估計不必重做敘事審查；實際上場景結構改動使敘事雜湊更新，後續已對 `5152905cd2a5ac0b` 另做 11/11 獨立盲審。預檢時 `timeline.json` SHA-256 `65e48861f66a7437ba3218a6601c89a1b52040a03fbcc5252ebdc5278fc2bc71` 的音訊核准仍屬舊模板。當時以現有每句 WAV 長度及時碼純記憶體重建，預期新版 SHA-256 `12b18320ed0e246b25ace3ea844f55bbc91f17374e95bc87c85fe1d2bd9b6790`；後續正式重建已精確得到該值，並重新送審、讀回此雜湊的音訊核准。Storyboard 仍無核准；新 manifest 的機器通過不能代替人工採用。

**正式採用前阻擋條件：**目前 `shot` 直接使用選中的圖片作 motion segment，原生 renderer 只處理 `diagram` 等卡片，沒有對單一 `shot` 加來源字樣的配置。生成提示詞也明確不要求模型畫字。`tent-opening-question` 須在生成畫面之外標「情境插畫／非證物復原」；`model-paper-card` 須在畫面或緊鄰且可讀的來源圖卡標「2021 年模型概念／Gaume、Puzrin／非現場實測」，不能沿用其原 `big` 字卡當已顯示。不得偷偷將這兩張照片式插畫算作來源畫面，也不得用短卡片吃掉超過 21 格的 `shot` 餘裕。小樣可以先作畫質與連戲判斷，**不能因此直接通過最終來源畫面與 QA**；排字與綁定方案需在後續正式剪輯前實作並驗證。

下一輪僅在主代理統一協調時，按站主六圖總額度中的 H04 兩鏡各做一張 MiniMax／一次正常 judge，不同鏡也要依序處理；逐張看原圖、實際選圖、假文字／假文件、相鄰畫面與帳本。若服務狀態或計費不明，停止而不重送。完整批次與成片仍待另行判斷。
