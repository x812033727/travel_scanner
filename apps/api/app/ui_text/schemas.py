from datetime import datetime

from pydantic import BaseModel, Field

from app.admin.schemas import AdminAuditView
from app.i18n import Locale

# The namespaces of apps/web/i18n/request.ts minus ``legacy`` (see UI_TEXT_LOCKED_NAMESPACES).
# tools/check-i18n.mjs compares this tuple with the catalog directory, so a namespace added
# on the web side fails CI until it is listed here as well.
UI_TEXT_NAMESPACES: tuple[str, ...] = (
    "account",
    "admin",
    "alerts",
    "auth",
    "availability",
    "common",
    "errors",
    "foodAdmin",
    "foods",
    "hotspotAdmin",
    "hotspotThemes",
    "hotspots",
    "metadata",
    "navigation",
    "newTrip",
    "pricing",
    "restaurants",
    "search",
    "stayAreas",
    "trips",
    "usage",
)
# legacy-ui-localizer.tsx rewrites DOM text by literal zh-TW string, so an override there
# would change API data on screen. Refused here, in the database and in the web loader.
UI_TEXT_LOCKED_NAMESPACES: tuple[str, ...] = ("legacy",)

UI_TEXT_VALUE_MAX_LENGTH = 2000
# The longest catalog default today is 335 characters.
UI_TEXT_DEFAULT_MAX_LENGTH = 4000
UI_TEXT_KEY_MAX_LENGTH = 200
UI_TEXT_BATCH_LIMIT = 100
NAMESPACE_PATTERN = r"^[A-Za-z][A-Za-z0-9]*$"
# Dotted path inside a namespace; ``-`` is the only non-word character the catalogs use.
KEY_PATTERN = r"^[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*$"


class UiTextWrite(BaseModel):
    value: str = Field(max_length=UI_TEXT_VALUE_MAX_LENGTH)
    # The API has no copy of the catalogs, so the editor sends the default it is
    # overriding; placeholder parity is checked against it and it is kept as a snapshot.
    default_value: str = Field(max_length=UI_TEXT_DEFAULT_MAX_LENGTH)


class UiTextBatchEntry(BaseModel):
    key: str = Field(pattern=KEY_PATTERN, max_length=UI_TEXT_KEY_MAX_LENGTH)
    # ``None`` restores the catalog default; a string is validated like a single PUT.
    value: str | None = Field(default=None, max_length=UI_TEXT_VALUE_MAX_LENGTH)
    default_value: str | None = Field(default=None, max_length=UI_TEXT_DEFAULT_MAX_LENGTH)


class UiTextBatchWrite(BaseModel):
    locale: Locale
    namespace: str = Field(pattern=NAMESPACE_PATTERN, max_length=64)
    entries: list[UiTextBatchEntry] = Field(min_length=1, max_length=UI_TEXT_BATCH_LIMIT)


class UiTextEntryView(BaseModel):
    namespace: str
    key: str
    locale: str
    value: str
    default_snapshot: str | None
    updated_at: datetime
    updated_by_email: str | None


class UiTextSnapshot(BaseModel):
    locale: str
    namespace: str | None
    # Content hash of every override in this locale; it changes on add, update and delete.
    version: str
    namespaces: list[str]
    locked_namespaces: list[str]
    namespace_counts: dict[str, int]
    entries: list[UiTextEntryView]
    audit: list[AdminAuditView]


class PublicUiText(BaseModel):
    locale: str
    version: str
    # Flat "<namespace>.<key>" -> text; namespaces never contain a dot, so the web loader
    # splits at the first one.
    entries: dict[str, str]
