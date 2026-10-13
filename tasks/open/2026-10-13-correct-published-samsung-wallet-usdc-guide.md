---
id: 2026-10-13-correct-published-samsung-wallet-usdc-guide
title: Correct published Samsung Wallet USDC guide across five locales
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-13T08:14:11Z
completed_at:
branch:
depends_on: []
scope:
  - docs/samsung-wallet-usdc-correction-2026-10-13.md
---

# Correct published Samsung Wallet USDC guide across five locales

## Why

正式站已公開五語 `crypto-news-samsung-wallet-solana-usdc-20261008`，其中摘要、內文與表格仍說轉帳費用及私鑰管理方式「尚未說明」。[Samsung 10/07 官方公告](https://news.samsung.com/us/samsung-wallet-bring-stablecoin-access-eligible-galaxy-users-us/)已明確說：外部相容錢包 USDC 轉帳不收 Samsung 費用（收款端可能有費用）、轉至 60 多國銀行帳戶費用可變；用戶不必自行管理私鑰，Bastion 提供託管，Coinbase 為次級託管。[Solana 原公告](https://solana.com/news/samsung-wallet)與 [Coinbase 原公告](https://www.coinbase.com/blog/coinbase-and-samsung-bring-usdc-to-samsung-wallet)可交叉核對。10/08 CoinDesk 同事件候選 `9c44b4b5-e727-4797-90f9-77445d4a8ace` 已以重複退件，其五語稿也誤寫銀行費用未說明及託管角色；不可直接搬稿取代既刊修訂。

## Definition of done

- [ ] 五語既刊稿準確區分：Samsung 不收的**相容外部錢包轉帳費**、可能存在的收款端費用，以及轉銀行的可變費用；不寫「全部免手續費」。
- [ ] 五語準確寫明 Bastion 託管／Coinbase 次級託管、合資格美國用戶及十月最後一週預計推出；8,200 萬為相容裝置數，非已啟用用戶數。
- [ ] 以官方來源逐語修訂、沿原有已刊 Guide 審稿與發布關卡，讀回五語已發版本、稽核及公開頁修正句。

## Steps

- [ ] 在後台 `/zh-TW/admin/guides` 讀 Guide `9e38d360-a0f7-4d5b-81c4-15af1224fcf2` 五語現有版本、錯句和來源。
- [ ] 核 Samsung／Solana／Coinbase 公告及必要的 Decrypt 原報導，寫審核用更正對照並保存於 `docs/samsung-wallet-usdc-correction-2026-10-13.md`。
- [ ] 逐語修正摘要、正文、費用／託管表格及 FAQ；走可稽核審稿與版本發布，核公開五頁。

## How to verify

從 `/zh-TW/admin/guides?article=9e38d360-a0f7-4d5b-81c4-15af1224fcf2` 核五語已發版本及修訂／稽核；打開 `https://mokaair.com/{zh-TW,zh-CN,en,ja,ko}/life/crypto-news-samsung-wallet-solana-usdc-20261008` 分別查外部錢包、銀行、託管及時程修正句。若遇 429，限速重試並記錄未驗完的語系。

## Notes

2026-10-13 審查者直接讀回繁中公開全文：描述、摘要、正文及表格都有「費用與私鑰管理方式尚未說明」；協作審查者另讀回簡中、英文、日文、韓文同類錯句。候選重複退件的成功提示、最新人工稽核與全站退件 971 已讀回。既刊稿尚未修改，本票維持 open；已刊更正不能靠本地文件或退件候選推定完成。
