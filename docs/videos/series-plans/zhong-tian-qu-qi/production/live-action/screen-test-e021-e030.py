#!/usr/bin/env python3
"""screen-test-e021-e030.py OUT_DIR [--r2] : the one screen test of arc 3 (e021-e030 r2, 〈搶親〉), written 2026-11-16 before
the arc's first episode, the way arc 2's was (screen-test-e011-e020.py and its round 2). NOT run here (Colab
Qwen-Image-Edit, paid; no Colab in the writing session). The manifest is meant for
~/mokaair-work/videos/_series/zhong-tian-qu-qi/live-screen-test-e021-e030/. Check before running:
    python3 -I .agents/skills/minimax-h3-colab/scripts/check_images_manifest.py OUT_DIR/e021-e030.json
(six warnings are expected: the three portrait pictures, two seeds each, are 864x1152, the portrait canvas, not 16:9).

Round 1 (no flag): 16 pictures x seeds 37033/37034 = 32 jobs, one manifest OUT_DIR/e021-e030.json (cap 40). The full
picture inventory, with the pictures that are reused as they are and the free ffmpeg ones, is r2-bible-e021-e030.md
〈場景與真人場景圖〉; only what neither an existing picture nor a free crop/grade can give is here:
- 3 faces:   zhengbo-portrait-l1 (e025), tangwanjin-portrait-l1 (e029) drawn fresh in the live-portrait style of
             hanbo/shimujiang/weishaoqing (screen-test.py HEAD on the grey canvas, cast.json look with props and smiles
             taken out); aling-veil-portrait-l1 (e027) a ONE-change edit of aling-portrait-l1 (the grey gauze veil: the
             e017 hair lesson - the picture wins over the text, so a veil that only the text asks for will not be drawn).
- 7 one-change edits of good live pictures (refs-live/README.md 第 16、17 集: Qwen edits work when they change one
             thing of a good picture; negative words do not remove big things):
             set-kezhan-l1 (hflip of set-chalou-l1, the staircase becomes a wall with a closed door),
             set-xujia-wu-ye-l1 (set-xujia-wu-l1 relit to night by candles), set-dukou-ye-l1 (a smoke-free crop of
             set-dukou-l2, flipped so the jetty comes in from the left, relit to a foggy night),
             set-chouduan-ye-l1 (the silk shop's back lane relit to a moonlit night: Xu-ji's back yard well in e021, the
             lane behind Xu-ji in e027-e028), set-shiqiao-ye-l1 (set-shiqiao-l2 relit to a bright moonlit night),
             set-xujia-yuan-dong-l1 (set-xujia-yuan-l3 with the persimmon tree bare, e030),
             set-xuji-pu-ye-l1 (set-xuji-pu-l1 relit to early night by oil lamps, e021).
- 5 fresh places on the grey canvas (no live picture is close): set-chuan-ye-l1 (the small ferry boat, foggy night),
             set-tangfang-l1 (the sugar shed), set-xianjie-l1 (the town street with Xu-ji left and Wei-ji across),
             set-dalao-l1 (the county jail), set-guangchang-l1 (the town square of the public hearing).
- 1 prop:    prop-liuye-zhi-l1 (e029 c10: the paper against the noon sun with the willow-leaf watermark; the e917
             lesson "下次出現這個道具前先畫道具參考圖" and e914's leaf drawn four ways).
Every pick gets a NEW id with its own l1 (never a new l-number of a set id an e910-e920 episode uses: pilot.py takes the
newest l-version of a set id, and those episodes must rebuild byte for byte); episodes send them by spec.json
swap_pictures with absolute paths (the e915-e917 relative-path lesson).

Round 2 (--r2, after the round-1 picks are filed in refs-live): 2 pictures x seeds 37035/37036 = 4 jobs, OUT_DIR/r2.json:
set-chuan-chen-l1 (the picked boat relit to dawn mist with gold sunrise bands, e023 c19-c27) and set-tangfang-ye-l1 (the
picked sugar shed relit to night by one oil lamp and the stove fire, e024 c19-c23). Try a free ffmpeg grade of the picks
first; run round 2 only if the grade still reads as day (bible 拍法 8).

The positive prompts are written only as what is there (bible 拍法 18); the things to keep out are in the negative files.
The portraits keep screen-test.py's HEAD frame, which arc 2's faces were drawn with.
"""
import json
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

out = Path(sys.argv[1]); (out / "prompts").mkdir(parents=True, exist_ok=True); (out / "base").mkdir(exist_ok=True)
ROUND2 = "--r2" in sys.argv[2:]
here = Path(__file__).resolve().parent
LIVE = here.parent / "assets" / "refs-live"
full = Path(tempfile.mkdtemp(prefix="st-full-"))  # screen-test.py writes its own manifests; keep them out of OUT_DIR
argv, sys.argv = sys.argv, ["screen-test.py", str(full)]  # screen-test.py imports sys itself and writes to argv[1]
st = runpy.run_path(str(here / "screen-test.py"), run_name="screen_test_lib")
sys.argv = argv
grey_p, grey_s = out / "base" / "grey-portrait.png", out / "base" / "grey-set.png"
for dst, (name, w, h) in ((grey_p, ("grey-portrait.png", 864, 1152)), (grey_s, ("grey-set.png", 1312, 736))):
    if not dst.is_file():
        shutil.copyfile(full / st["canvas"](name, w, h), dst)
shutil.rmtree(full, ignore_errors=True)


def ffmpeg(src, vf, dst):
    assert src.is_file(), f"{src} is missing"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", vf, str(dst)], check=True)
    return dst


def swap(text, old, new, cid):
    assert old in text, f"cast.json's {cid} sentence changed ({old!r} is gone); update screen-test-e021-e030.py"
    return text.replace(old, new)


NEGATIVE_WORDS = (" no ", " not ", "without", "never", "nobody", "nothing", " gone", " none")
STYLE = ("Ancient China, Song dynasty. Style: a photorealistic live-action photograph of a real location for a Chinese "
         "historical costume drama, shot on a cinema camera with a 24mm wide-angle lens at eye height, natural light, real "
         "wood, bamboo, thatch, stone, brick, plaster, earth, cloth and water textures, deep focus, everything sharp from "
         "front to back; a clean natural film image that fills the whole frame edge to edge.")
QUIET = "the place is quiet and deserted at this hour, every surface plain and bare"
PLACE = "A wide establishing photograph of a real location: {desc}."
CANVAS = "image 1 is a plain mid-grey canvas: use it only as the size and shape of the frame and draw the whole scene below over all of it. "
KEEP_TAIL = (" A real photograph, photorealistic live-action film image of a real location, natural light, deep focus, fills "
             "the whole frame edge to edge.")
NEG = ("3D render, CGI, game render, plastic, cartoon, anime, illustration, painting, text, writing, calligraphy, Chinese "
       "characters, letters, numbers, inscription, signboard, couplet, banner, poster, watermark, logo, people, person, "
       "crowd, figure, man, woman, child, silhouette, statue, animal, weapon, spear, sword, knife, axe, weapon rack, "
       "black bars, border")
NIGHT_NEG = ", daylight, sunlight, sun, sunbeams, light shafts, blue daytime sky, bright sky, daytime"

pictures = []  # (picture id, episode/shot that first needs it, base image path, prompt, negative, width, height, how)

if not ROUND2:
    SEEDS = (37033, 37034)
    # --- two new faces, drawn fresh like hanbo/shimujiang/weishaoqing (screen-test-e011-e020.py) -----------------------
    zheng = st["appearance"]("zhengbo")
    zheng = swap(zheng, "a little plump, kind eyebrows and a gentle smile",
                 "tall and thin with a slight stoop of the shoulders, a long lean face, kind tired eyes under gentle grey brows",
                 "zhengbo")
    zheng = swap(zheng, "a neat grey-white goatee", "a neat grey-white goatee and a thin grey moustache, grey hair in a small neat "
                 "topknot under a small black cloth cap", "zhengbo")
    zheng = swap(zheng, "a dark brown silk-faced padded long robe, a small writing brush tucked at his cuff",
                 "an ancient Chinese Song-dynasty old house steward's dark brown silk-faced padded cross-collared long robe",
                 "zhengbo")
    tang = st["appearance"]("tangwanjin")
    tang = swap(tang, "a round lucky face, smiling narrowed eyes, a short neat beard",
                "a round full face with ruddy cheeks, narrow eyes, a short neat black beard along the jaw and a black moustache, "
                "black hair in a topknot held by a small plain gold crown", "tangwanjin")
    tang = swap(tang, "a dark purple silk robe woven with gold ingot patterns, a string of gold keys hanging at his waist",
                "an ancient Chinese Song-dynasty rich merchant's dark purple silk cross-collared robe woven all over with small "
                "gold ingot-shaped motifs", "tangwanjin")
    for cid, text in (("zhengbo", zheng), ("tangwanjin", tang)):
        assert not re.search(r"smil|grin|brush|keys?\b|fan\b|knife|sword", text), f"{cid}: a smile or a prop is left in the portrait"
    for pid, desc, first in (("zhengbo-portrait-l1", zheng, "e025 c32"), ("tangwanjin-portrait-l1", tang, "e029 c32")):
        body = st["BLANK"] + st["HEAD"].format(desc=re.sub(st["FEET"], "", desc)) + " " + st["STYLE"]
        pictures.append((pid, first, grey_p, body, st["NEG"], 864, 1152, "fresh portrait on the grey canvas"))

    # --- A-ling's veil: one change of her live portrait -----------------------------------------------------------------
    veil = ("Image 1 is a photograph of a young woman: keep exactly everything in it - her face above the veil and every feature "
            "of it, her long brows and her eyes looking straight at the camera, her skin, the high black knot of hair with the "
            "plain wooden pin through it and the long black hair down her back, the white cross-collared linen robe with its "
            "wide white sash, her pose, the camera position and the framing, the plain grey studio backdrop and the soft even "
            "studio light. Change only one thing: a veil of soft, finely woven pale grey gauze covers her nose, her mouth and her "
            "chin, tied behind both ears with thin pale grey cords; the gauze lies smoothly over the bridge of her nose and hangs "
            "straight down to just below her jaw, matte and opaque enough that her nose and mouth show only as soft rounded "
            "shapes under it; her eyes and brows are fully visible above it. A real photograph, photorealistic live-action film "
            "portrait, natural skin texture, sharp focus, fills the whole frame edge to edge.")
    veil_neg = ("3D render, CGI, game render, plastic, cartoon, anime, illustration, painting, text, writing, Chinese characters, "
                "watermark, logo, second person, extra people, black bars, border, see-through veil, transparent gauze, lips "
                "showing through, visible mouth, smile, teeth, metal mask, face mask with straps, surgical mask, black veil, red "
                "veil, white veil, embroidered veil, beads, jewellery, hood, hat, scarf over the hair, loose hair, hair ornament")
    pictures.append(("aling-veil-portrait-l1", "e027 c10", LIVE / "aling-portrait-l1.png", veil, veil_neg, 864, 1152,
                     "one change of aling-portrait-l1"))

    # --- one-change edits of good live pictures ---------------------------------------------------------------------------
    kezhan_base = ffmpeg(LIVE / "set-chalou-l1.png", "hflip", out / "base" / "set-chalou-l1-hflip.png")
    kezhan = ("Image 1 is a photograph of an upstairs room in a county-town building: keep exactly everything in it - the camera "
              "position, the wide open window on the left with its wooden lattice shutter and the grey tiled roofs and grey sky "
              "outside, the long wooden bench under the window, the folding screen of four plain pale panels and the small side "
              "table at the back, the square wooden table in front with its brown clay teapot and two small cups, the dark wooden "
              "walls, beams and floorboards, and the soft grey overcast light from the window. Change only one thing: on the "
              "right, in the place of the staircase and its railing, there is a plain dark wooden plank wall like the others, "
              "with one closed wooden door of two plain panels set in it, its frame flush with the wall." + KEEP_TAIL)
    pictures.append(("set-kezhan-l1", "e022 c01", kezhan_base, kezhan,
                     NEG + ", staircase, stairs, steps, railing, banister, handrail, opening in the floor, lantern", 1312, 736,
                     "one change of set-chalou-l1 hflip"))

    wu_ye = ("Image 1 is a photograph of the inside of a poor farmhouse: keep exactly everything in it - the camera position, the "
             "rough brick-and-clay walls, the window in the left wall, the roof beams and thatch, the small wooden table in the "
             "middle with its bowl, the big clay jar at the front left, the clay pots on the right and the straw on the earth "
             "floor. Change only one thing, the time and the light: it is early night; the window is a dark grey-blue square of "
             "dusk sky; the room is lit warmly by a pair of red candles and one small clay oil lamp standing on the wooden table, "
             "their small flames the only light, a soft flickering warm glow on the table, the near walls and the beams, the "
             "corners and the roof in deep shadow." + KEEP_TAIL)
    pictures.append(("set-xujia-wu-ye-l1", "e022 c13", LIVE / "set-xujia-wu-l1.png", wu_ye,
                     NEG + NIGHT_NEG + ", bright window, sunlit window, lantern, torch, fire on the floor", 1312, 736,
                     "relight of set-xujia-wu-l1"))

    # set-dukou-l2's left 860 px hold the jetty, the posts, the reeds and the water and stop before the smoke column and the
    # burning house (x >= 880); flipped, the jetty comes in from the left as e022/e023/e025 shoot it.
    dukou_base = ffmpeg(LIVE / "set-dukou-l2.png", "crop=860:484:0:252,hflip,scale=1312:736:flags=lanczos",
                        out / "base" / "set-dukou-l2-left-hflip.png")
    dukou = ("Image 1 is a photograph of a small river landing: keep exactly everything in it - the camera position, the long "
             "wooden jetty coming in from the left on its posts, the tall bare mooring posts standing in the water, the reeds "
             "along the bank, the wide still water and the far low bank and hills. Change only one thing, the time and the "
             "weather: it is deep night in thick fog; a cold blue-grey fog lies on the water and drifts over the jetty and the "
             "far bank, so the far bank and the hills are only faint dark shapes; the sky is black-grey; the water is dark and "
             "still with a faint grey sheen; the cold grey glow of the fog is the only light, everything in cold blue-grey "
             "tones." + KEEP_TAIL)
    pictures.append(("set-dukou-ye-l1", "e022 c39", dukou_base, dukou,
                     NEG + NIGHT_NEG + ", sunset, sunrise, pink sky, red sky, orange glow, smoke, fire, flames, boat, raft, "
                                       "lantern, torch, moon", 1312, 736, "relight of set-dukou-l2 crop+hflip"))

    lane = ("Image 1 is a photograph of a back lane in a county town: keep exactly everything in it - the camera position, the "
            "grey brick walls and tiled eaves on both sides, the faded red wooden doors on the left, the bamboo drying pole with "
            "its four hanging cloths, the wooden tubs, the stone-paved lane running away into the distance, the round brick "
            "well with its wooden frame and the small thatched well roof on the right, and the plain blank board on the wall "
            "at the top left. Change only one thing, the time and the light: it is a clear night under a bright moon; cold "
            "blue moonlight lies on the stone slabs, the walls and the roof tiles, the eaves throw deep black shadows, the sky "
            "above is deep blue-black with a few stars; the small paper lantern hanging at the far end of the lane glows warm "
            "yellow, the only warm light, a little pool of yellow on the slabs under it." + KEEP_TAIL)
    pictures.append(("set-chouduan-ye-l1", "e021 c29", LIVE / "set-chouduan-l1.png", lane,
                     NEG + NIGHT_NEG + ", torch, fire, red lantern, many lanterns, string lights, neon", 1312, 736,
                     "relight of set-chouduan-l1"))

    bridge = ("Image 1 is a photograph of an old stone arch bridge in a town: keep exactly everything in it - the camera position, "
              "the single stone arch and its parapet, the stream under it and its reflection, the stone-lined bank and the dirt "
              "path on the left, the big river stones along the water, the bamboo on both sides and the tiled houses beyond. "
              "Change only one thing, the time and the light: it is a clear night under a bright, almost full moon high in the "
              "sky; cold blue-white moonlight on the arch, the parapet and the water, the moon's reflection breaking on the "
              "ripples, a thin low mist on the water lit silver, the houses dark with their doors and windows shut, deep black "
              "shadow under the arch on the left bank; the moonlight is the only light." + KEEP_TAIL)
    pictures.append(("set-shiqiao-ye-l1", "e027 c27", LIVE / "set-shiqiao-l2.png", bridge,
                     NEG + NIGHT_NEG + ", sunrise glow, golden light, lantern, torch, lit windows, fire", 1312, 736,
                     "relight of set-shiqiao-l2"))

    yard = ("Image 1 is a photograph of a farmhouse yard: keep exactly everything in it - the camera position, the thatched "
            "farmhouse on the left with its dark doorway, its lattice window and the stack of split firewood, the wooden yard gate "
            "under its small tiled roof, the trunk and the branches of the tree in the middle, the wooden bucket, the board "
            "leaning on the wall, the round stone well with its wooden windlass at the front right, the low mud wall along the "
            "right, the earth of the yard and the low warm sunlight from the right. Change only one thing: the tree is bare for "
            "early winter; its grey branches are empty, only two or three dry brown leaves still hang on them, and the bare "
            "twigs stand out clearly against the pale sky." + KEEP_TAIL)
    pictures.append(("set-xujia-yuan-dong-l1", "e030 c01", LIVE / "set-xujia-yuan-l3.png", yard,
                     NEG + ", persimmons, orange fruit, fruit on the tree, green leaves, red leaves, autumn foliage, blossoms, "
                           "beads, ornaments, lanterns", 1312, 736, "one change of set-xujia-yuan-l3"))

    shop = ("Image 1 is a photograph of the inside of an empty shop: keep exactly everything in it - the camera position, the "
            "empty wooden shelves and the low cabinet along the left wall, the street doorway with its three tall narrow "
            "openings in the middle of the back wall and the lattice panels beside it, the plain pale board walls on the right, "
            "the dark beams and the grey floor tiles. Change only one thing, the time and the light: it is early night; the "
            "three doorway openings show a deep blue night street with one red paper lantern glowing under the eaves across "
            "the street; the room is lit by the soft warm glow of two small oil lamps standing on a counter just outside the "
            "frame on the right, an even dim warm light across the floor and the shelves, the upper shelves and the corners in "
            "deep shadow." + KEEP_TAIL)
    pictures.append(("set-xuji-pu-ye-l1", "e021 c20", LIVE / "set-xuji-pu-l1.png", shop,
                     NEG + NIGHT_NEG + ", bars of sunlight on the floor, bright doorway, white daylight, torch", 1312, 736,
                     "relight of set-xuji-pu-l1"))

    # --- fresh places on the grey canvas -------------------------------------------------------------------------------
    FRESH = [
        ("set-chuan-ye-l1", "e022 c41",
         "a small old wooden river ferry boat on a quiet river at deep night in thick fog, seen from the side and a little above "
         "from the water: the stern at the left and the bow at the right, a worn plank deck and low gunwales, an arched canopy "
         "of woven split bamboo over the middle of the boat, open at both ends, a folded grey blanket on the deck inside it; one "
         "long bamboo punting pole lying along the near gunwale; at the very bow on the right one small round paper lantern on "
         "a short bamboo pole, glowing warm; around the boat black still water and dense cold blue-grey fog, the dim shapes of "
         "reeds and willows on the far bank; the little lantern is the only light, warm on the bow and the front of the canopy, "
         "everything else cold blue-grey; " + QUIET,
         NIGHT_NEG + ", sunset, moon, stars, second boat, raft, sail, motor, modern boat, rowing boat with oars, torch"),
        ("set-tangfang-l1", "e024 c19",
         "a long open-sided thatched shed beside a small stream outside a poor ancient Chinese Song-dynasty village, used as a "
         "sugar workshop, on a clear early-winter morning: a thatched roof on rough timber posts, the back closed by a plain "
         "earthen wall; on the left a long mud-brick stove with two round fire mouths and two big black iron woks set into its "
         "top; against the back wall on the left a plain wooden rack holding a row of ten brown clay funnels, points down, each "
         "standing in a squat clay jar; in the middle a big round stone hand mill on a low stone base with a wooden bucket "
         "under its spout; at the right back a long low wooden table with a stack of round flat bamboo trays on it; the wide "
         "open side on the right looking out onto a dirt path, the small stream and bare willow trees; bright low morning "
         "sunlight slanting in from the right across the earth floor; a thin white frost on the ground outside; " + QUIET,
         ", glass, metal machine, brick factory, chimney stack, modern kitchen, pots of food, lantern, torch"),
        ("set-xianjie-l1", "e024 c01",
         "a stone-paved street of an ancient Chinese Song-dynasty county town on a clear early-winter morning, seen along the "
         "street at eye height: on the left the open front of a small one-storey shop, all its wooden door panels taken down and "
         "stacked against the wall beside the doorway, a long plain wooden counter just inside; across the street on the right a "
         "bigger two-storey wooden shop with its ground floor standing open, a length of new red silk draped along its lintel, "
         "one wooden lattice window on its upper floor; the lintel boards above both shop fronts are plain bare wood; between "
         "them the grey stone slabs of the street white with frost, running away into the distance between more low "
         "grey-tiled shops with plain bare lintels and closed wooden shutters; bright low morning sunlight from the right casting "
         "long shadows across the street; " + QUIET,
         ", stalls, vegetables, fruit, awnings, flags, shop signs, hanging plaques, lanterns with writing, electric wires, "
         "air conditioner, cars"),
        ("set-dalao-l1", "e028 c26",
         "the entrance of an old ancient Chinese Song-dynasty county jail at night, seen from outside at eye height: a heavy gate "
         "of thick square wooden bars fills the middle of the picture, closed, with an iron hasp and a big iron padlock on it; on "
         "the left a plain square grey stone pillar beside the gate; through the bars a narrow stone-paved corridor runs straight "
         "away from the camera, on both sides of it small cells closed by thick wooden bars with straw on their floors; two "
         "burning torches fixed in iron brackets on the corridor wall throw warm orange light on the bars and the damp grey stone "
         "walls; in front of the gate the stone floor lies in cold blue night shadow; the two torches are the only light; " + QUIET,
         NIGHT_NEG + ", prisoners, skeleton, chains on the wall, blood, modern prison, steel bars, cage of metal, lantern"),
        ("set-guangchang-l1", "e028 c33",
         "the town square of an ancient Chinese Song-dynasty county town at noon on a clear early-winter day: a wide open square "
         "of packed earth edged with grey stone slabs; in the middle a square wooden platform about waist high with three wooden "
         "steps at its front left, its top covered with a plain red cloth; at the back of the platform a long dark wooden "
         "judgement desk with one flat rectangular wooden block and a shallow wooden tray on it and a plain chair behind it; on "
         "the right side of the platform one carved wooden armchair; at the left foot of the platform one plain wooden crate "
         "with two crossed strips of plain white paper pasted over its lid; around the square low grey-tiled shops and "
         "whitewashed walls with plain bare lintels and a few bare trees; at the right edge a wide dirt road leading into the "
         "square; strong overhead noon sunlight, short shadows, a deep blue sky; " + QUIET,
         ", mallet, gavel, hammer, stage curtains, flags, banners, stalls, gallows, cage, lanterns"),
    ]
    for pid, first, desc, extra in FRESH:
        pictures.append((pid, first, grey_s, CANVAS + PLACE.format(desc=desc) + " " + STYLE, NEG + extra, 1312, 736,
                         "fresh place on the grey canvas"))

    # --- the prop ----------------------------------------------------------------------------------------------------
    paper = (CANVAS + "A close-up photograph of a real prop on a film set of a Chinese historical costume drama: one sheet of "
             "thin off-white handmade paper fills the whole frame edge to edge, held up flat against a bright clear noon sky so "
             "the sunlight shines evenly through it from behind; the long pale fibres of the paper show as a soft cloudy "
             "texture; in the very middle of the sheet a faint willow-leaf shape the size of a palm, a little brighter than the "
             "paper around it, long and slender with pointed ends, a thin central vein and fine side veins, like a watermark seen "
             "against the light; the rest of the sheet is plain even paper. Style: a photorealistic live-action macro photograph, "
             "real paper fibres, soft even light, sharp focus on the paper; a clean natural film image.")
    pictures.append(("prop-liuye-zhi-l1", "e029 c10", grey_s, paper,
                     "3D render, CGI, cartoon, anime, illustration, painting, text, writing, calligraphy, Chinese characters, "
                     "letters, numbers, stamp, seal, red ink, printed pattern, glitter, sparkles, gold flecks, lens flare, sun "
                     "disc, hand, fingers, thumb, people, border, frame, black bars, green leaf, real leaf, tree, branches, "
                     "several leaves, dark leaf, stain, burn mark, hole", 1312, 736, "fresh prop on the grey canvas"))
    name = "e021-e030"
else:
    SEEDS = (37035, 37036)
    boat = LIVE / "set-chuan-ye-l1.png"
    shed = LIVE / "set-tangfang-l1.png"
    for p in (boat, shed):
        assert p.is_file(), f"refs-live/{p.name} is missing: round 2 relights the round-1 picks"
    dawn = ("Image 1 is a photograph of a small river ferry boat: keep exactly everything in it - the camera position, the boat, "
            "its plank deck, its woven bamboo canopy, the punting pole, the little lantern pole at the bow, the water and the "
            "banks. Change only one thing, the time and the light: it is sunrise after a foggy night; the fog has thinned to a "
            "soft pale mist, the sky pale gold and grey-blue, and the low sun from the right sends long bands of warm golden "
            "light through the mist across the water and the boat; the little lantern is out." + KEEP_TAIL)
    night = ("Image 1 is a photograph of a thatched sugar workshop: keep exactly everything in it - the camera position, the "
             "thatched roof and posts, the back wall, the mud-brick stove with its two iron woks, the rack of clay funnels, the "
             "stone mill and the bucket, the low table with its bamboo trays and the open right side. Change only one thing, the "
             "time and the light: it is night; through the open right side the path and the stream are dark under a black sky; "
             "inside, a red glow of fire burns in the stove mouths and one small clay oil lamp stands on the low table, their "
             "warm orange light the only light, white steam rising from the left wok, deep shadows under the roof." + KEEP_TAIL)
    pictures += [("set-chuan-chen-l1", "e023 c19", boat, dawn, NEG + ", night, black sky, moon, lantern flame, second boat",
                  1312, 736, "relight of the round-1 boat"),
                 ("set-tangfang-ye-l1", "e024 c19", shed, night, NEG + NIGHT_NEG + ", lantern, torch, candles, frost in sunlight",
                  1312, 736, "relight of the round-1 sugar shed")]
    name = "r2"

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
    summary.append({"picture": pid, "seeds": list(SEEDS), "base": how, "first_shot": first})
assert len(jobs) <= 40, f"{len(jobs)} jobs: the batch cap is 40"
(out / f"{name}.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
(out / f"{name}-pictures.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / f"{name}.json")
