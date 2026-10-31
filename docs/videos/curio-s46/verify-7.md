# S46 R4｜`bkw008` 畫面提示修正

2026-10-20 UTC。依 [R3 獨立覆核](verify-6.md)唯一書面畫面 HOLD，將開場倒敘至 1849 年文憑典禮的 `bkw008` 提示中 `one medical applicant in plain 1840s clothing` 改成 `one adult woman in plain 1840s clothing`。提示的教堂、文憑盒、光線及其他文字都未改。以 R3 `video.json` 備份作結構比對，**僅此一個 `data.prompt` 欄位有差異**；`research.md`、`brief.md`、`claims.md`、`script.md` 均與 R3 位元組相同。R3 已通過的 131 句史料旁白因而維持原版；沒有重新生成劇本。

| 檔案 | R4 SHA-256 |
| --- | --- |
| `research.md` | `99b8903431cb1e8a317513f260c33a5cd0d141aefec54b4c0a5ba205c126055d` |
| `brief.md` | `8012cab4d8c574a7b4f90f6e02d0ea1d2a96f63919c2377ac5c35de90bec9262` |
| `claims.md` | `b4819dd7fcec82efa2df0946be167abea7b21bfd0f231711923f5e09c2c657a9` |
| `video.json` | `af80b750d864fdd634ce0d6002f0edcf484b78959ae2ccee97d31c6863dd2061` |
| `script.md` | `6db66fc2bc2f671c76d28982162d6c7c304c9722bbde41aed8a67e58c607c918` |

原書仍是 GITenberg `65496-0.txt`，commit `16787df4911754c8e0401d12c896b943768f5d8d`，SHA-256 `b52caf559d763349953fe31101016cfb2d68662f152c28a564b6a6b93cac8ec6`。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s46 --json`：**0 errors、0 warnings**。R4 書面畫面須由獨立覆核者核定；兩名全新敘事盲讀者仍待審同一劇本。未生成付費媒體、未推站台、未聲稱站主已親自核准。
