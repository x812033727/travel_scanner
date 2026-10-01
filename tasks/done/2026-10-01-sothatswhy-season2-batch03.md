---
id: 2026-10-01-sothatswhy-season2-batch03
title: 原來如此第二季第三批：B48 S44 T33 A36 製作包與獨立審稿
status: done
priority: P2
area: docs
owner: codex-sothatswhy-batch03
claimed_at: 2026-10-01T06:21:40Z
created_at: 2026-10-01T06:21:39Z
completed_at: 2026-10-01T06:42:09Z
branch: codex/sothatswhy-season2-batch01
depends_on:
  - 2026-09-29-so-that-s-why-vet-the
scope:
  - docs/videos/so-thats-why/season2/B48.md
  - docs/videos/so-thats-why/season2/S44.md
  - docs/videos/so-thats-why/season2/T33.md
  - docs/videos/so-thats-why/season2/A36.md
  - docs/videos/so-thats-why/season2/reviews/batch03/
  - docs/videos/so-thats-why/season2/batch03-packaging.json
  - docs/videos/so-thats-why/season2/validate.mjs
---

# 原來如此第二季第三批：B48 S44 T33 A36 製作包與獨立審稿

## Why

接續使用者「繼續」，從尚未處置的92題選信用卡網路、冰塊昇華、非整點時區、QR錯誤修正。文字包累計由8到12，沿用草稿#1075與依賴#1073，不生成媒體或正式匯入。

## Definition of done

- [x] 四包有今日原始來源、限制、4000/2000內貼用欄位、480秒六章、各兩支180–220單位Shorts、具體英文原創插畫/AB縮圖與五語JSON。
- [x] 每包不同作者交叉事實、聽眾文字與五語審稿，必要修正閉合，報告及收據綁最終byte SHA256。
- [x] batch03-packaging.json相符，validator三批皆PASS，首二批正文/收據/bundle保持不變。
- [x] 母票及索引12/100、其餘88題未決；本批票在既有草稿PR結案。

## Steps

- [x] 核分支/worktree/遠端/PR碰撞並claim窄scope，比對已做八題和第一季、第三季、品牌故事與AI名詞。
- [x] 撰稿並當天直接查原始來源，未核史料及泛化排除。
- [x] 交叉審稿、修正、最終SHA收據。
- [x] 三批機械檢查、isolated drift拒絕、連結與票務、提交並更新草稿。

## How to verify

node docs/videos/so-thats-why/season2/validate.mjs，--batch=batch02，--batch=batch03；npm run check:tasks；git diff --cached --check。只有本批四列候選題更新，其他96列保持本turn起點，初兩批正文/審稿/bundle byte不變。

## Notes

- 驗收：三批validator全部PASS；isolated valid fixture通過，package/report/bundle drift各以exit1拒絕，unknown batch也拒絕。157個README/四包/四報告本地連結與LF/單一EOF通過；check:tasks驗1239檔，僅既有無關scope警告。僅本批四列候選題改動，原status/check/verdict及首二批正文、報告、收據與bundle保持byte不變。
- A36獨審兩處修訂已由原獨審者重讀final hash閉合；各包有不同作者的PASS/TEXT_ONLY報告與byte SHA收據，五語與章長只驗文字。
- 本票在草稿#1075更新並結案；母票保持開放（12/100，88未決），不表示已合併、完成長片逐字稿或媒體驗收。

- B38與品牌A25同問題，這批不做；改選沒有Visa主題品牌故事的B48。時區品牌A09講鐵路制度起源，T33只講UTC偏移與日期換算；S07講浮冰密度，S44只講固到氣；品牌A14講條碼歷史，A36只講錯誤修正及結構限制。沒有重寫既有相同問題。
- 個別請求處理模式與實際應用不能泛化。沒有金融建議、食安全域保證或真QR掃描實測，所有秒數為企劃估計。
