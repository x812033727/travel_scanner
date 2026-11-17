#!/usr/bin/env python3
"""screen-test-e031-e040.py OUT_DIR [--with-chen] [--horse-star] | OUT_DIR --sheet : the round-1 screen test of arc 4
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
hantian-yang, hantian-shou, shanjiao-qu-ye, then gucang-wai on the picked hantian-yang) stay as specs in the bible until the
round-1 picks are filed; they are not in this script yet.
The positive prompts are written only as what is there (bible 拍法 18); the things to keep out are in the negative files.

--sheet: after the run, writes contact sheets OUT_DIR/sheets/r1-NN.jpg from OUT_DIR/out/<id>-<seed>.png and
OUT_DIR/e031-e040-pictures.json: one row per picture, the base picture (for an edit) and the two seeds side by side at
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
assert FLAGS <= {"--with-chen", "--horse-star", "--sheet"}, f"unknown flag(s): {FLAGS}"
here = Path(__file__).resolve().parent
LIVE = here.parent / "assets" / "refs-live"
NAME = "e031-e040"
SEEDS = (37037, 37038)


def sheet():
    from PIL import Image, ImageDraw, ImageFont
    pics = json.loads((out / f"{NAME}-pictures.json").read_text(encoding="utf-8"))
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
        cells += [tile(out / "out" / f"{p['picture']}-{s}.png", f"{p['picture']} {s}") for s in p["seeds"]]
        rows.append(cells)
    per = 4
    for n in range(0, len(rows), per):
        chunk = rows[n:n + per]
        sh = Image.new("RGB", (3 * tw + 4 * gap, len(chunk) * (th + gap) + gap), (60, 60, 60))
        for r, cells in enumerate(chunk):
            for c, t in enumerate(cells):
                sh.paste(t, (gap + c * (tw + gap), gap + r * (th + gap)))
        dst = out / "sheets" / f"r1-{n // per + 1:02d}.jpg"
        sh.save(dst, quality=88)
        print("sheet ->", dst)


if "--sheet" in FLAGS:
    sheet()
    sys.exit(0)

(out / "prompts").mkdir(parents=True, exist_ok=True)
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

jobs, summary = [], []
for pid, first, base, body, neg, w, h, how in pictures:
    assert Path(base).is_file(), f"{base} is missing"
    folder = LIVE / "angles" if "angle" in pid else LIVE
    assert not (folder / f"{pid}.png").exists(), f"refs-live/{pid}.png already exists; pick a new id"
    if "portrait" not in how:  # the portraits keep screen-test.py's HEAD frame (arc 2's faces were drawn with it)
        for bad in NEGATIVE_WORDS:
            assert bad not in body.lower(), f"{pid}: the positive prompt has '{bad.strip()}' (write what is there)"
    prompt = out / "prompts" / f"{pid}.txt"
    prompt.write_text(body, encoding="utf-8")
    negf = out / "prompts" / f"negative-{pid}.txt"
    negf.write_text(neg, encoding="utf-8")
    jobs += [{"id": f"{pid}-{s}", "reference_images": [str(Path(base).resolve())], "prompt_file": str(prompt.resolve()),
              "negative_file": str(negf.resolve()), "width": w, "height": h, "seed": s, "latent": "empty"} for s in SEEDS]
    summary.append({"picture": pid, "seeds": list(SEEDS), "base": how, "base_path": str(Path(base).resolve()),
                    "first_shot": first})
assert len(jobs) <= 40, f"{len(jobs)} jobs: the batch cap is 40"
(out / f"{NAME}.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
(out / f"{NAME}-pictures.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(pictures), "pictures,", len(jobs), "jobs ->", out / f"{NAME}.json")
