"""No affiliate partner may receive a value derived from who the member is.

Two sites used to build one: `/affiliates/options` and the trip stay-area clickout,
both `uuid5` over `user.id`. Only Klook was exempted, and on the stay path that
exemption never fired at all because klook is absent from STAY_PARTNER_ORDER --
agoda, booking, trip_com and travelpayouts each received a value stable per
(member, trip).

The guarantee now rests on two things, and both are tested here: every egress calls
`safe_sub_id`, and no new derivation site appears. The second is what the source
scan is for -- a reviewer will not notice a `uuid5` in a file they are not reading.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest.mock import AsyncMock
from uuid import NAMESPACE_URL, uuid4, uuid5

import fakeredis.aioredis
import pytest

from app.affiliates.registry import AFFILIATE_PARTNERS, PARTNERS_BY_CODE
from app.affiliates.service import AffiliateContext, resolve_partner_target
from app.affiliates.sub_id import MAX_SUB_ID, SUB_ID_RE, coarse_sub_id, safe_sub_id
from app.config import Settings

API_ROOT = Path(__file__).resolve().parents[1]

MEMBER_DERIVED = uuid5(NAMESPACE_URL, "travel-scanner:affiliate:a-real-user-id").hex


class TestCoarseSubId:
    def test_drops_empty_segments_rather_than_rendering_them(self) -> None:
        """A click with no resolved destination must not become `aff_hotel__zh-TW`,
        and the no-destination spelling has to stay byte-identical to the label this
        repository already sent to Klook, or existing partner reporting splits."""
        assert coarse_sub_id("aff", "hotel", None, "zh-TW") == "aff_hotel_zh-TW"
        assert coarse_sub_id("aff", "hotel", "tokyo", "zh-TW") == "aff_hotel_tokyo_zh-TW"
        assert coarse_sub_id("svc", "tour", "osaka", "en", "trip") == "svc_tour_osaka_en_trip"

    def test_everything_it_builds_passes_the_gate(self) -> None:
        for destination in (None, "tokyo", "da-nang", "ho-chi-minh"):
            for locale in ("en", "ja", "ko", "zh-TW", "zh-CN"):
                value = coarse_sub_id("aff", "hotel", destination, locale)
                assert safe_sub_id(value, rebuild="aff_x_en") == value

    def test_caps_at_the_column_width(self) -> None:
        value = coarse_sub_id("aff", "hotel", "x" * 200, "zh-TW")
        assert len(value) <= MAX_SUB_ID
        assert SUB_ID_RE.fullmatch(value)

    def test_strips_characters_that_would_break_the_label(self) -> None:
        value = coarse_sub_id("aff", "hotel", "tokyo/../evil?x=1", "zh-TW")
        assert "/" not in value and "?" not in value and "=" not in value
        assert SUB_ID_RE.fullmatch(value)


class TestSafeSubId:
    @pytest.mark.parametrize(
        "value",
        [
            MEMBER_DERIVED,
            uuid4().hex,
            str(uuid4()),
            "private-user-id",
            "",
            None,
            "aff_hotel_" + uuid4().hex,  # right prefix, identifier smuggled in the tail
        ],
    )
    def test_refuses_anything_that_is_not_one_of_our_labels(self, value: str | None) -> None:
        assert safe_sub_id(value, rebuild="aff_hotel_en") == "aff_hotel_en"

    @pytest.mark.parametrize(
        "value",
        ["aff_hotel_en", "aff_hotel_tokyo_zh-TW", "dst_tour_osaka_ja", "svc_hotel_x_en_trip"],
    )
    def test_passes_real_labels_through_untouched(self, value: str) -> None:
        assert safe_sub_id(value, rebuild="aff_x_en") == value

    def test_never_writes_the_rejected_value_to_the_log(self, caplog) -> None:
        """If the gate is working, the rejected string is the identifier we are trying
        not to disclose. A log line is a second place it would leak to."""
        with caplog.at_level("WARNING"):
            safe_sub_id(MEMBER_DERIVED, rebuild="aff_hotel_en")
        assert caplog.records
        assert MEMBER_DERIVED not in caplog.text


@pytest.mark.parametrize("partner", [p.code for p in AFFILIATE_PARTNERS])
async def test_no_partner_receives_a_member_derived_sub_id(partner: str, monkeypatch) -> None:
    """Parametrised over the registry, so adding a partner adds a case. Every template
    field is set to one that echoes {sub_id}, which is the only way the value can reach
    a URL at all -- a partner whose real template omits it is covered anyway."""
    from app.affiliates.service import TravelpayoutsLinkClient

    definition = PARTNERS_BY_CODE[partner]
    # klook rewrites its target through klook_affiliate_target, which insists on a
    # klook.com host, so that partner needs a host it will accept.
    host = "www.klook.com" if partner == "klook" else "example.test"
    template = f"https://{host}/go?campaign={{sub_id}}&q={{query}}"
    overrides = {definition.template_field: template, definition.allowed_hosts_field: host}
    if partner == "klook":
        overrides |= {"klook_enabled": True, "klook_affiliate_id": "134379"}

    sent: list[str] = []

    async def create(self, target: str, sub_id: str, *, cache_context: str = "legacy") -> str:
        sent.append(sub_id)
        return f"https://example.test/tp?campaign={sub_id}"

    monkeypatch.setattr(TravelpayoutsLinkClient, "create", create)

    target = await resolve_partner_target(
        definition,
        AffiliateContext("hotel", "Tokyo", None, None, MEMBER_DERIVED),
        Settings(**overrides),
        fakeredis.aioredis.FakeRedis(decode_responses=True),
    )
    assert MEMBER_DERIVED not in target, f"{partner} received a member-derived sub_id"
    assert all(MEMBER_DERIVED not in value for value in sent)


async def test_the_other_egress_sanitises_too(monkeypatch) -> None:
    """`resolve_offer_target` reaches the Travelpayouts Links API without ever entering
    `resolve_partner_target`, so the gate there does not cover it."""
    from app.models import TravelServiceBrand, TravelServiceOffer
    from app.travel_services.channels import resolve_offer_target

    sent: list[str] = []

    async def create(self, target: str, sub_id: str, *, cache_context: str = "legacy") -> str:
        sent.append(sub_id)
        # The created link is validated against the brand host too, not just the input.
        return "https://www.tiqets.com/tp"

    from app.affiliates.service import TravelpayoutsLinkClient

    monkeypatch.setattr(TravelpayoutsLinkClient, "create", create)
    # A real registered brand: validate_offer_target checks the target host against it.
    brand = TravelServiceBrand(
        id=uuid4(), channel="travelpayouts", code="tiqets", enabled=True, approval="approved"
    )
    await resolve_offer_target(
        TravelServiceOffer(target_url="https://www.tiqets.com/x"),
        brand,
        Settings(),
        AsyncMock(),
        MEMBER_DERIVED,
        cache_context="fixture",
    )
    assert sent and MEMBER_DERIVED not in sent[0]
    assert SUB_ID_RE.fullmatch(sent[0])


SUB_ID_ASSIGNMENT = re.compile(r"sub_id\s*=\s*(?!.*coarse_sub_id|.*safe_sub_id)(.+)")
IDENTIFIER_SOURCE = re.compile(r"uuid5\(|uuid4\(|user\.id|trip\.id|\.hex\b")


def test_no_new_derivation_site_builds_a_sub_id_from_an_identifier() -> None:
    """The durable half of the guarantee. A future clickout that spells its own
    `sub_id = uuid5(...)` fails here rather than shipping, which is what the two sites
    this test exists for did for months.

    Deliberately narrow: it flags an assignment whose right-hand side mentions an
    identifier source, not every assignment. Re-materialising a stored value from a
    Redis token or a request payload is how the ledger writes work and is not a leak.
    """
    offenders: list[str] = []
    for path in sorted((API_ROOT / "app").rglob("*.py")):
        if path.name == "sub_id.py":
            continue
        for number, line in enumerate(path.read_text("utf-8").splitlines(), start=1):
            match = SUB_ID_ASSIGNMENT.search(line)
            if match and IDENTIFIER_SOURCE.search(match.group(1)):
                offenders.append(f"{path.relative_to(API_ROOT)}:{number}: {line.strip()}")
    assert not offenders, (
        "a sub_id is being built from an identifier instead of app.affiliates.sub_id."
        "coarse_sub_id:\n" + "\n".join(offenders)
    )
