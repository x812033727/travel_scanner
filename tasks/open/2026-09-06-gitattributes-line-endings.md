---
id: 2026-09-06-gitattributes-line-endings
title: repo 沒有 .gitattributes，CRLF 混入造成整檔衝突
status: open
priority: P2
area: meta
owner:
claimed_at:
created_at: 2026-09-06T00:54:02Z
completed_at:
branch:
depends_on: []
scope:
  - .gitattributes
---

# repo 沒有 .gitattributes，CRLF 混入造成整檔衝突

## Why

2026-09-06 合併 PR #168 時，`apps/web/components/trip-editor.tsx` 報出 3102 行的衝突
——「整個檔案都變了」。實際上那條分支只改了 3 行，其餘全是換行符：分支把檔案存成了
**CRLF**，而 base 與 main 都是 **LF**，git 於是認定每一行都被改過。

這在 Windows 上是常態性風險（這個專案的開發機是 Windows），而且症狀具有欺騙性 ——
看起來像兩個功能大規模衝突，實際上是空白字元。當時我花了不少時間才確認真正的改動
只有三行；下一個人不會知道要往這個方向查。

## Definition of done

- [ ] 倉庫根目錄有 `.gitattributes`，文字檔在倉庫內一律以 LF 存放。
- [ ] 之後在 Windows 上編輯並提交，不會再把整個檔案的換行符翻掉。

## Steps

- [ ] 新增 `.gitattributes`，至少涵蓋 `* text=auto eol=lf`，並對真正的二進位副檔名
      標 `binary`（圖片、字型、`.ico`、`.png`、`.woff2` 之類）。
- [ ] 確認需要 CRLF 的檔案（如果有 `.bat`／`.cmd`）另外標 `eol=crlf`。
- [ ] 檢查倉庫裡現有的檔案有沒有已經是 CRLF 的（見下方指令），有的話一次正規化。

## How to verify

```bash
git ls-files --eol | grep -v 'i/lf' | head        # 應該只剩刻意的例外
git add --renormalize . && git status --short     # 正規化後應該沒有意外的大量改動
```

之後在 Windows 上改一個 `.tsx` 存檔提交，`git show --stat` 只應該顯示實際改動的行數。

## Notes

當時的判斷方式，留給下次遇到「整檔衝突」時比對：

```bash
base=$(git merge-base HEAD origin/main)
git diff --stat $base HEAD -- <file>          # 1553 insertions / 1549 deletions（可疑）
git diff --stat $base origin/main -- <file>   # 2 insertions / 2 deletions（正常）
git show HEAD:<file> | file -                 # "with CRLF line terminators" ← 兇手
```

解法是以 LF 那一側為底、把另一側真正的改動用 `tr -d '\r'` 正規化後重新套上，而不是
手動去對三千行衝突標記。

順帶一提：`apps/web/AGENTS.md` 裡那段 Next.js 提示是 `next dev` 自動寫回的，
不是誰忘了刪 —— 把它跟工作一起 commit 才會讓工作區乾淨。
