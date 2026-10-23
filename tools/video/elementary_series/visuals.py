"""Elementary seasons two to six: original artwork plus readable English cards.

The earlier season's renderer is imported without mutation. A quiz's unrevealed
picture depends on its options and the common prompt, never the target, example,
teacher instruction, guided-reading flag or story speaker. All English is burned
into the picture, with the bottom 90 pixels reserved for optional translated CC.
"""
from __future__ import annotations

from PIL import Image

from elementary import visuals as classroom
from elementary.objects import NEW_VISUALS as LEGACY_NEW_VISUALS
from elementary.shared import preschool_visuals as shared
from elementary_series.objects import VALID_VISUALS, draw_object, parse_token, text_layout

WIDTH, HEIGHT, SCALE = shared.WIDTH, shared.HEIGHT, shared.SCALE
Pen, INK, TEAL = shared.Pen, classroom.INK, classroom.TEAL


def _choice_art(p, value, x, y, width, t, action_elapsed=None):
    kind, _ = parse_token(value)
    if kind == "legacy":
        classroom._choice_art(p, value, x, y, width, t, action_elapsed)
    else:
        draw_object(p, value, x, y, width-24, t)


def _draw_choices(p, choices, target, t, revealed=False, action_elapsed=None):
    values = [shared._choice_value(item) for item in choices]
    if not 2 <= len(values) <= 4:
        raise ValueError("Elementary choice scenes require two to four options")
    if len(set(values)) != len(values):
        raise ValueError("Elementary choices must be distinct")
    left, right, gap = 86, 1194, 22
    card_width = (right-left-gap*(len(values)-1))/len(values)
    for index, value in enumerate(values):
        left_edge = left+index*(card_width+gap)
        center = left_edge+card_width/2
        selected = revealed and value == target
        p.rect((left_edge,168,left_edge+card_width,469), "#E0DCCB", 24)
        p.rect((left_edge,162,left_edge+card_width,460), "#FFF3CE" if selected else "#FFFDF7",
               24,"#D2A64C" if selected else "#D7E1D2",3 if selected else 1.5)
        _choice_art(p,value,center,307,card_width,t,action_elapsed if selected else None)
        if selected:
            p.ellipse((center-17,145,center+17,179),TEAL)
            p.line([(center-8,162),(center-2,168),(center+9,156)],"#FFFFFF",3)


def english_strip_layout(text):
    """Place actual glyph bounds with a gap, leaving y=599 onward for dots.

    Font size is not the ink height and Pillow's middle anchor is not the ink
    center. Measuring the glyph boxes prevents a lower line or reading-aid
    rectangle from covering the descenders on the line above it.
    """
    lines = text_layout(text, 1110, 46, 26, 3)
    if len(lines) == 3:
        lines = text_layout(text,1110,28,26,3)
    if len(lines) == 1:
        return [(lines[0][0],lines[0][1],549)]
    bounds = [shared._font(size,True).getbbox(line,anchor="mm") for line,size in lines]
    heights = [(box[3]-box[1])/SCALE for box in bounds]
    top = 545-(sum(heights)+9*(len(lines)-1))/2
    positions = []
    for (line,size),box,height in zip(lines,bounds,heights):
        positions.append((line,size,top-box[1]/SCALE))
        top += height+9
    return positions


def _english_strip(p, text, guided=False):
    positioned = english_strip_layout(text)
    if guided:
        # All backgrounds precede all glyphs. Even if font metrics change,
        # drawing a later aid must never erase text already on the picture.
        for line,size,y in positioned:
            font = shared._font(size,True)
            box = font.getbbox(line,anchor="mm")
            left = 640-font.getlength(line)/(2*SCALE)
            offset = 0
            for word in line.split(" "):
                x = left+font.getlength(line[:offset])/SCALE
                width = font.getlength(word)/SCALE
                p.rect((x-3,y+box[1]/SCALE-3,x+width+3,y+box[3]/SCALE+3),"#F1F4E7",6)
                offset += len(word)+1
    for line,size,y in positioned:
        p.text((640,y),line,size,INK,True)


def _single_art(p, visual, t, scene, reveal_at, demo_start, scene_duration):
    kind, value = parse_token(visual)
    if kind in {"word","sentence"}:
        # The teaching sentence occupies a wide board, so it remains readable
        # even for a complete example. Both characters have quiet motion.
        shared._bear(p,155,461,.60,"neutral",t)
        shared._bird(p,1141,325,.52,t,-1)
        p.rect((275,176,1070,457),"#FFFDF5",20,"#D2DED0",2)
        draw_object(p,visual,672,314,730,t)
    elif kind != "legacy":
        shared._bear(p,243,460,.84,"neutral",t)
        shared._bird(p,1116,292,.55,t,-1)
        draw_object(p,visual,752,313,385,t)
    elif visual in LEGACY_NEW_VISUALS:
        if visual in {"sunny","pip"}:
            draw_object(p,visual,652,331,360,t)
        else:
            shared._bear(p,260,460,.87,"neutral",t)
            shared._bird(p,1048,279,.66,t,-1)
            draw_object(p,visual,738,313,350,t)
    elif visual in shared.COLORS:
        shared._bear(p,282,460,.92,"wave",t)
        shared._bird(p,1058,299,.62,t,-1)
        shared._ball(p,758,314,118,shared.COLORS[visual],t)
    elif visual in shared.COUNT_VALUES:
        shared._bear(p,234,460,.83,"neutral",t)
        shared._bird(p,1114,255,.47,t,-1)
        shared._count(p,visual,788,318,595,t,scene.get("layout","row"))
    elif visual in {"stand","sit","clap","happy","sad"}:
        action_start = reveal_at if scene.get("mode") == "quiz" else demo_start
        amount = shared._movement(visual,t-action_start) if visual in {"stand","sit"} else None
        shared._bear(p,570,463,1.08,visual,t,sit_amount=amount)
        shared._bird(p,875,333,.96,t,-1)
    elif visual in {"hello","goodbye","wave"}:
        shared._bear(p,491,463,1.08,visual,t)
        drift = min(t/max(1,scene_duration),1)*76 if visual == "goodbye" else 0
        shared._bird(p,844+drift,322-.2*drift,1.02,t,1 if visual == "goodbye" else -1)
    else:
        shared._bear(p,256,460,.88,"neutral",t)
        shared._bird(p,1080,282,.55,t,-1)
        draw_object(p,visual,770,308,405,t)


def render_frame(episode: dict, scene: dict, t: float, scene_duration: float = 20) -> Image.Image:
    """Render one 1280×720 RGB frame, raising on unsupported artwork/text."""
    t = max(0.0,float(t))
    mode = str(scene.get("mode","demo"))
    visual = str(scene.get("visual",scene.get("target","hello")))
    target = str(scene.get("target",visual))
    choices = scene.get("choices") or []
    for token in [visual,target,*[shared._choice_value(item) for item in choices]]:
        parse_token(token)
    if mode == "quiz" and choices and target not in [shared._choice_value(item) for item in choices]:
        raise ValueError("A quiz target must be one of its options")
    reveal_at = float(scene.get("reveal_at",12))
    demo_start = float(scene.get("demo_start",5))
    revealed = mode != "quiz" or t >= reveal_at
    image = classroom._background().copy()
    p = Pen(image)
    title = f"{int(episode.get('number',1)):02d}  /  {episode.get('title_en','English Club')}"
    p.text((1210,61),title,classroom._fit_text(title,744,19,13),INK,False,"rm")
    guided = bool(scene.get("guided_reading")) and revealed and t >= demo_start
    badge = "READ TOGETHER" if guided else {
        "demo":"LISTEN & LEARN","repeat":"YOUR TURN",
        "review":"LET'S REMEMBER","quiz":"LISTEN & CHOOSE",
    }.get(mode,"LET'S LEARN")
    p.text((74,130),badge,14,"#658978",True,"lm")
    if choices:
        _draw_choices(p,choices,target,t,revealed=mode == "quiz" and revealed,
                      action_elapsed=t-reveal_at)
    elif mode == "quiz" and not revealed:
        shared._bear(p,492,464,1.04,"neutral",t)
        shared._bird(p,824,335,1.02,t,-1)
    else:
        _single_art(p,visual,t,scene,reveal_at,demo_start,scene_duration)
    if mode != "quiz" and scene.get("story_speaker"):
        classroom._speech_pointer(p,str(scene["story_speaker"]))
    # Handle quiz first: even the instruction period must not print a target
    # from a localized lesson or an answer-bearing author instruction.
    if mode == "quiz":
        text = str(scene.get("demo",scene.get("english","Well done!"))) if revealed else "Listen and choose."
    elif t < demo_start and scene.get("instruction",{}).get("en"):
        text = str(scene["instruction"]["en"])
    else:
        text = str(scene.get("english",scene.get("demo","Hello!")))
    _english_strip(p,text,guided=guided)
    if mode == "repeat" or (mode == "quiz" and not revealed):
        phase = int(t*.65)%3
        for index in range(3):
            center = 625+index*15
            p.ellipse((center-3,599,center+3,605),TEAL if phase == index else "#D8E5D3")
    else:
        p.line([(602,602),(678,602)],"#E4CB8F",3)
    return image.resize((WIDTH,HEIGHT),Image.Resampling.LANCZOS)
