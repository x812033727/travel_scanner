#!/usr/bin/env python3
"""screen-test-e031-e040.py OUT_DIR [--with-chen] [--horse-star] | OUT_DIR --r2 | OUT_DIR --r3 | OUT_DIR [--r2|--r3] --sheet :
the screen test of arc 4
(e031-e040 r2, 〈旱年〉), written 2026-11-17 before the arc's first episode, the way arc 3's was (screen-test-e021-e030.py).
NOT run by the writer (Colab Qwen-Image-Edit, paid; the coordinator runs it, approved 2026-11-17, bible 待決事項 1).
The manifest is meant for ~/mokaair-work/videos/_series/zhong-tian-qu-qi/live-screen-test-e031-e040/. Check before running:
    python3 -I .agents/skills/minimax-h3-colab/scripts/check_images_manifest.py OUT_DIR/e031-e040.json
(six warnings are expected: the three portraits, two seeds each, are 864x1152, the portrait canvas, not 16:9).

Round 1 (no flag): 19 pictures x seeds 37037/37038 = 38 jobs, one manifest OUT_DIR/e031-e040.json (cap 40). The spec of
every picture is r2-bible-e031-e040.md 〈試鏡〉 第一輪 (one line each, numbered 1-20 there); the inventory of what is reused,
cropped or graded for free is 〈盤點〉 above it. Picture 9 of the bible (set-xujia-tangfang-chen-l1) is NOT in: its free grade
(free-e031-e040/tangfang_chen.py, refs-live README 第 4 篇章) reads as grey morning light and is filed. --with-chen puts it
back (40 jobs) if the coordinator rejects the free picture, under the id set-xujia-tangfang-chen2-l1 (the free
one keeps set-xujia-tangfang-chen-l1).
- 3 faces (fresh, screen-test.py HEAD on the grey canvas, calm, mouth closed, hands and props out):
             diaoqi-portrait-l1 (e037 c18), baidaifu-portrait-l1 (e039 c01), duizhang-portrait-l1 (e038 c23; ONE-word id:
             pilot.py only reads one-word person ids, the e020 guild-master lesson).
- 2 props on the grey canvas: prop-zaohongma-l1 (the chestnut horse, full body side view; e038, e039, e051, e053) and
             prop-changqiang-l1 (Qin Shuang's spear, e037 c26 to e060; decided 2026-11-17, bible 待決事項 7).
             The horse's coat follows the e930 s36 takes (2026-11-17 frames: both seeds chestnut-red all over, the mane and
             tail the same red-brown, a dark brown leather bridle; 9301101 has a plain forehead, 9301102 a white star).
             Default: plain forehead. If the e930 pick is 9301102, run with --horse-star.
- 3 one-change edits of good live pictures (refs-live/README.md 第 16、17 集: Qwen edits work when they change one thing):
             set-xujia-yuan-han-l1 (set-xujia-yuan-dong-qing2-l1, the field beyond the wall dried to cracked earth; e031
             c18-c30, written as afternoon low sun to match the picture, bible 待決事項 6), set-ganxi-l1 (set-liuxi-he-l1 with
             the stream run dry; e031 c31), set-hantian-l1 (set-qiutian-l2, the stubble rows become dry cracked earth; e034).
- 11 fresh places on the grey canvas, each written with arc 3 round 2's lens line (35 mm at eye height, level, upright),
             never "24mm wide establishing" (the town square came out fish-eye twice with it): set-shangyou-ba-l1,
             set-jingkeng-l1, set-citang-l1, set-shentan-l1 (the water wheel: this arc's key prop), set-cunkou-l1,
             set-shanjiao-qu-l1, set-xujia-houmen-ye-l1, set-guandao-ye-l1, set-chengmen-ye-l1, set-yiguan-men-ye-l1,
             set-gucang-ye-l1.
Every pick gets a NEW id with its own l1 (pilot.py takes the newest l-version of a set id, and e910-e930 must rebuild byte
for byte); episodes send them by spec.json swap_pictures with absolute paths. Rounds 2-3 (seeds 37039/37040: shentan-gongdi,
hantian-yang, hantian-shou, shanjiao-qu-ye, then gucang-wai on the picked hantian-yang) were specs in the bible until the
round-1 picks were filed; the round-1 picks moved some of them (see --r2 and --r3 below).

Round 2 (--r2, written 2026-11-17 after the round-1 picks were filed; live-action/screen-test-e031-e040-r1-picks.md):
12 pictures x seeds 37039/37040 = 24 jobs, OUT_DIR/r2.json, images expected in OUT_DIR/out-r2/ (st31r2.sh).
- 10 retakes of round-1 REDOs, same ids (none of them is in refs-live):
  * prop-zaohongma-l1 as an edit of OUT_DIR/out/prop-zaohongma-l1-37037.png, the only seed the no-star rerun made
    (37038 timed out twice): the horse is kept, the modern English saddle on its quilted pad becomes a plain old-style
    saddle on a square felt cloth, and the pale line down the front of the face goes;
  * two one-change edits of a round-1 seed that was right except for one thing: diaoqi-portrait-l1 from
    OUT_DIR/out/diaoqi-portrait-l1-37037.png (face, hair, light kept; the fresh red cut becomes a long pale healed scar from
    the brow to the cheek, and the knot-button tunic with the red sash becomes a crossed-collar tunic with a rope belt: two
    things on one garment-and-face edit, the picks table's choice) and set-gucang-ye-l1 from
    OUT_DIR/out/set-gucang-ye-l1-37038.png (only the hanging glass lantern on its arm becomes a clay oil lamp on an iron
    plate on the post, rule 33);
  * set-jingkeng-l1 as an edit of the filed set-hantian-l1 (an eye-height dry field that already reads right: only a row
    of well pits, earth heaps, baskets and beams with ropes is added; round 1 drew a paved plaza with nooses and a blue
    top-down painting);
  * six fresh places on the grey canvas, redrawn with REAL_LENS (a person standing on the ground, eye height, level) and
    an anti-aerial, anti-render negative, each description rewritten from what went wrong (picks table):
    set-shangyou-ba-l1 (no cart, gentle hills), set-shentan-l1 (side view of the pond and a big wheel from the bank),
    set-cunkou-l1 (no poles, no fish-eye), set-shanjiao-qu-l1 (empty ditch at a hill foot, no village),
    set-guandao-ye-l1 (road crossing from the right, moon in front of the camera so no shadow of the photographer),
    set-yiguan-men-ye-l1 (a stone hitching post, cold moonlight).
- 2 of the bible's round-2 pictures whose base is filed: set-hantian-yang-l1 and set-hantian-shou-l1, one-change edits of
  refs-live/set-hantian-l1 (seed 37038: the near field is the block in front of the low earth ridge that crosses the
  picture; that block is flooded and planted / golden; everything beyond the ridge stays dry).
Round 3 (--r3): 3 pictures x seeds 37039/37040 = 6 jobs, OUT_DIR/r3.json, images in OUT_DIR/out-r3/; each is a one-change
edit of a round-2 pick and stops with a clear message until that pick is filed in refs-live: set-shentan-gongdi-l1
(set-shentan-l1, the wheel half built), set-shanjiao-qu-ye-l1 (set-shanjiao-qu-l1 relit to a clear night with a thin
setting moon) and set-gucang-wai-l1 (set-hantian-yang-l1 with a low plank granary added on the right, its door swung back).
Round 1 can no longer be regenerated as it ran: its picks are filed and the job loop refuses an id that is already in
refs-live; OUT_DIR/e031-e040.json stays as it was run (--sheet still works). Each round writes its prompt files to its own folder (OUT_DIR/prompts/, prompts-r2/, prompts-r3/), so a retaken id never
overwrites the round-1 text that e031-e040.json still points at.
The positive prompts are written only as what is there (bible 拍法 18); the things to keep out are in the negative files.

--sheet: after the run, writes contact sheets OUT_DIR/sheets/r1-NN.jpg from OUT_DIR/out/<id>-<seed>.png and
OUT_DIR/e031-e040-pictures.json (with --r2 / --r3: r2-NN.jpg / r3-NN.jpg from out-r2/ / out-r3/ and r2- / r3-pictures.json): one row per picture, the base picture (for an edit) and the two seeds side by side at
656 px wide, each labelled; four rows per sheet; a missing seed is a dark tile marked MISSING.
"""
import json
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

out = Path(sys.argv[1])
FLAGS = set(sys.argv[2:])
assert FLAGS <= {"--with-chen", "--horse-star", "--sheet", "--r2", "--r3"}, f"unknown flag(s): {FLAGS}"
ROUND = 3 if "--r3" in FLAGS else 2 if "--r2" in FLAGS else 1
assert not (ROUND > 1 and FLAGS & {"--with-chen", "--horse-star"}), "--with-chen / --horse-star are round-1 flags"
assert not {"--r2", "--r3"} <= FLAGS, "one round at a time"
here = Path(__file__).resolve().parent
LIVE = here.parent / "assets" / "refs-live"
NAME = "e031-e040"
SEEDS = (37037, 37038) if ROUND == 1 else (37039, 37040)
ROUND_NAME = NAME if ROUND == 1 else f"r{ROUND}"          # manifest OUT_DIR/<ROUND_NAME>.json
ROUND_OUT = out / ("out" if ROUND == 1 else f"out-r{ROUND}")  # where the runner script puts the PNGs


def sheet():
    from PIL import Image, ImageDraw, ImageFont
    pics = json.loads((out / f"{ROUND_NAME}-pictures.json").read_text(encoding="utf-8"))
    (out / "sheets").mkdir(exist_ok=True)
    font = ImageFont.load_default(size=22)
    tw, th, gap = 656, 368, 8  # a 1312x736 tile at half size; portraits are fitted into the same box

    def tile(path, label):
        t = Image.new("RGB", (tw, th), (24, 24, 24))
        if path and Path(path).is_file():
            im = Image.open(path).convert("RGB")
            im.thumbnail((tw, th))
            t.paste(im, ((tw - im.width) // 2, (th - im.height) // 2))
        else:
            label += "  MISSING"
        d = ImageDraw.Draw(t)
        d.rectangle((0, 0, tw, 30), fill=(0, 0, 0))
        d.text((8, 4), label, fill=(255, 220, 0), font=font)
        return t

    rows = []
    for p in pics:
        base = p.get("base_path")
        cells = [tile(base, "base " + Path(base).stem)] if base and "grey" not in Path(base).name else []
        cells += [tile(ROUND_OUT / f"{p['picture']}-{s}.png", f"{p['picture']} {s}") for s in p["seeds"]]
        rows.append(cells)
    per = 4
    for n in range(0, len(rows), per):
        chunk = rows[n:n + per]
        sh = Image.new("RGB", (3 * tw + 4 * gap, len(chunk) * (th + gap) + gap), (60, 60, 60))
        for r, cells in enumerate(chunk):
            for c, t in enumerate(cells):
                sh.paste(t, (gap + c * (tw + gap), gap + r * (th + gap)))
        dst = out / "sheets" / f"r{ROUND}-{n // per + 1:02d}.jpg"
        sh.save(dst, quality=88)
        print("sheet ->", dst)


if "--sheet" in FLAGS:
    sheet()
    sys.exit(0)

PROMPTS = out / ("prompts" if ROUND == 1 else f"prompts-r{ROUND}")
PROMPTS.mkdir(parents=True, exist_ok=True)
(out / "base").mkdir(exist_ok=True)
full = Path(tempfile.mkdtemp(prefix="st-full-"))  # screen-test.py writes its own manifests; keep them out of OUT_DIR
argv, sys.argv = sys.argv, ["screen-test.py", str(full)]  # screen-test.py imports sys itself and writes to argv[1]
st = runpy.run_path(str(here / "screen-test.py"), run_name="screen_test_lib")
sys.argv = argv
grey_p, grey_s = out / "base" / "grey-portrait.png", out / "base" / "grey-set.png"
for dst, (name, w, h) in ((grey_p, ("grey-portrait.png", 864, 1152)), (grey_s, ("grey-set.png", 1312, 736))):
    if not dst.is_file():
        shutil.copyfile(full / st["canvas"](name, w, h), dst)
shutil.rmtree(full, ignore_errors=True)

NEGATIVE_WORDS = (" no ", " not ", "without", "never", "nobody", "nothing", " gone", " none")
CANVAS = "image 1 is a plain mid-grey canvas: use it only as the size and shape of the frame and draw the whole scene below over all of it. "
# arc 3 round 2's lens line (set-guangchang-l1): the 24mm / "wide establishing" words bent two rounds into fish-eye panoramas
LENS = ("A photograph of a real location taken at eye height with a 35mm lens, the camera level and square to the scene, "
        "the horizon straight and level, every wall, post and tree trunk standing upright: {desc}.")
STYLE = ("Ancient China, Song dynasty. Style: a photorealistic live-action photograph of a real location for a Chinese "
         "historical costume drama, shot on a cinema camera with a normal 35mm lens, natural perspective, straight lines, "
         "natural light, real wood, bamboo, thatch, stone, brick, plaster, earth, cloth and water textures, deep focus, "
         "everything sharp from front to back; a real photograph, a clean natural film image that fills the whole frame "
         "edge to edge.")
QUIET = "the place is quiet and deserted at this hour, every surface plain and bare"
KEEP_TAIL = (" A real photograph, photorealistic live-action film image of a real location, natural light, deep focus, fills "
             "the whole frame edge to edge.")
NEG = ("3D render, CGI, game render, plastic, cartoon, anime, illustration, painting, text, writing, calligraphy, Chinese "
       "characters, letters, numbers, inscription, signboard, plaque, couplet, banner, flag, poster, lantern, watermark, logo, "
       "people, person, crowd, figure, man, woman, child, silhouette, shadow of a person, statue, animal, weapon, spear, "
       "sword, knife, axe, weapon rack, black bars, border, fisheye, fish-eye lens, ultra wide angle, barrel distortion, "
       "curved horizon, bent horizon, tilted buildings, leaning walls, 360 panorama, dutch angle")
NIGHT_NEG = ", daylight, sunlight, sun, sunbeams, light shafts, blue daytime sky, bright sky, daytime"
NO_WHEEL = ", water wheel, waterwheel, mill wheel"
FIELD_NEG = ", flooded paddy field, water in the field, green rice, green crops, flowering tree, blossoms"

pictures = []  # (picture id, episode/shot that first needs it, base image path, prompt, negative, width, height, how)

# --- three new faces, drawn fresh like zhengbo/tangwanjin (screen-test-e021-e030.py) -------------------------------------
FACES = [
    ("diaoqi-portrait-l1", "e037 c18",
     "an East Asian man of thirty-five, tall and powerfully built with broad shoulders, a square jaw and thick dark "
     "eyebrows, hard watchful eyes, one long pale old scar in a single line running from his left brow bone down across "
     "his left cheekbone, black hair tied up in a rough topknot bound with a strip of torn cloth, an ancient Chinese "
     "Song-dynasty bandit's ragged rough earth-brown hemp cross-collared short tunic with frayed worn edges"),
    ("baidaifu-portrait-l1", "e039 c01",
     "an East Asian old man of sixty-eight, lean and spare with a thin lined face, bright sharp eyes, white hair in a small "
     "neat topknot, a white beard and moustache trimmed short at the line of his chin, an ancient Chinese Song-dynasty "
     "physician's faded moon-white old cross-collared long gown under a plain quilted off-white cotton vest"),
    ("duizhang-portrait-l1", "e038 c23",
     "an East Asian man in his forties, a broad square face, a short black beard and moustache, steady stern eyes, an "
     "ancient Chinese Song-dynasty garrison captain's black iron lamellar armour over his chest and shoulders, an "
     "open-faced round black iron helmet with one small tuft of red horsehair fixed at its very top"),
]
for pid, first, desc in FACES:
    assert not re.search(r"smil|grin|knife|sword|spear|medicine|lamp", desc), f"{pid}: a smile or a prop is in the portrait"
    body = st["BLANK"] + st["HEAD"].format(desc=re.sub(st["FEET"], "", desc)) + " " + st["STYLE"]
    neg = st["NEG"] + (", helmet without plume, red cloth hanging, red ribbons, red tassel on the shoulders, cape"
                       if pid.startswith("duizhang") else "")
    pictures.append((pid, first, grey_p, body, neg, 864, 1152, "fresh portrait on the grey canvas"))

# --- two props on the grey canvas -----------------------------------------------------------------------------------------
STAR = "a small white star on the middle of the forehead" if "--horse-star" in FLAGS else "a plain chestnut-red forehead"
horse = (CANVAS + "A photograph of one real horse standing in a plain mid-grey photo studio, the whole horse in the frame "
         "from the tips of its ears to its four hooves, seen exactly from the side, its head to the left: a strong "
         "chestnut-red horse with a glossy red-brown coat all over, the mane and the tail the same deep red-brown, "
         f"{STAR}, dark hooves; a plain dark brown leather bridle and reins and a plain dark brown leather saddle with "
         "plain iron stirrups; it stands calmly with all four hooves on the floor, its weight even, its ears forward. "
         "The plain mid-grey backdrop runs behind it and under its hooves, soft even studio light, a soft shadow under the "
         "horse. Style: a photorealistic live-action photograph of a real horse for a Chinese historical costume drama, "
         "a normal 50mm lens at the height of the horse's shoulder, natural perspective, real coat, hair and leather "
         "textures, sharp focus; a clean natural film image that fills the whole frame edge to edge.")
pictures.append(("prop-zaohongma-l1", "e038 c20", grey_s, horse,
                 "3D render, CGI, game render, plastic, cartoon, anime, illustration, painting, toy horse, statue, text, "
                 "writing, watermark, logo, people, rider, person, hands, black mane, black tail, white socks, white legs, "
                 "spots, grey horse, white horse, black horse, two horses, foal, saddle blanket with patterns, tassels, "
                 "bells, red ribbons, decorations, armour, rearing, galloping, running, cropped legs, cropped head, "
                 "extra legs, five legs, black bars, border, outdoor field, fence", 1312, 736,
                 "fresh prop on the grey canvas"))
spear = (CANVAS + "A photograph of one real prop lying flat on a floor of dark old wooden planks, seen from straight above, "
         "the whole prop in the frame from end to end, lying level from the left edge to the right edge: a long spear "
         "taller than a man, a straight plain pale wooden shaft as thick as a thumb, worn smooth, its butt end bound with a "
         "short band of plain iron, and at the right end one small plain leaf-shaped iron spearhead, dull grey and a little "
         "worn, fixed to the shaft by a short plain iron socket. Soft even light, the planks dark brown with fine grain. "
         "Style: a photorealistic live-action product photograph of a real film prop for a Chinese historical costume "
         "drama, real wood and iron textures, sharp focus from end to end; a clean natural film image that fills the "
         "whole frame edge to edge.")
pictures.append(("prop-changqiang-l1", "e037 c26", grey_s, spear,
                 "3D render, CGI, game render, plastic, cartoon, anime, illustration, painting, text, writing, engraving, "
                 "watermark, logo, people, hands, red tassel, red horsehair, red fringe, ribbon, flag, two spears, second "
                 "spear, halberd, axe blade, trident, crescent blade, sword, knife, bow, arrows, gold, jewels, ornate "
                 "decoration, carved dragon, black bars, border, fisheye, curved shaft", 1312, 736,
                 "fresh prop on the grey canvas"))

# --- one-change edits of good live pictures ---------------------------------------------------------------------------------
han = ("Image 1 is a photograph of a farmhouse yard: keep exactly everything in it - the camera position, the thatched "
       "farmhouse on the left with its dark doorway, its lattice window and the stack of split firewood, the wooden yard "
       "gate in the middle of the back wall under its small tiled roof, the bare tree and all its branches, the wooden "
       "bucket, the wooden boards leaning on the wall, the round stone well with its wooden windlass at the front right, "
       "the low stone-and-mud wall along the right, the earth of the yard, the far hills and the low warm sun at the right "
       "with its long shadows. Change only one thing: beyond the wall and through the open gate, the wide field is dry "
       "bare earth, pale yellow-brown and cracked into flat plates, with a few short dry broken stalks standing here and "
       "there, the far stream a thin dry line of pale stones, a little dust hanging in the warm light." + KEEP_TAIL)
pictures.append(("set-xujia-yuan-han-l1", "e031 c18", LIVE / "set-xujia-yuan-dong-qing2-l1.png", han,
                 NEG + NO_WHEEL + ", golden wheat, ripe grain, standing crops, green crops, green grass, rice, water, "
                                  "puddle, river, rain, snow, persimmons, fruit on the tree, leaves on the tree", 1312, 736,
                 "one change of set-xujia-yuan-dong-qing2-l1"))
ganxi = ("Image 1 is a photograph of a village stream: keep exactly everything in it - the camera position, the long wooden "
         "plank walkway on its posts running away down the middle, the weeping willows and the grey-tiled village houses "
         "on the left bank, the clumps of grass along both banks, the field on the right, the far hills and the sky. Change "
         "only one thing: the stream has run completely dry; its bed lies bare and empty under the walkway from bank to "
         "bank, pale grey-brown mud dried and cracked into flat curling plates, scattered round river stones and pebbles, "
         "a few dead waterweeds lying flat on the dry mud; the posts of the walkway stand in dry cracked mud; dry warm "
         "air." + KEEP_TAIL)
pictures.append(("set-ganxi-l1", "e031 c31", LIVE / "set-liuxi-he-l1.png", ganxi,
                 NEG + NO_WHEEL + ", water, river, stream water, puddle, pond, reflection in water, wet mud, rain, boat, "
                                  "bridge collapse", 1312, 736, "one change of set-liuxi-he-l1"))
hantian = ("Image 1 is a photograph of farm fields: keep exactly everything in it - the camera position, the long straight "
           "rows of the field running away from the camera, the grassy bank on the right, the big willow tree on the "
           "right, the low village houses and the small trees in the distance, the hills and the clear blue sky, and the "
           "low clear sunlight. Change only one thing: every row of the field is dry bare earth, pale yellow-brown and "
           "cracked into flat plates, the rows only low dry ridges of cracked soil with a few short dry broken stubble "
           "stalks." + KEEP_TAIL)
pictures.append(("set-hantian-l1", "e034 c27", LIVE / "set-qiutian-l2.png", hantian,
                 NEG + NO_WHEEL + FIELD_NEG + ", golden stubble, straw, harvested rice, water channel, puddle, mud",
                 1312, 736, "one change of set-qiutian-l2"))
if "--with-chen" in FLAGS:
    chen = ("Image 1 is a photograph of a small bedroom in a farmhouse: keep exactly everything in it - the camera position, "
            "the wooden door on the left, the cracked plaster walls, the wooden bed against the back wall with its pink "
            "quilted quilt and pillow, the window above the bed with its wooden frame, the wooden table at the front right "
            "with the two flat bundles and the white candle on it, the beams of the ceiling. Change only one thing, the "
            "time and the light: it is early morning; the window paper glows a soft pale white with grey dawn light, a "
            "soft cool grey-white light from the window falls on the bed, the walls and the table, the white candle on the "
            "table is cold and unlit with a black wick." + KEEP_TAIL)
    pictures.append(("set-xujia-tangfang-chen2-l1", "e038 c01", LIVE / "set-xujia-tangfang-l2.png", chen,
                     NEG + ", night, dark blue window, candle flame, lit candle, glowing candle, warm orange light, moon, "
                           "oil lamp", 1312, 736, "relight of set-xujia-tangfang-l2"))

# --- fresh places on the grey canvas ----------------------------------------------------------------------------------------
FRESH = [
    ("set-shangyou-ba-l1", "e031 c32",
     "the end of a dry stony riverbed in early spring on a hot dry afternoon: across the riverbed from bank to bank runs a "
     "low dam built of piled grey stones and hemp-sack earth bags, a flat earth track along its top wide enough for a cart; "
     "behind the dam a still pool of brown water; on the right a freshly dug earth ditch leads the water away from the pool "
     "into a field of bright green young rice; in front of the dam the dry riverbed of cracked mud and stones with a heap of "
     "big boulders; the stream bank on the left is dry bare earth; hot hazy white sunlight from high on the left, dust in "
     "the air; " + QUIET, NO_WHEEL + ", cart, mule, horse, concrete, modern dam, sluice gate of metal, pipes"),
    ("set-jingkeng-l1", "e032 c12",
     "a dry cracked hillside field at the edge of a village in early morning: a row of about twelve freshly dug square "
     "wells runs from the front left of the picture to the back right, each a dark square hole in the ground beside a heap "
     "of fresh yellow earth and one bamboo basket, over each hole a short wooden post with a coil of thick hemp rope hanging "
     "from it into the hole; the hole in the middle of the row is the deepest; the field around them is dry pale yellow "
     "earth cracked into plates; soft grey-white dawn light, a thin morning mist lying low over the ground; " + QUIET,
     ", head in the hole, person in the well, ladder, bucket of water, water, machinery, fence"),
    ("set-citang-l1", "e032 c27",
     "the inside of a small old village ancestral hall at dusk: on the left two tall wooden lattice doors stand pushed "
     "open inward, the warm last daylight of dusk outside them; on the right a long dark wooden offering table against the "
     "wall with a bronze incense burner and a row of small plain dark wooden ancestor tablets with smooth blank faces, two "
     "tall white candles burning at the two ends of the table; above the table one thick dark beam of a single whole tree "
     "trunk runs across the hall; the floor of worn grey-blue stone slabs; dim warm light from the candles and the doors; "
     + QUIET, ", writing on the tablets, characters on the wall, couplets, scrolls, portraits, statue of a god, red banners, "
              "red lanterns, many candles"),
    ("set-shentan-l1", "e033 c27",
     "the bottom of a deep rocky gully at noon: on the right a deep still pool of dark green water; at the edge of the pool, "
     "standing between two strong wooden frames, one large complete wooden water wheel about six metres across, its rim "
     "dipping into the pool: a thick wooden axle, twelve wide flat wooden paddles evenly round the rim, a ring of bamboo "
     "tubes tied along the rim; on the left at the mouth of the pool a wooden sluice board held by a thick rope, a short "
     "stone channel running from it under the wheel; from the top of the wheel a wooden trough carries water to a dug "
     "earth channel that climbs away to the upper right toward a dry cracked field; on the left bank a flat open patch of "
     "bare earth, on the right a big grey boulder, at the upper right the low earth ridge of a field; strong overhead noon "
     "sunlight, short shadows; " + QUIET,
     ", small wooden wheel, narrow wheel, tower, windmill, mill house, metal wheel, modern machinery, two wheels, "
     "broken wheel, waterfall"),
    ("set-cunkou-l1", "e035 c22",
     "the entrance of a poor village at dusk under an orange-red sky: on the left two heavy rough wooden palisade gates "
     "with one thick wooden bar lying across them, above the gates a small wooden gate tower with a little tiled roof; "
     "outside the gates a dirt road leads to a small wooden plank bridge over a dry ditch, an old willow tree beside the "
     "gates, low hills in the distance; on the right the village lane runs in between a few low mud-walled thatched houses; "
     "the gate posts are bare wood; warm orange dusk light from the right, long soft shadows; " + QUIET,
     ", torches, fire, red cloth, red strips, writing on the gate, guards, horse, cart"),
    ("set-shanjiao-qu-l1", "e036 c14",
     "the foot of a low brown mountain on a clear morning: a freshly dug dry irrigation channel about as deep as a man is "
     "tall, its bottom of dry earth, runs from the right of the picture to the left up to the foot of the mountain; at the "
     "head of the channel by the mountain a low earth embankment three paces wide crosses the channel, with one wooden "
     "sluice board set in it and a heap of dry straw beside it; both banks of the channel are dry pale yellow earth cracked "
     "into plates; far off on the right one small square field of green rice; bright white morning light; " + QUIET,
     NO_WHEEL + ", water in the channel, river, concrete, pipes, tools, shovels, carts"),
    ("set-xujia-houmen-ye-l1", "e037 c29",
     "the back gate of a poor farmhouse at night under a clear moon: a low wall of mud and stone runs across the picture, "
     "in it one narrow plank door standing half open, a stack of split firewood against the wall beside it; through the "
     "door and outside the wall a dark narrow lane runs away to the left between other low walls; cold blue moonlight lies "
     "on the top of the wall, the door and the firewood, the lane in deep shadow; the moonlight is the only light; " + QUIET,
     NIGHT_NEG + ", torch, fire, lit windows, moon disc in the sky, tiled roof gate, front gate"),
    ("set-guandao-ye-l1", "e038 c20",
     "a wide country high road of packed yellow earth at night, running from the right of the picture away to the left "
     "into the distance; on both sides dry bare fields; along the road a row of tall poplar trees stands as black shapes "
     "against the night sky; the moon at the upper right; cold blue moonlight on the road and the fields, long soft "
     "shadows of the poplars across the road; the moonlight is the only light; " + QUIET,
     NIGHT_NEG + ", milestone, stone tablet, stele, road sign, signpost, torch, fire, houses, cart, horse"),
    ("set-chengmen-ye-l1", "e038 c22",
     "the gate of a walled county town at night, the gate on the left of the picture: a tall grey brick gate tower over "
     "an arched gateway; the two great wooden gate doors studded with rows of iron nails stand shut; beside the gateway a "
     "small wooden side door stands half open; two burning torches set in iron brackets on the brick wall throw warm "
     "orange light; across the road in front of the gate stands a waist-high barrier of crossed wooden stakes; on the "
     "right the dirt road comes in from the dark countryside; cold blue moonlight elsewhere; " + QUIET,
     NIGHT_NEG + ", plaque over the gate, name board, notice board, posters, banners, guards, soldiers, many torches, "
                 "lanterns"),
    ("set-yiguan-men-ye-l1", "e038 c29",
     "the front of a small old shop on a narrow street of a county town at night, the shop front on the right of the "
     "picture: two plain wooden door panels shut, two stone steps up to them, a wooden hitching post standing in front of "
     "the steps; on both sides other shop fronts with their wooden shutters closed; the beam over every door is plain bare "
     "wood; cold blue moonlight on the stone-paved street, the eaves throwing deep shadows; the moonlight is the only "
     "light; " + QUIET,
     NIGHT_NEG + ", signboard over the door, shop sign, hanging sign, lanterns, lit windows, red silk, torches, horse"),
    ("set-gucang-ye-l1", "e040 c32",
     "the inside of a low wooden plank granary at night: on the right a row of stacked new hemp grain sacks, straw spread "
     "on the earth floor, a few round bamboo baskets, one wooden ladder leaning on the wall; on the left a wooden post with "
     "an iron bracket holding one small clay oil lamp, its small flame the only light, warm and soft on the sacks, the "
     "planks and the straw; at the back right a heavy plank door shut; high on the back wall one small window showing deep "
     "blue night; the corners in deep shadow; " + QUIET,
     NIGHT_NEG + ", moonbeams, light shafts through the window, beams of light, many lamps, candles, torches, lanterns, "
                 "fire on the floor"),
]
for pid, first, desc, extra in FRESH:
    pictures.append((pid, first, grey_s, CANVAS + LENS.format(desc=desc) + " " + STYLE, NEG + extra, 1312, 736,
                     "fresh place on the grey canvas, 35mm"))

# --- rounds 2 and 3 (2026-11-17, after the round-1 picks: live-action/screen-test-e031-e040-r1-picks.md) -----------------
# Round 1's list above is only built to keep its checks; a later round replaces it.
REAL_LENS = ("A real photograph taken by a person standing on the ground, the camera at the height of a man's eyes with a "
             "normal 35mm lens, pointing straight ahead and level, the horizon a straight level line across the upper part "
             "of the frame, every wall, post and tree trunk standing upright: {desc}.")
REAL_NEG = (", aerial view, drone shot, bird's-eye view, top-down view, high angle, looking down from above, 3D illustration, "
            "concept art, matte painting, digital painting, video game scenery, toy model, miniature, oversaturated colours, "
            "HDR, glossy surfaces, vignette, lens flare")


def r1_seed(pid, seed):
    p = out / "out" / f"{pid}-{seed}.png"
    assert p.is_file(), f"{p} is missing: round 2 edits that round-1 seed"
    return p


def filed(pid, needed_by):
    p = LIVE / f"{pid}.png"
    assert p.is_file(), f"refs-live/{pid}.png is not filed yet: {needed_by} edits it (pick it first)"
    return p


if ROUND == 2:
    pictures = []
    # diaoqi: 37037 has the right face (35, square jaw, not erniu's twin); its cut is fresh and red and short, and its
    # tunic has knot buttons and a red sash. The edit keeps the face and changes the scar and the tunic front.
    diaoqi = ("Image 1 is a casting portrait of a man in front of a plain mid-grey studio backdrop: keep exactly everything "
              "in it - the camera position and the framing, his face, his eyes, his thick eyebrows, his nose, his mouth "
              "and his square jaw, his calm hard expression with the mouth closed, his black hair in a rough topknot "
              "bound with a strip of torn cloth, his bare muscular arms, the grey backdrop and the soft light. Change only "
              "the scar and the front of his tunic: the scar is one long old scar, healed smooth, a single slightly raised "
              "line paler than the skin around it, starting at the outer end of his left eyebrow and running down across "
              "his left cheekbone to the middle of his cheek; his tunic is the same ragged earth-brown hemp, now a "
              "cross-collared tunic wrapped left over right across his chest and closed by its own overlap, a plain belt "
              "of twisted hemp rope tied round his waist, the frayed short sleeves as they are." + KEEP_TAIL)
    pictures.append(("diaoqi-portrait-l1", "e037 c18", r1_seed("diaoqi-portrait-l1", 37037), diaoqi,
                     st["NEG"] + ", fresh wound, open cut, blood, red cut, red scar, scab, stitches, knot buttons, frog "
                                 "buttons, toggles, Chinese buttons, red sash, red belt, coloured sash, sleeveless", 864, 1152,
                     "edit of the round-1 portrait 37037"))
    # gucang-ye: 37038 is right except the hanging glass lantern (a hung lantern and a kerosene lamp).
    gucang = ("Image 1 is a photograph of the inside of a wooden granary at night: keep exactly everything in it - the "
              "camera position, the plank walls, the stack of hemp grain sacks in the middle, the wooden ladder leaning "
              "on the right, the three wooden tubs, the straw on the earth floor, the small barred window showing deep "
              "blue night, the plank door at the right, the wooden post at the left edge and the warm low light. Change "
              "only one thing: the hanging lamp and the wooden arm it hangs from at the upper left become one small open "
              "clay oil lamp with a single small flame, sitting on a flat iron plate fixed to the side of the wooden post "
              "at the height of a man's shoulder; its flame is the only light, warm on the sacks, the planks and the "
              "straw." + KEEP_TAIL)
    pictures.append(("set-gucang-ye-l1", "e040 c32", r1_seed("set-gucang-ye-l1", 37038), gucang,
                     NEG + NIGHT_NEG + ", hanging lantern, glass lantern, hurricane lamp, kerosene lamp, oil lantern with "
                                       "glass, chain, hook, bracket arm, candles, torches, many lamps", 1312, 736,
                     "one change of round-1 seed 37038"))
    # prop-zaohongma-l1: the no-star rerun of round 1 made only 37037 (37038 timed out twice, 2026-11-17 20:00). 37037 has
    # the right horse (side view, red-brown all over, mane and tail the same, close to e930 s36 take 9301101) but a modern
    # English riding saddle on a quilted saddle pad, and a pale line along the front of the face; the edit keeps the horse.
    horse2 = ("Image 1 is a photograph of one chestnut-red horse standing side-on in a plain grey photo studio: keep exactly "
              "everything in it - the camera position and the framing, the whole horse from the tips of its ears to its "
              "hooves, its pose, its glossy red-brown coat, its red-brown mane and tail, its dark hooves, the dark brown "
              "leather bridle and reins, the grey backdrop, the soft light and the shadow under it. Change only the saddle "
              "and the face: the saddle is one plain dark brown leather saddle of an old Chinese style, with a high rounded "
              "front and a high rounded back, sitting on one plain dark brown felt cloth cut square, plain iron stirrups "
              "hanging on plain dark leather straps; the whole face from the forelock to the nose is the same even "
              "chestnut red as the neck." + KEEP_TAIL)
    pictures.append(("prop-zaohongma-l1", "e038 c20", r1_seed("prop-zaohongma-l1", 37037), horse2,
                     "3D render, CGI, game render, plastic, cartoon, anime, illustration, painting, toy horse, statue, text, "
                     "writing, watermark, logo, people, rider, person, hands, English saddle, modern riding saddle, quilted "
                     "saddle pad, saddle pad with piping, white star, blaze, white stripe on the face, white socks, black "
                     "mane, black tail, tassels, bells, red ribbons, decorations, armour, cropped legs, cropped head, extra "
                     "legs, black bars, border", 1312, 736, "one change of round-1 seed 37037"))
    # jingkeng: an edit of the filed dry field (eye height, real enough) instead of a fresh draw.
    jingkeng = ("Image 1 is a photograph of dry farm fields: keep exactly everything in it - the camera position, the dry "
                "cracked earth of the fields and the low earth ridge across them, the big willow tree on the right, the "
                "low village houses and small trees in the distance, the hills, the clear sky and the low clear sunlight. "
                "Add only one thing: a single row of twelve freshly dug square well pits runs across the cracked field "
                "from the near left corner diagonally away to the far right; each pit is a dark square hole one stride "
                "wide with a heap of fresh yellow earth and one round bamboo basket beside it, and one short wooden beam "
                "laid across its rim with a thick hemp rope tied round the beam and hanging straight down into the "
                "dark hole; the pit in the middle of the row is the deepest, with the biggest heap of earth; a thin low "
                "haze of early morning lies over the ground." + KEEP_TAIL)
    pictures.append(("set-jingkeng-l1", "e032 c12", filed("set-hantian-l1", "set-jingkeng-l1"), jingkeng,
                     NEG + NO_WHEEL + ", noose, rope loop, hangman's knot, paving, tiles, stone slabs, street, plaza, new "
                                      "houses in the field, people in the pits, head in the hole, ladder, water, flooded "
                                      "field, green rice, top-down view, aerial view", 1312, 736,
                     "one change of set-hantian-l1"))
    FRESH2 = [
        ("set-shangyou-ba-l1", "e031 c32",
         "a dry stony stream bed in a farming valley of low rounded green hills on a hot hazy afternoon in early spring: "
         "in the foreground the dry bed of grey cracked mud and loose rounded river stones runs straight away from the "
         "camera between two low earth banks; in the middle distance a low dam about as high as a man's chest crosses "
         "the bed from the left bank to the right bank, built of piled grey field stones and stacked brown hemp "
         "sandbags, a flat path of packed earth along its top; behind the dam a still pool of brown water; on the right "
         "bank a freshly dug earth ditch carries water off from the pool to one small field of bright green young rice; "
         "the left bank dry bare earth; hazy white sunlight, dust in the air; " + QUIET,
         NO_WHEEL + REAL_NEG + ", cart, wagon, wheelbarrow, mule, horse, karst peaks, steep pointed mountains, rice "
                               "terraces, terraced hills, concrete, modern dam, metal sluice gate, pipes"),
        ("set-shentan-l1", "e033 c27",
         "a round deep pool at the bottom of a shallow gully at noon, seen from the dry bank on the left: the pool of dark "
         "green still water fills the right half of the picture; standing in the pool near its left edge, seen from the "
         "side, one large wooden water wheel as tall as three men, twelve flat wooden paddles evenly spaced round its rim, "
         "a ring of small bamboo tubes tied along the rim, its thick round wooden axle resting on two heavy wooden "
         "A-frames planted one on each side of the wheel; a short stone channel runs from a wooden sluice board on the "
         "left side of the pool to under the wheel; from the top of the wheel a long open wooden trough on wooden posts "
         "carries water to a narrow earth ditch that climbs away to the upper right toward dry cracked fields; on the "
         "left bank a bare flat patch of earth; one big grey boulder on the right bank; a field ridge along the top right; "
         "strong overhead noon light, short shadows; " + QUIET,
         REAL_NEG + ", small wooden wheel, narrow wheel, tower, windmill, mill house, metal wheel, two wheels, broken wheel, "
                    "straight canal, brick channel, paving stones, waterfall, modern machinery"),
        ("set-cunkou-l1", "e035 c22",
         "the entrance of a small poor farming village at dusk under an orange-red sky: on the left two heavy gates of "
         "rough upright logs stand shut with one thick wooden bar laid across their middle, under a small gate roof of "
         "dark grey tiles on two log posts; outside the gates a dirt road in the foreground leads to a short plank "
         "footbridge over a dry ditch; beside the gates one old willow tree with long drooping branches; on the right a "
         "dirt village lane goes away past three low mud-brick houses with thatched roofs; low hills behind; warm orange "
         "light from the right, long soft shadows; " + QUIET,
         REAL_NEG + ", poles with crossbars, utility poles, power lines, wires, red figures, red cloth, red strips, torches, "
                    "fire, lanterns, writing on the gate, guards, horse, cart, render"),
        ("set-shanjiao-qu-l1", "e036 c14",
         "the foot of a steep brown scrubby hillside on a clear morning: a freshly dug empty irrigation ditch as deep as a "
         "man is tall, its bottom of dry brown earth, runs from the near right of the picture away to the left and ends at "
         "the foot of the hillside that fills the left background; near the hill end a raised earth bank three strides "
         "wide crosses the ditch, one plain wooden sluice board standing in a slot in the bank and a heap of dry straw on "
         "top of it; both banks are dry yellow earth cracked into plates, with fresh heaps of dug soil along them; far "
         "away on the right one small patch of green young rice; flat white morning light; " + QUIET,
         NO_WHEEL + REAL_NEG + ", water in the ditch, river, village, houses, rows of houses, pyramids, desert dunes, "
                               "sand, concrete, pipes, tools, shovels, carts"),
        ("set-guandao-ye-l1", "e038 c20",
         "a wide country high road of packed yellow earth at night: the road comes in from the right foreground and runs "
         "across the picture away to the far left; dry bare fields on both sides; a line of tall poplar trees along the "
         "far side of the road, black shapes against the night sky; the moon high in the upper right of the picture, in "
         "front of the camera; cold blue moonlight on the road and the fields, the long shadows of the poplars falling "
         "toward the camera across the road; the moonlight is the only light; the road empty; " + QUIET,
         NIGHT_NEG + REAL_NEG + ", the photographer's shadow, human shadow on the road, footprints, car lights, headlights, "
                                "distant lights, street lamps, milestone, stone tablet, stele, road sign, signpost, torch, "
                                "fire, houses, cart, horse"),
        ("set-yiguan-men-ye-l1", "e038 c29",
         "the front of a small old shop on a narrow stone-paved street of a Song-dynasty county town at night, the shop "
         "front on the right of the picture: two plain wooden door boards shut, two worn stone steps up to them, the "
         "lintel above the door plain bare wood; in front of the steps, at the edge of the street, one short plain stone "
         "hitching post, a square grey stone pillar as high as a man's waist with a round hole through its top; on both "
         "sides the next shops' door boards are shut, grey tiled eaves above; cold blue moonlight on the paving stones "
         "and the shop fronts, the eaves throwing deep shadows; the moonlight is the only light; " + QUIET,
         NIGHT_NEG + REAL_NEG + ", cross, crucifix, wooden post with a crossbar, signboard over the door, shop sign, hanging "
                                "sign, notice board, lanterns, lit windows, red silk, torches, horse, warm orange light on "
                                "the walls, Japanese architecture"),
    ]
    for pid, first, desc, extra in FRESH2:
        pictures.append((pid, first, grey_s, CANVAS + REAL_LENS.format(desc=desc) + " " + STYLE, NEG + extra, 1312, 736,
                         "fresh place on the grey canvas, 35mm, round-2 lens"))
    # the bible's round 2, base filed: the near block in front of the ridge (seed 37038 of set-hantian-l1)
    keep_field = ("Image 1 is a photograph of dry farm fields: keep exactly everything in it - the camera position, the low "
                  "earth ridge that crosses the fields from the left to the willow, the dry cracked rows beyond the ridge, "
                  "the big willow tree on the right, the low village houses and small trees in the distance, the hills, "
                  "the clear sky and the low clear sunlight. Change only one thing: the near field, the block in front of "
                  "the ridge that fills the lower half of the picture, ")
    yang = (keep_field + "is flooded with a thin sheet of still shallow water that mirrors the sky, planted with straight "
            "sparse rows of small young green rice seedlings standing in the water, the low earth ridges around it "
            "wet and dark; every field beyond the ridge stays dry pale cracked earth." + KEEP_TAIL)
    shou = (keep_field + "is a full field of ripe golden rice, the heavy golden heads bending low on yellow stalks, "
            "standing thick right to the edges of the block; every field beyond the ridge stays dry pale cracked "
            "earth." + KEEP_TAIL)
    hantian = filed("set-hantian-l1", "set-hantian-yang-l1 and set-hantian-shou-l1")
    pictures.append(("set-hantian-yang-l1", "e035 c09", hantian, yang,
                     NEG + NO_WHEEL + ", flooded valley, every field flooded, water beyond the ridge, green fields beyond "
                                      "the ridge, ripe grain, golden rice, flowers, rain, people, buffalo", 1312, 736,
                     "one change of set-hantian-l1"))
    pictures.append(("set-hantian-shou-l1", "e040 c13", hantian, shou,
                     NEG + NO_WHEEL + ", green rice, water, flooded field, golden fields beyond the ridge, wheat, sheaves, "
                                      "harvesters, sickles, people, buffalo, flowers", 1312, 736,
                     "one change of set-hantian-l1"))
elif ROUND == 3:
    pictures = []
    gongdi = ("Image 1 is a photograph of a deep pool in a gully with a wooden water wheel: keep exactly everything in it - "
              "the camera position, the pool, its banks, the boulder, the field ridge, the dry fields, the stone channel, "
              "the sluice board and the noon light. Change only one thing: the water wheel is half built: only its two "
              "heavy wooden A-frames and the thick wooden axle laid across them stand there, with half of the spokes "
              "fitted on one side and the rim and paddles still missing; a pile of sawn timber, planks and bamboo tubes "
              "lies on the bare patch of the left bank." + KEEP_TAIL)
    qu_ye = ("Image 1 is a photograph of a dry irrigation ditch at the foot of a hillside: keep exactly everything in it - "
             "the camera position, the ditch, the earth bank across it with the sluice board and the straw, the heaps of "
             "dug soil, the hillside, the far patch of rice. Change only one thing, the time and the light: it is a clear "
             "night late in the night; a thin crescent moon low in the west at the upper left, its cold blue light faint "
             "on the earth, the ditch bottom and the hillside in deep shadow, the sky dark blue with stars." + KEEP_TAIL)
    wai = ("Image 1 is a photograph of farm fields with one flooded field of young rice: keep exactly everything in it - "
           "the camera position, the flooded field and its young rice, the low ridge, the dry fields beyond, the willow, "
           "the far village, the hills, the sky and the light. Change only one thing: on the right side of the picture, on "
           "the dry ground beside the flooded field, stands one low granary of grey weathered wooden planks with a low "
           "thatched roof, its one heavy plank door swung back against the wall, the inside dark." + KEEP_TAIL)
    pictures += [
        ("set-shentan-gongdi-l1", "e033 c14", filed("set-shentan-l1", "set-shentan-gongdi-l1"), gongdi,
         NEG + ", finished water wheel, paddles on the rim, complete rim, two wheels, tower, crane, scaffolding with people",
         1312, 736, "one change of set-shentan-l1"),
        ("set-shanjiao-qu-ye-l1", "e037 c01", filed("set-shanjiao-qu-l1", "set-shanjiao-qu-ye-l1"), qu_ye,
         NEG + NIGHT_NEG + ", full moon, bright moon, torch, fire, lamps, water in the ditch", 1312, 736,
         "relight of set-shanjiao-qu-l1"),
        ("set-gucang-wai-l1", "e039 c24", filed("set-hantian-yang-l1", "set-gucang-wai-l1"), wai,
         NEG + NO_WHEEL + ", second building, many buildings, signboard on the granary, lanterns, carts, people, fence",
         1312, 736, "one change of set-hantian-yang-l1"),
    ]

jobs, summary = [], []
for pid, first, base, body, neg, w, h, how in pictures:
    assert Path(base).is_file(), f"{base} is missing"
    folder = LIVE / "angles" if "angle" in pid else LIVE
    assert not (folder / f"{pid}.png").exists(), f"refs-live/{pid}.png already exists; pick a new id"
    if "portrait" not in how:  # the portraits keep screen-test.py's HEAD frame (arc 2's faces were drawn with it)
        for bad in NEGATIVE_WORDS:
            assert bad not in body.lower(), f"{pid}: the positive prompt has '{bad.strip()}' (write what is there)"
    prompt = PROMPTS / f"{pid}.txt"
    prompt.write_text(body, encoding="utf-8")
    negf = PROMPTS / f"negative-{pid}.txt"
    negf.write_text(neg, encoding="utf-8")
    jobs += [{"id": f"{pid}-{s}", "reference_images": [str(Path(base).resolve())], "prompt_file": str(prompt.resolve()),
              "negative_file": str(negf.resolve()), "width": w, "height": h, "seed": s, "latent": "empty"} for s in SEEDS]
    summary.append({"picture": pid, "seeds": list(SEEDS), "base": how, "base_path": str(Path(base).resolve()),
                    "first_shot": first})
assert len(jobs) <= 40, f"{len(jobs)} jobs: the batch cap is 40"
(out / f"{ROUND_NAME}.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
(out / f"{ROUND_NAME}-pictures.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(pictures), "pictures,", len(jobs), "jobs ->", out / f"{ROUND_NAME}.json")
