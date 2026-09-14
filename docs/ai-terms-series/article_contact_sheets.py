"""Build four-article table screenshot sheets after render_articles.mjs completes.

This script does not render articles or assert that screenshots are current.
Use --not-before with the fresh render's start time to reject older inputs.
The output manifest binds every sheet to the exact screenshot bytes it used.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
INPUT = HERE / "qa" / "articles"
OUTPUT = HERE / "qa" / "layout-sheets"
GAP = 16
LABEL_HEIGHT = 72
SHEET_HEADING_HEIGHT = 52


def parse_timestamp(value: str) -> datetime:
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise argparse.ArgumentTypeError("Use an ISO 8601 timestamp with timezone.") from error
    if result.tzinfo is None:
        raise argparse.ArgumentTypeError("The timestamp must include a timezone.")
    return result.astimezone(timezone.utc)


def font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size)
    raise RuntimeError("A readable Arial or DejaVu Sans font is required.")


def is_uniform(image: Image.Image) -> bool:
    return all(low == high for low, high in image.getextrema())


def prepare_source(term: dict, viewport: str, cutoff: datetime | None, crop_width: int) -> dict:
    source = INPUT / f"{term['slug']}-{viewport}-table.png"
    stat = source.stat()
    modified = datetime.fromtimestamp(stat.st_mtime, timezone.utc)
    if cutoff is not None and modified < cutoff:
        raise ValueError(f"Screenshot predates --not-before: {source.name}")
    data = source.read_bytes()
    with Image.open(io.BytesIO(data)) as original:
        original.load()
        picture = original.convert("RGB")
    width, height = picture.size
    expected = (375, 812) if viewport == "mobile" else (1440, 1000)
    if (width, height) != expected:
        raise ValueError(f"Unexpected screenshot size for {source.name}: {picture.size}; expected {expected}")
    crop = (0, 0, width, height)
    if viewport == "desktop" and 0 < crop_width < width:
        left = (width - crop_width) // 2
        right = left + crop_width
        # Retain every nonuniform margin, including accidental page overflow.
        # The normal 768px article wrapper fits in the default 800px crop.
        if not is_uniform(picture.crop((0, 0, left, height))) or not is_uniform(
            picture.crop((right, 0, width, height))
        ):
            raise ValueError(
                f"Desktop margins contain content: {source.name}; inspect it or use --desktop-crop-width 0."
            )
        crop = (left, 0, right, height)
        picture = picture.crop(crop)
    return {
        "picture": picture,
        "id": term["id"],
        "slug": term["slug"],
        "viewport": viewport,
        "source": str(source.relative_to(HERE)).replace("\\", "/"),
        "source_sha256": hashlib.sha256(data).hexdigest(),
        "source_modified_utc": modified.isoformat(),
        "source_size": [width, height],
        "crop_box": list(crop),
        "display_size": list(picture.size),
    }


def draw_slug(draw: ImageDraw.ImageDraw, slug: str, x: int, y: int, width: int, face) -> None:
    remaining = slug
    for line in range(2):
        take = len(remaining)
        while take > 0 and draw.textlength(remaining[:take], font=face) > width:
            take -= 1
        if take == 0:
            raise ValueError(f"Label cannot fit: {slug}")
        draw.text((x, y + line * 18), remaining[:take], font=face, fill="#102A2B")
        remaining = remaining[take:]
        if not remaining:
            return
    raise ValueError(f"Slug needs more than two label lines: {slug}")


def make_sheet(items: list[dict], viewport: str, page_number: int, heading_font, label_font) -> dict:
    columns, rows = (4, 1) if viewport == "mobile" else (2, 2)
    tile_width = max(item["picture"].width for item in items)
    tile_height = max(item["picture"].height for item in items) + LABEL_HEIGHT
    canvas = Image.new(
        "RGB",
        (GAP + columns * (tile_width + GAP), SHEET_HEADING_HEIGHT + GAP + rows * (tile_height + GAP)),
        "#E8EBED",
    )
    draw = ImageDraw.Draw(canvas)
    first, last = items[0]["id"], items[-1]["id"]
    draw.text(
        (GAP, 14),
        f"Article table layout / {viewport} / {first:02d}-{last:02d} / native screenshot pixels",
        font=heading_font,
        fill="#102A2B",
    )
    records = []
    for index, item in enumerate(items):
        x = GAP + (index % columns) * (tile_width + GAP)
        y = SHEET_HEADING_HEIGHT + GAP + (index // columns) * (tile_height + GAP)
        draw.rectangle((x, y, x + tile_width - 1, y + LABEL_HEIGHT - 1), fill="white")
        draw.text((x + 10, y + 8), f"{item['id']:02d} / {viewport}", font=label_font, fill="#102A2B")
        draw_slug(draw, item["slug"], x + 10, y + 28, tile_width - 20, label_font)
        canvas.paste(item["picture"], (x, y + LABEL_HEIGHT))
        record = {key: value for key, value in item.items() if key != "picture"}
        record["sheet_position"] = [x, y + LABEL_HEIGHT]
        records.append(record)
    name = f"{viewport}-table-{page_number:02d}.png"
    output = OUTPUT / name
    canvas.save(output, optimize=True)
    return {
        "file": name,
        "viewport": viewport,
        "size": list(canvas.size),
        "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "articles": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--not-before", type=parse_timestamp, help="Reject screenshots older than this render start time.")
    parser.add_argument("--viewport", choices=["both", "mobile", "desktop"], default="both")
    parser.add_argument(
        "--desktop-crop-width", type=int, default=800,
        help="Crop only uniform desktop side margins to this width; 0 keeps the full 1440px viewport.",
    )
    args = parser.parse_args()
    if args.desktop_crop_width < 0 or 0 < args.desktop_crop_width < 768:
        parser.error("--desktop-crop-width must be 0 or at least the 768px article wrapper width.")
    catalogue = json.loads((HERE / "catalogue.json").read_text(encoding="utf-8"))
    terms = [{"id": item["id"], "slug": item["slug"]} for item in catalogue["terms"]]
    terms += [{"id": 82, "slug": "ai-terms-index"}, {"id": 83, "slug": "ai-glossary-50-terms"}]
    if len(terms) != 83 or len({term["slug"] for term in terms}) != 83:
        raise ValueError("Expected 81 catalogue articles followed by index and glossary.")
    viewports = ["mobile", "desktop"] if args.viewport == "both" else [args.viewport]
    # Preflight the complete selected input set before writing any output sheet.
    prepared = {
        viewport: [prepare_source(term, viewport, args.not_before, args.desktop_crop_width) for term in terms]
        for viewport in viewports
    }
    heading_font, label_font = font(18), font(14)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sheets = []
    for viewport, items in prepared.items():
        for start in range(0, len(items), 4):
            sheets.append(make_sheet(items[start:start + 4], viewport, start // 4 + 1, heading_font, label_font))
    report = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "not_before_utc": args.not_before.isoformat() if args.not_before else None,
        "scope": "Table-region viewport screenshots; this manifest does not constitute visual review.",
        "order": "catalogue.terms (81), ai-terms-index, ai-glossary-50-terms",
        "rendering": "No screenshot scaling. Mobile: four columns. Desktop: 2 by 2, uniform side margins optionally cropped.",
        "articles": len(terms),
        "screenshots": sum(len(items) for items in prepared.values()),
        "sheets": sheets,
    }
    manifest = OUTPUT / "manifest.json"
    temporary = manifest.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(manifest)
    print(json.dumps({"articles": len(terms), "screenshots": report["screenshots"], "sheets": len(sheets), "manifest": str(manifest)}))


if __name__ == "__main__":
    main()
