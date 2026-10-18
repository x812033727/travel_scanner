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
from junior_high import batch, build as course_build, package_series, player, objects
from junior_high.profile import JuniorHighRenderer, RENDERER, renderer_for
from junior_high.shared import audio, build, verify
from junior_high.verify_series import verify_structure, verify_output, SERIES_TITLE, QUIZ_INSTRUCTIONS


def course(episodes=None):
    return {"series_title": SERIES_TITLE, "version": 3,
            "episodes": episodes if episodes is not None else [lesson(n) for n in range(1, 73)]}


def lesson(number: int) -> dict:
    eid = f"ep{number:02d}"
    season = (number - 1) // 12 + 1
    grade = 7 + (season - 1) // 2
    scenes = []
    for index in range(1, 11):
        mode = "quiz" if index in {5, 7, 9} else "repeat" if index in {4, 8} else "demo"
        scene = {"id": f"{eid}-s{index:02d}", "mode": mode, "wait_seconds": 6 if mode == "quiz" else 5,
                 "english": "Listen and choose." if mode == "quiz" else "A book.", "demo": "A book.",
                 "visual": "sentence:A book.", "target": "sentence:A book.", "note_zh_TW": "聽讀練習",
                 "instruction": dict(QUIZ_INSTRUCTIONS),
                 "demo_translation": {locale: "A book." for locale in audio.CC_LOCALES}}
        if mode == "quiz":
            choices = ["sentence:A book.", "sentence:A pencil.", "sentence:A desk."]
            offset = (index - 5) // 2
            choices = choices[-offset:] + choices[:-offset] if offset else choices
            scene.update(choices=choices)
        if mode == "repeat":
            scene["guided_reading"] = True
        scenes.append(scene)
    reading = "Sam reads in the library after school. His friend Amy reads with him. They choose a short story about a quiet town. Sam likes the story because its people help each other."
    if grade >= 8:
        reading += " Amy writes a message to share this idea with her class."
    if grade == 9:
        reading += " Their teacher invites everyone to give an example from the story."
    return {"id": eid, "number": number, "season": season, "grade": grade, "duration": 180,
            "title_en": "Our class", "title_zh_TW": "教室", "topic": "School life",
            "parent_tip_zh_TW": "根據短文回答問題。", "objectives_zh_TW": ["讀懂句子", "找出細節", "寫出例句"],
            "titles": {locale: "Class" for locale in audio.CC_LOCALES}, "scenes": scenes,
            "practice": {"prompt_en": "Write three sentences about a school day.", "prompt_zh_TW": "寫三句話。",
                         "sample_answer_en": "I read after school. I like stories. I share them with Amy.",
                         "reading_en": reading, "questions": [
                             {"prompt_en": "Where does Sam read?", "answer_en": "In the library."},
                             {"prompt_en": "Who reads with Sam?", "answer_en": "Amy."},
                             {"prompt_en": "What do people in the story do?", "answer_en": "They help each other."}]}}


class CourseTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="junior-high-complete-test-")
        self.addCleanup(temporary.cleanup)
        self.output = Path(temporary.name)

    def test_uniform_renderer_covers_all_new_seasons_and_rejects_unknowns(self):
        self.assertIs(renderer_for(lesson(1)), RENDERER)
        self.assertIs(renderer_for(lesson(12)), RENDERER)
        for number in (13, 24, 25, 48, 49, 72):
            self.assertIs(renderer_for(lesson(number)), RENDERER)
        for season in (None, 0, 7, True, "1"):
            with self.assertRaises(audio.PipelineError):
                renderer_for({"id": "bad", "season": season})

    def test_all_artwork_dependencies_are_bound_and_recorded_library_is_used(self):
        profile = JuniorHighRenderer()
        library = {"name": "Pillow", "version": "fixture"}
        copies = {}
        fixture_fonts = tuple(self.output / name for name in ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf"))
        for path in fixture_fonts:
            path.write_bytes(b"font fixture")
        fonts = patch.object(objects, "FONT_PATHS", fixture_fonts)
        fonts.start()
        self.addCleanup(fonts.stop)
        for index, (name, source) in enumerate(profile.source_paths().items()):
            self.assertTrue(source.is_file(), name)
            path = self.output / f"source-{index}.py"
            path.write_bytes(source.read_bytes())
            copies[name] = path
        self.assertTrue({"junior_high/visuals.py", "junior_high/objects.py",
                         "junior_high/profile.py", "junior_high/shared.py",
                         "elementary_series/visuals.py", "elementary_series/objects.py",
                         "elementary/visuals.py", "elementary/objects.py", "elementary/profile.py",
                         "elementary/shared.py", "preschool/visuals.py", "preschool/objects.py",
                         "preschool/build.py", "fonts/DejaVuSans.ttf", "fonts/DejaVuSans-Bold.ttf"}.issubset(copies))
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

    def test_structure_requires_new_practice_and_uniform_profile_in_every_season(self):
        result = verify_structure(course())
        self.assertEqual(result["scenes"], 720)
        self.assertEqual(result["seasons"], {n: 12 for n in range(1, 7)})
        self.assertEqual(result["grades"], {7: 24, 8: 24, 9: 24})
        self.assertEqual(result["renderer_profiles"], {"all_six_seasons": RENDERER.name})

    def test_only_explicit_authoring_subset_admits_complete_seasons(self):
        source = course([lesson(n) for n in range(13, 25)])
        with self.assertRaises(verify.VerificationError):
            verify_structure(source)
        report = verify_structure(source, allow_season_subset=True)
        self.assertFalse(report["complete_course"])
        self.assertEqual(report["seasons"], {2: 12})
        source["episodes"].pop()
        with self.assertRaisesRegex(verify.VerificationError, "complete seasons"):
            verify_structure(source, allow_season_subset=True)

    def test_structure_rejects_missing_or_misgrouped_episodes_and_incomplete_teaching(self):
        baseline = course()
        mutations = [
            lambda x: x["episodes"].pop(),
            lambda x: x["episodes"][12].update(season=1),
            lambda x: x["episodes"][12]["scenes"][3].pop("guided_reading"),
            lambda x: x["episodes"][12]["practice"].pop("sample_answer_en"),
            lambda x: x["episodes"][12]["scenes"][4].update(english="A book."),
            lambda x: x["episodes"][12]["scenes"][4].update(choices=["book", "book"]),
            lambda x: x["episodes"][12]["scenes"][4]["instruction"].pop("ja"),
            lambda x: x["episodes"][12]["scenes"][6].update(mode="demo", wait_seconds=5),
            lambda x: x["episodes"][0].update(grade=8),
            lambda x: x["episodes"][0]["scenes"][0].update(visual="sentence:unsupported\nline"),
            lambda x: x["episodes"][0]["practice"].pop("reading_en"),
            lambda x: x["episodes"][0]["practice"]["questions"].pop(),
            lambda x: x["episodes"][0]["practice"]["questions"][0].update(extra="not allowed"),
            lambda x: x["episodes"][0]["scenes"][0].update(demo="word " * 17),
            lambda x: x["episodes"][0]["scenes"][0].update(demo="Here’s a book."),
            lambda x: x["episodes"][0]["scenes"][4]["instruction"].update(ja="answer"),
            lambda x: [scene.update(choices=[scene["target"], "word:other"])
                       for scene in x["episodes"][0]["scenes"] if scene["mode"] == "quiz"],
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
        self.assertIn("JUNIOR HIGH · 12 LESSONS", page)
        self.assertIn("國一・國二・國三", page)
        self.assertIn("第 6 季・國三・閱讀寫作與溝通", page)
        self.assertNotIn("SEASON 1 ·", page)
        self.assertNotIn("國小低年級英文第一季", page)
        self.assertNotIn("<script>bad()</script>", page)
        self.assertIn("English Lab", page)
        self.assertIn("自學提醒", page)
        self.assertIn('id="study-tip"', page)
        self.assertNotIn("孩子", page)
        self.assertNotIn("幼兒", page)
        self.assertIn('href="Practice.pdf"', page)
        voice = re.search(r'<select id="voice">(.*?)</select>', page).group(1)
        cc = re.search(r'<select id="cc">(.*?)</select>', page).group(1)
        self.assertEqual(len(re.findall('<option ', voice)), 5)
        self.assertEqual(len(re.findall('<option ', cc)), 5)
        self.assertNotIn('value="en"', cc)
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
            package_series.stage_package(course(),
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

    def test_build_uses_uniform_new_profile_for_skip_render_and_mux(self):
        episodes = [lesson(1), lesson(13)]
        argv = ["build.py", "--source", str(self.output / "resolved.json"), "--output", str(self.output),
                "--skip-valid", "--no-player"]
        with patch.object(sys, "argv", argv), patch.object(audio, "read_json", return_value=course(episodes)), \
                patch.object(audio, "audio_integrity"), patch.object(build, "valid_final", return_value=False) as valid, \
                patch.object(build, "render") as render, patch.object(build, "mux") as mux:
            course_build.main()
        for operation in (valid, render, mux):
            self.assertEqual([call.kwargs["renderer_profile"] for call in operation.call_args_list],
                             [RENDERER, RENDERER])

    def test_final_admission_rejects_stale_source_renderer_decode_and_same_size_media_changes(self):
        episode = lesson(1)
        directory = self.output / episode["id"]
        directory.mkdir()
        final = directory / "final.mp4"
        final.write_bytes(b"verified media fixture")
        profile = Mock()
        profile.recorded_fingerprint.return_value = "current-renderer"
        record = {"full_decode": True, "source_sha256": build.fingerprint(episode),
                  "renderer_sha256": "current-renderer", "bytes": final.stat().st_size,
                  "final_sha256": build.file_sha256(final)}
        with patch.object(build, "audio_integrity"):
            audio.atomic_json(directory / "checks.json", record)
            self.assertTrue(build.valid_final(episode, self.output, 15, renderer_profile=profile))
            for change in ({"source_sha256": "old"}, {"renderer_sha256": "old"}, {"full_decode": False}):
                audio.atomic_json(directory / "checks.json", {**record, **change})
                self.assertFalse(build.valid_final(episode, self.output, 15, renderer_profile=profile))
            audio.atomic_json(directory / "checks.json", record)
            final.write_bytes(b"x" * record["bytes"])
            self.assertFalse(build.valid_final(episode, self.output, 15, renderer_profile=profile))

    def test_partial_report_never_claims_full_course_completion(self):
        partial = verify_output(course(), self.output, allow_partial=True)
        self.assertEqual(partial["status"], "partial")
        self.assertFalse(partial["passed"])
        self.assertEqual(len(partial["missing"]), 72)
        strict = verify_output(course(), self.output)
        self.assertEqual(strict["status"], "failed")
        self.assertTrue(any(item["check"] == "complete_series" for item in strict["errors"]))
        subset = verify_output(course([lesson(n) for n in range(1, 13)]), self.output, allow_partial=True)
        self.assertEqual(subset["status"], "failed")
        self.assertTrue(any(item["check"] == "structure" for item in subset["errors"]))

    def test_matching_hash_cannot_hide_stale_reading_from_output_verification(self):
        source = course()
        measured = copy.deepcopy(source["episodes"][0])
        measured["source_sha256"] = audio.source_fingerprint(source["episodes"][0])
        measured["practice"]["questions"][0]["answer_en"] = "Old stale answer."
        directory = self.output / "ep01"
        directory.mkdir()
        (directory / "final.mp4").write_bytes(b"fixture")
        audio.atomic_json(directory / "checks.json", {})
        audio.atomic_json(self.output / "lessons.resolved.json", course([measured]))
        with patch.object(verify, "verify_timing") as timing:
            report = verify_output(source, self.output, allow_partial=True)
        timing.assert_not_called()
        self.assertFalse(report["passed"])
        self.assertEqual(report["errors"][0]["check"], "current_authoring")


class PackageSourceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="junior-high-package-source-")
        self.addCleanup(temporary.cleanup)
        self.output = Path(temporary.name)
        self.source_path = self.output / "authoring.json"
        self.resolved_path = self.output / "lessons.resolved.json"
        self.source = course()
        self.resolved = copy.deepcopy(self.source)
        for authored, measured in zip(self.source["episodes"], self.resolved["episodes"]):
            measured["source_sha256"] = audio.source_fingerprint(authored)
        audio.atomic_json(self.source_path, self.source)
        audio.atomic_json(self.resolved_path, self.resolved)
        self.existing_archive = self.output / package_series.ALL_ARCHIVE_NAME
        self.existing_archive.write_bytes(b"previous checked archive")

    def test_changed_practice_or_demo_cannot_publish_old_media(self):
        for field in ("practice", "reading", "answer", "demo"):
            with self.subTest(field=field):
                changed = copy.deepcopy(self.source)
                if field == "practice":
                    changed["episodes"][12]["practice"]["sample_answer_en"] = "pencil"
                elif field == "reading":
                    changed["episodes"][12]["practice"]["reading_en"] = changed["episodes"][12]["practice"]["reading_en"].replace("Sam", "Tim")
                elif field == "answer":
                    changed["episodes"][12]["practice"]["questions"][0]["answer_en"] = "In the classroom."
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
        self.assertEqual([item["file"] for item in report["packages"]],
                         [f"Sunny_Pip_Junior_High_Season_{season:02d}.zip" for season in range(1, 7)]
                         + ["Sunny_Pip_Junior_High_72_Episodes.zip"])
        self.assertTrue(all(item["files"] == 209 for item in report["packages"][:6]))
        self.assertEqual(report["renderer_profiles"], {"all_six_seasons": RENDERER.name})
        catalog = (self.output / package_series.CATALOG_NAME).read_bytes()
        self.assertTrue(catalog.startswith(b"\xef\xbb\xbf"))
        self.assertEqual(len(catalog.decode("utf-8-sig").splitlines()), 73)
        for grade in ("國一", "國二", "國三"):
            self.assertIn(grade, catalog.decode("utf-8-sig"))
        self.assertEqual(audio.read_json(self.output / "package-checks.json"), report)


class BatchTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="junior-high-complete-batch-")
        self.addCleanup(temporary.cleanup)
        self.output = Path(temporary.name)
        self.status_path = self.output / "batch-status.json"
        audio.atomic_json(self.status_path, {"passed": True, "status": "passed"})

    def context(self, episodes, manifest=None):
        context = ExitStack()
        self.addCleanup(context.close)
        context.enter_context(patch.object(sys, "argv", ["batch.py", "--source", str(self.output / "source.json"),
                                                        "--output", str(self.output), "--watch-audio"]))
        context.enter_context(patch.object(audio, "load_source", return_value=course(episodes)))
        audio.atomic_json(self.output / "lessons.resolved.json", course(episodes))
        audio.atomic_json(self.output / "audio-manifest.json", manifest or {"episodes": episodes})
        context.enter_context(patch.object(audio, "source_matches", return_value=True))
        context.enter_context(patch.object(batch, "verify_structure"))
        context.enter_context(patch.object(batch.time, "sleep"))
        return context

    def assert_failed(self, message):
        status = audio.read_json(self.status_path)
        self.assertFalse(status["passed"])
        self.assertEqual(status["status"], "failed")
        self.assertIn(message, status["error"])
        return status

    def test_complete_season_can_stream_only_with_explicit_subset_flag(self):
        source_path = self.output / "season01.json"
        source = course([lesson(n) for n in range(1, 13)])
        audio.atomic_json(source_path, source)
        audio.atomic_json(self.output / "lessons.resolved.json", course([*source["episodes"], lesson(13)]))
        audio.atomic_json(self.output / "audio-manifest.json", {"episodes": source["episodes"]})
        argv = ["batch.py", "--source", str(source_path), "--output", str(self.output)]
        with patch.object(sys, "argv", argv):
            with self.assertRaises(verify.VerificationError):
                batch.main()
        with patch.object(sys, "argv", argv + ["--allow-season-subset"]), \
                patch.object(audio, "episode_audio_ready", return_value=True), \
                patch.object(build, "valid_final", return_value=True), \
                patch.object(player, "write_player") as write:
            self.assertEqual(batch.main(), 0)
        status = audio.read_json(self.status_path)
        self.assertTrue(status["passed"])
        self.assertFalse(status["complete_course"])
        self.assertTrue(status["authoring_subset"])
        self.assertEqual(len(write.call_args.args[0]["episodes"]), 12)
        self.assertNotIn("ep13", status["complete"])

    def test_stale_authored_fields_cannot_enter_worker_queue_even_with_matching_hash(self):
        context = self.context([lesson(13)], {"status": "failed"})
        measured = lesson(13)
        measured["practice"]["questions"][0]["answer_en"] = "Stale answer."
        audio.atomic_json(self.output / "lessons.resolved.json", course([measured]))
        ready = context.enter_context(patch.object(audio, "episode_audio_ready", return_value=True))
        process = context.enter_context(patch.object(batch.subprocess, "Popen"))
        with self.assertRaisesRegex(RuntimeError, "Audio producer failed"):
            batch.main()
        ready.assert_not_called()
        process.assert_not_called()

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
                         [RENDERER, RENDERER])

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
