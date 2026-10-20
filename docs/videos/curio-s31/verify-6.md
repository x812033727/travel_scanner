# S31 R5｜來源與靜圖提示詞修稿交接（六）

2026-10-20。R4 的獨立文稿盲讀封存在 `/tmp/curio_s31_r4_blind_seal.md`：對 R4 script SHA `899dd8510fbd1a45e0596682df38c6ea18600c356681369ff2ffbde36d56c592`，官方 13 題為 **13/13 YES**。盲讀封存後另一位讀者依 [research.md](research.md) 的固定全文重核 97 句及 96 景提示詞，回執 `/tmp/curio_s31_r4_postseal_audit.md` 對 R4 判定 **BLOCKED**：ly045 多出史書未記的生日宴、ly037 畫出未記的宮內收果、ly077 以聞香代替「味未變」。R5 依該回執成組修正；R4 的 13/13 不延用為新稿的通過證明。

## R5 exact hash

| 產物 | SHA-256 |
| --- | --- |
| script.md | `332c875a835f89b428c124f578c380079976b9e35b396d098b086a56ba08cef2` |
| video.json | `4a0d0bc19c5b2ebbf6982a58a6c1331b6527b6fca4d02a5230e15edeae74c754` |
| claims.md | `83063009c6fec93840e0e6043118f7ed2df691b3e38651bc1590f12ad0ec2127` |

固定古籍版本、原句與每種文本的證據上限沿用 [research.md](research.md)，未添加新史料。R5 仍不指定果園、逐站路線、實際運送日數、荔枝品種、保鮮器具或同批貨身分。

## 來源與提示詞修法

| 位置 | R5 改動 |
| --- | --- |
| ly045–ly046 | 只說《新唐書》另一篇提到貴妃生日，再問這能否補出日期；ly047 才揭禮樂志的奏樂，不再說「生日宴」。[brief.md](brief.md) 的章節問題同步改為生日記載。 |
| ly037、ly077 | 抵京結果改畫讀者對照荔枝畫與只有一點的無標字地圖；兩條時間線改畫讀者對照無字卷與荔枝畫。不畫宮中收果，也不用聞香表示味道。ly030 亦改用讀者與果圖、卷冊呈現欲得鮮果，避免暗示已在宮內交付。 |
| ly016–ly017 | 把「看熱鬧的人」改成追問詩裡「無人知」涵蓋誰，隨即指出詩沒有知情者清單；不虛構場外觀眾。ly016 提示詞改成讀者與閉合詩卷。 |
| ly021–ly022 | 分別呈現幾騎漁陽探使回來、《霓裳》樂聲與第三首的祿山舞；不說後兩首全是宮裡聽到的邊地消息。ly021 圖改成路上回來的一位騎者；它不指為送荔枝者。 |
| ly076、ly078 | 兩句跨白居易果鐘與《新唐書》騎傳的推論，claims 由 `BJ` 改為 `BJ, NBG`。ly046 圖也由指向南方的地圖改成無字曆卷，配合追查日期。 |

## 本地核對與待審門檻

- `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s31`：0 errors、0 warnings；估全片 9.3 分鐘、片頭 45 秒、正文約 8 分 30 秒。
- script、claims、video 的 97/97 ID 順序與旁白字串相同；96/96 正文景為 still prompt，另有片尾一景；10 條不同 setup 的前向 loop。
- `npm run test:docs-videos`：236 pass、0 fail。`npm run check:tasks`：exit 0。`git diff --check`：無空白錯誤。
- 仍須新的、未看舊回執的讀者對本頁 **script SHA** 做官方 13 題盲讀，及另一位獨立讀者對本頁 **script／video／claims SHA** 重核固定全文、97 句主張及 96 景提示詞。兩關完成前不配音、生圖、配樂、合成或進行其他付費媒體。
