---
id: 2026-09-15-guide-titles-competing-queries
title: 三組文章標題和既有文章搶同一個查詢
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-15T12:49:32Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/gguf-quantization-explained.json
  - apps/api/app/guides/content/transcription-desktop-tools.json
  - apps/api/app/guides/content/whisper-local-transcription.json
  - apps/api/app/guides/content/claude-mcp-explained.json
---

# 三組文章標題和既有文章搶同一個查詢

## Why

2026-09-15 發布 317 篇前做過重複審查，結論是**內容都不重複**，但有三組標題會去搶同一個搜尋查詢。這三組現在都已上線：

| 這篇（要改） | 搶的是 | 問題 |
| --- | --- | --- |
| `gguf-quantization-explained`「量化是什麼：GGUF、Q4、Q8 怎麼選」 | `ai-term-quantization`「量化（Quantization）：用較少位元執行模型的取捨」 | 兩篇都以「量化是什麼」這個定義型查詢為目標。前者其實是 GGUF 檔名與 Ollama 實作，後者才是概念詞條。 |
| `claude-mcp-explained`「MCP 是什麼：讓 Claude 連上你的檔案、日曆與資料庫」 | `ai-term-model-context-protocol`「模型上下文協定（MCP）是什麼…」 | 前者三分之二是 Claude 連接器的設定示範，標題卻搶「MCP 是什麼」。 |
| `transcription-desktop-tools`「逐字稿工具怎麼用：MacWhisper 與 Whisper 桌面工作流」 | `whisper-local-transcription`「用 Whisper 本機轉錄逐字稿：會議與訪談的離線做法」 | 兩篇都寫明鎖定「逐字稿 AI」這個查詢。前者是圖形介面，後者是 pip 加指令列。 |

搜尋引擎會在同站兩篇之間輪流選一篇，兩篇排名都變差，讀者也分不清該看哪篇。

## Definition of done

- [ ] 三篇的標題，以及必要時的 description 首句，改成點明各自獨特角度的寫法。
      URL 不變；另一篇既有文章不改。
- [ ] 每組雙向互連：改標題的這篇連到對方，對方如果還沒連過來，就在本票範圍外另外處理。
      本票範圍只含要改標題的四個內容包，互連只改這四篇。
- [ ] 正式站以 `--slug` 限定匯入並發布更新，公開頁的 h1 已更新。

## Steps

- [ ] `gguf-quantization-explained`：標題改成實作型，例如「GGUF 量化怎麼選：Q4_K_M、Q8_0、F16 檔名與檔案大小」。在正文加一條連到 `ai-term-quantization` 的連結。
- [ ] `claude-mcp-explained`：標題以「在 Claude 裡怎麼加 MCP 連接器」為主。開頭連到 `ai-term-model-context-protocol` 的名詞解釋。
- [ ] `transcription-desktop-tools` 標題點明圖形介面，例如「MacWhisper 與 WhisperDesktop 逐字稿教學」；`whisper-local-transcription` 標題點明指令列，例如「用 Whisper 指令列在本機轉逐字稿：pip、ffmpeg 與 SRT 輸出」。在 `transcription-desktop-tools` 文末補一條連到 `whisper-local-transcription` 的連結（反方向已經有了）。
- [ ] 跑 `pack_cli lint --slug` 與內容包測試。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --slug gguf-quantization-explained
uv run pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py -q
# 部署後在主機限定這四篇（dry-run 應為四個 zh-TW update），再 --publish
python -m app.cli guides-import --actor-email <admin> --locale zh-TW --publish --dry-run \
  --slug gguf-quantization-explained --slug claude-mcp-explained \
  --slug transcription-desktop-tools --slug whisper-local-transcription
```

`tests/test_guides_content_links.py` 在 PR #526 才加入；那個 PR 還沒合併前，先跳過這個檔。

## Notes

- 審查方式分兩段，全部由代理讀原文判斷：
  - 第一段：16 個代理先找出 58 組候選。8 組高、中信心的候選，各由 3 位觀點不同的審查者讀原文，結果都是 0/3 判為重複。
  - 第二段：其餘 50 組由 1 位審查者初篩，判定重複的才升級加派 2 位。結果沒有一組需要升級。
- 標題互搶的判斷與改法建議都出自這些審查者。範例標題只是建議，請以文章實際內容定稿。
- 同一次審查中，`claude-skills-explained`（Agent Skills）與 `deepseek-privacy-and-data-flow`（DeepSeek 入門）也被提過。審查者判斷只需要互連、不必改標題，所以不列入本票。
