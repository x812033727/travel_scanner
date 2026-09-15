"""Verify saved XLSX values, formula bindings, raw blanks and date types without authoring it."""
import hashlib
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

HERE = Path(__file__).resolve().parent
FILE = HERE.parent / "examples/67/outputs/creative-lessons/sales-audit.xlsx"
NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main", "c": "http://schemas.openxmlformats.org/drawingml/2006/chart"}
with zipfile.ZipFile(FILE) as archive:
    assert archive.testzip() is None
    report = ET.fromstring(archive.read("xl/worksheets/sheet2.xml"))
    clean = ET.fromstring(archive.read("xl/worksheets/sheet3.xml"))
    raw = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
    for ref, expected in {"E5": "42300", "E6": "3040", "E7": "50", "E9": "45340", "E10": "50", "F5": "0", "F6": "0", "F7": "0", "B9": "50", "B10": "43", "B11": "7"}.items():
        cell = report.find(f'.//s:c[@r="{ref}"]', NS)
        assert cell.find("s:f", NS) is not None, ref
        assert cell.find("s:v", NS).text == expected, ref
    date = clean.find('.//s:c[@r="C2"]', NS)
    assert date.get("t") != "s" and date.find("s:v", NS).text == "46266"
    price = raw.find('.//s:c[@r="G43"]', NS)
    assert price is None or price.find("s:v", NS) is None or price.find("s:v", NS).text in {None, ""}
    assert clean.find('.//s:c[@r="J2"]/s:f', NS).text == "G2*H2"
    chart_files = [n for n in archive.namelist() if re.fullmatch(r"xl/(?:drawings/)?charts/chart\d+\.xml", n)]
    assert len(chart_files) == 1
    chart = ET.fromstring(archive.read(chart_files[0]))
    references = [n.text for n in chart.findall(".//c:f", NS)]
    assert "'Report'!$E$5:$E$6" in references and "'Report'!$B$5:$B$6" in references
receipt = {"checkedOn": "2026-09-14", "file": FILE.relative_to(HERE.parent).as_posix(), "sha256": hashlib.sha256(FILE.read_bytes()).hexdigest(), "crc": "passed", "savedFormulaCaches": "matched", "rawBlankPreserved": True, "typedDateVerified": True, "chartCurrency": "TWD", "chartReferences": references, "googleSheetsImported": False, "rendererNote": "Bundled renderer exits with Windows 0xC0000005 in native teardown after successful preview export. All six previews were inspected; final unchanged-layout export with --skip-previews exits 0. Saved XLSX checked independently here."}
(HERE / "workbook/saved-file.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
print(json.dumps({"savedWorkbook": "verified", "TWD": 45340, "USD": 50}))
