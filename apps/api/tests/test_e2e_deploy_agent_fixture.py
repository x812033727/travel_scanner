from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import Mock

import pytest

from app.deployments.schemas import AgentOverview


def _load_fixture() -> ModuleType:
    fixture_path = Path(__file__).parent / "support" / "e2e_deploy_agent.py"
    spec = spec_from_file_location("e2e_deploy_agent_contract_fixture", fixture_path)
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_signed_e2e_agent_exposes_schema_valid_deployment_overview(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    release_sha = "c" * 40
    monkeypatch.setenv("E2E_DEPLOY_AGENT_FIXTURE", "1")
    monkeypatch.setenv("DEPLOY_AGENT_SOCKET", "/tmp/travel-scanner-contract.sock")
    monkeypatch.setenv("DEPLOY_AGENT_HMAC_KEY", "fixture-key-with-at-least-32-characters")
    monkeypatch.setenv("RELEASE_SHA", release_sha)
    module = _load_fixture()

    overview = AgentOverview.model_validate(module.deployment_overview_payload())

    assert overview.connected is True
    assert overview.deployed_sha == release_sha
    assert overview.target_sha == release_sha
    assert overview.ci_status == "success"
    assert overview.commits == []
    assert [(check.name, check.status) for check in overview.checks] == [("signed_fixture", "ok")]


def test_signed_e2e_agent_refuses_windows_before_validation_or_socket_changes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    module = _load_fixture()
    socket_path = tmp_path / "preserved.sock"
    socket_path.write_text("existing socket sentinel", encoding="utf-8")
    validate = Mock(side_effect=AssertionError("Windows must refuse before validation"))
    monkeypatch.setattr(module, "sys", SimpleNamespace(platform="win32"), raising=False)
    monkeypatch.setattr(module, "SOCKET_PATH", socket_path)
    monkeypatch.setattr(module, "_validate_environment", validate)

    with pytest.raises(SystemExit, match=r"(?i)Unix sockets.*Windows"):
        module.main()

    validate.assert_not_called()
    assert socket_path.read_text(encoding="utf-8") == "existing socket sentinel"


def test_signed_e2e_agent_linux_still_requires_fixture_flag_before_socket_changes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    module = _load_fixture()
    socket_path = tmp_path / "preserved.sock"
    socket_path.write_text("existing socket sentinel", encoding="utf-8")
    monkeypatch.setattr(module, "sys", SimpleNamespace(platform="linux"), raising=False)
    monkeypatch.setattr(module, "SOCKET_PATH", socket_path)
    monkeypatch.delenv("E2E_DEPLOY_AGENT_FIXTURE", raising=False)

    with pytest.raises(SystemExit, match="E2E_DEPLOY_AGENT_FIXTURE=1 is required"):
        module.main()

    assert socket_path.read_text(encoding="utf-8") == "existing socket sentinel"
