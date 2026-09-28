---
id: 2026-09-28-video-shorts-skill-docs
title: Video shorts D1: the Shorts route in the youtube-video skill, the channel spec and the automation design
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-28T04:05:00Z
completed_at:
branch:
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

- [ ] `references/shorts.md`：Shorts 路線的操作步驟——三條內容線各自怎麼做、腳本格式、`build`／`check-audio`／`qa`／`package`／`push`／`import` 的用法與結束碼、自動品管 12 項各自沒過時怎麼修、實測的規範（凍結題目、各跑一次、照實寫）、已知的坑。只寫怎麼做；為什麼這樣做留在 `docs/videos/SHORTS.md`。
- [ ] `SKILL.md` 的路線清單加 Shorts，指到 `references/shorts.md`；`.claude/skills/youtube-video/SKILL.md` 是逐字複本。
- [ ] `references/formats.md` 的 Shorts 一節改成跟產線一致（長度、腳本、開場、結尾導流、三條內容線各一句）。
- [ ] `references/publish.md` 加「Shorts 的上架」：稽核前站主只拖檔案、網站認領；稽核後網站自己上傳；跟長片送出去的欄位差在哪裡；試作票實測的五項結果。
- [ ] `references/automated.md` 加工人的 Shorts 步驟與它在迴圈裡的位置。
- [ ] `docs/videos/README.md` 的成品規格表加 Shorts 一列（1080×1920、30 fps、25–55 秒、H.264／AAC、−14 LUFS、字卡字幕加一條 zh-TW CC、沒有章節與縮圖）；聲音一節說明 Shorts 用同一個頻道聲音。
- [ ] `docs/videos/AUTOMATION.md` 加一節「Shorts」，指到 `SHORTS.md`。
- [ ] `docs/videos/ai-shorts/README.md` 開頭加一段：排程、成效、花費的正本已經搬到後台的 Shorts 分頁，本機的 `track-init`、`report` 只剩離線用途。
- [ ] `npm run test:tools` 過（skill 的鏡射、路徑存在、沒有本機路徑）。

## Steps

- [ ] 等 T2 合併，照實際的指令與旗標寫，不照設計稿寫。
- [ ] 寫 `references/shorts.md`，再改其他檔。
- [ ] `cp .agents/skills/youtube-video/SKILL.md .claude/skills/youtube-video/SKILL.md`。

## How to verify

```bash
npm run test:tools
```

## Notes

- skill 的 reference 只能提到已經存在的路徑；不能出現本機工作區的路徑，也不能有 `support@mokaair.com` 以外的信箱。
- `SKILL.md` 本文最多 300 行。
- 只改 `docs/videos/**` 或 `.agents/skills/**` 不會觸發影片的兩個 workflow，只有 `ci.yml` 會跑。
