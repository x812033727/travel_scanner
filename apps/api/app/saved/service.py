"""One private saved-reference view; existing typed favorites remain authoritative.

Helpers never commit. Callers own the transaction, including collection changes.
Only public projections are returned; retained private references may be unavailable.
"""

from __future__ import annotations

import base64
import hashlib
import json
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

from sqlalchemy import (
    String,
    and_,
    case,
    cast,
    delete,
    exists,
    func,
    literal,
    or_,
    select,
    union_all,
)
from sqlalchemy import tuple_ as sql_tuple
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.community.models import Collection, CollectionItem, Post, PostRevision, Reaction
from app.discovery.policy import catalog_destination_ids, destination_id
from app.i18n import ERROR_DETAILS, Locale
from app.models import (
    FoodDestination,
    FoodFavorite,
    FoodMerchant,
    FoodMerchantFavorite,
    HotspotFavorite,
    HotspotGuide,
    RestaurantFavorite,
    RestaurantPlace,
    TravelHotspot,
    TravelServiceFavorite,
    TravelServiceProduct,
    User,
)
from app.problems import AppError

ALIASES = {"hotel": "service", "article": "guide", "video": "guide", "itinerary": "post"}
UUID_KINDS = {"hotspot", "food", "merchant", "service", "guide", "post", "pet_place"}
MAX_INBOX_ITEMS = 10_000
FAVORITES: dict[str, tuple[Any, Any]] = {
    "hotspot": (HotspotFavorite, HotspotFavorite.hotspot_id),
    "food": (FoodFavorite, FoodFavorite.food_id),
    "merchant": (FoodMerchantFavorite, FoodMerchantFavorite.merchant_id),
    "service": (TravelServiceFavorite, TravelServiceFavorite.product_id),
    "restaurant": (RestaurantFavorite, RestaurantFavorite.restaurant_place_id),
}


async def rate(session: AsyncSession, user: User) -> None:
    # The same policy surface is used by both existing collection adapters and the new API.
    from app.community.collections import rate as collection_rate

    await collection_rate(session, user)


def failure(code: str = "saved_item_not_found", status: int = 404) -> AppError:
    return AppError(status, code, ERROR_DETAILS["zh-TW"].get(code, code))


def fresh_product(product: TravelServiceProduct) -> bool:
    verified = product.verified_at
    if verified is None:
        return False
    verified = verified.replace(tzinfo=UTC) if verified.tzinfo is None else verified
    now = datetime.now(UTC)
    return now - timedelta(days=30) <= verified <= now


def canonical(kind: str, target: str, *, strict: bool = False) -> tuple[str, str]:
    kind = ALIASES.get(kind, kind)
    if not kind or len(kind) > 20 or not kind.replace("_", "").isalnum():
        raise failure("validation_error", 422)
    if not target or len(target) > 255 or any(ord(char) < 32 for char in target):
        raise failure("validation_error", 422)
    if kind in UUID_KINDS:
        try:
            target = UUID(target).hex
        except ValueError as exc:
            if strict:
                raise failure() from exc
            target = target.replace("-", "").lower()
    return kind, target


def public_id(kind: str, target: str) -> str:
    if kind in UUID_KINDS:
        try:
            return str(UUID(target))
        except ValueError:
            pass
    return target


def key_for(kind: str, target: str) -> str:
    kind, target = canonical(kind, target)
    return f"{kind}:{public_id(kind, target)}"


def parse_key(value: str) -> tuple[str, str]:
    if ":" not in value:
        raise failure("validation_error", 422)
    return canonical(*value.split(":", 1))


def uuid_text(column: Any) -> Any:
    return func.lower(func.replace(cast(column, String), "-", ""))


def collection_columns() -> tuple[Any, Any]:
    kind = case(
        *[(CollectionItem.kind == alias, name) for alias, name in ALIASES.items()],
        else_=CollectionItem.kind,
    )
    target = case(
        (kind.in_(sorted(UUID_KINDS)), uuid_text(CollectionItem.target)),
        else_=CollectionItem.target,
    )
    return kind, target


def references(user_id: UUID) -> Any:
    queries = []
    for kind, (model, column) in FAVORITES.items():
        target = RestaurantPlace.google_place_id if kind == "restaurant" else uuid_text(column)
        query = select(
            literal(kind).label("kind"),
            target.label("target"),
            model.created_at.label("saved_at"),
            literal("").label("collection_id"),
        )
        if kind == "restaurant":
            query = query.join(RestaurantPlace, RestaurantPlace.id == column)
        queries.append(query.where(model.user_id == user_id))
    kind, target = collection_columns()
    queries.append(
        select(
            kind.label("kind"),
            target.label("target"),
            CollectionItem.created_at.label("saved_at"),
            case((Collection.system_role.is_(None), uuid_text(Collection.id)), else_="").label(
                "collection_id"
            ),
        )
        .join(Collection, Collection.id == CollectionItem.collection_id)
        .where(Collection.user_id == user_id)
    )
    queries.append(
        select(
            literal("post").label("kind"),
            uuid_text(Reaction.post_id).label("target"),
            Reaction.created_at.label("saved_at"),
            literal("").label("collection_id"),
        ).where(Reaction.user_id == user_id, Reaction.kind == "save")
    )
    return union_all(*queries).subquery()


async def lock_account(
    session: AsyncSession, user: User, expected_user_id: UUID | None = None
) -> None:
    if expected_user_id is not None and expected_user_id != user.id:
        raise failure("saved_account_changed", 409)
    # Unified saved/collection writes share this first lock, including first-ever inbox creation.
    active = await session.scalar(
        select(User.id)
        .where(User.id == user.id, User.is_active.is_(True), User.deleted_at.is_(None))
        # NO KEY UPDATE serializes these writers without blocking the KEY SHARE
        # foreign-key checks made by legacy favorite INSERTs.
        .with_for_update(key_share=True)
    )
    if active is None:
        raise failure("authentication_required", 401)


async def states(session: AsyncSession, user: User, keys: list[str]) -> dict[str, Any]:
    pairs = list(dict.fromkeys(parse_key(key) for key in keys))
    if len(keys) > 100:
        raise failure("validation_error", 422)
    source = references(user.id)
    rows = (
        (
            await session.execute(
                select(source.c.kind, source.c.target, source.c.collection_id)
                .where(sql_tuple(source.c.kind, source.c.target).in_(pairs))
                .distinct()
            )
        ).all()
        if pairs
        else []
    )
    found: dict[tuple[str, str], set[str]] = {}
    for kind, target, collection_id in rows:
        memberships = found.setdefault((kind, target), set())
        if collection_id:
            memberships.add(str(UUID(collection_id)))
    return {
        "items": [
            {
                "key": key_for(kind, target),
                "saved": (kind, target) in found,
                "collection_ids": sorted(found.get((kind, target), set())),
            }
            for kind, target in pairs
        ]
    }


# Discovery displays a public count for these kinds only; "restaurant" is not one of them.
COUNTED_KINDS = {"hotspot", "food", "merchant", "service", "guide", "post"}
COUNT_BATCH = 200


def stored_kinds(kind: str) -> set[str]:
    """Every ``CollectionItem.kind`` that ``canonical`` folds into ``kind``."""
    return {kind} | {alias for alias, name in ALIASES.items() if name == kind}


def stored_targets(kind: str, target: str) -> set[str]:
    """Every spelling of ``target`` a collection row may hold.

    ``collection_columns`` normalises on read because older rows were written before
    ``public_id`` was applied. Matching those spellings on the raw column instead keeps
    the (kind, target) index usable; everything this codebase writes is the dashed
    lowercase form, and the hex and upper-case variants cover the legacy writers.
    """
    if kind not in UUID_KINDS:
        return {target}
    try:
        value = UUID(target)
    except ValueError:
        return {target, target.lower(), target.upper()}
    return {value.hex, value.hex.upper(), str(value), str(value).upper()}


async def collect_savers(
    session: AsyncSession,
    pairs: list[tuple[str, str]],
    savers: dict[tuple[str, str], set[UUID]],
) -> None:
    """Add the accounts that saved each pair, from all three places a save can land."""
    by_kind: dict[str, list[str]] = {}
    for kind, target in pairs:
        by_kind.setdefault(kind, []).append(target)
    for kind, targets in by_kind.items():
        model_column = FAVORITES.get(kind)
        if model_column is None:
            continue
        model, column = model_column
        identifiers: dict[UUID, tuple[str, str]] = {}
        for target in targets:
            try:
                identifiers[UUID(target)] = (kind, target)
            except ValueError:
                continue
        if not identifiers:
            continue
        rows = (
            await session.execute(
                select(model.user_id, column).where(column.in_(list(identifiers)))
            )
        ).all()
        for user_id, identifier in rows:
            pair = identifiers.get(identifier)
            if pair is not None:
                savers.setdefault(pair, set()).add(user_id)
    posts: dict[UUID, tuple[str, str]] = {}
    for target in by_kind.get("post", []):
        try:
            posts[UUID(target)] = ("post", target)
        except ValueError:
            continue
    if posts:
        rows = (
            await session.execute(
                select(Reaction.user_id, Reaction.post_id).where(
                    Reaction.kind == "save", Reaction.post_id.in_(list(posts))
                )
            )
        ).all()
        for user_id, post_id in rows:
            pair = posts.get(post_id)
            if pair is not None:
                savers.setdefault(pair, set()).add(user_id)
    kinds: set[str] = set()
    targets_wanted: set[str] = set()
    for kind, target in pairs:
        kinds |= stored_kinds(kind)
        targets_wanted |= stored_targets(kind, target)
    if not targets_wanted:
        return
    wanted = set(pairs)
    rows = (
        await session.execute(
            select(Collection.user_id, CollectionItem.kind, CollectionItem.target)
            .join(Collection, Collection.id == CollectionItem.collection_id)
            .where(
                CollectionItem.kind.in_(sorted(kinds)),
                CollectionItem.target.in_(sorted(targets_wanted)),
            )
        )
    ).all()
    for user_id, kind, target in rows:
        try:
            pair = canonical(kind, target)
        except AppError:
            continue
        if pair in wanted:
            savers.setdefault(pair, set()).add(user_id)


async def saved_counts(session: AsyncSession, keys: list[str]) -> dict[str, int]:
    """How many distinct accounts saved each reference, keyed by the caller's own strings.

    All three storage sites are read because ``ensure_base`` writes to exactly one of
    them per kind: typed favorites for places and products, ``Reaction`` for posts, and
    the collection inbox for guides, which have no typed table. Organizing a reference
    into a named list adds a second row for the same account, so the accounts are folded
    into a set rather than counted, matching ``COUNT(DISTINCT user_id)``.
    """
    wanted: dict[tuple[str, str], list[str]] = {}
    for key in keys:
        try:
            pair = parse_key(key)
        except AppError:
            continue
        if pair[0] in COUNTED_KINDS:
            wanted.setdefault(pair, []).append(key)
    savers: dict[tuple[str, str], set[UUID]] = {}
    pairs = list(wanted)
    for start in range(0, len(pairs), COUNT_BATCH):
        await collect_savers(session, pairs[start : start + COUNT_BATCH], savers)
    return {key: len(savers.get(pair, set())) for pair, group in wanted.items() for key in group}


async def insert_unique_reference(
    session: AsyncSession, model: Any, values: dict[str, Any], columns: list[str]
) -> bool:
    # Legacy favorite endpoints can write without the new account lock. The
    # database unique key makes our writer safe even when those requests race.
    insert = sqlite_insert if session.get_bind().dialect.name == "sqlite" else pg_insert
    statement = (
        insert(model)
        .values(**values)
        .on_conflict_do_nothing(index_elements=columns)
        .returning(model.id)
    )
    return await session.scalar(statement) is not None


async def ensure_base(
    session: AsyncSession,
    user: User,
    kind: str,
    target: str,
    *,
    saved_at: datetime | None = None,
) -> bool:
    """Preserve a previously owned reference, or a caller-validated new public reference."""
    kind, target = canonical(kind, target)
    if kind == "post":
        try:
            post_id = UUID(target)
        except ValueError:
            post_id = None
        if post_id is not None and await session.scalar(select(Post.id).where(Post.id == post_id)):
            existing_save = await session.scalar(
                select(Reaction.id).where(
                    Reaction.user_id == user.id,
                    Reaction.post_id == post_id,
                    Reaction.kind == "save",
                )
            )
            if existing_save is not None:
                return False
            return await insert_unique_reference(
                session,
                Reaction,
                {
                    "user_id": user.id,
                    "post_id": post_id,
                    "kind": "save",
                    **({"created_at": saved_at} if saved_at else {}),
                },
                ["user_id", "post_id", "kind"],
            )
    model_column = FAVORITES.get(kind)
    identifier: UUID | None = None
    if model_column:
        if kind == "restaurant":
            identifier = await session.scalar(
                select(RestaurantPlace.id).where(RestaurantPlace.google_place_id == target)
            )
        else:
            try:
                identifier = UUID(target)
            except ValueError:
                pass
        # Legacy unavailable/invalid references cannot acquire invalid typed foreign keys.
        if identifier is not None:
            model, column = model_column
            foreign_table = next(iter(column.property.columns[0].foreign_keys)).column.table
            present = await session.scalar(
                select(foreign_table.c.id).where(foreign_table.c.id == identifier)
            )
            if present is not None:
                existing = await session.scalar(
                    select(model.id).where(model.user_id == user.id, column == identifier)
                )
                if existing is not None:
                    return False
                values: dict[str, Any] = {"user_id": user.id, column.key: identifier}
                if saved_at is not None:
                    values["created_at"] = saved_at
                return await insert_unique_reference(
                    session, model, values, ["user_id", column.key]
                )
    inbox = await session.scalar(
        select(Collection).where(Collection.user_id == user.id, Collection.system_role == "inbox")
    )
    if inbox is None:
        inbox = Collection(user_id=user.id, name="Saved references", system_role="inbox")
        session.add(inbox)
        await session.flush()
    column_kind, column_target = collection_columns()
    existing = await session.scalar(
        select(CollectionItem.id).where(
            CollectionItem.collection_id == inbox.id, column_kind == kind, column_target == target
        )
    )
    if existing is not None:
        return False
    count = await session.scalar(
        select(func.count())
        .select_from(CollectionItem)
        .where(CollectionItem.collection_id == inbox.id)
    )
    if (count or 0) >= MAX_INBOX_ITEMS:
        raise failure("saved_item_limit", 403)
    session.add(
        CollectionItem(
            collection_id=inbox.id,
            kind=kind,
            target=public_id(kind, target),
            **({"created_at": saved_at} if saved_at else {}),
        )
    )
    await session.flush()
    return True


async def validate_public(session: AsyncSession, user: User, kind: str, target: str) -> None:
    from app.saved.router import _food, _hotspot, _merchant, _restaurant

    if kind in {"hotspot", "food", "merchant", "restaurant"}:
        await {
            "hotspot": _hotspot,
            "food": _food,
            "merchant": _merchant,
            "restaurant": _restaurant,
        }[kind](session, public_id(kind, target))
    elif kind == "service":
        from app.travel_services.service import catalog_config, product_enabled

        product = await session.get(TravelServiceProduct, UUID(target))
        config, _ = await catalog_config(session)
        if (
            not product
            or not config.public_enabled
            or product.status != "approved"
            or not product_enabled(config, product)
        ):
            raise failure()
        if product.kind == "hotel" and not fresh_product(product):
            raise failure()
    elif kind in {"guide", "post"}:
        from app.discovery.service import resolve_discovery_items

        if not await resolve_discovery_items(session, [key_for(kind, target)], user, "zh-TW"):
            raise failure()
    else:
        raise failure()


async def save_reference(
    session: AsyncSession,
    user: User,
    kind: str,
    target: str,
    expected_user_id: UUID | None = None,
) -> dict[str, Any]:
    input_kind = kind
    kind, target = canonical(kind, target, strict=True)
    await lock_account(session, user, expected_user_id)
    await rate(session, user)
    await validate_public(session, user, kind, target)
    if input_kind == "hotel":
        product = await session.get(TravelServiceProduct, UUID(target))
        if product is None or product.kind != "hotel":
            raise failure()
    before = (await states(session, user, [key_for(kind, target)]))["items"][0]
    created = await ensure_base(session, user, kind, target) and not before["saved"]
    if created:
        from app.analytics.service import record_event

        await record_event(
            session,
            "content_saved",
            path="/explore/collections",
            user_id=user.id,
            properties={"kind": kind},
        )
    return {
        "type": input_kind,
        "id": public_id(kind, target),
        "key": key_for(kind, target),
        "saved": True,
        "created": created,
        "collection_ids": before["collection_ids"],
    }


async def unsave_reference(
    session: AsyncSession,
    user: User,
    kind: str,
    target: str,
    expected_user_id: UUID | None = None,
) -> None:
    kind, target = canonical(kind, target)
    await lock_account(session, user, expected_user_id)
    await rate(session, user)
    if kind in FAVORITES:
        model, column = FAVORITES[kind]
        if kind == "restaurant":
            condition = column.in_(
                select(RestaurantPlace.id).where(RestaurantPlace.google_place_id == target)
            )
        else:
            condition = uuid_text(column) == target
        await session.execute(delete(model).where(model.user_id == user.id, condition))
    column_kind, column_target = collection_columns()
    await session.execute(
        delete(CollectionItem).where(
            CollectionItem.collection_id.in_(
                select(Collection.id).where(Collection.user_id == user.id)
            ),
            column_kind == kind,
            column_target == target,
        )
    )
    if kind == "post":
        await session.execute(
            delete(Reaction).where(
                Reaction.user_id == user.id,
                Reaction.kind == "save",
                uuid_text(Reaction.post_id) == target,
            )
        )


def filters_for(source: Any, item_type: str, destination: str) -> list[Any]:
    filters: list[Any] = []
    kind = ALIASES.get(item_type, item_type)
    if item_type != "all":
        filters.append(source.c.kind == kind)
    if item_type == "hotel":
        filters.append(
            exists(
                select(TravelServiceProduct.id).where(
                    uuid_text(TravelServiceProduct.id) == source.c.target,
                    TravelServiceProduct.kind == "hotel",
                )
            )
        )
    if item_type in {"article", "video"}:
        filters.append(
            exists(
                select(HotspotGuide.id).where(
                    uuid_text(HotspotGuide.id) == source.c.target,
                    HotspotGuide.content_type == item_type,
                )
            )
        )
    if item_type == "itinerary":
        filters.append(
            exists(
                select(Post.id)
                .join(PostRevision, PostRevision.id == Post.published_revision_id)
                .where(
                    uuid_text(Post.id) == source.c.target,
                    PostRevision.itinerary.is_not(None),
                    cast(PostRevision.itinerary, String) != "null",
                )
            )
        )
    if destination:
        destinations = catalog_destination_ids([destination_id(destination)])
        conditions = []
        for source_kind, model, column in (
            ("hotspot", TravelHotspot, TravelHotspot.destination_id),
            ("merchant", FoodMerchant, FoodMerchant.destination_id),
            ("service", TravelServiceProduct, TravelServiceProduct.destination_id),
        ):
            conditions.append(
                and_(
                    source.c.kind == source_kind,
                    exists(
                        select(model.id).where(
                            uuid_text(model.id) == source.c.target, column.in_(destinations)
                        )
                    ),
                )
            )
        conditions.append(
            and_(
                source.c.kind == "food",
                exists(
                    select(FoodDestination.id).where(
                        uuid_text(FoodDestination.food_id) == source.c.target,
                        FoodDestination.destination_id.in_(destinations),
                    )
                ),
            )
        )
        conditions.append(
            and_(
                source.c.kind == "guide",
                exists(
                    select(HotspotGuide.id)
                    .join(TravelHotspot, TravelHotspot.id == HotspotGuide.hotspot_id)
                    .where(
                        uuid_text(HotspotGuide.id) == source.c.target,
                        TravelHotspot.destination_id.in_(destinations),
                    )
                ),
            )
        )
        conditions.append(
            and_(
                source.c.kind == "post",
                exists(
                    select(Post.id)
                    .join(PostRevision, PostRevision.id == Post.published_revision_id)
                    .where(
                        uuid_text(Post.id) == source.c.target,
                        func.lower(PostRevision.destination).in_(destinations),
                    )
                ),
            )
        )
        filters.append(or_(*conditions))
    return filters


def cursor_context(user_id: UUID, item_type: str, destination: str, collection: UUID | None) -> str:
    return hashlib.sha256(f"{user_id}|{item_type}|{destination}|{collection}".encode()).hexdigest()


async def project_rows(
    session: AsyncSession,
    user: User,
    rows: list[Any],
    locale: Locale,
) -> list[dict[str, Any]]:
    from app.discovery.service import resolve_discovery_items
    from app.discovery.sources import catalog_items
    from app.travel_services.service import catalog_config, product_enabled

    identifiers: dict[str, list[UUID]] = {}
    for row in rows:
        kind = "hotel" if row.kind == "service" else row.kind
        if kind not in {"hotspot", "food", "merchant", "hotel"}:
            continue
        try:
            identifiers.setdefault(kind, []).append(UUID(row.target))
        except ValueError:
            pass
    resolved = {
        item.id: item for item in await catalog_items(session, locale, identifiers=identifiers)
    }
    content_keys = []
    for row in rows:
        if row.kind in {"guide", "post"}:
            try:
                content_keys.append(key_for(row.kind, str(UUID(row.target))))
            except ValueError:
                pass
    resolved.update(
        {
            item.id: item
            for item in await resolve_discovery_items(session, content_keys, user, locale)
        }
    )
    status_rows = (await states(session, user, [key_for(row.kind, row.target) for row in rows]))[
        "items"
    ]
    memberships = {row["key"]: row["collection_ids"] for row in status_rows}
    products = {
        UUID(row.target)
        for row in rows
        if row.kind == "service"
        and len(row.target) == 32
        and all(char in "0123456789abcdef" for char in row.target)
    }
    product_rows = (
        {
            product.id: product
            for product in (
                await session.scalars(
                    select(TravelServiceProduct).where(TravelServiceProduct.id.in_(products))
                )
            )
        }
        if products
        else {}
    )
    config = (await catalog_config(session))[0] if products else None
    restaurants = {
        row.google_place_id: row
        for row in (
            await session.scalars(
                select(RestaurantPlace).where(
                    RestaurantPlace.google_place_id.in_(
                        [r.target for r in rows if r.kind == "restaurant"]
                    ),
                    RestaurantPlace.is_suppressed.is_(False),
                    RestaurantPlace.identity_status.not_in(("moved", "not_found")),
                )
            )
        )
    }
    output = []
    for row in rows:
        key = key_for(row.kind, row.target)
        value: dict[str, Any] = {
            "key": key,
            "type": row.kind,
            "id": public_id(row.kind, row.target),
            "saved_at": row.saved_at.isoformat(),
            "unavailable": True,
            "collection_ids": memberships[key],
        }
        lookup = key_for("hotel" if row.kind == "service" else row.kind, row.target)
        if row.kind == "service":
            lookup = "hotel:" + public_id(row.kind, row.target)
        item = resolved.get(lookup)
        if item is not None:
            value.update(
                unavailable=False,
                discovery=item.model_dump(mode="json"),
                title=item.title,
                href=item.href,
            )
        elif row.kind == "service":
            try:
                product = product_rows.get(UUID(row.target))
            except ValueError:
                product = None
            if (
                product is not None
                and product.kind != "hotel"
                and product.status == "approved"
                and config is not None
                and config.public_enabled
                and product_enabled(config, product)
            ):
                value.update(
                    unavailable=False,
                    title=product.names_json.get(locale) or product.title,
                    subtitle=product.destination_id,
                    href=f"/destinations/{product.destination_id}/services?product={product.id}",
                )
        elif row.kind == "restaurant" and row.target in restaurants:
            value.update(
                unavailable=False,
                title="Google Maps",
                subtitle="",
                map_links=[
                    {"url": restaurants[row.target].generated_maps_url, "label": "Google Maps"}
                ],
            )
        output.append(value)
    return output


async def all_saved(
    session: AsyncSession,
    user: User,
    locale: Locale,
    *,
    item_type: str = "all",
    destination: str = "",
    collection: UUID | None = None,
    cursor: str | None = None,
    limit: int = 24,
) -> dict[str, Any]:
    from app.community.collections import active_account, owned_collection

    await active_account(session, user)
    if collection:
        await owned_collection(session, user, collection)
    source = references(user.id)
    filters = filters_for(source, item_type, destination)
    if collection:
        filters.append(source.c.collection_id == collection.hex)
    grouped = (
        select(source.c.kind, source.c.target, func.max(source.c.saved_at).label("saved_at"))
        .where(*filters)
        .group_by(source.c.kind, source.c.target)
        .subquery()
    )
    total = await session.scalar(select(func.count()).select_from(grouped)) or 0
    statement = select(grouped).order_by(
        grouped.c.saved_at.desc(), grouped.c.kind, grouped.c.target
    )
    context = cursor_context(user.id, item_type, destination, collection)
    if cursor:
        try:
            payload = json.loads(base64.urlsafe_b64decode(cursor.encode()))
            if payload["context"] != context:
                raise ValueError
            moment = datetime.fromisoformat(payload["at"])
            if moment.tzinfo is None:
                moment = moment.replace(tzinfo=UTC)
            kind, target = payload["kind"], payload["target"]
            if not isinstance(kind, str) or not isinstance(target, str):
                raise ValueError
        except (ValueError, KeyError, TypeError, UnicodeError) as exc:
            raise failure("saved_cursor_invalid", 422) from exc
        statement = statement.where(
            or_(
                grouped.c.saved_at < moment,
                and_(grouped.c.saved_at == moment, grouped.c.kind > kind),
                and_(
                    grouped.c.saved_at == moment, grouped.c.kind == kind, grouped.c.target > target
                ),
            )
        )
    rows = list((await session.execute(statement.limit(limit + 1))).all())
    page = rows[:limit]
    next_cursor = None
    if len(rows) > limit:
        last = page[-1]
        next_cursor = base64.urlsafe_b64encode(
            json.dumps(
                {
                    "context": context,
                    "at": last.saved_at.isoformat(),
                    "kind": last.kind,
                    "target": last.target,
                }
            ).encode()
        ).decode()
    return {
        "items": await project_rows(session, user, page, locale),
        "total": total,
        "has_more": next_cursor is not None,
        "next_cursor": next_cursor,
    }
