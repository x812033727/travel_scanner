from decimal import Decimal


def estimate(input_tokens: int, output_tokens: int, input_usd: str, output_usd: str) -> Decimal:
    """Rates are USD per million tokens; pass the current model's pricing."""
    if min(input_tokens, output_tokens) < 0:
        raise ValueError("token 數不能是負數")
    return (Decimal(input_tokens) * Decimal(input_usd) + Decimal(output_tokens) * Decimal(output_usd)) / Decimal(1_000_000)


if __name__ == "__main__":
    # 2026-09-14：Gemini 3.8 Flash Standard，未含其他工具或儲存費。
    print(estimate(2000, 500, "0.75", "3.75"))
