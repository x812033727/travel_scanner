import argparse
import asyncio

from sqlalchemy import select

from app.db import SessionFactory
from app.models import Plan, Subscription, UsageLedger, User
from app.usage.service import seed_plans


async def set_plan(email: str, plan_code: str) -> None:
    async with SessionFactory() as session:
        await seed_plans(session)
        user = await session.scalar(select(User).where(User.email == email.lower()))
        plan = await session.scalar(select(Plan).where(Plan.code == plan_code.upper()))
        if user is None or plan is None:
            raise SystemExit("User or plan was not found")
        subscription = await session.scalar(
            select(Subscription).where(Subscription.user_id == user.id).with_for_update()
        )
        if subscription is None:
            raise SystemExit("Subscription was not found")
        difference = plan.monthly_credits - subscription.credit_balance
        subscription.plan_id = plan.id
        subscription.credit_balance = plan.monthly_credits
        session.add(
            UsageLedger(
                user_id=user.id,
                subscription_id=subscription.id,
                entry_type="plan_adjustment",
                amount=difference,
                balance_after=subscription.credit_balance,
                reference=f"set-plan:{plan.code}:{subscription.period_start}",
                metadata_json={"plan": plan.code, "source": "cli"},
            )
        )
        await session.commit()
        print(f"{email} is now on {plan.code} with {plan.monthly_credits} credits")


def main() -> None:
    parser = argparse.ArgumentParser(description="Travel Scanner development utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)
    command = subparsers.add_parser("set-plan")
    command.add_argument("--email", required=True)
    command.add_argument("--plan", choices=["FREE", "PRO"], required=True)
    args = parser.parse_args()
    if args.command == "set-plan":
        asyncio.run(set_plan(args.email, args.plan))


if __name__ == "__main__":
    main()
