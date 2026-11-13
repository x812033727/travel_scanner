"""Generate video.json for sothatswhy-p26-plane-window (原來如此事務所 對話版 P26).

Run `python3 build_scenes.py` from anywhere: it rewrites video.json next to this file and freezes
every shot's camera move in cameras.json (a shot keeps the camera it was first given, so deleting
a shot never shifts the others: the camera is in the keyframe cache key).
Edit lines and prompts here, never in video.json.
Started from a copy of sothatswhy-p20-microwave-metal/build_scenes.py (series constants, helpers,
BANNED, assembly and self-checks unchanged; EXTRA and REWRITE start empty because P20's entries were picture
fixes for P20 only; SAY is empty because no line carries a Latin term); the content is new.
Every chief shot uses CHIEFFIX_DESC (uniform glossy jet-black hair, P20's wording); the base chief description
with the grey streak is no longer used in any prompt. CHARACTERS keeps the series appearance strings unchanged,
because the approved series sheets are keyed by them (series-sheets/README.md): changing them redraws the sheets.
2026-11-11 rules applied (dialogue-pilot README §4, §9, §10.6): the faster voice style for both characters,
`pauses: {line_ms: 0, scene_ms: 150}` and `still_motion: "beat"`, no `pause_after_ms` on lines except a
BEAT_MS beat on the line right before each `P:` payoff in the same scene, and only an upper bound on length.
Line caps here count punctuation (chief <= 25, kid <= 15), as in P01 and P20.
`script.md` is written by `node tools/video/cli.mjs script --slug sothatswhy-p26-plane-window` after this runs.
"""
import hashlib, itertools, json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "sothatswhy-p26-plane-window"
CHECKED = "2026-11-13"
BEAT_MS = 500   # 答案揭曉前的一拍（README §10.6）

# ---------- series constants (identical to P20, P04 and P01) ----------
VOICE = {"provider": "gemini", "name": "Sulafat",
         "style": "標準國語，咬字清楚，台北人平常說話的語調。事務所的所長，溫和、有耐心，像陪一個好奇的小朋友和你一起找答案。語速偏快、輕快，像節目主持人，一秒五個字以上，句與句緊接、不拖長尾音。"}
SHEET = "character reference: one single full-body figure standing in the centre, facing the viewer in a slight three-quarter turn, relaxed friendly pose, both hands clearly drawn, plain empty cream background with nothing else in the picture, no turnaround, no second view, no seal, no stamp, no signature, no text"
CHARACTERS = [
    {"id": "chief", "name": "所長",
     "appearance": "a friendly middle-aged woman, the chief of a small question office, with round black glasses, shoulder-length dark hair with a streak of grey tied in a low ponytail, a warm smile, a mustard-yellow cardigan over a white blouse, ink-navy trousers, brown shoes, a yellow pencil tucked behind one ear",
     "voice": dict(VOICE), "sheet_prompt": SHEET},
    {"id": "kid", "name": "小問",
     "appearance": "a curious eight-year-old girl with a short black bob haircut with straight bangs and one small cowlick sticking up on top, large round eyes, wearing a navy raincoat-style jacket with a mustard-yellow hood, white sneakers, both hands free",
     "voice": {"provider": "gemini", "name": "Leda", "style": "標準國語，咬字清楚，台北人平常說話的語調；八歲小女孩的聲音，好奇、活潑，問問題時句尾上揚，語速輕快，一秒五個字以上，不拖尾音"},
     "sheet_prompt": SHEET},
]

# Identity goes LAST in every prompt (P02: putting it first drifted some frames to photo or 3D).
KIDDESC = "the girl has a short black bob with straight bangs and one small cowlick on top and wears a navy raincoat jacket with a mustard-yellow hood"
WALL = "a plain pale wall behind her"
DAY = "bright daylight"
# Prompt words that P02/P05 taught us to keep out (README §3.1).
BANNED = re.compile(r"\b(no|not|without|text|blank|lamp|night|notebook|sign|signs|paper|poster|screen|book|calendar|whiteboard|thermometer|remote|label|magnet|microscope|arrow|arrows)\b", re.I)

CAMS = itertools.cycle(["push in", "pan left", "pull out", "drift", "tilt up", "pan right", "push in", "tilt down", "pull out", "drift"])
CAM_FILE = os.path.join(HERE, "cameras.json")
FROZEN = json.load(open(CAM_FILE, encoding="utf-8")) if os.path.exists(CAM_FILE) else {}

S = []
KIDFIX = set()
CHIEFFIX2 = set()  # every chief shot (P07/P14 round 5, P20): one uniform jet-black description
CHIEFFIX_DESC = "the chief is a slim young woman of about thirty with glossy jet-black hair tied in a low ponytail, round black glasses, a yellow pencil tucked behind her ear, a mustard-yellow cardigan over a white blouse, flat 2D cel-shaded cartoon drawing with ink outlines"
KIDFIX_TAIL = ', exactly matching her reference sheet: the same little girl every time, short black bob with straight bangs, navy raincoat with mustard-yellow hood, long navy trousers, hood folded down behind her neck, bare short black bob uncovered and hanging free, simple dot-like cartoon eyes as on the reference sheet, a round young child face with big round matching eyes looking the same way, flat 2D cel-shaded cartoon drawing with ink outlines'
EXTRA = {
}
REWRITE = {
    "kid-guess": "Waist-up medium shot of the girl in a bright cartoon office, raising one finger with a bright know-it-all grin, bright daylight, the girl is a flat 2D chibi cartoon girl of eight with jet-black hair cut in a short straight bob ending evenly at her jaw all the way round with blunt bangs and one small cowlick, simple dot-like cartoon eyes with matching even pupils, a closed navy raincoat jacket with a mustard-yellow hood resting down on her shoulders, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "old-jet": "Side view of the front half of an old-fashioned 1950s jet airliner body in plain unpainted silver metal, a rounded nose and a long row of small squarish windows, the wings out of the picture, parked on a sunny green airfield under a clear sky, soft morning light, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-got-it": "Waist-up medium shot of the girl in a bright cartoon office, holding up a small pair of round-tipped scissors with a big happy confident smile, bright daylight, the girl is a flat 2D chibi cartoon girl of eight with jet-black hair cut in a short straight bob ending evenly at her jaw all the way round with blunt bangs and one small cowlick, simple dot-like cartoon eyes with matching even pupils, a closed navy raincoat jacket with a mustard-yellow hood resting down on her shoulders, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-tube-q": "Waist-up medium shot of the girl in a bright cartoon office, looking down at the desk with a hopeful face and both hands together, bright daylight, the girl is a flat 2D chibi cartoon girl of eight with jet-black hair cut in a short straight bob ending evenly at her jaw all the way round with blunt bangs and one small cowlick, simple dot-like cartoon eyes with matching even pupils, a closed navy raincoat jacket with a mustard-yellow hood resting down on her shoulders, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-fast-q": "Head-and-shoulders close-up of the girl in a bright cartoon office, leaning forward with an eager curious face, bright daylight, the girl is a flat 2D chibi cartoon girl of eight with jet-black hair cut in a short straight bob ending evenly at her jaw all the way round with blunt bangs and one small cowlick, simple dot-like cartoon eyes with matching even pupils, a closed navy raincoat jacket with a mustard-yellow hood resting down on her shoulders, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-crowd-q": "Head-and-shoulders close-up of the girl in a bright cartoon office, frowning thoughtfully with one hand pressed to her cheek, bright daylight, the girl is a flat 2D chibi cartoon girl of eight with jet-black hair cut in a short straight bob ending evenly at her jaw all the way round with blunt bangs and one small cowlick, simple dot-like cartoon eyes with matching even pupils, a closed navy raincoat jacket with a mustard-yellow hood resting down on her shoulders, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "outro-wave": "Waist-up medium shot of the chief facing the viewer, waving goodbye with one open hand showing five fingers, a warm friendly smile, a plain pale cream wall behind, bright daylight. The chief is a slim young woman of about thirty drawn as a flat 2D chibi cartoon: glossy hair in one even jet-black colour tied in a short low ponytail at the nape, small bare earlobes, natural lips, round black glasses centred over even matching eyes, a yellow pencil tucked behind her ear, a mustard-yellow cardigan over a white collared blouse, navy trousers, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-real-q": "Waist-up medium shot of the girl in a bright cartoon office, looking up with wide serious eyes and both hands clasped in front of her, bright daylight, the girl is a flat 2D chibi cartoon girl of eight with jet-black hair cut in a short straight bob ending evenly at her jaw all the way round with blunt bangs and one small cowlick, simple dot-like cartoon eyes with matching even pupils, a closed navy raincoat jacket with a mustard-yellow hood resting down on her shoulders, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-where-q": "Head-and-shoulders close-up of the girl in a bright cartoon office, holding a flat rectangular sheet of cream card with a row of small sharp square window holes cut along it, one jagged tear running from the corner of one square hole to the edge of the sheet close to her face and studying its square windows with a frown, bright daylight, the girl is a flat 2D chibi cartoon girl of eight with jet-black hair cut in a short straight bob ending evenly at her jaw all the way round with blunt bangs and one small cowlick, simple dot-like cartoon eyes, a closed navy raincoat jacket with a mustard-yellow hood resting on her shoulders, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-sea-q": "Flat 2D cartoon illustration. Head-and-shoulders close-up of an 8-year-old chibi cartoon girl in a bright cartoon office, looking down with a quiet thinking face, eyes open, both hands resting on a smooth pure white toy airliner lying on the desk in front of her, bright daylight. Her jet-black hair is a short straight bob ending evenly at her jaw all the way round, with blunt straight bangs and one thin wispy cowlick strand on top; all of her hair hangs loose and the back of her neck shows. Simple dot eyes, navy raincoat jacket with a mustard-yellow hood lying flat behind her neck. The toy airliner is one clean white colour from nose to tail. simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-tank-q": "Close-up flat cartoon view of the silver side of an old airliner body filling the frame inside a bright hangar, calm blue water around its lower half, one small square window with four sharp pointed corners set in the riveted metal skin, a thin dark zigzag crack starting at the lower right sharp corner of that window and running out across the metal, smooth clean metal elsewhere, plain clean frame edges, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "chief-why-round": "Waist-up medium shot of the chief standing at the bank of a small cartoon stream, clear blue water flowing in smooth curving lines around a round grey stone sitting in the middle of the stream, she points at the stone with one finger and a warm smile, bright daylight, the chief is a slim young woman of about thirty drawn as a flat 2D chibi cartoon, glossy hair in one even jet-black colour tied in a low ponytail at the nape, small bare earlobes, natural lips, round black glasses centred over her eyes, a yellow pencil tucked behind her ear, a mustard-yellow cardigan over a white blouse, navy trousers, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "chief-fatigue": "Waist-up medium shot of the chief filling most of the frame, holding the two broken halves of a silver wire office clip in her open palm with a thoughtful face, a plain pale wall behind, bright daylight, the chief is a slim young woman of about thirty drawn as a flat 2D chibi cartoon, glossy hair in one even jet-black colour tied in a low ponytail at the nape, small bare earlobes, natural lips, round black glasses centred over her eyes, a yellow pencil tucked behind her ear, a mustard-yellow cardigan over a white blouse, navy trousers, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-round-q": "Waist-up medium shot of the girl in a bright cartoon office, holding up a strip of cream card with one small round hole in its middle and peering at the hole with a curious face, bright daylight, the girl is a flat 2D chibi cartoon girl of eight with jet-black hair cut in a short straight bob ending evenly at her jaw all the way round with blunt bangs and one small cowlick, simple dot-like cartoon eyes, a closed navy raincoat jacket with a mustard-yellow hood resting on her shoulders, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "square-corner": "Close-up of one corner of an airplane window shaped like a sharp square with a crisp pointed right-angle corner, set in a riveted silver metal wall, a few short bright blue lines crowding tightly at the pointed corner, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-main-q": "Waist-up medium shot of the girl in the exact centre of a bright cartoon office, holding a plain flat sheet of cream card low in front of her waist with both hands, looking at the viewer with a worried pleading face, bright daylight, the girl is a flat 2D chibi cartoon girl of eight with jet-black hair cut in a short straight bob ending evenly at her jaw all the way round with blunt bangs and one small cowlick, simple dot-like cartoon eyes with matching even pupils, a closed navy raincoat jacket with a mustard-yellow hood resting down on her shoulders, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "outro-chief": "Waist-up medium shot of a slim young woman of about thirty drawn as a flat 2D chibi cartoon, glossy hair in one even jet-black colour tied in a single low ponytail at the back of her neck, round black glasses, small bare earlobes, natural lips, a yellow pencil tucked behind one ear, a mustard-yellow cardigan over a white blouse and navy trousers, holding up one small plain all-white toy airliner in one hand with a neat row of small round-cornered windows, a curious smile, filling the frame, plain pale cream wall behind her, bright morning light, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "outro": "Flat 2D cartoon illustration of a chibi cartoon girl of about eight, jet-black short straight bob with blunt straight bangs, ending evenly at her jaw all the way round with the back of her neck showing, one thin wispy cowlick strand on top, simple dot eyes, navy raincoat jacket with a mustard-yellow hood folded down behind her neck, long navy trousers. Waist-up medium shot, a big happy smile, one hand giving a cheerful thumbs-up, plain warm cream background, bright morning light, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "chief-opinion": "Head-and-shoulders close-up of the chief smiling warmly with her hands loosely clasped, a small plain all-white toy airliner with rounded windows on the desk in front of her, a plain pale wall behind, bright daylight, the chief is a slim young woman of about thirty drawn as a flat 2D chibi cartoon, glossy hair in one even jet-black colour tied in a low ponytail at the nape, small bare earlobes, natural lips, round black glasses centred over her eyes, a yellow pencil tucked behind her ear, a mustard-yellow cardigan over a white blouse, navy trousers, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "chief-ask": "Head-and-shoulders close-up of the chief holding a small pair of round-tipped scissors and a flat sheet of cream card, raising her eyebrows with a playful asking smile, a plain pale wall behind, bright daylight, the chief is a slim young woman of about thirty drawn as a flat 2D chibi cartoon, glossy hair in one even jet-black colour tied in a low ponytail at the nape, small bare earlobes, natural lips, round black glasses centred over her eyes, a yellow pencil tucked behind her ear, a mustard-yellow cardigan over a white collared blouse, navy trousers, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "chief-rods": "Waist-up medium shot of a slim young woman of about thirty drawn as a flat 2D chibi cartoon, glossy hair in one even jet-black colour tied in a single low ponytail at the back of her neck, round black glasses, small bare earlobes, natural lips, a yellow pencil tucked behind one ear, a mustard-yellow cardigan over a white blouse. In one hand she holds up a short shiny orange-brown copper rod with a small V-shaped groove cut into its middle, in the other a short clear see-through glass rod with the same small V-shaped groove, a curious smile, plain pale cream wall behind her, bright daylight, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-fix-q": "Flat 2D cartoon illustration. Waist-up medium shot of the girl in a bright cartoon office, holding up a smooth pure white toy airliner, one clean white colour from nose to tail with a hopeful questioning face, bright daylight. The girl is an 8-year-old chibi cartoon girl with simple dot eyes, jet-black hair cut in a short straight bob ending evenly at her jaw all the way round with the back of her neck showing, blunt straight bangs and one tiny curl of cowlick on top, wearing a navy raincoat jacket with a mustard-yellow hood folded down behind her neck, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-why-round-q": "Flat 2D cartoon illustration. Head-and-shoulders close-up of the girl in a bright cartoon office, tapping one rounded window of a smooth pure white toy airliner, one clean white colour from nose to tail with one finger, with a puzzled frown, bright daylight. The girl is an 8-year-old chibi cartoon girl with simple dot eyes, jet-black hair cut in a short straight bob ending evenly at her jaw all the way round with the back of her neck showing, blunt straight bangs and one tiny curl of cowlick on top, wearing a navy raincoat jacket with a mustard-yellow hood folded down behind her neck, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-rivet-q": "Flat 2D cartoon illustration. Head-and-shoulders close-up of the girl in a bright cartoon office, squinting at a tiny silver rivet, a short metal pin with a round domed head, pinched between her thumb and index finger, bright daylight. The girl is an 8-year-old chibi cartoon girl with simple dot eyes, jet-black hair cut in a short straight bob ending evenly at her jaw all the way round with the back of her neck showing, blunt straight bangs and one tiny curl of cowlick on top, wearing a navy raincoat jacket with a mustard-yellow hood folded down behind her neck, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "chief-rivet": "Head-and-shoulders close-up of a woman holding up a tiny silver rivet, a short metal pin with a round domed head, pinched between her thumb and index finger, looking at it with a careful face, a plain pale wall behind her, bright daylight. The woman is a slim young woman of about thirty with glossy jet-black hair, one even black colour, combed back into a single low ponytail at the nape, round black glasses, a yellow pencil tucked behind one ear, small bare earlobes, natural pink lips, a mustard-yellow cardigan over a white collared blouse and navy trousers, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-blame": "Waist-up medium shot of the girl in a bright cartoon office, arms folded with a very sure frown, bright daylight, the girl is a flat 2D chibi cartoon girl of eight with jet-black hair cut in a short straight bob ending evenly at her jaw all the way round with blunt bangs and one small cowlick, simple dot-like cartoon eyes with matching even pupils, a closed navy raincoat jacket with a mustard-yellow hood resting down on her shoulders, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "chief-clip": "Head-and-shoulders close-up of the chief holding up one small silver wire office clip between two fingers, a knowing smile, a plain pale wall behind, bright daylight, the chief is a slim young woman of about thirty drawn as a flat 2D chibi cartoon, glossy hair in one even jet-black colour tied in a low ponytail at the nape, small bare earlobes, natural lips, round black glasses centred over her eyes, a yellow pencil tucked behind her ear, a mustard-yellow cardigan over a white collared blouse, navy trousers, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-same": "Waist-up medium shot of the girl in a bright cartoon office, pointing excitedly with one finger and a delighted surprised grin, bright daylight, the girl is a flat 2D chibi cartoon girl of eight with jet-black hair cut in a short straight bob ending evenly at her jaw all the way round with blunt bangs and one small cowlick, simple dot-like cartoon eyes with matching even pupils, a closed navy raincoat jacket with a mustard-yellow hood resting down on her shoulders, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "strips-pull": "Overhead close-up of one long cream card strip lying flat on a light wooden desk, a single small square hole cut in the middle of the strip, one clean dark jagged crack running from one sharp corner of the square hole straight out to the long edge of the strip, the two sides of the crack pulled slightly apart, two small hands holding the two ends of the strip, warm daylight, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-stress-q": "Head-and-shoulders close-up of the girl in a bright cartoon office, tilting her head with a curious face, bright daylight, the girl is a flat 2D chibi cartoon girl of eight with jet-black hair cut in a short straight bob ending evenly at her jaw all the way round with blunt bangs and one small cowlick, simple dot-like cartoon eyes with matching even pupils, a closed navy raincoat jacket with a mustard-yellow hood resting down on her shoulders, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "chief-stress": "Waist-up medium shot of the chief filling most of the frame, holding up a small square of silver metal sheet with a square hole in it and pointing at one sharp corner of the hole with a pencil, a focused face with matching even eyes, a plain pale wall behind, bright daylight, the chief is a slim young woman of about thirty drawn as a flat 2D chibi cartoon, glossy hair in one even jet-black colour tied in a low ponytail at the nape, small bare earlobes, natural lips, round black glasses centred over her eyes, a yellow pencil tucked behind her ear, a mustard-yellow cardigan over a white collared blouse, navy trousers, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "chief-hole": "Waist-up medium shot of the chief filling most of the frame, holding up a square of silver metal sheet with one round hole in its middle and pointing at the hole with one finger, a calm explaining smile, a plain pale wall behind, bright daylight, the chief is a slim young woman of about thirty drawn as a flat 2D chibi cartoon, glossy hair in one even jet-black colour tied in a low ponytail at the nape, small bare earlobes, natural lips, round black glasses centred over her eyes, a yellow pencil tucked behind her ear, a mustard-yellow cardigan over a white collared blouse, navy trousers, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-doors-q": "Head-and-shoulders close-up of the girl in a bright cartoon office, beside a big plain smooth all-white toy airliner on the desk, seen side-on so only the middle of its body fills the lower half of the frame, a row of small oval windows and one tall door outline with rounded corners, her index finger touching that door outline, a curious face, bright daylight, the girl is a flat 2D chibi cartoon girl of eight with loose jet-black hair cut in a short straight bob ending evenly at her jaw all the way round with blunt bangs and one thin curved hair strand standing up as a cowlick, simple dot-like cartoon eyes, a closed navy raincoat jacket with a mustard-yellow hood resting on her shoulders, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-every-q": "Waist-up medium shot of the girl in a bright cartoon office, holding a small plain all-white toy airliner up high in one hand as if it were flying, with a curious face, standing on the floor, bright daylight, the girl is an 8-year-old with a jet-black short straight chin-length bob hanging loose, blunt straight bangs and one small curl of cowlick on top, wearing a navy raincoat jacket with a mustard-yellow hood folded down behind her neck, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-pop": "Waist-up medium shot of the girl in a bright cartoon office, pressing both hands flat over her ears and squeezing her eyes shut as two curved lines with a wincing grin, a big round red balloon floating close beside her, bright daylight, the girl is an 8-year-old with a jet-black short straight chin-length bob hanging loose, blunt straight bangs and one small curl of cowlick on top, wearing a navy raincoat jacket with a mustard-yellow hood folded down behind her neck, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "cabin-aisle": "Wide shot inside a bright cartoon airliner cabin seen straight down the aisle, rows of soft blue seats, oval windows with smoothly rounded corners along both walls showing blue sky, smooth plain cream overhead bins and smooth plain cream ceiling panels, sunlight coming in, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "kid-guess-q": "Waist-up medium shot of the girl in a bright cartoon office, one finger on her chin and her head tilted with a puzzled face, bright daylight, the girl is a flat 2D chibi cartoon girl of eight with jet-black hair cut in a short straight bob ending evenly at her jaw all the way round with blunt bangs and one small cowlick, simple dot-like cartoon eyes with matching even pupils, a closed navy raincoat jacket with a mustard-yellow hood resting down on her shoulders, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
    "chief-strips": "Waist-up medium shot of a woman holding up two long strips of thin white card side by side at chest height, a playful mysterious smile. The strip in her right hand has one small square hole with sharp corners in its centre. The strip in her left hand has one small perfectly circular hole, like a coin-sized ring, in its centre. Plain pale wall, bright daylight. The woman is a slim young woman of about thirty with glossy jet-black hair, one even black colour, combed back into a single low ponytail at the nape, round black glasses, a yellow pencil tucked behind one ear, small bare earlobes, natural pink lips, a mustard-yellow cardigan over a white collared blouse and navy trousers, simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours",
}
def _shot(id, prompt, chars, lines, chapter):
    prompt = REWRITE.get(id, prompt + EXTRA.get(id, ""))
    assert not BANNED.search(prompt), (id, BANNED.search(prompt).group(0))
    assert id not in {s["id"] for s in S}, id
    assert len(prompt) <= 840, (id, len(prompt))  # MiniMax prompt budget (HANDOFF: about 840 characters)
    cam = FROZEN.get(id) or next(CAMS)
    S.append(dict(id=id, chapter=chapter, template="shot", data=dict(prompt=prompt, camera=cam, visual="still", characters=list(chars)), lines=list(lines)))
def kid(id, prompt, *lines, chapter=None):
    """The kid doing one simple thing, facing the camera, waist-up or head-and-shoulders."""
    KIDFIX.add(id)
    _shot(id, prompt.rstrip(". ") + ", " + KIDDESC + KIDFIX_TAIL, ["kid"], lines, chapter)
def chief(id, prompt, *lines, chapter=None):
    """The chief, always waist-up or head-and-shoulders, in front of a plain wall in daylight."""
    assert prompt.startswith(("Waist-up", "Head-and-shoulders")), id
    CHIEFFIX2.add(id)
    _shot(id, prompt.rstrip(". ") + ", " + CHIEFFIX_DESC, ["chief"], lines, chapter)
def scene(id, prompt, *lines, chapter=None):
    """No character: an object, a place or a mechanism drawn as a picture."""
    _shot(id, prompt, [], lines, chapter)
    S[-1]["data"]["nobody"] = True  # PR #2028: no person or face in an object-only shot
def k(t, e=None, tag=None): return ("kid", t, e, tag)
def c(t, e=None, tag=None): return ("chief", t, e, tag)

def C(action, close=False):
    return ("Head-and-shoulders close-up" if close else "Waist-up medium shot") + " of the chief " + action + ", " + WALL + ", " + DAY
def K(action, close=False, where=None):
    return ("Head-and-shoulders close-up" if close else "Waist-up medium shot") + " of the girl " + (where + " " if where else "") + action + ", " + DAY


# One drawing language for the whole episode (README §10.5: the image model cannot draw forces, stress, pressure,
# fields, diagrams, labels, arrows, counts or directions; plan visual rule: no generated stress-colour pictures
# pretending to be simulations). The main thread is ONE afternoon: 小問 flies to see her grandma tomorrow, so she
# built a little airliner body for fun from a rolled tube of thin white card with square windows cut in it, and it
# tore from a window corner. She brings it to the office and asks why real plane windows have round corners. The
# chief shows her two strips of card (square hole, round hole) to pull, a paperclip to bend, a balloon, and finally
# two notched rods (copper and glass, from the UNSW teaching page); she leaves planning to sit by the window.
# The one analogy carried from start to end is THE STREAM AROUND A STONE: water slides smoothly round a round
# stone but bunches up at the corners of a square block. The FAA lessons-learned page on the Comet describes the
# load in the skin in the same words ("the stress flows freely around the curved edges ... cannot smoothly flow
# around the abrupt corners"). Limits in claims.md C22. The paperclip is a demonstration of "many small pushes add
# up", with its limit said aloud (a plane's skin is pushed far less each flight, claims.md C12).
# No crash, wreckage, victims or real airline liveries anywhere; the Comet is an unpainted old silver jet on a
# sunny airfield and a fuselage in a water tank, both illustrations.
OFFICE = "in a bright cartoon office,"
STYLE = ", simple flat 2D cel-shaded cartoon drawing with clean ink outlines and flat colours"
TUBE = "a toy plane body rolled from thin white card with little square window holes"
SHEETK = "a flat rectangular sheet of cream card with a row of small sharp square window holes cut along it, one jagged tear running from the corner of one square hole to the edge of the sheet"
TUBET = TUBE + ", a short tear running from one window corner"
WINDOW = "an airliner cabin window seen from the seat beside it, a soft oval window with smoothly rounded corners set in a pale cream plastic wall, blue sky and white clouds outside"
STRIPS = "two long strips of thin white card, one with a small square hole cut in its middle and one with a small round hole cut in its middle"
CLIP = "a shiny silver metal paperclip"
PLANE = "a plain white cartoon airliner with a row of small rounded windows and plain unpainted tail"
ROUNDSTONE = "a clear shallow stream flowing around one smooth round grey stone, the water sliding round it in gentle even curves"
SQUAREBLOCK = "a clear shallow stream flowing around one square grey concrete block with sharp corners, the water bunching up into little white foamy swirls right at its two front corners"
COPPER = "a short copper rod with a small notch cut into its middle"
GLASS = "a short clear glass rod with a small notch cut into its middle"
OLDJET = "an old-fashioned 1950s jet airliner in plain unpainted silver metal with small squarish windows, its four engines hidden inside the thick wing roots right next to the body with only small round intakes showing and nothing hanging under the wings, parked on a sunny green airfield"
def obj(id, prompt, *lines, chapter=None):
    """An everyday-object frame with nobody in it, always in the flat cartoon style."""
    scene(id, prompt + STYLE + ", clean empty corners", *lines, chapter=chapter)

# ---------- 開場（系列片頭之後直接進場景，不做濃縮；結果都不先講）----------
obj("tube-tear", "Extreme close-up of one square window hole cut in a flat sheet of cream card, a jagged tear running diagonally out from one sharp corner of the square hole to the edge of the card, the card lying on a light wooden desk beside a small roll of clear sticky tape",
    k("所長！事務所有膠帶嗎？", "急著報案的語氣"),
    k("我做的飛機裂開了！", "委屈"), chapter="紙做的機身，從窗角裂開")
# Thumbnail shot (fixed before keyframes): the kid big and centred, the torn card plane in hand.
kid("kid-main-q", K("holding up " + TUBE + " in both hands at her chest, wide curious eyes on the viewer, in the exact centre of the picture", where=OFFICE),
    k("明天要坐飛機，我先做了一架。", "委屈"),
    k("你看，從窗戶的角裂開的。", "指給所長看", "S:tear"),
    c("有。先讓我看看。你剪的窗戶，是方方的？", "接住上一句"),
    k("對啊，跟我家的窗戶一樣。"))
obj("cabin-window", "Close-up of " + WINDOW,
    c("那你明天坐飛機，看看座位旁邊的窗戶。"),
    c("它的四個角，都是圓圓的。"))
chief("chief-strips", C("holding up " + STRIPS + " side by side with a playful mysterious smile"),
    c("我這裡有兩條硬紙，一條剪方洞，一條剪一樣寬的圓洞。", "賣關子"),
    c("兩條一起用力拉，你猜，哪一條先破？", "賣關子", "S:pull"))
obj("clip-desk", "Close-up of " + CLIP + " lying on a light wooden desk, catching a bright glint",
    c("還有這根迴紋針。彎一下，它沒事。"),
    c("那彎很多很多次呢？", "賣關子", "S:clip"))
obj("chief-outside", "View from inside an airliner cabin through one rounded window, far below a white sea of fluffy clouds, above a deep dark blue high sky",
    c("還有，飛機飛高以後，窗戶外面跟裡面，", "賣關子"),
    c("有一個很大的不同。", "賣關子", "S:outside"))
kid("kid-guess-q", K("holding a small plain white toy airliner up in front of her with a puzzled face", where=OFFICE),
    k("什麼不同？跟圓角有關嗎？", "句尾上揚"),
    c("有關。飛機的窗戶，為什麼要做成圓角？", "轉向觀眾", "S:main"))
kid("kid-guess", K("rubbing one finger along a rounded tabletop corner with a very confident grin", where=OFFICE),
    k("我知道！圓的才不會刮到手！", "篤定的錯猜", "S:scratch"))

# ---------- 第一章：明天的飛機，被空氣撐著 ----------
chief("chief-skin", C("smiling kindly and holding up one finger", close=True),
    c("不刮手是好事，可是答案在窗戶旁邊的機身。", "接住上一句", "P:scratch"),
    k("機身是什麼？", "句尾上揚"), chapter="明天的飛機，被空氣撐著")
obj("plane-side", "Wide side view of " + PLANE + " parked on a sunny airfield, its long smooth silver-white body shining",
    c("就是飛機那一整條長長的身體，外面多半包著金屬。"),
    k("它幹嘛要飛那麼高？", "句尾上揚"))
obj("plane-sky", "Wide shot of " + PLANE + " cruising high above a fluffy sea of white clouds under a deep blue sky",
    c("美國聯邦航空總署的飛行手冊說，", "接住上一句"),
    c("飛得高比較省油，還能飛在暴風雨上面。"))
kid("kid-air-q", K("looking up at the sky through a big office window with a curious face", where=OFFICE),
    k("那麼高，外面的空氣呢？", "句尾上揚"))
obj("chief-thin", "Wide shot of a tall snowy mountain peak rising above a white sea of clouds under a deep dark blue sky, thin wisps of cloud",
    c("很稀。手冊說，在大約八千五百公尺高，", "接住上一句"),
    c("空氣的壓力只剩地面的三分之一左右。", None, "P:outside"))
kid("kid-breathe", K("holding her breath with puffed cheeks and wide worried eyes", close=True, where=OFFICE),
    k("那我在飛機上，", "擔心"), k("會喘不過氣嗎？", "擔心"))
obj("chief-sealed", "Cutaway view of the inside of a simple cartoon airliner cabin with rows of empty blue seats, small round air vents in the ceiling softly blowing little curls of air",
    c("不會。客機的機艙是封起來的，"),
    c("裡面一直打進空氣，比外面多，這叫加壓。"))
obj("cabin-aisle", "Wide shot inside a bright cartoon airliner cabin, rows of soft blue seats, oval windows with rounded corners along both walls, sunlight coming in",
    c("通常讓機艙裡的空氣，"),
    c("像在大約兩千四百公尺的山上，人待著比較舒服。"))
kid("kid-push-q", K("pressing both palms together hard in front of her chest with a thinking frown", close=True, where=OFFICE),
    k("裡面空氣比外面多，", "想不通"), k("那會怎樣？", "句尾上揚", "S:push"))
chief("chief-balloon", C("holding up a round red balloon blown up big and tight"),
    c("你吹過氣球吧？裡面空氣多，氣球就被撐開。", "接住上一句"))
obj("balloon-big", "Close-up of a round red balloon blown up big and tight, its skin stretched shiny and smooth, tied with a short white string, floating over a light wooden desk",
    c("機艙也一樣：裡面的空氣，把機身往外推。", None, "P:push"),
    c("裡外推力的差，叫做壓差。"))
kid("kid-pop", K("covering her ears with both hands and squeezing her eyes shut as two happy curved lines, a big round red balloon floating beside her", where=OFFICE),
    k("氣球吹太多，會破掉！", "想起來"),
    c("對。所以飛很高時，機艙不會加到跟地面一樣。"))
obj("chief-limit", "Close-up of one round red balloon blown up big and tight on a light wooden desk, a thin dashed circle drawn just around it like a limit line",
    c("手冊說，機身設計時就定好，最多撐多大的壓差，"),
    c("加壓不能超過它。"))
kid("kid-every-q", K("holding the small plain white toy airliner up high as if it were flying, with a curious face", where=OFFICE),
    k("每次飛都會推嗎？", "句尾上揚", "S:every"))
obj("chief-cycle", "Close-up of two round red balloons side by side on a light wooden desk, the left one blown up big and round, the right one small and soft with its air let out",
    c("會。飛上去加壓，機身被撐一下；", "接住上一句"),
    c("落地前把壓放掉，又鬆回來。"),
    c("所以飛一趟，就是撐一下、再鬆一下。", None, "P:every"))
kid("kid-pane-q", K("pressing one fingertip against a window pane with a curious face", close=True, where=OFFICE),
    k("那窗戶也被推嗎？", "句尾上揚", "S:pane"))
chief("chief-doors", C("tracing a big rectangle in the air with one finger and a thoughtful face"),
    c("會。手冊還說，機身能撐多大的壓差，", "接住上一句"),
    c("看它多強，也常看窗戶和門這些地方。", None, "P:pane"))
kid("kid-doors-q", K("looking at the side of the toy airliner in her hands with a thinking face", close=True, where=OFFICE),
    k("窗戶跟門，有什麼特別？", "章尾停住，句尾上揚"))

# ---------- 第二章：拉一拉，方洞和圓洞 ----------
chief("chief-hole", C("making a round hole with her thumb and finger and looking through it with a playful smile", close=True),
    c("它們都是在機身上，開的一個洞。", "接住上一句"),
    c("機身被撐開時，外面那層金屬被拉得緊緊的。"), chapter="拉一拉，方洞和圓洞")
obj("hole-skin", "Close-up of the smooth silver-white metal side of an airliner around one rounded cabin window, neat rows of tiny rivets in the skin, bright daylight",
    c("洞那裡沒有金屬，機身裡的拉力只好繞過去。"),
    k("繞過去？怎麼繞？", "句尾上揚", "S:around"))
obj("stream-round", "Close-up from above of " + ROUNDSTONE + ", pebbles on the sunny stream bed",
    c("想像一條小溪，中間有一顆圓圓的石頭。"),
    c("水碰到它，順著圓邊，滑滑地流過去。"))
obj("stream-square", "Close-up from above of " + SQUAREBLOCK + ", pebbles on the sunny stream bed",
    c("換成一塊方方的水泥塊呢？"),
    k("水到了角那裡，擠成一團！", "驚訝"))
obj("chief-flow", "Close-up of one airplane window with smoothly rounded corners set in a silver metal wall, several smooth light blue lines flowing gently around its rounded corners",
    c("航空總署說，機身裡的力，也有點像這樣。"),
    c("圓角的窗戶，力順著彎彎的邊走，不太會堆起來。"),
    k("那方方的窗戶呢？", "追問"))
obj("square-corner", "Close-up of one corner of an old-fashioned squarish airplane window with a tight small-radius corner, set in a riveted silver metal wall",
    c("方窗戶的尖角，力轉得太急，就擠在角上。", "接住上一句", "P:around"))
kid("kid-crowd-q", K("squeezing her two fists together with a curious frown", close=True, where=OFFICE),
    k("擠在角上，會怎樣？", "句尾上揚", "S:crowd"))
chief("chief-stress", C("pressing one fingertip onto her other palm with a serious but kind face", close=True),
    c("角上那一小塊金屬，要承受的力比旁邊多很多。", "接住上一句"),
    c("工程師把這個叫做應力集中。", None, "P:crowd"))
kid("kid-stress-q", K("scrunching her nose with a puzzled face", close=True, where=OFFICE),
    k("應力是什麼？", "句尾上揚"),
    c("就是金屬裡面，每一小塊撐著的力。"))
kid("kid-round-q", K("holding up a strip of thin white card with a small round hole in it and peering through the hole", where=OFFICE),
    k("那圓洞就不會擠嗎？", "句尾上揚", "S:roundhole"))
obj("chief-three", "Close-up of a flat silver metal sheet lying on a light wooden desk with one round hole in its middle, three short bright blue lines bunched tightly at the left edge of the hole and three at the right edge, a single thin blue line far out near the corner of the sheet",
    c("也會。工程講義算過，一大片被拉的薄板開個圓洞，", "接住上一句"),
    c("洞邊應力最大的地方，大約是遠處的三倍。", None, "P:roundhole"))
kid("kid-sharp-q", K("pointing at the corner of a square card hole with a wide-eyed face", close=True, where=OFFICE),
    k("那尖尖的角呢？", "追問", "S:sharp"))
obj("chief-sharp", "Close-up of two small silver metal plates side by side on a light wooden desk, the left plate with a short crack ending in a soft rounded tip, the right plate with a crack ending in a very thin needle-sharp tip, a few short bright blue lines crowding tightly at the needle-sharp tip",
    c("更厲害。裂縫或角越尖，尖端的應力就越大。", None, "P:sharp"))
kid("kid-places-q", K("looking around the office with a curious face, one finger raised", where=OFFICE),
    k("只有窗戶會這樣嗎？", "句尾上揚", "S:places"),
    c("剛剛那份講義說，洞、轉角、溝槽、裂縫旁邊，", "接住上一句"),
    c("常常都會這樣。"))
obj("strips-pull", "Close-up of " + STRIPS + " held at both ends and pulled tight across a light wooden desk, the square-hole strip tearing in a short jagged line from one corner of its hole, the round-hole strip still whole",
    c("現在，來拉這兩條紙。"),
    k("方洞那條，從角裂開了！", "驚訝", "P:pull"))
kid("kid-same", K("holding up " + TUBET + " next to her face with a delighted surprised grin", where=OFFICE),
    k("跟我的飛機一樣！", "恍然"),
    c("對。還記得方水泥塊的角嗎？你剪的就是那種角。", None, "P:tear"))
kid("kid-metal-q", K("knocking on a shiny metal desk leg with her knuckles and a doubtful face", where=OFFICE),
    k("可是真的飛機是金屬，", "不服氣"), k("金屬也會被撐壞嗎？", "章尾停住，句尾上揚"))

# ---------- 第三章：迴紋針，彎了好多次 ----------
chief("chief-clip", C("holding up " + CLIP + " between two fingers with a knowing smile", close=True),
    c("一次不會。還記得這根迴紋針嗎？", "接住上一句"), chapter="迴紋針，彎了好多次")
obj("clip-bend", "Close-up of a straightened silver paperclip held between two fingertips and bent back and forth, a small bright kink at the bend, a light wooden desk below",
    c("把它扳過去，再扳回來，一次、兩次……"),
    k("彎好多次，就斷掉了！", "驚訝", "P:clip"))
chief("chief-fatigue", C("holding the two broken halves of a silver paperclip in her palm with a thoughtful face"),
    c("金屬被一次又一次地拉，就算每次都不大，"),
    c("最後也可能裂開。這叫做金屬疲勞。"))
kid("kid-tired", K("yawning with her arms stretched up, eyes closed as two happy curved lines", where=OFFICE),
    k("金屬也會累喔？", "好奇"),
    c("那是比喻。材料學的教材說，"))
obj("chief-steps", "Extreme close-up of a polished silver metal surface with one thin dark crack, the crack showing three small step-like marks along its length like tiny growth rings",
    c("裂縫常常先從表面冒出一點點，"),
    c("每拉一次，就往前長一點。"))
chief("chief-gentle", C("pinching a paperclip very gently between two fingers with a calm smile", close=True),
    c("機身每次被撐，不會像迴紋針那樣被扳彎。"),
    k("可是飛機要飛好多趟！", "想到了"),
    c("對。還記得嗎？飛一趟，就是撐一下、再鬆一下。"))
kid("kid-where-q", K("holding " + SHEETK + " close to her face and studying its little square windows with a frown", close=True, where=OFFICE),
    k("那裂縫會從哪裡開始？", "句尾上揚", "S:where"),
    c("你說呢？哪裡的力最擠？"))
obj("kid-corner", "Extreme close-up of one square window hole cut in a flat sheet of cream card, a jagged tear running diagonally out from one sharp corner of the square hole to the edge of the card, one small child's finger pointing right at the torn corner, light wooden desk",
    k("窗戶的角！", "篤定"),
    c("對。疲勞的裂縫，常從力最擠的地方長出來。", None, "P:where"))
kid("kid-grow-q", K("holding up one finger and moving it slowly forward with a worried face", close=True, where=OFFICE),
    k("小裂縫會一直長嗎？", "擔心", "S:grow"))
obj("chief-critical", "Close-up of two small silver metal plates side by side on a light wooden desk, the left plate with a very short thin crack, the right plate with a long crack that has suddenly run almost all the way across it",
    c("裂縫還短的時候，材料撐得住。", "接住上一句"),
    c("長到某個長度，它會突然很快地裂過去。", None, "P:grow"))
kid("kid-fast-q", K("holding up a strip of thin white card with a short tear in it and frowning at it", where=OFFICE),
    k("那什麼時候會快裂？", "追問"),
    c("要看裂縫多長，還有拉得多用力。"))
kid("kid-real-q", K("looking up with wide serious eyes and both hands holding " + SHEETK, where=OFFICE),
    k("真的有飛機這樣過嗎？", "小聲", "S:comet"))
obj("old-jet", "Wide side view of " + OLDJET + ", soft morning light",
    c("有。航空總署整理過一個例子，叫彗星號。", "接住上一句"),
    c("它是世界上第一種載客的加壓噴射客機。"))
obj("chief-comet", "Wide shot of an old 1950s silver jet airliner with smooth unmarked silver paint flying high over a calm blue sea under a clear sky, small squarish windows along its side",
    c("一九五四年，有兩架在飛行中出事，掉進海裡。"),
    c("調查的人，想找出機身是怎麼壞的。"))
obj("water-tank", "Wide shot of the long silver body of an old airliner sitting inside a giant open rectangular water tank in a big bright hangar, the tank filled with calm blue water up to the windows, two small cranes beside it",
    c("他們把另一架放進大水槽，往機艙裡灌水加壓，"),
    c("一次又一次，就像一趟又一趟的飛行。"))
obj("kid-tank-q", "Close-up of the side of an old silver airliner body inside a big bright hangar, one small squarish window with sharp corners set in the riveted metal skin, a thin dark crack running out from one sharp corner of that window across the metal, calm blue water line below",
    k("結果呢？", "追問"),
    c("加上它以前真的飛過的，一共三千多次，"),
    c("機身從一扇方方的逃生門窗戶的角裂開了。", None, "P:comet"))
kid("kid-sea-q", K("looking down with a quiet thinking face, both hands resting on the toy airliner", close=True, where=OFFICE),
    k("那掉進海裡的飛機呢？", "小聲"),
    c("其中一架，大部分的碎片從海裡撈了回來。", "接住上一句"))
obj("chief-adf", "Top-down view of a flat section of riveted silver metal roof panel, two small square panel windows set in it, a thin dark crack running out from one sharp corner of one small square window",
    c("最先裂的，是機頂放天線的方形小窗口。"),
    c("對撈回來的這一架，結論是：加壓機艙因金屬疲勞壞掉。"))
kid("kid-test-q", K("scratching her head with a puzzled frown", close=True, where=OFFICE),
    k("造飛機時，沒有先測嗎？", "不解"),
    c("有。做飛機的公司，拿一個機身，", "接住上一句"))
obj("chief-test", "Close-up of a thick grey water hose filling the inside of an old silver airliner body through an open hatch, inside a big bright hangar, calm blue water",
    c("測過一萬多次。可是它之前被加過兩倍的壓力，"),
    c("角上的金屬因此變了，測出來的次數太樂觀。"))
kid("kid-blame", K("folding her arms with a very sure frown", close=True, where=OFFICE),
    k("所以都是方窗害的！", "篤定的錯猜", "S:only"))
chief("chief-rivet", C("holding up a tiny shiny silver rivet between two fingers with a careful face", close=True),
    c("沒那麼簡單。後來一位英國學者研究，", "接住上一句"),
    c("裂縫都從開口旁邊的鉚釘孔、螺栓孔長出來。"))
kid("kid-rivet-q", K("squinting at a tiny shiny silver rivet held between her fingers", close=True, where=OFFICE),
    k("鉚釘是什麼？", "句尾上揚"),
    c("把兩片金屬釘在一起的小金屬釘。"),
    k("釘子的孔，也是洞耶！", "想起來"),
    c("對，還記得嗎？洞的旁邊，力也會擠。", None, "P:places"))
obj("chief-withey", "Close-up of one squarish airplane window set in a silver metal wall, a neat tight row of small round rivets running all around its frame",
    c("那位學者認為，窗戶怎麼固定，可能比形狀還要緊。"),
    c("形狀、孔和做法，是連在一起的。", None, "P:only"))
kid("kid-why-round-q", K("tapping the rounded window of the toy airliner with a puzzled frown", close=True, where=OFFICE),
    k("那幹嘛還要做圓角？", "章尾停住，句尾上揚"))

# ---------- 第四章：銅棒和玻璃棒，誰先斷 ----------
chief("chief-why-round", C("drawing a soft rounded corner in the air with one finger and a warm smile", close=True),
    c("還記得圓石頭旁邊的水嗎？角圓了，力也順多了，", "接住上一句"),
    c("裂縫就比較難冒出來。可是光靠形狀，還不夠。"), chapter="銅棒和玻璃棒，誰先斷")
kid("kid-material-q", K("holding up two small shiny rods, one copper-coloured and one clear, with a curious frown", where=OFFICE),
    k("那換一種不會裂的材料？", "句尾上揚", "S:material"))
chief("chief-rods", C("holding " + COPPER + " in one hand and " + GLASS + " in the other with a curious smile"),
    c("材料真的有差。有一份大學教材，比過兩根棒子：", "接住上一句"),
    c("一根銅棒，一根玻璃棒，都刻了一個小缺口。"))
obj("glass-rod", "Close-up of " + GLASS + " lying on a light wooden desk, broken cleanly into two pieces right at the notch",
    c("玻璃棒有了缺口，力小很多就斷了，"),
    c("裂口就從缺口那裡開始。"),
    k("玻璃好脆喔！", "驚訝"))
obj("copper-rod", "Close-up of " + COPPER + " lying on a light wooden desk, bent into a smooth gentle U-curve at the notch and still in one piece",
    c("銅棒有缺口，卻先彎下去，沒有比較容易斷。"),
    k("銅棒會彎，所以不怕缺口？", "恍然"))
obj("chief-energy", "Close-up of a copper rod bent into a smooth curve lying beside a glass rod snapped cleanly in two at a small V-shaped groove, both on a light wooden desk",
    c("拉一次是這樣：它斷之前會先變形，吸收很多力氣。", None, "P:material"),
    c("所以材料要挑；可是挑好了，還是可能疲勞。"))
kid("kid-fix-q", K("holding up the toy airliner with a hopeful questioning face", where=OFFICE),
    k("那彗星號後來怎麼改？", "句尾上揚", "S:fix"))
obj("chief-fix", "Close-up of one oval airplane window with a wide thick silver metal ring around it set in a smooth silver metal wall",
    c("那位學者寫到，後來窗戶周圍的金屬加厚了，"),
    c("新的型號，也換了窗戶的設計，少打鉚釘。"))
obj("oval-window", "Close-up of one oval airplane window with smoothly rounded ends set in a polished silver metal wall, a neat ring of small rivets around it, blue sky reflected in the glass",
    c("航空總署也提到，有一款改良型改成橢圓窗。", None, "P:fix"))
kid("kid-anyway-q", K("biting her lip with a worried face", close=True, where=OFFICE),
    k("要是還是有裂縫呢？", "擔心", "S:anyway"))
obj("chief-failsafe", "Close-up of a small square of silver metal sheet on a light wooden desk, a short thin crack running across it that stops right at a thick silver metal strip riveted across the sheet",
    c("現在的設計，會先想好萬一裂了怎麼辦。", "接住上一句"),
    c("像是讓力，有別條路可以走，"))
kid("kid-branch", K("drawing two branching lines in the air with one finger and an excited face", close=True, where=OFFICE),
    k("像小溪分成好幾條？", "聯想"),
    c("有點像。也要讓裂縫能停下來，或轉個方向。", None, "P:anyway"))
obj("inspector", "Wide shot of an aircraft mechanic in a plain navy overall standing on a low platform beside the silver-white side of an airliner in a bright hangar, shining a small flashlight closely on the smooth metal skin around a rounded cabin window",
    k("那誰知道有沒有裂縫？", "句尾上揚", "S:inspect"),
    c("美國的法規要求，造飛機的人要證明：", "接住上一句"))
chief("chief-rule", C("holding a thin plain grey folder open in both hands with a focused smile", close=True),
    c("在飛機能用的年限裡，不會因為疲勞出大事。"),
    c("連製造時的瑕疵，也要算進去。"))
chief("chief-check", C("holding up a small flashlight with a warm confident smile", close=True),
    c("還要訂好該做的檢查，讓維修的人照著做。", None, "P:inspect"),
    k("像定期去看牙醫！", "聯想"),
    c("有點像，只是檢查的是飛機的金屬。"))
obj("chief-your-window", "View from inside a modern airliner cabin of one window with smoothly rounded corners, a soft bright blue sky and a little white cloud outside",
    c("所以你看到的圓角窗，是很多設計裡的一個。", "轉向觀眾"))
kid("kid-tube-q", K("looking down at the desk with a hopeful face", where=OFFICE),
    k("那我的紙飛機呢？", "章尾停住，句尾上揚"))

# ---------- 收尾 ----------
chief("chief-ask", C("holding a small pair of round-tipped craft scissors and smiling encouragingly", close=True),
    c("你說呢？要怎麼剪？", "笑"), chapter="明天，靠窗坐")
kid("kid-got-it", K("holding up scissors with a big happy smile", where=OFFICE),
    k("原來如此！", "恍然大悟"), k("窗戶的角剪圓圓的，", "篤定"),
    k("就像剛剛那顆圓石頭旁的水！", "篤定", "P:main"),
    k("還記得嗎？真的飛機要定期檢查！", "篤定"))
chief("chief-opinion", C("smiling with her hands clasped, a thoughtful look", close=True),
    c("說得好。我覺得最妙的是：", "笑"),
    c("一個小小的圓角，背後是一整套設計和檢查。"))
# The outro is three pictures, no card, no stamp (series README §3.2, §10.1): the kid gives a thumbs-up.
kid("outro", "Waist-up medium shot of the girl with a big happy smile giving a big cheerful thumbs-up with one hand, bright morning light",
    k("明天我要坐窗邊，看圓圓的窗角！", "開心大聲"))
chief("outro-chief", "Waist-up medium shot of the chief holding up a small plain white toy airliner with a curious smile, filling the frame, a plain pale wall behind her, bright morning light",
      c("你坐飛機時，窗戶是什麼形狀？", "問句上揚，像聊天"), c("留言告訴我們。"))
chief("outro-wave", "Waist-up medium shot of the chief waving goodbye with a warm smile, a plain pale wall behind her, bright morning light",
      c("想一起找生活裡的為什麼，就訂閱原來如此事務所。", "誠懇"))

# ---------- assemble ----------
WHAT = {"tear": "小問的紙飛機為什麼從窗戶的角裂開", "pull": "方洞和圓洞的紙條一起拉，哪一條先破",
        "clip": "迴紋針彎很多很多次會怎樣", "outside": "飛機飛高以後，窗戶外面跟裡面有什麼不同",
        "main": "飛機的窗戶為什麼要做成圓角", "scratch": "圓角是不是為了不刮到手",
        "push": "機艙裡空氣比外面多會怎樣", "every": "每次飛都會把機身往外推嗎",
        "pane": "窗戶也會被推嗎", "around": "力怎麼繞過機身上的洞",
        "crowd": "力擠在角上會怎樣", "roundhole": "圓洞是不是就不會擠",
        "sharp": "尖尖的角會怎樣", "where": "裂縫會從哪裡開始",
        "grow": "小裂縫會不會一直長", "comet": "真的有飛機這樣過嗎",
        "only": "彗星號是不是都是方窗害的", "material": "材料有沒有差",
        "fix": "彗星號後來怎麼改", "anyway": "要是還是有裂縫怎麼辦",
        "inspect": "誰知道機身有沒有裂縫", "places": "只有窗戶會有應力集中嗎"}
# Latin terms the Mandarin voice must spell letter by letter (P13 GPS, P29 HTTPS/TLS). No line carries one:
# the FAA is said as 聯邦航空總署, the Comet as 彗星號, and no brand or airline is named.
SAY = []
scenes, loops_s, loops_p, n, beats = [], {}, {}, 0, 0
for sc in S:
    lines = []
    for sp, text, emo, tag in sc["lines"]:
        n += 1; lid = f"p{n:03d}"
        line = {"id": lid, "speaker": sp, "text": text}
        spoken = text
        for term, spell in SAY:
            spoken = spoken.replace(term, spell)
        if spoken != text:
            line["say"] = spoken
            line["say_for"] = hashlib.sha256(unicodedata.normalize("NFC", text).encode("utf-8")).hexdigest()[:12]
        assert not re.search(r"[A-Za-z]{2,}", spoken), (lid, "a Latin term needs a SAY entry (spelled letter by letter)")
        if emo: line["emotion"] = emo
        if tag and tag.startswith("P:") and lines:
            lines[-1]["pause_after_ms"] = BEAT_MS   # 同一景裡答案的前一句（README §10.6）
            beats += 1
        lines.append(line)
        if tag:
            kind, key = tag.split(":")
            (loops_s if kind == "S" else loops_p)[key] = lid
    out = {"id": sc["id"]}
    if sc["chapter"]: out["chapter"] = sc["chapter"]
    out["template"] = sc["template"]; out["data"] = dict(sc["data"]); out["lines"] = lines
    scenes.append(out)
assert set(loops_s) == set(loops_p) == set(WHAT), set(loops_s) ^ set(loops_p) ^ set(WHAT)
assert all(loops_s[key] < loops_p[key] for key in WHAT), [key for key in WHAT if loops_s[key] >= loops_p[key]]
loops = [{"setup": loops_s[key], "payoff": loops_p[key], "what": WHAT[key]} for key in sorted(WHAT, key=lambda key: loops_s[key])]


doc = {
    "schema_version": 1, "slug": SLUG, "format": "drama", "category": "explainer", "narration_locale": "zh-TW",
    "target_minutes": [8, 10], "voice": VOICE, "subtitles": {"burn_in": False}, "theme": "paper", "look": {"preset": "cute-cartoon"},
    # The series tag: the approved character sheets live in the series store and every episode reuses them (docs/videos/SERIES.md).
    "series": {"slug": "sothatswhy", "episode": 26, "chapter": 1},
    # 2026-11-11 (README §9 停頓, §10.6): no fixed pause between lines, a short gap between scenes, beat-timed stills.
    "pauses": {"line_ms": 0, "scene_ms": 150},
    "still_motion": "beat",
    # The series bed from P15 on (explainer-series/README.md, PR #2048): sothatswhy-bed-r2.m4a, remade from P02's paid take.
    "music": {"track": "sothatswhy-bed-r2.m4a", "sha256": "9bb4ba6fd16feb4a7f352144b2d89e9648acbbbbaa2173c27a7eefbdb70f28c6", "gain_db": -20, "duck_db": -10},
    "characters": CHARACTERS, "loops": loops,
    "youtube": {
        "category_id": 27, "made_for_kids": False, "default_language": "zh-TW",
        "title": "飛機窗戶的圓角，怎麼改變機身受力？｜原來如此事務所",
        "description": "小問明天要坐飛機，先用硬紙捲了一架小飛機，剪了一排方方的窗戶，結果紙從窗戶的角裂開了，她帶著它跑來事務所。真的飛機窗戶，為什麼四個角都是圓的？\n\n"
                       "這一集，所長先帶小問看飛機飛高以後發生什麼事：外面的空氣很稀，機艙加壓，裡面的空氣每一趟都把機身往外撐一下、落地前再鬆回來。"
                       "機身上開了窗戶，力只好繞過那個洞；所長用小溪繞過石頭來比：圓圓的邊，力順著走；方方的尖角，力就擠在角上，工程師叫它應力集中。"
                       "一次又一次的拉，就算每次都不大，金屬也可能從最擠的地方冒出小裂縫，慢慢長大，這叫金屬疲勞。"
                       "美國聯邦航空總署整理的彗星號例子裡，調查對厄爾巴島外海那一架的結論，是加壓機艙因為金屬疲勞而壞掉；後來的學者也指出，裂縫是從開口旁邊的鉚釘孔、螺栓孔長出來的，窗戶怎麼固定也很要緊，不能只怪窗角。"
                       "所以圓角只是其中一個：材料、厚度、怎麼做、萬一有裂縫怎麼擋住，還有定期檢查，都要一起顧到。\n\n"
                       "片中的飛機、窗戶、水槽和小溪都是 AI 生成的示意插圖，不是照片，也不是應力分析的結果。彗星號只引用調查與研究資料，沒有畫事故畫面。每個說法的出處列在下方參考資料。\n\n資料截至 " + CHECKED,
        "tags": ["飛機", "飛機窗戶", "圓角", "應力集中", "金屬疲勞", "加壓", "彗星號", "科普", "原來如此事務所"]},
    "thumbnail": {"template": "thumb", "data": {"headline": "飛機窗戶\n**為何圓角？**", "sub": "方角會讓力擠在一起", "shot": "kid-main-q", "subject": "right"}},
    "sources": [
        {"title": "FAA, Pilot's Handbook of Aeronautical Knowledge (FAA-H-8083-25), Chapter 7 Aircraft Systems: Pressurized Aircraft", "url": "https://www.faa.gov/sites/faa.gov/files/09_phak_ch7.pdf", "checked_on": CHECKED},
        {"title": "FAA Lessons Learned from Transport Airplane Accidents, de Havilland DH-106 Comet 1", "url": "https://www.faa.gov/lessons_learned/transport_airplane/accidents/G-ALYV", "checked_on": CHECKED},
        {"title": "M. E. Tuttle, University of Washington, Stress Concentrations (lecture notes)", "url": "https://courses.washington.edu/mengr556/StressConcentrations.pdf", "checked_on": CHECKED},
        {"title": "DoITPoMS, University of Cambridge, Brittle Fracture: Inglis and the crack tip stress idea", "url": "https://www.doitpoms.ac.uk/tlplib/brittle_fracture/crack_tip_stress.php", "checked_on": CHECKED},
        {"title": "UNSW Sydney School of Materials Science and Engineering, Crack theory: Introduction", "url": "https://www.unsw.edu.au/science/our-schools/materials/engage-with-us/high-school-students-and-teachers/online-tutorials/crack-theory/introduction", "checked_on": CHECKED},
        {"title": "UNSW Sydney, Fatigue failure", "url": "https://www.unsw.edu.au/science/our-schools/materials/engage-with-us/high-school-students-and-teachers/online-tutorials/crack-theory/fatigue-failure", "checked_on": CHECKED},
        {"title": "UNSW Sydney, Fracture mechanics", "url": "https://www.unsw.edu.au/science/our-schools/materials/engage-with-us/high-school-students-and-teachers/online-tutorials/crack-theory/fracture-mechanics", "checked_on": CHECKED},
        {"title": "UNSW Sydney, Fracture toughness", "url": "https://www.unsw.edu.au/science/our-schools/materials/engage-with-us/high-school-students-and-teachers/online-tutorials/crack-theory/fracture-mechanics/fracture-toughness", "checked_on": CHECKED},
        {"title": "UNSW Sydney, Brittle fracture (glass rod)", "url": "https://www.unsw.edu.au/science/our-schools/materials/engage-with-us/high-school-students-and-teachers/online-tutorials/crack-theory/introduction/brittle-facture", "checked_on": CHECKED},
        {"title": "UNSW Sydney, Ductile fracture (copper rod)", "url": "https://www.unsw.edu.au/science/our-schools/materials/engage-with-us/high-school-students-and-teachers/online-tutorials/crack-theory/introduction/ductile-fracture", "checked_on": CHECKED},
        {"title": "P. A. Withey, Fatigue failure of the de Havilland Comet I, Engineering Failure Analysis (1997)", "url": "https://ae.iitm.ac.in/~nidish/courses/as3020/files/mod2/dehavcomet.pdf", "checked_on": CHECKED},
        {"title": "P. A. Withey, The de Havilland Comet (RAeS Hamburg lecture, 2019-01-24)", "url": "https://www.fzt.haw-hamburg.de/pers/Scholz/dglr/hh/text_2019_01_24_Comet.pdf", "checked_on": CHECKED},
        {"title": "14 CFR 25.571 Damage-tolerance and fatigue evaluation of structure (eCFR)", "url": "https://www.ecfr.gov/current/title-14/section-25.571", "checked_on": CHECKED},
    ],
    "assets": [],
    "scenes": scenes,
}
json.dump(doc, open(os.path.join(HERE, "video.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
FROZEN.update({s["id"]: s["data"]["camera"] for s in scenes if s["template"] == "shot" and s["id"] not in FROZEN})
json.dump(FROZEN, open(CAM_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- self-checks (the series rules lint does not cover for a sothatswhy- slug) ----------
RATE = 4.4
def length(t): return sum(1 for ch in t if ch not in "，。、：；！？「」『』（）…—,.!?: ")
def han(t): return sum(1 for ch in t if "一" <= ch <= "鿿")
assert all(s["template"] == "shot" for s in scenes), "this series uses no cards"
assert not any("pause_after_ms" in l and l["pause_after_ms"] != BEAT_MS for s in scenes for l in s["lines"]), "lines carry no pause except the beat"
assert not any(re.search(r"grey streak|streak of grey|earring|lipstick", s["data"]["prompt"], re.I) for s in scenes), "the chief's hair is uniform jet-black (P20 lesson)"
outro_ids = {"outro", "outro-chief", "outro-wave"}
body = [s for s in scenes if s["id"] not in outro_ids]
chars = sum(length(l["text"]) for s in scenes for l in s["lines"])
body_chars = sum(length(l["text"]) for s in body for l in s["lines"])
body_han = sum(han(l["text"]) for s in body for l in s["lines"])
kidc = sum(length(l["text"]) for s in scenes for l in s["lines"] if l["speaker"] == "kid")
lines_all = [l for s in scenes for l in s["lines"]]
est = chars / RATE + 0.15 * (len(scenes) - 1) + BEAT_MS / 1000 * beats
per_shot = sorted(len(s["lines"]) for s in scenes)
shot_secs = sorted(sum(length(l["text"]) for l in s["lines"]) / RATE for s in scenes)
print(f"scenes {len(scenes)} shots {len(scenes)} lines {n} chars {chars} (body {body_chars}, body Han {body_han}) kid {kidc / chars:.0%} of chars, "
      f"{sum(l['speaker'] == 'kid' for l in lines_all) / n:.0%} of lines; est {est / 60:.1f} min at {RATE}/s "
      f"(+{len(scenes) - 1} scene gaps, {beats} beats, before the 11.9 s intro); loops {len(loops)}; "
      f"median lines a shot {per_shot[len(per_shot) // 2]}, median shot {shot_secs[len(shot_secs) // 2]:.1f} s", file=sys.stderr)
chap_t, chap = {}, None
for s in scenes:
    chap = s.get("chapter", chap)
    chap_t[chap] = chap_t.get(chap, 0) + sum(length(l["text"]) for l in s["lines"]) / RATE + 0.15
for ch, secs in chap_t.items(): print(f"  chapter {ch}: {secs:.0f} s", file=sys.stderr)
for s in scenes:
    secs = sum(length(l["text"]) for l in s["lines"]) / RATE
    if secs > 12: print(f"  shot over 12 s: {s['id']} {secs:.1f}", file=sys.stderr)
# Line caps count punctuation (P01 brief: chief <= 25, kid <= 15 characters, punctuation counted).
long_lines = [l for l in lines_all if len(l["text"]) > (15 if l["speaker"] == "kid" else 25)]
for l in long_lines: print(f"  long {l['speaker']} line {l['id']} ({len(l['text'])}): {l['text']}", file=sys.stderr)
assert not long_lines, "a line over its cap (punctuation counted)"
# a hook (a question, or a loop being planted) at least every 45 s
hooks, t, last, setups, gaps = [], 0.0, 0.0, set(loops_s.values()), []
for s in body:
    for l in s["lines"]:
        t += length(l["text"]) / RATE
        if l["text"].endswith("？") or l["id"] in setups:
            if t - last > 45: gaps.append(f"{t - last:.0f} s before {l['id']}")
            last = t
for g in gaps: print(f"  hook gap {g}", file=sys.stderr)
assert not gaps, "a stretch longer than 45 s without a question or a planted loop"
assert len(loops) >= 11, "the plan asks for at least 11 loops, every one paid off"
assert body_chars <= 3000, f"body {body_chars} characters: keep under 3,000"
assert all(s["data"]["camera"] for s in scenes)
cams = [s["data"]["camera"] for s in scenes]
assert all(not (a == b == c_) for a, b, c_ in zip(cams, cams[1:], cams[2:])), "three shots in a row with the same camera"
