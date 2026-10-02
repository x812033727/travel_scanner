---
id: 2026-09-28-video-shorts-skill-docs
title: Video shorts D1: the Shorts route in the youtube-video skill, the channel spec and the automation design
status: done
priority: P2
area: docs
owner: claude-opus-5-5-shorts-d1
claimed_at: 2026-10-02T09:05:45Z
created_at: 2026-09-28T04:05:00Z
completed_at: 2026-10-02T09:23:08Z
branch: claude/video-shorts-skill-docs
depends_on:
  - 2026-09-28-video-shorts-worker-lab
scope:
  - .agents/skills/youtube-video/SKILL.md
  - .claude/skills/youtube-video/SKILL.md
  - .agents/skills/youtube-video/references/shorts.md
  - .agents/skills/youtube-video/references/formats.md
  - .agents/skills/youtube-video/references/publish.md
  - .agents/skills/youtube-video/references/automated.md
  - docs/videos/README.md
  - docs/videos/AUTOMATION.md
  - docs/videos/ai-shorts/README.md
---

# Video shorts D1: the Shorts route in the youtube-video skill, the channel spec and the automation design

## Why

skill `youtube-video` 是 Codex 與 Claude Code 共用的做影片的說明書，現在列了五條路線，沒有一條是 Shorts；整個 skill 只有 `references/formats.md` 最後三行提到 Shorts，而且寫的是「60 秒內、稿子另存 `short-<n>.md`」，跟實際的產線（25–55 秒、一支一份 JSON 腳本）不一樣。這份 `formats.md` 還會整份送進企劃模型的提示詞。`docs/videos/README.md`（頻道規格）與 `docs/videos/AUTOMATION.md`（主機工人）也都沒有 Shorts。

設計全文在 `docs/videos/SHORTS.md`。

## Definition of done

- [x] `references/shorts.md`：Shorts 路線的操作步驟——三條內容線各自怎麼做、腳本格式、`build`／`check-audio`／`qa`／`package`／`push`／`import` 的用法與結束碼、自動品管 12 項各自沒過時怎麼修、實測的規範（凍結題目、各跑一次、照實寫）、已知的坑。只寫怎麼做；為什麼這樣做留在 `docs/videos/SHORTS.md`。
- [x] `SKILL.md` 的路線清單加 Shorts，指到 `references/shorts.md`；`.claude/skills/youtube-video/SKILL.md` 是逐字複本。
- [x] `references/formats.md` 的 Shorts 一節改成跟產線一致（長度、腳本、開場、結尾導流、三條內容線各一句）。
- [x] `references/publish.md` 加「Shorts 的上架」：稽核前站主只拖檔案、網站認領；稽核後網站自己上傳；跟長片送出去的欄位差在哪裡；試作票實測的五項結果。
- [x] `references/automated.md` 加工人的 Shorts 步驟與它在迴圈裡的位置。
- [x] `docs/videos/README.md` 的成品規格表加 Shorts 一列（1080×1920、30 fps、25–55 秒、H.264／AAC、−14 LUFS、字卡字幕加一條 zh-TW CC、沒有章節與縮圖）；聲音一節說明 Shorts 用同一個頻道聲音。
- [x] `docs/videos/AUTOMATION.md` 加一節「Shorts」，指到 `SHORTS.md`。
- [x] `docs/videos/ai-shorts/README.md` 開頭加一段：排程、成效、花費的正本已經搬到後台的 Shorts 分頁，本機的 `track-init`、`report` 只剩離線用途。
- [x] `npm run test:tools` 過（skill 的鏡射、路徑存在、沒有本機路徑）。

## Steps

- [x] 等 T2 合併，照實際的指令與旗標寫，不照設計稿寫。
- [x] 寫 `references/shorts.md`，再改其他檔。
- [x] `cp .agents/skills/youtube-video/SKILL.md .claude/skills/youtube-video/SKILL.md`。

## How to verify

```bash
npm run test:tools
```

## Notes

- skill 的 reference 只能提到已經存在的路徑；不能出現本機工作區的路徑，也不能有 `support@mokaair.com` 以外的信箱。
- `SKILL.md` 本文最多 300 行。
- 只改 `docs/videos/**` 或 `.agents/skills/**` 不會觸發影片的兩個 workflow，只有 `ci.yml` 會跑。
- **2026-10-02（claude-opus-5-5-shorts-d1）**：認領時被兩張過期的認領擋住（`2026-09-28-sothatswhy-shorts-from-episode`，PR #904／#950／#962 已合併；`2026-09-30-video-worker-moves-two-videos-at`，PR #999 已合併），用 `--force` 接手。
- 照 main（`fb8ef3e96`）上真的程式寫，不照設計稿：A3 伺服器（#1097：題庫、`shorts/next`、排片、每週報告、`subject` 階段）、W2 後台（#1118：題庫、素材箱、每週報告、受測模型與每月上限）、T2 工人（#1119：`shortsStep`、`lab.mjs`、提示詞）、#1120（卡住的 Short 不再擋住後面的時段）。每一句都對過程式：指令與旗標照 `tools/video/shorts/cli.mjs` 的 `HELP`，結束碼照它最後一行（`who: owner` → 3、`service` → 4、其他 → 1，`push` 沒出錯一律 0、要看 `waits`），12 項照 `qa.mjs` 的 `ITEM_IDS`，上傳包 4 項照 `package.mjs`，工人的順序照 `tools/video/automation/cli.mjs` 與 `shorts.mjs`，實測的步驟與自動修照 `lab.mjs` 的 `ORDER`、`QA_FIXES`、`MAX_FIX_ROUNDS`。
- 還沒有的寫成「還沒有」：精華的工人步驟（T3，另一個代理正在寫，沒碰 `tools/video/shorts`、`tools/video/automation`）、漫劇直式短篇（T4）、稽核後網站自己上傳（Y2）。開著的 PR 只在 `AUTOMATION.md` 提一次 #1124（Shorts 各階段模型的設定頁）是「待合併」；#1123 沒提。
- `publish.md` 的「試作票實測的五項結果」：五項在 P1（`2026-09-28-video-shorts-pilot-launch`）還沒測，所以寫成「待實測」清單（照 Y1 票 Notes 的五項），結果由 P1 回寫。P1 票寫的五項裡有「相關影片」，那一項 Y1 已經查官方頁確定 API 寫不了，換成 Y1 列的「有沒有被歸成 Shorts」。
- `docs/videos/README.md` 的聲音表原本還寫「供應商 Azure、頻道聲音還沒選」，跟 `automated.md`、`AUTOMATION.md` 與程式（`DEFAULT_VOICE` 是 Gemini Sulafat）不一致；要寫「Shorts 用同一個頻道聲音」就得先寫對頻道聲音，所以一起改成 Gemini Sulafat（Azure 是另一個可選的供應商）。這份檔案也會整份送進撰稿模型的提示詞。
- `SKILL.md` 的 description 多一句 Shorts（497 → 601 字元，上限 1024），讓「做 Shorts」也會觸發這個 skill。
- 綁定檔（`docs/videos/long-form/review.json`）：改了 `.agents/skills/youtube-video/SKILL.md`、`.claude/skills/youtube-video/SKILL.md`、`references/automated.md`、`references/formats.md`、`docs/videos/README.md` 五個，`node --test tools/video/long-form/review.test.mjs` 因此失敗（只列這五個 stale binding）。作者不自己重綁，交給獨立審查。
