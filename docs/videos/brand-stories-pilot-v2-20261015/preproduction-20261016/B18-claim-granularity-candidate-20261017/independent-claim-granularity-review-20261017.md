# B18 `t6` 主張粒度修正：獨立離線覆核

2026-10-17，Codex `/root/b18_full_story_sources`。**結論：PASS_OFFLINE_EXACT_DELTA_AND_BINDING；正式製作關卡仍為 HOLD。** 本報告只審這次單筆 metadata 修正；其餘 88 行完整故事與來源審讀見上一凍結候選的 `independent-full-story-source-review-20261017.md`。沒有修改候選劇本或素材，也沒有執行正式 worker／主機／付費工作。

- 本候選 `sha256.json` SHA-256：`1016D3DE91236AF487EEC891E256F43214D71A06BA806409084831F47584E198`；所列檔案實際 hash 全部吻合。它明確以 `CB28AE7BB6AED7A30C639318504E8E11386AEE8DE1404E9B71B1C372C1E40953` 作父版本。
- 獨立逐物件比較父版本與本版：`series.json`、`reuse-intent.json`、`hook`、`origin`、`idea`、`engine`、`now` 的位元組 hash 不變；`turn` 的全部 scene、旁白、視覺資料與 `loops` JSON 相同。65 筆 claim 中**只有 `t6.claim` 改動**，其 ID、景、S2／F12、`UNCHECKED`、note 及其他 64 筆都相同。
- `t6` 原句「做好的盤子從後場放上**直線**輸送帶」改成「做好的盤子從後場放上輸送帶」，現在逐字對應 `turn-s072/db1aee5c`：「他們先在後場完成一盤壽司，再把盤子放上輸送帶。」直線的事實留在下一景 `turn-s073/86198f0e`：「餐台不再只繞著吧台，而是拉成一條直線」，由 `t11` 承接。[發明協會沿革](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?age=high-growth&eid=00026&page=keii) 確實記載新業者在後場製作並放上直線輸送帶；此次收窄沒有增加新史實或改變業者範圍。
- `node build.mjs --check` 退出碼 0：仍是 85 景、88 行、66 插圖、19 卡、65 筆 `UNCHECKED`、0 lint／cute error、0 外部呼叫；靜態正文估時仍為 560.97 秒。沒有測得的 TTS 片長。

**覆核限制：**沿用上一凍結版的完整離線敘事／史料審讀判讀，這次不重稱為新的正式十三題 worker PASS。資料仍標 `worker_pass=false`、`full_story_pass=false`、`full_source_pass=false`、`tts_generated=false`；正式逐章查核、聽稿與成片驗收須另行取得收據。
