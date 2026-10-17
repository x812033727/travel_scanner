"""Local archive and extraction checks; no production host access."""

import hashlib
import io
import os
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import a01_stage_payload as stage


class StagePayloadTests(unittest.TestCase):
    def fixture(self, members: list[tuple[str, bytes | None]]) -> tuple[Path, Path, object]:
        directory = Path(tempfile.mkdtemp(prefix="a01-stage-test-"))
        archive = directory / "round12-r4-full-payload.tar.gz"
        with tarfile.open(archive, "w:gz") as tar:
            for name, content in members:
                info = tarfile.TarInfo(name)
                if content is None:
                    info.type = tarfile.DIRTYPE
                    tar.addfile(info)
                else:
                    info.size = len(content)
                    tar.addfile(info, io.BytesIO(content))
        pins = patch.multiple(
            stage, RELEASE=directory, ARCHIVE=archive, DEST=directory / "payload",
            EXPECTED_SHA=hashlib.sha256(archive.read_bytes()).hexdigest(),
            EXPECTED_MEMBERS=len(members),
            EXPECTED_FILES=sum(content is not None for _, content in members),
            EXPECTED_DIRS=sum(content is None for _, content in members),
        )
        self.addCleanup(lambda: __import__("shutil").rmtree(directory))
        return directory, archive, pins

    def test_regular_archive_inspects_and_stages_on_linux(self) -> None:
        directory, _, pins = self.fixture([("payload", None), ("payload/sub", None),
                                           ("payload/sub/file.txt", b"approved")])
        with pins:
            members = stage.inspect()
            self.assertEqual(len(members), 3)
            if os.name != "posix" or not hasattr(os, "O_NOFOLLOW"):
                self.skipTest("the host stage syscall path is Linux-only")
            stage.stage(members)
            self.assertEqual((directory / "payload/sub/file.txt").read_bytes(), b"approved")
            self.assertFalse(any(directory.glob(".a01-round12-payload-*")))
            with self.assertRaisesRegex(RuntimeError, "already exists"):
                stage.stage(members)

    def test_path_escape_refused(self) -> None:
        _, _, pins = self.fixture([("payload", None), ("payload/../outside", b"bad")])
        with pins, self.assertRaisesRegex(RuntimeError, "unsafe"):
            stage.inspect()

    def test_duplicate_path_refused(self) -> None:
        _, _, pins = self.fixture([("payload", None), ("payload/file", b"a"),
                                   ("payload/file", b"b")])
        with pins, self.assertRaisesRegex(RuntimeError, "duplicate"):
            stage.inspect()

    def test_link_refused(self) -> None:
        directory = Path(tempfile.mkdtemp(prefix="a01-stage-test-"))
        self.addCleanup(lambda: __import__("shutil").rmtree(directory))
        archive = directory / "round12-r4-full-payload.tar.gz"
        with tarfile.open(archive, "w:gz") as tar:
            root = tarfile.TarInfo("payload")
            root.type = tarfile.DIRTYPE
            tar.addfile(root)
            link = tarfile.TarInfo("payload/link")
            link.type = tarfile.SYMTYPE
            link.linkname = "/etc/passwd"
            tar.addfile(link)
        with patch.multiple(stage, RELEASE=directory, ARCHIVE=archive,
                            EXPECTED_SHA=hashlib.sha256(archive.read_bytes()).hexdigest(),
                            EXPECTED_MEMBERS=2):
            with self.assertRaisesRegex(RuntimeError, "link or special"):
                stage.inspect()

    def test_hash_drift_refused(self) -> None:
        _, _, pins = self.fixture([("payload", None)])
        with pins, patch.object(stage, "EXPECTED_SHA", "0" * 64):
            with self.assertRaisesRegex(RuntimeError, "SHA mismatch"):
                stage.inspect()


if __name__ == "__main__":
    unittest.main()
