#!/usr/bin/env python3
"""Export original text SVG diagrams with the same independently countable cells."""
import pathlib
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent
BG, INK, CORAL, GREEN = '#F8F5EF', '#172D33', '#D85E4A', '#477F72'


def write_svg(filename, target=None):
    root = ET.Element('svg', xmlns='http://www.w3.org/2000/svg', width='1280', height='720', viewBox='0 0 1280 720')
    def rect(x,y,w,h,fill,rx=0):
        ET.SubElement(root,'rect',x=str(x),y=str(y),width=str(w),height=str(h),fill=fill,rx=str(rx))
    def text(x,y,s,size=26,fill=INK,bold=False,anchor='start'):
        el=ET.SubElement(root,'text',x=str(x),y=str(y),fill=fill,**{'font-family':'Noto Sans CJK TC, sans-serif','font-size':str(size),'font-weight':'700' if bold else '400','text-anchor':anchor})
        el.text=str(s)
    rect(0,0,1280,720,BG)
    title='36 種組合，每格一樣可能' if target is None else f'總和 {target}：數出有利組合'
    text(62,86,title,47,bold=True)
    text(65,137,'兩顆公平、獨立的六面骰子；每格對應一個有順序的結果。',24,'#6B787A')
    x0,y0,cell,gap=156,245,53,8
    text(330,194,'第二顆 →',22,'#6B787A',anchor='middle')
    text(60,219,'第一顆',20,'#6B787A')
    for n in range(1,7):
        text(x0+(n-1)*(cell+gap)+cell/2,y0-20,n,24,'#6B787A',anchor='middle')
        text(x0-31,y0+(n-1)*(cell+gap)+cell/2+9,n,24,'#6B787A',anchor='middle')
    count=0
    for a in range(1,7):
        for b in range(1,7):
            active=target is not None and a+b==target
            count+=int(active)
            x,y=x0+(b-1)*(cell+gap),y0+(a-1)*(cell+gap)
            rect(x,y,cell,cell,CORAL if active else '#E9EBE4',9)
            text(x+cell/2,y+cell/2+9,a+b,23,'#FFFFFF' if active else INK,active,'middle')
    rect(672,240,543,330,'#FFFFFF',26)
    if target is None:
        text(713,292,'所有結果',26,'#6B787A')
        text(706,422,'36',120,GREEN,True)
        text(715,535,'6 × 6 = 36',43,bold=True)
    else:
        text(713,292,'有利組合 / 全部組合',26,'#6B787A')
        text(706,420,f'{count} / 36',88,CORAL,True)
        text(715,535,f'約 {count/36*100:.1f}%',43,CORAL,True)
    text(64,677,'原創練習範例 · 逐格可核對 · 未引用他人影片畫面',18,'#6B787A')
    ET.indent(root)
    ET.ElementTree(root).write(ROOT/filename,encoding='utf-8',xml_declaration=True)


if __name__=='__main__':
    for name,target in [('grid-all.svg',None),('grid-seven.svg',7),('grid-twelve.svg',12),('grid-six.svg',6)]:
        write_svg(name,target)
        print(name)
