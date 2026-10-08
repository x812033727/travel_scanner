"""Adult reading and extended writing with all answers on separate later pages."""
from __future__ import annotations

import html
import io
import os
from pathlib import Path
from adult_english.config import course_for_episodes


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


def chart_image(chart: dict, format: str) -> bytes:
    """Plot the authored fictional values on two explicitly labeled scales."""
    from matplotlib import rc_context
    from matplotlib.figure import Figure
    with rc_context({"svg.fonttype": "none", "svg.hashsalt": "adult-english-practice"}):
        figure = Figure(figsize=(7, 2.05), dpi=180, facecolor="white")
        axes = figure.subplots(1, 2)
        figure.subplots_adjust(left=.08, right=.97, bottom=.22, top=.73, wspace=.35)
        figure.suptitle(chart["title_en"], fontsize=11, color="#23394a", y=.99)
        for axis, baseline in zip(axes, (0, chart["axis_min"])):
            axis.bar(chart["labels"], chart["values"], width=.46, color="#387a83", zorder=3)
            axis.set_ylim(baseline, chart["axis_max"])
            axis.set_title("Zero baseline" if baseline == 0 else f"Axis starts at {baseline:g}", fontsize=9.5)
            axis.set_ylabel(chart["unit_en"], fontsize=9)
            axis.tick_params(labelsize=9)
            axis.grid(axis="y", color="#dce2e7", linewidth=.5, zorder=0)
            axis.spines[["top", "right"]].set_visible(False)
            for index, value in enumerate(chart["values"]):
                axis.text(index, value + (chart["axis_max"] - baseline) * .025,
                          f"{value:g}", ha="center", fontsize=10)
        stream = io.BytesIO()
        figure.savefig(stream, format=format, metadata={"Date": None} if format == "svg" else {})
        return stream.getvalue()


def chart_html(task: dict) -> str:
    chart = task.get("chart")
    if chart is None:
        return ""
    description = "; ".join(f"{label}: {value:g} {chart['unit_en']}"
                            for label, value in zip(chart["labels"], chart["values"]))
    svg = chart_image(chart, "svg").decode("utf-8")
    svg = svg[svg.index("<svg"):].replace("<svg ", '<svg role="img" aria-label="' + html.escape(description, quote=True) + '" ', 1)
    return ('<figure class="data-chart">' + svg + '<figcaption>'
            + html.escape(description) + '. Same values, different y-axis baselines.</figcaption></figure>')


def write_html(episodes: list[dict], destination: Path) -> Path:
    config = course_for_episodes(episodes)
    esc = html.escape
    pages, answers = [], []
    for episode in episodes:
        task = activity(episode)
        questions = "".join(
            f'<li><p>{esc(question["prompt_en"])}</p><div class="answer-line"></div></li>'
            for question in task["questions"])
        pages.append(f'''<article class="worksheet" data-episode="{episode['id']}">
<p class="eyebrow">{config.name_en.upper()} · STAGE {episode['stage']} · SEASON {episode['season']} · LESSON {episode['number']:02}</p>
<h2>{esc(episode['title_en'])}</h2><p class="local-title">{esc(episode['title_zh_TW'])}</p>
<h3>Read</h3><p class="reading">{esc(task['reading_en'])}</p>{chart_html(task)}
<h3>Think and answer</h3><ol>{questions}</ol>
<p class="tip">用文本中的資訊支持回答；寫作任務在下一頁。</p></article>
<article class="writing-sheet worksheet" data-episode="{episode['id']}">
<p class="eyebrow">{config.name_en.upper()} · STAGE {episode['stage']} · SEASON {episode['season']} · LESSON {episode['number']:02} · WRITING</p>
<h2>{esc(episode['title_en'])}</h2><h3>Plan, write, revise</h3>
<p class="prompt">{esc(task['prompt_en'])}</p><p>{esc(task['prompt_zh_TW'])}</p>
<p class="tip">先列重點，再寫草稿；可用虛構人物與情境。</p>
<div class="writing-lines" aria-label="作答空白">{''.join('<div></div>' for _ in range(14))}</div>
<p class="tip">檢查：回應任務每個要求｜理由有支持｜句子連貫｜詞數符合要求。</p></article>''')
        responses = "".join(f'<li>{esc(q["answer_en"])}</li>' for q in task["questions"])
        answers.append(f'''<section class="answer" data-episode="{episode['id']}">
<h3>{episode['number']:02} · {esc(episode['title_en'])}</h3><ol>{responses}</ol>
<p class="answer-label">Example writing</p><p class="model">{esc(task['sample_answer_en'])}</p></section>''')
    content = '''<!doctype html><html lang="zh-Hant"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sunny &amp; Pip · __COURSE_ZH__英文閱讀寫作練習</title><style>
body{font:16px/1.55 system-ui,"Noto Sans TC",sans-serif;color:#23394a;background:#eef2f4;margin:0}
main{max-width:850px;margin:auto;padding:30px}h1,h2,h3{line-height:1.25}h2{margin:6px 0;font-size:27px}
h3{font-size:17px;color:#227b79;margin:22px 0 8px}p{margin:6px 0}.worksheet{background:white;border:1px solid #c8d5dc;border-top:5px solid #227b79;border-radius:8px;margin:28px 0;padding:32px;break-after:page}
.eyebrow{font-size:12px;letter-spacing:.08em;color:#476674}.local-title{color:#476674}.reading{background:#f2f6f6;border-left:3px solid #63aaa2;padding:16px;line-height:1.7}
ol{padding-left:24px}li{margin:9px 0}.answer-line{height:56px;background:repeating-linear-gradient(to bottom,transparent 0,transparent 27px,#acbcc5 28px)}.writing-lines div{height:31px;border-bottom:1px solid #acbcc5}.tip{font-size:12px;color:#566e7c;margin-top:12px}
.answers{break-before:page;margin-top:60px}.answer{background:white;border:1px solid #c8d5dc;border-radius:8px;padding:24px;margin:20px 0;break-inside:avoid}.answer-label{font-size:13px;color:#227b79;font-weight:700}
.reading,.model{white-space:pre-line}
.data-chart{margin:14px 0;break-inside:avoid}.data-chart svg{display:block;width:100%;height:auto}.data-chart figcaption{font-size:11px;color:#476674}
.print{background:#227b79;color:white;border:0;padding:11px 18px;border-radius:6px;cursor:pointer}
@page{size:A4;margin:16mm}
@media print{.answer-line{background:none;height:56px}.answer-line::before,.answer-line::after{content:"";display:block;height:28px;box-sizing:border-box;border-bottom:1px solid #acbcc5}}
@media print{body{background:white;font-size:12px}main{padding:0;max-width:none}.cover{break-after:page}.worksheet{box-sizing:border-box;margin:0;padding:0;border:0;border-top:3px solid #227b79;min-height:0;break-inside:avoid;break-after:page}h1,h2,h3{break-after:avoid}h2{font-size:22px}h3{margin:14px 0 5px}.reading{padding:10px}li,.writing-lines{break-inside:avoid}.writing-lines div{height:27px;box-sizing:border-box}.answers{margin-top:0;break-before:page}.answer{box-sizing:border-box;margin:0;padding:0;border:0;border-radius:0;break-inside:avoid;break-after:page}.answer:last-child{break-after:auto}.print{display:none}}
</style><main><section class="cover"><h1>ENGLISH LAB · __COURSE_ZH__英文練習</h1><p>先看影片，再獨立閱讀與作答。每集三題理解或分析，以及一項有規定詞數的寫作任務。</p>
<p>示例答案在後方；開放式題目可有其他合理答案。這份材料用來練習，不作正式程度認證。</p><button class="print" onclick="window.print()">列印練習</button></section>'''
    content = content.replace("__COURSE_ZH__", config.name_zh)
    content += "".join(pages)
    content += '<div class="answers"><h1>Answers and Writing Examples</h1><p>先完成練習再核對；寫作例答示範表達方式，不是唯一正解。</p>'
    content += "".join(answers) + '</div></main></html>'
    path = destination / "Practice.html"
    path.write_text(content, encoding="utf-8")
    return path


def write_pdf(episodes: list[dict], destination: Path) -> Path:
    config = course_for_episodes(episodes)
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.utils import ImageReader, simpleSplit

    configured = os.environ.get("ADULT_ENGLISH_PRACTICE_FONT") or os.environ.get(f"{config.key.upper()}_PRACTICE_FONT")
    candidates = ([Path(configured)] if configured else []) + [
        parent / ".fonts/NotoSansTC-Regular.ttf" for parent in (destination, *destination.parents)]
    font_path = next((path for path in candidates if path.is_file()), None)
    if font_path is None:
        raise ValueError("Set ADULT_ENGLISH_PRACTICE_FONT to a static Traditional Chinese TrueType font")
    font = "AdultEnglishPractice"
    if font not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(font, str(font_path)))
    path = destination / "Practice.pdf"
    width, height = A4
    c = canvas.Canvas(str(path), pagesize=A4)
    c.setTitle(f"Sunny & Pip - {config.name_en} English Practice")
    c.setAuthor("Sunny & Pip English course")
    page = 0
    ink, teal = (.14, .23, .30), (.13, .48, .47)

    def split(value: str, size: float, available: float, chinese: bool) -> list[str]:
        if not chinese:
            result = []
            for paragraph in value.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
                result.extend(simpleSplit(paragraph, font, size, available) if paragraph else [""])
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
    y = text(f"{config.name_en} English Practice", 46, height - 112, 22)
    y = text(f"{config.name_zh}英文閱讀寫作｜{len(episodes)} 集", 46, y - 22, 18, True)
    for note in ("每集：閱讀一篇短文、回答三題，再完成寫作任務。",
                 f"閱讀 {config.reading_range[0]}–{config.reading_range[1]} 詞，寫作 {config.writing_range[0]}–{config.writing_range[1]} 詞。",
                 "依主題與先備能力選擇進度，逐步完成四個學習階段。",
                 "先獨立作答；需要時回看影片中的例句與說明。",
                 "答案與寫作示例放在後方，請完成後再核對。",
                 "寫作可用虛構人物與情境，不需要提供真實個人資料。",
                 "開放式題目可有其他合理答案，請用文本證據支持想法。",
                 "這套材料用於情境練習，不代表正式英語程度或專業認證。"):
        y = text(note, 46, y - 18, 13, True)
    text("Lessons " + ", ".join(f"{episode['number']:02}" for episode in episodes), 46, y - 25, 10)
    footer()

    for episode in episodes:
        task = activity(episode)
        c.setFillColorRGB(*teal)
        y = text(f"{config.name_en.upper()}  /  STAGE {episode['stage']}  /  SEASON {episode['season']}  /  LESSON {episode['number']:02}",
                 46, height - 47, 10)
        c.setFillColorRGB(*ink)
        y = text(episode["title_en"], 46, y - 8, 19)
        y = text(episode["title_zh_TW"], 46, y - 3, 12, True)
        y = heading("READ", y)
        y = text(task["reading_en"], 46, y, 12)
        if task.get("chart"):
            chart = task["chart"]
            chart_height = (width - 92) * 2.05 / 7
            c.drawImage(ImageReader(io.BytesIO(chart_image(chart, "png"))),
                        46, y - chart_height, width=width - 92, height=chart_height)
            y -= chart_height + 8
            description = "; ".join(f"{label}: {value:g} {chart['unit_en']}"
                                    for label, value in zip(chart["labels"], chart["values"]))
            y = text(chart["title_en"] + ": " + description + ".", 46, y, 9)
        y = heading("THINK AND ANSWER", y)
        for number, question in enumerate(task["questions"], 1):
            y = text(f"{number}. {question['prompt_en']}", 46, y, 11.5)
            rule(y - 11)
            rule(y - 34)
            y -= 48
        footer()
        c.setFillColorRGB(*teal)
        y = text(f"{config.name_en.upper()}  /  STAGE {episode['stage']}  /  SEASON {episode['season']}  /  LESSON {episode['number']:02}  /  WRITING",
                 46, height - 47, 10)
        c.setFillColorRGB(*ink)
        y = text(episode["title_en"], 46, y - 8, 19)
        y = heading("WRITE", y)
        y = text(task["prompt_en"], 46, y, 12)
        y = text(task["prompt_zh_TW"], 46, y - 2, 10.5, True)
        y = text("先列重點，再寫草稿。請回應題目每個要求，並用理由或文本資訊支持。", 46, y - 14, 10.5, True)
        if y < 475:
            raise ValueError(f"{episode['id']}: not enough room for fourteen writing lines")
        for offset in range(14):
            rule(y - 17 - offset * 26)
        text("自我檢查：任務要點完整｜理由有支持｜句子連貫｜詞數符合要求", 46, 70, 10, True)
        footer()

    for episode in episodes:
        c.setFillColorRGB(*teal)
        y = text("Answers and Writing Examples", 46, height - 47, 18)
        c.setFillColorRGB(*ink)
        y = text("先作答再核對。寫作與開放式題目可有其他合理答案。", 46, y - 3, 10.5, True)
        task = activity(episode)
        c.setFillColorRGB(*teal)
        y = text(f"{episode['number']:02} - {episode['title_en']}", 46, y - 15, 16)
        c.setFillColorRGB(*ink)
        y = heading("READING RESPONSES", y)
        for number, question in enumerate(task["questions"], 1):
            y = text(f"{number}. {question['answer_en']}", 46, y - 8, 12)
        y = heading("EXAMPLE WRITING", y - 10)
        y = text(task["sample_answer_en"], 46, y, 12)
        y = heading("REVIEW YOUR OWN RESPONSE", y - 14)
        for note in ("檢查你的答案是否回應每個要求，而不是只比對示例字句。",
                     "確認推論有文本支持；區分作者觀點、證據與自己的分析。",
                     "寫作可有不同立場與例子，只要理由合理且符合任務。"):
            y = text(note, 46, y - 5, 10.5, True)
        footer()
    c.save()
    return path


def write_practice(episodes: list[dict], destination: Path) -> list[Path]:
    if not episodes:
        raise ValueError("Practice material needs at least one episode")
    destination.mkdir(parents=True, exist_ok=True)
    return [write_html(episodes, destination), write_pdf(episodes, destination)]
