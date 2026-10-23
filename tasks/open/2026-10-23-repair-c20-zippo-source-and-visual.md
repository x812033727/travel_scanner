---
id: 2026-10-23-repair-c20-zippo-source-and-visual
title: Repair C20 Zippo source, visual and narrative holds
status: in-progress
priority: P1
area: docs
owner: codex-root-c20-script
claimed_at: 2026-10-23T05:30:28Z
created_at: 2026-10-23T05:30:23Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/story-everyday-zippo-c20/script.md
  - docs/videos/story-everyday-zippo-c20/script-source-notes.md
  - docs/videos/story-everyday-zippo-c20/visual-plan.md
  - docs/videos/story-everyday-zippo-c20/visual-plan.json
  - docs/videos/story-everyday-zippo-c20/reviews/author-script-receipt.md
---

# Repair C20 Zippo source and visual holds

## Why

第一輪獨立來源／配鏡審查 [PR #1732](https://github.com/x812033727/travel_scanner/pull/1732) 對 C20 作者稿 68 句判 65 PASS／3 HOLD：`c200207` 未說清 1933 售價／承諾是後來公司回顧；`c200310` 暗示看過同期銷售文件；`c200410` 把 1997 博物館開幕錯接到今日維修展示。三處已經 [PR #1735](https://github.com/x812033727/travel_scanner/pull/1735) 重核 PASS。兩位獨立只讀旁白 [PR #1739](https://github.com/x812033727/travel_scanner/pull/1739)、[PR #1741](https://github.com/x812033727/travel_scanner/pull/1741) 又一致指出開場未兌現的創辦動機問題與支線。本票接續將已核來源的主線修成可回答的作者稿；目前 v5 為 60 句，不擴大到付費或匯入。

## Definition of done

- [x] 三句旁白、來源註記及相配的兩張後製字卡／一個概念插圖都回到可說證據範圍。
- [x] 來源三句修訂版曾以 68 句／68 鏡、58 張概念插圖／10 張字卡通過獨立差異重核；歷史雜湊保留在作者收據。
- [x] v3 作者稿 64 句／64 鏡、55 張概念插圖／9 張字卡同 ID、同序，四檔新雜湊記入作者收據，推送原 draft PR #1728 並保持 `no-auto-merge`。
- [x] v5 60 句／60 鏡、53 插圖／7 字卡已同步稿件、逐句來源與兩份配鏡。
- [ ] v5 全文來源／配鏡及兩份新的純旁白盲讀均 PASS，才請站主核稿。

## Steps

- [x] 按 PR #1732 原始 Zippo 公司史及博物館頁的可見敘述窄修 `c200207`、`c200310`、`c200410`。
- [x] 同步第一輪 `script.md`、逐句註記、分鏡 Markdown／JSON 及作者收據，重算四檔雜湊。
- [x] 讀兩份盲讀的共同 HOLD，改問可由史料回答的保修邊界，收緊戰時、博物館及六億支支線。
- [x] 跑 64 句／64 鏡結構及 task/diff 檢查，提交／推送。
- [ ] v5 請非作者全文重核，兩位新讀者只看 v5 投影；三份 PASS 後才送站主。

## How to verify

以 `git show :<path>` 的位元組算 SHA-256；比對 v5 的 60 個旁白 ID、來源註記、Markdown 鏡頭和 JSON 的 ID／旁白／提示詞同序相同。執行 `npm run check:tasks`、`git diff --cached --check`；在 GitHub 讀回 PR #1728 的 draft、head、`no-auto-merge` label 與未啟用 auto-merge。新版由非作者全文重開原件；舊 68 句審查與盲讀不能用來核准新版。

## Notes

第一輪避免把後述 1933 售價及保證說成同期商品卡，也不把現今 Repair Clinic 倒定年到 1997；1997 是擴建後新館，第一間較小的館於 1993 年已開幕。v3 保留其區分，並移除不服務保修主線的六億支段落。獨立全文審查 PR #1746 再指出五處英國表格／寄件路線及虛構修復結果的誤導；該 v4 窄修稿當時紙上估約 521.8 秒，不是實際 TTS；v5 現況見下文。

v3 作者 head `d9d70e3fa8be4b73283847de0ae17ad2993f82e1` 曾推到 PR #1728；該次 GitHub 讀回是 draft、`no-auto-merge`，沒有 auto-merge request。v4 64 句只讀旁白歷史投影另存於 b16f 暫存目錄，SHA-256 `0AB3EE39F253B19604618BDF70424DBEEDA51711561673B3120A06563697F761`。`node tools/video/cli.mjs lint --help` 在此工作樹因缺少本機 `pinyin-pro` 套件於載入階段退出；不宣稱影片 lint 通過。當時的 v4 窄修已重新跑結構比對 64/64 與 `npm run check:tasks`；`git diff --cached --check` 尚待 Git 索引鎖移除後重跑。索引鎖精確刪除遭自動審查 `blocked by policy`，已請站主手動移除，未繞過。

## v5 交接（2026-10-23）

兩份 v4 盲讀 [PR #1755](https://github.com/x812033727/travel_scanner/pull/1755)、[PR #1757](https://github.com/x812033727/travel_scanner/pull/1757) 均 HOLD；v4 來源／配鏡 64/64 PASS 不覆蓋 v5。作者已把英國內膽劇透留到第五章、專利問答改成結構回收、戰時與博物館支線移除，尾聲 c200608 才回答主問。v5 60 句、53 插圖、7 字卡，MD／JSON／來源註記與逐句旁白 60/60 同序。開場 237 字元紙上約 56.9 秒；片頭後正文 2,176 字元紙上約 522.2 秒。正常語速 TTS 未實測，無付費、匯入、上傳或發布授權。

只讀旁白投影位於 C:\Users\x8120\.codex\worktrees\b16f\travel_scanㄐ\c20-zippo-narration-v5-author-20261023.txt，SHA-256 1065DBB1EA191F78A20286F6B76F64997D99D8B0C735E6168F974CFBC767F2CD。作者四檔確切暫存 blob SHA-256 見作者收據。下一步由非作者全文逐句重開一手原件、逐鏡檢查，並由兩位互不參照讀者只讀此新投影；三份新版收據全 PASS 才可請站主核稿。
