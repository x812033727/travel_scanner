#!/usr/bin/env python3
"""Rebuild the thumbnail subject from the two checked-in ForTy 2020 ROIs.

Run with Python 3, numpy, matplotlib and Pillow installed. No network requests,
basemap, invented pixels, resampling, or edits to the source JSON/SVG files.
Only thumbnail-grid.png and thumbnail-grid.json are written next to this file.
"""

from __future__ import annotations

import hashlib
import io
import json
import platform
import xml.etree.ElementTree as ET
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle
from PIL import Image


HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
PNG = HERE / "thumbnail-grid.png"
MANIFEST = HERE / "thumbnail-grid.json"
DOI = "https://doi.org/10.25452/figshare.plus.32288616.v1"
CLASS_NAMES = [
    "PrimaryForest",
    "NaturallyRegeneratingForest",
    "PlantedForest",
    "PlantationForest",
    "TreeCropsAndAgroforestry",
    "OtherLand",
]
# Same class-ID order and palette as the existing ROI SVGs and
# work/ai-tech-next/forty-demo/render_real_data_figure.py. The SVG fills are
# independently compared with the recomputed classes below.
COLORS = ["#1B7837", "#7FBF7B", "#1D91C0", "#E65FA9", "#E6AB02", "#FDE278"]
DESIGN_WIDTH, DESIGN_HEIGHT, DPI = 720, 680, 200
SCALE = DPI / 100
LAYOUT = {
    "A": {"left": 32, "top": 80, "size": 176, "red_frame_pt": 3.0},
    "B": {"left": 232, "top": 172, "size": 456, "red_frame_pt": 3.5},
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_roi(label: str, filename: str) -> dict:
    path = DATA / filename
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert doc["baseline_year"] == 2020
    roi = doc["roi"]
    if label == "A":
        bands = np.asarray(roi["stored_five_bands_row_major"], dtype=np.int64)
        transform = doc["metadata"]["window_transform"]
        row, col = doc["sample"]["roi_pixel"]["row"], doc["sample"]["roi_pixel"]["col"]
        selected = doc["sample"]
        original_classes = roi["class_ids_row_major"]
        original_other = roi["derived_other_row_major"]
        source_pixel = selected["source_pixel"]
    else:
        bands = np.asarray(roi["five_bands"], dtype=np.int64)
        transform = roi["transform"]
        selected = doc["selected_pixel"]
        # B uses the same source raster as A. Derive its ROI row/column from
        # the actual global source pixel and the ROI affine, not its SVG.
        source_affine = json.loads((DATA / "actual-roi-result.json").read_text())["metadata"]["transform"]
        global_row0 = int(round((transform[5] - source_affine[5]) / source_affine[4]))
        global_col0 = int(round((transform[2] - source_affine[2]) / source_affine[0]))
        row, col = selected["row"] - global_row0, selected["col"] - global_col0
        source_pixel = {"row": selected["row"], "col": selected["col"]}
        original_classes = roi["class_ids"]
        original_other = roi["other"]
    assert bands.shape == (5, 10, 10)
    assert transform[0] == transform[4] == 10 and transform[1] == transform[3] == 0
    assert np.all((bands >= 0) & (bands <= 250)), "Invalid / nodata bands"
    other = 250 - bands.sum(axis=0)
    assert np.all((other >= 0) & (other <= 250))
    six = np.concatenate([bands, other[None]], axis=0)
    assert np.all(six.sum(axis=0) == 250)
    classes = six.argmax(axis=0) + 1  # numpy returns the first maximum.
    np.testing.assert_array_equal(other, original_other)
    np.testing.assert_array_equal(classes, original_classes)
    assert (row, col) == (5, 5)
    selected_six = six[:, row, col]
    expected = [0, 248, 0, 0, 0, 2] if label == "A" else [0, 86, 0, 1, 77, 86]
    assert selected_six.tolist() == expected
    assert int(classes[row, col]) == 2

    svg_path = HERE / f"roi-{label.lower()}-grid.svg"
    svg = ET.fromstring(svg_path.read_text())
    cells = [node for node in svg.iter() if node.tag.endswith("rect")
             and node.get("width") == "46" and node.get("height") == "46"
             and node.get("fill", "").startswith("#")]
    assert len(cells) == 100
    for index, cell in enumerate(cells):
        r, c = divmod(index, 10)
        assert cell.get("fill").upper() == COLORS[int(classes[r, c]) - 1]
        assert float(cell.get("x")) == 540 + c * 46
        assert float(cell.get("y")) == 180 + (9 - r) * 46

    return {
        "label": label, "path": path, "svg_path": svg_path,
        "classes": classes, "six": six, "row": row, "col": col,
        "source_pixel": source_pixel, "transform": transform,
    }


def main() -> None:
    rois = [read_roi("A", "actual-roi-result.json"),
            read_roi("B", "actual-uncertain-roi-result.json")]
    font_candidates = [
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    ]
    font_path = next((p for p in font_candidates if p.is_file()), None)
    if font_path is None:
        raise RuntimeError("Install Noto Sans CJK; the Chinese sample label must render.")
    font = FontProperties(fname=str(font_path))
    fig = plt.figure(figsize=(7.2, 6.8), dpi=DPI, facecolor="none")
    colormap = ListedColormap(COLORS)
    norm = BoundaryNorm(np.arange(0.5, 7), colormap.N)
    text_outline = [pe.withStroke(linewidth=1.4, foreground="#173731")]

    def text(left: float, top: float, value: str, size: float, align="left") -> None:
        fig.text(left / DESIGN_WIDTH, 1 - top / DESIGN_HEIGHT, value,
                 ha=align, va="top", fontsize=size, fontproperties=font,
                 color="#FFFFFF", path_effects=text_outline)

    text(32, 18, "A", 32)
    text(232, 110, "B", 32)
    text(688, 35, "2020", 27, "right")
    text(32, 285, "兩處取樣", 15)

    for roi in rois:
        layout = LAYOUT[roi["label"]]
        left, top, size = layout["left"], layout["top"], layout["size"]
        ax = fig.add_axes([left / DESIGN_WIDTH,
                           (DESIGN_HEIGHT - top - size) / DESIGN_HEIGHT,
                           size / DESIGN_WIDTH, size / DESIGN_HEIGHT])
        ax.imshow(roi["classes"], origin="lower", cmap=colormap, norm=norm,
                  interpolation="nearest", extent=(-0.5, 9.5, -0.5, 9.5))
        # Light separators preserve the exact class-colour interiors.
        for edge in np.arange(-0.5, 10, 1):
            ax.axvline(edge, color="#FFFFFF", linewidth=0.65, zorder=2)
            ax.axhline(edge, color="#FFFFFF", linewidth=0.65, zorder=2)
        ax.add_patch(Rectangle((roi["col"] - 0.5, roi["row"] - 0.5), 1, 1,
                               fill=False, edgecolor="#EA4335",
                               linewidth=layout["red_frame_pt"],
                               joinstyle="miter", zorder=5))
        ax.set_xlim(-0.5, 9.5)
        ax.set_ylim(-0.5, 9.5)
        ax.set_aspect("equal")
        ax.set_axis_off()

    # Keep the complete 1440×1360 transparent subject; no tight-bbox cropping.
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=DPI, transparent=True,
                metadata={"Title": "ForTy 2020 — two separate ROI samples",
                          "Author": "Data: Neumann et al. (2026); adaptation: Mokaair",
                          "Description": "Real 10x10 ROI grids; residual OtherLand; first argmax; "
                                         "row 0 at bottom. CC BY 4.0. " + DOI})
    plt.close(fig)
    image_bytes = buffer.getvalue()
    with Image.open(io.BytesIO(image_bytes)) as image:
        assert image.size == (1440, 1360)
        assert image.mode == "RGBA"
        # Verify every cell interior in the actual rendered PNG, including
        # the y reversal and both green selected cells.
        for roi in rois:
            layout = LAYOUT[roi["label"]]
            cell = layout["size"] / 10
            for row in range(10):
                for col in range(10):
                    x = int(SCALE * (layout["left"] + (col + 0.5) * cell))
                    y = int(SCALE * (layout["top"] + (9.5 - row) * cell))
                    color = COLORS[int(roi["classes"][row, col]) - 1]
                    rgb = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))
                    assert image.getpixel((x, y)) == (*rgb, 255)
    PNG.write_bytes(image_bytes)

    manifest = {
        "asset": PNG.name,
        "sha256": sha256(PNG),
        "dimensions": {"width": 1440, "height": 1360, "transparent": True},
        "source": {
            "author": "Neumann et al. (2026)",
            "title": "Forest Typology 2020 (v1)",
            "doi": DOI,
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
        },
        "adaptation": {
            "author": "Mokaair",
            "changes": ["two separate 10×10 ROI crops", "OtherLand = 250 − sum(five stored bands)",
                        "first maximum in the fixed six-class order", "original class-colour redraw",
                        "unequal-size A/B composition", "red outlines on the actual selected pixels"],
            "no_satellite_basemap": True,
            "not_adjacent": True,
            "labels": ["A", "B", "2020", "兩處取樣"],
        },
        "inputs": {str(roi[key].relative_to(HERE.parent)): sha256(roi[key])
                   for roi in rois for key in ("path", "svg_path")},
        "generator": {"path": Path(__file__).name, "sha256": sha256(Path(__file__)),
                      "command": "python docs/videos/forty-forest-map/assets/thumbnail-grid.py"},
        "render": {"python": platform.python_version(), "numpy": np.__version__,
                   "matplotlib": matplotlib.__version__, "dpi": DPI,
                   "font_path": str(font_path), "font_sha256": sha256(font_path),
                   "interpolation": "nearest", "origin": "lower",
                   "orientation": "positive affine Y; row 0 at bottom; columns increase rightward",
                   "design_canvas": [DESIGN_WIDTH, DESIGN_HEIGHT], "layout": LAYOUT},
        "classes": [{"id": i + 1, "name": name, "color": COLORS[i]}
                    for i, name in enumerate(CLASS_NAMES)],
        "rois": [{"label": roi["label"], "width": 10, "height": 10,
                  "window_transform": roi["transform"],
                  "class_ids_source_row_major": roi["classes"].tolist(),
                  "source_pixel": roi["source_pixel"],
                  "selected_roi_pixel": {"row": roi["row"], "col": roi["col"]},
                  "selected_six_stored_values": roi["six"][:, roi["row"], roi["col"]].tolist(),
                  "selected_class_id": int(roi["classes"][roi["row"], roi["col"]]),
                  "selected_tied_maximum_count": int(np.sum(roi["six"][:, roi["row"], roi["col"]]
                                                           == roi["six"][:, roi["row"], roi["col"]].max()))}
                 for roi in rois],
        "validation": {"both_grids_recomputed_from_five_bands": True,
                       "computed_other_and_classes_match_checked_in_JSON": True,
                       "all_200_colours_and_positions_match_existing_SVG": True,
                       "all_200_rendered_cell_centres_checked": True,
                       "both_selected_pixels_display_same_original_green": True},
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"png": str(PNG), "sha256": manifest["sha256"],
                      "bytes": len(image_bytes), "dimensions": [1440, 1360]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
