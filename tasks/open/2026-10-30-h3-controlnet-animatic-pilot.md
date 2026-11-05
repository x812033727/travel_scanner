---
id: 2026-10-30-h3-controlnet-animatic-pilot
title: Pilot H3 Fun ControlNet Union 2.0 with a depth animatic, and the camera embeddings
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-30T06:39:20Z
completed_at:
branch:
depends_on:
  - 2026-10-30-h3-first-last-frame-camera
scope:
  - .agents/skills/minimax-h3-colab/assets/h3_control.ipynb
  - .agents/skills/minimax-h3-colab/scripts/animatic_depth.py
---

# Pilot H3 Fun ControlNet Union 2.0 with a depth animatic, and the camera embeddings

## Why

For moves and blocking that two keyframes cannot describe (an orbit, a crane over a crowd, a dolly
through a doorway) H3 has an official control branch: alibaba-pai MiniMax-H3-Fun-Controlnet-Union
(2.0 recommended; Canny, Depth, HED, MLSD, Pose; guidance-distilled, `guidance_scale` 1.0;
`control_context_scale` 1.0 strongest), loaded in ComfyUI with `ModelPatchLoader` and
`MiniMaxH3FunControlNetApply`; Comfy-Org ships it as
`model_patches/minimax_h3_fun_controlnet_union_2.0_pruned_int8_convrot.safetensors` (about 6.8 GB
for the branch). The official template pairs it with the Ref2VA model. A depth video of the planned
camera path (a grey-box animatic, or a 2.5D move over a keyframe's estimated depth) could then drive
the camera exactly. Comfy-Org also ships ten effect embeddings, several of them camera moves
(`minimaxh3_bullet_time`, `minimaxh3_spiral_ascent`, `minimaxh3_kiss_camera`,
`minimaxh3_truman_show`), used as `embedding:<name>` in the prompt.

## Definition of done

- [ ] One paid pilot (owner's go-ahead) on two e030 shots: a 2.5D depth animatic (keyframe depth +
      virtual camera) through ControlNet 2.0 with Ref2VA, at `control_context_scale` 1.0 and 0.6, against
      prompt-only and first/last-frame takes; camera accuracy from `2026-10-30-clip-qc-camera-move`,
      identity and look judged side by side.
- [ ] One take each with the bullet-time and spiral-ascent embeddings on a suitable shot.
- [ ] Findings and a go/no-go written to `references/camera-control.md` (that file belongs to
      `2026-10-30-h3-first-last-frame-camera`; widen this scope or hand the text over).

## Steps

- [ ] `scripts/animatic_depth.py`: depth of a keyframe (model and licence to choose), virtual camera
      path, depth video at the canvas size and 17k+5 frames.
- [ ] `assets/h3_control.ipynb` from the official template `video_minimax_h3_fun_controlnet_union.json`.

## Notes

- Licence: the ControlNet is a derivative of MiniMax-H3 under the MiniMax H3 Community License
  (territorial restrictions and the Acceptable Use Policy apply), the same terms as the base model.
- Whether the control branch works with the FL2VA model (first frame) is not stated; the template
  uses Ref2VA. Test that first.
