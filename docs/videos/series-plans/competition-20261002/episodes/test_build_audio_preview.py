"""Offline regression tests for the task-local audio preview assembler.

All WAV files here are synthetic, temporary fixtures, never production media.
Run with: python -m unittest discover -s <this directory> -p 'test_build_audio_preview.py'
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
import wave


SCRIPT_PATH = Path(__file__).with_name("build-audio-preview.py")
SPEC = importlib.util.spec_from_file_location("competition_audio_preview", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise ImportError(f"Cannot load {SCRIPT_PATH}")
PREVIEW = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = PREVIEW
SPEC.loader.exec_module(PREVIEW)

RATE = 48_000
SAMPLE_BYTES = 2
LOCKED_STATUS = "existing-measured-audio-edit-no-animation"


class BuildAudioPreviewTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="audio-preview-fixture-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.media = self.root / "media"
        self.media.mkdir()
        self.output = self.root / "output"
        self.sources: dict[str, tuple[Path, bytes]] = {}

    def write_json(self, name: str, value: object) -> Path:
        path = self.root / name
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
        return path

    def line(
        self,
        number: int,
        duration: float = 0.08,
        speaker: str = "zhitang",
        episode: int = 1,
    ) -> dict:
        line_id = f"WR-E{episode:02d}-L{number:03d}"
        runtime_id = f"{episode:02d}{number:06d}"
        frames = round(duration * RATE)
        # Different, nonzero PCM per line, including quiet edges that must survive.
        pattern = struct.pack("<hhhh", 1000 + number, -2000 - number, 3000 + number, 17)
        body_frames = max(0, frames - 16)
        pcm = b"\0\0" * min(8, frames)
        pcm += (pattern * ((body_frames + 3) // 4))[: body_frames * SAMPLE_BYTES]
        pcm += b"\0\0" * max(0, frames - len(pcm) // SAMPLE_BYTES)
        path = self.media / f"{runtime_id}.wav"
        with wave.open(str(path), "wb") as writer:
            writer.setnchannels(1)
            writer.setsampwidth(SAMPLE_BYTES)
            writer.setframerate(RATE)
            writer.writeframes(pcm)
        self.sources[line_id] = (path, pcm)
        return {
            "line_id": line_id,
            "runtime_id": runtime_id,
            "speaker_id": speaker,
            "text": f"測試第 {number} 句。",
        }

    @staticmethod
    def shot(
        number: int,
        lines: list[dict],
        start: float = 0,
        duration: float = 4,
        episode: int = 1,
        **extra: object,
    ) -> dict:
        return {
            "shot_id": f"WR-E{episode:02d}-S{number:02d}",
            "line_ids": [line.get("line_id", line.get("id")) for line in lines],
            "edit_window_s": {"start": start, "end": start + duration, "status": "planned"},
            **extra,
        }

    def run_preview(self, lines: list[dict], shots: list[dict], **kwargs: object) -> dict:
        dialogue = self.write_json("dialogue.json", {"episode": 1, "locale": "zh-TW", "lines": lines})
        edit = self.write_json("edit-plan.json", {"episode": 1, "locale": "zh-TW", "shots": shots})
        return PREVIEW.build_preview(dialogue, edit, self.media, self.output, **kwargs)

    def measured_shots(self) -> list[dict]:
        return json.loads((self.output / "measured-edit.json").read_text(encoding="utf-8"))["shots"]

    def read_pcm(self, path: Path) -> bytes:
        with wave.open(str(path), "rb") as reader:
            self.assertEqual(reader.getnchannels(), 1)
            self.assertEqual(reader.getsampwidth(), SAMPLE_BYTES)
            self.assertEqual(reader.getframerate(), RATE)
            return reader.readframes(reader.getnframes())

    def assert_no_output(self) -> None:
        self.assertFalse(self.output.exists() and any(self.output.rglob("*")))

    def assert_pcm_preserved(self, report: dict) -> None:
        frame_count = round(report["duration_s"] * RATE)
        expected_master = bytearray(frame_count * SAMPLE_BYTES)
        expected_stems: dict[str, bytearray] = {}
        for placement in report["measured_lines"]:
            line_id = placement["line_id"]
            source, pcm = self.sources[line_id]
            start_frame = round(placement["start_s"] * RATE)
            end_frame = round(placement["end_s"] * RATE)
            self.assertEqual(end_frame - start_frame, len(pcm) // SAMPLE_BYTES)
            self.assertAlmostEqual(placement["measured_voice_duration_s"], len(pcm) / SAMPLE_BYTES / RATE)
            self.assertEqual(placement["source_wav_sha256"], hashlib.sha256(source.read_bytes()).hexdigest())
            start = start_frame * SAMPLE_BYTES
            end = end_frame * SAMPLE_BYTES
            expected_master[start:end] = pcm
            speaker = placement["speaker_id"]
            stem = expected_stems.setdefault(speaker, bytearray(frame_count * SAMPLE_BYTES))
            stem[start:end] = pcm
            self.assertEqual(self.read_pcm(source), pcm, "Assembler modified a source WAV")
        self.assertEqual(self.read_pcm(self.output / "master.wav"), bytes(expected_master))
        for speaker, expected in expected_stems.items():
            with self.subTest(speaker=speaker):
                self.assertEqual(self.read_pcm(self.output / "stems" / f"{speaker}.wav"), bytes(expected))

    def test_duplicate_dialogue_line_is_rejected_before_output(self) -> None:
        line = self.line(1)
        with self.assertRaises(PREVIEW.PreviewError):
            self.run_preview([line, dict(line)], [self.shot(1, [line])])
        self.assert_no_output()

    def test_duplicate_line_assignment_is_rejected_before_output(self) -> None:
        line = self.line(1)
        with self.assertRaises(PREVIEW.PreviewError):
            self.run_preview([line], [self.shot(1, [line]), self.shot(2, [line], start=4)])
        self.assert_no_output()

    def test_duplicate_line_within_one_shot_is_rejected(self) -> None:
        line = self.line(1)
        with self.assertRaises(PREVIEW.PreviewError):
            self.run_preview([line], [self.shot(1, [line, line])])
        self.assert_no_output()

    def test_unassigned_line_is_rejected(self) -> None:
        first, missing = self.line(1), self.line(2)
        with self.assertRaises(PREVIEW.PreviewError):
            self.run_preview([first, missing], [self.shot(1, [first])])
        self.assert_no_output()

    def test_single_shot_above_eight_seconds_fails_without_partial_output(self) -> None:
        line = self.line(1, duration=7.51)
        with self.assertRaises(PREVIEW.PreviewError):
            self.run_preview([line], [self.shot(1, [line], duration=8)])
        self.assert_no_output()

    def test_silent_shot_keeps_planned_duration_after_voice_is_retimed(self) -> None:
        line = self.line(1, duration=0.125)
        report = self.run_preview(
            [line], [self.shot(1, [line]), self.shot(2, [], start=4, duration=3.375)]
        )
        voiced, silent = self.measured_shots()
        self.assertEqual(voiced["editorial_duration_s"], 2)
        self.assertEqual(silent["start_s"], 2)
        self.assertEqual(silent["editorial_duration_s"], 3.375)
        self.assertEqual(silent["end_s"], 5.375)
        self.assertEqual(silent["line_ids"], [])
        self.assertEqual(report["duration_s"], 5.375)
        self.assert_pcm_preserved(report)

    def test_short_silent_action_is_retained_without_padding(self) -> None:
        line = self.line(1)
        report = self.run_preview(
            [line], [self.shot(1, [line]), self.shot(2, [], start=4, duration=1.25)]
        )
        self.assertEqual(self.measured_shots()[1]["editorial_duration_s"], 1.25)
        self.assertEqual(report["duration_s"], 3.25)
        self.assert_pcm_preserved(report)

    def test_allowlisted_pairs_merge_at_eight_seconds_without_losing_lines(self) -> None:
        for first_number, second_number in ((34, 35), (38, 39)):
            with self.subTest(pair=(first_number, second_number)):
                self.output = self.root / f"merged-{first_number}"
                first = self.line(1, duration=3.5)
                second = self.line(2, duration=3.75, speaker="chengchuan")
                target = f"WR-E01-S{first_number:02d}"
                candidate = f"WR-E01-S{second_number:02d}"
                shots = [
                    self.shot(first_number, [first], continuity_group="wedding"),
                    self.shot(second_number, [second], start=4, continuity_group="wedding", candidate_merge_into=target),
                ]
                report = self.run_preview([first, second], shots)
                measured = self.measured_shots()
                self.assertEqual(len(measured), 1)
                self.assertEqual(measured[0]["merged_shot_ids"], [target, candidate])
                self.assertEqual(measured[0]["line_ids"], [first["line_id"], second["line_id"]])
                self.assertEqual(report["duration_s"], 8)
                self.assertEqual([item["line_id"] for item in report["measured_lines"]], measured[0]["line_ids"])
                self.assertAlmostEqual(report["measured_lines"][1]["start_s"], 3.95)
                self.assert_pcm_preserved(report)

    def test_merge_over_eight_seconds_preserves_two_shots_and_both_lines(self) -> None:
        first = self.line(1, duration=3.5)
        second = self.line(2, duration=3.76, speaker="chengchuan")
        shots = [
            self.shot(34, [first], continuity_group="wedding"),
            self.shot(35, [second], start=4, continuity_group="wedding", candidate_merge_into="WR-E01-S34"),
        ]
        report = self.run_preview([first, second], shots)
        measured = self.measured_shots()
        self.assertEqual([shot["shot_id"] for shot in measured], ["WR-E01-S34", "WR-E01-S35"])
        self.assertEqual([item["line_id"] for item in report["measured_lines"]], [first["line_id"], second["line_id"]])
        self.assertAlmostEqual(report["voice_total_s"], 7.26)
        self.assert_pcm_preserved(report)

    def test_allowlisted_pair_with_different_continuity_groups_is_not_merged(self) -> None:
        first, second = self.line(1), self.line(2)
        shots = [
            self.shot(34, [first], continuity_group="wedding"),
            self.shot(35, [second], start=4, continuity_group="warehouse", candidate_merge_into="WR-E01-S34"),
        ]
        report = self.run_preview([first, second], shots)
        self.assertEqual(len(self.measured_shots()), 2)
        self.assertEqual(len(report["measured_lines"]), 2)

    def test_nonadjacent_allowlisted_pair_is_not_merged(self) -> None:
        first, second = self.line(1), self.line(2)
        shots = [
            self.shot(34, [first], continuity_group="wedding"),
            self.shot(36, [], start=4, duration=2, continuity_group="wedding"),
            self.shot(35, [second], start=6, continuity_group="wedding", candidate_merge_into="WR-E01-S34"),
        ]
        report = self.run_preview([first, second], shots)
        self.assertEqual(len(self.measured_shots()), 3)
        self.assertEqual(len(report["measured_lines"]), 2)

    def test_unapproved_pair_is_not_merged_even_when_same_scene_and_short(self) -> None:
        first, second = self.line(1), self.line(2)
        shots = [
            self.shot(32, [first], continuity_group="wedding"),
            self.shot(33, [second], start=4, continuity_group="wedding", candidate_merge_into="WR-E01-S32"),
        ]
        report = self.run_preview([first, second], shots)
        self.assertEqual([shot["shot_id"] for shot in self.measured_shots()], ["WR-E01-S32", "WR-E01-S33"])
        self.assertEqual(len(report["measured_lines"]), 2)
        self.assert_pcm_preserved(report)

    def test_e2_document_normalizes_ids_and_uses_optional_runtime_map(self) -> None:
        for use_id_map in (False, True):
            with self.subTest(use_id_map=use_id_map):
                self.output = self.root / f"e2-{use_id_map}"
                line = self.line(1, episode=2)
                original_id = line.pop("line_id")
                line["id"] = original_id
                runtime_id = line["runtime_id"]
                mapping = None
                if use_id_map:
                    del line["runtime_id"]
                    mapping = self.write_json("id-map.json", {"lines": [{"original_id": original_id, "runtime_id": runtime_id}]})
                dialogue = self.write_json("e2-dialogue.json", {
                    "episode": 2,
                    "locale": "zh-TW",
                    "lines": [line],
                    "shots": [{
                        "id": "WR-E02-S01",
                        "line_ids": [original_id],
                        "planned_start_s": 0,
                        "planned_end_s": 4,
                        "planned_used_seconds": 4,
                    }],
                })
                report = PREVIEW.build_preview(dialogue, None, self.media, self.output, id_map_path=mapping)
                self.assertEqual(report["measured_lines"][0]["line_id"], original_id)
                self.assertEqual(report["measured_lines"][0]["runtime_id"], runtime_id)
                self.assertEqual(self.measured_shots()[0]["shot_id"], "WR-E02-S01")
                self.assert_pcm_preserved(report)

    def test_merge_preserves_target_picture_and_original_documents_with_source_hashes(self) -> None:
        first, second = self.line(1), self.line(2, speaker="chengchuan")
        target_data = {
            "prompt": "Fixture: Zhitang stands beside the wedding table.",
            "motion": "She sets down one pen.",
            "camera": "Locked medium shot.",
            "characters": ["zhitang"],
            "character_looks": {"zhitang": "zhitang-bride-veiled"},
            "fit": "trim",
            "transition": "cut",
            "visual": "clip",
            "extra_editorial_metadata": {"prop": "intact original", "hands": 2},
        }
        reply_data = {
            "prompt": "Fixture: Chengchuan stands at the opposite side.",
            "motion": "He turns his head once.",
            "camera": "Locked close-up.",
            "characters": ["chengchuan"],
            "character_looks": {"chengchuan": "chengchuan--base"},
        }
        shots = [
            self.shot(34, [first], scene_id="fixture-target-scene", data=target_data, continuity_group="wedding"),
            self.shot(35, [second], start=4, scene_id="fixture-reply-scene", data=reply_data,
                      continuity_group="wedding", candidate_merge_into="WR-E01-S34"),
        ]
        screenplay = self.root / "fixture-screenplay.md"
        screenplay.write_text("Synthetic test screenplay only.\n", encoding="utf-8")
        story_sha = hashlib.sha256(b"synthetic story source only").hexdigest()
        screenplay_sha = hashlib.sha256(screenplay.read_bytes()).hexdigest()
        dialogue_document = {
            "episode": 1,
            "locale": "zh-TW",
            "lines": [first, second],
            "source_binding": {"source_object_sha256": story_sha, "screenplay_sha256": screenplay_sha},
        }
        plan_document = {
            "episode": 1,
            "shots": shots,
            "source_binding": {"source_object_sha256": story_sha, "screenplay_path": str(screenplay)},
            "editorial_note": "Preserve both source actions for later picture review.",
        }
        dialogue = self.write_json("picture-dialogue.json", dialogue_document)
        plan = self.write_json("picture-plan.json", plan_document)
        report = PREVIEW.build_preview(dialogue, plan, self.media, self.output)
        measured = json.loads((self.output / "measured-edit.json").read_text(encoding="utf-8"))
        self.assertEqual(len(measured["shots"]), 1)
        merged = measured["shots"][0]
        self.assertEqual(merged["scene_id"], "fixture-target-scene")
        self.assertEqual(merged["data"], target_data, "A merge must retain the target's one action and visible cast")
        self.assertNotIn(reply_data["motion"], json.dumps(merged["data"]))
        self.assertEqual(merged["source_ids"], ["WR-E01-S34", "WR-E01-S35"])
        self.assertEqual(merged["merged_shot_ids"], merged["source_ids"])
        self.assertIn("off-screen dialogue", merged["picture_policy"])
        self.assertIn("do not combine both source actions", merged["picture_policy"])
        original = json.loads((self.output / "original-shot-plan.json").read_text(encoding="utf-8"))
        self.assertEqual(original["dialogue"], dialogue_document)
        self.assertEqual(original["edit_plan"], plan_document)
        for artifact in (report, measured, original):
            binding = artifact["source_binding"]
            self.assertEqual(binding["source_object_sha256"], story_sha)
            self.assertEqual(binding["screenplay_sha256"], screenplay_sha)
            self.assertEqual(binding["screenplay_path"], str(screenplay.resolve()))
            self.assertEqual(binding["dialogue"]["sha256"], hashlib.sha256(dialogue.read_bytes()).hexdigest())
            self.assertEqual(binding["edit_plan"]["sha256"], hashlib.sha256(plan.read_bytes()).hexdigest())
        self.assert_pcm_preserved(report)

    def test_e2_top_level_picture_fields_normalize_without_losing_character_looks(self) -> None:
        line = self.line(1, episode=2)
        line["id"] = line.pop("line_id")
        picture = {
            "prompt": "Fixture: two adults beside the wedding table.",
            "motion": "Zhitang places the document flat.",
            "camera": "Locked oblique close-up.",
            "character_looks": {"zhitang": "zhitang-bride-no-veil", "chengchuan": "chengchuan--base"},
            "fit": "trim",
            "transition": "cut",
            "visual": "clip",
        }
        document = {
            "episode": 2,
            "locale": "zh-TW",
            "lines": [line],
            "shots": [{
                "id": "WR-E02-S01",
                "line_ids": [line["id"]],
                "planned_start_s": 0,
                "planned_end_s": 4,
                "planned_used_seconds": 4,
                **picture,
            }],
        }
        dialogue = self.write_json("e2-picture-dialogue.json", document)
        report = PREVIEW.build_preview(dialogue, None, self.media, self.output)
        shot = self.measured_shots()[0]
        self.assertEqual(shot["scene_id"], "wr-e02-s01")
        self.assertEqual(shot["data"], {**picture, "characters": ["zhitang", "chengchuan"]})
        self.assertEqual(shot["source_ids"], ["WR-E02-S01"])
        self.assertEqual(shot["merged_shot_ids"], ["WR-E02-S01"])
        original = json.loads((self.output / "original-shot-plan.json").read_text(encoding="utf-8"))
        self.assertEqual(original["dialogue"], document)
        self.assertEqual(original["edit_plan"], document)
        self.assert_pcm_preserved(report)

    def test_master_and_speaker_stems_keep_complete_pcm_without_trim_or_stretch(self) -> None:
        first = self.line(1, duration=0.08)
        second = self.line(2, duration=0.125, speaker="chengchuan")
        original_files = {key: path.read_bytes() for key, (path, _) in self.sources.items()}
        report = self.run_preview([first, second], [self.shot(1, [first, second])])
        self.assertEqual(report["duration_s"], 2)
        self.assertEqual(report["actual_animated_video_seconds"], 0)
        self.assertAlmostEqual(report["voice_total_s"], 0.205)
        placements = report["measured_lines"]
        self.assertAlmostEqual(placements[0]["start_s"], 0.2)
        self.assertAlmostEqual(placements[0]["end_s"], 0.28)
        self.assertAlmostEqual(placements[1]["start_s"], 0.53)
        self.assertAlmostEqual(placements[1]["end_s"], 0.655)
        self.assert_pcm_preserved(report)
        for key, (path, _) in self.sources.items():
            self.assertEqual(path.read_bytes(), original_files[key])
        srt = (self.output / "zh-TW.srt").read_text(encoding="utf-8")
        vtt = (self.output / "zh-TW.vtt").read_text(encoding="utf-8")
        self.assertIn("00:00:00,200 --> 00:00:00,280", srt)
        self.assertIn("00:00:00.530 --> 00:00:00.655", vtt)
        for line in (first, second):
            self.assertEqual(srt.count(line["text"]), 1)
            self.assertEqual(vtt.count(line["text"]), 1)

    def locked_opening(self) -> tuple[list[dict], list[dict]]:
        boundaries = [0, 5, 9, 13.5, 16, 19, 21, 24, 28, 31.5, 34.5, 37, 40, 43.5, 48.5, 51]
        silent_shots = {6, 7, 11, 12, 15}
        lines, shots = [], []
        for number, (start, end) in enumerate(zip(boundaries, boundaries[1:]), start=1):
            shot_lines = []
            placements = []
            if number not in silent_shots:
                for offset in range(2 if number == 14 else 1):
                    line = self.line(len(lines) + 1)
                    digest = hashlib.sha256(self.sources[line["line_id"]][0].read_bytes()).hexdigest()
                    line["measurement"] = {"audio_duration_s": 0.08, "source_wav_sha256": digest}
                    lines.append(line)
                    shot_lines.append(line)
                    voice_start = start + (0.1 if number in (4, 8, 14) else 0.2) + offset * 0.33
                    placements.append({
                        **line,
                        "start_s": voice_start,
                        "end_s": voice_start + 0.08,
                        "measured_voice_duration_s": 0.08,
                        "source_wav_sha256": digest,
                        "time_stretch": False,
                        "trim_applied": False,
                    })
            shot = self.shot(
                number, shot_lines, start=start, duration=end - start, voice_placements=placements,
                scene_id=f"locked-fixture-scene-{number:02d}",
                data={"prompt": f"Locked fixture {number}.", "motion": "One fixture action.",
                      "characters": ["zhitang"], "character_looks": {"zhitang": "fixture-locked-look"}},
            )
            shot["edit_window_s"]["status"] = LOCKED_STATUS
            shots.append(shot)
        return lines, shots

    def test_locked_opening_remains_51_seconds_and_continuation_starts_at_51(self) -> None:
        lines, shots = self.locked_opening()
        continuation = self.line(12, duration=0.12)
        lines.append(continuation)
        shots.append(self.shot(16, [continuation], start=51, duration=4))
        report = self.run_preview(lines, shots)
        measured = self.measured_shots()
        for original, actual in zip(shots[:15], measured[:15]):
            self.assertEqual(actual["start_s"], original["edit_window_s"]["start"])
            self.assertEqual(actual["end_s"], original["edit_window_s"]["end"])
            self.assertEqual(actual["scene_id"], original["scene_id"])
            self.assertEqual(actual["data"], original["data"])
            self.assertEqual([p["start_s"] for p in actual["voice_placements"]], [p["start_s"] for p in original["voice_placements"]])
        self.assertEqual(measured[14]["end_s"], 51)
        self.assertEqual(measured[15]["start_s"], 51)
        self.assertEqual(report["duration_s"], 53)
        self.assert_pcm_preserved(report)

    def test_locked_opening_rejects_source_hash_mismatch_without_output(self) -> None:
        lines, shots = self.locked_opening()
        shots[0]["voice_placements"][0]["source_wav_sha256"] = "0" * 64
        with self.assertRaises(PREVIEW.PreviewError):
            self.run_preview(lines, shots)
        self.assert_no_output()

    def test_wrong_rate_width_or_channels_is_rejected_without_output(self) -> None:
        for rate, width, channels in ((24_000, 2, 1), (48_000, 1, 1), (48_000, 2, 2)):
            with self.subTest(rate=rate, width=width, channels=channels):
                line = self.line(1)
                source, _ = self.sources[line["line_id"]]
                with wave.open(str(source), "wb") as writer:
                    writer.setnchannels(channels)
                    writer.setsampwidth(width)
                    writer.setframerate(rate)
                    writer.writeframes(b"\x10" * (960 * width * channels))
                with self.assertRaises(PREVIEW.PreviewError):
                    self.run_preview([line], [self.shot(1, [line])])
                self.assert_no_output()


if __name__ == "__main__":
    unittest.main()
