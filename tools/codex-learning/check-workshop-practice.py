"""Verify the final workshops in temporary folders and build the CSV download."""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "docs/codex-learning/examples"
modules = {id_: json.loads((ROOT / f"docs/codex-learning/deep/modules/{id_}.json").read_text(encoding="utf-8")) for id_ in [12, 31, 32, 58, 59, 60]}
checks = []
git_env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
git_env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0")


def code(id_, label):
    return next(b["code"] for b in modules[id_]["blocks"] if b.get("type") == "code" and b["label"][0] == label)


def run(command, cwd, *, expected=0):
    result = subprocess.run(command, cwd=cwd, env=git_env if command[0] == "git" else None, capture_output=True, encoding="utf-8", timeout=30, check=False)
    assert result.returncode == expected, result.stdout + result.stderr
    return result


def node_tests(folder, names, passes, fails):
    result = run(["node", "--test", "--test-reporter=tap", *names], folder, expected=1 if fails else 0)
    assert re.search(rf"# pass {passes}\b", result.stdout) and re.search(rf"# fail {fails}\b", result.stdout), result.stdout


files = {name: (EXAMPLES / name).read_bytes() for name in ["clean_contacts.py", "test_clean_contacts.py", "contacts.csv"]}
for name, label in [("clean_contacts.py", "clean_contacts.py（完整參考）"), ("test_clean_contacts.py", "test_clean_contacts.py"), ("contacts.csv", "contacts.csv（保留測試空白）")]:
    assert files[name].decode("utf-8").replace("\r\n", "\n") == code(32, label)
files["contacts-unicode.csv"] = code(32, "contacts-unicode.csv").encode("utf-8")
files["README.md"] = """# CSV practice / CSV 練習 / CSV 练习 / CSV 実習 / CSV 실습

Reference files use fictional data only. Keep contacts.csv unchanged and use a new output filename each time.
參考程式只使用虛構資料。保留 contacts.csv，每次指定新的輸出檔名。完整五語操作與限制見下方教學。
参考程序只使用虚构数据。保留 contacts.csv，每次指定新的输出文件名。完整五语操作与限制见下方教程。
架空資料だけの参考実装です。contacts.csv を保持し、毎回新しい出力名を使います。全手順と制限は下記の教材にあります。
가상 자료만 쓰는 참고 코드입니다. contacts.csv를 보존하고 매번 새 출력 이름을 사용하세요. 전체 절차와 제한은 아래 학습 자료에 있습니다.

Requires Python 3.9 or later / 需要 Python 3.9 以上版本 / 需要 Python 3.9 及以上版本 / Python 3.9 以降が必要 / Python 3.9 이상 필요.

## Windows PowerShell
```powershell
py -3 clean_contacts.py contacts.csv cleaned-01.csv
py -3 -m unittest -v test_clean_contacts.py
```

## macOS / Linux
```sh
python3 clean_contacts.py contacts.csv cleaned-01.csv
python3 -m unittest -v test_clean_contacts.py
```

Expected / 預期 / 预期 / 期待 / 예상: kept=2, duplicate=1, invalid=1; 3 passing tests.
This writes a local output; it sends no email and does not publish anything.
教學 / 教程 / Tutorial / 教材 / 학습: https://mokaair.com/en/life/codex-csv-workshop
Use the site's language switcher for zh-TW, zh-CN, en, ja and ko.
""".encode()
archive_path = ROOT / "apps/web/public/guides/codex-csv-workshop/contacts-practice.zip"
archive_path.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(archive_path, "w", compression=ZIP_DEFLATED) as archive:
    for name, body in sorted(files.items()):
        info = ZipInfo("contacts-practice/" + name, date_time=(2026, 9, 14, 0, 0, 0))
        info.compress_type = ZIP_DEFLATED
        archive.writestr(info, body)
checks.append("The deterministic CSV ZIP contains the exact article input, reference program, tests and Unicode fixture")

with tempfile.TemporaryDirectory(prefix="codex-workshop-reference-") as temporary:
    root = Path(temporary).resolve()
    assert root.parent == Path(tempfile.gettempdir()).resolve()
    assert root.name.startswith("codex-workshop-reference-")
    csv_folder = root / "csv"
    csv_folder.mkdir()
    with ZipFile(archive_path) as archive:
        assert set(archive.namelist()) == {"contacts-practice/" + name for name in files}
        for name, body in files.items():
            assert archive.read("contacts-practice/" + name) == body
            (csv_folder / name).write_bytes(body)
    command = [sys.executable, "-X", "utf8", "clean_contacts.py"]
    base = run([*command, "contacts.csv", "cleaned-01.csv"], csv_folder)
    assert base.stdout == "" and json.loads(base.stderr) == {"kept": 2, "duplicate": 1, "invalid": 1}
    assert (csv_folder / "cleaned-01.csv").read_text(encoding="utf-8") == "name,email\nAlice,alice@example.test\nBob,bob@example.test\n"
    original = (csv_folder / "contacts.csv").read_bytes()
    output = (csv_folder / "cleaned-01.csv").read_bytes()
    run([*command, "contacts.csv", "cleaned-01.csv"], csv_folder, expected=1)
    run([*command, "contacts.csv", "contacts.csv"], csv_folder, expected=1)
    assert (csv_folder / "contacts.csv").read_bytes() == original == files["contacts.csv"]
    assert (csv_folder / "cleaned-01.csv").read_bytes() == output
    checks.append("CLI counts/output are correct; repeated output and same-input targets fail while preserving bytes")
    unicode = run([*command, "contacts-unicode.csv", "cleaned-unicode.csv"], csv_folder)
    assert json.loads(unicode.stderr) == {"kept": 1, "duplicate": 0, "invalid": 0}
    assert '"林, Alex"' in (csv_folder / "cleaned-unicode.csv").read_text(encoding="utf-8")
    for number, data in enumerate(["name,email\nAlice\n", "email,name\na@b.test,A\n", "name,email\nA,a@b.test,extra\n", 'name,email\n"unterminated,a@b.test\n']):
        (csv_folder / "bad.csv").write_text(data, encoding="utf-8")
        target = f"bad-{number}.csv"
        run([*command, "bad.csv", target], csv_folder, expected=1)
        assert not (csv_folder / target).exists()
    checks.append("Quoted Unicode is preserved; missing/extra columns, reversed headers and malformed quoting produce no output")
    first_input = code(32, "contacts-first-valid.csv")
    (csv_folder / "contacts-first-valid.csv").write_text(first_input, encoding="utf-8")
    first_result = run([*command, "contacts-first-valid.csv", "cleaned-first-valid.csv"], csv_folder)
    assert json.loads(first_result.stderr) == {"kept": 1, "duplicate": 1, "invalid": 1}
    assert (csv_folder / "cleaned-first-valid.csv").read_text(encoding="utf-8") == code(32, "cleaned-first-valid.csv 的預期內容")
    assert (csv_folder / "contacts-first-valid.csv").read_text(encoding="utf-8") == first_input
    assert (csv_folder / "contacts.csv").read_bytes() == original
    assert (csv_folder / "cleaned-01.csv").read_bytes() == output
    checks.append("An invalid first row does not reserve its email; exact later valid output and 1/1/1 counts are verified while prior files remain unchanged")
    tests = [sys.executable, "-X", "utf8", "-m", "unittest", "-v", "test_clean_contacts.py"]
    assert "Ran 3 tests" in run(tests, csv_folder).stderr
    (csv_folder / "clean_contacts.py").write_text(files["clean_contacts.py"].decode("utf-8").replace('target.open("x"', 'target.open("w"'), encoding="utf-8")
    mutated = run(tests, csv_folder, expected=1)
    assert "FAIL" in mutated.stderr and "FileExistsError not raised" in mutated.stderr
    (csv_folder / "clean_contacts.py").write_bytes(files["clean_contacts.py"])
    assert "Ran 3 tests" in run(tests, csv_folder).stderr
    checks.append("All three CSV tests pass, detect deliberately removed overwrite protection, then pass after restoration")

    maintenance = root / "maintenance"
    maintenance.mkdir()
    reference = ROOT / "docs/codex-learning/practice/expected"
    original_files = {p.name: p.read_bytes() for p in reference.iterdir() if p.is_file()}
    assert set(original_files) == {"core.mjs", "core.test.mjs", "app.js", "index.html", "style.css"}
    for name, body in original_files.items():
        (maintenance / name).write_bytes(body)
    node_tests(maintenance, ["core.test.mjs"], 3, 0)
    (maintenance / "maintenance.test.mjs").write_text(code(58, "maintenance.test.mjs"), encoding="utf-8")
    node_tests(maintenance, ["core.test.mjs", "maintenance.test.mjs"], 3, 3)
    helper = code(58, "core.mjs 的參考新增函式")
    (maintenance / "core.mjs").write_text(original_files["core.mjs"].decode("utf-8") + "\n" + helper, encoding="utf-8")
    app = original_files["app.js"].decode("utf-8")
    old_import = app.splitlines()[0]
    new_import = code(58, "app.js：替換原本的 core 匯入行").rstrip("\n")
    app = app.replace(old_import, new_import, 1)
    old = 'document.querySelector("#count").textContent = `${tasks.filter((task) => !task.completed).length} active / ${tasks.length} total`;'
    assert old in app
    new_count = code(58, "app.js：替換 render 中原本的統計賦值").rstrip("\n")
    app = app.replace(old, new_count.replace("\n", "\n  "))
    (maintenance / "app.js").write_text(app, encoding="utf-8")
    node_tests(maintenance, ["core.test.mjs", "maintenance.test.mjs"], 6, 0)
    assert all((maintenance / name).read_bytes() == original_files[name] for name in ["core.test.mjs", "index.html", "style.css"])
    checks.append("Maintenance starts with 3 passing tests, exposes 3 missing-helper failures, then passes all 6 with only the planned code changes")
    (maintenance / "app.js").write_text(app.replace("countTasks(tasks)", "countTasks(shown)"), encoding="utf-8")
    node_tests(maintenance, ["core.test.mjs", "maintenance.test.mjs"], 6, 0)
    probe = "import {addTask,toggleTask,visibleTasks,countTasks} from './core.mjs';const tasks=toggleTask(addTask(addTask([],'Read','a'),'Build','b'),'a');console.log(JSON.stringify({full:countTasks(tasks),filtered:countTasks(visibleTasks(tasks,'completed'))}));"
    observed = json.loads(run(["node", "--input-type=module", "-e", probe], maintenance).stdout)
    assert observed == {"full": {"active": 1, "total": 2}, "filtered": {"active": 0, "total": 1}}
    (maintenance / "app.js").write_text(app, encoding="utf-8")
    checks.append("Miswiring to shown leaves all six core tests green; direct data evaluation demonstrates the 0/1 versus 1/2 difference without claiming browser execution")
    changed = (maintenance / "core.mjs").read_text(encoding="utf-8")
    bad = helper.replace('active: tasks.filter((task) => !task.completed).length', 'active: tasks.length')
    (maintenance / "core.mjs").write_text(changed.replace(helper, bad), encoding="utf-8")
    node_tests(maintenance, ["core.test.mjs", "maintenance.test.mjs"], 4, 2)
    (maintenance / "core.mjs").write_text(changed, encoding="utf-8")
    node_tests(maintenance, ["core.test.mjs", "maintenance.test.mjs"], 6, 0)
    for name, body in original_files.items():
        (maintenance / name).write_bytes(body)
    extra_test = maintenance / "maintenance.test.mjs"
    assert extra_test.resolve().parent == maintenance and extra_test.name == "maintenance.test.mjs"
    extra_test.unlink()
    node_tests(maintenance, ["core.test.mjs"], 3, 0)
    assert {p.name: p.read_bytes() for p in maintenance.iterdir() if p.is_file()} == original_files
    checks.append("The new tests catch incorrect active counts; targeted restoration returns all five original files and 3 passing tests")

    paths = root / "path-trouble"
    (paths / "project").mkdir(parents=True)
    (paths / "other").mkdir()
    (paths / "project/marker.md").write_text(code(12, "project/marker.md"), encoding="utf-8")
    assert not (paths / "other/marker.md").exists()
    assert (paths / "other/../project/marker.md").read_text(encoding="utf-8") == "# Correct folder: PATH-PRACTICE-1\n"
    checks.append("The path drill's missing and explicit-relative paths match its declared fixture")
    pwsh = shutil.which("pwsh")
    assert pwsh, "The Windows PowerShell status example requires pwsh for this check"
    powershell = run([pwsh, "-NoProfile", "-NonInteractive", "-Command", code(12, "Windows PowerShell：目前在 project")], paths / "project")
    assert powershell.stdout.splitlines() == ["False", "# Correct folder: PATH-PRACTICE-1", "True"]
    assert "marker.md" in powershell.stderr
    assert (paths / "project/marker.md").read_text(encoding="utf-8") == code(12, "project/marker.md")
    checks.append("The exact PowerShell cmdlet-status exercise yields False then True and preserves the marker; POSIX shell execution remains untested")

    safety = root / "safety-lab"
    safety.mkdir()
    safety_files = {".env": code(59, ".env（只有假值）"), ".gitignore": code(59, ".gitignore（僅此新練習）"), "brief.md": code(59, "brief.md")}
    for name, value in safety_files.items():
        (safety / name).write_text(value, encoding="utf-8")
    run(["git", "init"], safety)
    assert run(["git", "check-ignore", "--", ".env"], safety).stdout.strip() == ".env"
    assert run(["git", "ls-files", "--", ".env"], safety).stdout == ""
    assert all((safety / name).read_text(encoding="utf-8") == value for name, value in safety_files.items())
    checks.append("A fresh isolated Git repository ignores the fictional env file without tracking or changing it; no model resistance or read-denial claim")

    broken = {p.name: p.read_bytes() for p in (ROOT / "docs/codex-learning/practice/broken").iterdir() if p.is_file()}
    for name in ["efficiency-a", "efficiency-b"]:
        target = root / name
        target.mkdir()
        for filename, value in broken.items():
            (target / filename).write_bytes(value)
        node_tests(target, ["core.test.mjs"], 2, 1)
        assert {p.name: p.read_bytes() for p in target.iterdir() if p.is_file()} == broken
    checks.append("Both efficiency reference copies reproduce the same 2-pass/1-failure baseline without edits; no usage or model-time measurements")

report = {"checkedAt": datetime.now(timezone.utc).isoformat(), "status": "passed", "checks": checks,
          "environment": "Windows; local Python and Node; isolated fictional files; explicit reference edits",
          "authorHashes": {str(i): sha256((ROOT / f"docs/codex-learning/deep/modules/{i}.json").read_bytes()).hexdigest() for i in [12, 31, 32, 58, 59, 60]},
          "archiveHash": sha256(archive_path.read_bytes()).hexdigest(),
          "notTested": ["Generated model implementations", "Actual Codex prompt-injection response", "Live usage comparison", "Post-refactor browser behavior", "macOS/Linux execution", "Publication or deployment"]}
(ROOT / "docs/codex-learning/evidence/workshop-reference.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(f"{len(checks)} workshop reference checks passed; CSV archive contains {len(files)} files")
