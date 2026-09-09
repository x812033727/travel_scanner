from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

from app.deployments.schemas import AgentOverview


def test_signed_e2e_agent_exposes_schema_valid_deployment_overview(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    release_sha = "c" * 40
    monkeypatch.setenv("E2E_DEPLOY_AGENT_FIXTURE", "1")
    monkeypatch.setenv("DEPLOY_AGENT_SOCKET", "/tmp/travel-scanner-contract.sock")
    monkeypatch.setenv("DEPLOY_AGENT_HMAC_KEY", "fixture-key-with-at-least-32-characters")
    monkeypatch.setenv("RELEASE_SHA", release_sha)
    fixture_path = Path(__file__).parent / "support" / "e2e_deploy_agent.py"
    spec = spec_from_file_location("e2e_deploy_agent_contract_fixture", fixture_path)
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    overview = AgentOverview.model_validate(module.deployment_overview_payload())

    assert overview.connected is True
    assert overview.deployed_sha == release_sha
    assert overview.target_sha == release_sha
    assert overview.ci_status == "success"
    assert overview.commits == []
    assert [(check.name, check.status) for check in overview.checks] == [
        ("signed_fixture", "ok")
    ]
