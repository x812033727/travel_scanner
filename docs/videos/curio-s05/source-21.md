# Curio S05 R21 source and alignment audit (after blind seal)

Blind answers: `/tmp/curio-s05-r21-blind-review.md`, SHA-256 `6d6914c592e290d8357de76a5628d3aa1c2d9c2f82683cf28474aa9852aa3ece`.
Audited script SHA-256: `d1edab784c98e7c5f9ddf733c3f3de5b6bfe95b07d47c53330fece4c228b44ec`.
Current video JSON SHA-256: `195d59004585eb518bcfea64f6de26778312d0b31ca9d0d7c9e7bd211d2df889`.
Current claims SHA-256: `cf5806e6b4f0c475244263cb33793aff2911a83141414d55b77b0d63ffc8e6fd`.

## Pinned text independently read

`/tmp/s05-sanguozhi` HEAD is `10a0b1ab3019d8821262f7402366d14fb4aaa102`; read `OEBPS/Text/035.htm` directly at p0, p1, p8, p21.

- p1's Chen Shou body has Xu Shu's `將軍宜枉駕顧之`, `由是先主遂詣亮，凡三往，乃見`, private conversation, `情好日密`, and the fish-water remark. The note's `魏略曰` follows and has `亮乃北行見備`, `備與亮非舊`, ox-tail scene, household registration advice, `備從其計，故衆遂彊`, and `以上客禮之`. The sequence and speaker distinctions in the script are supported.
- p1 gives `九州春秋所言亦如之` before `臣松之以爲`; Pei's quote of the memorial includes `諮臣以當世之事` after `三顧臣於草廬之中`, then Pei concludes `則非亮先詣備，明矣`. Thus the rewritten eg160 (`裴松之的引文接著是`) accurately labels whose quotation it is and quotes words actually in it. p8 contains the same phrase and the later `由是感激，遂許先帝以驅馳` used at eg162, which the script expressly labels as the complete memorial's continuation.
- p1 gives no decisive dates that order the two *proposed first-meeting* scenes or explicitly makes one a later reunion. p8 has `爾來二十有一年矣` and Pei's approximate earlier-year inference for the memorial scene, but it does not date the rival Fancheng scene relative to it. Rewritten eg134 (`設想`) remains a conditional test and is source-safe.
- p21 has Chen Shou's `乃三顧亮於草廬之中`; attributing it to the same Chen Shou as the biography is correct. p0 supplies the Guan Zhong/Yue Yi comparison and Xu Shu's esteem.

## Alignment

`video.json`: 90 scenes, 98 narration lines, 98 unique IDs. `script.md`: 98 spoken lines. Flattened JSON narration and script spoken lines match exactly in order and text: zero differences. `claims.md` mentions all 98 unique narration IDs and no ID absent from `video.json`. Final `outro` has eg097 and eg098 in both script and JSON. Metadata loop `eg005` names eg072 as payoff, while the question's exact sentence is revealed at eg069 and eg072 supplies Pei's reaction; this is a low-impact metadata timing nuance, not an unanswered spoken loop.

## Exact-hash narrative verdict and limits

All 13 official items answered in sealed blind review: 12 yes, 1 no (`no_recap`). Eg137 has already said the reverse account is Pei's preserved quotation rather than Chen Shou's main text; eg070 supplies Pei's contrary ruling. Eg139 repeats both at the ending. It summarizes rather than adding a sourced new consequence. This matches the first R21 blind reader's independently preserved concern. I did not change `script.md`, `video.json`, claims, paid media, or audio. This audit supports the historical wording and ID alignment only; it does not approve R21 TTS or carry R20 audio checks forward.
