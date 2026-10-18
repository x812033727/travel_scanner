"""Create printable English practice with separate example-answer pages.

New episodes supply practice tasks. The preserved first season derives a short
sentence activity from its existing parent guidance without editing lesson data.
ReportLab is imported only when producing the PDF, not for source verification.
"""
from __future__ import annotations

import html
from pathlib import Path
import os


def activity(episode: dict) -> dict:
    practice = episode.get('practice')
    if practice:
        for field in ('prompt_en', 'prompt_zh_TW', 'sample_answer_en'):
            if not isinstance(practice.get(field), str) or not practice[field].strip():
                raise ValueError(f"{episode['id']}: missing practice.{field}")
        return practice
    sample = next(scene['demo'] for scene in episode['scenes']
                  if scene.get('guided_reading') and scene.get('mode') == 'repeat')
    return {
        'prompt_en': 'Read the model. Say it, then copy one sentence.',
        'prompt_zh_TW': '看本集跟讀句，先說一次，再抄寫一句。也可以指圖並口說。',
        'model_en': sample,
        'sample_answer_en': sample,
    }


def write_html(episodes: list[dict], destination: Path) -> Path:
    esc = html.escape
    pages = []
    for episode in episodes:
        task = activity(episode)
        model = f'<p class="model">{esc(task["model_en"])}</p>' if task.get('model_en') else ''
        pages.append(f'''<article><p class="eyebrow">SEASON {episode['season']} · LESSON {episode['number']:02}</p>
<h2>{esc(episode['title_en'])}</h2><p>{esc(episode['title_zh_TW'])}</p>
<p class="prompt">{esc(task['prompt_en'])}</p><p>{esc(task['prompt_zh_TW'])}</p>{model}
<div class="lines" aria-label="作答空白"><div></div><div></div><div></div></div>
<p class="tip">完成後：說一遍；需要時回看影片。可以用虛構名字，不必寫真實個人資料。</p></article>''')
    answers = ''.join(f'<section class="answer"><h3>{e["number"]:02} · {esc(e["title_en"])}</h3><p>{esc(activity(e)["sample_answer_en"])}</p></section>' for e in episodes)
    content = '''<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sunny &amp; Pip · 英文練習與示例</title><style>
body{font:16px/1.6 system-ui,"Noto Sans TC",sans-serif;color:#253e35;background:#f6f5ed;margin:0}main{max-width:800px;margin:auto;padding:30px}h1,h2,h3{line-height:1.3}h2{margin:5px 0}article{background:white;border:1px solid #ccd9ce;border-radius:12px;margin:24px 0;padding:28px;break-inside:avoid}p{margin:8px 0}.eyebrow{font-size:12px;letter-spacing:.1em;color:#476e5a}.prompt,.model{font-size:20px}.model{background:#eff4e9;padding:10px}.lines div{height:42px;border-bottom:1px solid #a6b9a9}.tip{font-size:12px;color:#5d705f}.answers{break-before:page;margin-top:70px}.answer{break-inside:avoid;border-bottom:1px solid #ccd9ce;padding:10px 0}.answer h3{font-size:16px}.print{border:0;background:#2b6150;color:white;padding:10px 18px;border-radius:8px;cursor:pointer}@media print{body{background:white}main{max-width:none;padding:0}article{margin:0 0 20px;padding:20px;min-height:100mm}.print{display:none}.answers{break-before:page}}
</style><main><h1>Sunny &amp; Pip · 英文練習</h1><p>先看影片，再做本集練習。可以暫停、重看或請陪伴者協助；說、指圖與書寫都可以。</p><p>示例答案在後方，不是所有題目的唯一正解。這份練習不作正式程度測驗。</p><button class="print" onclick="window.print()">列印練習</button>'''
    content += ''.join(pages) + '<div class="answers"><h1>示例答案</h1><p>用來核對句型與表達方式；個人化的答案可以不同。</p>' + answers + '</div></main></html>'
    path = destination / 'Practice.html'
    path.write_text(content, encoding='utf-8')
    return path


def write_pdf(episodes: list[dict], destination: Path) -> Path:
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.utils import simpleSplit
    # Embed a static TrueType CJK font so PDF rendering needs no reader CMap.
    configured = os.environ.get('ELEMENTARY_PRACTICE_FONT')
    candidates = ([Path(configured)] if configured else []) + [
        parent / '.fonts/NotoSansTC-Regular.ttf' for parent in [destination, *destination.parents]
    ]
    font_path = next((item for item in candidates if item.is_file()), None)
    if font_path is None:
        raise ValueError('Set ELEMENTARY_PRACTICE_FONT to a static TrueType font covering Traditional Chinese')
    font = 'ElementaryPractice'
    if font not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(font, str(font_path)))
    path = destination / 'Practice.pdf'
    width, height = A4
    c = canvas.Canvas(str(path), pagesize=A4)
    c.setTitle('Sunny & Pip - Elementary English Practice')
    c.setAuthor('Sunny & Pip English course')
    page = 0

    def lines(text: str, size: float, max_width: float, chinese: bool = False) -> list[str]:
        if not chinese:
            return simpleSplit(text, font, size, max_width)
        # Character wrapping preserves CJK without relying on whitespace.
        result, current = [], ''
        for char in text:
            if char == '\n' or pdfmetrics.stringWidth(current + char, font, size) > max_width:
                if current:
                    result.append(current)
                current = '' if char == '\n' else char
            else:
                current += char
        if current:
            result.append(current)
        return result

    def text(value: str, x: float, y: float, size: float = 12, chinese: bool = False,
             max_width: float = width - 92) -> float:
        c.setFont(font, size)
        for line in lines(value, size, max_width, chinese):
            c.drawString(x, y, line)
            y -= size * 1.45
        return y

    def footer():
        nonlocal page
        page += 1
        c.setFont(font, 9)
        c.setFillColorRGB(.35, .43, .38)
        c.drawString(46, 24, 'Sunny & Pip - Elementary English')
        c.drawRightString(width - 46, 24, str(page))
        c.showPage()

    c.setFillColorRGB(.16, .30, .23)
    text('Sunny & Pip', 46, height - 70, 27)
    text('Elementary English Practice', 46, height - 111, 21)
    y = text(f'國小英文練習｜{len(episodes)} 集', 46, height - 155, 18, True)
    for note in ('看完影片後，選本集練習。可以先口說，再寫下來。',
                 '遇到不熟的句子可以重播、暫停，或請陪伴者協助。',
                 '請用虛構名字，不需要寫真實姓名、地址或其他個資。',
                 '示例答案放在練習後；個人化答案可以不同。',
                 '字母名稱與完整單字練習不等於孤立音素訓練。',
                 '這份活動用於學習，不代表正式英語程度測驗。'):
        y = text(note, 46, y - 19, 13, True)
    text('Lessons ' + ', '.join(f'{e["number"]:02}' for e in episodes), 46, y - 35, 10)
    footer()
    for episode in episodes:
        task = activity(episode)
        c.setFillColorRGB(.16, .30, .23)
        y = text(f"SEASON {episode['season']}  /  LESSON {episode['number']:02}", 46, height - 55, 11)
        y = text(episode['title_en'], 46, y - 12, 21)
        y = text(episode['title_zh_TW'], 46, y - 5, 15, True)
        y = text(task['prompt_en'], 46, y - 25, 15)
        y = text(task['prompt_zh_TW'], 46, y - 10, 13, True)
        if task.get('model_en'):
            y = text('Model: ' + task['model_en'], 46, y - 20, 16)
        if y < 265:
            raise ValueError(f"{episode['id']}: practice instructions leave too little writing space")
        c.setStrokeColorRGB(.64, .72, .66)
        for offset in range(5):
            line_y = y - 42 - 43 * offset
            c.line(46, line_y, width - 46, line_y)
        text('完成後：說一遍；可用指圖或口說代替書寫。', 46, 70, 11, True)
        footer()
    # Separate answer section: six model answers per page.
    for start in range(0, len(episodes), 6):
        c.setFillColorRGB(.16, .30, .23)
        y = text('Example Answers', 46, height - 55, 21)
        y = text('示例答案：可核對句型，個人化答案可以不同。', 46, y - 4, 12, True)
        for episode in episodes[start:start + 6]:
            y = text(f"{episode['number']:02} - {episode['title_en']}", 46, y - 20, 13)
            y = text(activity(episode)['sample_answer_en'], 58, y - 5, 12, max_width=width - 104)
        if y < 50:
            raise ValueError('Example answers overflow a PDF page')
        footer()
    c.save()
    return path


def write_practice(episodes: list[dict], destination: Path) -> list[Path]:
    destination.mkdir(parents=True, exist_ok=True)
    if not episodes:
        raise ValueError('Practice material needs at least one lesson')
    return [write_html(episodes, destination), write_pdf(episodes, destination)]
