"""The operator CLI cannot confuse offline preparation with an authenticated apply."""

import json
from pathlib import Path

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.video_automation import planning_cli
from app.video_automation.planning import bundle_hash

PACK = Path(__file__).resolve().parents[3] / "docs/videos/series-plans/borrowed-dawn"


def no_database(*args: object, **kwargs: object) -> None:
    raise AssertionError("offline preparation must not enter database mode")


def test_prepare_preserves_the_real_work_without_entering_database_mode(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(planning_cli, "run_import", no_database)
    output = tmp_path / "plan.json"
    planning_cli.main(["--pack", str(PACK), "--prepare", str(output)])
    bundle = json.loads(output.read_text())
    report = json.loads(capsys.readouterr().out)
    assert report == {
        "prepared": True,
        "sha256": bundle_hash(bundle),
        "ready_for_production": False,
    }
    plan = json.loads(bundle["files"]["plan.json"])
    assert plan["category"] == "anime"
    assert plan["runtime"]["story_minutes"] == 22
    assert plan["planned_episodes"] == 120
    assert plan["lead"] == "ensemble"


def test_stdout_prepare_keeps_the_bundle_and_receipt_on_separate_streams(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(planning_cli, "run_import", no_database)
    planning_cli.main(["--pack", str(PACK), "--prepare", "-"])
    captured = capsys.readouterr()
    bundle = json.loads(captured.out)
    assert json.loads(captured.err)["sha256"] == bundle_hash(bundle)


def test_wrong_apply_hash_is_refused_before_a_database_call(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(planning_cli, "run_import", no_database)
    with pytest.raises(SystemExit) as error:
        planning_cli.main(["--pack", str(PACK), "--apply", "--expected-sha256", "0" * 64])
    assert error.value.code == 1
    assert "exact --expected-sha256" in capsys.readouterr().err


def test_prepare_cannot_also_apply(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as error:
        planning_cli.main(["--pack", str(PACK), "--prepare", "-", "--apply"])
    assert error.value.code == 2
    assert "cannot be combined" in capsys.readouterr().err


def test_input_limit_and_object_shape_are_checked_before_validation(tmp_path: Path) -> None:
    source = tmp_path / "input.json"
    source.write_bytes(b" " * (planning_cli.MAX_INPUT_BYTES + 1))
    with pytest.raises(ValueError, match="8 MiB"):
        planning_cli.read_bundle(source)
    source.write_text("[]")
    with pytest.raises(ValueError, match="bundle object"):
        planning_cli.read_bundle(source)


def test_database_errors_do_not_print_connection_or_statement_secrets(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    async def broken_import(*args: object, **kwargs: object) -> dict[str, object]:
        raise SQLAlchemyError("do-not-print-connection-credentials")

    monkeypatch.setattr(planning_cli, "run_import", broken_import)
    with pytest.raises(SystemExit) as error:
        planning_cli.main(["--pack", str(PACK)])
    assert error.value.code == 1
    stderr = capsys.readouterr().err
    assert "verify database access" in stderr
    assert "do-not-print-connection-credentials" not in stderr
