"""Machine-gate tests use local generated fixtures; none are production evidence."""
from __future__ import annotations

import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

from files import digest, dumps, verify_screenshot
from readiness import ROOT, SLUGS, audit, reference, subtitles

STAMP = "2026-10-03T15:00:00+08:00"


def png() -> bytes:
    def chunk(kind: bytes, body: bytes) -> bytes:
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 320, 180, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress((b"\x00" + b"\x99" * 960) * 180)) + chunk(b"IEND", b"")


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="dots-contract-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def record(self, name: str, content: str | bytes) -> dict:
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode("utf-8") if isinstance(content, str) else content)
        return {"path": name, "sha256": digest(path)}

    def evidence(self):
        # Generated test fixtures exercise structural acceptance only. media_probe is
        # explicitly replaced; the public CLI always runs ffprobe on the actual file.
        inputs = [self.record("lessons/01.md", "test-only source text")]
        files = [self.record(f"build/content/{slug}.json", json.dumps({"slug": slug})) for slug in [*SLUGS, "dots-guide"]]
        build = {"version": 1, "state": "draft", "published": False, "articles": [*SLUGS, "dots-guide"], "inputs": inputs,
                 "source_assets": [], "catalogue_sha256": digest(ROOT / "apps/api/app/guides/series_data/dots.json"),
                 "files": [{**item, "path": item["path"][6:]} for item in files]}
        self.record("build/build-manifest.json", dumps(build))
        lessons = []
        for number, slug in enumerate(SLUGS, 1):
            capture = {**self.record(f"evidence/{number:02}/capture.json", dumps({"contract_test": number})), "origin": "real-dots", "authenticated": True, "captured_at": STAMP}
            screenshot = {**self.record(f"evidence/{number:02}/screen.png", png()), "origin": "real-dots", "redacted": True, "captured_at": STAMP}
            article_hash = digest(self.root / f"build/content/{slug}.json")
            review = {"reviewer": "contract-test-reviewer", "checked_at": STAMP, "files": {capture["path"]: capture["sha256"], screenshot["path"]: screenshot["sha256"], "article": article_hash},
                      "steps_reproduced": True, "result_checked": True, "redaction": True}
            video = {**self.record(f"media/{number:02}/final.mp4", b"unit-test media bytes"), "body_start_seconds": 10, "body_end_seconds": 510}
            for key in ("cc", "chapters", "thumbnail", "description"):
                value = "1\n00:00:10,000 --> 00:00:12,000\n測試字幕\n" if key == "cc" else "00:00 開始\n00:30 操作\n04:00 結果\n" if key == "chapters" else png() if key == "thumbnail" else "contract test data"
                suffix = "png" if key == "thumbnail" else "srt" if key == "cc" else "txt"
                video[key] = self.record(f"media/{number:02}/{key}.{suffix}", value)
            media_hashes = {video["path"]: video["sha256"], **{video[key]["path"]: video[key]["sha256"] for key in ("cc", "chapters", "thumbnail", "description")}}
            video["review"] = {"reviewer": "contract-test-reviewer", "checked_at": STAMP, "files": media_hashes,
                               **dict.fromkeys(("screen_readable", "audio", "cc_sync", "chapters", "redaction"), True)}
            lessons.append({"number": number, "capture": capture, "screenshots": [screenshot], "article_sha256": article_hash, "review": review, "video": video})
        applications = []
        for number in range(11, 17):
            item = {"number": number, "origin": "real-dots", "updated_in_same_task": True}
            hashes = {}
            for part in ("before", "after", "verification"):
                item[part] = self.record(f"evidence/apps/{number}-{part}.json", dumps({"contract_test": part}))
                hashes[item[part]["path"]] = item[part]["sha256"]
            item["review"] = {"reviewer": "contract-test-reviewer", "checked_at": STAMP, "files": hashes, "result_checked": True, "independent_calculation": True}
            applications.append(item)
        scheduling = {key: self.record(f"evidence/schedule/{key}.json", dumps({"contract_test": key}))
                      for key in ("execution", "main_stopped", "delegated_stopped", "schedule_cancelled")}
        scheduling["review"] = {"reviewer": "contract-test-reviewer", "checked_at": STAMP, "files": {ref["path"]: ref["sha256"] for ref in scheduling.values()}, "execution_observed": True, "stop_scopes_checked": True}
        evidence = {"version": 1, "lessons": lessons, "applications": applications, "scheduling": scheduling}
        self.save(evidence)
        return evidence

    def save(self, value: dict):
        self.record("evidence/acceptance.json", dumps(value))

    def audit(self):
        return audit(self.root, media_probe=lambda _path, _binary: {"duration_seconds": 520.0})

    def test_completeness_and_binding_allow_manifest_preparation_without_publishing(self):
        self.evidence()
        result = self.audit()
        self.assertEqual(result["errors"], [])
        self.assertTrue(result["ready"])
        self.assertFalse(result["published"])
        self.assertEqual(len(result["videos"]), 16)
        self.assertEqual(result["write_order"][-1], "dots-guide")

    def test_missing_actual_evidence_never_passes(self):
        self.record("evidence/acceptance.json", dumps({"version": 1, "lessons": [], "applications": [], "scheduling": {}}))
        result = self.audit()
        self.assertFalse(result["ready"])
        self.assertTrue(any("sixteen unique authenticated" in line for line in result["errors"]))
        self.assertTrue(any("six before/after" in line for line in result["errors"]))

    def test_hash_change_of_media_article_source_or_capture_invalidates_review(self):
        self.evidence()
        for filename in ("media/01/final.mp4", "build/content/dots-lesson-01.json", "lessons/01.md", "evidence/01/capture.json"):
            path = self.root / filename
            original = path.read_bytes()
            path.write_bytes(original + b"changed")
            with self.subTest(filename=filename):
                self.assertFalse(self.audit()["ready"])
            path.write_bytes(original)
        self.assertTrue(self.audit()["ready"])

    def test_qualified_flags_and_duration_are_required(self):
        evidence = self.evidence()
        evidence["lessons"][0]["video"]["body_end_seconds"] = 450
        evidence["lessons"][1]["capture"]["authenticated"] = False
        evidence["applications"][2]["review"]["independent_calculation"] = False
        evidence["scheduling"]["review"]["stop_scopes_checked"] = False
        self.save(evidence)
        result = self.audit()
        self.assertFalse(result["ready"])
        for expected in ("eight minutes", "authenticated", "independent_calculation", "stop_scopes_checked"):
            self.assertTrue(any(expected in line for line in result["errors"]), expected)

    def test_fixtures_cannot_be_promoted_and_paths_cannot_escape(self):
        errors = []
        self.assertIsNone(reference(self.record("evidence/mock-capture.json", dumps({"fixture": True})), self.root, "capture", errors))
        self.assertIsNone(reference({"path": "../outside.json", "sha256": "a" * 64}, self.root, "capture", errors))
        self.assertEqual(len(errors), 2)

    def test_png_and_cc_checks_reject_corruption(self):
        shot = self.root / "screen.png"
        shot.write_bytes(png())
        verify_screenshot(shot)
        shot.write_bytes(png()[:-3])
        with self.assertRaises(ValueError):
            verify_screenshot(shot)
        cc = self.root / "cc.srt"
        cc.write_text("1\n00:08:30,000 --> 00:09:00,000\n超出\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "beyond"):
            subtitles(cc, 520)
        cc.write_text("1\n00:00:10,000 --> 00:00:12,000\n正確\n\n2\n00:00:99,000 --> 00:02:00,000\n格式錯誤\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "below sixty"):
            subtitles(cc, 520)
        cc.write_text("1\n00:00:10,000 --> 00:00:12,000\n正確\n\n2\nwrong timing\n無法忽略\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "malformed"):
            subtitles(cc, 520)


if __name__ == "__main__":
    unittest.main()
