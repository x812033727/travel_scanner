---
id: 2026-10-25-ai-slides-outline-review-with-four
title: AI slides outline review with four cited pages
status: in-progress
priority: P2
area: docs
owner: codex-ai-tech-news
claimed_at: 2026-10-25T19:59:14Z
created_at: 2026-10-25T19:59:13Z
completed_at:
branch: codex/ai-tech-slides-20261025
depends_on: []
scope:
  - docs/videos/ai-slides-outline-review
---

# AI slides outline review with four cited pages

## Why

跟進2026-10-19/21 Google生成前大綱Review消息，交出同一份公共報告的4頁原創簡報及逐頁來源，以可審輸入、集中修改和可編輯交付教觀眾完成一份可用成品。依站主推薦自主／八語／直接後臺／持續下一支委派推進，不冒稱Notebook產品實測。

## Definition of done

- [ ] 正式稿、完整提示、五項數字與已RUN四頁成果對齊；不同作者事實／圖卡／敘事結果照實記錄。
- [ ] 繁中正文及成片均實測至少八分鐘，逐句音檢與成片QA完成。
- [ ] en/ja/ko/es/pt/id/vi/th各有metadata、CC及真正音檢的可下載M4A，直接後臺交付並核對角色／SHA／大小。
- [ ] 後臺實際核准狀態、未完成項與交接清楚，無YouTube公開／合併／部署。

## Steps

- [x] 本地／worktree／遠端／PR／後臺359列查重，建立隔離窄範圍任務。
- [x] 原創4頁PDF／PPTX／引用紀錄與56原檔SHA經獨立輸入審查。
- [x] 正常登記與Jev／協調者大綱採用（A0.99、示範0.93；remote pending與本機採用分開）。
- [ ] 正式稿及來源關卡。
- [ ] 樣卡／TTS／音檢／合成／CC／QA。
- [ ] 八語媒體、包裝及後臺驗證交付。

## How to verify

原生lint／事實／敘事／音檢／render／assemble／QA／package；npm run test:docs-videos及npm run check:tasks。data的實際copied-file-manifest與原56檔manifest分開，來源PDF依官方URL／SHA查；後臺使用正常工具路由由server驗SHA並回讀角色／大小，不冒稱遠端binary stream驗證。

## Notes

來源2026報告／2025資料；投資十億美元、企業總額與私人子集不可相加，US/China限相同私人融資口徑；88為受訪者自述，不是企業普查。70/79問項／母體尚未對齊，只作未解註記，不說Stanford錯。Notebook功能只有官方CITED、沒有帳號使用證據。作者初稿／feedback同次build，不能稱獨立pause或產品loop；PDF為image-backed，PPTX才editable且未原生PowerPoint渲染。

站主持續委派，例行選擇不重問；成片、八語、後臺核准各自實際驗證，PR必no-auto-merge。不改前兩片／第三片凍結source與聲音。
