import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AgentConfig:
    hmac_key: str
    github_token: str
    socket_path: Path = Path("/run/travel-scanner-deployer/deployer.sock")
    state_path: Path = Path("/var/lib/travel-scanner-deployer/state.sqlite3")
    lock_path: Path = Path("/run/travel-scanner-deployer/deploy.lock")
    mirror_path: Path = Path("/srv/travel-scanner/repository.git")
    releases_path: Path = Path("/srv/travel-scanner/releases")
    current_path: Path = Path("/srv/travel-scanner/current")
    backup_path: Path = Path("/var/backups/travel-scanner")
    runtime_env_path: Path = Path("/etc/travel-scanner/runtime.env")
    repo_url: str = "https://github.com/x812033727/travel_scanner.git"
    github_repo: str = "x812033727/travel_scanner"
    branch: str = "main"
    workflow_name: str = "CI"
    project_name: str = "travel-scanner"
    api_health_url: str = "http://127.0.0.1:8090/ready"
    web_health_url: str = "http://127.0.0.1:8091/"
    min_free_bytes: int = 5 * 1024 * 1024 * 1024
    release_retention: int = 5
    backup_retention: int = 7

    @classmethod
    def from_env(cls) -> "AgentConfig":
        key = os.environ.get("DEPLOY_AGENT_HMAC_KEY", "")
        token = os.environ.get("DEPLOY_AGENT_GITHUB_TOKEN", "")
        if len(key) < 32:
            raise RuntimeError("DEPLOY_AGENT_HMAC_KEY must contain at least 32 characters")
        if not token:
            raise RuntimeError("DEPLOY_AGENT_GITHUB_TOKEN is required")
        return cls(
            hmac_key=key,
            github_token=token,
            socket_path=Path(
                os.environ.get("DEPLOY_AGENT_SOCKET", "/run/travel-scanner-deployer/deployer.sock")
            ),
            state_path=Path(
                os.environ.get(
                    "DEPLOY_AGENT_STATE", "/var/lib/travel-scanner-deployer/state.sqlite3"
                )
            ),
        )
