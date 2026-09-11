"""Index collection references by (kind, target) so a saved count can be read directly."""

import sqlalchemy as sa
from alembic import context, op

revision = "0071_collection_item_lookup"
down_revision = "0070_map_identity_metadata"
branch_labels = None
depends_on = None

INDEX = "ix_community_collection_item_reference"
TABLE = "community_collection_items"


def upgrade() -> None:
    # 0001 creates current metadata, so a fresh installation already carries the index.
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    if inspector is not None:
        if not inspector.has_table(TABLE):
            return
        if INDEX in {row["name"] for row in inspector.get_indexes(TABLE)}:
            return
    op.create_index(INDEX, TABLE, ["kind", "target"])


def downgrade() -> None:
    inspector = None if context.is_offline_mode() else sa.inspect(op.get_bind())
    if inspector is not None and (
        not inspector.has_table(TABLE)
        or INDEX not in {row["name"] for row in inspector.get_indexes(TABLE)}
    ):
        return
    op.drop_index(INDEX, table_name=TABLE)
