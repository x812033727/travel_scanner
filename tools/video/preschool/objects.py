"""Original, cached vector props for the complete Sunny & Pip preschool series.

All coordinates are a 320 by 280 drawing board. Objects are drawn without labels,
so a child can answer a listening question from the picture itself. Unknown visual
identifiers raise ValueError instead of silently showing an unrelated character.
"""
from __future__ import annotations

import math
from functools import lru_cache

from PIL import Image, ImageDraw

INK = "#3F514B"
LINE = "#9D7959"
CREAM = "#F9DDB0"
TEAL = "#5B9E8C"
BLUE = "#73ADE0"
RED = "#EA776D"
YELLOW = "#F4CE64"
GREEN = "#9BCDAB"
WHITE = "#FFFDF7"
BODY_PARTS = frozenset("eyes ears nose mouth hands feet head shoulders".split())
NEW_VISUALS = frozenset((
    "please thank_you yes no big small up down in out on under open close "
    "eyes ears nose mouth hands feet head shoulders wash_hands dry_hands "
    "brush_teeth wash_face wake_up sleep hungry thirsty eat drink hot cold "
    "coat_on coat_off mom dad cat dog bird fish rabbit turtle cow sheep apple banana "
    "carrot tomato bread milk sun rain wind snow tree flower car bus "
    "circle square triangle fast slow walk stop jump turn"
).split())
ANIMATED = frozenset((
    "please thank_you yes no wash_hands dry_hands brush_teeth wash_face "
    "wake_up sleep hungry thirsty eat drink hot cold coat_on coat_off "
    "rain wind snow fast slow walk stop jump turn"
).split())


class Board:
    def __init__(self, image):
        self.d = ImageDraw.Draw(image)
        self.scale = image.width / 320

    def xy(self, value):
        return tuple(round(a * self.scale) for a in value)

    def ellipse(self, box, color, outline=None, width=2):
        self.d.ellipse(self.xy(box), color, outline, max(1, round(width * self.scale)))

    def rect(self, box, color, radius=0, outline=None, width=2):
        self.d.rounded_rectangle(self.xy(box), round(radius*self.scale), color, outline,
                                 max(1, round(width*self.scale)))

    def line(self, points, color=INK, width=2):
        self.d.line([self.xy(pt) for pt in points], color, max(1, round(width*self.scale)), joint="curve")

    def polygon(self, points, color, outline=None, width=2):
        self.d.polygon([self.xy(pt) for pt in points], color)
        if outline:
            self.line(points + [points[0]], outline, width)

    def arc(self, box, start, end, color=INK, width=2):
        self.d.arc(self.xy(box), start, end, color, max(1, round(width*self.scale)))


def shadow(p, x=160, y=242, w=90):
    p.ellipse((x-w, y-8, x+w, y+8), "#DCE5D1")


def ball(p, x, y, r=34):
    p.ellipse((x-r,y-r,x+r,y+r), RED, "#D46D65", 2)
    p.arc((x-r*.76,y-r*.77,x+r*.70,y+r*.73), 26, 150, WHITE, 3)
    p.ellipse((x-r*.51,y-r*.51,x-r*.17,y-r*.26), "#FFE5DB")


def arrow(p, start, end, color=TEAL, width=5):
    x1,y1 = start
    x2,y2 = end
    p.line([start,end], color, width)
    angle = math.atan2(y2-y1,x2-x1)
    p.polygon([(x2,y2),(x2-13*math.cos(angle-.55),y2-13*math.sin(angle-.55)),
               (x2-13*math.cos(angle+.55),y2-13*math.sin(angle+.55))], color)


def eyes(p, x, y, spacing=25, closed=False):
    for side in [-1,1]:
        ex=x+side*spacing
        if closed:
            p.arc((ex-7,y-5,ex+7,y+7), 10,170,INK,2.5)
        else:
            p.ellipse((ex-3,y-5,ex+3,y+4),INK)


def paw(p, x, y, r=13):
    p.ellipse((x-r,y-r,x+r,y+r),CREAM,LINE,1.6)
    for dx in [-5,0,5]:
        p.line([(x+dx,y-r+2),(x+dx,y-r+7)],"#C99776",1)


def arm(p, start, end):
    p.line([start,end],LINE,19)
    p.line([start,end],CREAM,15)
    paw(p,*end,10)


def bear(p, x=160, ground=244, scale=1, *, head_dx=0, head_dy=0,
         eyes_closed=False, arms="down", body_part=None, coat=False, back=False, shirt=TEAL):
    """A compact Sunny with the same cream fur, peach ears and teal pullover."""
    # Draw into a coordinate adapter so every body part and highlight transforms together.
    q = Transform(p,x,ground,scale)
    shadow(q,0,0,61)
    q.ellipse((-44,-48,-6,0),CREAM,LINE)
    q.ellipse((6,-48,44,0),CREAM,LINE)
    q.ellipse((-53,-123,53,-22),shirt,"#518876")
    q.rect((-39,-96,39,-25),shirt,8)
    q.line([(-33,-31),(33,-31)],"#A3C9B5",3)
    if not back:
        q.rect((-13,-74,13,-53),"#B5D6BD",4)
    if arms=="up":
        arm(q,(-44,-104),(-75,-148)); arm(q,(44,-104),(75,-148))
    elif arms=="front":
        arm(q,(-44,-104),(-20,-76)); arm(q,(44,-104),(20,-76))
    elif arms=="wide":
        arm(q,(-44,-104),(-81,-106)); arm(q,(44,-104),(81,-106))
    else:
        arm(q,(-44,-104),(-66,-65)); arm(q,(44,-104),(66,-65))
    if coat:
        q.polygon([(-42,-118),(-68,-92),(-57,-74),(-42,-88),(-42,-31),
                   (42,-31),(42,-88),(57,-74),(68,-92),(42,-118)],"#E4B451",LINE)
        q.line([(0,-116),(0,-32)],WHITE,3)
        for y in [-96,-77,-58]: q.ellipse((6,y-2,10,y+2),LINE)
    h=Transform(q,head_dx,head_dy,1)
    h.ellipse((-68,-216,-23,-170),CREAM,LINE)
    h.ellipse((23,-216,68,-170),CREAM,LINE)
    h.ellipse((-59,-207,-33,-181),"#EABB94")
    h.ellipse((33,-207,59,-181),"#EABB94")
    h.ellipse((-67,-200,67,-91),CREAM,LINE)
    if not back:
        h.ellipse((-39,-149,39,-99),"#FFF2D7")
        eyes(h,0,-156,25,eyes_closed)
        h.ellipse((-48,-143,-31,-132),"#EEB99B")
        h.ellipse((31,-143,48,-132),"#EEB99B")
        h.ellipse((-7,-139,7,-131),INK)
        h.line([(0,-132),(0,-124)],INK,1.5)
        h.arc((-18,-135,18,-111),20,160,INK,2)
    regions={"eyes":[(-38,-171,38,-145)],"ears":[(-74,-222,-19,-169),(19,-222,74,-169)],
             "nose":[(-17,-147,17,-121)],"mouth":[(-28,-135,28,-104)],
             "hands":[(-80,-79,-52,-51),(52,-79,80,-51)],
             "feet":[(-50,-27,-1,8),(1,-27,50,8)],"head":[(-77,-226,77,-83)],
             "shoulders":[(-61,-121,-29,-91),(29,-121,61,-91)]}
    for box in regions.get(body_part,[]):
        q.ellipse(box,None,"#D09C38",4)


class Transform:
    def __init__(self,p,x,y,s): self.p,self.x,self.y,self.s=p,x,y,s
    def point(self,pt): return (self.x+pt[0]*self.s,self.y+pt[1]*self.s)
    def box(self,b): return self.point(b[:2])+self.point(b[2:])
    def ellipse(self,b,c,outline=None,width=2): self.p.ellipse(self.box(b),c,outline,width*self.s)
    def rect(self,b,c,radius=0,outline=None,width=2): self.p.rect(self.box(b),c,radius*self.s,outline,width*self.s)
    def line(self,pts,color=INK,width=2): self.p.line([self.point(pt) for pt in pts],color,width*self.s)
    def polygon(self,pts,color,outline=None,width=2): self.p.polygon([self.point(pt) for pt in pts],color,outline,width*self.s)
    def arc(self,b,start,end,color=INK,width=2): self.p.arc(self.box(b),start,end,color,width*self.s)


def gift(p,x,y,size=48):
    p.rect((x-size/2,y-size/2,x+size/2,y+size/2),"#DA9AB1",4,"#B97693")
    p.rect((x-size/2-3,y-size/2-5,x+size/2+3,y-size/2+6),"#E9B1C4",3,"#B97693")
    p.rect((x-4,y-size/2-5,x+4,y+size/2),YELLOW)
    p.ellipse((x-20,y-size/2-19,x,y-size/2-3),None,"#D5A842",4)
    p.ellipse((x,y-size/2-19,x+20,y-size/2-3),None,"#D5A842",4)


def cup(p,x,y,size=1,full=True):
    q=Transform(p,x,y,size)
    q.arc((20,-27,44,8),265,95,LINE,7)
    q.polygon([(-24,-32),(26,-32),(21,30),(-19,30)],"#C9E2E7",LINE)
    if full:q.polygon([(-18,-8),(20,-8),(17,25),(-15,25)],"#7DBBD1")
    q.ellipse((-24,-39,26,-25),"#ECF8F9",LINE)
    if full:q.ellipse((-18,-35,20,-28),"#94CCD8")


def box_prop(p,x=160,y=177):
    p.polygon([(x-64,y-35),(x+29,y-35),(x+64,y-9),(x-29,y-9)],"#E7CF9F",LINE)
    p.polygon([(x-64,y-35),(x-29,y-9),(x-29,y+53),(x-64,y+25)],"#D1AE79",LINE)
    p.rect((x-29,y-9,x+64,y+53),"#E1C48F",1,LINE)
    p.line([(x+5,y-8),(x+5,y+52)],"#CDA979",2)


def draw_relation(p,token):
    shadow(p)
    if token in {"big","small"}:
        # Identical ball, scale is the only semantic difference.
        ball(p,160,145,84 if token=="big" else 35)
    elif token in {"up","down"}:
        p.line([(68,234),(252,234)],"#BED1AF",3)
        ball(p,160,77 if token=="up" else 196,32)
        arrow(p,(232,184 if token=="up" else 67),(232,72 if token=="up" else 181))
    elif token in {"in","out"}:
        p.polygon([(83,156),(163,127),(224,160),(146,185)],"#AD906C",LINE)
        if token=="in":ball(p,152,159,30)
        p.polygon([(83,156),(146,185),(146,239),(83,207)],"#D1AE79",LINE)
        p.polygon([(146,185),(224,160),(224,214),(146,239)],"#E1C48F",LINE)
        if token=="out":ball(p,261,210,27)
    else:
        # A low table gives 'on' and 'under' one clear, unobstructed reference.
        p.rect((77,133,90,233),"#C8AC84",4,LINE)
        p.rect((230,133,243,233),"#C8AC84",4,LINE)
        p.rect((71,124,250,153),"#E1C48F",5,LINE)
        ball(p,163,94 if token=="on" else 198,29)


def draw_door(p,token):
    shadow(p,160,248,91)
    p.rect((73,38,251,247),"#E7D8B9",7,LINE)
    p.rect((87,49,237,244),"#ABC5B3",2,LINE)
    if token=="close":
        p.rect((91,53,233,241),"#DFB583",3,LINE)
        p.rect((110,73,213,141),"#EAC89E",4,LINE)
        p.rect((110,157,213,221),"#EAC89E",4,LINE)
        p.ellipse((208,143,220,155),YELLOW,LINE)
    else:
        p.polygon([(91,53),(173,83),(173,263),(91,241)],"#DFB583",LINE)
        p.polygon([(103,74),(161,95),(161,142),(103,130)],"#EAC89E",LINE)
        p.polygon([(103,148),(161,160),(161,236),(103,219)],"#EAC89E",LINE)
        p.ellipse((153,155,163,167),YELLOW,LINE)


def draw_social(p,token,t):
    if token in {"yes","no"}:
        bear(p,head_dx=11*math.sin(t*math.tau) if token=="no" else 0,
             head_dy=9*math.sin(t*math.tau) if token=="yes" else 0)
        if token=="yes":
            arrow(p,(264,82),(264,130),TEAL,4); arrow(p,(244,130),(244,82),TEAL,4)
        else:
            arrow(p,(118,17),(155,17),TEAL,4); arrow(p,(203,17),(166,17),TEAL,4)
    else:
        # The same gift and two open paws establish requesting and receiving.
        bear(p,84,245,.79,arms="front",head_dy=4*math.sin(t*math.tau) if token=="thank_you" else 0)
        gift_x=204 if token=="please" else 160
        gift(p,gift_x,159,50)
        arm(p,(307,189),(gift_x+28,171))
        arm(p,(84,170),(133 if token=="please" else gift_x-24,181))
        if token=="thank_you":
            # Small warm rays celebrate receiving; no icon is used as the answer.
            for dx,dy in [(-15,-42),(0,-49),(15,-42)]:
                p.line([(gift_x+dx,159+dy),(gift_x+dx*1.2,159+dy-7)],"#D1A043",2)


def drop(p,x,y,r=7,color=BLUE):
    p.polygon([(x,y-r*1.8),(x-r*.85,y),(x+r*.85,y)],color)
    p.ellipse((x-r,y-r*.2,x+r,y+r*1.8),color)


def snowflake(p,x,y,r=19):
    for a in range(0,360,60):
        dx,dy=math.cos(math.radians(a)),math.sin(math.radians(a))
        p.line([(x-dx*r,y-dy*r),(x+dx*r,y+dy*r)],"#8BAEBF",2.5)
        for turn in [-.7,.7]:
            a2=math.radians(a)+turn
            p.line([(x+dx*r*.65,y+dy*r*.65),
                    (x+dx*r*.65-math.cos(a2)*r*.30,y+dy*r*.65-math.sin(a2)*r*.30)],"#8BAEBF",2)


def sun(p,x,y,r=30):
    p.ellipse((x-r,y-r,x+r,y+r),YELLOW,"#D9B351",2)
    for a in range(0,360,45):
        dx,dy=math.cos(math.radians(a)),math.sin(math.radians(a))
        p.line([(x+dx*(r+8),y+dy*(r+8)),(x+dx*(r+20),y+dy*(r+20))],"#D9B351",3)


def bread(p,x,y,size=1):
    q=Transform(p,x,y,size)
    q.rect((-45,-25,45,48),"#D9A766",10,LINE)
    q.ellipse((-54,-55,54,19),"#D9A766",LINE)
    q.rect((-37,-23,37,40),"#FFF0C8",7)
    q.ellipse((-43,-43,43,9),"#FFF0C8")
    for px,py in [(-20,0),(19,-19),(10,26),(-14,20)]:q.ellipse((px-2,py-2,px+2,py+2),"#E4C98E")


def apple(p,x,y,size=1):
    q=Transform(p,x,y,size)
    q.line([(0,-39),(5,-62)],LINE,6)
    q.ellipse((3,-62,34,-43),"#86B783",LINE,1)
    q.ellipse((-52,-46,17,48),RED,"#C7665E",2)
    q.ellipse((-17,-46,52,48),RED,"#C7665E",2)
    q.ellipse((-39,-40,39,47),RED)
    q.arc((-39,-34,12,31),185,258,"#FFDECB",4)
    q.line([(-4,47),(4,47)],"#C7665E",2)


def hygiene(p,token,t):
    wave=math.sin(t*math.tau)
    if token in {"wash_hands","dry_hands"}:
        bear(p,146,248,.92,arms="front")
        p.rect((67,187,254,222),"#E4EAE0",12,"#A9BAB3")
        p.ellipse((75,171,245,209),"#F8FCF7","#A9BAB3")
        p.ellipse((90,180,230,202),"#C9E3E4")
        p.line([(238,175),(238,140),(214,140),(214,151)],"#95B2B3",9)
        if token=="wash_hands":
            for i in range(4):
                yy=154+(i*12+t*32)%37
                p.line([(214,yy),(214,yy+6)],BLUE,3)
            arm(p,(96,153),(151+wave*4,183))
            arm(p,(194,153),(163-wave*4,185))
            for x,y in [(145,175),(167,172),(174,184),(150,192)]:
                p.ellipse((x-5,y-5,x+5,y+5),WHITE,"#A9CFD5",1)
            p.rect((58,153,85,176),"#DBADC2",4)
        else:
            p.rect((126,151,196,218),"#EBCB7F",5,"#D4B463")
            for x in [136,187]:p.line([(x,157),(x,212)],"#FFF1BF",3)
            arm(p,(96,153),(138,181+wave*8))
            arm(p,(194,153),(182,181-wave*8))
    elif token in {"brush_teeth","wash_face"}:
        bear(p,156,247,.96)
        if token=="brush_teeth":
            p.ellipse((139,131,173,146),WHITE,LINE,1)
            for x in [147,155,163]:p.line([(x,132),(x,142)],"#C7D9D2",1)
            px=159+wave*7
            arm(p,(213,146),(px+49,150))
            p.line([(px+10,140),(px+64,153)],"#D998AE",7)
            p.rect((px-8,132,px+22,143),WHITE,3,"#B4CDC8",1)
            for x in range(-4,21,5):p.line([(px+x,132),(px+x,140)],"#BBCBC4",1)
            for x,y in [(137,137),(170,146)]:p.ellipse((x-4,y-4,x+4,y+4),WHITE,"#BDDCD9",1)
        else:
            px=177+wave*5
            arm(p,(214,151),(px+15,125))
            p.rect((px-28,100,px+13,143),"#A5D0D6",8,"#7BAEBB")
            for x,y in [(103,125),(111,145),(205,97)]:drop(p,x,y+wave*2,4)


def routine(p,token,t):
    wave=math.sin(t*math.tau)
    if token in {"sleep","wake_up"}:
        # Same bed and pillow across both actions keep the contrast concrete.
        p.rect((38,185,281,237),"#B6A0C5",7,LINE)
        p.rect((44,220,59,255),"#AA91BC",3,LINE)
        p.rect((260,220,275,255),"#AA91BC",3,LINE)
        p.rect((42,118,54,218),"#B6A0C5",5,LINE)
        p.ellipse((65,159,133,202),WHITE,"#DADFCF")
        if token=="sleep":
            # Sunny rests on a pillow, tucked beneath a gently breathing blanket.
            q=Transform(p,103,195,.64)
            q.ellipse((-68,-83,-29,-44),CREAM,LINE)
            q.ellipse((29,-83,68,-44),CREAM,LINE)
            q.ellipse((-66,-73,66,21),CREAM,LINE)
            eyes(q,0,-30,24,True)
            q.ellipse((-7,-16,7,-8),INK)
            q.arc((-15,-11,15,7),20,160,INK,2)
            p.rect((140,164+wave,271,218),"#95C3BB",12,"#6EAAA2")
            for x in range(157,260,27):p.line([(x,173),(x,211)],"#C6DED1",2)
            p.ellipse((245,30,284,69),YELLOW)
            p.ellipse((259,24,289,55),"#F2F8E9")
        else:
            bear(p,155,222,.69,arms="up",eyes_closed=False)
            p.rect((102,194,248,218),"#95C3BB",10,"#6EAAA2")
            sun(p,273,49,18)
    elif token in {"hungry","thirsty","eat","drink"}:
        bear(p,128,248,.92,arms="front" if token in {"hungry","thirsty"} else "down")
        if token=="hungry":
            arm(p,(82,153),(126+wave*5,181))
            p.ellipse((210,146,301,175),WHITE,"#BECFBE")
            p.ellipse((226,152,286,168),None,"#D4DED1",1)
            # Thought bubble conveys wanting food; the foreground plate is empty.
            p.ellipse((197,32,303,124),WHITE,"#D4DED1")
            p.ellipse((190,118,204,132),WHITE,"#D4DED1",1)
            p.ellipse((180,132,188,140),WHITE,"#D4DED1",1)
            bread(p,250,79,.58)
        elif token=="thirsty":
            cup(p,235,193,.78,False)
            p.ellipse((201,40,294,132),WHITE,"#D4DED1")
            p.ellipse((191,129,205,143),WHITE,"#D4DED1",1)
            drop(p,248,82,19)
            arm(p,(84,153),(128,157))
        elif token=="eat":
            px=147+wave*10;py=140+wave*8
            arm(p,(179,153),(px+18,py+18))
            apple(p,px,py,.37)
            p.ellipse((212,206,305,229),WHITE,"#BECFBE")
            bread(p,255,204,.37)
        else:
            px=149+wave*7;py=145+wave*5
            arm(p,(179,153),(px+18,py+14))
            cup(p,px,py,.66)
    elif token in {"hot","cold"}:
        bear(p,146+wave*(2 if token=="cold" else 0),248,.93,
             arms="front" if token=="cold" else "wide")
        if token=="hot":
            sun(p,260,51,26)
            for x,y in [(94,90),(201,110),(211,129)]:drop(p,x,y+(t*14)%8,5)
            p.polygon([(254,175),(218,136),(222,112),(246,99),(269,105),(282,128)],"#D4B0C6",LINE)
            p.line([(254,175),(258,196)],LINE,5)
            for x,y in [(227,116),(250,106),(273,122)]:p.line([(254,174),(x,y)],WHITE,1)
        else:
            for x,y in [(54,72),(263,55),(252,176)]:snowflake(p,x,y,16)
            # A scarf and little shiver marks signal feeling cold.
            p.rect((94,135,197,151),"#D8A0B5",6,LINE,1)
            p.rect((172,145,189,188),"#D8A0B5",4,LINE,1)
            for x in [69,222]:p.line([(x,160),(x-4,168),(x+1,176),(x-3,184)],"#8BAEBF",2)
    elif token in {"coat_on","coat_off"}:
        bear(p,113,248,.91,coat=token=="coat_on")
        if token=="coat_off":
            # Sunny's teal top is visible; the removed coat hangs on a low peg.
            p.line([(257,82),(257,240)],LINE,5)
            p.line([(235,101),(277,101)],LINE,5)
            q=Transform(p,256,166,.67)
            q.polygon([(-42,-74),(-76,-39),(-58,-21),(-39,-40),(-39,59),
                       (39,59),(39,-40),(58,-21),(76,-39),(42,-74)],"#E4B451",LINE)
            q.line([(0,-71),(0,57)],WHITE,3)
        else:
            p.line([(254,83),(254,240)],LINE,5)
            p.line([(232,102),(276,102)],LINE,5)


def family(p,token):
    # A shared small Sunny makes the adult/child relationship visible in both cards.
    bear(p,104,246,.97,shirt="#B49AC9" if token=="mom" else "#C69772")
    bear(p,250,246,.48)
    arm(p,(148,150),(201,189))
    arm(p,(224,196),(201,189))
    if token=="mom":
        # A fixed lavender sweater and small flower distinguish this caregiver.
        for a in range(0,360,72):
            x=126+7*math.cos(math.radians(a));y=154+7*math.sin(math.radians(a))
            p.ellipse((x-5,y-5,x+5,y+5),"#F0D0A1")
        p.ellipse((122,150,130,158),"#D6A748")
    else:
        # Warm brown sweater and round glasses remain stable across all scenes.
        for x in [80,128]:p.ellipse((x-15,80,x+15,102),None,"#617A70",2)
        p.line([(95,90),(113,90)],"#617A70",2)


def turtle(p,x=161,y=173,size=1,step=0):
    q=Transform(p,x,y,size)
    shadow(q,0,52,102)
    q.polygon([(-65,22),(-98,32),(-68,36)],"#9BBC81",LINE)
    for dx in [-44,34]:
        q.ellipse((dx-14+step,29,dx+10+step,58),"#A6C590",LINE)
    q.ellipse((49,-9,103,39),"#A6C590",LINE)
    q.ellipse((82,1,88,10),INK)
    q.arc((85,11,98,26),30,140,INK,2)
    q.ellipse((-77,-57,74,46),"#91B483",LINE)
    q.polygon([(-20,-39),(17,-39),(36,-11),(15,17),(-22,17),(-39,-9)],"#ABC598",LINE)
    for a,b in [((-20,-39),(-37,-52)),((17,-39),(34,-52)),((36,-11),(70,-15)),
                ((15,17),(31,42)),((-22,17),(-39,42)),((-39,-9),(-73,-11))]:q.line([a,b],LINE,2)


def animal(p,token):
    shadow(p)
    if token=="turtle":
        turtle(p)
    elif token=="bird":
        p.polygon([(104,159),(64,133),(71,185),(123,189)],"#80B79A",LINE)
        p.ellipse((94,70,243,219),GREEN,"#6EA083")
        p.ellipse((124,131,218,208),"#DDF0D8")
        p.ellipse((109,130,166,171),"#7CB69C","#6EA083")
        p.ellipse((200,111,210,125),INK)
        p.polygon([(238,122),(272,134),(238,146)],"#D9A354",LINE)
        p.ellipse((204,138,223,150),"#E8B7A0")
        for x in [151,194]:p.line([(x,214),(x-4,241),(x+9,241)],"#C89B63",4)
    elif token=="fish":
        p.polygon([(92,119),(41,79),(46,188),(96,159)],"#F0B76B",LINE)
        p.polygon([(137,94),(168,66),(196,101)],"#F0B76B",LINE)
        p.polygon([(145,181),(162,215),(191,179)],"#F0B76B",LINE)
        p.ellipse((80,91,275,191),"#F3CB7C",LINE)
        p.ellipse((224,121,235,135),INK)
        p.arc((244,139,270,157),30,150,INK,2)
        p.arc((174,108,216,174),115,245,"#DDA95D",3)
        p.polygon([(165,137),(129,121),(135,162)],"#EFB465",LINE)
        for x,y,r in [(273,84,8),(289,58,12),(277,28,6)]:p.ellipse((x-r,y-r,x+r,y+r),None,"#94C2CF",2)
        p.line([(63,243),(112,237),(165,243),(220,237),(267,243)],"#B5D6D4",3)
    elif token in {"cat","dog","rabbit"}:
        fur={"cat":"#E8B37F","dog":"#C7A178","rabbit":"#EEDFC7"}[token]
        p.ellipse((106,124,215,240),fur,LINE)
        for x in [128,190]:p.ellipse((x-23,211,x+23,246),fur,LINE)
        if token=="cat":
            p.arc((190,139,280,233),265,92,LINE,17)
            p.arc((190,139,280,233),265,92,fur,13)
            p.polygon([(94,111),(105,36),(150,87)],fur,LINE)
            p.polygon([(172,86),(220,36),(229,113)],fur,LINE)
            p.polygon([(107,88),(111,55),(134,84)],"#D89088")
            p.polygon([(189,84),(214,55),(218,93)],"#D89088")
        elif token=="dog":
            p.ellipse((72,73,124,176),"#A77C58",LINE)
            p.ellipse((198,73,251,176),"#A77C58",LINE)
            p.arc((194,158,272,219),250,360,LINE,14)
            p.arc((194,158,272,219),250,360,fur,10)
        else:
            p.ellipse((108,11,147,116),fur,LINE)
            p.ellipse((177,11,216,116),fur,LINE)
            p.ellipse((118,26,137,97),"#E6B5AB")
            p.ellipse((188,26,206,97),"#E6B5AB")
            p.ellipse((198,190,233,222),WHITE,LINE)
        p.ellipse((87,69,234,183),fur,LINE)
        p.ellipse((121,125,203,173),"#FFF0D8")
        eyes(p,160,116,30)
        p.ellipse((151,132,170,144),"#725747" if token=="dog" else "#CB8F83")
        p.line([(161,143),(161,152)],INK,2)
        p.arc((142,139,181,166),20,160,INK,2)
        if token=="cat":
            for side in [-1,1]:
                for dy in [-7,6]:p.line([(160+side*38,145+dy),(160+side*80,143+dy*2)],LINE,2)
            for dx in [-12,0,12]:p.line([(160+dx,73),(160+dx*.7,91)],"#BA875F",3)
        if token=="dog":p.ellipse((161,153,175,171),"#E9AD9C",LINE,1)
    elif token=="cow":
        for x in [106,140,198,228]:p.rect((x-9,182,x+9,239),"#FBF5E7",5,LINE)
        p.ellipse((93,126,254,219),"#FBF5E7",LINE)
        p.ellipse((176,128,221,175),"#718782")
        p.ellipse((207,180,247,210),"#718782")
        p.line([(252,156),(270,204)],LINE,4)
        p.ellipse((264,198,278,220),"#718782")
        for side in [-1,1]:
            x=113+side*49
            p.ellipse((x-23,81,x+18,104),"#FBF5E7",LINE)
            p.polygon([(113+side*28,80),(113+side*37,42),(113+side*49,76)],"#DEC493",LINE)
        p.ellipse((61,62,165,176),"#FBF5E7",LINE)
        p.ellipse((63,66,101,118),"#718782")
        eyes(p,113,112,26)
        p.ellipse((63,126,166,181),"#E6B6A9",LINE)
        for x in [88,140]:p.ellipse((x-4,147,x+4,156),"#9A786D")
    elif token=="sheep":
        for x in [103,142,190,228]:p.rect((x-8,181,x+8,238),"#B69F86",5,LINE)
        for x,y in [(113,123),(142,107),(181,108),(215,124),(234,155),(220,184),
                    (187,199),(148,201),(112,187),(91,153)]:
            p.ellipse((x-30,y-30,x+30,y+30),"#FFF8E7","#BAAE96")
        p.ellipse((105,111,223,197),"#FFF8E7")
        p.ellipse((49,97,139,184),"#D3C2A8",LINE)
        p.ellipse((27,103,67,122),"#D3C2A8",LINE)
        p.ellipse((126,102,159,122),"#D3C2A8",LINE)
        for x,y in [(69,90),(96,81),(122,91)]:p.ellipse((x-19,y-17,x+19,y+17),"#FFF8E7","#BAAE96")
        eyes(p,94,135,20)
        p.ellipse((89,153,100,162),INK)
        p.arc((82,155,109,175),10,165,INK,2)


def food(p,token):
    shadow(p)
    if token=="apple":apple(p,160,152,1.5)
    elif token=="bread":bread(p,160,145,1.6)
    elif token=="banana":
        p.polygon([(83,57),(91,84),(99,115),(113,145),(137,165),(169,173),
                   (201,165),(229,141),(246,110),(253,93),(261,99),(258,135),
                   (242,174),(214,209),(177,228),(132,227),(95,207),(70,177),
                   (57,139),(60,104),(73,71)],YELLOW,LINE,3)
        p.line([(77,102),(76,141),(91,178),(122,201),(158,210),(195,199),(225,173)],"#E1B147",4)
        p.rect((72,43,88,69),"#9C9260",3,LINE)
        p.line([(252,94),(259,82)],LINE,7)
    elif token=="carrot":
        p.polygon([(107,85),(212,99),(146,248)],"#EFA364",LINE,3)
        p.ellipse((106,64,215,114),"#F3B177",LINE,2)
        for a,b in [((125,124),(155,130)),((167,152),(190,157)),((137,180),(153,184))]:p.line([a,b],"#CC844A",3)
        for end in [(113,28),(154,14),(200,32)]:
            p.line([(160,80),end],"#7BA572",9)
            p.ellipse((end[0]-8,end[1]-8,end[0]+8,end[1]+8),"#8FB681")
    elif token=="tomato":
        p.ellipse((70,93,249,242),RED,"#C7665E",3)
        p.polygon([(160,109),(115,83),(144,87),(147,59),(163,90),(191,65),(183,96),(218,104),(175,116)],"#7BA572",LINE)
        p.line([(159,92),(169,59)],"#7BA572",7)
        p.arc((91,110,217,217),185,245,"#FFD9BF",5)
    elif token=="milk":
        p.polygon([(106,84),(174,84),(211,112),(106,112)],"#DAE9E6",LINE)
        p.polygon([(106,84),(123,45),(190,45),(174,84)],WHITE,LINE)
        p.polygon([(174,84),(190,45),(225,78),(211,112)],"#B5D2D5",LINE)
        p.rect((106,112,211,245),WHITE,1,LINE)
        p.polygon([(211,112),(225,78),(225,216),(211,245)],"#B5D2D5",LINE)
        p.rect((108,134,209,164),"#A8CED7")
        # A small cow face identifies milk without any language-specific text.
        p.ellipse((133,180,187,220),"#EEE9DD",LINE)
        p.ellipse((128,180,144,191),"#EEE9DD",LINE)
        p.ellipse((177,180,193,191),"#EEE9DD",LINE)
        eyes(p,160,194,12)
        p.ellipse((144,204,177,222),"#E6B6A9",LINE)


def cloud(p,x,y,size=1,color="white"):
    color=WHITE if color=="white" else color
    for dx,dy,r in [(-34,4,24),(-7,-8,32),(29,5,26)]:
        p.ellipse((x+(dx-r)*size,y+(dy-r)*size,x+(dx+r)*size,y+(dy+r)*size),color,"#B7CFCB",1)
    p.rect((x-45*size,y+2*size,x+44*size,y+23*size),color,7*size)


def outside(p,token,t):
    if token=="sun":sun(p,160,137,64)
    elif token in {"rain","wind","snow"}:
        cloud(p,158,79,1.6,"#D8E6E5")
        if token=="rain":
            for i,(x,y) in enumerate([(87,142),(143,173),(207,139),(102,207),(224,208)]):
                drop(p,x,y+(t*32+i*5)%21,8)
            p.ellipse((69,247,252,265),"#C8E2E5")
        elif token=="snow":
            for i,(x,y) in enumerate([(79,164),(151,190),(228,155),(114,227),(227,230)]):
                snowflake(p,x+3*math.sin(t*math.tau+i),y+(t*14)%9,12)
            p.ellipse((45,249,284,276),WHITE,"#CFDDD7")
        else:
            for x,y,w in [(45,153,182),(85,193,165),(38,232,150)]:
                p.line([(x+t*12,y),(x+w-23+t*12,y)],"#91B2B8",4)
                p.arc((x+w-42+t*12,y-33,x+w+t*12,y),270,450,"#91B2B8",4)
            p.polygon([(109,157),(133,138),(139,150),(125,165)],"#9BBB83",LINE,1)
            p.polygon([(200,220),(220,204),(229,219),(210,233)],"#DABB75",LINE,1)
    elif token=="tree":
        shadow(p)
        p.polygon([(139,118),(182,115),(184,244),(132,244)],"#B79270",LINE)
        p.line([(160,187),(197,157)],LINE,5)
        p.line([(157,207),(119,176)],LINE,5)
        for x,y,r in [(160,72,52),(108,105,49),(208,105,48),(150,132,53)]:
            p.ellipse((x-r,y-r,x+r,y+r),"#9FBE83","#7B9E6B",2)
        p.ellipse((122,62,146,83),"#BDD29F")
    elif token=="flower":
        shadow(p)
        p.line([(160,123),(160,246)],"#82A77B",8)
        p.ellipse((109,176,158,208),"#9FBE83","#7B9E6B")
        p.ellipse((162,200,213,229),"#9FBE83","#7B9E6B")
        for a in range(0,360,60):
            x=160+math.cos(math.radians(a))*43;y=100+math.sin(math.radians(a))*43
            p.ellipse((x-29,y-29,x+29,y+29),"#E5ABC0","#C689A3")
        p.ellipse((130,70,190,130),YELLOW,"#C9A44D")
        for x,y in [(150,89),(169,90),(158,110)]:p.ellipse((x-2,y-2,x+2,y+2),"#BD9A47")
    elif token in {"car","bus"}:
        shadow(p,160,233,122)
        if token=="car":
            p.polygon([(39,172),(67,153),(99,101),(200,101),(242,149),(279,164),(279,215),(39,215)],RED,LINE,3)
            p.polygon([(84,150),(110,112),(148,112),(148,150)],"#DBECE9",LINE)
            p.polygon([(161,112),(193,112),(225,150),(161,150)],"#DBECE9",LINE)
            p.rect((42,176,58,191),YELLOW,3)
            p.rect((258,170,279,186),YELLOW,3)
            p.line([(163,167),(178,167)],LINE,3)
        else:
            p.rect((30,87,289,215),YELLOW,15,LINE,3)
            for x in [44,96,148]:p.rect((x,106,x+42,157),"#D5E7E6",5,LINE)
            p.rect((203,106,270,206),"#D5E7E6",4,LINE)
            p.line([(236,108),(236,205)],LINE,2)
            p.line([(42,176),(193,176)],"#D1A542",3)
        for x in [88,238]:
            p.ellipse((x-27,192,x+27,246),"#66766B",LINE,2)
            p.ellipse((x-12,207,x+12,231),"#EAEADD")


def movement(p,token,t):
    if token in {"fast","slow"}:
        # The same turtle travels the same path; only elapsed motion differs.
        x=160+57*math.sin(t*math.tau)
        turtle(p,x,168,.82,5*math.sin(t*math.tau*2))
        p.line([(48,242),(272,242)],"#C4D4B7",2)
    elif token=="jump":
        height=34*max(0,math.sin(t*math.tau))
        shadow(p,160,247,66)
        bear(p,160,244-height,.95,arms="up")
        arrow(p,(256,211),(256,141),TEAL,4)
    elif token=="walk":
        x=160+27*math.sin(t*math.tau)
        bear(p,x,244-3*abs(math.sin(t*math.tau*2)),.93)
        for i in range(4):
            fx=69+i*47
            p.ellipse((fx,249+(i%2)*7,fx+15,255+(i%2)*7),"#BDCFB0")
        # Alternating foreground feet make the walking action legible.
        for side in [-1,1]:
            fx=x+side*24+8*math.sin(t*math.tau)*side
            p.ellipse((fx-17,224,fx+17,241),CREAM,LINE)
    elif token=="stop":
        bear(p,136,244,.95)
        arm(p,(183,145),(236,125))
        paw(p,240,113,21)
        for dx in [-11,-3,5,13]:p.line([(240+dx,99),(240+dx,111)],"#C99776",1)
        p.line([(91,252),(218,252)],"#DABFA3",3)
    elif token=="turn":
        bear(p,160,244,.94,back=.25<t<.75)
        p.arc((76,206,243,262),0,310,TEAL,4)
        p.polygon([(222,211),(240,215),(229,228)],TEAL)


def shapes(p,token):
    shadow(p)
    if token=="circle":p.ellipse((78,57,242,221),"#CFA7C2","#B486A6",3)
    elif token=="square":p.rect((78,57,242,221),BLUE,0,"#699AC2",3)
    else:p.polygon([(160,49),(258,226),(62,226)],YELLOW,"#C6A34F",3)


def _draw(p,token,t):
    if token in {"please","thank_you","yes","no"}:draw_social(p,token,t)
    elif token in {"big","small","up","down","in","out","on","under"}:draw_relation(p,token)
    elif token in {"open","close"}:draw_door(p,token)
    elif token in BODY_PARTS:bear(p,body_part=token)
    elif token in {"wash_hands","dry_hands","brush_teeth","wash_face"}:hygiene(p,token,t)
    elif token in {"wake_up","sleep","hungry","thirsty","eat","drink","hot","cold","coat_on","coat_off"}:routine(p,token,t)
    elif token in {"mom","dad"}:family(p,token)
    elif token in {"cat","dog","bird","fish","rabbit","turtle","cow","sheep"}:animal(p,token)
    elif token in {"apple","banana","carrot","tomato","bread","milk"}:food(p,token)
    elif token in {"sun","rain","wind","snow","tree","flower","car","bus"}:outside(p,token,t)
    elif token in {"fast","slow","walk","stop","jump","turn"}:movement(p,token,t)
    elif token in {"circle","square","triangle"}:shapes(p,token)
    else:
        raise ValueError(f"Unsupported preschool object: {token!r}")


@lru_cache(maxsize=96)
def _sprite(token, width, scale, phase):
    image=Image.new("RGBA",(640,560),(0,0,0,0))
    _draw(Board(image),token,phase/8)
    return image.resize((width*scale,round(width*.875)*scale),Image.Resampling.LANCZOS)


def draw_object(p,token,x,y,width,t=0,**_kwargs):
    """Composite one cached object, centered on x/y; width uses Pen coordinates."""
    if token not in NEW_VISUALS:
        raise ValueError(f"Unknown preschool visual token: {token!r}")
    width=max(32,round(width))
    scale=round(p.image.width/1280)
    phase=int(t*(12 if token=="fast" else 2 if token=="slow" else 8))%8 if token in ANIMATED else 0
    art=_sprite(token,width,scale,phase)
    p.image.paste(art,(round(x*scale-art.width/2),round(y*scale-art.height/2)),art)
