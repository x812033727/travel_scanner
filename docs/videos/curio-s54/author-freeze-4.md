# S54｜作者第四版凍結：待獨立覆核

2026-10-20 UTC。這是依 [第三版獨立逐句史料與畫面覆核](source-script-independent-3.md) 的 HOLD 表格所做的窄幅修訂。此作者紀錄不宣告逐句史料、盲讀、媒體或政策 PASS；請審查者按下列精確雜湊重新查核。

| 凍結輸入 | SHA-256 |
| --- | --- |
| `research.md` | `625e52c6085c1ca809b39a0f6f62fea7bc1e11da91614b89a3f8f57ed30fa16e` |
| `brief.md` | `a991fe01f3567d00b65844fc886212d9e7ccea354109516fb8038319c369b132` |
| `claims.md` | `a59dd0bf361c0803bc3ecf048a15e315fd15097c09d90044f41f8458dc52b76f` |
| `video.json` | `689a737cf2f64a5e6c894601f07f318d966a3a3984da9bff4dc15383c2644480` |
| `script.md` | `cef9c47c8a7bc980b327e4753041821a7e35ac2b9fe1ec17581f70441ea40b2d` |

四版只改第三版覆核指出的地方：`s54118` 畫空存貨抽屜，主張列同時標 P09 與消息原文 P10／H L13354–13359；`s54125` 把未裁整張封套留在印製處；`s54130` 畫六月初倫敦收件所的空供應架；`s54141` 加 Leavitt L2433–2435 直接引證郵局收信時蓋銷記的時點，`research.md` P12 範圍延至 L2435。旁白文字未變，因此重新執行 `script` 後 `script.md` 雜湊與第三版相同。

第四版維持 7 章、146 個正文場景（140 插圖、6 張工具排字卡）、19 組 `loops`，另有三句片尾旁白。開頭 8 景書面估計 45 秒；排除開頭及片尾，正文 2,635 個漢字，以每分鐘 325 字估算 **8.11 分鐘**。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s54` 已重產逐句稿；`lint --slug curio-s54 --json` 回傳 **0 errors、0 warnings**，全段旁白書面估計 13.91 分鐘。146 列主張與正文場景 ID、文字逐列相符；實際片長仍待 TTS。

下一關是另一位工作者對本版做獨立逐句史料與書面畫面覆核，並保留兩位盲讀者對劇本的獨立評估。沒有合成語音、繪製付費插圖或送出影片。
