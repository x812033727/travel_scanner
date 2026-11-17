"""e930 fix2: s41 (the last shot of arc 3, handed over to e031) from a FIRST-FRAME still, after two multi-reference rounds failed.
Writes spec.json next to this file; mkjobs.py turns it into the two manifests. Written 2026-11-17, NOT run (paid Colab).

    python3 -I mkspec.py
    python3 -I mkjobs.py img <live>/fix2            # step 1: the Qwen-Image-Edit manifest (2 seeds) + the free cast sheet
    python3 -I mkjobs.py h3  <live>/fix2 <still.png> # step 2: the H3 first_frame manifest (2 seeds) from the picked still

Why (frames of fix1 checked 2026-11-17, scratchpad e930/f1/s41-*.jpg):
- d1 (1101, 1102) and fix1 (1201, 1202) all sent A-ling's, Wei's and Xu Yan's portraits with -qing2-l1 to Ref2VA, and the young
  woman (no picture) only in words. Every take brought her in mid-clip: d1 1101 large from the right foreground at ~3.4 s,
  1102 rising from the lower edge like a child; fix1 1201 A-ling at the well and two men at the back for ~3 s, then she walks
  in big from the right foreground; 1202 hard-cuts at ~2.5 s to a close of two identical back views of her (a clone). Text
  alone ("the same four people ... already there in the first frame", "nobody walks into or out of the frame") did not hold
  her: Ref2VA builds the opening from the pictures it was sent, and she has none.
- So fix2 fixes the whole hand-over layout in one photograph first, then animates that photograph (H3 first_frame), the way
  e031 (CG, 2026-10-28) ran Qwen first frames + FL2VA. The live-action e901-e930 runs never used a first-frame still for a clip
  (grep of colab/runs/e9*-live and the remake task: only refine-prep's stage-2 first frames and e905's cut still s36); this is
  the first. lessons.md §1: Qwen faces fall short of the portraits; here Xu Yan and the young woman show only their backs,
  Wei is small at the back wall, and A-ling is in left profile, so the face risk is smallest of any shot of the episode.

Step 1, the still (Qwen-Image-Edit-2509, 1312x736 = the H3 first-frame canvas, seeds 9301301/9301302, 8-step Lightning):
- Qwen takes at most three pictures (TextEncodeQwenImageEditPlus image1-image3). image 1 = set-xujia-yuan-dong-qing2-l1 (the
  s41 d1/fix1 set; the hand-over picture of r2-bible-e021-e030 / e031-e040 接點 30->31, the gate at 46-52% of the width, the
  well front right, low golden sun upper right: the s40/s41 dusk); image 2 = aling-portrait-l1 (rule 21: the veil-off shot
  sends the bare portrait, the veil picture would put the gauze back over her mouth; the gauze is written as an object, as
  fix1 did); image 3 = a cast sheet made here for free, xuyan-portrait-l1 (left) and weishaoqing-portrait-l1 (right) side by
  side on their own grey (mkjobs.py img, deterministic PIL, 1312x736).
- Tang Xiaotang gets NO picture and is never named: bible rule 3 (her back shots drop her three pictures), and her portrait
  carries long pink ribbons falling from the buns and her front face - a reference wins over the text (rule 19), and the
  dangling ribbon is exactly what grew into braids in e930 s29 and d1 s41. There is no back-view picture of her or of Xu Yan in
  refs-live (checked): their backs are written in words, Xu Yan's costume comes from the cast sheet.
- Positive text says only what is there (bible 拍法 18, screen-test-e031-e040.py's NEGATIVE_WORDS rule); what to keep out is
  in the negative file. latent empty (the notebook samples at denoise 1.0 either way; the layout comes from image 1).
- A-ling as the hand-over states her (r2-bible-e031-e040 接點 30->31, the "grey veil" of arc 3 at that moment): the long strip
  of pale grey gauze tied over her left ear only, blown out past her left cheek, her face bare, right hand a bucket of water;
  e031 c01 picks her up exactly there.

Step 2, the clip (H3 first_frame, smooth profile, G4, 1312x736, 8 s = the d1/fix1 purchase, seeds 9301301/9301302 = the
e9xx fix2 convention): the picked still as <Picture 1>; static camera; minimal motion - one breath for A-ling, a small head
turn of Wei toward the yard and back, a small tilt of Xu Yan's head toward her and back, her head still (rule 3: her face
never turns to us), only the gauze, a few strands of hair and the hems in the breeze. The prompt file is named
prompts/ref-s41-<seed>.txt and keeps "never the mood. " and "One continuous shot." once each, so live-action/refine-prep.py
can carry this motion text into the stage-2 refine like any fixN pick (it globs runpod/live/*/out/s41-<seed>.mp4).
Series prompt rules held by mkjobs.py's scan: nobody named or described who is not in frame (Tang Xiaotang never named in
either step); nothing hung up (no sign, lantern, hanging word); no "open"; her two buns with the pink ribbon wound tight, every
strand up, the nape bare; no braid word; no smile word.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
REFS = "/home/user/zt-work/docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live"
SEEDS = [9301301, 9301302]

IMG_PROMPT = (
    "Image 1 is a photograph of a farmhouse yard at sunset: keep exactly everything in it - the camera position, the farmhouse "
    "on the left, the wooden yard gate in the middle of the back wall, the bare tree, the walls, the golden field, the round "
    "stone well at the front right, and the low golden sun at the upper right with long shadows toward the lower left. "
    "Put four people into this yard, each with a long shadow toward the lower left. "
    "At the front right beside the well stands the young woman from image 2, full figure, her face, hair and plain grey-white "
    "cotton dress exactly as in image 2, long sleeves to her wrists; "
    "her body turned toward the yard gate, her face in left profile, eyes on the gate, lips closed; one round wooden bucket of "
    "water with a rope handle held low in her right hand; a long strip of soft half-transparent pale grey gauze tied by a thin "
    "grey tie over her left ear only, its free end blown out past her left cheek and shoulder in the wind, her face bare. "
    "Small and far back, in the yard gate in the middle of the back wall, stands the man on the right of image 3, full "
    "figure, his face, topknot with its green jade ornament and sapphire-blue brocade robe exactly as in image 3, a folded fan "
    "held shut in his right hand, his body half turned "
    "toward the well, his eyes on the well. "
    "In the middle of the yard between the camera and the gate, two people the same size stand shoulder to shoulder with "
    "their backs to the camera, both facing the gate, full figures: on the left the man on the left of image 3, the back of "
    "his head and his topknot tied with a cloth band toward us, his faded blue-grey scholar's robe patched at one "
    "elbow; at his right shoulder, the same distance from the camera, the top of her buns at the height of his ear, a "
    "slender young woman seen only from behind: her black hair gathered up into just two round buns set "
    "high on her head, one on each side, one short pink silk ribbon wound tight round the base of each bun with its ends "
    "tucked in; every strand is up in the two buns, so the bare nape of her neck shows smooth and clear down to the pink "
    "inner collar; a light peach-pink silk jacket and a pleated peach-pink skirt; the back of her head faces straight away "
    "from the camera. Exactly four people, each one once. "
    "A photorealistic live-action film still of a Chinese historical costume drama, natural perspective, deep focus, real "
    "skin, hair, cloth and earth textures, warm golden evening light, filling the whole frame edge to edge."
)
IMG_NEG = (
    "3D render, CGI, game render, plastic, cartoon, anime, illustration, painting, text, writing, calligraphy, Chinese "
    "characters, letters, numbers, inscription, signboard, plaque, couplet, banner, flag, poster, lantern, watermark, logo, "
    "fifth person, extra people, crowd, child, second young woman, twins, duplicate person, clone, braids, pigtails, plaits, "
    "long ribbons, ribbon streamers, ribbons falling down her back, loose hair down her back, her face, her profile, facing "
    "the camera, looking at the camera, smiling, veil over the mouth, mask, weapon, sword, knife, horse, cart, black bars, "
    "border, fisheye, ultra wide angle, barrel distortion, tilted horizon, dutch angle, night, blue sky at noon"
)

H3_PROMPT = (
    "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.\n\n"
    "integrated_multimodal_description: [Shot 1] Photorealistic live-action film footage of real actors in an ancient Chinese "
    "(Song-dynasty) period drama, shot on a cinema camera. The four people shown in <Picture 1> stay exactly where they stand "
    "in it from the first frame to the last: A-ling at the front right beside the round stone well, Wei Shaoqing small in the "
    "yard gate in the middle of the back wall, Xu Yan and the young woman with the two high round buns in the middle of the "
    "yard, the same size, shoulder to shoulder with their backs to us, she at his right shoulder; the first frame fixes their "
    "faces, hair and costumes, the yard and the low golden evening light, never the mood. "
    "A-ling stands still, her face in left profile, her eyes on the gate, her lips closed, the bucket low in her right hand; "
    "she draws one slow breath, her shoulders rising a little and settling. Wei Shaoqing stands frozen in the gate, his eyes "
    "on the well; once his head turns a little toward the middle of the yard and slowly back toward the well. Xu Yan's head "
    "tilts a little to his right toward the young woman and settles back toward the gate. The young woman keeps her head "
    "still, the back of her head toward us the whole shot, the bare nape of her neck clear above the pink inner collar, her "
    "two buns and their tight pink ribbons unchanged. Only the loose strip of pale grey gauze, a few strands of A-ling's hair "
    "and the hems of their clothes stir in the evening breeze. Only these four people are in the frame the whole shot, each "
    "one once; nobody walks into or out of the frame; no second copy of anyone appears. A-ling, Wei Shaoqing and Xu Yan say "
    "nothing in this shot: their lips stay pressed together from the first frame to the last, no talking, no mouthing words. "
    "The low golden evening sunlight and the long shadows stay unchanged. Every person in the frame wears dark cloth shoes on "
    "both feet. The camera holds a static shot. One continuous shot. The picture is clean, with no subtitles, captions or text "
    "anywhere on screen. Natural, realistic human motion of real actors; faces, hair and costumes stay as in the first frame.\n"
    "overall_soundscape: N/A\n"
    "non_diegetic_music: N/A"
)

spec = {
    "_note": "e930 fix2 s41: first-frame route; see mkspec.py's docstring. Not run as written (2026-11-17).",
    "seeds": SEEDS,
    "image": {
        "id": "s41-ff",
        "reference_images": [f"{REFS}/set-xujia-yuan-dong-qing2-l1.png", f"{REFS}/aling-portrait-l1.png", "SHEET"],
        "cast_sheet": {"name": "cast-xuyan-weishaoqing.png", "left": f"{REFS}/xuyan-portrait-l1.png",
                       "right": f"{REFS}/weishaoqing-portrait-l1.png", "width": 1312, "height": 736},
        "prompt": IMG_PROMPT, "negative": IMG_NEG, "width": 1312, "height": 736, "latent": "empty",
    },
    "h3": {"shot": "s41", "prompt": H3_PROMPT, "duration_seconds": 8, "width": 1312, "height": 736,
           "in_frame": ["A-ling", "Wei Shaoqing", "Xu Yan"]},
}
(HERE / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("spec ->", HERE / "spec.json", f"(image prompt {len(IMG_PROMPT)} chars, H3 prompt {len(H3_PROMPT)} chars)")
