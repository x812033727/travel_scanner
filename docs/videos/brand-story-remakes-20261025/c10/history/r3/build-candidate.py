from pathlib import Path
import json, hashlib, copy, subprocess, re
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
BASE=HERE/'history/r2'
ROOT=Path('/workspace/work/brand-story-20261025/c10-submission-root')
SLUG='story-everyday-oxo-c10-remake-20261025'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
jread=lambda p:json.loads(p.read_text())
def writej(name,value):
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
PROTECTED_BEFORE={
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r1/author-notes.json": "13f02cf2f9b6adca27a5bd9617cea242547e67cd2e44118279331681c5cb0a05",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r1/brief.md": "8d7cfdf5e852bb5c92259ecd3820fc3ab5a2dd80cb161052d5977581cce2913d",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r1/build-candidate.py": "497f4cb145aef8a584d0b3d80a905d2e165df697fdf6618885ec68fa7e47c880",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r1/claims.json": "0a8fa7f5800d711594692b070cba20da5093784184f2e07e752207d3e3125088",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r1/claims.md": "429690a70822b3a53da0c00c64bf8c4f0e49cc8db0609b2e7a469a64592f6af9",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r1/narration-only.json": "ab7fde650b340f9841a81ea33552cb172d7c893114b1a72748b586ffba77375f",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r1/narration-r1.tsv": "470acb201347bf63ede3189e9be4ac7b12c449b1e00d1b8fec3bef93eb79aecc",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r1/native-author-lint-r1.json": "fda240c7cb11182fbbdcb60f17e5d7cd6d726306713fbe3ba0b7c9a0bd519b21",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r1/original-preservation.json": "c0f04d1fb512db863b5bcf4a85cfb5843b4760a5998815c3b00c0cbbca1e3ee3",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r1/prompts-r1.tsv": "fb07dbd5f7f3cdf6d2e273795c57a6ee6227c5a2e50654b6eb9ded81faec5935",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r1/research-original.claims.json": "972924aa2bef4e3283130c8f4abaaf4446814a0c850699c774538e7113978c5e",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r1/research-original.md": "103534b03aa83d10d2d9c2b4c61ac8d0a45bad27384fff79418b44ea5eab4dc7",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r1/reviews/narrative-r1-a.raw.json": "e1f969eb6fa589467642742cd9272dfb7c3a18534e55b6f187a3bb0b928b9709",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r1/reviews/narrative-r1-b.raw.json": "4171f3b25e38bca141ce530532fa71aff2e0d731ac967c921a3876277a5e12dc",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r1/reviews/narrative-r1-binding.json": "20f5fe72e55b270c837a38d406c3cfa44b28e07920a502faffaf51f2b0d6cfae",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r1/reviews/narrative-r1-input.json": "5110869973ac244781e7ba89cb01a90d820f3bb95d11858bf4fd0e5cc789914b",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r1/reviews/narrative-r1.json": "a12e47fbfd86f441dbf8bae4203c7b55a41cc048f611c066945ca731e73ee762",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r1/reviews/source-r1-independent.json": "e5da16e3da4d282203893c82188610d1c03590c502caf1279dc4e9a95efb6784",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r1/script.md": "b9d80fae8d56cadeabf0ed12e6000c7a79707dc6c48197e9acca23e3d7a58712",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r1/series.json": "1921f3ee3513ac7448313a3e45cb2124e0d4fd16f240e526a292f7f5d85d27bc",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r1/verify-1.md": "86cb4fa34b0ed5bf14edc2fb7c41e005b43abc88d1a9b80c53a85e744b9e586b",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r1/video.json": "5c85945061cd8398f291fe6dc27ca55048ed65fe84a4d416fc7d22b050c3e91a",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/author-notes.json": "6f6fb8091c9e6eeda9e81ae163c91bb4f0f36215b912a353b8452204679762b7",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/brief.md": "6dd9206139441969b74723977804ae3568041cb4adfbfb9707926c6ac9e8d006",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/build-candidate.py": "9781851d704734a36560cebcd72cde2f4c3128cd1840258c62dfc19b361a030f",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/claims.json": "90eb9491aa72090db9650072dd1ee86e5c16500f29e6104eba84aca9110cb7d5",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/claims.md": "82ee10109a9d67ee81eb7baf7a9a47748900cd97aad3aabf9a4465ec01113b32",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/narration-only.json": "30b13c7304abe504dd44a31767843fa82972c19174b457efb5d962c815efed0d",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/narration-r1.tsv": "470acb201347bf63ede3189e9be4ac7b12c449b1e00d1b8fec3bef93eb79aecc",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/native-author-lint-r1.json": "fda240c7cb11182fbbdcb60f17e5d7cd6d726306713fbe3ba0b7c9a0bd519b21",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/native-author-lint-r2.json": "7796bde777f52797068d853135a35c20ec28994a9153ee38fee949ca83d7933a",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/original-preservation.json": "c0f04d1fb512db863b5bcf4a85cfb5843b4760a5998815c3b00c0cbbca1e3ee3",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/prompts-r1.tsv": "fb07dbd5f7f3cdf6d2e273795c57a6ee6227c5a2e50654b6eb9ded81faec5935",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/research-original.claims.json": "972924aa2bef4e3283130c8f4abaaf4446814a0c850699c774538e7113978c5e",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/research-original.md": "103534b03aa83d10d2d9c2b4c61ac8d0a45bad27384fff79418b44ea5eab4dc7",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/reviews/narrative-r1-a.raw.json": "e1f969eb6fa589467642742cd9272dfb7c3a18534e55b6f187a3bb0b928b9709",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/reviews/narrative-r1-b.raw.json": "4171f3b25e38bca141ce530532fa71aff2e0d731ac967c921a3876277a5e12dc",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/reviews/narrative-r1-binding.json": "20f5fe72e55b270c837a38d406c3cfa44b28e07920a502faffaf51f2b0d6cfae",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/reviews/narrative-r1-input.json": "5110869973ac244781e7ba89cb01a90d820f3bb95d11858bf4fd0e5cc789914b",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/reviews/narrative-r1.json": "a12e47fbfd86f441dbf8bae4203c7b55a41cc048f611c066945ca731e73ee762",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/reviews/narrative-r2-a.raw.json": "b0827a43936fe68b87cad0edba6ddc03f984c5adaee9f539df8db553f6383f02",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/reviews/narrative-r2-b.raw.json": "5eed238cd2db384e9a3a1ef6c913d9fe46186052e9c8d7a9d72807bc7c1cfb68",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/reviews/narrative-r2-binding.json": "c113c9b24c366f17e469d899d8ab094018257ff93d456ca77c95969e8fcaab38",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/reviews/narrative-r2-input.json": "25bc84968fc2d54c26273cf105eb416755eb4470f1faab4dee7d6e7d8f26fca7",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/reviews/narrative-r2.json": "a06f368caae18b7419216fe486095330db4e04765901031aaa04140524a2084d",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/reviews/source-r1-independent.json": "e5da16e3da4d282203893c82188610d1c03590c502caf1279dc4e9a95efb6784",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/reviews/source-r2-independent.json": "47dbbf69261861b7ad9b84099eff0ceda19199f2f26b2ebe32e97a0057600932",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/runtime-lint-r2.json": "885da2700a67130984e0083ad2f56f6a6a9090ebf6fa431cc1df934acad20bb3",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/script.md": "7c13f1cffbc88c6f608874f013c58c186e72153b089707eb26f61280b87619a0",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/series.json": "b5775cd76d1b694b683e7d7ac2ea3c56072ed2c60f98f603862099b9d0136ebb",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/verify-1.md": "822fe3f70750e5cec138c02f27e4414af363023eb8478273e4301efe9ef39a58",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/history/r2/video.json": "b088f6595787973edd30392cddc6eb65fe5d01c4d1c877e365e558dbd8e4f717",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/narration-r1.tsv": "470acb201347bf63ede3189e9be4ac7b12c449b1e00d1b8fec3bef93eb79aecc",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/native-author-lint-r1.json": "fda240c7cb11182fbbdcb60f17e5d7cd6d726306713fbe3ba0b7c9a0bd519b21",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/native-author-lint-r2.json": "7796bde777f52797068d853135a35c20ec28994a9153ee38fee949ca83d7933a",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/original-preservation.json": "c0f04d1fb512db863b5bcf4a85cfb5843b4760a5998815c3b00c0cbbca1e3ee3",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/prompts-r1.tsv": "fb07dbd5f7f3cdf6d2e273795c57a6ee6227c5a2e50654b6eb9ded81faec5935",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/research-original.claims.json": "972924aa2bef4e3283130c8f4abaaf4446814a0c850699c774538e7113978c5e",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/research-original.md": "103534b03aa83d10d2d9c2b4c61ac8d0a45bad27384fff79418b44ea5eab4dc7",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/reviews/narrative-r1-a.raw.json": "e1f969eb6fa589467642742cd9272dfb7c3a18534e55b6f187a3bb0b928b9709",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/reviews/narrative-r1-b.raw.json": "4171f3b25e38bca141ce530532fa71aff2e0d731ac967c921a3876277a5e12dc",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/reviews/narrative-r1-binding.json": "20f5fe72e55b270c837a38d406c3cfa44b28e07920a502faffaf51f2b0d6cfae",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/reviews/narrative-r1-input.json": "5110869973ac244781e7ba89cb01a90d820f3bb95d11858bf4fd0e5cc789914b",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/reviews/narrative-r1.json": "a12e47fbfd86f441dbf8bae4203c7b55a41cc048f611c066945ca731e73ee762",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/reviews/narrative-r2-a.raw.json": "b0827a43936fe68b87cad0edba6ddc03f984c5adaee9f539df8db553f6383f02",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/reviews/narrative-r2-b.raw.json": "5eed238cd2db384e9a3a1ef6c913d9fe46186052e9c8d7a9d72807bc7c1cfb68",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/reviews/narrative-r2-binding.json": "c113c9b24c366f17e469d899d8ab094018257ff93d456ca77c95969e8fcaab38",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/reviews/narrative-r2-input.json": "25bc84968fc2d54c26273cf105eb416755eb4470f1faab4dee7d6e7d8f26fca7",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/reviews/narrative-r2.json": "a06f368caae18b7419216fe486095330db4e04765901031aaa04140524a2084d",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/reviews/source-r1-independent.json": "e5da16e3da4d282203893c82188610d1c03590c502caf1279dc4e9a95efb6784",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/reviews/source-r2-independent.json": "47dbbf69261861b7ad9b84099eff0ceda19199f2f26b2ebe32e97a0057600932",
  "/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/c10/runtime-lint-r2.json": "885da2700a67130984e0083ad2f56f6a6a9090ebf6fa431cc1df934acad20bb3",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/blind-narrative-v4-reader-a-20261022.md": "193281146d38ca5fbf8cb0c6ab11c2afc16ca978cd620a77ef66630872d154ab",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/blind-narrative-v4-reader-b-20261022.md": "f0056dd8765c514acf5ea1812c097c042c16bbed15466c33c60aa8e4d850addd",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/brief.md": "b0390bbd4555ee59baae0a22f365de0ed709d3084b6846ba051fce1157c83c2d",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/claims.md": "79eace852701703c3960f4b2a01ec7034fa09daea464f7a255e4742d9a6e9dad",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/production-quote.md": "3f17e7cd7ac41004c99f04f069aff996ab13b997660ef4d2e98ac59fed48ee17",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/reviews/canonical-video-preflight-20261024.md": "404d02197cd2296b0e771b7f45d02f9cb708ece25bedf70d1c4140d679b6c23e",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/reviews/independent-canonical-conversion-20261024.md": "229d94d1a7f3394c59363a60fc81dc144075a93d2635a008c222155a5d9902d6",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/reviews/independent-script-source-review.md": "c09c30af2040523458146839f1ca8e397c3f6d1df64545dcb93269a73cf2f5c4",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/reviews/independent-treatment-source-review.md": "a5af14315fa2dfa1a84f970d68ed86b3233d1c51ee287e1c7f7b058b70d5c8a3",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/reviews/narrative-reader-v2-a.md": "efe610965b2f0adc8f709ca8d19ce6a17cfa9e929e3487b418dbba5f0cc7b576",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/reviews/narrative-reader-v3-a.md": "c83927e45cc474d4df822497bff7c0da8cb9128ee0d335e9771ce421a93b5671",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/reviews/narrative-reader-v5-a.md": "f40f8ca19f614b563da88dd151809cc232b2020cb5a816057c9fe79e225047f3",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/reviews/narrative-reader-v5-b.md": "a003277bfd09944a4c673323cedc722dca0e17b3e1cdec43aa8d37d256ad5488",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/reviews/owner-paid-pilot-approval.md": "933412438ae821d0f32c2253f8d60b8e13bc33116b1907a7d757a7ea8a80e371",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/reviews/owner-script-approval.md": "7ce74c7057b308b372a957bb9df0d752602518bf5c0628449828ac997d884090",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/reviews/source-visual-delta-v2.md": "4998b5d41accdcbd5b8afc3840004a50eafa34a7e4ec67698f5c8b05da29696a",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/reviews/source-visual-delta-v3.md": "0b9b9d9ae9bf714b9b86794e9a1b20d01648e613c58f76c18c49e089ddf9e4c0",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/reviews/source-visual-delta-v4.md": "91e73e60124c8def4dc5e8e624872783aa3b346a1e0bd200e816ade2f0b0dd78",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/reviews/source-visual-delta-v5.md": "c7f7a523f744279b429a805b2183a070222e923606da8a22d03c249d45150671",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/script-source-notes.md": "617d9076bc95602df51a383a5a3c0303396b727befe1c7470fdd730c1887fe33",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/script.md": "04a5945ddf219868cdc8e52936447a6d7329544976f6a2dc72a7f3b6841175a1",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/series.json": "7a7e659421beb33bd6d7a155913780174648adbef296904c7e6c557879ec5d0a",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/source-matrix.md": "4deeb89a2028184e73f681fcfd3c9b7fb44463b364bf0d26ac9941f557f156a6",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/treatment.md": "cd541d96e66042ca9a5ede0c4017355c536d16fc7092249c9ccb15d266f4d550",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/verify-1.md": "3405237f3cbdb4502f43ab020f2de25af94fcd55227a213f521bd4d0dcf688fc",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/video.json": "81c2170c32cdddfdb6d9f1f43079f7643361885811fb49be579af1ea0a4122f2",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/visual-plan.json": "a73bdcccc62026aeb6f156bd4479e295c7a5c9b5021a0a4e1382cf67f06cd781",
  "/workspace/work/brand-remakes-source/docs/videos/story-everyday-oxo-c10/visual-plan.md": "c4d5adbda74ff30aab774db2288f9fa8c9134360b4d1d619964bbcf256c0a1ca",
  "/workspace/work/brand-story-20261025/c10-audit/__pycache__/fetch.cpython-312.pyc": "c7a4e56165fec99b43e320b1fb1085a07fcf44d0ad866679c8ad2d5ad2ce1015",
  "/workspace/work/brand-story-20261025/c10-audit/build-research.py": "d633858ca393aff4946969bd9a4530a6b3ad42b6fd76a2aee23b552a4f0f39ae",
  "/workspace/work/brand-story-20261025/c10-audit/canonical-lint-r1.txt": "12cb4d462641a842929c78c2c3dd85091bf04ee59a23773648810aaf069e9711",
  "/workspace/work/brand-story-20261025/c10-audit/claims.json": "972924aa2bef4e3283130c8f4abaaf4446814a0c850699c774538e7113978c5e",
  "/workspace/work/brand-story-20261025/c10-audit/fetch.py": "0d0a3f361c6b263ff9977bc35cf4eb943e9fa623bb2e368c0eb53374d073b43c",
  "/workspace/work/brand-story-20261025/c10-audit/initialized-author-media/story-everyday-oxo-c10-remake-20261025/story/lexicon-transactions/7140124d-95fd-4d44-84c8-6a8471cd0a02.json": "c1e00413c4cc85e2913c8463abe213696cc88fbd9b0e258dfc318ec28d0ed389",
  "/workspace/work/brand-story-20261025/c10-audit/initialized-author-root/docs/videos/lexicon.json": "e91a7de47dfe80156ad3acb21b8a6ee02e6978d6bf085e42c926aa138f9c19d5",
  "/workspace/work/brand-story-20261025/c10-audit/initialized-author-root/docs/videos/story-everyday-oxo-c10-remake-20261025/brief.md": "8d7cfdf5e852bb5c92259ecd3820fc3ab5a2dd80cb161052d5977581cce2913d",
  "/workspace/work/brand-story-20261025/c10-audit/initialized-author-root/docs/videos/story-everyday-oxo-c10-remake-20261025/claims.md": "429690a70822b3a53da0c00c64bf8c4f0e49cc8db0609b2e7a469a64592f6af9",
  "/workspace/work/brand-story-20261025/c10-audit/initialized-author-root/docs/videos/story-everyday-oxo-c10-remake-20261025/script.md": "d0e95fbde9d09405188827bf0bc17cc7397e0fc53c391348bdeea21ce7864ad8",
  "/workspace/work/brand-story-20261025/c10-audit/initialized-author-root/docs/videos/story-everyday-oxo-c10-remake-20261025/series.json": "1921f3ee3513ac7448313a3e45cb2124e0d4fd16f240e526a292f7f5d85d27bc",
  "/workspace/work/brand-story-20261025/c10-audit/initialized-author-root/docs/videos/story-everyday-oxo-c10-remake-20261025/story-lexicon/current.json": "56be815778a92a1a5f8333c9a696be834575a0da7e43b2a610fae0de38201370",
  "/workspace/work/brand-story-20261025/c10-audit/initialized-author-root/docs/videos/story-everyday-oxo-c10-remake-20261025/story-lexicon/events/a4146d813478ce9c7451e1766d2364cc91946fd1afa3ee06cd78837d4249d381.json": "a4146d813478ce9c7451e1766d2364cc91946fd1afa3ee06cd78837d4249d381",
  "/workspace/work/brand-story-20261025/c10-audit/initialized-author-root/docs/videos/story-everyday-oxo-c10-remake-20261025/story-lexicon/versions/d014fecce1a05c703a4c3bf039f64ae833d3f10e72b3ac4b04cd8cbaa42845e0.json": "d014fecce1a05c703a4c3bf039f64ae833d3f10e72b3ac4b04cd8cbaa42845e0",
  "/workspace/work/brand-story-20261025/c10-audit/initialized-author-root/docs/videos/story-everyday-oxo-c10-remake-20261025/video.json": "5c85945061cd8398f291fe6dc27ca55048ed65fe84a4d416fc7d22b050c3e91a",
  "/workspace/work/brand-story-20261025/c10-audit/narration-r1.tsv": "470acb201347bf63ede3189e9be4ac7b12c449b1e00d1b8fec3bef93eb79aecc",
  "/workspace/work/brand-story-20261025/c10-audit/native-author-lint-r1-before-cadence.json": "34d31ffbe238bc798a95c69b3c0d8cd622798e312133c37f77f390f06b8afc71",
  "/workspace/work/brand-story-20261025/c10-audit/native-author-lint-r1-before-final-cadence.json": "783732aa97bdbc8d378ce8058560eeff009d0316802b116daae9e37261b5d319",
  "/workspace/work/brand-story-20261025/c10-audit/native-author-lint-r1-initial-id-errors.json": "3736e172657cc23b0f37df14dbc8ed09221e599b86d65c9e7b24ee1bb59acb52",
  "/workspace/work/brand-story-20261025/c10-audit/native-author-lint-r1.json": "fda240c7cb11182fbbdcb60f17e5d7cd6d726306713fbe3ba0b7c9a0bd519b21",
  "/workspace/work/brand-story-20261025/c10-audit/original-line-claims.json": "d0931ed030105bc2ce4d0bdbd97c5a4aee1d50e8fc3f899e25bd4dd18ad549c8",
  "/workspace/work/brand-story-20261025/c10-audit/original-preservation.json": "c0f04d1fb512db863b5bcf4a85cfb5843b4760a5998815c3b00c0cbbca1e3ee3",
  "/workspace/work/brand-story-20261025/c10-audit/prompts-r1.tsv": "fb07dbd5f7f3cdf6d2e273795c57a6ee6227c5a2e50654b6eb9ded81faec5935",
  "/workspace/work/brand-story-20261025/c10-audit/r1-source-qa/C1.page-27.txt.independent.txt": "6904e3bada85ab6f610e9a2c072a32f497f9fd9be9fe73e9fcb100c2a5b3399f",
  "/workspace/work/brand-story-20261025/c10-audit/r1-source-qa/C3.page-85.txt.independent.txt": "525d89ae265eb867b04312663cc0cc1ef524c76110a396a9e5914fedd21c4b44",
  "/workspace/work/brand-story-20261025/c10-audit/r1-source-qa/C3.page-86.txt.independent.txt": "ebc064343c9c800b9de6e92b0dddfa0eb1261f98a6f540099cad2faa8dfa2105",
  "/workspace/work/brand-story-20261025/c10-audit/r1-source-qa/M1-image-receipt.json": "fd3614e6c9b9d9ecfa47062431cda2668b0e666b4b06f19686c14b87ae797912",
  "/workspace/work/brand-story-20261025/c10-audit/r1-source-qa/M1-original-object.jpg": "75e4d43469b7f7cfe2da9eef335fae15e53a9f01f00f66e46bbb7a84dd6e0956",
  "/workspace/work/brand-story-20261025/c10-audit/r1-source-qa/P0-page-3.png": "81c65a80535034cefc3fc17ff9415da9e1fdeef5098279332e79def87938e2aa",
  "/workspace/work/brand-story-20261025/c10-audit/r1-source-qa/P0.page-1.txt.independent.txt": "a3b9eb08302e57aa2326778e3523fea6a97887b67544c6564bc0c36497427961",
  "/workspace/work/brand-story-20261025/c10-audit/r1-source-qa/P0.page-4.txt.independent.txt": "fcaa53640cc36b66766b6279b4fe0db39c21929747ba5c150f0849be5fe56f0e",
  "/workspace/work/brand-story-20261025/c10-audit/r1-source-qa/P0.page-5.txt.independent.txt": "1b21ff9f7a4b4d6d34687a99ff8903352402f0228394bb9386cb68f61510a1e7",
  "/workspace/work/brand-story-20261025/c10-audit/r1-source-qa/P0.page-6.txt.independent.txt": "80aceeab73f94b71beb61c1d0b847c3c3f1935800c652e8a1ccb537a2a318998",
  "/workspace/work/brand-story-20261025/c10-audit/r1-source-qa/evidence-binding-check.json": "55348ff0ef98a660a2d8fd18791432eda90258e33ca8f12062c3ded6089ee8fc",
  "/workspace/work/brand-story-20261025/c10-audit/r1-source-qa/validate-evidence.py": "f29c65174b5aaa8e8d98ccae9f27491be7c0542e0fff0e5cc67f447c09c01efa",
  "/workspace/work/brand-story-20261025/c10-audit/r1-source-qa/write-source-report.py": "46a13488095f42d94423edc3a7c37a4969571bf8d804ff6bbe147b123a76c173",
  "/workspace/work/brand-story-20261025/c10-audit/research.md": "103534b03aa83d10d2d9c2b4c61ac8d0a45bad27384fff79418b44ea5eab4dc7",
  "/workspace/work/brand-story-20261025/c10-audit/round-1/blind-a.raw.json": "e1f969eb6fa589467642742cd9272dfb7c3a18534e55b6f187a3bb0b928b9709",
  "/workspace/work/brand-story-20261025/c10-audit/round-1/blind-b.raw.json": "4171f3b25e38bca141ce530532fa71aff2e0d731ac967c921a3876277a5e12dc",
  "/workspace/work/brand-story-20261025/c10-audit/round-1/blind-binding.json": "20f5fe72e55b270c837a38d406c3cfa44b28e07920a502faffaf51f2b0d6cfae",
  "/workspace/work/brand-story-20261025/c10-audit/round-1/blind-input.json": "5110869973ac244781e7ba89cb01a90d820f3bb95d11858bf4fd0e5cc789914b",
  "/workspace/work/brand-story-20261025/c10-audit/round-1/blind-instructions.txt": "2a2c87c37aada594ce6766de2a2bc9ef606f8ba539b84a8aad9907b416bfe587",
  "/workspace/work/brand-story-20261025/c10-audit/round-1/narrative-r1.json": "a12e47fbfd86f441dbf8bae4203c7b55a41cc048f611c066945ca731e73ee762",
  "/workspace/work/brand-story-20261025/c10-audit/round-2/blind-a.raw.json": "b0827a43936fe68b87cad0edba6ddc03f984c5adaee9f539df8db553f6383f02",
  "/workspace/work/brand-story-20261025/c10-audit/round-2/blind-b.raw.json": "5eed238cd2db384e9a3a1ef6c913d9fe46186052e9c8d7a9d72807bc7c1cfb68",
  "/workspace/work/brand-story-20261025/c10-audit/round-2/blind-binding.json": "c113c9b24c366f17e469d899d8ab094018257ff93d456ca77c95969e8fcaab38",
  "/workspace/work/brand-story-20261025/c10-audit/round-2/blind-input.json": "25bc84968fc2d54c26273cf105eb416755eb4470f1faab4dee7d6e7d8f26fca7",
  "/workspace/work/brand-story-20261025/c10-audit/round-2/blind-instructions.txt": "2a2c87c37aada594ce6766de2a2bc9ef606f8ba539b84a8aad9907b416bfe587",
  "/workspace/work/brand-story-20261025/c10-audit/round-2/narrative-r2.json": "a06f368caae18b7419216fe486095330db4e04765901031aaa04140524a2084d",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/C1-page-27.png": "02914fa1d478d38aff23f9ffc0ddbdeded7aff68e5bdd535120a20527fd90cb6",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/C1.page-27.txt": "58db6616a054a486338d6039962cf08bc59ad32a68c7d56dbf12ec733933d298",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/C1.pdf": "c0ebfd2e60070a27bda46943f6e4b4443dd7acc0dfcf07360080833415d458ae",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/C1.txt": "7b821ba4b2789560a9ddfc39080f465b447f6dbc38065359b284297bf7ff17e8",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/C2.page-1.txt": "19194b79a8d1fbea5463e4eb66200455f74bfedaa0864069c1df5da9d8b086eb",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/C2.pdf": "25abc404872270deb8de966ad4657b1f8c2b4c9d36428d0666b3370b109d5042",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/C2.txt": "9af9b255cd3ecb1640e9fcc7bb902fafd8c1a0531e3725a274513e0274c8a0a8",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/C3-page-86.png": "9b36496f8f5a2cc4821e2be8e67835eea4bf23a42373a05601f38cc2631694bd",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/C3.page-1.txt": "98f3963b2f944c6432ef02d37659adea65bb7a738fb0574f6e1cb5bb068e2dc1",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/C3.page-85.txt": "9c2c4716ee46098810bb4d4d3d734383b9a494b4af12c7c4ae18642d3657e436",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/C3.page-86.txt": "59c9ad172939f8cd19835289ceef381f71d254673c408ce402ab10be222a7232",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/C3.pdf": "e22eb47183680499a55b95d0f8eb057b68d14c5651b6982b40c1e4f9a55278e1",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/C3.txt": "1c5953ecad685cd0f8e9504c980e945c2dd0bacb6d324333ab3e19755436a2bf",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/I1.html": "e437c6c4718e9be32ca90bd0b61f93b10a70f65d78fa2e26222201137f067c6a",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/I1.paragraphs.txt": "fa7237d1aedb2b3bae7cc966c754de999d1c77fc1c8b047fa2aac425cbc2f396",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/I2.html": "954b31ec5cd1dda118bcb7cd9f513cfe910035b1f1a256e4d271e02d7b227f24",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/I2.paragraphs.txt": "67895072451f96e7172c85229587462abb2b0a8e0cd2d7e53f1648926bef08d4",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/I3.html": "a5895f3f16550fcd51eb5e4749344cd7775e92651d77360108917c5150ebe529",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/I3.paragraphs.txt": "340eaac5e566ec91ec73400f2cf843bbe6d8e7603c1a4ae937669743462c7d9c",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/I4.html": "ad89204ed9ae7a9b41bb25daeeb4a4915e12d70d808b706fcb3e3e7ffea75ead",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/I4.paragraphs.txt": "ee825070e77fb2ac52427357bcbbaca56cb8eabf3d21ab24f3b2ffb225c39b26",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/I5.html": "8ef4f6d1d8f45b3e21985bd194a46fa20b5fcb8d45d9d64e2244dc1d42916396",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/I5.paragraphs.txt": "4b80dd92320aa7099f30c0f12c222c1b47165f7952963d509c7d98e2eb7813f6",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/M1.html": "a0763317f1bb4828e2bcb6271e9a71f56f51324f636910c99eb6f5e7b11f7b9f",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/M1.paragraphs.txt": "eda12acdea78e379d58c623b018e9fe9532842f19808a92c24787c3b91d9f059",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/M2.html": "9dd035a297fbaebd96f43b83eb11e20f119d6aad00bc5fd16202069aaee90230",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/M2.paragraphs.txt": "b98c1ead91e5860fad13ac385d08cd07d9ec505d315f52e7dae7a1284a4b1436",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/M3.html": "f38ffd29a12d3d906f22e05e4538c68d4ecde6615993b8a6e4d7a38eda848cb0",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/M3.paragraphs.txt": "9cb57511d669894f87b87639bfa6ea77f10710285784017b7bacad96f1cbee77",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/M4.html": "d8ad135914fdca00ef051cf925d34e8ef0a1cacbcdcac2da8b1323a9645031b0",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/M4.paragraphs.txt": "4380a19fcb3a3a79bc7381053223a7bd77797103744701ac7ee7a6dd09d59464",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/M5.html": "297b00c72421903cea78332efe9d3a4fb2f7d81257e60bd517e218ad05afc2eb",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/M5.paragraphs.txt": "5b0861127f58d8efe7a79808e2a08f62cc7af163a6b95a6282deb31780904cc5",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/M6.html": "44ebb81882e9c17b94cd0bc6215f79b89a83bff95d0da048a558331e8114b2e6",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/M6.paragraphs.txt": "e65d5b91556ffc16772db63c2da053e35220fde0d1c2eb180c6311e5ec1c0537",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/P0-page-1.png": "a5f7e44957adaa6a882362b42977470539e79b85ac999a12ccb669c12b9cbaff",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/P0-page-2.png": "8206b213167a6c6e000d83bf0fded170cbea0775d430daeb3931989b0b07ccc5",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/P0-page-5.png": "cb1f8bcaad453c2e6ccb0366e227de2c6722a02c377942c09847e459c18fe4eb",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/P0.page-1.txt": "20fdb02721438fdbbbaba32c1308aa145ff7735533c9b0f03597e83e7569720a",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/P0.page-2.txt": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/P0.page-4.txt": "9e66912b96dc7afe4aaa072caf583f93b8c817bebb7edee437b4b0785b582100",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/P0.page-5.txt": "31a7204b032e8e116143766c732f9bde280e7e5eb20b762a46ef1f55ca39f24a",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/P0.page-6.txt": "6d584aafb8330c00ea8f6c47f300445292c953055032f8cee410119eb9759411",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/P0.pdf": "1b46a98b5b97ea3f3ee0e576e8fe3f5b24b537e2c72d2f984229fd53265a6c7b",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/P0.txt": "5c051abe0a30a917e360e7bdd93c9ee2c45a800acfba89aa2add48df72d50871",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/P0meta.html": "9010e5a841cf0acfb13facfaa2c3318bc8118020ec071d15de099eb9a628fd01",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/P0meta.paragraphs.txt": "c95edb7112d213641c697aa1e117776b99a4196b4c407d2c5b60cb917675b5d6",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/P1.page-1.txt": "7e861935238576d9ea70fe8a7dcba2dea8cdccaad8f989ac78fd4e23cea9cf3e",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/P1.pdf": "c7b5f98d7254ad53d6fe9b4f8cb7b8961b34a958dd5f41db46721638da3cb99e",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/P1.txt": "0254d80dc0d6e6fb81dd635a5e1e1e0832e787bae9b70b1d5d0ed12a414b689c",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/P1meta.html": "9010e5a841cf0acfb13facfaa2c3318bc8118020ec071d15de099eb9a628fd01",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/P1meta.paragraphs.txt": "c95edb7112d213641c697aa1e117776b99a4196b4c407d2c5b60cb917675b5d6",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/S1.html": "5fe35f20e6158a044716bc12725dd893edc4c4c05609db9f98edfd1a3d5d6251",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/S1.paragraphs.txt": "23ab89337b2fa8529785b1ba2fbdbd6bc435e7e6a4bd6a4a2de71f03705d2c0a",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/S2.html": "bac7cbaf9782810db2f7bcd0d440350610394bce0b8ed6ba89d6b2f1cb0f581c",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/S2.paragraphs.txt": "a31bcd5d0dd7b93347497576392b902f259d404a473c77f4463544e417c280e6",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/S3.html": "263b46bd27a3fc4bd7df003a5d8e293d58cbe9d6e2596d216226f8802fb92600",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/S3.paragraphs.txt": "4f25c436915708df0badbbac8b5f8d38e125454ecdfa4d3b0f04cafd7f5aa868",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/S4.html": "1ca89a96caab0a09a13571bb2fa68601fa01d0cf9f38a6f8bf0f2a91cdec47f3",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/S4.paragraphs.txt": "99d4fca2e65c4117a6d511257a24ea0070a6db0fc374242cf1b634538bf821c4",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/S5.html": "3bf3dcfbf6317f1948382c04d2ff5c124eda623b527a4546c800a423eda77f1f",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/S5.paragraphs.txt": "51e870a3f6aae7d4541f007306266b4ca06e37b450cf3aba663d10b537139443",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/S7.html": "9b4c3394812ba097de6b19438b1928d155297bb8488db03997af45c7a186d08f",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/S7.paragraphs.txt": "49aec83dc8293040198012872298c1e272f51b80bb827e9d344cd81ed700a02b",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/fetch-manifest-extra.json": "44d4b348d24289c4b12b7bc8f3bfdcbd393673c260f079f837ec37e9cefd6c4a",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/fetch-manifest-final.json": "0b6fa005c41353c6491fdfe1dd4a2f6414d6aa12f5c7c4ce267a90b80e2c8b1d",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/fetch-manifest-original-patent.json": "953744f764c3fbdc50887deeea4d3947b18fd3c93bed65c64ab6fe06aab27695",
  "/workspace/work/brand-story-20261025/c10-audit/source-cache/fetch-manifest.json": "137fda38096ca204bad3ecf1b60b2791e062eca3dae8aa1d26fcb822446d26b7",
  "/workspace/work/brand-story-20261025/c10-audit/write-research.py": "e921af2e4be48558bdefd86791276f1391c7ad2d12c191f52d0555148effc945",
  "/workspace/work/brand-story-20261025/c10-submission-root/docs/videos/lexicon.json": "e91a7de47dfe80156ad3acb21b8a6ee02e6978d6bf085e42c926aa138f9c19d5",
  "/workspace/work/brand-story-20261025/c10-submission-root/docs/videos/story-everyday-oxo-c10-remake-20261025/brief.md": "6dd9206139441969b74723977804ae3568041cb4adfbfb9707926c6ac9e8d006",
  "/workspace/work/brand-story-20261025/c10-submission-root/docs/videos/story-everyday-oxo-c10-remake-20261025/claims.md": "82ee10109a9d67ee81eb7baf7a9a47748900cd97aad3aabf9a4465ec01113b32",
  "/workspace/work/brand-story-20261025/c10-submission-root/docs/videos/story-everyday-oxo-c10-remake-20261025/script.md": "eb17281e57ebe8372550a407e6c6e3f8fce5aa451779d1806f6ca743072e7880",
  "/workspace/work/brand-story-20261025/c10-submission-root/docs/videos/story-everyday-oxo-c10-remake-20261025/series.json": "b5775cd76d1b694b683e7d7ac2ea3c56072ed2c60f98f603862099b9d0136ebb",
  "/workspace/work/brand-story-20261025/c10-submission-root/docs/videos/story-everyday-oxo-c10-remake-20261025/story-lexicon/current.json": "56be815778a92a1a5f8333c9a696be834575a0da7e43b2a610fae0de38201370",
  "/workspace/work/brand-story-20261025/c10-submission-root/docs/videos/story-everyday-oxo-c10-remake-20261025/story-lexicon/events/a4146d813478ce9c7451e1766d2364cc91946fd1afa3ee06cd78837d4249d381.json": "a4146d813478ce9c7451e1766d2364cc91946fd1afa3ee06cd78837d4249d381",
  "/workspace/work/brand-story-20261025/c10-submission-root/docs/videos/story-everyday-oxo-c10-remake-20261025/story-lexicon/versions/d014fecce1a05c703a4c3bf039f64ae833d3f10e72b3ac4b04cd8cbaa42845e0.json": "d014fecce1a05c703a4c3bf039f64ae833d3f10e72b3ac4b04cd8cbaa42845e0",
  "/workspace/work/brand-story-20261025/c10-submission-root/docs/videos/story-everyday-oxo-c10-remake-20261025/verify-1.md": "86cb4fa34b0ed5bf14edc2fb7c41e005b43abc88d1a9b80c53a85e744b9e586b",
  "/workspace/work/brand-story-20261025/c10-submission-root/docs/videos/story-everyday-oxo-c10-remake-20261025/video.json": "b088f6595787973edd30392cddc6eb65fe5d01c4d1c877e365e558dbd8e4f717",
  "/workspace/work/brand-story-20261025/c10-submission-root/runtime-manifest.json": "67e60d094da74bacc9d0c39665287ab6071abe0d4cfca7488cf09a20512387e0"
}
for name,digest in PROTECTED_BEFORE.items():
    assert sha(Path(name))==digest,name
r2bindings={f:sha(BASE/f) for f in ['video.json','script.md','narration-only.json','claims.json']}
receipt=BASE/'reviews/source-r2-independent.json'
assert sha(receipt)=='47dbbf69261861b7ad9b84099eff0ceda19199f2f26b2ebe32e97a0057600932'
r2receipt=jread(receipt)
assert all(r2receipt['input_sha256'][name]==digest for name,digest in r2bindings.items())
old=jread(BASE/'video.json')
oldclaims=jread(BASE/'claims.json')
oldnarration=jread(BASE/'narration-only.json')
old_byid={line['id']:line for scene in old['scenes'] for line in scene['lines']}
old_scenes={scene['id']:scene for scene in old['scenes']}
assert old['slug']==SLUG
CHANGED={'c10a16':'專利描述，拇指與食指伸進兩側孔口，捏住柄尾，必要時便能拉動工具。'}
DELETED=['c10l01']
DELETION_REASON='刪除重述上架轉場及推出年，商店章直接接觀眾拿陌生削皮器的情境；推出日期仍在原標題／說明與來源記錄中，不增新歷史動作。'
doc=copy.deepcopy(old)
scenes=[]
pending_chapter=None
for scene in doc['scenes']:
    original_chapter=scene.get('chapter')
    scene['lines']=[line for line in scene['lines'] if line['id'] not in DELETED]
    if not scene['lines']:
        if original_chapter:
            pending_chapter=original_chapter
        continue
    if pending_chapter:
        assert not scene.get('chapter')
        scene['chapter']=pending_chapter
        pending_chapter=None
    for line in scene['lines']:
        if line['id'] in CHANGED:
            line['text']=CHANGED[line['id']]
    scenes.append(scene)
doc['scenes']=scenes
assert pending_chapter is None
assert doc['scenes'][:9]==old['scenes'][:9]
assert doc['loops']==old['loops']
assert all(loop[key] not in DELETED for loop in doc['loops'] for key in ['setup','payoff'])
series=jread(BASE/'series.json')
writej('video.json',doc)
writej('series.json',series)
brief=(BASE/'brief.md').read_text()
brief=brief.replace('r2 修訂作者候選','r3 修訂作者候選').replace('作者r2，HOLD','作者r3，HOLD')
brief += '''
## r2 → r3 限定修訂

開場九句、17.8公分MoMA館藏單件的範圍、所有既有材料與動作歸屬不改。c10a16僅刪與前句重複的掛鉤用途，保留專利原文的拇指／食指進入兩側孔口、捏住柄尾、必要時拉動工具這個新動作。刪c10l01的推出／上架轉場，商店章直接由觀眾面對陌生工具開始，事件章名移到c10l02，不加摘要或無來源動作。

挖芽眼段及其原來源措辭不改，未為單人no_detour意見擴大修改。沒有填時長；正文及實際語音長度分開記錄。本版仍待新獨立來源／書面配鏡差分與兩位全新讀者，r2通過收據只綁定原r2輸入。
'''
(HERE/'brief.md').write_text(brief)
row_byid={row['line_id']:copy.deepcopy(row) for row in oldclaims['claims']}
rows=[]
narration=[]
chapter=None
for scene in doc['scenes']:
    chapter=scene.get('chapter',chapter)
    for line in scene['lines']:
        row=row_byid[line['id']]
        row['text']=line['text']
        rows.append(row)
        narration.append({'id':line['id'],'scene':scene['id'],'chapter':chapter,'text':line['text']})
writej('narration-only.json',narration)
script=['# C10 OXO｜r3 作者附來源稿','','作者候選，非canonical核准劇本。ID／章名／來源／註解不進旁白。','']
last=None
for row,line in zip(rows,narration):
    if line['chapter']!=last:
        script += ['','## '+line['chapter'],'','| ID | 旁白 | 來源材料／性質 |','|---|---|---|']
        last=line['chapter']
    script.append('| '+line['id']+' | '+line['text']+' | '+(', '.join(row['material_refs']) or '觀眾互動／CTA')+'；'+row['kind']+' |')
(HERE/'script.md').write_text('\n'.join(script)+'\n')
claims=copy.deepcopy(oldclaims)
claims['revision']='r3'
claims['scope']='author r3 source anchors only; all independent r3 verdicts pending'
claims['input_sha256']={f:sha(HERE/f) for f in ['video.json','script.md','narration-only.json']}
claims['r2_input_sha256']=r2bindings
claims['r2_review_sha256']={f:sha(BASE/'reviews'/f) for f in ['source-r2-independent.json','narrative-r2.json','narrative-r2-a.raw.json','narrative-r2-b.raw.json']}
claims['claims']=rows
claims['source_qa']=False
claims['visual_qa']=False
assert claims['additional_author_materials']['A09']==oldclaims['additional_author_materials']['A09']
writej('claims.json',claims)
md=['# C10 OXO｜r3 作者逐句來源錨點','','研究材料索引Nxx見research-original.claims.json；Axx為同一已取得原件補用的窄段。完整短摘錄、locator與cacheSHA在claims.json。這不是獨立查核。','','| ID | 種類 | 原件材料 | 界線 |','|---|---|---|---|']
for row in rows:
    md.append('| '+row['line_id']+' | '+row['kind']+' | '+(', '.join(row['material_refs']) or 'CTA')+' | '+('；'.join(dict.fromkeys(row['limits'])) if row['limits'] else '不作史實')+' |')
(HERE/'claims.md').write_text('\n'.join(md)+'\n')

# Full initialized project loaded first; only doc/brief/series replaced in memory.
# No canonical, source-cache, dictionary or media writes.
code=r'''
import fs from 'node:fs';import assert from 'node:assert/strict';import {createHash} from 'node:crypto';
import {loadProject,lintProject} from './tools/video/core/state.mjs';
import {STORY_VOICE_STYLE} from './tools/video/automation/register.mjs';
import {spokenUnits,estimateTimeline,FPS} from './tools/video/core/timeline.mjs';
import {eachLine,spokenText} from './tools/video/core/schema.mjs';
const [source,root]=process.argv.slice(1),read=f=>fs.readFileSync(f,'utf8'),hash=f=>createHash('sha256').update(fs.readFileSync(f)).digest('hex'),d=JSON.parse(read(source+'/video.json')),s=JSON.parse(read(source+'/series.json')),slug=d.slug;
const loaded=loadProject({root,slug});
const context={root,canonical_video_sha256:hash(loaded.file),initialized_dictionary_terms:Object.keys(loaded.lexicon.terms).length,initialized_dictionary_value_sha256:createHash('sha256').update(JSON.stringify(loaded.lexicon)).digest('hex'),shelf_dictionary_value_sha256:createHash('sha256').update(JSON.stringify(loaded.shelfLexicon)).digest('hex')};
assert(context.initialized_dictionary_terms>0);
const p={...loaded,doc:d,brief:read(source+'/brief.md'),series:s},lint=lintProject(p),timeline=estimateTimeline(d),flat=[...eachLine(d)],sum=xs=>xs.reduce((n,l)=>n+spokenUnits(spokenText(l)),0),total=sum(flat.map(x=>x.line)),first=d.scenes.findIndex((x,i)=>i>0&&x.chapter),opening=sum(d.scenes.slice(0,first).flatMap(x=>x.lines??[])),outro=sum(d.scenes.filter(x=>x.template==='outro').flatMap(x=>x.lines??[])),shots=d.scenes.filter(x=>x.template==='shot');
const shotTimes=timeline.scenes.filter(x=>shots.some(s=>s.id===x.id)).map(x=>({id:x.id,seconds:(x.end_frame-x.start_frame)/FPS}));
const cadence=lint.warnings.filter(x=>/no open loop between/.test(x.message));
assert.equal(d.voice.style,STORY_VOICE_STYLE);assert(!d.series);assert.equal(d.category,'story');
assert.equal(lint.errors.length,0,JSON.stringify(lint.errors));assert.equal(cadence.length,0,JSON.stringify(cadence));assert(Math.max(...shotTimes.map(x=>x.seconds))<=12);
const chapters=[];let current;for(const sc of d.scenes){if(sc.chapter){current={title:sc.chapter,text:''};chapters.push(current);}current.text+=(sc.lines??[]).map(l=>l.text).join('');}
const counts=chapters.map(x=>({chapter:x.title,you:(x.text.match(/你/g)??[]).length,i:(x.text.match(/我/g)??[]).length}));assert(counts.every(x=>x.you&&x.i));
const positions=new Map();let units=0;for(const {line}of flat){positions.set(line.id,units);units+=spokenUnits(spokenText(line));}
const events=[...new Set(d.loops.flatMap(l=>[positions.get(l.setup),positions.get(l.payoff)]))].sort((a,b)=>a-b),points=[0,...events,units],maxGap=Math.max(...points.slice(1).map((x,i)=>x-points[i]));
console.log(JSON.stringify({scope:'author native mechanical preflight only; no independent source, narrative, media or owner verdict',context,source_video_sha256:hash(source+'/video.json'),brief_sha256:hash(source+'/brief.md'),series_sha256:hash(source+'/series.json'),lint,cadence_warning_count:cadence.length,native_units:{total,opening,body_after_opening:total-opening,outro_narration:outro,body_without_opening_and_outro:total-opening-outro},lines:flat.length,scenes:d.scenes.length,illustration_scenes:shots.length,maximum_estimated_shot_seconds:Math.max(...shotTimes.map(x=>x.seconds)),estimated_total_seconds:timeline.total_frames/FPS,shot_times:shotTimes,chapter_viewer_counts:counts,author_loop_plan:{entries:d.loops.length,distinct_payoffs:new Set(d.loops.map(x=>x.payoff)).size,maximum_gap_units:maxGap,maximum_gap_seconds_at_4_5_units:maxGap/4.5,independent_narrative_verdict:false},exact_native_story_voice:true,actual_timing_verified:false,provider_calls:0,backend_writes:0}));
'''
run=subprocess.run(['node','--input-type=module','-e',code,str(HERE),str(ROOT)],cwd=REPO,capture_output=True,text=True)
if run.returncode:
    raise RuntimeError(run.stderr)
result=json.loads(run.stdout)
writej('native-author-lint-r3.json',result)
newlines={line['id']:line['text'] for line in narration}
assert set(old_byid)-set(newlines)==set(DELETED)
assert not set(newlines)-set(old_byid)
assert {key for key in newlines if newlines[key]!=old_byid[key]['text']}==set(CHANGED)
for scene in doc['scenes']:
    original=old_scenes[scene['id']]
    assert scene['data']==original['data']
    if scene['id']!='c10r1-l02':
        assert scene.get('chapter')==original.get('chapter')
    else:
        assert scene['chapter']==old_scenes['c10r1-l01']['chapter']
for row in rows:
    original=next(x for x in oldclaims['claims'] if x['line_id']==row['line_id'])
    assert row=={**original,'text':newlines[row['line_id']]}
    if row['line_id'] not in CHANGED:
        assert row==original
checks=set()
for row in rows:
    for ev in row['evidence']:
        file=Path(ev['readable_cache_path'])
        assert sha(file)==ev['readable_cache_sha256'],file
        checks.add((str(file),ev['readable_cache_sha256']))
        record=next(x for x in claims['source_records'] if x['id']==ev['source'])
        assert sha(Path(record['path']))==ev['source_bytes_sha256']
        checks.add((record['path'],ev['source_bytes_sha256']))
        assert re.sub(r'\s','',ev['short_excerpt']).lower() in re.sub(r'\s','',file.read_text()).lower(),(row['line_id'],ev)
# R3 a16 remains the original conditional patent disclosure, not a claim that every
# retail peeler or every user actually follows this gripping method.
a16=next(x for x in rows if x['line_id']=='c10a16')
patent=Path(a16['evidence'][0]['readable_cache_path']).read_text()
assert 'the thumb and forefinger which enter' in patent
assert 'necessary, pull on the handle or otherwise manipulate' in patent
assert not (HERE/'verify-1.md').exists()
for name,digest in PROTECTED_BEFORE.items():
    assert sha(Path(name))==digest,name
delta={
    'changed_narration':[{'id':key,'before':old_byid[key]['text'],'after':text,'reason':'共同no_recap：刪重複掛鉤用途，保留專利原文支持的兩指入孔、捏柄尾與必要時拉動的新動作。'} for key,text in CHANGED.items()],
    'deleted_narration':[{'id':key,'text':old_byid[key]['text'],'reason':DELETION_REASON} for key in DELETED],
    'added_narration':[],
    'opening_nine_scenes_unchanged':True,
    'all_retained_prompts_cameras_data_unchanged':True,
    'chapter_marker_moved':{'from_scene':'c10r1-l01','to_scene':'c10r1-l02','title':old_scenes['c10r1-l01']['chapter']},
    'loop_endpoints_changed':False,
    'unchanged_retained_narration_count':len(newlines)-len(CHANGED),
    'retained_full_claim_objects_unchanged':len(rows)-len(CHANGED),
    'source_evidence_fields_unchanged_for_all_retained_claims':True,
    'not_pursued':'單人l17挖芽眼no_detour及非必要位置措辭advisory均不追；不動已通過開場。'
}
notes={
    'status':'HOLD_PENDING_NEW_INDEPENDENT_SOURCE_WRITTEN_VISUAL_AND_TWO_FRESH_READERS',
    'revision':'r3','author':'/root/c03_review_ko_es','r1_author':'/root/c06_translate_en_ja',
    'scope':'C10 current author files/builder only; histories, research, reviews, old episode, canonical R2, runtime dictionaries and original raw bytes unchanged',
    'input_sha256':{f:sha(HERE/f) for f in ['video.json','script.md','narration-only.json','claims.json']},
    'r2_input_sha256':r2bindings,'r2_review_sha256':claims['r2_review_sha256'],
    'delta_from_r2':delta,'narration_plan':result['native_units'],
    'native_mechanical':{k:v for k,v in result.items() if k!='shot_times'},
    'native_lint_receipt_sha256':sha(HERE/'native-author-lint-r3.json'),
    'source_number_unchanged':oldclaims['additional_author_materials']['A09'],
    'current_evidence_byte_bindings_rechecked':len(checks),
    'protected_files':{'count':len(PROTECTED_BEFORE),'all_unchanged':True,'before_after_sha256':PROTECTED_BEFORE},
    'planning_note':'保留約3.1k有效正文；沒有padding。目標實聲720–840秒仍未測，原生估時不是實際音訊證據。',
    'independent_source_pass':False,'independent_visual_pass':False,'native_narrative_pass':False,
    'verify_written':False,'owner_approval':False,'actual_narration_seconds':None,
    'translations_created':False,'provider_calls':0,'backend_writes':0,'generated_media':0,'git_actions':0
}
writej('author-notes.json',notes)
print(json.dumps({'status':notes['status'],'input_sha256':notes['input_sha256'],'units':result['native_units'],'lines':result['lines'],'scenes':result['scenes'],'errors':result['lint']['errors'],'cadence_warnings':result['cadence_warning_count'],'warnings':result['lint']['warnings'],'maximum_estimated_shot_seconds':result['maximum_estimated_shot_seconds'],'protected_files_unchanged':len(PROTECTED_BEFORE),'changed_ids':list(CHANGED),'deleted_ids':DELETED},ensure_ascii=False))
