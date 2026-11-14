"""e909 fix2 (pick-review.md 中等 3): s25 and s26 bring the dagger in from screen right, as in s24; a straight dagger."""
import json, pathlib
SCAR = "one thin long-healed scar, pale whitish and never red, across the inside of her left wrist"
DAG = "one straight dagger with a straight-backed single-edged iron blade about a palm long, not curved, no guard, and a wooden grip wrapped in black cloth"
S = {
 "s25": {"replace": [
   ["his eyes straining sideways toward Aling off screen left behind his shoulder, his face three-quarter,",
    "his eyes straining sideways toward the woman behind his left shoulder off screen right, his face three-quarter to screen right,"],
   ["at the bottom edge of the frame a woman's left hand in a grey-white sleeve, one pale old scar across the inside of her left wrist, holding one dagger with a single-edged iron blade about a palm long and a wooden grip wrapped in black cloth, its sharp edge turned in toward his neck and its blunt back facing outward;",
    "from the RIGHT edge of the frame one slender woman's forearm in a plain grey-white long sleeve reaches in from behind his left shoulder, her left hand holding " + DAG + ", its sharp edge laid against the left side of his neck on screen right and its blunt back facing outward, the inside of that wrist turned toward us showing " + SCAR + "; her face and body never appear; nothing at all enters from the left edge of the frame;"],
   ["the dagger hand at the bottom edge does not move", "the dagger hand at the right edge does not move"]]},
 "s26": {"replace": [
   ["the left hand in a grey-white cotton sleeve holding one dagger with a single-edged iron blade about a palm long and a wooden grip wrapped in black cloth in a forward grip, its sharp edge turned up toward the edge of a blue-grey robe collar at the top of the frame and its blunt back facing outward; one pale old scar across the inside of her left wrist, clearly visible;",
    "the left hand in a plain grey-white cotton sleeve reaching in from the RIGHT edge of the frame, holding " + DAG + " in a forward grip, its sharp edge turned toward the edge of a man's blue-grey robe collar at the left of the frame and its blunt back facing outward; the inside of her left wrist turned up toward us, showing " + SCAR + "; nothing enters from the left edge but the collar;"]]},
}
pathlib.Path(__file__).with_name("spec.json").write_text(json.dumps({"seeds": [9091301, 9091302], "shots": S}, ensure_ascii=False, indent=1), encoding="utf-8")
