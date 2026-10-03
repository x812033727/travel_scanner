# 系統一模型這一集：站主要決定的事與研究紀錄

這份不放進 `brief.md`：大綱關卡會把整份 brief 交給 Jev 判斷，合約與分工的討論不該讓它讀。企劃日 2026-10-03，企劃票 `2026-10-03-ai-terms-episode-system-one-plan`。

## 為什麼是這個名詞

站主要的是 TypeSafe 的發表文〈Introducing System One Models & Jev〉（https://typesafe.ai/blog/introducing-system-one-models-and-jev ，2026-09-15）。系列一集講一個名詞、不講產品，所以這集講文章提出的類別名「系統一模型」，Jev 只當第一個例子。

- 這是廠商創的詞，有前例：系列裡的 Agent Skills 也是。規則是講清楚「這是誰的說法」。
- 至少三家用同一個概念：Cloudflare、Liquid AI 叫「決策模型」，Together 叫「類似 Jev 的分類器」；Hugging Face 上也有開放權重的模型自稱 "System 1 decision model"。
- 上一輪先做了「校準（Calibration）」的企劃，那是誤讀了要求。它仍是一個合理的名詞，要不要做由站主決定（見下面第 2 項），它的兩張票已設成 `blocked`。

## 站主要決定的事

1. **跟 P1 試片票 `2026-09-29-video-pilot-jev-decision-model` 怎麼分工**。那張票做的是同一篇發表文的獨立說書影片，題目「爆紅的 Jev 不聊天只做決定：快 200 倍、便宜 400 倍是真的嗎？」，要查核價格、193.6×／444.6×、RLCD、創辦人。這些正是本系列不講的東西。三個選擇：
   - **併入（建議）**：這集取代那支產品片，試片票改寫或結案。同一家廠商的片只剩一支，最不像業配；代價是失去跟參考片 `2mtn-Qp59y4` 逐點同題的比較。
   - 分題：這集只講名詞，試片改查「數字是真的嗎」。三支片圍著站上付費使用的同一家廠商，最像業配。
   - 只做試片：不出這集，違反這次的要求。
   這個 session 不能改那張票（只能寫自己認領的票），而且它的依賴已經完成，`npm run tasks -- next` 現在就可能把它發出去，所以要盡快決定。
2. **校準那一集**：`docs/videos/ai-term-calibration/` 的企劃與兩張票（`2026-10-03-ai-term-calibration-article`、`2026-10-03-ai-term-calibration-video`）要保留成另一集，還是放棄。保留就把兩張票改回 `open`；這集不再口頭指向它。
3. **公開客戶關係**。TypeSafe 的客戶合約（https://typesafe.ai/legal/mca ，頁面註明 Last updated Sep 23, 2026，2026-10-03 開過）§16.4 原文："Nothing in this Agreement grants either Party the right to use the name, brand, or logo of the other Party, and neither Party may publicly announce that the Parties have entered into the Agreement, except with the other Party’s prior consent or as required by Laws; provided, however, that TypeSafe may use the name, brand, or logo of Customer … on TypeSafe’s website or in other promotional materials …"。§16.5 規定同意要書面。以下只是條文字面，不是法律意見：
   - 不需要同意：講 TypeSafe 公開的名詞與產品、引用時掛名；說這支影片不是業配、TypeSafe 沒有付錢也沒有參與。
   - 字面上需要事先書面同意：說出或露出 Mokaair 是 TypeSafe 的付費客戶、站上的新聞和旁白檢查用它，包括第 4 章的實跑和第 5 章的生產紀錄。
   - 拿不到同意時，第 4 章實跑和第 5 章要拿掉，示範要重新規劃（候選：本機跑開放權重的同類模型，或讓站上的生成式模型限定只回一個選項；都還沒驗證）。不建議改成匿名說「我們站上用的一個判斷模型」：這集講的就是 TypeSafe 的名詞，匿名會誤導觀眾。repo 的 `README.md` 已公開寫明站上使用 Jev，這點也要一起考慮。
   - 若帳號接受的是 2026-09-23 以前的版本，舊版可能仍有效到通知後約 60 天（§16.7），要確認 §16.4 與 §14.1 在帳號接受的版本裡寫法相同。
4. **機密資訊條款**。同一份合約 §14.1 把 "Customer’s Fees and all pricing information"、"Documentation" 列為 TypeSafe 的機密資訊，而且寫明不受「已公開」例外的限制。片中不放帳單、額度、用量金額、主控台畫面；引用公開文件與這條字面上的緊張關係，由站主或顧問判斷。另外 typesafe.ai 的使用條款（§3(b)(ii)、§4）限制公開展示網站內容，所以 brief 已經規定不截文件頁面的畫面。
5. **付費宣傳**。書面確認三件事：帳號從沒拿過 Promotional Credits（合約 §8.2(b)）、沒有綁在報導上的提早體驗或優惠、TypeSafe 沒有參與或影響內容。三項都成立，Studio「含付費宣傳」勾否、說明欄放一句揭露；任何一項不成立就要勾。產線沒有這個欄位，是 Studio 的手動步驟。
6. **大綱與品管由誰判**。這支講的就是 Jev，又讓 Jev 挑大綱、判成片的「像不像業配」，是自己判自己。後台的「由 Jev 挑大綱」與成片自動核准都是全域開關，這支發起前要暫時關掉，或由站主手動核准兩個關卡。另外 TypeSafe 的 API 會收到這支的 brief、旁白全文和每一句旁白，所以揭露句不能說 TypeSafe「沒看過稿子」，只能說沒有參與、審閱或影響。
7. **寫稿當天的金鑰**。後台卡片上的金鑰是加密存放的，腳本只讀環境變數，要由站主從 TypeSafe 主控台另外提供，共 4 次呼叫。
8. **第 5 章說到哪裡**。照實說會公開三件事：新聞發布關卡讓它直接判斷中文、發布門檻是手動調的、旁白零標記就自動核准。要照實說，還是先改程式再播。
9. **頻道立場的條號**。repo 寫立場還是空白，但 2026-10-02 Jev 已經用立場挑過一支的大綱（`docs/videos/sothatswhy-t27/production-record.md:11`），所以後台應該存了立場，條號未知。寫稿當天看後台：條號對得上就把站主觀點第一行改成 `套用立場：N、M`；系列提案第 8、9 條要不要存進去也一起決定。
10. **先寫文章**。票 `2026-10-03-ai-term-system-one-model-article`；也要決定這篇要不要進 `docs/ai-terms-series/catalogue.json` 和總索引。
11. **名詞庫那一列**：category 用 `foundation` 還是 `training`；tier 2 要不要插隊；跟校準那一列的先後。
12. **標題**：建議「系統一模型（System One Model）是什麼？它只從你列的選項裡挑，也會挑錯｜AI 名詞十分鐘」。
13. **上架檔期**：不跟任何 TypeSafe 相關的片相鄰。

## 名詞庫的一列（製作票加進 `terms.json`）

```json
{
  "id": "system-one-model",
  "video_slug": "ai-term-system-one-model",
  "source_guide": "ai-term-system-one-model",
  "article_url": "https://mokaair.com/zh-TW/life/ai-term-system-one-model",
  "article_title": "系統一模型（System One Model）是什麼：只交選項和機率的 AI",
  "zh": "系統一模型",
  "en": "System One Model",
  "short": "系統一模型",
  "aliases": ["System One", "決策模型", "System 1", "System One Models", "decision model", "快思慢想"],
  "category": "foundation",
  "playlist": "foundations",
  "tier": 2,
  "suggested_order": null,
  "hook": "它一個字都不寫，只從你列的選項裡挑一個、附上機率：答案一定在清單裡，不代表是對的。",
  "related": ["reasoning-model", "small-language-model", "llm-as-a-judge", "large-language-model", "hallucination"],
  "existing_videos": [],
  "status": "planned",
  "video_id": null,
  "published_at": null,
  "notes": "TypeSafe 2026-09-15 發表文提出的類別名；旁白不講產品名、價格、速度倍數。分工與揭露見 docs/videos/ai-term-system-one-model/notes.md。"
}
```

`article_title` 是暫定。加這一列要一起改 `counts`、`tools/video/long-form/plans.mjs` 的 `CATALOG_COUNTS`（81）、重建 `docs/videos/long-form/plans.json`，後台目錄也綁著總數。`docs/videos/ai-terms` 與 `docs/videos/lexicon.json` 目前被別的進行中或審查中的票占著，製作票要等它們放開。

## 研究沒能確認的事

- 2026-09-15 之前有沒有人把 "System One model" 當成模型類別名稱用過：搜尋不到五次，不能說是「那天發明的」。
- Jev 的大小與架構沒有公開，RLCD 沒有論文或資料集。
- 「校準過」：沒有找到公開的校準量測。TypeSafe 的 workflow evals 量的是跟兩個大型模型平均答案的一致率，不是校準。
- 「不會幻覺」「沒有型別錯誤」：TypeSafe 自己寫 "Our number is not empirical."。
- 中文準度：TypeSafe 沒有公布；站上也還沒量（`jev-review` 的真金鑰量測沒做，影子測量第一份報告是 `runs_with_shadow_rows: 0`）。
- 後台現值：新聞發布門檻是否仍為 0.55、旁白自動核准是否開著。
- 帳號有沒有拿過 Promotional Credits，TypeSafe 會不會同意公開客戶關係。

## 研究中發現、已開票的問題

- `2026-10-03-jev-comments-drifted-from-vendor-docs`：`jev.py` 說選項上限是我們自訂、TypeSafe 沒有 models 端點，兩句都過時；分級函式把是非題機率和選擇題信心值比同一個門檻；`docs/news-automation.md` 兩處過時。
- `2026-10-03-jev-noul-criteria-keys-yes-no`：是非題的說明欄位 TypeSafe 文件規定 `true`／`false`，站上三處送 `yes`／`no`，效果未知。
- `2026-10-03-narration-homophone-misses-ni-variant`：旁白同音字規則漏掉「妳／你」。
- 校準企劃 `docs/videos/ai-term-calibration/brief.md` 有三句對站上做法的描述是錯的，已在本次一起改正。
