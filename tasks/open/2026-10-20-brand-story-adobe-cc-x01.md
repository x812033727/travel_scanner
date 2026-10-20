---
id: 2026-10-20-brand-story-adobe-cc-x01
title: 製作 Adobe Creative Cloud 品牌故事本機試看片
status: in-progress
priority: P1
area: docs
owner: codex-gpt6-adobe-x01
claimed_at: 2026-10-20T09:13:41Z
created_at: 2026-10-20T09:13:38Z
completed_at:
branch: codex/brand-story-adobe-cc-x01
depends_on: []
scope:
  - docs/videos/story-everyday-adobe-cc-x01
---

# 製作 Adobe Creative Cloud 品牌故事本機試看片

## Why

站主要求持續製作品牌影片，沿用奇聞檔案局的說書節奏、MiniMax 可愛插圖、配樂、濃縮開場與片頭片尾規則。原訂下一題 C03 Moleskine 的兩個官方網域在此雲端被代理白名單擋住，無法先做逐項原件查核；Adobe Creative Cloud 已有可讀的 SEC 年報初查，可先作為既定 C01–C20 以外的 X01 補充試片。必須把 Adobe 公司整體的訂閱收入與 Creative Cloud 單一產品分清楚。

## Definition of done

- [x] SEC 一手原件支持六章因果主線、逐句稿與資料卡，另一代理獨立查核並綁定最終內容雜湊；說故事盲評與 `lint` 過關。
- [ ] 在整支 US$25 硬上限內，完成至少八分鐘正文、MiniMax `image-01` 插圖、配樂、30–60 秒濃縮開場（旁白實測 52.57 秒）、5 秒概念片頭、21 秒概念片尾、1080p 本機試片及可關閉繁中字幕。
- [ ] 完成視覺、音訊、媒體格式、來源連結、成本與上架包交接；正式品牌素材、正式音訊／品管與 YouTube 可點片尾連結未通過前，不宣稱正式成片。

## Steps

- [x] 讀 Adobe 2012、2013、2015、2025 SEC 10-K 與相關同期原件，寫六章 Treatment 和每項主張來源，獨立核查。
- [x] 寫繁中逐字稿、場景提示詞、鉤子表與 YouTube 文案；另一代理盲評，跑 lint 零錯誤。
- [x] 做整片成本乾跑與預算表，確認餘額和 US$25 上限後才付費生成旁白、插圖、配樂。
- [ ] 完成本機概念片頭片尾、渲染、字幕、整檔影音 QA 與交接。

## How to verify

從儲存庫根目錄以 `node --use-env-proxy /workspace/video-tool-cli.mjs <command> --slug story-everyday-adobe-cc-x01 --workdir /workspace/.brand-video-workdir` 依序執行 `lint`、`tts --dry-run`、`tts`、`check-audio`、`keyframes --dry-run --takes 3`、`keyframes --takes 3`、`render`、`music --dry-run`、`music`；再跑本集試片合成、`ffprobe`／`ffmpeg -xerror` 整檔解碼、字幕時序、`npm run test:docs-videos`、`npm run check:tasks`。

## Notes

2026-10-20：X01 是原 20 集之外的補充題，不改 C03 Moleskine 編輯順位。Moleskine 與 D’Ieteren 網域在當前雲端回 CONNECT 403；環境設定新增草稿又因 `stale_base` 失敗，已將四個必要網域與交接寫進 `/workspace/c03-source-access-handoff.md`。Adobe 四份 SEC 原件可回 HTTP 200；本機影片工具權杖可唯讀取得媒體狀態，但正式品牌動畫仍在主機工作區之外。站主既定每支 US$25 上限及「用建議決定、無須逐項詢問」適用本機試片。逐句來源、文稿及成本乾跑已完成，87 句旁白已合成，正文 602.53 秒、開場 52.57 秒；付費語音的一次回覆中斷按可能收費保守計入（`reviews/tts-recovery.md`）。兩輪自動音訊複查已完成，4 個近義轉錄旗標待人工聽核；插圖尚在製作。未知的語音／轉錄費不得記零。
