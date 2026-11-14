# builds the window vf strings (1920x1080 coords) from draft (960x544) boxes
import json
KX=2.0; KY=1080/544
def lin(keys,i):
    # keys [(t,v)] -> piecewise linear expr in T
    e=f"{keys[-1][1]:.1f}"
    for (t0,v0),(t1,v1) in reversed(list(zip(keys,keys[1:]))):
        e=f"if(lt(T,{t1}),{v0:.1f}+{(v1-v0)/(t1-t0):.3f}*(T-{t0}),{e})"
    return f"if(lt(T,{keys[0][0]}),{keys[0][1]:.1f},{e})" if keys[0][0]>0 else e
def window(tag, boxes, lo, mix=(0.30,0.34,0.42), feather=14):
    """boxes: list of static (x0,y0,x1,y1) draft coords, or ('track',[(t,x0,y0,x1,y1),...])"""
    rects=[]
    for b in boxes:
        if b[0]=='track': rects.append([(t,x0*KX,y0*KY,x1*KX,y1*KY) for t,x0,y0,x1,y1 in b[1]])
        else: rects.append([(0,b[0]*KX,b[1]*KY,b[2]*KX,b[3]*KY)])
    X0=int(min(min(k[1] for k in r) for r in rects))//2*2; Y0=int(min(min(k[2] for k in r) for r in rects))//2*2
    X1=-(-int(max(max(k[3] for k in r) for r in rects))//2*2); Y1=-(-int(max(max(k[4] for k in r) for r in rects))//2*2)
    X1=min(X1,1920); Y1=min(Y1,1080); W=X1-X0; H=Y1-Y0
    kr,kg,kb=mix
    R=f"(r(X,Y)/{kr})"; G=f"(g(X,Y)/{kg})"; B=f"(b(X,Y)/{kb})"
    key=f"clip(({G}-{lo})/25,0,1)*clip((28-abs({R}-{G}))/10,0,1)*clip(({B}-{R}+40)/12,0,1)*clip((246-{G})/8,0,1)"
    masks=[]
    for r in rects:
        if len(r)==1:
            _,a,b,c,d=r[0]; a-=X0;c-=X0;b-=Y0;d-=Y0
            masks.append(f"clip((X-{a:.0f})/{feather},0,1)*clip(({c:.0f}-X)/{feather},0,1)*clip((Y-{b:.0f})/{feather},0,1)*clip(({d:.0f}-Y)/{feather},0,1)")
        else:
            xa=lin([(k[0],k[1]-X0) for k in r],0); ya=lin([(k[0],k[2]-Y0) for k in r],0); xb=lin([(k[0],k[3]-X0) for k in r],0); yb=lin([(k[0],k[4]-Y0) for k in r],0)
            masks.append(f"clip((X-({xa}))/{feather},0,1)*clip((({xb})-X)/{feather},0,1)*clip((Y-({ya}))/{feather},0,1)*clip((({yb})-Y)/{feather},0,1)")
    m=masks[0]
    for x in masks[1:]: m=f"max({m},{x})"
    return (f"split[{tag}0][{tag}1];[{tag}1]crop={W}:{H}:{X0}:{Y0},colorchannelmixer=rr={kr}:gg={kg}:bb={kb},format=rgba,"
            f"geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*{key}*{m}'[{tag}2];[{tag}0]format=rgba[{tag}3];[{tag}3][{tag}2]overlay={X0}:{Y0},format=yuv420p")
S={
 's07': window('w7',[(555,110,745,258)],150),
 's08': window('w8',[(700,78,898,238)],150),
 's09': window('w9',[(320,10,500,170),(810,0,960,240)],150),
 's12': window('w12',[(545,75,705,225)],150),
 's13': window('w13',[(490,36,705,185),(870,0,960,205)],150),
 's17': window('w17',[(585,66,808,218)],150),
 's18': window('w18',[('track',[(0,603,0,795,124),(1,605,40,791,182),(2,615,104,797,240),(3,628,122,810,259),(4,641,128,824,266),(5,649,130,832,269),(6,655,130,839,269),(7,665,126,850,265),(7.5,683,115,872,255),(8,711,104,905,246),(8.5,746,109,945,254),(9.2,790,112,960,258)])],95),
}
json.dump(S,open('vf-windows.json','w'),indent=1)
for k,v in S.items(): print(k,len(v))
