# 共用導聽指示與 Day01 生成順序：獨立補充覆核

覆核日期：2026-10-08。覆核者：`airport_claims_review`，與 generator／逐集稿件作者不同。

**文字及生成順序覆核通過；不構成製作、語音、成片或發布核准。** 本輪補足先前 300 句逐集英文 guides 以外的共用文字。實際欄位名為 `COACH`／`CHAPTERS`，不是 `COMMON`。

## 實際讀過的文字範圍

| 範圍 | 數量 | 語言 | 結果 |
| --- | --- | --- | --- |
| `COACH` 八種導聽指示 | 8 × 5 = 40 | en、zh-TW、zh-CN、ja、ko | 五語意思一致，沒有額外旅運或醫療／安全主張 |
| `CHAPTERS` 七種章名 | 7 × 5 = 35 | 同上 | 與實際聽力階段一致 |
| `description()` 虛構情境說明 | 1 × 5 = 5 | 同上 | 說明數字、公司名與地點為練習例子，實際安排另行確認 |

共 80 段共用文字已逐段閱讀；不把它們併入先前 300 句英文 guides 而重複計數。這是獨立 AI 文字覆核，不是人類母語者實聽。

## 發現並完成的修正

1. 原 `practice` 要求逐一完整「句子」並在固定停頓內說完，但生成器單位是台詞 turn，可含多個句子，而且每段練習停頓固定 4 秒。作者已在五語改成逐段台詞練習，並明確允許需要時暫停影片；`contrast` 同步加入暫停指示。查核者已重讀五語修改。
2. `CHAPTERS.practice` 同步改為台詞逐段練習；日文與韓文不再宣稱每張只有一個完整句子。
3. 韓文章名原本表示「沒有幫助再聽」，與英文固定顯示不一致，已改為 `힌트를 줄여 다시 듣기`（減少提示再聽）。

目前英文練習指示：

> Practice one line at a time. Listen, then repeat. Pause the video if you need more time.

重聽指示只建議關掉「翻譯字幕」，沒有要求關掉固定英文。`natural pace` 仍是待語音實測確認的製作意圖，不能由文字審查保證實際發音自然。

## Day01 的教學目的與時長

- `brief.md` 的鉤子是 Zone B／C 聽辨，目標是詢問報到地點並確認區域、櫃檯與方向；兩段對話及三題測驗吻合此目標。
- 重播各有目的：先理解、連結問答、開口跟讀、辨識第二情境變化、測驗、減少翻譯提示重聽。這是使用者要求的聽力練習，不以單純重複次數宣稱足夠教學品質。
- 以修訂後 adapter 執行 `prepareLesson()`，並將預期位元組與最新落地檔案比對，新 Day01 為 95 個條目；正文文字估算 545.6 秒，練習／作答固定停頓合計 68 秒。
- 600 秒是成片目標，包含品牌素材；`measured_body_seconds`、`branding_seconds`、`measured_total_seconds` 都是 `null`，`release_ready` 是 `false`。
- 尚未量到旁白與正式品牌素材長度，不能據此稱影片已經 10 分鐘。實際合成後必須重新計算；不足時補有目的的教學內容，不用任意靜音、慢播或無目的重播補時。
- 4 秒是練習提示的預留空間，現在的指示明確允許學習者按暫停完成較長台詞，沒有保證所有人都能在 4 秒說完。

## Day01 測驗來源與順序

已人工核對來源文字與答案，再以生成結果檢查每題順序：題目 → 三個選項 → 完整證據對話 → 作答提示／停頓 → 解答。沒有把舊版的字詞重疊猜測邏輯帶入。

| 題目 | 證據 ID | 所聽到的關鍵語境 | 答案 |
| --- | --- | --- | --- |
| Q1 區域 | B01、B02 | 詢問 Maple Airlines 報到區，回覆 Zone D 並以 Delta 確認字母 | B：Zone D |
| Q2 櫃檯 | B03、B04、B05、B06 | 先說 30–34，再完整播放 13／30 的更正與 three zero | C：30–34 |
| Q3 經過藥局後 | B07、B08 | 詢問路線，回答經過藥局後右轉；樓梯旁並非上樓 | A：Turn right |

三組 `evidence_ids` 都對應明確台詞，重播引用同一份英文 source take；以上是生成稿／引用關係驗證，尚未代表真正音檔已聽到正確句子。

四個 `teaching-audio` 路由也已核對：所有 dialogue 仍使用英文文字與 `speech_locale: en`，所有教學／題目／解答則使用選定語言；各語 CC 保留翻譯文字。這證明來源路由符合要求，不表示多語音軌已合成或已在 YouTube 啟用。

## 雜湊與整合紀錄

既有 `claims-review.json` 的歷史全文 SHA-256 原樣保留。本輪重新計算確認 **60／60 的 `reviewed_english_content_sha256` 相同**，但 metadata 整合後 **60／60 的全文 SHA-256 都不同**；不可描述成全文 hash 一致。

root 的整合紀錄是新增非口播來源、claims、縮圖標題與狀態欄位；本覆核實際確認的是先前已審的英文內容沒有改變。新的共用 COACH 修訂不在 lesson JSON 內，以上另行覆核。

adapter 已完成 fresh prepare。本查核者重新生成 Day01 預期內容並逐一比對以下 **12 個落地檔案**，位元組全部相同；同時重新閱讀 brief、三題引用順序與解答，確認以上結論對應實際磁碟新版本。沒有合成、送審或核准。

| 新 Day01 落地檔案 | SHA-256 |
| --- | --- |
| video.json | `b8d6971b1be453d460802c35e6b40f7ed9dbabee80af887cfe1e79cb92921c76` |
| brief.md | `28042307899f92e198f9dcfdc7f262b4d6b3c89e341ff72359e8d7cfe2872847` |
| claims.md | `8e4fb3445ed06b78950e141fa6877191380a3124fcd1c0c9a7664c25d4a52d2b` |
| teaching-audio.json | `83c76410767f59c6df1de551f83ed389e14980aa6a98a4f3ab24d1696f94a3fc` |
| duration-plan.json | `da1249c073f13c212b54a707d0e34b0a468f75f6341d3a0df4ac90a2453e4a04` |
| caption-plan.json | `dc80c6b38a53add5c1741e48af2dd531a567679fdaf0be6378b244ca67014d93` |
| metadata-plan.json | `077f6b69c0d09c559d4e890abe8db9adf71535d5227cace07cef0bdcd4207c81` |
| line-map.json | `47530c5f401b8c6dc322cf222606fdc812a8d851af783b012a5c41cf9007b6e7` |
| i18n/zh-TW.json | `47ba6c8f5fed22891bcdadcec4a440d259be567990815f9fdab67c9a2504450c` |
| i18n/zh-CN.json | `16a99d381a96df49ad75dfc4e89155e4cec627c377e404729aab92663b1ce113` |
| i18n/ja.json | `caff83ddb47717ac49f62ce2e7721ce362548ac8bd2d6509ee0e58033bd15fe7` |
| i18n/ko.json | `bb994220895a04ce804ad4cc109324df4c1edfa1539d645349704b688f7b38f6` |

已閱讀 60 個英文縮圖短標題，均是當集主題標籤而非新政策保證；Day12 使用 `Docs Ready`，Day46 使用 `Next Flight`。此處確認文字意義，未以此宣稱縮圖視覺測試。60 集的共用指示、章名與說明文字產生相同語義雜湊。

## 機器可讀的文字覆核紀錄

下列紀錄只綁定本查核者實際閱讀的共用文字與主題短標題。`existing_editorial_report` 另記錄已存在的 Day02–21 獨立 PASS 報告全文雜湊、原審稿者及原結論：原審稿者已離開本輪，不冒用其身分補簽，也不聲稱本查核者重新完成其語言審查。該報告任何位元組變更都須重新確認，不能沿用歷史 PASS；其他審稿者的明確 marker 決定是其目前機器可讀狀態，撤回或取代時須同步更新該 decision。所有紀錄都不屬於製作核准。

<!-- airport-shared-review-v1 {"schema_version":1,"decision":"text_review_passed","reviewer":"airport_claims_review","shared_instructions_sha256":"ef3bfaca98c258e4cae1c5b0ada1a217e984742b2ddd792c7fa7b80f22ad101f","thumbnail_headlines":{"1":"Right Counter","2":"Which Level","3":"Start Here","4":"Booking Found","5":"Right Flight","6":"Window Please","7":"Together Please","8":"Bag Drop","9":"Extra Weight","10":"Boarding Details","11":"Security Ahead","12":"Docs Ready","13":"Tray Check","14":"Liquid Check","15":"Extra Screening","16":"Follow Along","17":"Gate Located","18":"Time Check","19":"Find Facilities","20":"Quick Bite","21":"Boarding Now","22":"Your Group","23":"Need Assistance","24":"New Gate","25":"Delay Update","26":"Last Call","27":"Name Called","28":"Bag Recheck","29":"Scan Again","30":"Seat Located","31":"Buckle Up","32":"Devices Away","33":"Seat Trouble","34":"Meal Choice","35":"Drink Please","36":"Allergy Alert","37":"Comfort Please","38":"Where Next","39":"Feeling Unwell","40":"Stay Seated","41":"Transfer Help","42":"Next Flight","43":"Collect Bags","44":"Screening Again","45":"Will I?","46":"Next Flight","47":"Visit Purpose","48":"Stay Details","49":"Onward Plans","50":"Please Repeat","51":"Belt Found","52":"Bag Missing","53":"Describe It","54":"Damage Report","55":"Delivery Details","56":"Declare What","57":"Ride Ready","58":"Flight Cancelled","59":"Departure Challenge","60":"Arrival Challenge"},"existing_editorial_report":{"path":"verify-02-21.md","recorded_by":"airport_claims_review","original_reviewer":"airport_lessons_42_60","recorded_decision":"text_review_passed","report_sha256":"aa02a3dacbbbf14e781898486862aae0e19878831c6e8dab7d13a0271f0bbc6b"}} -->

## 範圍限制

這份補充覆核不包含任何新旅行事實；已查核的旅運來源仍以 [claims-review.md](claims-review.md)／[claims-review.json](claims-review.json) 為準。發音、自然語速、對話聲線辨識、CC 實際時序、畫面字級、品牌、響度、600 秒實測、11 項成片 QA 與 4 項上傳包 QA 都不能由本次文字／順序結果代替。
