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
from adult_english import batch, build as course_build, package_series, player, objects
from adult_english.profile import AdultEnglishRenderer, RENDERER, renderer_for
from adult_english.shared import audio, build, verify
from adult_english.verify_series import verify_structure, verify_output, QUIZ_INSTRUCTIONS
from adult_english.config import COURSES, get_course, document_course


def course(episodes=None, kind="university"):
    if episodes:
        kind = episodes[0]["course"]
    return {"series_title": get_course(kind).series_title, "version": 4, "course": kind,
            "episodes": episodes if episodes is not None else [lesson(n, kind) for n in range(1, 49)]}


def lesson(number: int, kind: str = "university") -> dict:
    eid = f"ep{number:02d}"
    season = (number - 1) // 12 + 1
    scenes = []
    for index in range(1, 11):
        mode = "quiz" if index in {5, 7, 9} else "repeat" if index in {4, 8} else "review" if index == 10 else "demo"
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
    reading += "\n\nDuring a meeting, the group compares two possible reading schedules. One plan gives everyone a quiet hour on Friday, while the other offers shorter sessions on three days. Sam prefers the shorter sessions because students can discuss a new idea after each one. Amy asks the teacher to try the plan for a month before deciding whether it should continue."
    reading += " They will record attendance and ask members which schedule feels useful. The teacher explains that these classroom observations can guide a small decision but cannot represent every student in town."
    reading += " After the trial, the club will compare the notes from each meeting. Any recommendation should explain both the benefits and the limits of the evidence they gathered during the month."
    sample = "I study in the library after school because it gives me a quiet place to think. My friend Amy often joins me, and we compare notes about our lessons. We choose one question to discuss instead of trying to review everything at once. This small routine helps us notice ideas that we missed in class. I would recommend trying it for a week before making a longer plan."
    sample += " However, this approach may not suit students who prefer to work alone, so the group should offer a choice."
    sample += " We could also record which questions lead to useful discussion and use that evidence when we revise our study schedule."
    if kind == "university":
        reading += " The group will also compare alternative explanations before sharing its conclusion with other readers."
        sample += " Before reaching a conclusion, we should compare another explanation and ask whether the available evidence can distinguish between these different possibilities."
    writing_range = "-".join(map(str, get_course(kind).writing_range))
    return {"id": eid, "number": number, "season": season, "stage": season, "course": kind, "duration": 180,
            "title_en": "Our class", "title_zh_TW": "教室", "topic": "School life",
            "parent_tip_zh_TW": "根據短文回答問題。", "objectives_zh_TW": ["讀懂句子", "找出細節", "寫出例句"],
            "titles": {locale: "Class" for locale in audio.CC_LOCALES}, "scenes": scenes,
            "practice": {"prompt_en": f"Write {writing_range} words recommending a study routine with a reason and a limitation.", "prompt_zh_TW": f"寫 {writing_range} 詞，推薦學習習慣並說明理由與限制。",
                         **({"chart": {"title_en": "Fictional library visits", "labels": ["Before", "After"],
                                       "values": [40, 50], "axis_min": 35, "axis_max": 55,
                                       "unit_en": "visits"}} if number == 45 else {}),
                         "sample_answer_en": sample,
                         "reading_en": reading, "questions": [
                             {"prompt_en": "Where does Sam read?", "answer_en": "In the library."},
                             {"prompt_en": "Who reads with Sam?", "answer_en": "Amy."},
                             {"prompt_en": "What do people in the story do?", "answer_en": "They help each other."}]}}


class CourseTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="adult-English-complete-test-")
        self.addCleanup(temporary.cleanup)
        self.output = Path(temporary.name)

    def test_uniform_renderer_covers_all_new_seasons_and_rejects_unknowns(self):
        self.assertIs(renderer_for(lesson(1)), RENDERER)
        self.assertIs(renderer_for(lesson(12)), RENDERER)
        for number in (1, 12, 13, 24, 25, 36, 37, 48):
            self.assertIs(renderer_for(lesson(number)), RENDERER)
        for season in (None, 0, 5, True, "1"):
            with self.assertRaises(audio.PipelineError):
                renderer_for({"id": "bad", "season": season})

    def test_all_artwork_dependencies_are_bound_and_recorded_library_is_used(self):
        profile = AdultEnglishRenderer()
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
        self.assertTrue({"adult_english/visuals.py", "adult_english/objects.py",
                         "adult_english/profile.py", "adult_english/shared.py", "adult_english/config.py",
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
        self.assertEqual(result["scenes"], 480)
        self.assertEqual(result["seasons"], {n: 12 for n in range(1, 5)})
        self.assertEqual(result["stages"], {n: 12 for n in range(1, 5)})
        self.assertEqual(result["renderer_profiles"], {"all_four_seasons": RENDERER.name})

    def test_course_identity_rejects_mixed_headers_episodes_stages_and_legacy_grades(self):
        baseline = course()
        mutations = [
            lambda x: x.pop("course"),
            lambda x: x.update(course="workplace"),
            lambda x: x["episodes"][0].update(course="workplace"),
            lambda x: x["episodes"][0].update(stage=True),
            lambda x: x["episodes"][12].update(stage=1),
            lambda x: x["episodes"][0].update(grade=12),
        ]
        for mutate in mutations:
            changed = copy.deepcopy(baseline)
            mutate(changed)
            with self.assertRaises(verify.VerificationError):
                verify_structure(changed)
        with self.assertRaisesRegex(verify.VerificationError, "Wrong course"):
            verify_structure(baseline, course="workplace")
        self.assertEqual(verify_structure(course(kind="workplace"))["course"], "workplace")

    def test_identical_episode_ids_from_other_course_cannot_reuse_media_receipts(self):
        university = lesson(1)
        workplace = {**university, "course": "workplace"}
        measured = {**university, "source_sha256": audio.source_fingerprint(university)}
        self.assertFalse(audio.source_matches(workplace, measured))
        self.assertNotEqual(build.fingerprint(university), build.fingerprint(workplace))
        audio.atomic_json(self.output / "lessons.resolved.json", course(kind="workplace"))
        report = verify_output(course(), self.output, allow_partial=True)
        self.assertFalse(report["passed"])
        self.assertTrue(any(error["check"] == "course_identity" for error in report["errors"]))

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
            lambda x: x["episodes"][0].update(stage=8),
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

    def test_course_specific_reading_and_writing_boundaries_and_paragraphs(self):
        for kind, config in COURSES.items():
            source = course([lesson(n, kind) for n in range(1, 13)])
            first = source["episodes"][0]
            self.assertIn("\n\n", first["practice"]["reading_en"])
            self.assertFalse(verify_structure(source, allow_season_subset=True)["complete_course"])
            for field, (low, high) in zip(("reading_en", "sample_answer_en"), (config.reading_range, config.writing_range)):
                for count in (low, high):
                    changed = copy.deepcopy(source)
                    changed["episodes"][0]["practice"][field] = " ".join(["word"] * count)
                    verify_structure(changed, allow_season_subset=True)
                for count in (low - 1, high + 1):
                    changed = copy.deepcopy(source)
                    changed["episodes"][0]["practice"][field] = " ".join(["word"] * count)
                    with self.assertRaises(verify.VerificationError):
                        verify_structure(changed, allow_season_subset=True)

    def test_three_quizzes_must_use_all_three_answer_positions(self):
        source = course()
        scene = source["episodes"][0]["scenes"][8]
        scene["choices"] = [scene["target"], "sentence:A desk.", "sentence:A pencil."]
        with self.assertRaisesRegex(verify.VerificationError, "cover 0, 1 and 2"):
            verify_structure(source)

    def test_quiz_audio_matches_answer_and_distinct_tokens_cannot_hide_duplicate_text(self):
        source = course()
        source["episodes"][0]["scenes"][4]["demo"] = "A pencil."
        with self.assertRaisesRegex(verify.VerificationError, "target text must match"):
            verify_structure(source)
        source = course()
        source["episodes"][0]["scenes"][4]["choices"][1] = "word:A book."
        with self.assertRaisesRegex(verify.VerificationError, "distinct displayed texts"):
            verify_structure(source)

    def test_chart_is_optional_and_accepts_valid_scales(self):
        source = course()
        chart = source["episodes"][44]["practice"]["chart"]
        source["episodes"][0]["practice"]["chart"] = copy.deepcopy(chart)
        source["episodes"][0]["practice"]["chart"].update(values=[40.5, 50.5], axis_min=0, axis_max=50.5)
        self.assertTrue(verify_structure(source)["complete_course"])
        for episode in source["episodes"]:
            episode["practice"].pop("chart", None)
        self.assertTrue(verify_structure(source)["complete_course"])

    def test_chart_rejects_missing_schema_and_unreadable_labels(self):
        source = course([lesson(n) for n in range(37, 49)])
        mutations = [
            lambda p: p.update(chart=None),
            lambda p: p["chart"].pop("axis_min"),
            lambda p: p["chart"].update(extra="ignored"),
            lambda p: p["chart"].update(labels=["Before"]),
            lambda p: p["chart"].update(labels=["Before", "After", "Later"]),
            lambda p: p["chart"].update(labels=["Before", ""]),
            lambda p: p["chart"].update(labels=["Before", "之後"]),
            lambda p: p["chart"].update(title_en=" "),
            lambda p: p["chart"].update(unit_en="visits\n"),
            lambda p: p["chart"].update(values=[40]),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index):
                changed = copy.deepcopy(source)
                mutate(changed["episodes"][8]["practice"])
                with self.assertRaisesRegex(verify.VerificationError, "chart"):
                    verify_structure(changed, allow_season_subset=True)

    def test_chart_rejects_nonfinite_boolean_and_clipped_scales(self):
        source = course([lesson(n) for n in range(37, 49)])
        changes = [
            {"values": [0, 50]}, {"values": [-1, 50]}, {"values": [True, 50]},
            {"values": ["40", 50]}, {"values": [float("nan"), 50]},
            {"values": [40, float("inf")]}, {"values": [10**1000, 50]},
            {"axis_min": True}, {"axis_min": float("nan")}, {"axis_min": -1},
            {"axis_min": 40}, {"axis_min": 45}, {"axis_min": 60},
            {"axis_max": False}, {"axis_max": float("inf")}, {"axis_max": 49},
            {"axis_max": 35}, {"axis_max": 0},
        ]
        for changed_fields in changes:
            with self.subTest(changed_fields=changed_fields):
                changed = copy.deepcopy(source)
                changed["episodes"][8]["practice"]["chart"].update(changed_fields)
                with self.assertRaisesRegex(verify.VerificationError, "chart"):
                    verify_structure(changed, allow_season_subset=True)

    def test_player_brands_adult_stages_and_embeds_only_selected_season(self):
        episodes = [lesson(n) for n in range(37, 49)]
        episodes[0]["title_zh_TW"] = "</script><script>bad()</script>"
        path = player.write_player(course(episodes), self.output)
        page = path.read_text(encoding="utf-8")
        self.assertIn("UNIVERSITY · 12 LESSONS", page)
        self.assertIn("大學英文・四階段學習", page)
        self.assertIn("第 4 季・階段 4・成果表達與學術銜接", page)
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
        self.assertEqual([episode["id"] for episode in data], [f"ep{n}" for n in range(37, 49)])
        self.assertTrue(all(episode["course"] == "university" and episode["stage"] == 4 for episode in data))

    def test_workplace_player_and_practice_use_only_their_course_and_separate_answers(self):
        from adult_english.practice import write_html
        episodes = [lesson(n, "workplace") for n in range(1, 13)]
        page = player.write_player(course(episodes), self.output).read_text()
        self.assertIn("WORKPLACE · 12 LESSONS", page)
        self.assertIn("第 1 季・階段 1・求職與入職", page)
        self.assertNotIn("UNIVERSITY", page)
        self.assertNotIn("高三", page)
        practice = write_html(episodes, self.output).read_text()
        self.assertEqual(practice.count('<article class="worksheet"'), 12)
        self.assertEqual(practice.count('<article class="writing-sheet worksheet"'), 12)
        self.assertEqual(practice.count('<section class="answer"'), 12)
        self.assertLess(practice.rindex('<article '), practice.index('<section class="answer"'))
        self.assertIn("WORKPLACE · STAGE 1 · SEASON 1", practice)
        self.assertIn(episodes[0]["practice"]["sample_answer_en"], practice)

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
            self.assertFalse(build.valid_final({**episode, "course": "workplace"}, self.output, 15,
                                               renderer_profile=profile))
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
        self.assertEqual(len(partial["missing"]), 48)
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
    kind = "university"

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="adult-English-package-source-")
        self.addCleanup(temporary.cleanup)
        self.output = Path(temporary.name)
        self.source_path = self.output / "authoring.json"
        self.resolved_path = self.output / "lessons.resolved.json"
        self.config = get_course(self.kind)
        self.source = course(kind=self.kind)
        self.resolved = copy.deepcopy(self.source)
        for authored, measured in zip(self.source["episodes"], self.resolved["episodes"]):
            measured["source_sha256"] = audio.source_fingerprint(authored)
        audio.atomic_json(self.source_path, self.source)
        audio.atomic_json(self.resolved_path, self.resolved)
        self.existing_archive = self.output / self.config.all_archive_name
        self.existing_archive.write_bytes(b"previous checked archive")

    def test_changed_practice_or_demo_cannot_publish_old_media(self):
        for field in ("practice", "reading", "answer", "demo"):
            with self.subTest(field=field):
                changed = copy.deepcopy(self.source)
                if field == "practice":
                    changed["episodes"][12]["practice"]["sample_answer_en"] = changed["episodes"][12]["practice"]["sample_answer_en"].replace("I study", "We study")
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

    def test_same_episode_ids_from_other_course_cannot_enter_packaging(self):
        other = course(kind="workplace" if self.kind == "university" else "university")
        audio.atomic_json(self.resolved_path, other)
        with patch.object(package_series, "verify_output") as full_verify:
            with self.assertRaisesRegex(verify.VerificationError, "Wrong course"):
                package_series.preflight(self.source, other, self.output)
        full_verify.assert_not_called()
        self.assertEqual(self.existing_archive.read_bytes(), b"previous checked archive")

    def test_matching_source_hash_cannot_hide_changed_authored_fields(self):
        changed = copy.deepcopy(self.resolved)
        changed["episodes"][12]["practice"]["sample_answer_en"] = changed["episodes"][12]["practice"]["sample_answer_en"].replace("I study", "We study")
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
        self.assertEqual(len(report["packages"]), 5)
        self.assertEqual(report["source_sha256"], build.file_sha256(self.source_path))
        self.assertEqual(report["resolved_sha256"], build.file_sha256(self.resolved_path))
        self.assertEqual(report["packages"][-1]["episodes"], 48)
        self.assertEqual(report["packages"][-1]["files"], 821)
        self.assertEqual([item["file"] for item in report["packages"]],
                         [f"{self.config.archive_prefix}_Season_{season:02d}.zip" for season in range(1, 5)]
                         + [self.config.all_archive_name])
        self.assertTrue(all(item["files"] == 209 for item in report["packages"][:4]))
        self.assertEqual(report["renderer_profiles"], {"all_four_seasons": RENDERER.name})
        catalog = (self.output / self.config.catalog_name).read_bytes()
        self.assertTrue(catalog.startswith(b"\xef\xbb\xbf"))
        self.assertEqual(len(catalog.decode("utf-8-sig").splitlines()), 49)
        for stage in ("階段 1", "階段 2", "階段 3", "階段 4"):
            self.assertIn(stage, catalog.decode("utf-8-sig"))
        self.assertEqual(audio.read_json(self.output / "package-checks.json"), report)


class WorkplacePackageSourceTests(PackageSourceTests):
    kind = "workplace"


class BatchTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="adult-English-complete-batch-")
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

    def test_wrong_course_output_is_rejected_without_mutating_existing_status_or_logs(self):
        source_path = self.output / "university.json"
        audio.atomic_json(source_path, course())
        audio.atomic_json(self.output / "lessons.resolved.json", course(kind="workplace"))
        before = self.status_path.read_bytes()
        argv = ["batch.py", "--source", str(source_path), "--output", str(self.output)]
        with patch.object(sys, "argv", argv), patch.object(batch.subprocess, "Popen") as worker:
            with self.assertRaisesRegex(ValueError, "Wrong course"):
                batch.main()
        worker.assert_not_called()
        self.assertEqual(self.status_path.read_bytes(), before)
        self.assertFalse((self.output / "build-logs").exists())

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
