# 審查並套用品牌故事的發音建議

[`story-lexicon-integration.md`](story-lexicon-integration.md) 讓每個品牌故事在第一章之前釘選一份不可變的發音字典。之後撰稿模型在某章寫出字典裡沒有的外語詞時，工人不會偷偷改字典：

- 這章照樣存下來；
- 撰稿模型給的念法存成不可變的建議檔 `<工作區>/<slug>/story/lexicon-proposals/<sha256>.json`（`{schema_version, slug, before_sha256, additions, next}`，檔名是內容的 SHA-256）；
- 這個詞記進 `auto.json` 的 `story.lexicon_pending`，影片卡住，後台顯示「pronunciation proposals saved for reviewed revision」或「story lexicon proposals need a reviewed revision: …」。

要讓故事繼續，得由人（或獨立的審查代理）看過這些詞，發布一個「審查過」的新字典版本。`tools/video/core/lexicon-revision.mjs` 與 `story-lexicon-revise` 子指令就是做這件事的；它最後呼叫 `lexicon-store.mjs` 的 `reviseStoryLexicon`，交易（兩個 LEASE、意圖檔、不可變檔、current 指標、回讀、收據）完全沿用那邊。

## 指令

```bash
# 1. 列出建議，印出審查收據範本（不寫任何檔）
node tools/video/cli.mjs story-lexicon-revise --slug <slug> [--workdir <base>] [--proposal <sha>]... [--json]

# 2. 檢查填好的收據（乾跑，不寫任何檔）
node tools/video/cli.mjs story-lexicon-revise --slug <slug> [--workdir <base>] --review receipt.json

# 3. 發布
node tools/video/cli.mjs story-lexicon-revise --slug <slug> [--workdir <base>] --review receipt.json --apply
```

結束碼：0 成功（列出、乾跑通過、已發布、或這張收據早就發布過）；1 被拒（印出錯誤碼與原因）；2 用法錯誤。

列出時每份建議有一個狀態：

| 狀態 | 意思 |
| --- | --- |
| `current` | 針對目前釘選的字典做的，還有詞沒進字典：會出現在範本裡 |
| `applied` | 它的詞全都已在字典裡 |
| `stale` | 針對舊版字典做的，還有詞沒進字典（例如被 reject 的詞）：不能用來發布 |
| `invalid` | 檔名不是內容的 SHA-256、不是這集的、欄位不對，或 `next` 不是「目前字典＋這些詞」 |

`--proposal` 可重複，只把指定的建議放進範本。同一版字典上累積的多份建議（好幾章各寫出新詞）可以在一張收據裡一起審。

## 審查收據

範本長這樣（`decision`、`reviewer`、`reviewed_at`、`independent` 要人填）：

```json
{
  "schema_version": 1,
  "kind": "story_lexicon_revision_review",
  "slug": "story-adapt-michelin-guide-stars",
  "lexicon_sha256": "<目前釘選字典的 SHA-256>",
  "proposals": ["<建議檔的 SHA-256>"],
  "decisions": {
    "Paul": { "proposed": null, "decision": "accept" },
    "Bocuse": { "proposed": "博古斯", "decision": "accept_as", "spoken": "保羅博古斯", "reason": "全名念法" }
  },
  "reviewer": "pei",
  "reviewed_at": "2026-10-17T11:30:00Z",
  "independent": true,
  "note": "選填"
}
```

- `decisions` 的詞必須剛好是所選建議裡還沒進字典的詞，一個不多一個不少；`proposed` 必須等於建議檔寫的（不能偷改）。
- `decision`：
  - `accept`：照建議的念法（`null` 表示「聲音照字面念就對」）。幾份建議對同一個詞給了不同念法時不能用，要用 `accept_as` 選一個。
  - `accept_as`：改成 `spoken` 的念法（1–80 字），或 `spoken: null`。
  - `reject`：這個詞不進字典。`reason` 選填。
- `reviewer`：審查的人或獨立代理。含 `worker`、`writer`、`listener`、`checker`、`automation`、`auto`、`self`、`system`、`pipeline`、`bot` 等字的會被拒——工人、撰稿或聽稿模型不能審自己的建議。
- `reviewed_at`：含時區的 ISO 8601 時間，不能在未來。
- `independent` 必須是 `true`。
- `lexicon_sha256` 必須等於目前釘選的版本；中間有人發布過別的版本，這張收據就過期，要重新產範本重審。

工具檢查全部吻合後，用「目前釘選的字典＋接受的詞」組出下一版的位元組（被 reject 的詞不進去），以**收據檔原始位元組**的 SHA-256 當 `reviewSha256` 呼叫 `reviseStoryLexicon`。收據原樣存一份到 `<工作區>/<slug>/story/lexicon-reviews/<sha256>.json`（不可變），字典事件的 `review_sha256` 指向它，之後查得到為什麼改。

### 錯誤碼

| 錯誤碼 | 原因 |
| --- | --- |
| `STORY_LEXICON_REVISION_WORKDIR_UNPROVEN` | 工作目錄不是這集的：不存在、`auto.json` 的 slug 不同、沒有 story 狀態，或 `story/chapters` 沒有章節檔 |
| `STORY_LEXICON_MIGRATION_REQUIRED` | 這集還沒釘選字典（先看 [`story-lexicon-migration.md`](story-lexicon-migration.md)） |
| `LEXICON_TRANSACTION_INCOMPLETE` | 有沒做完的字典交易，先處理它 |
| `LEXICON_STOPPED` | 有 STOP 檔 |
| `video_project_leased` | 別的程序（例如工人正在跑這集）拿著專案 LEASE |
| `STORY_LEXICON_REVIEW_INVALID` | 收據不是 JSON、欄位不對、`kind` 不對、`proposals` 空的或重複 |
| `STORY_LEXICON_REVIEW_SLUG_MISMATCH` | 收據是別集的 |
| `STORY_LEXICON_REVIEW_STALE` | 收據審的字典版本不是目前的 |
| `STORY_LEXICON_PROPOSAL_UNKNOWN`／`_STALE`／`_APPLIED`／`_INVALID` | 收據指的建議不存在、過期、已套用或檔案不對 |
| `STORY_LEXICON_REVIEW_DECISIONS_MISMATCH` | 有詞沒決定，或決定了建議裡沒有的詞 |
| `STORY_LEXICON_REVIEW_DECISION_INVALID` | 決定的值不對（未知的 decision、`accept_as` 沒有 `spoken`、`proposed` 被改過…） |
| `STORY_LEXICON_REVIEWER_INVALID` | 沒有 reviewer，或 reviewer 是工人／撰稿／聽稿／自動化 |
| `STORY_LEXICON_REVIEW_TIME_INVALID` | `reviewed_at` 格式不對或在未來 |
| `STORY_LEXICON_REVIEW_NOT_INDEPENDENT` | `independent` 不是 `true` |
| `STORY_LEXICON_REVISION_NOTHING_ACCEPTED` | 全部 reject，沒有新版本可發布 |

所有拒絕都發生在拿 LEASE、寫任何檔之前，所以被拒的那一次什麼都沒寫，連 `LEASE` 檔都沒有。`--apply` 時在兩個 LEASE 底下再全部檢查一次才寫。同一張收據再跑一次 `--apply`，工具從字典事件鏈認出它已發布，回報 `already_applied`、什麼都不寫。

## 正式主機上的操作步驟

不要在本機對正式站的資料跑。正式主機上 repo 在 `/opt/mokaair`，影片工作區在 `/var/lib/mokaair/video-work`，要在工人所在的容器內跑，並帶上工作區（指令自己會接上 slug）：

```bash
cd /opt/mokaair
# 在工人的容器裡（容器名稱照部署設定）：
VIDEO_WORKDIR=/var/lib/mokaair/video-work node tools/video/cli.mjs story-lexicon-revise --slug story-adapt-michelin-guide-stars
```

1. 跑上面的列出指令，確認第一行的工作目錄是 `/var/lib/mokaair/video-work/<slug>`、沒有 `REFUSED`，看清楚每份建議與每個詞。
2. 把印出的範本存成檔（例如 `/tmp/<slug>-lexicon-review.json`），由人逐詞決定，填上 `reviewer`、`reviewed_at`、`independent: true`。決定念法時可以先用 `audition` 試聽。
3. `--review <檔>` 乾跑，確認「accept／reject」與字典 SHA-256 變化是預期的。
4. 加 `--apply` 發布。成功會印出新版本號、事件 SHA-256 與收據存放位置。
5. **到後台 `/admin/videos` 對這集按「重試這支影片」**。工人下一輪看到字典版本變了，會把各章的查核與聽稿標記清掉、重新跑（重試上限的計數不會重置），之後再照常往下走；字典版本會進到語音雜湊，依賴舊字典的音檔核准與快取會照常失效。

以 `story-adapt-michelin-guide-stars` 為例：建議是 `{"Paul": null, "Bocuse": "博古斯"}`，兩個都 `accept` 就是 `Paul` 照字面念、`Bocuse` 念「博古斯」。

## reject 的詞會讓故事繼續卡住

工人只有在 `story.lexicon_pending` 的每個詞都已在釘選字典裡時才放行（`automation/story.mjs` 的 `advanceStory`）。被 reject 的詞不進字典，所以那集發布後仍會卡在「story lexicon proposals need a reviewed revision: <詞>」；而且這個詞多半還在章節文字裡，lint 也不會過。發布之後那份建議變成 `stale`，這個工具不能再拿它收進字典；要讓故事繼續，只能改寫那一章不用這個詞並由人處理 `lexicon_pending`，或等撰稿模型在之後的重寫裡再提出一次新建議。讓工人在 reject 後把那章退回撰稿、清掉該詞的 pending，是另開的工作（見 `tasks/open/`）。所以除非確定要改寫，否則優先用 `accept` 或 `accept_as`。

## 不在範圍內

- 不改 `lexicon-store.mjs`、`story-lexicon.mjs`、`story-lexicon-integration.md`（屬於 A01 轉換的票）；只用它們匯出的函式。
- 不處理 A01（`story-rolling-suitcase-v2`）的 80 筆查核事件轉換。
- 不提供後台按鈕；審查與發布都在主機上以指令完成。
