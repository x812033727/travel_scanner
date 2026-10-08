"""Printable junior-high readings, independent questions and writing practice."""
from __future__ import annotations

import html
import os
from pathlib import Path


def activity(episode: dict) -> dict:
    task = episode.get("practice", {})
    for key in ("reading_en", "prompt_en", "prompt_zh_TW", "sample_answer_en"):
        if not isinstance(task.get(key), str) or not task[key].strip():
            raise ValueError(f"{episode['id']}: missing practice.{key}")
    questions = task.get("questions")
    if not isinstance(questions, list) or len(questions) != 3:
        raise ValueError(f"{episode['id']}: practice needs three independent questions")
    for question in questions:
        if not all(isinstance(question.get(key), str) and question[key].strip()
                   for key in ("prompt_en", "answer_en")):
            raise ValueError(f"{episode['id']}: incomplete practice question")
    return task


def write_html(episodes: list[dict], destination: Path) -> Path:
    esc = html.escape
    pages, answers = [], []
    for episode in episodes:
        task = activity(episode)
        questions = "".join(
            f'<li><p>{esc(question["prompt_en"])}</p><div class="answer-line"></div></li>'
            for question in task["questions"])
        pages.append(f'''<article class="worksheet" data-episode="{episode['id']}">
<p class="eyebrow">GRADE {episode['grade']} · SEASON {episode['season']} · LESSON {episode['number']:02}</p>
<h2>{esc(episode['title_en'])}</h2><p class="local-title">{esc(episode['title_zh_TW'])}</p>
<h3>Read</h3><p class="reading">{esc(task['reading_en'])}</p>
<h3>Think and answer</h3><ol>{questions}</ol>
<h3>Write</h3><p class="prompt">{esc(task['prompt_en'])}</p><p>{esc(task['prompt_zh_TW'])}</p>
<div class="writing-lines" aria-label="作答空白">{''.join('<div></div>' for _ in range(5))}</div>
<p class="tip">先自己作答，再看後方例答。寫作可用虛構人物與情境。</p></article>''')
        responses = "".join(f'<li>{esc(q["answer_en"])}</li>' for q in task["questions"])
        answers.append(f'''<section class="answer" data-episode="{episode['id']}">
<h3>{episode['number']:02} · {esc(episode['title_en'])}</h3><ol>{responses}</ol>
<p class="answer-label">Example writing</p><p class="model">{esc(task['sample_answer_en'])}</p></section>''')
    content = '''<!doctype html><html lang="zh-Hant"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sunny &amp; Pip · 國中英文閱讀寫作練習</title><style>
body{font:16px/1.55 system-ui,"Noto Sans TC",sans-serif;color:#23394a;background:#eef2f4;margin:0}
main{max-width:850px;margin:auto;padding:30px}h1,h2,h3{line-height:1.25}h2{margin:6px 0;font-size:27px}
h3{font-size:17px;color:#227b79;margin:22px 0 8px}p{margin:6px 0}.worksheet{background:white;border:1px solid #c8d5dc;border-top:5px solid #227b79;border-radius:8px;margin:28px 0;padding:32px;break-after:page}
.eyebrow{font-size:12px;letter-spacing:.08em;color:#476674}.local-title{color:#476674}.reading{background:#f2f6f6;border-left:3px solid #63aaa2;padding:16px;line-height:1.7}
ol{padding-left:24px}li{margin:9px 0}.answer-line{height:25px;border-bottom:1px solid #acbcc5}.writing-lines div{height:31px;border-bottom:1px solid #acbcc5}.tip{font-size:12px;color:#566e7c;margin-top:12px}
.answers{break-before:page;margin-top:60px}.answer{background:white;border:1px solid #c8d5dc;border-radius:8px;padding:24px;margin:20px 0;break-inside:avoid}.answer-label{font-size:13px;color:#227b79;font-weight:700}
.print{background:#227b79;color:white;border:0;padding:11px 18px;border-radius:6px;cursor:pointer}
@media print{body{background:white;font-size:12px}main{padding:0;max-width:none}.worksheet{margin:0;border:0;border-top:3px solid #227b79;padding:16px 0;min-height:255mm}h2{font-size:22px}h3{margin:14px 0 5px}.reading{padding:10px}.writing-lines div{height:27px}.answer{padding:15px;border-radius:0}.print{display:none}}
</style><main><h1>ENGLISH LAB · 國中英文練習</h1><p>先看影片，再獨立閱讀與作答。每集三題閱讀或句型應用，加上一項短文寫作。</p>
<p>示例答案在後方；開放式題目可有其他合理答案。這份材料用來練習，不作正式程度認證。</p><button class="print" onclick="window.print()">列印練習</button>'''
    content += "".join(pages)
    content += '<div class="answers"><h1>Answers and Writing Examples</h1><p>先完成練習再核對；寫作例答示範表達方式，不是唯一正解。</p>'
    content += "".join(answers) + '</div></main></html>'
    path = destination / "Practice.html"
    path.write_text(content, encoding="utf-8")
    return path


def write_pdf(episodes: list[dict], destination: Path) -> Path:
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.utils import simpleSplit

    configured = os.environ.get("JUNIOR_HIGH_PRACTICE_FONT") or os.environ.get("ELEMENTARY_PRACTICE_FONT")
    candidates = ([Path(configured)] if configured else []) + [
        parent / ".fonts/NotoSansTC-Regular.ttf" for parent in (destination, *destination.parents)]
    font_path = next((path for path in candidates if path.is_file()), None)
    if font_path is None:
        raise ValueError("Set JUNIOR_HIGH_PRACTICE_FONT to a static Traditional Chinese TrueType font")
    font = "JuniorHighPractice"
    if font not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(font, str(font_path)))
    path = destination / "Practice.pdf"
    width, height = A4
    c = canvas.Canvas(str(path), pagesize=A4)
    c.setTitle("Sunny & Pip - Junior High English Practice")
    c.setAuthor("Sunny & Pip English course")
    page = 0
    ink, teal = (.14, .23, .30), (.13, .48, .47)

    def split(value: str, size: float, available: float, chinese: bool) -> list[str]:
        if not chinese:
            result = simpleSplit(value, font, size, available)
        else:
            result, line = [], ""
            for char in value:
                if char == "\n" or pdfmetrics.stringWidth(line + char, font, size) > available:
                    if line:
                        result.append(line)
                    line = "" if char == "\n" else char
                else:
                    line += char
            if line:
                result.append(line)
        if any(pdfmetrics.stringWidth(line, font, size) > available + .1 for line in result):
            raise ValueError("Practice text contains an overlong unbreakable word")
        return result

    def text(value: str, x: float, y: float, size: float = 12, chinese: bool = False,
             available: float = width - 92, leading: float = 1.40) -> float:
        c.setFont(font, size)
        for line in split(value, size, available, chinese):
            if y < 49:
                raise ValueError(f"Practice content overflows PDF page {page + 1}")
            c.drawString(x, y, line)
            y -= size * leading
        return y

    def heading(label: str, y: float) -> float:
        c.setFillColorRGB(*teal)
        y = text(label, 46, y - 8, 12)
        c.setFillColorRGB(*ink)
        return y - 3

    def rule(y: float):
        if y < 63:
            raise ValueError(f"Practice writing line overflows PDF page {page + 1}")
        c.setStrokeColorRGB(.65, .73, .77)
        c.line(46, y, width - 46, y)

    def footer():
        nonlocal page
        page += 1
        c.setFont(font, 9)
        c.setFillColorRGB(.35, .44, .49)
        c.drawString(46, 24, "ENGLISH LAB - Sunny & Pip")
        c.drawRightString(width - 46, 24, str(page))
        c.showPage()

    c.setFillColorRGB(*ink)
    text("ENGLISH LAB", 46, height - 70, 28)
    y = text("Junior High English Practice", 46, height - 112, 22)
    y = text(f"國中英文閱讀寫作｜{len(episodes)} 集", 46, y - 22, 18, True)
    for note in ("每集：閱讀一篇短文、回答三題，再完成短文寫作。",
                 "先獨立作答；需要時回看影片中的例句與說明。",
                 "答案與寫作示例放在後方，請完成後再核對。",
                 "寫作可用虛構人物與情境，不需要提供真實個人資料。",
                 "開放式題目可有其他合理答案，請用文本證據支持想法。",
                 "這套材料用於分級學習，不代表正式英語程度認證。"):
        y = text(note, 46, y - 18, 13, True)
    text("Lessons " + ", ".join(f"{episode['number']:02}" for episode in episodes), 46, y - 25, 10)
    footer()

    for episode in episodes:
        task = activity(episode)
        c.setFillColorRGB(*teal)
        y = text(f"GRADE {episode['grade']}  /  SEASON {episode['season']}  /  LESSON {episode['number']:02}",
                 46, height - 47, 10)
        c.setFillColorRGB(*ink)
        y = text(episode["title_en"], 46, y - 8, 19)
        y = text(episode["title_zh_TW"], 46, y - 3, 12, True)
        y = heading("READ", y)
        y = text(task["reading_en"], 46, y, 12)
        y = heading("THINK AND ANSWER", y)
        for number, question in enumerate(task["questions"], 1):
            y = text(f"{number}. {question['prompt_en']}", 46, y, 11.5)
            rule(y - 11)
            y -= 25
        y = heading("WRITE", y)
        y = text(task["prompt_en"], 46, y, 12)
        y = text(task["prompt_zh_TW"], 46, y - 2, 10.5, True)
        if y < 185:
            raise ValueError(f"{episode['id']}: not enough room for five writing lines")
        for offset in range(5):
            rule(y - 17 - offset * 25)
        footer()

    for start in range(0, len(episodes), 3):
        c.setFillColorRGB(*teal)
        y = text("Answers and Writing Examples", 46, height - 47, 18)
        c.setFillColorRGB(*ink)
        y = text("先作答再核對。寫作與開放式題目可有其他合理答案。", 46, y - 3, 10.5, True)
        for episode in episodes[start:start + 3]:
            task = activity(episode)
            c.setFillColorRGB(*teal)
            y = text(f"{episode['number']:02} - {episode['title_en']}", 46, y - 15, 12)
            c.setFillColorRGB(*ink)
            for number, question in enumerate(task["questions"], 1):
                y = text(f"{number}. {question['answer_en']}", 46, y - 3, 10.5)
            y = text("Example writing: " + task["sample_answer_en"], 46, y - 7, 10.5)
        footer()
    c.save()
    return path


def write_practice(episodes: list[dict], destination: Path) -> list[Path]:
    if not episodes:
        raise ValueError("Practice material needs at least one episode")
    destination.mkdir(parents=True, exist_ok=True)
    return [write_html(episodes, destination), write_pdf(episodes, destination)]
