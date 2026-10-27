#!/usr/bin/env python3
"""Create original text PDFs and actual page extraction outside the repository.

No AI extraction output or spreadsheet result is fabricated by this generator.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from pypdf import PdfReader

MATERIALS = Path(__file__).resolve().parent
FONT_REGULAR = Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
FONT_BOLD = Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
pdfmetrics.registerFont(TTFont('LabSans', str(FONT_REGULAR)))
pdfmetrics.registerFont(TTFont('LabSans-Bold', str(FONT_BOLD)))

def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def make_pdf(quote: dict, notice: str, out: Path) -> None:
    c = canvas.Canvas(str(out), pagesize=A4, pageCompression=1, invariant=1)
    c.setTitle(f"{quote['supplier']} original fictional quotation ({quote['revision']})")
    c.setAuthor("Mokaair original teaching materials")
    width, height = A4
    colour = HexColor(quote['colour'])
    for page_num, page in enumerate(quote['pages'], 1):
        c.setFillColor(colour); c.rect(0, height - 126, width, 126, stroke=0, fill=1)
        c.setFillColor(white); c.setFont('LabSans', 10)
        c.drawString(46, height - 35, 'MOKAAIR  /  ORIGINAL PRACTICE DOCUMENT')
        title_size = 19
        while pdfmetrics.stringWidth(page['heading'], 'LabSans-Bold', title_size) > width - 92:
            title_size -= 0.5
        c.setFont('LabSans-Bold', title_size)
        c.drawString(46, height - 73, page['heading'])
        c.setFont('LabSans', 11)
        c.drawString(46, height - 101, f"{quote['filename']}    |    Page {page_num} of 2")
        y = height - 166
        for i, line in enumerate(page['lines']):
            c.setFillColor(HexColor('#173042'))
            c.setFont('LabSans-Bold' if any(line.startswith(p) for p in ['Unit price:', 'Shipping:', 'Quoted quantity:']) else 'LabSans', 12)
            for wrapped in simpleSplit(line, c._fontname, 12, width - 100):
                c.drawString(50, y, wrapped); y -= 19
            y -= 15
        c.setStrokeColor(HexColor('#CBD5DC')); c.line(46, 108, width - 46, 108)
        c.setFillColor(HexColor('#536573')); c.setFont('LabSans', 9)
        for i, line in enumerate(simpleSplit(notice, 'LabSans', 9, width - 92)):
            c.drawString(46, 88 - i * 13, line)
        c.setFont('LabSans', 9)
        c.drawString(46, 40, f"{quote['supplier']} / {quote['revision']} / fictional exercise only")
        c.drawRightString(width - 46, 40, f"{page_num} / 2")
        c.showPage()
    c.save()

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    root = args.out.resolve(); pdfs = root / 'pdfs'; previews = root / 'previews'
    pdfs.mkdir(parents=True, exist_ok=True); previews.mkdir(exist_ok=True)
    source = json.loads((MATERIALS / 'quote-source.json').read_text())
    documents = []; rendered = []
    for quote in source['quotes']:
        target = pdfs / quote['filename']
        make_pdf(quote, source['exercise_notice'], target)
        reader = PdfReader(target)
        assert len(reader.pages) == 2
        pages = [{'page': i + 1, 'text': p.extract_text()} for i, p in enumerate(reader.pages)]
        assert all(p['text'].strip() for p in pages)
        documents.append({'source_file': target.name, 'sha256': digest(target), 'pages': pages})
        prefix = previews / target.stem
        command = ['pdftoppm', '-png', '-scale-to', '1400', str(target), str(prefix)]
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        rendered.append({'command': command, 'exit_code': result.returncode})
    extracted = {'schema_version': 1, 'method': 'Actual pypdf PdfReader.pages[n].extract_text(); text PDFs; no OCR', 'documents': documents}
    (root / 'extracted-pages.json').write_text(json.dumps(extracted, ensure_ascii=False, indent=2) + '\n')
    (root / 'requirements.txt').write_text((MATERIALS / 'requirements.txt').read_text())
    (root / 'analysis-prompt.txt').write_text((MATERIALS / 'analysis-prompt.txt').read_text())
    manifest = {
        'generated_at_utc': datetime.now(timezone.utc).isoformat(),
        'method': 'Original ReportLab PDFs, extracted with actual installed pypdf; actual Poppler preview rendering',
        'tools': {p: version(p) for p in ['reportlab', 'pypdf', 'openpyxl', 'Pillow']},
        'embedded_fonts': [{'path': str(p), 'sha256': digest(p)} for p in [FONT_REGULAR, FONT_BOLD]],
        'source_inputs': [{'name': p.name, 'sha256': digest(p)} for p in [MATERIALS / 'quote-source.json', MATERIALS / 'requirements.txt', MATERIALS / 'analysis-prompt.txt']],
        'documents': [{'source_file': d['source_file'], 'sha256': d['sha256'], 'pages': len(d['pages'])} for d in documents],
        'rendering': rendered,
        'previews': [{'name': p.name, 'sha256': digest(p)} for p in sorted(previews.glob('*.png'))],
        'extracted_pages_sha256': digest(root / 'extracted-pages.json'),
        'truth_provided_to_ai': False,
        'ai_extraction_executed': False,
        'note': 'The generator does not create or claim any AI extraction. A separate actual AI agent must read only requirements, prompt, and extracted pages.'
    }
    (root / 'generation-receipt.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'output': str(root), 'documents': len(documents), 'pages': sum(len(d['pages']) for d in documents), 'previews': len(manifest['previews']), 'ai_extraction_executed': False}))

if __name__ == '__main__':
    main()
