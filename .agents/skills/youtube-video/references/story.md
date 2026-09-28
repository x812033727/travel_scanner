# 品牌故事：工人怎麼把一個企劃做成影片

品牌故事是 AI 漫劇底下的一種作品類型（設計在 `docs/videos/STORY.md`）：一支 12–15 分鐘、只有旁白、約 90 張卡通靜態圖加緩慢運鏡、燒錄字幕的非虛構短片，講一個品牌、一件日用品或一個天天在用的標準怎麼來、生意怎麼運作。影片的 `format` 仍是 `drama`，100 個故事是同一部 `kind: "story"` 作品的 100 集。這份寫**工人怎麼做**與人手動接手時看哪裡；實作在 `tools/video/automation/story.mjs`（提示詞在 `tools/video/automation/story-prompts.mjs`），測試在 `tools/video/automation/story.test.mjs`。

## 工人拿到什麼

企劃清單在 `docs/videos/story-plans/brand-stories-100/`，查核過、編譯成 `stories.json`，由站主在主機上匯入（`python -m app.cli video-story-import`）。工人不讀那個檔，從 API 拿：

- `GET /video/automation/series/next` 回 `kind: "episode"`、`series.kind: "story"` 的工作。作品帶 `hands_off: true`、`visual_tier: "stills"`、`target_minutes`（13）、`image_model`、`look`（`style`、`negative`、`motion`，每個故事共用的畫風）。
- 集數帶 `slug`（企劃定好的影片代號，`story-…`）與 `beats`（整份企劃）：`id`、`category`、`region`、`subject`、`question`、六段 `chapters`（`hook`、`origin`、`idea`、`engine`、`turn`、`now`，各一個 `point`）、`takeaway`、`must_verify`（`claim`、`sources`、`core`、`attributed`、`reviewer_only`）、`sources`（`url`、`publisher`、`kind`、`supports`、`checked`）、`caveats`、`names`、`cast`、`image_notes`、`sensitivity`、`related_guide`、`thumbnail`、`publish`。
- `POST …/series/<作品>/episodes/<n>/start` 一定要用企劃的 `slug`，用別的伺服器回 409 `video_series_story_slug`。開始時伺服器會再檢查一次作品是否暫停、每日、同時進行與每月上限（PR #918），不行就回 409 `video_series_story_held`：工人這一輪結束、什麼都不寫，下一輪再問。

## 主幹（一步最多一次模型呼叫）

| # | 步驟 | 模型呼叫（variant） | 產出 | 關卡 |
| --- | --- | --- | --- | --- |
| 1 | 開始：寫 `<VIDEO_DOCS>/series.json`（`kind: "story"`、`names`、`slug`、`episode`、`characters`、`visual_tier: "stills"`、企劃、畫風、圖片模型）與 `brief.md` | 無 | `series.json`、`brief.md` | 大綱在本機核准（備註寫「題目是站主核准過的企劃清單」）；作品沒有共用畫風就卡住 |
| 2 | 撰稿：一章一次，依序六章 | `writer:story` ×6 | `<VIDEO_WORKDIR>/<SLUG>/story/chapters/<章>.json`；第六章寫完合併成 `video.json`、`claims.md`、`script.md` | `lint`：錯誤落在哪一章就退回那一章（同一個 variant，帶 `lint_errors`），每章最多 3 次 |
| 3 | 查核：一章一次，每次新 session | `verifier:story` ×6 | 那一章的句子 patch 與主張表；六章都查完寫 `verify-1.md` | 一章改超過 3 個事實就再查一輪，最多照漫劇設定的查核輪數 |
| 4 | 聽眾審稿：一章一次 | `listener:story` ×6 | 句子 patch（數字、拉丁字詞、字典詞改了的那句不套用） | — |
| 5 | 劇本關卡 | 無 | `script.md` | 故事沒有劇本關卡：在本機核准，備註寫原因（PR #870 起每支漫劇都有這一步） |
| 6 | `look`：只有企劃有 `cast` 時 | 無（設定圖沒過才有 `writer:story-fix`） | `characters/` | 免關卡作品由 judge 自動選 |
| 7 | `tts` → **長度** → `check-audio` | 長度不對時 `writer:story`（帶 `resize`） | `timeline.json` | 量到的旁白要在目標 ±（−1:30、+2:30）之內，13 分鐘就是 11:30–15:30；見下面「長度」 |
| 8 | `keyframes` → 分鏡關卡 | 沒過的鏡頭 `writer:story-fix` | `keyframes/` | 免關卡作品由伺服器依 judge 決定；超過 47 鏡送聯絡表 |
| 9 | `render`、`clips`（全靜態圖：只寫 manifest，不花錢）、`music`、`assemble`、`captions` | 無 | `final.mp4` | 檢查全過 |
| 10 | 成片關卡（`qa`）、`package`、上架確認 | 無 | `upload/` | 自動品管與上傳包檢查；上架確認後回報 `POST …/episodes/<n>/done` |

一支故事正常是 **18 次模型呼叫**（6 撰稿、6 查核、6 聽眾審稿），每一次都帶 variant，所以伺服器不算進每月排程草稿。多出來的只有：lint 退回、查核第二輪、長度修正（每輪 3 次：改寫、查核、審稿）、圖片修正、旁白被 Jev 標記後的改寫（`listener:rewrite`，沿用漫劇的）。故事**不寫前情、不做合集、不送劇本關卡**。

2026-09-28 用真實企劃的形狀量過（A01、A06、B18、T03，替身頁面每頁 60,000 字、數字全在第 40,000 字之後）：最大的一次請求約 71 KB（A06 第二章的撰稿，23 個來源），提示詞不到 8,000 字，一章的回答不到 10,000 字（約 3,000–5,000 token），都在轉送的 295 秒、4 MB 與輸出上限 32,000 之內。

## 長度從哪裡來

數字集中在 `story.mjs` 的 `chapterBudgets`：每分鐘 250 字、鉤子 30 秒內說完、其餘五章照權重分（`engine` 最長），每鏡平均約 8.7 秒。13 分鐘的故事是 3,250 字、89 鏡（鉤子 125 字 3 鏡、起點 625 字 17 鏡、點子 563 字 16 鏡、生意 874 字 24 鏡、轉折 625 字 17 鏡、現在 438 字 12 鏡）；測試守著加總等於目標。

企劃的六段要點合起來只有 800–1,600 字，差的不是撰稿模型要自己編的：來自來源頁面的段落（比企劃說得多）與把事實講清楚。撰稿提示詞明講：企劃以外的內容一定出自給它的段落，查核會去那裡找；段落沒有更多就寫短一點，不塞空話、不寫記憶裡的東西。

**tts 之後量長度**：太長就把最長的一章砍短，太短就把最「瘦」的一章（實際秒數對配額比例最低，鉤子除外）補長，每輪一章、最多兩輪（`LENGTH_FIX_ROUNDS`）。改過的那章重新查核、重新審稿、重新核准劇本、重錄改過的句子，再量一次。兩輪仍不在範圍內就卡住，原因寫量到的長度；要補長時撰稿模型回 `no_more`（段落沒有更多可講），也卡住，交給站主決定（做短一點，或換一個故事）。長度對之前不會請 Jev 聽。

## 查核怎麼做（與漫劇最大的差別）

- **企劃的事實是確立的**：`must_verify` 每一條在匯入前都由第二個人對過來源（`reviews/<代號>.json`）。查核模型確認稿子說的跟企劃一樣，並在頁面段落裡找撰稿模型**自己加的**數字、年份、人名、引述；哪裡都找不到、企劃也沒有的拿掉（NOT FOUND）。
- **`attributed: true`**：旁白要說是誰的說法（「照某某的說法」「據說」），講成定論的句子要改。
- **`reviewer_only: true`**：這條沒有工人讀得到的來源。查核模型不去找，照企劃的寫法核對，數字與年份一個字都不能多；工人也不把這條的來源頁面交給它。
- **`caveats` 是命令**：說不要講的就不講，說各來源不一的數字照它的寫法講。撰稿與查核都拿到。
- **段落，不是頁首**：工人的讀取程式只留前 40,000 字、不讀 PDF 與超過 3 MB 的頁面。故事改用 `pageReader({ whole: true })` 拿整頁文字（其他呼叫者拿到的跟以前一樣），用那一章的數字、年份（含昭和、平成、令和、民國的寫法）、名字、引號裡的詞在整頁裡找，切出前後各 500 字的段落，每頁最多 8,000 字、每次呼叫最多 40,000 字；找不到就給頁首並註明「先換算紀年與單位」。整頁存在 `story/pages/`，同一支影片的十二次呼叫只抓一次（暫時的失敗不存，下一步再抓）。
- **讀不到的來源**（PDF、太大、少於 400 字的頁面）交給模型的是企劃裡那個來源的 `supports`，標明是企劃查核時讀到的、不是這次讀的。
- 查核提示詞要模型先換算昭和、平成、民國紀年與 billion／億，再說找不到。查核過程不進旁白。
- 每章的主張表 id 是章的字母加編號（`h1`、`e12`）；判定是 `CONFIRMED`、`PLAN`、`CHANGED`、`ATTRIBUTED`、`NOT FOUND`。`verify-1.md` 是六章的表加上模型的報告（報告裡的直線換掉，品管的 `facts` 項只讀表），NOT FOUND 的主張不會再被任何場景引用。

## 畫面

- 畫風是作品的 `look`（`preset: "custom"`），每個故事一樣，沒有吉祥物。
- 提示詞、鏡頭、角色外觀不得出現 `names` 裡的任何名字（lint 的故事規則）；撰稿時就先 lint 那一章，名字出現在提示詞裡就退回那一章，任何圖片都還沒畫。圖片修正（`writer:story-fix`）也是先 lint，出現名字的修正不保存。
- 反覆出場的人物（企劃的 `cast`，0–3 個）寫進 `characters`：名稱用 id 的字（拿掉名字），外觀照企劃，聲音用旁白的（沒有人說話，但 lint 要有）。沒有 `cast` 的故事沒有設定圖兩步。
- `image_notes` 與 `sensitivity: "care"` 原樣交給撰稿；`care` 不畫事故本身，畫制度與人怎麼改變。

## 工作區裡多的東西

| 檔案 | 內容 |
| --- | --- |
| `story/chapters/<章>.json` | 那一章的名稱、場景（id 是 `<章>-01`…，最後一章的片尾卡是 `now-outro`）、主張表（含判定與註記）、查核報告、鉤子選的縮圖鏡頭 |
| `story/pages/<雜湊>.json` | 讀過的來源頁面整頁文字，或讀不到的原因 |
| `auto.json` 的 `story` | 每章寫了幾次、lint 錯誤、修了幾次、查核輪數、聽過沒；長度修了幾輪、量到的長度；站主退回旁白的備註 |

## 卡住與站主能做的

| 原因（審核頁清單第一列） | 站主怎麼辦 |
| --- | --- |
| `writer failed 2 times in a row: chapter …` | 看 `answers/` 裡模型說了什麼；按「重試」讓工人再問一次 |
| `chapter … still fails lint after 3 fixes` | 通常是字典少了詞或某鏡太長；人修 `story/chapters/<章>.json` 後重試 |
| `the narration measures …, under/over …` | 做短一點（目前沒有開關，要改程式或手動砍）或放棄這支、換下一個故事 |
| `the story cannot be written: …` | 企劃或作品少了東西（例如作品沒有 `look`）：在後台補上再重試 |
| `the owner sent the narration back … changed nothing` | 退回旁白的備註聽眾審稿做不到（它不改數字與名字）：人改稿或放棄 |

站主在影片頁退回旁白（寫原因）時，工人把備註交給聽眾審稿、一章一次改完，重新核准劇本、重錄、再送旁白。站主在劇本討論串留言，工人回一則說明怎麼改（故事的稿子不從討論串整份重寫），不呼叫模型。

## 手動接手

- `node tools/video/cli.mjs status --slug <SLUG>` 看做到哪；故事的步驟就是漫劇的（沒有 `cast` 時少兩步 look）。
- 撰稿、查核、審稿的提示詞給人讀的版本在 `.agents/skills/youtube-video/references/prompts/`（`writer-story.md`、`verifier-story.md`、`listener-story.md`）；工人實際送出的是 `story-prompts.mjs`，兩邊不一致以程式為準。
- 手動改一章：改 `story/chapters/<章>.json`，下一輪工人合併、lint；改了句子的章要重新查核的話，把 `auto.json` 那一章的 `checked` 設成 `false`。不要直接改 `video.json`：下一次合併會用各章的檔覆蓋它。

## 坑

- 漫劇設定分頁的「各階段常設指示」也會接在故事的提示詞後面（格式是 `drama`），而且寫明「和上面的規則衝突時以它為準」。寫常設指示時要記得故事也會讀到。
- `look.motion` 在 lint 最多 300 字，伺服器允許 400：超過的部分合併時會被截掉。
- 放棄一支故事之外，目前沒有「接受這個長度」或「跳過這個故事」的開關；長度卡住的影片重試也會再卡一次。
