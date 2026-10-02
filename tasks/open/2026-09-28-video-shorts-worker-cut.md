---
id: 2026-09-28-video-shorts-worker-cut
title: Video shorts T3: highlights cut from the published tutorials, rewritten for the vertical frame
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-shorts-t3
claimed_at: 2026-10-02T09:05:29Z
created_at: 2026-09-28T03:50:00Z
completed_at:
branch: claude/video-shorts-worker-cut
depends_on:
  - 2026-09-28-video-shorts-worker-lab
scope:
  - tools/video/shorts/cut.mjs
  - tools/video/shorts/cut.test.mjs
  - .agents/skills/youtube-video/references/prompts/shorts-cut.md
  - tools/video/shorts/lab.mjs
  - tools/video/automation/shorts.mjs
  - tools/video/automation/shorts.test.mjs
---

# Video shorts T3: highlights cut from the published tutorials, rewritten for the vertical frame

## Why

站主選的第二條內容線是「長片精華」：每支教學長片切 1–2 支直式短片，把觀眾導回完整影片與文章。長片是 16:9 的投影片、一句可以很長、字幕不燒錄；直接裁成直式會看不到字。所以精華不是剪片，是用同一份查核過的內容重寫成直式字卡，旁白用同一個頻道聲音。

設計全文在 `docs/videos/SHORTS.md`（§三條內容線）。

## Definition of done

- [x] `make` 在題目的 `line` 是 `cut` 時走 `cut.mjs`：輸入是來源長片的 `video.json`（由伺服器在 `shorts/next` 的脈絡裡給，或從工人自己的工作區讀）、它的查核報告、它在 YouTube 上的影片 id。
- [x] 挑段落（`planner`、`variant: shorts-cut`）：一支長片挑 1–2 段，每段有自己的鉤子與結論、不需要前文就聽得懂、估計 25–55 秒；兩段不能講同一件事。
- [x] 改寫（`writer`、`variant: shorts-cut`）：字卡照 Shorts 腳本的限制（標題 36 字、每句 38 字、最多 5 列）；**只能用來源長片裡已經查核過的事實與數字**，不准加新的說法；第一句是鉤子，最後一句把觀眾導回完整影片。
- [x] lint：腳本裡出現的每個數字與拉丁字詞都要在來源長片的稿子裡找得到（沿用 `rewrite.mjs` 比對數字與拉丁字詞的做法）；找不到就是錯誤。
- [x] `source` 記下來源影片的代號、影片 id 與用到的句子 id；說明欄第一行是完整影片的連結，第二行是對應文章的連結（帶 `utm_source=youtube&utm_medium=shorts&utm_campaign=<Shorts 代號>`）。
- [x] 品管的 `evidence` 項：來源影片存在、已公開、沒有被放棄；`links` 項：兩個連結都回 200。
- [x] 句子跟長片一字不差、聲音相同時，旁白快取命中，不重新合成。
- [x] 測試：挑段落的檢查、數字與拉丁字詞的比對、連結的組法、來源不符時的拒絕。

## Steps

- [x] 讀 `tools/video/automation/rewrite.mjs` 與 `tools/video/core/metadata.mjs` 的 `articleUrl`。
- [x] `cut.mjs` 與提示詞。
- [x] 測試。
- [ ] 拿第二批的一支長片（已核准的）在本機試做一支，放進票的 Notes。（只做了不打模型、不打站的離線試做，見 Notes；整支成片等主機部署後第一個精華題目）

## How to verify

```bash
node --test tools/video/shorts/cut.test.mjs
npm run test:tools
```

## Notes

- 「相關影片」（Shorts 連回完整影片的欄位）能不能用 API 寫，要等 `2026-09-28-video-shorts-pilot-launch` 實測；在那之前連結只放說明欄。
- 長片還沒公開時不做它的精華：精華要連得回去。
- 文章頁曾經會把網址的查詢字串（含 UTM）轉址拿掉；組連結之前先確認那個問題修了沒有，沒修就在 Notes 記下並另開票。
- PR #880 的 12 支是同一種內容（六集長片各切兩支），它們用 `import` 進來，不走這裡。

### 2026-10-02 做了什麼（claude-opus-5-5-shorts-t3）

- 認領時被 `2026-09-28-sothatswhy-shorts-from-episode`（claude-opus，scope `tools/video/shorts/`）擋住；派工說明列它是 PR #904/#950/#962 已合併的過期認領，用 `--force` 接手。
- **怎麼接上 T2 的派工**：`shorts.mjs` 的 `MAKES` 加 `cut`；`make` 依 `job.line` 選 `CutShort` 或 `LabShort`（實測線的 `labRefusal` 照舊在 start 之前擋）；`follow` 依 `lab.json` 的 `line` 選類別。`CutShort` 繼承 `LabShort`：成片、聽寫、品管、打包、送審、等站主、重試都共用，`lab.mjs` 只改成讓子類別帶自己的 `line`、步驟順序、後台清單與提示詞（`static line/order/checklist`、`instructions()`），所以 `tellSite` 回報 `shorts_line: "cut"`，伺服器的 policy 照 PR #998 不問「有示範」；工具端送 policy 的內容沒變（測試檢查）。scope 因此加了 `lab.mjs`、`shorts.mjs`、`shorts.test.mjs`（原本斷言「不做 cut」的兩個測試改成用漫劇題目當不做的線，另加一個精華派工測試）。
- **來源從哪裡讀**：伺服器的 make 工作只有 `SourceVideo`（slug、標題、format、YouTube id、公開時間、source_guide），沒有稿子。稿子與查核報告從工人自己的 checkout 讀：`docs/videos/<source>/video.json`、最新一輪 `verify-<n>.md`、`claims.md`；文章從 `apps/api/app/guides/content/<source_guide>.json`。凍結成 `_shorts/<slug>/cut/source.json` 並記雜湊（之後每一步都核對，改了就卡住）。
- **來源不符就卡住，不是跳過**：題目不是 cut、沒有來源、伺服器給的來源不是題目的、不是 slides 教學、沒有 YouTube id、公開時間未到或沒有、工人沒有那支的 video.json、沒有查核報告、video.json 的 slug 不符——都先 start 再以原因 block。理由：`next_job` 會一直回同一個最早的時段，不 start 就每輪都被問、後面的時段全卡；block 之後伺服器跳過它（PR #1120），站主在「需要你」看到原因，公開後按重試即可。
- **挑段落一次給兩個題目**：伺服器每支長片開 `cut-1`、`cut-2` 兩個題目。企劃模型對一支長片只挑一次（`_shorts/_cuts/<source>.json`），每個題目拿下一段還沒人拿的；程式檢查句子 id 存在、照長片順序、兩段不共用句子、重點不同、估計秒數在設定與 25–55 之間。沒有段落可拿的題目以 `dropped` 結案（附原因）。伺服器的 `done` 只收 `making` 的題目，所以要先 start，會留下一支空的 Shorts 在「製作中」——另開票 `2026-10-02-a-highlight-topic-finished-as-dropped`。
- **lint**：每段可見文字（標題、說明、話題標籤、標籤、字卡、旁白）的數字與拉丁字詞用 `rewrite.mjs` 的 `factTokens` 比對長片的旁白、卡片 data 與標題（數字照寫法、字詞不分大小寫）；最後一句旁白要有「長片」或「完整影片／版」。撰稿模型在同一輪拿到問題重寫一次，兩輪都不過算失敗，連兩次卡住。
- **連結**：`source.url` 是 `https://youtu.be/<id>`，`package.mjs` 把它放說明欄第一段；說明欄自己的第一段是 `完整文章：<文章網址>`（`utm_source=youtube&utm_medium=shorts&utm_campaign=<Shorts 代號>`），撰稿模型的字句在後。因為 `composeDescription` 用空行分段，兩行之間隔一個空行；沒去改 `package.mjs`（匯入的 12 支精華也走它）。長片沒有 source_guide 或內容包不在工人那裡時不放文章連結（凍結時的訊息會寫 `no article to link`）。
- **UTM 被轉址拿掉的問題**：PR #786（`9f586971c`，文章頁保留查詢字串，不再 307 到乾淨網址）已修，所以直接帶 UTM。
- **旁白快取**：成片前把長片 `<work base>/<source>/audio/<line id>.wav` 複製進 Shorts 的 `_shorts/.speech-server/<phraseKey>.wav`，條件是那一句跟長片的某一句一字不差，而且長片 `audio/cache.json` 記的 key 等於用 Shorts 的聲音算出的 `[voiceFields(voice), spokenParts(text)]`（也就是同一個聲音、同樣的字）；build 之後就不會為那句合成。聲音或 style 不同、改寫過的句子照常合成。
- **品管**：`qa.mjs` 原本就有 cut 的 evidence（來源存在、已公開或已核准、沒被放棄）與 links（說明欄每個網址 200、完整影片連結要有）；測試確認兩個連結都被檢查、來源被放棄或沒公開時不過。
- **離線試做**（不打模型、不打站、不合成）：用本 repo 的 `ai-agent-vs-chatbot`（142 句、`verify-1.md`、內容包 `ai-agents-explained` 是 life）手挑 ag012–ag015、ag083–ag086 一段，照撰稿規則手寫 5 景 9 句（8 句與長片一字不差、159 字約 40 秒）；`cutProblems` 沒有問題，說明欄是 `完整影片：https://youtu.be/…`、空行、`完整文章：https://mokaair.com/zh-TW/life/ai-agents-explained?utm_source=youtube&utm_medium=shorts&utm_campaign=ai-agent-vs-chatbot-cut-1`。真正的整支成片（企劃、撰稿、查核模型、伺服器旁白、ffmpeg）要等主機部署後第一個精華題目；本機這輪規定不能打真的模型與站。
- 驗證：`node --test tools/video/shorts/*.test.mjs tools/video/automation/*.test.mjs` 全過；`npm run test:tools`、`npm run check:tasks` 結果見 PR。
