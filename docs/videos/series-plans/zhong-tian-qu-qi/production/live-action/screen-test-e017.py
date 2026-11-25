#!/usr/bin/env python3
"""screen-test-e017.py OUT_DIR : the three e017 pictures of the paper workshop after the fire (writer-tools/e017-r2/r2.py,
2026-11-15). NOT run here (no Colab in the writing session). Seeds 37019/37020 (e016 used 37013-37016), 6 jobs, one manifest
OUT_DIR/e017.json; prompts in OUT_DIR/prompts/. The manifest is meant for
~/mokaair-work/videos/_series/zhong-tian-qu-qi/live-screen-test-e017/. Check before running:
    python3 -I .agents/skills/minimax-h3-colab/scripts/check_images_manifest.py OUT_DIR/e017.json

Why: the e011-e020 screen test's set-zhifang-shao-l1 (37002) and set-zhifang-gujia-ye-l1 (37001), looked at full size, are
unusable for e017: shao-l1 is a CG render of an INTACT thatched house with lattice windows and a brick-paved yard, the charred
poles and three tubs only lying in front of it (the wrong state: the script's workshop burned to the ground and its roof fell
in); gujia-ye-l1 is a pure 3D render (a tiled mound, a stone-paved square between tiled halls, a pine frame on a pavement) that
matches neither the live shed nor any other live picture. The lesson (e015 s25, e016 review 必改 17): a set picture in the
wrong state wins over the text, so the wrong-state picture is not sent; e017 needs these three:
- set-zhifang-shao-l2 (e017 s17-s26, the morning after the fire): an edit of set-gongpeng-l3 (the live day shed of e016, same
  camera: the stone back and left walls, the open right side), burnt: the roof gone and open sky above, the timber posts
  charred stumps and one fallen charred beam, the floor deep in grey ash, the big tub charred black, the table a charred heap,
  the walls blackened with soot, a few thin wisps of white smoke, and beyond the open right side a low bamboo fence with one
  section pushed over flat (the script's footprints lead out to it). Morning sun from the right.
- set-zhifang-gujia-ye-l2 (e017 s27-s35, that night): an edit of set-gongpeng-ye-l2 (the live shed by night, same camera):
  the burnt roof and posts cleared away, the ash raked into a low grey heap along the left wall, and in the middle a new
  frame of four upright posts of freshly peeled pale pine and two crossbeams on top, open to the starry sky; a bonfire of split
  logs on a ring of stones at the front left where the tub stood; two plain pale paper lanterns hanging from the crossbeams.
- set-zhifang-gujia-chen-l1 (e017 s36-s40, dawn of the twelfth day): an edit of set-gongpeng-l3 with the same frame at first
  light: the bonfire burnt down to grey embers with one thin thread of smoke, pale gold dawn light low from the right, the sky
  pale. A dawn shot sent the night picture would come out as night (bible 拍法 8, the other way round).
gen-dh.mjs maps "burnt paper workshop", "new timber frame" and "new timber frame at dawn" to these ids (shared edit, e910-e916
rebuild byte for byte); pilot.py takes the newest l-version, so the l2 picks replace the l1 renders for every later episode (e018's night
shots at the half-roofed frame start from gujia-ye-l2: bible 第 18 集). prep917.sh stops until all three
are in refs-live (e016's set-dukou-l2, which s01 sends, is already there).
The positive prompts are written only as what is there (bible 拍法 18); the things to keep out are in the negative files.

Round 2 (writer-tools/e017-r2/review.md 必改 1, 2026-11-15, after the coordinator's pick of round 1: gujia-ye-l2 = 37020,
gujia-chen-l1 = 37019, shao-l2 not taken): `screen-test-e017.py OUT_DIR --r2` writes OUT_DIR/r2.json with ONE picture,
set-xujia-yuan-huo-l1, seeds 37023/37024: the yard set-xujia-yuan-l3 with ONE change (the e016 ferry lesson, README 第 16 集:
a one-change edit works, negative words do not remove big objects): beyond the low mud wall on the right, the thatched roof of
the work shed burning with tall flames under one rolling plume of dark smoke, its firelight on the top of the wall. Everything
else is kept as it is, the board and the stick leaning on the right wall included (review 建議: look at the stick when picking;
if it has grown into a weapon, a second removal edit takes it out). The yard shots s02-s10, s13-s15 send it in place of l3
(spec.json swap_pictures, prep917.sh); a new set id with its own l1, so pilot.py's newest-l-version of set-xujia-yuan stays l3.
Check: python3 -I .agents/skills/minimax-h3-colab/scripts/check_images_manifest.py OUT_DIR/r2.json
"""
import json
import sys
from pathlib import Path

out = Path(sys.argv[1]); (out / "prompts").mkdir(parents=True, exist_ok=True)
LIVE = Path(__file__).resolve().parent.parent / "assets" / "refs-live"
SEEDS = (37019, 37020)

STYLE = ("Ancient China, Song dynasty. Style: a photorealistic live-action photograph of a real location for a Chinese historical "
         "costume drama, shot on a cinema camera at eye height, natural light, real wood, bamboo, rope, stone, ash, charcoal and "
         "earth textures, deep focus, everything sharp from front to back; a clean natural film image that fills the whole frame "
         "edge to edge.")
QUIET = "the place is quiet and deserted at this hour, every surface plain"
PLACE = "A wide establishing photograph of a real location: {desc}."
KEEP = ("image 1 is a photograph of the place: keep exactly its camera position, the low stone back wall and left wall with the "
        "tiled roofs and trees beyond them, the open right side and the squat stone mortar in the middle; change everything "
        "else into what is described here. ")

PICTURES = [
    ("set-zhifang-shao-l2", "set-gongpeng-l3", "e017 s17",
     KEEP,
     "the same papermaking work shed of a poor ancient Chinese Song-dynasty farmhouse on the morning after it burned down, a real "
     "photograph: (1) the roof has burned away and the open pale morning sky is above, only the charred black stumps of the "
     "timber posts standing, one long charred beam lying across the floor from the left; (2) the whole floor is deep in soft "
     "grey ash with black charcoal pieces of split bamboo lying in it; (3) at the front left the big round wooden tub is "
     "charred black, its staves cracked; at the right a low heap of charred black planks where the table stood; (4) the stone "
     "walls are blackened with soot up to their tops; (5) a few thin wisps of white smoke rise straight up from the ash; "
     "(6) beyond the open right side a low fence of plain bamboo stakes, one section of it pushed over flat on the ground; "
     "(7) bright clear morning sunlight from the right, crisp shadows; " + QUIET),
    ("set-zhifang-gujia-ye-l2", "set-gongpeng-ye-l2", "e017 s27",
     KEEP,
     "the same place late at night, a real night photograph: (1) the burnt roof and posts are cleared away and the black night "
     "sky full of small cold stars is open above; (2) the grey ash is raked into one long low heap along the foot of the left "
     "wall, the floor bare swept earth; (3) in the middle stands a new frame of freshly peeled pale yellow pine: four thick "
     "round posts standing upright in a square and two round crossbeams laid across their tops, open to the sky; (4) at the "
     "front left a bonfire of split logs burns on a ring of stones, its warm orange light on the new posts and the walls; "
     "(5) two plain round pale paper lanterns hang from the near crossbeam, each with a small candle burning inside; "
     "(6) deep dark night, only the bonfire and the two lanterns give light; " + QUIET),
    ("set-zhifang-gujia-chen-l1", "set-gongpeng-l3", "e017 s36",
     KEEP,
     "the same place at first light of dawn, a real photograph: (1) the burnt roof and posts are cleared away and the pale dawn "
     "sky is open above, a soft gold glow low on the right; (2) the grey ash is raked into one long low heap along the foot of "
     "the left wall, the floor bare swept earth; (3) in the middle stands a new frame of freshly peeled pale yellow pine: four "
     "thick round posts standing upright in a square and two round crossbeams laid across their tops, open to the sky, one "
     "plain wooden ladder leaning against the right-hand post; (4) at the front left a ring of stones holding a bed of grey "
     "embers, one thin thread of smoke rising from it; (5) cool pale dawn light with low gold light from the right on the new "
     "pine; " + QUIET),
]
NEG = ("3D render, CGI, game render, plastic, cartoon, anime, illustration, painting, text, writing, calligraphy, Chinese "
       "characters, letters, inscription, signboard, couplet, banner, poster, watermark, logo, people, person, crowd, figure, "
       "man, woman, child, silhouette, statue, animal, weapon, spear, sword, knife, axe, black bars, border")
NEG_BY = {
    "set-zhifang-shao-l2": NEG + ", roof, thatch, intact building, walls of a house, windows, lattice, paving, brick floor, "
                                 "tiles on the floor, flames, fire, glowing embers, rack, A-frame, poles leaning",
    "set-zhifang-gujia-ye-l2": NEG + ", roof, thatch, tiles on the frame, tiled mound, paving, stone-paved square, daylight, "
                                     "moon, full moon, torch, brazier, metal lamp, ladder, rack",
    "set-zhifang-gujia-chen-l1": NEG + ", roof, thatch, tiles on the frame, flames, fire, night, moon, lanterns, torch, "
                                       "paving, rack",
}
ROUND2 = "--r2" in sys.argv[2:]
if ROUND2:
    SEEDS = (37023, 37024)
    ONE = ("Image 1 is a photograph of the place: keep exactly everything in it - the camera position, the low thatched farmhouse "
           "with its dark doorway, lattice window and stack of split firewood on the left, the plain wooden yard gate under its "
           "small tiled roof, the persimmon tree with its orange fruit, the wooden bucket, the wooden board leaning on the wall, "
           "the round stone well with its wooden windlass at the front right, the low mud wall running along the right, the "
           "stones and the earth of the yard, and the low warm sunrise light. Change only one thing: beyond the low mud wall on "
           "the right, just behind the wall where the field was, the thatched roof of a small work shed rises above the wall top "
           "and is burning: tall orange flames along its thatch and one thick rolling plume of dark grey smoke rising from it "
           "and drifting up to the right across the sky, the orange firelight glowing on the top of the mud wall. A real "
           "photograph, photorealistic live-action film image of a real location, natural light, deep focus, fills the whole "
           "frame edge to edge.")
    PICTURES = [("set-xujia-yuan-huo-l1", "set-xujia-yuan-l3", "e017 s02", ONE, None)]
    NEG_BY["set-xujia-yuan-huo-l1"] = ("3D render, CGI, game render, plastic, cartoon, anime, illustration, painting, text, writing, "
                                       "Chinese characters, watermark, logo, people, person, figure, silhouette, animal, weapon, "
                                       "spear, black bars, border, flames in the yard, fire on the farmhouse, fire on the tree, "
                                       "fire on the gate, burning ground")
jobs, summary = [], []
for pid, base, first, rule, desc in PICTURES:
    src = LIVE / f"{base}.png"
    assert src.is_file(), f"refs-live/{base}.png is missing; {pid} is an edit of it"
    assert not (LIVE / f"{pid}.png").exists(), f"refs-live/{pid}.png already exists; pick a new l-number"
    body = rule if desc is None else rule + PLACE.format(desc=desc) + " " + STYLE
    for bad in (" no ", " not ", "without", "never", "nobody", "nothing", " gone"):
        assert bad not in body.lower(), f"{pid}: the positive prompt has '{bad.strip()}' (write what is there)"
    prompt = out / "prompts" / f"{pid}.txt"
    prompt.write_text(body, encoding="utf-8")
    neg = out / "prompts" / f"negative-{pid}.txt"
    neg.write_text(NEG_BY[pid], encoding="utf-8")
    jobs += [{"id": f"{pid}-{s}", "reference_images": [str(src)], "prompt_file": str(prompt), "negative_file": str(neg),
              "width": 1312, "height": 736, "seed": s, "latent": "empty"} for s in SEEDS]
    summary.append({"picture": pid, "seeds": list(SEEDS), "base": "edit of " + base, "first_shot": first})
name = "r2" if ROUND2 else "e017"
(out / f"{name}.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
(out / f"{name}-pictures.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(jobs), "jobs ->", out / f"{name}.json")
