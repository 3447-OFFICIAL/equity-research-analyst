from dataclasses import dataclass


@dataclass(frozen=True)
class DCFResult:
    intrinsic_value: float
    terminal_value: float
    margin_of_safety: float | None


def calculate_dcf(
    starting_fcf: float,
    growth_rate: float,
    discount_rate: float,
    terminal_growth_rate: float,
    periods: int = 5,
    market_price: float | None = None,
) -> DCFResult:
    if discount_rate <= terminal_growth_rate:
        raise ValueError("discount_rate must be greater than terminal_growth_rate")
    if periods <= 0:
        raise ValueError("periods must be positive")

    projected_fcfs = [starting_fcf * ((1 + growth_rate) ** year) for year in range(1, periods + 1)]
    present_value_fcfs = sum(fcf / ((1 + discount_rate) ** year) for year, fcf in enumerate(projected_fcfs, start=1))
    terminal_value = projected_fcfs[-1] * (1 + terminal_growth_rate) / (discount_rate - terminal_growth_rate)
    present_value_terminal = terminal_value / ((1 + discount_rate) ** periods)
    intrinsic_value = present_value_fcfs + present_value_terminal
    margin_of_safety = None
    if market_price is not None and intrinsic_value != 0:
        margin_of_safety = (intrinsic_value - market_price) / intrinsic_value
    return DCFResult(
        intrinsic_value=intrinsic_value,
        terminal_value=terminal_value,
        margin_of_safety=margin_of_safety,
    )
