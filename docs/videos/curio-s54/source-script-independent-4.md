# S54｜第四版逐句史料與書面畫面獨立覆核

2026-10-20 UTC。**結論：PASS（本版逐句史料與書面畫面）。** 第三版獨立覆核的四項 HOLD 差距均已修妥；第三版已查過的其餘內容在第四版沒有變動。這不是兩位新讀者盲評、TTS 實測、付費插圖或成片 PASS。

## 凍結輸入與固定原文

五份輸入的本次 SHA-256 均與 `author-freeze-4.md` 相同。我再次直接從三個固定 Git 提交的 `raw.githubusercontent.com` 全文 URL 取得原始位元組，重算來源 SHA-256，再讀受影響的原文行。

| 輸入 | 本次 SHA-256 |
| --- | --- |
| `research.md` | `625e52c6085c1ca809b39a0f6f62fea7bc1e11da91614b89a3f8f57ed30fa16e` |
| `brief.md` | `a991fe01f3567d00b65844fc886212d9e7ccea354109516fb8038319c369b132` |
| `claims.md` | `a59dd0bf361c0803bc3ecf048a15e315fd15097c09d90044f41f8458dc52b76f` |
| `video.json` | `689a737cf2f64a5e6c894601f07f318d966a3a3984da9bff4dc15383c2644480` |
| `script.md` | `cef9c47c8a7bc980b327e4753041821a7e35ac2b9fe1ec17581f70441ea40b2d` |
| [A：1839 年法案固定印本 OCR](https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Butterworths-short-s/Butterworths-1839.txt#L9188-L9240) | `f19541ff9faab28b3d61739f09e23b40115fe2220eda870c2d7cd0867758e254` |
| [H：希爾回憶錄第一卷固定全文](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt) | `3bdf96943eea935aec86101874f15aa8f60d518db1437902da52b446f006f939` |
| [L：Leavitt 1848 年固定全文](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt) | `cc4b05beb60da3f29bc3565b9bdcefa8a643bf972454c7c0a14690f5bdd49d5e` |

## 第三版 HOLD 的四項覆核

| 位置 | 第四版內容與原文 | 判定 |
| --- | --- | --- |
| `s54118` 提示詞、主張列 | 畫面現在是 1840 年五月倫敦收件所的 **`empty stock drawer`**；[H L13354–13359](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13354-L13359) 說五月一日開售六天後，沒有任何倫敦收件所領到郵票。主張列已補 P10／該直接行號，與原 P09 的准用日證據分開。 | PASS |
| `s54125` 提示詞 | 未裁整張封套現在由印製處的工人拿著，沒有放入收件所。[H L13361–13369](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13361-L13369) 說印製處仍想交未裁整張，而郵局拒絕把它們交給收件所。 | PASS |
| `s54130` 提示詞 | 現在是 **`early June 1840`** 的倫敦收件所和 **`empty supply shelf`**。[H L13345–13347](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13345-L13347) 記五月一日首次開售；[H L13383–13389](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13383-L13389) 說一個月後倫敦收件所仍未獲供應，兩部門各執一詞。 | PASS |
| `s54141` 主張列與 P12 | 主張列已補 [L L2433–2435](https://github.com/GITenberg/Cheap-Postage_27196/blob/df94d1d290d2b99b1af422c3595438dea38fbdd8/27196-0.txt#L2433-L2435)，其明寫郵局在收進信的辦公處蓋銷記，防止二次使用；研究表 P12 的來源範圍與文字也延至 L2435。原有 [A 第五條 L9230–9240](https://github.com/Anterotesis/statutes/blob/eb9f01613383da6020f6a10b8c600dc92bcb5361/Butterworths-short-s/Butterworths-1839.txt#L9230-L9240) 只支持法定不得重用條件，沒有再被用來單獨承擔銷記時點。 | PASS |

為核實這是窄幅修訂，我在暫存記憶中將 `video.json` 的上述三條提示詞、`claims.md` 的兩處新引證及三處 P12 行號、`research.md` 的 P12 文字和行號逐項還原；三份還原內容的 SHA-256 **各自精確等於 `author-freeze-3.md` 所列第三版雜湊**。`brief.md` 與 `script.md` 本身也保有第三版雜湊。故第三版已逐項審過的其他旁白、卡片及插圖提示詞沒有新改動。

第四版仍有 146 個正文場景（140 條插圖提示詞、6 張工具排字卡）、19 組 `loops` 和三句片尾旁白。程式逐列核對 `claims.md`、`video.json`、`script.md` 的正文 ID、文字與順序，完全一致。重新執行 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s54 --json` 得 **0 errors、0 warnings**；工具估計 149 句、13.9128 分鐘，並非實際 TTS 時長。本版可進入兩位新讀者盲評和後續媒體關卡。
