# S52 R24 opening batch: native visual HOLD

2026-10-21 UTC. The R24 written prompt/source review passed, but the first five newly generated opening images **do not pass human visual review**. The paid run was stopped after these five images. `/workspace/.video-work/curio-s52/STOP` is present; the remaining storyboard must not be released as completed media.

The exact `video.json` SHA-256 at generation was `cf3211e99155afd7cd71c715f6c6fd6055c43975a3a20e199b4582dda6f13677`. Its first two R21/R22 images retain their separately documented native KEEP decisions. The private ledger totals at this stop are **US$0.1250**, 10 image calls, 9 judge calls, zero reservations, below the previously approved **US$4.46** whole-episode ceiling. This includes earlier R21/R22 attempts. The fifth new image (`s52007`) was downloaded and charged before the STOP took effect, but was **not judged**; no judge result may be inferred for it.

| Shot | Original image SHA-256 | Machine result | Direct native-image finding |
| --- | --- | --- | --- |
| `s52003` | `10579139c8810fa94125b489328f94eb64c5228c23c7712d58857dad1bd1a8a5` | 9.71/10, FAIL subject | Modern-looking toddler in a sleeveless shirt, hands resting on a diagram rather than tracing the dot. Human REJECT. |
| `s52004` | `6e3d1d54fdde31dc7dc3725540439d342b83e31a9427ca54352e63177db5457a` | 9.00/10, FAIL frame/details | Childlike figure with modern cap and clothing, black top/bottom bars, no close document shot. Human REJECT. |
| `s52005` | `d19254a11bb864c2b5a987cfcbbacfd5b4506444911407a9c599e73429a90250` | 7.18/10, machine PASS | Modern schoolchild and large flip chart replace an eighteenth-century adult clerk and archive petition. This materially misplaces the event. Human REJECT despite machine PASS. |
| `s52006` | `9ba31632e618f9ddc9d1b27246cc53b81571bba89dafa81fa95887e5d0d5e3ae` | 9.29/10, machine PASS | Modern child holding an apparent cardboard box on a shore replaces an adult period boat crew member with an instrument case. Human REJECT despite machine PASS. |
| `s52007` | `8e38db11d3837f935389ff47bff497ad1b2fa5432edd945d47bed5dd7b92dda4` | Paid image, no judge call | Two modern schoolchildren and pseudo-written sheets replace one editor examining a blank timing sheet. Human REJECT; leave machine verdict unrecorded. |

The five prompts use generic roles (`observer`, `curator`, `clerk`, `crew member`, `editor`) and omit the explicit adult age, mature features, period clothing and coherent period props that rescued `s52001` and `s52002`. This is a **systemic prompt failure** with this model and series look, not five isolated minor decorative discrepancies. Modern schoolchildren would imply a different time and activity from the 1768–69 historical narration. Do not count these images as final art even where the automated judge passed.

Next: prepare a narrow written R25 repair with explicit adult period subjects and one action per shot, independently check source and framing, then test no more than one additional take on a small pilot before expanding. Respect the per-scene three-image/two-prompt-round ceiling. Keep the unchanged first two accepted images and the STOP file; preserve all private paid originals and ledger entries for audit. Full 111-shot art, music, assembly, captions, QA and upload links remain pending.
