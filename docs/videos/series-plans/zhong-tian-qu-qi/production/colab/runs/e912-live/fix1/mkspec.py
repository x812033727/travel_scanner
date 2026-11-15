"""e912 fix1: retakes merged from review-picks-a/b (s02 s04 s22 s24 s26 s33), same steps as e911 fix1.

Decided in picks-merged.tsv: s26 and s33 both reviewers retake; s02, s04, s22 (picks-a retake, picks-b kept 1101) and s24
(picks-b retake, picks-a kept 1101) retaken after frame checks, because the problem runs through the whole take and cannot be
cut or patched: s02 all three women stare into the lens from frame 0 and smile from 2.5 s; s04 Hu speaks into the lens from
5 s to the end (and both background men wear sword hilts in sharp focus); s22 the foreground official's hat is a cloth wrap
with long hanging tails (not Hu's winged futou), a man in black holds a sheathed sword in sharp focus 0-3 s, Xu Yan grins
with teeth through the whole line; s24 the pouch is grey-brown (dark red everywhere else) and turns into an abacus in her
hands. s08 (picks-a retake) is kept: 1101 wide shot, spear at the gate and small hilts patched in post, as e911 did.

retake.py starts from st1, so the d1 edits of e912-live/spec.json for these shots (s02, s22, s24) are applied first.
Lessons written in (e911 fix1/fix2, both reviews of e912 d1):
- weapons: wherever d1 wrote men in black behind someone (s04, s22), the model gave them swords; they are cut out of the
  frame, the background is a dark wall or fence, torches held off screen, "nobody stands behind him", no weapon racks,
  poles or spears; nobody's title word is written (no constable, runner, magistrate in the new text). Every hand written.
- waists out of the frame where a man stands (s04 chest up, s22 and s24 waist up).
- lens: s02 the camera is moved off to the left and their eyes go to a man far beyond the right edge; the front portraits of
  Tang Xiaotang and A-ling go (picks-a: the front portraits turned them to the lens; their angle pictures stay; Qin Shuang
  has only her portrait, so hers stays). s04 he turns to screen right into profile instead of "toward the whole yard"
  (which put him face to the lens). s33 drops xuyan-portrait-l1 (both reviewers) and spreads the action over ten seconds
  (both drafts did it in 2 s and then stared into the lens for 8).
- no smile: e911 fix2 s21 wrote "no smile" hard and both seeds still grinned after 4 s. So no shot relies on a negative:
  every face that must not smile gets a concrete hard action (jaw set, biting the lip, frown, sniff and turn away), s24 is
  bought at 6 s instead of 8 (duration_seconds below, applied by mkjobs.py; retake.py copies st1's), and s26 has Hu turn
  away and leave in the last two seconds, so the late-grin window is his back.
- props: s24 the dark-red pouch and the abacus are both in hands from the first frame, "nothing changes into anything else".
- paper: s22/s24 only a small blank slip, no sheet front.
- hanging things: "no hanging beads", plus corn and chili strings (s33 d1 1101, s31/s32 d1 1102).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
D1SPEC = json.loads((HERE.parent / "spec.json").read_text(encoding="utf-8"))["shots"]

LINES = ["Facial expressions follow the action and lines described below,", "Facial expressions follow the action described below,"]
BEADS = ["no strings of beads and no glitch effects anywhere.",
         "no strings of beads, no hanging beads, no bead curtains, no strings of red beads, no strings of corn or chili hanging "
         "anywhere and no glitch effects anywhere."]
NOWEAPONS = "no weapon racks, no poles, no spears, no tassels and no weapons of any kind anywhere"

S = {
 "s02": {"replace": D1SPEC["s02"]["replace"] + [
   ["medium shot past one blank paper lantern with no writing hanging under the eaves in the foreground: at the house door the three women side by side, framed from the knees up with space above their heads, their faces three-quarter to screen right toward the young man in the middle of the yard off screen right, never the lens:",
    "medium shot from the left side of the house door, the camera standing off to the left of the three women at chest height, past one blank paper lantern with no writing hanging under the eaves in the foreground: at the house door the three women side by side, framed from the knees up with space above their heads, all three faces in three-quarter profile turned toward screen right, their eyes on a young man standing in the middle of the yard far beyond the right edge of the frame, at the height of a standing man's eyes; nobody faces the camera and nobody looks at the lens at any moment:"],
   ["Qin Shuang moved: her brows easing, one corner of her mouth loosening a little, not a smile; Tang Xiaotang moved: her eyes suddenly wet and shining, lips pressed together, no smile; A-ling still: eyes slowly lifting, lips closed;",
    "Qin Shuang moved but holding it in: her jaw set hard, she swallows once and blinks fast, her lips pressed into a flat line; Tang Xiaotang close to tears and worried: her eyes wet and shining, she bites her lower lip, her chin trembling, her brows drawn up; A-ling still and cold: her face unmoving, her lips closed;"],
   ["behind them only the dark doorway and darkness and the orange flicker of torches held by people out of the frame; no torch on a stand, in the ground or on a wall, no brazier;",
    "behind them only the dark wooden door frame, the dark doorway and the dark earth wall of the house, soft and out of focus; the warm orange torchlight falls on their faces from off screen right, every torch held by people outside the frame; no flame and no fire anywhere in the frame: no torch on a stand, in the ground or on a wall, no brazier, no fire bowl;"],
   ["no smile at any moment, not even at the end of the shot, until the last frame,",
    "their faces stay hard and tearful to the last frame, the corners of their mouths pulled down, their cheeks never lifting, no smile, their heads turned toward screen right, never toward the camera,"],
   LINES, BEADS],
  "drop_pictures": ["tangxiaotang-portrait-l1.png", "aling-portrait-l1.png"]},
 "s04": {"replace": [
   ["framed from the knees up with clear space above his head, at first his face three-quarter to screen left toward the young man off screen left, then turning toward the whole yard, his eyes sweeping past the lens, never into it;",
    "framed from the chest up with clear space above his head, his waist below the bottom edge of the frame, the camera at his eye level off to screen left; at first his face three-quarter to screen left toward the young man off screen left; then he turns his body to screen right, toward the people of the yard standing beyond the right edge of the frame, so that we see him in profile; his eyes never pass the lens and never look into it; his left hand stays clenched in a fist in front of his belly and his right hand flings his wide right sleeve;"],
   ["scornful: a cold sneer at one corner of his mouth, eyes narrowed, mouth wide between words;",
    "scornful and hard: eyes narrowed to slits, brows drawn down, nostrils flared, one corner of his mouth pulled down in a cold sneer, mouth wide only on the shouted words, no grin and no laughing;"],
   ["behind him, soft and out of focus and seen only from the chest up, two men in plain black robes and black caps, each holding one burning torch up in his right hand, his left hand empty and out of the frame, no spear, no sword, no scabbard, no blade of any kind; darkness and the orange flicker of torches held by people out of the frame; no torch on a stand, in the ground or on a wall, no brazier. Besides him, only the other people the composition names are in the frame;",
    "behind him only the dark earth wall of the farmhouse and darkness, soft and out of focus, and the orange flicker of torches held by people outside the frame; nobody else is in the frame, no figures behind him; no torch on a stand, in the ground or on a wall, no brazier, " + NOWEAPONS + ". He is the only person in the frame;"],
   ["first Magistrate Hu sneers and steps back one pace, then turns toward the whole yard and flings one wide sleeve out, then speaks, raising his voice,",
    "first Magistrate Hu sneers with narrowed eyes and steps back one pace; then he turns his body to screen right and flings his right wide sleeve out hard to the side, his left fist clenched at his belly; then, his face in profile toward screen right, he speaks, raising his voice, his eyes on the people off screen right, never on the camera, his brows drawn down and his face hard to the last frame,"],
   BEADS]},
 "s22": {"replace": D1SPEC["s22"]["replace"] + [
   ["only the back of his black gauze futou hat, the back of his neck and his left shoulder in a blue-green official robe,",
    "only the back of his black gauze futou hat, a stiff black hat with two short flat wings sticking straight out to the sides at ear height and nothing hanging from it, no ribbons and no cloth tails, the back of his neck and his left shoulder in a blue-green robe,"],
   ["the small slip between two fingers of his right hand and the dark red silk pouch, smeared with mud in his left hand,",
    "the small blank slip pinched between the first two fingers of his right hand at chest height and the palm-sized dark red silk drawstring pouch, smeared with mud, held low in his left hand, both hands in front of him the whole shot,"],
   ["cool and pointed: brows level, eyes hard, the faintest wry curl at one corner of his mouth, no grin, teeth never showing, lips moving between words;",
    "cool and pointed: brows drawn slightly down, eyes hard and narrowed, jaw set, he speaks low and level; between words his lips close into a firm flat line with one corner pressed in, no grin and no smile at any moment;"],
   ["behind him only darkness and the orange flicker of torches held by people out of the frame; no torch on a stand, in the ground or on a wall, no brazier; no blade, no knife, no sword, no scabbard, no sheathed weapon at anyone's waist, no spear, no pole and no staff anywhere in the frame; every man in black holds only one burning torch in his right hand, his left hand empty, a plain black cloth sash at his waist with nothing hanging from it.",
    "behind him only the dark bamboo fence and the dark night, soft and out of focus, and the orange flicker of torches held by people outside the frame; nobody stands behind him, no men in black, no torch-bearers and no other figures anywhere in the background; no torch on a stand, in the ground or on a wall, no brazier, no fire bowl; no blade, no knife, no sword, no scabbard, " + NOWEAPONS + "."],
   ["Xu Yan rises to his full height and takes one step toward the official, stopping an arm's length away, the slip raised a little;",
    "Xu Yan rises to his full height and takes one step toward the official, stopping an arm's length away, the slip raised a little in his right hand, the pouch still in his left; his eyes stay on the official, never on the camera, and his face stays cool and hard to the last frame;"],
   BEADS]},
 "s24": {"replace": D1SPEC["s24"]["replace"] + [
   ["framed from the knees up with clear space above his head, facing screen right toward the magistrate off screen right,",
    "both of them framed from the waist up with clear space above their heads, their waists below the bottom edge of the frame, Xu Yan facing screen right toward the official off screen right,"],
   ["cool: brows level, eyes steady, lips moving evenly between words, no smile;",
    "cool: brows level, eyes steady, lips moving evenly between words, no smile; from the first frame he holds a palm-sized dark-red silk drawstring pouch smeared with mud in his left hand and a small folded blank paper slip in his right hand;"],
   ["held against her chest,", "hugged against her chest with both arms from the first frame to the last,"],
   ["focused: brows drawn, lips closed, no smile;",
    "worried and tense: brows knitted into a frown, she bites her lower lip, her eyes darting to the torchlight off screen right, lips pressed together, no smile;"],
   ["behind them only darkness and the orange flicker of torches held by people out of the frame;",
    "behind them only the dark earth wall of the farmhouse and darkness, soft and out of focus, and the orange flicker of torches held by people outside the frame; nobody else behind them;"],
   ["Xu Yan slips the slip back into the pouch, pulls the drawstring tight and, without turning his head, passes the pouch back with his left hand to Tang Xiaotang behind him; she takes it and hugs it against her chest together with the abacus and nods once;",
    "while speaking Xu Yan tucks the blank slip into the dark-red pouch with his right hand and pulls the drawstring tight; then, without turning his head, he reaches his left arm straight back and holds out the dark-red pouch; Tang Xiaotang takes it with her right hand and presses it on top of the abacus against her chest, both arms around them, and gives one tight nod with a frown; the pouch stays the same dark-red silk pouch and the abacus stays the same abacus to the last frame, nothing changes into anything else;"],
   ["no talking, no mouthing words, no smile at any moment,",
    "no talking, no mouthing words, her brows knitted in a worried frown and her lower lip caught between her teeth to the last frame, her cheeks never lifting, no smile at any moment,"],
   BEADS],
  "duration_seconds": 6},
 "s26": {"replace": [
   ["close-up of Magistrate Hu, in his black official gauze hat and blue-green seventh-rank official robe,",
    "close-up of Magistrate Hu, in his black gauze futou hat with its two short stiff flat wings clearly visible on both sides the whole shot and his blue-green round-collared robe,"],
   ["sour and muttering to himself: eyes narrowed, mouth twisting, lips moving low between words, no smile;",
    "sour and uneasy, muttering to himself: brows knitted hard, eyes narrowed, jaw clenched, the corners of his mouth pulled down, lips barely moving low between words, no smile and no teeth;"],
   ["behind him only the dark road beyond the gate and a few small torch flames moving away, each torch held up by one person too dark and small to make out, carrying nothing else: no spears, no poles, no flags; no brazier.",
    "behind him beyond the gate only the empty dark country road and black fields, with two or three tiny torch flames far away in the distance; nobody stands near the gate or anywhere close behind him; no flags, no banners, " + NOWEAPONS + "; no torch on a stand, no brazier."],
   ["Magistrate Hu glances back at the yard and mutters to himself, his whole head staying in the frame; then he turns and hurries away out of the frame to screen right;",
    "Magistrate Hu glances back at the yard over his shoulder with narrowed eyes and mutters to himself through his clenched jaw, his whole head staying in the frame; in the last two seconds he gives one short sharp sniff, turns his face away from the yard with a scowl and hurries out of the frame to screen right;"],
   ["no smile at any moment, not even at the end of the shot, until the last frame,",
    "his scowl never softens, his cheeks never lift and the corners of his mouth stay pulled down, no smile and no grin at any moment, not even at the end of the shot, until the last frame,"],
   BEADS]},
 "s33": {"replace": [
   ["framed from the waist up with clear space above his head and his raised hands, his face three-quarter to screen right, never the lens;",
    "the camera off to screen left of him at chest height, framed from the waist up with clear space above his head and his raised hands, his face three-quarter to screen right or in profile the whole shot, his eyes always on a point off screen right or on the ground, never the lens, never facing the camera;"],
   ["no other torch, no lantern on a stand, no brazier;",
    "no other torch, no lantern on a stand, no brazier; nothing hangs from any pole, eave or wall;"],
   ["Xu Yan springs up from the stone stool, grabs his hair with both hands and turns half round on the spot; then his hands drop to his sides and his shoulders sag;",
    "Xu Yan sits on a round stone stool at the start, his face three-quarter to screen right; over the first two seconds his eyes go wide; then he springs up off the stool, grabs his hair with both hands and slowly turns half round on the spot, so that we see his profile and then the back of his head, still clutching his hair; around the middle of the shot he turns back to three-quarter screen right, his hands slowly sliding down from his hair; in the last seconds his hands drop to his sides, his shoulders sag and his head droops, his eyes on the muddy ground off screen right; the movement is spread evenly over the whole ten seconds, he never stops still and never stands staring ahead;"],
   LINES, BEADS],
  "drop_pictures": ["xuyan-portrait-l1.png"]},
}
(HERE / "spec.json").write_text(json.dumps({"seeds": [9121201, 9121202], "shots": S}, ensure_ascii=False, indent=1), encoding="utf-8")
