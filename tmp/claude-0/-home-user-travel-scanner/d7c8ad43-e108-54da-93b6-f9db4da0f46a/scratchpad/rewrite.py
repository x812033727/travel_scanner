import json, sys
path = sys.argv[1]
d = json.load(open(path, encoding="utf-8"))
KEY = "the small old brass key, as long as his finger, with a plain round bow and no markings"
P = {}
P["c01"] = ("Inside the ancestral hall of the old Shen house at night, looking from inside toward the two lattice doors in the middle of the frame; their paper panels and the courtyard beyond are dark. "
 f"Exactly one person in the whole frame: Fu Bo in his grey Chinese jacket, half turned from the camera, both hands on the two open doors; {KEY}, already sits in the keyhole of the plain brass lock on their inner side. "
 "In the first two seconds he pulls both doors shut, turns the key once, pulls it out into his right hand and turns round to face the camera. Warm red candlelight from off screen on his face. "
 "Brows drawn together, eyes wet, lips trembling; he does not smile at any moment. Fu Bo speaks a Mandarin line, his lips, jaw and cheeks moving clearly with every syllable, his voice trembling. "
 "End: the doors shut behind him, the key pinched in his right hand.")
P["c01b"] = ("Inside the ancestral hall of the old Shen house at night. From the first frame to the last, the frame is filled by one old man's right hand in a grey Tang-jacket cuff, "
 "pinching in its palm a small old brass key as long as his finger, with a plain round bow and no markings. Behind the hand, out of focus, the closed lattice doors, their paper panels dark with the night outside; "
 "warm red candlelight falls on the hand from out of frame; the oil lamp is out of the frame. In the first half second the fingers tighten on the key until the knuckles whiten, and the hand trembles once. "
 "Only this one hand is in the frame; no face, no mouth, no second hand. End: the key held tight in the fist.")
P["c02"] = ("Inside the ancestral hall of the old Shen house at night, seen from the doorway looking north, a round straw cushion on the floor in the foreground. "
 "Exactly one person in the whole frame: Shen Yuetang in the off-white burial robe and white cloth shoes, her thick black braid over her right shoulder, on screen left in front of the old dark red-brown medicine cabinet of thirty unlabelled drawers, as tall as her shoulders and wider than her outstretched arms. "
 "On screen right the round bronze mirror and the empty reclining chair in shadow. In the first second she turns slowly toward the doorway just right of the camera, back straight, hands folded in front of her waist, "
 "and looks first into the eyes of someone there, then down at his hand. Calm, level gaze; she does not smile at any moment. "
 "Shen Yuetang speaks a Mandarin line, her lips, jaw and cheeks moving clearly with every syllable, calm. End: standing, hands folded, looking toward the doorway.")
P["c03"] = ("Inside the ancestral hall of the old Shen house at night, looking toward the doorway; behind him only the closed lattice doors, their paper panels dark. "
 f"Exactly one person in the whole frame: Fu Bo in his grey Chinese jacket, {KEY}, pinched in his right hand. "
 "In the first second his shoulders jolt; he takes one step forward and stops, the hand holding the key trembling. Eyes red and wet, brows raised and drawn together; he does not smile at any moment. "
 "Fu Bo speaks a Mandarin line, his lips, jaw and cheeks moving clearly with every syllable, his voice trembling, looking toward screen left. End: standing one step nearer, the key in his right hand.")
P["c04"] = ("Inside the ancestral hall of the old Shen house at night. Exactly two people in the whole frame. From behind Fu Bo's left shoulder: his grey jacket shoulder and the back of his very short white hair, soft, in the foreground at the right of the frame; his face is not seen. "
 "On screen left Shen Yuetang in the off-white burial robe stands in front of the old medicine cabinet of thirty drawers with brass ring pulls and no labels, the cabinet as tall as her shoulders. "
 "In the first two seconds, without turning round, she steps half a step back until her back almost touches the cabinet, reaches her right hand behind her, and her fingertips touch the brass ring of the top-left drawer at her shoulder height; her eyes never leave him. "
 "Steady, grave gaze; she does not smile at any moment. Shen Yuetang speaks a Mandarin line, her lips, jaw and cheeks moving clearly with every syllable, calm. Fu Bo keeps his mouth closed. End: her right fingertips resting on that ring.")
P["c05"] = ("Inside the ancestral hall of the old Shen house at night. The first frame is tight on the front of the old dark red-brown medicine cabinet, brass ring pulls, no labels on any drawer, and a young woman's bare right hand, no ring on it, in an off-white burial-robe cuff, reaching backwards, on the brass ring of the top-left drawer; "
 "warm orange-gold light from screen right; the lamp itself is out of the frame. From the very first second the hand pulls each drawer out half an inch and pushes it back, one after another along the row of six, then down to the next row and the next, faster and faster, the wood knocking in a steady rhythm. "
 "For the bottom two rows she squats slowly: only the hem of the robe and the trouser legs drop into the frame, and the hand keeps going. Her face is never in the frame; only this one hand. End: the hand on the bottom row, every drawer flush.")
P["c06"] = ("Inside the ancestral hall of the old Shen house at night, seen low from the door side looking north, a round straw cushion on the floor in the foreground. "
 "Exactly two people in the whole frame: on screen left Shen Yuetang in the off-white burial robe squats with her back to the old medicine cabinet, her right hand reaching back to the rightmost drawer of the bottom row; "
 "in the foreground on screen right Fu Bo, seen from behind, in his grey Chinese jacket, the small brass key in his right hand; his face is not seen. "
 "In the first second she pushes that last drawer in with a click and all thirty drawers stand perfectly flush. Then she rises slowly and steadily, back straight, and folds both hands in front of her waist, face calm and grave, not smiling. "
 "Fu Bo freezes; the key slips halfway out of his fingers but he keeps hold of it. Everyone's mouth is closed. End: she stands before the flush cabinet, hands folded; Fu Bo stands still.")
P["c07"] = ("Inside the ancestral hall of the old Shen house at night, seen from floor level; behind him only the closed lattice doors, their paper panels dark. "
 f"Exactly one person in the whole frame: Fu Bo in his grey Chinese jacket, {KEY}, in his right fist. "
 "In the first two seconds his knees give way and he sinks slowly to kneel on the wooden floor, both hands pressing the floor, the key still in his right fist, and lifts his face to look up toward screen left. "
 "Tears run down his lined cheeks, brows drawn up, mouth trembling; he does not smile at any moment. Fu Bo speaks a Mandarin line, his lips, jaw and cheeks moving clearly with every syllable, choked with tears. "
 "End: kneeling on both knees, hands on the floor, face lifted to screen left.")
P["c08"] = d["shots"]["c08"]["prompt"] + " End: the taller flame burning steadily."
P["c09"] = ("Inside the ancestral hall of the old Shen house at night, looking down from behind Shen Yuetang's right shoulder: her shoulder and thick black braid in the off-white burial robe, soft, in the foreground at the left of the frame; her face is never seen. "
 "At the lower right Fu Bo in his grey Chinese jacket kneels on the floor, looking up at her, eyes wet, not smiling. Exactly two people in the whole frame. "
 "In the first two seconds she steps forward once, bends and reaches out her right hand in its off-white cuff to hold him under the elbow; his own right hand, in a grey sleeve, holds the small brass key and trembles. "
 "She says something low and slow with her back to the camera; her mouth is never seen. Fu Bo keeps his mouth closed the whole shot. End: she bends over him, her right hand under his elbow; he still kneels.")
P["c10"] = ("Inside the ancestral hall of the old Shen house at night, the altar behind them. Exactly two people in the whole frame, seen side-on: on screen left Shen Yuetang in the off-white burial robe; on screen right Fu Bo in his grey Chinese jacket. "
 "First frame: he is already half risen from his knees, her right hand under his left elbow. Within the first second he stands up straight, leaning on her hand; she lets go and folds her hands in front of her waist. "
 "He wipes his eyes with his right cuff, the small brass key still in that fist, glances toward the reclining chair off screen right, and looks back at her. Both faces grave; neither smiles at any moment. "
 "Fu Bo speaks a Mandarin line, his lips, jaw and cheeks moving clearly with every syllable, low, wiping his tears. Yuetang keeps her mouth closed. End: both standing face to face.")
P["c11"] = ("Inside the ancestral hall of the old Shen house at night; behind her only a corner of the old medicine cabinet. Exactly one person in the whole frame: Shen Yuetang in the off-white burial robe, her thick black braid over her right shoulder, framed from mid-chest up from the first frame to the last. "
 "In the first second she lays her bare right palm flat on her chest just below the stand-up collar, fingers together; her left hand stays folded at her waist, below the frame. "
 "She looks into someone's eyes off screen right, steady and grave; she does not smile at any moment. Shen Yuetang speaks a Mandarin line, her lips, jaw and cheeks moving clearly with every syllable, calm. End: her right palm still on her chest.")
P["c12"] = ("Inside the ancestral hall of the old Shen house at night, seen from behind the old wooden reclining chair: its cane-woven back fills the foreground, the chair empty, no one and no clothes on it. "
 "Exactly two people in the whole frame, further back, standing side by side in front of the altar: Shen Yuetang in the off-white burial robe and Fu Bo in his grey Chinese jacket. "
 "In the first second both turn their heads at the same moment and look at the empty chair in the foreground; Fu Bo steps half a step back. Both faces grave; neither smiles at any moment. Everyone's mouth is closed. "
 "End: both standing, looking at the empty chair.")
P["c13"] = ("Inside the ancestral hall of the old Shen house at night; behind her only a corner of the altar. Exactly one person in the whole frame: Shen Yuetang in the off-white burial robe, her thick black braid over her right shoulder, framed from mid-chest up from the first frame to the last. "
 "In the first second she turns her head back from the reclining chair and looks at someone off screen right, eyes searching, brows slightly raised; she does not smile at any moment. "
 "Shen Yuetang speaks a Mandarin line, her lips, jaw and cheeks moving clearly with every syllable, soft. End: looking off screen right.")
P["c14"] = ("Inside the ancestral hall of the old Shen house at night; behind him only a corner of the altar and the blank ancestral tablets, out of focus. "
 f"Exactly one person in the whole frame: Fu Bo in his grey Chinese jacket, {KEY}, in his right hand. "
 "In the first second he straightens up and, out of habit, touches the silver chain of his pocket watch with his left fingertips. He looks at her face off screen left, eyes red and wet; he does not smile at any moment. "
 "Fu Bo speaks a Mandarin line, slowly, his lips, jaw and cheeks moving clearly with every syllable; he pauses for one breath, then speaks a second Mandarin line, hoarse, his lips moving clearly. "
 "End: standing, left fingertips on the watch chain.")
P["c15"] = ("Inside the ancestral hall of the old Shen house at night; behind her only a corner of the old medicine cabinet. Exactly one person in the whole frame: Shen Yuetang in the off-white burial robe, framed from the waist up so her folded hands show at the bottom edge. "
 "In the first second she goes still; her folded hands tighten once; her eyes drop, then lift again to someone off screen right. Lips pressed between words, brows slightly drawn; she does not smile at any moment. "
 "Shen Yuetang speaks a Mandarin line, her lips, jaw and cheeks moving clearly with every syllable, low. End: hands folded, looking off screen right.")
P["c16"] = ("Inside the ancestral hall of the old Shen house at night; behind him only the closed lattice doors, their paper panels dark. "
 "Exactly one person in the whole frame: Fu Bo in his grey Chinese jacket, the small old brass key in his right hand. "
 "In the first second he shakes his head, glances over his shoulder at the closed doors behind him, and looks back at her off screen left. Brows knotted, mouth turned down, troubled; he does not smile at any moment. "
 "Fu Bo speaks a Mandarin line, his lips, jaw and cheeks moving clearly with every syllable, uneasy. End: facing screen left, the key in his hand.")
P["c17"] = ("Inside the ancestral hall of the old Shen house at night; behind her only a corner of the old medicine cabinet. Exactly one person in the whole frame: Shen Yuetang in the off-white burial robe, framed from the waist up, hands folded in front of her waist. "
 "In the first second she lifts her chin slightly; the corners of her mouth curve into a faint smile; her gaze toward screen right is steady. "
 "Shen Yuetang speaks a Mandarin line, her lips, jaw and cheeks moving clearly with every syllable, light and unhurried. End: chin up, the faint smile.")
P["c18"] = ("Inside the ancestral hall of the old Shen house at night. Exactly two people in the whole frame: at the back in the middle, from the first frame, Fu Bo in his grey Chinese jacket stands at the altar beside the brass lamp; "
 "on screen left Shen Yuetang in the off-white burial robe stands in front of the old medicine cabinet, hands folded, watching him. "
 f"In the first two seconds his left hand lifts one corner of the lamp's plain square wooden base a finger's width, his right hand slides {KEY}, under it, and he sets the base down flat; the lamp stays upright and lit. "
 "Then he turns to her and bows deeply, face grave, not smiling. Fu Bo speaks a Mandarin line, his lips, jaw and cheeks moving clearly with every syllable, bowing. Yuetang keeps her mouth closed. "
 "End: the key hidden under the base, his hands empty, half bowed toward her.")
P["c19"] = ("Inside the ancestral hall of the old Shen house at night, one red candle at the corner of the altar in the foreground; the paper panels of the doors are dark. "
 "Exactly two people in the whole frame: on screen right Shen Yuetang in the off-white burial robe, from the first frame already sitting on the old wooden reclining chair with its cane seat; at the doorway in the background Fu Bo in his grey Chinese jacket, hands empty. "
 "In the first two seconds she lies back slowly, folds her hands at her waist and closes her eyes, her chest rising and falling gently, her face peaceful; she is resting, alive. "
 "At the same time Fu Bo bows deeply, steps back over the threshold and pulls the two lattice doors shut; through the paper panels a faint dark outline of him sits down on the stone step outside. "
 "Everyone's mouth is closed. End: the doors shut; she lies breathing, eyes closed.")
P["c20"] = ("Inside the ancestral hall of the old Shen house at night. The first frame is tight on the altar: two brand-new full-length red candles, one at each end, the left one already burning, and the brass oil lamp between them. "
 "From the first second a young woman's bare right hand, no ring on it, in a moon-white cotton cuff, holds a lit wooden match, shorter than her finger, to the wick of the right-hand new candle; "
 "the wick catches, the hand shakes the match out, and the new flame slowly stands up straight. Only this one hand is in the frame; no face. End: both new candles burning, the hand drawn back out of the frame.")
BIN = "the lidded green metal trash bin, about thigh-high,"
P["c21"] = ("The east covered corridor of the old Shen house at night under warm paper-shaded lamps, the courtyard beyond the pillars dark; a red-brown wooden pillar in the foreground. "
 "Exactly two people in the whole frame: Shen Yuetang in her moon-white high-collared cotton shirt and navy ankle-length skirt sits on the long wooden bench facing the camera, hands folded at her waist; "
 "Fu Bo in his grey Chinese jacket, hands empty, stands on her left, on screen right, bending slightly toward her. "
 f"Far off on screen right the kitchen door with {BIN} outside it; far off on screen left a closed bedroom door with no light behind it; nobody else anywhere. "
 "From the first second Fu Bo speaks a Mandarin line, bending, his lips, jaw and cheeks moving clearly with every syllable, low; Yuetang listens, grave, not smiling, mouth closed. "
 "Then he straightens and she nods once. End: she sits, he stands upright beside her.")
P["c22"] = ("The east covered corridor of the old Shen house at night; behind her only a wooden pillar and the dark courtyard. Exactly one person in the whole frame: Shen Yuetang in her moon-white high-collared cotton shirt, her thick black braid tied with a dark blue cord over her right shoulder, seated, framed from mid-chest up from the first frame to the last. "
 "In the first second she turns her head to look at an unlit bedroom door off screen left, then turns back to someone off screen right. Brows slightly drawn, worried; she does not smile at any moment. "
 "Shen Yuetang speaks a Mandarin line, her lips, jaw and cheeks moving clearly with every syllable, soft and concerned. End: looking off screen right.")
P["c23"] = ("The east covered corridor of the old Shen house at night; behind him only a warm paper-shaded lamp and the dark courtyard. Exactly one person in the whole frame: Fu Bo in his grey Chinese jacket, hands empty. "
 "From the first second he sighs and shakes his head, mouth turned down, tired and worried; he does not smile at any moment. "
 "Fu Bo speaks a Mandarin line, his lips, jaw and cheeks moving clearly with every syllable, sighing. As soon as he finishes he bows slightly and starts to turn toward screen right. "
 "End: halfway through the turn, his right shoulder toward screen right.")
P["c24"] = ("The east covered corridor of the old Shen house at night, seen low, the armrest of the long bench in the foreground; the courtyard beyond the pillars dark. "
 "Exactly one girl in the whole frame: Shen Xiaoman, bangs and blazer shoulders damp, her navy pleated skirt below the knee and dry, in her right hand a navy school backpack as big as her torso, dripping water, three small brass bells on a faded red cord at its front zip. "
 f"In the first second she comes in fast from screen right and stops at {BIN} outside the kitchen door; her left hand lifts the lid, her right stuffs the dripping bag inside, the lid drops shut, and she walks on toward screen left, head down. "
 "Eyes lowered, lips pressed tight; she never smiles or speaks. On the bench in the foreground, in shadow, only the folded hands and navy skirt hem of a seated young woman; the girl does not see her. "
 "Everyone's mouth is closed. End: the lid shut, the girl leaving at screen left.")
P["c25"] = ("The east covered corridor of the old Shen house at night. From the first frame to the last the frame is tight on the lidded green metal trash bin outside the kitchen door, its lid already rocking gently, a puddle of water on the floor beside it; far off on screen left, out of focus, a bedroom door. "
 "In the first second one muffled ring comes from inside the bin; the lid keeps rocking; then far off that bedroom door swings shut. No person anywhere in the frame. End: the lid settling still.")
P["c26"] = ("The east covered corridor of the old Shen house at night under a warm paper-shaded lamp; behind her only a wooden pillar and the dark courtyard. Exactly one person in the whole frame: Shen Yuetang in her moon-white high-collared cotton shirt, her thick black braid over her right shoulder, framed from mid-chest up from the first frame to the last. "
 "First frame: she is already nearly upright from the bench; in the first second she straightens to stand, folds both hands in front of her waist, and turns her head toward the kitchen door off screen right. "
 "Brows drawn, eyes fixed and worried; she does not smile at any moment. Her lips stay together the whole shot; the line is her inner voice. End: standing, looking off screen right.")
for k, v in P.items():
    d["shots"][k]["prompt"] = v
    print(k, len(v))
open(path, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
