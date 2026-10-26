#!/usr/bin/env python3
"""Original deterministic thumbnail diagram; no official UI, no image service."""
from pathlib import Path
import hashlib,json,subprocess,shutil
P=Path(__file__).resolve().parent
SVG='''<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="1000" viewBox="0 0 1120 1000">
<title>同一份配送表：回覆預覽與完整交付</title>
<desc>本片原創示意。40列是本例回覆預覽的顯示數，省略只涉及顯示；完整查詢結果可另存CSV或Parquet後重開核對。不是DuckDB官方介面，未揭後段完整結果筆數。</desc>
<rect width="1120" height="1000" fill="#f5f0e5"/>
<g font-family="Noto Sans CJK TC,Noto Sans TC,sans-serif" fill="#1f2a44">
<text x="560" y="86" text-anchor="middle" font-size="68" font-weight="800">同一份配送表</text>
<rect x="74" y="124" width="972" height="320" rx="28" fill="#ffffff" stroke="#1b7772" stroke-width="8"/>
<text x="122" y="218" font-size="88" font-weight="900">回覆預覽</text>
<rect x="786" y="152" width="214" height="88" rx="24" fill="#efaa4c"/>
<text x="893" y="216" text-anchor="middle" font-size="64" font-weight="900">40列</text>
<rect x="126" y="262" width="470" height="18" rx="9" fill="#c3d6cf"/><rect x="628" y="262" width="322" height="18" rx="9" fill="#c3d6cf"/>
<text x="560" y="354" text-anchor="middle" font-size="76" font-weight="900" fill="#c55435">⋯ 省略 ⋯</text>
<rect x="126" y="390" width="470" height="18" rx="9" fill="#c3d6cf"/><rect x="628" y="390" width="322" height="18" rx="9" fill="#c3d6cf"/>
<path d="M560 464 V526" fill="none" stroke="#1b7772" stroke-width="18" stroke-linecap="round"/><path d="M524 512 L560 552 L596 512" fill="none" stroke="#1b7772" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>
<text x="560" y="616" text-anchor="middle" font-size="66" font-weight="800">按條件另存完整結果</text>
<rect x="74" y="650" width="972" height="250" rx="28" fill="#e0ece4" stroke="#1b7772" stroke-width="8"/>
<text x="560" y="736" text-anchor="middle" font-size="86" font-weight="900">完整交付檔</text>
<rect x="132" y="774" width="336" height="90" rx="16" fill="#ffffff" stroke="#1b7772" stroke-width="5"/>
<text x="300" y="843" text-anchor="middle" font-size="68" font-weight="900">CSV</text>
<rect x="506" y="774" width="482" height="90" rx="16" fill="#ffffff" stroke="#1b7772" stroke-width="5"/>
<text x="747" y="843" text-anchor="middle" font-size="68" font-weight="900">Parquet</text>
<text x="560" y="961" text-anchor="middle" font-size="50" font-weight="700">原創示意｜可重開核對</text>
</g></svg>'''
def main():
 svg=P/'thumbnail-subject.svg';png=P/'thumbnail-subject.png';svg.write_text(SVG)
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-c:v','librsvg','-i',str(svg),'-frames:v','1',str(png)]
 r=subprocess.run(cmd,capture_output=True,text=True,timeout=30);assert r.returncode==0,r.stderr
 def rec(p):return {'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 fingerprinted=P/('thumbnail-subject-'+rec(png)['sha256'][:16]+'.png');shutil.copyfile(png,fingerprinted)
 (P/'thumbnail-subject-provenance.json').write_text(json.dumps({'kind':'Original deterministic vector teaching diagram','license':'CC0-1.0 original asset; no third-party image/UI/logo','fixture':'../public-run/demo/input/parcels.csv','actual_preview_evidence':'../public-run/runlogs/agent-preview.stdout.txt','facts':['40 displayed rows; omitted display does not imply data loss','Full query output can be saved asCSV/Parquet and reopened; output row counts not shown'],'is_official_DuckDB_UI':False,'shows_final_480_or1200_answers':False,'rasterizer_argv':cmd,'svg':rec(svg),'png':rec(png),'content_addressed_png':{'path':fingerprinted.name,**rec(fingerprinted)}},ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'svg':rec(svg),'png':rec(png)}))
if __name__=='__main__':main()
