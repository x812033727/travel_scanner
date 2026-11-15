#!/usr/bin/env python3
"""screen-test-e016.py OUT_DIR : the four e016 pictures, decided by the coordinator after the independent review
(writer-tools/e016-r2/review.md 必改 8, 17, 18 and 建議 on the raft and the shed, 2026-11-15). NOT run here (no Colab in the
writing session). Seeds 37013/37014 (e015 used 37011/37012), 8 jobs, one manifest OUT_DIR/e016.json; prompts in OUT_DIR/prompts/.
Check before running:
    python3 -I .agents/skills/minimax-h3-colab/scripts/check_images_manifest.py OUT_DIR/e016.json

Each picture is a Qwen-Image-Edit edit of the refs-live picture it replaces (image 1), keeping its layout and camera unless
said otherwise. The positive prompts are written only as what is there (bible 拍法 18: a negated noun in a prompt is drawn);
the things to keep out are only in the negative-prompt files.
- set-dukou-l2 (必改 17, 18; e016 s41, s42): the ferry landing at dawn of l1 with one column of black smoke rising behind the
  village on the right into the pale sky above it (the red glow stays low on the far left horizon), and the jetty standing
  empty: where l1's covered boat was moored there is open calm water. The smoke is the episode's closing hook; l1 had none and
  its boat would be read as the raft.
- set-shuyuan-l2 (必改 8; e016 s29-s38): the academy gate redrawn with a normal lens at eye height (l1 is an ultra-wide
  distortion): the vermilion doors and three stone steps on the right, the street running away to the left between plain
  white plaster walls and dark wooden plank shop fronts; above the doors one smooth blank wooden plaque with fine straight
  grain (l1's swirling grain read as faint ink strokes); every eave plain dark wood (l1's dozen hanging white boards grow
  writing); inside the open doors only a stone-paved courtyard and a tree (l1 had a red plastic-looking tub and a modern bench).
- set-zhufa-ye-l2 (建議; e016 s18-s28, and s39 through its mirror): the raft at night of l1, same layout and camera, as a real
  night photograph: real green-yellow bamboo poles with nodes, rough hemp lashings, the two brown oilcloth bundles, the
  stern pole with its crossbar and one plain pale paper lantern, reeds and dark trees, stars. After the pick, s39 (going
  upstream, the bow on screen right) uses a horizontally mirrored copy made with
      ffmpeg -v error -i refs-live/set-zhufa-ye-l2.png -vf hflip refs-live/set-zhufa-ye-l2-flip.png
  (an empty set has no cross collar to flip; bible 拍法 9 is about people).
- set-gongpeng-l3 (建議, the coordinator's choice; e016 s09-s17): the day shed of l2 with a bare packed-earth floor, the far
  left showing only the bare stone wall where l2's two tall A-frames of poles leaned, and both vats holding only smooth
  pulp with bare rims where l2's crossed stirring sticks lay; everything else kept. In e014 the A-frames were drawn as long
  poles in s15 and the bamboo mats became poles and rakes (s30, s32).
pilot.py takes the newest l-version of a set, so the picks saved as refs-live/set-dukou-l2.png, set-shuyuan-l2.png,
set-zhufa-ye-l2.png and set-gongpeng-l3.png go to every later live prep naming those sets (e014's and e015's day-shed retakes
included, which wanted the same things gone); prep916.sh stops until all four and the mirror are there.
"""
import json
import sys
from pathlib import Path

out = Path(sys.argv[1]); (out / "prompts").mkdir(parents=True, exist_ok=True)
LIVE = Path(__file__).resolve().parent.parent / "assets" / "refs-live"
SEEDS = (37013, 37014)

STYLE = ("Ancient China, Song dynasty. Style: a photorealistic live-action photograph of a real location for a Chinese historical "
         "costume drama, shot on a cinema camera at eye height, natural light, real wood, bamboo, rope, thatch, plaster, stone, "
         "water and earth textures, deep focus, everything sharp from front to back; a clean natural film image that fills the "
         "whole frame edge to edge.")
QUIET = "the place is quiet and deserted at this hour, every surface plain"
PLACE = "A wide establishing photograph of a real location: {desc}."

PICTURES = [
    ("set-dukou-l2", "set-dukou-l1", "e016 s41",
     "image 1 is a photograph of the place: keep exactly its camera position, the wide calm water, the tall bare wooden mooring "
     "posts standing in the water, the low wooden jetty running out from the right bank, the dry grass along the right bank, "
     "the dirt path up the bank, the low thatched and tiled village houses on the right, the blue hills far off at the left and "
     "the dawn light; change only the things described here. ",
     "the same ferry landing below a poor ancient Chinese Song-dynasty village at dawn, a real photograph: (1) from behind the "
     "village houses on the right one single thick column of black smoke rises and rolls high into the pale dawn sky above the "
     "village, its dark plume leaning a little to the left, its base hidden behind the roofs; (2) the low wooden jetty stands "
     "empty, its grey planks bare all the way to its end, and all around it and between the mooring posts only open calm water "
     "reflecting the sky; (3) the red glow of dawn stays low along the far left horizon, the sky pale above it; "
     + QUIET),
    ("set-shuyuan-l2", "set-shuyuan-l1", "e016 s29",
     "image 1 shows the layout of the place: keep its arrangement, the gate with its pair of open vermilion doors under a dark "
     "tiled gate roof and the three wide stone steps on the right, and the stone-paved street running away to the left; redraw "
     "it as a natural photograph taken with a normal 35mm lens at eye height from across the street, straight upright walls "
     "and natural proportions. ",
     "the gate of a county academy in an ancient Chinese Song-dynasty county town on a clear autumn morning, a real photograph: "
     "(1) on the right three wide grey stone steps up to a pair of open vermilion doors under a dark tiled gate roof; above the "
     "doors one smooth blank wooden plaque of plain brown wood with fine straight grain running evenly from end to end; (2) "
     "through the open doors only a plain stone-paved courtyard and one green tree; (3) the stone-paved street runs away to the "
     "left between long plain white plaster walls with dark tiled copings and dark wooden plank shop fronts, every eave plain "
     "dark wood; (4) bright clear morning sunlight, crisp soft shadows on the stone; "
     + QUIET),
    ("set-zhufa-ye-l2", "set-zhufa-ye-l1", "e016 s18",
     "image 1 shows the place: keep exactly its layout and camera position, the raft lying from the lower left toward the "
     "middle, its stern pole with the lantern at the right, the river between dark banks, the reeds and dark trees on both "
     "banks, the low hills and the starry sky; change it into a real night photograph as described here. ",
     "a long bamboo raft floating on a quiet river in an ancient Chinese Song-dynasty countryside late at night, a real night "
     "photograph: (1) the raft is eight thick poles of real green-yellow bamboo with natural nodes and a matte natural surface, "
     "lashed side by side with rough brown hemp rope; (2) in its middle two rounded bundles wrapped in worn brown oilcloth and "
     "tied with hemp rope, stacked low; (3) at its stern on the right one tall bamboo pole standing upright with a short "
     "crossbar, from which hangs one plain pale paper lantern with a small candle burning inside, its warm glow on the "
     "bundles and on the dark water; (4) real reeds and dark trees along both banks, low dark hills, a deep black sky full of "
     "small cold stars, the water lit only by starlight and the lantern; "
     + QUIET),
    ("set-gongpeng-l3", "set-gongpeng-l2", "e016 s09",
     "image 1 is a photograph of the place: keep exactly its layout and camera position, the dark timber roof and posts, the "
     "open right side, the low stone back and left walls with the green plants at their foot, the tiled roofs and trees beyond "
     "them, the two big round wooden vats of milky white pulp at the front left, the squat stone mortar in the middle, the old "
     "wooden table at the right and the warm daylight; change only the things described here. ",
     "the same open-sided papermaking work shed of a poor ancient Chinese Song-dynasty farmhouse by day, a real photograph: "
     "(1) the floor is bare packed earth, smooth, even and brown from wall to wall; (2) at the far left only the bare stone "
     "wall with its green plants at the foot, clear from the floor to the roof; (3) both vats hold only smooth milky white "
     "pulp, their round wooden rims bare all the way round; "
     + QUIET),
]
NEG = ("3D render, CGI, game render, plastic, cartoon, anime, illustration, painting, text, writing, calligraphy, Chinese "
       "characters, letters, inscription, signboard, couplet, banner, poster, watermark, logo, people, person, crowd, figure, "
       "man, woman, child, silhouette, statue, animal, weapon, spear, sword, knife, black bars, border")
NEG_BY = {
    "set-dukou-l2": NEG + ", boat, covered boat, sampan, moored boat, raft, ship, fire flames, white smoke, fog bank",
    "set-shuyuan-l2": NEG + ", fisheye, ultra-wide distortion, curved walls, hanging boards, white boards, sign boards, plaque "
                            "with writing, wood grain swirls, plastic bucket, red bucket, modern bench, modern objects, lion statue",
    "set-zhufa-ye-l2": NEG + ", 3D, black plastic pipes, glossy tubes, moon, full moon, daylight, people on the raft, second "
                             "lantern, torch, fire",
    "set-gongpeng-l3": NEG + ", tiled floor, cracked tiles, paving stones, A-frame, tripod, leaning poles, poles, sticks, "
                             "stirring sticks, paddles, rack, ladder, rake, staff",
}
# Round 2 (2026-11-15, the coordinator's pick of round 1): set-shuyuan-l2, set-zhufa-ye-l2 (+ its mirror) and set-gongpeng-l3
# (cropped) are in refs-live; set-dukou-l2 failed in both seeds (a modern brick factory chimney under the smoke, and the
# covered boat kept at the jetty). `screen-test-e016.py OUT_DIR --r2` writes OUT_DIR/r2.json with set-dukou-l2 only, seeds
# 37015/37016: the smoke billows up from among the thatched roofs of the far village houses like a burning house, the jetty is
# bare planks on posts in open water with only reeds at the water's edge; an edit of set-dukou-l1 (it keeps the layout).
ROUND2 = "--r2" in sys.argv[2:]
if ROUND2:
    SEEDS = (37015, 37016)
    PICTURES = [("set-dukou-l2", "set-dukou-l1", "e016 s41",
                 "image 1 is a photograph of the place: keep exactly its camera position, the wide calm water, the tall bare "
                 "wooden mooring posts standing in the water, the low wooden jetty running out from the right bank, the dry grass "
                 "along the right bank, the dirt path up the bank, the low thatched and tiled village houses on the right, the "
                 "blue hills far off at the left and the dawn light; change only the things described here. ",
                 "the same ferry landing below a poor ancient Chinese Song-dynasty farming village at dawn, a real photograph: "
                 "(1) a house in the village is burning: thick dark smoke billows up from among the low thatched roofs of the far "
                 "village houses on the right, rising in one rolling dark plume over the roofs into the pale dawn sky, a faint "
                 "orange glow low between the roofs where it rises, the roofs themselves low thatch and grey tile; (2) the low "
                 "wooden jetty is bare grey planks laid on wooden posts, open calm water all around it and between the mooring "
                 "posts, reflecting the sky; (3) only green and dry reeds along the water's edge by the right bank; (4) the red "
                 "glow of dawn stays low along the far left horizon, the sky pale above it; " + QUIET)]
    NEG_ROUND2 = ("chimney, factory, tower, smokestack, brick chimney, industrial building, boat, sampan, canopy, covered boat, "
                  "moored boat, raft, ship")
jobs, summary = [], []
for pid, base, first, rule, desc in PICTURES:
    src = LIVE / f"{base}.png"
    assert src.is_file(), f"refs-live/{base}.png is missing; {pid} is an edit of it"
    assert not (LIVE / f"{pid}.png").exists(), f"refs-live/{pid}.png already exists; pick a new l-number"
    body = rule + PLACE.format(desc=desc) + " " + STYLE
    for bad in (" no ", " not ", "without", "never", "nobody", "nothing", "gone"):
        assert bad not in body.lower(), f"{pid}: the positive prompt has '{bad.strip()}' (write what is there)"
    prompt = out / "prompts" / (f"{pid}-r2.txt" if ROUND2 else f"{pid}.txt")
    prompt.write_text(body, encoding="utf-8")
    neg = out / "prompts" / (f"negative-{pid}-r2.txt" if ROUND2 else f"negative-{pid}.txt")
    neg.write_text(NEG_BY[pid] + (", " + NEG_ROUND2 if ROUND2 else ""), encoding="utf-8")
    jobs += [{"id": f"{pid}-{s}", "reference_images": [str(src)], "prompt_file": str(prompt), "negative_file": str(neg),
              "width": 1312, "height": 736, "seed": s, "latent": "empty"} for s in SEEDS]
    summary.append({"picture": pid, "seeds": list(SEEDS), "base": "edit of " + base, "first_shot": first})
name = "r2" if ROUND2 else "e016"
(out / f"{name}.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
(out / f"{name}-pictures.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / f"{name}.json")
