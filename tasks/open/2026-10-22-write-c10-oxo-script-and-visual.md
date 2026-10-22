---
id: 2026-10-22-write-c10-oxo-script-and-visual
title: Write C10 OXO script and visual plan
status: review
priority: P1
area: docs
owner: codex-c10-oxo-script
claimed_at: 2026-10-22T14:06:36Z
created_at: 2026-10-22T14:06:24Z
completed_at:
branch: codex/brand-story-oxo-c10-script
depends_on: []
scope:
  - docs/videos/story-everyday-oxo-c10/script.md
  - docs/videos/story-everyday-oxo-c10/visual-plan.md
  - docs/videos/story-everyday-oxo-c10/visual-plan.json
  - docs/videos/story-everyday-oxo-c10/script-source-notes.md
---

# Write C10 OXO script and visual plan

## Why

站主已採用 C10 OXO 六章企劃，卻還沒有可供逐句查核與審核的繁中旁白及逐鏡。這張票只交付非付費稿件；獨立來源審查、盲讀、TTS、媒體費用與上架另有關卡。

## Definition of done

- [x] 對照已採用 Treatment 撰寫六章、逐句有 ID 與來源界線的單旁白稿。
- [x] 逐句 JSON 與人可讀逐鏡表一對一，遵守奇聞檔案局風格、書擋與畫面界線。
- [x] 腳本與資料格式檢查通過，草稿 PR 可供獨立查核和站主後續審稿；不在此票宣稱劇本已核准。

## Steps

- [x] 讀 brand-story、youtube-video/story、curio-episode、task-board 規則，核對企劃與來源矩陣 SHA。
- [x] 直接重讀 Cooper Hewitt、MoMA、OXO、Design Council、LA Times、Smart Design 可讀頁面。
- [x] 寫 80 句約 2,461 字元草稿，80 鏡一對一；只按鏡數預檢插圖 71／80。
- [x] 跑 JSON/ID/卡片、故事規格與任務檢查，補齊留下的風險與 PR 連結。

## How to verify

`npm run check:tasks` PASS；`git diff --check` PASS；PowerShell 比對稿件、JSON、閱讀版逐鏡表的全部 80 個 ID、唯一性、卡片連續數、非空畫面、畫風與書擋 PASS。`npm run test:docs-videos` 在此新工作樹因缺 `pinyin-pro` 失敗，屬與本次純文稿無關的全倉依賴環境問題；未把它稱為通過。真正的 480 秒正文與插圖時間占比須待有站主付費核准的 TTS 才能驗。

## Notes

既有 Treatment SHA-256 `CD541D96E66042CA9A5EDE0C4017355C536D16FC7092249C9CCB15D266F4D550`、矩陣 SHA-256 `4DEEB89A2028184E73F681FCFD3C9B7FB44463B364BF0D26AC9941F557F156A6`。S4 首批 15 件與 S6/S7 20 件衝突，正文不定數；1989 設計、1990 上市分開。S6 的零售商與消費者反應是 2000 年回憶；MoMA 是設計評價而非銷售紀錄。全片沒有付費媒體、上傳或發布授權。

草稿 [PR #1689](https://github.com/x812033727/travel_scanner/pull/1689) 以企劃分支為基底，供獨立逐句來源查核、兩位盲讀與站主後續劇本審核。現有 script SHA-256 `1A05017A9C6DF2A60365655975E00AC954AF799D2264C9E006F89B21449C2CB3`、visual JSON SHA-256 `4241FC748B5FA81927EC81B3FAAF4BEC8AC332AA5893F7B2DC3C6CD240AE1CF9`；補這段任務註記不改稿件 bytes。
