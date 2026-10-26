#!/usr/bin/env python3
"""Render actual calculated rows as clearly labelled teaching previews, not app screenshots."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.colors import HexColor

FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
pdfmetrics.registerFont(TTFont('LabSans','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('LabSans-Bold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

def f(size, bold=False): return ImageFont.truetype(BOLD if bold else FONT,size)
def display(amount): return f'{float(amount):,.2f}' if amount is not None else '待確認'

def png_table(key, rows, out):
    labels={'original-10':('原報價：10 張','Cedar 的最低單價，還不是可比較的送達總價。'), 'revised-10':('補齊運費：10 張','Cedar 修訂版與 Aster 同價；Birch 仍是已知可比最低。'), 'revised-20':('需求改成：20 張','沿用各家明示的 10–20 張條件重算，最低總價換成 Cedar。')}
    title,subtitle=labels[key]
    image=Image.new('RGB',(1920,1080),'#F6F8FA'); d=ImageDraw.Draw(image)
    d.rectangle((0,0,1920,180),fill='#123D52')
    d.text((88,38),'MOKAAIR  原創 PDF 比價練習',font=f(26),fill='#CFE6ED')
    d.text((88,83),title,font=f(54,True),fill='white')
    d.text((88,220),subtitle,font=f(34),fill='#173042')
    xs=[88,345,620,915,1210,1505]
    heads=['供應商','原始單價','商品含稅','運費含稅','送達總價','判斷']
    d.rounded_rectangle((72,305,1850,390),radius=12,fill='#123D52')
    for x,head in zip(xs,heads): d.text((x,323),head,font=f(31,True),fill='white')
    for index,row in enumerate(rows):
        y=408+index*145
        bg='#DDF3E4' if row['lowest_comparable'] else '#FFF0CC' if not row['comparable'] else '#FFFFFF'
        d.rounded_rectangle((72,y,1850,y+128),radius=10,fill=bg)
        values=[row['supplier'],display(row['unit_price']),display(row['goods_gross']),display(row['shipping_gross']),display(row['delivered_total']),'最低' if row['lowest_comparable'] else '不排序' if not row['comparable'] else '可比較']
        for x,value in zip(xs,values): d.text((x,y+18),value,font=f(39,True if x in [88,1210] else False),fill='#173042')
        d.text((345,y+77),'未稅' if row['unit_tax_mode']=='exclusive' else '已含稅',font=f(23),fill='#536573')
        d.text((620,y+77),f"來源：{row['source_file']}  第 1、2 頁",font=f(23),fill='#536573')
    d.text((88,890),'金額：虛構練習 TWD；5% 僅是教材明示的計算假設。',font=f(29),fill='#536573')
    d.text((88,944),'以實際 AI 抽出的欄位經 Decimal 計算；這是結果預覽，並非試算表軟體截圖。',font=f(27),fill='#536573')
    image.save(out/f'{key}.png')

def pdf_summary(scenarios,out):
    dest=out/'comparison-one-page.pdf'; c=canvas.Canvas(str(dest),pagesize=landscape(A4),invariant=1)
    width,height=landscape(A4)
    c.setTitle('Original fictional PDF quotation comparison: all three scenarios')
    c.setFillColor(HexColor('#123D52'));c.rect(0,height-95,width,95,fill=1,stroke=0)
    c.setFillColor(HexColor('#FFFFFF'));c.setFont('LabSans-Bold',23);c.drawString(36,height-47,'THREE QUOTES, ONE COMPARABLE BASIS')
    c.setFont('LabSans',11);c.drawString(36,height-71,'Actual AI field extraction + independently verified Decimal calculations / TWD')
    y=height-128
    for key,rows in scenarios.items():
        c.setFillColor(HexColor('#123D52'));c.setFont('LabSans-Bold',14);c.drawString(36,y,key);y-=24
        c.setFont('LabSans-Bold',11)
        for x,t in [(36,'Supplier'),(185,'Goods gross'),(325,'Shipping gross'),(475,'Delivered total'),(625,'Status')]:c.drawString(x,y,t)
        y-=21;c.setFont('LabSans',11)
        for row in rows:
            for x,t in [(36,row['supplier']),(185,row['goods_gross']),(325,row['shipping_gross'] if row['shipping_gross'] is not None else 'UNKNOWN'),(475,row['delivered_total'] if row['delivered_total'] is not None else 'UNKNOWN'),(625,'LOWEST COMPARABLE' if row['lowest_comparable'] else 'NOT COMPARABLE' if not row['comparable'] else 'comparable')]:c.drawString(x,y,t)
            y-=20
        y-=19
    c.setFont('LabSans',10);c.setFillColor(HexColor('#536573'))
    c.drawString(36,59,'Fictional suppliers. 5% is an exercise assumption, not a real tax ruling or offer.')
    c.drawString(36,42,'Unknown shipping stays unknown. Cedar revised replaces Cedar original. Written quantity range: 10-20.')
    c.save();return dest

def main():
    p=argparse.ArgumentParser();p.add_argument('--results',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    scenarios=json.loads((a.results/'comparison.json').read_text());a.out.mkdir(parents=True,exist_ok=True)
    for key,rows in scenarios.items():png_table(key,rows,a.out)
    baseline=json.loads((a.results/'baseline-and-normalized-order.json').read_text())
    image=Image.new('RGB',(1920,1080),'#F6F8FA');d=ImageDraw.Draw(image)
    d.rectangle((0,0,1920,180),fill='#123D52')
    d.text((88,38),'MOKAAIR  原創 PDF 比價練習',font=f(26),fill='#CFE6ED')
    d.text((88,83),'只排單價，會得到什麼？',font=f(54,True),fill='white')
    d.text((88,232),'這是三個原始單價的實際算術排序，不是某個 AI 回答失敗的畫面。',font=f(34),fill='#173042')
    for i,(supplier,price) in enumerate(zip(baseline['unit_price_order'],baseline['unit_prices'])):
        y=353+i*143;d.rounded_rectangle((88,y,1825,y+120),radius=12,fill='#FFFFFF')
        d.text((125,y+25),str(i+1),font=f(46,True),fill='#935627')
        d.text((260,y+25),supplier,font=f(46,True),fill='#173042')
        d.text((800,y+25),display(price),font=f(46,True),fill='#173042')
        d.text((1210,y+34),'含稅' if supplier=='Birch' else '未稅',font=f(34),fill='#536573')
    d.text((88,859),'三個數字還沒放在同一個稅與運費基礎上。',font=f(39,True),fill='#935627')
    d.text((88,941),'下一步先看規格、數量、稅與運費，再比較送達總價。',font=f(31),fill='#536573')
    image.save(a.out/'headline-baseline.png')
    print(json.dumps({'previews':4,'summary_pdf':str(pdf_summary(scenarios,a.out)),'source':str(a.results/'comparison.json'),'not_app_screenshots':True}))
if __name__=='__main__':main()
