import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

ACTIVE = (
    "queued",
    "preflight",
    "building",
    "backing_up",
    "migrating",
    "activating",
    "verifying",
    "rolling_back",
)

ACTIVE_DATABASE = ("queued", "running")


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


class AgentStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        return connection

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        connection = self._connect()
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self._connection() as db:
            db.executescript(
                """
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS nonces (
                    nonce TEXT PRIMARY KEY,
                    created_at INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    stage TEXT NOT NULL,
                    previous_sha TEXT,
                    target_sha TEXT NOT NULL,
                    target_commit_subject TEXT,
                    ci_url TEXT,
                    backup_name TEXT,
                    rollback_status TEXT,
                    failure_code TEXT,
                    failure_detail TEXT,
                    started_at TEXT,
                    finished_at TEXT,
                    created_at TEXT NOT NULL
                );
                CREATE UNIQUE INDEX IF NOT EXISTS uq_agent_active_job
                    ON jobs ((1))
                    WHERE status IN ('queued','preflight','building','backing_up','migrating',
                                     'activating','verifying','rolling_back');
                CREATE TABLE IF NOT EXISTS events (
                    job_id TEXT NOT NULL,
                    sequence INTEGER NOT NULL,
                    stage TEXT NOT NULL,
                    status TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (job_id, sequence),
                    FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE
                );
                CREATE TABLE IF NOT EXISTS database_jobs (
                    job_id TEXT PRIMARY KEY,
                    action TEXT NOT NULL CHECK(action IN ('backup','analyze')),
                    status TEXT NOT NULL CHECK(status IN ('queued','running','succeeded','failed')),
                    backup_name TEXT,
                    checksum_sha256 TEXT,
                    size_bytes INTEGER,
                    schema_revision TEXT,
                    release_sha TEXT,
                    failure_code TEXT,
                    failure_detail TEXT,
                    started_at TEXT,
                    finished_at TEXT,
                    created_at TEXT NOT NULL
                );
                CREATE UNIQUE INDEX IF NOT EXISTS uq_agent_active_database_job
                    ON database_jobs ((1))
                    WHERE status IN ('queued','running');
                CREATE TABLE IF NOT EXISTS database_events (
                    job_id TEXT NOT NULL,
                    sequence INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (job_id, sequence),
                    FOREIGN KEY (job_id) REFERENCES database_jobs(job_id) ON DELETE CASCADE
                );
                CREATE TABLE IF NOT EXISTS verified_backups (
                    backup_name TEXT PRIMARY KEY,
                    checksum_sha256 TEXT NOT NULL,
                    size_bytes INTEGER NOT NULL CHECK(size_bytes > 0),
                    schema_revision TEXT NOT NULL,
                    release_sha TEXT NOT NULL,
                    source TEXT NOT NULL CHECK(source IN ('deployment','manual')),
                    source_job_id TEXT,
                    verified_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS ix_verified_backups_verified_at
                    ON verified_backups (verified_at DESC);
                """
            )

    def consume_nonce(self, nonce: str, instant: int) -> bool:
        try:
            with self._connection() as db:
                db.execute("DELETE FROM nonces WHERE created_at < ?", (instant - 120,))
                db.execute("INSERT INTO nonces(nonce, created_at) VALUES (?, ?)", (nonce, instant))
            return True
        except sqlite3.IntegrityError:
            return False

    def create_job(self, job_id: str, target_sha: str) -> dict[str, Any]:
        existing = self.get_job(job_id)
        if existing:
            return existing
        with self._connection() as db:
            # BEGIN IMMEDIATE serializes admission across deployment and database jobs.
            # The file lock remains the final host-level guard during execution.
            db.execute("BEGIN IMMEDIATE")
            if db.execute(
                "SELECT 1 FROM database_jobs WHERE status IN ('queued','running') LIMIT 1"
            ).fetchone():
                raise sqlite3.IntegrityError("a database operation is active")
            db.execute(
                "INSERT INTO jobs(job_id,status,stage,target_sha,created_at) VALUES(?,?,?,?,?)",
                (job_id, "queued", "queued", target_sha, now_iso()),
            )
        self.event(job_id, "queued", "queued", "部署工作已排入佇列")
        job = self.get_job(job_id)
        if job is None:
            raise RuntimeError("job creation failed")
        return job

    def update(self, job_id: str, **values: Any) -> None:
        allowed = {
            "status",
            "stage",
            "previous_sha",
            "target_commit_subject",
            "ci_url",
            "backup_name",
            "rollback_status",
            "failure_code",
            "failure_detail",
            "started_at",
            "finished_at",
        }
        selected = {key: value for key, value in values.items() if key in allowed}
        if not selected:
            return
        assignments = ",".join(f"{key}=?" for key in selected)
        with self._connection() as db:
            db.execute(
                f"UPDATE jobs SET {assignments} WHERE job_id=?",  # noqa: S608
                (*selected.values(), job_id),
            )

    def claim_job(self, job_id: str) -> bool:
        with self._connection() as db:
            result = db.execute(
                "UPDATE jobs SET status='preflight', stage='preflight' "
                "WHERE job_id=? AND status='queued'",
                (job_id,),
            )
        return result.rowcount == 1

    def event(self, job_id: str, stage: str, status: str, message: str) -> None:
        with self._connection() as db:
            sequence = int(
                db.execute(
                    "SELECT COALESCE(MAX(sequence),0)+1 FROM events WHERE job_id=?", (job_id,)
                ).fetchone()[0]
            )
            db.execute(
                "INSERT INTO events VALUES(?,?,?,?,?,?)",
                (job_id, sequence, stage, status, message, now_iso()),
            )

    def active_job(self) -> dict[str, Any] | None:
        placeholders = ",".join("?" for _ in ACTIVE)
        with self._connection() as db:
            row = db.execute(
                f"SELECT * FROM jobs WHERE status IN ({placeholders}) ORDER BY created_at DESC LIMIT 1",  # noqa: S608
                ACTIVE,
            ).fetchone()
        return self._with_events(row) if row else None

    def get_job(self, job_id: str) -> dict[str, Any] | None:
        with self._connection() as db:
            row = db.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone()
        return self._with_events(row) if row else None

    def _with_events(self, row: sqlite3.Row) -> dict[str, Any]:
        result = dict(row)
        with self._connection() as db:
            events = [
                dict(item)
                for item in db.execute(
                    "SELECT sequence,stage,status,message,created_at FROM events "
                    "WHERE job_id=? ORDER BY sequence",
                    (result["job_id"],),
                ).fetchall()
            ]
        result["events"] = events
        return cast(dict[str, Any], json.loads(json.dumps(result)))

    def create_database_job(self, job_id: str, action: str) -> dict[str, Any]:
        existing = self.get_database_job(job_id)
        if existing:
            if existing["action"] != action:
                raise sqlite3.IntegrityError("job id was already used for another action")
            return existing
        if action not in {"backup", "analyze"}:
            raise ValueError("unsupported database operation")
        with self._connection() as db:
            db.execute("BEGIN IMMEDIATE")
            placeholders = ",".join("?" for _ in ACTIVE)
            if db.execute(
                f"SELECT 1 FROM jobs WHERE status IN ({placeholders}) LIMIT 1",  # noqa: S608
                ACTIVE,
            ).fetchone():
                raise sqlite3.IntegrityError("a deployment is active")
            db.execute(
                "INSERT INTO database_jobs(job_id,action,status,created_at) VALUES(?,?,?,?)",
                (job_id, action, "queued", now_iso()),
            )
        self.database_event(job_id, "queued", "資料庫工作已排入佇列")
        job = self.get_database_job(job_id)
        if job is None:
            raise RuntimeError("database job creation failed")
        return job

    def claim_database_job(self, job_id: str) -> bool:
        with self._connection() as db:
            result = db.execute(
                "UPDATE database_jobs SET status='running', started_at=? "
                "WHERE job_id=? AND status='queued'",
                (now_iso(), job_id),
            )
        return result.rowcount == 1

    def update_database_job(self, job_id: str, **values: Any) -> None:
        allowed = {
            "status",
            "backup_name",
            "checksum_sha256",
            "size_bytes",
            "schema_revision",
            "release_sha",
            "failure_code",
            "failure_detail",
            "started_at",
            "finished_at",
        }
        selected = {key: value for key, value in values.items() if key in allowed}
        if not selected:
            return
        assignments = ",".join(f"{key}=?" for key in selected)
        with self._connection() as db:
            db.execute(
                f"UPDATE database_jobs SET {assignments} WHERE job_id=?",  # noqa: S608
                (*selected.values(), job_id),
            )

    def database_event(self, job_id: str, status: str, message: str) -> None:
        with self._connection() as db:
            sequence = int(
                db.execute(
                    "SELECT COALESCE(MAX(sequence),0)+1 FROM database_events WHERE job_id=?",
                    (job_id,),
                ).fetchone()[0]
            )
            db.execute(
                "INSERT INTO database_events VALUES(?,?,?,?,?)",
                (job_id, sequence, status, message, now_iso()),
            )

    def active_database_job(self) -> dict[str, Any] | None:
        placeholders = ",".join("?" for _ in ACTIVE_DATABASE)
        with self._connection() as db:
            row = db.execute(
                f"SELECT * FROM database_jobs WHERE status IN ({placeholders}) "  # noqa: S608
                "ORDER BY created_at DESC LIMIT 1",
                ACTIVE_DATABASE,
            ).fetchone()
        return self._database_with_events(row) if row else None

    def get_database_job(self, job_id: str) -> dict[str, Any] | None:
        with self._connection() as db:
            row = db.execute("SELECT * FROM database_jobs WHERE job_id=?", (job_id,)).fetchone()
        return self._database_with_events(row) if row else None

    def _database_with_events(self, row: sqlite3.Row) -> dict[str, Any]:
        result = dict(row)
        with self._connection() as db:
            events = [
                dict(item)
                for item in db.execute(
                    "SELECT sequence,status,message,created_at FROM database_events "
                    "WHERE job_id=? ORDER BY sequence",
                    (result["job_id"],),
                ).fetchall()
            ]
        result["events"] = events
        return cast(dict[str, Any], json.loads(json.dumps(result)))

    def record_verified_backup(
        self,
        *,
        backup_name: str,
        checksum_sha256: str,
        size_bytes: int,
        schema_revision: str,
        release_sha: str,
        source: str,
        source_job_id: str | None,
        verified_at: str,
    ) -> None:
        """Persist only backups that already passed pg_restore verification."""
        if source not in {"deployment", "manual"}:
            raise ValueError("unsupported backup source")
        if size_bytes <= 0:
            raise ValueError("verified backup size must be positive")
        with self._connection() as db:
            db.execute(
                """
                INSERT INTO verified_backups(
                    backup_name, checksum_sha256, size_bytes, schema_revision,
                    release_sha, source, source_job_id, verified_at
                ) VALUES(?,?,?,?,?,?,?,?)
                ON CONFLICT(backup_name) DO UPDATE SET
                    checksum_sha256=excluded.checksum_sha256,
                    size_bytes=excluded.size_bytes,
                    schema_revision=excluded.schema_revision,
                    release_sha=excluded.release_sha,
                    source=excluded.source,
                    source_job_id=COALESCE(excluded.source_job_id, verified_backups.source_job_id),
                    verified_at=excluded.verified_at
                """,
                (
                    backup_name,
                    checksum_sha256,
                    size_bytes,
                    schema_revision,
                    release_sha,
                    source,
                    source_job_id,
                    verified_at,
                ),
            )

    def attach_verified_backup_to_job(self, backup_name: str, job_id: str) -> None:
        with self._connection() as db:
            db.execute(
                "UPDATE verified_backups SET source_job_id=? "
                "WHERE backup_name=? AND source='deployment'",
                (job_id, backup_name),
            )

    def list_verified_backups(self, limit: int = 50) -> list[dict[str, Any]]:
        bounded_limit = max(1, min(limit, 100))
        with self._connection() as db:
            rows = db.execute(
                "SELECT backup_name, checksum_sha256, size_bytes, schema_revision, "
                "release_sha, source, source_job_id, verified_at "
                "FROM verified_backups ORDER BY verified_at DESC LIMIT ?",
                (bounded_limit,),
            ).fetchall()
        return [cast(dict[str, Any], dict(row)) for row in rows]

    def prune_verified_backups(self, retained_names: set[str]) -> None:
        """Remove catalog entries whose owned dump was rotated or deleted."""
        with self._connection() as db:
            if not retained_names:
                db.execute("DELETE FROM verified_backups")
                return
            placeholders = ",".join("?" for _ in retained_names)
            db.execute(
                f"DELETE FROM verified_backups WHERE backup_name NOT IN ({placeholders})",  # noqa: S608
                tuple(sorted(retained_names)),
            )
