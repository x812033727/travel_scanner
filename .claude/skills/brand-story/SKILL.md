---
name: brand-story
description: 品牌故事（kind story 的非虛構旁白長片，參考頻道黑猫研究院）的做法與經驗：站主定下不能改的事（MiniMax image-01 加 cute-mystery、約 10 分鐘、每 30–45 秒一個鉤子、縮圖大字品牌名、不抄參考頻道）、一批故事怎麼從選題做到可匯入（Treatment、獨立撰寫、另一個代理逐來源查核、build.mjs、唯讀試跑匯入）、主機產線卡住時怎麼處理（盲評兩位讀者、念法審查交給另一個代理、重試不重置故事計數、部署前 drain）、查核的教訓。要企劃、改編、匯入、推進、修或重做任何一支品牌故事（story- 開頭的 slug，含 brand-stories 各批），先讀這個 skill，再讀 youtube-video 的 story.md。Plan, adapt, import and push brand-story episodes through the host worker the way the owner approved.
metadata:
  short-description: 品牌故事：站主定案、一批怎麼做、產線卡住怎麼辦
---

# 品牌故事（brand-story）

品牌故事講一個品牌、一件日用品或一個天天在用的標準背後的生意：一個反常的問題、一條因果主線、
可愛插圖加說書旁白，約 10 分鐘。影片是漫劇格式（`format: drama`），每一批故事是一部
`kind: "story"` 作品的各集，由主機工人逐章撰稿、查核、審稿後照漫劇的步驟做到「可以上架」。

這份 skill 是**怎麼把它做好**：站主的定案、一批的做法、產線上踩過的坑。工人每一步怎麼跑、
卡住的原因字串與手動接手，在 `.agents/skills/youtube-video/references/story.md`，不在這裡重寫。

## 先讀

1. `.agents/skills/youtube-video/references/story.md`：工人的主幹、長度、查核、畫面、卡住時站主怎麼辦。
2. 最新一批的企劃包當範本：`docs/videos/brand-stories-adapt-20261017/README.md`（改編參考頻道熱門前五，
   2026-10-17）；前一批 `docs/videos/brand-stories-five-20261014/README.md` 有整集時間軸與製作前檢查。
3. 稿子的規則：`.agents/skills/youtube-video/references/script-writing.md` §故事主線與鉤子。
4. 為什麼這樣設計：`docs/videos/STORY.md`（頁首的 2026-10-15 決定蓋過頁內的 Gemini／13 分鐘舊規格）。

## 站主定案（改任何一條都要先問站主）

| 項目 | 定案 | 來源 |
| --- | --- | --- |
| 參考頻道 | 黑猫研究院（`@qiqiqushi0`）。**只學類型，不抄內容**：題目可以借，故事、來源、查核、標題、縮圖全部自己做；不讀它的逐字稿 | 站主 2026-09-28、2026-10-17；YouTube 非原創內容政策 |
| 畫面 | MiniMax `image-01`，`look: {"preset": "cute-mystery"}` 一字不加（不寫 `style`、`negative`）；插圖寫法照 `.agents/skills/curio-episode/SKILL.md` §插圖提示詞怎麼寫 | 站主 2026-10-15 |
| 長度 | 約 10 分鐘，旁白正文至少 8 分鐘；來源不夠就做短，不灌水 | 站主 2026-10-15 |
| 鉤子 | 正文**每 30–45 秒**（約 130–200 字）至少一個懸念、反轉或揭露，沒有超過 45 秒的空檔；每章停在一個未解的問題上；`loops` 十分鐘至少 8 個。lint 對品牌故事與奇聞檔案局照這個數字警告（`tools/video/core/narrative.mjs` 的 `TIGHT_CADENCE`） | 站主 2026-10-18「講故事也要放鉤子，不然會很無聊看不下去」；`tools/video/automation/story-prompts.mjs` |
| 開場 | 第一秒就在一個具體場景，30–60 秒講到第一個說不通的地方就停，最後一句是這支要回答的問題；不打招呼、不念目錄 | `script-writing.md` §開場濃縮 |
| 片頭片尾 | 頻道 5 秒片頭放在開場濃縮之後；21 秒 v4 片尾；旁白不講下一支是什麼 | `docs/videos/BRANDING.md` |
| 結尾三句 | 回答開場的問題、一個跟故事相連的留言題、一個有理由的訂閱邀請 | 2026-10-14 五集包 |
| 字幕與語言 | 不燒字幕；繁中 CC 一定有；英／日／韓配音由站主在成片後手動勾，不自動選 | 站主 2026-10-15 |
| 縮圖 | 企劃的 `thumbnail.brand`：左上用大字橘色寫公司名（SEIKO、米其林、A4 紙），不放商標圖、不讓 AI 畫 logo | 站主 2026-10-18「縮圖要一眼看出是哪家公司」 |
| 圖裡不能有 | 商標、可讀的字、真人長相、版權角色（連剪影與招牌道具都不行）；品牌名、產品名、真人名（企劃的 `names`）不得出現在提示詞，lint 擋 | `docs/videos/STORY.md` §圖像規則 |
| 吉祥物 | 不要 | 站主 2026-09-28 |
| 預算 | 一支整片上限 US$25；付費生成前把整批張數與總額一次報給站主、一次核准 | 2026-10-15 試作包 |

## 一批故事怎麼做（照 2026-10-17 改編五集的做法）

1. **選題**。題材公式是「人人看過的名字＋一個反常的問題＋誰在收錢」。改編參考頻道時讀它的「熱門」排序
   （頻道影片頁的「熱門」chip；內建瀏覽器拿得到標題與觀看數，拿不到逐字稿），記下名次、觀看、長度。
   一般選題從 `docs/videos/story-plans/brand-stories-100/` 的題庫挑，避開參考頻道做過的題目。
2. **每一集一份 Treatment**（`<ID>-<題目>.md`）：對照參考影片、觀眾與包裝（標題三案、縮圖假設）、
   **一條主線**、開場濃縮的旁白草稿、六章預算，以及**一個參考影片沒有、有一手來源的轉折**——
   這是我們贏的地方（例如 Seiko 那集：瑞士其實先做出石英錶、壓垮瑞士的主因是瑞郎大漲）。
   參考影片講錯或講過頭的說法要被查核修正或改成有歸屬的說法，寫進 README 的「我們贏在哪」。
3. **匯入列**：`episodes/<ID>.json`（六章 `beats`：`hook`、`origin`、`idea`、`engine`、`turn`、`now`；
   `must_verify`、`sources`、`caveats`、`names`、`cast`、`image_notes`、`sensitivity`、`thumbnail`、`publish`）。
   欄位意思在 `docs/videos/STORY.md` §企劃清單與集數列。
4. **獨立查核**：每一集交給**另一個代理**逐來源對過 `must_verify`，寫 `episodes/reviews/<ID>.json`，綁故事
   內容的雜湊——故事改一個字就要重查。查核的人留下的 `notes`（最多 800 字）會變成撰稿模型讀的 `caveats`。
5. **編譯**：`node docs/videos/brand-stories-adapt-20261017/build.mjs`（新的一批複製這支並改路徑；
   `--draft` 在查核前只檢查結構）產生 `stories.json`，不手改。
6. **匯入正式站**（要站主同意）：主機上先唯讀試跑
   `python -m app.cli video-story-import --series <作品> --limit 1 < stories.json`，確認只建第一列、沒有 slug
   衝突，再以**完全相同的參數**加 `--apply`。同一個 id 再匯入只更新還沒開始的列。
7. **工人做完之後**：成片站主核准 → 語言（站主勾）→ 重新打包 → 站主上傳。打包之後才改的東西
   （例如新縮圖）要等語言做完、重新 `package` 才會進上傳包。

每一集的工人產出（逐字稿）仍要逐章查核、聽眾審稿與說故事盲評；企劃的查核只核准企劃裡的事實。

## 主機產線卡住時

工人的卡住原因與手動接手在 `story.md` §卡住與站主能做的。下面是 2026-10-17／18 推五集時量到的、
那份文件沒寫的事：

- **說故事盲評問兩位讀者**（`verifier:narrative`，`tools/video/core/narrative.mjs`）：一位讀者會隨機改判，
  B25 只有一位讀者時手修了七輪才過，所以改成兩位都答「否」才算沒過。重評時每次都是新讀者，鬆緊差一兩題，
  不要為了一位讀者的「否」一直改稿。
- **聽眾審稿會照舊的盲評意見加假的回呼**：退回的 `owner_note` 寫「第三章要回收開場」時，它可能硬塞一句
  不存在的回呼。重評前讀一次改過的那幾句。
- **念法建議交給另一個代理審**：撰稿模型提的外語念法在 `<VIDEO_WORKDIR>/<SLUG>/story/lexicon-proposals/`，
  用 `node tools/video/cli.mjs story-lexicon-revise --slug <SLUG> --review <收據> --apply` 發布。收據宣稱是
  `independent`，所以**推進產線的那個對話不能自己填**（自動模式會以自我核准擋下）；開一個子代理，給它
  slug、目前的 `lexicon_sha256`、proposal 的 sha 與原則「台灣一般念法、同一集同類詞念法一致」，由它審、
  寫收據、乾跑、`--apply`，reviewer 名字要跟主對話不同；主對話之後只按重試。
- **後台「重試」不重置故事專用的計數**（`auto.json` 的 `story`：每章寫了幾次、修了幾次）。計數滿了的章，
  按重試還是卡；要人改那一章或把計數歸零。
- **重試可以在主機的 api 容器呼叫**：`retry_project`（`apps/api/app/video_reviews/admin_service.py`），
  稽核紀錄會記在傳進去的管理員名下，回報時講清楚是誰按的。
- **部署前先 drain 工人**：撰稿工作一支接一支，等不到空檔。在工作區根目錄放 `STOP` 檔，等手上那一步
  做完再部署，部署後刪掉 `STOP`。提示詞的 digest 改了，正在做的那一階段會再付一次。
- **同時進行的集數**：推一批時可以把全站 `drama.series_max_in_flight` 從 1 調到 2，**那一批做完要改回 1**，
  並在票上寫明誰改的、何時要改回。

## 查核的教訓

- 流傳的商業故事**幾乎每一個都有錯**：年份、數字、「誰先做的」。撰稿代理可以用 sonnet，查核用 opus；
  機械性的補來源 sonnet 就夠。
- 官方頁面常用昭和、平成、民國紀年，外文寫 billion、企劃寫億：先換算再說找不到。
- 對 Node 的 fetch 回 403 但瀏覽器讀得到的站，改列 Wayback Machine 存檔（存檔算原發行者的頁面）。
- **移除來源前先確認靠它的說法還有沒有別的來源**；有一輪把 10 MB 的報告當死連結移除，連帶讓一句因果
  說法失去唯一的來源。
- 工人讀不到 PDF、超過 3 MB 的頁面、一頁只留前 40,000 字；每個必查事實至少要有一頁工人讀得到，
  真的沒有就標 `reviewer_only`。`node tools/video/story-plans/validate.mjs` 驗企劃結構與查核綁定。
- 查核過程不進旁白（不說「經查證」）；傳說可以講，但要說它是傳說。

## 交接

做到一半要停：把狀態寫進看板的票（哪幾集在哪一關、卡在哪一句、花了多少、主機上改過哪些設定還沒改回），
不要只寫在對話或 PR 描述。下一個接手的模型（Claude 或 Codex）讀的是票、這份 skill 和 `story.md`。
