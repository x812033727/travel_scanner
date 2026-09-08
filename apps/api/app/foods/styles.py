"""Style reviews are editorial judgements, never map/publication authority."""

from datetime import UTC, date, datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, model_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, FoodMerchant, FoodMerchantStyle, User
from app.problems import AppError
from app.restaurants.editorial import validate_editorial_url

MerchantStyle = Literal["instagrammable", "artsy"]
StyleStatus = Literal["pending", "approved", "rejected"]
STYLE_NAMES = {
    "instagrammable": {
        "zh-TW": "網美店",
        "zh-CN": "网美店",
        "en": "Photogenic shops",
        "ja": "写真映えするお店",
        "ko": "사진 찍기 좋은 가게",
    },
    "artsy": {
        "zh-TW": "文青店",
        "zh-CN": "文艺店",
        "en": "Arts & culture shops",
        "ja": "アート・カルチャーのお店",
        "ko": "예술·문화 감성 가게",
    },
}


class StyleEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    style: MerchantStyle
    evidence_url: str = Field(min_length=1, max_length=2048)
    evidence_title: str = Field(min_length=1, max_length=255)
    rationale: str = Field(min_length=10, max_length=1000)
    checked_on: date

    @model_validator(mode="after")
    def validate_evidence(self) -> "StyleEvidence":
        validate_editorial_url(self.evidence_url)
        # Calendar dates are supplied in the operator's local timezone.
        if self.checked_on > date.fromordinal(datetime.now(UTC).date().toordinal() + 1):
            raise ValueError("Evidence cannot be checked in the future")
        return self


class StyleReview(StyleEvidence):
    status: StyleStatus


class StyleReviewRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    reason: str = Field(min_length=3, max_length=500)
    expected_updated_at: AwareDatetime | None = None
    review: StyleReview


def style_filter(style: str | None, status: str = "approved") -> Any | None:
    if not style:
        return None
    return FoodMerchant.id.in_(
        select(FoodMerchantStyle.merchant_id).where(
            FoodMerchantStyle.style == style, FoodMerchantStyle.status == status
        )
    )


def review_view(row: FoodMerchantStyle) -> dict[str, Any]:
    return {
        "style": row.style,
        "status": row.status,
        "evidence_url": row.evidence_url,
        "evidence_title": row.evidence_title,
        "rationale": row.rationale,
        "checked_on": row.checked_on.isoformat(),
        "reviewed_at": row.reviewed_at.replace(tzinfo=UTC).isoformat() if row.reviewed_at else None,
        "updated_at": row.updated_at.replace(tzinfo=UTC).isoformat(),
    }


async def reviews(session: AsyncSession, merchant_id: UUID) -> list[dict[str, Any]]:
    return [
        review_view(row)
        for row in (
            await session.scalars(
                select(FoodMerchantStyle)
                .where(FoodMerchantStyle.merchant_id == merchant_id)
                .order_by(FoodMerchantStyle.style)
            )
        ).all()
    ]


async def review_style(
    session: AsyncSession, merchant_id: UUID, payload: StyleReviewRequest, user: User
) -> dict[str, Any]:
    # Serialize creation as well as edits, without locking an absent child row.
    merchant = await session.scalar(
        select(FoodMerchant).where(FoodMerchant.id == merchant_id).with_for_update()
    )
    if merchant is None:
        raise AppError(404, "food_merchant_not_found", "找不到店家")
    row = await session.scalar(
        select(FoodMerchantStyle)
        .where(
            FoodMerchantStyle.merchant_id == merchant_id,
            FoodMerchantStyle.style == payload.review.style,
        )
        .execution_options(populate_existing=True)
    )
    expected = payload.expected_updated_at
    if (row is None) != (expected is None) or (
        row is not None
        and expected is not None
        and row.updated_at.replace(tzinfo=UTC) != expected.astimezone(UTC)
    ):
        raise AppError(409, "merchant_style_changed", "風格資料已變更，請重新載入")
    before = review_view(row) if row else None
    values = payload.review.model_dump()
    if row is None:
        row = FoodMerchantStyle(merchant_id=merchant_id, **values)
        session.add(row)
    else:
        for field, value in values.items():
            setattr(row, field, value)
    now = datetime.now(UTC)
    row.updated_at = now
    row.reviewed_at = now if row.status != "pending" else None
    row.reviewed_by_user_id = user.id if row.status != "pending" else None
    await session.flush()
    after = review_view(row)
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="food_merchant_style_reviewed",
            target=f"food_merchant:{merchant_id}:{row.style}",
            metadata_json={"reason": payload.reason, "before": before, "after": after},
        )
    )
    await session.commit()
    return after
