# S49 R15｜固定來源與書面畫面獨立差分覆核

2026-10-20 UTC。**PASS**，僅限下列 R15 精確檔案的來源、逐句主張及書面畫面；查核者未撰寫 R15 稿件，也未生成或驗收圖片、音訊或影片。

| 固定檔 | SHA-256 |
| --- | --- |
| `brief.md` | `b9658ef9df619b6c92ba440ff395065a7702206690a72be863da24bcf098e8e9` |
| `research.md` | `f5da15ac571478389b9b9920832f79434f83af0d312cb84747dcdb680a667750` |
| `claims.md` | `a9e869d51c898ad1cdd11d02291aff52198067c3cc8c154db899205fedc351f5` |
| `script.md` | `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a` |
| `video.json` | `1cc788913568dc241e57221692b979fb9a699c7c0c36becacdb3e0c65109a37d` |

我從 `research.md` 所列兩個固定 GitHub commit 的 **raw URL** 重新下載完整原文，以逐位元組比較核對本地檔。Locke 名下 1859 年重印本 L SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`；Jacoby 1902 年評論 J SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`。兩份下載均與研究檔記載的本地原文位元組相同。L 是 1835 年《太陽報》文章的**後出重印**，並非已查得的 1835 原報頁；J 是後出分析及引文，並非第二份獨立月面觀測。

| R15 差分 | 獨立對讀結論 |
| --- | --- |
| `moon064` 旁白、`claims.md` 錨點和提示詞 | L [804–806](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L804-L806) 逐項寫樹形似橡樹、闊而有光澤的葉似月桂、黃色花串從樹枝下垂。新版中文是忠實壓縮，直接錨點正確。畫面只讓讀報人於乾淨紙頁畫闊葉樹與垂花；未把它做成原報影像、真月面照片或 Herschel 真觀測，亦無來源矛盾。前句 `moon062` 已稱「紙上的」山景，`claims.md` 仍明標虛構報導的想像畫面。 |
| 刪 `moon075`、改 `moon076` | L [1009–1015](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L1009-L1015) 確有二足海狸、幼崽、小屋及煙；`moon074` 把用火明確限定為文章由煙所作推論。刪去再次說「想像海狸不是標本」的 `moon075`，不刪掉必要來源界線。新版 `moon076` 明說「這片紙上月面」，只向下文的有翼居民提問，沒有暗示真實月面居民；原提示詞仍是印刷工人面對未完成的乾淨草圖。`moon076→moon082` 的 loop 端點仍存在。 |
| 改 `moon083` | L [1175–1193](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L1175-L1193) 先寫約半英里的視距，換鏡後又聲稱表觀近至八十碼；新版提問「下一段觀測距離」有確切原文支撐，緊接的 `moon084` 回答八十碼。提示詞未改，是讀者在有翼身影草圖上用放大鏡，沒有呈現為真觀測器材。 |
| 刪 `moon097` | L [1410–1495](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L1410-L1495) 的神殿和居民吃果子仍由 `moon096` 以「故事」限定；L [1525–1535](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L1525-L1535) 隨即寫隔天鏡片意外，接 `moon098` 的問題並無史料跳接。刪去重複的「不是建築遺址觀測資料」句，未把神殿或火災變成已核實史實。 |

**差分範圍核驗：**從 R15 `video.json` 只回復 `moon064/076/083` 的 R14 景，插回 `moon075/097`，序列化後 SHA-256 恰為 R14 凍結值 `8297aff2b6ebafec29bb192e7070ebaa9913ed6f321ff4bcdb2ac53827b4f95a`。同法回復 `claims.md` 的五列，得到 R14 `6429496dad004e2e4c1d6b1def31e1c9631a08bad4b2ae0529240ba12f12d91d`；回復並重編號 `script.md`，連同 R14 生成器尾註，得到 R14 `0903ccc03e433c44d7f41f9ebf2325a6c051d7be50622bba5209a87d1802d2e1`。故未發現上述項目外的 R14→R15 稿件差分；`brief.md`、`research.md` 雜湊未變。未改段落沿用 [R14 獨立來源結論](r14-source-independent.md)，但本結論只綁本頁 R15 雜湊。

逐一比對 R15 的 128 個編號景、`claims.md` 列及 `script.md` 旁白，ID、順序與文字一致；另有片尾三句，合計 131 個唯一 line ID。`moon075/097` 不在正文、主張表或編號景；11 個 loops 的 setup／payoff 全在。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s49 --json` 回報 **0 errors、0 warnings**，`git diff --check -- docs/videos/curio-s49` 通過。這是固定原文及**書面**畫面的 PASS；R14 敘事 HOLD、舊音訊與任何媒體關卡均不由此移轉。
