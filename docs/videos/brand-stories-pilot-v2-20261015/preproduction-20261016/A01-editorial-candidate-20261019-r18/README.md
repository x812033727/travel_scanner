# A01 輪子行李箱 r18：通路措辭與安檢鉤子校正候選 — HOLD

這是從已釘選 r17 離線稿衍生的**另一份候選**。建置器先驗證 r17 全部輸出，以及修正後的 25 筆來源企劃包，再只建立此資料夾的輸出。r17 與更早候選、正式機、媒體及付費素材均不改動；舊審查不自動核准 r18。

## 兩處台詞與一筆主張

- 第 56 鏡 `now-1993-retail/r3n03` 改為：「1993 年，記者寫道：主要百貨或行李專門店，已有四家品牌的輪子登機箱可選。」[Judi Dash 當年的實測報導](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html)說受測的四家品牌型號可在主要百貨**或**行李專門店選購，並未保證四家在每一家百貨同時上架。`n56` 主張同步限縮到原文的「或」與四家受測品牌；前一句 Travelpro 初期郵購仍沿用同篇來源。此段只證 1993 年可買到，不推算銷量或普及率。
- 第 43 鏡 `turn-security-question/r6t01` 改為：「如果把兩樣東西鎖在一起，安檢員會怎麼回答？」第 48 鏡仍只回「好。」[Plath 受訪引述](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)沒有給出可獨立核對的通關結果；旁白和畫面都不補通關情節。

開場到 1939 年輪箱、百貨試拉、Plath 車庫實驗和 1993 年可選購的鉤子 setup／payoff ID 不變。65 鏡、77 句、73 筆仍為 `PENDING` 的主張、18 個公開引用來源、畫風、圖片提示詞與相機動作也不變。來源映射以新的 `n56` 文字重算，URL 和企劃／公開索引不變。

## 三種來源集合

| 集合 | 筆數 | 狀態 |
| --- | ---: | --- |
| 此候選 `candidate/series.json` 的編輯企劃來源 | **23** | 沿用 r17，未新增來源。 |
| 另包 `A01-r16-source-plan-25-candidate-20261019/candidate/series.json` 的**擬採用**企劃來源 | **25** | 本建置器只讀並驗證；未裝入此候選，也未寫入正式機。 |
| 此候選 `candidate/video.json.sources` 的公開引用 | **18** | 與 73 筆主張的 URL 對齊；不得把 25 筆內部來源直接公開。 |

## 使用界線

離線 `validation.json` 的秒數只由文字代理估算，沒有實際 TTS、剪輯或盲聽。正式機仍須核對 104→新版本、六章、重新編號的主張、verifier、listener、兩名獨立敘事讀者、正式 `story/reviews/script-review.json`、圖片聯絡表和 US$25 帳本。此候選保持 **HOLD**，不授權主機寫入、解除 STOP、付費呼叫、合成或上傳。

在儲存庫根目錄執行：

```bash
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-editorial-candidate-20261019-r18/build.mjs --check
```
