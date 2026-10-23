"""Offline admission, course isolation and packaging regressions; no codecs or TTS."""
from __future__ import annotations

import copy
from contextlib import ExitStack
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from elementary.profile import RENDERER as ORIGINAL_RENDERER
from elementary_series import batch, build as course_build, package_series, player
from elementary_series.profile import ElementarySeriesRenderer, RENDERER, renderer_for
from elementary_series.shared import audio, build, verify
from elementary_series.verify_series import verify_structure


def lesson(number: int) -> dict:
    eid = f"ep{number:02d}"
    scenes = []
    for index in range(1, 11):
        mode = "quiz" if index in {5, 7, 9} else "repeat" if index == 4 else "demo"
        scene = {"id": f"{eid}-s{index:02d}", "mode": mode, "wait_seconds": 6 if mode == "quiz" else 5,
                 "english": "Listen and choose." if mode == "quiz" else "A book.", "demo": "A book.",
                 "visual": "book", "instruction": {locale: "Listen and choose." for locale in audio.VOICES},
                 "demo_translation": {locale: "A book." for locale in audio.CC_LOCALES}}
        if mode == "quiz":
            scene.update(choices=["book", "pencil"], target="book")
        if mode == "repeat":
            scene["guided_reading"] = True
        scenes.append(scene)
    return {"id": eid, "number": number, "season": (number - 1) // 12 + 1, "duration": 180,
            "title_en": "Our class", "title_zh_TW": "教室", "objectives_zh_TW": ["練習說一句話"],
            "titles": {locale: "Class" for locale in audio.CC_LOCALES}, "scenes": scenes,
            "practice": {"prompt_en": "Write one word.", "prompt_zh_TW": "寫一個單字。", "sample_answer_en": "book"}}


class CourseTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="elementary-complete-test-")
        self.addCleanup(temporary.cleanup)
        self.output = Path(temporary.name)

    def test_renderer_selection_preserves_first_season_and_rejects_unknowns(self):
        self.assertIs(renderer_for(lesson(1)), ORIGINAL_RENDERER)
        self.assertIs(renderer_for(lesson(12)), ORIGINAL_RENDERER)
        for number in (13, 24, 25, 48, 49, 72):
            self.assertIs(renderer_for(lesson(number)), RENDERER)
        for season in (None, 0, 7, True, "1"):
            with self.assertRaises(audio.PipelineError):
                renderer_for({"id": "bad", "season": season})

    def test_all_artwork_dependencies_are_bound_and_recorded_library_is_used(self):
        profile = ElementarySeriesRenderer()
        library = {"name": "Pillow", "version": "fixture"}
        copies = {}
        for index, (name, source) in enumerate(profile.source_paths().items()):
            self.assertTrue(source.is_file(), name)
            path = self.output / f"source-{index}.py"
            path.write_bytes(source.read_bytes())
            copies[name] = path
        self.assertTrue({"elementary_series/visuals.py", "elementary_series/objects.py",
                         "elementary_series/profile.py", "elementary_series/shared.py",
                         "elementary/visuals.py", "elementary/objects.py", "elementary/profile.py",
                         "elementary/shared.py", "preschool/visuals.py", "preschool/objects.py",
                         "preschool/build.py"}.issubset(copies))
        with patch.object(profile, "source_paths", return_value=copies):
            initial = profile.fingerprint(15, library)
            for name, path in copies.items():
                original = path.read_bytes()
                path.write_bytes(original + b"\n# changed dependency\n")
                self.assertNotEqual(initial, profile.fingerprint(15, library), name)
                path.write_bytes(original)
            record = {"renderer_profile": profile.name, "renderer_version": build.RENDER_VERSION,
                      "render_library": library}
            with patch.object(build, "render_library", side_effect=AssertionError("should use recorded library")):
                self.assertEqual(initial, profile.recorded_fingerprint(record, 15))
            self.assertIsNone(profile.recorded_fingerprint({**record, "renderer_profile": ORIGINAL_RENDERER.name}, 15))

    def test_structure_accepts_unchanged_first_season_and_all_six_seasons(self):
        source = {"episodes": [lesson(n) for n in range(1, 73)]}
        for episode in source["episodes"][:12]:
            episode.pop("practice")
            for scene in episode["scenes"]:
                scene.pop("guided_reading", None)
        result = verify_structure(source)
        self.assertEqual(result["scenes"], 720)
        self.assertEqual(result["seasons"], {n: 12 for n in range(1, 7)})

    def test_structure_rejects_missing_or_misgrouped_episodes_and_incomplete_teaching(self):
        baseline = {"episodes": [lesson(n) for n in range(1, 73)]}
        mutations = [
            lambda x: x["episodes"].pop(),
            lambda x: x["episodes"][12].update(season=1),
            lambda x: x["episodes"][12]["scenes"][3].pop("guided_reading"),
            lambda x: x["episodes"][12]["practice"].pop("sample_answer_en"),
            lambda x: x["episodes"][12]["scenes"][4].update(english="A book."),
            lambda x: x["episodes"][12]["scenes"][4].update(choices=["book", "book"]),
            lambda x: x["episodes"][12]["scenes"][4]["instruction"].pop("ja"),
            lambda x: x["episodes"][12]["scenes"][6].update(mode="demo", wait_seconds=5),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index):
                changed = copy.deepcopy(baseline)
                mutate(changed)
                with self.assertRaises(verify.VerificationError):
                    verify_structure(changed)

    def test_player_brands_all_grades_and_embeds_only_selected_season(self):
        episodes = [lesson(n) for n in range(61, 73)]
        episodes[0]["title_zh_TW"] = "</script><script>bad()</script>"
        path = player.write_player({"episodes": episodes}, self.output)
        page = path.read_text(encoding="utf-8")
        self.assertIn("ELEMENTARY ENGLISH · 12 LESSONS", page)
        self.assertIn("國小低・中・高年級", page)
        self.assertIn("第 6 季・高年級・閱讀寫作與分享", page)
        self.assertNotIn("SEASON 1 ·", page)
        self.assertNotIn("國小低年級英文第一季", page)
        self.assertNotIn("<script>bad()</script>", page)
        data = json.loads(re.search(r'<script id="episode-data" type="application/json">(.*?)</script>', page, re.S).group(1))
        self.assertEqual([episode["id"] for episode in data], [f"ep{n}" for n in range(61, 73)])

    def test_season_archive_contains_only_its_media_and_no_english_cc(self):
        episodes = [lesson(n) for n in range(13, 25)]
        records = {e["id"]: {"duration": 180} for e in episodes}
        media = self.output / "media"
        for episode in episodes:
            for relative in package_series.EPISODE_FILES:
                path = media / episode["id"] / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                # These are membership/CRC fixtures, not valid media fixtures.
                path.write_text("fixture", encoding="utf-8")
        directory = self.output / "staged" / "Season_02"
        def fake_practice(selected, destination):
            paths = [destination / name for name in ("Practice.html", "Practice.pdf")]
            for path in paths:
                path.write_text("practice fixture: " + ",".join(e["id"] for e in selected), encoding="utf-8")
            return paths

        with patch.object(package_series, "write_practice", side_effect=fake_practice):
            package_series.stage_package({"episodes": [lesson(n) for n in range(1, 73)]},
                                         episodes, records, media, directory)
        archive = self.output / "season.zip"
        receipt = package_series.create_archive(directory, archive, episodes)
        self.assertEqual(receipt["episodes"], 12)
        self.assertEqual(receipt["files"], 209)
        self.assertEqual(receipt["episode_ids"], [e["id"] for e in episodes])
        with zipfile.ZipFile(archive) as handle:
            self.assertIsNone(handle.testzip())
            self.assertFalse(any(name.endswith(("/en.srt", "/en.vtt")) for name in handle.namelist()))
            page = handle.read("Season_02/index.html").decode()
        data = json.loads(re.search(r'<script id="episode-data" type="application/json">(.*?)</script>', page, re.S).group(1))
        self.assertEqual(len(data), 12)
        self.assertTrue(all(e["season"] == 2 for e in data))

    def test_build_uses_season_specific_profile_for_skip_render_and_mux(self):
        episodes = [lesson(1), lesson(13)]
        argv = ["build.py", "--source", str(self.output / "resolved.json"), "--output", str(self.output),
                "--skip-valid", "--no-player"]
        with patch.object(sys, "argv", argv), patch.object(audio, "read_json", return_value={"episodes": episodes}), \
                patch.object(audio, "audio_integrity"), patch.object(build, "valid_final", return_value=False) as valid, \
                patch.object(build, "render") as render, patch.object(build, "mux") as mux:
            course_build.main()
        for operation in (valid, render, mux):
            self.assertEqual([call.kwargs["renderer_profile"] for call in operation.call_args_list],
                             [ORIGINAL_RENDERER, RENDERER])


class PackageSourceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="elementary-package-source-")
        self.addCleanup(temporary.cleanup)
        self.output = Path(temporary.name)
        self.source_path = self.output / "authoring.json"
        self.resolved_path = self.output / "lessons.resolved.json"
        self.source = {"episodes": [lesson(n) for n in range(1, 73)]}
        self.resolved = copy.deepcopy(self.source)
        for authored, measured in zip(self.source["episodes"], self.resolved["episodes"]):
            measured["source_sha256"] = audio.source_fingerprint(authored)
        audio.atomic_json(self.source_path, self.source)
        audio.atomic_json(self.resolved_path, self.resolved)
        self.existing_archive = self.output / package_series.ALL_ARCHIVE_NAME
        self.existing_archive.write_bytes(b"previous checked archive")

    def test_changed_practice_or_demo_cannot_publish_old_media(self):
        for field in ("practice", "demo"):
            with self.subTest(field=field):
                changed = copy.deepcopy(self.source)
                if field == "practice":
                    changed["episodes"][12]["practice"]["sample_answer_en"] = "pencil"
                else:
                    changed["episodes"][12]["scenes"][0]["demo"] = "A pencil."
                audio.atomic_json(self.source_path, changed)
                with patch.object(package_series, "verify_output") as full_verify, \
                        patch.object(package_series.tempfile, "TemporaryDirectory") as staging:
                    with self.assertRaisesRegex(verify.VerificationError, "current authoring"):
                        package_series.package_series(self.source_path, self.resolved_path, self.output)
                    full_verify.assert_not_called()
                    staging.assert_not_called()
                self.assertEqual(self.existing_archive.read_bytes(), b"previous checked archive")
                self.assertFalse((self.output / "package-checks.json").exists())

    def test_matching_source_hash_cannot_hide_changed_authored_fields(self):
        changed = copy.deepcopy(self.resolved)
        changed["episodes"][12]["practice"]["sample_answer_en"] = "stale worksheet"
        audio.atomic_json(self.resolved_path, changed)
        with patch.object(package_series, "verify_output") as full_verify:
            with self.assertRaisesRegex(verify.VerificationError, "current authoring"):
                package_series.preflight(self.source, changed, self.output)
            full_verify.assert_not_called()

    def test_alternate_resolution_cannot_bypass_verified_output(self):
        alternate_path = self.output / "different.resolved.json"
        audio.atomic_json(alternate_path, self.resolved)
        with self.assertRaisesRegex(verify.VerificationError, "output directory"):
            package_series.package_series(self.source_path, alternate_path, self.output)
        alternate = copy.deepcopy(self.resolved)
        alternate["episodes"][12]["duration"] = 181
        with self.assertRaisesRegex(verify.VerificationError, "output resolution"):
            package_series.preflight(self.source, alternate, self.output)
        self.assertEqual(self.existing_archive.read_bytes(), b"previous checked archive")

    def test_full_verification_must_pass_before_creating_any_archive(self):
        with patch.object(package_series, "verify_output", return_value={
                "passed": False, "status": "failed", "errors": [{"episode": "ep13", "error": "stale clip"}]}), \
                patch.object(package_series.tempfile, "TemporaryDirectory") as staging:
            with self.assertRaisesRegex(verify.VerificationError, "stale clip"):
                package_series.package_series(self.source_path, self.resolved_path, self.output)
            staging.assert_not_called()
        self.assertEqual(self.existing_archive.read_bytes(), b"previous checked archive")

    def test_matching_current_source_packages_all_seasons_and_records_both_hashes(self):
        # Admission is exercised with real source fingerprints and archive CRCs.
        # Codec/timing validation is represented by its successful verifier result.
        for episode in self.resolved["episodes"]:
            for relative in package_series.EPISODE_FILES:
                path = self.output / episode["id"] / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                if relative == "checks.json":
                    audio.atomic_json(path, {"duration": 180})
                else:
                    path.write_text("fixture", encoding="utf-8")

        def fake_practice(selected, destination):
            paths = [destination / name for name in ("Practice.html", "Practice.pdf")]
            for path in paths:
                path.write_text("Practice: " + ",".join(e["id"] for e in selected), encoding="utf-8")
            return paths

        with patch.object(package_series, "verify_output", return_value={"passed": True}) as full_verify, \
                patch.object(package_series, "write_practice", side_effect=fake_practice):
            report = package_series.package_series(self.source_path, self.resolved_path, self.output)
        full_verify.assert_called_once_with(self.source, self.output)
        self.assertTrue(report["ready"])
        self.assertEqual(len(report["packages"]), 7)
        self.assertEqual(report["source_sha256"], build.file_sha256(self.source_path))
        self.assertEqual(report["resolved_sha256"], build.file_sha256(self.resolved_path))
        self.assertEqual(report["packages"][-1]["episodes"], 72)
        self.assertEqual(report["packages"][-1]["files"], 1229)
        self.assertEqual(audio.read_json(self.output / "package-checks.json"), report)


class BatchTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="elementary-complete-batch-")
        self.addCleanup(temporary.cleanup)
        self.output = Path(temporary.name)
        self.status_path = self.output / "batch-status.json"
        audio.atomic_json(self.status_path, {"passed": True, "status": "passed"})

    def context(self, episodes, manifest=None):
        context = ExitStack()
        self.addCleanup(context.close)
        context.enter_context(patch.object(sys, "argv", ["batch.py", "--source", str(self.output / "source.json"),
                                                        "--output", str(self.output), "--watch-audio"]))
        context.enter_context(patch.object(audio, "load_source", return_value={"episodes": episodes}))
        audio.atomic_json(self.output / "lessons.resolved.json", {"episodes": episodes})
        audio.atomic_json(self.output / "audio-manifest.json", manifest or {"episodes": episodes})
        context.enter_context(patch.object(audio, "source_matches", return_value=True))
        context.enter_context(patch.object(batch.time, "sleep"))
        return context

    def assert_failed(self, message):
        status = audio.read_json(self.status_path)
        self.assertFalse(status["passed"])
        self.assertEqual(status["status"], "failed")
        self.assertIn(message, status["error"])
        return status

    def test_producer_failure_overwrites_old_success_and_starts_no_worker(self):
        context = self.context([lesson(13)], {"status": "failed"})
        context.enter_context(patch.object(audio, "episode_audio_ready", return_value=False))
        process = context.enter_context(patch.object(batch.subprocess, "Popen"))
        with self.assertRaisesRegex(RuntimeError, "Audio producer failed"):
            batch.main()
        self.assert_failed("Audio producer failed")
        process.assert_not_called()

    def test_zero_worker_exit_without_verified_final_is_failure(self):
        context = self.context([lesson(13)])
        context.enter_context(patch.object(audio, "episode_audio_ready", return_value=True))
        context.enter_context(patch.object(build, "valid_final", return_value=False))
        process = Mock()
        process.poll.return_value = 0
        context.enter_context(patch.object(batch.subprocess, "Popen", return_value=process))
        write = context.enter_context(patch.object(player, "write_player"))
        with self.assertRaisesRegex(RuntimeError, "without a valid"):
            batch.main()
        self.assert_failed("without a valid")
        write.assert_not_called()

    def test_failed_worker_terminates_other_worker_and_closes_logs(self):
        context = self.context([lesson(13), lesson(14)])
        context.enter_context(patch.object(audio, "episode_audio_ready", return_value=True))
        context.enter_context(patch.object(build, "valid_final", return_value=False))
        failed, active = Mock(), Mock()
        failed.poll.return_value, active.poll.return_value = 7, None
        processes = context.enter_context(patch.object(batch.subprocess, "Popen", side_effect=[failed, active]))
        with self.assertRaisesRegex(RuntimeError, "build exit 7"):
            batch.main()
        self.assert_failed("build exit 7")
        active.terminate.assert_called_once_with()
        active.wait.assert_called_once_with(timeout=10)
        self.assertTrue(all(call.kwargs["stdout"].closed for call in processes.call_args_list))

    def test_player_failure_prevents_success_even_when_resume_media_are_valid(self):
        context = self.context([lesson(1), lesson(13)])
        context.enter_context(patch.object(audio, "episode_audio_ready", return_value=True))
        valid = context.enter_context(patch.object(build, "valid_final", return_value=True))
        context.enter_context(patch.object(player, "write_player", side_effect=OSError("player failure")))
        with self.assertRaisesRegex(OSError, "player failure"):
            batch.main()
        self.assert_failed("player failure")
        self.assertEqual([call.kwargs["renderer_profile"] for call in valid.call_args_list],
                         [ORIGINAL_RENDERER, RENDERER])

    def test_success_is_recorded_after_the_player_is_written(self):
        context = self.context([lesson(13)])
        context.enter_context(patch.object(audio, "episode_audio_ready", return_value=True))
        context.enter_context(patch.object(build, "valid_final", return_value=True))

        def player_write(*args):
            self.assertFalse(audio.read_json(self.status_path)["passed"])

        context.enter_context(patch.object(player, "write_player", side_effect=player_write))
        self.assertEqual(batch.main(), 0)
        self.assertTrue(audio.read_json(self.status_path)["passed"])


if __name__ == "__main__":
    unittest.main()
