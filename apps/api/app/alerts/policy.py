from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class PriceTriggerDecision:
    should_notify: bool
    next_armed: bool
    event_type: str | None


def evaluate_price_trigger(
    *,
    target_price: Decimal | None,
    baseline_price: Decimal | None,
    last_notified_price: Decimal | None,
    armed: bool,
    observed_price: Decimal,
) -> PriceTriggerDecision:
    if target_price is not None:
        if observed_price > target_price:
            return PriceTriggerDecision(False, True, None)
        if armed:
            return PriceTriggerDecision(True, False, "target_reached")
        return PriceTriggerDecision(False, False, None)
    reference = last_notified_price if last_notified_price is not None else baseline_price
    if reference is not None and observed_price < reference:
        return PriceTriggerDecision(True, True, "new_low")
    return PriceTriggerDecision(False, True, None)
