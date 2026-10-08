"""Offline regressions for course isolation and recorded renderer provenance.

These synthetic checked-file fixtures test admission decisions, not codecs.
Production mux performs the complete real audio/video decode.
"""
from __future__ import annotations

import copy
from contextlib import ExitStack
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from elementary.shared import audio, build, PRESCHOOL, verify as shared_verify
from elementary.profile import ElementaryRenderer, RENDERER
from elementary.player import write_player
from elementary.verify_series import verify_media, verify_structure
from elementary import batch, player


class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="elementary-profile-test-")
        self.output = Path(self.temporary.name)
        self.addCleanup(self.temporary.cleanup)
        library = patch.object(build, "render_library", return_value={"name": "Pillow", "version": "fixture"})
        library.start()
        self.addCleanup(library.stop)
        self.episode = {"id": "ep01", "number": 1, "season": 1, "duration": 180,
                        "title_en": "Book", "title_zh_TW": "書", "source_sha256": "authored-fixture",
                        "scenes": [{"id": "ep01-s01", "english": "Book", "duration": 18}]}
        directory = self.output / "ep01"
        for name in [*audio.audio_artifact_paths(), "final.mp4", "picture.mp4", "poster.jpg"]:
            path = directory / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(f"checked fixture: {name}".encode())
        receipt = audio.capture_audio_integrity(self.episode, self.output)
        audio.atomic_json(self.output / "audio-manifest.json", {"episodes": [{
            "id": "ep01", "ready": True, "duration": 180, "source_sha256": "authored-fixture",
            "artifact_integrity": receipt,
        }]})
        self.picture = {"source_sha256": build.fingerprint(self.episode),
                        "renderer_version": build.RENDER_VERSION, "render_fps": 15,
                        "renderer_profile": RENDERER.name, "render_library": build.render_library(),
                        "renderer_sha256": RENDERER.fingerprint(15),
                        **audio.file_digest(directory / "picture.mp4")}
        streams = [{"codec_type": "video", "codec_name": "h264", "pix_fmt": "yuv420p",
                    "width": 1280, "height": 720, "r_frame_rate": "30/1"}]
        streams.extend({"codec_type": "audio", "codec_name": "aac", "duration": "180",
                        "tags": {"language": build.LANGUAGES[locale], "handler_name": build.TITLES[locale]}}
                       for locale in build.LOCALES)
        streams.extend({"codec_type": "subtitle", "codec_name": "mov_text",
                        "tags": {"language": build.LANGUAGES[locale], "handler_name": build.TITLES[locale]}}
                       for locale in build.SUBTITLES)
        self.checks = {"episode": "ep01", "file": "ep01/final.mp4", "duration": 180,
                       "full_decode": True, "source_sha256": build.fingerprint(self.episode),
                       "renderer_profile": RENDERER.name, "renderer_version": build.RENDER_VERSION,
                       "renderer_sha256": RENDERER.fingerprint(15), "render_fps": 15,
                       "render_library": build.render_library(),
                       "bytes": (directory / "final.mp4").stat().st_size,
                       "final_sha256": build.file_sha256(directory / "final.mp4"),
                       "audio_tracks": list(build.LOCALES), "cc_tracks": list(build.SUBTITLES),
                       "english_cc": False, "english_text": "embedded into picture",
                       "artifact_integrity": receipt, "picture_integrity": self.picture,
                       "media_probe": {"streams": streams, "format": {"duration": "180"}}}
        audio.atomic_json(directory / "picture.checks.json", self.picture)
        audio.atomic_json(directory / "checks.json", self.checks)

    def test_preschool_default_fingerprint_is_unchanged(self):
        sources = {name: build.file_sha256(PRESCHOOL / name) for name in ("visuals.py", "objects.py")}
        expected = build.fingerprint({"sources": sources, "fps": 15, "render_version": 3,
                                      "resolution": [1280, 720], "output_fps": 30, "crf": 22,
                                      "render_library": build.render_library()})
        self.assertEqual(build.renderer_fingerprint(15), expected)
        self.assertNotEqual(RENDERER.fingerprint(15), expected)

    def test_elementary_and_shared_artwork_changes_both_invalidate_record(self):
        profile = ElementaryRenderer()
        copies = {}
        for index, (name, source) in enumerate(profile.source_paths().items()):
            path = self.output / f"renderer-source-{index}"
            path.write_bytes(source.read_bytes())
            copies[name] = path
        with patch.object(profile, "source_paths", return_value=copies):
            initial = profile.fingerprint(15)
            for name in ("elementary/visuals.py", "elementary/objects.py", "preschool/visuals.py", "preschool/objects.py"):
                original = copies[name].read_bytes()
                copies[name].write_bytes(original + b"\n# changed drawing\n")
                self.assertNotEqual(initial, profile.fingerprint(15), name)
                copies[name].write_bytes(original)
                self.assertEqual(initial, profile.fingerprint(15), name)

    def test_recorded_library_is_used_and_unknown_profiles_fail(self):
        recorded = RENDERER.recorded_fingerprint(self.picture, 15)
        with patch.object(build, "render_library", return_value={"name": "Pillow", "version": "new-build"}):
            self.assertEqual(recorded, RENDERER.recorded_fingerprint(self.picture, 15))
            self.assertNotEqual(recorded, RENDERER.fingerprint(15))
        self.assertIsNone(RENDERER.recorded_fingerprint({**self.picture, "renderer_profile": "unknown"}, 15))
        self.assertIsNone(build.profile_fingerprint(self.picture, 15))

    def test_picture_resume_and_media_require_the_explicit_course_profile(self):
        self.assertEqual(build.require_picture(self.episode, self.output, 15, renderer_profile=RENDERER), self.picture)
        with self.assertRaises(audio.PipelineError):
            build.require_picture(self.episode, self.output, 15)
        self.assertTrue(build.valid_final(self.episode, self.output, 15, renderer_profile=RENDERER))
        self.assertFalse(build.valid_final(self.episode, self.output, 15))
        self.assertTrue(verify_media(self.episode, self.output, self.checks)["full_decode"])
        with self.assertRaises(shared_verify.VerificationError):
            shared_verify.verify_media(self.episode, self.output, self.checks)
        changed = copy.deepcopy(self.episode)
        changed["scenes"][0]["english"] = "Pencil"
        with self.assertRaises(audio.PipelineError):
            build.require_picture(changed, self.output, 15, renderer_profile=RENDERER)

    def test_preschool_pilot_flag_cannot_bypass_elementary_provenance(self):
        checks = {**self.checks, "imported_from_pilot": True,
                  "renderer_sha256": build.renderer_fingerprint(15)}
        audio.atomic_json(self.output / "ep01/checks.json", checks)
        self.assertFalse(build.valid_final(self.episode, self.output, 15, renderer_profile=RENDERER))
        with self.assertRaisesRegex(shared_verify.VerificationError, "pilots cannot"):
            verify_media(self.episode, self.output, checks)

    def test_elementary_player_changes_only_template_branding(self):
        title = "PRESCHOOL 幼兒啟蒙 </script><script>bad()</script>"
        episodes = [{**self.episode, "id": f"ep{n:02d}", "number": n, "title_zh_TW": title}
                    for n in range(1, 13)]
        path = write_player({"episodes": episodes}, self.output)
        page = path.read_text()
        self.assertIn("ELEMENTARY · SEASON 1 · 12 LESSONS", page)
        self.assertIn("國小低年級英文第一季", page)
        self.assertIn('const seasonNames = {"1": "第 1 季・我的英文教室"};', page)
        self.assertIn("PRESCHOOL 幼兒啟蒙 \\u003c/script\\u003e", page)
        self.assertNotIn("<script>bad()</script>", page)

    def test_structure_rejects_omitted_episode_and_wrong_season(self):
        episodes = []
        for number in range(1, 13):
            episode = {**self.episode, "id": f"ep{number:02d}", "number": number,
                       "objectives_zh_TW": ["認識書本"],
                       "titles": {locale: "Book" for locale in audio.CC_LOCALES},
                       "scenes": [{"id": f"ep{number:02d}-s{scene:02d}", "mode": "demo", "wait_seconds": 5}
                                  for scene in range(1, 11)]}
            episodes.append(episode)
        self.assertEqual(verify_structure({"episodes": episodes})["scenes"], 120)
        with self.assertRaises(shared_verify.VerificationError):
            verify_structure({"episodes": episodes[:-1]})
        episodes[-1]["season"] = 2
        with self.assertRaises(shared_verify.VerificationError):
            verify_structure({"episodes": episodes})


class BatchStatusTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="elementary-batch-test-")
        self.addCleanup(temporary.cleanup)
        self.output = Path(temporary.name)
        self.status_path = self.output / "batch-status.json"
        # Resume must replace a previous successful receipt even if the new run
        # fails before its first normal progress update.
        audio.atomic_json(self.status_path, {"passed": True, "status": "passed"})

    def run_context(self, episodes, manifest):
        context = ExitStack()
        self.addCleanup(context.close)
        context.enter_context(patch.object(sys, "argv", ["batch.py", "--source", str(self.output / "source.json"),
                                                        "--output", str(self.output), "--watch-audio"]))
        context.enter_context(patch.object(batch.audio, "load_source", return_value={"episodes": episodes}))
        audio.atomic_json(self.output / "lessons.resolved.json", {"episodes": episodes})
        audio.atomic_json(self.output / "audio-manifest.json", manifest)
        context.enter_context(patch.object(batch.audio, "source_matches", return_value=True))
        context.enter_context(patch.object(batch.time, "sleep"))
        return context

    def assert_failed_status(self, message):
        status = audio.read_json(self.status_path)
        self.assertFalse(status["passed"])
        self.assertEqual(status["status"], "failed")
        self.assertEqual(status["active"], [])
        self.assertIn(message, status["error"])
        return status

    def test_audio_producer_failure_replaces_old_success_receipt(self):
        context = self.run_context([{"id": "ep01"}], {"status": "failed"})
        context.enter_context(patch.object(batch.audio, "episode_audio_ready", return_value=False))
        process = context.enter_context(patch.object(batch.subprocess, "Popen"))
        write = context.enter_context(patch.object(player, "write_player"))
        with self.assertRaisesRegex(RuntimeError, "Audio producer failed"):
            batch.main()
        self.assert_failed_status("Audio producer failed")
        process.assert_not_called()
        write.assert_not_called()

    def test_worker_failure_terminates_other_workers_and_closes_logs(self):
        episodes = [{"id": "ep01"}, {"id": "ep02"}]
        context = self.run_context(episodes, {"episodes": episodes})
        context.enter_context(patch.object(batch.audio, "episode_audio_ready", return_value=True))
        context.enter_context(patch.object(batch.build, "valid_final", return_value=False))
        failed = Mock()
        failed.poll.return_value = 7
        active = Mock()
        active.poll.return_value = None
        process = context.enter_context(patch.object(batch.subprocess, "Popen", side_effect=[failed, active]))
        write = context.enter_context(patch.object(player, "write_player"))
        with self.assertRaisesRegex(RuntimeError, "build exit 7"):
            batch.main()
        status = self.assert_failed_status("build exit 7")
        self.assertIn("ep01", status["failed"])
        active.terminate.assert_called_once_with()
        active.wait.assert_called_once_with(timeout=10)
        self.assertTrue(all(call.kwargs["stdout"].closed for call in process.call_args_list))
        write.assert_not_called()

    def test_success_is_recorded_only_after_player_finishes(self):
        for player_fails in (True, False):
            with self.subTest(player_fails=player_fails):
                episodes = [{"id": "ep01"}]
                with self.run_context(episodes, {"episodes": episodes}) as context:
                    context.enter_context(patch.object(batch.audio, "episode_audio_ready", return_value=True))
                    context.enter_context(patch.object(batch.build, "valid_final", return_value=True))
                    context.enter_context(patch.object(batch.subprocess, "Popen"))
                    events = []
                    atomic_json = audio.atomic_json

                    def observe_receipt(path, value):
                        if path == self.status_path and value.get("passed"):
                            self.assertEqual(events, ["player finished"])
                        atomic_json(path, value)

                    def write_player(*args):
                        status = audio.read_json(self.status_path)
                        self.assertFalse(status["passed"])
                        self.assertEqual(status["status"], "rendering")
                        if player_fails:
                            raise OSError("player write failed")
                        events.append("player finished")

                    context.enter_context(patch.object(batch.audio, "atomic_json", side_effect=observe_receipt))
                    context.enter_context(patch.object(player, "write_player", side_effect=write_player))
                    if player_fails:
                        with self.assertRaisesRegex(OSError, "player write failed"):
                            batch.main()
                        self.assert_failed_status("player write failed")
                    else:
                        self.assertEqual(batch.main(), 0)
                        status = audio.read_json(self.status_path)
                        self.assertTrue(status["passed"])
                        self.assertEqual(status["status"], "passed")
                        self.assertEqual(status["active"], [])


if __name__ == "__main__":
    unittest.main()
