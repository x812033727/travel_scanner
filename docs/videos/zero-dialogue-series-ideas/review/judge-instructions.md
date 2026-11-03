## 評分表（每一份作品各打一次，100 分）

| 軸 | 滿分 | 評什麼 |
| --- | --- | --- |
| hook | 15 | 前 2 秒：第一格就有衝突或怪事，讓人不想滑走 |
| premise | 10 | 一句話說得出的設定，一般人一看就有共鳴 |
| laughs | 20 | 笑點密度：真的會笑的點，不是只有可愛 |
| escalation | 10 | 情況一次比一次糟或荒謬，不是同一個笑點重複 |
| surprise | 15 | 至少一個觀眾猜不到、但回頭看合理的反轉 |
| character | 10 | 角色的反應有個性、具體，不是空泛的形容 |
| payoff | 10 | 結尾收得有力，有重看或追下一集的理由 |
| share | 10 | 看完會想轉給某個具體的人 |

誠實打分，不要客氣；你在滑 Shorts，這支不好笑你會直接滑走。七份之間要拉開差距。

## 回覆格式

只回一個 JSON 物件，不要任何其他文字、不要 markdown 圍欄：

{
  "judge": "<你的代號>",
  "works": [
    {
      "work": "A",
      "scores": {"hook": 0, "premise": 0, "laughs": 0, "escalation": 0, "surprise": 0, "character": 0, "payoff": 0, "share": 0},
      "total": 0,
      "beats": [{"shot": "s04-xxx", "joke": "這一鏡的笑點", "funny": 3}],
      "would_scroll_away_at": "鏡號，或 null（看完）",
      "fixes": ["具體到哪一鏡、改成什麼"]
    }
  ],
  "most_want_to_follow": {"work": "X", "why": "為什麼最想追這個系列的下一集"},
  "ranking": ["由好到差的作品代號"]
}

beats 的 funny 是 1–5：1 不好笑、3 會心一笑、5 笑出聲。works 要包含全部七份。
