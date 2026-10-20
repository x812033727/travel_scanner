# Curio S05 R22 independent source and alignment audit

Script SHA-256: `8e9632a4d1cce5a25a2876db16ea8d7c66de1d5d0544c367541b2cd845ae8121`.
Video SHA-256: `cb0b83c24d20be9ee39c2cd2b07f59acdaedc10f73e8541d9f2da15aedabf7fe`.
Claims SHA-256: `cf2b9f440e62e93f43f904635c97f14eac36324e04a64ebc2e2034caa740a016`.
Pinned source checkout `/tmp/s05-sanguozhi` HEAD `10a0b1ab3019d8821262f7402366d14fb4aaa102`; direct HTML checked at `OEBPS/Text/035.htm`.

## Primary source findings

- `p0` names Zhuge's Jingzhou farming, Guan Zhong / Yue Yi comparison, and Xu Shu among the few friends who believed his ability. This supports `eg102` and `eg103` without assigning an unsupported exact cottage site.
- `p1` Chen Shou main text: `時先主屯新野。徐庶見先主，先主器之`, then `諸葛孔明者，卧龍也`, `君與俱來`, `此人可就見，不可屈致也。將軍宜枉駕顧之`, `由是先主遂詣亮，凡三往，乃見`. This supports the Xu Shu and three visits line group `eg008`–`eg020`, especially `eg173`'s explicit direction and `eg015`–`eg016`.
- `p1` main text continues Liu Bei's private `計將安出` consultation, his `善`, `情好日密`, Guan Yu / Zhang Fei's displeasure, and `孤之有孔明，猶魚之有水也`. Supports `eg020`–`eg031`, `eg144`–`eg146`, and the first sequence test `eg063`–`eg065`.
- The distinct `p1` Pei note opens `魏略曰：劉備屯於樊城...亮乃北行見備，備與亮非舊`, then narrates guests leaving, Bei not asking the purpose, yak tail hair (`髦牛尾` / `結毦`), Zhuge's challenge, troop registration advice, `備從其計，故衆遂彊`, and `乃以上客禮之`. Supports `eg035`–`eg057`. The spoken restriction at `eg116` is precise: it does not assert Liu Biao separately issued an order.
- The same `p1` note reads `九州春秋所言亦如之。臣松之以爲亮表云「先帝不以臣卑鄙，猥自枉屈，三顧臣於草廬之中，諮臣以當世之事」，則非亮先詣備，明矣。雖聞見異辭，各生彼此，然乖背至是，亦良爲可怪。` Thus `eg061` / `eg130` separate the additional book from Pei's own view. Revised `eg160` is directly accurate: Pei's quoted excerpt does continue to `諮臣以當世之事`. `eg069` gives the exact sentence asked for at `eg005`; `eg070` and `eg072` then give Pei's judgment and reaction.
- `p8` memorial itself has `臣本布衣，躬耕於南陽`, `不求聞達於諸侯`, the three visits and consultation, and then `由是感激，遂許先帝以驅馳`, `爾來二十有一年矣`. `eg162` correctly labels its quotation as subsequent memorial text rather than more of Pei's p1 excerpt. The attached note dates the memorial's northern campaign to 建興五年, supporting the 227 opening.
- `p20` begins `臣壽等言`; `p21` says `乃三顧亮於草廬之中`; `p25` signs 陳壽. Therefore `eg082`–`eg083` correctly identify the collection preface as Chen Shou's own writing, not a second independent author.
- Revised `eg134` says both ordering attempts are `設想` and that these two extant passages supply no date that determines the before/after relationship. The ordering difficulties use textual `備與亮非舊` versus `情好日密` and Xu Shu's `將軍豈願見之乎`; they are labeled the video's hypothetical tests rather than an analysis falsely attributed to Pei. No claim that people could meet only once.
- The absence of an initial named informant in the quoted `魏略` passage, Pei's short `九州春秋所言亦如之`, and no complete second account in this note support the bounded uncertainty in `eg075`–`eg080`.

## Alignment and prompts

- Independently parsed the script's scene headings and spoken text/emotion fields against `video.json`: 89 of 89 scenes in exact order; 97 of 97 lines match exact text, scene, and emotion. All 97 video IDs are unique. The 97 claim-table IDs exactly equal the video ID set, with no omissions, duplicates, or stale IDs. `eg139` is absent from all three current files and `visit-085a` is absent from the current scene list.
- Current `video.json` has 86 image `shot` prompts, 2 `big` text cards, and 1 outro. Every `shot` has a nonempty prompt and camera and `visual: still`. Prompts pair with their narration subjects: Xin Ye arrival / Xu Shu, Bei's cottage visits, Fancheng / Zhuge and yak tail, two ordering hypotheses, and Pei's scroll/source inquiry. `visit-069` card is the exact `三顧臣於草廬之中` reveal. Scene images use blank or unmarked documents, so they do not manufacture readable ancient text; no prompt contradicts its paired line in this pass.
- `loops` has `eg005`→`eg069`, matching the exact question about which sentence Pei found surprising. All nine setup/payoff IDs exist and match their spoken answers. `eg072` is Pei's later reaction, not the answer to which sentence.
- `node tools/video/cli.mjs lint --slug curio-s05 --json` returned 0 errors, 0 warnings, 97 lines, estimated 9.28 minutes.

Result: source, script/claims/video alignment, loop placement, and current prompt pairing PASS for the exact hash above. This audit did not perform R22 TTS, audio listening, image generation, or paid media production.
