# C 系列來源收據移植紀錄

2026-10-23 將歷史收據中的 Windows 使用者設定檔絕對路徑前綴一律換為 `<home>`。其餘字元與換行不變；這是公開倉庫主機資訊遮蔽，不改劇本、主張或審查判定。下表列出每個收據遮蔽前後的 SHA-256。

C19 的 PR #1738 與 #1748 在同一路徑留下不同內容；前者原檔另存 `story-everyday-seven-bank-c19/reviews/independent-delta-review-20261023-pr1738.md`，後者保留原路徑。兩版未合成單一查核判定。

| 收據 | 原 SHA-256 | 遮蔽後 SHA-256 |
| --- | --- | --- |
| `docs/videos/story-everyday-bialetti-c16/reviews/author-script-receipt.md` | `02966bb80b9da35a4f3420d4949cf570575554a8f3bf9becbe2f436757d6f22d` | `6967bd93acc68dd950d614905e8fb90d7a52ac5d80c95e86046e406b25b0d208` |
| `docs/videos/story-everyday-bubble-wrap-c04/reviews/transfer-and-lexicon.md` | `09d84d1e8d18a14097814fbc1f3741301da51b526e76b71ca5293f3518dde18e` | `feab74302e4a6f948d96582d5b6f997d47084333083b360805b66850b9725bc0` |
| `docs/videos/story-everyday-camelbak-c14/reviews/blind-narration-v1-coordinator.md` | `2dfb2bbfc82b993eec88bb2a9d22ad4fc26a1008ada1f865d42de9416e656237` | `8ff2da330d98c8b3d5c6aee56590e92f4b554a799920392147c5277cbd620812` |
| `docs/videos/story-everyday-camelbak-c14/reviews/blind-narration-v2-coordinator.md` | `0b53c94bb9e20dda0285b6c6b8d152c0d0bd13832df2013f0122f23b7614aeff` | `a1cb1bd69045c906f5214a3265318c27eeb8479cd7e3437c202e01ac55918b84` |
| `docs/videos/story-everyday-camelbak-c14/reviews/blind-narration-v6-coordinator.md` | `e0b180767eef530dd1003dfb7b71944906394b6d45daf5f1ad2d92399f5bf2ee` | `a1001d75c566f6d9aa60d7b037d631538736d9d2791006f542439cafb249ff1b` |
| `docs/videos/story-everyday-camelbak-c14/reviews/blind-narration-v8-coordinator.md` | `f315a90cd24e0daeeb7107f5f98146e73b9cf2f2efd5c99436674ee4a2e3d78e` | `2a91b3ab7cd89183387597ba12a06c384f37d7b608ade5f3ec5bc1e4200636c2` |
| `docs/videos/story-everyday-fiskars-c18/reviews/blind-v4-reader-1.md` | `07cde955c0acd16a72c94e6d213a7fdb2cb55badedd4bf188134b5cc185990b1` | `e6e7a89873e523777a86f8dcef61ec9e7a0393a5e28efb404775bcf1452ab624` |
| `docs/videos/story-everyday-kikkoman-c08/reviews/blind-narration-v5-3-coordinator.md` | `9bf59c3160c6353d6af920053fdb40dfe062ae8f17c017d074a6d897bc63c9fe` | `4cb07840d274efc5dd795950f894e7ae95074c171e6f2199375b1b7cf37bf144` |
| `docs/videos/story-everyday-oxo-c10/reviews/narrative-reader-v5-a.md` | `bdd2a94cc9e83392a763afdea632ce045dfc27c63c80fededa9ae1ca94096c8d` | `f40f8ca19f614b563da88dd151809cc232b2020cb5a816057c9fe79e225047f3` |
| `docs/videos/story-everyday-oxo-c10/reviews/narrative-reader-v5-b.md` | `9ae826cf9dda03361f859f98815ae9fbe1c7a3fefe7778ad41b9cbc5db797ea7` | `a003277bfd09944a4c673323cedc722dca0e17b3e1cdec43aa8d37d256ad5488` |
| `docs/videos/story-everyday-play-doh-c06/production-pilot.md` | `73f7fb5968fcf25bfbe6564f5507d02396c59d8c9386ef9924ec61ab9049334c` | `b696001d022434ace50d12810cf8a675a8b5a487ba503c9a80d8ba2922c8bf30` |
| `docs/videos/story-everyday-seven-bank-c19/reviews/author-script-receipt-20261023.md` | `9a645a8e48f7bf32c8ae87a483eaf915b46a18aee71de0a15ee398244db807f2` | `71af3140acf42bb98078fa7d42b600ad911153b4cefc6a232f520f890935030f` |
| `docs/videos/story-everyday-ucc-c11/reviews/narration-v6-blind-coordinator.md` | `cdd3d6a033705aae21689ae877745d9b69913cfb6fc22f6dd53eeac508a56c54` | `c943c8547fab0e7f74e6782fd2a363d5160abd4f144af42f40bef86b1b75acc2` |
| `docs/videos/story-everyday-ucc-c11/reviews/narrative-reader-v4-a-author-transcription.md` | `7257f9b8e4a54ee8f4ccf5478c7497468f566d4464eca81b945c57a297a54f4e` | `34082e1548e173a103d70711fb9242a13641ffd6b2ab1a09c1bff55efe056007` |
| `docs/videos/story-everyday-ucc-c11/reviews/narrative-reader-v4-b-author-transcription.md` | `a3615d38334c58c916f8939c893d281e805771ca2b3ef6bfac2258bcee77367e` | `6f72b482f1bf748d5e2e1d7632cfbf4cab395d35162e7a190296a61383af678d` |
| `docs/videos/story-everyday-zippo-c20/reviews/author-script-receipt.md` | `6fe5e933e961657a3e422ad615225f6b87f7e1619476576830477dfc9b628677` | `951a99952154c0a252b1f9d9741d107fa72a90eb50ca205feaf25c17b8003220` |
| `docs/videos/story-everyday-zippo-c20/reviews/blind-v5r1-fresh-1-receipt.md` | `a2bf9c0d97a166b4d7d0f61c86165c0052e8adf43631d33024ac3c63a52ff1b5` | `e7b89ee9824307d4a250df4ca7d3ae99f11c8bfd3b95d0bcb4a4ff058ae4ade5` |
| `docs/videos/story-everyday-zippo-c20/reviews/blind-v5r1-fresh-2-receipt.md` | `5872e8dcefbf26b27b0bbb329a054a6e090f0a6aedc9fcecadb95e7d8921787e` | `00ac65d81ec509a8537bdf8367b403ff322bc123602f5cdb1fdb41a8dada6560` |
| `docs/videos/story-everyday-bialetti-c16/reviews/blind-v6-reader-a.md` | `f11cf01d5f2d8764f2145e0205ecec04b1c072749c72218e817b499c34f671af` | `7c81632d5967d93d3ddf1a2ce6cfc46f10ff86fa55277298bb7e631b6f14d9a7` |
| `docs/videos/story-everyday-bubble-wrap-c04-pilot/production-progress.md` | `ee246e9622ddc9c3dec35f7e7e62ac15f01cb8da7b6584141cdafa9cd8b4bb6d` | `38052afa40c29632fdb88671ff69471c29afe1c55ad70eb38a5146ca65298955` |
| `docs/videos/story-everyday-pyrex-c12-script/reviews/blind-narration-v2-a-b-holds.md` | `3dc654eead53e0077cb533eeb19624e05312edb9f0da9f7ba2544735abafb649` | `0b5d63b413df0f3b33416627dce14512ce5621a7051028a158531257ddafdb71` |
| `docs/videos/story-everyday-seven-bank-c19/reviews/blind-narration-a-20261023.md` | `002c40b3c308319c392e00278d16f6a6e1353f98a2f6086c01badfc9697b47d0` | `68d384eee364e1088fc7aea1655715aba4a726f551cf43f347bb53124a14a5f0` |
| `docs/videos/story-everyday-seven-bank-c19/reviews/context-exposed-narrative-review-v4.md` | `ab2f450fae0a640f7658c96bc3d85bfee562d6921bab65c2395abb4bf776f5f3` | `3b37702920835fe7b6add7f2d559d88d4a947d8c25e32419854735c5efa7ad63` |
| `docs/videos/story-everyday-zippo-c20/reviews/independent-blind-v4-reader-a-parity.md` | `6ddd6dd6d0e9b9d0fb2dbeada28cdd5ba4f32b98c66e737a9f16e61c9dc24a8f` | `ed4840cd11517fd32e8e78568cfd4635ad597d0d03f19d7491a4cc1ab35cffeb` |
| `docs/videos/story-everyday-zippo-c20/reviews/reader2-v4-receipt.md` | `f3ecce65b0419441fdf50ed8d03f399bed01e79d827ae2a0b060262b49fa4ed4` | `2bf0b05185a192a10df0a6f8a8dccfd3acb85410f6c76096a1bd85a34c0f604e` |
