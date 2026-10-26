# 正式v4交付安全收據與完整SHA

這裡的 exact copy 保留原bytes；summary 明確是既有實際收據的摘錄，不是新音檢／QA／上游provider收據。完整大proof及原後臺snapshot留在外部工作目錄，透過[index.json](index.json) fullSHA綁定，不重複複製binary／rawjournal／auth。

| 本地檔案 | bytes | SHA-256 |
| --- | ---: | --- |
| [PT-v3-unknown-provider-outcome.summary.json](PT-v3-unknown-provider-outcome.summary.json) | 3092 | `bc63da45f91d179e4b269f47dcb3d0b64a2724f876e9e4af7f51697fdad1e9d5` |
| [actual-delivery-and-37-download-roles.summary.json](actual-delivery-and-37-download-roles.summary.json) | 25930 | `50b0cce91421d18544e27ec79165351c53ce007a6d0df42fdad0e599ed9ef412` |
| [deliver-forty-branded-v4-checked-caption-assets.root-result.json](deliver-forty-branded-v4-checked-caption-assets.root-result.json) | 54271 | `f9b12728187f34f6efbc55c3ea90471376a3d2704cb448237f8284ffdbb3f981` |
| [forty-branded-checked-caption-helper.author-freeze.json](forty-branded-checked-caption-helper.author-freeze.json) | 4460 | `95d33c3ad079c9b3971f5443f4739189ab91d95c0edaacca1256b7cc4de3f92a` |
| [forty-branded-checked-caption-helper.peer-review.json](forty-branded-checked-caption-helper.peer-review.json) | 6417 | `afcf716c8e8861a114c93593d7ab94cff291c0ae544e1dd6ce5c1ed22bae00b9` |
| [forty-branded-checked-caption-helper.selftests.final-instrumented.json](forty-branded-checked-caption-helper.selftests.final-instrumented.json) | 22925 | `53fb4de283648eb7a297561d13685f8318628953e5d54d691fa2eaf7532d61d3` |
| [forty-branded-checked-caption-native-text.root-review.json](forty-branded-checked-caption-native-text.root-review.json) | 7502 | `2f606801163adb045a6670264bddd062909352361ecbdcde4343357d659166eb` |
| [forty-branded-final.actual-native-qa-step.json](forty-branded-final.actual-native-qa-step.json) | 5413 | `c3714af7e5dbe81f530701a86bdb3d3fad4469bb7df6b525cf3eb8f08448b7dd` |
| [forty-branded-v4-main-helper.peer-review.json](forty-branded-v4-main-helper.peer-review.json) | 8508 | `0283cb7dc2b9ddd9860c6026b22ff133179009fcbbee3d62b1443e996ec8b469` |
| [forty-current-captions.handoff.json](forty-current-captions.handoff.json) | 15928 | `8ebcb7a9fa46728e836d8cf4551ff94f279c9f3f365fbac3a3d9cd395209ed21` |
| [forty-master92-strict-current.2026-10-26T04-02-22-009Z.validation.json](forty-master92-strict-current.2026-10-26T04-02-22-009Z.validation.json) | 1665 | `5de2be3bdb5d02a8866703391fc95070f2607ff7609a691a950bfd2bd466bd79` |
| [forty-pt-branded-R1-v3.root-unknown-outcome-review.json](forty-pt-branded-R1-v3.root-unknown-outcome-review.json) | 1443 | `bdd5318d339910e8428f18bc32833bdf8b7f49e90312b1bb9d91b014e4787648` |
| [master92-and-four-current-audio.summary.json](master92-and-four-current-audio.summary.json) | 13901 | `2e5c3b641c7480cad46d7e812a7ae0da25225b59f5ed914545e3c6fb4cfda239` |
| [qa.json](qa.json) | 4316 | `b14466b19eb9beb3f96ae84b08a538235a6763dcef29a356fd26d2629e2760d2` |
| [series-tts-service-hold.json](series-tts-service-hold.json) | 5127 | `ad19fab46b2044ba5ea34ffd14a2d980d195f363007e456cdb3a02694661c384` |
| [source-snapshots/es.production-before-doc-refresh.json](source-snapshots/es.production-before-doc-refresh.json) | 15060 | `cb5bdb276eef260c9ed53976fe60232a3c232331ba29cb9f5ed46f1fcfc4c4e5` |
| [source-snapshots/pt.production-before-doc-refresh.json](source-snapshots/pt.production-before-doc-refresh.json) | 14543 | `854a5f62e109088684b81466124bc50c030e3a919760fba5f8635604ed1ad5a9` |
| [source74-documentation-change-boundary.json](source74-documentation-change-boundary.json) | 43854 | `fb01d83b8b6423c162b61295a6ebdefd1fbd1373c4449f1764a0cd20b012a116` |

[來源74文件更新邊界](source74-documentation-change-boundary.json)逐項列出製作時、目前工作檔及Git979c SHA，只有四份進度文件改動。

actual大收據fullSHA：

- main＋四M4A：`de3f67369239428ba714b8ff16d7d2bd4ee4ba78bc6e94bee2e87b9416e45268`；05:24:15.249Z，保留oldapproved12。
- CC＋標題說明：`f9b12728187f34f6efbc55c3ea90471376a3d2704cb448237f8284ffdbb3f981`；06:02:27.467Z，25新增下載roles／總37。
- authenticated保存project：`4587ae3ab58da9fa4aaf9a2b74e410256b60bb50a97a42c8ba0d4c02ce3c0aed`；last_synced06:02:26.141214Z，沒有宣稱這是本輪新GET。
- PTv3原driver：`270e87da89dcda63898f8ac657294eca7645dba6ad76f1d5e6955163386c7e62`；原錯誤欄未改，rootbdd531更正HTTP範圍，provider計費仍UNKNOWN。

來源snapshot的dirty es／pt原檔不stage；snapshot fullSHA與不同的Git979c blob SHA分開列在index。只有當root審查freeze後，才能精確stage所列文件。這裡不聲稱GitHEAD的i18n路徑已包含實際製作用語。

原生QA完整[qa.json](qa.json) false10/11、35CPS與ES/PT harderrors均保留；舊approvedBODY QA11不是新版QA。已交外語4/8，all8與overallfalse。普通POST無CAS；server組裝+authenticatedrolemetadata不等於binary下載重算SHA。
