"""Offline regressions for source-bound sidecars and mux-only provenance.

Run: python -m unittest discover -s tools/video/preschool -p 'test_*.py'
Fixtures model already-produced artifacts; no speech provider or delivered media
is touched. These tests exercise tampering and resume/packaging decisions, not
codec correctness (the production build performs the complete media decode).
"""
from __future__ import annotations

import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from audio import (PipelineError, atomic_json, audio_artifact_paths,
                   audio_integrity, capture_audio_integrity, episode_audio_ready,
                   file_digest, read_json, verify_picture_artifact)
from build import (LOCALES, SUBTITLES, RENDER_VERSION, fingerprint, mux,
                   renderer_fingerprint, valid_final)
from package_series import preflight


class IntegrityTests(unittest.TestCase):
    def setUp(self):
        library = patch("build.render_library", return_value={"name": "Pillow", "version": "test-fixture"})
        library.start()
        self.addCleanup(library.stop)
        self.temporary = tempfile.TemporaryDirectory(prefix="preschool-integrity-test-")
        self.output = Path(self.temporary.name)
        self.addCleanup(self.temporary.cleanup)
        self.episodes, self.records = [], []
        for number in range(1, 49):
            eid = f"ep{number:02d}"
            episode = {"id": eid, "number": number, "season": (number - 1) // 12 + 1,
                       "duration": 180, "title_zh_TW": "測試", "title_en": "Cat",
                       "objectives_zh_TW": ["Recognize cat"], "source_sha256": "authoring-source",
                       "scenes": [{"id": f"{eid}-s01", "english": "Cat", "duration": 18}]}
            directory = self.output / eid
            for name in [*audio_artifact_paths(), "final.mp4", "picture.mp4", "poster.jpg"]:
                path = directory / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(f"checked artifact: {eid}/{name}".encode())
            receipt = capture_audio_integrity(episode, self.output)
            record = {"id": eid, "ready": True, "duration": 180,
                      "source_sha256": episode["source_sha256"], "artifact_integrity": receipt}
            digest = file_digest(directory / "final.mp4")
            checks = {"episode": eid, "full_decode": True, "duration": 180,
                      "audio_tracks": list(LOCALES), "cc_tracks": list(SUBTITLES),
                      "english_cc": False, "english_text": "embedded into picture",
                      "source_sha256": fingerprint(episode), "bytes": digest["bytes"],
                      "final_sha256": digest["sha256"], "artifact_integrity": receipt,
                      "renderer_version": RENDER_VERSION, "render_library": {"name": "Pillow", "version": "test-fixture"},
                      "renderer_sha256": renderer_fingerprint(15)}
            picture = {"source_sha256": fingerprint(episode), "renderer_version": RENDER_VERSION,
                       "renderer_sha256": renderer_fingerprint(15), "render_library": {"name": "Pillow", "version": "test-fixture"},
                       "render_fps": 15, **file_digest(directory / "picture.mp4")}
            checks["picture_integrity"] = picture
            atomic_json(directory / "checks.json", checks)
            atomic_json(directory / "picture.checks.json", picture)
            self.episodes.append(episode)
            self.records.append(record)
        atomic_json(self.output / "audio-manifest.json", {"episodes": self.records})

    def tamper(self, relative: str):
        path = self.output / "ep01" / relative
        original = path.read_bytes()
        path.write_bytes(bytes([original[0] ^ 1]) + original[1:])
        self.assertEqual(len(original), path.stat().st_size)

    def test_same_size_audio_change_blocks_resume_build_and_package(self):
        episode = self.episodes[0]
        self.assertTrue(episode_audio_ready(episode, self.output, self.records[0]))
        self.tamper("audio/ja.m4a")
        self.assertFalse(episode_audio_ready(episode, self.output, self.records[0]))
        self.assertFalse(valid_final(episode, self.output, 15))
        with self.assertRaisesRegex(PipelineError, "artifact hash or source mismatch"):
            preflight({"episodes": self.episodes}, self.output)
        with patch("build.run") as ffmpeg:
            with self.assertRaises(PipelineError):
                mux(episode, self.output)
            ffmpeg.assert_not_called()

    def test_same_size_caption_change_blocks_resume_and_package(self):
        self.tamper("captions/ko.vtt")
        self.assertFalse(episode_audio_ready(self.episodes[0], self.output, self.records[0]))
        with self.assertRaisesRegex(PipelineError, "artifact hash or source mismatch"):
            preflight({"episodes": self.episodes}, self.output)

    def test_new_audio_receipt_can_replace_an_old_final_receipt(self):
        self.tamper("audio/ja.m4a")
        updated = capture_audio_integrity(self.episodes[0], self.output)
        self.records[0]["artifact_integrity"] = updated
        atomic_json(self.output / "audio-manifest.json", {"episodes": self.records})
        self.assertTrue(episode_audio_ready(self.episodes[0], self.output))
        self.assertFalse(valid_final(self.episodes[0], self.output, 15))
        with self.assertRaisesRegex(PipelineError, "artifact hash or source mismatch"):
            preflight({"episodes": self.episodes}, self.output)

    def test_same_duration_new_text_cannot_reuse_picture_in_mux_only(self):
        changed = copy.deepcopy(self.episodes[0])
        changed["scenes"][0]["english"] = "Dog"
        self.assertEqual(changed["duration"], self.episodes[0]["duration"])
        with patch("build.run") as ffmpeg:
            with self.assertRaisesRegex(PipelineError, "picture source/timing"):
                mux(changed, self.output)
            ffmpeg.assert_not_called()

    def test_missing_or_changed_picture_receipt_requires_render(self):
        self.tamper("picture.mp4")
        with self.assertRaisesRegex(PipelineError, "rerun without --mux-only"):
            mux(self.episodes[0], self.output)
        (self.output / "ep01/picture.checks.json").unlink()
        with self.assertRaisesRegex(PipelineError, "rerun without --mux-only"):
            mux(self.episodes[0], self.output)

    def test_unknown_legacy_artifacts_are_not_blessed_by_hashing_them(self):
        for file in ("audio-manifest.json", "ep01/checks.json"):
            (self.output / file).unlink()
        self.assertFalse(episode_audio_ready(self.episodes[0], self.output))
        with self.assertRaisesRegex(PipelineError, "legacy sidecars need"):
            audio_integrity(self.episodes[0], self.output)

    def test_present_bad_receipt_never_falls_back_to_legacy(self):
        self.records[0]["artifact_integrity"]["version"] = 99
        with patch("audio.verify_legacy_audio") as legacy:
            self.assertFalse(episode_audio_ready(self.episodes[0], self.output, self.records[0]))
            legacy.assert_not_called()

    def test_new_audio_receipt_must_still_match_a_legacy_final(self):
        path = self.output / "ep01/checks.json"
        checks = read_json(path)
        del checks["artifact_integrity"]
        atomic_json(path, checks)
        self.assertTrue(episode_audio_ready(self.episodes[0], self.output))
        with patch("audio.verify_legacy_audio", side_effect=PipelineError("encoded audio differs")) as legacy:
            self.assertFalse(valid_final(self.episodes[0], self.output, 15))
            legacy.assert_called_once()
        with patch("audio.verify_legacy_audio", side_effect=PipelineError("encoded audio differs")):
            with self.assertRaisesRegex(PipelineError, "encoded audio differs"):
                preflight({"episodes": self.episodes}, self.output)

    def test_new_picture_receipt_cannot_replace_final_bound_picture(self):
        self.tamper("picture.mp4")
        path = self.output / "ep01/picture.checks.json"
        receipt = read_json(path)
        receipt.update(file_digest(self.output / "ep01/picture.mp4"))
        atomic_json(path, receipt)
        with self.assertRaisesRegex(PipelineError, "checked final's picture receipt"):
            verify_picture_artifact(self.episodes[0], self.output)

    def test_new_picture_receipt_must_still_match_a_legacy_final(self):
        path = self.output / "ep01/checks.json"
        checks = read_json(path)
        del checks["picture_integrity"]
        atomic_json(path, checks)
        with patch("audio.packet_fingerprints", side_effect=[["new picture"], ["old final"]]) as packets:
            with self.assertRaisesRegex(PipelineError, "legacy picture differs"):
                verify_picture_artifact(self.episodes[0], self.output)
            self.assertEqual(packets.call_count, 2)


if __name__ == "__main__":
    unittest.main()
