# H05 v2｜62 個插圖鏡頭的來源與畫面路線稽核

日期：2026-10-14。只核對現行 `video.json` 的插圖鏡頭、已核准的逐句音訊時間軸、已記錄的三輪開場圖失敗，以及 [FBI 案件史](https://www.fbi.gov/history/cases-and-criminals/db-cooper-hijacking)、[FBI 2016 聲明](https://www.fbi.gov/contact-us/field-offices/seattle/news/press-releases/update-on-investigation-of-1971-hijacking-by-d.b.-cooper)、[Kaye、Meltzer 2020 論文](https://pmc.ncbi.nlm.nih.gov/articles/PMC7400570/)中的相關原始陳述。這是分鏡與提示詞預檢；沒有新增付費圖像，也沒有全片畫面可供驗收。

## 時間與關卡邊界

- 現行 62 個 `shot` 共 **318.533 秒**，佔實際 535.767 秒的 **59.45%**。降到 50% 的可用空間只有 **50.650 秒**；不能把所有難畫的實物或科學鏡頭改成文字卡，仍宣稱插圖比例通過。
- 實際 108 畫面狀態，平均 5.0 秒、最長 7.3 秒；`cadenceProblems=[]`。本輪只改 13 個 `data.prompt`，沒有改場景型別、順序、台詞、reveal、語音或 timeline。`narrativeHash=65c64491d8a53b77`、`speechHash=7d8cb6cb30ba87d9`、`timeline.json` SHA-256 `8128f74e74f2dad44ea0c6a1465f2a333c4cb30d0b7f9cfb14829f414becd984`，仍是站主已核准的版本。
- 本輪前 `video.json` SHA-256 `f90cc5e16c1da87b46d9a59ffc4be8af4d313778ad3c88750350d36ae2b8ab7e`；本輪後 `74102087ca465c7c73044e1182671641965cc19cbd6f4d0470d11fcb9c16e6e3`。更改插圖提示詞會使受影響鏡頭的 `pictures_hash` 改變；先前生成的圖不能直接被新版採用。

## 已做的 13 個窄修

| 鏡頭 | 來源／先前風險 | 目前提示詞只改的畫面意圖 |
| --- | --- | --- |
| `open-note` | c04；兩隻手交紙條容易生出畸形肢體或假字 | 改成一隻手遞無字折紙，空服員只露袖口；保留遞交動作。 |
| `open-tail` | c07 的畫面界線原定只畫遠景飛機；舊稿畫出空中階梯 | 遠處無標誌三引擎機身與夜雲，不畫階梯、人或推定落點；該句事實由旁白說。 |
| `captain-note` | c25 有轉交第二張紙條，但舊稿要畫兩手交接、駕駛艙內部 | 空服員背影在駕駛艙門口持無字折紙，不猜機長手勢或儀表細節。 |
| `demand-question` | c01/c05 未說有桌上紙包；舊稿發明紙包 | 以機場服務通道與外面的停機坪建立即將在西雅圖兌現條件的場域。 |
| `agency-alert` | c26 只說 FBI 在飛行中得知消息，未記通報媒介 | 以探員拿出空白卷宗開始工作作概念場景，不畫電話通報或假公文。 |
| `second-flight-night` | c06 說飛機再起飛；舊稿只有空跑道 | 遠景無標誌飛機離地，對上旁白動詞。 |
| `sand-find` | c12 未記採證紙袋；舊稿把它放在河岸 | 改成沙洲近景，避開虛構紙袋、尋獲洞口或額外鈔票。 |
| `tie-brand` | c27 說黑領帶留機上；舊稿發明透明典藏套 | 領帶掛在空座，避免推論後續包裝、儲存方式。 |
| `tie-storage-box` | c08 說取得 DNA 樣本，沒有公開採樣操作細節 | 只看黑領帶纖維，不畫棉棒、試管或取樣手勢。 |
| `tip-standard` | c30 沒有「身分欄位」官方表格；舊稿讓 AI 畫空白表單 | 傳聞紙張與封閉物證袋保持距離，不畫表格、名字或已確認嫌疑人。 |
| `control-limit` | c17 的十一月實驗直接浸河水；舊稿並排兩瓶河水誤示兩組都先採瓶裝水 | 兩份現代對照紙片與單瓶水，與原鈔隔開；不模擬兩個實驗的精確器具。 |
| `layers-sample` | c19 的關鍵是較大矽藻位於原鈔夾層；舊稿只畫封閉金屬盒 | 用簡化紙層剖面與一枚內側小點呈現位置，不冒充原論文顯微照片或生物形態。 |
| `simple-story-changed` | c18/c20 沒有確定年份／抵岸日；舊稿以冬景暗示季節 | 中性陰天的空河岸，不畫季節標誌、抵岸人物或搬運路線。 |

## 其餘 49 鏡的預檢處置

完整逐鏡的原始提示詞和各鏡來源 ID 仍在 `video.json`。以下兩組加上上表 13 鏡，覆蓋全部 62 鏡且沒有重複：

| 狀態 | 鏡頭 ID | 後續驗證點 |
| --- | --- | --- |
| 22 鏡：具體物件或行動，提示詞暫保留（112.533 秒） | `open-drink`, `open-threat`, `open-boy`, `open-tie`, `open-scope`, `open-question`, `briefcase-latches`, `suit-and-tie`, `sealed-ransom-bag`, `seattle-ground`, `delivery-table`, `aircraft-search`, `chute-cord`, `boy-bank`, `transport-question`, `sample-room`, `single-bill-sample`, `modern-control-context`, `seasonal-comparison`, `star-fragments`, `burial-edge`, `burial-inner` | 驗真人／手與道具是否多生、文件是否有假字、原件與示意是否混淆；`star-fragments` 和兩張滲入圖另查生物形態與紙層位置。未看新圖，不判可用。 |
| 27 鏡：空場／抽象轉場，提示詞暫保留（139.767 秒） | `cabin-back`, `airport-window-day`, `vacant-cabin`, `cabin-front-curtain`, `night-clouds`, `forest-unknown`, `arrival-cabin`, `witness-interview-room`, `two-empty-chairs`, `portrait-limit`, `interview-notebook`, `nationwide-leads`, `archive-many-folders`, `comparison-desk`, `search-empty-land`, `survival-question`, `other-money-unknown`, `place-not-route`, `distance-not-drift`, `opinion-evidence-gap`, `tip-wealth`, `retained-evidence`, `study-year`, `diatom-explained`, `bloom-season`, `season-not-arrival`, `prototype-method` | 多張空機艙、空森林、空河岸或文件近景連續出現，容易只換圖、不提供新資訊。要以相鄰三鏡的實速有聲小樣看節奏與觀看任務；`bloom-season` 的單純河景本身不會證明矽藻季節資料，需依旁邊來源卡承載數據。沒有藉空景灌滿插圖配額的驗收資格。 |

## 預檢與下一個小樣

`lint --json` 為 0 errors、0 warnings；全部 62 鏡 `keyframes --dry-run --takes 1` 均未超 MiniMax 提示詞預算，一次圖像加 judge 的估算約 **US$0.84**，未發送付費請求。MiniMax `image-01` 本機設定為 1K 且不接受 style reference；前三輪開場共 9 張各自的失敗與人工觀察見 `visual-pilot-03.md`，不能從 dry-run、原有 judge 總分或這次改字推成美術可用。

現行 `thumbnail.data.shot=boy-bank` 仍指向未核准、要求特定孩童與鈔票的重建鏡；不得用目前失敗或尚未驗證的圖當縮圖。正式縮圖須另選有來源、權利可追溯且人工實看的主體，並在完整畫面審核後定案。

下一輪代表小樣的**離線候選**是主稿第一段連續三鏡 `open-drink` → `open-note` → `open-threat`，未取得站主後續付費生圖指示前不執行。屆時需正常判圖、人工逐張檢查，再用已核准 WAV 對時觀看；它能同時測試風格一致、匿名人物／手部、無字紙條與物件的閱讀順序。若依同一路線再次出現假字、畸形手或擬真漂移，應停在 `needs_revision`，重新設計插圖製作路線或獲准改動場景型別及重新綁核准，不能批次畫完 62 鏡或放寬 50%／8 秒規則。即使三鏡過關，其餘 59 鏡仍須按來源與畫面實看，尤其科學示意鏡。
