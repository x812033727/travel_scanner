"""Generate original synthetic inputs and independently downloadable lab packages."""
import json
import shutil
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXAMPLES = HERE / "examples"


def put(name: str, value) -> None:
    file = EXAMPLES / name
    file.parent.mkdir(parents=True, exist_ok=True)
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)
    file.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def build() -> None:
    for number in range(1, 21):
        put(f"78/documents/doc{number:02d}.md", f"# 海風活動 {number:02d}\n\n第 {number} 組活動，預計 {number + 5} 人，日期待確認。\n\n## 來源\n作者建立的合成資料。")
    for number in (1, 2):
        put(f"79/docs/doc{number:02d}.md", (EXAMPLES / f"78/documents/doc{number:02d}.md").read_text(encoding="utf-8"))
    shutil.copyfile(EXAMPLES / "78/pipeline.py", EXAMPLES / "79/pipeline.py")
    shutil.copyfile(EXAMPLES / "78/no-tools.toml", EXAMPLES / "79/no-tools.toml")
    finding = {"file": "src/limit.mjs", "line": 1, "quote": "export const limit = (n) => Math.min(10, n);",
               "check": "lower-bound", "recommendation": "Add a lower bound of zero."}
    docs_finding = {"file": "docs/limits.md", "line": 2, "quote": "輸入最小值為 0，最大值為 100。",
                    "check": "upper-bound-documentation", "recommendation": "Change the documented upper bound to 10."}
    put("77/fixture-code-report.json", {"agent": "authored-code-fixture", "status": "complete", "findings": [finding]})
    put("77/fixture-docs-report.json", {"agent": "authored-docs-fixture", "status": "complete", "findings": [docs_finding]})
    put("77/report-contract.json", {"note": "The two fixture reports are authored examples, not generated agent results.", "required": ["agent", "status", "findings"], "findingFields": ["file", "line", "quote", "check", "recommendation"]})
    for number in range(1, 11):
        target = f"doc{number % 10 + 1:02d}.md#details" if number != 3 else "missing.md#details"
        text = f'# 文件 {number:02d}\n\n<a id="details"></a>\n\n第 {number} 份合成作業說明；修訂前需核對來源。\n\n[下一份]({target})\n\n## 來源\n作者提供的十份本機範例。\n'
        put(f"80/documents/doc{number:02d}.md", text)
    original = (EXAMPLES / "80/documents/doc03.md").read_text(encoding="utf-8")
    put("80/reference-proposals.json", {"doc03.md": original.replace("missing.md#details", "doc04.md#details")})
    put("80/bad-proposals.json", {"doc03.md": original.replace("missing.md#details", "invented.md#details")})
    put("80/docs-plan.toml", '''description = "Propose a bounded document correction; no automatic write."
prompt = """
檢查 documents/doc01.md 到 doc10.md 的本機連結，只提出有資料可追查的修正。
回傳 JSON 物件，鍵是需修改的 docNN.md，值是該篇完整修訂內容。
找不到目標請說明，不建立網址或資料；不寫入原檔。參數：{{args}}
"""''')
    put("80/run-log.md", "# 維護執行紀錄\n\nCLI／模型版本：\n實際輸入與命令：\n是否 fixture：\n已知斷鏈：\n模型實際輸出路徑：\n檢查結果：\n人工確認及 Git 差異：\n")
    license_text = (HERE.parent / "md/examples/69/LICENSE.txt").read_text(encoding="utf-8")
    for number in range(75, 81):
        put(f"{number}/LICENSE.txt", license_text)
        put(f"{number}/README.md", f"# Gemini 深入教學 {number} 練習包\n\n2026-09-14，Mokaair 原創，MIT 授權。\n\n先複製到新的教材資料夾，依網站文章操作；不要直接放入正式專案的 .gemini 或 .github。本機固定輸入、作者參考答案與模型回答分開標示。沒有測試帳號也可以執行 fixture；它不會呼叫模型。\n\nCLI 固定 0.59.0；第 75 篇採 MCP Python SDK 2.2.0，請先安裝 requirements.txt。其他篇的 Python 程式使用標準函式庫。\n")


def package() -> None:
    for number in range(75, 81):
        with zipfile.ZipFile(EXAMPLES / f"lesson-{number}.zip", "w", zipfile.ZIP_DEFLATED) as archive:
            for file in sorted((EXAMPLES / str(number)).rglob("*")):
                if not file.is_file() or any(part in {"__pycache__", ".venv", ".git"} for part in file.parts):
                    continue
                info = zipfile.ZipInfo(file.relative_to(EXAMPLES).as_posix(), (2026, 9, 14, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, file.read_bytes())
    with zipfile.ZipFile(EXAMPLES / "automation-verification.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        files = [HERE / "verify-cli.mjs", HERE / "verification/test_exercises.py", HERE / "verification/README.md"]
        for number in range(75, 81):
            files.extend((EXAMPLES / str(number)).rglob("*"))
        for file in sorted(files):
            if not file.is_file() or any(part in {"__pycache__", ".venv", ".git"} for part in file.parts):
                continue
            info = zipfile.ZipInfo(file.relative_to(HERE).as_posix(), (2026, 9, 14, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, file.read_bytes())


if __name__ == "__main__":
    build()
    package()
