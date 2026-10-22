---
id: 2026-10-22-c04-bubble-wrap-approved-local-pilot
title: C04 Bubble Wrap approved local pilot
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-c04-pilot
claimed_at: 2026-10-22T03:32:58Z
created_at: 2026-10-22T03:32:53Z
completed_at:
branch: codex/brand-story-bubble-wrap-c04-local-pilot
depends_on: []
scope:
  - docs/videos/story-everyday-bubble-wrap-c04-pilot
---

# C04 Bubble Wrap approved local pilot

## Why

站主已於 2026-10-22 明確核准 C04 Bubble Wrap 定稿的腳本／逐鏡方向及單支本機試片製作，整支 US$25 為硬停線，84 張插圖每鏡最多三次、94 句旁白與一首配樂；不含上傳或發布。腳本草稿 PR #1670 仍在 review，正式成片和站主驗收仍是後續關卡。本票只管隔離 C04 試片的核准收據、實際 TTS 長度、音訊／圖像／配樂與試片證據，不碰 C03 或其他作品。

## Definition of done

- [ ] 留下綁定 C04 定稿三份 SHA-256 與批准範圍的站主收據，先檢查 STOP、已有付費台帳、登入及成本狀態。
- [ ] 先合成 94 句 TTS，音訊逐句檢查，並以實際時間軸證明第 02–06 章純旁白至少 480 秒；不足時先停，不買圖。
- [ ] 時長與音訊關卡合格後才製作至多 84 張 MiniMax 插圖、每鏡累計至多三次；逐張驗收 Curio 畫風與史實界線，讀回台帳。
- [ ] 只製作一首配樂，獨立解碼量到交付長度，避免將請求秒數當成實際音檔秒數；完成本機概念試片與影音 QA。
- [ ] 整支可見費用與未知帳項均對 US$25 上限保守停線，留下輸出雜湊、未完成關卡及保留的付費素材；不私上傳、不發布、不合併、不部署。

## Steps

- [ ] 讀當前品牌故事與 Curio 製作規則；建立 hash-bound owner approval，隔離媒體 workdir 並做付費前預檢。
- [ ] 跑 TTS、量 02–06 章實際秒數、做音訊檢查與必要窄範圍修正。
- [ ] 再跑圖像、配樂乾跑與受限正式生成；保留工作檔與台帳。
- [ ] 組本機概念試片、做 QA、回報成片／審核／發布的準確狀態。

## How to verify

`Get-FileHash` 對稿、畫面表與影片資料讀回；`node tools/video/cli.mjs status/tts/check-audio/keyframes/music --slug story-everyday-bubble-wrap-c04 --workdir <base>` 的乾跑與實跑輸出，`ffprobe` 對第 02–06 章時間軸、配樂與本機試片長度，以及 `ffmpeg -v error -xerror` 整檔解碼。`npm run check:tasks` 與相關影片 lint／測試以追蹤樹驗證；任何 `STOP` 或未知已付費 POST 都停下查明，不盲重送。

## Notes

起點為 #1670 head commit `4f02e21ae5975a68394377d9f9c3352c42e5c915` 的新託管工作樹，非帶有政策阻擋未追蹤副本的腳本工作樹。此票不宣稱站主已核准正式頻道片頭片尾、後台成片審查或 YouTube Studio 結束畫面元素。正式 TTS 開始前先寫 `docs/videos/story-everyday-bubble-wrap-c04-pilot/approval.md`。
