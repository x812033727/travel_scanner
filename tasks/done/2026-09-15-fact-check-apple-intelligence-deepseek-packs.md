---
id: 2026-09-15-fact-check-apple-intelligence-deepseek-packs
title: Apple Intelligence 與 DeepSeek 兩篇生活分享：iOS 27 日期、Siri AI 系統需求、V4.1-Flash 模型卡的推論框架說法查證更正
status: done
priority: P2
area: docs
owner: claude-opus-5
claimed_at: 2026-09-15T15:44:31Z
created_at: 2026-09-15T15:44:25Z
completed_at: 2026-09-15T15:59:24Z
branch: claude/fact-check-apple-deepseek-packs
depends_on: []
scope:
  - apps/api/app/guides/content/apple-intelligence-guide.json
  - apps/api/app/guides/content/deepseek-beginner-guide.json
---

# Apple Intelligence 與 DeepSeek 兩篇生活分享：iOS 27 日期、Siri AI 系統需求、V4.1-Flash 模型卡的推論框架說法查證更正

## Why

兩篇已上線的生活分享有三處和一手來源不符：

- `apple-intelligence-guide` 寫 iOS 27 在 9 月 15 日推出。Apple Newsroom 的公告日期是 2026 年 9 月 14 日。
- 同一篇的系統需求（iOS 18.1、7 GB、Apple Watch Series 6 起）抄自繁體中文版 support.apple.com/zh-tw/121115。那一版是 7 月 10 日發佈的舊版，描述的還是 iOS 26 那一代。英文版在 9 月 14 日已改成 iOS 27 世代的需求。
- `deepseek-beginner-guide` 寫 V4.1-Flash 的模型卡示範用 vLLM／SGLang 啟動。DeepSeek 寫的模型卡與它連結的 inference 說明都沒有提到這兩個框架。

## Definition of done

- [x] 兩個內容包的日期、機型、系統需求、推論方式都和 2026-09-15 的一手來源一致，重新查過的來源 `checked_on` 為 2026-09-15。
- [x] 兩個 slug 的 `pack_cli lint` 通過，`tests/test_guides_content_pack.py` 與 `tests/test_guides_content_links.py` 通過。
- [ ] 部署後以 `--slug` 更新匯入正式站（本 PR 不匯入）。

## Steps

- [x] Apple：依英文版 121115（9 月 14 日）、127893〈How to get Siri AI〉、Newsroom、apple.com/tw 產品頁更新機型、系統需求與儲存空間、語言段、版本段。另補一段繁中文件仍是舊版的說明，以及 iOS 27 設定路徑與 Siri AI 開啟方式。
- [x] Apple：表格「影像魔杖限 iOS、iPadOS」改為「不支援 Mac」。英文版與舊中文版的 visionOS 清單都有影像魔杖。
- [x] DeepSeek：重寫途徑三的硬體段。「總參數 552B」改為模型卡寫的「骨幹參數 552B」，並補上每 token 啟用 8B／16B。
- [x] 更新來源清單，兩包都卡在上限 20 筆。
- [ ] 部署後：`guides-import` 以 `--slug apple-intelligence-guide` 與 `--slug deepseek-beginner-guide` 更新匯入。

## How to verify

```bash
cd apps/api
PYTHONIOENCODING=utf-8 uv run python -m app.guides.pack_cli lint --slug apple-intelligence-guide
PYTHONIOENCODING=utf-8 uv run python -m app.guides.pack_cli lint --slug deepseek-beginner-guide
uv run pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py
```

在 Windows 上，lint 一報錯就會因為 cp1252 無法印出中文而 traceback，所以要加 `PYTHONIOENCODING=utf-8`。
`sitemap_budget` 警告在改動前就有。

## Notes

- **vLLM／SGLang 的說法怎麼來的。** huggingface.co 模型頁的「Use this model → Local Apps」選單裡有 `vllm serve` 與 `sglang.launch_server` 指令。那是 Hugging Face 對每個模型自動產生的通用範本，不是 DeepSeek 寫的。
  - DeepSeek 寫的 README（`/raw/main/README.md`）只有「Minimal Inference」一節，指向 `inference/README.md`。那份說明自稱是 readable reference implementation rather than a production serving engine，做法是 `convert.py --model-parallel 8` 之後用 `torchrun` 執行。
  - 真正由 DeepSeek 寫出 vLLM／SGLang 指令的是 V4-Pro-0813 的模型卡（vLLM 範例是 single 4×GB300 node）。
  - 查模型卡要讀 raw README，不要讀整頁 HTML。
- **參數量。** 模型卡寫 552B backbone，另有 196B 參數的 Engram。Hugging Face 的 safetensors 中繼資料是 763B params、totalFileSize 約 510 GB。
- **繁中支援文件落後英文版。** 9 月 15 日：
  - zh-tw/121115 仍是 2026-07-10 版。
  - zh-tw/127893 直接回英文內容。
  - 繁中 iPhone 使用手冊仍是 iOS 26 版，設定路徑是「Apple Intelligence 與 Siri」。英文 iOS 27 手冊已改成 Settings → Siri。
  - 英文手冊的舊 topic id（如 `iph22b72984d`）在 iOS 27 版會導回首頁，所以「AirPods 即時翻譯未開放歐盟」這格沒法用 iOS 27 版複核，維持原樣。
  - 繁中手冊與支援文件改版後，這篇的設定路徑段與繁中版說明段要再核一次。
- apple.com/tw/os/ios 與 /os/macos 在 9 月 15 日已沒有推出日期文字，原本只為日期引用，所以從來源移除，讓出上限名額。
- 內容包 schema：`sources` 最多 20 筆，每筆 `title` 最多 200 字元。
- 抓取一律用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 當 User-Agent。
