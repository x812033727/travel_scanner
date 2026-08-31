from decimal import Decimal

from app.alerts.policy import evaluate_price_trigger


def test_target_notifies_only_on_crossing_and_rearms_above_target() -> None:
    reached = evaluate_price_trigger(
        target_price=Decimal("100"),
        baseline_price=Decimal("120"),
        last_notified_price=None,
        armed=True,
        observed_price=Decimal("99"),
    )
    assert reached.should_notify is True
    assert reached.next_armed is False
    assert reached.event_type == "target_reached"
    repeated = evaluate_price_trigger(
        target_price=Decimal("100"),
        baseline_price=Decimal("120"),
        last_notified_price=Decimal("99"),
        armed=reached.next_armed,
        observed_price=Decimal("95"),
    )
    assert repeated.should_notify is False
    assert repeated.next_armed is False
    reset = evaluate_price_trigger(
        target_price=Decimal("100"),
        baseline_price=Decimal("120"),
        last_notified_price=Decimal("99"),
        armed=False,
        observed_price=Decimal("105"),
    )
    assert reset.next_armed is True


def test_no_target_notifies_only_for_new_lows() -> None:
    first = evaluate_price_trigger(
        target_price=None,
        baseline_price=Decimal("100"),
        last_notified_price=None,
        armed=True,
        observed_price=Decimal("90"),
    )
    assert first.should_notify is True
    unchanged = evaluate_price_trigger(
        target_price=None,
        baseline_price=Decimal("100"),
        last_notified_price=Decimal("90"),
        armed=True,
        observed_price=Decimal("95"),
    )
    assert unchanged.should_notify is False
    lower = evaluate_price_trigger(
        target_price=None,
        baseline_price=Decimal("100"),
        last_notified_price=Decimal("90"),
        armed=True,
        observed_price=Decimal("89"),
    )
    assert lower.should_notify is True
