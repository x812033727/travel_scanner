"""YouTube thumbnails (1280x720) for the 3D donghua cut, drawn on a first frame.

  python thumb-dh.py <frame.png> <out.jpg> <headline> <badge> [--cc]

Short-drama look: the frame slightly lifted, a dark band rising from the bottom, the series name
top-left, a red episode badge top-right, the headline in thick yellow strokes at the bottom
(a newline in the headline splits it into two lines), and an optional "CC字幕" tag.
"""
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

W, H = 1280, 720
BOLD = "C:/Windows/Fonts/msjhbd.ttc"
SERIES = "種田娶妻打天下"


def font(size):
    return ImageFont.truetype(BOLD, size)


def fit(draw, text, start, max_w):
    size = start
    while size > 40:
        f = font(size)
        if draw.textbbox((0, 0), text, font=f, stroke_width=size // 9)[2] <= max_w:
            return f
        size -= 4
    return font(size)


def main():
    src, out, headline, badge = sys.argv[1:5]
    cc = "--cc" in sys.argv[5:]
    img = Image.open(src).convert("RGB")
    # Cover-crop to 16:9 and lift contrast and colour a little, as thumbnails read small.
    r = max(W / img.width, H / img.height)
    img = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
    left, top = (img.width - W) // 2, (img.height - H) // 2
    img = img.crop((left, top, left + W, top + H))
    img = ImageEnhance.Contrast(img).enhance(1.12)
    img = ImageEnhance.Color(img).enhance(1.15)
    # Bottom band for the headline, a light one at the top for the series name.
    shade = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(shade)
    for y in range(H):
        a = 0
        if y > H * 0.52:
            a = int(215 * ((y - H * 0.52) / (H * 0.48)) ** 1.2)
        elif y < 120:
            a = int(120 * (1 - y / 120))
        sd.line([(0, y), (W, y)], fill=a)
    img = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), img, shade)
    d = ImageDraw.Draw(img)
    # Series name, top-left, gold.
    d.text((32, 22), SERIES, font=font(54), fill=(243, 210, 122), stroke_width=5, stroke_fill=(30, 12, 0))
    # Episode badge, top-right, red.
    bf = font(52)
    bw = d.textbbox((0, 0), badge, font=bf)[2]
    d.rounded_rectangle([W - bw - 70, 20, W - 24, 100], radius=14, fill=(206, 24, 30), outline=(255, 236, 160), width=4)
    d.text((W - bw - 47, 28), badge, font=bf, fill=(255, 255, 255))
    # Headline, bottom, yellow with a heavy black stroke and a soft glow under it.
    lines = headline.split("\\n") if "\\n" in headline else headline.split("\n")
    y = H - 34
    for line in reversed(lines):
        f = fit(d, line, 132 if len(lines) == 1 else 112, W - 80)
        box = d.textbbox((0, 0), line, font=f, stroke_width=f.size // 9)
        y -= box[3] - box[1] + 6
        glow = Image.new("L", (W, H), 0)
        ImageDraw.Draw(glow).text((40, y - box[1]), line, font=f, fill=200, stroke_width=f.size // 5)
        img.paste((0, 0, 0), mask=glow.filter(ImageFilter.GaussianBlur(10)))
        d = ImageDraw.Draw(img)
        d.text((40, y - box[1]), line, font=f, fill=(255, 226, 64), stroke_width=f.size // 9, stroke_fill=(0, 0, 0))
    if cc:
        cf = font(40)
        cw = d.textbbox((0, 0), "CC字幕", font=cf)[2]
        d.rounded_rectangle([W - cw - 60, 116, W - 24, 176], radius=10, fill=(255, 255, 255))
        d.text((W - cw - 42, 120), "CC字幕", font=cf, fill=(20, 20, 20))
    img.save(out, quality=92)


main()
