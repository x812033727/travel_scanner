"""Real directory links must not allow reads/writes outside the named roots."""
from __future__ import annotations

import contextlib
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import test_authoring_kit as kit_fixtures
from authoring_kit import authoring_kit
from files import contained
from package import package


def directory_link(test: unittest.TestCase, target: Path, link: Path) -> None:
    link.parent.mkdir(parents=True, exist_ok=True)
    try:
        link.symlink_to(target, target_is_directory=True)
    except OSError as error:
        if os.name != "nt":
            test.skipTest(f"Directory symlinks unavailable: {error}")
        result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], capture_output=True, check=False,
                                creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode:
            test.skipTest(f"Windows cannot create a test symlink or junction: {error}")


def remove_directory_link(link: Path) -> None:
    if link.is_symlink():
        link.unlink()
    else:
        link.rmdir()  # Remove the junction itself, never recursively its target.


@contextlib.contextmanager
def forbid_outside_reads(outside: Path):
    originals = {name: getattr(Path, name) for name in ("read_bytes", "read_text")}

    def guarded(name):
        def read(path, *args, **kwargs):
            if path.resolve().is_relative_to(outside.resolve()):
                raise AssertionError(f"An outside source was read before rejection: {path}")
            return originals[name](path, *args, **kwargs)
        return read

    with patch.object(Path, "read_bytes", guarded("read_bytes")), patch.object(Path, "read_text", guarded("read_text")):
        yield


class PackagePathTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="dots-boundary-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.workspace, self.repo, self.outside = (self.base / name for name in ("workspace", "repo", "outside"))
        self.repo.mkdir()
        self.outside.mkdir()
        for number in range(11, 17):
            directory = self.workspace / "examples" / str(number)
            directory.mkdir(parents=True)
            for filename in ("initial.txt", "change.txt"):
                (directory / filename).write_text("owned synthetic input", encoding="utf-8")

    def test_external_lesson_junction_is_rejected_before_read_zip_or_repo_install(self):
        external_inputs = self.outside / "inputs"
        external_inputs.mkdir()
        for filename in ("first.txt", "second.txt"):
            (external_inputs / filename).write_text("outside source must never be read", encoding="utf-8")
        original = self.workspace / "examples/11"
        contained(original, self.workspace)
        shutil.rmtree(original)
        directory_link(self, external_inputs, original)
        directory_link(self, self.outside, self.workspace / "assets")
        with forbid_outside_reads(self.outside), self.assertRaisesRegex(ValueError, "escapes allowed workspace"):
            package(self.workspace, repo=self.repo, install_downloads=True)
        self.assertFalse(list(self.outside.rglob("*.zip")))
        self.assertFalse((self.workspace / "build-authoring").exists())
        self.assertFalse((self.repo / "apps").exists())

    def test_every_output_root_and_late_destination_is_preflighted_before_any_zip(self):
        roots = [self.workspace / "assets", self.workspace / "assets/dots-course/downloads",
                 self.workspace / "build-authoring", self.workspace / "build-authoring/examples/16",
                 self.repo / "apps/web/public", self.repo / "apps/web/public/dots-course/downloads"]
        for index, link in enumerate(roots):
            with self.subTest(link=link):
                external = self.outside / str(index)
                external.mkdir()
                directory_link(self, external, link)
                try:
                    with self.assertRaisesRegex(ValueError, "escapes allowed workspace"):
                        package(self.workspace, repo=self.repo, install_downloads=True)
                    self.assertFalse(list(self.workspace.rglob("*.zip")))
                    self.assertFalse(list(external.rglob("*")))
                    self.assertFalse(list(self.repo.rglob("*.zip")))
                finally:
                    remove_directory_link(link)

    def test_nested_link_in_later_source_is_checked_before_traversal_or_archive_creation(self):
        (self.outside / "first.txt").write_text("outside", encoding="utf-8")
        directory_link(self, self.outside, self.workspace / "examples/16/nested")
        with forbid_outside_reads(self.outside), self.assertRaisesRegex(ValueError, "escapes allowed workspace"):
            package(self.workspace, repo=self.repo, install_downloads=True)
        self.assertFalse((self.workspace / "assets").exists())
        self.assertFalse((self.repo / "apps").exists())

    def test_late_archive_file_link_is_rejected_before_the_first_archive_is_created(self):
        destination = self.workspace / "assets/dots-course/downloads/lesson-16.zip"
        destination.parent.mkdir(parents=True)
        target = self.outside / "escaped.zip"
        try:
            destination.symlink_to(target)
        except OSError as error:
            self.skipTest(f"File symlink creation unavailable: {error}")
        with self.assertRaisesRegex(ValueError, "escapes allowed workspace"):
            package(self.workspace, repo=self.repo, install_downloads=True)
        self.assertFalse(target.exists())
        self.assertFalse((destination.parent / "lesson-11.zip").exists())
        self.assertFalse((self.repo / "apps").exists())


class AuthoringPathTests(unittest.TestCase):
    def setUp(self):
        fixture = kit_fixtures.AuthoringKitTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.workspace, self.repo = fixture.workspace, fixture.repo
        self.outside = self.workspace.parent / "outside"
        self.outside.mkdir()

    def test_source_directory_escape_is_rejected_without_reading_external_authoring(self):
        for filename in ("initial.md", "change.md"):
            (self.outside / filename).write_text("outside source", encoding="utf-8")
        source = self.workspace / "examples/11"
        contained(source, self.workspace)
        shutil.rmtree(source)
        directory_link(self, self.outside, source)
        with forbid_outside_reads(self.outside), self.assertRaisesRegex(ValueError, "escapes allowed workspace"):
            authoring_kit(self.workspace, repo=self.repo, install=True)
        self.assertFalse((self.workspace / "build-authoring").exists())
        self.assertFalse((self.repo / "docs").exists())

    def test_staging_and_repo_docs_roots_are_preflighted_before_any_text_output(self):
        roots = [self.workspace / "build-authoring", self.workspace / "build-authoring/docs/videos/dots-lesson-16",
                 self.repo / "docs", self.repo / "docs/videos/dots-lesson-16"]
        for index, link in enumerate(roots):
            with self.subTest(link=link):
                external = self.outside / str(index)
                external.mkdir()
                directory_link(self, external, link)
                try:
                    with self.assertRaisesRegex(ValueError, "escapes allowed workspace"):
                        authoring_kit(self.workspace, repo=self.repo, install=True)
                    self.assertFalse(list(external.rglob("*")))
                    self.assertFalse(list((self.workspace / "build-authoring").rglob("*.md")))
                    self.assertFalse(list((self.repo / "docs").rglob("*.md")))
                finally:
                    remove_directory_link(link)


if __name__ == "__main__":
    unittest.main()
