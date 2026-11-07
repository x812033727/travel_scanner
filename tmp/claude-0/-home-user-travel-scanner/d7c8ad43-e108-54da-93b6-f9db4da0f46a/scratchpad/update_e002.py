import json, sys
from pathlib import Path

P = Path("/home/user/travel_scanner/docs/videos/tai-nainai-e002/shots-en.json")
d = json.loads(P.read_text(encoding="utf-8"))
S = d["shots"]

RING = "a thick old plain silver ring with a small square seal face, worn on her LEFT ring finger with the seal toward her palm"
HALL = "Inside the main hall of the old Shen house at night, lit by a warm hanging lamp overhead"

S["c01"]["prompt"] = (
    "The stone-paved courtyard of the old Shen house at night, the three stone steps of the ancestral hall; deep black night sky. "
    "Exactly two people in the whole frame: Shen Yuetang in the off-white burial robe on the top step, and exactly one woman in a wine-red dress, Lin Meifeng, at the foot. "
    "First frame: two lidded white porcelain teacups and a black lacquered tray in mid-air above the flagstones. "
    "Within the first second both cups shatter on the flagstones, tea splashing, the tray landing upside down. "
    "At once Meifeng lunges up one step and with her right hand yanks Yuetang's left wrist down; Yuetang is pulled half a step forward, not struggling, mouth closed. "
    "Warm yellow veranda light from off screen; a distant orange-gold glow on the altar. "
    "Meifeng speaks a Mandarin line, lips moving clearly, shrill. "
    "End: Meifeng on the lowest step gripping the wrist, Yuetang standing above her."
)

S["c01b"]["prompt"] = (
    "The stone-paved courtyard of the old Shen house at night. From the first frame to the last, two separate hands fill the frame. "
    "From screen left: a woman's right hand with bright red nails and a wine-red knit sleeve, bare fingers, gripping a wrist hard. "
    "Hanging limp on screen right: a young woman's left hand in a loose off-white burial-robe sleeve, wearing " + RING + ". "
        "Within the first second the red-nailed fingers squeeze tighter and their knuckles whiten; the limp hand stays open and loose. "
    "Below, soft out of focus, white porcelain shards and spilled tea on the flagstones; warm yellow light. "
    "Only these two hands and forearms are in the frame; the faces are out of frame above."
)
S["c01b"]["motion"] = "Within the first second the red-nailed hand squeezes the limp ringed wrist tighter and its knuckles whiten; the ringed hand stays loose."

S["c02"]["prompt"] = (
    "The courtyard of the old Shen house at night: Shen Yuetang standing upright on the top stone step of the ancestral hall, in the off-white burial robe, her thick black braid over her right shoulder. "
    "She stands from the first frame to the last; the camera pushes from her chest to her face. "
    "Behind her the dark hall door frame and one distant orange-gold glow on the altar; warm yellow veranda light on her face. "
    "Exactly one face in the frame: hers. At the lower right edge a red-nailed hand in a wine-red knit sleeve grips her left wrist; only that hand and sleeve show. "
    "In the first second she lowers her head and looks down at her own off-white robe and white cloth shoes; then slowly raises her head, the corners of her mouth curving into a small closed-lip smile. "
    "Her lips stay together the whole shot; the line is her inner voice. "
    "End: she stands on the step, head up, the faint smile."
)

S["c03"]["prompt"] = (
    "The courtyard of the old Shen house at night, a red-brown pillar of the west veranda in the foreground on screen left. "
    "The sky above the roofs is deep black night; the only light is the warm yellow veranda paper lanterns. "
    "Exactly three people: from screen left Shen Jianye in his brown double-breasted suit, a black phone in his right hand with its screen turned away, strides out of the west veranda; "
    "on screen right Lin Meifeng in her wine-red knit dress grips the left wrist of Shen Yuetang, standing on the lowest stone step in the off-white burial robe. "
    "Jianye stops before the women and looks Yuetang up and down; Meifeng lifts the wrist high to show him. "
    "First Jianye speaks a Mandarin line, lips moving clearly, frowning; then Meifeng speaks a Mandarin line, lips moving clearly, shrill, while Jianye's mouth is closed. "
    "Yuetang's mouth stays closed. End: the three standing at the steps."
)

S["c05"]["prompt"] = (
    HALL + "; a chair back of the long rosewood table in the foreground. "
    "On the left wall, far back, a tall dark wooden case seen edge-on, its front turned away. "
    "Exactly three faces. In the first second Lin Meifeng in her wine-red dress pulls Shen Yuetang by the left wrist in through the small courtyard door at the back right; "
    "Yuetang in the off-white burial robe walks steadily; Shen Jianye in his brown suit follows. "
    "Far back right, behind the post under the staircase, only the edge of a light grey hood shows, small and blurred. "
    "Meifeng hauls her to the open floor right of the table's near end, steps to Yuetang's left still gripping the wrist, and points at her. "
    "Meifeng speaks a Mandarin line, lips moving clearly, contemptuous; the others' mouths stay closed. "
    "End: Meifeng on screen left, Yuetang to her right, Jianye behind."
)

S["c06"]["characters"] = ["yuetang-18", "meifeng"]
S["c06"]["ref_characters"] = ["yuetang-18"]
S["c06"]["prompt"] = (
    HALL + ". Shen Yuetang in close-up from the first frame to the last, pushing from her chest until her face and shoulders fill the frame. "
    "Off-white burial robe, thick black braid over her right shoulder, back straight. "
    "At the lower left edge a red-nailed hand in a wine-red knit sleeve holds her left wrist up at chest height; only that hand shows. "
    "Behind her only a corner of the rosewood table and the blurred side table. Exactly one face in the frame: hers. "
    "In the first second she lowers her gaze to the red-nailed hand on her wrist; then she lifts her eyes to someone off screen left and speaks word by word. "
    "Brows level, gaze steady, calm; she does not smile at any moment. "
    "She speaks a Mandarin line, lips, jaw and cheeks moving clearly, calm and deliberate. End: her face fills the frame, eyes on screen left."
)

S["c07"]["ref_characters"] = ["meifeng"]
S["c07"]["prompt"] = (
    HALL + ". Over the shoulder: in the right foreground, blurred, one off-white burial-robe shoulder and the back of a black-haired head, seen only from behind. "
    "On screen left, exactly one woman in a wine-red knit dress and pearl necklace, Lin Meifeng, faces the camera, her red-nailed hand holding an off-white-sleeved wrist between them. "
    "Behind her only white wall and dark rosewood; nobody else in the room. "
    "From the first second her smile freezes and drains away: brows lifting, eyes fixed, lips parting in silent shock; she does not smile again. "
    "Within the first two seconds her red-nailed fingers open one by one and her hand drops to her side. "
    "The young woman in the foreground speaks a Mandarin line, back to the camera, calm; Meifeng says nothing. "
    "End: Meifeng standing stunned, her empty hand hanging at her side."
)

S["c11"]["prompt"] = (
    HALL + ". From the first frame to the last, Shen Yuetang's face and shoulders fill the frame; the camera pushes in slowly. "
    "Off-white burial robe, thick black braid over her right shoulder. "
    "At the lower right edge only a dark blue uniform cuff and a man's hand hold her left elbow. "
    "Behind her a corner of the rosewood table and the blurred side table. Exactly one face in the frame: hers. "
    "In the first second she turns her head toward screen right, looks into someone's eyes and then at his glasses; her eyes soften for a moment, mouth still, then she speaks. "
    "Brows level and relaxed, eyes steady, lips a calm straight line between words, composed; she does not smile at any moment and her eyes never widen. "
    "She speaks a Mandarin line, lips, jaw and cheeks moving clearly, calm. End: she looks off screen right."
)

S["c12"]["camera"] = "insert close-up, low near the floor, locked, slow motion"
S["c12"]["prompt"] = (
    "Inside the main hall of the old Shen house at night. The first frame: an old man's two hands in grey Chinese-jacket cuffs at the top of the frame, holding one small plain white porcelain cup, open at the top, full of tea; "
    "the dark wooden floorboards fill the lower half of the frame, open floor straight below the hands; behind, the front door soft out of focus. "
    "The whole clip plays in slow motion. Within the first second the hands tremble and the cup slips out between the fingers; it falls straight down onto the wooden floorboards and breaks into three white porcelain shards on the wooden floor, tea splashing out. "
    "The two empty hands stay frozen in mid-air above. Only the hands are in the frame; the face is out of frame above. "
    "End: three white porcelain shards in a small splash of tea on the wooden floor, the empty hands still raised."
)
S["c12"]["motion"] = "In slow motion, within the first second the cup slips from the trembling hands, falls to the wooden floor and breaks into three white porcelain shards while the empty hands stay in mid-air."

S["c15"]["prompt"] = (
    HALL + ", a chair back in the foreground. "
    "Exactly three sharp faces, left to right: Lin Meifeng in her wine-red dress, bent over laughing, a black phone in her raised right hand, its back to the camera; Officer Kai in dark blue uniform, lips pressed; Shen Yuetang in the off-white burial robe. "
    "Behind Meifeng a heavyset man in a brown suit laughs at the table, his face only a blur. "
    "In the right foreground an old man in a grey Chinese-style jacket, white hair, seen only from behind, stands inside the front door. "
    "In the first second her thumb moves to press; before it does Kai raises his right hand and covers the phone; her thumb stops. "
    "Meifeng speaks a Mandarin line, lips moving clearly, breathless with laughter. Yuetang: brows level, mouth a flat closed line, unsmiling. "
    "End: Kai's hand over the phone."
)

S["c16"]["camera"] = "low-angle close shot, slow push-in"
S["c16"]["prompt"] = (
    "Inside the main hall of the old Shen house at night, seen from low down looking up. From the first frame to the last, Fu Bo's face and shoulders fill most of the frame: an old man in a grey Chinese-style jacket, his hands empty. "
    "Close behind him a plain white wall beside a dark wooden door frame. Exactly one person in the frame. "
    "His eyes are fixed on someone's face off screen left; brows drawn together, mouth a flat closed line, shaken; he does not smile at any moment in this shot. "
    "In the first second he steps back once, then a second time, until his back meets the white wall and he stops; his throat moves as he swallows. Mouth closed. "
    "End: he stands with his back pressed to the white wall, staring off screen left."
)
S["c16"]["motion"] = "In the first second the old man steps back once, then again, until his back meets the white wall, and swallows, staring off screen left."

S["c17"]["prompt"] = (
    HALL + ". Exactly three people, left to right: Lin Meifeng in wine red, a black phone in her right hand; "
    "Officer Kai in uniform, a small black notebook and a pen in his left hand; Shen Yuetang in the off-white burial robe, wearing " + RING + ". "
    "In the first second Meifeng thrusts the phone past Kai at Yuetang's ring hand. By two seconds Kai looks down, clips the pen into the small black notebook and reaches his right hand toward the ring. "
    "Meifeng: brows arched, red lips tight; she does not smile at any moment. "
    "First Meifeng speaks a Mandarin line, lips moving clearly, shrill; then Kai speaks one, nodding, while Meifeng's mouth is closed. "
    "Yuetang's mouth stays closed. End: Kai's hand out toward the ring."
)

S["c18"]["prompt"] = (
    "Inside the main hall of the old Shen house at night. From the first frame to the last, two separate hands fill the frame. "
    "On screen right a young woman's left hand in an off-white burial-robe sleeve, back of the hand to the camera, fingers still, wearing " + RING + ", so only the plain band shows on the back of her finger. "
    "From screen left a man's right thumb and forefinger in a dark blue uniform cuff pinch that plain band; his hand touches only the ring. "
    "In the first second his fingers pull the ring outward along her finger, then twist it; it does not move at all. Her hand stays perfectly still. "
    "His fingertips whiten with effort, then let go and draw back out of frame. Behind, the off-white robe blurred. "
    "Only the two hands are in frame. End: her still hand alone, the ring in place."
)

S["c19"]["prompt"] = (
    HALL + ": Officer Kai in his dark blue police uniform, a small black notebook in his left hand; behind him only the dark rosewood table. Exactly one face in the frame: his. "
    "In the first second he shakes out his reddened right fingers and sighs, shoulders dropping. "
    "Brows drawn together, mouth a flat line between words, troubled and awkward; he does not smile or grin at any moment in this shot. "
    "He closes the small black notebook and tucks it into his breast pocket, then with his right hand takes an off-white sleeve at the elbow at the right edge of the frame and starts to turn toward the camera. "
    "Officer Kai speaks a Mandarin line, lips, jaw and cheeks moving clearly, sighing. "
    "End: halfway through his turn, his hand on the off-white sleeve."
)

S["c22"]["prompt"] = (
    "The black-lacquered double gate of the old Shen house at night, seen from low down at threshold height looking up from the lane; both gate leaves already stand wide open from the first frame, red and blue light sweeping over them. "
    "Exactly two people in the frame. Within the first second Fu Bo, an old man in a grey Chinese-style jacket, rushes in from the dark passage, stops behind the high wooden threshold and slaps both hands onto the two doorposts, gripping them. "
    "One step behind him in the passage, exactly one woman in a wine-red dress, Lin Meifeng, mouth closed. "
    "Fu Bo pants, brows drawn together, mouth tense, unsmiling, and raises his eyes to look out at the lane. "
    "Fu Bo speaks a Mandarin line, lips moving clearly, out of breath, his voice shaking but not raised. "
    "End: Fu Bo standing in the gateway gripping both doorposts, Meifeng behind his shoulder."
)

S["c23"]["ref_characters"] = ["fubo", "meifeng", "akai"]
S["c23"]["prompt"] = (
    "The front gate of the old Shen house at night, seen from the lane through the open double gate; red and blue light sweeps the black gate leaves. "
    "In the foreground on the stone step outside the threshold, exactly two figures seen only from behind: on the left Officer Kai in a pressed dark blue police uniform, a radio on his belt, his right hand at her elbow; "
    "on the right a slim young woman in an off-white burial robe, a thick black braid down her back. "
    "Inside, facing the camera, exactly one old man in a grey Chinese-style jacket, Fu Bo, stands behind the threshold gripping both doorposts. "
    "In the first second exactly one woman in a wine-red dress, Lin Meifeng, leans out from behind his shoulder and grabs his sleeve. "
    "Meifeng speaks a Mandarin line, lips moving clearly, shrill, disbelieving; Fu Bo's mouth stays closed, brows drawn. "
    "End: Fu Bo in the gateway, Meifeng clutching his sleeve."
)

for k in ["c01", "c01b", "c02", "c03", "c05", "c06", "c07", "c11", "c12", "c15", "c16", "c17", "c18", "c19", "c22", "c23"]:
    n = len(S[k]["prompt"])
    print(k, n, "OVER" if n > 900 else "")
P.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
