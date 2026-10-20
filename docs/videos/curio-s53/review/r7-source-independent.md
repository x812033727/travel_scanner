# S53 R7｜史料與書面畫面獨立差分覆核：PASS

2026-10-20 UTC。此 PASS 僅適用以下精確檔案的來源、逐句主張和書面畫面；敘事隔離雙盲、政策、新語音與成片仍須另驗。

| 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `8e44f47693dd75ad0a7509ab0f495c06adcc2e614b8c8bc09a51559d7202a27c` |
| `research.md` | `2e61530c650852281402476041175154ee69c414daf7431d6aa0db352e7c3d22` |
| `claims.md` | `bb865641a72e06c8883b3706d440f838d16996c3d8328f7cbd77a8f8856ab74e` |
| `video.json` | `472bd73d16b25a4c8bec53d8e9cca8024ec159f367352e2a7b03bc2a8b299b54` |
| `script.md` | `a5931c83a5fcd448b83a8be9d2865c904672fa09ce4f5bec6388d74fad3a58ec` |

重新下載 [固定 1913 年救濟調查全文](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt)，SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`，與研究表一致。[L5011–5018](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L5011-L5018) 說 Associated Charities 為部分家庭搬修小屋，工作從 1907 年 7 月至 **1908 年 6 月下旬**。R7 `s53096` 現明說「直到一九〇八年六月下旬」，修復 [R6 獨立覆核](r6-source-independent.md)指出的「那年」歧義；沒有把慈善機構的部分小屋外推成全部遷走的 5,343 棟。畫面仍是普通小屋牆邊的匿名工匠修繕，不冒充現場原照片或暗示只靠他一人完成搬遷。

R7 `video.json` 僅一處「直到一九〇八年六月下旬。」；逆向換回「直到那年六月下旬。」重現 R6 SHA `429789688823f0162d5153d88b759baba7943ca8bb2e8c70191c9d478e66411e`。`claims.md` 同法重現 R6 SHA `72b5c0a33b0cf119193a6a6aa6edd6fc70819d5aedc915d8f3b0b00e4cfad152`。R6 其餘五句已在該輪直接核過固定原文，R5 其餘場景則有 [逐句獨立審核](r5-source-independent.md)。本版 127 句的分鏡與主張 ID／文字仍相符，`lint --slug curio-s53 --json` 為 **0 errors、1 warning**：工具提醒 `一九〇八年` 在三個事件句重複。這是保留明確年份以免誤讀 1907 年的編輯選擇，不影響史料或畫面 PASS；語音辨識仍須用新稿實測。
