---
id: 2026-09-16-retitled-guides-stale-link-text
title: 17 篇文章仍以四篇改過的舊標題當連結文字
status: review
priority: P3
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-19T09:28:04Z
created_at: 2026-09-16T03:49:41Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on:
  - 2026-09-15-guide-titles-competing-queries
scope:
  - apps/api/app/guides/content/ai-for-youtube-creators.json
  - apps/api/app/guides/content/ai-meeting-notes-tools.json
  - apps/api/app/guides/content/ai-video-subtitles-translation.json
  - apps/api/app/guides/content/ai-voice-cloning-elevenlabs.json
  - apps/api/app/guides/content/claude-computer-use-explained.json
  - apps/api/app/guides/content/claude-desktop-mobile-app-setup.json
  - apps/api/app/guides/content/claude-in-chrome-browser-agent.json
  - apps/api/app/guides/content/claude-skills-explained.json
  - apps/api/app/guides/content/huggingface-guide.json
  - apps/api/app/guides/content/llama-models-explained.json
  - apps/api/app/guides/content/lm-studio-getting-started.json
  - apps/api/app/guides/content/local-ai-gpu-buying-guide.json
  - apps/api/app/guides/content/local-llm-hardware-requirements.json
  - apps/api/app/guides/content/mcp-servers-for-everyone.json
  - apps/api/app/guides/content/ollama-getting-started.json
  - apps/api/app/guides/content/ollama-with-code-editors.json
  - apps/api/app/guides/content/qwen-local-deployment.json
---

# 17 篇文章仍以四篇改過的舊標題當連結文字

## Why

`2026-09-15-guide-titles-competing-queries` 在 2026-09-16 把四篇的標題改成各自的角度：

| slug | 舊標題（仍是 17 篇的連結文字） | 新標題 |
| --- | --- | --- |
| `gguf-quantization-explained` | 量化是什麼：GGUF、Q4、Q8 怎麼選 | GGUF 量化怎麼選：Q4_K_M、Q8_0、F16 的檔名、檔案大小與記憶體 |
| `claude-mcp-explained` | MCP 是什麼：讓 Claude 連上你的檔案、日曆與資料庫 | 在 Claude 裡怎麼加 MCP 連接器：讀資料夾與查行事曆的設定示範 |
| `transcription-desktop-tools` | 逐字稿工具怎麼用：MacWhisper 與 Whisper 桌面工作流 | MacWhisper 與 WhisperDesktop 圖形介面逐字稿教學：不打指令的本機轉寫流程 |
| `whisper-local-transcription` | 用 Whisper 本機轉錄逐字稿：會議與訪談的離線做法 | 用 Whisper 指令列在本機轉逐字稿：pip、ffmpeg 安裝與 SRT 字幕輸出 |

scope 裡的 17 篇（`grep -l` 四個舊標題找出來的）還以舊標題當 `article` inline 的 `text`。連結仍然有效（slug 沒變），只是讀者看到的文字和落地頁的 h1 不一樣，而且舊文字又把「量化是什麼」「MCP 是什麼」這種定義型查詢的訊號送回改過角度的文章。

## Definition of done

- [x] 17 篇裡指向這四篇的 `article` inline，`text` 改成新標題或描述目標內容的短語（例如「GGUF 量化怎麼選」）。
- [x] `grep -l` 四個舊標題在 `apps/api/app/guides/content/` 下找不到任何檔案。
- [ ] 正式站以 `--slug` 限定匯入這 17 篇並發布。

## Steps

- [x] `grep -n` 四個舊標題，逐檔改 inline `text`（只改文字，不動 slug／kind）。
- [x] `uv run python -m app.guides.pack_cli lint --slug …` ×17、`uv run pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py -q`（跑的是 `lint --kind life`，涵蓋這 17 篇）。

## How to verify

```bash
cd apps/api/app/guides/content
grep -l -e "量化是什麼：GGUF、Q4、Q8 怎麼選" -e "MCP 是什麼：讓 Claude 連上你的檔案、日曆與資料庫" \
  -e "逐字稿工具怎麼用：MacWhisper 與 Whisper 桌面工作流" -e "用 Whisper 本機轉錄逐字稿：會議與訪談的離線做法" *.json
# 應該沒有輸出
```

## Notes

- 2026-09-16 開票時這 17 篇都不在任何進行中任務的 scope 內；四篇 `ai-*` 不在 `2026-09-13-life-ai-batch-11` 的 20 篇裡。
- 連結文字是 `relink`／`autolink` 用當時的標題產生的；工具不會回頭更新，所以要手改。

### 2026-09-19 done in repo (claude-fable-5-1)

改法：逐檔 `json.load` 走結構，只改 `type: article`、slug 是四篇之一、`text` 等於舊標題的 inline，
再用 `pack_ingest` 寫包的同一組設定寫回（`json.dumps(..., ensure_ascii=False, indent=2) + "\n"`；
改之前先確認 17 檔空跑 round-trip 逐位元相同），所以每檔的 diff 只有 inline `text` 那一行。
17 篇都只有 zh-TW，一共 20 個 inline，沒有其他 locale 要處理。

| pack | 指向的 slug | 改成 |
| --- | --- | --- |
| `ai-for-youtube-creators` | whisper-local-transcription | 新標題 |
| `ai-meeting-notes-tools` | whisper-local-transcription、transcription-desktop-tools | 新標題 ×2 |
| `ai-video-subtitles-translation` | whisper-local-transcription、transcription-desktop-tools | 新標題 ×2 |
| `ai-voice-cloning-elevenlabs` | transcription-desktop-tools | 新標題 |
| `claude-computer-use-explained`、`claude-desktop-mobile-app-setup`、`claude-in-chrome-browser-agent`、`claude-skills-explained`、`mcp-servers-for-everyone` | claude-mcp-explained | 新標題（各 1 個） |
| `huggingface-guide`、`lm-studio-getting-started`、`local-llm-hardware-requirements`、`ollama-getting-started`、`ollama-with-code-editors`、`qwen-local-deployment` | gguf-quantization-explained | 新標題（各 1 個） |
| `llama-models-explained` | gguf-quantization-explained（句中，同句另兩個連結都是全標題） | 新標題 |
| `local-ai-gpu-buying-guide` | gguf-quantization-explained（句中，前面已有 q4_K_M／q8_0 與量化詞條連結） | 短語「GGUF 量化怎麼選」 |

獨立成段的 inline（relink 產生、只有一個 inline 的 `rich_paragraph`）一律用完整新標題，和落地頁 h1 一致；
只有 `local-ai-gpu-buying-guide` 那句是散文，用短語比較順。slug、kind 都沒動。

驗證（2026-09-19，本機）：
- `grep -l` 四個舊標題於 `apps/api/app/guides/content/*.json`：無輸出。
- `cd apps/api && uv run python -m app.guides.pack_cli lint --kind life`：exit 0、911 entries checked；
  17 篇底下只有原本就有的 `no_summary` warning，沒有 error。
- `uv run pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py -q`：12 passed, 5 skipped。

主機步驟（部署後，`--slug` 可重複）：

```bash
python -m app.cli guides-import --actor-email <admin> --dry-run \
  --slug ai-for-youtube-creators --slug ai-meeting-notes-tools --slug ai-video-subtitles-translation \
  --slug ai-voice-cloning-elevenlabs --slug claude-computer-use-explained --slug claude-desktop-mobile-app-setup \
  --slug claude-in-chrome-browser-agent --slug claude-skills-explained --slug huggingface-guide \
  --slug llama-models-explained --slug lm-studio-getting-started --slug local-ai-gpu-buying-guide \
  --slug local-llm-hardware-requirements --slug mcp-servers-for-everyone --slug ollama-getting-started \
  --slug ollama-with-code-editors --slug qwen-local-deployment
# 應列 17 篇 zh-TW 的更新；確認後同一串參數把 --dry-run 換成 --publish，再勾上面第三項並 done。
```
