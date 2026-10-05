---
id: 2026-10-03-claude-computer-use-explained-recheck
title: claude-computer-use-explained 的工具版本與 beta 字樣可能落後一版
status: done
priority: P3
area: docs
owner: claude-opus-5-5-ai-article-rechecks
claimed_at: 2026-10-05T06:14:08Z
created_at: 2026-10-03T12:04:02Z
completed_at: 2026-10-05T06:48:49Z
branch: claude/ai-article-rechecks
depends_on: []
scope:
  - apps/api/app/guides/content/claude-computer-use-explained.json
---

# claude-computer-use-explained 的工具版本與 beta 字樣可能落後一版

## Why

AI 名詞第二批寫電腦操作（Computer Use）時讀到：Anthropic 開發者文件現在是分版本的 computer use 工具組，較早版本仍標 beta。
`claude-computer-use-explained`（2026-09-14）的工具名稱與 beta 字樣可能落後一版。方案與平台的說法沒有查。

## Definition of done

- [x] 文中工具名稱、版本、beta 狀態與當天官方文件一致；方案與平台說法逐條複查。

## Steps

- [x] 讀 Anthropic computer use tool 文件與 Claude 說明中心現行頁。

## How to verify

`pack_cli lint --slug claude-computer-use-explained --warnings`；查證紀錄寫進票。

## Notes

- 來源：`docs/ai-terms-series/batch-02/staging/ai-term-computer-use/` 撰稿者回報。

### 查證紀錄（2026-10-05，claude-opus-5-5-ai-article-rechecks）

十個來源都用 `curl -sSL`、User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`
重抓，全部 200，轉純文字逐段對照；十筆 `checked_on` 都改成 2026-10-05。正文本來就不寫工具版本字串，維持不寫。

改了（兩處）：

- 第四種形式那段「官方文件說 computer use 工具只在 API 上提供，不在一般的 Claude App 裡」→「官方開發者文件把
  computer use 工具標為 Claude API 上的正式功能（較早的工具版本仍是 beta），每個動作都由你的程式在你自己控制的環境裡執行」。
  今天的頁面（https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool ，也讀了同址的 `.md`）
  frontmatter 是 `status: ga`，平台 Claude API 與 Google Cloud 為 ga、Claude Platform on AWS／Bedrock／Foundry 為 beta；
  新版是一個 client toolset（17 個成員工具，不需 beta 標頭），舊的兩個工具版本「remain available in beta」並各要 beta 標頭；
  頁面沒有任何「只在 API、不在 Claude App」的句子，而且桌面版本身就有電腦操作，原句與第一種形式矛盾。
- 這個來源的標題「工具已為正式版」→「新版工具組在 Claude API 與 Google Cloud 為正式版、較早的工具版本與其他平台仍是 beta、
  由你的程式在自己控制的環境執行」。

逐條保留（今天的頁面仍這樣寫）：

- 桌面版電腦操作：beta；Pro 與 Max（Team、Enterprise 目前沒有）；macOS 與 Windows 的桌面 App，在 Cowork 與 Claude Code 裡；
  Settings > General（Desktop app 底下）的「Enable computer use」；每個應用程式先授權；投資交易與加密貨幣預設封鎖；
  封鎖清單；比連接器慢、複雜流程有時要再跑一次。https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork
- Cowork 內建瀏覽器：側邊面板、與自己的瀏覽器分開、逐站匯入 cookie；Pro、Max、Team，Enterprise 要 owner 開通；
  macOS、Windows 與 Linux（beta）仍寫「rolling out gradually」；桌面 App 要開著並連線。
  https://support.claude.com/en/articles/16607400-use-the-built-in-browser-in-claude-cowork
- Claude in Chrome：所有付費方案；只支援 Google Chrome，不支援其他 Chromium 瀏覽器與行動裝置；讀、點、打字、填表、開關分頁。
  https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome
- 三種權限模式（Manually approve／Automatically approve／Skip all approvals）、單次或整站授權、Your approved sites、
  永遠不做的動作（購買、建帳號、信用卡與證件資料、永久刪除、交易）。https://support.claude.com/en/articles/12902446-claude-in-chrome-permissions-guide
- 提示詞注入與銀行對帳單的例子、風險不是零、成人與盜版網站封鎖、金融網站先問、禁止繞過驗證碼、不建議用於金融與醫療與他人個資。
  https://support.claude.com/en/articles/12902428-use-claude-in-chrome-safely
- Cowork 是什麼、桌面／網頁／行動版、付費方案。https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork
- 截圖每張約 1,000–1,800 個輸入 token、解析度建議、下拉選單與捲軸改用鍵盤、每步截圖驗證的提示詞、放大（zoom）動作、
  四條安全建議、分類器掃描截圖後先確認指令來源：皆在 computer use tool 頁。
- 像素計算、虛擬鍵盤、翻頁動畫式畫面認知（https://www.anthropic.com/news/developing-computer-use）；
  捲動、拖曳、縮放對模型是難題（https://www.anthropic.com/news/3-5-models-and-computer-use）；
  產品頁的所有付費方案、避開金流與密碼管理與敏感個資、保護不是萬無一失（https://claude.com/claude-in-chrome）。

看到但沒改：

- 說明中心各頁頂端新加了「Claude Cowork is now just Claude」的說明，正逐步推給 Pro 與 Max，選單可能不再有 Chat／Cowork
  兩個選項。正文的「消費端形式的名稱、方案與平台都還在變……以官網為準」已涵蓋，沒有改寫全文的 Cowork 用語。
- claude.com/claude-in-chrome 頂端寫「now generally available」，說明中心仍寫 Chrome 側邊面板是 beta；正文沒有寫 Chrome 的
  beta 或正式狀態，不受影響。
- 表格圖說與圖解描述的「2026 年 9 月依……整理」是整理時間，內容今天複查無誤，沒有改。

驗證：`PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --kind life --slug claude-computer-use-explained` 0 errors；
加 `--warnings` 只有既有的 `no_summary`（本系列都沒有 summary 區塊，與本票無關）。
