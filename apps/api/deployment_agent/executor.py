import json
import os
import re
import shutil
import subprocess
import time
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from deployment_agent.config import AgentConfig
from deployment_agent.security import sanitize
from deployment_agent.store import AgentStore, now_iso

SHA = re.compile(r"^[0-9a-f]{40}$")


class CommandError(RuntimeError):
    pass


class CommandRunner:
    def run(
        self,
        args: Sequence[str],
        *,
        cwd: Path | None = None,
        env: Mapping[str, str] | None = None,
        timeout: int = 900,
        output_path: Path | None = None,
    ) -> str:
        stdout: Any = subprocess.PIPE
        handle = None
        if output_path is not None:
            handle = output_path.open("wb")
            stdout = handle
        try:
            completed = subprocess.run(
                list(args),
                cwd=cwd,
                env=dict(env) if env else None,
                stdin=subprocess.DEVNULL,
                stdout=stdout,
                stderr=subprocess.PIPE,
                timeout=timeout,
                check=False,
                shell=False,
            )
        finally:
            if handle:
                handle.close()
        if completed.returncode:
            stderr = completed.stderr.decode(errors="replace") if completed.stderr else ""
            raise CommandError(sanitize(stderr) or f"command exited with {completed.returncode}")
        return completed.stdout.decode(errors="replace").strip() if completed.stdout else ""


class DeploymentExecutor:
    def __init__(
        self,
        config: AgentConfig,
        store: AgentStore,
        runner: CommandRunner | None = None,
    ) -> None:
        self.config = config
        self.store = store
        self.runner = runner or CommandRunner()

    def _git(self, *args: str) -> str:
        return self.runner.run(["git", "--git-dir", str(self.config.mirror_path), *args])

    def _ensure_mirror(self) -> None:
        if not self.config.mirror_path.exists():
            self.config.mirror_path.parent.mkdir(parents=True, exist_ok=True)
            self.runner.run(
                ["git", "clone", "--mirror", self.config.repo_url, str(self.config.mirror_path)]
            )
        remote = self._git("remote", "get-url", "origin")
        if remote != self.config.repo_url:
            raise CommandError("repository origin does not match the pinned repository")
        self._git(
            "fetch",
            "--prune",
            "origin",
            f"+refs/heads/{self.config.branch}:refs/heads/{self.config.branch}",
        )

    def _target(self) -> tuple[str, str]:
        self._ensure_mirror()
        sha = self._git("rev-parse", f"refs/heads/{self.config.branch}").lower()
        if not SHA.fullmatch(sha):
            raise CommandError("remote main did not resolve to a commit SHA")
        subject = sanitize(self._git("show", "-s", "--format=%s", sha), 255)
        return sha, subject

    def _current_sha(self) -> str | None:
        try:
            target = self.config.current_path.resolve(strict=True)
        except (FileNotFoundError, RuntimeError):
            return None
        return target.name if SHA.fullmatch(target.name) else None

    def _ci(self, sha: str) -> tuple[str, str | None]:
        url = (
            f"https://api.github.com/repos/{self.config.github_repo}/actions/runs"
            f"?head_sha={sha}&branch={self.config.branch}&event=push&per_page=30"
        )
        request = Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.config.github_token}",
                "User-Agent": "travel-scanner-deployer/1",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        try:
            with urlopen(request, timeout=10) as response:
                payload = json.load(response)
        except (HTTPError, URLError, TimeoutError, ValueError) as exc:
            raise CommandError("GitHub CI status could not be verified") from exc
        for run in payload.get("workflow_runs", []):
            if run.get("name") == self.config.workflow_name:
                status = (
                    str(run.get("conclusion"))
                    if run.get("status") == "completed"
                    else str(run.get("status") or "unknown")
                )
                return status, str(run.get("html_url") or "") or None
        return "missing", None

    def _health(self, url: str) -> bool:
        try:
            with urlopen(url, timeout=5) as response:
                return 200 <= cast(int, response.status) < 300
        except (HTTPError, URLError, TimeoutError):
            return False

    def overview(self) -> dict[str, Any]:
        current = self._current_sha()
        active = self.store.active_job()
        if active:
            target = str(active["target_sha"])
            subject = str(active.get("target_commit_subject") or "Deployment in progress")
            ci_status = "success"
            ci_url = active.get("ci_url")
        else:
            target, subject = self._target()
            ci_status, ci_url = self._ci(target)
        commits: list[dict[str, str]] = []
        if not active and current and current != target:
            output = self._git("log", "--format=%H%x09%s", "--max-count=20", f"{current}..{target}")
            for line in output.splitlines():
                sha, _, title = line.partition("\t")
                if SHA.fullmatch(sha):
                    commits.append({"sha": sha, "subject": sanitize(title, 255)})
        checks = [
            {
                "name": "api",
                "status": "ok" if self._health(self.config.api_health_url) else "warning",
                "detail": "API ready"
                if self._health(self.config.api_health_url)
                else "API currently unavailable",
            },
            {
                "name": "web",
                "status": "ok" if self._health(self.config.web_health_url) else "warning",
                "detail": "Web ready"
                if self._health(self.config.web_health_url)
                else "Web currently unavailable",
            },
        ]
        return {
            "connected": True,
            "deployed_sha": current,
            "target_sha": target,
            "target_commit_subject": subject,
            "ci_status": ci_status,
            "ci_url": ci_url,
            "commits": commits,
            "checks": checks,
        }

    def preflight(self) -> dict[str, Any]:
        checks: list[dict[str, str]] = []
        for name, command in (
            ("git", ["git", "--version"]),
            ("docker", ["docker", "info"]),
            ("compose", ["docker", "compose", "version"]),
        ):
            try:
                self.runner.run(command, timeout=30)
                checks.append({"name": name, "status": "ok", "detail": "可用"})
            except CommandError:
                checks.append({"name": name, "status": "failed", "detail": "無法使用"})
        free = shutil.disk_usage(self.config.releases_path.parent).free
        checks.append(
            {
                "name": "disk",
                "status": "ok" if free >= self.config.min_free_bytes else "failed",
                "detail": f"可用空間 {free // (1024**3)} GiB",
            }
        )
        try:
            self._runtime_environment()
            checks.append({"name": "runtime_env", "status": "ok", "detail": "Runtime env 已就緒"})
        except CommandError as exc:
            checks.append({"name": "runtime_env", "status": "failed", "detail": sanitize(str(exc))})
        postgres_container = f"{self.config.project_name}-postgres-1"
        for name, command in (
            (
                "database",
                [
                    "docker",
                    "exec",
                    postgres_container,
                    "pg_isready",
                    "-U",
                    "travel",
                    "-d",
                    "travel_scanner",
                ],
            ),
            (
                "pg_dump",
                ["docker", "exec", postgres_container, "pg_dump", "--version"],
            ),
        ):
            try:
                self.runner.run(command, timeout=30)
                checks.append({"name": name, "status": "ok", "detail": "可用"})
            except CommandError:
                checks.append({"name": name, "status": "failed", "detail": "無法使用"})
        target: str | None = None
        try:
            target, _ = self._target()
            ci_status, _ = self._ci(target)
            checks.append(
                {
                    "name": "github_ci",
                    "status": "ok" if ci_status == "success" else "failed",
                    "detail": f"CI: {ci_status}",
                }
            )
        except CommandError as exc:
            checks.append({"name": "github_ci", "status": "failed", "detail": sanitize(str(exc))})
        checks.extend(self.overview().get("checks", []) if target else [])
        return {
            "ok": all(item["status"] != "failed" for item in checks),
            "checked_at": now_iso(),
            "checks": checks,
            "target_sha": target,
        }

    def bootstrap_current(self) -> str:
        if self._current_sha():
            raise CommandError("current release is already initialized")
        target, _ = self._target()
        ci_status, _ = self._ci(target)
        if ci_status != "success":
            raise CommandError("latest main has not passed the required CI workflow")
        self._point_current(self._release(target))
        return target

    def _compose(self, release: Path, sha: str, *args: str, timeout: int = 900) -> str:
        environment = self._runtime_environment()
        environment.update(
            {
                "RELEASE_SHA": sha,
                "RUNTIME_ENV_FILE": str(self.config.runtime_env_path),
                "DEPLOY_AGENT_SOCKET_DIR": str(self.config.socket_path.parent),
                "COMPOSE_PROJECT_NAME": self.config.project_name,
            }
        )
        return self.runner.run(
            ["docker", "compose", "-f", "docker-compose.prod.yml", *args],
            cwd=release,
            env=environment,
            timeout=timeout,
        )

    def _runtime_environment(self) -> dict[str, str]:
        if not self.config.runtime_env_path.is_file():
            raise CommandError("runtime environment file is missing")
        inherited_names = (
            "PATH",
            "HOME",
            "USER",
            "LANG",
            "LC_ALL",
            "DOCKER_HOST",
            "DOCKER_CONFIG",
            "XDG_RUNTIME_DIR",
            "SYSTEMROOT",
        )
        environment = {
            name: os.environ[name] for name in inherited_names if name in os.environ
        }
        for raw_line in self.config.runtime_env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            name, value = line.split("=", 1)
            name = name.strip()
            if not re.fullmatch(r"[A-Z][A-Z0-9_]*", name):
                raise CommandError("runtime environment contains an invalid variable name")
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
                value = value[1:-1]
            environment[name] = value
        return environment

    def _stage(self, job_id: str, stage: str, message: str) -> None:
        self.store.update(job_id, status=stage, stage=stage)
        self.store.event(job_id, stage, "running", message)

    def _release(self, sha: str) -> Path:
        release = self.config.releases_path / sha
        self.config.releases_path.mkdir(parents=True, exist_ok=True)
        if not release.exists():
            self._git("worktree", "add", "--detach", str(release), sha)
        actual = self.runner.run(["git", "rev-parse", "HEAD"], cwd=release).lower()
        if actual != sha:
            raise CommandError("release directory does not match the target SHA")
        return release

    def _backup(self, release: Path, sha: str) -> str:
        self.config.backup_path.mkdir(parents=True, exist_ok=True)
        name = f"travel-scanner-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}-{sha[:7]}.dump"
        path = self.config.backup_path / name
        environment = self._runtime_environment()
        environment.update(
            {
                "RUNTIME_ENV_FILE": str(self.config.runtime_env_path),
                "COMPOSE_PROJECT_NAME": self.config.project_name,
            }
        )
        self.runner.run(
            [
                "docker",
                "compose",
                "-f",
                "docker-compose.prod.yml",
                "exec",
                "-T",
                "postgres",
                "sh",
                "-c",
                'exec pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc',
            ],
            cwd=release,
            env=environment,
            timeout=600,
            output_path=path,
        )
        if not path.is_file() or path.stat().st_size == 0:
            raise CommandError("database backup is empty")
        self._rotate_backups()
        return name

    def _rotate_backups(self) -> None:
        backups = sorted(
            self.config.backup_path.glob("travel-scanner-*.dump"),
            key=lambda item: item.stat().st_mtime,
            reverse=True,
        )
        for backup in backups[self.config.backup_retention :]:
            if backup.resolve().parent == self.config.backup_path.resolve():
                backup.unlink()

    def _verify_three_times(self) -> bool:
        consecutive = 0
        for _ in range(12):
            if self._health(self.config.api_health_url) and self._health(
                self.config.web_health_url
            ):
                consecutive += 1
                if consecutive == 3:
                    return True
            else:
                consecutive = 0
            time.sleep(2)
        return False

    def _point_current(self, release: Path) -> None:
        temporary = self.config.current_path.with_name("current.next")
        if temporary.exists() or temporary.is_symlink():
            temporary.unlink()
        temporary.symlink_to(release, target_is_directory=True)
        temporary.replace(self.config.current_path)

    def _cleanup(self) -> None:
        releases = sorted(
            (
                item
                for item in self.config.releases_path.iterdir()
                if item.is_dir() and SHA.fullmatch(item.name)
            ),
            key=lambda item: item.stat().st_mtime,
            reverse=True,
        )
        current = self._current_sha()
        keep: set[str] = {current} if current else set()
        for release in releases:
            if len(keep) >= self.config.release_retention:
                break
            keep.add(release.name)
        for release in releases:
            if (
                release.name not in keep
                and release.resolve().parent == self.config.releases_path.resolve()
            ):
                self._git("worktree", "remove", "--force", str(release))
                for image in (
                    f"travel-scanner-api:{release.name}",
                    f"travel-scanner-web:{release.name}",
                ):
                    try:
                        self.runner.run(["docker", "image", "rm", image], timeout=60)
                    except CommandError:
                        pass
        self._rotate_backups()

    def deploy(self, job_id: str, expected_sha: str) -> None:
        lock_descriptor = os.open(self.config.lock_path, os.O_CREAT | os.O_RDWR, 0o660)
        try:
            import fcntl

            fcntl.flock(  # type: ignore[attr-defined]
                lock_descriptor,
                fcntl.LOCK_EX | fcntl.LOCK_NB,  # type: ignore[attr-defined]
            )
        except (ImportError, BlockingIOError):
            os.close(lock_descriptor)
            self.store.update(
                job_id,
                status="failed",
                failure_code="deployment_lock_busy",
                failure_detail="another host deployment holds the lock",
                finished_at=now_iso(),
            )
            self.store.event(job_id, "queued", "failed", "另一個主機部署仍持有鎖定")
            return
        try:
            self._deploy_locked(job_id, expected_sha)
        finally:
            fcntl.flock(  # type: ignore[attr-defined]
                lock_descriptor, fcntl.LOCK_UN  # type: ignore[attr-defined]
            )
            os.close(lock_descriptor)

    def _deploy_locked(self, job_id: str, expected_sha: str) -> None:
        previous = self._current_sha()
        activated = False
        release: Path | None = None
        failure_code = "deployment_preflight_failed"
        self.store.update(job_id, started_at=now_iso(), previous_sha=previous)
        try:
            self._stage(job_id, "preflight", "正在重新驗證 main 與 CI")
            target, subject = self._target()
            ci_status, ci_url = self._ci(target)
            if target != expected_sha:
                failure_code = "deployment_target_changed"
                raise CommandError("deployment target changed")
            if ci_status != "success":
                failure_code = "deployment_ci_not_green"
                raise CommandError("required CI workflow is not successful")
            if target == previous:
                self._stage(job_id, "verifying", "代理重啟後正在重新確認已切換版本")
                if not self._verify_three_times():
                    self.store.update(
                        job_id,
                        status="manual_intervention_required",
                        stage="verifying",
                        failure_code="deployment_health_failed",
                        failure_detail="代理重啟後，current 版本未通過健康檢查",
                        finished_at=now_iso(),
                    )
                    self.store.event(
                        job_id,
                        "verifying",
                        "failed",
                        "代理重啟後 current 版本不健康，需要主機管理員處理",
                    )
                    return
                self.store.update(
                    job_id,
                    status="succeeded",
                    stage="succeeded",
                    target_commit_subject=subject,
                    ci_url=ci_url,
                    finished_at=now_iso(),
                )
                self.store.event(
                    job_id,
                    "succeeded",
                    "succeeded",
                    "代理重啟後已確認部署版本健康",
                )
                return
            self.store.update(job_id, target_commit_subject=subject, ci_url=ci_url)
            release = self._release(target)
            failure_code = "deployment_build_failed"
            self._stage(job_id, "building", "正在驗證 Compose 並建置版本映像")
            self._compose(release, target, "config", "--quiet", timeout=120)
            self._compose(release, target, "build", "api", "web", timeout=1800)
            failure_code = "deployment_backup_failed"
            self._stage(job_id, "backing_up", "正在建立 PostgreSQL 備份")
            backup_name = self._backup(release, target)
            self.store.update(job_id, backup_name=backup_name)
            failure_code = "deployment_migration_failed"
            self._stage(job_id, "migrating", "正在套用向前相容資料庫 migration")
            self._compose(release, target, "run", "--rm", "migrate", timeout=600)
            failure_code = "deployment_activation_failed"
            self._stage(job_id, "activating", "正在啟動新版本服務")
            activated = True
            self._compose(
                release,
                target,
                "up",
                "-d",
                "--remove-orphans",
                "postgres",
                "redis",
                "api",
                "worker",
                "alert-worker",
                "alert-scheduler",
                "web",
                timeout=900,
            )
            failure_code = "deployment_health_failed"
            self._stage(job_id, "verifying", "正在連續驗證 API 與 Web 健康狀態")
            if not self._verify_three_times():
                raise CommandError("new application did not pass health checks")
            self._point_current(release)
            self.store.update(job_id, status="succeeded", stage="succeeded", finished_at=now_iso())
            self.store.event(job_id, "succeeded", "succeeded", "部署完成並已切換 current release")
        except Exception as exc:
            detail = sanitize(str(exc)) or "deployment failed"
            if activated and previous:
                self.store.update(job_id, status="rolling_back", stage="rolling_back")
                self.store.event(
                    job_id, "rolling_back", "running", "健康檢查失敗，正在回退上一版應用"
                )
                try:
                    previous_release = self.config.releases_path / previous
                    self._compose(
                        previous_release, previous, "up", "-d", "--remove-orphans", timeout=900
                    )
                    if not self._verify_three_times():
                        raise CommandError("previous application did not recover")
                    self.store.update(
                        job_id,
                        status="rolled_back",
                        stage="rolled_back",
                        rollback_status="succeeded",
                        failure_code=failure_code,
                        failure_detail=detail,
                        finished_at=now_iso(),
                    )
                    self.store.event(
                        job_id,
                        "rolled_back",
                        "rolled_back",
                        "新版本未通過健康檢查，已回退上一版應用",
                    )
                    return
                except Exception:
                    self.store.update(
                        job_id,
                        status="manual_intervention_required",
                        stage="rolling_back",
                        rollback_status="failed",
                        failure_code="deployment_rollback_failed",
                        failure_detail=detail,
                        finished_at=now_iso(),
                    )
                    self.store.event(
                        job_id, "rolling_back", "failed", "應用回退失敗，需要主機管理員處理"
                    )
                    return
            self.store.update(
                job_id,
                status="failed",
                failure_code=failure_code,
                failure_detail=detail,
                finished_at=now_iso(),
            )
            failed_job = self.store.get_job(job_id)
            self.store.event(
                job_id,
                str(failed_job["stage"]) if failed_job else "failed",
                "failed",
                detail,
            )
        finally:
            try:
                self._cleanup()
            except Exception:
                pass
