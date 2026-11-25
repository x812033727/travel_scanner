#!/usr/bin/env python3
"""screen-test-e011-e020.py OUT_DIR : the one screen test of arc 2 (e011-e020 r2, 〈肥皂與白紙〉): the 22 live-action
references r2-bible-e011-e020.md lists as new (4 portraits, 18 places; day and night counted apart). NOT run; waits for
the owner's go-ahead to spend, two seeds each (37001/37002) like e007-e010. e011 and e012 need no new picture.

The batch cap of check_images_manifest.py is 40 jobs, so the 44 jobs go out as two manifests in episode order:
  OUT_DIR/e011-e020-a.json : what e013-e015 first need (9 pictures, 18 jobs);
  OUT_DIR/e011-e020-b.json : what e016-e020 first need (13 pictures, 26 jobs).
Each job id is <picture>-<seed>; the picture id is the refs-live name without -l1.

Lessons written in (e007-e010 picks and the bible's 〈真人版的拍法〉):
- portraits: head and shoulders, calm, mouth closed, not smiling, no props (Wei Shaoqing's cast.json scornful smile and
  fan, Elder Han's staff and the carpenter's wood shavings are taken out; the shots write them), Song-dynasty
  cross-collared costume words like screen-test.py's LIVE_LOOK;
- every place prompt says the place is empty of people (e009's first two rounds of Tang Xiaotang's room drew a woman);
- nothing written anywhere: every signboard, plaque, grave marker and lantern is written as blank (e007 37001 and
  e008 grew fake characters on signboards);
- night is night: each night set names its light (stars, moon, lantern, candle, bonfire) and says there is no daylight,
  and takes a negative that names daylight (e010's yard at night came out a sunny day with a yellow field);
- the side each door, window, opening and road is on is the one the e013-e020 scripts' 場頭 shoot it from.
set-gongpeng-ye is the same shed as set-gongpeng with the night light (bible: 用 set-gongpeng-l1 改光). The day shed is
picked in this same round, so until refs-live/set-gongpeng-l1.png exists the night shed is drawn from the text on the
grey canvas; once the owner has picked the day shed, run this again and the night shed becomes an edit of it (the e010
yard-at-night route) for a second round of that one picture.
Same templates, style, negative prompt, grey canvas and seeds as screen-test.py.
"""
import json
import re
import runpy
import sys
from pathlib import Path

out = Path(sys.argv[1]); (out / "prompts").mkdir(parents=True, exist_ok=True); (out / "base").mkdir(exist_ok=True)
here = Path(__file__).resolve().parent
LIVE = here.parent / "assets" / "refs-live"
st = runpy.run_path(str(here / "screen-test.py"), run_name="screen_test_lib",
                    init_globals={"sys": type("S", (), {"argv": ["x", str(out / "_full")]})})


def swap(text, old, new, cid):
    assert old in text, f"cast.json's {cid} sentence changed ({old!r} is gone); update screen-test-e011-e020.py"
    return text.replace(old, new)


# --- the four new faces -------------------------------------------------------------------------------------------
shi = st["appearance"]("shimujiang")
shi = swap(shi, "a pencil-like wooden stick", "one thin plain wooden stick pushed through it", "shimujiang")
shi = swap(shi, "a faded brown short work jacket with sleeves rolled up, a leather apron covered in wood shavings, calloused hands",
           "an ancient Chinese Song-dynasty craftsman's faded brown hemp cross-collared short work jacket with the sleeves rolled up, "
           "a plain worn leather apron over it, clean, nothing on his skin", "shimujiang")

han = st["appearance"]("hanbo")
han = swap(han, "a faded washed-out grey cotton long robe, leaning on a polished old bamboo walking staff",
           "an ancient Chinese Song-dynasty village elder's faded, washed-out grey cotton cross-collared long robe", "hanbo")

wei = st["appearance"]("weishaoqing")
wei = swap(wei, "handsome but frivolous, peach-blossom eyes, thin lips always curled in a scornful smile",
           "handsome, peach-blossom eyes, thin lips", "weishaoqing")
wei = swap(wei, "a sapphire-blue brocade robe woven with gold thread, a fine white jade pendant at his waist, a gold-flecked folding fan in his hand",
           "an ancient Chinese Song-dynasty noble young master's sapphire-blue brocade cross-collared robe woven with gold thread",
           "weishaoqing")
# not in cast.json; the bible's 新人物 row: small and thin, eyebrows sloping down like the character 八, a grey silk robe.
# Kept apart from Sun the shopkeeper (long face, grey beard, green satin) and Magistrate Hu (plump, official hat).
hanghui = ("East Asian man of fifty, small and thin with narrow sloping shoulders, a narrow sallow face, sparse eyebrows that slope "
           "steeply down at their outer ends, small careful eyes, a short sparse black moustache and no beard, hair in a small neat "
           "topknot under a small black cloth cap, an ancient Chinese Song-dynasty merchant's plain grey silk cross-collared robe")
for cid, text in (("shimujiang", shi), ("hanbo", han), ("weishaoqing", wei), ("hanghui", hanghui)):
    assert not re.search(r"smil|grin|fan\b|staff|shaving|knife|sword", text), f"{cid}: a smile or a prop is left in the portrait"

PORTRAITS = [  # (picture id, description, episode that first needs it)
    ("shimujiang-portrait", shi, 13),
    ("hanbo-portrait", han, 15),
    ("weishaoqing-portrait", wei, 20),
    ("hanghui-huizhang-portrait", hanghui, 20),
]

# --- the eighteen places ------------------------------------------------------------------------------------------
SONG = "a poor ancient Chinese Song-dynasty"
EMPTY = "the place is completely empty: no person, no figure, no face and no animal anywhere in the picture"
BLANK_TEXT = "nothing written, carved or painted anywhere: no characters, no letters, no signs"
NIGHT = "it is truly night: no daylight, no sunlight and no blue daytime sky anywhere"
SETS = [  # (picture id, description, episode that first needs it, night?)
    ("set-mujiang-fang",
     f"the far end of a narrow packed-earth lane in {SONG} village in the late morning: on the right a village carpenter's workshop "
     "of timber and packed earth under a thatched roof, its plain wooden door standing open and a closed wooden window shutter "
     "above and to the right of the door, a heap of pale wood shavings on the ground at the doorway; through the open door the "
     "workshop inside: an old heavy workbench with one long planed plank on it, saws, wood planes and an ink-line reel hanging "
     "on the back wall, a bundle of long bamboo poles leaning in a corner; the lane running away to the left between low earthen "
     f"walls; clear slanting late-morning sunlight coming from the left; no signboard over the door; {BLANK_TEXT}", 13, False),
    ("set-zhulin-fen",
     "a small clearing deep in a dense bamboo grove behind an ancient Chinese Song-dynasty village at deep night: tall dense "
     "bamboo on every side, a narrow dirt path coming in from the left, a little to the right of the middle a small low earthen "
     "grave mound with one plain blank wooden marker board standing in front of it, bare weathered wood; no moon, a black sky "
     "with stars glimpsed between the bamboo leaves, faint cold blue starlight the only light, the bamboo trunks picked out in "
     f"cold blue and the shadows deep; no fire, no lantern, no candle, no paper offerings; {NIGHT}; {BLANK_TEXT}", 13, True),
    ("set-gongpeng",
     f"a simple open-sided work shed beside {SONG} farmhouse, used as a papermaking workshop, in the early morning: a thatched "
     "roof on rough timber posts, open on three sides, the wide open side on the right facing a packed-earth yard; on the left "
     "two big wooden soaking tubs with split bamboo soaking in water, in the middle a big round wooden tub full of milky white "
     "paper pulp and a stone mortar, on the right an old bare wooden table; at the back of the shed a smooth plastered earthen "
     "drying wall; low warm early-morning sunlight slanting in through the open right side, a sheen of white light on the pulp; "
     f"{BLANK_TEXT} on any post, wall or tub", 14, False),
    ("set-gongpeng-ye",
     f"the same open-sided papermaking work shed beside {SONG} farmhouse late at night just before dawn: a thatched roof on rough "
     "timber posts, open on three sides with the wide open side on the right; two big wooden soaking tubs on the left, a big "
     "round wooden tub of milky white paper pulp and a stone mortar in the middle, an old wooden table on the right with one "
     "short candle almost burnt down standing on it, its small flame the only light inside, warm and dim, deep shadows at the "
     "back by the plastered earthen drying wall; beyond the open right side the sky a deep blue-grey just before dawn with no "
     f"sun; {NIGHT}; {BLANK_TEXT}", 15, True),
    ("set-dagu-chang",
     "a large village threshing ground in ancient Chinese Song-dynasty countryside at dawn in late autumn: a wide flat floor of "
     "tamped yellow earth, stacks of rice straw piled round its edge, beyond it harvested rice-stubble fields not yet ploughed "
     "and a few bare trees; thin morning mist lying low over the ground, low cold golden sunlight coming from the right, long "
     f"shadows; {BLANK_TEXT}", 15, False),
    ("set-qiutian",
     "a harvested autumn rice-stubble field in ancient Chinese Song-dynasty countryside in the afternoon: dry, drained dark soil "
     "with short rows of cut rice stubble, not flooded, no water, no green shoots; the field fills the left and the middle of "
     "the picture, and on the right a raised earthen field ridge a little higher than the field runs from front to back, a "
     "willow tree on the ridge with yellowing autumn leaves; low hills and a few thatched village roofs far off; clear late "
     f"autumn afternoon light from the left; not spring, not a paddy, no plough, no tools; {BLANK_TEXT}", 15, False),
    ("set-shiqiao",
     "an old single-arch stone bridge over a shallow slow stream outside an ancient Chinese Song-dynasty village in the early "
     "morning: a packed-earth road comes in from the left to the head of the bridge in the middle, the bridge running away to "
     "the right over the stream; across the bridge head one thick rough wooden log laid level on two wooden trestles, blocking "
     "the way; the water under the arch, a row of bamboo along the bank; morning mist lying on the water, low cold golden light "
     f"coming from the right; no notice board, no signboard; {BLANK_TEXT}", 15, False),
    ("set-zhufa-ye",
     "a bamboo raft on a quiet stream in ancient Chinese Song-dynasty countryside at deep night: the raft about three metres "
     "long, eight thick bamboo poles lashed side by side, heading toward the left; in the middle of it two bundles wrapped in "
     "oiled cloth and tied with hemp rope; at its stern on the right one bamboo pole standing upright with one blank paper "
     "lantern hanging from it, glowing warm; both banks black silhouettes of bamboo and willow; no moon, a black sky full of "
     "stars, the dark water reflecting the starlight and the warm glow of the lantern, the lantern and the stars the only "
     f"light; nobody on the raft; {NIGHT}; {BLANK_TEXT}, the lantern plain", 16, True),
    ("set-shuyuan",
     "the front gate of an ancient Chinese Song-dynasty county academy on a town street in the morning: set back on the right of "
     "the picture three wide stone steps up to a pair of vermilion-red double doors standing open, a plain blank wooden plaque "
     "over the gate and no couplets beside it, a grey tiled roof with upturned eaves and whitewashed walls; the stone-paved "
     "street running away to the left past low tiled shops whose signboards are blank; bright morning sunlight from the right "
     f"casting the shadows of the steps; no table, no cart; {BLANK_TEXT}", 16, False),
    ("set-dukou",
     "a small ferry landing where a stream meets a wider river in ancient Chinese Song-dynasty countryside at dawn: a short "
     "wooden jetty and a few weathered wooden mooring posts at the water's edge, reeds along the bank, a packed-earth slope "
     "rising to the upper right toward a poor thatched farmhouse and, further off, a small village of thatched roofs; dawn, "
     f"the sky along the horizon glowing red and the water catching the red; no smoke, no fire, no boat, no raft; {BLANK_TEXT}",
     16, False),
    ("set-zhifang-shao",
     f"the burnt-out ruin of a thatched papermaking work shed beside {SONG} farmhouse in the morning just after the fire has "
     "been put out: charred black bamboo posts fallen across the ground, a thick layer of grey ash and black embers, three round "
     "wooden tubs scorched black, a few thin wisps of white smoke rising from the ashes; the farmhouse yard and its earthen wall "
     "at the left edge, at the right back a bamboo fence with one section trampled flat; clear dry morning sunlight from the "
     f"right; no flames; {BLANK_TEXT}", 17, False),
    ("set-zhifang-gujia-ye",
     f"the cleared ground of a burnt-down work shed beside {SONG} farmhouse at deep night: the grey ash swept into heaps at one "
     "side, in the middle a new bare timber frame of freshly peeled pale pine posts, four tall main posts joined by two cross "
     "beams and no roof; a bonfire burning on the ground at the front left, two blank paper lanterns hanging from the cross "
     "beams glowing warm; the farmhouse yard wall at the left; a black sky; the bonfire and the two lanterns the only light, "
     f"warm orange on the pale wood, deep darkness beyond; {NIGHT}; {BLANK_TEXT}, the lanterns plain", 17, True),
    ("set-chalou",
     "a private room on the upper floor of an ancient Chinese Song-dynasty county-town teahouse on an overcast late-autumn "
     "morning: an open wooden lattice window on the right looking out over grey tiled town roofs, the top of a wooden staircase "
     "on the left, a square wooden table in the middle with one clay teapot and two small clay teacups on it, a small table by "
     "the window, a folding screen with plain blank panels, wooden walls with nothing hung on them; soft flat grey-white "
     f"overcast light from the window on the right; no wine jar, no wine cups; {BLANK_TEXT}", 18, False),
    ("set-qianfu-houmen-ye",
     "a narrow alley behind a rich ancient Chinese Song-dynasty manor at deep night: high plastered walls, the mouth of the "
     "alley on the left, on the right the manor's back gate, two black wooden doors standing half open; through them the back "
     "courtyard of the manor: a round stone table in the middle and, under the eaves of a covered walkway, one blank paper "
     "lantern glowing warm; no moon, an overcast black sky; the lantern's glow spilling out through the gap of the doors onto "
     f"the alley stones the only light, the alley itself dark; {NIGHT}; {BLANK_TEXT}, the lantern plain", 18, True),
    ("set-xianya-gongtang",
     "the court hall inside an ancient Chinese Song-dynasty county yamen on an overcast day: at the middle back on a low dais the "
     "magistrate's long judgement desk with one flat rectangular wooden block and a brush rack on it, a chair behind it; behind "
     "the desk a large folding screen of plain blank panels and above it a blank wooden plaque; red wooden pillars, a grey stone "
     "floor open in front of the desk with room for two rows of constables along the left and right; the entrance doorway on "
     f"the left letting in soft grey-white overcast light; no mallet, no hammer, no weapon rack; {BLANK_TEXT}", 18, False),
    ("set-xianya-ceting",
     "a small plain side room off the court hall of an ancient Chinese Song-dynasty county yamen on an overcast day: a long "
     "narrow wooden side table against the back wall, two plain wooden armchairs, a doorway on the left hung with a plain undyed "
     "cloth curtain, one paper lattice window giving soft grey-white light; plain walls with nothing hung on them; "
     f"{BLANK_TEXT}", 18, False),
    ("set-wuding",
     "the grey-tiled roof of a small ancient Chinese Song-dynasty farmhouse at night in late autumn, seen along the roof: rows of "
     "old grey roof tiles, the ridge running across the picture; a bamboo ladder leaning against the eaves on the left; below "
     "the eaves the dark yard and the top of a persimmon tree with almost all its leaves gone and a few persimmons left; deep "
     "night, a black sky, a bright moon high at the upper right, its cold white moonlight the only light, a faint sheen of "
     f"frost on the tiles; no lantern, no candle; {NIGHT}; {BLANK_TEXT}", 19, True),
    ("set-xuji-pu",
     "the open front of a small new shop on a stone-paved street of an ancient Chinese Song-dynasty county town on an early "
     "winter morning, seen from the street: the wooden door panels all taken down so the whole front stands open; over the "
     "doorway a signboard wholly covered by a plain red cloth; inside, a wooden counter on the left with a tall stool behind it, "
     "two rows of empty wooden shelves along the right, a plain back door at the back; next door on the right the front of a "
     "silk shop with bolts of coloured cloth hanging at its door and a blank signboard; the stone slabs in front white with "
     f"frost; low clear early-winter sunlight from the right; every signboard blank; {BLANK_TEXT}", 20, False),
]
assert len(PORTRAITS) + len(SETS) == 22 and len({s[0] for s in SETS}) == 18
for sid, desc, _, night in SETS:
    assert not re.search(r"\b(person|man|woman|people)\b(?! anywhere)", desc.replace(EMPTY, "")), f"{sid}: a person is named"
    if night:
        assert "only light" in desc and NIGHT in desc, f"{sid}: a night set must name its only light and rule out daylight"

# --- manifests ----------------------------------------------------------------------------------------------------
edit_rule = ("image 1 is a photograph of the place: keep exactly its layout, posts, tubs, table, roof, floor, props and camera "
             "position; the only change is the light and time of day described here. ")
day_shed = LIVE / "set-gongpeng-l1.png"
grey_p = str(out / st["canvas"]("grey-portrait.png", 864, 1152))
grey_s = str(out / st["canvas"]("grey-set.png", 1312, 736))
(out / "prompts" / "negative.txt").write_text(st["NEG"], encoding="utf-8")
(out / "prompts" / "negative-set.txt").write_text(st["NEG"] + ", people, person, crowd, figure", encoding="utf-8")
(out / "prompts" / "negative-night.txt").write_text(
    st["NEG"] + ", people, person, crowd, figure, daylight, sunlight, blue sky, daytime, bright sky", encoding="utf-8")

items = []  # (picture id, prompt, width, height, base, negative, episode)
for pid, desc, ep in PORTRAITS:
    items.append((pid, st["BLANK"] + st["HEAD"].format(desc=re.sub(st["FEET"], "", desc)), 864, 1152, grey_p, "negative.txt", ep))
for sid, desc, ep, night in SETS:
    if sid == "set-gongpeng-ye" and day_shed.is_file():
        body, base = edit_rule + st["PLACE"].format(desc=desc), str(day_shed)
    else:
        body, base = st["BLANK"] + st["PLACE"].format(desc=desc), grey_s
    items.append((sid, body, 1312, 736, base, "negative-night.txt" if night else "negative-set.txt", ep))

parts = {"e011-e020-a": [], "e011-e020-b": []}
summary = []
for pid, body, w, h, base, neg, ep in sorted(items, key=lambda i: i[6]):
    (out / "prompts" / f"{pid}.txt").write_text(body + " " + st["STYLE"], encoding="utf-8")
    part = "e011-e020-a" if ep <= 15 else "e011-e020-b"
    parts[part] += [{"id": f"{pid}-{s}", "reference_images": [base], "prompt_file": str(out / "prompts" / f"{pid}.txt"),
                     "negative_file": str(out / "prompts" / neg), "width": w, "height": h, "seed": s, "latent": "empty"}
                    for s in st["SEEDS"]]
    summary.append({"picture": f"{pid}-l1", "first_episode": ep, "manifest": part, "night": neg == "negative-night.txt",
                    "base": "edit of set-gongpeng-l1" if base == str(day_shed) else "grey canvas"})
for name, jobs in parts.items():
    (out / f"{name}.json").write_text(json.dumps({"jobs": jobs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
(out / "e011-e020-pictures.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(", ".join(f"{len(v)} jobs -> {out / (k + '.json')}" for k, v in parts.items()))
