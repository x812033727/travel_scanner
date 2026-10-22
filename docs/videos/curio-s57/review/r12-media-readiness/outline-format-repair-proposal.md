# S57 outline card format: narrow repair proposal

**Proposal only; no `brief.md` bytes changed here.** `review-push --gate outline` sent a pending card, but reported `the brief has 0 options; the judge takes 2 to 3`. The site's `outlineOptions` parser reads only lines beginning `### 選項 A：…` / `### 選項 B：…`, followed before the next heading by `一行說明：…` and `開場鉤子：…`. It does not parse the current `## A／B 案` Markdown table. The current card therefore cannot express a valid A/B choice.

Minimal authored change: replace only that table with two option blocks, keeping its original A/B titles and explanations. Supply a short hook for each from its existing premise:

```markdown
## A／B 案

### 選項 A：找到人之後，還有第二個選擇（推薦）
一行說明：從李文斯頓在烏吉吉缺物資開場，沿相遇、勸回家、短暫同行、補給重到手與兩人分路走到答案。S 與 L 兩個視角都能逐段查；節拍比單純還原名句更有轉折。
開場鉤子：「一本五道封印的日記將隨史丹利往海岸走，日記主人會同行嗎？」

### 選項 B：名句到底說了沒有？
一行說明：以「Dr. Livingstone, I presume?」查名言真偽。S 寫了、L 沒記，缺錄音或同場獨立逐字證詞；只能得到「史丹利出版書如此寫」，無法將十分鐘問題徹底回答。故不用 B。
開場鉤子：「那句著名英文招呼，真有兩名當事人都記下來嗎？」
```

The `（推薦）` marker is removed from the parsed title by `outlineOptions`. Running the repository parser against the proposed Markdown code block returned exactly two entries, keys `A`,`B`, each with a nonempty title, summary and hook (exit 0). Before any new `review-push`, the author should apply a narrow brief change, verify the parser output, obtain independent delta review and rebind the outline SHA. `script.md` and spoken `video.json` lines need no change for this format correction. The existing one-shot policy request used only the narration and `## 站主觀點`; if those bytes remain identical, compare the new `policyRequest` SHA with the retained request before deciding whether a new Jev call is needed. Do not claim the current zero-option card was a valid owner decision.
