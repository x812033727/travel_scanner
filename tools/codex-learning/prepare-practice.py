"""Prepare reproducible, explicitly incomplete exercise variants and a public ZIP."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from practice_archive import package_practice

ROOT = Path(__file__).resolve().parents[2]
base = ROOT / "docs/codex-learning/practice"
source = base / "expected"
for variant in ["start", "broken"]:
    target = base / variant
    target.mkdir(parents=True, exist_ok=True)
    for path in sorted(source.iterdir()):
        if not path.is_file():
            continue
        body = path.read_text(encoding="utf-8")
        if path.name == "core.mjs":
            if variant == "start":
                begin = body.index("export function visibleTasks")
                end = body.index("export function decodeTasks")
                body = (
                    body[:begin]
                    + "// EXERCISE: implement the Active and Completed filters.\n"
                    + "export function visibleTasks(tasks, filter) {\n  return tasks;\n}\n\n"
                    + body[end:]
                )
            else:
                body = body.replace(
                    'if (filter === "completed") return tasks.filter((task) => task.completed);',
                    '// EXERCISE: this predicate is deliberately wrong.\n  '
                    'if (filter === "completed") return tasks.filter((task) => !task.completed);',
                )
        (target / path.name).write_text(body, encoding="utf-8")

destination = ROOT / "apps/web/public/guides/codex-first-project/todo-practice.zip"
count = package_practice(base, destination, base / "manifest.json")
print(f"Prepared {count} explicit exercise files and {destination.name}")
skill = base / "skills/todo-acceptance/SKILL.md"
skill_zip = ROOT / "apps/web/public/guides/codex-skills/todo-acceptance.zip"
skill_zip.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(skill_zip, "w", ZIP_DEFLATED) as archive:
    archive.write(skill, "todo-acceptance/SKILL.md")
print(f"Prepared {skill_zip.name}; example only, not installed in Codex")
