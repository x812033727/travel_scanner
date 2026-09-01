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
