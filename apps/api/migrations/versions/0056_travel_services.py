"""Reviewed travel services and anonymous affiliate click dimensions.

Frozen PostgreSQL DDL; existence guards support 0001 metadata-based fresh installs.
Downgrade preserves nullable click actors rather than deleting anonymous history.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0056_travel_services"
down_revision: str | None = "0055_analytics_event_names"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLES = {
    "travel_service_brands": """CREATE TABLE travel_service_brands (
	id UUID NOT NULL, 
	project_id VARCHAR(32) NOT NULL, 
	code VARCHAR(64) NOT NULL, 
	approval VARCHAR(16) NOT NULL, 
	enabled BOOLEAN NOT NULL, 
	version INTEGER NOT NULL, 
	evidence_url VARCHAR(2048), 
	verified_at TIMESTAMP WITH TIME ZONE, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_service_brand_project UNIQUE (project_id, code), 
	CONSTRAINT ck_brand_approval CHECK (approval IN ('unknown','pending','approved','rejected'))
);
CREATE INDEX ix_travel_service_brands_project_id ON travel_service_brands (project_id);""",
    "travel_service_config": """CREATE TABLE travel_service_config (
	id INTEGER NOT NULL, 
	data JSON NOT NULL, 
	version INTEGER NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id)
)
""",
    "travel_service_products": """CREATE TABLE travel_service_products (
	id UUID NOT NULL, 
	source_key VARCHAR(255) NOT NULL, 
	kind VARCHAR(16) NOT NULL, 
	destination_id VARCHAR(64) NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	names_json JSON NOT NULL, 
	facts JSON NOT NULL, 
	source_url VARCHAR(2048) NOT NULL, 
	status VARCHAR(16) NOT NULL, 
	version INTEGER NOT NULL, 
	verified_at TIMESTAMP WITH TIME ZONE, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT ck_service_kind CHECK (kind IN ('hotel','transfer','tour','esim')), 
	CONSTRAINT ck_service_status CHECK (status IN ('pending','approved','disabled')), 
	UNIQUE (source_key)
);
CREATE INDEX ix_travel_service_products_kind ON travel_service_products (kind);
CREATE INDEX ix_travel_service_products_destination_id ON travel_service_products (destination_id);
CREATE INDEX ix_travel_service_products_status ON travel_service_products (status);""",
    "travel_service_favorites": """CREATE TABLE travel_service_favorites (
	id UUID NOT NULL, 
	user_id UUID NOT NULL, 
	product_id UUID NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_service_favorite UNIQUE (user_id, product_id), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE, 
	FOREIGN KEY(product_id) REFERENCES travel_service_products (id) ON DELETE CASCADE
);
CREATE INDEX ix_travel_service_favorites_product_id ON travel_service_favorites (product_id);
CREATE INDEX ix_travel_service_favorites_user_id ON travel_service_favorites (user_id);""",
    "travel_service_imports": """CREATE TABLE travel_service_imports (
	id UUID NOT NULL, 
	actor_id UUID, 
	source VARCHAR(32) NOT NULL, 
	status VARCHAR(16) NOT NULL, 
	rows_json JSON NOT NULL, 
	result_json JSON NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(actor_id) REFERENCES users (id)
)
""",
    "travel_service_offers": """CREATE TABLE travel_service_offers (
	id UUID NOT NULL, 
	product_id UUID NOT NULL, 
	brand_id UUID NOT NULL, 
	target_url VARCHAR(2048) NOT NULL, 
	static_url VARCHAR(2048), 
	verification_context VARCHAR(64),
	scope VARCHAR(16) NOT NULL, 
	status VARCHAR(16) NOT NULL, 
	version INTEGER NOT NULL, 
	verified_at TIMESTAMP WITH TIME ZONE, 
	expires_at TIMESTAMP WITH TIME ZONE, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_service_offer_target UNIQUE (brand_id, target_url), 
	CONSTRAINT ck_service_offer_status CHECK (status IN ('pending','approved','disabled')), 
	CONSTRAINT ck_service_offer_scope CHECK (scope IN ('product','destination')), 
	FOREIGN KEY(product_id) REFERENCES travel_service_products (id) ON DELETE CASCADE, 
	FOREIGN KEY(brand_id) REFERENCES travel_service_brands (id) ON DELETE CASCADE
);
CREATE INDEX ix_travel_service_offers_brand_id ON travel_service_offers (brand_id);
CREATE INDEX ix_travel_service_offers_product_id ON travel_service_offers (product_id);
CREATE INDEX ix_travel_service_offers_status ON travel_service_offers (status);""",
    "trip_service_selections": """CREATE TABLE trip_service_selections (
	id UUID NOT NULL, 
	trip_id UUID NOT NULL, 
	product_id UUID NOT NULL, 
	item_id UUID, 
	idempotency_key VARCHAR(128) NOT NULL, 
	request_hash VARCHAR(64) NOT NULL, 
	status VARCHAR(16) NOT NULL, 
	details JSON NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_trip_service_operation UNIQUE (trip_id, idempotency_key), 
	CONSTRAINT uq_trip_service_product UNIQUE (trip_id, product_id), 
	CONSTRAINT ck_selection_status CHECK (status IN ('planned','booked','cancelled')), 
	FOREIGN KEY(trip_id) REFERENCES trip_plans (id) ON DELETE CASCADE, 
	FOREIGN KEY(product_id) REFERENCES travel_service_products (id), 
	FOREIGN KEY(item_id) REFERENCES trip_plan_items (id) ON DELETE SET NULL
);
CREATE INDEX ix_trip_service_selections_trip_id ON trip_service_selections (trip_id);
CREATE INDEX ix_trip_service_selections_product_id ON trip_service_selections (product_id);""",
}


def upgrade() -> None:
    existing = (
        set() if op.get_context().as_sql else set(sa.inspect(op.get_bind()).get_table_names())
    )
    for name, ddl in TABLES.items():
        if name not in existing:
            for statement in ddl.split(";"):
                if statement.strip():
                    op.execute(sa.text(statement))
    columns = (
        set()
        if op.get_context().as_sql
        else {c["name"] for c in sa.inspect(op.get_bind()).get_columns("affiliate_clicks")}
    )
    for name, length in (
        ("brand", 64),
        ("service_type", 16),
        ("placement", 24),
        ("destination_id", 64),
    ):
        if name not in columns:
            op.add_column("affiliate_clicks", sa.Column(name, sa.String(length), nullable=True))
    indexes = (
        set()
        if op.get_context().as_sql
        else {i["name"] for i in sa.inspect(op.get_bind()).get_indexes("affiliate_clicks")}
    )
    if "ix_affiliate_clicks_brand" not in indexes:
        op.create_index("ix_affiliate_clicks_brand", "affiliate_clicks", ["brand"])
    op.alter_column("affiliate_clicks", "user_id", nullable=True)


def downgrade() -> None:
    existing = set(sa.inspect(op.get_bind()).get_table_names())
    for name in reversed(TABLES):
        if name in existing:
            op.drop_table(name)
    columns = {c["name"] for c in sa.inspect(op.get_bind()).get_columns("affiliate_clicks")}
    for name in ("brand", "service_type", "placement", "destination_id"):
        if name in columns:
            op.drop_column("affiliate_clicks", name)
