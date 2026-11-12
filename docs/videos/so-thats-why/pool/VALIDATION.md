# 第七十二批素材池驗證

由 4,299 增至 4,321 個入選核心。本批是 2026-11-12 第二十二輪素材審視（補讀第十六到十九輪覆核點名的原文）：23 個原提案、22 個新核心，另有退回與作者的不收紀錄。前版 4,299 個入選與 627 組題案逐項保留。[舊庫快照](checkpoint-4299.json) · [第二十二輪紀錄](reviews/material-20261111-round22.json)

提案由八位作者撰寫（F54–F61），另八位未參與撰寫的覆核者（V57–V64）核對作者快取雜湊、重抓來源並逐筆讀工具紀錄。舊核心已有的事實不重計，並在[去重紀錄](DEDUP.md)新增覆核寫明的分題理由。

題案：沒有新增；八題仍後備。可成題長題維持 86 組，題案維持 627 組。

## 本機檢查

- `node tools/video/so-thats-why/pool/cli.mjs build`、`check`：PASS（4,711 筆原題、4,321 個入選、627 組題案、高相似待決 0）。
- `node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`：32 項通過。

這些檢查不代表完整製作稿或成片驗收，本批沒有做搜尋頁的瀏覽器檢查，也沒有讀遠端 CI。
