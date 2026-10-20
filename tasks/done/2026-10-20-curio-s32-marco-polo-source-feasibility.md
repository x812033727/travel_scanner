---
id: 2026-10-20-curio-s32-marco-polo-source-feasibility
title: Curio S32 Marco Polo original source feasibility
status: done
priority: P2
area: docs
owner: codex-gpt6-s32-source
claimed_at: 2026-10-20T06:16:11Z
created_at: 2026-10-20T06:16:06Z
completed_at: 2026-10-20T06:22:12Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s32
---

# Curio S32 Marco Polo original source feasibility

## Why

題庫 S32 把「沒寫長城、茶、纏足」和「紙幣、鹽稅細節吻合」直接推向馬可波羅是否到過中國的二選一結論。站主要持續做新的歷史系列；先找可重讀原文，確認這集能否講出來源支持、至少八分鐘的故事，避免把沉默、後世編校或概述當成親歷證明。

## Definition of done

- [x] 固定可讀《馬可波羅遊記》及《元史》原文版本，指出精確段落、史料層級與可說／不可說界線。
- [x] 給出可開稿的安全 A 案、候補 B 案和必須延後的題庫結論；此票不製作劇本或付費媒體。

## Steps

- [x] 查無其他 Curio S32 認領，持有 `docs/videos/curio-s32` 窄 scope。
- [x] 從固定 GitHub commit 完整讀取 1903 年 Yule–Cordier 英譯校注兩卷及 Kanripo《元史》卷 93／94。
- [x] 比對紙鈔、鹽政、長城等遺漏的說法，記下版本差異與不可驗證的學界共識。
- [x] 留下 [`research.md`](../../docs/videos/curio-s32/research.md) 供下一輪企劃。

## How to verify

重開 `research.md` 所列固定 `raw.githubusercontent.com` 連結，核對 SHA-256 與行號；或讀 GitHub 固定 commit 的 blob。`npm run check:tasks` 必須 exit 0。

## Notes

可行但須**縮題**：推薦 A 案問「一張紙幣，能證明馬可波羅到過中國嗎？」，《遊記》紙鈔制度與《元史》〈鈔法〉可跨文本核對；相符不能證明親身到訪，缺寫長城也不能證明未到。卷二「受可汗派去查杭州稅」只見 Pauthier 一版，G 本只說聽過帳目，不採為確定履歷。原題庫「中文史料找不到名字」及「學界多數認為到過」沒有足夠原文與現代學術全文支持，先不寫入稿。Gutenberg、Brill、Crossref、OpenAlex、Cambridge、JSTOR、Wikisource 均在本雲端遭 CONNECT 403；固定 GitHub 鏡像 HTTP 200。沒有付費請求。
