# Curio S38 two-shot pilot: independent human visual QA

Date: 2026-10-20. Scope: the **original** 1280×720 JPEGs below, viewed directly at original resolution; read-only inspection of `video.json`, the `cute-mystery` look in `tools/video/core/drama.mjs`, and the pinned 1666 Pepys diary. This is a visual assessment, not approval to generate the remaining shots or use these images in a final cut. The later `pf002-1-trim.jpg` selected in the keyframe manifest was **not** the image assessed here.

| Scene | Original image SHA-256 | Independent verdict |
| --- | --- | --- |
| `pf001` | `608203b99cd453ad7218d8c773c93ca92900997d2a9a73a1be44090cba60ccb0` | **PASS** |
| `pf002` | `a3ed5ba33ae9c8f1741524d3eedac6d22255c20f568abf4ed211bf92b66902ba` | **PASS, with minor craft reservations** |

## `pf001` — PASS

The image clearly depicts **two bearded men**, not children: the large heads and eyes are the requested chibi proportions, while facial hair, adult dress, and their working action communicate adult characters. Both have complete wooden-shaft, iron-blade spades, with visible hands on the handles. The open soil pit, raised spoil, grass, distant brick boundary wall, dim light, linen cuffs, coats, knee breeches, and boots give a plausible illustrated 1666 English garden. I see no East Asian robes, modern digging equipment, writing, or visibly broken anatomy/tool. A small red mark on one sleeve reads as a palette accent, not a clearly identifiable modern badge.

It **misses the requested waist-down crop**: both faces and full figures are shown. This is a prompt-framing defect, but it does not misstate the line's action or Pepys's diary, and it does not make the men read as toddlers. Its clean outlined chibi characters and navy/teal/ochre palette match the `cute-mystery` look well enough for this pilot.

## `pf002` — PASS, with minor craft reservations

The foreground cheese reads as a **single intact round of hard yellow-gold cheese**. Its large face is continuous rind-colored material; the small irregular brown patches read as surface marks. There is no exposed pale cut interior and **no round holes** suggesting Swiss cheese. It is not a child-height wheel: close framing enlarges it, but its size relative to the visible adult-size hands is within a plausible whole-cheese range. The pit is visibly dug into uneven earth rather than built as a stone well. Wine vessels are visible beside it. Only hands and 1660s-style cuffs are shown, so the image neither shows a child nor provides much independent age evidence; the sleeves and hand scale are consistent with the adult diggers in `pf001`.

One upper hand seems to steady the rim mainly with an extended finger while its other fingers disappear behind the wheel. The pose is awkward for the weight of a whole Parmesan, yet the second hand touches the other side and the cheese is already supported against the pit lip. This is an **anatomy/physical-action imperfection**, not a different cheese or a different historical event. The jar mouths do not display unmistakable stoppers at this view size; they are ambiguous rather than visibly spilling. No modern object is identifiable. The image uses deeper shading and more cinematic lighting than the flatter chibi reference, but its outlined shapes, muted teal/ochre palette, and illustrated surfaces still fit the series closely enough. I would not treat the machine's zero style score or single-finger finding alone as a material reason to reject this pilot.

## Historical boundary and decision limit

The 4 September 1666 diary says that Pepys and Sir W. Pen dug **another** garden pit in the evening, put **their wine** in it, and Pepys added `my Parmazan cheese` (`4200.txt` L65997–66002; pinned text SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`). The exact `video.json` lines and prompts show the digging and then the deposit of wine and cheese. The diary does **not** establish the cheese's size, packaging, or later retrieval. Neither still contradicts those points. Both are cartoons, so they do not establish Pepys's actual appearance or a documented pit shape.

The two stills pass this **limited, substantive visual pilot**. The visible deviations are crop, grip, shading, and uncertain vessel sealing; these merit attention if refining a final image, but they are not the earlier material errors of child diggers, East Asian dress, a holey Swiss wedge, or a constructed well. No project files, approval state, or paid generation were changed by this review.
