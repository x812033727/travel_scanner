---
id: 2026-09-06-line-link-keyword-chinese-only
title: LINE 綁定關鍵字只認繁體中文，日英韓讀者照著做也綁不上
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T18:18:12Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/line/router.py
  - apps/api/tests/test_line_webhook.py
---

# LINE 綁定關鍵字只認繁體中文，日英韓讀者照著做也綁不上

## Why

`apps/api/app/line/router.py` 判斷「使用者想綁定帳號」的條件是：

```python
if event_type == "follow" or text in {"綁定", "連結帳號", "綁定帳號"}:
```

三個關鍵字都是繁體中文，完全比對。`/alerts` 頁面現在會用讀者的語系告訴他「加入好友後傳送
『綁定』」——那個詞刻意保留繁中而且有測試釘住，因為翻掉了 bot 就不認（見
`2026-09-06-alerts-hardcoded-zh-tw`）。

問題是這樣要求一個日文或韓文讀者去輸入他看不懂、也打不出來的兩個漢字。而且**失敗是無聲的**：
bot 收到不認得的訊息就什麼都不回，使用者只會看到帳號一直沒連上，沒有任何訊息告訴他哪裡錯了。

`follow` 事件本身就會觸發同一段流程，所以剛加好友的人不受影響；受影響的是加了好友之後
才回到網站、需要重新送一次關鍵字的人，以及被封鎖後要重連的人（那條路徑的文案就是叫他重送）。

## Definition of done

- [ ] 五個語系的讀者都能用自己看得懂的字綁定成功。
- [ ] 送出不認得的訊息時，bot 會回一句「我看不懂，請傳送 X」而不是靜默。
- [ ] 現有三個繁中關鍵字仍然有效（已經在用的人不能被弄壞）。

## Steps

- [ ] 關鍵字集合擴充到各語系的等價詞，例如 `link`、`connect`、`連携`、`リンク`、`연결`、
      `계정 연결`，比對前先 `strip()` 與 casefold。
- [ ] 加一條 fallback：文字訊息不在集合內時回一句多語提示，附上目前可用的關鍵字。
      這比擴充關鍵字更重要——它把無聲失敗變成看得見的失敗。
- [ ] 前端 `alerts.line.keywordHint` 的 `{keyword}` 之後可以改成該語系的關鍵字；
      在後端接受之前不要改，`line-connection-panel.test.tsx` 有測試釘住這件事。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_line_webhook.py -q
```

## Notes

- 這是做 `2026-09-06-alerts-hardcoded-zh-tw` 時發現的：把頁面翻成五語系之後，
  才看得出來「照著做」在四個語系是做不到的。頁面翻譯本身不受影響，那張任務已經完成。
- 別把關鍵字改成只接受英文，現有使用者已經在用繁中那三個。
