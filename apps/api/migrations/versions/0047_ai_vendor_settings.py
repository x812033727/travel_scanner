"""Move the AI vendor keys and Base URLs onto one ``ai_vendors`` provider row.

Revision ID: 0047_ai_vendor_settings
Revises: 0046_guide_backfill_attempts

Until this revision the admin page kept the OpenAI, Claude and MiniMax keys (and their
Base URLs) on the ``ai_planner`` row and the Gemini key on the ``gemini_guides`` row,
while AI guide search quietly borrowed the planner's keys. The provider definitions
now list those eight fields on a single ``ai_vendors`` provider, and
``apply_runtime_overrides`` reads a stored field back only while the row's own
definition still lists it — so without this move every key an operator ever saved
would silently stop applying on the first deploy of the new code.

The move decrypts each old row's secret blob with the same derivation the app uses
(``sha256(SETTINGS_ENCRYPTION_KEY or APP_SECRET_KEY)``), merges the moved fields into
``ai_vendors`` (values already saved there win), re-encrypts what is left on the old
rows and clears their last test result, which covered fields they no longer own. A
blob that cannot be decrypted aborts the transaction on purpose: the app raises the
same error for that row, and carrying on would drop the keys. A disabled
``ai_planner`` row used to null the three keys for every feature; after the move the
keys stay live on ``ai_vendors`` and ``ai_planner_enabled`` only stops the planner.

Idempotent: a second run finds nothing left to move. An install that only ever used
environment variables has no rows and is left alone; the Settings names are unchanged.
"""

import base64
import hashlib
import json
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Protocol
from uuid import uuid4

import sqlalchemy as sa
from alembic import op
from cryptography.fernet import Fernet, InvalidToken

from app.config import get_settings

revision: str = "0047_ai_vendor_settings"
down_revision: str | None = "0046_guide_backfill_attempts"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TARGET = "ai_vendors"
# provider -> (config fields, secret fields) that leave that row. Frozen here on
# purpose: a migration describes the shape at the time it was written, not whatever
# PROVIDER_DEFINITIONS says later.
MOVED: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "ai_planner": (
        ("openai_api_base_url", "anthropic_api_base_url", "minimax_api_base_url"),
        ("openai_api_key", "anthropic_api_key", "minimax_api_key"),
    ),
    "gemini_guides": (
        ("hotspot_guide_gemini_base_url",),
        ("hotspot_guide_gemini_api_key",),
    ),
}
# The enable flag a source row recreated on downgrade takes, so a downgrade never
# switches Gemini article search on by itself.
SOURCE_ENABLED_FLAG = {
    "ai_planner": "ai_planner_enabled",
    "gemini_guides": "hotspot_guide_gemini_enabled",
}

# ``config`` is PostgreSQL json (not jsonb): bind dicts through sa.JSON so SQLAlchemy
# serialises them the way the ORM does, and never touch the column with ``||``.
provider_configs = sa.table(
    "provider_configs",
    sa.column("id", sa.Uuid()),
    sa.column("provider", sa.String()),
    sa.column("enabled", sa.Boolean()),
    sa.column("priority", sa.Integer()),
    sa.column("config", sa.JSON()),
    sa.column("secret_config_encrypted", sa.Text()),
    sa.column("last_test_status", sa.String()),
    sa.column("last_test_message", sa.Text()),
    sa.column("created_at", sa.DateTime(timezone=True)),
    sa.column("updated_at", sa.DateTime(timezone=True)),
)


class KeyMaterial(Protocol):
    settings_encryption_key: str | None
    app_secret_key: str


@dataclass
class VendorRow:
    config: dict[str, Any] = field(default_factory=dict)
    secrets: dict[str, str] = field(default_factory=dict)


def split_vendor_fields(
    sources: dict[str, VendorRow], target: VendorRow | None
) -> tuple[VendorRow, dict[str, VendorRow]]:
    """Pure: the merged ``ai_vendors`` row and the stripped source rows.

    A value already stored on the target wins over the one being moved; fields that
    do not move stay on their source row untouched.
    """
    merged = VendorRow(dict(target.config), dict(target.secrets)) if target else VendorRow()
    stripped: dict[str, VendorRow] = {}
    for provider, row in sources.items():
        config_fields, secret_fields = MOVED[provider]
        remaining = VendorRow(dict(row.config), dict(row.secrets))
        for name in config_fields:
            if name in remaining.config:
                merged.config.setdefault(name, remaining.config.pop(name))
        for name in secret_fields:
            if name in remaining.secrets:
                merged.secrets.setdefault(name, remaining.secrets.pop(name))
        stripped[provider] = remaining
    return merged, stripped


def has_moved_fields(sources: dict[str, VendorRow]) -> bool:
    return any(
        any(name in row.config for name in MOVED[provider][0])
        or any(name in row.secrets for name in MOVED[provider][1])
        for provider, row in sources.items()
    )


def _fernet(settings: KeyMaterial | None = None) -> Fernet:
    material = settings or get_settings()
    raw = material.settings_encryption_key or material.app_secret_key
    return Fernet(base64.urlsafe_b64encode(hashlib.sha256(raw.encode()).digest()))


def _decrypt(provider: str, blob: str | None, fernet: Fernet) -> dict[str, str]:
    if not blob:
        return {}
    try:
        payload = json.loads(fernet.decrypt(blob.encode()))
    except (InvalidToken, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(
            f"provider_configs[{provider}].secret_config_encrypted cannot be decrypted with "
            "the current SETTINGS_ENCRYPTION_KEY/APP_SECRET_KEY; restore the key before "
            "migrating"
        ) from exc
    if not isinstance(payload, dict) or any(
        not isinstance(key, str) or not isinstance(value, str) for key, value in payload.items()
    ):
        raise RuntimeError(f"provider_configs[{provider}] holds secrets that are not a string map")
    return payload


def _encrypt(values: dict[str, str], fernet: Fernet) -> str | None:
    if not values:
        return None
    payload = json.dumps(values, ensure_ascii=False, sort_keys=True).encode()
    return fernet.encrypt(payload).decode()


def _load_rows(bind: sa.Connection) -> dict[str, Any]:
    statement = sa.select(provider_configs).where(provider_configs.c.provider.in_([*MOVED, TARGET]))
    return {row["provider"]: row for row in bind.execute(statement).mappings()}


def _vendor_row(row: Any, fernet: Fernet) -> VendorRow:
    return VendorRow(
        dict(row["config"] or {}),
        _decrypt(str(row["provider"]), row["secret_config_encrypted"], fernet),
    )


def upgrade() -> None:
    if op.get_context().as_sql:
        return  # a data move cannot be emitted as SQL
    bind = op.get_bind()
    if "provider_configs" not in set(sa.inspect(bind).get_table_names()):
        return
    rows = _load_rows(bind)
    fernet = _fernet()
    sources = {
        provider: _vendor_row(rows[provider], fernet) for provider in MOVED if provider in rows
    }
    if not has_moved_fields(sources):
        return
    target = _vendor_row(rows[TARGET], fernet) if TARGET in rows else None
    merged, stripped = split_vendor_fields(sources, target)
    now = datetime.now(UTC)
    if TARGET in rows:
        bind.execute(
            sa.update(provider_configs)
            .where(provider_configs.c.provider == TARGET)
            .values(
                config=merged.config,
                secret_config_encrypted=_encrypt(merged.secrets, fernet),
                enabled=True,
                updated_at=now,
            )
        )
    else:
        bind.execute(
            sa.insert(provider_configs).values(
                id=uuid4(),
                provider=TARGET,
                enabled=True,
                priority=100,
                config=merged.config,
                secret_config_encrypted=_encrypt(merged.secrets, fernet),
                created_at=now,
                updated_at=now,
            )
        )
    for provider, row in stripped.items():
        bind.execute(
            sa.update(provider_configs)
            .where(provider_configs.c.provider == provider)
            .values(
                config=row.config,
                secret_config_encrypted=_encrypt(row.secrets, fernet),
                last_test_status=None,
                last_test_message=None,
                updated_at=now,
            )
        )


def downgrade() -> None:
    if op.get_context().as_sql:
        return
    bind = op.get_bind()
    if "provider_configs" not in set(sa.inspect(bind).get_table_names()):
        return
    rows = _load_rows(bind)
    if TARGET not in rows:
        return
    fernet = _fernet()
    vendors = _vendor_row(rows[TARGET], fernet)
    settings = get_settings()
    now = datetime.now(UTC)
    for provider, (config_fields, secret_fields) in MOVED.items():
        config = {
            name: vendors.config.pop(name) for name in config_fields if name in vendors.config
        }
        secrets = {
            name: vendors.secrets.pop(name) for name in secret_fields if name in vendors.secrets
        }
        if not config and not secrets:
            continue
        if provider in rows:
            existing = _vendor_row(rows[provider], fernet)
            for name, value in config.items():
                existing.config.setdefault(name, value)
            for name, secret in secrets.items():
                existing.secrets.setdefault(name, secret)
            bind.execute(
                sa.update(provider_configs)
                .where(provider_configs.c.provider == provider)
                .values(
                    config=existing.config,
                    secret_config_encrypted=_encrypt(existing.secrets, fernet),
                    updated_at=now,
                )
            )
        else:
            bind.execute(
                sa.insert(provider_configs).values(
                    id=uuid4(),
                    provider=provider,
                    enabled=bool(getattr(settings, SOURCE_ENABLED_FLAG[provider])),
                    priority=100,
                    config=config,
                    secret_config_encrypted=_encrypt(secrets, fernet),
                    created_at=now,
                    updated_at=now,
                )
            )
    bind.execute(sa.delete(provider_configs).where(provider_configs.c.provider == TARGET))
