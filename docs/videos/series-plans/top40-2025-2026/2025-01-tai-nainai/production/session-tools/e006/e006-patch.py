import re
from pathlib import Path
p=Path('e006-gen-en.py'); t=p.read_text()

def block_span(sid):
    s=t.index(f'shot("{sid}", ')
    m=re.compile(r'\nshot\("c\d\d", |\nORDER = ').search(t, s+5)
    return s, m.start()+1
def drop(sid):
    global t
    s,e=block_span(sid); t=t[:s]+t[e:]
def put(sid, new):
    global t
    s,e=block_span(sid); t=t[:s]+new.strip('\n')+'\n'+t[e:]
def block(sid):
    s,e=block_span(sid); return t[s:e]
def edit(sid,o,n):
    global t
    s,e=block_span(sid); b=t[s:e]; assert o in b,(sid,o); t=t[:s]+b.replace(o,n)+t[e:]

for sid in ('c02','c03','c13','c30'): drop(sid)

# costume constants
t=t.replace('''ZY = ("Shen Zhiyuan with short neat black hair, a white pharmacist's coat worn open over a dark navy shirt with the sleeves rolled to the elbows, "
      "dark grey trousers and black sneakers")''',
'''ZY = ("Shen Zhiyuan with short neat black hair, a white pharmacist's coat worn open over a dark navy shirt, the white coat sleeves pushed up to mid-forearm, "
      "dark grey trousers and black sneakers")
ZY_UP = ("Shen Zhiyuan with short neat black hair, a white pharmacist's coat worn open over a dark navy shirt, the white coat sleeves pushed up to mid-forearm")''')
t=t.replace('MF = (', '''YT_UP = ("Shen Yuetang in her moon-white high-collared cotton shirt with frog buttons fastened to the throat and long narrow sleeves, "
         "one thick braid over her right shoulder")
FB_UP = ("Fu Bo, a very old man with very short white hair, in his neatly ironed light blue-grey Chinese-style jacket with frog buttons, "
         "the silver chain of a pocket watch at a button")
MF = (''',1)
assert 'ZY_UP' in t and 'YT_UP' in t
WIDE={'c01','c16','c25','c38'}
for sid in re.findall(r'shot\("(c\d\d)", ', t):
    if sid in WIDE: continue
    s,e=block_span(sid); b=t[s:e]
    b=b.replace('{YT}','{YT_UP}').replace('{FB}','{FB_UP}').replace('{ZY}','{ZY_UP}')
    b=b.replace("a white coat cuff with a dark navy shirt sleeve rolled to the elbow", "a white coat sleeve pushed up to mid-forearm")
    t=t[:s]+b+t[e:]

# c05
edit('c05',"standing at the west side of the long red-wood table; in the first frame her bare right hand has just set one small white porcelain teacup on the table at the bottom "
    "\"\n    f\"edge of the frame; {MORNING_R}.",
    "standing at the west side of the long red-wood table, both hands already folded at her waist in the first frame; one small white porcelain teacup already stands on the "
    "\"\n    f\"table in front of him at the bottom edge of the frame; {MORNING_R}.")
edit('c05',"In the first second she draws her right hand back and folds both hands at her waist;","In the first second she inclines her head a little;")
edit('c05','motion="She sets down his tea, folds her hands','motion="His tea already served, she folds her hands')
edit('c05','clip_seconds=8','clip_seconds=8')
# c07 c09 c24 c36 -> MCU
for sid in ('c07','c24','c36'):
    edit(sid,'camera="Close-up, slow push in from chest to face"','camera="Medium close-up, gentle push in to a medium close-up"')
    edit(sid,'Exactly one person in the whole frame: {YT_UP}','Exactly one person in the whole frame, a medium close-up from the chest up: {YT_UP}')
edit('c09','camera="Low-angle close-up, slow push in from chest to face"','camera="Low-angle medium close-up, gentle push in to a medium close-up"')
edit('c09','Exactly one person in the whole frame: "','Exactly one person in the whole frame, a medium close-up from the chest up: "')
edit('c09',"slowly and firmly, her lips, jaw and cheeks moving clearly with every syllable, and at each item her bare right forefinger taps lightly on the back of her left hand. ",
     "slowly and firmly, her lips, jaw and cheeks moving clearly with every syllable, giving one small nod of the chin at each item. ")
edit('c09','motion="Back straight, she lists the three things an old shop contract must attach, tapping her hand at each."','motion="Back straight, she lists the three things an old shop contract must attach."')
edit('c09','clip_seconds=8','clip_seconds=10')
edit('c07','below the bottom edge "\n    "of the frame','below the bottom edge "\n    "of the frame')
# c10
edit('c10',"morning sunlight from \"\n    \"screen right glints on his gold-rimmed glasses.","morning sunlight from \"\n    \"screen right glints on his gold-rimmed glasses, which have already slid halfway down his nose in the first frame.")
edit('c10',"In the first second his glasses slide a little down his nose and he pushes them back up \"\n    \"with his right middle finger;","In the first second he pushes his glasses back up his nose \"\n    \"with his right middle finger;")
edit('c10','motion="His glasses slip down his nose and he pushes them back, caught out."','motion="Caught out, he pushes his slipped glasses back up his nose."')
# c11 clip 10
edit('c11','clip_seconds=8','clip_seconds=10')
# c14
edit('c14','{BLACK} and {BROWN} stacked under his left arm.','{BLACK} and {BROWN} already stacked together under his left arm.')
# c17
put('c17','''shot("c17", D2, camera="Insert, close-up, locked", characters=["yuetang-18"], ref_characters=[], no_set=True, no_face=True, action_seconds=3, prompt=(
    f"{KITCHEN}. The first frame is already tight on a young woman's soapy left hand in the centre of the frame, back of the hand up, a narrow moon-white cuff folded back "
    "to the wrist; the thick old silver ring is only on her left ring finger, its seal face turned to the palm and unseen. Only the fingertips of her bare right thumb and "
    "forefinger, with no ring, reach in from the right edge of the frame and pinch the ring; a white sink far out of focus behind. In the first second the fingertips twist "
    "the ring and pull; it does not move at all, the fingertips slip off and withdraw past the right edge. The ring stays only on her left ring finger the whole shot. Only "
    "her hands are in the frame, no face. End: her left hand alone in the centre, the ring still on its ring finger."),
    motion="Her fingertips twist and pull at the ring; it will not move.")''')
# c19 c27 c36 clip 10
for sid in ('c19','c27','c36'): edit(sid,'clip_seconds=8','clip_seconds=10')
# c21
edit('c21','camera="Close-up, slow push in from chest to face"','camera="Close-up, locked"')
edit('c21',"The same face from the first frame to the last: eyes a little warm and wet at the rims,","Her face in three-quarter profile turned toward screen left, eyes lowered to the lower left; the same face from the first frame to the last: eyes a little warm and wet at the rims,")
edit('c21',"In the first frame she is looking down at her hand;","In the first frame she is looking down to the left at her hand;")
edit('c21','action_seconds=4','action_seconds=3')
# c22
edit('c22',"cuffs \"\n    \"folded back to the wrist, holding a white cotton cloth in both hands below her chest at the bottom edge of the frame.","cuffs \"\n    \"folded back to the wrist, both hands folded at her waist at the bottom edge of the frame.")
edit('c22',"In the first second she dries both hands on the white cloth, puts it down and folds her \"\n    \"hands at her waist;","In the first second she draws her folded hands in and \"\n    \"straightens her back;")
edit('c22','motion="Drying her hands, she asks','motion="Hands folded, she asks')
# c28
edit('c28',"{DINING}; {D_DOOR.format(who='him')}; the camera on her side, at his left front.","{DINING}; behind him only an out-of-focus dark wooden cupboard and a cream wall, the doorway beyond the right edge of the frame; the camera on her side, at his left front.")
edit('c28','addressee="the open doorway beyond the right edge of the frame, in profile"','addressee="the doorway beyond the right edge of the frame, in profile"')
edit('c28',"eyes turned to the doorway at screen right","eyes turned to the doorway beyond the right edge of the frame")
edit('c28',"his head is already turned to the doorway; in the first second he takes one step toward it;","his head is already turned to the doorway off screen right; in the first second he takes one step toward it;")
# c29
put('c29','''shot("c29", D3, camera="Medium shot, tracking with Shen Zhiyuan from the doorway toward the table", characters=["zhiyuan"], no_set=True, action_seconds=3, prompt=(
    f"{DINING}; the edge of the doorway frame along the right edge of the picture, the dark open doorway behind him, the only doorway in view; {LAMPLIGHT}. Exactly one "
    f"person in the whole frame: {ZY}, a folded white A4 sheet in his right hand with its blank back to the camera, nothing written visible. Brows pulled down hard, eyes "
    "fixed on the table toward screen left, jaw clenched, a sharp breath out through the nose, no smile. In the first frame he has just stepped through the doorway; from the "
    "first second he strides quickly toward screen left. His lips stay closed. End: halfway to the table."),
    motion="Zhiyuan strides in from the doorway with a folded sheet of paper.")''')
# c31 includes slap
edit('c31',"standing at the table, his right hand pressed on the sheet at the bottom edge of the frame;","standing at the table, a folded white sheet in his right hand at the bottom edge of the frame;")
edit('c31',"eyes fixed down at her far off to the lower left,","eyes fixed down at her, well off to the left of the lens and below it,")
edit('c31',"In the first second he leans forward over the table;","In the first second he slaps the folded sheet down on the table, blank back up, nothing written visible, presses it flat with his palm and leans forward over the table;")
edit('c31','motion="Leaning over the notice,','motion="Slapping the notice down,')
# c32
edit('c32',"Lin Meifeng: eyes kept down \"\n    \"on the phone,","Lin Meifeng: face in three-quarter profile turned toward screen right, eyes kept down \"\n    \"on the phone,")
# c38
put('c38','''shot("c38", D3, camera="Medium two-shot, locked", characters=["yuetang-18", "xiaoman"], looks={"xiaoman": "damp"}, no_set=True, action_seconds=3, prompt=(
    f"{DINING}, half an hour later; seen side-on at the doorway end of the room; in the lower left foreground a corner of the table and the lidded white porcelain soup pot, "
    f"no longer steaming; beyond the doorway it is dark; {LAMPLIGHT}. Exactly two people in the whole frame; everyone else is out of the frame to the left. On screen right, "
    f"in the first frame already standing in the doorway with her head bowed, {XM}. On screen left, in the first frame already at the doorway end of the table two steps "
    f"from her, {YT}. Shen Xiaoman: eyes lowered, lips pressed tight, chin trembling, no smile. Shen Yuetang: brows squeezed together, eyes on the girl's face and then on "
    "her empty hands and shoulders, lips closed. In the first second Shen Yuetang takes two slow, steady steps and stops in front of her; the girl's shoulders draw in. "
    "Everyone's lips stay closed. End: the two of them face to face."),
    motion="Xiaoman stands in the doorway, head bowed; Yuetang steps up and stops in front of her.")''')
# c41
edit('c41',"In the first second Shen Yuetang puts both hands on the girl's shoulders and holds them; the girl bows her head \"\n    \"and sobs aloud;",
     "From the first frame both of Shen Yuetang's hands already rest on the girl's shoulders; in the first second the girl bows her head \"\n    \"and sobs aloud;")
# clip 8 for wav >= 5 s, keep; c28 and c22 already? set
for sid in ('c28',):
    if 'clip_seconds' not in block(sid): edit(sid,'no_set=True,','no_set=True, clip_seconds=8,')
p.write_text(t)
print('ok')
